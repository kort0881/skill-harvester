---
name: "infinite-gratitude"
description: "Multi‑agent research skill that dispatches several research agents to explore a topic in parallel, compiles findings, and iterates until the user is satisfied."
---

# Infinite Gratitude 🐾

> 無限貓報恩 | 無限の恩返し
> Multi‑agent research that keeps bringing gifts back — like cats! 🐱

## Quick Reference

| Option | Values | Default |
|--------|--------|---------|
| `topic` | Required | - |
| `--depth` | quick / normal / deep | normal |
| `--agents` | 1‑10 | 5 |

## Usage

```bash
/infinite-gratitude "pet AI recognition"
/infinite-gratitude "RAG best practices" --depth deep
/infinite-gratitude "React state management" --agents 3
```

## Behavior

### Step 1: Split Directions
Split `{topic}` into a set of parallel research directions (default 5):
1. GitHub projects
2. HuggingFace models
3. Papers / articles
4. Competitors
5. Best practices

### Step 2: Dispatch Agents
For each direction a background research agent is launched:
```python
Task(
    prompt="Research {direction} for {topic}...",
    subagent_type="research-scout",
    model="haiku",
    run_in_background=True
)
```

### Step 3: Collect Gifts
When agents finish, their outputs are merged into a structured report.

### Step 4: Loop
If the compiled report raises follow‑up questions, ask the user whether to continue. If the user answers **yes**, return to Step 2 with the new questions.

### Step 5: Final Report
Present the aggregated findings and any key take‑aways.

## Example Output
```
🐾 Infinite Gratitude!

📋 Topic: "pet AI recognition"
🐱 Dispatching 5 agents...

━━━━━━━━━━━━━━━━━━━━━━
🎁 Wave 1
━━━━━━━━━━━━━━━━━━━━━━

🐱 GitHub: MegaDescriptor, wildlife-datasets...
🐱 HuggingFace: DINOv2, CLIP...
🐱 Papers: Petnow uses Siamese Network...
🐱 Competitors: Petnow 99%...
🐱 Tutorials: ArcFace > Triplet Loss...

💡 Key: Data volume is everything!

🔍 New questions:
   - How to implement ArcFace?
   - How to use MegaDescriptor?

Continue? (y/n)

🐾 by washinmura.jp
```

## Notes
- Uses the `haiku` model to keep inference cost low.
- Default is 5 agents per wave; the `--agents` flag can adjust this up to 10.
- `--depth` controls how many iterative loops are performed (quick = 1 wave, deep = continue until the user stops).

## Additional Resources
- Agent configuration details: `references/agent-config.md`

## Related Skills
- **ai-dojo** – Foundation for AI coding agents
- **research-scout** – Single‑agent research implementation

---
*Part of 🥋 AI Dojo Series by [Washin Village](https://washinmura.jp) 🐾*
