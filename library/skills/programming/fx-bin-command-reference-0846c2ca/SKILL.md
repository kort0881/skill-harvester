---
name: "fx-bin-command-reference"
description: "Comprehensive guide to installing, using, and developing with the fx-bin CLI utility collection."
---

# FX-BIN Command Reference

A comprehensive guide to all **fx-bin** commands, installation, and usage patterns.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Installation](#installation)
3. [Available Commands](#available-commands)
4. [Command Details](#command-details)
5. [Common Use Cases](#common-use-cases)
6. [Development Commands](#development-commands)
7. [Architecture Notes](#architecture-notes)
8. [Key Files](#key-files)
9. [Getting Help](#getting-help)
10. [Documentation](#documentation)

---

## Project Overview

**fx-bin** is a Python utility collection providing command‑line tools for file operations such as counting, size analysis, searching, text replacement, and a simple upload server. It is packaged with Poetry and distributed via PyPI.

- **Package Name**: `fx-bin`
- **Repository**: https://github.com/frankyxhl/fx_bin
- **PyPI**: https://pypi.org/project/fx-bin/
- **Python Version**: 3.11+ required
- **Unified CLI**: All utilities are accessed through a single `fx` command
- **Key Technologies**: Click, Loguru, Returns

### Key Features
- Security‑hardened (path traversal, command injection protection)
- >95 % test coverage (TDD/BDD)
- Optimized for large‑scale operations
- Cross‑platform (Windows, macOS, Linux)
- Modern Python (3.11+ functional patterns)

---

## Installation

### Via pip (recommended)
```bash
pip install fx-bin
```

### Via pipx (isolated)
```bash
pipx install fx-bin
pipx upgrade fx-bin   # upgrade to latest
```

### From source
```bash
git clone https://github.com/frankyxhl/fx_bin.git
cd fx_bin
poetry install
poetry run fx --help
```

**Requirements**: Python 3.11+, dependencies (`click`, `loguru`, `returns`) are installed automatically.

---

## Available Commands
| Command | Description | Primary Use Case |
|---------|-------------|------------------|
| `fx files` | Count files in directories | Project statistics |
| `fx size` | Analyze file/directory sizes | Disk usage analysis |
| `fx ff` | Find files by keyword | Quick file location |
| `fx fff` | Find first matching file | Single‑result lookups |
| `fx filter` | Filter files by extension | File organization |
| `fx replace` | Replace text in files | Bulk text replacement |
| `fx backup` | Timestamped backups | Safe snapshots |
| `fx root` | Find Git project root | Navigation |
| `fx realpath` | Get absolute path | Path resolution |
| `fx today` | Create/navigate to today’s workspace | Daily file organization |
| `fx organize` | Organize files by date | Media/document archiving |
| `fx list` | List all commands | Discovery |
| `fx help` | Show help information | Quick reference |
| `fx version` | Show version and system info | Version checking |

---

## Command Details

### 1. `fx files` – File Counter
```bash
fx files                # current directory
fx files /path/to/dir   # specific path
fx files dir1 dir2 dir3 # multiple directories
```
Counts files and prints `<path>: <count> files`.

### 2. `fx size` – Size Analyzer
```bash
fx size                 # current directory
fx size /path/to/dir    # specific directory
fx size . --limit 10   # top 10 largest files
fx size . --unit MB    # display in MB
fx size . --sort asc   # ascending order
fx size . --all        # include hidden files
```
Options: `--limit N`, `--unit UNIT`, `--sort ORDER`, `--all`.

### 3. `fx ff` – File Finder
```bash
fx ff test                     # names containing "test"
fx ff .py                     # Python files
fx ff test --include-ignored   # include .git, .venv, node_modules
fx ff src --exclude "*test*"  # exclude test files
```
Smart defaults exclude common ignored directories; case‑insensitive; recursive.

### 4. `fx fff` – Find First File
Alias for `fx ff --first`. Returns the first match and exits.
```bash
fx fff config
```
Useful in scripts where only one path is needed.

### 5. `fx filter` – File Filter by Extension
```bash
fx filter py .                     # Python files sorted by creation time
fx filter "jpg,png,gif" . --format detailed
fx filter pdf ~/Docs --sort-by modified --reverse
fx filter txt . --no-recursive
```
Options: `--sort-by`, `--reverse`, `--format`, `--no-recursive`.

### 6. `fx replace` – Text Replacer
```bash
fx replace "old" "new" file.txt
fx replace "v1" "v2" *.py
```
Safety: atomic writes, binary files skipped, automatic backup, permission preservation.

### 7. `fx backup` – File Backup
```bash
fx backup data.json
fx backup my_project --compress
fx backup config.yaml --backup-dir ./archive
fx backup important.txt --timestamp-format %Y-%m-%d_%H-%M
```
Creates timestamped backups; optional compression and custom directories.

### 8. `fx root` – Find Git Root
```bash
fx root                # prints "Git root: <path>"
fx root --cd           # prints only the path (for `cd` scripts)
```

### 9. `fx realpath` – Absolute Path
```bash
fx realpath .
fx realpath ../foo
fx realpath ~/Downloads
```
Resolves symlinks and normalizes paths.

### 10. `fx today` – Daily Workspace
```bash
fx today                     # creates ~/Downloads/YYYYMMDD
fx today --base ~/Projects   # custom base
fx today --format %Y-%m-%d   # custom date format
fx today --cd                # output path only
fx today --dry-run           # preview only
```
Creates a date‑based directory for daily work.

### 11. `fx organize` – File Organization
```bash
fx organize ~/Photos                     # organize by creation date
fx organize . -o ~/Sorted --depth 2      # custom output & depth
fx organize . --dry-run                  # preview only
fx organize . -i "*.jpg" -i "*.png"    # include only images
```
Options include `--output`, `--date-source`, `--depth`, conflict handling, include/exclude patterns, hidden files, recursion, cleaning empty dirs, dry‑run, and verbosity.

### 12. `fx list` – List Commands
```bash
fx list
```
Shows a brief description of every sub‑command.

### 13. `fx help` – Help Information
```bash
fx help      # or fx -h / fx --help
```
Displays built‑in help for the CLI and each sub‑command.

### 14. `fx version` – Version Information
```bash
fx version
```
Outputs the current version and repository URL.

---

## Common Use Cases
*Project analysis, code repository management, media/document organization, daily workflow automation, bulk operations, system maintenance* – each illustrated with concise command pipelines.

---

## Development Commands
### Testing
```bash
poetry run pytest                # all tests
poetry run pytest -m hypothesis  # property‑based tests
```
### Code Quality
```bash
poetry run black .
poetry run flake8 fx_bin/
poetry run mypy fx_bin/
poetry run bandit -r fx_bin/
poetry run safety check
```
### Build & Publish
```bash
poetry install --with dev
poetry build
pip install -e .
poetry publish   # maintainers only
```
### Workflow
```bash
git clone https://github.com/frankyxhl/fx_bin.git
cd fx_bin
poetry install --with dev
git checkout -b feature/new-command
# run tests, format, lint, commit, push
```

---

## Architecture Notes
*Package structure, module pattern, unified Click CLI, functional programming (Returns), testing strategy* – summarized for developers.

---

## Getting Help
```bash
fx COMMAND --help   # command‑specific help
fx help              # general help
fx list              # list all commands
fx version           # version info
```
Online resources: GitHub repo, PyPI page, Click docs, Returns docs, pytest‑bdd, Hypothesis.

---

## Documentation
*Internal*: `CLAUDE.md`, `README.md`, `SKILL.md` (this file). *External*: Click, Returns, pytest‑bdd, Hypothesis.

---

**Document Version**: 1.0.0 | **Last Updated**: 2025-09-06 | **fx-bin Version**: 2.5.6
