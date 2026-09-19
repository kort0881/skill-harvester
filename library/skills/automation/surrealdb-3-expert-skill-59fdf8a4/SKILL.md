---
name: "surrealdb"
description: "Expert SurrealDB 3 skill covering architecture, SurrealQL, multi‑model data modeling, security, deployment, performance tuning, SDK integration and ecosystem tools."
---

# SurrealDB 3 Skill

This skill provides expert‑level guidance and automation for SurrealDB 3 (v3.1.4+). It includes health‑check and schema‑introspection scripts, deployment best‑practices, performance tuning tips, and integration details for the full SDK ecosystem.

## Prerequisites
- **SurrealDB CLI** – `brew install surrealdb/tap/surreal` (macOS) or follow the official [install docs](https://surrealdb.com/docs/surrealdb/installation).
- **Python 3.10+** – required for the skill scripts.
- **uv** – `brew install uv` or `pip install uv`.
- Optional: **Docker** (for containerised instances) and any language SDK you plan to use (JS, Python, Go, Rust, Java, Kotlin, .NET, C, PHP, Swift, Ruby).

## Environment Variables
| Variable | Description | Default |
|---|---|---|
| `SURREAL_ENDPOINT` | SurrealDB server URL | `http://localhost:8000` |
| `SURREAL_USER` | Username (root for local dev) | `root` |
| `SURREAL_PASS` | Password (root for local dev) | `root` |
| `SURREAL_NS` | Namespace | `test` |
| `SURREAL_DB` | Database | `test` |

> **Credential warning**: The examples use `root/root` only for local development. Use scoped, least‑privilege users in production.

## Quick Start (Local Development)
```bash
# 1. Start an in‑memory instance (dev only)
surreal start memory --user root --pass root --bind 127.0.0.1:8000

# 2. Verify the skill can reach the server
uv run scripts/doctor.py

# 3. Import a schema file
surreal import --endpoint http://localhost:8000 --user root --pass root --ns test --db test schema.surql

# 4. Dump the full schema as JSON
uv run scripts/schema.py export --format json
```

## Core Scripts
| Script | Purpose |
|---|---|
| `scripts/doctor.py` | Health check – verifies CLI, connectivity, version compatibility, and storage engine status. |
| `scripts/schema.py` | Introspects the running database; can list tables, dump full schema, or export as SurrealQL/JSON. |
| `scripts/onboard.py --agent` | Emits a JSON capabilities manifest for AI‑agent integration. |
| `scripts/check_upstream.py` | Compares upstream SurrealDB repositories against the skill’s provenance snapshot. |

All scripts output **human‑readable** information on *stderr* and **machine‑readable JSON** on *stdout*.

## Major Capability Areas
- **SurrealQL Mastery** – full coverage of CREATE, SELECT, UPDATE, RELATE, LIVE SELECT, DEFINE, REMOVE, INFO, transactions, futures and built‑in functions.
- **Multi‑Model Data Modeling** – document, graph, vector, time‑series and geospatial schemas in a single database.
- **Graph Queries** – `RELATE` and traversal operators (`->`, `<-`, `<->`).
- **Vector Search** – HNSW indexes, similarity functions, RAG pipelines.
- **Security & Permissions** – row‑level security, JWT, `DEFINE ACCESS`, `DEFINE USER`.
- **Deployment & Operations** – binary, Docker, Helm charts, storage‑engine selection, backup/restore, monitoring.
- **Performance Tuning** – index strategies, `EXPLAIN`, connection pooling, batch ops.
- **SDK Integration** – official bindings for JavaScript/TypeScript, Python, Go, Rust, Java, Kotlin, .NET, C, PHP, Swift, Ruby.
- **Surrealism WASM Extensions** – author custom functions/modules in Rust compiled to WASM.
- **SurrealML (preview)** – in‑database inference artifacts (`.surml`).
- **SurrealMCP** – Model Context Protocol server for AI‑agent access.
- **Editor Tooling** – LSP, tree‑sitter grammar, CodeMirror packages.
- **LangChain (Python)** – vector‑store integration via `langchain-surrealdb`.
- **Ecosystem Tools** – Surrealist IDE, Surreal‑Sync CDC, SurrealFS, SurrealKit, n8n nodes, GitHub Action `setup-surreal`.

## Example Workflows
### New Project Setup
```bash
uv run scripts/doctor.py
surreal start rocksdb://data/myproject.db --user root --pass root
# Design schema (see rules/data-modeling.md)
surreal import --endpoint http://localhost:8000 --user root --pass root \
  --ns myapp --db prod schema.surql
uv run scripts/schema.py introspect
```

### Migration from SurrealDB v2
```bash
# Export from v2
surreal export --endpoint http://old:8000 --user root --pass root \
  --ns myapp --db prod v2-backup.surql
# Review breaking changes (rules/surrealql.md)
# Import into v3
surreal import --endpoint http://localhost:8000 --user root --pass root \
  --ns myapp --db prod v2-backup.surql
uv run scripts/schema.py introspect
```

### Production Deployment Checklist
1. Choose storage engine (memory/rocksdb/surrealkv/TiKV).  
2. Harden security – define users, permissions, JWT.  
3. Create necessary indexes (unique, search, vector HNSW).  
4. Run `uv run scripts/doctor.py --endpoint https://prod:8000`.
5. Verify schema with `uv run scripts/schema.py introspect --endpoint https://prod:8000`.

## Rule Reference Files
- `rules/surrealql.md`
- `rules/data-modeling.md`
- `rules/graph-queries.md`
- `rules/vector-search.md`
- `rules/security.md`
- `rules/deployment.md`
- `rules/performance.md`
- `rules/sdks.md`
- `rules/surrealism.md`
- `rules/surrealml.md`
- `rules/surrealmcp.md`
- `rules/editor-tooling.md`
- `rules/langchain.md`
- `rules/ecosystem-integrations.md`
- `rules/surrealist.md`
- `rules/surreal-sync.md`
- `rules/surrealfs.md`
- `rules/surrealkit.md`
- `rules/gotchas.md`

## Upstream Source Check
```bash
uv run scripts/check_upstream.py        # human readable
uv run scripts/check_upstream.py --json # JSON for agents
uv run scripts/check_upstream.py --stale # show repos with new commits
```

## Provenance (snapshot 2026‑06‑17)
| Repository | Release |
|---|---|
| surrealdb/surrealdb | v3.1.4 |
| surrealdb/surrealist | surrealist‑v3.9.0 |
| surrealdb/surrealdb.js | v2.0.3 |
| surrealdb/surrealdb.py | v2.0.0 (PyPI) |
| surrealdb/surrealkit | v0.7.0 |
| surrealdb/surrealmcp | v0.4.0 |

All documentation reflects the state of these repos as of the snapshot date.
