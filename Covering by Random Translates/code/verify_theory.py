#!/usr/bin/env python3
"""
GREEN-081 theory verifier (exact integer arithmetic where feasible).

V1  Symbolic identity  C(p-2,k)/C(p,k) == (p-k)(p-k-1)/(p(p-1)).
V2  Exhaustive enumeration (p=7,k=2,m=3) and (p=13,k=3,m=4) over ALL
    (A, t_1..t_m) of the uncovered-count X:
        E X   == p*q^m,          q   = 1 - k/p
        E X^2 == p*q^m + p(p-1)*f^m,  f = C(p-2,k)/C(p,k)
    compared as exact Fractions.
V3  Monte Carlo (p=101,k=10,m=100, 20000 trials): empirical mean/std of X
    vs closed form (mean mu, sd from Var = EX^2 - (EX)^2 <= mu).
V4  Regime magnitudes mu = p*(1-1/sqrt p)^(100 sqrt p) at p=997, 10007.
Exit code != 0 on any failure.
"""
import sys
from fractions import Fraction
from itertools import combinations, product

import numpy as np

FAIL = False


def check(name, cond, detail=""):
    global FAIL
    tag = "PASS" if cond else "FAIL"
    if not cond:
        FAIL = True
    print(f"{tag}: {name} {detail}")


def closed_form_moments(p, k, m):
    q = Fraction(p - k, p)
    f = Fraction((p - k) * (p - k - 1), p * (p - 1))
    mu = p * q ** m
    ex2 = mu + p * (p - 1) * f ** m
    return mu, ex2


def exhaustive(p, k, m):
    """Return exact (Fraction(EX), Fraction(EX2)) over all A and all t^m."""
    pts = list(range(p))
    tuples = np.array(list(product(pts, repeat=m)), dtype=np.int64)
    n_t = tuples.shape[0]
    sumX = 0
    sumX2 = 0
    for A in combinations(pts, k):
        inA = np.zeros(p, dtype=bool)
        inA[list(A)] = True
        X = np.zeros(n_t, dtype=np.int64)
        for x in pts:
            hits = np.zeros(n_t, dtype=bool)
            for i in range(m):
                hits |= inA[(x - tuples[:, i]) % p]
            X += (~hits)
        sumX += int(X.sum())
        sumX2 += int((X * X).sum())
    n_tot = n_t * len(list(combinations(pts, k)))
    return Fraction(sumX, n_tot), Fraction(sumX2, n_tot)


def v1_symbolic():
    try:
        import sympy as sp
        p, k = sp.symbols("p k", positive=True)
        lhs = sp.binomial(p - 2, k) / sp.binomial(p, k)
        rhs = (p - k) * (p - k - 1) / (p * (p - 1))
        diff = sp.simplify(lhs - rhs)
        ok = diff == 0
        check("V1 symbolic C(p-2,k)/C(p,k) == (p-k)(p-k-1)/(p(p-1))", ok,
              f"(simplify diff = {diff})")
    except Exception as e:  # pragma: no cover
        check("V1 symbolic", False, f"sympy error: {e}")


def v2_enumeration():
    for (p, k, m) in [(7, 2, 3), (13, 3, 4)]:
        emp_ex, emp_ex2 = exhaustive(p, k, m)
        cf_mu, cf_ex2 = closed_form_moments(p, k, m)
        var_emp = emp_ex2 - emp_ex ** 2
        var_cf = cf_ex2 - cf_mu ** 2
        check(
            f"V2 exhaustive p={p},k={k},m={m}: E X",
            emp_ex == cf_mu,
            f"enum={float(emp_ex):.12g} closed={float(cf_mu):.12g}",
        )
        check(
            f"V2 exhaustive p={p},k={k},m={m}: E X^2",
            emp_ex2 == cf_ex2,
            f"enum={float(emp_ex2):.12g} closed={float(cf_ex2):.12g}",
        )
        check(
            f"V2 exhaustive p={p},k={k},m={m}: Var(X) <= E X",
            var_emp <= emp_ex,
            f"Var={float(var_emp):.6g} <= mu={float(emp_ex):.6g}",
        )


def v3_mc():
    rng = np.random.default_rng(20260826)
    p, k, m, n = 101, 10, 100, 20000
    mu_cf, ex2_cf = closed_form_moments(p, k, m)
    var_cf = ex2_cf - mu_cf ** 2
    xs = np.empty(n, dtype=np.int64)
    for i in range(n):
        A = rng.choice(p, size=k, replace=False)
        inA = np.zeros(p, dtype=bool)
        inA[A] = True
        t = rng.integers(0, p, size=m)
        covered = np.zeros(p, dtype=bool)
        covered[(A[None, :] + t[:, None]) % p] = True
        xs[i] = p - int(covered.sum())
    emp_mu = xs.mean()
    emp_sd = xs.std(ddof=1)
    se = np.sqrt(float(var_cf)) / np.sqrt(n)
    check("V3 MC mean vs closed form",
          abs(emp_mu - float(mu_cf)) < 4 * se,
          f"emp={emp_mu:.5f} closed={float(mu_cf):.5f} (4SE={4 * se:.5f})")
    rel = abs(emp_sd / np.sqrt(float(var_cf)) - 1)
    check("V3 MC sd vs closed form", rel < 0.10,
          f"emp_sd={emp_sd:.5f} closed_sd={np.sqrt(float(var_cf)):.5f} "
          f"relerr={rel:.4f}")
    check("V3 MC Var <= mean (Theorem A variance bound)",
          xs.var() <= emp_mu + 1e-9,
          f"emp_var={xs.var():.5f} emp_mean={emp_mu:.5f}")


def v4_regime():
    for p in (997, 10007):
        import math
        k = math.isqrt(p)
        m = round(100 * math.sqrt(p))
        mu = p * (1 - 1 / math.sqrt(p)) ** m
        check(f"V4 regime mu(p={p}) < 1e-38", mu < 1e-38,
              f"k={k} m={m} mu={mu:.3e}")
        print(f"     mu(p={p}, m=round(100*sqrt(p))={m}) = {mu:.6e}")


if __name__ == "__main__":
    v1_symbolic()
    v2_enumeration()
    v3_mc()
    v4_regime()
    print("VERIFY_THEORY:", "ALL PASSED" if not FAIL else "FAILURES PRESENT")
    sys.exit(1 if FAIL else 0)
