# GREEN-036 — Multiplicatively Closed Set Density

**Status: OPEN.** Nothing here settles it; this dossier adds proofs of partial
results, an exact census, and verified code.

**Source:** Ben Green, *100 Open Problems*, #36 ·
<https://www.unsolvedmath.com/problems/GREEN-036>

## Problem

Let `A` be the smallest set with `2, 3 ∈ A` and
`a1, a2 ∈ A ⟹ a1·a2 − 1 ∈ A`. Does `A` have positive asymptotic density,
i.e. is `d(A) = lim |A ∩ [1,N]| / N > 0`?

## Results at a glance

| claim | strength |
|---|---|
| `A` avoids residue 1 mod 3, so upper density ≤ **2/3** | PROVEN (Lemma A) |
| `\|A ∩ [1,N]\| ≥ ⌊(⌊log₂N⌋−1)²/4⌋ ~ 0.5203·(ln N)²`, via injective family `(2^{i+1}+1)(2^{j+1}+1)−1` (2-adic cascade) | PROVEN (Lemma B) |
| exact census `F(10^8) = 55,939,931`; density `0.500 → 0.559` rising every decade; local exponents → 1.0079 | COMPUTED, exact to 10^8 |
| among all primes p ≤ 500 only `S_3 = {0,2}` is proper; no modulus m ≤ 500 beats 2/3 | COMPUTED |
| mean-field root `Σ_{b∈A} b^{−(1+α)} = 1` gives α* = 0.4734 vs OLS α̂ = 1.01600 ± 0.00254 — rejected ×9124 ⇒ membership is self-affine, not pseudorandom | HEURISTIC, quantitatively rejected |

Full derivations: [`notes.md`](notes.md); typeset report:
[`report.pdf`](report.pdf) / compilable source [`report.tex`](report.tex).

## Reproduce

```bash
python3 verify_solution.py          # X = 10^7, ~20 s, 9/9 checks PASS
python3 verify_solution.py 100000000  # production run, ~6.5 min
python3 generate_pdf.py             # rebuilds report.pdf from data/
```

Standard library only, deterministic, no network. Artifacts land in `data/`.

## Files

| file | role |
|---|---|
| `problem.md` | statement + metadata + headline numbers |
| `notes.md` | derivation log: proofs, heuristic, numerics |
| `next.md` | research brief: resolve the density question itself |
| `attack.md` | attack iteration 1: obstruction theory (L1–L5) + gap analysis |
| `attack_verify.py` | targeted structural checks (powers of 2, hole families, lcm bounds) |
| `attack2.md` | attack iteration 2: AP-hole theorem T1, doubling recurrence T3, rescue phenomenon |
| `attack3.md` | attack iteration 3: method barrier, orbit coincidences, conditional growth chain (C1') |
| `verify_solution.py` | exact DP census + all checks (CLI bound X) |
| `generate_pdf.py` / `report.pdf` | pure-Python (reportlab) PDF build |
| `report.tex` | standalone LaTeX mirror (inline appendix verbatim) |
| `data/run_output.txt` | production-run console output (verbatim) |
| `data/census_summary.json` | machine-readable summary |
| `data/census.csv.gz` | first 10^6 elements of A |

Upstream tree: <https://github.com/GamebP/MathProblems/tree/main/GREEN-036>
