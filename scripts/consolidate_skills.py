from __future__ import annotations

import argparse
import json
import os
import re
from collections import defaultdict
from typing import Any

from groq import Groq
from tenacity import retry, stop_after_attempt, wait_exponential

from common import (
    INDEX_FILE,
    REPORTS_DIR,
    SKILLS_DIR,
    ensure_library_index,
    load_yaml,
    now_iso,
    save_json,
    sha256_text,
    slugify,
    utc_stamp,
)

SYSTEM_PROMPT = """You curate a high-quality Agent Skills library.
Several accepted skills cover closely related work. Create ONE consolidated canonical skill
that retains distinct, useful nuances while eliminating duplicates and unsupported claims.

Return ONLY valid JSON:
{
  "should_consolidate": true | false,
  "title": "title",
  "category": "category slug",
  "summary": "short summary",
  "reason": "why these are duplicates or why not",
  "canonical_skill_markdown": "complete SKILL.md with YAML frontmatter",
  "source_library_ids": ["..."]
}

Requirements for canonical_skill_markdown:
- YAML frontmatter must include name and description.
- Include scope, prerequisites, inputs, workflow steps, validation/quality checks,
  common failure modes and an adaptation section where appropriate.
- Never include secrets, unsafe instructions, or fabricated commands.
- Preserve attribution in a Sources / Derived From section that lists supplied library IDs.
"""

TOKEN_PATTERN = re.compile(r"[A-Za-zА-Яа-яЁё0-9_-]{3,}")


def tokenize(text: str) -> set[str]:
    return {token.lower() for token in TOKEN_PATTERN.findall(text)}


def jaccard(a: set[str], b: set[str]) -> float:
    return len(a & b) / max(1, len(a | b))


def load_skill_text(library_id: str) -> str:
    return (SKILLS_DIR / library_id / "SKILL.md").read_text(
        encoding="utf-8",
        errors="replace",
    )


def find_groups(index: dict[str, Any], threshold: float, limit: int) -> list[list[dict[str, Any]]]:
    by_category: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for skill in index["skills"]:
        if not skill.get("deprecated_by"):
            by_category[skill.get("category", "general")].append(skill)

    groups: list[list[dict[str, Any]]] = []

    for items in by_category.values():
        consumed: set[str] = set()
        for item in items:
            if item["library_id"] in consumed:
                continue

            left = tokenize(f"{item.get('title', '')} {item.get('summary', '')} {' '.join(item.get('tags', []))}")
            group = [item]

            for other in items:
                if other["library_id"] == item["library_id"] or other["library_id"] in consumed:
                    continue
                right = tokenize(f"{other.get('title', '')} {other.get('summary', '')} {' '.join(other.get('tags', []))}")
                if jaccard(left, right) >= threshold:
                    group.append(other)

            if len(group) >= 2:
                for member in group:
                    consumed.add(member["library_id"])
                groups.append(group)

            if len(groups) >= limit:
                return groups

    return groups


def get_client() -> Groq:
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise RuntimeError("GROQ_API_KEY is missing.")
    return Groq(api_key=key)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=20), reraise=True)
def ask_model(client: Groq, model: str, group: list[dict[str, Any]]) -> dict[str, Any]:
    documents = []
    for skill in group:
        text = load_skill_text(skill["library_id"])[:18000]
        documents.append(
            {
                "library_id": skill["library_id"],
                "title": skill["title"],
                "summary": skill["summary"],
                "skill_markdown": text,
            }
        )

    response = client.chat.completions.create(
        model=model,
        temperature=0.15,
        max_completion_tokens=7000,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": json.dumps(
                    {"candidate_group": documents},
                    ensure_ascii=False,
                    indent=2,
                ),
            },
        ],
    )
    return json.loads(response.choices[0].message.content)


def consolidate(limit: int) -> dict[str, Any]:
    settings = load_yaml("settings.yml")["consolidation"]
    threshold = float(settings["minimum_similarity"])
    index = ensure_library_index()
    groups = find_groups(index, threshold, limit)
    client = get_client()
    model = os.getenv("GROQ_CONSOLIDATION_MODEL", "openai/gpt-oss-120b")
    results: list[dict[str, Any]] = []

    for group in groups:
        try:
            review = ask_model(client, model, group)
            if not review.get("should_consolidate"):
                results.append(
                    {
                        "source_library_ids": [item["library_id"] for item in group],
                        "consolidated": False,
                        "reason": review.get("reason", ""),
                    }
                )
                continue

            category = slugify(review.get("category") or group[0]["category"], 50)
            title = review.get("title") or f"Consolidated {category} skill"
            content = review.get("canonical_skill_markdown", "").strip()
            if not content:
                raise ValueError("The model did not return canonical_skill_markdown.")

            group_hash = sha256_text("|".join(sorted(item["library_id"] for item in group)))[:10]
            directory = SKILLS_DIR / category / f"{slugify(title)}-canonical-{group_hash}"
            directory.mkdir(parents=True, exist_ok=True)
            (directory / "SKILL.md").write_text(content + "\n", encoding="utf-8")

            library_id = f"{category}/{directory.name}"
            metadata = {
                "library_id": library_id,
                "title": title,
                "category": category,
                "tags": sorted(set(tag for item in group for tag in item.get("tags", []))),
                "summary": review.get("summary", ""),
                "source": {
                    "type": "monthly_consolidation",
                    "derived_from": [item["library_id"] for item in group],
                },
                "accepted_at": now_iso(),
                "content_hash": sha256_text(content),
                "review": {
                    "decision": "canonical_consolidation",
                    "reason": review.get("reason", ""),
                    "model": model,
                },
            }
            save_json(directory / "metadata.json", metadata)
            index["skills"].append(metadata)

            originals = {item["library_id"] for item in group}
            for item in index["skills"]:
                if item["library_id"] in originals:
                    item["deprecated_by"] = library_id
                    item["consolidated_at"] = now_iso()

            event = {
                "created_at": now_iso(),
                "canonical_library_id": library_id,
                "source_library_ids": sorted(originals),
                "model": model,
                "reason": review.get("reason", ""),
            }
            index["consolidations"].append(event)
            results.append({**event, "consolidated": True})
        except Exception as error:
            results.append(
                {
                    "source_library_ids": [item["library_id"] for item in group],
                    "consolidated": False,
                    "error": str(error),
                }
            )

    index["updated_at"] = now_iso()
    save_json(INDEX_FILE, index)
    report = {
        "type": "monthly_consolidation",
        "created_at": now_iso(),
        "model": model,
        "groups_checked": len(groups),
        "results": results,
    }
    save_json(REPORTS_DIR / f"consolidation-{utc_stamp()}.json", report)
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--limit",
        type=int,
        default=int(os.getenv("MAX_CONSOLIDATION_GROUPS", "5")),
    )
    args = parser.parse_args()
    report = consolidate(args.limit)
    print(f"Groups checked: {report['groups_checked']}")
