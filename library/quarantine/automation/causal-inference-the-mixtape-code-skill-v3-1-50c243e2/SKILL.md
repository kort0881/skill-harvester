---
name: "causal-inference-the-mixtape-code-skill-v3-1"
description: "A practitioner‑focused skill that guides users from identifying the causal design to generating runnable Python, R, or Stata code for a wide range of causal‑inference methods. It includes a design‑router, validated script templates, cross‑backend checks via StatsPAI, and detailed diagnostics to produce publishable results."
---

# Causal Inference: The Mixtape — Code Skill (v3.1)

This skill helps users who need to **implement a causal‑inference method** (DiD, staggered DiD, event study, IV/2SLS, regression discontinuity, synthetic control, propensity‑score matching, Honest DiD, wild‑cluster bootstrap, Callaway‑Sant'Anna, Sun‑Abraham, Bacon decomposition, double‑machine learning, causal forests, etc.) in **Python, R, or Stata**.  It follows the workflow advocated in Scott Cunningham’s *Causal Inference: The Mixtape*, extended with recent finance applications and machine‑learning‑based patterns.

---

## 1. Route the design before writing code

Ask the user how treatment was assigned and follow the decision tree below.  The tree maps the assignment mechanism to a causal design and suggests the appropriate estimator.

```
How was treatment assigned?
├─ Randomised                          → diff‑in‑means + RI
├─ Threshold on a running variable     → RDD / fuzzy / diff‑in‑disc
├─ Policy date, one date for all       → 2×2 DiD → event study
├─ Policy date, dates VARY             → staggered: Bacon → CS/SA/BJS
├─ One treated unit, many controls     → synthetic control
├─ Self‑selected + an instrument       → IV / 2SLS (LATE)
├─ Self‑selected + rich observables    → matching / IPW / DML
└─ None of the above                   → use associational language
```

The full tree, estimator choices, and a **StatsPAI** second‑opinion function (`sp.detect_design`, `sp.recommend`, `sp.preflight`) are documented in `references/design-router.md`.  When the design is still unclear, consult `references/method-selection.md` (Chinese‑language guide with links to Stata tutorials).

---

## 2. Choose a Python backend

```python
import statspai as sp  # pip install statspai
```

**StatsPAI** is the primary backend; it implements a broad set of Stata/R causal‑inference commands (`regress`, `ivregress`, `reghdfe`, `csdid`, `rdrobust`, `synth`, `psmatch2`, `outreg2`, Bacon, Callaway‑Sant'Anna, Sun‑Abraham, Honest DiD, wild‑cluster bootstrap, DAGs, Conley SEs, etc.).  Alternative backends are:

* `pyfixest` – fast high‑dimensional fixed effects and independent wild bootstrap.
* `linearmodels` – deep IV and panel diagnostics.
* `statsmodels` – plain OLS/GLM.
* R or Stata – when the reference implementation or replication target requires them.

Cross‑backend validation details are in `references/statspai-guide.md`.

---

## 3. Methods covered

| Method | Python (StatsPAI) | R | Stata | Script template |
|---|---|---|---|---|
| OLS / regression | `sp.regress` | `estimatr` | `reg`, `reghdfe` | — |
| DiD (2×2) | `sp.feols` | `fixest` | `reghdfe` | `02` |
| Event study | `sp.event_study` | `fixest i()` | `reghdfe` | `03` |
| Staggered DiD | `sp.callaway_santanna`, `sp.sun_abraham`, `sp.did_imputation` | `did`, `fixest` | `csdid` | `04` |
| Bacon decomposition | `sp.bacon_decomposition` | `bacondecomp` | `bacondecomp` | `04` |
| Regression discontinuity | `sp.rdrobust`, `sp.rddensity` | `rdrobust` | `rdrobust` | `05` |
| Instrumental variables | `sp.ivreg` | `AER`, `fixest` | `ivregress` | `06` |
| Synthetic control | `sp.synth`, `sp.sdid` | `Synth`, `synthdid` | `synth`, `sdid` | `07` |
| Matching / PSM / IPW | `sp.match`, `sp.ipw`, `sp.psmatch2` | `MatchIt` | `teffects`, `cem` | `08` |
| Double / Debiased ML | `DoubleML`, `EconML` | `DoubleML`, `grf` | `ddml`, `pdslasso` | — |
| DAGs / collider bias | `sp.dag`, `dowhy` | `dagitty` | — | `sim_collider_bias.py` |
| Randomisation inference | `sp.ri_test` | `ri2` | `ritest` | `09` |
| Clustered inference / wild bootstrap | `sp.wild_cluster_bootstrap` | `fwildclusterboot` | `boottest` | `10` |
| Honest DiD / pre‑trend power | `sp.honest_did`, `sp.pretrends_power` | `HonestDiD` | `honestdid` | `11` |
| ... | ... | ... | ... | ... |

---

## 4. Core workflow

1. **Route** the design using `design-router.md` (or `method-selection.md` if needed).
2. **Load** the corresponding template from `method-patterns.md` (or the runnable script in `scripts/`).
3. **Adapt** variable names, fixed‑effects structure, and clustering (cluster at the level of treatment assignment).
4. **Diagnose** with the design‑specific checks in `reporting-checklist.md`.
5. **Report** key summary statistics (N, number of clusters, treated share, baseline mean, economic magnitude) – avoid reporting t‑statistics alone.
6. **Write** the identification paragraph using the verb patterns in `identification-writing-patterns.md`.

---

## 5. Common pitfalls (selected)

* **TWFE bias in staggered DiD** – run `sp.bacon_decomposition` and report Callaway‑Sant'Anna or Sun‑Abraham instead of the naïve TWFE estimate.
* **Event‑study reference period** – ensure the omitted period is correctly dropped; otherwise coefficients are collinear.
* **Clustering too finely** – always cluster at the level of treatment assignment; clustering at a finer level understates SEs.
* **Synthetic control inference** – with a single treated unit report permutation‑based p‑values rather than t‑ratios.
* **DML without cross‑fitting** – use out‑of‑fold predictions; otherwise regularisation bias re‑enters.
* **Non‑causal framing** – avoid causal language unless the design provides exogenous variation.

Full list (1‑19) is in the original skill document.

---

## 6. Reference files

| File | Purpose |
|---|---|
| `references/design-router.md` | Assignment mechanism → design → estimator → diagnostics |
| `references/method-selection.md` | Chinese guide mapping setting → assumption → method |
| `references/statspai-guide.md` | StatsPAI API map and gotchas |
| `references/method-patterns.md` | Code templates for all methods |
| `references/dml-causal-ml.md` | DML model classes, cross‑fitting, causal forests |
| `references/reporting-checklist.md` | Checklist of mandatory reporting items |
| `references/identification-writing-patterns.md` | Templates for the identification paragraph |
| … | … |

---

## 7. Runnable scripts

The `scripts/` directory contains 13 validated templates plus shared utilities (`_common.py`).  Run the full validation suite with:

```bash
python scripts/validate_all.py --list   # list all scripts
python scripts/validate_all.py --quick  # skip the slow script
```

---

*Use this skill whenever a user asks for causal‑inference code, diagnostics, or identification write‑ups.  Follow the routing step first, then generate a reproducible script or an answer via the MCP server (`statspai-mcp`) as appropriate.*
