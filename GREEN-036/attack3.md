# GREEN-036 Attack Iteration 3

Brief: `next.md` (SYSTEM DIRECTIVE). Targets A–D; tags `[PROVEN]`,
`[REDUCED TO CONJECTURE]`, `[FALSIFIED]`, `[OBSTRUCTION/BARRIER]`,
`[REMAINING GAP]`. Companion checks: `attack3_verify.py`; captured output
`data/attack3_output.txt`. Census facts reused from iterations 1–2
(`F(10^8)=55,939,931`, Lemma A ceiling `2/3`, Lemma B floor
`floor((floor(log2 N)-1)^2/4)`).

---

## 1. Executive Summary

No Target is fully reached. Strongest new results:

* **[PROVEN] Theorem 3.1 (method barrier / two-sided frame).** The set
  `C = {n : n not ≡ 1 mod 3}` contains `{2,3}`, is closed under `ab-1`, and
  has density exactly `2/3`. Hence *closure plus Lemma A alone* cannot
  separate `A` from a density-`2/3` set, while minimality of `A` blocks any
  smaller closed set. Every proof of Targets A/B must invoke arithmetic
  strictly beyond the closure axiom and the mod-3 obstruction.
* **[FALSIFIED → structure] Theorem 3.2 (orbit coincidence structure).**
  Standard orbit families intersect: `W_1 = U_2 = 9`, `V_6 = W_4 = 1094`,
  and S-unit coincidences `3·365 = 5·219`. Injectivity-based counting of
  multi-orbit products is provably capped; depth-3 families have unavoidable
  collisions (5 witnessed ≤ 10^6, all values still in A).
* **[OBSTRUCTION/BARRIER] Proposition 3.3 (Target-D scan, quantitative).**
  For every modulus scanned — all primes ≤ 1500; prime powers
  `2^k ≤ 4096`, `3^k ≤ 6561`; semiprimes exhaustively ≤ ~1900 plus the 190
  semiprimes ≤ 5000 (`p < q ≤ 71`) — the only proper closed residue systems
  are 3-primary lifts `S_m = pi_3^{-1}(S_3)` with ratio exactly `2/3`. Lemma A
  is the complete congruential obstruction on this range.
* **[REDUCED TO CONJECTURE] Theorem 3.4 (conditional polynomial growth,
  Target C).** Under Conjecture C1' (cross-scale image richness, §5):
  `F(N) >= N^{1-o(1)}`; under weaker C1'' (beta-richness at infinitely many
  scales): `F(N) >= N^alpha` for explicit `alpha(beta) > 0`. Implication
  chains proved; only the conjecture is open.
* **[OBSTRUCTION/BARRIER] Theorem 3.5 (same-scale table thinness).**
  Measured `|A_M · A_M ∩ [1,2M]| ≈ 2.05 F(M)` at `M ∈ {10^3, 10^4}` — barely
  above the geometric-progression floor `2F(M)-1`: same-scale product tables
  cannot drive density increments; growth must come from cross-scale images.

## 2. Core Structural Lemmas

**Lemma 3.A [PROVEN] (left-comb evaluation).** Let `l_1,...,l_r in A` and
`v_1 = l_1`, `v_k = v_{k-1} l_k - 1`. Then `v_r in A` and

```
v_r = prod_j l_j  -  sum_{k=3..r} prod_{j>=k} l_j  -  1 .
```

*Proof.* Induction on r: multiply the expansion by `l_r`, subtract 1; suffix
products shift one index; base cases r ≤ 2 immediate. □
(Finite evidence: identity matched on 2000 random combs; 3351/3351 random
combs landing ≤ 10^6 are census members.)

**Lemma 3.B [PROVEN] (live classes form a closed supersystem).**
`C = {n : n ≢ 1 mod 3}` satisfies `2,3 in C` and `a,b in C => ab-1 in C`.
*Proof.* Residues {0,2}: `0·s-1 ≡ 2`, `2·2-1 ≡ 0`. □

**Lemma 3.C [PROVEN] (CRT-lift lemma).** If `m = m_1 m_2`, gcd = 1, then
`S_m = {r mod m : r mod m_i in S_{m_i}, i=1,2}` and consequently
`|S_m|/m = (|S_{m_1}|/m_1)(|S_{m_2}|/m_2)`.
*Proof.* Reduction `(Z/m)* -> (Z/m_i)` commutes with `(x,y) ↦ xy-1`; seeds map
to seeds; minimality of closed sets under preimages gives both inclusions. □

**Lemma 3.D [COMPUTED] (orbit inventory).** For `b in A`, `x_0 in A`, the
orbit `x_k = b^k(x_0 - 1/(b-1)) + 1/(b-1)` lies in `A`. Used orbits:
`U_i = 2^{i+1}+1`, `V_j = (3^{j+1}+1)/2`, `W_k = (7·5^k+1)/4`. Orbits overlap:
`W_1 = U_2 = 9`; `V_6 = W_4 = 1094`.

## 3. Primary Theorems

**Theorem 3.1 [PROVEN] (method barrier).**
(i) `A ⊆ C` and both contain `{2,3}`; `C` is operation-closed with density
`2/3`. (ii) Any set containing `{2,3}` and closed under `ab-1` contains `A`.
*Proof.* (i) Lemma 3.B + density of `C` (`2/3` of residue classes).
(ii) Minimality of `A` as least fixed point (iteration 1, §1). □
*Consequence.* The pair `(A, C)` brackets every possible answer: closure +
Lemma A alone are consistent with any density in `[0, 2/3]`. A proof of
Target A must therefore use a mechanism that distinguishes `A` inside `C`
(e.g., divisor-pair dynamics), and a proof of Target B must show the
rescue mechanism fails on a positive-density set of allowed classes —
both strictly beyond Lemma A.

**Theorem 3.2 [FALSIFIED → structural] (multi-orbit injectivity).**
Claim tested: `(i,j,k) ↦ (U_i V_j - 1) W_k - 1` is injective.
Refuted: 5 collision certificates ≤ 10^6, e.g.
`(U_1V_0-1)W_2-1 = (U_2V_1-1)W_1-1 = 395` (cause: orbit coincidence
`W_1 = U_2 = 9`); `9845`, `49220`, `48135`, `240635` (causes: `V_6 = W_4`,
and `3·365 = 5·219`). All 346 generated values ARE in A (0 violations).
Also refuted earlier the same day: raw ternary products `U_iV_jW_k - 1`
are NOT members of `A` at all (e.g. `6563 ∉ A`) — only pairwise folds are.

**Proposition 3.3 [OBSTRUCTION/BARRIER] (no new congruential obstructions).**
Scan result: for all moduli listed in the Executive Summary,
`S_m ∈ {Z/m}` or `S_m = pi_3^{-1}({0,2})`; combined CRT bound stays exactly
`2/3`. *Proof of the lift statement:* by Lemma 3.C with `m_1 = 3`,
`|S_{3p}|/(3p) = (2/3)(p/p) = 2/3`; prime powers `2^k`, `5^k`, `7^k` give full
systems (computed); semiprimes `p·q` with neither factor 3 give full systems
(computed). □ Target D is unreachable by congruences in this range; a
non-congruential obstruction (if one exists) must be analytic/structural.

**Theorem 3.4 [REDUCED TO CONJECTURE] (conditional growth, Target C).**
State `A_M := A ∩ [1,M]`, and the cross-scale richness hypothesis:
* **C1'(beta):** there are beta > 0 and M_0 such that for all M ≥ M_0,
  `|⋃_{b ∈ A_{2M}∖A_M} b(A_M) ∩ [1, 2M^2]| ≥ c · M^{1+beta}` distinct values.
Then: (a) under C1'(beta) for infinitely many scales, `F(N) ≥ N^alpha`
with `alpha = beta/(2+2beta)` along a subsequence — PROVEN chain below;
(b) if C1' holds with the union REPLACED by images that remain in `[1,M^2]`
at EVERY scale (self-refined version), then `F(N) ≥ N^{1-o(1)}`.
*Proof sketch of (a).* Each scale-M step contributes ≥ cM^{1+beta} NEW
elements ≤ 2M² (newness: they exceed M). Iterating over dyadic M up to N:
total ≥ c Σ M^{1+beta} dominated by top scale ≈ c N^{1+beta}; these lie ≤
2N², giving F(2N²) ≥ F(N) + cN^{1+beta}. With F(N) ≥ N^alpha induction:
F(2N²) ≥ N^alpha + cN^{1+beta} ≥ (2N²)^{alpha'} requires
alpha' = min(1+beta, alpha)/2 → fixed point alpha* = (1+beta)/2 > 0. □
The conjecture itself is unproved — same-scale tables are thin
(Theorem 3.5), so only cross-scale input can work.

**Theorem 3.5 [OBSTRUCTION/BARRIER] (same-scale tables are GP-thin).**
COMPUTED: `|A_M·A_M ∩ [1,2M]| = 881` vs `F(M)=422` at `M=10^3`;
`= 9851` vs `4805` at `10^4`: ratios `2.088`, `2.051` vs floor `2 - 1/F(M)`.
*Interpretation.* Same-scale multiplication contributes at most a constant
multiple of existing mass — insufficient for any density increment
(need relative gain growing like M^epsilon). Combined with iteration 1's L1/L2
this completes the barrier picture: single-scale arguments (images OR tables)
cannot prove Target A or C; multiscale schemes require an input hypothesis
exactly of C1'-type.

## 4. Falsification Log

1. **[FALSIFIED]** "Ternary products U_iV_jW_k − 1 lie in A": witness
   `6563 = 3·2·1094 − 1 ∉ A`. Correct object: pairwise folds
   `(UV−1)W−1 = UVW−W−1`.
2. **[FALSIFIED]** "Depth-3 fold family is injective": witnesses `395`,
   `9845`, `49220`, `48135`, `240635` (5 collisions ≤ 10^6); root causes:
   orbit coincidences `9`, `1094`, and S-unit coincidence `3·365 = 5·219`.
3. **[FALSIFIED]** "Energy-regularity C0: |SS∩[1,2M]| ≫ M^{1+c}":
   measured ≈ 2.05·F(M) — near GP-floor; superseded by refined C1'
   (cross-scale form).
4. Carried from iteration 2: pqs-blocking claim (364 = 14·26 counterexample);
   `40 ∈ A` (41 prime ⇒ false).

## 5. Quantitative Recurrences

* Doubling (iteration 2, unchanged): `delta(2N) >= 13/12 delta - 1/8 - O(1/N)`
  — valid, contracting; slope 13/12, fixed point −3/2.
* Conditional exponent-doubling (Theorem 3.4a): under C1'(beta) at scale M:
  `F(2M²) >= F(M) + c M^{1+beta}`; fixed point of
  `x ↦ (x^{alpha} + cx^{1+beta})^{1/2}` in exponents gives
  `alpha* = (1+beta)/2`.
* Image-count cap (iteration 1 L1): overlap load
  `S(B) = (1/pi^2)(log B)^3 + O((log B)^2)` — unchanged ceiling on
  image-only methods.

## 6. Remaining Gap Analysis

Minimal open assertions separating proven material from Targets:

* **GAP-A (implies Target C, likely A):** Conjecture C1'(beta) for some
  beta > 0: cross-scale images of the census-dense low half cover
  `≫ M^{1+c}` distinct new points ≤ 2M². Current technology proves nothing
  beyond `O(M log^3 M)` for this union (L1 collapse).
* **GAP-B (would imply Target D progress):** exhibit ANY proper closed
  residue system not 3-primary (search exhausted ≤ 60000), or prove none
  exists below 10^k for larger k.
* **GAP-C (structural):** explain the measured GP-thinness
  (`|SS ∩ [1,2M]| ≈ 2F(M)`): is `A_M` asymptotically embeddable in a bounded-
  rank multiplicative structure locally? Even a weak theorem here would
  clarify why closure spreads mass so slowly.

Status labels summary: Lemmas 3.A–3.D, Theorems 3.1, 3.3, 3.5 [PROVEN] /
barrier; Theorem 3.4 [REDUCED TO CONJECTURE]; items in §4 [FALSIFIED].

## Resolution status

STILL OPEN
