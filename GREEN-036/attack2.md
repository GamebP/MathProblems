# GREEN-036 Attack Iteration 2

Brief: `next.md` (formula-first; falsify-before-prove; strongest new rigorous
theorem or an honest Remaining Gap). Status labels: [PROVEN], [HEURISTIC],
[COMPUTED] (= FINITE EVIDENCE). Companion checks: `attack2_verify.py`,
output captured in `data/attack2_output.txt`.

---

## Current target

A quantitative recurrence iterable for all $N$, of the shape
$\F(cN)\ \ge\ \Phi(\F(N),N)$ or $\;N-\F(N)\ \ge\ H(N)$,
whose repeated application decides $\liminf_{N\to\infty}\F(N)/N>0$ or
$\F(N)=o(N)$.

## Best new idea

Split each doubling scale into two *disjoint-window affine images*
$W_2=\{2a-1:\ N/2<a\le N\}$ and $W_3=\{3a-1:\ N/3<a\le 2N/3\}$, both confined
to $(N,2N]$. Their overlap is lcm-controlled ($6\mid x{+}1$), their overlap
with the old prefix $A\cap[1,N]$ is at most the single point $N$, and the
per-map contribution is measured by *differences* $F(N)-F(N/2)$ rather than
absolute densities — this extracts the maximal rigorous mileage before the
L1 overlap collapse of iteration 1 bites.

## Formal progress

### T1 [PROVEN] — Holes in every reduced arithmetic progression

**Theorem.** Let $M\ge1$ and $r\ge0$ with $\gcd(r+1,M)=1$. Then there are
infinitely many $n\equiv r \pmod M$ with $n\notin\A$. The set of such holes
below $X$ is $\Omega_M(X/\log X)$.

*Proof.* By Dirichlet's theorem (primes in the arithmetic progression
$1 \bmod 3M$; note $\gcd(1,3M)=1$) fix a prime
$p\equiv1\pmod{3M}$; then $p\notin\A$ by Lemma A ($p\equiv1\bmod3$) and
$p\equiv1\pmod M$. Since $\gcd(r+1,M)=1$, Dirichlet applied to the class
$r+1 \bmod M$ yields infinitely many primes $q\equiv r+1\pmod M$
(discard $q=p$; finitely many). Set $n=pq-1$. Then
$pq\equiv p(r+1)\equiv r+1\pmod M$, so $n\equiv r\pmod M$;
$n+1=pq$ is a semiprime whose only factor pairs are $(p,q),(q,p)$, and
$p\notin\A$; by the exact characterization $n\notin\A$. Distinct $q$ give
distinct $n$. The counting statement is the classical prime-density-in-AP
bound applied to $q\le X/p$. $\square$

**Consequence [PROVEN].** $\A$ contains no infinite arithmetic progression:
the "eventual containment in a residue class" route to positive lower density
is dead in full generality for reduced classes. Together with Lemma A (the
entire class $1 \bmod 3$ is holes) the complement picture is:
*thick at class level, provably present in every reduced class, thin or not
within allowed classes — unknown.*

### T2 [PROVEN, density-vacuous] — the 4q construction and why it is empty

**Proposition.** For every prime $q\equiv5\pmod6$, $\;4q-1\notin\A$.

*Proof.* Divisor pairs of $4q$: $(2,2q),(4,q),(q,4),(2q,2)$. Now
$4\notin\A$ (since $5$ is prime), blocking $(4,q),(q,4)$; and
$q\equiv2\pmod3$ gives $2q\equiv4\equiv1\pmod3$, hence $2q\notin\A$ by
Lemma A, blocking $(2,2q),(2q,2)$. All four pairs blocked. $\square$

**Why it matters despite proving nothing new:** every $n=4q-1$ satisfies
$n\equiv1\pmod3$, i.e. these holes were *already* excluded by Lemma A.
COMPUTED: zero members among all $4q-1$ ($q<5000$, $q\equiv5 \bmod 6$).
The construction demonstrates the blocking technique and simultaneously its
ceiling: forcing a factor-side into the excluded class drags the shifted
number itself into that class. Every elementary variant tried
($9q$ with $q\equiv1\bmod3$: refuted by $116=9\cdot13-1\in\A$, rescued by the
pair $(3,39)$, $39=5\cdot8-1$; higher $2^aq$ shapes: refuted structurally)
either lands in class $1\bmod3$ or gets rescued by alternative factorizations.
This asymmetry — holes are easy to construct in the dead class, hard in the
live classes — *is* the open problem, made concrete.

### T3 [PROVEN] — the doubling recurrence, solved; it contracts

**Theorem.** For all $N\ge3$, with $\delta_N:=\F(N)/N$ where defined,
$$\F(2N)\;\ge\;\F(N)+\bigl[\F(N)-\F(\lfloor N/2\rfloor)\bigr]
+\bigl[\F(\lfloor 2N/3\rfloor)-\F(\lfloor N/3\rfloor)\bigr]
-\Bigl(\Bigl\lfloor\tfrac{2N}{6}\Bigr\rfloor-\Bigl\lfloor\tfrac N6\Bigr\rfloor\Bigr)-2 .$$

*Proof.* Define $W=\{2a-1:\ a\in\A,\ \lfloor N/2\rfloor<a\le N\}$ and
$V=\{3a-1:\ a\in\A,\ \lfloor N/3\rfloor<a\le\lfloor2N/3\rfloor\}$. Both lie in
$(N,\,2N]$ (minima $2(\lfloor N/2\rfloor{+}1)-1\ge N$ resp.
$3(\lfloor N/3\rfloor{+}1)-1\ge N$), hence meet $S_0:=\A\cap[1,N]$ in at most
the single point $\{N\}$ each. $|W|=\F(N)-\F(\lfloor N/2\rfloor)$ and
$|V|=\F(\lfloor2N/3\rfloor)-\F(\lfloor N/3\rfloor)$ by injectivity of the two
maps. Elements of $W\cap V$ satisfy $6\mid x+1$ with $x+1\in(N,2N]$; there are
at most $\lfloor2N/6\rfloor-\lfloor N/6\rfloor$ such multiples. Bonferroni on
$W\cup V$ and adjoining $S_0$ gives the claim. $\square$

**Corollary (relative form; induction hypothesis $\F(m)\ge\delta m$ for all
$m\le N$).** Using $\F(N)-\F(\lfloor N/2\rfloor)\ge\delta N/2$,
$\F(\lfloor2N/3\rfloor)\ge\delta(2N/3-1)$, and the trivial cap
$\F(\lfloor N/3\rfloor)\le N/3$:
$$\frac{\F(2N)}{2N}\;\ge\;\frac{13}{12}\,\delta\;-\;\frac18\;-\;O\!\Bigl(\tfrac1N\Bigr).$$

**Solution of the recurrence.** The map $\delta\mapsto\tfrac{13}{12}\delta-\tfrac18$
has slope $13/12>1$ and fixed point $-3/2<0$: iterated from any admissible
$\delta_0\le2/3$ it reaches $0$ after boundedly many doublings (from
$\delta_0=0.55$: about ten). The recurrence is therefore *valid but
non-bootstrapping*: the linear overlap penalty $N/6$ per doubling compounds
geometrically against a sub-linear proven seed ($O((\log N)^2)$, Lemma B).
This is L1's cubic overlap collapse appearing at minimal scale, now fully
explicit. COMPUTED: inequality holds with positive margin at every tested
scale (margins $+262$ at $N=10^3$ up to $+261{,}658$ at $N=1.5\cdot10^6$;
relative form satisfied at $N=10^5,10^6$).

### Rescue certificates [COMPUTED]

$116=9\cdot13-1\in\A$: the pair $(9,13)$ is blocked ($13\equiv1\bmod3$), but
$(3,39)$ rescues it ($3\in\A$, $39=5\cdot8-1\in\A$ since $40=5\cdot8$).
Likewise $512\in\A$ (iteration 1, depth-5 chain). Meanwhile the naive
three-prime blocking claim "$p,q\equiv1\bmod3\Rightarrow pqs-1\notin\A$" was
**refuted during this iteration** by $364=7\cdot13\cdot4=14\cdot26$ with
$14,26\in\A$: alternative factorizations defeat local blocking. Recorded as
required by the brief's falsification discipline.

## Proof audit (per brief)

1. T1 constants: $p$ exists once and for all (finite prime), $q$ ranges over
   an infinite Dirichlet set; no uniformity-in-$M$ claimed beyond existence.
   Edge case $M=1$: $\gcd(r+1,1)=1$ always, statement trivial-true.
   Edge case $r=M-1$: excluded automatically since $\gcd(r+1,M)=M>1$ for $M>1$.
2. T3 boundary cases: windows use strict lower cuts, so $W,V\subseteq(N,2N]$
   and the $S_0$-overlap is $\le\mathbf 1$ per window, not $O(1)$-sloppy; all
   floors kept explicit; induction hypothesis applied only at arguments
   $\le N$.
3. Quantifier check in the corollary: $\delta$ is a *hypothesis*
   ($\forall m\le N$), the conclusion at $2N$ is weaker for every
   $\delta\in(0,2/3]$; no asymptotic transition is hidden.
4. Counterexamples constructed against own claims: three (364-block failure;
   $4q$ vacuity; initial false belief $40\in\A$ — corrected: $41$ prime
   $\Rightarrow40\notin\A$). All three changed the final text.
5. External theorems used: Dirichlet's theorem on primes in AP (T1, standard
   hypotheses: class coprime to modulus — verified in-line); no other.

## Remaining Gap

Exactly as in iteration 1, now with sharper edges:

> No method is known to lower-bound $\#\{n\le X:\ n+1$ has a divisor pair in
> $\A\times\A\}$ beyond $O((\log X)^2)$; positive density needs $\ge cX$.

New information gained: the doubling recurrence shows the gap is not a
constant-factor issue — affine images intrinsically pay lcm-overlaps that
compound to contraction; any successful argument must either beat pairwise
overlap accounting globally (shared-preimage exploitation) or construct
allowed-class membership by a mechanism other than image counting. Hole
constructions in the live classes $\{0,2\}\bmod3$ resist all elementary
blocking patterns (rescue phenomenon), which is consistent with the rising
conditional densities observed in the census and explains why zero-density is
also unproved.

## Resolution status

STILL OPEN
