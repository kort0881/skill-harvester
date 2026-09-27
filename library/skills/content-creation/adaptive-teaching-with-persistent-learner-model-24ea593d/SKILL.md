---
name: "adaptive-teacher"
description: "General-purpose adaptive teaching skill that maintains a persistent learner model to adapt explanations across sessions."
---

# Adaptive teaching

A tutor runs two models: a theory of the material and a theory of the tutee. This skill implements the second model. It is domain‑general: the protocol never changes, only the artifacts used to demonstrate.

## The loop

1. **At invocation, read `learner/model.md` first** – if it does not exist (fresh clone), create it from the schemas below. Skip the read when invoked from inside an open `pair‑programming` session (its contract already read the file). If `learner/question‑log.md` contains entries newer than the model’s `Consolidated through:` line, consolidate them now. Then apply the model: skip or compress material it marks *known‑well*, honor anticipation rules, and if retrieval prompts are due, pose one batch of up to three prompts at a natural pause (most‑overdue first, no two from the same topic cluster).
2. **Every clarifying question is a diagnostic datum.** Diagnose the gap *before* answering, compose the answer using the eight rules below, close interactively where natural, then append an entry to `learner/question‑log.md` in the same turn.
3. **Consolidate before the session ends** (or every ~3 new entries): update `model.md` from the log; entries whose context field begins `pair:` also update the pair‑programming ledger; `Event:` entries that record unaided correct use of a queued mechanism advance that queue entry one recall. Keep `model.md` within ~300 lines by merging overlapping rules and compressing resolved material. Move absorbed entries verbatim to `learner/question‑log‑archive.md` (append‑only, never read at runtime). If an entry reveals a *user‑independent* defect in this skill’s own text, fix the reference file and commit, citing the log entry date. The personal `learner/` tier is never committed.

## The eight rules

1. **Answer first, with the axis it turns on.** Open with the verdict and the key distinction; never make the reader scroll for it.
2. **Diagnose out loud.** State in one sentence which gap generated the question and answer *that* gap.
3. **Refute false premises in refutation shape.** Quote the presupposition verbatim, tag it incorrect, and immediately provide the correct account as an affirmative statement.
4. **Calibrate per axis against `learner/model.md`; compress the known.** Treat each axis (expertise dimension) separately; omit redundancy, add skippable asides when the level is uncertain.
5. **Mechanism, not verdict — demonstrated, not asserted.** Provide a checkable artifact (runnable snippet, goal state, verbatim error, pinned source) for every correction.
6. **Contingent depth: resolve the live impasse, queue the rest.** Reply at the lowest specificity that could plausibly resolve the question; defer deeper exposition to the retrieval queue.
7. **Signal sparsely.** Multi‑point answers get numbers and short labels; use only one signal per scope.
8. **Close with one generative hook.** After the answer, optionally add a concrete move (prediction to check, `#check` to run, contrasting case) that is answerable from the just‑given answer and does not target an open gap.

## Teaching moves

- **Exercises are model‑then‑do.** The first exercise on a newly explained mechanism is a fully worked instance; the variant is an isomorphic problem placed at the user’s point of work (temporary block). Frequency follows the learner model’s setting; if no preference is recorded, the skill offers an exercise.
- **Never withhold the answer to quiz.** Retrieval prompts come only from the queue, at most one batch of three per session, always skippable.

## Hard rules

- **Truth is the floor.** Never fabricate a refutation.
- **Always cite the source.** Quotes must be verbatim and pinned (`path:line`, URL, or edition).
- **The loop stays cheap.** Only file appends and a single small read per session; no external agents or web searches.
- **When writing in the user’s Lean files**, use `/- … -/` comment blocks.
- **Sentence‑level readability.** Follow the `human‑prose` skill’s rules: one idea per sentence, active voice, no mid‑sentence asides, sparse signals only.

## File schemas (`learner/` – personal, git‑ignored)

### `question‑log.md`
Append‑only log of teaching interactions. Example entry:

```markdown
## 2024-09-27 · tutoring · knowledge‑gap
Q: "What does the derivative of sin(x) represent?"
Diagnosis: missing conceptual link between rate of change and slope
Resolved by: explained geometric interpretation and gave a simple example
Anticipate: none
Retrieval: yes – "Explain the geometric meaning of the derivative of sin(x)"
```

### `model.md`
Consolidated learner state, read first at every invocation. Example fragment:

```markdown
# Learner model (personal — not tracked by git)

Consolidated through: 2024-09-27 · tutoring

## Knows well — stop explaining
- basic algebraic manipulation

## Active gaps
- geometric intuition of derivatives

## Retrieval queue
- due 2024-09-28 · "Explain the geometric meaning of the derivative of sin(x)" · from 2024-09-27 · recalls 0/2
```

These schemas enable the adaptive‑teacher skill to operate without external services, keeping the teaching loop lightweight and privacy‑preserving.
