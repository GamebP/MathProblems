# Adversarial Verification of EP-15 Report

Do **not** rewrite the report yet.

Treat the report as a claimed mathematical proof/research document that may contain subtle false statements. Your job is to independently verify it and identify exactly which claims are valid, invalid, unsupported, or overstated.

The central question is:

$$
\sum_{n\ge1}(-1)^n\frac{n}{p_n}
$$

Do **not** assume the report's conclusions are correct merely because they are plausible or because citations are provided.

For every nontrivial claim, use the following standard:

1. Check whether the claimed result actually follows from the preceding equations.
2. Check asymptotic orders carefully, including missing factors of \(\log n\), \(\log\log n\), and powers of \(n\).
3. Distinguish rigorously between:

   * theorem,
   * consequence of a cited theorem,
   * heuristic,
   * numerical evidence,
   * conditional result,
   * conjecture,
   * and meta-mathematical claim.
4. Never upgrade a heuristic or compatibility argument into a proof.
5. Check that citations actually establish the specific statement being attributed to them.
6. If a statement is false, provide a concrete counterargument or corrected formula.
7. If a statement is merely unproved, explain exactly what is missing.
8. Do not reject a claim merely because it is unusual; demonstrate the mathematical failure.

Pay particular attention to these sections:

## 1. R3: Cipolla residual

Check rigorously whether the report can simultaneously claim

$$
p_n-E(n)
=O\!\left(\frac{n(\log\log n)^3}{(\log n)^3}\right)
$$

and

$$
p_n-E(n)\ll n e^{-c\sqrt{\log n}}
$$

for the **finite Cipolla truncation**

$$
E(n)=n\left(
L+\ell-1+\frac{\ell-2}{L}
-\frac{\ell^2-6\ell+11}{2L^2}
\right).
$$

Determine whether the de la Vallée Poussin error for \(\pi(x)\) can legitimately be transferred to this finite \(E(n)\), or whether that exponential estimate is false because the omitted Cipolla terms dominate it.

Then determine the correct rigorous envelope for

$$
\delta_n=\frac np_n-\frac n{E(n)}.
$$

Give the corrected equations explicitly.

## 2. R5: the constructed world \(W(\theta,\rho)\)

Determine whether the construction actually proves the claim

> “There is a self-consistent world indistinguishable from the primes with respect to every currently published unconditional prime theorem.”

Do not accept the construction merely because individual examples of known theorems appear compatible.

Identify the exact logical gap between:

$$
\text{“compatible with the listed theorems”}
$$

and

$$
\text{“compatible with every published unconditional theorem.”}
$$

Check every place marked [HEURISTIC] and explain whether those gaps are essential.

Determine whether \(W(\theta,\rho)\) is genuinely a rigorous countermodel or only a heuristic/adversarial model.

## 3. R5 drift calculation

Independently recompute the claimed asymptotic

$$
\sum_{k\le K}\tilde b_k
=
\frac{1-\theta}{2}\log\log K+O(1).
$$

Check all factors carefully, especially:

$$
\tilde p_{2k-1},
\qquad
\tilde p_{2k},
\qquad
\tilde g_{2k-1},
$$

and the denominator of \(\tilde b_k\).

Verify whether the claimed \(1/(k\log k)\) drift really occurs.

Also verify whether the proposed “sprinkle” and compensator construction genuinely has a convergent total effect on the pair series.

## 4. “Exact missing implication”

Check whether this statement is actually proved:

$$
\text{uniform parity-resolved gap statistics}
\Longleftrightarrow
\text{parity-equidistribution of }\pi(m).
$$

Determine whether the report proves an equivalence, only one implication, or neither.

Similarly inspect the statement that a bound such as

$$
\sum_{n\le x}(-1)^{\pi(n)}
\ll
\frac{x}{(\log\log x)^{1.1}}
$$

is exactly equivalent to the required gap-statistic statement.

Do not infer equivalence from both quantities being related in Tao's argument.

## 5. R2 total variation

Verify the GPY input and the deduction

$$
TV(N)\gg\log\log N.
$$

Check the Window Lemma carefully. In particular, check whether lower density of a set \(A\) really implies the claimed number of elements in every multiplicative window.

Check whether the GPY statement being cited gives the required density in **index space**, rather than merely a statement that has to be translated into index density.

## 6. R1 monotonicity

Verify every step proving infinitely many upward and downward steps.

In particular check the use of:

$$
\liminf g_n\le246,
$$

Westzynthius,

and

$$
p_n/n\sim\log n.
$$

Confirm whether “eventually monotone in neither direction” is established correctly.

## 7. Numerical claims

Check whether the numerical data can legitimately be described as:

> “verify convergence-consistency”

rather than merely numerical evidence.

Also check the fixed-point rounding argument:

$$
\text{total error}\le \frac{N}{2M}.
$$

Determine whether rounding each term independently really gives this bound and whether the displayed table is internally consistent.

Do not treat \(N=10^7\) as evidence that an infinite series converges without clearly labeling it numerical evidence.

## 8. Tao's conditional result

Verify exactly what Tao's published theorem proves under his quantitative Hardy–Littlewood conjecture.

State precisely:

* what the conjecture assumes,
* what Tao proves from it,
* whether it directly establishes convergence,
* and whether the report attributes anything stronger to Tao than the paper actually proves.

Use the published paper rather than relying solely on the report's wording.

## 9. Final classification

Produce a table with columns:

| Claim | Status | Why | Correct replacement |

Use statuses:

* PROVED
* CORRECT CONSEQUENCE
* CONDITIONAL
* NUMERICAL ONLY
* HEURISTIC
* UNSUPPORTED
* FALSE / MATHEMATICALLY INCORRECT

For every FALSE claim, give the corrected mathematical statement.

For every UNSUPPORTED claim, state exactly what additional theorem would be required.

Finally give a verdict answering:

> Does the report currently constitute a valid proof of convergence, a valid proof of divergence, or a valid proof that the problem cannot currently be solved unconditionally?

Do not rewrite the report. Do not make it sound more convincing. The goal is to find mathematical mistakes, overclaims, and logical gaps before any rewrite.
