---
name: "write-skill"
description: "Use when creating, editing, or improving Claude Code skills (SKILL.md files). Also use when a skill isn't triggering reliably or needs restructuring."
---

# Writing Claude Code Skills

A skill is a folder that Claude explores, not a file it reads. The SKILL.md is the entrypoint, but `scripts/`, `references/`, and `assets/` around it are just as important. Skills load through progressive disclosure: descriptions are always present, the body loads when triggered, and supporting files load only when Claude reads them.

## Step 1: Choose a Purpose

Every skill fits one purpose category. Choosing the right one shapes what the skill contains and how it should be structured.

| Category | What It Does | Examples |
|---|---|---|
| Library / API Reference | Teaches Claude about internal tools, APIs, SDKs | MCP server docs, internal API patterns |
| Product Verification | Pairs with testing frameworks to confirm code works | TDD workflows, integration test runners |
| Data Fetching | Connects to monitoring/data stacks with credential handling | Metrics dashboards, event source queries |
| Business Process | Automates workflows, keeps logs for consistency | PR workflows, deployment checklists |
| Code Scaffolding | Generates boilerplate where templates alone aren't enough | Project setup, component generators |
| Code Quality | Enforces standards, sometimes spawning adversarial subagents | Linting, audit dispatchers |
| CI/CD | Babysits PRs, retries flaky tests, resolves merge conflicts | PR monitors, build fixers |
| Runbook | Walks through multi‑tool investigations from a symptom | Incident response, debugging playbooks |
| Infrastructure Operations | Finds orphaned resources, posts findings, executes cascading cleanup | Resource cleanup, environment provisioning |

The best skills fit one category cleanly. Confusing skills straddle several.

Then choose a **structural pattern** based on how the skill teaches:

| Structure | Examples | Key Patterns |
|---|---|---|
| Discipline | TDD, verification | Iron Laws, rationalization tables, red‑flags lists |
| Technique | debugging, research | Templates, reference tables, step‑by‑step procedures |
| Workflow | planning, execution | Flowcharts, cross‑references, integration sections |
| Reference | API docs, tools | Architecture diagrams, comparison tables |

Purpose (what the skill does) × Structure (how it teaches) = the design space.

## Step 2: Name and Structure

```
skill-name/
  SKILL.md              # Required – frontmatter + instructions
  scripts/              # Executable code (runs without consuming context)
  references/           # Documentation loaded into context as needed
  assets/               # Templates, config files, icons
```

- **Name**: kebab‑case, max 64 chars, must match directory name
- Use gerunds for processes: `creating-skills`, `testing-hooks`
- Avoid vague names: `helper`, `utils`, `tools`

**Claude does NOT auto‑explore skill folders.** It follows explicit references in SKILL.md only. Every file in `scripts/`, `references/`, and `assets/` must be enumerated in the body or Claude won't know it exists. Keep references one level deep – if `advanced.md` references `details.md`, Claude may only partially read the second file.

**Scripts are first‑class.** The most powerful thing you can put in a skill folder is code. Scripts execute and return results without their source code occupying context. A validation script, a language detector, a test runner – these preserve context for reasoning while delegating deterministic work to code.

## Step 3: Write the Description

The description is how Claude decides whether to load your skill. This is the highest‑leverage part of skill authoring.

**Rules:**
1. **Start with "Use when..."** – triggering conditions only
2. **Include trigger keywords** – words and phrases users would actually say, error messages they'd encounter, symptoms they'd describe
3. **Be aggressively specific** – "Use when tests have race conditions" not "For async testing"
4. **Make it pushy** – Claude undertriggers skills. Include contexts like "even if they don't explicitly ask for X"
5. **NEVER summarize the workflow**

```yaml
# BAD: Summarizes workflow
description: Use for TDD - write test first, watch it fail, write minimal code, refactor

# GOOD: Triggering conditions only
description: Use when implementing any feature or bugfix, before writing implementation code
```

**Debug triggers:** Ask Claude "When would you use the [skill name] skill?" It quotes the description back. Adjust based on what's missing.

**Limits:** Max 1024 characters per description. All descriptions share a budget of ~2 % of the context window (fallback 16K chars, ~30‑40 skills at ~100 words each). Exceeding the budget causes silent truncation – skills vanish without warning. Run `/context` to check.

## Step 4: Design the Content

### Start with Gotchas

**Gotchas are the highest‑signal content in any skill.** A skill without a gotchas section hasn't been used enough. Gotchas are built from observed failure points – the specific, concrete ways Claude goes wrong without guidance.

```markdown
## Gotchas

### Claude will try to mock the database
When tests touch persistence, Claude defaults to mocking. This burned us last quarter when mocked tests passed but the production migration failed because mocks diverged from the actual schema. Always use the real test database.

### The retry logic swallows connection errors
Claude's default error handling catches too broadly. Connection errors in the job queue must propagate to trigger the circuit breaker. Catch only ValueError and ValidationError – let everything else raise.
```

Each gotcha explains what happens, why it's wrong, and what to do instead.

### Explain the Why, Not MUSTs

Claude has theory of mind. When it understands *why* a practice matters – the incident that motivated the rule, the failure mode it prevents – it handles edge cases that rigid constraints miss.

If you find yourself writing ALWAYS or NEVER in capitals, that's a signal to stop and ask whether the reasoning can be explained instead.

### Push Past Defaults

Effective skill content pushes Claude out of its default patterns, not back into them. Focus on:
- Company‑specific conventions Claude can't know
- Counter‑intuitive best practices that contradict Claude's training
- Domain knowledge that only comes from experience with this codebase
- Patterns Claude consistently gets wrong without guidance

### Match Structure to Skill Type

**Discipline skills** need anti‑rationalization mechanisms:
1. Rationalization table – maps common excuses to reality checks
2. Red‑flags list – thoughts that mean "stop"
3. Explicit loophole closure – forbid specific workarounds Claude might exploit
4. One Iron Law – a non‑negotiable statement that anchors the entire discipline

**Technique skills** need templates, reference tables, and step‑by‑step procedures.

**Workflow skills** need cross‑references between phases, integration points with other skills, and clear handoff criteria.

**Reference skills** need comparison tables, architecture diagrams, and context for when each option is appropriate.

### Quality Markers

| Marker | Excellent | Mediocre |
|---|---|---|
| Agent internal state | Red‑flags map thoughts to actions | Rules without self‑monitoring |
| Empirical grounding | "24 failures", "6 iterations" | No evidence of real use |
| Executable algorithms | Pseudocode, templates, checklists | Abstract principles only |
| Good/Bad comparisons | Side‑by‑side with explanation | One example or none |
| Scope boundaries | Explicit "when NOT" with reasoning | Missing or vague |

## Step 5: Organize for Progressive Disclosure

Skills load in three stages with dramatically different costs:

| Level | What Loads | When | Token Impact |
|---|---|---|---|
| 1 | Name + description | Always | ~100 tokens per skill |
| 2 | SKILL.md body | When skill triggers | ~1‑2 % of context |
| 3 | Referenced files | When Claude reads | On‑demand only |

**The file system IS the progressive disclosure mechanism.** Put the core workflow in SKILL.md. Put heavy reference material in `references/`. Put executable tools in `scripts/`.

### The Routing Pattern

When a domain has many subspecialties, consolidate descriptions and route to reference files:

```markdown
## Language‑Specific References

Read the appropriate reference based on the project:
- Swift code (.swift) → `references/swift.md`
- TypeScript/React (.ts, .tsx) → `references/typescript.md`
- C++ (.cpp, .h) → `references/cpp.md`
- PostgreSQL queries → `references/postgres.md`
```

## Step 6: Test and Iterate

### Testing
1. **Triggering** – does the skill activate on relevant queries? Target 90 % on a test set.
2. **Functional** – does Claude follow the instructions correctly? Use Given/When/Then format.
3. **Performance** – compare runs with‑skill vs without‑skill; track pass rate, token usage, tool calls.

### Skills Evolve Through Use

1. Draft → Test → Observe → Add Gotchas → Test again → Periodic review.

## Step 7: Deploy

1. Create the skill directory in the appropriate location:
   - Global: `~/.claude/skills/skill-name/`
   - Project: `.claude/skills/skill-name/`
   - Plugin: `skills/skill-name/` within the plugin structure
2. Verify the skill appears in `/context` on next conversation start.
3. Check budget – ensure other skills aren't being truncated.

## Frontmatter Quick Reference

```yaml
---
name: skill-name          # kebab‑case, max 64 chars, must match directory
description: Use when ... # Max 1024 chars, triggering conditions only
---
```

Optional fields include `user-invocable`, `disable-model-invocation`, `context`, `model`, `allowed-tools`, and `hooks`.

## Additional Resources
- `references/frontmatter.md` – complete frontmatter fields
- `references/routing-pattern.md` – complex organization and composability
- `references/evaluation.md` – description optimization loops and benchmarking
- `references/hooks.md` – event‑handler hooks

## Common Mistakes

| Mistake | Fix |
|---|---|
| Description summarizes workflow | Description = triggering conditions only |
| No gotchas section | Add observed failure points as the first maintenance pass |
| Skill too long (500+ lines) | Move reference material to `references/` |
| No trigger keywords | Add error messages, symptoms, tool names to description |
| Vague description | "Use when tests have race conditions" not "For testing" |
| Multi‑language examples | One excellent example in the most relevant language |
| No scope boundaries | Add "When NOT to use" section |
| States the obvious | Focus on what Claude gets wrong, not what it already knows |
| ALWAYS/NEVER without reasoning | Explain why – Claude handles edge cases better with context |
| Narrative storytelling | Convert to patterns, tables, checklists |
| Files not enumerated in SKILL.md | Claude won't discover unenumerated files |
| Nested file references | Keep references one level deep from SKILL.md |
| Write‑once, never revised | Skills evolve through gotchas, testing, periodic review |
| Untested skill | Test triggering + functional + performance |
