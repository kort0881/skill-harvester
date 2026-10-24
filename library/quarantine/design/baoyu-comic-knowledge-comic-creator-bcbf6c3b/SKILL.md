---
name: "baoyu-comic"
description: "Knowledge comic creator supporting multiple art styles and tones. Creates original educational comics with detailed panel layouts and sequential image generation."
---

# Knowledge Comic Creator

Create original knowledge comics with flexible art‑style × tone combinations.

## Usage
```bash
/baoyu-comic posts/turing-story/source.md
/baoyu-comic article.md --art manga --tone warm
/baoyu-comic               # then paste content
```

## Options
### Visual Dimensions
| Option | Values | Description |
|--------|--------|-------------|
| `--art` | `ligne-claire` (default), `manga`, `realistic`, `ink-brush`, `chalk` | Art style / rendering technique |
| `--tone` | `neutral` (default), `warm`, `dramatic`, `romantic`, `energetic`, `vintage`, `action` | Mood / atmosphere |
| `--layout` | `standard` (default), `cinematic`, `dense`, `splash`, `mixed`, `webtoon` | Panel arrangement |
| `--aspect` | `3:4` (default, portrait), `4:3` (landscape), `16:9` (widescreen) | Page aspect ratio |
| `--lang` | `auto` (default), `zh`, `en`, `ja`, … | Output language |

### Partial Workflow Options
| Option | Description |
|--------|-------------|
| `--storyboard-only` | Generate storyboard only, skip prompts and images |
| `--prompts-only` | Generate storyboard + prompts, skip images |
| `--images-only` | Generate images from an existing prompts directory |
| `--regenerate N` | Regenerate specific page(s) only (e.g., `3` or `2,5,8`) |

Details: `references/partial-workflows.md`

## Art Styles (画风)
| Style | 中文 | Description |
|-------|------|-------------|
| `ligne-claire` | 清线 | Uniform lines, flat colors, European comic tradition (Tintin, Logicomix) |
| `manga` | 日漫 | Large eyes, manga conventions, expressive emotions |
| `realistic` | 写实 | Digital painting, realistic proportions, sophisticated |
| `ink-brush` | 水墨 | Chinese brush strokes, ink wash effects |
| `chalk` | 粉笔 | Chalkboard aesthetic, hand‑drawn warmth |

## Tones (基调)
| Tone | 中文 | Description |
|------|------|-------------|
| `neutral` | 中性 | Balanced, rational, educational |
| `warm` | 温馨 | Nostalgic, personal, comforting |
| `dramatic` | 戏剧 | High contrast, intense, powerful |
| `romantic` | 浪漫 | Soft, beautiful, decorative elements |
| `energetic` | 活力 | Bright, dynamic, exciting |
| `vintage` | 复古 | Historical, aged, period authenticity |
| `action` | 动作 | Speed lines, impact effects, combat |

## Preset Shortcuts
| Preset | Equivalent | Special Rules |
|--------|-----------|---------------|
| `--style ohmsha` | `--art manga --tone neutral` | Visual metaphors, NO talking heads, gadget reveals |
| `--style wuxia` | `--art ink-brush --tone action` | Qi effects, combat visuals, atmospheric elements |
| `--style shoujo` | `--art manga --tone romantic` | Decorative elements, eye details, romantic beats |

## Compatibility Matrix
| Art Style | ✓✓ Best | ✓ Works | ✗ Avoid |
|-----------|---------|---------|---------|
| ligne-claire | neutral, warm | dramatic, vintage, energetic | romantic, action |
| manga | neutral, romantic, energetic, action | warm, dramatic | vintage |
| realistic | neutral, warm, dramatic, vintage | action | romantic, energetic |
| ink-brush | neutral, dramatic, action, vintage | warm | romantic, energetic |
| chalk | neutral, warm, energetic | vintage | dramatic, action, romantic |

Details: `references/auto-selection.md`

## Auto Selection
Content signals determine default art + tone + layout (or preset):
| Content Signals | Recommended |
|-----------------|-------------|
| Tutorial, how‑to, programming, educational | **ohmsha** preset |
| Pre‑1950, classical, ancient | `realistic` + `vintage` |
| Personal story, mentor | `ligne-claire` + `warm` |
| Martial arts, wuxia | **wuxia** preset |
| Romance, school life | **shoujo** preset |
| Biography, balanced | `ligne-claire` + `neutral` |

When a preset is recommended, load `references/presets/{preset}.md` and apply its special rules.

## Script Directory
All scripts reside in the `scripts/` subdirectory.
**Agent Execution Instructions**:
1. Determine this `SKILL.md` directory as `{baseDir}`.
2. Script path = `{baseDir}/scripts/<script-name>.ts`.
3. Replace `{baseDir}` placeholders with the actual path.
4. Resolve `${BUN_X}` runtime: use `bun` if installed, otherwise `npx -y bun`.

**Script Reference**:
| Script | Purpose |
|--------|---------|
| `scripts/merge-to-pdf.ts` | Merge comic pages into a PDF |

## File Structure
Output directory: `comic/{topic‑slug}/`
- **Slug**: 2‑4 word kebab‑case (e.g., `alan-turing-bio`). If a conflict exists, append a timestamp.

**Contents**:
| File | Description |
|------|-------------|
| `source-{slug}.{ext}` | Original source files |
| `analysis.md` | Content analysis |
| `storyboard.md` | Storyboard with panel breakdown |
| `characters/characters.md` | Character definitions |
| `characters/characters.png` | Character reference sheet |
| `prompts/NN-{cover|page}-[slug].md` | Generation prompts |
| `NN-{cover|page}-[slug].png` | Generated images |
| `{topic‑slug}.pdf` | Final merged PDF |

## Language Handling
Detection priority: `--lang` flag → `EXTEND.md` language setting → user conversation language → source content language. The chosen language is used for all interactions (storyboard, prompts, UI messages). Technical terms remain English.

## Workflow
### Progress Checklist
```
Comic Progress:
- [ ] Step 1: Setup & Analyze
  - [ ] 1.1 Preferences (EXTEND.md) ⛔ BLOCKING
  - [ ] 1.2 Analyze, 1.3 Check existing
- [ ] Step 2: Confirmation – Style & options ⚠️ REQUIRED
- [ ] Step 3: Generate storyboard + characters
- [ ] Step 4: Review outline (conditional)
- [ ] Step 5: Generate prompts
- [ ] Step 6: Review prompts (conditional)
- [ ] Step 7: Generate images ⚠️ CHARACTER REF REQUIRED
  - [ ] 7.1 Generate character sheet FIRST → `characters/characters.png`
  - [ ] 7.2 Generate pages WITH `--ref characters/characters.png`
- [ ] Step 8: Merge to PDF
- [ ] Step 9: Completion report
```

### Flow Diagram (textual)
```
Input → [Preferences]
   ├─ Found → Continue
   └─ Not found → First‑time setup ⛔ BLOCKING → Save EXTEND.md → Continue

Analyze → [Check Existing?] → [Confirm Style + Reviews] → Storyboard → [Review?] → Prompts → [Review?] → Images → PDF → Complete
```

### Step Details
| Step | Action | Key Output |
|------|--------|------------|
| 1.1 | Load `EXTEND.md` (blocking if missing) | Config loaded |
| 1.2 | Analyze content | `analysis.md` |
| 1.3 | Check existing directory | Conflict handling |
| 2 | Confirm style, focus, audience, review preferences | User‑provided options |
| 3 | Generate storyboard + characters | `storyboard.md`, `characters/` |
| 4 | (Optional) Review outline | User approval |
| 5 | Generate prompts | `prompts/*.md` |
| 6 | (Optional) Review prompts | User approval |
| 7.1 | Generate character sheet (mandatory) | `characters/characters.png` |
| 7.2 | Generate pages with character reference | `*.png` files |
| 8 | Merge pages into PDF | `{slug}.pdf` |
| 9 | Completion report | Summary message |

#### Image Generation (Step 7) – Critical Rules
* **Character sheet is mandatory** – generate first, backup existing file if present.
* Use an installed image‑generation skill (e.g., `baoyu-imagine`). Follow its `SKILL.md` interface; do **not** call internal scripts directly.
* Pass `characters/characters.png` as `--ref` when the downstream skill supports it; otherwise prepend character descriptions to each prompt.
* Backup existing prompt and image files before regeneration.
* Default aspect ratios: character sheet `4:3`; page images `3:4`.

## EXTEND.md – Preferences (Blocking)
If `EXTEND.md` is missing, run the first‑time setup described in `references/config/first-time-setup.md` before any other step. The file can configure:
* Watermark settings
* Preferred art/tone/layout
* Custom style definitions
* Character presets
* Language preference

## References
* Core templates: `analysis-framework.md`, `character-template.md`, `storyboard-template.md`, `ohmsha-guide.md`
* Style definitions: `references/art-styles/`, `references/tones/`, `references/presets/`, `references/layouts/`
* Workflow details: `workflow.md`, `auto-selection.md`, `partial-workflows.md`
* Configuration: `config/preferences-schema.md`, `config/first-time-setup.md`, `config/watermark-guide.md`

## Page Modification
| Action | Steps |
|--------|-------|
| **Edit** | Update prompt file **first** → `--regenerate N` → Regenerate PDF |
| **Add** | Create new prompt at desired position → Generate with character ref → Renumber subsequent pages → Update storyboard → Regenerate PDF |
| **Delete** | Remove files → Renumber subsequent pages → Update storyboard → Regenerate PDF |

**Important**: Always modify the prompt file before regenerating to keep changes reproducible.

## Notes
* Image generation typically takes 10‑30 seconds per page.
* Auto‑retry once on generation failure.
* Use stylized alternatives for sensitive public figures.
* Maintain style consistency via a session ID.
* Step 2 confirmation is mandatory; steps 4/6 are conditional based on user request.
* Step 7.1 character sheet **must** be generated before any page images.
* Watermark and language are configured once in `EXTEND.md`.
