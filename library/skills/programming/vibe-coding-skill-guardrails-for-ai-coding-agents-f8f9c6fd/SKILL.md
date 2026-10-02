---
name: "vibecodingskill"
description: "Cross‑agent coding reliability skill for preventing AI hallucination and context forgetting. Use when an agent writes, reviews, debugs, or completes code, especially when API accuracy, long‑context continuity, verification evidence, or multi‑agent projection behavior matters."
---

# Vibe Coding Skill

## Purpose

This skill exists for two failure modes only:

1. **Hallucination** – inventing APIs, imports, functions, behavior, or completion claims without evidence.
2. **Forgetting** – losing the task goal, constraints, key files, current state, or acceptance criteria in long work.

Do not turn this into a general software methodology. Keep the core protocol small and let each agent projection adapt the mechanics.

## Core Gates

Every coding task passes through only the gates required by its risk level.

### 1. Ambiguity Gate

- State any ambiguity briefly.
- Prefer reading code or docs over asking when the answer is discoverable locally.
- Ask the user only when a wrong assumption would change the outcome or risk safety/data/production behavior.

### 2. Context Gate

- Keep the task goal, hard constraints, acceptance criteria, and key files visible.
- For long tasks, checkpoint the current state before switching subtasks.
- Before generating or editing, re‑read the files or definitions that actually govern the change.
- Load only relevant chunks; do not dump unrelated files into context.

> See `context/forgetting-control.md` for long‑context, multi‑file, or resumed tasks. See `context/chunking-strategy.md` when files or repositories are large.

### 3. Reality Gate

- Verify uncertain APIs, imports, framework behavior, dependency versions, and local patterns from source, types, docs, or existing code before editing.
- After editing, re‑read changed code and verify imports, signatures, types, and claims against reality.
- For bug fixes, follow `core/systematic-debugging.md`: reproduce, isolate, fix, verify.

> See `triggers/hallucination-control.md` for L2+ tasks or whenever unfamiliar APIs, dependencies, generated code, or safety‑sensitive calls are involved.

### 4. Completion Gate

- Do not claim "done", "fixed", "passing", or "works" without fresh evidence gathered after the last change.
- Run the relevant build, test, lint, type‑check, reproduction, or smoke command.
- Read the output and exit status.
- If verification fails or is skipped, report that clearly and do not claim success.

> Read `core/verification-before-completion.md` before making completion claims.

## Complexity Levels

Use `triggers/complexity-triage.md` to classify the task, then apply the matching gates.

| Level | Typical task | Required gates | User‑visible output |
|-------|--------------|----------------|---------------------|
| L0 Trivial | typo, rename, formatting, comment | Completion Gate (light) | Usually no process report |
| L1 Standard | single function/file, small bug fix | Ambiguity + Completion; Reality if API is uncertain | One‑line plan + verification summary |
| L2 Complex | multi‑file feature, new module, API design, refactor | Ambiguity + Context + Reality + Completion | Short plan, key evidence, verification summary |
| L3 Critical | auth, crypto, permissions, migrations, production, finance, data‑loss risk | All gates + user confirmation + independent review if available | Explicit gates, risks, evidence, verification |

Escalate immediately if work touches security, data integrity, production deployment, or hidden cross‑module contracts.

## Debugging Override

For bug reports, failed tests, failed builds, or runtime errors, debugging rules override the normal edit flow:

```
Reproduce -> Isolate -> Fix -> Verify
```

Do not guess‑patch before reproducing or isolating unless the user explicitly accepts an unverified speculative edit.

## Memory Rules

- Persist only project‑specific facts, decisions, conventions, root causes, and reusable pitfalls.
- Do not persist generic programming advice or routine task logs.
- For L2+ tasks, compress checkpoints when the task spans subtasks or context becomes noisy.
- Agent‑specific storage is defined in `context/memory-compression.md`.

## Agent Projections

`SKILL.md` is the source of truth. Projection files adapt the same gates to each agent:

| Agent | Entry file | Adaptation |
|-------|------------|------------|
| Codex | `projections/AGENTS.md` | terminal evidence, `rg`, file reads, concise reporting |
| Claude | `projections/CLAUDE.md` | extended thinking, project memory, longer context discipline |
| Cursor | `projections/.cursorrules` | inline rules, `@Codebase`, `@Docs`, Problems panel |
| Trae | `projections/TRAE.md` | `Read`, `SearchCodebase`, `Grep`, `GetDiagnostics`, `RunCommand`, `TodoWrite` |

Projection activation rule: agents read their own project‑root entry files, not this `projections/` folder. Use `scripts/install-projections.ps1` to copy the selected projection to the target project root and install the core skill at `vibecodingskill/SKILL.md`.

## Skip Conditions

Skip deep gates when:

- The task is pure Q&A and does not involve code changes or code claims.
- The task is L0 and local evidence is enough.
- The user explicitly says to skip verification or deep checks.

When checks are skipped by user request, say the work is unverified. Do not claim it is correct.
