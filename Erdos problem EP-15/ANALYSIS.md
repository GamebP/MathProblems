# EP-15 — Analysis: $\sum_{n\ge1}(-1)^n n/p_n$

**Working target:** Erdős Problem EP-15 (erdosproblems.com/15; UnsolvedMath EP-15).
**Status of this document:** research analysis + reduction + obstruction isolation. Every claim is either proved in-file, cited, or explicitly labeled `[CONDITIONAL]` / `[HEURISTIC]` / `[NUMERICAL]` / `[UNVERIFIED-citation]`.

---

## (A) Exact target

> **Question (EP-15, verbatim).** Is it true that
> $$S \;=\; \sum_{n=1}^{\infty} (-1)^n \frac{n}{p_n}$$
> converges, where $p_n$ denotes the $n$-th prime?

Write throughout:
$$a_n := \frac{n}{p_n}, \qquad g_n := p_{n+1}-p_n, \qquad S_N := \sum_{n\le N} (-1)^n a_n .$$
The series starts with $(-1)^1 a_1 = -1/2$, so $S_{2K} = \sum_{k\le K}(a_{2k}-a_{2k-1})$ exactly (pairing $(1,2),(3,4),\dots$).

---

## (B) Verdict block

> ### VERDICT
> * **UNCONDITIONALLY OPEN.** No unconditional proof or disproof of convergence of $\sum (-1)^n n/p_n$ is known. This investigation does **not** solve the problem and does not claim to.
> * **CONDITIONAL [PROVEN under HL-strong]:** convergence holds assuming the Quantitative Hardy–Littlewood prime-tuples conjecture (Conjecture 1.3 of Tao, arXiv:2308.07205, with $k\le(\log\log x)^5$, power-savings error $Cx^{1-\varepsilon}$): Theorem 1.4 of [Ta23].
> * **NUMERICAL: CONVERGENCE-CONSISTENT through $N=10^7$** at exact fixed-point precision (§R6): steadily shrinking half-decade increments, no drift signal, paired partial sums bounded after the transient first pair.
> * The problem is **not solved and not disproved** here. What is delivered: rigorous proofs that the classical alternating-series machinery is inapplicable (R1, R2), an exact reduction to an isolated parity-resolved open subproblem (R3, R4), a counterexample-world construction showing no current unconditional theorem can decide the question (R5), and integration of the numerical evidence (R6).

---

## (C) Rigorous reductions

### R1. The Leibniz (alternating) test is PROVABLY inapplicable

Leibniz requires $a_n = n/p_n$ to be eventually non-increasing (to $0$). It is not — in either direction.

**Exact monotonicity chain.** For all $n\ge1$,
$$a_{n+1}<a_n \iff \frac{n+1}{p_{n+1}}<\frac{n}{p_n}
\iff (n{+}1)p_n < n p_{n+1}
\iff n p_n + p_n < n p_n + n g_n
\iff \boxed{\,n\,g_n > p_n\,},$$
and symmetrically $a_{n+1}>a_n \iff ng_n<p_n$. So upward steps of $(a_n)$ are exactly the indices where the gap is smaller than the local mean gap scale $p_n/n$.

**Claim 1 (upward steps occur infinitely often).**
*Proof.* Maynard's theorem (strengthening Zhang [Zh14]; constant via Polymath8b [Po14]) gives $\liminf_n g_n \le 246$, hence $g_n\le 246$ for infinitely many $n$. By the prime number theorem, $p_n/n \sim \ln n \to \infty$; choose $n_0$ with $p_n/n > 246$ for $n\ge n_0$. For infinitely many $n \ge n_0$ we then have $ng_n \le 246\,n < p_n$, i.e. $a_{n+1}>a_n$. $\square$

**Claim 2 (downward steps also occur infinitely often).**
*Proof.* Westzynthius [We31] proved $\limsup g_n/\ln p_n = +\infty$; hence $g_n>\tfrac32\ln p_n$ for infinitely many $n$. Since $p_n\ge n$, $\ln p_n\ge\ln n$, so $g_n>\tfrac32\ln n$ infinitely often; while PNT gives $p_n/n=(1+o(1))\ln n$, so $p_n/n\le\tfrac54\ln n$ for $n\ge n_0$. Along infinitely many indices both hold: $ng_n>p_n$, i.e. $a_{n+1}<a_n$. $\square$

**Conclusion.** $(a_n)$ is eventually monotone in neither direction; the Leibniz test cannot even be formulated, unconditionally. `[NUMERICAL cross-check: 42.13% of steps $n\le10^7$ are downward — strong two-sided fluctuation.]`

### R2. The Dirichlet bounded-variation criterion is PROVABLY inapplicable (unconditional)

Dirichlet test (BV form): if $a_n\to0$ and $(a_n)$ has bounded total variation, then $\sum(-1)^na_n$ converges (Abel summation). We show total variation diverges **unconditionally**.

**Exact step identity.**
$$a_{n+1}-a_n=\frac{(n{+}1)p_n-np_{n+1}}{p_np_{n+1}}
=\frac{np_n+p_n-n(p_n+g_n)}{p_np_{n+1}}
=\boxed{\;\frac{p_n-ng_n}{p_np_{n+1}}\;} \tag{2.1}$$
(sign consistent with R1: positive step $\iff p_n>ng_n$).

**Input (unconditional, cited): GPY positive-proportion small gaps.** Goldston–Pintz–Yıldırım [GPY11, Theorem 1]: for every fixed $\eta>0$,
$$P(x,\eta):=\frac{1}{\pi(x)}\#\{p_n\le x:\ g_n\le \eta\ln p_n\}\ \gg_\eta\ 1 .$$

**Proposition.** Fix $\eta=\tfrac14$. Let $A=\{n: g_n\le \eta\ln p_n\}$. Then for some $c>0$ and all large $N$,
$$TV(N):=\sum_{n<N}|a_{n+1}-a_n| \;\ge\; \sum_{\substack{n\le N\\ n\in A}} \frac{c}{n\ln n} \;\gg\; c'\,\delta\,\ln\ln N \;\longrightarrow\;\infty,$$
where $\delta=\delta(\eta)>0$ is the GPY lower density.
*Proof.* Step 1 (pointwise bound). For $n\in A$: by (2.1),
$$|a_{n+1}-a_n|=\frac{p_n-ng_n}{p_np_{n+1}}\ \ge\ \frac{p_n-\eta\,n\ln p_n}{p_np_{n+1}}
=\frac{1}{p_{n+1}}\Bigl(1-\eta\,\frac{n\ln p_n}{p_n}\Bigr).$$
Since $p_n/n\sim\ln n$, we have $n\ln p_n/p_n \to 1$; with $\eta=1/4$ the bracket is $\ge 1/2$ for $n\ge n_0$. Also $p_{n+1}\sim n\ln n$, so $|a_{n+1}-a_n|\ge \tfrac{c}{n\ln n}$ on $A$, $c>0$ absolute.
Step 2 (weighted sum over a positive-lower-density set). GPY gives $A(N)\ge\delta N$ for all $N\ge N_0$. **Window Lemma:** for any $A\subseteq\mathbb N$ with lower density $\delta>0$, $\sum_{n\in A,\,n\le N}\frac{1}{n\ln n}\gg_\delta\ln\ln N$.
*Proof of Lemma.* Let $r:=4/\delta\,(>2)$ and $x_j:=x_0 r^j$ with $x_0:=\max(2N_0,r)$. Each window $W_j:=(x_j/r,\,x_j]$ satisfies
$\#\,(A\cap W_j)=A(x_j)-A(x_j/r)\ \ge\ \delta x_j-x_j/r\ \ge\ (\delta/2)x_j$
(since $1/r=\delta/4<\delta$; here we used only the *total* lower density, no blockwise hypothesis). The $W_j$ are pairwise disjoint, lie in $[1,N]$ for $x_j\le N$, and
$$\sum_{n\in A\cap W_j}\frac{1}{n\ln n}\ \ge\ \#\,(A\cap W_j)\cdot\frac{1}{x_j\ln x_j}\ \ge\ \frac{\delta}{2\ln x_j}
=\frac{\delta}{2(j\ln r+\ln x_0)},$$
and summing over $j\le\log_r(N/x_0)$ gives $\gg_\delta\ln\ln N$. $\square$
Combining Steps 1–2 finishes the Proposition. $\square$

*(Audit note: an earlier draft summed GPY density block-by-block, which does not follow from total lower density alone; the Window Lemma above is the corrected, fully rigorous route.)*

**Conclusion.** $TV(N)\to\infty$ unconditionally (empirically like $0.55\ln\ln N$, §R6); the BV hypothesis fails, so Dirichlet-BV provably cannot decide EP-15. *(Of course $TV\to\infty$ does not imply divergence of the series — it only kills this proof route; cf. $\sum(-1)^n/\sqrt n$.)*

### R3. Smooth/fluctuation decomposition: reduction to a parity-blind residual

**Cipolla expansion** [Ci02]. With $L=\ln n$, $\ell=\ln\ln n$:
$$p_n=n\Bigl(L+\ell-1+\frac{\ell-2}{L}-\frac{\ell^2-6\ell+11}{2L^2}+O\!\Bigl(\frac{\ell^3}{L^3}\Bigr)\Bigr).$$
Fix the truncation
$$E(n):=n\Bigl(L+\ell-1+\frac{\ell-2}{L}-\frac{\ell^2-6\ell+11}{2L^2}\Bigr),\qquad f(n):=\frac{n}{E(n)},$$
so that $|p_n-E(n)|\ll n\,\ell^3/L^3$ (order of the omitted term) and moreover $|p_n-E(n)|\ll n e^{-c\sqrt{\ln n}}$ by inversion of the de la Vallée Poussin error term $\pi(x)=\operatorname{li}(x)+O(xe^{-c\sqrt{\ln x}})$ [vK01, DLVP].

**Lemma 1 ($f$ is eventually strictly decreasing, explicit derivative).**
Writing $u=\ln n$ and $G(u)= L+\ell-1+\frac{\ell-2}{L}-\frac{\ell^2-6\ell+11}{2L^2}$ (so $E(n)=nG(u)$, $f(n)=1/G(u)$):
$$f'(n)=-\frac{G'(u)/n}{G(u)^2},\qquad
G'(u)=1+\frac1u+\frac{3-\ln u}{u^2}+\frac{(\ln u)^2-7\ln u+14}{u^3}.$$
(The identity was verified symbolically by CAS.) Since $(\ln u)^2-7\ln u+14$ has negative discriminant ($49-56<0$), it is positive for all $u$; hence $G'(u)\ge 1+\frac1u-\frac{(\ln u-3)_+}{u^2}\ge \tfrac12$ for all $u\ge e^3$, giving
$$-\frac{2}{n\,G(u)^2}\ \le\ f'(n)\ \le\ -\frac{1}{2\,n\,G(u)^2}\qquad (u\ge e^3).$$
So $f'<0$ eventually, $f(n)\asymp 1/\ln n\to0$. $\square$
By Leibniz, $\sum(-1)^nf(n)$ converges with remainder $\le f(N{+}1)\ll 1/\ln N$.

**Lemma 2 (exact residual identity).**
$$a_n=f(n)+\delta_n,\qquad
\delta_n:=\frac{n}{p_n}-\frac{n}{E(n)}
=-\,(p_n-E(n))\cdot\frac{n}{p_n\,E(n)},$$
so, using $p_n,E(n)\asymp n\ln n$ (PNT):
$$|\delta_n|\ \lesssim\ \frac{|p_n-E(n)|}{n\ln^2 n}\ \ll\ \min\Bigl(\frac{\ell^3}{L^3},\ e^{-c\sqrt{\ln n}}\Bigr). \tag{3.1}$$
$\square$ Consequently: **the original series converges $\iff \sum(-1)^n\delta_n$ converges** (the $f$-part converges by Lemma 1).

**Why the residual is stuck unconditionally.** The envelope (3.1) decays slower than any power and is non-summable; worse, $\delta_n$ inherits the erratic sign of $p_n-E(n)$ and no monotonicity or parity structure is known for it. All zero-free-region technology bounds the *envelope* $|p_n-E(n)|$ and is **parity-blind**: it provides no information on $(-1)^n$-correlations of the fluctuations.

**What RH-grade input would (and would not) give.** Under RH, von Koch [vK01]: $\pi(x)=\operatorname{li}(x)+O(\sqrt x\ln x)$; inverting (mean-value/inverse-function estimate) yields $p_n=\operatorname{li}^{-1}(n)+O(\sqrt n\,\ln^2 n)$, whence $|\delta_n|=O(n^{-1/2+o(1)})$. `[CONDITIONAL: RH]`
But envelope decay alone still does **not** suffice: the comparison sequence $\delta'_n=(-1)^n/(\sqrt n\ln n)$ satisfies the very same envelope while $\sum(-1)^n\delta'_n=\sum 1/(\sqrt n\ln n)$ diverges. The Dirichlet-eta phenomenon ($\sum(-1)^n n^{-s+i\tau}$ converges for $\Re s>0$) relies on the rigid monomial structure $n^{-s}$, i.e. on full control of the two-sided fluctuations including their phases — for $\delta_n$ this is exactly parity-resolved information about primes which neither ZFC-current technology nor RH supplies. Interchanging limit operations over zeros (explicit-formula expansions of $p_n-\operatorname{li}^{-1}(n)$ as a sum over zeros, then alternating summation) is not available in any published form. **No published unconditional or RH-only proof exists; the published conditional route is HL-strength (Tao).** Marked honestly: *theorem* = Lemmas 1–2 + (3.1); *plausible-but-unpublished* = "RH reopens an eta-type argument".

**Cross-reference to the published route.** Tao [Ta23], recording an unpublished observation of Said (mathoverflow.net/questions/313999), proves the exact asymptotic relation
$$\sum_{n\le x}\frac{(-1)^n n}{p_n}=\frac12\sum_{2\le m\le x/\log x}\frac{(-1)^{\pi(m)}}{m\log m}+C+o(1), \tag{3.2}$$
reducing EP-15 to convergence of $\sum_m (-1)^{\pi(m)}/(m\log m)$, i.e. to cancellation in $(-1)^{\pi(m)}$ — again precisely parity-of-prime-counting information, obtained in [Ta23] from Conjecture 1.3 (quantitative HL) via Gallagher-type Poisson statistics plus the Banks–Ford–Tao random sifted model, giving $\sum_{n\le x}(-1)^{\pi(n)}\ll x/(\log\log x)^{1.1}$ `[CONDITIONAL: Conj. 1.3 of Ta23]`.

### R4. Pair reformulation — EXACT identities (no approximation)

Define the pair terms $b_k := a_{2k}-a_{2k-1}$, so that $S_{2K}=\sum_{k\le K}b_k$ **exactly**, and $S_{2K+1}=S_{2K}-a_{2K+1}$ with $a_{2K+1}\to0$; therefore
$$\boxed{\ \sum_{n\ge1}(-1)^n\frac{n}{p_n}\ \text{converges}\ \iff\ \sum_k b_k\ \text{converges}\ } \tag{4.0}$$

**Closed form.**
$$b_k=\frac{2k}{p_{2k}}-\frac{2k-1}{p_{2k-1}}
=\frac{2k\,p_{2k-1}-(2k-1)p_{2k}}{p_{2k-1}\,p_{2k}},$$
and inserting $g_{2k-1}=p_{2k}-p_{2k-1}$:
$$2k\,p_{2k-1}-(2k-1)p_{2k}=2k\,p_{2k-1}-(2k-1)(p_{2k-1}+g_{2k-1})
=\bigl[2k-(2k-1)\bigr]p_{2k-1}-(2k-1)g_{2k-1}
=p_{2k-1}-(2k-1)g_{2k-1}.$$
Hence
$$\boxed{\ b_k=\dfrac{p_{2k-1}-(2k-1)\,g_{2k-1}}{p_{2k-1}\,p_{2k}}\ },\qquad
b_k>0 \iff g_{2k-1}<\frac{p_{2k-1}}{2k-1}. \tag{4.1}$$
**Sign convention & sign check.** $b_k$ is defined as $a_{2k}-a_{2k-1}$ so that $S_{2K}=\sum_{k\le K}b_k$ with the series starting $(-1)^1$; positivity means the *even-indexed* term is larger, which happens iff the odd-indexed gap $g_{2k-1}$ is *below* the local mean-gap threshold $p_{2k-1}/(2k-1)\approx \ln(2k)$. Numerical sanity checks (exact rational arithmetic, sieve to $1.4\times10^6$):
* $k=1$: $b_1=a_2-a_1=\tfrac23-\tfrac12=\tfrac16$, and (4.1) gives $\frac{p_1-1\cdot g_1}{p_1p_2}=\frac{2-1}{6}=\frac16$. ✓ (matches $\max_K|B_K|=\tfrac16$ attained at $K=1$ in the data);
* both closed forms of (4.1) verified equal to $a_{2k}-a_{2k-1}$ for **all** $k\le 50{,}000$. ✓

> ⚠️ **Erratum vs. the tasking sheet:** the prompt states "$b_k>0\iff g_{2k-1}>p_{2k-1}/(2k-1)$" and offers numerator "$(2k-1)g-p$". Both are sign-inverted; the correct chain, verified above, is $2kp_{2k-1}-(2k-1)p_{2k}=p_{2k-1}-(2k-1)g_{2k-1}$, so $b_k>0\iff g_{2k-1}<p_{2k-1}/(2k-1)$. Intuition confirms: a *smaller-than-average* gap before $p_{2k}$ makes $n/p_n$ jump *up* across the pair. The qualitative conclusions are unaffected.

**Leading-order model form.** With $p_{2k-1}\asymp p_{2k}\asymp 2kL_k$, $L_k:=\ln(2k)$:
$$b_k=\frac{2kL_k-(2k-1)g_{2k-1}\pm O(kL_k\cdot\xi)}{4k^2L_k^2(1+o(1))}
\ \asymp\ \frac{L_k-g_{2k-1}}{2k\,L_k^2}
=\frac{1-g_{2k-1}/L_k}{2k\,L_k}. \tag{4.2}$$
So $|b_k|$ has typical size $\asymp 1/(k\ln k)$ (since $|L-g|\asymp L$ under exponential gap statistics) — matching the observed $TV(N)\sim0.55\ln\ln N$ — while its **sign** is governed by whether the odd-indexed normalized gap $g_{2k-1}/L_k$ falls below/above $1$. Convergence of $\sum_kb_k$ is thus a statement about **parity-resolved statistics of normalized gaps**: any persistent bias between odd-indexed and even-indexed gaps creates a one-signed drift $\sim\frac{|1-\theta|}{2}\ln\ln K$. This is the isolated open subproblem; it is equivalent (via (3.2)) to parity-equidistribution of $\pi(m)$ in log-length intervals. Nothing weaker than HL-tuples-strength input is known to control it (see R5).

### R5. Counterexample world $W(\theta,\rho)$: current unconditional theorems cannot decide EP-15

We construct a hypothetical "arithmetic world" — a strictly increasing integer sequence $(\tilde p_j)$ playing the role of the primes — exhibiting a persistent odd/even gap bias yet satisfying every published unconditional property of the primes at their current strength. Components marked (P) are proved below; compatibility items marked (C) are enforced by construction with cost estimates proved, up to standard balancing arguments labeled [HEURISTIC] where noted.

**Definition of $W(\theta,\rho)$.** Let $L_k=\ln(2k)$, $\ell_k=\ln\ln(2k)$, and $\Lambda_k:=L_k+\ell_k$; fix $\theta\in(0,2)$, $\theta\neq1$, $\rho\in[0,1)$.
1. *(Bulk, P)* For $k\notin\mathcal A$ (below), set $\tilde g_{2k-1}=\theta \Lambda_k(1+\xi_k)$, $\tilde g_{2k}=(2-\theta)\Lambda_k(1+\xi'_k)$ with balanced deterministic signs $\xi,\xi'=\pm o(1)$ chosen so pair totals stay $2\Lambda_k(1+O(\xi))$; per-pair mean gap is exactly preserved: $\tilde g_{2k-1}+\tilde g_{2k}=2\Lambda_k=2\bigl(\ln(2k)+\ln\ln(2k)\bigr)$ when $\xi=\xi'=0$. *(The $\ell_k$ layer is what makes the world reproduce the full Cipolla main terms; see (ii).)*
2. *(Sprinkle, P)* On a set $\mathcal A$ of lower density $\rho$ among odd positions, shrink the odd gap to a value $\in[2,246]$ (bounded gaps at positive density), and redistribute the borrowed mass $\Delta_k=\theta\Lambda_k-O(1)$ onto odd compensators at positions $k'$ with $k<k'\le k+k^{1/2}$ (same parity!), so that each event contributes to $\tilde S_{2K}$ only its *mismatch*: $\bigl|\frac{1}{2k\Lambda_k}-\frac{1}{2k'\Lambda_{k'}}\bigr|\lesssim\frac{k'-k}{k^2\Lambda_k}\lesssim\frac{1}{k^{3/2}\Lambda_k}$.
3. *(Pulses, P)* Each redistribution/pulse keeps all even-indexed cumulative sums unchanged beyond a local window: enlarging $\tilde g_{2k}$ by $\Delta$ and shrinking $\tilde g_{2k+2}$ by $\Delta$ lifts only $\tilde p_{2k+1}$, by $\le O(L_k)$.

**(i) Pair-drift retains the $(\theta-1)$ divergence; sprinkle contribution converges (P).**
From the exact identity (4.1), $\tilde b_k=\tilde b_k(\tilde g_{2k-1})$ depends on the odd gap directly and on even gaps only through denominators/baselines.

*Proof sketch that the corrected drift law is unchanged under the $\Lambda_k$ pattern (verbatim).* With $\tilde g_{2k-1}=\theta\Lambda_k$ and the uniform baseline of (ii), $\tilde p_m=m(\ln m+\ln\ln m-1)+O(m/\ln m)$, so $\tilde p_{2k-1}=(2k-1)(L_k+\ell_k-1)+O(k/\ln k)$ (off-by-one costs $O(1)$ in each factor) and $\tilde p_{2k}=2k\,\Lambda_k+O(k/\ln k)$. Substituting into (4.1):
$$\tilde b_k=\frac{\tilde p_{2k-1}-(2k-1)\,\theta\Lambda_k}{\tilde p_{2k-1}\,\tilde p_{2k}}
=\frac{(2k-1)\bigl[(1-\theta)\Lambda_k-1\bigr]+O(k/\ln k)}{(2k)^2\Lambda_k^2\,(1+o(1))},$$
which decomposes into three series:
$$\underbrace{\frac{(1-\theta)\Lambda_k}{2k\,\Lambda_k^2}\sim\frac{1-\theta}{2k\,L_k}}_{\text{parity drift}},\qquad
\underbrace{-\frac{1}{2k\,\Lambda_k^2}}_{\text{systematic }-1\text{ term}},\qquad
\underbrace{O\!\Bigl(\frac{1}{k\,\Lambda_k^2\ln k}\Bigr)}_{\text{baseline error}}.$$
The first sums like $\frac{1-\theta}{2}\sum_{k\le K}\frac1{k\ln k}\sim\frac{1-\theta}{2}\ln\ln K$ — **divergent for every $\theta<1$** (and for $\theta>1$ with opposite sign); the second and third are $O\bigl(\sum 1/(k\ln^2k)\bigr)=O(1)$: convergent. Hence
$$\sum_{k\le K}\tilde b_k=\frac{1-\theta}{2}\ln\ln K+O(1):$$
the drift law is **unchanged to leading order** by the $\ell_k$ upgrade. $\square$

Sprinkled events: direct effect of one bounded-gap replacement is $\asymp\frac{\Lambda_k}{2k\Lambda_k^2}=\frac{1}{2k\Lambda_k}$; its same-parity compensator contributes $-\frac{1}{2k'\Lambda_{k'}}$; net per event $\lesssim\frac{1}{k^{3/2}\ln k}$, and even granting all $\rho K$ events the trivial bound, $\sum_{k\ge2}\frac{1}{k^{3/2}\ln k}<\infty$. Pulse effects land only on baselines: $\partial\tilde b/\partial p\asymp 1/p^2$, contributing $\lesssim\sum_k\frac{\Lambda_k}{k^2\Lambda_k^2}=\sum\frac{1}{k^2\ln k}<\infty$. Total sprinkle+pulse contribution: an absolutely convergent series of order $\sum O(1/(k^{3/2}\ln k))$ (same convergent class as the announced $\sum O(1/(k\ln^2k))$). **Hence $W(\theta,\rho)$ has divergent $\sum_k\tilde b_k$ for every $\theta\neq1$, independent of $\rho$.**

> ⚠️ **Erratum vs. the executed probe script.** `ep15_partial_sums.py` (adversarial block) accumulated $(\theta-1)\sum_{k\le K}\frac{1}{2kL_k^2}$ — denominator $L_k^2$ without the numerator factor $L_k$ from (4.2) — whose total **converges** ($\sum_k 1/(k\ln^2 k)<\infty$); the printed values ($-0.722145,-0.144429,-0.014443$ at $K=10^6$, $\theta=0.5,0.9,0.99$) therefore do not themselves exhibit the claimed $\ln\ln$-divergence, and the script's stated per-pair form $\frac{g-L_k}{2kL_k^2}$ carries the opposite sign to the true leading order $(4.2)$. Corrected model drift at $K=10^6$: $(1-\theta)\sum_{k\le10^6}\frac{1}{2k\ln(2k)}=(1-\theta)(1.997918\dots)$, i.e. $+0.998959,+0.199792,+0.019979$ for $\theta=0.5,0.9,0.99$ (sign now matching (4.1): sub-average odd gaps push $S_{2K}$ **up**). The qualitative conclusion — any persistent parity bias forces divergence — survives and is proved above.

**(ii) Telescoping ⇒ the world reproduces the FULL Cipolla main terms (P).** Per construction, $\tilde g_{2k-1}+\tilde g_{2k}=2\Lambda_k$ in bulk; each redistribution moves mass only within odd positions across a $k^{1/2}$-window, so odd-position cumulative mass is conserved up to window-boundary leakage $\ll\rho K^{1/2}\ln K$ at $2K$; pulses have zero net effect on even cumulatives. Summing over pairs, the $\theta$-dependence **cancels exactly** in even-indexed cumulatives ($\theta\Sigma_\Lambda+(2-\theta)\Sigma_\Lambda=2\Sigma_\Lambda$):
$$\tilde p_{2K}=2+\sum_{k\le K}(\tilde g_{2k-1}+\tilde g_{2k})=2+2\sum_{k\le K}\Lambda_k+O\bigl(\rho K^{1/2}\ln K\bigr).$$
Euler–Maclaurin bookkeeping: $\sum_{k\le K}\ln(2k)=K\ln(2K)-K+O(\ln K)$ (Stirling), and, using the antiderivative $\frac{\mathrm d}{\mathrm dx}\bigl[x\ln\ln x-\operatorname{li}(x)\bigr]=\ln\ln x$ together with $\operatorname{li}(x)=\frac{x}{\ln x}\bigl(1+O(\tfrac1{\ln x})\bigr)$,
$$\sum_{k\le K}\ell_k=\sum_{k\le K}\ln\ln(2k)=K\ln\ln(2K)-\tfrac12\operatorname{li}(2K)+O(\ln\ln K)=K\ln\ln(2K)-\frac{K}{\ln(2K)}+O\Bigl(\frac{K}{\ln^2K}\Bigr).$$
Therefore
$$\tilde p_{2K}=2K\bigl(\ln(2K)+\ln\ln(2K)-1\bigr)+O\Bigl(\frac{K}{\ln K}\Bigr),$$
and, since one further increment costs $O(\ln N)$ and pulse lifts are $O(\ln N)$, uniformly for all $N$:
$$\boxed{\ \tilde p_N=N\bigl(\ln N+\ln\ln N-1\bigr)+O\Bigl(\frac{N}{\ln N}\Bigr)\ }$$
— i.e. $W(\theta,\rho)$ reproduces the **full Cipolla main terms through the constant $-1$**, with honestly stated residual $O(N/\ln N)=o(N)$ (the world does not track sub-constants such as the $(\ell-2)/L$ term; every published unconditional statistic involves only main terms through this precision or is an upper bound — PNT first and second order, BHP-type gap upper bounds, Zhang–Maynard/Pintz existence-at-density statements). Consequently $\tilde\psi(x)=\tilde\vartheta(x)$ matches the true-prime PNT scale with identical leading and second-order structure up to $o(N)$; $\tilde\pi(x)/\pi_{\mathbb P}(x)\to1$ at PNT scale — macro-statistics match the true primes up to local perturbations. `[HEURISTIC: enforcing the full de la Vallée Poussin *error* inside $W$ requires a standard discrepancy-balancing choice of the $\xi$'s; the main-term statement just given is proved.]`

**(iii) Compatibility with published unconditional theorems (P/C).**
* Bounded gaps i.o. and at density: built in (sprinkle, size $\le246$, density $\rho>0$) → Zhang/Maynard/Polymath/Pintz-type statements satisfiable. (P)
* Upper bounds on gaps: bulk gaps $\le 2\Lambda_k(1+\xi_{\max})+O(1)=O(\ln N)$ (second-order Cipolla scale included), $\ll p_N^{0.525}$ → BHP exponent compatible; PNT matched through the $\ln\ln N$ term per (ii). (P)
* Large-gap limsup lower bounds (Westzynthius/Erdős–Rankin/Ford–Green–Konyagin–Maynard–Tao): insert Rankin-scale gaps at super-exponentially sparse positions $n_j$ (both parities; even ones pulse-compensated). Cost to $\sum_k\tilde b_k$ per event: $\lesssim\Delta_j/(n_j\ln n_j)$ (odd) resp. $\lesssim\Delta_j/(n_j^2\ln n_j)$-baseline class (even); choosing $n_j=2^{2^j}$ makes $\sum_j\Delta_j/(n_j\operatorname{polylog})<\infty$ since $\Delta_j\le n_j^{o(1)}$. (P)
* Maier-matrix irregularities, GPY positive-proportion-$\eta$-small gaps, LDG distributional statements: accommodated by tuning $\xi$-statistics and the sprinkle profile. `[HEURISTIC]`
Every currently *published unconditional* theorem about primes is an upper-bound/existence statement compatible with these choices.

**Conclusion (the isolation).** There is a self-consistent world $W(\theta,\rho)$, indistinguishable at the level of all proven prime statistics, in which $\sum_k\tilde b_k$ diverges like $\frac{1-\theta}{2}\ln\ln K$. Therefore **no currently unconditional theorem distinguishes our primes from a world where the series diverges.** The missing information is exactly **parity-resolved local gap correlation** — how $g_{2k-1}$ distributes around $p_{2k-1}/(2k-1)$ versus $g_{2k}$ around $p_{2k}/(2k)$. This is supplied by Hardy–Littlewood: Gallagher's calculation (HL ⇒ Poissonian counts in $(x,x+\lambda\log x]$, mean parity $e^{-2\lambda}$), quantified via Kuperberg's singular-series moment estimates and the Banks–Ford–Tao random sifted model, yielding Tao's bound $\sum_{n\le x}(-1)^{\pi(n)}\ll x/(\log\log x)^{1.1}$ [Ta23].

**EXACT missing implication (quote).**
> "Uniform-in-$\lambda$ parity-resolved asymptotics for $\#\{k\le K:\ g_{2k-1}\le\lambda\,p_{2k-1}/(2k-1)\}$ across $\lambda$ (equivalently: equidistribution of the parity of $\pi(m)$ in intervals $(x,x+\lambda\log x]$, i.e. a power-saving bound for $\sum_{n\le x}(-1)^{\pi(n)}$) $\Rightarrow$ the signed pair series $\sum_k b_k$ converges $\Rightarrow$ $\sum(-1)^nn/p_n$ converges." Tao [Ta23] establishes the needed consequence of this chain modulo the Quantitative HL prime-tuples conjecture (his Conjecture 1.3); nothing weaker is known to supply it — by R5, anything weaker that remains compatible with $W(\theta\neq1,\rho)$ provably cannot.

### R6. Numerical evidence integration `[NUMERICAL]`

Computed at exact fixed-point arithmetic (scale $M=10^{60}$, round-half-up per term, rigorous accumulated rounding bound $\le N/(2M)$; validated against `fractions.Fraction` at $N=5000$, $|$diff$|=1.581\times10^{-59}$; independent pass at $M'=10^{50}$ agrees to 40 significant digits; sieve self-checks $p_{10^6}=15485863$, $p_{10^7}=179424673$):

| $N$ | $S_N=\sum_{n\le N}(-1)^n n/p_n$ | increment $S_N-S_{N/2}$ | err.\ bound |
|---|---|---|---|
| $10^3$ | $+0.01186889173738435952\ldots$ | $-8.081\cdot10^{-3}$ | $5\cdot10^{-58}$ |
| $10^4$ | $-0.003290179164309845181\ldots$ | $-3.068\cdot10^{-3}$ | $5\cdot10^{-57}$ |
| $10^5$ | $-0.01353568322452828242\ldots$ | $-2.507\cdot10^{-3}$ | $5\cdot10^{-56}$ |
| $10^6$ | $-0.01985921629843783672\ldots$ | $-1.611\cdot10^{-3}$ | $5\cdot10^{-55}$ |
| $10^7$ | $-0.02428703417779226395\ldots$ | $-1.202\cdot10^{-3}$ | $5\cdot10^{-54}$ |

Interpretation:
* **Increments decay steadily** ($-8.08\to-1.20$ in units of $10^{-3}$ per half-decade); no drift signal. Consistent with slow conditional rate $O((\log\log x)^{-0.1})$ [Ta23] and with the putative limit $\approx-0.052161$ estimated in [Ta23]: $S_{10^7}=-0.0243$ is still far above it, as expected for logarithmic-rate convergence.
* **Term scale** $a_N=N/p_N$: $0.1263\ (10^3)\to0.0557\ (10^7)$; slow, as in R3.
* **Non-monotonicity empirical:** $\#\{n\le10^7: a_{n+1}<a_n\}/N=0.4213$ (58% of steps increase) — Leibniz fails empirically too, matching the proof in R1.
* **Total variation (exact):** $TV(10^6)=1.4346694\ldots$, $TV(10^7)=1.5262825\ldots$; $TV/\ln\ln N\approx0.546\to0.549$, growing without apparent bound — BV criterion fails, matching R2's $\gg\ln\ln N$.
* **Pair sums** $B_K=S_{2K}$: $\max_{K\le5\cdot10^6}|B_K|=\tfrac16$ **exactly at $K=1$** (transient first pair $\tfrac23-\tfrac12$); thereafter bounded well below. Cancellation ratio $\max|B_K|/TV_{\text{pair}}(10^7)=0.2212$ — massive sustained cancellation between pair terms, as required for convergence.
* **Companion Erdős series** $C_N=\sum_{n\le N}(-1)^n/(ng_n)$: $C(10^6)=-0.969706102197659$, $C(10^7)=-0.969826739960779$, half-decade drifts $\le2.9\cdot10^{-5}$ — converging. *(Open unconditionally and even under Ta23's Conjecture 1.3 — see (D).)*
* **Pre-registered divergence criteria:** divergence would manifest as (α) non-vanishing amplitude of $\Delta_N=S_N-S_{N/2}$, or (β) sustained $\ln\ln$-drift of $B_K$ (cf. the $W(\theta)$ probe magnitude $\frac{|1-\theta|}{2}\ln\ln K$). Neither is observed through $10^7$.

---

## (D) Sibling problems

**D.1 $\sum(-1)^n/g_n$ DIVERGES — unconditional, trivial modulo bounded gaps.** Maynard/Polymath8b: $g_n\le246$ infinitely often ⇒ summands satisfy $|(-1)^n/g_n|=1/g_n\ge1/246$ along an infinite sequence ⇒ terms do not tend to $0$ ⇒ divergence (ordinary and alternating alike). Also recorded in [Ta23, §5]. `[NUMERICAL: $\#\{n\le10^7:g_n=2\}=738597$.]` Contrast Weisenberg's observation [per erdosproblems.com page; UNVERIFIED-citation]: under HL $k$-tuples the partial sums are unbounded in at least one direction — the sibling diverges *robustly*, while the weighted original resists proof.

**D.2 Weighted variants.** Define the two siblings
$$U_c:=\sum_n\frac{1}{n\,g_n\,(\ln\ln n)^c}\ \ (\text{no sign}),\qquad
V_c:=\sum_n\frac{(-1)^n}{n\,g_n\,(\ln\ln n)^c}.$$

*(a) $U_c<\infty$ for $c>2$ — reproduced cleanly (this is the "absolute convergence" theorem).* Input (upper-bound-sieve class; cf.\ "sparsity of very small gaps" $\#\{p_n\le x:\ g_n\le h\}\ll\min(h/\ln x,1)\,\pi(x)$, [GPY11, Thm 2]; the sharp dyadic form is attributed on the problem page to a Selberg-sieve argument of Sawhney `[UNVERIFIED-citation]`):
$$\#\{n\in[Y,2Y]:\ g_n\in[\varepsilon\ln n,2\varepsilon\ln n)\}\ \ll\ \varepsilon Y .$$
Fix a dyadic block $[Y,2Y]$, $\lambda=\ln Y$. For the $\varepsilon$-class, each term satisfies $1/(ng_n(\ln\ln n)^c)\le\frac{2}{Y\cdot\varepsilon\lambda\cdot(\ln\lambda)^c}$, whence the class contributes
$$\ll\ \varepsilon Y\cdot\frac{2}{Y\,\varepsilon\lambda\,(\ln\lambda)^c}=\frac{2}{\ln Y\,(\ln\ln Y)^c}
\qquad(\text{independent of }\varepsilon).$$
The number of active classes is $J\approx\log_2\lambda$ (truncate at $\varepsilon\ge1/\lambda$: below that the class is empty since $g_n\ge2$), so
$$\sum_{Y<n\le2Y}\frac{1}{ng_n(\ln\ln n)^c}\ \ll\ \frac{\log\lambda}{\lambda(\ln\lambda)^c}+\underbrace{\frac{C}{\ln^3 Y(\ln\ln Y)^c}}_{\text{large-}g\text{ stratum (Markov: }\#\{g\ge G\}\ll Y/G\text{, weight }(1/G))}\ \asymp\ \frac{(\ln\ln Y)^{1-c}}{\ln Y}.$$
Summing over $Y=2^m$: $\sum_m\frac{(\ln m)^{1-c}}{m}$ converges $\iff c>2$. Hence $U_c<\infty$ for $c>2$ — matching Erdős–Nathanson [per page; `UNVERIFIED-citation`] and Sawhney's sieve proof as relayed by the page.

*(b) $U_c=\infty$ for $c\le1$ — unconditional.* By GPY Theorem 1, the set $A_\eta=\{n:g_n\le\eta\ln p_n\}$ has lower density $\delta_\eta>0$ for every fixed $\eta>0$; on $A_\eta$,
$$\frac{1}{ng_n(\ln\ln n)^c}\ \ge\ \frac{1}{n\cdot\eta\ln n\cdot(\ln\ln n)^c},$$
and the Window Lemma of §R2 (Step 2) applied to $A_\eta$ yields $\sum_{n\in A_\eta,n\le N}\frac{1}{n\ln n}\gg\ln\ln N$, so
$$\sum_{n\le N,\,n\in A_\eta}\frac{1}{ng_n(\ln\ln n)^c}\ \gg_\eta\ \sum_{\text{windows }j}\frac{1}{\ln x_j(\ln\ln x_j)^c}\ \asymp\ \sum_j\frac{1}{j(\ln j)^c}\ =\ \infty\iff c\le1.$$
*(This strengthens the naive typical-gap heuristic $\sum\frac{1}{n\ln n(\ln\ln n)^c}$, which also diverges exactly for $c\le1$.)*

*(c) Regime $1<c\le2$ and the alternating sibling.* $V_c$ converges absolutely for $c>2$ by (a). At the endpoint: [Ta23, §5] sketches (argument due to Ford) that $V_2$ **diverges** assuming Conjecture 1.3 — refuting, conditionally, the Er98 conjecture "for all $c>0$" at $c=2$. For $0\le c<2$ convergence of $V_c$ remains open **even under Conjecture 1.3** [Ta23, §5]; probabilistic heuristics (independent random signs, Khintchine's inequality) support convergence of $V_0=\sum(-1)^n/(ng_n)$ — the numerically convergent companion of R6 — and suggest more generally $\sum(-1)^n/(n^\theta g_n)$ converges for $\theta>\tfrac12$ [Ta23].

> ⚠️ **Erratum vs. the tasking sheet.** The sheet's claim "absolute convergence FAILS for every $c$" (with $\sum\frac{1}{ng_n(\ln\ln n)^c}\asymp\sum\frac{1}{n(\ln\ln n)^c}$) is **incorrect as stated**: the proposed comparison drops the essential $1/\ln n$ factor ($\mathbb E[1/g]\asymp\ln\ln n/\ln n$, not $\asymp1$ — the exponential-law constant $\mathbb E|g-\ln n|\asymp\ln n$ concerns $|g-\ln n|$, not $1/g$), and $\sum\frac{1}{n\ln n(\ln\ln n)^c}$ itself converges for $c>1$. The correct three-regime picture proved/cited above: $U_c=\infty$ for $c\le1$ (proved, GPY-based), $U_c<\infty$ for $c>2$ (Erdős–Nathanson/Sawhney), $1<c\le2$ resolved only conditionally at $c=2$ (divergence of $V_2$ under Conj.\ 1.3 [Ta23]).

**D.3 Why the siblings bracket the original.** Removing the weight ($1/g_n$ instead of $n/p_n$-type decay) destroys term-to-zero and gives unconditional divergence (D.1); keeping a stronger weight ($1/(ng_n)$) produces a series that plausibly converges but is beyond even HL-strong at $c=0$. The original sits at the critical weighting $a_n\asymp1/\ln n$ where absolute convergence fails, monotonicity fails, BV fails — and only parity-resolved information can decide.

---

## (E) Obstruction statement — THE deliverable

> **BOXED OBSTRUCTION.** The series $\sum_{n\ge1}(-1)^n n/p_n$ sits exactly in the dead zone of alternating-series theory: its terms $a_n=n/p_n$ decay only like $1/\ln n$, far too slowly for absolute convergence ($\sum 1/\ln n$ diverges); the bounded-gaps theorems of Zhang–Maynard force $a_{n+1}>a_n$ infinitely often (indeed $a_{n+1}<a_n\iff ng_n>p_n$, and $g_n\le246\ll p_n/n$ i.o.), so Leibniz's monotonicity hypothesis is provably false in both directions; the exact step identity $a_{n+1}-a_n=(p_n-ng_n)/(p_np_{n+1})$, evaluated on the GPY positive-density set of gaps $\le\eta\ln p_n$, gives total variation $\gg\sum 1/(n\ln n)\sim\ln\ln N\to\infty$ (observed: $TV(N)\approx0.55\ln\ln N$), killing the Dirichlet–BV criterion; and after subtracting the smooth Cipolla model $f(n)=n/E(n)$ — whose alternating sum converges — the residual $\sum(-1)^n\delta_n$, $\delta_n=-n(p_n-E(n))/(p_nE(n))$, has envelope $|\delta_n|\ll e^{-c\sqrt{\ln n}}$ (RH would merely sharpen it to $n^{-1/2+o(1)}$, which by itself decides nothing: $(-1)^n n^{-1/2}/\ln n$ meets that envelope with divergent alternating sum). All unconditional error-term technology is parity-blind and monotonicity-free: it bounds $|p_n-E(n)|$ but says nothing about the odd/even correlation that drives the exact pair terms $b_k=\bigl(p_{2k-1}-(2k-1)g_{2k-1}\bigr)/(p_{2k-1}p_{2k})$, on which convergence is exactly pinned by $S_{2K}=\sum_{k\le K}b_k$. The counterexample world $W(\theta,\rho)$ — parity-biased bulk gaps whose pair-means $2\Lambda_k$, $\Lambda_k=\ln(2k)+\ln\ln(2k)$, telescope to $\tilde p_N=N(\ln N+\ln\ln N-1)+O(N/\ln N)=N\cdot(\text{full Cipolla main terms})+o(N)$, compensated bounded-gap sprinkle, sparse huge gaps — satisfies every published unconditional prime statistic while its pair series diverges like $\frac{1-\theta}{2}\ln\ln K$ (the systematic non-parity pieces of $\tilde b_k$ form convergent series $\sum O(1/(k\ln^2k))$); hence resolution demands genuinely new, **parity-resolved local prime statistics**. Exact missing bridge: *"uniform-in-$\lambda$ parity-resolved asymptotics for $\#\{k\le K: g_{2k-1}\le\lambda p_{2k-1}/(2k-1)\}$ (equivalently parity-equidistribution of $\pi(m)$ in log-length intervals / a power-saving $\sum_{n\le x}(-1)^{\pi(n)}\ll x/(\log\log x)^{1.1}$) $\Rightarrow\sum_kb_k$ converges $\Rightarrow$ EP-15 convergent"* — supplied today only by the Quantitative Hardy–Littlewood prime-tuples conjecture via Tao's random-sifted-model proof; nothing weaker is known, and nothing weaker can suffice by R5.

---

## (F) Sources

* **[Ta23]** T. Tao, *The convergence of an alternating series of Erdős, assuming the Hardy–Littlewood prime tuples conjecture*, arXiv:2308.07205 (2023); Comm. Amer. Math. Soc. **4** (2024), no. 3, 80–96. [Verified: abstract, Conj. 1.3, Thm 1.4, eq. (2.1)/Said equivalence, §5 sibling remarks, numerical limit ≈ −0.052161.]
* **[Er98]** P. Erdős, *Some of my new and almost new problems and questions on combinatorial number theory, prime and additive number theory*, Number theory (Eger, 1996), de Gruyter, Berlin, 1998, pp. 169–180. [Problem E7, p. 203 referenced via Ta23; sibling conjectures as relayed by the problem pages.]
* **[Zh14]** Y. Zhang, *Bounded gaps between primes*, Ann. of Math. (2) **179** (2014), 1121–1174. [Volume/pages verified.]
* **[Ma15]** J. Maynard, *Small gaps between primes*, Ann. of Math. (2) **181** (2015), 383–413. [Standard citation; used for $\liminf(p_{n+m}-p_n)\ll m^3e^{4m}$ / dense clusters.]
* **[Po14]** D. H. J. Polymath, *Variants of the Selberg sieve, and bounded intervals containing many primes*, J. Aust. Math. Soc. **97** (2014), 321–347. [$\liminf g_n\le246$.]
* **[GPY11]** D. A. Goldston, J. Pintz, C. Y. Yıldırım, *Positive proportion of small gaps between consecutive primes*, Publ. Math. Debrecen **79** (2011), 433–444; arXiv:1103.3986. [Theorem 1: $P(x,\eta)\gg_\eta1$; Theorem 2: sparsity of very small gaps.] See also *Primes in tuples IV*, Acta Arith. **160** (2013). [Used in §R2, §D.]
* **[We31]** Ø. Westzynthius, *Über die Verteilung der Zahlen, die zu den n ersten Primzahlen teilerfremd sind*, Comment. Phys.-Math. Soc. Sci. Fennicae **5** (1931), no. 25, 1–37. [Large gaps.]
* **[Ci02]** M. Cipolla, *La determinazione asintotica dell'$n$-mo numero primo*, Matematiche (Catania) **8** (1902), 132–146. [Expansion of $p_n$.]
* **[vK01]** H. von Koch, *Sur la distribution des nombres premiers*, Acta Math. **24** (1901), 159–182. [RH error term.]
* **[Ga76]** P. X. Gallagher, *On the distribution of primes in short intervals*, Israel J. Math. **23** (1976), 193–198. [Poisson statistics from HL; used in Ta23.]
* **[BFT]** W. D. Banks, K. Ford, T. Tao, random sifted model paper (referenced as [1]/[2] in Ta23; exact coordinates [UNVERIFIED-citation]); **[Ku]** V. Kuperberg, quantitative singular-series moments (referenced as [11] in Ta23; [UNVERIFIED-citation]).
* **[Bl]** B. Bloom, erdosproblems.com/15 (page relaying EP-15 status, Er98 conjectures, Weisenberg and Sawhney remarks). [Page facts as given; Sawhney/Weisenberg/Erdős–Nathanson citation details UNVERIFIED-citation.]
* **[UM]** UnsolvedMath, entry EP-15. [Status Open; facts relayed in tasking confirmed against [Ta23] and [GPY11].]
* Said, unpublished observation, mathoverflow.net/questions/313999 (equivalence recorded in [Ta23]). [Verified via Ta23 footnote.]

**Labels used for unverifiable second-hand claims:** Sawhney's attribution and exact statement; Weisenberg's remark; Erdős–Nathanson bibliographic details; Banks–Ford–Tao and Kuperberg coordinates. All mathematical content relying on them is independently derived or clearly separated above.
