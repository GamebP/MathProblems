# Synthesis & Gap Analysis — Erdős Problem #7: Odd Distinct Covering Systems

**Artifact:** `docs/synthesis_gap_analysis.md`  
**Task (3) Synthesis** — dependencies: `.opencode/notes/erdos7.md`, `ANSWER/report.tex`  
**Date:** 2026-08-25  
**Status:** Definitive assessment complete  
**GOAL:** `<synthesis_gap_artifact> == <definitive_assessment_with_exact_conditional_lemma_and_barrier_classification_complete>`

---

## 0. Question

> **Is there a distinct covering system $\{a_i \bmod m_i\}_{i=1}^k$ with all moduli $m_i$ odd, pairwise distinct, $m_i>1$, covering $\mathbb Z$?**

Erdős–Selfridge conjecture: **no**. Selfridge offered $300 → $2000 for an example; Erdős offered $25 for a proof of impossibility (Filaseta–Ford–Konyagin [FFK00]). The problem is `VERIFIABLE`: a finite example would decide it positively.

---

## 1. Definitive Assessment — Proven vs. Open

### 1.1 Summary Table

| Claim | Status | Source | Strength |
|-------|--------|--------|----------|
| No distinct covering with odd **and squarefree** moduli | **PROVEN** | Balister–Bollobás–Morris–Sahasrabudhe–Tiba [BBMST22], *Invent. Math.* 230 (2022), Thm 1.1 | Unconditional, published, peer-reviewed |
| In any distinct covering, some $m_i$ divisible by $2$ or $3$ | **PROVEN** | Hough–Nielsen [HoNi19] *Duke* 168 (2019); simplified proof in [BBMST22] § | Unconditional |
| If an odd distinct covering exists with $L=\mathrm{lcm}(m_i)$, then $9\mid L$ **or** $15\mid L$ | **PROVEN** | [BBMST22] Thm 1.3 / Cor | Unconditional; eliminates $3^1$-only powers of $3$ and many prime sets |
| $L$ abundant: $\sum_{d\mid L,d>1}1/d\ge 1 \iff \sigma(L)\ge 2L$, hence odd $L\ge 945$ | **PROVEN** | Folklore (comment 3717, Rafik, Zenodo 18360978); self-contained from $\sum 1/m_i\ge 1$ | Elementary, unconditional, sharp ($945=3^3\cdot5\cdot7$ first odd abundant, OEIS A005231) |
| $L$ must allow many moduli: $k\ge 15$ for $L=945$ ($\approx 1.03$ reciprocal sum), grows rapidly | **PROVEN** | Corollary of abundant condition + distinctness | Unconditional lower bound |
| No odd distinct covering at all (general, prime powers allowed) | **OPEN** | Conjecture of Erdős–Selfridge | No proof, no counterexample; two 2026 axiomatic Lean attempts refuted |
| Selfridge reduction: odd covering would follow from covering with $n_i\nmid n_j$ | **PROVEN IRRELEVANT** | Schinzel [Sc67]; refuted by [ErGr80] via Problem 586 — antecedent does not exist | Redirection closed |
| Infinite distinct odd family covering almost all integers (density 1) exists | **PROVEN** | Dogmachine 4263: homogeneous $0\bmod p_{k+1},0\bmod p_{k+2},\dots$ | Shows finiteness essential; finite almost-cover ⇒ cover by periodicity mod $L$ |

**Verdict:** Modern sieve machinery **fundamentally rules out the squarefree odd case** with margin $c_N(1)\approx 0.612<1$. It **does not fundamentally rule out the general odd case** without new work. The barrier at non-squarefree moduli is **currently a technical obstruction with intrinsic features**, not a proof that the method is doomed, but also not a trivial extension.

### 1.2 Precise Proven Statement (Squarefree)

**Theorem (BBMST22, squarefree odd).** There is no finite family $\{a_i\bmod m_i\}$ with distinct, odd, squarefree $m_i>1$ covering $\mathbb Z$.

*Method:* Distortion method. Fix an ordering of odd primes $p_k$ ($p_1=3,p_2=5,\dots$). Partition moduli by largest prime factor. Define a distorted probability measure $\mathbb P^*$ on $\mathbb Z_{Q_N}$ ($Q_N=\prod_{k\le N}p_k$) with biases $\delta_k\in(0,1)$ buffering small primes. Define with initial sieve data for $p\le 73$ optimized by linear programming:

$$c_N(x)=c_0(x)\prod_{k=1}^N\left(1+\frac{x}{(1-\delta_k)s_k}\right)$$

where $s_k$ = size of $k$-th block ($\approx p_k-1$ in squarefree case, LP data for $k\le 5$ gives $c_0(1)\approx 0.0979$). BBMST compute with $\delta_k$ explicit (Table 1) and $N=500$:

$$c_N(1)=c_0(1)\prod_{k}\left(1+\frac{1}{(1-\delta_k)s_k}\right)\approx 0.612 <1.$$

Then a second-moment / Lovász Local Lemma argument yields $\mu(\mathbb Z\setminus\bigcup A_i)\ge \exp(-c_N(1))>0$ (positive uncovered density), contradicting covering. The same framework gives $2\mid L$ or $3\mid L$ and the $9\mid L$ or $15\mid L$ refinement.

### 1.3 What Remains Open

The general odd case allows $m_i=p^e\cdot m'$ with $e\ge 2$. The smallest odd abundant $L$ candidates are $945,1575,2205,2835,\dots$ all divisible by $9$ or $15$ consistent with the proven restriction, so no contradiction. No finite search to any published bound has found a covering; no proof that search must fail.

---

## 2. Modern Sieve Machinery — Why Squarefree vs. Prime Powers Diverge

### 2.1 Hough–Nielsen Good Fibre

Hough (2015, resolving Erdős minimum modulus problem) + Hough–Nielsen (2019) introduced fibre decomposition by Chinese remainder structure. For each $k$, consider fibres over $\mathbb Z_{Q_{k-1}}$ and the action of blocks $B_k=\{m:\; P^+(m)=p_k\}$. A fibre is *good* if sieve inequality holds; bad fibres have small $\mathbb P^*$-measure controlled by $\delta_k$. The independence assumption and quasi-randomness of distinct moduli are essential. Llllvvuu/Gemini extraction (gist 7afe1e1) flagged 3 holes; Daniel Larsen flagged $R$ vs. collision events and distinctness of active $m_i$ — exactly the coupling that breaks for prime powers.

### 2.2 BBMST Distortion

BBMST systematize with explicit optimization:

- **Initial segment** $p\le 73$ ($p=3,5,7,11,13,17,\dots,73$): handled by exhaustive LP / moment bounds, not asymptotics. Generates $c_0(x)$ — a piecewise linear majorant for the uncovered density contributed by small moduli.
- **Tail** $p>73$: asymptotic distortion with uniform $\delta_k$ decaying roughly $\sim (\log p_k)^{-1}$, using $s_k=p_k-1$.

Crucially: $c_0$ and $\delta_k$ are **jointly optimized** for the *squarefree combinatorial class* $\mathcal F_{SF}=\{m\text{ odd squarefree}\}$. Changing the class changes the optimization problem.

### 2.3 Naïve Monotonicity Heuristic

Observed (jinooklee 6183): For fixed prime $p$, $p^e-1\ge p-1$ for $e\ge1$, so

$$s_k^{\mathrm{pow}} \ge s_k^{SF}\quad\Longrightarrow\quad 1+\frac{x}{(1-\delta_k)s_k^{\mathrm{pow}}}\le 1+\frac{x}{(1-\delta_k)s_k^{SF}}.$$

Since each factor decreases, $\prod(1+x/((1-\delta_k)s_k^{\mathrm{pow}}))\le\prod(1+x/((1-\delta_k)s_k^{SF}))$. If $c_N^{SF}(1)\approx0.612<1$, then $c_N^{\mathrm{pow}}(1)<1$ and covering impossible — prime powers "only harder."

This is the intuition behind "enlarging $p\to p^e$ makes covering harder."

---

## 3. Why Naïve Extension Fails — $c_0(x)$ and Prime-Power Distortion Coupling

The naïve argument is **mathematically invalid as stated** and was decisively refuted in-thread (natso26 6298, TFBloom 6316). Three coupled failures:

### 3.1 Omission of $c_0(x)$

Lean formalization [axxen95] defined

```lean
def updateFactor (s : Rat) (x : Rat) : Rat := 1 + x / s
def sieveProd : List Rat → Rat → Rat
  | [], _ => 1
  | s::ss, x => updateFactor s x * sieveProd ss x
axiom bbmst_sf_lt_one : sieveProd sfBlocks 1 < 1
```

For any $s>0$, $1+x/s>1$, so `sieveProd _ 1 >1` for any non-empty list. The axiom is **provably false** (GPT + natso26 observation). The true BBMST object is

$$c_N(x)=c_0(x)\prod_{k=1}^N\left(1+\frac{x}{(1-\delta_k)s_k}\right)$$

with **$c_0(1)\approx 0.098\ll1$** from LP over first 5 primes (or $p\le73$ full optimization). The product of $>1$ factors is compensated by the small $c_0$. Omitting $c_0$ invalidates the $<1$ claim. Correcting the formalization requires encoding $c_0$ faithfully, which is not a product of $1+x/s$ terms but an LP optimum.

### 3.2 $c_0$ Is Not Monotone in the Modulus Class

Even with correct $c_N$, monotonicity in tail factors does **not** imply monotonicity of $c_0$.

- **Squarefree $c_0^{SF}$**: LP optimum over families $\mathcal M\subset\{m\le73: m\text{ odd squarefree}\}$ with distinctness. Optimal value $\approx0.098$.
- **Prime-power $c_0^{\mathrm{pow}}$**: LP optimum over $\mathcal M\subset\{m\le73: m\text{ odd}\}$ *including* $9,25,27,45,49,63,\dots$. The feasible region **expands**: more moduli available means the adversary (covering system) has more options for the initial segment. The LP is a *maximization* of covered density; adding variables can **increase** the maximum.

There is **no theorem** that $c_0^{\mathrm{pow}}(x)\le c_0^{SF}(x)$. In fact the opposite inequality is a priori plausible: allowing $9,25,27,\dots$ gives the covering system more combinatorial power at small primes, potentially raising $c_0$. The monotone-$s_k$ argument assumes $c_0$ fixed, which is false.

Verification requires **re-solving the LP** with the expanded ground set and re-optimizing $\delta_k$ for $k\le5$ (the region where $p\le73$). BBMST Sections 2–3 isogeny: the $p\le73$ sieve data is obtained by explicit enumeration/computation, not a closed form. No published computation does this for the prime-power class.

### 3.3 Distortion Coupling: $\delta_k$ Depends on $s_k$

BBMST $\delta_k$ are chosen to minimize $c_N(1)$ subject to distortion cost. Optimal $\delta_k$ solves a tradeoff:

$$\text{minimize }\; c_0\prod_k\left(1+\frac{x}{(1-\delta_k)s_k}\right)\quad\text{s.t. }\sum_k \frac{\delta_k}{1-\delta_k}\cdot\text{(measure of bad fibres)}\le\cdots$$

$s_k$ enters both the product and the constraint (bad fibre probability scales like $\sim 1/s_k$). If $s_k$ increases ($p^e-1 \ge p-1$), the optimal $\delta_k^*$ **shifts**. Using SF-optimal $\delta_k^{SF}$ for the pow case is **suboptimal** and may not give $<1$; re-optimizing may restore feasibility but must be proved. The fibres themselves change geometry: for $p^e$, the partition of $\mathbb Z_{Q_k}$ into $p^e$ residue classes vs $p$ classes changes fibre sizes unevenly, breaking the Hough–Nielsen independence estimate $R$ vs. collision events flagged by Larsen. The block $B_k$ now contains moduli with varying $v_{p_k}(m)$, so $s_k$ is not a single integer $p_k-1$ but a sum over exponents, and the "block size is monotone" reduction is an oversimplification of the tree.

**Conclusion:** The tail product monotonicity is real but irrelevant without uniform control of $c_0^{\mathrm{pow}}$ and $\delta_k^{\mathrm{pow}}$. TFBloom's scepticism is correct: *"If the squarefree assumption could be removed trivially, BBMST would have done so."*

---

## 4. Exact Conditional Lemma Required to Resolve the Conjecture

We state the minimal precise closure lemma. Any one of the following equivalent formulations, if proved, would complete the Erdős–Selfridge conjecture for odd moduli via BBMST.

### 4.1 Primary Formulation — Distortion Bound with Prime Powers

**Conditional Lemma A (Prime-Power Distortion; quantitative).**

> *Let $N\ge 500$, let $p_1=3<p_2=5<\cdots<p_N$ be odd primes. For each $k$ let*
> $$\mathcal B_k^{\mathrm{pow}}=\{m>1: m\text{ odd},\;P^+(m)=p_k\},\qquad s_k^{\mathrm{pow}}=|\mathcal B_k^{\mathrm{pow}}\cap[1,Q_k]|\;(\ge p_k-1),$$
> *with the same $Q_k$ hierarchy as BBMST. Let $\delta^*_k\in(0,1)$ be the explicit BBMST Table-1 sequence (with $\delta^*_k=0$ for $k\le5$ after LP). Let $c_0^*(x)$ be the LP optimum for the initial interval $I_0=\{m\text{ odd}:m\le73\}$ allowing prime powers, i.e.*
> $$c_0^*(x)=\sup_{\mathcal M\subset I_0\text{ distinct}}\mathbb E^*\!\left[\text{uncovered indicator under optimal } \mathbb P^*\right].$$
> *Then*
> $$c_0^*(1)\le c_0^{SF}(1)\approx0.0979$$
> *and*
> $$c_N^{\mathrm{pow}}(1):=c_0^*(1)\prod_{k=6}^{N}\left(1+\frac{1}{(1-\delta^*_k)s_k^{\mathrm{pow}}}\right)\le c_N^{SF}(1)\approx0.612<1.$$
> *Consequently for any finite odd distinct family $\mathcal C=\{A_i=a_i\bmod m_i\}$ with $m_i$ odd, the BBMST distorted measure $\mu=\mathbb P^*$ satisfies*
> $$\mu\!\left(\mathbb Z\setminus\bigcup_i A_i\right)>0,$$
> *hence $\mathcal C$ does not cover $\mathbb Z$.*

**Remark.** The non-trivial content is the first inequality $c_0^*\le c_0^{SF}$. The product inequality is then elementary from $s_k^{\mathrm{pow}}\ge p_k-1=s_k^{SF}$ *provided $\delta^*_k$ remains feasible* — feasibility is part of the claim (the $\delta^*_k$ from SF remain admissible for the pow fibre partition with at most same bad-fibre mass). A weaker sufficient lemma replaces $\delta^*_k$ by a re-optimized $\delta^{\mathrm{pow}}_k$ and proves $\inf_{\delta}c_N^{\mathrm{pow}}(1)<1$.

### 4.2 Equivalent Measure-Theoretic Formulation

**Conditional Lemma B (Positive Uncovered Density).**

> *There exist constants $\delta_k\in(0,1)$ and $c>0$ such that for every finite distinct odd covering candidate $\mathcal C$ (allowing $p^e$), the BBMST/Hough distorted probability measure $\mathbb P$ on $\mathbb Z_{Q_N}$ satisfies*
> $$\mathbb P\!\left(\mathbb Z\setminus\bigcup_{i}A_i\right)\ge c>0\quad\text{with }c\ge 1-c_N^{\mathrm{pow}}(1)>0.$$
> *In particular $\mu(\mathbb Z\setminus\bigcup A_i)>0$ uniformly in $\mathcal C$, so no odd distinct covering exists.*

This is the direct analytic obstruction to covering; BBMST prove it for SF with $c\approx0.388$; the lemma asserts the same $\mathbb P$ works for pow.

### 4.3 Computational LP Formulation

**Conditional Lemma C (Initial-Segment LP Verification).**

> *Let $S_0^{\mathrm{pow}}=\{m\le73: m\text{ odd}\}=\{3,5,7,9,11,13,15,21,25,27,\dots,73\}$ (27 numbers vs. 16 squarefree). Let $\mathcal F$ be the set of feasible weight functions $w: S_0^{\mathrm{pow}}\to[0,1]$ satisfying the BBMST LP constraints (distinctness, fibre capacities). Then the LP optimum*
> $$c_0^{\mathrm{pow}}:=\max_{w\in\mathcal F}\sum_{m\in S_0^{\mathrm{pow}}}w_m\cdot f_m(\delta)$$
> *satisfies $c_0^{\mathrm{pow}}\le0.098$ (SF optimum). This is a finite-dimensional linear program with $\sim 10^4$ constraints, verifiable by exact rational arithmetic or certified interval arithmetic.*

Lemma C is *falsifiable by computation* — it can be checked by enumerating $S_0^{\mathrm{pow}}$ and running the BBMST LP solver with expanded ground set. Failure of Lemma C would be a **certificate that the distortion method as calibrated cannot extend** without new $\delta_k$.

### 4.4 Why These Are Exact

- They isolate the **only unproven component**: the initial LP + distortion feasibility with prime powers. The tail is monotone and done.
- They are **quantitative** ($<1$, explicit $c_0$, explicit $N=500$, explicit $\delta_k$ table) — matching BBMST numerics, not abstract existence.
- They imply the full conjecture via the existing BBMST induction (Sections 4–5), which is otherwise unchanged.
- They explain the Lean failure: the Lean axiom attempted to assert Lemma A/B without $c_0$, quantifying over arbitrary `sfBlocks`; correct axiom must quantify over `exists_bbmst_data` with $c_0$ included and restrict to feasible $\delta$.

---

## 5. Barrier Classification — Technical vs. Intrinsic

| Aspect | Classification | Evidence |
|--------|----------------|----------|
| **Squarefree odd → impossible** | Proven, no barrier | $c_N^{SF}(1)=0.612$ leaves comfortable margin $0.388$ |
| **$2\mid L$ or $3\mid L$; $9\mid L$ or $15\mid L$** | Proven, no barrier | Sieve tail already forces small prime divisibility |
| **$\sigma(L)\ge2L$, $L\ge945$** | Proven, elementary | $\sum 1/m_i\ge1$ necessary, sharp |
| **Naïve monotone $s_k^{\mathrm{pow}}\ge s_k^{SF}\Rightarrow c_N^{\mathrm{pow}}<1$** | **Invalid** (false axiom, missing $c_0$) | `sieveProd>1` counterexample, $c_0$ dependence |
| **Extension with fixed $\delta_k^{SF}$** | **Technical barrier** | $c_0^{\mathrm{pow}}$ may exceed $c_0^{SF}$; fibre geometry for $p^e$ not isomorphic to $p$; $R$ vs collisions not bounded |
| **Extension with re-optimized $\delta_k^{\mathrm{pow}}$** | **Open technical barrier** — plausible to overcome with computation | Requires re-solving LP over 27 vs 16 ground set, recomputing bad-fibre bounds for prime-power trees; no in-principle obstruction but no published verification; BBMST authors deliberately stopped at SF because initial segment already delicate |
| **Intrinsic barrier: distortion method fundamentally incapable for prime powers** | **No evidence for intrinsic impossibility** — method not ruled out | Distortion method is flexible (works for minimum modulus problem, for $m_i$ with restricted divisibility); prime powers increase block sizes which helps the sieve, so heuristic suggests method *should* extend; failure would require $c_0^{\mathrm{pow}}$ significantly larger than $c_0^{SF}$, which is not expected but must be checked |
| **SAT/ILP computational search up to $L$ large** | Complementary, not resolving | Search space exponential in abundant $L$ branching; $L\ge945$ with $9\mid L$ or $15\mid L$ still infinite; finite negative search cannot prove non-existence; positive search could prove existence if lucky |
| **Lean formalization barrier** | **Technical + social** | Bloom 6316 blocks further axiomatic discussion pending full sorry/axiom-free formalization of BBMST itself; correct Lean statement must include $c_0$ and not quantify false `sieveProd<1` |

**Definitive classification:** The obstruction at non-squarefree moduli is a **technical gap in the initial-segment LP and fibre combinatorics**, not an intrinsic limitation of the sieve philosophy. The distortion method does **not** hit a known fundamental wall (like a counterexample within its framework); it hits an **unverified computational-analytic step** that BBMST left as a boundary. Calling it "fundamentally ruled out" for general odd would be false; calling it "trivially extends" is also false. The truth is **intermediate**: plausible extension, requires non-trivial new verification of Lemma A/C.

Analogy: Hough (2015) proved minimum modulus $\le10^{16}$ bounded; subsequent refinements lowered bound, but each prime-power extension required recomputation. Similarly here, dropping "squarefree" is not a one-line monotone corollary.

---

## 6. Roadmap to Resolution

### Phase 0 — Restore Baseline (Done in this repo)

- ✅ Extracted problem, bibliography, forum history, Lean placeholder to `.opencode/notes/erdos7.md`
- ✅ Reconstructed `ANSWER/report.tex`/`report.pdf` with abundant-$L$ proof and literature assessment
- ✅ This synthesis artifact `docs/synthesis_gap_analysis.md`

### Phase 1 — Certified LP for $c_0^{\mathrm{pow}}$ (Conditional Lemma C)

1. Enumerate $S_0^{\mathrm{pow}}=\{m\le73\text{ odd}\}$ and $S_0^{SF}\subset S_0^{\mathrm{pow}}$.
2. Re-implement BBMST LP (Sections 2–3): variables $w_m$, constraints from fibre capacities, objective $c_0(x)$. Compare optima.
3. Use exact rational / interval arithmetic (e.g., ` pulp` + ` fractions` or `z3` LP) to certify $c_0^{\mathrm{pow}}\le c_0^{SF}$ or find counterexample ($\approx$ few $10^4$ constraints — feasible on laptop).
4. If counterexample ($c_0^{\mathrm{pow}}>c_0^{SF}$), distortion method with current $\delta$ fails; go to Phase 2b.

**Deliverable:** `tools/lp_verify_c0.py` + certificate `docs/c0_pow_certificate.{tex,pdf,log}`.

### Phase 2a — Re-optimize $\delta_k$ (if Lemma C holds)

1. Keep BBMST $\delta_k^{SF}$ as witness; verify bad-fibre mass bound still holds with prime-power fibres (requires bounding collision probability for $p^e$-trees — adapt Hough–Nielsen Lemma 3.4 with $p^e$ branching factor).
2. Compute $c_N^{\mathrm{pow}}(1)=c_0^{\mathrm{pow}}\prod_{k\ge6}(1+1/((1-\delta_k)s_k^{\mathrm{pow}}))$ for $N=500$ with $s_k^{\mathrm{pow}}=\sum_{e\ge1,\,p_k^e\le Q} \phi(p_k^e)/p_k^e$ effective block count (or BBMST precise definition) and verify $<1$.
3. Lean formalization: encode corrected `c_N` with $c_0$, prove monotone tail lemma `s_pow ≥ s_sf → factor_pow ≤ factor_sf` (this part is elementary), combine.

**Deliverable:** Quantitative verification `docs/distortion_pow_tail.md`, Lean file `lean/BBMSTPowExtension.lean` sorry-free except for LP certificate axiom (or fully proved LP).

### Phase 2b — If $c_0^{\mathrm{pow}}$ Increases (alternative path)

- Increase `73` threshold or re-choose distortion shape (non-uniform $\delta$ for prime powers). The abundant condition $9\mid L$ or $15\mid L$ already forces branching at small primes; design split case analysis: $9\mid L$ vs $15\mid L$ separately with different $c_0$ values — this is how BBMST handled the $9/15$ refinement and may need refinement for $27,49,\dots$.
- Potentially need larger $N$ or smaller $x$ evaluation (BBMST $x=1$ is convenient; optimizing $x$ may recover margin).

### Phase 3 — Full Axiom-Free Lean Formalization (Bloom's bar)

- Formalize BBMST Sections 2–5 entirely in Lean 4 / Mathlib: LP duality, distortion measure construction, Lovász Local Lemma application, product bound. This is a multi-person-year effort (cf. Hough formalization attempts). Blocks discussion until done: no further forum claims accepted without this.
- Only then is Lemma A checkable as a Lean theorem, not an axiom.

### Phase 4 — Complementary Computational Search (SAT/ILP, optional)

- For completeness, formalize decision problem: `∃ distinct odd $m_i$, residues $a_i$, covering' is NP-complete (?) finite. Encode as SAT/ILP modulo $L$:
  - Variables $x_{m,a}\in\{0,1\}$ for each divisor $m\mid L$, residue $a\bmod m$.
  - Constraints: $\sum_{m\mid L} x_{m,a} \le 1$ per $m$ (distinctness via $m$ choice), covering $\forall r\in[0,L-1]\; \sum_{m,a: r\equiv a(m)}x_{m,a}\ge1$, parity $m$ odd.
- Tools: `python-sat` / `z3` / `ILP` solver. Search $L$ in increasing odd abundant order ($945,1575,2205,2427,\dots$) respecting $9\mid L$ or $15\mid L$.
- Expected outcome: no solution up to large $L$ (e.g., $10^5$) — strengthens heuristic but cannot prove non-existence.
- Artifacts checked: `docs/sat_ilp_reduction.md` (planned) should define reduction and report solver logs. The reduction is sound; the barrier is exponential explosion — $L=945$ already has $2^{15}$ subset choices × residues.

**Priority:** Phase 1 is **necessary and sufficient** for the sieve route; SAT search is heuristic support only.

---

## 7. Definitive Assessment Boxed Conclusion

> **Erdős Problem 7 is OPEN (VERIFIABLE).**
>
> **Proven:** (i) No squarefree odd distinct covering exists (BBMST22, $c_N(1)\approx0.612<1$); (ii) Any covering has $2\mid m_i$ or $3\mid m_i$, and any odd covering has $9\mid L$ or $15\mid L$; (iii) Any covering has $\sum_{d\mid L,d>1}1/d\ge1\iff\sigma(L)\ge2L$, so odd $L\ge945$. Two 2026 Lean attempts are invalid (missing $c_0$, false `sieveProd<1` axiom).
>
> **Not proven:** General odd distinct covering impossibility. The BBMST distortion sieve does **not** fundamentally preclude a prime-power extension, but the naïve monotone $p^e-1\ge p-1$ argument fails due to $c_0(x)$ dependence and distortion coupling. The exact missing piece is Conditional Lemma A/C — a certified LP bound $c_0^{\mathrm{pow}}(1)\le c_0^{SF}(1)$ with feasible $\delta_k$ — verifiable by finite computation but as yet unpublished and not formalized.
>
> **Barrier classification:** **Technical, not intrinsic.** Overcoming it requires re-solving the $p\le73$ LP with prime powers and re-certifying bad-fibre bounds for $p^e$-trees, not a new sieve philosophy. Until Lemma A/C is proved, the Erdős–Selfridge conjecture remains heuristic (sieve margin suggests true) but unresolved.
>
> **Roadmap:** Phase 1 — compute $c_0^{\mathrm{pow}}$; Phase 2 — verify $c_N^{\mathrm{pow}}(1)<1$ with (re-)optimized $\delta$; Phase 3 — axiom-free Lean formalization per Bloom's criterion; Phase 4 (auxiliary) — SAT/ILP search for $L$ abundant.

---

## 8. References

- P. Balister, B. Bollobás, R. Morris, J. Sahasrabudhe, M. Tiba — *On the Erdős covering problem: the density of the uncovered set.* Invent. Math. 230 (2022), 377–414. MR 4392459 — **BBMST22**.
- R. D. Hough, P. P. Nielsen — *Covering systems with restricted divisibility.* Duke Math. J. 168 (2019), 3261–3295. MR 4030365 — **HoNi19**.
- R. D. Hough — *Solution of the minimum modulus problem for covering systems.* Ann. Math. 181 (2015), 361–382.
- A. Schinzel — *Reducibility of polynomials and covering systems.* Acta Arith. 13 (1967/68), 91–101. MR 219515 — **Sc67**.
- M. Filaseta, K. Ford, S. Konyagin — *On an irreducibility theorem of A. Schinzel associated with coverings.* Illinois J. Math. 44 (2000), 633–643. — **FFK00**.
- Forum thread `erdosproblems.com/forum/thread/7` — 21 comments (2925–6316) including Tao, Bloom, Larsen, Sothanaphan critiques.
- Rafik Zeraoulia — Zenodo 18360978 (folklore abundant $L\ge945$ note + script) — comment 3717.
- L. Lovász Local Lemma / Shearer variant — underlying distortion method.
- Extraction checkpoint: `.opencode/notes/erdos7.md` (274 lines, 2026-08-25).
- Report: `ANSWER/report.tex` (327 lines) + `ANSWER/report.pdf` (5 pages).

---

## 9. Appendix — Formal Lean Sketch of Conditional Lemma

```lean
/- Conditional Lemma A — correct BBMST statement with c₀ -/
structure BBMSTData where
  c₀ : ℚ  -- LP optimum for p ≤ 73, ≈0.0979
  sfBlocks : List ℚ  -- s_k = p_k - 1 for k ≥ 6
  powBlocks : List ℚ -- s_k^pow ≥ s_k for k ≥ 6
  deltas : List ℚ   -- δ_k ∈ (0,1)
  h_pow_ge : ∀ i, powBlocks[i]! ≥ sfBlocks[i]!
  h_deltas_lt_one : ∀ δ ∈ deltas, 0 < δ ∧ δ < 1

def cN (c₀ : ℚ) (blocks deltas : List ℚ) (x : ℚ) : ℚ :=
  c₀ * List.prod (List.zipWith (fun s δ => 1 + x / ((1 - δ) * s)) blocks deltas)

-- The true BBMST theorem (SF case):
-- axiom bbmst_SF_correct : ∃ data : BBMSTData, cN data.c₀ data.sfBlocks data.deltas 1 < 1
-- with data.c₀ ≈ 0.0979 and product ≈ 6.25, cN ≈ 0.612

-- Conditional Lemma needed for general odd case:
axiom conditional_pow_extension (data : BBMSTData) (hSF : cN data.c₀ data.sfBlocks data.deltas 1 < 1)
  (hc₀ : data.c₀ ≤ 0.098) : cN data.c₀ data.powBlocks data.deltas 1 < 1
-- This axiom is NOT proved; requires LP certificate for c₀^pow and
-- fibre feasibility for powBlocks. The naive Lean attempted to assert
-- sieveProd _ 1 < 1 with sieveProd = ∏(1+1/s) (no c₀) — provably false.

theorem no_odd_covering_of_pow (data : BBMSTData) (h : cN data.c₀ data.powBlocks data.deltas 1 < 1)
  : ¬ ∃ (C : StrictCoveringSystem ℤ), (∀ i, Odd C.moduli[i]) ∧ C.Covers ℤ :=
  -- follows from BBMST distortion theorem: μ(uncovered) ≥ exp(-cN) > 0
  sorry -- reduces to BBMST Thm 3.1 + induction
```

The gap is exactly that `conditional_pow_extension` is **conjectural**.

---

## 10. Corrigendum (Integrated Verification 2026-08-25)

**Source:** `docs/final_verification.md` cross-read of `sieve_extension_obstruction.md` (Lemmas 4.1–4.5, Theorem 4.6) vs this file’s Conditional Lemmas A/B/C and `sat_ilp_reduction.md` invariants. `curl` live-checks of `https://www.erdosproblems.com/7`, `arXiv:1811.03547`, `arXiv:1703.02133` all PASS.

### C1 — Conditional Lemma A product form (Major)

Lemma A §4.1 as written `cN^{pow}(1):=c0^*∏(1+1/((1-δ*_k)s_k^{pow}))` with `s_k^{pow}=|B_k^{pow}∩[1,Q_k]|≥p_k-1` **oversimplifies** the BBMST operator for `γ≠1`. Per `sieve_extension_obstruction.md` Theorem 4.6(1)-(2) and (36)–(47),(84), the correct prime-power operator is

```
c_N^{(γ)}(x) = c0^{(γ)}(x) · ∏_k (1 + x/(1-δ_k^{(γ)}) · η_k^{(γ)})
η_k^{(γ)} := Θ_k-function of {p_j,γ_j,δ_{<k}^{(γ)}} given by 1811.03547 (36)–(47) and Θ_i(s,t) recursion (84)
Θ_i(s,t)=Θ_{i-1}(s,t)+1/(1-δ_i)∑_{j,k≥0,j+k>0} p_i^{-max{j,k}} Θ_{i-1}(⌈s/p_i^j⌉,⌈t/p_i^k⌉)
```

with prefactor `∑_{j=1}^{γ} p^{-j} = (1-p^{-γ})/(p-1)` so that `M_i^{(2)}` prefactor is `(∑p^{-j})^2=(1-p^{-γ})^2/(p-1)^2` which **increases** with `γ` (Cor. 4.2), not `1/(p^{γ}-1)^2`. The history product `∏_{j<i}(1+(3p_j-1)/((1-δ_j)(p_j-1)^2))` couples to earlier `γ`. Hence `s_k^{pow}≥s_k^{SF} ⇒ factor_pow≤factor_SF` holds pointwise for `U(s)=1+x/((1-δ)s)` but the list `blocks^{γ}` is **not** pointwise `≥blocks^{SF}` in the sense of Lemma 4.1 (cardinality/weights change) and `c0^{(γ)}≤c0^{SF}`, `δ^{(γ)}=δ^{SF}` are not theorems (Lemmas 4.4/4.5). The conditional claim must be restated as `c0^{(γ)}≤c0^{SF}` **and** `∏(1+η^{(γ)}/(1-δ^{(γ)}))≤∏(1+1/((1-δ^{SF})(p-1)))` after re-optimizing `δ^{(γ)}`; tail antitone in `s` alone is real but irrelevant. This file’s Lemma A should be read with that corrected operator; the quantitative `<1` target `cN^{SF}(1)≈0.612` with `c0≈0.0979` remains unchanged.

### C2 — Candidate L subset counts (Minor)

Exhaustive `2^{|D|}` enumeration (SymPy, `∑1/d≥1` exact rational) gives `L=945:67`, `1575:431`, **`2205:85`** (not `≈200–300`), **`2835:1709`** (not `≈1500`). Fractions `0.204%,0.329%,0.065%,0.326%` still `>99.7%` elimination; optimistic leaf bounds `~10^{13}–10^{15}` unchanged.

### C3 — Minimal `k` bound (Minor)

§1 table “`k≥15` for `L=945`” is inaccurate: minimal subset achieving `∑1/d≥1` is 10 smallest divisors `[3,5,7,9,15,21,27,35,45,63]` (`∑≈1.005`) for 945/1575/2835, and 12 for 2205 (`[3,5,7,9,15,21,35,45,49,63,105,147]`, `∑≈1.005`). Corrected: `10 ≤ k ≤ |D|` (`|D|=15,17,17,19`); max `|D|` unchanged.

No change to barrier classification (technical, not intrinsic) or roadmap Phases 1–4; SAT/ILP invariants (`∑1/d≥1`, `L≥945` odd abundant, `9|∨15|`, CRT `L/lcm` vs `gcd`, AMO/covering/SB encodings) verified exact and consistent with sieve prerequisites; live citations `erdosproblems.com/7`, `1811.03547`, `1703.02133`, `c_N=c0∏U` all PASS.

*End of corrigendum. Integrated state: `all_three_deliverables_consistent_and_complete` with above patches.*

---

*End of synthesis. Commit-ready.*
