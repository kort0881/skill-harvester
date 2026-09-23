---
name: "html-anything"
description: "Generate a polished, single‑file HTML page from an idea, file, folder, URL, or exported dataset, automatically selecting a design system and producing assets as needed."
---

# html‑anything

**Purpose**
Convert an idea, file, folder, URL, or export request into a ready‑to‑share HTML page. The skill chooses an appropriate design system (teaching, dashboard, timeline, etc.) and produces `output.html` plus an optional `assets/` folder.

**When to use**
- User asks for a webpage, teaching site, dashboard, report, atlas, or any visual, shareable output.
- User provides a file/folder/URL that should be browsable or visualised.

**Inputs**
| Mode | Description |
|------|-------------|
| Idea / brief | Short description of the desired page. |
| Local file | Path to a file (CSV, PDF, Markdown, etc.). |
| Folder | Path to a directory to be explored. |
| URL | Web address to fetch and transform. |
| Export request | Name of a source platform; the skill will give export steps. |

**Outputs**
- `output.html` (or `<name>.html`) placed next to the source.
- Optional `assets/` folder with generated images, icons, etc.
- A short response containing the path and a note about browser verification.

**Core workflow**
1. **Understand request** – determine input mode.
2. **Export guidance** – if only a source name is given, return concise export steps and stop.
3. **Inspect source** – sample files, fetch URLs, or expand brief into a content plan.
4. **Select style** – automatically pick one of the predefined styles (`teaching`, `dashboard`, `timeline‑story`, …).
5. **Load style contract** – read the corresponding style prompt and any `referenceHtml`/`referenceAssets`.
6. **Build HTML** – generate markup, inline CSS/JS, and embed assets (or create `assets/` folder).
7. **Verify in a browser** – check rendering, responsiveness, contrast, and interaction.
8. **Hand‑off** – return the file path and brief status.

**Design requirements**
- Mobile‑first, WCAG AA contrast, focus states, 44 px touch targets.
- Inline CSS/JS; no external CDN unless explicitly allowed.
- Optional dark‑mode support for data‑heavy reports.
- `data-ha-style="<selected‑style>"` attribute on `<html>`.

**Privacy**
- Treat generated HTML as sensitive; mask personal identifiers unless the user requests otherwise.
- Do not provide professional legal/medical advice.

**Example**
```
User: "Create a teaching site about the solar system."
Skill response: (generates `output.html` using the `teaching` style and returns the path)
```
