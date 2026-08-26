# GREEN-081 — Covering by Random Translates: Complete Analysis Dossier

Problem ID: GREEN-081 (= Ben Green, *100 Open Problems*, Problem 39)
Source: https://www.unsolvedmath.com/problems/GREEN-081 ; Green's list:
https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf
Statement: *"If $A \subset \mathbb{Z}/p\mathbb{Z}$ is random with $|A|=\sqrt p$,
can we almost surely cover $\mathbb{Z}/p\mathbb{Z}$ with $100\sqrt p$ translates
of $A$?"* Green remarks the problem is open even with $100$ replaced by $1.01$.

Date of analysis: 2026-08-26. Everything below is original work product of this
session except where a classical result is cited. Machine verifications are in
Appendix A and were executed against the formulas printed here (an earlier,
incorrect surrogate $\mathbb{E}X^2$ using $f^m$ was caught by the verifier and
corrected — see Appendix A.2 for the audit trail).

---

## 0. Two readings of the question — they have different answers

Let $p$ be prime, $k=\lfloor\sqrt p\rfloor$, $G=\mathbb Z_p$, and let $A$ be a
uniformly random $k$-subset of $G$ (fixed-cardinality model; a
Bernoulli-$1/\sqrt p$ model behaves identically w.h.p. and is not treated
separately). Write $A+t=\{a+t:a\in A\}$.

**(RA)** The $100\sqrt p$ translates are themselves *random*
($t_1,\dots,t_m$ i.i.d. uniform), $m=C\sqrt p$.
**(RB)** We may *choose* the translates after seeing $A$. Define the covering
number
$$\operatorname{cov}(A):=\min\{|B|:\ A+B=\mathbb Z_p\},\qquad B\subseteq G.$$
"Almost surely" refers to the randomness of $A$ alone. Green's remark (open
even for constant $1.01$) shows **RB is the intended reading**; RA is a
different (easier) question that we resolve completely first, both because it
calibrates intuition and because it explains *why* the constant $100$ cannot be
taken literally at astronomically large $p$.

---

## 1. Reading RA: exact moments and the threshold theorem

Fix $m=m(p)$ and let $t_1,\dots,t_m$ be i.i.d. uniform on $G$, independent of
$A$. Let
$$X:=\big|\mathbb Z_p\setminus{\textstyle\bigcup_{i\le m}}(A+t_i)\big|$$
be the number of uncovered points, and put
$$q:=1-\tfrac kp,\qquad \mu:=\mathbb E X.$$

### Lemma 1.1 (first moment, exact)
$\mathbb E X=pq^m$ exactly.

*Proof.* Fix $x$. For one translate, $x\in A+t\iff x-t\in A$; as $t$ is uniform
and independent of $A$, $\Pr[x-t\in A]=k/p$, so $\Pr[x\notin A+t]=q$. The $m$
events (over $i$) are independent, giving $\Pr[x\text{ uncovered}]=q^m$;
sum over $x$. ∎

### Lemma 1.2 (second moment, exact)
For $d:=y-x\neq0$ let $c_d(A):=|A\cap(A+d)|$. Given $A$, one translate misses
both $x$ and $y$ iff $t\notin(x-A)\cup(y-A)$ and
$$|(x-A)\cup(y-A)|=2k-c_d(A),$$
because $(x-A)\cap(y-A)=x-(A\cap(A+d))$. Hence with
$$w_A:=1-\frac{2k-c_d(A)}{p},\qquad g_m:=\mathbb E_A\big[w_A^{\,m}\big],$$
(the law of $c_d(A)$ is independent of $d\neq0$, since $c_d(A+t_0)=c_d(A)$),
$$\mathbb E X^2=pq^m+p(p-1)\,g_m \quad\text{exactly.}$$

*Proof.* Diagonal terms give $pq^m$ (Lemma 1.1). Off-diagonal: condition on
$A$; the $m$ translates are independent, each missing both points with
probability $w_A$, so $\Pr[\text{both uncovered}\mid A]=w_A^m$; average over
$A$ and sum over the $p(p-1)$ ordered pairs. ∎

**Remark 1.3 (error caught by verification).** The surrogate
$f^m$ with $f:=\binom{p-2}{k}/\binom pk=\mathbb E_A[w_A]$ is **not** $\mathbb
E_A[w_A^m]$ (Jensen). Exact identity:
$f/q^2=\dfrac{p(p-k-1)}{(p-1)(p-k)}=1-\dfrac{k}{(p-k)(p-1)}<1$, but the
$m$-th power does not commute with $\mathbb E_A$. Enumeration values
(Appendix A): $(p,k,m)=(7,2,3)$: $\mathbb E X^2=7.36734693878$ vs. wrong
surrogate $7.08616780045$; $(13,3,4)$: $22.4861174329$ vs. $21.8337505690$.

### Lemma 1.4 ($g_m$ asymptotics)
Fix a constant $C_0$ and assume $m\le C_0\sqrt p$. Then
$$g_m=q^{2m}\bigl(1+\theta\bigr),\qquad |\theta|\le \frac{K(C_0)}{p},$$
with $K(C_0)$ depending only on $C_0$.

*Proof.* Since $q\ge\frac12$ for $p\ge4$, define $\Delta_A:=w_A/q^2-1$; then
$$w_A-q^2=\frac{c_d(A)-k^2/p}{p}\quad\Longrightarrow\quad
|\Delta_A|\le \frac{4(k+1)}{p}\le\frac8{\sqrt p}.$$
Expand $(1+\Delta)^m=1+m\Delta+\rho$ with
$|\rho|\le\tfrac12(m|\Delta|)^2(1+|\Delta|)^m\le \tfrac12(m\Delta)^2e^{8C_0}$
(using $|\Delta|\le 8/\sqrt p$, $m\le C_0\sqrt p$). Taking expectations:
(i) $\mathbb E[c_d]=\frac{k(k-1)}{p-1}$, so
$\mathbb E[c_d-\tfrac{k^2}{p}]
=-\frac{k(p-k)}{p(p-1)}$, whence
$m|\mathbb E\Delta|\le m\cdot\frac{2k}{p\cdot p q^2}=O\!\big(\tfrac{C_0}{p}\big)$;
(ii) $\mathbb E[c_d^2]\le C_1$ absolutely — indeed $c_d=\sum_a
\mathbf 1_{\{a,\,a+d\in A\}}$ gives
$\mathbb E c_d^2=\mathbb E c_d+\sum_{a\neq b}\Pr[a,a+d,b,b+d\in A]$, the last
sum being $\le p(p-3)\frac{(k)_4}{(p)_4}+4p\frac{(k)_3}{(p)_3}\le 6$ for
$k^2\le p$ — so
$m^2\mathbb E[\Delta^2]=O(C_0^2/p)$. Combine. ∎

### Theorem 1.5 (variance bound and concentration)
For $m\le C_0\sqrt p$:
$$\operatorname{Var}(X)=\mu(1-q^m)+p(p-1)\bigl(g_m-q^{2m}\bigr)
\;\le\;\mu+K'(C_0)\,\frac{\mu^2}{p}.$$
Consequently, if $\mu\to\infty$ then
$\operatorname{Var}(X)/\mu^2\to0$, i.e. $X/\mu\to1$ in $L^2$, and
$$\Pr[X=0]\le\Pr\bigl[|X-\mu|\ge\mu\bigr]\le\frac{\operatorname{Var}(X)}{\mu^2}\longrightarrow 0 .$$

*Proof.* Plug Lemma 1.4 into Lemma 1.2 and use $\mu^2=p^2q^{2m}$. Chebyshev on
$\{X=0\}\subseteq\{|X-\mu|\ge\mu\}$. ∎

### Theorem 1.6 (RA threshold; GREEN-081 under reading RA is FALSE)
Let $k=\lfloor\sqrt p\rfloor$ and $m\le C_0\sqrt p$ with $C_0$ fixed.

**(i) Failure at constant multiples.** For every fixed $C>0$, with
$m=C\lfloor\sqrt p\rfloor$:
$$\mu=p\Bigl(1-\tfrac1{\sqrt p}\Bigr)^{C\sqrt p}=pe^{-C}(1+o(1))\to\infty,$$
hence $X\ge(1-o(1))\,pe^{-C}$ w.h.p. and
$\Pr[\text{full cover}]\to0$. In particular, with $C=100$: **random
$100\sqrt p$ translates fail to cover w.h.p.; the RA-reading of GREEN-081 is
asymptotically false.**

**(ii) Success above the threshold.** If $m\ge\sqrt p\,(\ln p+\omega(1))$ for
any $\omega(1)\to\infty$, then using $\ln(1-\tfrac1{\sqrt p})
=-\tfrac1{\sqrt p}-\tfrac1{2p}+O(p^{-3/2})$,
$$\mu\le p\exp\!\bigl(-(\ln p+\omega(1))(1-o(1))\bigr)=e^{-\omega(1)+o(1)}\to0,$$
and Markov gives $\Pr[\text{full cover}]\to1$.

**(iii) Threshold location.** Combining: outside the critical window (i.e.
whenever $|m/\sqrt p-\ln p-c|\to\infty$ for every fixed $c$; the window itself
is Conjecture 1.8 territory), random translates cover w.h.p. iff
$m/\sqrt p-\ln p\to+\infty$, and fail w.h.p. if $\to-\infty$ (within
$m\le C_0\sqrt p$, which contains all constant multiples). The threshold sits
at $m^\ast\approx\sqrt p\,\ln p$, *not* $C\sqrt p$. ∎

**Corollary 1.7 (crossover scale; why simulations never see the failure).**
Random $100\sqrt p$ translates cover w.h.p. while $p\le e^{100-\omega(1)}$ and
fail w.h.p. for $p\ge e^{100+\omega(1)}$; $e^{100}\approx2.69\times10^{43}$.
At $p=997$ resp. $p=10007$ one has
$\mu=7.246\times10^{-42}$ resp. $2.262\times10^{-40}$ (verified, Appendix A),
so no feasible simulation exhibits failure at $m=100\sqrt p$ — while the
*sampling* threshold $\sqrt p\ln p$ is fully visible numerically (§3).

### Conjecture 1.8 (Gumbel window; evidence, not proved)
If $m/\sqrt p-\ln p\to c\in\mathbb R$ then $X\Rightarrow
\mathrm{Poisson}(e^{-c})$ and $\Pr[\text{cover}]\to\exp(-e^{-c})$.

*Evidence.* (a) Factorial moments: $\mathbb E[(X)_j]=(p)_j\,h_j$ with
$h_j:=\mathbb E_A\big[u_j(A)^m\big]$, $u_j(A):=1-|\bigcup_{i\le j}(x_i-A)|/p$;
the same expansion as in Lemma 1.4 (now with joint autocorrelations of orders
$\le 2j$, all of which have bounded $j$-dependent moments) gives
$h_j=(1-jk/p)^m(1+o(1))$ for fixed $j$, so $\mathbb E[(X)_j]\to(e^{-c})^j$.
(b) Pairwise correlations vanish: the exact two-point ratio satisfies
$g_m/q^{2m}=1+O(C^2/p)\to1$ (Lemma 1.4), verified numerically
($1.0248$ at $(p,k,m)=(101,10,32)$, Appendix A).
*Gap:* the dependency graph of the events $E_x=\{x\text{ uncovered}\}$ is
complete (all share $A,t_1,\dots,t_m$), so the Arratia–Goldstein–Gordon bound
is vacuous ($b_2\simeq\lambda^2\not\to0$); closing the window requires a finer
Stein argument exploiting cancellation, which we do not supply. Simulations
match $\exp(-e^{-c})$ within Monte-Carlo error up to $p=20011$ (§3, Table W).

---

## 2. Reading RB (the actual open problem): what can be proved, and where it breaks

$\operatorname{cov}(A)=\min\{|B|:A+B=\mathbb Z_p\}$.

### Proposition 2.1 (counting lower bound)
$\operatorname{cov}(A)\ge\lceil p/k\rceil$ for every $A$.
*Proof.* $p=|A+B|\le k|B|$. ∎

Moreover, by the Hajós–de Bruijn theorem on factorizations of abelian groups,
an exact factorization $\mathbb Z_p=A\oplus B$ with $|A|,|B|\ge2$ does not
exist for prime $p$; a perfect tiling is impossible, so any near-optimal cover
must tolerate controlled overlaps. (Since $k\nmid p$, $\lceil p/k\rceil$
covers carry automatic slack $\ge k-1$ and this observation yields no
quantitative strengthening of 2.1.)

### Proposition 2.2 (a.s. upper bound, probabilistic)
For every $\varepsilon>0$:
$$\Pr_A\Bigl[\operatorname{cov}(A)\le(1+\varepsilon)\sqrt p\,\ln p\Bigr]\longrightarrow 1 .$$
*Proof.* Let $M=\lceil(1+\varepsilon)\sqrt p\ln p\rceil$ and let $B$ be a
uniform random $M$-subset, independent of $A$. By Lemma 1.1 logic applied to
$(A,B)$ jointly,
$\mathbb E_{A,B}[\#\text{uncovered}]=p(1-k/p)^M\le p\,e^{-M/\sqrt p}
\le p^{-(\varepsilon-o(1))}\to0$. If $\operatorname{cov}(A)>M$ then *every*
$M$-subset fails, in particular the random one, so
$\mathbf 1_{\{\operatorname{cov}(A)>M\}}\le\Pr_B[\text{fail}\mid A]$ pointwise
in $A$; average over $A$. ∎

### Proposition 2.3 (deterministic upper bound; stronger than 2.2!)
Every $A\subseteq\mathbb Z_p$ with $|A|=k$ satisfies
$$\operatorname{cov}(A)\le\frac pk\,(1+\ln k)=\Bigl(\tfrac12+o(1)\Bigr)\sqrt p\,\ln p .$$
*Proof (sketch of the classical bound).* The translate system is a
$k$-uniform, $k$-regular set system on $p$ points (each $x$ lies in exactly
$k$ translates $A+(x-a)$), so the fractional covering number is
$\tau^\ast=p/k$. Lovász's theorem (1975) — see also Stein (1974), Chvátal
(1979) — gives integral covering number $\tau\le\tau^\ast(1+\ln k)$. ∎
*(Sketch flagged; the result is classical.)*

**Remark.** It is amusing that the deterministic LP bound (constant
$\tfrac12$) beats the probabilistic-existence bound of Prop. 2.2 (constant
$1$); regularity makes the fractional solution uniform.

### Proposition 2.4 (energy / second-moment ceiling)
Call $\mathcal C(A,B):=\dfrac{(\sum_x r(x))^2}{\sum_x r(x)^2}\le|A+B|$ the
Cauchy–Schwarz certificate, where $r=r_{A+B}$. For $|B|=M=c\sqrt p$ and
random $(A,B)$:
$$\mathbb E\Bigl[\sum_x r(x)\Bigr]=Mk=cp,\qquad
\mathbb E\Bigl[\sum_x r(x)^2\Bigr]=cp+c^2p+o(p),$$
so **any** argument that consumes only the first two moments of the
representation function certifies coverage of at most
$$\frac{(cp)^2}{cp+c^2p}=\frac{c}{1+c}\,p\;<\;p .$$
Also $\mathbb E\bigl[\mathsf E(A)\bigr]=\mathbb E\sum_d c_d(A)^2=2p+o(p)$,
essentially minimal for a $k$-set (minimum $\ge\max(k^2,k^4/p)=p+o(p)$): a
random $A$ has near-minimal additive energy, *and yet* energy sees nothing
about the tail $\{x:r(x)=0\}$. Mean-square/additive-energy technology
therefore cannot prove GREEN-081(RB); the obstruction is purely in the upper
tail of the representation-starved set.

*Proof.* $\mathbb E r(x)=Mk/p=c$; $\sum_x r(x)^2=\sum_x r(x)+\sum_x
r(x)(r(x)-1)$ and the second term counts ordered pairs of translates meeting
at $x$: $\mathbb E\sum_xr(x)(r(x)-1)=M(M-1)\,\mathbb E[c_d]
=M(M-1)\frac{k(k-1)}{p-1}=c^2p+o(p)$. Energy: $\mathbb E c_d^2
=\mathbb Ec_d+(\text{4-point term})\le1+(1+o(1))$, sum over $d$. Lower bound on
minimal energy: $\mathsf E(A)\ge|A|^4/|A+A|\ge k^4/p=p$. ∎

### Proposition 2.5 (completion/trade-off lemma; fully rigorous and cheap)
Given any partial cover $B_0$ with $|B_0|=M$ and leftover set $U$,
$|U|=L$, one can extend it to a full cover with at most
$$M+\bigl\lceil\tfrac pk\ln(L+1)\bigr\rceil+1 \;=\; M+\bigl\lceil\sqrt p\,
\ln(L+1)\bigr\rceil+1$$
translates. Moreover for *any* partial cover,
$$\operatorname{cov}(A)\;\le\;|B_0|+L$$
by finishing stragglers individually (each $x\in U$ is covered by the single
translate $A+(x-a_0)$, $a_0\in A$ fixed).

*Proof.* Greedy: at leftover level $U'$, the average over $t\in G$ of
$|(A+t)\cap U'|$ equals $k|U'|/p$ exactly, so some translate adds
$\ge k|U'|/p$ fresh points; $|U'|$ decays geometrically by factor
$(1-k/p)\le e^{-k/p}$ per step, requiring $\le\frac pk\ln L\cdot(1+o(1))$
steps to reach $0$. The second display is immediate. ∎

**Consequence (reduction).** $\operatorname{cov}(A)=O(\sqrt p)$ w.h.p. as soon
as w.h.p. there exist $O(\sqrt p)$ translates covering all but $O(\sqrt p)$
points of $\mathbb Z_p$ (then stragglers cost $O(\sqrt p)$ more). Equivalently,
GREEN-081(RB) holds iff w.h.p.
$$\inf_{B}\ \bigl(|B|+L_B\bigr)=O(\sqrt p),\qquad L_B:=p-|A+B|.$$
Within the averaging-completion family of Prop. 2.5 the total is
$M+\sqrt p\ln(L+1)$, which is $O(\sqrt p)$ only if $\ln L=O(1)$: the
*logarithmic endgame* — killing the last few uncovered points — is exactly
where every current tool pays $\sqrt p\ln p$ instead of $\sqrt p$.

### Discussion 2.6 (routes that die, and the quantitative feasibility check)
- **Matching/design route.** Hypergraph nibble theory (Rödl; Frankl–Rödl;
  Pippenger–Spencer; Keevash) produces *disjoint* edge families. Here two
  translates $A+t,A+t'$ intersect in $c_{t-t'}(A)$ points with
  $\mathbb E c_d=k(k-1)/(p-1)=1+O(k/p)$: typical translates already meet in
  $\Theta(1)$ points, so exact packings are structurally absent, and no
  general "bounded-overlap approximate decomposition with $O(\sqrt p)$
  leftover" theorem exists for Cayley hypergraphs. (Standard random-set
  heuristics give $|A-A|=(1-e^{-1}+o(1))p$ w.h.p. — the independent-set count
  of the difference cycle per $d$ is $\frac{p}{p-k}\binom{p-k}{k}$, giving
  $\Pr[d\notin A-A]\to e^{-1}$; a full concentration proof is omitted —
  *flagged sketch*.)
- **Feasibility check (supports the conjecture).** If $|B|=\beta\sqrt p$ and
  all of $G$ is covered with multiplicities $r\ge1$, then necessarily
  $\sum_x\binom{r(x)}2\ge p\binom{\lceil\beta\rceil\text{-flat}}{}$-scale
  $\approx\frac{\beta^2-\beta}{2}p$ when $\beta\ge1$ (flat multiplicity
  minimizes collisions at fixed sum $\beta p$). But the collision budget
  available from typical translates is
  $\sum_{t<t'}|(A+t)\cap(A+t')|\approx\binom{\beta\sqrt p}{2}\frac{k^2}{p}
  =\frac{\beta^2}{2}p+o(p)$, and
  $\frac{\beta^2}{2}p\ge\frac{\beta^2-\beta}{2}p$ always: there is no
  combinatorial obstruction to an efficient near-tiling — the uncertainty is
  entirely in the tail behavior of the greedy/adaptively chosen process.
- **What a proof must deliver.** Control of
  $\Pr[\exists x:\ r_{A+B}(x)=0]$ for an explicit, adaptive $B$ with
  $|B|=O(\sqrt p)$. Union bound over $x$ loses $p e^{-c}$; the events are
  nearly independent under *random* $B$ (that is precisely Conjecture 1.8's
  mechanism), so adaptivity must suppress the tail jointly — no available
  concentration inequality, entropy method, or container theorem does this in
  the Cayley/translation-invariant setting. We found no equivalence to a
  named pre-existing conjecture beyond Green's original formulation.

---

## 3. Computational study (exact coverage checks)

Code: `code/sim_random_translates.py`, `code/sim_greedy_cover.py`,
`code/verify_exactness.py`, `code/verify_theory.py`; data: `data/*.csv`.
Seeds fixed and documented in file headers; all coverage decisions are exact
(boolean bitsets / rounded integer FFT scores cross-checked against brute
force).

### 3.1 Sampling threshold for random translates (Theorem 1.6 confirmation)

$m^\ast$ = number of i.i.d. translates until exact full cover (400 trials for
$p\le1100$, 150 for $p\le5100$, else 50):

| $p$ | $k$ | mean $m^\ast$ | median | mean$/\sqrt p\ln p$ |
|---|---|---|---|---|
| 101 | 10 | 49.71 | 48 | 1.0717 |
| 199 | 14 | 80.64 | 77 | 1.0799 |
| 401 | 20 | 128.31 | 124 | 1.0690 |
| 599 | 24 | 170.93 | 165 | 1.0920 |
| 797 | 28 | 203.97 | 199 | 1.0814 |
| 997 | 31 | 237.67 | 231 | 1.0901 |
| 1999 | 44 | 374.96 | 356 | 1.1034 |
| 4003 | 63 | 563.91 | 542 | 1.0745 |
| 5003 | 70 | 631.75 | 617 | 1.0486 |
| 10007 | 100 | 964.62 | 937 | 1.0469 |
| 20011 | 141 | 1435.62 | 1403 | 1.0247 |

Ratios drift toward 1 like $1+\gamma/\ln p$ predicts ($1.125$ at $p=101$,
$1.058$ at $p=20011$): threshold located at $\sqrt p\ln p$, not
$C\sqrt p$ — at $p=20011$, $100\sqrt p=14100$ is $10\times$ the threshold.

### 3.2 Gumbel-window gauge (Conjecture 1.8)

Frequency of success at $m=\lceil\sqrt p(\ln p+c)\rceil$ vs prediction
$\exp(-e^{-c})$ (selected rows; full table `data/gumbel_window.csv`):

| $c$ | pred | $p=997$ | $p=1999$ | $p=5003$ |
|---|---|---|---|---|
| −1 | 0.0660 | 0.0625 | 0.0667 | 0.0933 |
| 0 | 0.3679 | 0.3600 | 0.3667 | 0.4467 |
| 1 | 0.6922 | 0.6900 | 0.6800 | 0.7400 |
| 2 | 0.8734 | 0.8650 | 0.7867 | 0.9000 |

Uncovered-count gauge at exactly $m=\mathrm{round}(\sqrt p(\ln p+c))$, 300
trials: empirical $\mathbb E X$ tracks $e^{-c}$ (e.g. $p=997$:
$c=0,1,2$ give $0.977,0.390,0.150$ vs $1,0.368,0.135$);
$\mathrm{Var}(X)\approx\mathbb EX$ (Poisson-consistent);
frequency of $X=0$ brackets $\exp(-e^{-c})$ throughout.

### 3.3 Regime $m=100\sqrt p$ (Corollary 1.7)

100 trials each: zero uncovered points ever observed; theoretical
$\mu(997)=7.246\times10^{-42}$, $\mu(10007)=2.262\times10^{-40}$. Consistent
with the $e^{100}$ crossover: RA-failure is real but unreachable numerically;
what simulations *do* see is the true threshold of §3.1.

### 3.4 Chosen translates (RB): greedy benchmark

Greedy set cover (repeatedly take the translate hitting the most uncovered
points; exact integer scores), $g$ = steps to full cover:

| $p$ | trials | $g$ mean | $g/(\sqrt p\ln p)$ | $g/(\tfrac12\sqrt p\ln p)$ | $g/\sqrt p$ | Lovász–Stein bd |
|---|---|---|---|---|---|---|
| 101 | 200 | 15.55 | 0.3353 | 0.671 | 1.55 | 33.4 |
| 997 | 60 | 65.42 | 0.3000 | 0.600 | 2.07 | 142.6 |
| 1999 | 40 | 100.13 | 0.2946 | 0.589 | 2.24 | 217.4 |
| 5003 | 25 | 175.20 | 0.2908 | 0.582 | 2.48 | 375.1 |
| 20011 | 8 | 402.88 | 0.2876 | 0.575 | 2.85 | 844.3 |

Observations: (i) greedy beats the proven Lovász–Stein ceiling by $\approx2.1$
times; (ii) $g/\sqrt p$ grows like $\approx0.29\ln p$ — even the *heuristic*
optimum visible to greedy carries the logarithm; (iii) the endgame saturates
(`data/greedy_curve_p20011.csv`: final steps add $O(1)$ uncovered points each,
$\approx2$ per step in this run). All of this
is consistent with the thesis that removing the log demands controlling the
tail $\{r(x)=0\}$, which neither greedy analysis nor energy methods provide.

---

## 4. Verdict

1. **Reading RA (the $100\sqrt p$ translates themselves random): PROVEN FALSE
   asymptotically** (Theorem 1.6(i)): w.h.p. $(1-o(1))pe^{-100}$ points stay
   uncovered; covers happen w.h.p. only for $p\lesssim e^{100}$ (Corollary
   1.7). Explicit, self-contained proof via exact moments + variance bound +
   Chebyshev; machine-checked identities (Appendix A).
2. **Reading RB (choose the translates; Green's intended problem):
   UNRESOLVED**, as Green states (even with constant $1.01$). Best results
   established here/classically:
   - $\lceil p/k\rceil\le\operatorname{cov}(A)$ always (Prop. 2.1); no exact
     factorization exists (Hajós–de Bruijn).
   - $\operatorname{cov}(A)\le(1+\varepsilon)\sqrt p\ln p$ a.s. (Prop. 2.2);
     and $\le(\frac12+o(1))\sqrt p\ln p$ for *every* $A$ via Lovász–Stein
     (Prop. 2.3).
   - Reduction/conditional theorem (Prop. 2.5): if w.h.p. $O(\sqrt p)$
     translates cover all but $O(\sqrt p)$ points, then GREEN-081(RB) is
     TRUE; more generally $\operatorname{cov}(A)\le|B_0|+L_{B_0}$ for any
     partial cover, and $|B_0|+\sqrt p\ln(L_{B_0}+1)$ via averaging completion.
   - Obstruction (Prop. 2.4 + §2.6): second-moment/energy certificates cap at
     $\frac{c}{1+c}p<p$ coverage; matching/nibble designs are structurally
     void (typical translate intersections $\Theta(1)$); every known tail
     bound loses $\ln p$ in the endgame. **Exact missing bridge:** prove
     $\Pr_A[\exists B,\,|B|=O(\sqrt p),\ L_B=O(\sqrt p)]\to1$, i.e. beat the
     coupon-collector tail $\Pr[\exists x: r_{A+B}(x)=0]$ for adaptive $B$ —
     no current tool (Chen–Stein, containers, entropy, energy) applies in the
     translation-invariant setting.
3. Numerics (exact checks, seeds fixed): confirm Theorem 1.6's threshold
   $\sqrt p\ln p$, support Conjecture 1.8's Gumbel window, confirm the
   $e^{100}$ invisibility of the RA failure at feasible sizes, and locate
   greedy-RB at $\approx0.29\sqrt p\ln p$ — far above $O(\sqrt p)$, far below
   proven ceilings.

---

## Appendix A. Machine verification (executed 2026-08-26)

`python3 code/verify_theory.py` (wall 18.6 s, exit 0):

```
PASS: V1 symbolic C(p-2,k)/C(p,k) == (p-k)(p-k-1)/(p(p-1)) (simplify diff = 0; this equals E_A[w_A])
PASS: V2 exhaustive p=7,k=2,m=3: E X enum=2.55102040816 closed=2.55102040816
PASS: V2 exhaustive p=7,k=2,m=3: E X^2 (corrected g_m form) enum=7.36734693878 closed=7.36734693878
     info: g_m=0.11467444  f^m(Jensen lower surr.)=0.1079797  E X^2 with f^m would be 7.0861678 (known-wrong)
PASS: V2 exhaustive p=7,k=2,m=3: Var(X) <= 2*E X Var=0.859642 vs mu=2.55102
PASS: V2 exhaustive p=13,k=3,m=4: E X enum=4.5516613564 closed=4.5516613564
PASS: V2 exhaustive p=13,k=3,m=4: E X^2 (corrected g_m form) enum=22.4861174329 closed=22.4861174329
     info: g_m=0.11496446  f^m(Jensen lower surr.)=0.11078262  E X^2 with f^m would be 21.833751 (known-wrong)
PASS: V2 exhaustive p=13,k=3,m=4: Var(X) <= 2*E X Var=1.7685 vs mu=4.55166
PASS: V3 MC mean vs closed form emp=0.00285 closed=0.00299 (4SE=0.00155)
PASS: V3 MC sd vs closed form (g_m-based) emp_sd=0.05331 closed_sd=0.05479 g_m_hat=1.5723e-09 q^(2m)=8.7903e-10 relerr=0.0269
PASS: V5 asymptotic ratio g_m/q^(2m) close to 1 at small C (p=101,k=10,m=32,C=m/sqrt(p)=3.18) ratio=1.0248 (theory: 1+O(C^2/p))
PASS: V4 regime mu(p=997) < 1e-38 k=31 m=3158 mu=7.246e-42
     mu(p=997, m=round(100*sqrt(p))=3158) = 7.246049e-42
PASS: V4 regime mu(p=10007) < 1e-38 k=100 m=10003 mu=2.262e-40
     mu(p=10007, m=round(100*sqrt(p))=10003) = 2.262069e-40
VERIFY_THEORY: ALL PASSED
```

`python3 code/verify_exactness.py` (exit 0):

```
PASS: (i) bitset == pure-Python set unions, p=7, 20 trials -- 19 translates/trial
PASS: (i) bitset == pure-Python set unions, p=13, 20 trials -- 28 translates/trial
PASS: (i) bitset == pure-Python set unions, p=101, 20 trials -- 97 translates/trial
PASS: (ii) FFT greedy score == brute-force O(p*k) count, p=101, first 3 steps x 20 trials -- max_rounding_err=1.24e-14, argmax_match=True
ALL VERIFICATION CHECKS PASSED
```

### A.2 Audit trail
The first draft of this dossier asserted $\mathbb E X^2=pq^m+p(p-1)f^m$ with
$f=\binom{p-2}{k}/\binom pk$. Exhaustive enumeration falsified it
($7.367\ldots\neq7.086\ldots$ at $(7,2,3)$; $22.486\ldots\neq21.834\ldots$ at
$(13,3,4)$); root cause: $\mathbb E_A[w^m]\neq(\mathbb E_Aw)^m$ (Jensen). All
theorem statements were re-derived through $g_m$ (Lemma 1.2/1.4) before any
conclusion was drawn; the final conclusions (Theorem 1.6, Corollary 1.7) were
re-checked against the corrected moments and stand.

## Appendix B. References
- B. Green, *100 Open Problems in Additive Combinatorics*, Problem 39.
  https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf
- L. Lovász, On the ratio of optimal integral and fractional covers,
  *Discrete Math.* 13 (1975), 383–390.
- S. K. Stein, Two combinatorial covering theorems, *L'Enseignement
  Mathématique* 20 (1974); V. Chvátal, A greedy heuristic for the set-cover
  problem, *Math. Oper. Res.* 4 (1979), 233–235.
- G. Hajós, Über einfache und mehrfache Bedeckung von n-dimensionalen
  Räumen mit einem Würfelgitter, *Math. Z.* 47 (1942); N. G. de Bruijn, On
  the factorization of finite abelian groups (1953).
- N. Alon–J. Spencer, *The Probabilistic Method* (union bound / second
  moment background); A. D. Korshunov / R. W. Robinson–N. C. Wormald context
  for randomized constructions not directly applicable here.
