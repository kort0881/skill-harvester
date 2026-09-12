---
name: "sourcesage-cli"
description: "Generate AI-friendly repository documentation with the SourceSage CLI."
---

# SourceSage CLI

## Overview
Use the SourceSage CLI from a local checkout to generate a repository summary for the current repository or any other local repository. Prefer the local checkout over a globally installed `sourcesage` binary. The tool root is the directory containing this `SKILL.md`.

## Prerequisites
- Python 3.9+ and `uv` installed.
- Access to the repository you want to analyse (local path).
- The SourceSage source tree (contains `pyproject.toml` and `sourcesage/cli.py`).

## Workflow
1. **Determine the tool root and target repository**
   - If no target is specified, analyse the current workspace.
   - If the current workspace is *not* the SourceSage repo, invoke the CLI from its checkout using `uv run --directory <sourcesage-root> sage …`.
2. **Select the minimal command that satisfies the request**
   - Current repo summary: `uv run sage`
   - Lite mode: `uv run sage --lite`
   - Japanese output: `uv run sage -l ja`
   - Analyse another repo (default output): `uv run --directory <sourcesage-root> sage --repo "<target-repo>"`
   - Lite mode for another repo: `uv run --directory <sourcesage-root> sage --repo "<target-repo>" --lite`
   - Custom output directory: `uv run --directory <sourcesage-root> sage --repo "<target-repo>" -o "<output-dir>"`
   - Deprecated diff report: `uv run --directory <sourcesage-root> sage --repo "<target-repo>" --diff`
3. **Verify generated artifacts**
   - Repository summary: `<output-dir>/.SourceSageAssets/Repository_summary.md`
   - Diff report (if requested): `<output-dir>/.SourceSageAssets/RELEASE_REPORT/Report_<latest-tag>.md`
   - Open the markdown file and provide a short human‑readable summary of its contents.
   - In `--lite` mode, ensure the file contains the tree, Git info, statistics, and root README files, but omits the `## File Contents` section.
4. **Report side‑effects**
   - Expect a `.SourceSageignore` file to be created if absent.
   - Use `--ignore-file` to override ignore rules; avoid `--use-ignore` unless the CLI is updated.

## Command Notes
- Inside the SourceSage repo: `uv run sage` (entry points are defined in `pyproject.toml`).
- Outside the repo: `uv run --directory <sourcesage-root> sage …` to avoid a global install.
- Fallback to `sourcesage` or `sage` only when the package is already installed and `uv` is unavailable.
- Language selection: `-l ja` for Japanese, `-l en` for English.
- Use `--lite` for a lightweight first pass.
- Use `-o <output-dir>` to place artifacts outside the repository root.
- Use `--repo <path>` to analyse a different repository.

## Validation
- Execute the chosen command; do not merely describe it.
- Confirm the expected markdown file exists.
- Read the file and report its path plus a concise summary of the content.
- If you modify any execution instructions, re‑run the exact command to ensure consistency.

## Avoid
- Do not rely on README examples that differ from the actual implementation in `sourcesage/cli.py`.
- Do not silently overwrite existing artifacts when a specific destination is requested.
- Do not describe usage from memory; inspect the source files when possible.
