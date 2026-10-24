---
name: "openclaw-docs"
description: "Retrieve authoritative OpenClaw documentation, diagnose issues, and safely execute state‑changing actions for installation, configuration, operation, and troubleshooting."
---

# OpenClaw Documentation Skill

Use the synchronized official documentation as the source of truth. Load only the files and sections needed for the current request to keep context small.

## Prerequisites
- Local checkout of the OpenClaw documentation repository with a `references/` directory.
- A file‑search tool (`rg` recommended). If unavailable, use the host’s equivalent search command.
- Ability to run `openclaw --version` when version information is required.

## Establish the Version Boundary
1. Read `references/SOURCE.json` when provenance or freshness matters.
2. Run `openclaw --version` for operational work, if the CLI is available.
3. Treat the references as documentation for the recorded upstream `main` revision. Flag a possible version mismatch when the installed OpenClaw version is older.
4. **Never** invent a command, flag, configuration key, default, or migration step. Search the references and state uncertainty when the documentation does not provide an answer.

> **Note:** Do not update the installed skill during ordinary questions. Refresh only when the user explicitly asks to install or update the skill.

## Progressive Documentation Search
Choose the narrowest route that fits the request.

### 1. Exact error, command, or configuration key
Search `references/` directly for:
- The exact error message.
- The full CLI command or subcommand.
- The complete configuration key.
- Distinctive log text, provider name, or channel name.

When `rg` is available, use:
```bash
rg -n -i --glob '*.md' --glob '*.mdx' '<exact text>' references
rg -l -i --glob '*.md' --glob '*.mdx' '<keyword>' references
```
If `rg` is not present, substitute with an equivalent search (e.g., `grep -R`).

### 2. Broad topic
1. Read `references/SKILL_INDEX.md`.
2. Open exactly one matching catalog under `references/_catalog/`.
3. If the catalog links to alphabetical sections, open exactly one matching section.
4. Select **at most three** candidate documents using their `summary` and `read_when` metadata.
5. Inspect headings or search within those documents before reading long sections.
6. Expand to another document, section, or catalog only when the first candidates are insufficient.

### 3. Topic routing table
| User intent | Start with |
|---|---|
| Installation, update, migration, deployment | `references/_catalog/install.md` |
| Gateway configuration, service, networking | `references/_catalog/gateway.md` |
| Messaging channels (Telegram, Slack, etc.) | `references/_catalog/channels.md` |
| Model providers (Anthropic, OpenAI, etc.) | `references/_catalog/providers.md` |
| Exact `openclaw` command or flag | `references/_catalog/cli.md` |
| Tools, skills, permissions | `references/_catalog/tools.md` |
| Cron, hooks, tasks, webhooks | `references/_catalog/automation.md` |
| Agents, sessions, memory, routing | `references/_catalog/concepts.md` |
| Nodes or OS‑specific behavior | `references/_catalog/nodes.md` and `references/_catalog/platforms.md` |
| UI (WebChat, dashboard, TUI) | `references/_catalog/web.md` |
| Security, exposure, incident response | `references/_catalog/security.md` and `references/_catalog/gateway.md` |
| Unclear symptom or general troubleshooting | `references/_catalog/help.md` |

If a catalog does not exist in an older snapshot, search the corresponding `references/<topic>/` directory directly.

## Diagnose from Evidence
Match diagnostics to the symptom instead of running a universal command ladder.
- **Gateway reachability:** inspect status, service state, and relevant Gateway logs.
- **Single channel issues:** inspect Gateway reachability, channel status, policy, and channel‑specific troubleshooting page.
- **Model failures:** inspect provider authentication, model resolution, and the exact provider error.
- **Configuration failures:** identify the active config path, exact rejected key, and matching reference.
- **Update/migration failures:** establish installed version, install method, and target version before recommending changes.

Begin with read‑only observations. Preserve exact errors and command output when searching the documentation.

## Control State‑Changing Actions
Treat edits, installations, updates, `--fix`, `--force`, restarts, uninstalls, credential changes, pairing approvals, and message sends as state‑changing actions.
1. Explain what will change and the likely impact.
2. Confirm the target and scope from available evidence.
3. Obtain explicit user authorization when it is not already clear.
4. Prefer previews, validation, backups, and reversible operations.
5. Re‑check status after the change.

Never expose tokens, passwords, session data, auth profiles, or secrets in the response. Redact them from any copied output.

## Produce the Answer
- Lead with the diagnosis or requested outcome.
- Provide commands only after confirming them in the synchronized references.
- Separate documented facts from inferences.
- Mention relevant version assumptions or mismatch risks.
- Cite the local reference paths used so the user can verify the answer.
- Keep unexplored alternatives out of context unless the primary route fails.

## Maintenance (Run Only on Explicit Request)
```bash
sh scripts/sync-docs.sh
python3 scripts/generate_index.py --check
python3 -m unittest -v tests/test_repo.py
```
For an installed Git checkout, install or update with:
```bash
bash <skill-directory>/scripts/install-skill.sh <skill-directory>
```
Do **not** run `scripts/sync-docs.sh` or regenerate indexes during normal OpenClaw assistance.
