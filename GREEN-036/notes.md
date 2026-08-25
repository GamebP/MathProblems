# GREEN-036 — Derivation Log

Status labels: **[PROVEN]** rigorous proof included; **[COMPUTED]** exact finite
computation, machine-checked, no claim beyond the computed range; **[HEURISTIC]**
formal calculation whose hypotheses are not verified; **[OPEN]** unresolved.

Notation: `F(N) = |A ∩ [1,N]|`, `v₂(n)` = 2-adic valuation, `λ = floor(log2 N)`.

---

## 1. Well-foundedness and the exact characterization [PROVEN]

**Structural fact.** If `n = a1*a2 − 1 ∈ A` with `a1,a2 ∈ A` then
`a1, a2 ≥ 2` (1 ∉ A: seeds are 2,3 and ab−1 ≥ 2·2−1 = 3), hence
`a1 a2 = n+1` gives `a1, a2 ≤ (n+1)/2 < n` for n > 1.

Consequently the operation strictly decreases max-factor to value, so:

**Exact characterization.** `n ∈ A ⟺ n ∈ {2,3}` or `∃ a,b ∈ A : n = ab − 1`.

*Proof.* (⊆) is minimality of A. (⊇) Let `A'` = {2,3} ∪ {ab−1 : a,b ∈ A}.
Then `A ⊆ A'`: any generation tree for n either is a seed or splits at the root
into two smaller elements of A, which by induction on tree size lie in `A'`
(well-founded by the structural fact). Conversely `A' ⊆ A` by closure. ∎

This makes A a well-defined *least fixed point* and justifies increasing-order DP.

## 2. Exact generation algorithm and its correctness [PROVEN] + [COMPUTED]

Algorithm (`generate_A(X)` in verify_solution.py): bytearray membership bits;
min-heap of discovered-unexpanded values; sorted list `small` = A∩[1,√X].

- pop smallest unexpanded m; let `lim = min(m, X//m)`;
- for a in `small` ascending while `a ≤ lim`: insert `n = m*a−1` if new.

**Soundness:** only true elements are inserted (each inserted value is ma−1 with
m,a ∈ A). **Completeness:** pushes always exceed the popped value (n = ma−1 ≥ 2m−1 > m),
so pops occur in increasing order; by strong induction, when m is popped every
element of A∩[1,m] is discovered, and any pair (a,b) with product ≤ X is consumed
at the expansion of its larger factor M ≤ (X+1)/2 < X, whose partner is
≤ min(M, X/M) ≤ √X and already known. Hence at break time A∩[1,X] is exactly
the set of marked bits.

**Independent cross-check [COMPUTED]:** naive fixpoint iteration
S ← S ∪ {ab−1 ≤ X} from S={2,3} reproduces the DP census exactly on [1,3000]
(|A| = 1358 both sides).

## 3. Lemma A and the 2/3 ceiling [PROVEN]

**Lemma A.** No element of A is ≡ 1 (mod 3).

*Proof.* Residues mod 3: 2 ≡ 2, 3 ≡ 0. The table of rs − 1 mod 3 for
r,s ∈ {0,2}: 0·s − 1 ≡ 2; 2·0 − 1 ≡ 2; 2·2 − 1 ≡ 0. So {0,2} is closed under
the operation and contains the seeds; by minimality A's residues lie in {0,2},
i.e. never 1 mod 3. ∎

**Corollary.** Upper density d̄(A) ≤ 2/3. [PROVEN]

**Census check [COMPUTED]:** 0 of 55,939,931 elements below 10^8 are 1 mod 3.

## 4. Residues modulo arbitrary m [PROVEN]

For any modulus m let S_m = minimal subset of Z/m containing {2 mod m, 3 mod m}
closed under (r,s) ↦ rs−1 (computable by fixpoint iteration).

**Proposition.** The residue set {a mod m : a ∈ A} equals S_m exactly.
*Proof.* (⊆) generation-tree induction as in §1: residues of A are obtained by
the same operation from seed residues, hence lie in the closed set S_m.
(⊇) each element of S_m is produced after finitely many closure steps from the
seed residues; induction on that step count lifts representatives back through
the operation, which commutes with reduction mod m. ∎

**Density consequence [PROVEN]:** d̄(A) ≤ |S_m|/m for every m; for coprime
moduli the bounds combine via CRT: d̄(A) ≤ Π |S_{m_i}|/m_i.

**Computation [COMPUTED]:** over all primes p ≤ 500 the only proper S_p is
S_3 = {0,2} (all other 94 primes give S_p = Z/p); over all composite moduli
4 ≤ m ≤ 500 none beats 2/3 (e.g. S_9 = {0,2,3,5,6,8}, ratio exactly 6/9).
So the residue method yields nothing beyond Lemma A in this range; combined
best bound remains **2/3**.

## 5. Lemma B: an explicit (log N)^2 lower bound [PROVEN]

Families inside A:
- P_k = 2^k + 1 (k ≥ 1): orbit of 3 under x ↦ 2x−1 (t_{j+1}−1 = 2(t_j−1)). [PROVEN]
- V_j = (3^{j+1}+1)/2 (j ≥ 1): orbit of 2 under x ↦ 3x−1 (fixed point 1/2:
  t_k − 1/2 = 3^k·(2 − 1/2)). [PROVEN]

**Lemma B.** For N ≥ 8,
|A ∩ [1,N]| ≥ floor((floor(log2 N) − 1)^2 / 4) ≥ (log2 N − 2)^2 / 4
= (ln N)^2/(4 ln²2) + O(ln N), with explicit constant c = 1/(4 ln²2) ≈ 0.5203.

*Proof.* Consider z_{ij} = P_{i+1} P_{j+1} − 1 = (2^{i+1}+1)(2^{j+1}+1) − 1,
defined for integers 0 ≤ i ≤ j; all lie in A by two applications of closure.
Expansion: z_{ij} = 2^{i+j+2} + 2^{i+1} + 2^{j+1}.

*Distinctness (2-adic cascade).* 
- If i < j: z = 2^{i+1}(1 + 2^{j−i} + 2^{j+1}) and the bracket is odd, so
  v₂(z) = i+1 and odd part q = 1 + 2^{j−i} + 2^{j+1}.
- If i = j ≥ 1: z = 2^{i+2}(2^i + 1), v₂(z) = i+2, odd part 2^i + 1.
- Degenerate diagonal i = j = 0: z = 8 = 2³. This is the only pure power of 2
  in the family: every off-diagonal entry has odd part q ≥ 1 + 2 + 8 > 1, and
  every diagonal entry with i ≥ 1 has odd part 2^i + 1 > 1; moreover any
  off-diagonal entry is ≥ 14 > 8 and diagonal entries with i ≥ 1 are
  ≥ 5·5 − 1 = 24 > 8, so no other pair produces 8.

Given z in the image: if two off-diagonal pairs collide, v₂ forces i = i', then
q equality reads 2^{j−i}(1 + 2^{i+1}) = 2^{j'−i}(1 + 2^{i+1}) with the bracket
odd, forcing j = j'. If two diagonals collide, v₂ forces i = i'. Off-diagonal vs
diagonal collision would force simultaneously i+1 = i'+2 and
1 + 2^d + 2^{d+i+1} = 2^{i'} + 1, i.e. 2^d (1 + 2^{i+1}) = 2^{i'}: a power of 2
divisible by the odd integer 1 + 2^{i+1} ≥ 3 — impossible. Injective. ∎ (family)

*Counting.* If s := i+j+3 ≤ λ := floor(log₂ N) then z ≤ 2^{s−1} + 2^{s−2} + 2^{s−2}
with strict inequality (equality would need i+1 = j+1 = s−2 together with
s = i+j+3, absurd), so z < 2^s ≤ N. All pairs with 0 ≤ i ≤ j, i+j ≤ λ−3 therefore
contribute distinct members of A∩[1,N], and their number is
Σ_{s=0}^{λ−3}(floor(s/2)+1) = floor((λ−1)²/4). ∎ [PROVEN]

**Mixed family [COMPUTED, injectivity not proven].**
w_{ij} = U_i V_j − 1, U_i = 2^{i+1}+1, V_j = (3^{j+1}+1)/2. If injective over the
full rectangle the constant improves to (ln N)²/(2 ln 2 ln 3) ≈ 0.6566·(ln N)².
Partial analysis: V_j is even iff j+1 is odd (3^{odd} ≡ 3 mod 8), and for odd
V_j one has w = 2^{i+1}V_j + (V_j − 1) with v₂(V_j − 1) = v₂(j+1) + 1, so
v₂(w) = min(i+1, v₂(j+1)+1) away from ties: the valuation recovers only this
minimum, and ties between candidate index pairs prevent full recovery.
Computed up to 10^8: 216 values, all in A, zero collisions.

**Honest scale note.** At N = 10^8 these give 168 resp. 216 elements against
F(10^8) = 55,939,931: the proven lower bound is exponentially far from observed
behavior. Its value is methodological (first nontrivial unconditional growth).

## 6. Census results [COMPUTED, exact up to 10^8]

Production run X = 10^8 (pure Python DP, 6m31s wall, 9/9 checks PASS):

| k | F(10^k) | F(10^k)/10^k | local exponent | harmonic increment/decade | δ̂_k |
|---|---------|--------------|----------------|---------------------------|------|
| 1 | 5 | 0.500000 | – | 1.2694 | 0.5513 |
| 2 | 39 | 0.390000 | 0.8921 | 0.8178 | 0.3552 |
| 3 | 422 | 0.422000 | 1.0342 | 0.9470 | 0.4113 |
| 4 | 4805 | 0.480500 | 1.0564 | 1.1029 | 0.4790 |
| 5 | 51508 | 0.515080 | 1.0302 | 1.1838 | 0.5141 |
| 6 | 535585 | 0.535585 | 1.0170 | 1.2318 | 0.5350 |
| 7 | 5493428 | 0.549343 | 1.0110 | 1.2637 | 0.5488 |
| 8 | 55939931 | 0.559399 | 1.0079 | 1.2871 | 0.5590 |

(local exponent e_k = log F(10^k)/F(10^{k-1}) / log 10; harmonic increment =
Σ_{b∈A∩(10^{k-1},10^k]} 1/b; δ̂_k = increment / ln 10 estimates density.)

Further facts below 10^6 (complete census stored):
- first elements: 2, 3, 5, 8, 9, 14, 15, 17, 23, 24, 26, 27, 29, 33, 39, ...
- smallest non-members: 1, 4, 6, 7, 10, 11, 12, 13, 16, 18, ... (note 6, 11, 62
  are ≢ 1 mod 3 yet absent: A is a *proper* subset of the allowed classes);
- max gap between consecutive elements below 10^6 is 10 (between 2159 and 2169);
- conditional density within allowed classes {n ≢ 1 mod 3}: rises
  0.591 → 0.803 across 10^2 … 10^6.

Interpretation [COMPUTED trend, OPEN conclusion]: raw density rises every decade;
local exponents descend toward 1 from above; harmonic increments approach
δ̂·ln10 with δ̂ ↑ ~0.56. All trends are consistent with convergence of F(N)/N
to a positive limit ≤ 2/3, and inconsistent (on this range) with density zero;
no theorem either way.

## 7. Mean-field heuristic and its quantitative rejection [HEURISTIC → REJECTED]

Assume (H1) equidistribution: |A ∩ [1,M] ∩ (−1 mod b)| ≈ F(M)/b uniformly in b.
Then counting, for each b ∈ A, the candidate images ba − 1 ≤ N:

    F(N) ≈ Σ_{b ∈ A, b ≤ (N+1)/3} F(N/b)/b .

Ansatz F(N) ~ c·N^α (α > 0) and division by cN^α gives the self-consistency
equation

    Σ_{b ∈ A} b^{-(1+α)} = 1 .   (∗)

Since H_A(X) = Σ_{b∈A∩[1,X]} 1/b ≈ δ̂·ln X diverges (δ̂ ≈ 0.559 at 10^8),
LHS(∗) decreases continuously from ∞ to 0 as α: 0⁺ → ∞, so (∗) has a unique
solution α* — IF the ansatz and (H1) hold.

Numerics (exact truncated sums for b ≤ 2·10^5, 64 log-buckets per decade above;
root residual 2.5e-11):
- α*_trunc(10^8) = 0.473442 (stable: 0.472709 already at 10^6);
- integral surrogate δ·2^{−α}/α = 1 gives α*(δ=0.5594) = 0.4185,
  α*(δ=2/3) = 0.4785;
- mean-field predicts F(10^8) ≈ (10^8)^{0.4734} ≈ 6131 vs actual 55,939,931:
  **rejected by four orders of magnitude** (factor 9124).
- Meanwhile direct log-log OLS over decades 4–8 gives α̂ = 1.01600 ± 0.00254
  (R² = 0.99998), drifting down through 1.0079 locally: the data hug the α = 1
  boundary, i.e. near-linear growth.

Why the mean-field fails here [analysis, not a theorem]:
1. **Self-affine imaging, not independent sampling.** Every b ∈ A carries the
   entire near-copy {ba − 1 : a ∈ A} into A. Membership of ba−1 is then highly
   correlated with membership of a — the OR-condition "n+1 has SOME divisor pair
   in A×A" boosts probabilities above the product of marginals.
2. **Modular rigidity.** Equidistribution already fails globally: class 1 mod 3
   is empty of A. More such rigid classes may exist at larger moduli.
3. Consequently (∗) and its α* describe a random model of A, not A itself.
   The empirical exponent hugging 1 suggests positive density is plausible;
   the divergence of Σ 1/b over A is consistent with (but does not imply)
   d(A) > 0.

## 8. What would settle GREEN-036

To prove positive density one needs something like F(N) ≥ cN: plausibly via
showing A eventually contains all numbers in some arithmetic progression
r mod M with gcd(r,M)=1-compatible structure, or a bootstrap ("A is dense in
allowed classes at height T ⟹ denser at height T'"). Obstruction: small
counterexamples (6, 11, 62, 2159–2169 gap) show A misses allowed classes at
small height, so any progression claim needs a threshold phenomenon.
To prove density zero one must reverse the monotone rising trend observed over
eight decades — no mechanism is visible. The 2/3 ceiling from Lemma A is the
only proven constraint; finding ANY stricter provable constraint (larger-modulus
rigidity, p-adic constraints, complement stability) would be genuine progress.

## 9. Reproducibility

`python3 verify_solution.py [X]` regenerates everything (default X = 10^7,
about 20 s; production run used X = 10^8, about 6.5 min, output captured
verbatim in data/run_output.txt; summary in data/census_summary.json).
Standard library only; deterministic; no network, no RNG.
