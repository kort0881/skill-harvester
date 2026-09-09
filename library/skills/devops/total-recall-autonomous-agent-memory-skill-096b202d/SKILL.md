---
name: "total-recall"
description: "Autonomous memory skill for OpenClaw agents that observes, compresses, and consolidates conversation logs without external databases."
---

# Total Recall — Autonomous Agent Memory

**The only memory skill that watches on its own.**

Total Recall captures recent conversation transcripts, compresses them with an LLM into prioritized notes, and stores them in `observations.md`. It automatically consolidates older entries, recovers missed sessions, and can run a nightly “Dream Cycle” to archive and decay memories. No external databases or vector stores are required.

## Architecture

```
Layer 1: Observer (cron, every 15‑30 min) → compresses recent messages → observations.md
Layer 2: Reflector (auto‑triggered when observations > 8000 words) → consolidates, removes superseded info
Layer 3: Session Recovery (runs on every /new or /reset) → captures any missed session data
Layer 4: Reactive Watcher (inotify daemon, Linux only) → triggers Observer after 40+ new JSONL writes
Layer 5: Pre‑compaction hook (memoryFlush) → emergency capture before OpenClaw compacts context
```

## Quick Start

1. **Install the skill**
   ```bash
   clawdhub install total-recall
   ```
2. **Set your API key** (add to `.env` or OpenClaw config)
   ```bash
   OPENROUTER_API_KEY=sk-or‑v1‑xxxxx
   ```
3. **Run the setup script**
   ```bash
   bash skills/total-recall/scripts/setup.sh
   ```
   - Creates `memory/`, `logs/`, and backup directories.
   - Installs a systemd user service for the reactive watcher (Linux).
   - Prints the cron entries you need to add.
4. **Load observations at agent startup**
   Add to your agent’s startup prompt:
   ```
   At session startup, read `memory/observations.md` for cross‑session context.
   ```

## Platform Support

| Platform | Observer + Reflector + Recovery | Reactive Watcher |
|----------|-------------------------------|-----------------|
| Linux (Debian/Ubuntu) | Full | With `inotify-tools` |
| macOS | Full (cron only) | Not available |

All core scripts are portable Bash; platform‑specific helpers are in `_compat.sh`.

## Configuration

Environment variables (with defaults) control behaviour:

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENROUTER_API_KEY` | (required) | API key for LLM calls |
| `MEMORY_DIR` | `$OPENCLAW_WORKSPACE/memory` | Directory for `observations.md` |
| `SESSIONS_DIR` | `~/.openclaw/agents/main/sessions` | Where session JSONL files live |
| `OBSERVER_MODEL` | `stepfun/step-3.5-flash:free` | Primary compression model |
| `REFLECTOR_MODEL` | `nvidia/nemotron-3-super-120b-a12b:free` | Consolidation model |
| `LLM_BASE_URL` | `https://openrouter.ai/api/v1` | Base URL for OpenAI‑compatible APIs |
| `LLM_MODEL` | `deepseek/deepseek-v3.2` | Default model for LLM calls |
| `REFLECTOR_WORD_THRESHOLD` | `8000` | Word count that triggers the reflector |
| `OBSERVER_LINE_THRESHOLD` | `40` | Lines that trigger the reactive watcher |
| `OBSERVER_COOLDOWN_SECS` | `300` | Cool‑down between watcher triggers |

### Provider Examples

```bash
# OpenRouter (default)
export OPENROUTER_API_KEY="your-key"

# Ollama (local)
export LLM_BASE_URL="http://localhost:11434/v1"
export LLM_API_KEY="ollama"
export LLM_MODEL="llama3.1:8b"

# Groq
export LLM_BASE_URL="https://api.groq.com/openai/v1"
export LLM_API_KEY="your-groq-key"
export LLM_MODEL="llama-3.3-70b-versatile"
```

## Files Created

```
memory/
  observations.md          # Main observation log
  observation-backups/     # Reflector backups (last 10 kept)
  .observer-last-run       # Timestamp of last observer run
  .observer-last-hash      # MD5 hash of last processed messages
logs/
  observer.log
  reflector.log
  session-recovery.log
  observer-watcher.log
```

## Cron Jobs (added by `setup.sh`)

| Job | Schedule | Description |
|-----|----------|-------------|
| `memory-observer` | Every 15 min | Compress recent conversation |
| `memory-reflector` | Hourly | Consolidate observations when large |

## Reactive Watcher (Linux only)

```bash
# Install inotify-tools (Debian/Ubuntu)
sudo apt install inotify-tools

# Check watcher status
systemctl --user status total-recall-watcher

# View logs
journalctl --user -u total-recall-watcher -f
```

## Cost

All default models are free‑tier on OpenRouter, resulting in ~$0.00/month for typical usage (15‑30 cron runs per day, each processing a few hundred tokens).

## How It Works (Technical Overview)

### Observer
1. Locate recent session JSONL files.
2. Filter out sub‑agent/cron sessions.
3. Extract user and assistant messages within the look‑back window.
4. Deduplicate using an MD5 hash.
5. Send the extracted text to the LLM with a compression prompt.
6. Append the LLM’s prioritized notes to `observations.md`.
7. If the word count exceeds the threshold, trigger the reflector.

### Reflector
1. Back up the current `observations.md`.
2. Send the full log to the LLM with a consolidation prompt.
3. Verify the output is shorter than the input.
4. Replace the original file with the consolidated version.
5. Prune old backups, keeping the most recent ten.

### Session Recovery
Runs on every `/new` or `/reset` command:
1. Hash recent lines of the last session file.
2. Compare with the stored observer hash.
3. If they differ, run the observer with a longer look‑back (4 hours).
4. Fallback to raw message extraction if the LLM call fails.

### Reactive Watcher
1. Monitor the session directory with `inotifywait`.
2. After 40+ new JSONL lines, trigger the observer (subject to a 5‑minute cooldown).
3. Reset the counter when a cron‑based observer run occurs.

## Dream Cycle (Optional Nightly Archival)

The Dream Cycle runs as a full agent turn (not a direct bash call) and performs deeper archiving:
- Classifies observations by impact and age.
- Archives items that exceed their TTL.
- Adds semantic hooks for alternative search phrasing.
- Applies confidence scores and importance decay.
- Promotes recurring patterns to “staging” for human review.

### Setup
1. Ensure `setup.sh` has created the Dream Cycle directories.
2. Add a nightly cron entry that invokes the agent with the `dream-cycle-prompt.md` system prompt (see the skill for the exact command).
3. Start with `READ_ONLY_MODE=true` to review logs before committing changes.

### Configuration
| Variable | Default | Description |
|----------|---------|-------------|
| `DREAM_TOKEN_TARGET` | `8000` | Desired token count after consolidation |
| `READ_ONLY_MODE` | `false` | When `true`, the cycle runs in dry‑run mode |

## Troubleshooting

- **Observer not running?** Check `logs/observer.log`, verify the API key, and ensure the cron entry is active (`crontab -l`).
- **Observations not loaded?** Confirm your agent’s startup prompt reads `memory/observations.md` and that `MEMORY_DIR` points to the correct location.
- **Watcher not triggering (Linux)?** Verify `inotify-tools` is installed, and inspect the systemd service status.
- **Dream Cycle too aggressive?** Enable `READ_ONLY_MODE=true` and adjust `DREAM_TOKEN_TARGET` upward.
- **Dream Cycle not archiving enough?** Lower `DREAM_TOKEN_TARGET` to increase consolidation.

---
