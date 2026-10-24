---
name: "create-skills"
description: "Guide for authoring Claude SKILL.md files, covering intent capture, anatomy, description writing, body composition, testing, packaging, and common pitfalls."
---

# Creating Claude Skills

Skills are reusable instruction sets that teach Claude how to perform specific tasks consistently and well. A skill is a folder with a `SKILL.md` file and optional supporting resources. When triggered, Claude reads the `SKILL.md` and follows its instructions.

## When to Create a Skill

Create a skill when:
- A task needs **consistent, repeatable execution** across many conversations
- The task involves **specific tools, sequences, or output formats** that Claude wouldn't know by default
- You've iterated on a workflow manually and want to **capture what works**
- The instructions are too detailed to repeat every time but too important to leave to chance

Don't create a skill when:
- A simple prompt gets the job done
- The task is a one‑off
- The behavior is already built into Claude

## Workflow

```
1. Capture Intent → 2. Research & Interview → 3. Draft SKILL.md →
4. Test with real prompts → 5. Refine → 6. Package & deliver
```

## Step 1: Capture Intent

Answer these four questions:
1. **What should the skill enable Claude to do?**
2. **When should it trigger?**
3. **What's the expected output?**
4. **Are the outputs objectively verifiable?**

If the conversation already contains a workflow, extract the tools, sequence, and input/output formats. Fill gaps with targeted questions.

## Step 2: Skill Anatomy

```
skill-name/
├── SKILL.md              ← Required. The instruction file.
│   ├── YAML frontmatter   (name + description)
│   └── Markdown body      (instructions)
│
└── Optional resources/
    ├── scripts/           Executable code for deterministic tasks
    ├── references/        Docs loaded into context as needed
    └── assets/            Templates, icons, fonts used in output
```

**Do not include** human‑focused docs like `README.md`.

### Progressive Disclosure (Three‑Level Loading)
| Level | What | When loaded | Size guidance |
|-------|------|-------------|---------------|
| **1. Metadata** | `name` + `description` in YAML frontmatter | Always | ~100 words |
| **2. SKILL.md body** | Full markdown instructions | When skill triggers | <500 lines ideal |
| **3. Bundled resources** | Scripts, references, assets | On‑demand via explicit read | Unlimited |

## Step 3: Writing the YAML Frontmatter

### `name`
A short, lowercase, hyphenated identifier (e.g., `docx`, `frontend-design`).

### `description` (Critical)
The description is the primary trigger. Use a “pushy” style that lists primary and secondary trigger phrases and explicit exclusions.

**Template**
```yaml
description: >
  [What the skill does — 1 sentence].
  Use this skill when [primary triggers].
  Also use when [secondary triggers].
  Covers [key capabilities].
  Do NOT use for [explicit exclusions].
```

**Checklist**
- States what the skill does
- Lists explicit trigger phrases
- Includes secondary triggers
- Mentions relevant file types/extensions
- Provides exclusions
- Slightly “pushy” to avoid under‑triggering

## Step 4: Writing the SKILL.md Body

### Structure Patterns
| Pattern | Best for |
|---------|----------|
| Workflow‑based | Sequential processes |
| Task‑based | Distinct operations |
| Reference/Guidelines | Standards, specs |
| Capabilities‑based | Integrated systems |

### Writing Principles
- Use **imperative** form.
- **Explain the WHY**, not just the WHAT.
- Avoid heavy‑handed `MUST`/`NEVER`; provide reasoning.
- Include **few‑shot examples**.
- Define output formats explicitly.

**Example of a few‑shot section**
```markdown
## Commit message format

**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT‑based authentication

**Example 2:**
Input: Fixed crash when uploading files over 10MB
Output: fix(upload): handle large file uploads without crash
```

### Organizing Large Skills
If the body exceeds ~500 lines, move detailed content to `references/` files and point to them from the main `SKILL.md`.

### Scripts & Assets
Scripts handle deterministic tasks (e.g., file conversion). Assets hold static templates, fonts, icons, etc.

## Step 5: Testing

Create 2‑3 realistic test prompts that a user would actually say. Verify:
1. Skill triggers correctly
2. Claude follows the instructions
3. Output quality meets expectations
4. Edge cases are handled

Optionally, add an `evals/evals.json` file for structured evaluation.

## Step 6: Common Pitfalls & Fixes
| Pitfall | Fix |
|---------|-----|
| Skill never triggers | Make description more explicit and “pushy” |
| Skill triggers on wrong requests | Add clear exclusions |
| Claude ignores instructions | Add few‑shot examples |
| Output format inconsistent | Provide exact template |
| SKILL.md too long | Split into `references/` files |
| Skill too rigid | Replace MUST/NEVER with reasoning |
| Skill only works for test examples | Generalize principles |
| Wasted steps | Remove unproductive instructions |

## Step 7: Packaging & Delivery
1. Verify folder structure and valid YAML frontmatter.
2. Check all referenced files exist.
3. Copy the skill folder to the output directory.
4. Present a brief summary and installation steps.
5. (Optional) Run `scripts/package_skill.py <path/to/skill-folder>` to create a `.skill` archive.

---

**Quick Reference**: A ready‑to‑use template is available at `templates/skill-template.md` within the skill folder.

---

**Meta‑Advice for Skill Authors**
- Spend most time perfecting the description.
- Explain reasoning, not just rules.
- Draft, then revisit with fresh eyes.
- Generalize from specific feedback.
- Keep the skill lean and focused.
- Aim for broad applicability.
- Set high standards; Claude can meet them.
