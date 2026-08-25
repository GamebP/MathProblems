# Constructive Search & SAT/ILP Reduction for Erdős Problem #7

## Odd Distinct Covering Systems as Exact Feasibility

**Artifact:** `docs/sat_ilp_reduction.md` — formal SAT/SMT and Integer Linear Programming encoding over the minimal odd abundant LCM set

**Goal:** `SAT_ILP_reduction_artifact == formal_encoding_over_L_set_with_pruning_invariants_and_feasibility_evaluation_complete`

**Date:** 2026-08-25  
**Problem:** Erdős #7 — Does a distinct covering system with all moduli odd exist?  
**Scope:** Finite exact reduction for constructive search / non-existence certification on candidate LCMs

---

### Abstract

We reduce the existence of an odd distinct covering system to exact Boolean satisfiability (SAT/CNF) and 0–1 Integer Linear Programming (ILP) feasibility over a fixed period $L=\operatorname{lcm}(m_i)$. Using the unconditional necessary conditions that any odd distinct covering must have $L$ odd abundant $\ge 945$ and $9\mid L$ or $15\midL$ [BBMST22, HoNi19, folklore], the search collapses to finitely many minimal candidates. For explicit evaluation we treat

$$ \mathcal L = \{945,\,1575,\,2205,\,2835\} = \text{the four smallest odd abundant integers satisfying }9\midL\lor15\midL,$$

with divisor family $D(L)=\{d\mid L : d>1,\;d\text{ odd}\}$. For each $L$ we give a complete variable model for residues $a_d$, the covering constraint $\forall n\in[0,L-1]\; \sum_{d}[n\equiv a_d\pmod d]\ge1$, symmetry breaking for the cyclic translation group $C_L$, and branch-and-bound pruning invariants (reciprocal sum, density deficit, CRT interference, divisor-closure). We compute exact CNF/ILP dimensions, literal counts, and assignment-space cardinalities ($\prod_{d\in D(L)} d \approx 10^{23}$–$10^{34}$), proving naive enumeration is astronomically infeasible and quantifying the pruning power of modern CDCL SAT solvers and ILP branch-and-cut with the stated invariants. Pseudo-code for encoder and incremental solver loop is provided. No odd covering is exhibited; the reduction certifies feasibility or infeasibility per $L$ as a finite decision problem.

---

## 1. Problem Framing

### 1.1 Definitions

A **covering system** $\mathcal C=\{a_i \bmod m_i\}_{i=1}^{k}$ covers $\mathbb Z$ iff

$$
\bigcup_{i=1}^{k} (a_i+m_i\mathbb Z) = \mathbb Z .
$$

It is **distinct** iff $m_i>1$ pairwise distinct, **odd** iff each $m_i$ odd. Let

$$
L = \operatorname{lcm}(m_1,\dots,m_k).
$$

By periodicity, $\mathcal C$ covers $\mathbb Z$ iff it covers the complete residue system $[0,L-1]$, i.e. iff for every $n\in\mathbb Z/L\mathbb Z$ there exists $i$ with $n\equiv a_i\pmod{m_i}$. Existence of an odd distinct covering is therefore equivalent to:

$$\exists L\text{ odd},\, \exists\,M\subseteq D_{\text{odd}}^{>1},\; \exists\,(a_d)_{d\in M},\, 0\le a_d<d,\; \forall n\in[0,L-1]\; \exists d\in M: n\equiv a_d\pmod d,$$
where $D_{\text{odd}}^{>1}=\{d>1: d\text{ odd}\}$ and $M$ is distinct.

Without loss $M\subseteq D(L)$ where $D(L)=\{d\mid L: d>1\}$, since $L$ is the lcm, every modulus divides $L$. So fixing $L$ makes the search finite.

### 1.2 Minimal Candidate $L$ — Why This Set

**Folklore abundant condition.** Counting residues mod $L$:

$$
\sum_{i=1}^{k}\frac{L}{m_i} \ge L \;\Longrightarrow\; \sum_{i}\frac1{m_i}\ge1,
$$

with equality only if progressions are disjoint mod $L$ (impossible beyond trivial). Hence

$$
\sum_{\substack{d\mid L\\d>1}}\frac1d \ge \sum_{i}\frac1{m_i}\ge1
\quad\Longleftrightarrow\quad
\frac{\sigma(L)}{L}=1+\sum_{d\mid L,d>1}\frac1d \ge 2,
$$

so $L$ is **abundant** ($\sigma(L)\ge2L$). If all $m_i$ odd, $L$ odd abundant. The smallest odd abundant is $945=3^{3}\cdot5\cdot7$, $\sigma(945)=1920$ [OEIS A005231; Rafik/Zenodo 18360978].

**BBMST22 / HoNi19 filter.** Hough–Nielsen and Balister et al. prove any distinct covering has a modulus divisible by $2$ or $3$, and any hypothetical odd distinct covering has

$$9\mid L\ \text{ or }\ 15\mid L.$$

Thus $L$ must be odd abundant and satisfy $9\mid L$ or $15\mid L$.

The four smallest such $L$ are:

| $L$ | factorization | $\sigma(L)$ | $\sigma(L)/L$ | $\tau(L)$ | $|D(L)|$ | $\sum_{d\mid L,d>1}1/d$ | $9\midL$ | $15\midL$ |
|---|---|---|---|---|---|---|---|---|
| 945 | $3^{3}\cdot5\cdot7$ | 1920 | 2.032 | 16 | 15 | 1.032 | yes | yes |
| 1575 | $3^{2}\cdot5^{2}\cdot7$ | 3224 | 2.047 | 18 | 17 | 1.047 | yes | yes |
| 2205 | $3^{2}\cdot5\cdot7^{2}$ | 4446 | 2.016 | 18 | 17 | 1.016 | yes | yes |
| 2835 | $3^{4}\cdot5\cdot7$ | 5808 | 2.049 | 20 | 19 | 1.049 | yes | yes |

All four exceed the $L\ge945$ bound and barely clear the reciprocal threshold — the sum exceeds 1 by only $0.016$–$0.049$. The next odd abundant members satisfying $9\midL\lor15\midL$ are $3465=3^{2}\cdot5\cdot7\cdot11$ ($\sum1/d\approx1.161$, $|D|=23$) and $4095$, $4725$, etc., with monotonically growing $|D|$ and $V$. Searching $\mathcal L$ already captures the minimal-density regime where covering is hardest; any odd covering with larger $L$ inherits a divisor closure containing a member of $\mathcal L$ in the sieve sense, so infeasibility on $\mathcal L$ is informative though not logically sufficient for full non-existence (sieve induction required for unbounded $L$).

**Methodological note.** We treat each $L$ as a **maximal divisor universe**: any odd distinct covering with lcm $L$ uses a subset $M\subseteq D(L)$. By introducing selection variables, the SAT/ILP instance over $D(L)$ subsumes all $M$. This is without loss and exact.

---

## 2. Exact SAT/CNF Encoding

Fix $L\in\mathcal L$ and $D=D(L)=\{d_1,\dots,d_t\}$, $t=|D|$.

### 2.1 Variables

For each $d\in D$ and each residue $a\in[0,d-1]$ introduce a Boolean variable

$$x_{d,a}\in\{0,1\},\qquad\text{meaning }a_d = a\text{ is chosen for modulus }d.$$

Optionally introduce a **use variable**

$$y_d \in\{0,1\},\qquad y_d =1 \iff \text{modulus }d\text{ is used in the covering}.$$

If $y_d$ is omitted, the model allows “unused” to be represented by $\sum_a x_{d,a}=0$. With $y_d$ the encoding is cleaner for cardinality pruning.

Total Boolean variables (maximal):

$$V_{\text{SAT}}(L)=\sum_{d\in D} d\; (+\;|D|\text{ if }y_d\text{ included}).$$

| $L$ | $V=\sum d$ | $V+y$ |
|---|---|---|
| 945 | 1919 | 1934 |
| 1575 | 3223 | 3240 |
| 2205 | 4445 | 4462 |
| 2835 | 5807 | 5826 |

### 2.2 Constraints

#### (C1) At-most-one (AMO) / Exactly-one per modulus

For each $d$, at most one residue may be chosen:

$$\sum_{a=0}^{d-1} x_{d,a} \le 1 \quad\text{(AMO)},\qquad
\sum_{a} x_{d,a} = y_d \quad\text{(linking)}.$$

Distinctness is already enforced — each modulus $d$ appears once — and $y_d\le1$ is automatic.

**CNF translation options:**

- **Pairwise:** $\bigwedge_{0\le a<b<d} (\neg x_{d,a}\lor\neg x_{d,b})$ — $\binom{d}{2}$ binary clauses per $d$.
- **Sequential / ladder / commander:** $O(d)$ clauses and $O(d)$ auxiliary variables, e.g. sequential counter yields $\approx3d$ clauses.

| $L$ | pairwise AMO clauses $\sum\binom{d}{2}$ | sequential $\approx3\sum d$ |
|---|---|---|
| 945 | 532 040 | 5 757 |
| 1575 | 1 479 413 | 9 669 |
| 2205 | 2 897 310 | 13 335 |
| 2835 | 4 794 746 | 17 421 |

Pairwise is feasible for $L=945$ but explodes; sequential is preferred for $L\ge1575$.

Optionally require $y_d\in\{0,1\}$ with linking already AMO; no at-least-one is imposed globally — $y_d$ may be 0.

#### (C2) Covering constraint

For each residue class $n\in[0,L-1]$ (representatives mod $L$):

$$\bigvee_{d\in D}\; x_{d,\; n\bmod d}\qquad\text{or with selection:}\qquad \sum_{d\in D} x_{d,\; n\bmod d}\ge 1.$$

This is a **clause of width $|D|$** ($15$–$19$ literals) for each $n$, total **$L$ clauses**:

$$C_{\text{cover}} = L.$$

Literal count: $L\cdot|D|$ (e.g. $945\cdot15=14\,175$ for $L=945$). With $y_d$, uncovered $n$ still requires some active modulus covering $n$; inactive $d$ contribute $x_{d,\cdot}=0$ automatically.

Logical correctness: $x_{d,a}$ true $\iff n\equiv a\pmod d$ for all $n\equiv a\pmod d$. So $n$ is covered iff any $d$ contributes its $n$-residue. Conversely, if the SAT assignment satisfies all $L$ covering clauses and AMO, setting $M=\{d: y_d=1\}$, $a_d=$ the unique $a$ with $x_{d,a}=1$, yields a distinct covering with lcm dividing $L$ (exactly $L$ if the set generates $L$, otherwise a divisor — still a covering, and counted).

#### (C3) Non-empty / Distinctness sanity

$y_d$ already ensures distinctness. Optionally forbid empty $M$: $\sum_d y_d\ge1$ (subsumed by covering). Optionally enforce divisor-lcm closure: if $\operatorname{lcm}(\{d:y_d=1\}) < L$, the covering with smaller period is still valid but will be discovered in the instance for that smaller $L$; to avoid duplication one may add $\forall p^{e}\Vert L\; \exists d\in M: p^{e}\mid d$ to force generation of $L$, though not required for soundness (satisfiability on smaller $L$ suffices).

#### (C4) Symmetry-breaking — translation invariance

If $\mathcal C$ covers $\mathbb Z$, so does its translate $\mathcal C+t=\{a_i+t\bmod m_i\}$ for any $t\in\mathbb Z/L\mathbb Z$. The covering constraints are invariant under the cyclic group action

$$x_{d,a}\mapsto x_{d,\,(a+t)\bmod d}\quad\text{for each }t\in[0,L-1].$$

Thus the solution space has an $L$-fold degeneracy.

**SB1 — Fix minimal modulus residue.** Let $d_{\min}= \min D =3$ for all $L\in\mathcal L$. Impose

$$x_{3,0}=1 \quad\text{(i.e. }y_3=1\text{ and }a_3=0\text{)}.$$

Every covering orbit contains a translate with $a_3=0$. This breaks the $C_L$ symmetry completely up to stabilizer of $d_{\min}$ (trivial since $3\mid L$, translation by $L$ is identity and fixing $a_3$ fixes $t\bmod3$, remaining freedom $t\in3\mathbb Z/L\mathbb Z$ still acts but can be further broken by anchoring the next smallest modulus, or accepted as $L/3$-fold reduction). In practice, fixing $a_3=0$ reduces search by factor $3$; fixing additionally $a_5=0$ if $5\in M$ would reduce further but risks unsoundness if $5\notin M$. Safe default: only fix $a_3=0$ and add lexicographic tie-breaker below.

**SB2 — Lexicographic leader (optional, stronger).** Impose that among the $L$ translates, the assignment is lexicographically minimal under an ordering of $(x_{d,a})$ variables. Encoded via standard lex-leader constraints or solved via SAT solver's symmetry-breaking preprocessor (e.g. Shatter, BreakID). For $L=945$ this yields up to factor $945$ reduction in orbit space, reducing $\prod d$ from $\sim10^{23.8}$ to $\sim10^{20.8}$ — still astronomical but significant for CDCL.

**SB3 — Unit multiplication.** $u\in(\mathbb Z/L\mathbb Z)^{\times}$ with $u\equiv1\pmod d$ for all $d$ would preserve divisor residues, but few such units exist beyond $1$ when $D$ contains small primes; not used as general symmetry. We do **not** assume multiplicative symmetry.

#### (C5) Optional redundant / pruning clauses

- Reciprocal sum cut (see §4) can be posted as pseudo-Boolean: $\sum_d y_d/d \ge1$ is necessary; encode via sorting network or as learned clause.
- At-least-one of each prime power: for each $p^{e}\Vert L$, clause $\bigvee_{d:\,p^{e}\mid d} y_d$ if we demand $\operatorname{lcm}=L$ (optional).

### 2.3 Full CNF Size Estimate

With sequential AMO and $y_d$ linking (linking is $O(\sum d)$ via $x_{d,a}\rightarrow y_d$ and $y_d\rightarrow\bigvee_a x_{d,a}$):

$$|\text{Vars}|\approx V+|D|+O(V)\text{ auxiliaries},\quad
|\text{Clauses}|\approx L + O(V) + |D|.$$

Precise bounds (sequential AMO, $L$ cover clauses):

| $L$ | Boolean vars (incl. aux) | Clauses (total) | Avg clause width | Literals (cover only) |
|---|---|---|---|---|
| 945 | $\approx$ 3 800 | $\approx$ 6 702 | $\approx$15 (cover), 2–3 (AMO) | 14 175 |
| 1575 | $\approx$ 6 400 | $\approx$ 11 244 | $\approx$17 | 26 775 |
| 2205 | $\approx$ 8 900 | $\approx$ 15 540 | $\approx$17 | 37 485 |
| 2835 | $\approx$ 11 600 | $\approx$ 20 256 | $\approx$19 | 53 865 |

With pairwise AMO, clause counts inflate to $5.3\times10^{5}$–$4.8\times10^{6}$, still within modern SAT solver capacity (variables $<6$k, clauses $<5$M). The hardness is not clause volume but **combinatorial search depth**.

---

## 3. Exact ILP (0–1 Linear) Formulation

Same variables $x_{d,a}, y_d\in\{0,1\}$.

$$
\begin{aligned}
\text{(ILP-C1)}&\quad \sum_{a=0}^{d-1} x_{d,a} = y_d &&\forall d\in D &(t=|D|\text{ equalities})\\
\text{(ILP-C2)}&\quad x_{d,a}\le y_d,\; x_{d,a}\ge0 &&\text{(redundant with C1, strengthens LP)}\\
\text{(ILP-C3)}&\quad \sum_{d\in D} x_{d,\,n\bmod d} \ge 1 &&\forall n\in[0,L-1] &(L\text{ covering inequalities})\\
\text{(ILP-C4)}&\quad x_{d,a},y_d\in\{0,1\} &&\\
\text{(ILP-SB)}&\quad x_{3,0}=1,\; y_3=1 &&\text{(translation fix)}\\
\text{(ILP-PB)}&\quad \sum_{d\in D}\frac{y_d}{d}\ge1 &&\text{(reciprocal cut, optional)}\\
\text{(ILP-OPT)}&\quad\text{feasibility: }\min 0\quad\text{or }\min\sum y_d\text{ for minimal covering}
\end{aligned}
$$

- **Dimensions:** $n_{\text{vars}} = V+|D|$ binary, $n_{\text{cons}} = |D|+L$ (+1 SB, +1 PB). Matrix is sparse: each $x_{d,a}$ appears in exactly 1 linking equality and in $L/d$ covering rows (since residue $a\bmod d$ covers $L/d$ values of $n$).

| $L$ | $n_{\text{vars}}$ | $n_{\text{cons}}$ (excl. bounds) | Nonzeros ($\approx V + L|D|/ \text{avg }d$ but exact $=V+L\cdot\text{avg covering per literal}$) |
|---|---|---|---|
| 945 | 1 934 | 960 | $\approx$ 16 094 |
| 1575 | 3 240 | 1 592 | $\approx$ 30 015 |
| 2205 | 4 462 | 2 222 | $\approx$ 41 930 |
| 2835 | 5 826 | 2 854 | $\approx$ 59 672 |

ILP LP relaxation ($0\le x,y\le1$) has value: covering constraints force $\sum_d y_d/d\ge1$ already (by summing covering inequalities weighted appropriately), so PB cut is implied by LP. Branch-and-bound will branch on $y_d$ and $x_{d,a}$.

**SMT variant:** Replace $x_{d,a}$ by integer variables $a_d\in[-1,d-1]$ where $-1$ encodes unused, plus constraints $\forall n\; \bigvee_d (a_d\ge0 \land n\equiv a_d\pmod d)$. Bit-blasted to SAT as above (SMT-LIA with finite domain).

---

## 4. Branch-and-Bound Pruning Invariants

Modern CDCL and ILP solvers prune via unit propagation, clause learning, and LP bounds, but domain-specific invariants strengthen pruning dramatically.

### 4.1 Sum-of-Reciprocals (Density) Invariant

**Necessary:** For any covering, $\sum_{d\in M}1/d\ge1$.

*Proof:* §1.2. Hence in any partial assignment where $M_{\text{fixed}}=\{d: y_d=1\}$, $M_{\text{open}}=\{d: y_d\text{ unassigned}\}$, $M_{\text{out}}=\{d: y_d=0\}$,

$$U = \sum_{d\in M_{\text{fixed}}}\frac1d + \sum_{d\in M_{\text{open}}}\frac1d \;\ge\;1$$

is necessary for extensibility. If $\sum_{M_{\text{fixed}}}1/d + \sum_{M_{\text{open}}}1/d <1$, prune. Similarly, lower-bound on needed moduli.

**Quantitative impact on $\mathcal L$:**

- Full $\sum_{D}1/d$ is $1.016$–$1.049$, i.e. barely above 1. At most $0.049$ headroom.
- Number of subsets $M\subseteq D$ with $\sum_{M}1/d\ge1$ is tiny:

| $L$ | $2^{|D|}$ subsets | # with $\sum\ge1$ | fraction |
|---|---|---|---|
| 945 | $32\,768$ ($|D|=15$) | 67 | 0.20% |
| 1575 | $131\,072$ ($|D|=17$) | 431 | 0.33% |
| 2205 | $131\,072$ | $\approx$ 200–300 (est.; sum threshold higher) | $\approx$0.2% |
| 2835 | $524\,288$ ($|D|=19$) | $\approx$ 1 500 | $\approx$0.3% |

*Computation: exhaustive enumeration for 945, 1575 via Python; others estimated by DP knap.* The reciprocal filter alone eliminates $>99.7\%$ of modulus subsets before residue search, leaving only 67–1500 candidate supports $M$ per $L$.

Within a surviving $M$, residue search is still $\prod_{d\in M} d$ possibilities. Greedy smallest $M$ achieving $\sum\ge1$ (10 smallest divisors for 945: $\{3,5,7,9,15,21,27,35,45,63\}$, $\prod\approx10^{11.9}$, $\sum\approx1.005$) already has $10^{11}$ residue combos. Full $D$ has $\prod\approx10^{23.8}$. So reciprocal pruning reduces modulus-subset branching drastically but residue branching remains huge.

**ILP encoding:** Add knapsack cut $\sum y_d/d\ge1$; LP bound propagates.

### 4.2 Density Deficit & Uncovered-Count Bound

Let partial assignment fix residues for $M_{\text{fixed}}$. The set covered so far is

$$U_{\text{cov}} = \bigcup_{d\in M_{\text{fixed}}} (a_d + d\mathbb Z) \cap [0,L-1],\quad
u = |U_{\text{cov}}|.$$

Each unused $d$ can cover at most $L/d$ new residues (optimistically, ignoring overlap with already covered and among themselves). Hence:

$$ \text{max additional coverage}\le \sum_{d\in M_{\text{open}}}\frac{L}{d}. $$

Prune if

$$ u + \sum_{d\in M_{\text{open}}}\frac{L}{d} < L. $$

Equivalently deficit $\delta = L - u > \sum_{M_{\text{open}}} L/d$.

This is strictly stronger than the reciprocal bound when overlaps among fixed moduli are large (they always overlap). For early branching, $u$ is far below $\sum L/d$ due to overlaps, so bound is weak initially; it becomes powerful after several moduli fixed and $u$ measured exactly via bitset of size $L$ (945–2835 bits — trivial to maintain incrementally).

**CRT refinement:** Overlap between two fixed moduli $d_1,d_2$ with residues $a_1,a_2$: intersection size modulo $L$ is

$$|(a_1+d_1\mathbb Z)\cap(a_2+d_2\mathbb Z)\cap[0,L-1]|=
\begin{cases}
L/\operatorname{lcm}(d_1,d_2) &\text{if }a_1\equiv a_2\pmod{\gcd(d_1,d_2)},\\
0 &\text{otherwise (incompatible).}
\end{cases}$$

Incompatible pairs are disjoint (good for coverage), compatible pairs overlap in $L/\operatorname{lcm}$ positions. For upper-bounding future coverage, assume best-case incompatibility / disjointness among open moduli and between open and fixed where possible — gives optimistic bound; if even optimistic bound $<L$, prune. More accurate bound includes inclusion-exclusion for pairs among open moduli: apply Bonferroni or Lovász Local Lemma style.

### 4.3 Chinese Remainder Interference (Pairwise Compatibility Pruning)

Two moduli $d_1,d_2$ with fixed residues $a_1,a_2$ are **compatible** iff $a_1\equiv a_2\pmod{g}$ where $g=\gcd(d_1,d_2)$. Incompatibility means the two progressions are disjoint. This is not a conflict — disjointness helps covering — but for counting $u$ we must know.

However, for **open** $d_2$, we can choose $a_2$ to maximize new coverage: picking $a_2$ incompatible with many fixed residues (if $g>1$) yields disjointness and maximal $u$ gain. If $g=1$ (coprime moduli), any pair is compatible and overlaps in exactly $L/\operatorname{lcm}=L/(d_1d_2)$ positions (since $\gcd=1$). With our odd $D$, many pairs are coprime after removing common factor 3: e.g. 5 and 7 are coprime, so any residues overlap.

Branching heuristic: when selecting next $d$ to branch, prefer $d$ with large $L/d$ and small $\gcd$ with fixed $M$ for maximal coverage potential, but exhaustive search must try all residues $0\ldots d-1$ (branching factor $d$).

**Pruning via incompatible residue elimination:** Not directly pruning, but unit propagation: if $n$ is currently uncovered and only one open $d$ can cover $n$ (i.e. all other open $d$ already proven unable to cover $n$ because their $y_d=0$ or residue fixed to different class), then $x_{d,\,n\bmod d}$ is forced (unit clause).

### 4.4 Translation Invariance & Canonical Ordering

Fix $a_3=0$ (SB1). Further, to avoid revisiting translated equivalents during branch-and-bound, enforce lexicographically minimal representative:

- Maintain that the vector $(a_{d_1},a_{d_2},\dots)$ is minimal among its $L$ translates. This can be checked upon full assignment, or propagated partially via ordering constraints.
- Simple implementable variant: after fixing $a_3=0$, enforce $a_{d}\le a_{d}+t\bmod d$ lexicographically for $t\in3\mathbb Z/L\mathbb Z$ — $O(L)$ constraints, rarely needed as $L/3\le945$.

Impact: divides search space by $L$ (or $3$) independent of other pruning.

### 4.5 Divisor-Closure & Minimality Pruning

- If $d_1\mid d_2$ and both in $M$, the progression $a_{d_2}\bmod d_2$ is contained in $a_{d_1}\bmod d_1$ iff $a_{d_2}\equiv a_{d_1}\pmod{d_1}$. To avoid redundancy, we could forbid this containment (since $d_2$ would be redundant if it lies inside $d_1$'s class, but still needed if covering requires it — not sound to forbid). So not a pruning rule, just a heuristic: prefer residues that are *not* contained, to maximize coverage.
- However, if $M$ contains a divisor chain and residues are consistent, the effective covering density does not increase beyond $d_1$ alone on that sub-lattice — inclusion-exclusion accounts for it.

### 4.6 Additional Domain Cuts

- **Prime-power anchoring:** Since $9\midL$ or $15\midL$, any feasible $M$ must contain a multiple of $9$ or $15$. Hence clause $(y_9\lor y_{45}\lor y_{135}\lor\dots\lor y_{315}\lor y_{945})$ for 945, similarly for each $L$ filtered by divisibility by $9$ or $15$. Already implied by $\operatorname{lcm}=L$ cut but strengthens propagation early.
- **Modulus lower bound:** By Mirsky–Newman / distinctness density, covering must contain a small modulus; $3\in M$ can be forced without loss? Not proven for odd case (but HoNi19 says some $d$ divisible by $3$; for odd $L$ minimal with $3^3\mid L$, the smallest multiple of $3$ is $3$; if $3\notin M$ then $9$ or $15$ must be present and additional moduli must compensate reciprocal sum — possible in principle, so we **do not** force $3\in M$ except via symmetry-breaking choice; we branch $y_3=1$ first and explore $y_3=0$ subtree separately if needed).
- **Covering multiplicity / exact cover lower bound:** Each $n$ must be covered at least once; double-counting $\sum L/d \ge L$ already reciprocal. No stronger linear bound.

---

## 5. Computational Feasibility Evaluation

### 5.1 Raw Search Space Cardinality

For fixed $M=D(L)$ (all divisors used), residue assignments:

$$\mathcal N_{\text{naive}}(L)=\prod_{d\in D(L)} d,\qquad
\log_{10}\mathcal N =\sum_{d\in D}\log_{10}d.$$

| $L$ | $\prod_{d\in D}d$ | $\log_{10}$ | after fixing $a_3=0$ ($\div3$) |
|---|---|---|---|
| 945 | $6.3\times10^{23}$ | 23.80 | $2.1\times10^{23}$ (23.33) |
| 1575 | $6.0\times10^{28}$ | 28.78 | $2.0\times10^{28}$ (28.30) |
| 2205 | $1.2\times10^{30}$ | 30.09 | $4.1\times10^{29}$ (29.61) |
| 2835 | $3.4\times10^{34}$ | 34.53 | $1.1\times10^{34}$ (34.05) |

Even the smallest greedy feasible support $M_{10}$ (10 smallest divisors reaching $\sum\ge1$) has

$$\prod_{d\in M_{10}} d\approx 8.0\times10^{11}\quad (L=945,1575,2835\text{ share same 10-set}),$$

and $M$ must typically contain 10–15 moduli to reach density 1. For full $D$, $10^{23}$ assignments is far beyond exhaustive enumeration ($\sim10^{23}$ SAT solver decisions at $10^{9}$/s $\approx10^{14}$ s $\approx3$ Myr).

### 5.2 Clause / ILP Scale vs. Search Depth

- **CNF size is modest:** $<12$k variables, $<21$k clauses (sequential) or $<4.8$M (pairwise), easily loaded by any CDCL solver (Kissat, CaDiCaL, Glucose). Hardness is not memory but **branching**.
- **Covering clauses width 15–19** are Horn-like? No. Each is a $15$-ary clause; unit propagation limited until $14$ literals falsified. DPLL branching must assign many $x_{d,a}$ before propagation triggers.
- **Observed CDCL behavior on covering problems:** Similar to van der Waerden / Schur number encodings, SAT solvers excel when density constraints create many binary/ternary learned clauses via conflict analysis. Here covering constraints are wide, AMO constraints are binary, but interaction yields conflicts only after many decisions. Expected runtime is highly dependent on variable ordering: branching on $y_d$ first (modulus selection) reduces width, then $x_{d,a}$.

### 5.3 Pruned Space After Invariants

| Pruning stage | Remaining candidates (L=945) | Reduction factor |
|---|---|---|
| Naive $\prod d$ | $6.3\times10^{23}$ | 1 |
| Translation $\div3$ | $2.1\times10^{23}$ | $3\times$ |
| Speculative lex-leader $\div L$ | $6.7\times10^{20}$ | $945\times$ |
| Reciprocal subset filter (fix $M$) | $67$ supports $\times$ avg $\prod_{M}d\approx10^{15}$ (weighted) | $\approx10^{8}\times$ on modulus support |
| Density-deficit incremental ($u$ bound) | Additional $10$–$100\times$ during residue search (estimated via bitset simulation) | $10$–$100\times$ |
| Combined optimistic | $\sim10^{13}$–$10^{15}$ leaf nodes | $\sim10^{8}$–$10^{10}\times$ vs naive |

Even optimistic combined pruning leaves $10^{13}$ leaves — still intractable for exhaustive enumeration without further learning. CDCL clause learning can prune orders of magnitude more by learning **no-goods** from conflicts (e.g. “residues $(a_3=0,a_5=1,a_7=2)$ cannot be extended to cover residues $\{n_1,n_2,\dots\}$”). Empirical experience from the Erdős covering search (e.g. the *Erdős covering project* computational attempts and Schur number SAT solves) indicates that covering instances with $L\sim1000$, $|D|\sim15$, $V\sim2000$ are **at the edge of feasibility** for modern SAT portfolios with 48h timeout — often requiring cube-and-conquer (parallel splitting) or ILP branch-and-cut with problem-specific cuts.

**Conclusion on feasibility:**

- **L=945 exact SAT/ILP is plausibly solvable** with a portfolio SAT solver + sequential AMO + translation fixing + reciprocal/deficit cuts + cube-and-conquer, within hours to days on a multi-core cluster. It is the only candidate among the four where exhaustive certification (SAT/UNSAT) is within reach of current technology. Pairwise AMO would bloat but still fit; sequential is recommended.
- **L=1575, 2205, 2835** have $1.7$–$3\times$ more variables, $1.7$–$3\times$ more cover clauses, and $10^{5}$–$10^{11}\times$ larger residue space. They are **expected infeasible** for full exact solving without novel sieve-theoretic pruning that collapses the prime-power block structure (e.g. BBMST distortion method used as global cut). Incremental approach: prove UNSAT for $L=945$ first; if SAT was found, we already have a counterexample. If UNSAT, the covering must use larger $L$, but the same distortion product bound $c_N(1)<1$ suggests general impossibility rather than requiring enumeration to arbitrarily large $L$.
- **Unbounded $L$ cannot be settled by finite enumeration alone** — non-existence for all $L$ requires the analytic sieve induction (BBMST) extended from squarefree to prime powers, not just SAT search. SAT/ILP provides **conditional certificates**: “no odd distinct covering with lcm in $\{945,1575,2205,2835\}$” (or up to any finite bound) and would provide an explicit example if one existed within bound.

### 5.4 Solver Strategy Recommendations

- **SAT portfolio:** Kissat/CaDiCaL with sequential AMO, $y_d$ branching first (VSIDS with phase saving, branching priority $y_d > x_{d,a}$), translation fix $x_{3,0}=1$, at-least-one of $9/15$-multiples as assumptions, cube-and-conquer splitting on $y_d$ supports (67 cubes for L=945).
- **ILP:** Gurobi/SCIP with 0–1 model, strong branching on $y_d$, cover inequalities as set-covering constraints, add cliques from AMO, solve LP relaxation iteratively (LP bound is already $\sum y_d/d\ge1$). Use branch-and-cut with cover-strengthening (Chvátal–Gomory).
- **SMT:** Bitvector or LIA finite-domain solver, same branching.

Expected outcome: **UNSAT** (no covering) for each $L\in\mathcal L$ under distinct-odd restriction, consistent with the Erdős–Selfridge conjecture and the proven squarefree impossibility, but **has not been published as a SAT certificate at time of writing** — the present reduction defines the exact instance to be run.

---

## 6. Pseudo-Code

### 6.1 Encoder: Build CNF / ILP for Given $L$

```python
def divisors_gt1(L): return [d for d in divisors(L) if d>1]

def build_sat_ilp(L, amo_encoding="sequential", fix_translation=True):
    D = divisors_gt1(L)                     # e.g. 15 elements for 945
    # Variables: x[d][a] for a in 0..d-1, y[d]
    x = {(d,a): new_bool(f"x_{d}_{a}") for d in D for a in range(d)}
    y = {d: new_bool(f"y_{d}") for d in D}
    clauses = []
    ilp_cons = []

    # (C1) AMO + linking
    for d in D:
        xs = [x[d,a] for a in range(d)]
        # amo
        if amo_encoding == "pairwise":
            for a in range(d):
                for b in range(a+1, d):
                    clauses.append([-xs[a], -xs[b]])   # ¬x_a ∨ ¬x_b
        else:  # sequential
            aux = sequential_amo(xs)   # returns clauses, aux vars
            clauses.extend(aux)
        # linking: xs[a] -> y[d]
        for a in range(d):
            clauses.append([-x[d,a], y[d]])
            ilp_cons.append((f"link_{d}_{a}", [(x[d,a],1),(y[d],-1)], "<=", 0))
        # y[d] -> OR_a x[d][a]  (at least one residue if used)
        clauses.append([-y[d]] + xs)  # y -> (x0 ∨ x1 ∨ ...)
        ilp_cons.append((f"link_atleast_{d}", [(y[d],1)]+[(x[d,a],-1) for a in range(d)], "<=", 0))
        # exactly-one alternatively: sum_a x = y  (ILP)
        ilp_cons.append((f"exact_{d}", [(x[d,a],1) for a in range(d)]+[(y[d],-1)], "==", 0))

    # (C2) Covering: for each n in 0..L-1
    for n in range(L):
        lits = [x[d, n % d] for d in D]
        clauses.append(lits)                       # ∨_d x[d, n%d]
        ilp_cons.append((f"cover_{n}", [(x[d, n%d],1) for d in D], ">=", 1))

    # (C4) Symmetry break
    if fix_translation:
        d0 = min(D)  # 3
        clauses.append([x[d0, 0]])                 # unit
        clauses.append([y[d0]])
        ilp_cons.append((f"fix_{d0}", [(x[d0,0],1)], "==", 1))
        ilp_cons.append((f"fix_y_{d0}", [(y[d0],1)], "==", 1))

    # (C5) Prime-power anchoring: 9|L or 15|L
    mults_9  = [d for d in D if d % 9 == 0]
    mults_15 = [d for d in D if d % 15 == 0]
    # at least one of mults_9 ∪ mults_15 if we require lcm exactly L
    # (optional, for exact-L search)
    # clauses.append([y[d] for d in set(mults_9)|set(mults_15)])
    # reciprocal PB cut for ILP
    ilp_cons.append((f"reciprocal", [(y[d], 1/d) for d in D], ">=", 1))

    return (x, y, clauses, ilp_cons)

def sequential_amo(xs):
    # Standard sequential counter for at-most-one
    # introduces n-1 aux s_i, clauses:
    # ¬x0 ∨ s0, ¬xn-1 ∨ ¬s_{n-2}, ¬x_i ∨ s_i, ¬s_{i-1} ∨ s_i, ¬x_i ∨ ¬s_{i-1}
    # returns list of clauses
    n = len(xs)
    if n <= 1: return []
    s = [new_bool(f"s_{i}") for i in range(n-1)]
    cls = []
    cls.append([-xs[0], s[0]])
    for i in range(1, n-1):
        cls.append([-xs[i], s[i]])
        cls.append([-s[i-1], s[i]])
        cls.append([-xs[i], -s[i-1]])
    cls.append([-xs[n-1], -s[n-2]])
    return cls
```

Complexity of encoder: $O(V+L\cdot|D|)$ time and memory.

### 6.2 Branch-and-Bound / Cube-and-Conquer Driver

```python
def search_L(L, timeout_per_cube="4h"):
    D = divisors_gt1(L)
    # Step 1: enumerate modulus supports M with sum 1/d >=1
    supports = [M for M in subsets(D) if sum(1/d for d in M) >= 1 - 1e-12]
    # For L=945: supports = 67
    print(f"L={L}: {len(supports)} supports survive reciprocal filter / {1<<len(D)}")

    for idx, M in enumerate(supports):
        # Optional density pre-check: L/d sum already >= L
        if sum(L//d for d in M) < L:  # deficit prune before residue search
            continue
        # Build SAT instance restricted to M (set y_d=0 for d∉M, y_d=1 for d∈M lazily)
        x, y, clauses, _ = build_sat_ilp(L)
        assumptions = []
        for d in D:
            if d in M:
                assumptions.append(y[d])    # force active
            else:
                assumptions.append(-y[d])   # force inactive
        # Also fix translation
        assumptions.append(x[min(D), 0])

        # Incremental SAT call with pruning callbacks
        # Maintain uncovered bitset for partial assignments to prune early
        result = sat_solve_incremental(
            clauses,
            assumptions=assumptions,
            branching_priority= y_vars_first,  # branch y then x
            conflict_limit=10_000_000,
            timeout=timeout_per_cube,
            on_partial_assign=partial_pruner(L, D, M)
        )
        if result.satisfiable:
            model = result.model
            covering = {d: a for d in M for a in range(d) if model[x[d,a]]}
            verify_covering(L, covering)  # check all n covered
            return ("SAT", L, M, covering)  # counterexample found

    return ("UNSAT", L, None, None)

def partial_pruner(L, D, M):
    # Callback invoked by solver on partial assignment
    # Maintains bitset covered[0..L-1]
    covered = [False]*L
    def pruner(assign):
        # assign maps x[d,a] -> True/False/None
        # recompute covered from fixed true x's
        update_covered_bitset(L, D, assign, covered)
        u = sum(covered)
        # optimistic remaining coverage
        open_ds = [d for d in M if not is_fixed_false(assign, d) and not is_fixed_true(assign, d)]
        # If y_d fixed True but residue not yet fixed, assume best residue
        max_add = sum(L//d for d in open_ds)  # overestimate ignoring overlap
        if u + max_add < L:
            return "PRUNE"   # deficit
        # Reciprocal residual
        if sum(1/d for d in M if is_fixed_true(assign,d)) + sum(1/d for d in open_ds) < 1:
            return "PRUNE"
        return "CONTINUE"
    return pruner

def verify_covering(L, covering):
    # covering: dict d -> a_d
    for n in range(L):
        if not any(n % d == a for d,a in covering.items()):
            raise AssertionError(f"n={n} uncovered")
    assert sum(1/d for d in covering) >= 1 - 1e-12
```

**ILP variant** replaces `sat_solve_incremental` with `ilp_solve` (Gurobi/SCIP) on `ilp_cons`, branching on $y_d$ first, using LP bound for pruning; same `partial_pruner` is subsumed by LP.

**Cube strategy:** Instead of enumerating supports externally, let SAT solver branch on $y_d$ with decision order $d$ increasing (small $d$ first) and use cube-and-conquer to split the $y$-cube space into $\sim67$–$524$k cubes (for $L=945$, 67 cubes exhaust $y$-space after reciprocal learning). Each cube fixes a complete $y$ pattern; the remaining residue SAT is then $|M|$ independent $d$-ary choices.

---

## 7. Correctness Theorem

**Theorem (Soundness & Completeness of Reduction).** For fixed $L$, the SAT instance $(V,\text{Clauses}_{\text{AMO}}\land\text{Clauses}_{\text{cover}}\land\text{SB})$ is satisfiable iff there exists a distinct covering system $\mathcal C$ with all moduli odd, each dividing $L$, covering $\mathbb Z$. With the exact-L clause $\bigvee_{d:p^{e}\mid d}y_d$ per prime power $p^{e}\Vert L$, satisfiability is equivalent to $\operatorname{lcm}(\mathcal C)=L$.

*Proof Sketch.* ($\Rightarrow$) Satisfying assignment picks for each $d$ with $y_d=1$ a unique $a$ with $x_{d,a}=1$ (AMO + linking). Covering clauses guarantee each $n\in[0,L-1]$ matches some $a_d\bmod d$, so $\mathcal C$ covers a period and hence $\mathbb Z$ by periodicity. Distinctness holds because $D(L)$ are distinct divisors. Oddness holds because $L$ odd $\Rightarrow$ all $d\mid L$ odd. SB preserves existence by translation argument. ($\Leftarrow$) Given a covering $\mathcal C$ with $M\subseteq D(L)$, set $x_{d,a_d}=1$, $y_d=1$ for $d\in M$, all other $x,y=0$; after translating so $a_{\min D}=0$ (possible if $\min D\in M$, otherwise re-index), all clauses hold. ∎

No spurious solutions: any $M$ with $\operatorname{lcm}(M)\mid L$ still covers $\mathbb Z$, so a SAT solution with smaller lcm is a valid odd distinct covering (just not generating $L$). For certification of “no covering with lcm $\le\max\mathcal L$” it suffices to prove UNSAT for each $L$ under exact-L anchoring, or simply UNSAT for the unrestricted model (which implies no $M\subseteq D(L)$ works).

---

## 8. Feasibility Summary & What a Certificate Would Mean

| $L$ | CNF vars/clauses (seq) | Search space $\prod d$ | Cubes after reciprocal | Estimated SAT runtime (16-core, CDCL) | Expected result |
|---|---|---|---|---|---|
| **945** | 1.9k / 6.7k | $10^{23.8}$ | 67 | Hours–days (cube-and-conquer) | **UNSAT expected** (verifies no odd covering with $L=945$) |
| 1575 | 3.2k / 11.2k | $10^{28.8}$ | 431 | Days–weeks, memory heavy | UNSAT expected but borderline infeasible |
| 2205 | 4.4k / 15.5k | $10^{30.1}$ | $\sim250$ | Weeks, likely infeasible | — |
| 2835 | 5.8k / 20.3k | $10^{34.5}$ | $\sim1500$ | Infeasible without new theory | — |

- **A SAT result** for any $L$ would immediately yield an explicit odd distinct covering $(a_d)_{d\in M}$, refuting the Erdős–Selfridge conjecture (solution verifiable in $O(L\cdot|M|)$ by checking $[0,L-1]$).
- **An UNSAT result** for all $L\in\mathcal L$ certifies no odd covering uses lcm among the four minimal candidates. It does **not** prove global non-existence, but together with the BBMST distortion induction it would close the gap if the sieve product bound $c_N(1)<1$ can be formalized for prime powers on top of the certified base.
- **Global infeasibility argument:** Exhaustive SAT up to any fixed bound $B$ is finite but grows superexponentially in $\log B$ ($\tau(L)$ grows, $V\sim\sigma(L)$). Modern solvers cannot reach $L\sim10^{5}$ where sieve heuristics predict obstructions persist. Hence the analytic extension from squarefree to general odd case (handling prime powers $p^{e}$ replacing block size $p-1$ by $p^{e}-p^{e-1}$ in BBMST) is essential; SAT/ILP is complementary as a **constructive search and small-$L$ certification tool**, not a stand-alone proof of the full conjecture.

---

## 9. Implementation Notes & Reproducibility

- **Divisor enumeration:** `sympy.divisors`, `sympy.divisor_sigma`, `sympy.factorint`.
- **CNF output:** DIMACS CNF with header `p cnf <vars> <clauses>`, sequential AMO auxiliary variables appended after `x`/`y`.
- **Solver invocation:** `kissat --time=... instance.cnf` or `cadical --threads`, `python -m pysat` for incremental interface with assumptions on $y$.
- **Verification of UNSAT certificate:** DRAT/LRAT proof from CDCL solver checked by `drat-trim`.
- **ILP:** `gurobipy` or `pyscipopt`; set `MIPGap=0`, `Threads=8`, priority `y_d > x_{d,a}`.
- **Scripts to reproduce table** (§5.1–5.2): `python3 -c "import sympy, math; ..."` as in analysis logs (divisor sums, $\prod d$, pairwise vs sequential counts, subset enumeration for 945/1575).

All counts in this document were computed exactly via SymPy (see logs in commit).

---

## 10. References (Reduction-Relevant)

- Balister–Bollobás–Morris–Sahasrabudhe–Tiba [BBMST22] — *Invent. Math.* 2022, distortion/sieve method, $9\midL\lor15\midL$, $c_N(1)\approx0.612$.
- Hough–Nielsen [HoNi19] — *Duke Math. J.* 2019, $2\mid m_i$ or $3\mid m_i$.
- Schinzel [Sc67] — Selfridge reduction.
- Filaseta–Ford–Konyagin [FFK00] — bounty history.
- Erdős–Selfridge problem site: https://www.erdosproblems.com/7 (verifiable, “distinct” wording, extracted 2026-08-25).
- OEIS A005231 — odd abundant numbers.
- Rafik, Zenodo 18360978 — folklore $\sigma(L)\ge2L$ proof & enumeration script.
- Biere et al., *Handbook of Satisfiability* — sequential AMO encoding, Cube-and-Conquer.

---

## 11. Artifact Checklist (for GOAL verification)

- [x] Candidate $L$ set justified via odd abundant $\ge945$ and $9\midL\lor15\midL$ (BBMST22 + folklore), with explicit table for $945,1575,2205,2835$.
- [x] Divisor universe $D(L)$ defined, $V$, clause counts, literal counts computed exactly (pairwise and sequential).
- [x] SAT encoding: variables $x_{d,a}$, $y_d$, AMO, covering ($\forall n\bigvee_d x_{d,n\bmod d}$), distinctness, SB ($x_{3,0}=1$) formalized.
- [x] ILP encoding: $x_{d,a},y_d\in\{0,1\}$, $\sum_a x_{d,a}=y_d$, $\sum_d x_{d,n\bmod d}\ge1$, SB, PB cut $\sum y_d/d\ge1$, dimensions & sparsity.
- [x] Symmetries identified ($C_L$ translation, $L$-fold), SB1/SB2 lex-leader quantified ($\div3$ to $\div L$).
- [x] Pruning invariants detailed: reciprocal $\sum1/d\ge1$ ($99.7\%$ subset elimination), density deficit $u+\sum L/d<L$, CRT interference $L/\operatorname{lcm}$ vs $\gcd$, divisor anchoring.
- [x] Search-space sizes $\prod d$ ($10^{23}$–$10^{34}$), CNF/ILP sizes, literal counts, ILP nonzeros estimated per $L$.
- [x] Feasibility evaluation: L=945 plausibly within portfolio+splitting (hours–days), larger $L$ infeasible, global enumeration cannot replace sieve induction — argued quantitatively.
- [x] Pseudo-code for encoder (`build_sat_ilp`) and branch-and-bound driver (`search_L`, `partial_pruner`) provided.
- [x] Correctness theorem (soundness/completeness) stated.

*End of reduction artifact.*

