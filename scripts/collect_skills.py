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

SEEN_FILE = CANDIDATES_DIR / "seen.json"
PENDING_FILE = CANDIDATES_DIR / "pending.json"


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
    print(f"Collected: {result['collected_count']}")
