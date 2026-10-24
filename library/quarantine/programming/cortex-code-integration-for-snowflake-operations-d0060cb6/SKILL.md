---
name: "cortex-code-integration"
description: "Routes Snowflake‑related requests from Claude Code to the Cortex Code CLI with configurable security envelopes and audit logging."
---

# Cortex Code Integration — Reference Documentation

> **Installation**: `npx skills add snowflake-labs/subagent-cortex-code --copy`
> Installs the skill under `skills/cortex-code/` (agent‑agnostic).

## Overview
This skill enables Claude Code to delegate Snowflake‑specific operations to the **Cortex Code** CLI running in head‑less mode. All non‑Snowflake work is handled directly by Claude Code.

## Architecture
- **Dynamic discovery** of Cortex capabilities at session start.
- **LLM‑based semantic routing** (no simple keyword matching).
- **Security wrapper** with three approval modes:
  1. **prompt** – user approves predicted tools (default).
  2. **auto** – auto‑approve, mandatory audit logging.
  3. **envelope_only** – auto‑approve, no tool prediction, envelope blocklist only.
- Stateless Cortex execution; context is explicitly enriched.
- Hybrid memory: Claude keeps full conversation, Cortex receives only the enriched prompt.
- Audit logging in JSONL for compliance.

## Configuration
Create or edit `config.yaml` in the skill’s install directory (or use an organization‑wide policy at `~/.snowflake/cortex/claude-skill-policy.yaml`). Key fields:
```yaml
approval_mode: prompt   # or auto, envelope_only
security:
  sanitize_conversation_history: true
  credential_blocking: true
  envelope: RW           # default envelope (RO, RW, RESEARCH, DEPLOY, NONE)
  disallowed_tools: []   # custom blocklist when envelope = NONE
audit_log_path: "./audit.log"
```

## Session Initialization
1. **Discover Cortex capabilities**
   ```bash
   python scripts/discover_cortex.py
   ```
   - Runs `cortex skill list`.
   - Parses each skill’s `SKILL.md` front‑matter.
   - Caches the mapping in `~/.cache/cortex-skill/`.
2. **Load routing context** – cached data is kept in memory for the session.

## Request Handling Workflow
1. **Analyze request**
   ```bash
   python scripts/route_request.py --prompt "USER_PROMPT_HERE"
   ```
   Returns a JSON decision (`cortex` or `claude`) with a confidence score.
2. **Routing decision**
   - **Cortex** if the request mentions Snowflake objects, Snowflake‑SQL, Cortex AI features, Snowpark, data‑governance, etc.
   - **Claude** for local file work, generic programming, other databases, DevOps, Git, etc.
3. **Security envelope & approval** (only for Cortex paths)
   - The wrapper reads `approval_mode`.
   - In **prompt** mode it runs:
     ```bash
     python scripts/security_wrapper.py --prompt "ENRICHED_PROMPT" --envelope "RW"
     ```
     showing a tool‑prediction prompt to the user.
   - In **auto** / **envelope_only** the call proceeds automatically, respecting the envelope blocklist.
4. **Context enrichment**
   - Pull recent Claude exchanges (last 2‑3 turns).
   - Pull recent Cortex session summaries:
     ```bash
     python scripts/read_cortex_sessions.py --limit 3
     ```
   - Build the final prompt:
     ```text
     # Claude context
     ...

     # Recent Cortex work
     ...

     # User request
     USER_PROMPT_HERE
     ```
5. **Execute Cortex headlessly**
   ```bash
   python scripts/execute_cortex.py \
     --prompt "ENRICHED_PROMPT" \
     --connection "connection_name" \
     --envelope "RW" \
     --disallowed-tools "tool1" "tool2"
   ```
   - Internally runs `cortex -p "prompt" --output-format stream-json`.
   - Parses the NDJSON stream, handling `assistant`, `tool_use`, and `result` events.
6. **Return results** – format SQL tables, artifacts, or status messages back to Claude.

## Security Envelopes
| Envelope | Allowed | Blocked |
|----------|---------|---------|
| **RO** | Read‑only tools, SELECT queries | Write, Edit, destructive Bash |
| **RW** | Read/Write, most SQL/DML | Destructive Bash (`rm -rf`, `sudo` etc.) |
| **RESEARCH** | Read + web tools | Write, destructive Bash |
| **DEPLOY** | Deployment tools (e.g., `snowflake_deploy`) | Destructive Bash |
| **NONE** | Custom blocklist via `--disallowed-tools` |

## Examples
### 1. Snowflake query
**Prompt**: "Show me the top 10 customers by revenue in Snowflake"
- Routed to Cortex, envelope **RW**.
- Executes `SELECT … ORDER BY total DESC LIMIT 10` via `snowflake_sql_execute`.
- Returns a formatted table.

### 2. Local file read
**Prompt**: "Read the config.json file in this directory"
- Routed to Claude; uses the built‑in `Read` tool.

### 3. Data‑quality check
**Prompt**: "Check data quality for the SALES_DATA table"
- Routed to Cortex, envelope **RW**.
- Runs the `data-quality` skill, returns a report with null‑rate, duplicates, etc.

## Troubleshooting
- **Cortex CLI not found**: ensure `cortex` is in `$PATH` (`~/.snowflake/cortex/`).
- **Approval prompt missing**: verify `approval_mode` in `config.yaml` or organization policy.
- **Credential path detected**: remove credential references from the prompt or adjust the allowlist.
- **Audit log absent**: confirm `audit_log_path` and directory permissions.
- **Routing mis‑classifies**: edit `scripts/route_request.py` to add custom trigger patterns.

## Advanced Customisation
Edit `scripts/route_request.py` to extend forced patterns:
```python
FORCE_CORTEX_PATTERNS = ["snowflake", "cortex", "warehouse", "snowpark"]
FORCE_CLAUDE_PATTERNS = ["local file", "git commit", "python script"]
```

---
