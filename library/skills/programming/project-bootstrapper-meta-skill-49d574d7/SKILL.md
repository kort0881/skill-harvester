---
name: "project-bootstrapper"
description: "Generates a complete, project‑specific set of guardrails, standards, and auxiliary skills before any application code is written. Works for single‑language or polyglot projects and enforces real‑time version verification."
---

# Project Bootstrapper

## Overview
The **Project Bootstrapper** is a meta‑skill that creates a suite of concrete, enforceable skills (architecture, security, testing, DevOps, etc.) tailored to a new software project. It runs **before any code exists**, ensuring that every subsequent development step follows a vetted, version‑locked set of standards.

## Activation
The skill activates when the user:
- Describes a new project idea and uses keywords such as `bootstrap`, `new project`, `start project`, `set up`, or `generate skills`.
- Requests a skill suite for an existing codebase.
- Asks for coding standards, scaffolding, or development guardrails.

## Prerequisites
1. `references/skill-catalog.md` – catalog of all possible skill domains.
2. `references/skill-template.md` – the required skeleton for each generated skill.
3. `references/generation-guide.md` – domain‑specific generation instructions.
4. `references/quality-standards.md` – checklist for skill quality.
5. `references/cross-cutting-concerns.md` – shared rules across skills.

## Phase 1 – Project Intelligence Gathering
### 1.1 Idea & Scope
Collect the following from the user (ask only what is missing):
- **Product**: one‑sentence description, type (web app, CLI, library, etc.), target users.
- **Scale**: expected users, data volume, availability SLA.
- **Constraints**: required technologies, existing codebase, team size, timeline, budget, compliance.
### 1.2 Tech‑Stack Decision & Version Verification
For every technology the user selects, **verify the latest stable version** using a real‑time lookup (WebSearch/WebFetch or equivalent). Record the version, source URL, verification date, and release date. Example record:
```
Technology: Next.js
Version: 16.1.0
Verified via: https://nextjs.org/blog/next-16-1-0
Verification date: 2026-03-09
Release date: 2026-02-15
```
Pin the exact version in all generated configuration files.
### 1.3 Skill Map Generation
Based on the confirmed stack, produce a **skill map** that lists every skill to be generated. Mandatory skills include:
- `project-architecture`
- `{language}-standards`
- `security-hardening`
- `error-handling`
- `data-validation`
- `testing-strategy`
- `performance-optimization`
- `git-workflow`
- `documentation-standards`
- `privacy-compliance`
- `dependency-management`
Add conditional skills (e.g., `api-design`, `ui-engineering`, `devops-pipeline`) as needed.

**Wait for user confirmation** before proceeding to the next phase.

## Phase 2 – Skill Generation Engine
### 2.1 Generation Order (Layers)
Generate skills in dependency layers (0 → 7) so later skills can reference earlier ones. See the original document for the full layer table.
### 2.2 File Structure for Each Skill
```
{skill-name}/
├── SKILL.md          # ≤ 500 lines, follows skill‑template.md
├── references/
│   ├── patterns.md
│   ├── anti-patterns.md
│   └── checklist.md
└── templates/        # optional code/templates
```
### 2.3 Content Requirements (per skill)
1. YAML front‑matter (name & description).
2. Activation conditions.
3. Project‑specific context (tech choices, paths).
4. 15‑40 numbered core rules with rationale and runnable code examples.
5. Approved patterns (copy‑paste ready).
6. Anti‑patterns with severity markers.
7. Measurable performance budgets.
8. Security checklist.
9. Error‑scenario table.
10. Edge‑case handling.
11. Integration points to other skills.
12. Pre‑commit checklist.

## Phase 3 – Output Layout
```
{project-root}/
├── .claude/
│   └── skills/
│       ├── project-architecture/
│       │   └── SKILL.md
│       ├── python-standards/
│       │   └── SKILL.md
│       └── ... (all generated skills)
│   └── _bootstrap-manifest.json
├── .gitignore
└── (application code will be added later)
```
The manifest records the project name, timestamp, tech‑stack, generated skills, and coverage flags.

## Phase 4 – Validation
Run the provided JavaScript or Python validators against `.claude/skills/`. Ensure:
- All tech‑stack components are covered.
- No contradictory rules.
- All `depends_on` references exist.
- Full coverage of security, performance, privacy, testing, and error handling.
- Every rule is verifiable (lint rule, test, or checklist).

## Phase 5 – Continuous Compliance (project‑manager skill)
The automatically generated `project-manager` skill monitors code changes, blocks commits that violate any active skill, and produces weekly compliance reports. Install the pre‑commit hook as described in the original document.

## Phase 6 – Handoff
1. Verify that all skills exist under `.claude/skills/`.
2. Explain how the `project-manager` skill enforces ongoing compliance.
3. Demonstrate the validator commands.
4. Transition to actual development – the generated guardrails are now active.

---
