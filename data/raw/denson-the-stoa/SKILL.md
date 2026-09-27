---
name: the-stoa-about
description: Entry-point skill for The Stoa repo. Read when a fresh user lands cold; gives a 30-second pitch and routes to the visual tour (skills/stoa-intro/) or guided install (skills/install-stoa/).
---

# The Stoa — entry-point skill

## What this skill is for

You are an agent in a freshly cloned `the-stoa` repo. The PRINCIPAL — the human who just opened this repo in Claude Code — is exploratory. They have not yet decided whether they want to install anything, fork anything, or just read.

Your job in this turn is to **route**, not to dump. Give them a tight 30-second pitch of what The Stoa is, then offer three concrete next steps and let them pick. Do not start the tour or the install without explicit consent. Do not recite the case study end-to-end.

The signals that this skill is the right thing to load:
- The PRINCIPAL just opened the repo and asked something open-ended (*"what is this?"*, *"explain this repo"*, *"give me the tour"*).
- The PRINCIPAL has not named a specific deliverable, file, or task.
- The repo's `CLAUDE.md` pointed you here as the entry point.

If the PRINCIPAL has a specific concrete ask (*"install this on my widget-builder project"*, *"show me the case study §3"*) — skip the pitch and route directly. Don't make them sit through the framing.

---

## Elevator pitch

When the PRINCIPAL asks an open-ended *"what is this?"* / *"explain The Stoa"*, lead with this. Verbatim is fine for cold encounters; condense or rearrange if mid-stream. **Do NOT recite the case study** — this is the canonical short version.

> The Stoa is a recursive three-role agent architecture for Claude Code, built on `bw` (beadwork) as durable cross-session substrate.
>
> Three seats, repeated at every tier (user / project / sub-project): a chief-of-staff (POLYBIUS) that converses with the human and holds memory across sessions, an orchestrator (PLINY) that dispatches the team and reconciles their verdicts, and a team of specialized sub-agents (CAPTAINs) each with one focused job — architect, plan-critic, executor, verifier, reviewer, etc. (ten in the current roster). The recursion is the architectural commitment — same shape at every scope, no special-casing.
>
> Two operational modes coexist: a formal multi-stage gauntlet for hardening work toward production, and pair-programming where the human actively co-drives and collaborates with the agents to get to a prototype worth iterating on. Without the pair-programming mode, the gauntlet would over-engineer drafts — running formal verification, review, and spec-checking on sketches that hadn't yet figured out what they were. Adding pair-programming for the discovery phase is what unlocked token-efficient exploration before the gauntlet's hardening machinery kicks in. Clean PASS ships autonomously — no routing every commit through the human.
>
> MIT-licensed; deployable onto your own work.

After the pitch, offer the three-way branch (visual tour / install / read deeper) per the section below.

---

## Where to find more (for the agent reading this skill)

When the PRINCIPAL asks follow-up questions after the pitch, route to the right reference rather than improvising or reciting from memory. Map:

| Question shape | Read |
|---|---|
| *"What's bw?"* / *"How does beadwork work?"* | The bw repo (separate project). Web-search the current URL — don't trust training-data URLs for tools that may have moved. Don't answer from pitch context alone; the pitch only names bw as a dependency. |
| *"What's POLYBIUS / PLINY exactly?"* | `substrate/MAJOR_POLYBIUS.md` / `substrate/MAJOR_PLINY.md` — the role files (spec-authoritative). |
| *"What does CAPTAIN_X do?"* | `substrate/CAPTAIN_X.md` for the specific officer envelope. |
| *"How does the gauntlet pipeline work?"* | Case study §6 (Information flow with cycles). |
| *"Why three roles, not one?"* | Case study §3. |
| *"How does trust distribute across the seats?"* | Case study §3.5 (Three trust patterns). |
| *"What's the recursion claim, in detail?"* | Case study §4 (Why recursion) + §7 (Asymmetric visibility). |
| *"Why does role-file voice matter?"* | Case study §5 (voice discipline is structural). |
| *"Tell me more about the two operational modes."* | Case study §6.5. |
| *"What disciplines fell out of this?"* | Case study §8 — the 22-child `u--7yg` empirical record at `user-beadwork/u--7yg`. |
| *"Show me a worked example."* | Case study §9 (Arc 14 sub-project spawning, end-to-end). |
| *"Where's it going?"* / *"Hypergraph?"* | Case study §10. |
| *"What's the architecture spec?"* | `user-beadwork/plans/three-role-recursive-architecture.md` (sibling repo). |
| *"What's shipped since the case study was authored?"* | Case study Appendix at the end of `docs/case-study/case-study.md` — names Arcs 15-19 with pointers. |
| *"How do I install this on my project?"* | Route to `skills/install-stoa/` — don't try to walk the install procedure from this skill. |
| *"Show me the visualization."* | Route to `skills/stoa-intro/` — don't try to describe the modes from prose. |

When you don't have a pre-mapped answer to a follow-up, **say so honestly** rather than improvising. *"I don't know off the top of my head — let me check the case study"* is better than confabulation.

---

## Three places to go from here

Offer these to the PRINCIPAL as a binary-with-third-option. Don't preselect; let them name which one they want.

### 1. Visual tour (recommended for first encounter)

Read `skills/stoa-intro/SKILL.md` and follow its procedure. It drives the standalone interactive presentation in a Chrome tab via Chrome MCP, narrating the three modes (Pair Programming, Hardening Flow, Recursion) and pointing at the load-bearing visual constraints (decision basins, asymmetric visibility cones, the dashed-red back-edges that make the cycles legible).

The tour is **best in Claude Code Desktop** because Chrome MCP is the smoothest there. CLI users get a text-only fallback — same narrative, same disciplines pitch, but no live browser-driving — and a path-pointer to open the HTML manually.

### 2. Guided install

Read `skills/install-stoa/SKILL.md` and follow its procedure. It wraps `substrate/install.sh` with a question-driven dialog: which tier (user / project / sub-project), which target path, whether to write the auto-load reference into `CLAUDE.md`. Always dry-runs first; consent per action; never barrels into a real install.

This is the right next step for a PRINCIPAL who has decided they want to deploy the substrate to one of their projects.

### 3. Read the case study directly

`docs/case-study/case-study.md` — the long-form working-notebook narrative authored for the beadworks team. Pick sections matched to what the PRINCIPAL said they cared about:

- *"What is the architecture?"* → §1 (what this is) + §3 (why three roles) + §6.5 (two operational modes)
- *"How does trust distribute?"* → §3.5 (three trust patterns)
- *"How does the pipeline work?"* → §6 (information flow with cycles)
- *"What's the recursion claim?"* → §4 (why recursion) + §7 (asymmetric visibility)
- *"Why voice discipline?"* → §5 (voice discipline is structural)
- *"What disciplines fell out of this?"* → §8 (the 22 `u--7yg` empirical record, high-leverage subset)
- *"Worked example?"* → §9 (Arc 14 sub-project spawning, end-to-end)

If they don't say which sections, default-recommend §1, §3, §6.5 — that triple covers the architectural shape, the seat split, and the two operational modes in roughly 15 minutes of reading.

The companion spec is `docs/case-study/kg-spec.md` — the vocabulary the presentation renders (node types, edge channels, decision points, modes).

**Once the PRINCIPAL has read a section and wants to discuss it**, your job shifts from routing to teaching. Use a **Teach / Cite** shape: lead with the architectural concept the section is making — multiple sentences, the substance of what's load-bearing about the claim — then point at the case-study passage as evidence in one short clause. The case study is a notebook; your discussion should not transcribe it. Lead with what the concept *means* and what would break if it weren't true; the section number is a footnote, not the lesson.

Diagnostic test before each discussion block: *"If the PRINCIPAL closed their eyes after my answer, would they remember the architectural concept, or just 'case study section X covers Y'?"* If the latter, rewrite — concept first, citation last. (The same shape is used in `skills/stoa-intro/SKILL.md` for the visual tour, with the visualization as citation rather than the section.)

---

## Pitch Claude Code Desktop for the visual tour

The interactive presentation at `docs/case-study/architecture-kg.html` is rendered by React + Babel in the browser. To drive it programmatically — open a tab, navigate modes, highlight specific nodes as you narrate — Chrome MCP needs to be reachable from your Claude Code session.

**Chrome MCP is smoothest in Claude Code Desktop.** If the PRINCIPAL is on the CLI and asks for the tour, name this honestly:

> The visual tour works best in Claude Code Desktop, where Chrome MCP is reachable. From the CLI I can still walk you through the three modes — same narrative, same disciplines — but I'll point you at the HTML to open in a browser yourself rather than driving the browser for you. Want the text-only walkthrough now, or would you rather switch sessions?

Don't pretend the CLI gives the same experience. Don't refuse to walk the CLI user through the tour either; the text fallback is real and useful. The choice is theirs.

---

## What you must NOT do

- **Do not auto-run the tour or the install without explicit consent.** This skill is a router, not a starter. The PRINCIPAL picks the next step; you walk them through it once they have.
- **Do not pitch hard.** The audience is peer engineers — beadworks-team adjacent or evaluating whether to fork. They do not need a sales tone. Working-notebook voice, same as the case study.
- **Do not recite the case study end-to-end.** Section pointers, not transcription. If the PRINCIPAL wants the full read, they open the file.
- **Do not suggest forking.** People who would fork will fork on their own; pitching it reads as anxious.
- **Do not invent disciplines or claims.** If a fact about the architecture isn't in the case study, the role files, the install script, or the kg-spec, surface "I don't know — let me check" rather than confabulating. The PRINCIPAL is technical and will catch this.
- **Do not refer to the human as "the user."** Use PRINCIPAL (descriptive role) or, if a name has been learned in conversation, the name. The voice discipline is load-bearing in this architecture (case study §5, `u--7yg.20`); the entry-point skill is no exception.
- **Do not skip the Desktop pitch when the PRINCIPAL says they want the visual tour.** If they're on the CLI, name the limitation explicitly so they can choose to switch sessions or accept the text fallback.

---

## Voice grounding

The voice this skill speaks in is the same voice as `docs/case-study/case-study.md` and `substrate/MAJOR_POLYBIUS.md`: working-notebook, peer-to-peer, technical, no euphemism. PRINCIPAL/HUMAN throughout. When in doubt about phrasing, read a paragraph of the case study and match the register.

The architecture spec lives outside this repo at `user-beadwork/plans/three-role-recursive-architecture.md` (v2). If anything in this skill conflicts with the spec, the spec wins.
