Do NOT rewrite this document.

Treat it as a potentially flawed research note and perform a hostile mathematical audit.

The goal is not to agree with the report. The goal is to find every place where the mathematics, scope, or logical status is overstated.

First verify the exact original GREEN-028 problem statement and distinguish it from any enlarged or modified target class.

Most importantly, audit the following.

### 1. Target-class equivalence

The original target is

$$
a(x)b(y)c(x+y)(-1)^{q(x,y)}.
$$

The report instead studies

$$
a(x)b(y)c(x+y)e_p(Q(x,y)).
$$

Determine rigorously whether the second class actually contains the first when \(p\) is odd.

Do NOT assume that “quadratic phase” and “\((-1)^q\)” are interchangeable.

If they are different classes, explicitly state whether the report is solving:

* the original problem,
* a stronger problem,
* a weaker problem,
* or a different problem.

Also check every sentence claiming that the enlarged class “contains both readings”.

### 2. Spectral identity

Independently derive

$$
\mathbb E_h\|\Delta_{(h,h)}f\|_\square^4
=
\sum_{\xi_1+\xi_2+\xi_3+\xi_4=0}
|\widehat{B_f}(\xi)|^2.
$$

Check every conjugation, sign, Fourier normalization, and the fact that the shift vector is

$$
(h,h,h,h).
$$

State whether the identity is fully correct.

### 3. \(U^3\) reduction

Derive from definitions, not numerical testing, whether

$$
\mathbb E_h\|\Delta_{2h}c\|_{U^2}^4
=
\|c\|_{U^3}^8.
$$

Verify the factor \(2h\), all conjugations, and the normalization.

If correct, provide a short exact derivation.

### 4. Diagonal family

Verify that

$$
f(x,y)=d(x-y)
$$

satisfies

$$
\Delta_{(h,h)}f\equiv1.
$$

Then derive the transformed correlation under

$$
x=(m+s)/2,\qquad y=(m-s)/2.
$$

Check whether the claimed “equivalent open trilinear inequality” is actually equivalent to the ORIGINAL GREEN-028 problem, or only to the enlarged target-class variant.

### 5. Rank-one rigidity theorem

Verify every displayed formula in R4, including the block decomposition of the quadratic form.

Check whether

$$
\Delta_{(h,h)}f(x,y)
=
\alpha_h(x)\beta_h(y)e_p(\omega_h)
$$

really follows for arbitrary unimodular \(a,b,d\) and quadratic \(Q\).

Then determine precisely what has been proved about the converse.

Do not accept “the converse is open” without separating:

* what the report proves,
* what is conjectured,
* and what is merely suspected.

### 6. Cubic mixed-twist collapse

Recompute from scratch the claim for

$$
\psi(x,y)=x_0y_0^2.
$$

Verify:

$$
\Delta_{(h,h)}\psi
=
2h_0x_0y_0+h_0y_0^2+2h_0^2y_0+h_0^2x_0+h_0^3.
$$

Then verify the box average for \(h_0\neq0\):

$$
\|\Delta_{(h,h)}f\|_\square^4=p^{-1}.
$$

Then independently derive

$$
\mathbb E_h\|\Delta_{(h,h)}f\|_\square^4
=
\frac{2p-1}{p^2}.
$$

Check the direction count explicitly.

### 7. General rank-r statement

Check whether

$$
\|\Delta_{(h,h)}f\|_\square^4=p^{-r}
$$

really follows whenever the surviving mixed component has rank \(r\).

Do NOT assume the co-factors cancel. Determine the exact hypotheses needed.

Classify the report's current wording as either:

* theorem,
* theorem under extra hypotheses,
* heuristic,
* or false.

### 8. Non-absorption lemma

Verify rigorously that

$$
e_p(\lambda x_1y_2)\notin
\{a(x)b(y)c(x+y)\}
$$

for \(n\ge2\).

Check the four-point multiplicative difference argument and the symmetry under swapping \(u,v\).

Make sure there are no hidden assumptions about \(a,b,c\).

### 9. Numerical optimization

Do NOT describe numerical optimization as proving a supremum.

Determine whether the reported “best correlation” is:

* a certified global optimum,
* a local optimum,
* or merely the best value found.

Check whether 1000 random restarts provide any mathematical guarantee.

Replace claims such as “the best correlation is” with the mathematically correct status when appropriate.

### 10. Literature-status claims

Every statement of the form:

* “no known theorem”
* “remains open”
* “no known implication”
* “exact open residue”
* “no other gap remains”
* “this is the current obstruction”

must be classified separately as a literature claim rather than a mathematical deduction.

Do not accept such claims without evidence.

### 11. Final verdict

Produce a table:

| Claim | Exact status | Mathematical reason | Required correction |

Use:

PROVED
CONDITIONAL
NUMERICAL ONLY
HEURISTIC
UNSUPPORTED
FALSE
SCOPE ERROR

Then answer exactly:

1. Does the document prove GREEN-028?
2. Does it prove a stronger/weaker/different statement?
3. Which displayed equations are actually false?
4. Which conclusions are valid despite the errors?
5. What are the minimum changes required to make the document mathematically honest?

Do not rewrite the paper until this audit is complete.
