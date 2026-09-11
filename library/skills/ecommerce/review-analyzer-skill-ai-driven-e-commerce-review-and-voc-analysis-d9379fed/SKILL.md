---
name: "review-analyzer-skill"
description: "AI‑driven e‑commerce review and VOC analysis. Generates a 22‑dimension tagged dataset, a 15‑chapter insight report, optional visual dashboards and Feishu sync from CSV or Sellersprite source."
---

# Review Analyzer Skill (v2.2)

## Overview
The skill transforms raw product reviews into actionable insights:
- **22‑dimensional AI tagging** (demographics, sentiment, quality, etc.)
- **15‑chapter insight report** with anomaly cards and data appendix
- **6 optional visual dashboards** (premium‑gold, posthog‑analytics, stripe‑executive, linear‑minimal, dark‑tech, warm‑editorial)
- **Feishu synchronization** of documents and charts

## Prerequisites
- Python 3.8+
- `pip install pandas jinja2 requests python-dotenv tqdm`
- (Optional) Sellersprite API key if you want to fetch reviews directly from Sellersprite.
- (Optional) `lark-cli` installed and authenticated for Feishu sync.

## Installation
```bash
pip install pandas jinja2 requests python-dotenv tqdm
```

## Usage
### 1. Prepare input
- **CSV source (recommended)** – a file containing at least `review_id`, `title`, `content`, `rating` columns.
- **Sellersprite source (optional)** – provide `--source sellersprite --asin <ASIN> --site <region>`; the tool will fetch reviews using the supplied API key.

### 2. Run the pipeline
```bash
# CSV example
python3 main.py "reviews.csv" --llm agent --max-reviews 100 --creator "AI Assistant"

# Sellersprite example
python3 main.py --source sellersprite --asin B001OAXE0S --site US \
    --llm agent --max-reviews 100 --creator "AI Assistant"
```
Available flags:
- `--max-reviews N` – limit number of reviews (default 100).
- `--template <name>` – choose a dashboard template (default `premium-gold`).
- `--feishu-sync` – upload results to Feishu.
- `--resume <workdir>` – resume a previously started run (idempotent).

### 3. Interactive parameter collection (for agents)
When invoked by an autonomous agent, the skill expects the following questions to be asked in order:
1. **Data source** – CSV or Sellersprite.
2. **Number of reviews** – 100 (default), 300, or all.
3. **Feishu sync** – yes/no.
4. **Dashboard template** – none or one of the six styles.
5. **Report author** – default `AI Assistant` or custom (only if a template is chosen).
The agent must collect these answers before proceeding.

### 4. Resume workflow (deterministic steps)
1. `python3 main.py …` – loads data, creates batch prompts, writes them to `workdir/tagging/`.
2. Agent reads each `batch_XXX_prompt.md`, generates JSON tags, and saves `batch_XXX.json`.
3. `python3 main.py --resume <workdir>` – aggregates tags, creates `report_prompt.md`.
4. Agent writes the full 15‑chapter markdown report to `workdir/report_draft.md` following the prompt.
5. Final `--resume` call produces:
   - `评论采集及打标数据_{ASIN}.csv`
   - `分析洞察报告_{ASIN}.md`
   - Optional `可视化洞察报告_{ASIN}.html`
   - Optional Feishu document.

## Output files
| File | Description |
|------|-------------|
| `评论采集及打标数据_{ASIN}.csv` | 22‑dimensional tag table |
| `分析洞察报告_{ASIN}.md` | 15‑chapter insight report |
| `可视化洞察报告_{ASIN}.html` | Dashboard (if a template was selected) |
| Feishu doc | Full report + charts (if sync enabled) |

## License
MIT © Buluu@新西楼.AI
