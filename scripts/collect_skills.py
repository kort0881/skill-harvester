from __future__ import annotations

import argparse
import os
import time
from pathlib import Path
from typing import Any

from github import Auth, Github
from github.GithubException import GithubException, RateLimitExceededException

from common import (
    CANDIDATES_DIR,
    RAW_DIR,
    category_from_text,
    extract_title,
    load_json,
    load_yaml,
    now_iso,
    safe_relative_path,
    save_json,
    sha256_text,
    slugify,
    utc_stamp,
)
from integrity import check_bundle

SEEN_FILE = CANDIDATES_DIR / "seen.json"
PENDING_FILE = CANDIDATES_DIR / "pending.json"

# Что из папки навыка вообще имеет смысл качать. Бинарники, картинки и модели
# пропускаем: они не нужны для воспроизведения инструкции, но раздувают репозиторий.
BUNDLE_EXTENSIONS = {
    ".md",
    ".py",
    ".sh",
    ".bash",
    ".js",
    ".mjs",
    ".cjs",
    ".ts",
    ".tsx",
    ".jsx",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
    ".conf",
    ".txt",
    ".csv",
    ".html",
    ".css",
    ".sql",
}


def github_client() -> Github:
    token = os.getenv("GITHUB_TOKEN")
    return Github(auth=Auth.Token(token)) if token else Github()


def load_seen() -> set[str]:
    payload = load_json(SEEN_FILE, {"keys": []})
    return set(payload.get("keys", []))


def append_pending(records: list[dict[str, Any]]) -> None:
    pending = load_json(PENDING_FILE, {"items": []})
    current = pending.get("items", [])
    known = {item["candidate_id"] for item in current}

    for record in records:
        if record["candidate_id"] not in known:
            current.append(record)

    pending["items"] = current
    pending["updated_at"] = now_iso()
    save_json(PENDING_FILE, pending)


def fetch_skill_content(client: Github, repo_full_name: str, path: str) -> str | None:
    try:
        repo = client.get_repo(repo_full_name)
        contents = repo.get_contents(path)
        if isinstance(contents, list):
            return None
        return contents.decoded_content.decode("utf-8", errors="replace")
    except RateLimitExceededException:
        print("GitHub rate limit hit while fetching content. Waiting 60s.")
        time.sleep(60)
        return None
    except GithubException as error:
        print(f"Cannot fetch {repo_full_name}/{path}: {error.status}")
        return None


def fetch_bundle(
    client: Github,
    repo_full_name: str,
    source_dir: str,
    target_dir: Path,
    max_total_bytes: int,
    max_files: int,
    max_file_bytes: int,
) -> dict[str, Any]:
    """Скачивает папку навыка целиком: SKILL.md со скриптами и references.

    Без этого в библиотеку попадали записи, которые ссылаются на `scripts/x.py`,
    а самого скрипта нет — половина прошлого набора была нерабочей.
    """
    stats: dict[str, Any] = {
        "downloaded": [],
        "skipped": [],
        "failed": [],
        "total_bytes": 0,
        "complete": False,
    }
    repo = client.get_repo(repo_full_name)

    def walk(directory: str, relative_prefix: str = "") -> None:
        if len(stats["downloaded"]) >= max_files or stats["total_bytes"] >= max_total_bytes:
            return
        try:
            entries = repo.get_contents(directory)
        except RateLimitExceededException:
            print("GitHub rate limit hit while walking bundle. Stopping.")
            time.sleep(60)
            return
        except GithubException as error:
            stats["failed"].append(f"{directory}: {error.status}")
            return

        if not isinstance(entries, list):
            entries = [entries]

        for entry in entries:
            relative = f"{relative_prefix}{entry.name}"
            if entry.type == "dir":
                walk(entry.path, f"{relative}/")
                continue
            extension = Path(entry.name).suffix.lower()
            if extension not in BUNDLE_EXTENSIONS:
                stats["skipped"].append(relative)
                continue
            if entry.size and entry.size > max_file_bytes:
                stats["skipped"].append(f"{relative} ({entry.size}B)")
                continue
            if stats["total_bytes"] + (entry.size or 0) > max_total_bytes:
                stats["skipped"].append(f"{relative} (budget)")
                continue
            try:
                payload = entry.decoded_content.decode("utf-8", errors="replace")
            except GithubException as error:
                stats["failed"].append(f"{relative}: {error.status}")
                continue
            destination = target_dir / safe_relative_path(relative)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(payload, encoding="utf-8")
            stats["downloaded"].append(relative)
            stats["total_bytes"] += len(payload.encode("utf-8"))

    walk(source_dir)
    stats["complete"] = not stats["failed"]
    return stats


def collect(limit: int) -> dict[str, Any]:
    settings = load_yaml("settings.yml")
    query_config = load_yaml("queries.yml")
    client = github_client()
    seen = load_seen()
    collected: list[dict[str, Any]] = []
    seen_additions: list[str] = []

    min_stars = settings["collection"].get("min_repo_stars", 0)
    max_size = settings["collection"].get("max_skill_file_size_bytes", 180000)
    max_pages = settings["github"].get("max_pages_per_query", 3)
    bundle_limits = settings["collection"].get("bundle", {})
    max_bundle_bytes = int(bundle_limits.get("max_total_bytes", 400000))
    max_bundle_files = int(bundle_limits.get("max_files", 40))
    max_bundle_file_bytes = int(bundle_limits.get("max_file_bytes", 65536))
    per_page = 30

    for source in query_config.get("queries", []):
        if len(collected) >= limit:
            break

        query = source["query"]
        hint = source.get("category_hint", "general")
        print(f"Searching: {query}")

        try:
            results = client.search_code(
                query=query,
                sort=settings["github"].get("search_sort", "indexed"),
                order=settings["github"].get("search_order", "desc"),
            )
        except RateLimitExceededException:
            print("GitHub search rate limit hit. Waiting 60s and skipping this query.")
            time.sleep(60)
            continue
        except GithubException as error:
            print(f"Search failed for '{query}': {error.status} {error.data}")
            continue

        processed_in_query = 0

        try:
            for code_result in results:
                if len(collected) >= limit:
                    break
                if processed_in_query >= max_pages * per_page:
                    break
                processed_in_query += 1

                repository = code_result.repository
                if settings["collection"].get("skip_archived_repositories", True) and repository.archived:
                    continue
                if repository.stargazers_count < min_stars:
                    continue
                if code_result.size and code_result.size > max_size:
                    continue

                source_key = f"{repository.full_name}:{code_result.path}:{code_result.sha}"
                if source_key in seen:
                    continue

                content = fetch_skill_content(client, repository.full_name, code_result.path)
                if not content or len(content.strip()) < 50:
                    continue

                content_hash = sha256_text(content)
                raw_path = (
                    RAW_DIR
                    / slugify(repository.full_name.replace("/", "-"))
                    / safe_relative_path(code_result.path)
                )
                raw_path.parent.mkdir(parents=True, exist_ok=True)
                raw_path.write_text(content, encoding="utf-8")

                source_dir = str(Path(code_result.path).parent).replace("\\", "/")
                source_dir = "" if source_dir == "." else source_dir
                bundle = fetch_bundle(
                    client,
                    repository.full_name,
                    source_dir,
                    raw_path.parent,
                    max_total_bytes=max_bundle_bytes,
                    max_files=max_bundle_files,
                    max_file_bytes=max_bundle_file_bytes,
                )
                # Оценка целостности по тому, что реально лежит на диске рядом с SKILL.md.
                integrity = check_bundle(content, raw_path.parent)

                title = extract_title(content, fallback=Path(code_result.path).parent.name)
                detected_category = category_from_text(
                    f"{title}\n{content[:5000]}",
                    fallback=hint,
                )
                candidate_id = sha256_text(f"{repository.full_name}:{code_result.path}:{content_hash}")[:24]

                record = {
                    "candidate_id": candidate_id,
                    "status": "pending",
                    "discovered_at": now_iso(),
                    "source": {
                        "repository": repository.full_name,
                        "repository_url": repository.html_url,
                        "default_branch": repository.default_branch,
                        "path": code_result.path,
                        "html_url": code_result.html_url,
                        "api_sha": code_result.sha,
                        "repo_stars": repository.stargazers_count,
                        "repo_forks": repository.forks_count,
                        "repo_license": repository.license.name if repository.license else None,
                        "repo_updated_at": repository.updated_at.isoformat()
                        if repository.updated_at
                        else None,
                    },
                    "raw_file": str(raw_path.relative_to(raw_path.parents[2])),
                    "title": title,
                    "category_hint": detected_category,
                    "content_hash": content_hash,
                    "content_characters": len(content),
                    "bundle": {
                        "source_dir": source_dir,
                        "downloaded": bundle["downloaded"],
                        "skipped": bundle["skipped"],
                        "failed": bundle["failed"],
                        "total_bytes": bundle["total_bytes"],
                        "references": integrity["references"],
                        "missing": integrity["missing"],
                        "complete": integrity["complete"],
                    },
                }
                collected.append(record)
                seen_additions.append(source_key)
        except RateLimitExceededException:
            print("GitHub rate limit hit mid-pagination. Stopping this query early.")
            continue

    append_pending(collected)
    seen.update(seen_additions)
    save_json(SEEN_FILE, {"keys": sorted(seen), "updated_at": now_iso()})

    report = {
        "type": "weekly_collection",
        "created_at": now_iso(),
        "collected_count": len(collected),
        "incomplete_count": sum(1 for item in collected if not item["bundle"]["complete"]),
        "items": collected,
    }
    report_path = CANDIDATES_DIR / f"collection-{utc_stamp()}.json"
    save_json(report_path, report)
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--limit",
        type=int,
        default=int(os.getenv("MAX_CANDIDATES_PER_RUN", "40")),
    )
    args = parser.parse_args()
    result = collect(args.limit)
    print(f"Collected: {result['collected_count']}; incomplete: {result['incomplete_count']}")
