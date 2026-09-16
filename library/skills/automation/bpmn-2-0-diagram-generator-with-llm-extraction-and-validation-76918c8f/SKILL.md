---
name: "bpmn-generator"
description: "Enterprise‑grade BPMN 2.0 diagram generator that turns natural‑language process descriptions into OMG‑compliant BPMN XML files and SVG previews. The tool runs a four‑phase pipeline – Intent Extraction (LLM → JSON Logic‑Core), Validation (dead‑lock detection, structural soundness), Auto‑Layout (ElkJS) and Serialization – and supports full BPMN 2.0 element set, multi‑pool collaborations, and an optional optimisation mode that emits non‑blocking redesign advisories."
---

# Overview

The generator can be used via CLI, programmatic API, or HTTP endpoint. It is
designed for enterprise environments where strict compliance and deterministic
behaviour are required.

## Pipeline

```
User Text → Intent Extraction (LLM) → JSON Logic‑Core
          ↓ Validation (rules, dead‑lock detection)
          ↓ Auto‑Layout (ElkJS Sugiyama algorithm)
          ↓ Serialization (pipeline.js)
          → BPMN 2.0 XML + SVG preview
```

*The LLM never handles coordinates – layout is fully algorithmic.*

## Modes

- **Document (default, IST)** – faithfully capture the described process.
- **Optimize (Soll)** – enable the optimisation advisory layer which suggests
  redesigns (parallelisation, task merging, lane relocation, etc.) as
  non‑blocking `advisories`. Advisories are never applied automatically.

### Selecting a mode

| Entry point | Command / payload |
|-------------|-------------------|
| CLI | `node bpmn/pipeline.js in.json out --optimize` |
| Programmatic | `runPipeline(lc, {mode: "optimize"})` |
| HTTP | POST `{ "logicCore": {...}, "mode": "optimize" }` to `/api/v1/generate` |
| MCP | `mode: "optimize"` on `generate_bpmn` etc. |

## Redesign Toolbox (optimise mode)

Transforms are deterministic JavaScript functions located in
`scripts/bpmn/redesign.js`. Each transform provides a `preview*` (feasibility) and
`apply*` (execution) function and returns a change record `{added, removed,
modified}`. Examples:

- `parallelize` – split a linear task chain into a parallel‑gateway split/join.
- `mergeTasks` – collapse a linear chain into a single task (requires explicit name).
- `relane` – move a node to a different lane.
- `reorderKnockouts` – reorder exclusive‑gateway checks (requires explicit order).
- `isolateException` – convert an inline exception branch into a boundary event.

All transforms perform a sound‑ness check after execution and roll back on
structural errors.

## Validation (Phase 2)

The pipeline enforces the following **errors** (pipeline aborts):
- At least one `startEvent` and one `endEvent`.
- All edge `source`/`target` IDs must exist.
- No XOR‑split feeding an AND‑join (dead‑lock detection).
- Message flows reference valid pool/node IDs.

**Warnings** are reported but do not stop the pipeline unless `--strict` is
used, which treats warnings as fatal.

## Running the Generator

```bash
# Install dependencies (once)
cd scripts && npm install

# Generate from a JSON Logic‑Core file
node bpmn/pipeline.js my-process.json my-process

# Inline mode (no script execution) – generate artifacts directly in the
# conversation as code blocks.
```

Outputs:
- `my-process.bpmn` – BPMN 2.0 XML with DI coordinates.
- `my-process.svg` – SVG preview.
- `my-process_logic.json` – Logic‑Core JSON for future amendments.

## Amendment Flow

To edit an existing diagram, load its Logic‑Core JSON, apply atomic changes
using the amendment prompt, re‑validate, and re‑run the pipeline. IDs are
preserved.

## Safety & Compliance

- No LLM calls are made during the redesign phase.
- All generated XML complies with OMG BPMN 2.0.2 specifications (gatewayDirection,
  event definitions, DI bounds, etc.).
- Strict mode (`--strict`) ensures no warnings are shipped.

---
