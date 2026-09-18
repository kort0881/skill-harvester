---
name: "mav-slidecraft-skill"
description: "Create animation‑rich, zero‑dependency HTML presentations from scratch or by converting PowerPoint files."
---

# Mav SlideCraft Skill

Generate a single‑file HTML presentation that runs entirely in the browser, with built‑in animations, texture overlays, and strict viewport fitting.

## Core Principles
1. **Zero Dependencies** – All CSS/JS is inlined; no npm or build tools.
2. **Viewport Fitting** – Every slide uses `height:100vh` (or `100dvh`) and never scrolls.
3. **Design Discipline** – Fixed layout catalog, muted colour palette, limited animation duration (200‑600 ms), and theme rhythm (`light`, `dark`, `hero light`, `hero dark`).
4. **Font & Texture First** – Use a designated display font and real scanned textures from `references/textures.css`.
5. **Accessibility** – Respect `prefers-reduced-motion` and provide a low‑power `B`‑key toggle.

## Prerequisites
- Python 3 with `python-pptx` (`pip install python-pptx`) for PPT conversion.
- Node 18+ for the validation script (`scripts/validate-deck.mjs`).
- Optional: Vercel CLI (`npx vercel`) for deployment, Playwright for PDF export.

## Workflow Phases
### Phase 0 – Detect Mode
| Mode | Description |
|------|-------------|
| A | New presentation – start at Phase 1 |
| B | PPTX conversion – jump to Phase 4 |
| C | Enhance an existing HTML file |

### Phase 1 – Content Discovery
Ask the user a single multi‑choice question covering purpose, length, content readiness, editing preference, and horizontal deck desire. Record the answers for later steps.

### Phase 2 – Style Discovery
Present the numbered list of 11 visual style combos (e.g., Neo‑Brutalism + 3D, Retro‑Futurism, Maximalism, etc.). After the user selects a style, load the corresponding reference file from `references/combo‑<n>-*.md` together with shared assets:
- `viewport-base.css`
- `html-template.md`
- `animation-patterns.md`
- `theme-rhythm.md`
- `layout-catalog.md`
- `checklist.md`
- Delight Library files
- Texture CSS

### Phase 3 – Generate Presentation
1. **Plan Theme Rhythm** – Create a markdown table mapping each slide to a theme and layout (e.g., `hero dark | L01`).
2. **Image Requirement** – Ask whether the user will provide images. If yes, give a folder structure guide (`images/` with naming conventions).
3. **Content Preview** – Render an ASCII preview of each slide for user confirmation.
4. **HTML Generation** – Assemble a single `index.html` that:
   - Inlines the full `viewport-base.css` and any style‑specific CSS.
   - Imports the selected display and body fonts via Google Fonts (with Fontshare fallback).
   - Embeds texture base64 data from `textures.css` into `:root`.
   - Uses layout identifiers from `layout-catalog.md` (`data‑layout="L01"`).
   - Adds three Delight micro‑interactions (at least one hover and one non‑hover) following `usage-system.md`.
   - Implements `fitSlideContent()` to keep content inside the viewport.
   - Provides `prefers-reduced-motion` and `B`‑key low‑power toggles.
5. **Validation** – Run `node scripts/validate-deck.mjs index.html` and fix any checklist failures.

### Phase 4 – PPT Conversion (optional)
```bash
python scripts/extract-pptx.py input.pptx output_dir
```
Review extracted titles/content, then continue with Phase 2‑3 using the extracted data.

### Phase 5 – Delivery
- Validate the final HTML.
- Run the checklist (`references/checklist.md`).
- Optionally delete temporary preview folders.
- Open the file locally (`open index.html`).
- Summarize location, style, slide count, and navigation keys.

### Phase 6 – Share & Export (optional)
| Option | Command |
|--------|---------|
| Deploy to Vercel | `npx vercel login && npx vercel` |
| Export to PDF | `bash scripts/export-pdf.sh index.html presentation.pdf` |
| Both | Run both commands sequentially |

## Supporting Files Overview
| File | Purpose |
|------|---------|
| `references/html-template.md` | Base HTML structure and JS logic |
| `references/viewport-base.css` | Core responsive CSS |
| `references/layout-catalog.md` | Standard layout skeletons (L01‑L09) |
| `references/textures.css` | Base64‑encoded scanned textures |
| `scripts/validate-deck.mjs` | Static validation script |
| `scripts/deploy.sh` / `export-pdf.sh` | Helper scripts for deployment and PDF export |

---

*This skill is intended for designers, developers, or AI agents that need to produce high‑quality, animation‑rich HTML slide decks without external dependencies.*
