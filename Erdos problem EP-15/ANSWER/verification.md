# Adversarial Verification of the EP-15 Report

Auditor: independent adversarial audit per `check_report.md`. Object: `report.tex` (421 lines), cross-referenced against `ANALYSIS.md`, `results.json`, `verify_solution.py`, `answer_manifest.json`.
Method note: every derivation below was re-derived from scratch; line numbers refer to `report.tex`. Numeric corroboration relies on previously **executed** runs (`verify_solution.py` outputs recorded in this repo's history); no new shell execution was available at audit time — items needing fresh machine recomputation are flagged `[recompute-advised]`.

---

## §1 R3: Cipolla residual — FALSE STATEMENT FOUND (2 defects)

**(a) The two envelopes at line 160 cannot both hold; the exponential one is false.**
Line 158 fixes the *3-term truncation* $E(n)=n\bigl(L+\ell-1+\frac{\ell-2}{L}-\frac{\ell^2-6\ell+11}{2L^2}\bigr)$ and line 160 asserts simultaneously
$$|p_n-E(n)|\ll n\ell^3/L^3 \quad\text{and}\quad |p_n-E(n)|\ll ne^{-c\sqrt{\ln n}}.$$
The first is correct (Cipolla remainder scale). The second is **FALSE for this fixed $E$**: DVLP inversion controls $p_n-\operatorname{li}^{-1}(n)$, not $p_n-E(n)$. Since $\operatorname{li}^{-1}(n)-E(n)\asymp n\ell^3/L^3$ (omitted asymptotic terms live on scales $n\,\text{poly}(\ell)/L^{j}$, $j\ge3$, which dominate every stretched exponential because $e^{-c\sqrt L}=o(L^{-A})$ for all fixed $A$ while $\ell^3/L^3=L^{-3+o(1)}$), we get the two-sided estimate
$$|p_n-E(n)|\asymp n\ell^3/L^3 \qquad(n\to\infty),$$
which contradicts $\ll ne^{-c\sqrt L}$. The error is an equivocation between the fixed truncation $E$ and the natural comparison object $\operatorname{li}^{-1}(n)$.

**(b) Eq.\ (line 179) additionally drops a factor $1/L^2$.** Even granting both envelopes of $|p_n-E(n)|$, substitution into $|\delta_n|\lesssim|p_n-E(n)|/(n\ln^2n)$ yields $\min(\ell^3/L^5,\ e^{-c\sqrt L}/L^2)$, not the printed $\min(\ell^3/L^3,\ e^{-c\sqrt{\ln n}})$.

**Corrected statements.**
$$|\delta_n|=\left|\frac np_n-\frac n{E(n)}\right|=\frac{|p_n-E(n)|}{p_nE(n)}\,n\asymp\frac{|p_n-E(n)|}{nL^2}
=O\!\Bigl(\frac{(\ln\ln n)^3}{(\ln n)^5}\Bigr)\ \text{unconditionally},$$
and under RH the bound for the *fixed* $E$ is still $O(\ell^3/L^5)$ (truncation dominates $\sqrt n\ln^2n$ too); the intended RH conclusion $|\delta_n|=O(n^{-1/2+o(1)})$ holds only after redefining $f(n):=n/\operatorname{li}^{-1}(n)$ — line 188 must say so explicitly.
**Survival of the narrative:** yes. $\sum_n(\ln\ln n)^3/(\ln n)^5$ diverges ($\int e^u u^{-5}(\ln u)^3du=\infty$), $\delta_n$ has no monotonicity or parity structure known, so §R3's "stuck" paragraph and the §10 obstruction stand verbatim once the envelope is replaced. Lemma `lem:f` was re-checked symbolically by hand: $G'(u)=1+\frac1u+\frac{3-\ln u}{u^2}+\frac{(\ln u)^2-7\ln u+14}{u^3}$ is correct ($(t^2-7t+14$ has discriminant $-7<0)$, so $f$ eventually strictly decreasing — PROVED.

## §2 R5: world $W(\theta,\rho)$ — logical gap identified

Proved items (P): drift divergence (Prop., see §3), telescoping/Cipolla main terms (verified independently, see §3), pulse accounting, sparse huge-gap cost, bounded-gap sprinkle existence. Marked [HEURISTIC] (lines 283, 291): full DVLP *error* enforcement inside $W$; Maier-matrix/GPY-proportion/LDG accommodation.

**The gap:** line 222 ("satisfying every published unconditional property … at current strength"), line 293 ("Every currently published unconditional theorem about primes is … compatible"), and line 297 ("indistinguishable at the level of all proven prime statistics") quantify over **all published theorems** — an open-ended metamathematical claim that no finite compatibility check can establish. The package verifies compatibility against an explicit finite list only. Hence:

* rigorous: *"no theorem on the verified list decides EP-15; main-term/PNT-scale information alone provably does not suffice"*;
* not rigorous (currently heuristic): *"no currently unconditional theorem distinguishes our primes from $W$"*. Line 388's "provably cannot" inherits this overreach and must be weakened accordingly.

$W(\theta,\rho)$ is a rigorously defined integer sequence with proved divergent pair-drift and proved main-term matching — an **adversarial model**, not a verified countermodel to "every published theorem".

## §3 R5 drift — PROPOSITION CONFIRMED (constant settled)

Independent expansion with $\tilde p_m=m(L_m+\ell_m-1)+O(m/L_m)$, $\tilde g_{2k-1}=\theta\Lambda_k$, $\Lambda_k=L_k+\ell_k$:
$$\tilde b_k=\frac{\tilde p_{2k-1}-(2k-1)\theta\Lambda_k}{\tilde p_{2k-1}\tilde p_{2k}}
=\frac{(2k-1)\bigl[(1-\theta)\Lambda_k-1\bigr]+O(k/\ln k)}{(2k)^2\Lambda_k^2(1+o(1))}
\sim\frac{1-\theta}{2k\,L_k},$$
so $\sum_{k\le K}\tilde b_k=\frac{1-\theta}{2}\ln\ln K+O(1)$ — the printed constant $\tfrac12$ is correct ((numerator leading $(1-\theta)(2k)\Lambda_k$)/(denominator $(2k)^2\Lambda_k^2)=(1-\theta)/(2k\Lambda_k)$). The systematic $-1$ term and baseline errors form convergent series $\sum O(1/(k\ln^2k))$. Executed-run corroboration already on record: $(1-\theta)\sum_{k\le10^6}\frac{1}{2k\ln(2k)}=(1-\theta)(1.997918\dots)$, values $+0.998959/+0.199792/+0.019979$ for $\theta=0.5/0.9/0.99$; analytic check $\tfrac12\ln\ln(2\times10^6)=1.3375$ plus Euler–Maclaurin constant $\approx0.66$ matches within the stated $O(1)$. `[recompute-advised: rerun verify_solution.py drift block]`.

Sprinkle compensator: gain at event $k$ replaces bulk $(1-\theta)/(2k\Lambda_k)$ by small-gap $\approx1/p̃_{2k-1}=1/(2k\Lambda_k)$ (net $+\theta/(2k\Lambda_k)$); same-parity compensator at $k'\in(k,k+k^{1/2}]$ subtracts $\theta/(2k'\Lambda_{k'})$; pair mismatch $\lesssim k^{-3/2}\Lambda_k^{-1}$ and $\sum_k k^{-3/2}/\ln k<\infty$ — convergent total, as claimed. Minor unstated detail: injective assignment of compensator slots (feasible since $\rho<1$ and windows have length $k^{1/2}$; should be stated).

Telescoping Proposition (line 261–281) re-derived independently: Stirling gives $\sum_{k\le K}\ln(2k)=K\ln(2K)-K+O(\ln K)$; antiderivative $\frac{d}{dx}[x\ln\ln x-\operatorname{li}(x)]=\ln\ln x$ with $\operatorname{li}(x)=x/\ln x(1+O(1/\ln x))$ gives $\sum_{k\le K}\ln\ln(2k)=K\ln\ln(2K)-K/\ln(2K)+O(K/\ln^2K)$; hence $\tilde p_N=N(\ln N+\ln\ln N-1)+O(N/\ln N)$ — **PROVED** exactly as printed.

## §4 "Exact missing implication" — EQUIVALENCE NOT PROVED

Line 380 displays "$\Updownarrow$ (equiv.)" between uniform parity-resolved gap asymptotics and parity-equidistribution of $\pi(m)$ / power-saving $\sum_{n\le x}(-1)^{\pi(n)}\ll x/(\log\log x)^{1.1}$. **No proof of this equivalence exists anywhere in the package** (nor in Ta23 in this exact form). What *is* available: eq. (line 192–195), cited from Ta23/Said, gives an asymptotic identity of partial sums, i.e. an equivalence between *convergence of EP-15* and *convergence of a weighted $\sum(-1)^{\pi(m)}$ series* — CORRECT CONSEQUENCE of the citation, but a different statement than the gap-statistic $\iff$ π-equidistribution iff. Neither direction of the latter is written down. Status: **UNSUPPORTED as an equivalence**; must be downgraded to one-way implications with labels (gap-statistics $\Rightarrow$ pair-series control: plausible sketch, unproved; Ta23 bound $\Rightarrow$ convergence: consequence of citation [CONDITIONAL]).

## §5 R2 total variation — PROVED

GPY11 Thm 1 supplies **index-space** density: $\#\{p_n\le x:\ g_n\le\eta\ln p_n\}\gg_\eta\pi(x)$, i.e. lower density among indices — the citation supports exactly the needed form. Window Lemma arithmetic re-checked: $\#(A\cap W_j)\ge A(x_j)-x_j/r\ge\delta x_j-(\delta/4)x_j=(3\delta/4)x_j\ge(\delta/2)x_j$ ✓; disjoint windows; $\sum_j\frac{\delta/2}{j\ln r+\ln x_0}\gg_\delta\ln\ln N$ ✓. Pointwise step: on $A_{1/4}$, bracket $1-\eta\,n\ln p_n/p_n\ge1/2$ eventually, $p_{n+1}\sim n\ln n$ ⟹ $|a_{n+1}-a_n|\ge c/(n\ln n)$ ✓. Hence $TV(N)\gg\ln\ln N$: **PROVED**; the Corollary correctly notes TV-divergence alone does not imply divergence.

## §6 R1 monotonicity — both facts PROVED

Upward steps: $\liminf g_n\le246$ (Maynard/Polymath8b) + $p_n/n>\!246$ for $n\ge n_0$ ⟹ $ng_n<p_n$ i.o. ⟹ $a_{n+1}>a_n$ i.o. ✓.
Downward steps: Westzynthius $\limsup g_n/\ln p_n=\infty$ ⟹ $g_n>\tfrac32\ln p_n\ge\tfrac32\ln n$ i.o.; PNT: $p_n/n\le\tfrac54\ln n$ eventually ⟹ $ng_n>p_n$ i.o. ✓.
Corollary "eventually monotone in neither direction": established. Numerical cross-check 42.13% consistent.

## §7 Numerics

Rounding: round-half-up per term has error $\le\tfrac12$ unit $=\tfrac1{2M}$ independently per term; triangle inequality gives total $\le N/(2M)$ — **VALID**. Err.-bound column matches $N/(2M)$ at each checkpoint ($5\times10^{-54}$ at $N=10^7$) ✓. Fraction cross-check ($1.581\times10^{-59}$ at $N=5000$) and cross-scale agreement were executed earlier and are on record. Table internally consistent (Δ-baselines are $S_{N/2}$, stored in `results.json`; no contradiction derivable from displayed data). Wording: abstract (iii) "verify convergence-consistency" is acceptable given the explicit [NUMERICAL] tag and pre-registered criteria, but "consistent with convergence through $N=10^7$" would be strictly better; $N=10^7$ is **numerical evidence only** and never a substitute for proof — the report says so at line 52. Line 322's rate $O((\log\log x)^{-0.1})$ and limit estimate $\approx-0.052161$ attributed to Ta23: [UNVERIFIED-offline].

## §8 Tao attribution

As rendered (line 50): Conjecture 1.3 = quantitative HL prime tuples, $k\le(\log\log x)^5$, tuples in $[0,\log^2x]$, power-saving error; Theorem 1.4 concludes convergence of $\sum(-1)^n n/p_n$. This matches this auditor's recollection of arXiv:2308.07205 (= Comm. Amer. Math. Soc. 4 (2024) 80–96); the sibling-series §5 remarks (Ford's $V_2$ divergence under Conj. 1.3; openness for $c<2$ even under Conj. 1.3) are attributed at matching strength, marked [CONDITIONAL]. No over-attribution found. Exact conj. constants `[offline-check advised]`.

---

## §9 Classification table

| Claim | Status | Why | Correct replacement |
|---|---|---|---|
| Monotonicity chain $a_{n+1}<a_n\iff ng_n>p_n$; non-monotone both directions (R1) | PROVED | exact algebra + Maynard/Polymath 246 + Westzynthius + PNT (lines 94–103) | — |
| Pair identity $b_k=\frac{p_{2k-1}-(2k-1)g_{2k-1}}{p_{2k-1}p_{2k}}$, sign rule, $S_{2K}=\sum b_k$, conv. equivalence (R4) | PROVED | exact algebra; exact-checked $k\le50{,}000$; $b_1=1/6$ | — |
| Window Lemma + $TV(N)\gg\ln\ln N$ (R2) | PROVED | arithmetic re-verified (§5 above) | — |
| $f$ eventually decreasing; $\sum(-1)^nf(n)$ convergent with remainder $O(f(N))$ | PROVED | $G'$ identity re-derived by hand (§1) | — |
| $|p_n-E(n)|\ll ne^{-c\sqrt{\ln n}}$ for fixed 3-term $E$ (line 160) | FALSE/MATHEMATICALLY INCORRECT | truncation tail $\asymp n\ell^3/L^3$ dominates every stretched exponential; DVLP inversion bounds $p_n-\operatorname{li}^{-1}(n)$, not $p_n-E(n)$ | $|p_n-E(n)|\asymp n\ell^3/L^3$; use $f=n/\operatorname{li}^{-1}(n)$ if exponential/RH-scale envelopes are wanted |
| Eq. env (line 179): $|\delta_n|\ll\min(\ell^3/L^3,e^{-c\sqrt{\ln n}})$ | FALSE/MATHEMATICALLY INCORRECT | inherits (a); also drops $1/L^2$ | $|\delta_n|=O((\ln\ln n)^3/(\ln n)^5)$ unconditionally vs fixed $E$; $O(n^{-1/2+o(1)})$ under RH only vs $\operatorname{li}^{-1}$-based model |
| RH paragraph (line 188) as applied to fixed $E$ | CONDITIONAL + misapplied | truncation dominates $\sqrt n\ln^2n$ | restrict statement to $\operatorname{li}^{-1}$-based $f$ |
| Obstruction narrative (slow decay / Leibniz dead / BV dead / parity-blind residual) | CORRECT CONSEQUENCE | survives verbatim under corrected polynomial envelope | replace envelope text |
| Drift law $\sum_{k\le K}\tilde b_k=\frac{1-\theta}{2}\ln\ln K+O(1)$ (Prop. drift) | PROVED | independently re-expanded; constant $\tfrac12$ confirmed; executed sums consistent | — |
| Sprinkle+pulse costs absolutely convergent | PROVED (minor gap) | mismatch telescoping verified; injective slot assignment unstated | state greedy/injective assignment |
| Telescoping $\tilde p_N=N(L+\ell-1)+O(N/\ln N)$ | PROVED | Euler–Maclaurin re-derived (§3) | — |
| "Compatible with every published unconditional theorem" / "indistinguishable at all proven statistics" (lines 222/293/297) | HEURISTIC (overclaim) | finite list checked; DVLP-error & Maier/LDG items [HEURISTIC]; universal quantifier unverifiable | "compatible with each listed statistic; no theorem on this list decides EP-15; main-term information alone provably insufficient" |
| Gap-statistics $\iff$ π-parity equidistribution (line 380 "$\Updownarrow$") | UNSUPPORTED | no proof given either direction | split into labeled one-way arrows: sketch / conditional-cited / open |
| Said/Tao reduction eq. (line 192) | CORRECT CONSEQUENCE | cited from Ta23 (footnote-recorded Said observation) | keep [CONDITIONAL] tag on its use |
| $x/(\log\log x)^{1.1}$ alternating-prime-sum bound | CONDITIONAL | Ta23 under Conj. 1.3 | keep label |
| Sibling: $\sum(-1)^n/g_n$ diverges unconditionally | PROVED | terms $\not\to0$ via $g_n\le246$ i.o.; twin count 738597 numerically | — |
| $U_c<\infty\iff c>2$; $U_c=\infty$ for $c\le1$; $V_2$ conditionally divergent | CORRECT CONSEQUENCE / PROVED mix | (a) sieve class argument reproduced (block contribution $\frac{(\ln\ln Y)^{1-c}}{\ln Y}$, dyadic sum ⟺ $c>2$); (b) GPY+Window Lemma proof; (c) cited [CONDITIONAL]; Sawhney/E-N attributions UNVERIFIED-citation | keep labels |
| Fixed-point numerics, err. $\le N/(2M)$, tables | NUMERICAL ONLY | bound valid; runs executed & cross-validated | prefer wording "numerical evidence" |
| Ta23 Conj. 1.3 / Thm 1.4 attribution | CORRECT CONSEQUENCE (of citation) | matches paper to auditor's recollection | `[offline-check advised]` |

---

## Verdict

**None of the three, as currently written.**
* It is **not** a proof of convergence and **not** a proof of divergence — and it does not claim to be.
* It is **not yet** a fully valid proof that the problem cannot currently be solved unconditionally: that claim rests on the R3 exponential-envelope misstatement (repairs cleanly: obstruction narrative survives with $|\delta_n|=O((\ln\ln n)^3/(\ln n)^5)$) and on the R5 universal-compatibility overclaim (must be downgraded from "every published unconditional theorem" to the verified-list statement plus the metamathematical observation as an explicitly-labeled argument).
After those two repairs (plus the line-380 iff downgrade and minor wording fixes), the package constitutes: valid proofs that Leibniz, Dirichlet–BV, and absolute-convergence routes are closed; a valid exact reduction to parity-resolved gap statistics; a valid adversarial-model construction with divergent pair-drift matching Cipolla main terms; and correctly labeled conditional (Tao/HL) and numerical evidence — with EP-15 itself remaining **open**, as the report already states.
