---
name: "agent-recall"
description: "Persistent compounding memory system for AI agents, providing session management, recall, and insight tracking. Supports a default 5‑tool surface and an optional 18‑tool full mode. Local‑only storage, Obsidian‑compatible, optional Supabase backend."
---

# AgentRecall v3.4.30 – Quick Overview

AgentRecall is a **local‑only** memory layer for AI agents. It stores journals, insights, and knowledge rooms as markdown/JSON under `~/.agent-recall/`. The system works without network access, telemetry, or external credentials.

## Core Concepts
- **Two‑verb model** – `session_start` (inhale) loads context; `session_end` (exhale) saves and compounds.
- **Default surface (5 tools)** – `session_start`, `session_end`, `remember`, `recall`, `check`.
- **Full surface (18 tools)** – enabled with `npx agent-recall-mcp --full` for pipelines, project boards, bootstrap, etc.
- **Palace rooms** – hierarchical markdown folders that hold persistent knowledge, decisions, and insights.
- **Salience scoring** – relevance = recency + access + connections; stale rooms are flagged.

## Installation (once)
```bash
# Add the MCP server for any compatible client
npx -y agent-recall-mcp
```
Configure your MCP client (Claude, Cursor, VS Code, etc.) to point to the server, e.g.:
```json
{ "mcpServers": { "agent-recall": { "command": "npx", "args": ["-y","agent-recall-mcp"] } } }
```

## Default Tools
### `session_start({project})`
Loads prior context.
**Returns**: `project`, `identity`, `insights`, `active_rooms`, `cross_project`, `recent`, `watch_for`, `corrections`, `resume`.
**Typical use**:
```js
session_start({project:"my-app"})
```
Read the returned fields and brief the human.

### `remember({content, context})`
Stores a piece of knowledge. The system auto‑classifies and routes it.
**Returns**: `routed_to`, `classification`, `auto_name`.
```js
remember({content:"We switched to GraphQL for flexible queries", context:"architecture decision"})
```

### `recall({query, limit})`
Searches all stores (palace, journal, insights) using RRF ranking.
**Returns**: array of ranked results with stable IDs.
```js
recall({query:"JWT httpOnly cookies", limit:5})
```
Optionally provide feedback to improve future rankings:
```js
recall({query:"auth patterns", feedback:[{id:"abc123",useful:true}]})
```

### `session_end({summary, insights, trajectory})`
Compounds the session: writes a journal entry, updates awareness, consolidates palace rooms.
**Returns**: `journal_written`, `awareness_updated`, `palace_consolidated`, `insights_processed`, `card`.
```js
session_end({
  summary:"Implemented auth module with JWT refresh rotation.",
  insights:[{title:"JWT refresh tokens need httpOnly cookies", evidence:"XSS vector discovered", applies_when:["auth","jwt"], severity:"critical"}],
  trajectory:"Next: add rate limiting"
})
```

### `check({goal, confidence, assumptions, …})`
Before a complex task, records the agent’s understanding and returns warnings (`watch_for`) and similar past mistakes.
Two‑call pattern:
1. **Pre‑check** – verify intent.
2. **Post‑correction** – record human correction.
```js
check({goal:"Build REST API", confidence:"medium", assumptions:["CRUD endpoints"]})
```
After correction:
```js
check({goal:"Build REST API", confidence:"high", human_correction:"Use GraphQL", delta:"API style"})
```

## Full‑Mode Tools (optional)
Enable with `npx agent-recall-mcp --full`. Highlights:
- `project_board()` – list all projects with status.
- `project_status({project})` – quick health snapshot.
- `bootstrap_scan()` / `bootstrap_import()` – import existing git/Claude projects into AgentRecall.
- Pipeline and skill management tools for advanced workflows.

## Typical Session Flow
1. `session_start()` → load context.
2. `check()` if the task is ambiguous.
3. During work, call `remember()` whenever you learn something.
4. Use `recall()` to fetch past decisions or patterns.
5. After any correction, call `check()` again to record it.
6. `session_end()` → persist everything.

## Security & Privacy
- **Zero network** – all operations are local.
- **No credentials** – does not require API keys.
- **Filesystem scope** – reads/writes only under `~/.agent-recall/` (configurable via `--root`).
- **No code execution** – the MCP server never runs arbitrary shell commands.
- **Transparent storage** – all data is plain markdown/JSON, viewable in any editor or Obsidian vault.

## Storage Layout (example)
```
~/.agent-recall/
  awareness.md
  awareness-state.json
  projects/<name>/
    journal/YYYY-MM-DD.md
    palace/rooms/<room>/
    palace/identity.md
    palace/graph.json
```

## License
MIT – see the repository at https://github.com/Goldentrii/AgentRecall-X.
