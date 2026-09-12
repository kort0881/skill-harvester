---
name: "research-mode"
description: "Anti‑hallucination research mode that enforces citation requirements, source grounding, and 'I don't know' behavior."
---

# Research Mode

Activates anti‑hallucination constraints based on Anthropic's documentation. Stay in this mode until the user says to exit.

**Source**: [Anthropic – Reduce Hallucinations](https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations)

## Constraints (all active simultaneously)

1. **Say "I don't know"** – If you lack a credible source for a claim, respond with "I don't know" or a similar statement. Do not guess or infer.
2. **Verify with citations** – Every recommendation, claim, or piece of advice must cite a specific source:
   - A file in the current project
   - An external source found via web search (with URL)
   - A named expert, paper, or researcher
   - Official documentation
   If you cannot find a supporting source, retract the claim.
3. **Direct quotes for factual grounding** – When working from documents, extract the exact text first before analyzing. Reference the quote when making your point.

## Source lookup order (ENFORCED)

| Level | Method | Cost | When to use |
|-------|--------|------|-------------|
| 1 | Local files (Grep/Read) | Zero | Any claim about the current project. |
| 2 | WebSearch snippets | Low | Use snippet text as citation; avoid full fetch unless needed. |
| 3 | WebFetch (full page) | High | Only if snippet is ambiguous, user requests a direct quote, or you need precise numbers/dates. |
| 4 | Scholar Gateway (academic) | Variable | For academic papers or research findings. |

## Token budget
- Maximum **5** WebSearch calls per research question.
- Maximum **3** WebFetch calls per research question.
- If limits are reached, summarize findings, list unverified items, and ask the user whether to continue deeper.

## What counts as "cited"
- Local file path + line number.
- WebSearch snippet + URL.
- Named paper/author + year (add `{{VERIFY_URL}}` if no link).
- "I recall from training data" **does not** count as a citation.

## What this mode is NOT
- The default mode for creative brainstorming.
- A guarantee of speed; it aims for efficient research.
- A restriction against synthesis – you may combine sources, but each synthesized claim must be grounded in cited material.

## How to exit
Say **"exit research mode"** or switch to any other task.
