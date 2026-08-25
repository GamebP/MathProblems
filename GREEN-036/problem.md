# GREEN-036 — Multiplicatively Closed Set Density

**Source:** Ben Green, "100 Open Problems" — Number Theory, problem #36.
https://www.unsolvedmath.com/problems/GREEN-036

**Status:** OPEN (as of the source listing; nothing in this dossier settles it).

**Category:** set systems / multiplicative closure / asymptotic density.

## Problem statement

Let `A` be the smallest set of positive integers such that:

1. `2 ∈ A` and `3 ∈ A`;
2. if `a1, a2 ∈ A` then `a1*a2 − 1 ∈ A`.

**Question.** Does `A` have positive *asymptotic density*, i.e. is

```
d(A) = lim_{N→∞} |A ∩ [1, N]| / N  > 0 ?
```

## First observations (proved in notes.md / report)

- Every element of A other than 2, 3 equals a1·a2−1 with a1, a2 ∈ A and
  a1, a2 ≤ (n+1)/2 < n: generation is well-founded (no circularity).
- **Lemma A:** no element of A is ≡ 1 (mod 3). Hence upper density d̄(A) ≤ 2/3.
- A contains the orbits {2^k+1} (from 3 under x ↦ 2x−1) and {(3^{k+1}+1)/2}
  (from 2 under x ↦ 3x−1), and all pairwise products minus one thereof,
  giving |A∩[1,N]| ≥ c(log N)^2 lower bounds.

## Dossier contents

| file | role |
|---|---|
| `README.md` | entry point: results at a glance + reproduction |
| `notes.md` | derivation log: proofs, heuristic, numerics |
| `next.md` | research brief for the density-resolution attack |
| `attack.md` | attack iteration 1: obstructions L1-L2, rigidity L3-L4, powers-of-2 census, GAP statement |
| `attack_verify.py` | targeted checks behind attack.md (finite evidence) |
| `verify_solution.py` | exact census + all checks (CLI bound X, default 10^7) |
| `data/run_output.txt` | verbatim captured output of the production run at X = 10^8 |
| `data/census_summary.json` | machine-readable results of the production run |
| `data/census.csv.gz` | first 10^6 elements of A |
| `report.tex` | LaTeX manuscript mirror (compilable where TeX exists) |
| `generate_pdf.py` + `report.pdf` | PDF built with pure Python (reportlab) |

Headline computational facts (production run X = 10^8, 9/9 checks PASS):

```
F(10^k): 5, 39, 422, 4805, 51508, 535585, 5493428, 55939931
F(10^8)/10^8 = 0.559399   (rising; proven ceiling 2/3 = 0.666667)
OLS log-log exponent alpha_hat = 1.01600 ± 0.00254
mean-field alpha* = 0.4734  -> REJECTED by the census (off by factor 9124)
residue method: only p = 3 gives a proper closed residue set for p <= 500;
                no modulus m <= 500 beats the 2/3 bound.
```
