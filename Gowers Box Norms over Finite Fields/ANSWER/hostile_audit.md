# HOSTILE MATHEMATICAL AUDIT — GREEN-028 manuscript set

Auditor role: adversarial reviewer. Mandate: `ANSWER/check_report.md` (left unmodified).
Scope audited: root `report.tex` (authoritative), `ANSWER/{answer_manifest.json, report.tex}`,
`derivation.txt`, `evidence.txt`, `verify_solution.py`, `data/*`.
No file other than this audit was created or modified.

---

## 0. Original target locked

GREEN-028 (root report L84–90; manifest "problem"): p odd, f : F_p^n x F_p^n -> C,
|f| <= 1; if E_h ||Delta_(h,h) f||_box^4 >= delta, must f correlate with
a(x)b(y)c(x+y)(-1)^{q(x,y)} (a,b,c one-variable, q polynomial)?

Two readings of the phase:
* (i)  (-1)^q = e_p(Q), deg Q <= 2 — candidate class C_i = C = {abc e_p(Q)}.
* (ii) genuinely {+/-1}-valued factor — class C_ii = {abc sigma : sigma : G^2 -> {+/-1}}.
       With unbounded-degree q EVERY sign pattern arises: q=(1-x^{p-1})(1-y^{p-1})
       produces the single-point flip (machine-checked [H] below).

Key elementary fact (machine-checked [A]): for odd p, e_p(F_p) ∩ {+/-1} = {+1};
no function e_p(R) of any kind ever takes the value -1.

---

## 1. Verdict table

| # | Claim (location) | Exact status | Mathematical reason | Required correction |
|---|------------------|--------------|---------------------|---------------------|
| 1 | "C contains the candidate classes of BOTH readings"; "applies unchanged to both readings"; "strengthens each positive result and weakens no negative one" (root L99–109; ANSWER report.tex setup ¶; derivation.txt L14–17; manifest R5 dominance phrasing) | SCOPE ERROR / FALSE (containment fails for reading ii) | Every member of C has swap-symmetric mixed multiplicative second difference D_{u,v}F = D_{v,u}F (the abc coboundary c(m+u+v)c(m)/[c(m+u)c(m+v)] is symmetric in u,v; u^T B v is symmetric when n=1). Counterexample sigma = 1 - 2*delta_{(0,0)} on F_5^2: D_{(1,2)}sigma(4,3) = -1 but D_{(2,1)}sigma(4,3) = +1 [B]; all 3000 random C-members (generic unimodular a,b,c + general quadratic Q) are symmetric. Hence C_ii is NOT subset of C. Exact relation: n=1: C = T0 STRICTLY CONTAINED IN C_ii; n>=2: INCOMPARABLE (e_p(lambda x1y2) in C\C_ii because e_p(lambda) not in {+/-1}; single-flip sigma in C_ii\C). "A {+-1}-valued phase is a unimodular factor" is a non sequitur: membership requires the specific a(x)b(y)c(x+y)e_p(Q) structure, not mere unimodularity. | Delete the both-readings containment sentence in all four places; state that every result addresses reading (i)/class C only; add the incomparability statement with the explicit counterexample; note that under reading (ii) with unbounded-degree q the transmitted question degenerates (any unimodular f correlates positively with an aligned sign pattern), so reading (i) is the substantive reading. |
| 2 | Proposition A: E_h ||Delta_(h,h) f||_box^4 = sum_{xi in Xi_0} |Bhat_f(xi)|^2, shift vector u=(h,h,h,h) (root §2, eq:spectral) | PROVED | Re-derived from definitions: box expansion assembles E_z B_f(z+u) * conj(B_f(z)); Fourier orthonormality gives sum_xi |Bhat|^2 e_p(xi·u); xi·u = h·(xi1+xi2+xi3+xi4); E_h e_p(h·kappa) = 1_{kappa=0}. All conjugations, signs and normalizations correct. Independently re-implemented and machine-verified at (p,n)=(3,1),(5,1),(3,2): max diff 1.7e-16 [C]. | None. |
| 3 | Lemma absorb (n=1); Lemma noabsorb (n>=2, arbitrary functions alpha,beta,gamma) | PROVED | xy = ((x+y)^2-x^2-y^2)/2 coefficient algebra reproduces Bxy; mixed-difference argument forces w1*s2 = s1*w2 for all s,w, contradiction at s=e2,w=e1. No regularity/hidden assumptions on alpha,beta,gamma. | None. |
| 4 | Prop B factorization ||abw(x+y)||_box^4 = ||w||_U2^4; Corollary reduction E_h||Delta_(h,h)[abc]||^4 = E_h||Delta_{2h}c||_U2^4 = ||c||_U3^8 incl. factor 2h and cube-average equivalence (root §3) | PROVED (scope: phaseless T0; reaches reading-(i) members only at n=1 via absorption) | Delta_(h,h)[abc](x,y) = a_h(x) b_h(y) Delta_{2h}c(x+y): factor 2h exact since (x+h)+(y+h)=x+y+2h; h -> 2h bijective for odd p; relabeling (h,m,r,s) -> (x,h1,h2,h3) maps the eight factors bijectively onto subset sums with matching conjugation signs. Machine-verified with generic non-root-of-unity unimodular phases: all three displays equal 0.42972... simultaneously [D]. | Add scope tag "phaseless class T0 / reading (i)". |
| 5 | Observation C: f=d(x-y) meets hypothesis at delta=1; twisted-trilinear display; ANSWER R3 wording "the maximal-hypothesis case of THE problem IS EXACTLY a uniform positive lower bound for this trilinear correlation" | First parts PROVED; the "exactly" equivalence is a SCOPE ERROR | d((x+h)-(y+h))*conj(d(x-y)) = 1 identically ✓; x=(m+s)/2, y=(m-s)/2 bijective (odd p) ✓; display equals class-C correlation ✓. But equivalence holds only for the delta=1 case of the READING-(i)/class-C problem; under reading (ii) the fourth factor is an unconstrained sign matrix, which the trilinear reduction does not capture. Mandate item 4 last part answered: equivalent to reading-(i) variants ONLY, not to the original problem under reading (ii). | Qualify R3/O1 with "reading (i)"; O1 is not the delta=1 case of the transmitted problem under reading (ii). |
| 6 | Theorem D block formulas: Delta_(h,h)f = alpha_h(x) beta_h(y) e_p(omega_h); P = M_xx + M_xy, R = M_yx + M_yy, omega_h = (1/2)(h,h)^T M (h,h) + l^T(h,h) | PROVED | Q(z+(h,h))-Q(z) = (M delta)^T z + (1/2) delta^T M delta + l^T delta is separately affine: mixed coefficient vanishes identically; d-factor cancels. Convention check: Q=Ax^2+Bxy+Cy^2+... corresponds to M=[[2A,B],[B,2C]], giving P=2A+B, R=B+2C, omega_h=(A+B+C)h^2+(D+E)h — matches direct expansion; pointwise machine check over ALL (h,x,y) at (5,1) with random factors and mixed-term Q: max dev 6.66e-16 [F]. Holds for arbitrary unimodular a,b,d and quadratic Q. | None. |
| 7 | Conjecture D' (necessity): "every unimodular f with pointwise rank-one diagonal increments satisfies the parallelogram equation Theta(u+w,v+t) Theta(u-w,v-t) = Theta(u+t,v-w) Theta(u-t,v+w)" (root Conj D'; ANSWER Step 4; manifest R4) | FALSE as a necessity claim | Violated by members of the report's OWN sufficiency family. With Theta(u,v)=f((u+v)/2,(u-v)/2): f=e_p(x^2) at p=5, (u,v,w,t)=(1,-1,1,1): LHS = e_p(2), RHS = 1 [E]. Also f=e_p(xy): LHS=e_p(1), RHS=1. Even the pure constituent Theta=d(v) of every family member fails: d(v+t)d(v-t) vs d(v-w)d(v+w) with d=e_p(v^2) differ unless t^2=w^2. Companion sentence "for multiplicative-phase constituents the equation holds immediately because each constituent sees arguments that cancel pairwise" is likewise FALSE: the a,b,d constituents evaluate at (u+v)/2 +/- (w+t)/2 vs (u+v)/2 +/- (t-w)/2 and at v+t,v-t vs v-w,v+w — no pairwise cancellation for generic phases; only the e_p(Q) part cancels, up to e_p(w^2-t^2). The correct necessary-and-sufficient condition equivalent to rank-one is the rectangle law on the derivative: Delta(x1,y1)Delta(x2,y2)=Delta(x1,y2)Delta(x2,y1) for all x1,x2,y1,y2 and each h — which is definitional, hence carries no reduction content; the converse classification is simply open. | Delete eq:parallelogram as stated; replace by the rectangle condition (or any corrected nontrivial invariant after genuine re-derivation); rewrite Conjecture D' to assert only family membership of rank-one functions; remove "holds immediately for multiplicative-phase constituents"; fix manifest R4 ("converse classification reduces to ... parallelogram equation") which asserts a false reduction. |
| 8 | Sharpness corollary: cubic twist e_p(xy^2); increment 2h xy + h y^2 + 2h^2 y + h^2 x + h^3; rank-one destroyed for 4 of 5 directions at p=5 (0.8) | PROVED | Increment expansion verified term-by-term and pointwise inside [F]; rectangle/minor test gives failing directions {1,2,3,4}, fraction 0.8 [F]. | None. |
| 9 | Collapse law: ||Delta_(h,h) f||_box^4 = 1 if h0=0, p^{-1} if h0!=0; E_h = (2p-1)/p^2 independent of n and of a,b,d,Q | PROVED | Increment algebra exact ([F] pointwise 6.66e-16); corner-combination kills all one-variable terms and constants; survivor E_{u,v} e_p(2h0 u0 v0) = P(v0=0) = p^{-1} for 2h0 != 0; direction count p^{n-1} + (p-1)p^{n-1}*p^{-1} over p^n gives (2p-1)/p^2 (5/9, 9/25, 13/49 at p=3,5,7). Independently machine-verified per direction: values [1, .2, .2, .2, .2], average 0.36 = 9/25 at (5,1); unperturbed control exactly 1 [F]. | None. |
| 10 | Rank-r robustness corollary (manifest R6 / ANSWER Step 6): "if the only non-pairwise-cancelling factor is e_p(B_h) with cross-block C of rank r then ||Delta||^4 = p^{-r} (a fortiori <= p^{-r} alongside pairwise-cancelling factors)" | CONDITIONAL — theorem under extra hypotheses | Corner combination of bilinear B reduces to u^T C v; E_u e_p(u^T Cv) vanishes unless Cv=0, giving p^{-r} — but ONLY under the stated sole-survivor hypothesis. Non-pairwise-cancelling companions can conspire and RAISE the value above p^{-r}: demonstrated on F_5^2 — C = I_2 (rank 2) alone gives 1/25, while adding companion block [[0,0],[0,1]] leaves combined cross-rank 1 and raises the value to 1/5 > 1/25 [G]. The ANSWER derivation's parenthetical concedes this; the visible text of manifest R6 does not carry the caveat next to its "a fortiori" clause. Classification demanded by mandate item 7: theorem-under-extra-hypotheses (not bare theorem, not heuristic, not false). | Insert the sole-survivor/pairwise-cancellation hypothesis inline in manifest R6 before the "a fortiori" clause. |
| 11 | Strengthened non-absorption: e_p(lambda x1y2) not in T0 for n>=2, lambda != 0, arbitrary (unimodular) a,b,c; T0 STRICTLY CONTAINED IN rigidity family | PROVED | Four-point difference D_{u,v} e_p(lambda x1y2) = e_p(lambda u1v2) constant; representation forces c(m+u+v)c(m) = e_p(lambda u1v2) c(m+u)c(m+v); LHS symmetric in u<->v for EVERY c; u=e1, v=e2 forces e_p(lambda)=1, i.e. lambda=0. Needs only nonzero values of a,b,c (guaranteed by unimodularity); no hidden assumptions. Symmetric-half absorption identities verified ((x1+y1)(x2+y2) expansion; x1y2-x2y1 = (1/2)(s1 m2 - s2 m1)). Scope paragraph in root/ANSWER honestly notes that under reading (i) the witness IS in the transmitted class. | None mathematical; see #12 on the surrounding literature-status sentences. |
| 12 | Numerics: M defined as "sup"; Table 4 caption "Maximal correlations"; manifest R5 "the best correlation is 0.7236067977..." ; "optimizing over arbitrary unimodular a,b,c already dominates the supremum over the full stated class" | NUMERICAL ONLY / overstated status language | Alternating phase maximization on a nonconvex functional converges to stationary points; 1000 restarts provide NO certificate of global optimality. The quoted numbers are best-FOUND LOWER BOUNDS for the true supremum. The dominance sentence is valid only under reading (i) at n=1 (absorption makes the class equal to T0); under reading (ii) the stated class is strictly larger and the computed quantity does NOT dominate it. Positive: the quadratic-control computation is exactly right (4x^2+4y^2-2(x+y)^2 = 2(x-y)^2 gives corr = 1; naive witness gives Gauss value 1/sqrt(p) — both re-derived here). | Relabel everywhere: "best found" (lower bound), caption "Best-found correlations"; keep "sup" only as definition of the unattained quantity; attach reading-(i)+n=1 qualifier to the dominance sentence; do not describe the search as proving or computing a supremum. |
| 13 | Literature-status sentences: "The problem is open in both directions"; "not known to imply"; "no implication from the spectral condition to correlation is currently known"; "remains open"; "no counterexample are known"; "exact open residue"; "no other gap remains between the rigidity family and the transmitted readings" (root abstract/L148–156/§7; ANSWER box + Step 5 + Step 7 scope; manifest direct_answer/missing_bridge) | UNSUPPORTED as deductions — these are LITERATURE claims | None is derived from anything in the paper; none carries a citation to a survey or search record. They are plausible and consistent with the paper's own partial results, but they are assertions about the published landscape and must be labeled as such; "no other gap remains" additionally asserts a completeness of the reduction program that nothing in the paper establishes. | Tag each such sentence explicitly as a literature-status claim (e.g., "literature claim, not established here"); soften "no other gap remains"/"exact open residue" to "the reductions of this paper leave precisely these two named questions". |
| 14 | ANSWER Step 7 scope: "Whether the FULL transmitted class covers the rigidity family up to uniform correlation IS PRECISELY the twisted trilinear inequality (O1)" | UNSUPPORTED equivalence claim | Not proved anywhere: O1 concerns targets d(x-y) against class C at delta=1; coverage of the whole rigidity family (members ab d(x-y) e_p(Q)) up to uniform correlation is a different quantified statement. Under reading (i) rigidity members lie in C themselves, making one direction trivial and the claimed equivalence ill-posed rather than deep. | Downgrade to "is motivated by / related to O1". |
| 15 | n>=2 twist-range paragraph citing Lemma noabsorb to justify that the pullback twist "ranges over all quadratic forms in (s,m)" (root L469–485) | Correct conclusion, irrelevant citation | Surjectivity of Q -> Q o L for invertible linear L is what yields the range claim; Lemma noabsorb (non-absorbability) is not needed for it and does not imply it. | Replace citation with the pullback-surjectivity argument. |
| 16 | data/probe_large_p.{py,txt} (p = 11,13,17 decay probe) exists in data/ but is unreported in root report.tex, ANSWER/report.tex and manifest evidence_refs | Transparency gap (minor) | Manuscript cites only p in {5,7}; the probe shows cubic_best 0.5429 at p=11 BELOW random_best 0.6451 — relevant, unmentioned context. | Reference the probe or fold it into §Numerics with the same best-found caveat. |

Defect tally: 3 MAJOR (#1 scope error, #7 false conjecture/false "holds immediately", #12 numerics sup-language),
4 MODERATE (#5 equivalence scope error, #10 hidden-hypothesis presentation, #13 literature-status assertions,
#14 unsupported O1-equivalence), 3 MINOR (#15 citation, #16 transparency, plus truncation-hedging inconsistencies
between manifest R6/R7 and ANSWER derivation). All other audited displays are TRUE.

---

## 2. Machine verification log (independent throwaway code, stdlib only, this audit)

* [A] e_p(t) = -1 has no solution for p in {3,5,7}: confirmed.
* [B] sigma = 1-2*delta_(0,0) on F_5^2: D_(1,2)sigma(4,3) = -1.0, D_(2,1)sigma(4,3) = +1.0;
      3000/3000 random class-C members (generic unit-modulus a,b,c, general quadratic Q)
      satisfy swap symmetry. Hence reading-(ii) class is not contained in C.
* [H] q=(1-x^4)(1-y^4) mod 5 reproduces sigma via (-1)^q: confirmed (reading-(ii) reach).
* [C] Spectral identity independently reimplemented (naive box average + own DFT):
      (3,1): 0.6049382716049383 vs 0.6049382716049384, diff 1.11e-16;
      (5,1): 0.488 vs 0.48800000000000004, diff 1.67e-16;
      (3,2): 0.29875188402851865 vs 0.29875188402851870, diff 5.55e-17.
* [D] U3 reduction at p=5, generic unimodular phases:
      E_h box = 0.42971982354976, E_h U2-of-Delta_h c = 0.42971982354976, cube average = 0.42971982354976.
* [E] Parallelogram violations at p=5: f=e_p(x^2): LHS=-0.809017+0.587785j vs RHS=1;
      f=e_p(xy): LHS=0.309017+0.951057j vs RHS=1; constituent Theta=d(v), d=e_p(v^2): violated.
* [F] Thm D splitting + cubic increment pointwise over all (h,x,y) at (5,1): max dev 6.66e-16;
      sharpness minor test: failing directions {1,2,3,4}, fraction 0.8;
      collapse per-direction values [1, 0.2, 0.2, 0.2, 0.2], average 0.36 = 9/25;
      unperturbed control exactly 1.
* [G] Rank conspiracy on F_5^2: E e_p(u^T I_2 v) = 1/25; with added non-cancelling companion
      [[0,0],[0,1]] the value rises to 1/5 > 1/25 — "a fortiori <= p^{-r}" needs the sole-survivor hypothesis.

Provided suite `verify_solution.py` was read line-by-line: it recomputes from definitions on both sides
(exact rational accumulation for Check 1 LHS; axis-by-axis DFT for RHS; independent closed-form predictions
in Check 7); its reported residuals in verification.json are consistent with the manuscript quotes.
Its optimization outputs are heuristic local searches (correctly coded as such inside the script, but
promoted to sup-language in the manuscript).

---

## 3. The five mandated answers

1. Does the document prove GREEN-028? — NO. Verdict UNRESOLVED stands; no correlation statement
   in either direction is proved for any delta.
2. Stronger/weaker/different? — DIFFERENT-and-narrower coverage: the paper works entirely on the
   READING-(i) variant over the enlarged class C (a strict superset of reading-(i) targets, hence a
   genuinely stronger target side than reading (i)); relative to reading (ii) it addresses a DIFFERENT
   problem and proves nothing about it (C_ii is not contained in C; incomparable at n>=2). Within its
   classes it proves structural reductions only — no correlation lower bound, no counterexample.
3. Which displayed equations are actually false?
   (a) the eq:class scope sentence "contains the candidate classes of both readings";
   (b) Conjecture D''s parallelogram equation as a NECESSITY claim (violated at p>=5 by e_p(x^2),
       e_p(xy), and by the pure constituent Theta=d(v));
   (c) "the equation holds immediately for multiplicative-phase constituents";
   (d) manifest R4/R7 wording asserting the converse "reduces to" that equation and that the two named
       questions constitute the "exact open residue" with "no other gap remaining".
   All core quantitative identities (spectral identity, absorption/no-absorption, Prop B, U3 reduction
   with 2h, Theorem D splitting, sharpness count, collapse-law values 1 and p^{-1} and (2p-1)/p^2,
   direction count, control-witness identities) are TRUE.
4. Which conclusions survive despite the errors? — Proposition A (independently reverified);
   Lemmas absorb/noabsorb and their strengthened arbitrary-factor version; Prop B; the U3 Corollary
   (phaseless class; reading-(i) at n=1); Observation C at delta=1 for reading (i); Theorem D and the
   0.8-sharpness corollary; the collapse law; T0 STRICTLY CONTAINED IN rigidity family for n>=2.
   Numerics survive ONLY as best-found lower bounds plus the exact quadratic-control computation.
5. Minimum changes for honesty — (i) delete/correct the four "both readings" passages per table row 1;
   (ii) replace Conjecture D' and its motivation per row 7; (iii) relabel numerics as best-found and
   qualify dominance per row 12; (iv) tag every open/no-known-implication/exact-residue sentence as a
   literature claim and drop "no other gap remains" per rows 13–14; (v) add the sole-survivor caveat
   inline in manifest R6 per row 10; (vi) fix the noabsorb citation per row 15.

— End of hostile audit.
