from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
CANDIDATES_DIR = DATA_DIR / "candidates"
REPORTS_DIR = DATA_DIR / "reports"
STATE_DIR = DATA_DIR / "state"
LIBRARY_DIR = ROOT / "library"
SKILLS_DIR = LIBRARY_DIR / "skills"
INDEX_FILE = LIBRARY_DIR / "index.json"

for folder in (RAW_DIR, CANDIDATES_DIR, REPORTS_DIR, STATE_DIR, SKILLS_DIR):
    folder.mkdir(parents=True, exist_ok=True)

load_dotenv(ROOT / ".env")


def now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def utc_stamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


def load_yaml(relative_path: str) -> dict[str, Any]:
    with (CONFIG_DIR / relative_path).open("r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def save_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8", errors="ignore")).hexdigest()


def slugify(value: str, max_length: int = 80) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9а-яё]+", "-", value, flags=re.IGNORECASE)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return (value[:max_length].strip("-") or "unnamed-skill")


def safe_relative_path(value: str) -> str:
    value = value.replace("\\", "/").strip("/")
    value = re.sub(r"[^A-Za-z0-9._/-]+", "-", value)
    return value.replace("..", "-")


def parse_frontmatter(markdown: str) -> tuple[dict[str, Any], str]:
    if not markdown.startswith("---"):
        return {}, markdown

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", markdown, re.DOTALL)
    if not match:
        return {}, markdown

    try:
        metadata = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        metadata = {}

    if not isinstance(metadata, dict):
        metadata = {}

    return metadata, match.group(2)


def markdown_excerpt(text: str, max_chars: int = 750) -> str:
    cleaned = re.sub(r"\s+", " ", text).strip()
    return cleaned[:max_chars] + ("…" if len(cleaned) > max_chars else "")


def extract_title(markdown: str, fallback: str) -> str:
    metadata, body = parse_frontmatter(markdown)
    for key in ("name", "title"):
        if metadata.get(key):
            return str(metadata[key]).strip()

    heading = re.search(r"^#\s+(.+)$", body, flags=re.MULTILINE)
    return heading.group(1).strip() if heading else fallback


def ensure_library_index() -> dict[str, Any]:
    default = {
        "schema_version": 1,
        "updated_at": None,
        "skills": [],
        "consolidations": [],
    }
    index = load_json(INDEX_FILE, default)
    for key, value in default.items():
        index.setdefault(key, value)
    return index


def find_library_skill_by_hash(content_hash: str) -> dict[str, Any] | None:
    index = ensure_library_index()
    return next(
        (item for item in index["skills"] if item.get("content_hash") == content_hash),
        None,
    )


def category_from_text(text: str, fallback: str = "general") -> str:
    categories = load_yaml("categories.yml").get("categories", {})
    normalized = text.lower()
    best_name = fallback
    best_score = 0

    for name, config in categories.items():
        score = sum(
            1 for keyword in config.get("keywords", []) if keyword.lower() in normalized
        )
        if score > best_score:
            best_name = name
            best_score = score

    return best_name


def git_commit_if_changed(message: str) -> bool:
    if os.getenv("GITHUB_ACTIONS") != "true":
        return False

    if not shutil.which("git"):
        return False

    try:
        subprocess.run(["git", "add", "data", "library"], cwd=ROOT, check=True)
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        if not status.stdout.strip():
            return False

        subprocess.run(
            ["git", "config", "user.name", "github-actions[bot]"],
            cwd=ROOT,
            check=True,
        )
        subprocess.run(
            [
                "git",
                "config",
                "user.email",
                "41898282+github-actions[bot]@users.noreply.github.com",
            ],
            cwd=ROOT,
            check=True,
        )
        subprocess.run(["git", "commit", "-m", message], cwd=ROOT, check=True)
        subprocess.run(["git", "push"], cwd=ROOT, check=True)
        return True
    except subprocess.CalledProcessError as error:
        print(f"Git commit skipped: {error}")
        return False
