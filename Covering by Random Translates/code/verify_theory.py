#!/usr/bin/env python3
"""
GREEN-081 theory verifier v2 (exact integer/rational arithmetic where feasible).

Corrected second-moment identity (v1 of this file documented the failure of
the naive closed form with f^m; Jensen gap):
    X   = number of points of Z_p left uncovered by m i.i.d. random translates
    q   = 1 - k/p
    mu  = E X = p*q^m                                   [exact]
    w_A = 1 - (2k - c_d(A))/p,  c_d(A) = |A n (A+d)|, fixed d != 0
    g_m = E_A[w_A^m]
    E X^2 = p*q^m + p*(p-1)*g_m                          [exact]

V1  Symbolic identity  C(p-2,k)/C(p,k) == (p-k)(p-k-1)/(p(p-1))  (= E_A w_A).
V2  Exhaustive enumeration over ALL (A,t_1..t_m) for (p=7,k=2,m=3),
    (p=13,k=3,m=4): E X and E X^2 vs exact-Fraction closed forms where g_m is
    computed along an INDEPENDENT code path (A-enumeration only, no t-tuples).
    Informational: shows the naive f^m surrogate and its Jensen gap.
V3  Monte Carlo (p=101,k=10,m=100, 20000 trials): empirical mean/sd of X vs
    closed forms (g_m estimated from 200000 fresh A-draws).
V5  Asymptotic ratio check: g_m/q^{2m} -> 1 for m <= C*sqrt(p); measured at
    (p,k,m)=(101,10,32) where theory predicts |ratio-1| <~ m^2 E[d^2]/2 small.
V4  Regime magnitudes mu = p*(1-1/sqrt p)^round(100 sqrt p) at p=997,10007.
Exit code != 0 on any failure.
"""
import math
import sys
from fractions import Fraction
from itertools import combinations, product

import numpy as np

FAIL = False
D = 1  # shift used inside c_d(A); distribution over uniform A is d-independent


def check(name, cond, detail=""):
    global FAIL
    tag = "PASS" if cond else "FAIL"
    if not cond:
        FAIL = True
    print(f"{tag}: {name} {detail}")


def exact_gm(p, k, m):
    """g_m = E_A[w_A^m] as an exact Fraction, d=1."""
    acc = Fraction(0)
    for A in combinations(range(p), k):
        s = set(A)
        c = sum(1 for a in A if (a + D) % p in s)
        w = Fraction(p - 2 * k + c, p)
        acc += w ** m
    return acc / Fraction(math.comb(p, k), 1)


def closed_form_moments(p, k, m, gm=None):
    q = Fraction(p - k, p)
    mu = p * q ** m
    if gm is None:
        gm = exact_gm(p, k, m)
    ex2 = mu + p * (p - 1) * gm
    return mu, ex2, gm


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
    n_tot = n_t * math.comb(p, k)
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
              f"(simplify diff = {diff}; this equals E_A[w_A])")
    except Exception as e:  # pragma: no cover
        check("V1 symbolic", False, f"sympy error: {e}")


def v2_enumeration():
    for (p, k, m) in [(7, 2, 3), (13, 3, 4)]:
        emp_ex, emp_ex2 = exhaustive(p, k, m)
        cf_mu, cf_ex2, gm = closed_form_moments(p, k, m)
        var_emp = emp_ex2 - emp_ex ** 2
        var_cf = cf_ex2 - cf_mu ** 2
        q = Fraction(p - k, p)
        f = Fraction((p - k) * (p - k - 1), p * (p - 1))
        naive = p * q ** m + p * (p - 1) * f ** m
        check(f"V2 exhaustive p={p},k={k},m={m}: E X",
              emp_ex == cf_mu,
              f"enum={float(emp_ex):.12g} closed={float(cf_mu):.12g}")
        check(f"V2 exhaustive p={p},k={k},m={m}: E X^2 (corrected g_m form)",
              emp_ex2 == cf_ex2,
              f"enum={float(emp_ex2):.12g} closed={float(cf_ex2):.12g}")
        print(f"     info: g_m={float(gm):.8g}  "
              f"f^m(Jensen lower surr.)={float(f ** m):.8g}  "
              f"E X^2 with f^m would be {float(naive):.8g} (known-wrong)")
        check(f"V2 exhaustive p={p},k={k},m={m}: Var(X) <= 2*E X",
              var_emp <= 2 * emp_ex,
              f"Var={float(var_emp):.6g} vs mu={float(emp_ex):.6g}")


def sample_gm(p, k, m, n, rng):
    """Float Monte-Carlo estimate of g_m = E_A[w_A^m], d=1."""
    tot = 0.0
    for _ in range(n):
        A = rng.choice(p, size=k, replace=False)
        inA = np.zeros(p, dtype=bool)
        inA[A] = True
        c = int(inA[(A + D) % p].sum())
        tot += ((p - 2 * k + c) / p) ** m
    return tot / n


def v3_mc():
    rng = np.random.default_rng(20260826)
    p, k, m, n = 101, 10, 100, 20000
    q = 1 - k / p
    mu_cf = p * q ** m
    gm_est = sample_gm(p, k, m, 200000, rng)
    ex2_cf = mu_cf + p * (p - 1) * gm_est
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
    se = np.sqrt(max(var_cf, 1e-300)) / np.sqrt(n)
    check("V3 MC mean vs closed form",
          abs(emp_mu - mu_cf) < 4 * se,
          f"emp={emp_mu:.5f} closed={mu_cf:.5f} (4SE={4 * se:.5f})")
    rel = abs(emp_sd / np.sqrt(var_cf) - 1)
    check("V3 MC sd vs closed form (g_m-based)", rel < 0.10,
          f"emp_sd={emp_sd:.5f} closed_sd={np.sqrt(var_cf):.5f} "
          f"g_m_hat={gm_est:.6g} q^(2m)={q ** (2 * m):.6g} relerr={rel:.4f}")


def v5_ratio():
    rng = np.random.default_rng(555)
    p, k, m = 101, 10, 32
    q = 1 - k / p
    gm = sample_gm(p, k, m, 200000, rng)
    ratio = gm / q ** (2 * m)
    check("V5 asymptotic ratio g_m/q^(2m) close to 1 at small C",
          0.75 < ratio < 1.25,
          f"(p=101,k=10,m=32,C=m/sqrt(p)={m / np.sqrt(p):.2f}) "
          f"ratio={ratio:.4f} (theory: 1+O(C^2/p))")


def v4_regime():
    import math
    for p in (997, 10007):
        kk = math.isqrt(p)
        m = round(100 * math.sqrt(p))
        mu = p * (1 - 1 / math.sqrt(p)) ** m
        check(f"V4 regime mu(p={p}) < 1e-38", mu < 1e-38,
              f"k={kk} m={m} mu={mu:.3e}")
        print(f"     mu(p={p}, m=round(100*sqrt(p))={m}) = {mu:.6e}")


if __name__ == "__main__":
    v1_symbolic()
    v2_enumeration()
    v3_mc()
    v5_ratio()
    v4_regime()
    print("VERIFY_THEORY:", "ALL PASSED" if not FAIL else "FAILURES PRESENT")
    sys.exit(1 if FAIL else 0)
