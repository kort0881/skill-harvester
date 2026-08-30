from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from groq import Groq
from tenacity import retry, stop_after_attempt, wait_exponential

from common import (
    CANDIDATES_DIR,
    INDEX_FILE,
    REPORTS_DIR,
    ROOT,
    SKILLS_DIR,
    ensure_library_index,
    find_library_skill_by_hash,
    load_json,
    load_yaml,
    markdown_excerpt,
    now_iso,
    parse_frontmatter,
    save_json,
    slugify,
    utc_stamp,
)

PENDING_FILE = CANDIDATES_DIR / "pending.json"
ANALYZED_FILE = CANDIDATES_DIR / "analyzed.json"

SYSTEM_PROMPT = """You are the strict curator of a public Agent Skills library.
Evaluate a candidate SKILL.md independently and return ONLY valid JSON.

The library accepts practical skills in many areas: programming, DevOps, research,
content, music, design, language learning, education, productivity, networking/privacy
and automation.

Scoring:
- quality_score (0-100): clear structure, explicit prerequisites, inputs/outputs,
  practical steps, examples, verification, maintainability.
- uniqueness_score (0-100): distinctive workflow, domain expertise, non-generic value.
- usefulness_score (0-100): real usefulness for a user or AI agent.
- safety_score (0-100): 100 means safe; lower it for harmful, deceptive, secret-stealing,
  exploit-oriented, illegal, privacy-invasive or destructive instructions.
- total_score (0-100): weighted overall decision score.

Reject content that requests or normalizes secret exfiltration, malware, credential theft,
destructive commands without safeguards, evasion of law enforcement, or clearly harmful actions.

Return this exact JSON schema:
{
  "decision": "accept" | "reject" | "needs_revision",
  "title": "short descriptive title",
  "category": "one short category slug",
  "summary": "2-4 sentences",
  "quality_score": 0,
  "uniqueness_score": 0,
  "usefulness_score": 0,
  "safety_score": 0,
  "total_score": 0,
  "strengths": ["..."],
  "weaknesses": ["..."],
  "tags": ["lowercase tag"],
  "safety_flags": ["..."],
  "recommended_improvements": ["..."],
  "normalized_skill_markdown": "A polished SKILL.md only if decision is accept; otherwise empty string"
}

For accepted skills, normalized_skill_markdown must preserve the source's useful intent,
be self-contained, and begin with YAML front matter containing name and description.
Do not invent technical claims, APIs, commands, or sources that were not supported by the candidate.
"""


def read_raw_file(relative_path: str) -> str:
    absolute = ROOT / "data" / relative_path
    return absolute.read_text(encoding="utf-8", errors="replace")


def get_client() -> Groq:
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise RuntimeError("GROQ_API_KEY is missing. Add it to .env or GitHub Secrets.")
    return Groq(api_key=key)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=20), reraise=True)
def model_review(client: Groq, model: str, candidate: dict[str, Any], content: str) -> dict[str, Any]:
    max_content = content[:26000]
    user_prompt = f"""Candidate metadata:
{json.dumps({
    "source_repository": candidate["source"]["repository"],
    "source_path": candidate["source"]["path"],
    "repository_stars": candidate["source"]["repo_stars"],
    "title_guess": candidate["title"],
    "category_hint": candidate["category_hint"]
}, ensure_ascii=False, indent=2)}

Candidate SKILL.md:
---BEGIN SKILL---
{max_content}
---END SKILL---"""

    response = client.chat.completions.create(
        model=model,
        temperature=0.15,
        max_completion_tokens=6500,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    return json.loads(response.choices[0].message.content)


def clean_model_markdown(markdown: str, title: str, summary: str) -> str:
    markdown = (markdown or "").strip()
    if not markdown:
        return ""

    metadata, body = parse_frontmatter(markdown)
    name = slugify(str(metadata.get("name") or title))
    description = str(metadata.get("description") or summary).replace('"', "'").strip()
    return f'---\nname: "{name}"\ndescription: "{description}"\n---\n\n{body.strip()}\n'


def publish_skill(candidate: dict[str, Any], review: dict[str, Any], source_content: str) -> dict[str, Any]:
    title = review.get("title") or candidate["title"]
    category = slugify(review.get("category") or candidate["category_hint"], 50)
    skill_slug = slugify(title)
    candidate_prefix = candidate["candidate_id"][:8]
    target_dir = SKILLS_DIR / category / f"{skill_slug}-{candidate_prefix}"
    target_dir.mkdir(parents=True, exist_ok=True)

    normalized = clean_model_markdown(
        review.get("normalized_skill_markdown", ""),
        title,
        review.get("summary", ""),
    )
    if not normalized:
        normalized = source_content

    (target_dir / "SKILL.md").write_text(normalized, encoding="utf-8")
    metadata = {
        "library_id": f"{category}/{target_dir.name}",
        "title": title,
        "category": category,
        "tags": review.get("tags", []),
        "summary": review.get("summary", ""),
        "source": candidate["source"],
        "discovered_at": candidate["discovered_at"],
        "accepted_at": now_iso(),
        "content_hash": candidate["content_hash"],
        "source_excerpt": markdown_excerpt(source_content),
        "review": review,
    }
    save_json(target_dir / "metadata.json", metadata)
    return metadata


def analyze(limit: int) -> dict[str, Any]:
    settings = load_yaml("settings.yml")
    analysis_settings = settings["analysis"]
    pending_payload = load_json(PENDING_FILE, {"items": []})
    analyzed_payload = load_json(ANALYZED_FILE, {"items": []})
    pending = pending_payload.get("items", [])
    existing_analyzed_ids = {item["candidate_id"] for item in analyzed_payload.get("items", [])}

    client = get_client()
    model = os.getenv("GROQ_ANALYSIS_MODEL", "openai/gpt-oss-120b")
    min_total = int(os.getenv("MIN_TOTAL_SCORE", analysis_settings["minimum_total_score"]))
    min_quality = int(os.getenv("MIN_QUALITY_SCORE", analysis_settings["minimum_quality_score"]))
    min_unique = int(os.getenv("MIN_UNIQUENESS_SCORE", analysis_settings["minimum_uniqueness_score"]))
    min_chars = analysis_settings["min_content_characters"]

    index = ensure_library_index()
    processed: list[dict[str, Any]] = []
    keep_pending: list[dict[str, Any]] = []

    candidates_to_process = [item for item in pending if item["candidate_id"] not in existing_analyzed_ids][:limit]
    ids_to_process = {item["candidate_id"] for item in candidates_to_process}

    for candidate in pending:
        if candidate["candidate_id"] not in ids_to_process:
            keep_pending.append(candidate)

    for candidate in candidates_to_process:
        try:
            content = read_raw_file(candidate["raw_file"])
            if len(content.strip()) < min_chars:
                review = {
                    "decision": "reject",
                    "title": candidate["title"],
                    "category": candidate["category_hint"],
                    "summary": "The candidate is too short to be a reliable standalone skill.",
                    "quality_score": 0,
                    "uniqueness_score": 0,
                    "usefulness_score": 0,
                    "safety_score": 100,
                    "total_score": 0,
                    "strengths": [],
                    "weaknesses": ["Insufficient instructional content."],
                    "tags": [],
                    "safety_flags": [],
                    "recommended_improvements": ["Add reproducible instructions and examples."],
                    "normalized_skill_markdown": "",
                }
            elif find_library_skill_by_hash(candidate["content_hash"]):
                review = {
                    "decision": "reject",
                    "title": candidate["title"],
                    "category": candidate["category_hint"],
                    "summary": "Exact duplicate of an existing library item.",
                    "quality_score": 0,
                    "uniqueness_score": 0,
                    "usefulness_score": 0,
                    "safety_score": 100,
                    "total_score": 0,
                    "strengths": [],
                    "weaknesses": ["Duplicate content hash."],
                    "tags": [],
                    "safety_flags": [],
                    "recommended_improvements": [],
                    "normalized_skill_markdown": "",
                }
            else:
                review = model_review(client, model, candidate, content)

            safety_flags = review.get("safety_flags", [])
            accepted = (
                review.get("decision") == "accept"
                and int(review.get("total_score", 0)) >= min_total
                and int(review.get("quality_score", 0)) >= min_quality
                and int(review.get("uniqueness_score", 0)) >= min_unique
                and int(review.get("safety_score", 0)) >= 70
                and not safety_flags
            )

            result = {
                "candidate_id": candidate["candidate_id"],
                "candidate": candidate,
                "reviewed_at": now_iso(),
                "model": model,
                "accepted": accepted,
                "review": review,
            }

            if accepted:
                metadata = publish_skill(candidate, review, content)
                if not any(item["library_id"] == metadata["library_id"] for item in index["skills"]):
                    index["skills"].append(metadata)
                result["library_id"] = metadata["library_id"]

            processed.append(result)
            print(f"{candidate['title']}: {'ACCEPTED' if accepted else 'rejected'}")
        except Exception as error:
            candidate["last_error"] = str(error)
            keep_pending.append(candidate)
            print(f"Analysis failed for {candidate['candidate_id']}: {error}")

    index["updated_at"] = now_iso()
    save_json(INDEX_FILE, index)

    analyzed_payload.setdefault("items", []).extend(processed)
    analyzed_payload["updated_at"] = now_iso()
    save_json(ANALYZED_FILE, analyzed_payload)

    pending_payload["items"] = keep_pending
    pending_payload["updated_at"] = now_iso()
    save_json(PENDING_FILE, pending_payload)

    report = {
        "type": "daily_analysis",
        "created_at": now_iso(),
        "model": model,
        "processed": len(processed),
        "accepted": sum(1 for item in processed if item["accepted"]),
        "rejected": sum(1 for item in processed if not item["accepted"]),
        "items": processed,
    }
    save_json(REPORTS_DIR / f"analysis-{utc_stamp()}.json", report)
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--limit",
        type=int,
        default=int(os.getenv("MAX_ANALYZE_PER_RUN", "12")),
    )
    args = parser.parse_args()
    result = analyze(args.limit)
    print(f"Processed: {result['processed']}; accepted: {result['accepted']}")
