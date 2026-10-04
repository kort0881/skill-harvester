---
name: "math-skill"
description: "A structured workflow for AI assistants to solve mathematical problems with rigorous step‑by‑step reasoning, systematic verification, and transparent uncertainty handling."
---

# Math Skill

## Purpose
Enable AI assistants to handle mathematical tasks of any difficulty—arithmetic, algebra, calculus, proofs, and research‑level problems—by following a disciplined workflow that guarantees verified solutions.

## Scope
Covers foundations through advanced topics such as multivariable calculus, linear algebra, differential equations, abstract algebra, topology, number theory, optimization, and mathematical modeling. Also supports problem generation, solution checking, and counterexample search.

## Out of Scope
Pure opinion, non‑mathematical creative writing, factual look‑ups without reasoning, code generation unrelated to math, and general small‑talk.

## Language Matching
- Use the user‑specified language if provided; otherwise match the user's primary language.
- Typeset all formulas in LaTeX (`$...$` or `$$...$$`).
- Keep theorem names in English with brief translations when needed.

## Input Classification
Each request is first classified into one of the categories below (e.g., `calculation`, `equation_solving`, `proof`). The classification determines the verification methods to apply.

| Category | Typical Verification Methods |
|---|---|
| calculation | A, E |
| algebra_simplification | A, E, G |
| equation_solving | A, B, G |
| ... | ... |

(Full table as in the original document.)

## Seven‑Step Reasoning Workflow
1. **Problem Parsing** – Extract given conditions, goal, variables, domains, and implicit constraints.
2. **Mathematical Modeling** – Translate the problem into equations, inequalities, graphs, etc.
3. **Method Selection** – Choose the most direct, robust method (e.g., substitution, factoring, induction).
4. **Step‑by‑Step Solution** – Execute the method with full justification, citing theorems and showing intermediate steps.
5. **Verification** – Apply at least two verification methods from the Verification Engine (e.g., Back‑Substitution, Domain Check, Numerical Sampling).
6. **Error Correction** – If verification fails, backtrack, identify the error, correct it, and re‑verify.
7. **Final Answer** – Present the simplified answer, domain restrictions, and a brief verification summary.

## Verification Engine (Methods)
- **A: Back‑Substitution** – Substitute solution back into original equations.
- **B: Domain Check** – Ensure all domain constraints are satisfied.
- **C: Boundary Check** – Test edge cases and parameter extremes.
- **D: Reverse Derivation** – Derive original conditions from the answer.
- **E: Numerical Sampling** – Verify with representative numeric values.
- **F: Dimensional Analysis** – Check consistency of units (when applicable).
- **G: Limits & Special Cases** – Evaluate limits and special parameter values.
- **H: Independent Method Cross‑Validation** – Solve using a different approach.
- **I: Counterexample Search** – Look for counterexamples to claimed statements.
- **J: Formal Logic Check** – Validate logical structure of proofs.
- **K: Computational Consistency Check** – Verify computations via alternative calculations.

## Example (Illustrative)
*Problem*: Solve \(x^2 - 5x + 6 = 0\).
1. **Parsing** – Identify a quadratic equation in \(x\).
2. **Modeling** – Write as \(ax^2+bx+c=0\) with \(a=1,b=-5,c=6\).
3. **Method Selection** – Use factoring.
4. **Solution** – \((x-2)(x-3)=0 \Rightarrow x=2\) or \(x=3\).
5. **Verification** –
   - A: Substitute: \(2^2-5·2+6=0\) and \(3^2-5·3+6=0\).
   - B: No domain violations.
6. **Error Correction** – Not needed.
7. **Final Answer** – \(x=2\) or \(x=3\). Verification passed.

## Search Policy
- Search only when uncertain about a theorem, definition, or when the user explicitly requests external information.
- Prioritize authoritative sources (arXiv, MathStackExchange, etc.) and never copy verbatim.

## Hard Problem Protocol
For competition‑level or research problems, follow the enhanced protocol: initial assessment, targeted search, first‑principles analysis, and clear documentation of uncertainty.

---
