---
name: "security-audit-rlm"
description: "Run and troubleshoot privacy‑preserving, local RLM security audits for large legacy .NET codebases, producing actionable markdown and JSON reports without loading the entire repository into model context."
---

# Security Audit RLM

Use this skill to operate `audit.py` as a tool‑driven RLM workflow for large repositories.

**Repository:** `https://github.com/mitkox/megacode`

## Prerequisites
- Deno installed (`deno --version`)
- Python 3.9+ installed and accessible in PATH
- Required Python packages installed (see `requirements.txt` in the repo)
- Model endpoint reachable (default `http://localhost:8000/v1`)

## Execution Steps
1. **Run a baseline audit**
   ```bash
   AUDIT_VERBOSE=1 python audit.py --source-root <repo-path>
   ```
2. **Confirm generated outputs**
   - `security_audit_report.md`
   - `security_audit_metadata.json`
   - `security_audit_manifest.jsonl`

## Tuning for Large Legacy Repos
Adjust the following flags to keep the RLM workflow within resource limits:
- **Planner churn**: `--max-iterations 8..12`
- **LLM call budget**: `--rlm-max-llm-calls 60..100`
- **REPL output size**: `--rlm-max-output-chars 15000..30000`
- **Tool payload limits**:
  - `--tool-max-lines 200..400`
  - `--tool-max-chars 20000..40000`
  - `--search-max-files 800..2000`
  - `--search-max-matches 200..600`
- **Runtime limits**: `--timeout-seconds 600..1800`, `--retries 1..2`

## Operating Rules
- Keep analysis local when privacy constraints require it.
- Use RLM tool access only; avoid full‑context repository injection.
- Keep intermediate output concise and deterministic.
- Prioritize high‑severity findings with file/line evidence and concrete fixes.

## Troubleshooting
- **Stalled run**: enable verbose mode, reduce `--max-iterations` or `--rlm-max-output-chars`.
- **Model truncation**: increase `--lm-max-tokens` if the backend supports it, or further reduce tool output limits.
- **Path/file access errors**: ensure the audit flow uses tool‑only repository access (`list_manifest`, `read_file`, `search_pattern` tools) and re‑run after confirming `audit.py` includes those tools.

## Deliverable Format
The final report must contain the following sections in `security_audit_report.md`:
1. Executive Summary
2. Critical Findings (CRITICAL/HIGH) – include file path, line number, and remediation steps.
3. Other Findings (MEDIUM/LOW)
4. Remediation – actionable recommendations for each finding.

---
