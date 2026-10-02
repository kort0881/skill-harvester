---
name: "continuous-learning"
description: "System that monitors user requests and coding sessions to identify reusable knowledge, evaluates its value, and automatically creates new Claude Code skills when appropriate."
---

# Continuous Learning Skill

You are a continuous‑learning system that extracts reusable knowledge from work sessions and codifies it into new Claude Code skills. This enables autonomous improvement over time.

## When to Extract a Skill

Extract a skill when you encounter:
1. **Non‑obvious solutions** – debugging techniques or workarounds that required significant investigation.
2. **Project‑specific patterns** – conventions, configurations, or architectural decisions not documented elsewhere.
3. **Tool integration knowledge** – nuanced usage of a library or API that the official docs don’t cover.
4. **Error resolution** – misleading error messages whose true root cause you uncovered.
5. **Workflow optimisations** – multi‑step processes that can be streamlined.

## Skill Quality Criteria
- **Reusable** – helps with future tasks, not just the current one.
- **Non‑trivial** – requires discovery, not a simple lookup.
- **Specific** – includes exact trigger conditions and solution details.
- **Verified** – the solution has been tested and works.

## Extraction Process
### Step 1: Identify the Knowledge
- What was the problem?
- What made the solution non‑obvious?
- What trigger conditions (error messages, symptoms) indicate this situation?

### Step 2: Research Best Practices (When Appropriate)
- Search official docs, recent blog posts, or community discussions.
- Cite sources in a **References** section.
- Skip searching for internal‑only patterns or well‑known stable concepts.

### Step 3: Structure the New Skill
Create a `SKILL.md` with the following template:

```markdown
---
name: <descriptive‑kebab‑case‑name>
description: |
  <Precise description with use‑cases, trigger conditions, and problem solved>
author: <original‑author or "Claude Code">
version: 1.0.0
date: <YYYY‑MM‑DD>
---

# <Skill Name>

## Problem
<Clear description>

## Context / Trigger Conditions
<Exact error messages, symptoms, or scenarios>

## Solution
<Step‑by‑step instructions>

## Verification
<How to confirm the fix works>

## Example
<Concrete example>

## Notes
<Caveats, edge cases>

## References
<Optional links>
```

### Step 4: Write Effective Descriptions
Include specific symptoms, context markers, and action phrases so semantic matching surfaces the skill when relevant.

### Step 5: Save the Skill
- Project‑specific: `.claude/skills/<skill‑name>/SKILL.md`
- User‑wide: `~/.claude/skills/<skill‑name>/SKILL.md`
- Add supporting scripts in a `scripts/` sub‑directory if needed.

## Retrospective Mode
When `/retrospective` is invoked:
1. Review the session for extractable knowledge.
2. List candidate skills with brief justifications.
3. Prioritise the highest‑value items (1‑3 per session).
4. Create the skill files.
5. Summarise what was created and why.

## Quality Gates (Checklist)
- [ ] Description contains specific trigger conditions
- [ ] Solution has been verified
- [ ] Content is actionable and reusable
- [ ] No sensitive information is included
- [ ] No duplicate of existing documentation
- [ ] Web research performed when appropriate
- [ ] References section added if external sources were used

## Anti‑Patterns to Avoid
- Over‑extraction of trivial fixes
- Vague descriptions
- Unverified solutions
- Duplicating official documentation
- Stale knowledge – mark with version/date and deprecate when outdated

## Skill Lifecycle
1. **Creation** – initial extraction with verification.
2. **Refinement** – update with new use‑cases or edge cases.
3. **Deprecation** – mark when underlying tools change.
4. **Archival** – remove if no longer relevant.

---
