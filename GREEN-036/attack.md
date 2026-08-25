# GREEN-036 Attack Iteration 1

Brief: `next.md`. Objective: resolution mechanism for
$d(A)=\lim_{N\to\infty}F(N)/N$, $F(N)=|A\cap[1,N]|$, not more partial results.
Everything below marked FINITE EVIDENCE comes from `attack_verify.py`
(reproducible, stdlib-only) and carries no asymptotic weight.

---

## Current target

Bootstrap theorem of the form

$$F(N)\ \ge\ \delta N \quad\Longrightarrow\quad F(CN)\ \ge\ \Phi(\delta)\,CN,
\qquad \Phi(\delta)>\delta .$$

Repeated application would force positive lower density from any seed scale;
combined with Lemma A ($\bar d(A)\le 2/3$) this is the natural route to
$d(A)>0$. This iteration determines **whether such a bootstrap can exist in
one step** (answer: provably not, see Formal progress L2) and identifies the
exact junction where every multi-step route currently stalls.

## Best new idea

**Prime rigidity + the OR-mechanism.** Membership in $A$ is governed by an
*existential* divisor-pair condition, $n\in A \iff n+1$ has *some* divisor
pair in $A\times A$, which makes membership monotone in the factorization
richness of $n+1$. Two exact consequences proved below:

1. *(Rigidity)* For distinct primes $p,q$: $\;pq-1\in A \iff p\in A$ and
   $q\in A$. Non-membership propagates through the prime graph
   ($11\notin A$ forces $\{11q-1\}\notin A$), but only along
   $O(N/\log N)$-thin families — complements generated this way cannot
   obstruct positive density.
2. *(Deep certificates)* Membership can be witnessed by arbitrarily deep
   recursively-linked chains. FINITE EVIDENCE: $2^9=512\in A$ because
   $513=3\cdot 171$, $171\in A$ because $172=2\cdot 86$, $86\in A$ because
   $87=3\cdot 29$, $29\in A$ because $30=2\cdot 15$, $15\in A$ because
   $16=2\cdot 8$, $8\in A$ because $9=3\cdot 3$. No bounded-depth local
   criterion captures $A$; this is why the mean-field model failed and why
   single-scale arguments cannot work.

## Formal progress

### L1 (Image counting cap; deterministic Bonferroni)

For $b\ge2$ let $T_b(x)=bx-1$. Then:

**(a)** $|T_b(A)\cap[1,N]| = F(\lfloor (N+1)/b\rfloor)$ exactly.

*Proof.* $T_b$ is injective and $T_b(a)\le N \iff a\le (N+1)/b$. $\square$

**(b)** For $b_1\ne b_2$:
$|(T_{b_1}A)\cap(T_{b_2}A)\cap[1,N]| \le \lfloor (N+1)/\operatorname{lcm}(b_1,b_2)\rfloor$.

*Proof.* $x$ in the intersection satisfies $x+1=b_1a_1=b_2a_2\le N+1$, so
$\operatorname{lcm}(b_1,b_2)\mid x+1$; multiples of $L$ in $[1,N+1]$ number
$\lfloor(N+1)/L\rfloor$. $\square$

**(c)** Consequently, for any finite $B\subseteq A$,
$$\Bigl|\bigcup_{b\in B}\bigl(T_b(A\cap[1,N])\bigr)\cap[1,N]\Bigr|
\;\ge\; \sum_{b\in B} F\!\Bigl(\frac{N+1}{b}\Bigr)\;-\;\sum_{\{b_1,b_2\}\subseteq B}
\frac{N+1}{\operatorname{lcm}(b_1,b_2)} .$$

**(d) Overlap load.** Let $S(B)=\sum_{2\le b_1<b_2\le B}\gcd(b_1,b_2)/(b_1b_2)$.
Using $\gcd(m,n)=\sum_{d\mid\gcd(m,n)}\varphi(d)$,

$$\sum_{m,n\le B}\frac{\gcd(m,n)}{mn}=\sum_{d\le B}\frac{\varphi(d)}{d^2}\,
H_{\lfloor B/d\rfloor}^2,\qquad
\sum_{d\le B}\frac{\varphi(d)}{d^2}=\frac{6}{\pi^2}\log B+O(1),$$

so $S(B)=\dfrac{1}{\pi^2}(\log B)^3+O((\log B)^2)$.

**Consequence (cap).** Even under the optimistic ansatz $F(M)\approx\delta M$,
the inclusion–exclusion lower bound collapses to triviality once
$(\log B)^3/\pi^2 \gtrsim \delta\,\log B$, i.e. $B\gtrsim e^{\pi\sqrt{\delta}}$
(up to constants). Images of a dense low-scale region therefore cannot by
themselves certify density growth: pairwise overlaps among affine images are
cubic in log-scale while the mass is only linear. Any working bootstrap must
exploit the OR-mechanism across many scales simultaneously.

FINITE EVIDENCE (X = 2·10⁶): $|(2A{-}1)\cap(3A{-}1)\cap[1,X]|=324{,}421\le333{,}333$;
$|(3A{-}1)\cap(5A{-}1)|=132{,}814\le133{,}333$ — the bound (b) is nearly tight
(99.6%), confirming overlaps are structural, not accidental.

### L2 (Multiplication-table obstruction; one-step bootstrap impossible)

**Theorem (Erdős 1960; quantified by Ford, Annals 2008).** With
$M(N)=|\{ab:\ 1\le a,b\le N\}|$ (distinct products),
$$M(N)\asymp \frac{N^2}{(\log N)^{\delta_F}}(\log\log N)^{3/2},
\qquad \delta_F=1-\frac{1+\log\log 2}{\log 2}\approx 0.08607 .$$

*Hypothesis check.* Ford counts distinct products over the full square
$[1,N]^2$; replacing it by $S\times S$ with $S\subseteq[2,N]$ can only shrink
the set, and shifting products down by 1 is a bijection on values. Both
operations preserve the $\asymp$-upper-bound direction used here. $\square$

**Corollary (obstruction).** For every $S\subseteq[2,N]$:
$$|\{ab-1:\ a,b\in S\}\cap[1,N^2]|\;\le\;M(N)\;=\;o(N^2).$$
Hence *one* closure step applied to an arbitrary dense seed produces a set of
relative density $o(1)$ at height $N^2$: there is **no** one-jump implication
$F(N)\ge\delta N \Rightarrow F(N^2)\ge \Phi'(\delta)N^2$ obtainable from the
closure rule alone. Elements at height $N^2$ must be built through
$\sim\log N$ intermediate scales; a bootstrap argument must control error
accumulation across all of them, or exploit the OR-mechanism rather than
product coverage. This kills the naive form of routes 3 and 6.

### L3 (Complement propagation along primes)

**Lemma.** If $p\notin A$ is prime, then $pq-1\notin A$ for every prime $q$.

*Proof.* Suppose $pq-1\in A$ with $pq\ge 5$. By the exact characterization,
$ pq = ab$ with $a,b\in A$, $a,b\ge2$. The only factorizations of the
semiprime $pq$ into two factors $\ge2$ are $(p,q)$ and $(q,p)$, so
$p\in A$ — contradiction. $\square$

**Anchor.** $11\notin A$: $12=2\cdot6=3\cdot4$, and $4\notin A$ (5 prime),
$6\notin A$ (7 prime). FINITE EVIDENCE: all $9{,}592$ numbers
$\{11q-1: q\le10^5 \text{ prime}\}$ are outside $A$.

**Density remark.** All hole families produced this way (over any fixed set
of anchors) have counting function $O(N/\log N)$: they have asymptotic
density $0$ and therefore do **not** obstruct $d(A)>0$. Route 2 yields
rigidity structure, not a zero-density mechanism.

### L4 (Divisor-pair rigidity; the 2-chain test)

**Lemma.** For $m\ge2$: $\;2m-1\in A$ iff $m\in A$ or there is a divisor
pair $(a,b)$ of $2m$ with $a,b\in A$ and $\{a,b\}\ne\{2,m\}$.

*Proof.* $2m-1\in A\iff 2m$ has a divisor pair in $A\times A$ (exact
characterization); the pairs of $2m$ are $(2,m),(m,2)$ plus
$(d,\,2m/d)$ over further divisors. $\square$

**Corollary (prime rigidity).** If $p\ge5$ is prime, the only factor pairs of
$2p$ and $qp$ (q prime) involve $p$ itself; hence
$p\in A \iff 2p-1\in A \iff qp-1\in A$ for each prime $q\ne p$.

### L5 (Powers of two: computed structure, FINITE EVIDENCE)

Exact membership test (well-founded recursion on divisor pairs, memoized;
prunes Lemma-A residues) gives, for $k\le40$:
$$2^k\in A \iff k\in\{1,3,9,15,17,21,23,25,27,29,33,35,39\}.$$

Notes: no even $k>0$ works (for even $k$, every prime $r\equiv1\pmod3$
dividing $2^k+1$ — e.g. Fermat-type factors — blocks recursively);
for odd $k$, $3\mid 2^k+1$ and membership cascades through
$(2^k+1)/3$ with unbounded certificate depth ($k=9$ needs depth $\ge5$,
see Best new idea). An earlier hand analysis claiming "$k\in\{1,3\}$ only"
was **falsified** by this computation — recorded as a caution against
shallow local reasoning about $A$.

## Critical gap

The single statement whose absence blocks everything:

> **GAP.** No method is known to lower-bound the count of $n\le X$ for which
> $n+1$ possesses a divisor pair in $A\times A$, beyond the
> $O((\log X)^2)$ families of Lemma B. Positive density needs
> $\ge cX$ such $n$.

Equivalently: the deep-certificate mechanism (Best new idea #2) demonstrably
operates ($2^9$, and the rising conditional densities inside the allowed
classes — 0.803 at $10^6$, FINITE EVIDENCE from the dossier), but nothing
quantifies how many integers it rescues. Routes 1/3/6 stall exactly at L1's
overlap collapse and L2's $o(N^2)$ cap; route 2 gives only thin complements;
route 7 found no new obstructions to quantify (none exist mod $m\le500$).

## Counterexample search

* Tested the proposed one-step bootstrap against L2: fails unconditionally
  (multiplication-table sparsity) — survived as an obstruction, not a theorem
  for positive density.
* Tested "shallow membership criteria": falsified by $2^9\in A$
  (certificate depth 5) — no bounded-depth rule captures $A$.
* Tested the L1 intersection bound empirically at four pairs $(b_1,b_2)$:
  never violated; near-tight for $(3,5)$ (99.6% of the lcm ceiling).
* Tested anchor-hole propagation: $11\notin A$ and $9{,}592/9{,}592$ holes
  confirmed; family is density-$0$, so it survives as structure but does not
  decide the density question.

## Next mathematical direction

Quantify **certificate depth**: define the derivation-depth function
$\depth(n)$ (minimal generation-tree height of $n\in A$). The computed
pattern suggests membership of structured sequences (odd powers of two)
reduces to long $3$-chains $m \mapsto (m\cdot 3^{j}+c)/2^{e}$-style cascades.
Two concrete questions, either of which would constitute real progress:

1. Prove that for every odd $k$, $2^k\in A$ depends only on the residue
   behaviour of finitely many recursively-defined cofactors
   $(2^k+1)/3^{\,v_3(2^k+1)}\cdots$ — or exhibit $k$ where the cascade is
   provably infinite (which would produce new infinite hole families).
2. Show that the union of affine images $T_a(A\cap[1,Y])$ over
   $a\in A\cap[Y,CY]$ covers $\gg Y^{2}/\operatorname{polylog}$ *distinct new*
   elements despite the L1 overlaps — i.e. beat the cubic overlap load by
   exploiting that overlapping images share their preimages (common multiples
   of small lcm are themselves heavily in $A$).

## Resolution status

STILL OPEN
