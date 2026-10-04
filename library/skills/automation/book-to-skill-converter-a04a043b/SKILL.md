---
name: "book-to-skill"
description: "Converts books and documents (PDF, EPUB, DOCX, HTML, Markdown, plain text, RTF, MOBI/AZW with Calibre) into structured agent skills that extract deterministic decision‑logic as First Principles and Standard Operating Procedures (SOPs). Use when the user wants to operationalize an author's method into executable step‑by‑step procedures, apply it while working, or build a reusable decision base from a file."
---

# Book-to-Skill Converter

Transform written knowledge into actionable agent skills by extracting structure — not producing summaries.

## Philosophy

Books hide deterministic decision‑logic inside prose. This skill extracts that logic as two artifacts: **First Principles** (the irreducible truths the author's method rests on) and **Standard Operating Procedures** (the executable step‑by‑step the author actually uses).

- **Extract logic, not prose.** A skill is not a book report — it is a decision engine.
- **ANTI‑FABRICATION RULE.** Convert content into an SOP *only when the author provides procedural substance*. When the author is probabilistic or heuristic, capture it as a **Heuristic** (an if‑then under uncertainty), **NOT** a fabricated deterministic SOP. Never invent steps, thresholds, or ordering the source does not contain. Every SOP and every Principle must be traceable to its chapter.
- **First Principle admission rubric.** A line qualifies ONLY if it is:
  1. an *assertion* (a claim, not a topic);
  2. *causal or foundational* — other ideas in the book derive from it;
  3. *irreducible* — it cannot be decomposed into a more basic claim from the same book.
  Format: claim + the "because" + what it lets you stop debating.
- **Preserve the author's precision.** Exact framework names, exact thresholds. A named procedure keeps its name.
- **Layer depth appropriately.** Simple books → simple skills. Dense books → reference files and on‑demand chapters.

---

## Modes of Operation

1. **Full Conversion (Default)** – Run Steps 0‑9, output complete skill directory.
2. **Analyze Only** – Run Steps 0‑3, produce a structured extraction report, stop before generating files.
3. **Generate from Prior Analysis** – Skip Steps 0‑3, use provided analysis, run Steps 4‑9.
4. **Update / Fold‑in** – Detect existing skill, run a reduced workflow to merge new content.

---

## Step 0 – Out‑of‑Scope Check

If no arguments are provided, respond with:
```
book-to-skill requires a supported document path, folder, or glob pattern. Usage: `book-to-skill <path‑to‑document‑folder‑or‑glob>... [skill‑name‑slug]`
```
Identify `INPUT_PATHS` and optional `SKILL_NAME`. If any `INPUT_PATHS` point to an existing skill directory or `SKILL_NAME` matches a skill in `SKILLS_HOME`, treat the run as **Update/Fold‑in** (Mode 4).

---

## Step 1 – Validate Input

Ensure at least one supported file, directory, or glob is present. Supported extensions: `.pdf .epub .docx .txt .md .markdown .rst .adoc .html .htm .rtf .mobi .azw .azw3`. Abort with a clear error if none are found.

---

## Step 1.5 – Identify Content Type

Ask the user to choose the content type (technical, text‑heavy, transcript, or not‑sure). Store as `BOOK_TYPE` and inform the user which extractor will be used.

---

## Step 2 – Extract Text

Locate `extract.py` in the possible skill roots, then run:
```bash
PYTHON_BIN="${PYTHON_BIN:-python3}"
"$PYTHON_BIN" "$SCRIPT_PATH" $INPUT_PATHS --mode $BOOK_TYPE --install-missing ask
```
The script produces `full_text.txt` and `metadata.json` in a temporary work directory.

---

## Step 2.5 – Pre‑flight Cost Estimate

Read `metadata.json`, compute token estimates, display an estimate table, and ask the user to confirm proceeding (or switch to *Analyze Only*).

---

## Step 2.6 – REPL‑style Access for Large Books

For books > 50 k tokens, advise using `grep`/`sed` with line offsets instead of loading the whole file into context.

---

## Step 3 – Analyze Book Structure

- **Transcript mode** – Detect course title, instructor, timestamps, and segment by module markers.
- **Technical/Text mode** – Read the first 8 k characters to find title, author, chapter headings, and TOC.

If in *Analyze Only* mode, output an Extraction Report and stop.

---

## Step 4 – Ask Purpose (Full Conversion only)

Prompt the user to select the intended use (apply SOPs, think with models, reference chapters, or all). Derive `DEPTH` (`reference` vs `study`).

---

## Step 5 – Determine Skill Name

If a slug was supplied, use it; otherwise propose two options (author‑concept and title‑based) and let the user choose.

---

## Step 5.5 – Lineage Detection (optional Set membership)

Search existing skills for the same author. If matches are found, ask the user whether the new book belongs to that lineage and obtain a publication year if applicable. Update or create a set manifest after generation.

---

## Step 6 – Create Skill Directory

```bash
mkdir -p "$SKILLS_HOME/$SKILL_NAME/chapters"
```

---

## Step 7 – Generate Chapter Summaries

Apply a token‑budget matrix based on `BOOK_TYPE` and `DEPTH`. For each chapter (or transcript module) create a markdown file:
```markdown
# Chapter N: <Full Title>

## Core Idea
<1‑2 sentence summary>

## First Principles
- **<Principle>** — because <reason>

## Standard Operating Procedures
- **<SOP Name>**: <trigger / steps / failure modes>

## Heuristics
- **<Heuristic>**: <why it matters>

## Worked Example (only for study depth)
<concrete example from the source>
```
Technical books add a **Code Examples** section; transcript modules also include a `## Timestamp` and optional `## Visual Reference`.

---

## Step 8 – Glossary & First Principles File

Aggregate all extracted principles, definitions, and terminology into `glossary.md` and `first_principles.md` at the skill root.

---

## Step 9 – Finalize Skill Metadata

Create `SKILL.md` with front‑matter containing:
- `name`
- `description`
- `source_title`
- `source_author`
- `source_date` (from lineage step if applicable)
- `book_type`
- `depth`
- `generated_at`

Add a short **Core** section summarizing the most important SOPs and principles based on the user's purpose selection.

---

## Step 9.7 – Optional Temporal Evolution Audit

If the skill belongs to a set with ≥ 2 members, offer to run an audit that compares principles across versions and highlights evolution.

---

*End of Book‑to‑Skill Converter workflow.*
