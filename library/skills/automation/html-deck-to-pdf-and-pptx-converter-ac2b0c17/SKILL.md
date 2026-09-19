---
name: "zan-html-to-ppt"
description: "Convert a guizang-ppt-skill generated horizontal‑scroll HTML deck into a PDF and image‑based PPTX for offline presentations."
---

# zan-html-to-ppt

> Convert a guizang‑ppt‑skill HTML deck (horizontal scroll, single‑file, `<section class="slide">` structure) into offline assets: a PDF and an image‑based PPTX.

## What the skill does

- **Input**: A guizang‑ppt‑skill style HTML deck (URL, local file, or directory containing `index.html`).
- **Outputs**:
  - `<out>/deck.pdf` – multi‑page PDF, 16:9 full‑bleed.
  - `<out>/deck.pptx` – PPTX where each slide is a full‑size PNG background (non‑editable).
  - `<out>/frames/slide‑NN.png` – raw PNGs for each slide (default 5760×3240, `--scale 3`).

## Workflow

### Step 1 – Gather required information
1. **Deck location** (choose one):
   - Running HTTP URL, e.g. `http://localhost:8810/deck/`
   - Local HTML file path, e.g. `/path/to/deck/index.html` (the skill will start a temporary server)
   - Local directory (the skill will look for `index.html` inside)
2. **Output directory** (optional, default `./out`).
3. **Scale / resolution** (optional, default `--scale 3`).

### Step 2 – Install dependencies
```bash
bash <SKILL_ROOT>/scripts/setup.sh
```
The script is idempotent; the first run installs npm packages and a Chromium binary (~150 MB).

### Step 3 – Run the main script
```bash
node <SKILL_ROOT>/scripts/build.mjs <input> --out <output-dir>
```
| Parameter | Default | Meaning |
|---|---|---|
| `<input>` | – | URL, local HTML file, or directory (required) |
| `--out <dir>` | `./out` | Output folder |
| `--width <px>` | `1920` | CSS viewport width |
| `--height <px>` | `1080` | CSS viewport height |
| `--scale <n>` | `3` | `deviceScaleFactor` (3 → 5760×3240) |
| `--wait <ms>` | `2500` | Upper bound for waiting after a slide change |
| `--format pdf,pptx` | both | Comma‑separated list of formats to generate |

Typical console output:
```
🌐  http server :60199  root=/path/to/web
📍  Open: http://localhost:60199/deck/
📐  Viewport 1920×1080 · scale=3× (out 5760×3240) · wait=2500ms · out=/path/to/out
🎞  8 slides
  ✓ 1/8
  ✓ 2/8
  ...
📄  deck.pdf
📊  deck.pptx
✅ Done → /path/to/out/
```

### Step 4 – Report results to the user
Provide the paths to `deck.pdf`, `deck.pptx`, the total slide count, and (optionally) the PNG frames directory.

## Example interaction
**User**: "Convert my deck at `/Users/X/web/deck/index.html` to PPT and put it in `~/Downloads/2026q4-pitch/`."
**Agent**:
```bash
# First time – install dependencies
bash <SKILL_ROOT>/scripts/setup.sh

# Run conversion
node <SKILL_ROOT>/scripts/build.mjs /Users/X/web/deck/index.html --out ~/Downloads/2026q4-pitch/
```
After the script finishes, reply:
> "Conversion complete ✅ – 8 slides captured.
> - PDF: `~/Downloads/2026q4-pitch/deck.pdf`
> - PPTX: `~/Downloads/2026q4-pitch/deck.pptx`
> - PNG frames are in `~/Downloads/2026q4-pitch/frames/`."

If the user complains about file size, suggest `--scale 2`. If a slide appears blank, suggest increasing `--wait`.

## Technical details (for advanced users)
1. **Base URL handling** – `build.mjs` reads `<base href>` to determine the server root.
2. **Static mode** – Press `B` (guizang shortcut) to disable animations; WebGL background remains.
3. **Slide navigation** – Uses `document.querySelectorAll('#nav .dot')[i].click()` instead of keyboard events.
4. **Animation awareness** – After navigation, polls `document.getAnimations()` until none are running, capped by `--wait`.
5. **Font loading** – Waits for `document.fonts.ready` plus network idle before capturing.
6. **Device scale factor** – `--scale 3` yields Retina‑quality screenshots; lower values reduce size.
7. **Error resilience** – Each slide is captured in a try/catch; failures are reported but do not abort the whole run.
8. **PPTX sizing** – Derived from `--width/--height`; supports non‑16:9 decks without distortion.

## Troubleshooting
| Symptom | Likely cause | Fix |
|---|---|---|
| Blank slide | Animation not finished | Increase `--wait` (e.g., `--wait 4000`) |
| Missing fonts | Google Fonts not loaded | Ensure internet access and increase `--wait` |
| Layout mismatch | Viewport size differs from deck design | Set `--width`/`--height` to match the deck (default 1920×1080) |
| Local images 404 | Incorrect `<base href>` handling | Provide the whole directory, not a single file |
| Chromium fails to start | Dependencies not installed | Re‑run `bash scripts/setup.sh` |
| Output blurry | Scale too low | Use `--scale 4` (larger files) |
| Output too large | Scale too high | Use `--scale 2` |

## Repository layout
```
zan-html-to-ppt/
├─ SKILL.md          ← this document
├─ README.md         ← project overview
├─ LICENSE           ← MIT
├─ scripts/
│  ├─ package.json   ← Playwright, pdf‑lib, pptxgenjs
│  ├─ setup.sh       ← installs npm deps & Chromium (idempotent)
│  └─ build.mjs      ← core conversion script
```
