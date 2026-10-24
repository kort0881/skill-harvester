"""Аудит уже опубликованной библиотеки теми же ситами, что и при приёме.

Зачем: правила ужесточаются задним числом. В библиотеке остаются навыки, которые
сейчас не прошли бы приём — со ссылками на отсутствующие скрипты, с рекламой
внутри, не по профилю. Скрипт находит их и (по флагу) уносит в карантин,
не удаляя: вернуть — один `mv`.

    python scripts/audit_library.py --dry
    python scripts/audit_library.py --quarantine
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Any

from common import (
    INDEX_FILE,
    LIBRARY_DIR,
    ROOT,
    SKILLS_DIR,
    load_json,
    load_yaml,
    now_iso,
    save_json,
    utc_stamp,
    REPORTS_DIR,
)
from integrity import precheck, similarity

QUARANTINE_DIR = LIBRARY_DIR / "quarantine"


def audit_item(skill_dir: Path, gates: dict[str, Any], profile: dict[str, Any] | None) -> dict[str, Any]:
    skill_md_path = skill_dir / "SKILL.md"
    if not skill_md_path.exists():
        return {"passed": False, "reasons": ["no_skill_md"], "bundle": {"missing": [], "files": []},
                "promo": {"hits": []}, "fit": {"score": None}}

    text = skill_md_path.read_text(encoding="utf-8", errors="replace")
    # Для опубликованного навыка бандл — это его собственная папка.
    result = precheck(
        text,
        skill_dir,
        profile=profile,
        require_complete_bundle=bool(gates.get("require_complete_bundle", True)),
        min_fit=int(gates.get("minimum_fit_score", 35)),
        max_promo_hits=int(gates.get("max_promo_hits", 0)),
    )
    # SKILL.md сам себя не считает: он есть в списке файлов, но ссылки на него нет.
    return result


def find_duplicate_groups(items: list[dict[str, Any]], threshold: float) -> list[dict[str, Any]]:
    groups: list[dict[str, Any]] = []
    seen: set[str] = set()
    for i, left in enumerate(items):
        if left["library_id"] in seen:
            continue
        cluster = [left["library_id"]]
        left_text = f"{left.get('title','')} {left.get('summary','')}"
        for right in items[i + 1:]:
            if right["library_id"] in seen:
                continue
            right_text = f"{right.get('title','')} {right.get('summary','')}"
            score = similarity(left_text, right_text)
            if score >= threshold:
                cluster.append(right["library_id"])
                seen.add(right["library_id"])
        if len(cluster) > 1:
            seen.add(left["library_id"])
            groups.append({"keep": left["library_id"], "duplicates": cluster[1:]})
    return groups


def audit(quarantine: bool = False) -> dict[str, Any]:
    settings = load_yaml("settings.yml")
    gates = settings.get("gates", {})
    profile_payload = load_yaml("target-profile.yml") if gates.get("use_target_profile", True) else {}
    profile = profile_payload if profile_payload.get("enabled") else None

    index = load_json(INDEX_FILE, {"skills": [], "consolidations": []})
    items = index.get("skills", [])

    findings: list[dict[str, Any]] = []
    clean: list[str] = []

    for item in items:
        library_id = item.get("library_id", "")
        skill_dir = SKILLS_DIR / library_id
        result = audit_item(skill_dir, gates, profile)
        entry = {
            "library_id": library_id,
            "title": item.get("title"),
            "passed": result["passed"],
            "reasons": result.get("reasons", []),
            "missing": (result.get("bundle") or {}).get("missing", []),
            "promo": (result.get("promo") or {}).get("hits", []),
            "fit_score": (result.get("fit") or {}).get("score"),
        }
        if result["passed"]:
            clean.append(library_id)
        else:
            findings.append(entry)
        if not result["passed"]:
            print(
                f"FAIL {library_id}: {', '.join(entry['reasons'])}"
                f" | missing={len(entry['missing'])} promo={len(entry['promo'])} fit={entry['fit_score']}"
            )

    duplicates = find_duplicate_groups(items, float(gates.get("near_duplicate_similarity", 0.72)))

    moved: list[str] = []
    if quarantine and findings:
        QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)
        for entry in findings:
            source = SKILLS_DIR / entry["library_id"]
            target = QUARANTINE_DIR / entry["library_id"]
            if not source.exists():
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                shutil.rmtree(target)
            shutil.move(str(source), str(target))
            moved.append(entry["library_id"])

        moved_set = set(moved)
        index["skills"] = [item for item in items if item.get("library_id") not in moved_set]
        index["updated_at"] = now_iso()
        save_json(INDEX_FILE, index)

    report = {
        "type": "library_audit",
        "created_at": now_iso(),
        "total": len(items),
        "passed": len(clean),
        "failed": len(findings),
        "reasons": _reason_counts(findings),
        "duplicate_groups": duplicates,
        "moved_to_quarantine": moved,
        "findings": findings,
    }
    save_json(REPORTS_DIR / f"audit-{utc_stamp()}.json", report)
    return report


def _reason_counts(findings: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for entry in findings:
        for reason in entry["reasons"] or ["unknown"]:
            counts[reason] = counts.get(reason, 0) + 1
    return counts


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--quarantine", action="store_true", help="унести провалившиеся в library/quarantine")
    parser.add_argument("--dry", action="store_true", help="только отчёт (по умолчанию)")
    args = parser.parse_args()
    result = audit(quarantine=args.quarantine)
    print(
        f"Всего: {result['total']}; прошли: {result['passed']}; провалили: {result['failed']}"
        f"; причины: {result['reasons']}; дубли-группы: {len(result['duplicate_groups'])}"
        f"; в карантине: {len(result['moved_to_quarantine'])}"
    )
