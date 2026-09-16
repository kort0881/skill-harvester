---
name: "humanize"
description: "Detect and remove AI‑generated writing patterns from prose, producing a natural, human‑like rewrite. The skill scans for 41 known patterns, applies statistical tells, and supports voice calibration based on a user‑provided writing sample."
---

# Humanize – Remove AI Writing Patterns

## Overview
The **humanize** skill acts as a writing editor that identifies AI‑style artifacts and rewrites text to sound natural. It merges pattern catalogs from several open‑source projects and adds statistical signals (burstiness, type‑token ratio, etc.).

## How to Invoke
| Mode | Input | Output |
|------|-------|--------|
| **Pasted text** (default) | Raw text supplied in the conversation | Draft audit, bullet‑point list of detected patterns, and final rewritten text |
| **File mode** | Path to a markdown/text file | In‑place rewrite (git‑aware) with a short change summary |
| **Repo audit mode** | Directory path | Ranking of files by AI‑flavor, dominant patterns per file, optional batch rewrite |
| **Embedded mode** | Text supplied by another agent | Only the final rewritten text (no audit) |

## Process
1. **Scan** the input for the 41 patterns listed below and compute statistical tells.
2. **Draft** a rewrite that removes the patterns while preserving all factual information.
3. **Audit** – produce a bullet list of each detected pattern and the change applied.
4. **Finalize** – apply the audit fixes, ensure no em‑dash or en‑dash characters remain (unless a user sample explicitly uses them), and output the final text.

## Voice Calibration (optional)
If the user provides a writing sample:
1. Analyse sentence length, vocabulary, punctuation, recurring phrases, and transitions.
2. Mirror those habits in the rewrite, overriding default style rules (e.g., em‑dash usage).
If no sample is given, the default style rules apply.

## Pattern Catalog (selected examples)
### 1. Significance inflation
*Watch for*: “pivotal moment”, “crucial role”, “underscores its importance”.
*Fix*: Remove exaggerated framing while keeping the fact.
### 2. Notability name‑dropping
*Watch for*: Lists of media outlets without context.
*Fix*: Keep only citations that the source actually provides.
### 3. Superficial –ing analyses
*Watch for*: “…symbolizing…”, “…reflecting…”.
*Fix*: Replace with concrete description.
### 4. Promotional language
*Watch for*: “vibrant”, “groundbreaking”, “state‑of‑the‑art”.
*Fix*: Use neutral wording.
### 5. Vague attributions
*Watch for*: “Experts believe…”, “Industry reports say…”.
*Fix*: Cite a real source or drop the claim.
… *(the remaining 36 patterns are included in the full skill document)*

## Statistical Tells
| Signal | Human | AI |
|--------|-------|----|
| Burstiness (sentence‑length variation) | High | Low |
| Type‑token ratio | 0.5‑0.7 | 0.3‑0.5 |
| Trigram repetition | Low | High |
| Paragraph uniformity | Varied | Even |

When rewriting, explicitly vary sentence length, avoid synonym cycling, and keep paragraph sizes uneven.

## Verification
The bundled `sloplint` CLI (if installed) can be used to measure the four statistical tells:
```bash
sloplint scan <file-or-dir>
```
Run it on the draft and on the final rewrite; the final version should show higher burstiness and a higher type‑token ratio.

## Output Formats
* **Default (pasted text)** – returns a JSON object with three fields: `draft`, `audit` (array of pattern‑change strings), and `final`.
* **File / Repo modes** – writes the final text back to the file(s) and prints a concise markdown table summarising changes.
* **Embedded** – prints only the `final` string.

## Safety & Ethics
* Never fabricate facts. If a claim requires external detail that is not present, either ask the user for clarification or omit the detail.
* Respect the author’s voice: only add personality when the content type (blog, essay, personal) calls for it.
* The skill does **not** modify code blocks, front‑matter, or link targets.

---
