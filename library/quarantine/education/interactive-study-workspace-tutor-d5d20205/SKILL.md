---
name: "study"
description: "Interactive learning tutor with spaced repetition, research helpers, and restart‑safe study workspaces. Use when the user wants to learn something new: teach me, I want to study, help me learn, study X, create a course on, tutorial for, walk me through learning. Also use for commands like study init, study start, study status, study review, study break, and book catalog setup/search. Works across Claude Code, Codex, Hermes, Cline, OpenCode, and other Agent Skills‑compatible clients for programming, math, physics, science, engineering, and other structured learning."
---

# Study Workspace - Interactive Tutor

A structured learning environment where **you write the code**, and the agent teaches, guides, and supervises. Every lesson has notes and exercises you implement yourself, with spaced repetition for long‑term retention.

## Philosophy

- **You do the work** – The agent teaches and supervises, you implement
- **Structured lessons** – each lesson = notes + exercise + review
- **Spaced repetition** – FSRS algorithm resurfaces concepts before you forget
- **Research‑backed content** – lessons enriched by live docs, notebooks, web research, and sciagent‑skills domain expertise
- **ADHD‑aware** – energy gating, capped reviews, no guilt, detailed break state
- **Git‑tracked progress** – all attempts saved, safe to experiment

## Agent Compatibility

This skill follows the open Agent Skills folder shape: `SKILL.md` plus optional `references/`, `templates/`, and `scripts/`. The durable behavior is the study workspace contract, not any single agent client’s slash‑command implementation.

Before running a workflow in a new client, read:
- `references/agent-adapters.md` for Claude Code, Codex, Hermes, Cline, OpenCode, and generic agent setup.
- `references/workspace‑lifecycle.md` for the init/start/break/resume state contract shared by all agents.

## Commands

### `study init <topic> [--template=<name>] [--source <path>]`
Initialize a new study workspace.

**Steps:**
1. Read `references/workspace‑lifecycle.md` for the shared workspace contract.
2. Sanitize topic to a directory name, create workspace, `git init`.
3. **Template resolution** – read `references/template‑resolution.md`:
   - Auto‑detect language from topic → select template + mode (code‑as‑subject or code‑as‑tool).
   - Detect scientific domain → attach matching sciagent‑skills if plugin is installed.
   - Copy template files, create `lessons/`, `practice/`, `notes/`, `.fsrs/`.
4. **Ask learning approach** (project‑based, concept‑based, challenge‑based) and store the choice.
5. If `--source` is provided, ingest the material (NotebookLM, pdfplumber, etc.) and record it in the config.
6. If a book catalog exists at `~/.config/study/book-catalog.json`, suggest matching books and let the user add them as sources.
7. Create `.study-config.json` (see Config Schema below), commit, and show a welcome message.

### `study start`
Start or resume a learning session.

- Checks the current `session_state.phase` and either resumes or begins a fresh session.
- Performs an energy check (full, half, fumes) to decide whether to present a new lesson, a review, or suggest a break.
- Optionally asks for a time budget.
- Executes an FSRS warm‑up review (max 3 items, ≤5 min).
- Enters the **Main Lesson Loop** (teach → user implements → review → completion) described below.

### `study status`
Show a progress overview derived from `.study-config.json`. If a visual‑explainer is available, generate an HTML dashboard; otherwise output a plain‑text summary.

### `study review`
Run a standalone spaced‑repetition session using the FSRS protocol.

### `study add‑source <path>`
Add a PDF/ebook to the current workspace, ingesting it via the research‑agents backend.

### `study catalog build <library‑path>`
Build a personal book catalog:
```bash
cd <skill‑dir>/scripts/catalog && uv run study‑catalog build <library‑path>
```

### `study catalog search <query>`
Search the catalog:
```bash
cd <skill‑dir>/scripts/catalog && uv run study‑catalog search "<query>"
```

### `study break`
Save session state, write a session summary, and commit before exiting.

## Lesson Structure
Each lesson file lives in `lessons/NN‑topic.md` and follows this template:
```markdown
# Lesson N: Topic

## Concept
[Clear explanation — enriched by research agent findings]

## Key Points
- Point 1
- Point 2

## Reference Example (Don't Copy!)
[Small example illustrating the concept]

## Common Pitfalls
- Pitfall and how to avoid it

## Exercise

### What to Build
[Clear description]

### Requirements
1. Requirement 1
2. Requirement 2

### Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2

### Where to Work
Create your implementation in: `practice/lesson‑NN/`
```

## Teaching Rules
1. **NEVER write implementation code for the user.** Small reference examples (2‑5 lines) are OK.
2. **Guide, don't solve.** Provide hints, ask probing questions, and point to concepts.
3. **Feedback is specific.** Quote the user’s code, explain why it is right or wrong.
4. **Encourage experimentation.** Git history preserves all attempts.

## User Interaction
After presenting a new lesson:
```
What would you like to do?
1. Read the lesson and start the exercise
2. I have questions about the concept first
3. Take a break
```
After providing feedback:
```
What's next?
1. I'll revise my implementation
2. Questions about the feedback
3. I think it's done — final review?
4. Move to next lesson
5. Take a break
```
When the user is stuck, ask for the specific confusion, give hints, optionally spawn a research sub‑agent, and point to relevant lesson sections.

## Visual Enrichment
Read `references/visual‑libraries.md` to select the appropriate rendering library (KaTeX, JSXGraph, Plotly.js, p5.js, SchemDraw, etc.). If a visual‑explainer sub‑agent is available, invoke it with a prompt that specifies the desired output location (e.g., `practice/lesson‑NN/diagrams/`). If not, fall back to ASCII diagrams.

## Config Schema (v3)
```json
{
  "version": 3,
  "topic": "Go Concurrency",
  "template": "go-idiomatic",
  "template_mode": "code-as-subject",
  "approach": "concept",
  "end_goal": null,
  "difficulty": "beginner",
  "difficulty_override": null,
  "next_calibration_at_lesson": 4,
  "mode": "tutorial",
  "created": "2026-04-04T10:00:00Z",
  "sciagent_skills": [],
  "sciagent_primary": null,
  "progress": {
    "current_lesson": 0,
    "lessons_completed": 0,
    "session_count": 0,
    "last_session": null
  },
  "lessons": [],
  "session_state": {
    "phase": "idle",
    "pending_action": null,
    "context": null,
    "energy": null,
    "time_budget_minutes": null
  },
  "sources": [],
  "review": {
    "fsrs_data_path": ".fsrs/cards.json",
    "items_due": 0,
    "last_review": null
  },
  "catalog_path": "~/.config/study/book-catalog.json"
}
```

## Git Conventions
- `[agent]` – lesson notes, feedback, guidance written by the active agent
- `[user]` – user’s implementation work
- `[session]` – session start/end markers

Always commit before switching turns to keep `git diff` reliable for review.

## Workspace Layout
```
workspace/
├── .study-config.json
├── .fsrs/cards.json
├── lessons/
│   ├── plan.md              (project approach only)
│   ├── 01-intro.md
│   └── 02-next-topic.md
├── practice/
│   ├── lesson-01/
│   └── lesson-02/
├── notes/
│   ├── feedback-2026-04-04.md
│   └── session-2026-04-04.md
├── sources/                  (chunked text from PDFs, if no NLM)
└── [template files]          (go.mod, Makefile, etc.)
```

## Learning Approaches
- **concept** (default) – focused lessons with standalone exercises.
- **project** – build toward a final product; each lesson advances the build.
- **challenge** – progressive difficulty, minimal notes, maximum practice.

The chosen approach is stored in `.study-config.json` under `approach` and influences lesson generation.

## Modes
Per‑session modes that can change within an approach:
- **tutorial** – structured lessons with concepts + exercises (default)
- **practice** – work on exercises without new concepts
- **exploration** – user‑driven, the agent assists and answers questions
- **review** – spaced‑repetition of previous lessons via FSRS
