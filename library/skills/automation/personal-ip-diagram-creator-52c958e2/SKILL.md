---
name: "ip-diagram-creator"
description: "Generate a reusable set of minimalist hand‑drawn visual assets from a user’s personal photo, profile screenshot, bio or other identity material, and use those assets to illustrate long‑form content, knowledge cards, or PPT presentations."
---

# Personal IP Diagram Creator

## Overview
This skill helps an AI agent transform a user‑provided personal identity (photo, homepage screenshot, bio, etc.) into a stable **IP character** and then create visual content (hand‑drawn illustrations, knowledge‑cards, or PPT slides) that consistently features that character.

## Prerequisites
- The execution environment must be able to **read images** (or accept a textual description if images are unavailable).
- Either an **image‑generation tool** (e.g., `image_gen`, Stable Diffusion, DALL·E) is available **or** the agent can output a prompt that the user can copy into an external generator.
- The user must **explicitly authorize** any personal photos or screenshots they provide.

## Inputs
| Parameter | Description |
|-----------|-------------|
| `identity_material` | One or more of: personal photo, homepage screenshot, avatar, short bio, account profile. |
| `content_source` | Text to be visualised – can be a long article, outline, script, or a single sentence. |
| `mode` (optional) | Desired visual mode: `illustration`, `knowledge_card`, or `ppt`. If omitted the skill selects the best mode automatically. |
| `generate_now` (optional) | Boolean flag. When `true` and an image‑generation tool is present, the skill will issue the generation call; otherwise it returns a ready‑to‑copy prompt. |

## Outputs
- **Role‑building cards** – a *Character Info Card* and three *Asset Prompts* (`01_role_anchor`, `02_role_spec`, `03_action_scene`).
- **Content Confirmation Card** – summarises core points, layout, and visual specifications.
- **Prompt(s)** for image generation (or the generated images if the environment supports it).
- **Repair prompts** for any required revisions.

## Workflow
1. **Environment Check** – Detect image‑generation capability and image‑reading ability.
2. **Entry Point Determination** – Decide whether the user needs a new character, already has assets, or only wants visual assets.
3. **Character Construction**
   - Extract identity cues from `identity_material`.
   - Produce a *Character Info Card*.
   - Generate three asset prompts:
     1. `01_角色主锚图` – main anchor portrait.
     2. `02_角色规范说明图` – style & restriction guide.
     3. `03_动作_表情_小比例场景扩展图` – action/scene variations.
   - Ask the user to confirm or request revisions.
4. **Content Understanding**
   - Parse `content_source` to identify core ideas, turning points, and visual anchors.
   - Create a *Shot List* (for long texts) or expand a single‑sentence theme.
5. **Visual Mode Selection**
   - Choose among **hand‑drawn illustration**, **knowledge‑card**, or **PPT** based on content size and user intent.
   - Output a *Visual Mode Recommendation* block containing:
     - Mode, preferred image type, default size, information density, layout suggestion, role distribution, and rationale.
6. **Confirmation Card**
   - Present a structured card (type, size, core viewpoint, titles, text, metaphor, role actions, required elements, etc.) for user approval.
7. **Generation / Prompt Export**
   - If an image tool is present and `generate_now` is true, call it with the fully‑formed prompt.
   - Otherwise, return the prompt(s) plus a *repair prompt* for later tweaking.
8. **QA & Repair**
   - Verify that the character matches the anchor, that the visual conveys the confirmed points, and that style constraints are met.
   - If any check fails, produce a concise repair instruction.

## Example Interaction
**User:** "帮我把我的个人简介和这张头像做成一套手绘风格的知识卡。"

**Skill Response (summary):**
1. *Character Info Card* created from the uploaded photo and bio.
2. Asset prompts generated for the three role assets.
3. Content parsed – core ideas: *创新、协作、成长*.
4. Visual mode: **knowledge_card** – 3‑card set, A4 size, moderate information density.
5. *Content Confirmation Card* displayed for approval.
6. Since no image generator is detected, the skill returns the three ready‑to‑copy prompts and corresponding repair prompts.

## Safety & Authorization
- Only process images **explicitly provided by the user** and confirmed as their own.
- Never request or store images of third parties without clear consent.
- All generated assets are for the user’s personal or professional use; they must not be redistributed as public domain assets without permission.
- The skill never fabricates a likeness when insufficient visual data is supplied – it will ask the user for more description.

## References (internal)
- `references/identity-and-character.md`
- `references/visual-language.md`
- `references/content-workflow.md`
- `references/modes-and-sizes.md`
- `references/ppt-presentation-mode.md`
- `references/prompt-templates.md`
- `references/qa-repair.md`
- `references/safety-and-assets.md`
