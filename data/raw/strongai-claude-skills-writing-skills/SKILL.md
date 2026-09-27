---
name: write-skill
description: Use when creating, editing, or improving Claude Code skills (SKILL.md files). Also use when a skill isn't triggering reliably or needs restructuring.
---

# Writing Claude Code Skills

A skill is a folder that Claude explores, not a file it reads. The SKILL.md is the entrypoint, but `scripts/`, `references/`, and `assets/` around it are just as important. Skills load through progressive disclosure: descriptions are always present, the body loads when triggered, and supporting files load only when Claude reads them.

## Step 1: Choose a Purpose

Every skill fits one purpose category. Choosing the right one shapes what the skill contains and how it should be structured.

| Category                  | What It Does                                                         | Examples                                   |
| ------------------------- | -------------------------------------------------------------------- | ------------------------------------------ |
| Library / API Reference   | Teaches Claude about internal tools, APIs, SDKs                      | MCP server docs, internal API patterns     |
| Product Verification      | Pairs with testing frameworks to confirm code works                  | TDD workflows, integration test runners    |
| Data Fetching             | Connects to monitoring/data stacks with credential handling          | Metrics dashboards, event source queries   |
| Business Process          | Automates workflows, keeps logs for consistency                      | PR workflows, deployment checklists        |
| Code Scaffolding          | Generates boilerplate where templates alone aren't enough            | Project setup, component generators        |
| Code Quality              | Enforces standards, sometimes spawning adversarial subagents         | Linting, audit dispatchers                 |
| CI/CD                     | Babysits PRs, retries flaky tests, resolves merge conflicts          | PR monitors, build fixers                  |
| Runbook                   | Walks through multi-tool investigations from a symptom               | Incident response, debugging playbooks     |
| Infrastructure Operations | Finds orphaned resources, posts findings, executes cascading cleanup | Resource cleanup, environment provisioning |

The best skills fit one category cleanly. Confusing skills straddle several.

Then choose a **structural pattern** based on how the skill teaches:

| Structure  | Examples            | Key Patterns                                         |
| ---------- | ------------------- | ---------------------------------------------------- |
| Discipline | TDD, verification   | Iron Laws, rationalization tables, red-flags lists   |
| Technique  | debugging, research | Templates, reference tables, step-by-step procedures |
| Workflow   | planning, execution | Flowcharts, cross-references, integration sections   |
| Reference  | API docs, tools     | Architecture diagrams, comparison tables             |

Purpose (what the skill does) x Structure (how it teaches) = the design space.

## Step 2: Name and Structure

```
skill-name/
  SKILL.md              # Required -- frontmatter + instructions
  scripts/              # Executable code (runs without consuming context)
  references/           # Documentation loaded into context as needed
  assets/               # Templates, config files, icons
```

- **Name**: kebab-case, max 64 chars, must match directory name
- Gerunds for processes: `creating-skills`, `testing-hooks`
- Avoid vague names: `helper`, `utils`, `tools`

**Claude does NOT auto-explore skill folders.** It follows explicit references in SKILL.md only. Every file in `scripts/`, `references/`, and `assets/` must be enumerated in the body or Claude won't know it exists. Keep references one level deep -- if `advanced.md` references `details.md`, Claude may only partially read the second file.

**Scripts are first-class.** The most powerful thing you can put in a skill folder is code. Scripts execute and return results without their source code occupying context. A validation script, a language detector, a test runner -- these preserve context for reasoning while delegating deterministic work to code. When test runs reveal Claude independently writing the same helper script across sessions, that's a signal to bundle it in `scripts/`.

## Step 3: Write the Description

The description is how Claude decides whether to load your skill. This is the highest-leverage part of skill authoring.

**Rules:**
1. **Start with "Use when..."** -- triggering conditions only
2. **Include trigger keywords** -- words and phrases users would actually say, error messages they'd encounter, symptoms they'd describe
3. **Be aggressively specific** -- "Use when tests have race conditions" not "For async testing"
4. **Make it pushy** -- Claude undertriggers skills. Include contexts like "even if they don't explicitly ask for X"
5. **NEVER summarize the workflow**

**Why rule 5 matters:** A description saying "dispatches subagent per task with code review between tasks" caused Claude to perform ONE review, even though the body specified TWO. Claude treated the description as sufficient instruction and never read deeply enough into the body to discover the second review. Changing to pure triggering conditions fixed it. The description says *when* to activate. The body says *what* to do.

```yaml
# BAD: Summarizes workflow
description: Use for TDD - write test first, watch it fail, write minimal code, refactor

# GOOD: Triggering conditions only
description: Use when implementing any feature or bugfix, before writing implementation code
```

**Debug triggers:** Ask Claude "When would you use the [skill name] skill?" It quotes the description back. Adjust based on what's missing.

**Limits:** Max 1024 characters per description. All descriptions share a budget of ~2% of context window (fallback 16K chars, ~30-40 skills at ~100 words each). Exceeding the budget causes silent truncation -- skills vanish without warning. Run `/context` to check.

For rigorous description optimization, see `references/evaluation.md`.

## Step 4: Design the Content

### Start with Gotchas

**Gotchas are the highest-signal content in any skill.** A skill without a gotchas section hasn't been used enough. Gotchas are built from observed failure points -- the specific, concrete ways Claude goes wrong without guidance.

A gotcha is NOT a generic best practice. It is a particular mistake that was actually observed, described precisely enough that Claude can recognize when it's about to make the same mistake. Add gotchas as the first section of a new skill and make them the primary focus of every maintenance pass.

```markdown
## Gotchas

### Claude will try to mock the database
When tests touch persistence, Claude defaults to mocking. This burned us last quarter
when mocked tests passed but the production migration failed because mocks diverged
from the actual schema. Always use the real test database.

### The retry logic swallows connection errors
Claude's default error handling catches too broadly. Connection errors in the job
queue must propagate to trigger the circuit breaker. Catch only ValueError and
ValidationError -- let everything else raise.
```

Each gotcha explains what happens, why it's wrong, and what to do instead. The "why" is what gives Claude the judgment to handle edge cases the gotcha doesn't explicitly cover.

### Explain the Why, Not MUSTs

Claude has theory of mind. When it understands *why* a practice matters -- the incident that motivated the rule, the failure mode it prevents -- it handles edge cases that rigid constraints miss.

A rule that says "NEVER mock the database in these tests" is less effective than explaining that last quarter, mocked tests passed while a production migration broke because the mocks diverged from the actual schema. The explanation carries the rule AND the judgment about when it applies.

If you find yourself writing ALWAYS or NEVER in capitals, that's a signal to stop and ask whether the reasoning can be explained instead. Reserve imperative constraints for genuine non-negotiables where the reasoning is too subtle or the consequences too severe to leave to judgment.

### Push Past Defaults

Effective skill content pushes Claude out of its default patterns, not back into them. Restating what Claude already knows wastes context. Focus on:

- Company-specific conventions Claude can't know
- Counter-intuitive best practices that contradict Claude's training
- Domain knowledge that only comes from experience with this codebase
- Patterns Claude consistently gets wrong without guidance

If the skill content matches what Claude would do anyway, it's not earning its budget.

### Match Structure to Skill Type

**Discipline skills** need anti-rationalization mechanisms because Claude will find convincing reasons to skip the hard parts:

1. **Rationalization table** -- maps common excuses to reality checks ("The test is trivial" -> "Trivial tests catch regression")
2. **Red-flags list** -- thoughts that mean "stop" ("I already know this works" -> run the test anyway)
3. **Explicit loophole closure** -- forbid specific workarounds Claude might exploit
4. **One Iron Law** -- a non-negotiable statement that anchors the entire discipline

**Technique skills** need templates, reference tables, and step-by-step procedures that provide structure without removing judgment.

**Workflow skills** need cross-references between phases, integration points with other skills, and clear handoff criteria.

**Reference skills** need comparison tables, architecture diagrams, and context for when each option is appropriate.

### Quality Markers

From analysis of 18 production skills:

| Marker                | Excellent                          | Mediocre                      |
| --------------------- | ---------------------------------- | ----------------------------- |
| Agent internal state  | Red-flags map thoughts to actions  | Rules without self-monitoring |
| Empirical grounding   | "24 failures", "6 iterations"      | No evidence of real use       |
| Executable algorithms | Pseudocode, templates, checklists  | Abstract principles only      |
| Good/Bad comparisons  | Side-by-side with explanation      | One example or none           |
| Scope boundaries      | Explicit "when NOT" with reasoning | Missing or vague              |

## Step 5: Organize for Progressive Disclosure

Skills load in three stages with dramatically different costs:

| Level | What Loads         | When                | Token Impact          |
| ----- | ------------------ | ------------------- | --------------------- |
|     1 | Name + description | Always              | ~100 tokens per skill |
|     2 | SKILL.md body      | When skill triggers | ~1-2% of context      |
|     3 | Referenced files   | When Claude reads   | On-demand only        |

**The file system IS the progressive disclosure mechanism.** Put the core workflow in SKILL.md. Put heavy reference material (API docs, lookup tables, exhaustive examples) in `references/`. Put executable tools in `scripts/`.

### The Routing Pattern

When a domain has many subspecialties, separate skills consume the description budget rapidly. Fifteen programming subskills at 100 words each eat 40% of the budget even when the user is writing documentation.

The routing pattern consolidates subspecialties under a single description. One SKILL.md body acts as a router, directing Claude to the appropriate reference file:

```markdown
## Language-Specific References

Read the appropriate reference based on the project:
- Swift code (.swift files): Read `references/swift.md`
- TypeScript/React (.ts, .tsx): Read `references/typescript.md`
- C++ (.cpp, .h): Read `references/cpp.md`
- PostgreSQL queries: Read `references/postgres.md`
```

Fourteen descriptions eliminated, ~7000 characters returned to the budget. The content is preserved; only the loading mechanism changes.

For the complete routing pattern with examples, the flag-file enhancement for conditional hooks, and composability guidance, see `references/routing-pattern.md`.

### Size Guidance

- **SKILL.md body**: under 500 lines (~2,000-3,000 words)
- **One excellent code example** in the most relevant language, not multi-language
- **Keep references one level deep** from SKILL.md
- Monitor `/context` for budget warnings when running 20+ skills

## Step 6: Test and Iterate

### Testing

Three areas:

1. **Triggering**: Does the skill activate on relevant queries? NOT on unrelated ones? Target: 90% on 10-20 test queries.
2. **Functional**: Does Claude follow the instructions correctly? Handle edge cases? Use Given/When/Then format.
3. **Performance**: Run with-skill vs without-skill on the same task. Track pass rate, messages, tool calls, tokens.

For the full evaluation methodology -- including description optimization loops, parallel test runs, and statistical benchmarking -- see `references/evaluation.md`.

### Skills Evolve Through Use

A skill without observed failures hasn't been tested seriously. The lifecycle:

1. **Draft** -- write the initial skill based on what you know
2. **Test** -- run against realistic scenarios
3. **Observe** -- watch where Claude goes wrong
4. **Add gotchas** -- each failure becomes a gotcha
5. **Test again** -- verify the gotchas help
6. **Review periodically** -- as models improve, guardrails that helped weaker models may constrain stronger ones

Anthropic's AskUserQuestion tool took three complete redesigns. The first two were technically sound but Claude didn't gravitate toward using them. Skills should be designed with the expectation that the first version won't be right.

## Step 7: Deploy

1. **Create the skill directory** in the appropriate location:
   - Global: `~/.claude/skills/skill-name/`
   - Project: `.claude/skills/skill-name/`
   - Plugin: `skills/skill-name/` within the plugin structure
2. **Verify** the skill appears in `/context` on next conversation start
3. **Check budget** -- ensure other skills aren't being truncated

## Frontmatter Quick Reference

```yaml
---
name: skill-name          # kebab-case, max 64 chars, must match directory
description: Use when ... # Max 1024 chars, triggering conditions only
---
```

Key optional fields:

| Field                      | Purpose                                                |
| -------------------------- | ------------------------------------------------------ |
| `user-invocable: false`    | Hidden from `/` menu; only Claude can trigger          |
| `disable-model-invocation` | User-only via `/name`; removed from description budget |
| `context: fork`            | Runs in isolated subagent context                      |
| `model`                    | Override model for this skill                          |
| `allowed-tools`            | Space-delimited pre-approved tools                     |
| `hooks`                    | Event handlers scoped to skill lifetime                |

For the complete frontmatter reference including all fields, string substitutions, dynamic context, and persistent data patterns, see `references/frontmatter.md`.

For frontmatter hooks (component-scoped event handlers), see `references/hooks.md`.

## Additional Resources

- **`references/frontmatter.md`** -- Complete frontmatter fields, string substitutions, persistent data patterns
- **`references/routing-pattern.md`** -- Complex skill organization, flag-file enhancement, composability
- **`references/evaluation.md`** -- Description optimization loops, parallel testing, benchmarking
- **`references/hooks.md`** -- Frontmatter hooks: all events, handler types, output formats

## Common Mistakes

| Mistake                          | Fix                                                          |
| -------------------------------- | ------------------------------------------------------------ |
| Description summarizes workflow  | Description = triggering conditions only                     |
| No gotchas section               | Add observed failure points as the first maintenance pass    |
| Skill too long (500+ lines)      | Move reference material to `references/`                     |
| No trigger keywords              | Add error messages, symptoms, tool names to description      |
| Vague description                | "Use when tests have race conditions" not "For testing"      |
| Multi-language examples          | One excellent example in the most relevant language          |
| No scope boundaries              | Add "When NOT to use" section                                |
| States the obvious               | Focus on what Claude gets wrong, not what it already knows   |
| ALWAYS/NEVER without reasoning   | Explain why -- Claude handles edge cases better with context |
| Narrative storytelling           | Convert to patterns, tables, checklists                      |
| Files not enumerated in SKILL.md | Claude won't discover unenumerated files                     |
| Nested file references           | Keep references one level deep from SKILL.md                 |
| Write-once, never revised        | Skills evolve through gotchas, testing, periodic review      |
| Untested skill                   | Test triggering + functional + performance                   |
