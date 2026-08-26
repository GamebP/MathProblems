# GREEN-081 "Covering by Random Translates" — Final Report

**Date:** 2026-08-26 · **Analyst:** ox-alpha (@orchestrator), with delegated
computation (@coder) and independent review (@reviewer). All mathematics in
`derivation.md`; machine checks in `code/verify_theory.py`,
`code/verify_exactness.py`; raw data in `data/`.

---

## 1. The problem, split honestly into two questions

> If $A \subset \mathbb{Z}/p\mathbb{Z}$ is random with $|A|=\sqrt p$, can we
> almost surely cover $\mathbb{Z}/p\mathbb{Z}$ with $100\sqrt p$ translates of
> $A$?

The phrase has two readings. Under **RA** the translates are themselves random;
under **RB** we choose them after seeing $A$ (covering number
$\operatorname{cov}(A)$). Green's remark that he cannot do it even with
constant $1.01$ shows **RB is the intended open problem**. We resolve RA
completely — it is false asymptotically, with an elementary proof — and map RB
precisely: what is provable today, what breaks, and the exact missing bridge.

## 2. Verdicts

### 2.1 Reading RA: **PROVEN FALSE (asymptotically)**

Let $k=\lfloor\sqrt p\rfloor$, $t_1,\dots,t_m$ i.i.d. uniform, $X$ = number of
uncovered points. Exact moments:

$$\mathbb EX=pq^m,\qquad
\mathbb EX^2=pq^m+p(p-1)\,g_m,\qquad
g_m:=\mathbb E_A\!\Bigl(1-\frac{2k-c_d(A)}{p}\Bigr)^{\!m}=q^{2m}\Bigl(1+O_{C}\tfrac1p\Bigr)$$

with $q=1-k/p$, $c_d(A)=|A\cap(A+d)|$, valid for $m\le C\sqrt p$. Hence

$$\operatorname{Var}(X)\le \mu+K(C)\,\frac{\mu^2}{p},\qquad \mu:=pq^m ,$$

so whenever $\mu\to\infty$: $\;X/\mu\to1$ in $L^2$ and
$\Pr[X=0]\le\operatorname{Var}/\mu^2\to0$. For $m=100\lfloor\sqrt p\rfloor$:
$\mu=pe^{-100}(1+o(1))\to\infty$, therefore

$$\boxed{\text{random }100\sqrt p\text{ translates leave }(1-o(1))\,pe^{-100}\text{ points uncovered w.h.p.}}$$

Conversely $\Pr[\text{cover}]\to1$ once $m\ge\sqrt p(\ln p+\omega(1))$
(Markov). So the true threshold for *random* translates is
$m^\ast=\sqrt p\ln p(1+o(1))$ — outside the critical window governed by
Conjecture 1.8: **no fixed constant works as $p\to\infty$.**
The crossover is at $p\approx e^{100}\approx2.69\times10^{43}$ — for every
prime a computer will ever touch, $100\sqrt p$ random covers succeed with
failure probability $<10^{-38}$ ($\mu(997)=7.246\times10^{-42}$,
$\mu(10007)=2.262\times10^{-40}$, machine-checked).

An instructive audit point: our first draft asserted
$\mathbb EX^2=pq^m+p(p-1)f^m$ with $f=\binom{p-2}{k}/\binom pk$; exhaustive
enumeration falsified it (Jensen gap $\mathbb E_A[w^m]>(\mathbb E_Aw)^m$),
the identity was re-derived through $g_m$, and all conclusions re-checked.
This correction is recorded in `derivation.md` Appendix A.2.

### 2.2 Reading RB (Green's actual question): **UNRESOLVED**

Established here:

$$\Bigl\lceil\tfrac pk\Bigr\rceil\;\le\;\operatorname{cov}(A)\;\le\;
\underbrace{\Bigl(\tfrac12+o(1)\Bigr)\sqrt p\ln p}_{\text{every }A\text{ (Lovász–Stein)}}\qquad
\text{and}\qquad \operatorname{cov}(A)\le(1+\varepsilon)\sqrt p\ln p\ \text{a.s.}$$

plus the reduction theorem: if w.h.p. $O(\sqrt p)$ chosen translates cover all
but $O(\sqrt p)$ points then $\operatorname{cov}(A)=O(\sqrt p)$ w.h.p.
(stragglers finish one translate each); more generally
$\operatorname{cov}(A)\le|B_0|+\lceil\sqrt p\ln(L_{B_0}+1)\rceil+1$ for any
partial cover.

**Exact obstruction.** With $r=r_{A+B}$, Cauchy–Schwarz certification using
only $\sum r$, $\sum r^2$ caps coverage at $\frac{c}{1+c}p<p$ for
$|B|=c\sqrt p$ — mean-square/additive-energy methods *cannot* reach full
coverage (and $\mathbb E[\mathsf E(A)]\approx2p$ is near-minimal yet tail-blind).
Matching/nibble design theory is structurally void here because typical
translates intersect in $\Theta(1)$ points
($\mathbb E c_d=k(k-1)/(p-1)\to1$). Every completion argument available pays
$\sqrt p\ln L$ on the leftover (coupon-collector endgame). **Missing bridge,
stated once:** prove
$$\Pr_A\bigl[\exists B:\ |B|=O(\sqrt p),\ L_B=O(\sqrt p)\bigr]\xrightarrow[p\to\infty]{}1,$$
i.e. beat the tail $\Pr[\exists x: r_{A+B}(x)=0]$ adaptively. No current tool
(second moment, Janson, Chen–Stein — dependency graph complete — entropy,
containers, LP-rounding) does this in a translation-invariant setting, and we
found no reduction of the statement to any other named conjecture.

**Numerical placement of RB** (exact greedy benchmark): $g\approx
0.288\sqrt p\ln p$ at $p=20011$ — below the proven $(1/2)\sqrt p\ln p$
ceiling by $2.1\times$, but still carrying the logarithm; consistent with the
thesis that the log dies only via unproven adaptive tail control.

## 3. Evidence summary

| Item | Result |
|---|---|
| Theory verifier (`verify_theory.py`, exit 0) | 14/14 PASS: symbolic identity, exact-Fraction enumeration at $(7,2,3)$ & $(13,3,4)$, MC at $(101,10,100)$ within $4$SE / sd relerr $0.027$, ratio test $1.0248$, regime $\mu$ magnitudes |
| Mechanics verifier (`verify_exactness.py`, exit 0) | bitset coverage ≡ pure-Python set unions ($p=7,13,101$); FFT greedy scores ≡ brute force, max rounding err $1.24\times10^{-14}$ |
| Threshold sim (11 primes, ≤400 trials) | $m^\ast/(\sqrt p\ln p)=1.02$–$1.10$, drifting to 1 like $1+\gamma/\ln p$ |
| Gumbel window sim | success freq at $c=0$ → $0.36$ vs $\exp(-e^{0})=0.3679$; $\mathbb EX\to e^{-c}$; Var ≈ mean |
| Regime $100\sqrt p$ | 200/200 perfect covers, max uncovered $=0$, matching $\mu<10^{-40}$ |
| Greedy sim | table §3.4 of `derivation.md`; endgame adds $O(1)$ points per step ($\approx2$ in this run) |

## 4. Answer to GREEN-081, in one paragraph

As literally stated with *random* translates, the assertion is **false for
large $p$** (though true with overwhelming probability for every
$p\lesssim e^{100}$): the correct constant must grow like $\ln p$, threshold
$100\to\sqrt p\ln p/\sqrt p$. As intended by Green — chosen translates, i.e.
$\operatorname{cov}(A)=O(\sqrt p)$ almost surely — the problem is **open**;
we contribute sharp partial results
($\lceil p/k\rceil\le\operatorname{cov}(A)\le(\frac12+o(1))\sqrt p\ln p$
always, $(1+\varepsilon)\sqrt p\ln p$ a.s., greedy empirically
$\approx0.29\sqrt p\ln p$), a conditional theorem reducing it to an
$O(\sqrt p)$-leftover near-packing statement, and a precise account of why
second-moment, energy, and nibble technology each provably cannot close it.

## 5. Files

```
Covering by Random Translates/
├── answer_manifest.json          # machine-readable verdict + evidence
├── derivation.md                 # full statements, proofs, verbatim verifier output
├── report.md                     # this file
├── code/
│   ├── sim_random_translates.py  # threshold/Gumbel/uncovered-count/regime experiments
│   ├── sim_greedy_cover.py       # chosen-translates greedy benchmark (exact FFT scores)
│   ├── verify_exactness.py       # mechanics cross-validation
│   └── verify_theory.py          # symbolic + exhaustive + MC theory checks
└── data/
    ├── random_translates_threshold.csv
    ├── gumbel_window.csv
    ├── uncovered_counts.csv
    ├── regime_100sqrtp.csv
    ├── greedy_cover.csv
    └── greedy_curve_p20011.csv
```

Seeds are fixed and documented in file headers; all runs reproduce
byte-identically.
