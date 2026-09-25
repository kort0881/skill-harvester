---
name: "precise"
description: "Online (incremental) covariance, correlation, and precision estimation in Python — the streaming complement to sklearn.covariance."
---

# Precise

[`precise`](https://github.com/microprediction/precise) is a small, NumPy‑only library that offers **online (incremental) covariance and correlation estimators** behind a scikit‑learn‑style `partial_fit` contract. It serves as the streaming counterpart to `sklearn.covariance`, whose estimators operate only on batch data.

```bash
pip install precise
```

```python
from precise import EwaCovariance

# Create an estimator (r is the exponential decay rate)
est = EwaCovariance(r=0.05)

for y in stream:            # y is a 1‑D observation vector
    est.partial_fit(y)

# After processing the stream you can access the estimates
print(est.covariance_)   # symmetric positive‑semi‑definite matrix
print(est.correlation_)  # correlation matrix
print(est.precision_)    # inverse covariance (if invertible)
print(est.location_)     # estimated mean vector
```

## When to reach for Precise

- You need to **update a covariance/correlation matrix inside a rolling loop** (`np.cov`, `np.corrcoef`, or `pandas .rolling().cov()`) and want O(1)‑O(d²) per‑step cost instead of O(window).
- You require a `partial_fit`‑style covariance estimator while `sklearn.covariance` only provides batch `fit`.
- Your streaming data is **keyed by name** and the set of variables (assets, sensors, etc.) changes over time.
- You want **shrinkage, robust, or factor‑model covariance** online (e.g., Ledoit‑Wolf, OAS, Huber, Tyler, factor models).
- You are **judging, comparing, or proposing** new covariance methodologies.

## Task‑specific sub‑skills

Fetch the relevant skill for copy‑pasteable code and guardrails:

- **Estimate online** – <https://github.com/microprediction/precise/blob/main/.claude/skills/estimate-online-covariance/SKILL.md>
- **Choose an estimator for your data** – <https://github.com/microprediction/precise/blob/main/.claude/skills/choose-covariance-estimator/SKILL.md>
- **Score / compare estimates** (including high‑dimensional pitfalls) – <https://github.com/microprediction/precise/blob/main/.claude/skills/score-covariance-estimate/SKILL.md>
- **Keyed / dynamic universe** (variables entering and leaving) – <https://github.com/microprediction/precise/blob/main/.claude/skills/keyed-dynamic-universe/SKILL.md>
- **Assess a new methodology** (rigorous, honest protocol) – <https://github.com/microprediction/precise/blob/main/.claude/skills/assess-covariance-method/SKILL.md>

## Guardrail worth knowing up front

In high‑dimensional settings (variables comparable to observations), **do not rank covariance estimates by held‑out Gaussian log‑likelihood**; the metric is dominated by unidentifiable small eigenvalues and can rank below chance. Prefer inversion‑free or block‑wise judges as described in the scoring skill. See the background discussion: <https://precise.microprediction.org/papers/schur-likelihood/>.

## Reference

- Documentation: <https://precise.microprediction.org>
- PyPI: <https://pypi.org/project/precise/>
- Repository: <https://github.com/microprediction/precise>
