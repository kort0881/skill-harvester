---
name: "agentic-kaggle-skill"
description: "End‑to‑end workflow for Kaggle competitions, covering validation, data preparation, model development, multi‑notebook pipelines, off‑loading to Kaggle, and submission tracking."
---

# Agentic Kaggle Skill

## Overview
This skill guides an AI agent (or a data scientist) through a full Kaggle competition lifecycle, from reading the competition page to retrieving the final public score. It supports both classic file‑submission competitions and code‑competition notebooks, and it leverages Kaggle‑hosted notebooks/datasets for heavy compute or data‑access needs.

## Prerequisites
- Kaggle account with API token configured (`kaggle.json`).
- Python 3.9+ with common ML libraries (pandas, scikit‑learn, LightGBM, CatBoost, XGBoost, PyTorch/TensorFlow as needed).
- Access to the repository’s `scripts/` folder (included in the source repo).
- Sufficient local or Kaggle compute resources for the chosen model complexity.

## Operating Loop
1. **Read competition page** – Identify submission type (file vs. notebook), rules, data‑use policy, metric, and any leakage warnings.
2. **Gather intel** – If available, browse top public notebooks and discussion threads for clues (not as authority).
3. **Classify task** – Binary, multiclass, multilabel, regression, ranking, image, text, time‑series, etc.
4. **Design folds** – Add a `fold` column to the training set (use `scripts/make_folds.py`).
5. **Build baseline** – Create a metric‑correct baseline and generate out‑of‑fold (OOF) predictions plus a valid submission file.
6. **Plan stronger architecture** – Once the baseline is trustworthy, outline diverse model families, feature/embedding producers, pseudo‑labeling, distillation, calibration, and an ensemble/stacker.
7. **Iterate with validation gates** – Change one thing at a time, or run parallel producer notebooks that generate independent artifacts.
8. **Off‑load heavy jobs** – Use Kaggle notebooks/scripts for GPU‑intensive or memory‑heavy stages.
9. **Multi‑notebook pipeline** –
   - Producer notebooks generate private Kaggle datasets (features, embeddings, model checkpoints, OOF predictions).
   - Consumer notebook attaches those datasets (`/kaggle/input/...`) and creates the final OOF/test predictions and submission.
10. **Submit** – Upload the final artifact (file or notebook) to Kaggle and retrieve the score.
11. **Debug code‑competition failures** – Pull logs, classify the failure, patch, rerun, and resubmit until a concrete result is obtained.
12. **Track metadata** – Log CV scores, public LB, seeds, code version, data version, and artifact paths for every run.
13. **Ensemble responsibly** – Only with OOF predictions that have no in‑fold leakage.

## Resource Map (internal references)
- `references/method-map.md` – High‑level workflow diagram.
- `references/information-sharing-policy.md` – Rules for publishing code/datasets.
- `references/competition-intel.md` – How to incorporate competition‑specific intel.
- `references/cross-validation-and-metrics.md` – Fold and metric selection guidance.
- `references/tabular-workflow.md` – Feature engineering for tabular data.
- `references/image-text-workflow.md` – Tips for vision/NLP tasks.
- `references/kaggle-code-competition-pipeline.md` – Notebook‑scored competition specifics.
- `references/advanced-notebook-architecture.md` – Multi‑producer pipelines.
- `references/kaggle-offload.md` – When and how to run on Kaggle.
- `references/kaggle-pipeline-datasets.md` – Managing intermediate Kaggle datasets.
- `references/submission-endgame.md` – Final submission checklist.
- `references/code-competition-debugging.md` – Debugging hidden‑run failures.
- `references/ensembling-and-reproducibility.md` – Best practices for stacking/blending.

## Default Kaggle Procedure
### Validation first
- Re‑implement the competition metric locally (including clipping, thresholds, sample weights).
- Verify allowed external data, pretrained models, and public code.
- Choose folds that mimic the hidden test distribution (StratifiedKFold, GroupKFold, TimeSplit, etc.).
- Save OOF predictions for every model – they are the currency for analysis and ensembling.

### Baseline ladder
1. **Metric‑only / constant baseline** – sanity‑check submission format.
2. **Fast classical baseline** – LightGBM/CatBoost/XGBoost for tabular, TF‑IDF + linear model for text, pretrained backbone for images.
3. **Strong baseline** – Stable folds, clean artifacts, OOF predictions.
4. **Feature/model experiments** – One primary metric per experiment, log changes.
5. **Ensembling / stacking** – After several diverse models are validated.

### Off‑loading
When RAM/VRAM limits are hit, use `scripts/prepare_kaggle_kernel.py` to create a Kaggle kernel folder, run it, and collect `experiment_log.json`, `metrics.jsonl`, and an artifact manifest via `kaggle kernels output`.

## Definition of Done
The skill is complete only when **one** of the following is recorded:
- A submission has been sent, processed, and the public score (or status) is logged.
- For a code competition, the final consumer notebook has been submitted and its score retrieved.
- A concrete blocker (missing credentials, quota exhausted, competition closed, etc.) is documented with the next required action.

## Validation Choices (quick map)
| Scenario | Recommended splitter |
|---|---|
| Balanced classification | `StratifiedKFold` |
| Imbalanced classification | Stratified + class weights |
| Regression | `KFold` or binned stratified |
| Grouped entities (patient, session, etc.) | `GroupKFold` |
| Time series / forecasting | Time‑aware split |
| Image groups | Group by subject/scene |
| Text duplicates | Group by source key |
| Tiny data | Increase number of folds |

## Modeling Priorities
- **Tabular** – Start with tree boosting; add CatBoost for heavy categorical interactions.
- **Linear / NN** – Scale numeric features, encode categoricals carefully.
- **Target encoding** – Compute OOF, apply smoothing, avoid leakage.
- **Images** – Verify dataset, transforms, and metric before changing architecture.
- **Text** – Keep a TF‑IDF baseline even when using transformers.
- **Hyper‑parameter search** – Only after stable folds and baseline; tune LR, depth, regularization, sampling, n_estimators with early stopping.

## Competition Hygiene
- Keep raw data read‑only.
- Do not commit private datasets, model checkpoints, or credentials to public repos.
- Store all mutable parameters in config files or CLI args.
- Seed all libraries (Python, NumPy, torch, etc.).
- Log run IDs, git commit, hardware, elapsed time, and artifact paths.
- Maintain a pipeline manifest linking producer kernels, dataset versions, and consumer runs.
- Keep intermediate datasets private unless competition rules allow public sharing.
- Record submission metadata (message, timestamp, status, score, errors).
- Never train a stacker on in‑sample base predictions or use validation targets outside fold boundaries.

## Useful Commands
```bash
# Scaffold a new competition workspace
python3 <skill-dir>/scripts/scaffold_competition.py --root .

# Create stratified folds
python3 <skill-dir>/scripts/make_folds.py \
  --input input/train.csv \
  --output input/train_folds.csv \
  --target target \
  --strategy stratified \
  --n-splits 5

# Create grouped folds
python3 <skill-dir>/scripts/make_folds.py \
  --input input/train.csv \
  --output input/train_folds.csv \
  --target target \
  --group-col patient_id \
  --strategy group

# Prepare a Kaggle GPU kernel folder
python3 <skill-dir>/scripts/prepare_kaggle_kernel.py \
  --output kaggle_kernels/exp_lgbm_gpu \
  --username kaggle-user \
  --slug exp-lgbm-gpu \
  --title "exp lgbm gpu" \
  --competition playground-series-sample \
  --accelerator NvidiaTeslaT4

# Prepare a private Kaggle dataset for feature artifacts
python3 <skill-dir>/scripts/prepare_kaggle_dataset.py \
  --output kaggle_datasets/exp_features_v1 \
  --username kaggle-user \
  --slug exp-features-v1 \
  --title "exp features v1" \
  --description "OOF‑safe feature artifacts for experiment exp_features_v1"

# Prepare a private Kaggle dataset for model artifacts
python3 <skill-dir>/scripts/prepare_kaggle_dataset.py \
  --output kaggle_datasets/exp_model_v1 \
  --username kaggle-user \
  --slug exp-model-v1 \
  --title "exp model v1" \
  --description "Trained model artifacts for experiment exp_model_v1" \
  --artifact-kind model
```
