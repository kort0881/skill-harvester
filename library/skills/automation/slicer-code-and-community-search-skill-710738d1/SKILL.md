---
name: "slicer"
description: "Search and reason over 3D Slicer source code, extensions, discourse archive, and related resources."
---

# Slicer Skill

This skill equips an AI coding agent with the ability to answer questions about the **3D Slicer** application, its extensions, and community discussions. It works with local clones or remote web APIs and offers both lexical (BM25) and semantic (dense‑embedding) ranked search.

## Safety Policy

- The `gh` CLI and Discourse endpoints are **READ‑ONLY**. The agent must never create, edit, or post anything on the user's behalf without **explicit, specific approval** for that exact action.
- If a public post is appropriate, the agent should **draft the text and hand it to the user** for final approval and posting.

## Prerequisites

- `git` – cloning repositories (not needed in *web* mode).
- `perl` – parsing CMake files for SuperBuild dependencies (full mode only).
- `bash` – to run the provided `setup.sh` script.
- Optional: `gh` CLI for authenticated GitHub API access (higher rate limits).

## Setup Modes

| Mode | Disk usage | What is cloned | Indexes built |
|------|------------|----------------|---------------|
| **full** | ~15 GB | Slicer source, all extensions, discourse archive, build dependencies, optional coding‑chat transcripts | `none`, `bm25`, or `hybrid` (as chosen) |
| **lightweight** | ~1 GB | Source + ExtensionsIndex metadata (JSON only) | Same index options |
| **web** | minimal | No clones – all access via web APIs | Forced to `none` |

Run the script to select a mode and index type:
```sh
./setup.sh                # interactive first‑run
./setup.sh --mode full    # or lightweight | web
./setup.sh --indexes bm25|hybrid|none
./setup.sh --force        # ignore 24 h stamp cache
```
The script writes `.setup‑stamp.json` containing the chosen `mode` and `indexes`.

## Ranked Search (MCP Server)

When an index is built, a stdio MCP server `slicer‑skill‑search` is started exposing:
- `search_source(query, top_k=10, mode="auto", lexical_weight=1.0, vector_weight=1.0)`
- `search_discourse(query, top_k=10, mode="auto", lexical_weight=1.0, vector_weight=1.0)`
- `index_status()`

### Choosing a mode
| mode | When to use |
|------|-------------|
| `lexical` | Exact identifiers, symbols, file paths |
| `vector`  | Conceptual or paraphrased questions |
| `hybrid`  | Default – combines both signals |
| `auto`    | Picks `hybrid` if both indexes exist, otherwise falls back |

### Example call
```python
hits = search_source("vtkMRMLScalarVolumeNode GetImageData", top_k=5, mode="hybrid", lexical_weight=2.0)
for h in hits:
    print(h["path"], h["score"], h["snippet"])
```
Each hit contains `{path, abs_path, score, line, snippet}`; use the `Read` tool with `abs_path` to fetch the full file.

## Raw Shell Search (fallback)

When indexes are missing or for resources not indexed, use standard CLI tools:
```sh
# Search extension docs (full mode)
find slicer-extensions/ -name "*.md" -exec grep -l "<topic>" {} \;

# Grep in the source tree
git -C slicer-source grep -n "vtkNew"

# Search coding‑chat transcripts
grep -rn "SegmentEditor" CodingChats-conversations/sessions/
```
In *lightweight* mode, extensions can be cloned on‑demand:
```sh
url=$(jq -r '.scm_url' slicer-extensions/ExtensionName.json)
git clone --depth 1 $url slicer-extensions/ExtensionName
```

## Web‑Based Search (lightweight & web modes)

```sh
# Discourse search
curl -s "https://discourse.slicer.org/search.json?q=<query>"

# GitHub code search (requires gh CLI)
gh search code "<query>" --repo Slicer/Slicer --limit 20

# Raw file fetch
curl -s "https://raw.githubusercontent.com/Slicer/Slicer/main/<path>"
```

## Suggested Workflow
1. Read `.setup‑stamp.json` to determine the active mode.
2. Prefer the MCP `search_*` functions for natural‑language queries.
3. If `index_status()` reports a missing or stale index, fall back to raw `git grep`/`find` or the web APIs.
4. When a query is slow over the web, suggest upgrading to a heavier mode.
5. Always draft any public message and obtain explicit user approval before posting.

## Verification
```sh
cat .setup-stamp.json   # confirm mode and indexes
ls slicer-source/CMakeLists.txt   # source present
ls slicer-extensions/README.md   # extensions metadata
```

---
