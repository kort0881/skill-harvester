---
name: "fireworks-open-eli5"
description: "Create evidence‑aware, interactive visual explainers as self‑contained offline HTML. Use when a user asks to explain a concept, repository module, engineering trade‑off, or incident with a diagram, walkthrough, ELI5 treatment, data/request trace, failure view, or teach‑back."
---

# Fireworks Open ELI5

Turn a difficult system into a truthful visual story. Produce a portable JSON spec first, then a deterministic, self‑contained HTML explainer.

## Non‑negotiable boundary

- Evidence comes before visual polish. Label every evidence item `verified`, `inferred`, or `analogy`.
- Never make an analogy look like implementation truth.
- Generated HTML files are **local only** – they are not published, uploaded, or sent without explicit user request.
- Rendering performs **no network calls**. Any cited URL is a reader‑facing link, not a runtime dependency.
- Browser‑local history, favorites, and annotations are disabled until the reader opts‑in.
- PDF export invokes the browser print dialog. PNG exports one scene; PPTX and DOCX export one scene per slide or page. Native `.pages` output is allowed only after the installed Pages app actually saves it.

## Workflow

1. **Identify** audience, question, language, and the core element that travels through the story (e.g., request, packet, decision, event, or user action).
2. **Choose a story grammar** (pick exactly one):
   - `concept`: intuition → mechanism → boundary.
   - `module`: entry point → transformations → outputs/dependencies.
   - `tradeoff`: shared goal → competing options → consequences/decision rule.
   - `incident`: normal path → break and propagation → detection/recovery.
3. **Gather evidence** – inspect local files for repository work; use authoritative sources for external claims and record uncertainty explicitly.
4. **Create a version‑1 JSON spec** following `references/spec-contract.md`. Use 3–7 scenes, 2–6 nodes per scene, a complete truth ladder, trace, glossary, teach‑back, evidence map, and the required mode‑specific `modeData`. Include failure information where relevant.
5. **Validate before rendering**:
   ```bash
   node scripts/validate.mjs path/to/spec.json
   ```
6. **Render** to a new local file:
   ```bash
   node scripts/render.mjs path/to/spec.json path/to/explainer.html
   ```
   The renderer refuses to overwrite an existing file unless `--force` is supplied, in which case it performs an atomic replacement and still rejects symbolic links.
7. **Validate the spec and artifact together**:
   ```bash
   node scripts/validate.mjs path/to/spec.json path/to/explainer.html
   ```
8. **Manual QA** (when a browser is available): open the HTML at desktop width and at 390 px, verify layout, focus handling, interactive sections, zero remote requests, and that each evidence card displays its status, core basis, and source locator.
9. **Workspace interaction test**: open/dismiss the modal drawer via mouse and keyboard, confirm focus return, enable the library intentionally, reload and verify that favorites and plain‑text annotations persist only for same‑origin explainers.
10. **Export verification**: check print stylesheet, PNG signature and dimensions, PPTX/DOCX ZIP signatures and required OOXML parts, and the fallback download link when automatic downloads are suppressed. For native Pages export, run `scripts/serve.mjs`, verify the `.pages` package contains `Index/Document.iwa`, reopen in Pages, then re‑run validators after any change.

## Report language

- The final QA, status, handoff, and generated‑artifact report default to the language of the user’s latest substantive request.
- An explicit `report-language` request overrides the default.
- `spec.language` only controls the generated explainer interface; it does **not** force the conversation report language.
- In mixed‑language conversations, ignore short acknowledgements when choosing the report language. Preserve code, commands, paths, identifiers, exact errors, and source titles when translation would reduce precision.

## Story construction rules

- Title must be a concrete promise, not a generic label.
- Keep the summary to one sentence and each node to one responsibility.
- Prefer 3–5 scenes; use 6–7 only when omitting a stage would distort causality.
- Edges are short‑verb relationships or actions.
- The trace must visit real node IDs in a meaningful order.
- Include failure data only when impact, visible symptom, and fallback are known.
- Place limitations in `truthLadder.caveat`, not in tiny disclaimers.
- Cite source IDs on the scenes or nodes they support; do not cite a source merely because it is adjacent to the claim.

## Quality gate

The work is ready as a local artifact only when:
- The validator returns `ok: true` for both the spec and rendered HTML.
- All IDs and references resolve.
- Every required interactive section has content.
- The selected story mode satisfies its semantic contract.
- The HTML is deterministic and includes a spec SHA‑256 meta tag.
- The artifact byte‑matches the supplied spec and uses trusted CSP hashes.
- No external resources, unsafe runtime APIs, or remote fonts are present.
- Persisted reader state is opt‑in, namespaced, bounded, same‑origin, and kept outside the deterministic spec hash.
- Annotations render as plain text and cannot create executable markup.
- Global and local playback share a single state machine and never run together.
- Each trace step activates the real outgoing relationship path (or a sink’s incoming path), keeping label and arrow state aligned, and highlights only the evidence that supports that step.
- Scene evidence cards preserve `verified`/`inferred`/`analogy` boundaries and expose core text plus an actionable locator without fetching remote previews.
- Exported PNG, PPTX, and DOCX packages have the expected signatures and structure and contain their evidence footer; a claimed native Pages export has also reopened in Pages.
- Mobile uses the stacked flow rather than shrinking the desktop SVG.
- The final report follows the user’s current interaction language, names the generated spec and HTML paths, and states whether desktop, mobile, persistence, playback, evidence, and export browser QA were run.

If evidence is incomplete, generate only when the evidence map and caveat make the gap unmistakable; otherwise stop and report the missing evidence.
