---
name: lib-to-skill
description: Agentize a programming library — use when asked to create a skill package, agentize a library, or add AI agent support for an existing project.
---

# lib-to-skill

A skill package converts a programming library into structured guidance for AI agents. It contains a `SKILL.md` (the agent's entry point), guides, helper scripts, and append-only experience files. lib-to-skill is itself a skill package: this file guides you through creating one.

## Available Tools

All scripts live in `scripts/`. Call them as needed — there is no fixed order.

| Script | How to invoke | Purpose | When to call |
|---|---|---|---|
| `check_env.mjs --repo <path>` | `node scripts/check_env.mjs` | Verify runtime version, package importable, key deps (language-adaptive: Python/Node.js/Rust/Go) | Before anything else on an untested environment |
| `check_lsp.sh --repo <path> [--package <name>]` | `bash scripts/check_lsp.sh` (**not** `node`) | Detect language and available LSP / analysis tools | Before extracting API — determines how to proceed |
| `extract_docs.mjs --repo <path>` | `node scripts/extract_docs.mjs` | List documentation files (paths + sizes) for AI to read | When you need to locate docs without knowing the repo structure |
| `run_smoke_test.mjs --cmd "<cmd>" --cwd <path>` | `node scripts/run_smoke_test.mjs` | Run a shell command, report exit code + last 20 lines | Before committing any example command to a guide |

## Agentization Workflow

This is a reference path, not a fixed pipeline. Adapt based on what you learn.

1. **Orient** — Locate the repo. If not given, ask. Read README and any existing docs briefly.
2. **Check environment** — Run `node scripts/check_env.mjs --repo <path> [--package <name>]`. The script auto-detects the repo language (Python/Node.js/Rust/Go) and runs appropriate checks. Read its output:
   - **FAIL on runtime**: install the missing runtime (e.g. Python, Node.js, Go, Rust toolchain)
   - **FAIL on import / node_modules missing**: run the install command shown in the output
   - **Install commands**: shown automatically from the repo's package manifest — run the suggested command
   - **Key deps FAIL** (Python): install individually or run the bulk install command shown
   - **No venv** (Python): create one first (e.g. `uv venv` or `python3 -m venv .venv && source .venv/bin/activate`)
   - **Accelerator info**: note device type (CUDA/XPU/NPU/MPS/CPU-only) in the skill's Environment Setup section so future agents don't attempt device-specific features that won't work
3. **Detect tools** — Run `bash scripts/check_lsp.sh --repo <path> --package <name>`. Follow its recommendation:
   - LSP/pydoc available → use the suggested command to inspect the API
   - Nothing available → read source files directly; check `experience/LEARNINGS.md` for known format characteristics of this library
4. **Locate docs** — Run `node scripts/extract_docs.mjs --repo <path>` to get a file list, then read the relevant ones with the Read tool.
5. **Identify key patterns** — From tool output and direct file reading, determine:
   - The minimal working command (entry point)
   - How configuration is structured and overridden
   - Whether a dry-run / no-hardware mode exists
   - How to run tests
   - Primary extension points
   - Where outputs/checkpoints go
6. **Draft SKILL.md** — Fill `templates/SKILL.template.md`. Every line must be actionable. Target ~400 tokens. The template includes a `## Self-Evolution` section — keep it as-is so every invocation reminds the agent to record new findings. Include a `## Guides` section at the bottom that lists each guide file with a one-line description of when to read it — this is how agents discover that guides exist.
   **QUALITY STANDARD:** `superpowers:writing-skills` defines the canonical SKILL.md authoring rules — frontmatter format (`name`/`description` required, max 1024 chars), CSO (description must start with "Use when…" and describe only triggering conditions, never workflow), token efficiency targets, and cross-referencing syntax. Apply those rules when drafting.
7. **Validate examples** — For each command in SKILL.md or guides, run `node scripts/run_smoke_test.mjs --cmd "..." --cwd <path>` to confirm it exits 0.
8. **Write guides** — Create `guides/01_quickstart.md` through `guides/05_deployment.md` using the validated commands. After writing, verify that the `## Guides` index in SKILL.md accurately reflects the final guide titles and descriptions.
9. **Generate skill-specific scripts** — If the library has non-obvious env requirements, write `skills/<name>/scripts/check_env.mjs` that extends the generic one with library-specific checks (CUDA version, system libs, etc.). If it produces recognizable error patterns, write `skills/<name>/scripts/error_detector.sh` from `templates/hook.template.sh`.
10. **Initialize experience files** — Create `skills/<name>/experience/LEARNINGS.md`, `ERRORS.md`, `FEATURE_REQUESTS.md` with the standard headers (see `templates/experience_entry.template.md`).
    If no LSP was available in step 3, record the library's source structure characteristics in `LEARNINGS.md` — this guides future AI sessions that also lack LSP access.
11. **Install to platform skill directory** — Make the skill discoverable by the target AI platform. Skills are installed as symlinks so edits to `skills/<name>/` take effect immediately.
    - **Default (project-level)**: `ln -sfn "$(pwd)/skills/<name>" <target-project>/.claude/skills/<name>`
    - **User-level** (accessible across all projects): `ln -sfn "$(pwd)/skills/<name>" ~/.claude/skills/<name>`
    - After linking, the skill appears as `/<name>` in Claude Code — users can invoke it directly; the AI auto-discovers it from the frontmatter `description`.
    - **lib-to-skill itself must be installed at user-level** so it remains available across all projects for ongoing agentization and self-improvement work: `ln -sfn /path/to/lib-to-skill ~/.claude/skills/lib-to-skill`. Project-level install alone is insufficient because lib-to-skill is a cross-project tool.
    - For generated skills (e.g., `torch-fsdp`): install at project-level to the project that uses the skill; install at user-level if the skill is general-purpose enough to be useful across multiple projects.
12. **Validate self-evolution** — Verify that the skill actually works end-to-end by running representative tasks against it and feeding findings back in. Skip only if the environment cannot execute code at all.
    - Design 3–5 tasks that together cover the skill's main scenarios (e.g., basic usage, debugging a common error, performance tuning). Choose tasks that will exercise different guides.
    - **Run validation inline** (in the main agent): read each guide and execute its key examples using `run_smoke_test.mjs`. Background subagents in Claude Code only have Bash access if the relevant commands are pre-approved in `settings.json` with `permissionMode: dontAsk` — without that setup, they silently fail all shell commands. Foreground subagents (no `run_in_background`) can prompt interactively, but block the main agent while running.
    - After running each scenario, record findings:
      - Gaps or inaccuracies → fix directly in SKILL.md or the relevant guide
      - Errors encountered → append to `experience/ERRORS.md`
      - Missing coverage → append to `experience/FEATURE_REQUESTS.md`
      - Non-obvious patterns discovered → append to `experience/LEARNINGS.md`
    - Re-run any failed scenario after fixing the gap to confirm the fix works.

## Evolution Workflow

At the end of any task using a skill package, ask: did new knowledge emerge?

- **Error encountered and resolved** → needs an entry in `skills/<name>/experience/ERRORS.md`
- **Pattern or insight found** → needs an entry in `skills/<name>/experience/LEARNINGS.md`
- **Missing coverage in the skill** → needs an entry in `skills/<name>/experience/FEATURE_REQUESTS.md`

**Write the experience entry inline** (do not delegate to a background subagent — they lack Bash/Write permissions in Claude Code). Steps:
- Read the target experience file to find the current highest NNN for today's date
- Write the new entry per `templates/experience_entry.template.md` (ID format: `{PREFIX}-YYYYMMDD-NNN`, increment from highest NNN today)
- Check for existing related entries and add `See Also` links if found
- Check promotion criteria and update `SKILL.md` or `lib-to-skill/SKILL.md`/`templates/` if met

**Promotion criteria**:
- Recurrence-Count ≥ 3, across ≥ 2 distinct tasks, within 30 days → update `SKILL.md`, mark entry `promoted`
- Same pattern across multiple libraries → update `lib-to-skill/SKILL.md` or `templates/`, mark entry `promoted_to_framework`

## Decision Guidelines

- **Environment Setup section in SKILL.md**: always fill it in. State the install command, key non-obvious deps, and hardware requirements. Agents working in a fresh environment need this before they can do anything else.
- Generate a skill-specific `scripts/check_env.mjs` (extending the generic one) when the library has additional env requirements: specific runtime version constraints, required system libraries, build tools (`ninja`, `ccache`, `cmake`), or multi-step install sequences.
- Generate a skill-specific `error_detector.sh` when the library produces recognizable error patterns that benefit from automatic capture.
- Split a library into multiple sub-skills when it has clearly distinct usage modes (e.g., training vs. inference) that would not co-exist in one SKILL.md.
- A SKILL.md that is accurate but incomplete is better than one that is comprehensive but inaccurate. Mark gaps with `# TODO` and add to FEATURE_REQUESTS.md.
