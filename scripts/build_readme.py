from __future__ import annotations

from collections import defaultdict

from common import INDEX_FILE, LIBRARY_DIR, load_json, now_iso

README_FILE = LIBRARY_DIR / "README.md"


def build() -> None:
    index = load_json(
        INDEX_FILE,
        {"skills": [], "consolidations": [], "updated_at": None},
    )
    active = [skill for skill in index["skills"] if not skill.get("deprecated_by")]
    categories = defaultdict(list)

    for skill in active:
        categories[skill.get("category", "general")].append(skill)

    lines = [
        "# Curated Agent Skills Library",
        "",
        "Автоматически собранная и проверенная библиотека Agent Skills.",
        "",
        f"Последнее обновление: `{index.get('updated_at') or now_iso()}`",
        "",
        f"Активных skills: **{len(active)}**",
        "",
        "## Категории",
        "",
    ]

    for category in sorted(categories):
        lines.append(f"### {category}")
        lines.append("")
        lines.append("| Skill | Описание | Теги | Источник |")
        lines.append("|---|---|---|---|")

        for skill in sorted(categories[category], key=lambda item: item["title"].lower()):
            source = skill.get("source", {})
            if source.get("type") == "monthly_consolidation":
                origin = "monthly consolidation"
            else:
                origin = source.get("repository", "unknown")
            tags = ", ".join(skill.get("tags", [])[:6]) or "—"
            summary = skill.get("summary", "").replace("|", "\\|").replace("\n", " ")
            path = f"./skills/{skill['library_id']}/SKILL.md"
            lines.append(f"| [{skill['title']}]({path}) | {summary} | {tags} | {origin} |")

        lines.append("")

    lines.extend(
        [
            "## Примечание",
            "",
            "Каждый skill сохраняет метаданные происхождения в `metadata.json`. "
            "Проверяйте лицензию и исходный репозиторий перед коммерческим или чувствительным использованием.",
            "",
        ]
    )

    README_FILE.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    build()
