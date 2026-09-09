---
name: "repo-task-proof-loop"
description: "Repo‑local workflow skill for large coding tasks, providing a repeatable proof loop with spec freeze, build, evidence, verification, and fix phases."
---

# Repo Task Proof Loop

Use this skill when the user wants a repeatable, auditable implementation workflow for a non‑trivial coding task, especially a feature, refactor, migration, or bug fix that should leave repo‑local proof in `.agent/tasks/<TASK_ID>/`.

All task artifacts created by this workflow must stay inside the repository.

When the examples below mention `scripts/task_loop.py`, that path is relative to this skill root. Run it while your shell working directory is inside the target repository.

## What this skill does
1. Initializes a strict repo‑local task folder under `.agent/tasks/<TASK_ID>/`.
2. Seeds or updates the required artifact files.
3. Installs project‑scoped Codex and Claude subagent templates into `.codex/agents/` and `.claude/agents/`.
4. Updates the repo‑root `AGENTS.md` Codex baseline plus the repo's Claude guide file (`CLAUDE.md` or `.claude/CLAUDE.md`) with a managed block that explains the workflow.
5. Guides the agent through a strict loop: spec freeze → builder implementation → evidence packing → fresh verification → minimal fix → fresh verification again until `PASS`.

See:
- `references/REFERENCE.md`
- `references/COMMANDS.md`
- `references/SUBAGENTS.md`
- `references/SCHEMAS.md`

## Commands this skill supports
Treat the following words as commands when the user invokes this skill:

- `init <TASK_ID>`: create `.agent/tasks/<TASK_ID>/`, install or refresh subagent templates, and update `AGENTS.md` plus the repo's Claude guide file.
- `freeze <TASK_ID>`: create or refine `spec.md` from the user task, task file, and repo guidance.
- `build <TASK_ID>`: implement the task against the frozen spec.
- `evidence <TASK_ID>`: create or refresh `evidence.md`, `evidence.json`, and raw artifacts without changing production code.
- `verify <TASK_ID>`: run a fresh verifier pass and write `verdict.json`, plus `problems.md` when needed.
- `fix <TASK_ID>`: apply the smallest safe fix set from `problems.md`, then refresh the evidence bundle.
- `run <TASK_ID>`: execute the full loop from spec freeze through verification.
- `status <TASK_ID>`: summarize current artifact status.

If the user does not supply a command, infer the next step from repo state:
- If the task folder does not exist, run `init` first.
- If `spec.md` is missing or placeholder‑only, do `freeze`.
- If implementation is not yet complete, do `build`.
- If evidence is stale or missing, do `evidence`.
- If no fresh verdict exists, do `verify`.
- If verdict is not `PASS`, do `fix`.

## Initialization step
Run the bundled initializer from the repository root or current working directory inside the repo:

```bash
scripts/task_loop.py init --task-id <TASK_ID>
```

Optional task seeding:

```bash
scripts/task_loop.py init --task-id <TASK_ID> --task-file path/to/task.md
scripts/task_loop.py init --task-id <TASK_ID> --task-text "User task text"
```

The initializer will:
- resolve the repo root
- create `.agent/tasks/<TASK_ID>/`
- create all required artifacts, including placeholders under `raw/`
- install project‑scoped subagent files
- insert or refresh managed workflow blocks in `AGENTS.md` and the repo's Claude guide file

For Codex, the managed workflow block is kept in the repo‑root `AGENTS.md`. For Claude Code, it is kept in the repo‑root `CLAUDE.md`.

## Heavy‑task default workflow
For large tasks, keep the user‑facing request simple. In Codex, continue serially unless the user explicitly asks for delegation or parallel agent work.

### Preferred delegated sequence
1. `init <TASK_ID>` (if needed) and confirm `spec.md` exists.
2. Spawn exactly one spec‑freezer subagent and wait for it.
3. Spawn exactly one builder subagent and let it implement.
4. Continue with the same builder session for evidence packing.
5. Spawn exactly one fresh verifier subagent and wait for it.
6. If verdict is not `PASS`, spawn exactly one fixer subagent.
7. Spawn one fresh verifier subagent again.
8. Repeat steps 6‑7 until the verifier returns `PASS` or the user stops the loop.

### Codex adaptive fan‑out (optional)
Use only after explicit user authorization and when the task benefits from bounded parallel work. Limit parallel helpers to a maximum of three and keep the overall orchestration shallow.

## Spec freeze requirements
`spec.md` must contain at least:
- original task statement
- explicit acceptance criteria labeled `AC1`, `AC2`, …
- constraints
- non‑goals

Do not edit production code during spec freeze.

## Evidence packing requirements
`evidence.md` and `evidence.json` must judge each acceptance criterion independently with `PASS`, `FAIL`, or `UNKNOWN`. Every `PASS` must cite concrete proof such as file paths, commands run, exit codes, output summaries, or artifact paths under `raw/`.

## Fresh verification requirements
The verifier must run in a fresh session or fresh subagent and must not modify production code. It writes:
- `.agent/tasks/<TASK_ID>/verdict.json`
- `.agent/tasks/<TASK_ID>/problems.md` (only when overall verdict is not `PASS`).

## Fixer requirements
The fixer reads only `spec.md`, `verdict.json`, and `problems.md`. It must reconfirm each listed problem before editing, make the smallest safe change set, avoid regressing passing criteria, regenerate evidence artifacts, and stop without writing a final sign‑off.

## Validation
Before claiming the workflow is correctly initialized or the artifact set is complete, run:

```bash
scripts/task_loop.py validate --task-id <TASK_ID>
```

Run `validate` only after `init` has fully finished.

For a quick summary:

```bash
scripts/task_loop.py status --task-id <TASK_ID>
```

## Guardrails
- Keep `.agent/tasks/<TASK_ID>/` inside the repo.
- Treat UI checklists as ephemeral; the durable state lives in the task folder.
- Never claim task completion unless every acceptance criterion is `PASS`.
- Separate evaluator and fixer roles.
- Preserve existing user guidance outside the managed blocks in `AGENTS.md` and the repo's Claude guide file.
