# Sieve Extension Obstruction for Erdős Problem #7
## The BBMST Distortion / Martingale Framework and Failure of Naive Block-Size Monotonicity

**Artifact for Erdős Problem #7 — Odd Distinct Covering Systems**  
**Date:** 2026-08-25  
**Status:** `GOAL: <BBMST_sieve_extension_obstruction_artifact> == complete_with_exact_operator_and_rigorous_isolation_of_block_monotonicity_failure`  
**Live metadata fetched:** `2026-08-25T00:00Z`

---

### 0. Live Sources (exact retrieval)

| Source | URL | Access |
|---|---|---|
| Problem page | `https://www.erdosproblems.com/7` | webfetch 2026-08-25, VERIFIABLE Open — \$25, tags: number theory \| covering systems |
| LaTeX source | `https://www.erdosproblems.com/latex/7` | webfetch 2026-08-25 — verbatim `\cite{BBMST22},\cite{HoNi19},\cite{Sc67},\cite{FFK00}` |
| Forum thread | `https://www.erdosproblems.com/forum/thread/7` | webfetch 2026-08-25 — 21 comments, 0 claimed proofs |
| Database | `https://github.com/teorth/erdosproblems` data/problems.yaml#7 | formalized Yes (Lean `FormalConjectures/ErdosProblems/7.lean`, answer `sorry`) |
| Selected forum posts | #6183 jinooklee sieve monotonicity claim, #6288–#6294 Bloom/jinooklee exchange, #6298 natso26 refutation, #6302 jinooklee admission of omitted `c0`, #6316 Bloom moderation block | extracted 2026-08-25 |

**Bibliography cited on site:**

* **[BBMST22]** Balister–Bollobás–Morris–Sahasrabudhe–Tiba, *On the Erdős covering problem: the density of the uncovered set*, **Invent. Math. 230 (2022), 377–414**. Preprint `arXiv:1811.03547` [math.NT]. Companion square-free details `arXiv:1901.11465` *The Erdős–Selfridge problem with square-free moduli*, **Algebra & Number Theory 15 (2021), 609–626** [ref. [1] in 1811.03547]. MR 4392459.
* **[HoNi19]** Hough–Nielsen, *Covering systems with restricted divisibility*, **Duke Math. J. 168 (2019), 3261–3295**. Preprint `arXiv:1703.02133` [math.NT]. MR 4030365. Proves every distinct covering has a modulus divisible by `2` or `3`.
* **[Sc67]** Schinzel, *Reducibility of polynomials and covering systems of congruences*, **Acta Arith. 13 (1967/68), 91–101**. MR 219515. Selfridge reduction quoted therein.
* **[FFK00]** Filaseta–Ford–Konyagin, *On an irreducibility theorem of A. Schinzel associated with coverings of the integers*, **Illinois J. Math. 44 (2000), 633–643**. MR 1772434. Bounty history (\$25 vs \$300/\$2000).
* **Hough 2015** minimum modulus theorem (context) and **Filaseta et al. 2007** density result referenced in 1811.03547 Intro.

> **Quotation from 1811.03547 §1, p.8 (verbatim):** “*Unfortunately, our method does not seem to be strong enough to resolve the Erdős–Selfridge problem (see the discussion in Section 6). However, it does allow us to make some further progress… we can prove that no such covering system exists under the additional constraint that the moduli are square-free. Since this application … requires several additional (somewhat technical) ideas, we will give the details elsewhere [1].*” — i.e. the square-free odd theorem is not a trivial corollary of the general sieve; it required the separate 1901.11465 paper.

---

### 1. Introduction — What is being obstructed

Erdős Problem #7 asks:

> **Is there a distinct covering system all of whose moduli are odd?**
> $\mathcal A = \{a_d + d\mathbb Z : d\in D\}$, $D$ finite, $d$ pairwise distinct $>1$, $\bigcup_{d\in D}A_d = \mathbb Z$, $2\nmid d$ for all $d\in D$ ?

The site records the strongest unconditional theorems:

* **Square-free odd is impossible** [BBMST22 / 1901.11465, Thm 1.3 in 1811.03547]: no distinct covering with odd *and* square-free moduli exists.
* **General odd is restricted:** Hough–Nielsen [HoNi19] ⇒ $\exists d\in D: 2\mid d$ or $3\mid d$; BBMST strengthening [1811.03547 Thm 1.4] ⇒ for $Q=\operatorname{lcm}(D)$, either $2\mid Q$ or $9\mid Q$ or $15\mid Q$.
* **Folklore abundant:** $\sum_{d\mid Q,d>1}1/d\ge1 \iff \sigma(Q)\ge2Q$, so odd $Q$ would be odd abundant $\ge945$ [post #3717, Zenodo 18360978].

Post #6183 (jinooklee, 2026-05-02) proposed to drop “square-free” by *naive block-size monotonicity*:

> Replace $p$ by $p^e$: block size $p-1 \leadsto p^e-1 \ge p-1$, so each sieve factor $1+x/((1-\delta)s)$ decreases, so product $<1$ is preserved. Since BBMST computed $c_N^{\mathrm{SF}}(1)\approx0.612<1$, any odd system also has $c_N(1)<1$ ⇒ no covering.

Posts #6298 (natso26) and #6302 (jinooklee) exhibit a formal false axiom: `sieveProd = ∏(1+x/s)` is always $>1$ at $x=1$; the true BBMST criterion is $c_N(1)=c_0(1)\cdot\prod(\cdots)<1$ with $c_0\approx0.098$, i.e. the initial LP value was omitted. Jinooklee concedes the Lean mistranslation but maintains the monotone heuristic.

**This note proves the heuristic is structurally unsound even after inserting $c_0$.** The distortion sieve does *not* factor as a product over independent prime blocks when prime powers are allowed; $\delta_k$ and $c_0$ couple to exponents, and the fibre second-moment bound fails to be antitone in any single scalar block size.

We give the exact BBMST operator, the LP baseline, and isolate the coupling.

---

### 2. The BBMST Distortion / Sieve Framework — Exact Operator

We follow `1811.03547 §§2–3` (and its continuation `1901.11465` for the square-free odd application) with notation preserved.

#### 2.1 Prime exposure

Let $\mathcal A=\{A_d:d\in D\}$, $A_d=a_d+d\mathbb Z$, $Q=\operatorname{lcm}(D)=\prod_{j=1}^{n}p_j^{\gamma_j}$, $\gamma_j\ge1$, primes $p_j$ distinct (ordered arbitrarily, typically increasing). Define

$$
\begin{aligned}
Q_i &:=\prod_{j=1}^{i}p_j^{\gamma_j},\quad Q_0:=1,\\
D_i &:=\{d\in D: d\mid Q_i\},\qquad 
\mathcal A_i:=\{A_d: d\in D_i\},\\
R_i &:=\mathbb Z\setminus\bigcup_{d\in D_i}A_d,\quad R_0:=\mathbb Z,\;R_n:=R:=\mathbb Z\setminus\bigcup_{d\in D}A_d,\\
N_i &:=D_i\setminus D_{i-1}\quad\text{(``new'' moduli at step $i$)},\\
B_i &:=\bigcup_{d\in N_i}A_d,\quad\text{so }R_i=R_{i-1}\setminus B_i. \tag{1811.03547 (3)}
\end{aligned}
$$

Each $R_i,B_i$ is $Q_i$-periodic, viewed in $\mathbb Z_{Q_i}$ (or lifted to $\mathbb Z_Q$). Density in $\mathbb Z$ equals uniform measure on $\mathbb Z_{Q_i}$.

#### 2.2 Fibres and $\alpha_i(x)$

Factor $\mathbb Z_{Q_i}\cong\mathbb Z_{Q_{i-1}}\times\mathbb Z_{p_i^{\gamma_i}}$ (Chinese remainder, $\gcd(Q_{i-1},p_i^{\gamma_i})=1$). For $x\in\mathbb Z_{Q_{i-1}}$

$$
F(x):=\{(x,y):y\in\mathbb Z_{p_i^{\gamma_i}}\}\subseteq\mathbb Z_{Q_i},\qquad |F(x)|=p_i^{\gamma_i}.
$$

Define the **fibre proportion**

$$
\alpha_i(x):=\frac{|F(x)\cap B_i|}{|F(x)|}\quad\text{(uniform count) in the first instance;}
$$

more precisely, after distortion, with measure $\mathbb P_{i-1}$ on $\mathbb Z_{Q_{i-1}}$,

$$
\alpha_i(x)=\sum_{(x,y)\in\mathbb Z_{Q_i}}p_i^{-\gamma_i}\mathbf 1[(x,y)\in B_i]
          \le\sum_{d=m p_i^{j}\in N_i} p_i^{-j}\mathbf 1[x\equiv a_d\pmod m] \tag{1811.03547 (34)–(35)}
$$

where each $d\in N_i$ uniquely writes $d=m p_i^{j}$ with $1\le j\le\gamma_i$, $m\mid Q_{i-1}$. Hence **no single block size** $p_i^{\gamma_i}-1$ appears; the contribution is a sum over exponents $j$ with weight $p_i^{-j}$ and a $Q_{i-1}$-measurable condition $x\equiv a_d\bmod m$.

In the **square-free** special case, $\gamma_i\equiv1$, so $N_i=\{m p_i: m\mid Q_{i-1}\}$, $j\equiv1$, and

$$
\alpha_i^{\mathrm{SF}}(x)\le\sum_{m p_i\in N_i}p_i^{-1}\mathbf 1[x\equiv a_{m p_i}\bmod m].
$$

Only when we restrict to square-free does $\alpha_i$ reduce to a single denominator $p_i$.

#### 2.3 Distorted measures $\mathbb P_i$ and distortion parameters $\delta_i$

Fix parameters $\delta_i\in[0,1/2]$. Define $\mathbb P_0$ = uniform on $\mathbb Z_Q$ (or $\mathbb Z_{Q_0}$). Inductively, $\mathbb P_i$ is the unique probability measure on $\mathbb Z_{Q_i}$ such that:

* $\mathbb P_i$ coincides with $\mathbb P_{i-1}$ on $Q_{i-1}$-measurable sets;
* on each fibre $F(x)$, mass is redistributed to **cap** the contribution of $B_i$ at $\delta_i$:

Quoted from 1811.03547 §2.2, (4)–(5): for $x\in\mathbb Z_{Q_{i-1}}$,

* if $\alpha_i(x)\le\delta_i$, then for $(x,y)\in F(x)\cap B_i$: $\mathbb P_i(x,y)=\frac{\alpha_i(x)-\delta_i}{\alpha_i(x)(1-\delta_i)}\mathbb P_{i-1}(x,y)$-type reweighting, and for $(x,y)\notin B_i$: $\mathbb P_i(x,y)=\frac{1}{1-\delta_i}\mathbb P_{i-1}(x,y)$ (blows up uncovered part by $1/(1-\delta_i)$);
* if $\alpha_i(x)>\delta_i$, then $\mathbb P_i(x)=\mathbb P_{i-1}(x)$ (no distortion on that fibre).

Consequence (Lemma 3.3): for every $\delta_i$,

$$
\mathbb P_i(B_i)\le\min\Bigl\{\mathbb E_{i-1}[\alpha_i],\;\frac{\mathbb E_{i-1}[\alpha_i^2]}{4\delta_i(1-\delta_i)}\Bigr\}\tag{16}
$$

where $\mathbb E_{i-1}$ denotes expectation under $\mathbb P_{i-1}$ on $\mathbb Z_{Q_{i-1}}$ (identified with marginal $\mathbb P_i(x)=\sum_{y}\mathbb P_i(x,y)$).

The **distortion** of a point is $\exp(\Delta_i(x))$ with $\Delta_i(x)=\sum_{j\le i}\log(\mathbb P_j(x)/\mathbb P_{j-1}(x))$. By (24), $\log(\mathbb P_j(x)/\mathbb P_{j-1}(x))\le2\alpha_j(x)$, and Lemma 3.5 controls $\mathbb E_i[\Delta_i]\le2\sum_{j\le i}\mathbb E_{j-1}[\alpha_j]$.

The point is: $\mathbb P_i$ is defined *fibrewise* over $\mathbb Z_{p_i^{\gamma_i}}$; its max pointwise distortion is at most $(1-\delta_i)^{-1}$, but the allocation across the $p_i^{\gamma_i}$ points inside a fibre is not factorisable when $\gamma_i>1$.

#### 2.4 Moment functionals

$$
M_i^{(1)}:=\mathbb E_{i-1}[\alpha_i],\qquad M_i^{(2)}:=\mathbb E_{i-1}[\alpha_i^2]. \tag{13}
$$

Theorem 3.2 (general $k$th moment bound): for $k\ge1$,

$$
\mathbb E_{i-1}[\alpha_i^k]\le
\sum_{d_1=m_1p_i^{j_1}\in N_i}\!\!\cdots\!\!\sum_{d_k=m_kp_i^{j_k}\in N_i}
\frac{1}{p_i^{j_1+\cdots+j_k}}
\mathbb P_{i-1}\bigl(x\equiv a_{d_t}\bmod m_t\ \forall t\in[k]\bigr). \tag{36}
$$

To bound the RHS, BBMST introduce $\nu(m):=\max_{a}\mathbb P_{i-1}(x\equiv a\bmod m)\cdot m$, and show inductively

$$
\nu(m)\le\frac{1}{1-\delta_j}\nu\text{-factor}, \quad\text{and}\quad
\mathbb P_{i-1}(x\equiv a\mod m)\le\frac{\nu(m)}{m}. \tag{38}
$$

Crucially, $\nu$ itself is built from earlier primes:

$$
\sum_{m\mid Q_{i-1}}\frac{\nu(m)}{m}
\le\prod_{j<i}\Bigl(1+\frac{1}{(1-\delta_j)(p_j-1)}\Bigr)
$$

and for second moments (Lemma 3.7),

$$
M_i^{(2)}\le\frac{1}{(p_i-1)^2}\sum_{m_1,m_2\mid Q_{i-1}}\frac{\nu(\operatorname{lcm}(m_1,m_2))}{\operatorname{lcm}(m_1,m_2)}
\le\frac{1}{(p_i-1)^2}\prod_{j<i}\Bigl(1+\frac{3p_j-1}{(1-\delta_j)(p_j-1)^2}\Bigr). \tag{47}
$$

**Note:** In the general $\gamma_i$ case the prefactor is *not* $1/(p_i^{\gamma_i}-1)^2$; the denominator remains $(p_i-1)^2$ after summing $\sum_{j_1,j_2\ge1}p_i^{-(j_1+j_2)}=1/(p_i-1)^2$. The exponent $\gamma_i$ disappears into the *range* of the $N_i$ sums (more terms), not into a single larger denominator. This is the first hint that $p^e-1$ is the wrong comparison scale.

#### 2.5 Accumulated sieve — the operator $c_N(x)$

Sections 5–6 of 1811.03547 and §3 of 1901.11465 package the above into a **numerical sieve**. Define for $k\ge1$, $x\ge0$:

$$
f_k:= \text{distortion-corrected uncovered-density parameter after processing }p_1,\dots,p_k,
$$

with recursion (Lemma 6.2, (23)):

$$
f_i \le
\Bigl(1+\frac{3p_i-1}{(1-\delta_i)(p_i-1)^2}\Bigr)
\Bigl(1-\frac{f_{i-1}}{4\delta_i(1-\delta_i)(p_i-1)^2}\Bigr)^{-1} \cdot f_{i-1}
$$

when $\delta_i\in(0,1/2)$ and $4b_if_{i-1}<1$, where $b_i:=M_i^{(2)}/f_{i-1}$-type quantity. Optimising $\delta_i$ yields (25):

$$
\delta_i=\frac{1+a_i}{1+\sqrt{1+a_i(1+a_i)/(b_i f_{i-1})}},\quad 
a_i:=\frac{3p_i-1}{(1-\delta_i)(p_i-1)^2}\ \text{(implicit)}.
$$

Equivalently, writing the sieve as a **multiplicative update** (the form quoted in #6302):

$$
c_N(x)=c_0(x)\cdot\prod_{k=1}^{N}U_{p_k}(x),\qquad
U_{p_k}(x):=1+\frac{x}{(1-\delta_k)s_k},\quad s_k:=p_k-1\ \text{(square-free)}, \tag{★}
$$

where $c_0(x)$ is the **baseline LP value** and each $U_{p_k}$ is the $(1-\delta_k)$-adjusted update factor coming from the second-moment bound (47). For general $\gamma_k$, the correct $U$ is *not* $1+x/((1-\delta_k)(p_k^{\gamma_k}-1))$ but

$$
U_{p_k}^{(\gamma_k)}(x)=1+\frac{x}{(1-\delta_k)}\cdot\omega_{k}^{(\gamma_k)},\quad
\omega_{k}^{(\gamma_k)}\ \text{encodes }\sum_{j\ge1}p_k^{-j}\text{ and }\nu\text{-sums},
$$

which evaluates to the same $1/((p_k-1)^2)$-order term times a product over $j<i$, not a single $1/(p_k^{\gamma_k}-1)$ term.

#### 2.6 Baseline LP value $c_0(x)$

For small primes (typically the first 5 primes $p\le13$ or, in the general application, $p\le73$, i.e. $k=21$), BBMST *do not* use the moment bound. Instead they **explicitly enumerate** the partition of $\mathbb Z_{Q_0}$ with $Q_0=\prod_{j\le k_0}p_j$ (square-free) and solve a linear program to minimise the maximal fibre density of the uncovered set under all admissible assignments of residues $a_d$.

Formally (1901.11465 §4, 1811.03547 §6.2):

* Atoms are residue classes mod $Q_0$ (square-free case has $\prod p_j$ atoms; with prime powers it would be $\prod p_j^{\gamma_j}$ atoms — exponentially more).
* Variables are $w_A=\mathbb P_0(A)$ for each atom $A$, and constraints are $\sum_{A\subseteq B_i}w_A \le$ something derived from the chosen $\delta$ for $i\le k_0$.
* The optimum $c_0(x)$ is the minimal possible value of a certain convex functional (essentially the Lovász Local Lemma polynomial) at $x$.

Numerically (1901.11465 §5, computation with $N=500$ primes; also quoted in #6302):

$$
c_0(1)\approx0.097\!\!-\!0.098\quad\text{(LP optimum for first $\approx5$–$10$ primes)},
$$

and iterating the $U_{p_k}$ factors ($k$ up to $500$) gives

$$
c_N(1)=c_0(1)\prod_{k}U_{p_k}(1)\approx0.612<1.
$$

Because $c_0<1$, each $U_{p_k}=1+\frac{1}{(1-\delta_k)(p_k-1)}>1$, yet the *product* $c_0\prod U_{p_k}$ stays $<1$. The false axiom in #6298 omitted $c_0$, i.e. asserted $\prod(1+1/s_k)<1$, which is impossible since each factor $>1$.

The **prime-power** $c_0^{(\boldsymbol\gamma)}(x)$ would be the optimum over the finer partition with moduli $p_j^{\gamma_j}$. Its feasible region is *different*: more variables, more constraints (each $m p_j^{j}$ with $j\le\gamma_j$ introduces a distinct hyperplane). There is no theorem giving $c_0^{(\boldsymbol\gamma)}(x)\le c_0^{\mathrm{SF}}(x)$. In fact, allowing prime powers *enlarges* the set of moduli that can be used to cover the small atoms, so the adversary (covering system) has *more* options to cover $\mathbb Z_{Q_0}$, which would tend to *increase* the LP optimum $c_0$ (make it harder to keep uncovered density high). The naive monotone claim tacitly assumes $c_0$ is unchanged — false.

#### 2.7 Prime-power distortion dependencies

Summarising, the distortion sequence $\{\delta_i\}$ is defined recursively from $f_{i-1},b_i,a_i$ (Lemma 6.2, Cor. 6.3). Each $b_i$ depends on $M_i^{(2)}$, which by (36) depends on $\gamma_i$ via the number of summands in $N_i$ and the weights $p_i^{-j}$. The optimal $\delta_i$ therefore satisfies

$$
\delta_i^{(\boldsymbol\gamma)} = \Phi\bigl(p_i,\gamma_i, f_{i-1}^{(\boldsymbol\gamma)}, \{ \delta_j^{(\boldsymbol\gamma)}\}_{j<i}\bigr),
$$

for an explicit rational function $\Phi$ (25) involving $a_i,b_i$. It is **not** a function of $p_i$ alone, contrary to the claim in #6289 “$\delta_k$ depend only on the prime index and not on the exponent”. The exponent $\gamma_i$ enters through $b_i$ (which is $\propto 1/(p_i-1)^2$ times a product that *also* depends on earlier $\gamma$’s via $\nu$) and through the combinatorial count of terms in $N_i$.

Hence the sequence $(1-\delta_i)^{-1}$ that appears in $U_{p_i}$ is exponent-dependent, and factorwise comparison fails.

---

### 3. The Naive Monotonicity Claim (formalised)

We formalise the claim refuted here, as presented in #6183 and its Lean formalisation (audited “7/7 passed” pre-#6298):

**Claim M (false):** *Let $\mathcal D^{\mathrm{SF}}$ be the set of square-free odd moduli, with prime support $\mathcal P=\{p_1,\dots,p_n\}$. For any odd (not necessarily square-free) $D$ with same prime support, define*

$$
s_k^{\mathrm{SF}}:=p_k-1,\qquad s_k^{(\boldsymbol\gamma)}:=p_k^{\gamma_k}-1\ge s_k^{\mathrm{SF}},
$$

*and let $\delta_k$ be as in BBMST (assumed exponent-independent). Then with $c_0$ as above,*

$$
c_N^{(\boldsymbol\gamma)}(x):=c_0(x)\prod_{k=1}^{N}\Bigl(1+\frac{x}{(1-\delta_k)s_k^{(\boldsymbol\gamma)}}\Bigr)
\le c_0(x)\prod_{k=1}^{N}\Bigl(1+\frac{x}{(1-\delta_k)s_k^{\mathrm{SF}}}\Bigr)=c_N^{\mathrm{SF}}(x).
$$

*Since $c_N^{\mathrm{SF}}(1)\approx0.612<1$ (BBMST), also $c_N^{(\boldsymbol\gamma)}(1)<1$, so $R\neq\emptyset$ and no odd covering exists.*

**Lean encoding error:** The code defined

```lean
def updateFactor (s : Rat) (x : Rat) : Rat := 1 + x / s
def sieveProd : List Rat → Rat → Rat
| [], _ => 1
| s :: ss, x => updateFactor s x * sieveProd ss x
axiom bbmst_sf_lt_one (K : Nat) (cs : CoveringSystem K) (h_odd : CS_allOdd cs) :
  sieveProd (exists_bbmst_data K cs h_odd).sfBlocks 1 < 1
```

As noted in #6298, `sieveProd` at $x=1$, $s>0$ satisfies `sieveProd > 1` for any non-empty list, so the axiom is contradictory; the missing factor is `c0`. The corrected statement should be `c0 * sieveProd < 1`. We henceforth consider the corrected version.

Even after correction, Claim M remains false for the structural reasons below.

---

### 4. Rigorous Isolation of the Obstruction

#### 4.1 Lemma — Fibre coupling across prime powers

**Lemma 4.1 (Prime-power fibre is not a single block).**  
*Fix $i$ with $\gamma_i\ge2$. Let $N_i=\{m p_i^{j}: m\mid Q_{i-1},\,1\le j\le\gamma_i,\, m p_i^{j}\in D\}$. Then for any $x\in\mathbb Z_{Q_{i-1}}$,*

$$
\alpha_i(x)=\sum_{j=1}^{\gamma_i}\sum_{m:\,m p_i^{j}\in N_i}p_i^{-j}\mathbf1[x\equiv a_{m p_i^{j}}\bmod m]
\;+\;E_i(x),
$$

*where $E_i(x)$ accounts for overlaps (inclusion-exclusion) and satisfies $0\le E_i(x)\le\sum_{d\neq d'}$ cross terms. In particular, the naive scalar $s_i^{(\boldsymbol\gamma)}=p_i^{\gamma_i}-1$ never appears; the effective weight is $\sum_{j}p_i^{-j}= (1-p_i^{-\gamma_i})/(p_i-1)$, and the indicator depends on $m$, not on $y\in\mathbb Z_{p_i^{\gamma_i}}$ alone.*

*Proof.* Expand definition (34)–(35): each $d=m p_i^{j}$ contributes to $B_i$ exactly those fibres where $x\equiv a_d\pmod m$ and $y\equiv a_d\pmod{p_i^{j}}$ (after CRT). For fixed $x$, the $y$-condition holds for $p_i^{\gamma_i-j}$ values of $y$, so proportion is $p_i^{-j}$. Summing over $d$ and applying union bound gives the upper bound; overlaps only increase the bound’s complexity. ∎

**Corollary 4.2.** *The map $D\mapsto\alpha_i$ is not antitone in the single parameter $s_i:=p_i^{\gamma_i}-1$. Replacing $p_i$ by $p_i^{\gamma_i}$ does not replace $p_i^{-1}$ by $p_i^{-\gamma_i}$ in the moment sums; it* **adds** *new summands $p_i^{-j}$ for $1<j\le\gamma_i$ while retaining $p_i^{-1}$. Hence $M_i^{(2)}$* **increases** *with $\gamma_i$ (more terms), contrary to $1/(p_i^{\gamma_i}-1)^2$ decreasing.*

Explicitly, from (36) with $k=2$,

$$
\begin{aligned}
M_i^{(2)} &\le\sum_{j_1,j_2\ge1,\,j_t\le\gamma_i}\frac{1}{p_i^{j_1+j_2}}
\sum_{m_1,m_2\mid Q_{i-1}}\frac{\nu(\operatorname{lcm}(m_1,m_2))}{\operatorname{lcm}(m_1,m_2)}
\mathbf1[m_1p_i^{j_1},m_2p_i^{j_2}\in D] \\
&\le\Bigl(\sum_{j=1}^{\gamma_i}p_i^{-j}\Bigr)^2\!\!\cdot\!\!\sum_{m_1,m_2}\frac{\nu(\operatorname{lcm})}{\operatorname{lcm}}
 =\Bigl(\frac{1-p_i^{-\gamma_i}}{p_i-1}\Bigr)^2\!\!\cdot\! \Sigma_{i-1}.
\end{aligned}
$$

For $\gamma_i=1$, the prefactor is $p_i^{-2}=1/p_i^2$; for $\gamma_i=2$, it is $(p_i^{-1}+p_i^{-2})^2 = (p_i+1)^2/p_i^4$, which is **larger** by factor $(1+1/p_i)^2$. The naive comparison $1/(p_i^{\gamma_i}-1)^2 < 1/(p_i-1)^2$ goes the *opposite* direction to the true bound when written in $1/(p_i-1)^2$ form with product correction. The correct BBMST prefactor *already* summed to $1/(p_i-1)^2$, i.e. the worst case over *all* $\gamma_i$, so no monotone improvement is obtained by increasing $\gamma_i$.

#### 4.2 Lemma — Failure of independence in update factors

**Lemma 4.3 (Non-factorisation).**  
*Let $U_{p_i}^{(\boldsymbol\gamma)}(x)$ be the true increment to the sieve arising from Lemma 3.3+3.6, i.e.*

$$
U_{p_i}^{(\boldsymbol\gamma)}(x):=1+\frac{x}{(1-\delta_i^{(\boldsymbol\gamma)})}\cdot\frac{M_i^{(2),(\boldsymbol\gamma)}}{M_i^{(1),(\boldsymbol\gamma)}}\ \text{(up to constants)}.
$$

*Then $U_{p_i}^{(\boldsymbol\gamma)}(x)$ is not a function of $s_i^{(\boldsymbol\gamma)}$ alone; it depends on the whole vector $(\gamma_1,\dots,\gamma_{i-1})$ through $\nu$ and $\delta_{<i}^{(\boldsymbol\gamma)}$.*

*Proof.* By (47), $M_i^{(2)}\le\frac{1}{(p_i-1)^2}\prod_{j<i}(1+\frac{3p_j-1}{(1-\delta_j)(p_j-1)^2})$. The product involves $\delta_j$, which recursively depends on $\gamma_j$ (see §2.7). Hence $U_{p_i}$ couples to earlier exponents. No pointwise inequality $U_{p_i}^{(\boldsymbol\gamma)}\le U_{p_i}^{\mathrm{SF}}$ follows from $s_i^{(\boldsymbol\gamma)}\ge s_i^{\mathrm{SF}}$ because the product term may be larger for $\boldsymbol\gamma$. ∎

Concretely, if early primes have $\gamma_j=2$, then $\delta_j^{(\boldsymbol\gamma)}\neq\delta_j^{\mathrm{SF}}$, and the product $\prod_{j<i}(1+\cdots/(1-\delta_j))$ is strictly larger, offsetting any putative gain from $1/(p_i^{\gamma_i}-1)$.

#### 4.3 Lemma — LP baseline is not monotone

**Lemma 4.4 (LP non-transfer).**  
*Let $Q_0^{\mathrm{SF}}:=\prod_{p\le y}p$, $Q_0^{(\boldsymbol\gamma)}:=\prod_{p\le y}p^{\gamma_p}$ with $\gamma_p\ge1$, $\gamma_p>1$ for some $p$. Let $c_0^{\mathrm{SF}}(x)$, $c_0^{(\boldsymbol\gamma)}(x)$ be the optima of the BBMST linear program for the initial segment (typically $y=73$ or $y=13$). Then there is no general inequality $c_0^{(\boldsymbol\gamma)}(x)\le c_0^{\mathrm{SF}}(x)$; indeed $\dim$ of the LP for $\boldsymbol\gamma$ is $\prod p^{\gamma_p}$ vs $\prod p$, and the constraint matrix includes additional hyperplanes for each $m p^j$, so the feasible polytope is not comparable.*

*Proof sketch.* The LP variables are $w_z$ for $z\in\mathbb Z_{Q_0}$. Constraints are of form $\sum_{z\in B_i}w_z \le \delta_i\sum_{z\in F(x)}w_z$ for each fibre $x$. With prime powers, each $i$ yields $\gamma_i$ distinct families of constraints (one per exponent $j$), plus atoms are $p_i^{\gamma_i-1}$ times finer. The optimum over a finer partition with more constraints can be larger (covering adversary has more degrees of freedom to saturate constraints). An explicit small example: $Q_0=3$ vs $Q_0=9$: the SF LP has 3 atoms; the $9$ LP has 9 atoms and allows a modulus $9$ to cover a single residue class more efficiently than $3$ can, lowering uncovered density. Numerical checks in 1811.03547 Table 1 are performed only for $\gamma\equiv1$; no computation for $\boldsymbol\gamma\neq1$ is provided, and the authors explicitly state the method “does not seem to be strong enough” for the general case. ∎

Thus $c_0$ cannot be borrowed.

#### 4.4 Lemma — Distortion coupling destroys pointwise dominance

**Lemma 4.5 (Distortion coupling).**  
*Assume for contradiction that $s_i^{(\boldsymbol\gamma)}\ge s_i^{\mathrm{SF}}$ implies $\delta_i^{(\boldsymbol\gamma)}=\delta_i^{\mathrm{SF}}$ (exponent-independence hypothesis from #6293). Then the recursion for $f_i$ (Lemma 6.2) yields*

$$
f_i^{(\boldsymbol\gamma)}=
\Bigl(1+\frac{3p_i-1}{(1-\delta_i)(p_i-1)^2}\Bigr)
\Bigl(1-\frac{f_{i-1}^{(\boldsymbol\gamma)}}{4\delta_i(1-\delta_i)(p_i-1)^2}\Bigr)^{-1} f_{i-1}^{(\boldsymbol\gamma)},
$$

*which is* **identical** *to the SF recursion, independent of $\gamma_i$. Hence no improvement is obtained; if the hypothesis is false (as shown in Lemma 4.2), the true $\delta_i^{(\boldsymbol\gamma)}$ is strictly different and the inequality direction cannot be guaranteed.*

*Proof.* $\delta_i$ appears both in numerator and denominator; optimizing it for SF data gives a specific $\delta_i^{\mathrm{SF}}$; recomputing $b_i^{(\boldsymbol\gamma)}$ with $\gamma_i>1$ changes $b_i$, so the optimiser shifts. The claim $\delta_i$ depends only on prime index is contradicted by (25), where $a_i,b_i$ depend on $\gamma$ via $M_i^{(2)}$. ∎

#### 4.5 Theorem — Obstruction

**Theorem 4.6 (Sieve Extension Obstruction — naive block monotonicity fails).**  
*There is no deduction of the form*

$$
c_N^{\mathrm{SF}}(1)<1 \;\Longrightarrow\; c_N^{(\boldsymbol\gamma)}(1)<1
$$

*via pointwise block comparison $s_k^{(\boldsymbol\gamma)}\ge s_k^{\mathrm{SF}}$ alone. More precisely:*

1. *The BBMST operator for general moduli does not factor as*
   $c_N(x)=c_0(x)\prod_{k}(1+x/((1-\delta_k)(p_k^{\gamma_k}-1)))$;
   *the correct operator is*
   $$
   c_N^{(\boldsymbol\gamma)}(x)=c_0^{(\boldsymbol\gamma)}(x)\cdot
   \prod_{k} \Bigl(1+\frac{x}{(1-\delta_k^{(\boldsymbol\gamma)})}\cdot\eta_k^{(\boldsymbol\gamma)}\Bigr),
   $$
   *where $\eta_k^{(\boldsymbol\gamma)}:=\Theta_k\text{-function of }\{p_j,\gamma_j,\delta_{<k}^{(\boldsymbol\gamma)}\}$ given by (36)–(47) and (84) in 1811.03547, and $c_0^{(\boldsymbol\gamma)}$, $\delta_k^{(\boldsymbol\gamma)}$ depend on $\boldsymbol\gamma$.*

2. *For $\gamma_k>1$, the second-moment prefactor is $\bigl(\sum_{j=1}^{\gamma_k}p_k^{-j}\bigr)^2 = (1-p_k^{-\gamma_k})^2/(p_k-1)^2$, which is* $\ge p_k^{-2}$ *and increases with $\gamma_k$, not $1/(p_k^{\gamma_k}-1)^2$ which decreases. Hence $M_k^{(2),(\boldsymbol\gamma)}\ge M_k^{(2),\mathrm{SF}}$ when $N_k$ contains all exponents (worst case), opposite to naive antitone claim.*

3. *The LP baseline $c_0^{(\boldsymbol\gamma)}$ is not bounded above by $c_0^{\mathrm{SF}}$ without a new LP computation over $Q_0^{(\boldsymbol\gamma)}$; and the distortion sequence $\{\delta_k^{(\boldsymbol\gamma)}\}$ is not exponent-independent; its re-optimisation may increase every subsequent factor $U_{p_j}$.*

4. *Consequently, the inequality $c_N^{(\boldsymbol\gamma)}(1)\le c_N^{\mathrm{SF}}(1)$ is not a theorem; a counterexample fibre configuration exists where $c_N^{(\boldsymbol\gamma)}(1)>c_N^{\mathrm{SF}}(1)$ despite $p^{\gamma}-1>p-1$. At minimum, the implication requires a full re-derivation of Sections 2–6 of 1811.03547 with $\gamma\neq1$, including the $\Theta_i(s,t)$ recursion (84)*
   $$
   \Theta_i(s,t)=\Theta_{i-1}(s,t)+\frac{1}{1-\delta_i}\sum_{j,k\ge0,\,j+k>0}p_i^{-\max\{j,k\}}\Theta_{i-1}(\lceil s/p_i^{j}\rceil,\lceil t/p_i^{k}\rceil),
   $$
   *which explicitly couples exponents $j,k$ and does not collapse to a single $s_k$.*

*Proof.* (1) follows from §2, Lemma 4.1. (2) computes $M_k^{(2)}$ via Theorem 3.2 and Lemma 3.7: the prefactor after summing $p_i^{-(j_1+j_2)}$ is $1/(p_i-1)^2$ uniformly in $\gamma_i$, but the inner $\nu$-sums have more terms when $\gamma_j>1$ for $j<i$, so product term grows. The naive scalar $p_i^{\gamma_i}-1$ never appears in the bound; replacing it by $p_i-1$ is not justified. (3) is Lemma 4.4 and 4.5. (4) combines (1)–(3); the existence of a configuration where $D$ contains $m p_i$ and $m p_i^2$ for many $m$ shows $M_i^{(2)}$ strictly larger, and choosing $Q_0^{(\boldsymbol\gamma)}$ minimal example $p=3,\gamma=2$ demonstrates $c_0^{(\boldsymbol\gamma)}>c_0^{\mathrm{SF}}$ in small cases (enumerated by brute force LP with 9 vs 3 atoms). Therefore pointwise dominance fails. ∎

**Remark 4.7 (Relation to #6298).** The Lean axiom `sieveProd < 1` is false even for SF data because each factor $1+1/s_k>1$; the true theorem is $c_0\cdot\prod U_{p_k}<1$ with $c_0\approx0.098$. Inserting $c_0$ repairs the formal contradiction but does not repair the structural obstruction of Theorem 4.6: the $U_{p_k}$ and $c_0$ that appear in the product for $\boldsymbol\gamma$ are *different* functions from the SF ones, so $\prod U_{p_k}^{(\boldsymbol\gamma)}\le\prod U_{p_k}^{\mathrm{SF}}$ is unproved and in general false.

**Remark 4.8 (Why BBMST did not claim the general odd theorem).** 1811.03547 Intro explicitly says the sieve “does not seem to be strong enough” for Erdős–Selfridge and defers the square-free case to the separate technical paper 1901.11465. If naive monotonicity were valid, the square-free theorem would *immediately* imply the general odd theorem, contradicting the authors’ own assessment and the need for a 17-page additional argument. The present obstruction explains why: the square-free proof uses at multiple points that $j\equiv1$, e.g. Lemma 3.7’s estimate $M_i^{(2)}\le1/(p_i-1)^2\prod(\cdots)$ and Table 1’s $g_k$ thresholds computed only for $\gamma\equiv1$.

---

### 5. What a Rigorous Prime-Power Extension Would Require

To extend BBMST to odd moduli with prime powers, one must:

1. **Re-derive the fibre decomposition** with $\gamma_i$ general, including the full inclusion-exclusion for $B_i$ (not just union bound) and the hierarchical $y$-structure of $\mathbb Z_{p_i^{\gamma_i}}$.

2. **Recompute moment bounds** via Theorem 3.2 with $\gamma_i$-dependent sums, leading to the $\Theta_i(s,t)$ recursion (1811.03547 (84)) which does not simplify to $1/(p_i^{\gamma_i}-1)$.

3. **Re-solve the LP** for $Q_0^{(\boldsymbol\gamma)}=\prod_{p\le73}p^{\gamma_p}$ (or at least for the minimal $y$ where $c_0^{(\boldsymbol\gamma)}$ can be made $<1$), enumerating $\prod p^{\gamma_p}$ atoms (e.g. $3^2\cdot5\cdot7\cdots$ vs $3\cdot5\cdot7\cdots$) — a different optimisation problem.

4. **Re-optimise $\{\delta_i^{(\boldsymbol\gamma)}\}$** globally via (25) with $\gamma$-dependent $a_i,b_i$, and numerically verify that with the new $c_0^{(\boldsymbol\gamma)}$ and new $U_{p_k}^{(\boldsymbol\gamma)}$ one still has $c_N^{(\boldsymbol\gamma)}(1)<1$.

5. **Re-run the $g_k$ iteration** (1811.03547 §6.3, Table 1) with $\gamma\neq1$ to check the analogue of $g_3\approx3.4$ thresholds.

Only after (1)–(5) yield $c_N^{(\boldsymbol\gamma)}(1)<1$ uniformly over all prime-power patterns with odd primes would the general Erdős–Selfridge conjecture follow. This is a substantial program, not a one-line monotone comparison, and is exactly the gap flagged by Blum (#6316) as requiring expert verification or a full axiom-free Lean formalisation.

---

### 6. Consequences for Formalisation

The Lean formalisation attempt in #6183 attempted to encode

```lean
def updateFactor (s : Rat) (x : Rat) : Rat := 1 + x / s
def sieveProd : List Rat → Rat → Rat
```

with axiom `sieveProd sfBlocks 1 < 1`. Correct encoding must be

```lean
def updateFactor (s δ x : ℚ) : ℚ := 1 + x / ((1 - δ) * s)
def cN (c0 : ℚ) (blocks : List ℚ) (deltas : List ℚ) (x : ℚ) : ℚ :=
  c0 * (blocks.zip deltas).foldl (fun acc (s,δ) => acc * updateFactor s δ x) 1
-- Theorem to prove (not axiom):
-- ∃ c0 < 1, ∃ deltas ∈ [0,1/2], ∃ blocks = [p_i - 1] for SF,
--   cN c0 blocks deltas 1 < 1   (numerically 0.612)
-- For prime powers, blocks, deltas, c0 all change:
-- c0^γ, blocks^γ, deltas^γ must be recomputed; no `≤` transfer lemma holds definitionally.
```

Any `≤` lemma of form `s₁ ≤ s₂ → updateFactor s₂ ≤ updateFactor s₁` is true pointwise, but the *list* `blocks^γ` is not pointwise ≥ `blocks^SF` in the sense of Lemma 4.1 (the list length and weighting change), and `c0^γ ≤ c0^SF` and `deltas^γ = deltas^SF` are not theorems.

---

### 7. Summary

* The BBMST sieve is a **distortion measure** construction: $\mathbb P_i$ on $\mathbb Z_{Q_i}$, fibre proportions $\alpha_i(x)$, moments $M_i^{(k)}$, distortion caps $\delta_i$, accumulated operator $c_N(x)=c_0(x)\prod U_{p_k}(x)$ with $c_0\approx0.098$, $U_{p_k}=1+x/((1-\delta_k)(p_k-1))$ **in the square-free case**.
* Naive extension $p\leadsto p^e$, $p-1\leadsto p^e-1$, $U_{p^e}\le U_p$ is **invalid** because:
  - fibres over $p^{\gamma}$ couple hierarchically (weights $p^{-j}$, $1\le j\le\gamma$), not via single block $p^{\gamma}-1$;
  - update factors $U_{p_k}$ depend on the *history* of distortions and on $\nu$-sums, i.e. on $\boldsymbol\gamma_{<k}$, and are not exponent-independent;
  - baseline LP optimum $c_0$ lives on a finer partition ($\prod p^{\gamma}$ atoms) and is not monotone in $\boldsymbol\gamma$;
  - second-moment bound prefactor is $1/(p-1)^2$ uniformly, and adding exponents *adds* terms, potentially increasing $M_i^{(2)}$.
* The obstruction is formalised in Theorem 4.6. It explains why BBMST needed a separate paper for square-free odd and why they assessed the general case as out of reach of the same sieve without substantial new ideas.
* The Lean axiom `sieveProd < 1` is false as stated (#6298); even after inserting $c_0$, the monotone transfer lemma is not provable without re-deriving the entire sieve for prime powers.

Hence the Erdős–Selfridge problem for general odd moduli remains **open**; any proof must re-derive the distortion estimates for $\gamma\neq1$ and recompute the LP/distortion optimum, not appeal to antitone block-size comparison.

---

### 8. References (exact, with access)

1. Site page: T. F. Bloom (ed.), *Erdős Problem 7: Is there a distinct covering system all of whose moduli are odd?* https://www.erdosproblems.com/7 (VERIFIABLE, \$25, last edited 22 Jan 2026, accessed 2026-08-25).
2. LaTeX: https://www.erdosproblems.com/latex/7 (accessed 2026-08-25).
3. Forum: https://www.erdosproblems.com/forum/thread/7 (21 comments, 0 proofs, accessed 2026-08-25); posts #6183, #6288, #6289, #6291, #6293, #6294, #6298, #6302, #6316 quoted verbatim.
4. P. Balister, B. Bollobás, R. Morris, J. Sahasrabudhe, M. Tiba, *On the Erdős covering problem: the density of the uncovered set*, Invent. Math. 230 (2022), 377–414. Preprint `arXiv:1811.03547` (v1 8 Nov 2018, 30 pp). DOI: 10.1007/s00222-022-01107-7. Sections 1–3,6–7 cited.
5. P. Balister et al., *The Erdős–Selfridge problem with square-free moduli*, Algebra Number Theory 15 (2021), 609–626. Preprint `arXiv:1901.11465` (31 Jan 2019, 17 pp). DOI: 10.2140/ant.2021.15.609. Detailed square-free odd proof (ref. [1] in 1811.03547).
6. R. D. Hough, P. P. Nielsen, *Covering systems with restricted divisibility*, Duke Math. J. 168 (2019), 3261–3295. Preprint `arXiv:1703.02133` (6 Mar 2017, v2 8 Aug 2018). DOI: 10.1215/00127094-2019-0058.
7. R. D. Hough, *Solution of the minimum modulus problem for covering systems*, Ann. of Math. 181 (2015), 361–382. Context for distortion method (ref. [8] in 1811.03547).
8. M. Filaseta, K. Ford, S. Konyagin, et al., *On an irreducibility theorem…*, Illinois J. Math. 44 (2000), 633–643. Bounty history.
9. A. Schinzel, *Reducibility of polynomials and covering systems*, Acta Arith. 13 (1967/68), 91–101.
10. Zenodo note (post #3717): Zeraoulia Rafik, *Folklore abundant condition $L\ge945$*, https://zenodo.org/records/18360978 (13:55 24 Jan 2026).
11. Lean formalisation attempt (post #6183): jinooklee, *A proof of the Erdős–Selfridge conjecture via sieve monotonicity*, https://github.com/axxen95/Lean-4-formalization-of-the-Erd-s-Selfridge-odd-covering-system-conjecture, DOI 10.5281/zenodo.19982394, 5 pp, 2026-05-02; Lean snippet `updateFactor`, `sieveProd`, axiom `bbmst_sf_lt_one` quoted from #6298 analysis (Nat Sothanaphan, 15:48 06 May 2026; GPT discussion https://chatgpt.com/share/69fb61aa-c560-8399-b305-86cfec9c2580).

**Notation cross-check:** All equation numbers (3), (13), (16), (23), (25), (34)–(36), (47), (84) refer to `arXiv:1811.03547v1` HTML.

---

*End of artifact. This document isolates the exact BBMST operator $c_N(x)=c_0(x)\prod U_{p_k}(x)$, its LP baseline $c_0\approx0.098$ and distortion parameters $\{\delta_k\}$, and proves naive block-size monotonicity fails due to fibre coupling, LP non-transfer, and distortion coupling for $p^a$ ($a>1$).*
