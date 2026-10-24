"""Проверки качества собранного навыка.

Три независимых сита, которые применяются ДО обращения к модели:

* целостность бандла — навык ссылается на файлы, которые обязаны лежать рядом;
* реклама внутри навыка — продажа курсов/подписок вместо инструкции;
* пригодность к нашему стеку — навык должен попадать в целевые домены,
  иначе библиотека превращается в свалку «интересного вообще».

Всё здесь детерминировано и без сети: результат одинаков на одинаковом входе.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Iterable

# Пути, на которые ссылается SKILL.md и которые обязаны существовать в бандле.
REFERENCE_PATTERN = re.compile(
    r"(?<![\w/.-])"
    r"((?:scripts|references|templates|assets|examples|docs)/[\w./\-]+\.(?:py|sh|bash|md|json|ya?ml|toml|txt|csv|js|mjs|ts|tsx|jsx|html))"
)

# Признаки торговли и монетизации внутри навыка.
PROMO_PATTERNS: tuple[tuple[str, str], ...] = (
    ("gumroad", r"gumroad\.com"),
    ("stripe-payment-link", r"(?:buy|pay)\.stripe\.com"),
    ("lemonsqueezy", r"lemonsqueezy\.com"),
    ("payhip", r"payhip\.com"),
    ("patreon", r"patreon\.com"),
    ("kofi", r"ko-fi\.com"),
    ("buymeacoffee", r"buymeacoffee\.com"),
    ("buy-now", r"(?i)\bbuy now\b"),
    ("join-course", r"(?i)\bjoin (?:my|our|the) (?:course|community|membership|academy|program)\b"),
    ("subscribe-upsell", r"(?i)\bsubscribe to (?:my|our) (?:channel|newsletter|course)\b"),
    ("price-tag", r"(?i)(?:one[- ]time|only)\s*\$\s?\d{2,}|\$\s?\d{2,}\s*(?:usd|one[- ]time)"),
    ("affiliate", r"(?i)\baffiliate (?:link|program)\b"),
    ("limited-time", r"(?i)\blimited[- ]time (?:offer|deal)\b"),
)

DEFAULT_BUNDLE_DIRS = ("scripts", "references", "templates", "assets", "examples")


def _clean_reference(value: str) -> str:
    return value.strip().strip(".,;:)]}\"'")


def extract_references(text: str) -> list[str]:
    """Возвращает уникальные относительные пути, упомянутые в SKILL.md."""
    found: list[str] = []
    for match in REFERENCE_PATTERN.finditer(text or ""):
        path = _clean_reference(match.group(1))
        if path not in found:
            found.append(path)
    return sorted(found)


def is_glob_reference(path: str) -> bool:
    return any(char in path for char in "*?")


def missing_references(references: Iterable[str], files: set[str]) -> list[str]:
    """Какие из ссылок не покрыты файлами бандла.

    Глобы (`references/*.md`) считаются покрытыми, если есть хотя бы один файл
    под этим префиксом: точное имя в тексте могло быть примером.
    """
    normalized = {item.replace("\\", "/") for item in files}
    missing: list[str] = []
    for ref in references:
        ref = ref.replace("\\", "/")
        if is_glob_reference(ref):
            prefix = ref.split("*")[0]
            if any(item.startswith(prefix) for item in normalized):
                continue
            missing.append(ref)
            continue
        if ref not in normalized:
            missing.append(ref)
    return missing


def bundle_files(bundle_dir: Path) -> set[str]:
    if not bundle_dir.exists():
        return set()
    return {
        str(path.relative_to(bundle_dir)).replace("\\", "/")
        for path in bundle_dir.rglob("*")
        if path.is_file()
    }


def check_bundle(skill_md: str, bundle_dir: Path) -> dict[str, Any]:
    """Целостность навыка: ссылки против фактических файлов рядом с SKILL.md."""
    references = extract_references(skill_md)
    files = bundle_files(bundle_dir)
    missing = missing_references(references, files)
    return {
        "references": references,
        "files": sorted(files),
        "missing": missing,
        "complete": not missing,
        "file_count": len(files),
    }


def detect_promo(text: str) -> dict[str, Any]:
    """Ищет торговлю внутри навыка. Чем больше совпавших шаблонов, тем хуже."""
    hits: list[str] = []
    for name, pattern in PROMO_PATTERNS:
        if re.search(pattern, text or ""):
            hits.append(name)
    return {"hits": hits, "count": len(hits), "promotional": bool(hits)}


def _tokens(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-zA-Zа-яА-ЯёЁ][\w\-]{2,}", (text or "").lower())
        if len(token) > 2
    }


def similarity(first: str, second: str) -> float:
    """Жаккар по словам: устойчивее диффлиба на коротких summary."""
    left, right = _tokens(first), _tokens(second)
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def fit_score(text: str, profile: dict[str, Any]) -> dict[str, Any]:
    """Насколько навык попадает в целевые домены владельца (0-100).

    Формула намеренно простая: для каждого домена считаем число попаданий
    ключевых слов, нормируем на три попадания (s_d), берём лучший домен и
    добавляем по 5 баллов за каждый дополнительный домен с s_d >= 0.5.
    """
    lowered = (text or "").lower()
    domains = profile.get("domains") or []
    scored: list[dict[str, Any]] = []

    for domain in domains:
        keywords = [str(item).lower() for item in domain.get("keywords", [])]
        hits = sum(1 for keyword in keywords if keyword and keyword in lowered)
        strength = min(1.0, hits / 3) if hits else 0.0
        scored.append(
            {
                "domain": domain.get("name", "unnamed"),
                "hits": hits,
                "strength": round(strength, 3),
            }
        )

    scored.sort(key=lambda item: (item["strength"], item["hits"]), reverse=True)
    if not scored or scored[0]["strength"] == 0:
        return {"score": 0, "best_domain": None, "domains": scored}

    best = scored[0]
    bonus = 5 * sum(1 for item in scored[1:] if item["strength"] >= 0.5)
    score = min(100, round(best["strength"] * 100) + bonus)
    return {"score": score, "best_domain": best["domain"], "domains": scored[:5]}


def precheck(
    skill_md: str,
    bundle_dir: Path,
    profile: dict[str, Any] | None = None,
    require_complete_bundle: bool = True,
    min_fit: int = 0,
    max_promo_hits: int = 0,
) -> dict[str, Any]:
    """Сводит все сита в один вердикт. Пустой `reasons` = кандидат проходит."""
    bundle = check_bundle(skill_md, bundle_dir)
    promo = detect_promo(skill_md)
    fit = fit_score(skill_md, profile) if profile else {"score": None, "domains": []}

    reasons: list[str] = []
    if require_complete_bundle and not bundle["complete"]:
        reasons.append("incomplete_bundle")
    if promo["count"] > max_promo_hits:
        reasons.append("promotional")
    if profile and fit["score"] is not None and fit["score"] < min_fit:
        reasons.append("off_profile")

    return {
        "passed": not reasons,
        "reasons": reasons,
        "bundle": bundle,
        "promo": promo,
        "fit": fit,
    }
