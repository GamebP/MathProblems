#!/usr/bin/env python3
"""
GREEN-036 ("Multiplicatively Closed Set Density", Ben Green open problem #36).

Exact computational study of
    A = smallest subset of Z_{>0} containing 2, 3 and closed under
        (a1, a2) |-> a1*a2 - 1.

This script is self-contained (Python standard library only) and performs:

  1. exact generation of A cap [1, X] by increasing-order DP
     (correctness proof in report.tex / notes.md; independently cross-checked
      here against a naive round-based closure at a smaller bound),
  2. Lemma A check (no element of A is 1 mod 3),
  3. Lemma B explicit lower-bound families (P-orbit, pairwise Z-products,
     mixed U x V products) with membership/injectivity checks,
  4. residue census S_m = minimal closed subset of Z/m containing {2, 3}
     for all primes p <= 500 and all composite moduli m <= 500,
  5. growth analysis: per-decade counts, local exponents, log-log OLS fit,
     truncated zeta equation sum_{b in A} b^{-(1+alpha)} = 1 (with and
     without power-law tail correction), truncated harmonic sums,
  6. artifacts: data/census_summary.json, data/census.csv.gz.

Usage:  python3 verify_solution.py [X]       (default X = 10**7)
"""

import gzip
import heapq
import json
import math
import sys
import time
from bisect import insort
from itertools import compress
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
LOG_BUCKETS_PER_DECADE = 64
SMALL_EXACT_LIMIT = 200_000      # exact zeta/harmonic contributions below this
NAIVE_CHECK_X = 3_000            # independent naive-closure cross-check bound


# ----------------------------------------------------------------------
# 1. Exact census of A cap [1, X]
# ----------------------------------------------------------------------
def generate_A(X):
    """Increasing-order DP.

    Invariant (proved in the report): when m is popped, every element of
    A cap [1, m] is already discovered, and every element a of A used in a
    generating pair (m, a) with m*a-1 <= X satisfies
        a <= min(m, X // m) <= sqrt(X),
    so iterating partners over the sorted list `small` of A cap [1, sqrt X]
    is complete.  Every pushed value exceeds the currently popped value,
    hence heap pops occur in strictly increasing order.
    """
    if X < 3:
        raise ValueError("X must be >= 3")
    S = int(math.isqrt(X))
    member = bytearray(X + 1)
    member[2] = member[3] = 1
    small = [2, 3]                    # sorted list of A cap [1, sqrt(X)]
    heap = [2, 3]
    while heap:
        m = heapq.heappop(heap)
        if m > X:
            break
        lim = min(m, X // m)
        for a in small:
            if a > lim:
                break
            n = m * a - 1
            if not member[n]:
                member[n] = 1
                if n <= S:
                    insort(small, n)
                heapq.heappush(heap, n)
    return member


def naive_closure(X):
    """Independent brute-force closure: iterate S <- S u {ab-1 <= X} to fixpoint."""
    S = {2, 3}
    while True:
        new = {a * b - 1 for a in S for b in S if 3 <= a * b - 1 <= X}
        if new <= S:
            return S
        S |= new


# ----------------------------------------------------------------------
# 2. Residue census
# ----------------------------------------------------------------------
def closed_residue_set(m):
    """Minimal subset of Z/m containing residues 2, 3, closed under rs-1."""
    S = {2 % m, 3 % m}
    while True:
        new = {(r * s - 1) % m for r in S for s in S}
        if new <= S:
            return S
        S |= new


def primes_below(n):
    sieve = bytearray([1]) * n
    sieve[0:2] = b"\x00\x00"
    for i in range(2, math.isqrt(n) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
    return [i for i in range(n) if sieve[i]]


# ----------------------------------------------------------------------
# 3. Growth statistics helpers
# ----------------------------------------------------------------------
def bucket_index(b):
    return int(LOG_BUCKETS_PER_DECADE * math.log10(b))


def analyze_density(member, X, F):
    """Single compressed pass over census elements:
    returns (small_exact_list, bucket_counts, bucket_log_midpoints,
             per_decade_harmonic_increments, decade_cumulative_counts)."""
    K = int(math.log10(X))
    n_buck = LOG_BUCKETS_PER_DECADE * (K + 1)
    bcount = [0] * n_buck
    lmid = [math.log(10.0 ** ((j + 0.5) / LOG_BUCKETS_PER_DECADE))
            for j in range(n_buck)]
    dharm = [0.0] * K                      # harmonic mass of (10^(k-1), 10^k]
    small = []
    els = compress(range(2, X + 1), memoryview(member)[2:X + 1])
    for b in els:
        if b <= SMALL_EXACT_LIMIT:
            small.append(b)                # handled exactly in zeta
        else:
            bcount[bucket_index(b)] += 1   # bucket approx for zeta tail
        dharm[int(math.log10(b))] += 1.0 / b
    decade_cum = [member.count(1, 2, min(10 ** k, X + 1)) for k in range(1, K + 1)]
    return small, bcount, lmid, dharm, decade_cum


def zeta_trunc(alpha, small, bcount, lmid):
    s = math.fsum(b ** (-1.0 - alpha) for b in small)
    t = 0.0
    for j, c in enumerate(bcount):
        if c:
            t += c * math.exp(-(1.0 + alpha) * lmid[j])
    return s + t


def solve_zeta(small, bcount, lmid, lo=1e-3, hi=3.0):
    """Solve sum_{b in A cap [1,X]} b^{-(1+alpha)} = 1 by bisection."""
    flo, fhi = zeta_trunc(lo, small, bcount, lmid) - 1.0, \
               zeta_trunc(hi, small, bcount, lmid) - 1.0
    if flo < 0 or fhi > 0:
        return None, flo, fhi
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        fm = zeta_trunc(mid, small, bcount, lmid) - 1.0
        if fm > 0:
            lo, flo = mid, fm
        else:
            hi, fhi = mid, fm
        if hi - lo < 1e-10:
            break
    return 0.5 * (lo + hi), flo, fhi


def ols_slope(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    beta = sxy / sxx
    alpha0 = my - beta * mx
    ss_res = sum((y - (alpha0 + beta * x)) ** 2 for x, y in zip(xs, ys))
    ss_tot = sum((y - my) ** 2 for y in ys)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return beta, alpha0, r2


# ----------------------------------------------------------------------
# main
# ----------------------------------------------------------------------
def main():
    X = int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 7
    T = {}
    results = {"X": X}
    print(f"GREEN-036 verification run, X = {X}")
    print("=" * 72)

    # -- 1. exact census -------------------------------------------------
    t0 = time.time()
    member = generate_A(X)
    F = member.count(1, 2, X + 1)
    T["census_dp"] = round(time.time() - t0, 2)
    print(f"[1] exact census DP: |A cap [1,{X}]| = {F}   ({T['census_dp']}s)")
    results["F_X"] = F

    # -- 2. independent exactness cross-check ----------------------------
    t0 = time.time()
    Xn = min(NAIVE_CHECK_X, X)
    dp_small = {i for i in range(2, Xn + 1) if member[i]}
    nv = naive_closure(Xn)
    exact_match = dp_small == nv
    T["naive_crosscheck"] = round(time.time() - t0, 2)
    print(f"[2] naive closure cross-check at X={Xn}: "
          f"DP |A|={len(dp_small)}, naive |A|={len(nv)}, identical={exact_match}"
          f"   ({T['naive_crosscheck']}s)")
    results["naive_check"] = {"X": Xn, "dp_size": len(dp_small),
                              "naive_size": len(nv), "identical": exact_match}

    # -- 3. Lemma A -------------------------------------------------------
    viol = sum(1 for i in range(3, X + 1) if member[i] and i % 3 == 1)
    print(f"[3] Lemma A: elements congruent to 1 (mod 3) in census: {viol} "
          f"(out of {F}); predicted 0")
    results["lemmaA_violations"] = viol
    results["observed_density"] = F / X
    print(f"    observed raw density F({X})/{X} = {F / X:.6f}  "
          f"(proven upper bound 2/3 = {2 / 3:.6f})")

    # -- 4. decade table ---------------------------------------------------
    K = int(math.log10(X))
    decade_cum = analyze_and_counts = None
    t0 = time.time()
    small, bcount, lmid, dharm, decade_cum = analyze_density(member, X, F)
    T["density_pass"] = round(time.time() - t0, 2)
    print(f"[4] count table |A cap [1,10^k]| and per-decade increments "
          f"({T['density_pass']}s):")
    print("      k   F(10^k)      increment   F/N       local exp  harm incr  delta_hat")
    prev = 0
    dec_incr = []
    loc_exp = []
    for k in range(1, K + 1):
        c = decade_cum[k - 1]
        inc = c - prev
        le = math.log(c / prev, 10) if prev > 0 else float("nan")
        hi = dharm[k - 1]
        dh = hi / math.log(10)
        dec_incr.append(hi)
        if prev > 0:
            loc_exp.append(le)
        print(f"     {k:2d}  {c:11d}  {inc:10d}   {c / 10 ** k:.6f}  "
              f"{le:8.4f}  {hi:8.4f}  {dh:.4f}")
        prev = c
    results["decade_cumulative"] = decade_cum
    results["decade_harmonic_increments"] = dec_incr
    results["local_exponents"] = loc_exp

    # -- 5. Lemma B families ----------------------------------------------
    print("[5] Lemma B lower-bound families:")
    t0 = time.time()
    kmax = int(math.log(X, 2))
    P = [2 ** k + 1 for k in range(1, kmax + 1)]          # orbit of 3 under x->2x-1
    p_ok = all(member[p] for p in P if p <= X)
    print(f"    P-orbit 2^k+1, k=1..{min(kmax, int(math.log2(X)))}: "
          f"{sum(1 for p in P if p <= X)} values, all in A: {p_ok}")

    # pairwise Z-products (P x P), PROVEN distinct by 2-adic cascade
    z_vals = []
    z_coll = 0
    for ii in range(len(P)):
        ui = P[ii]
        if 2 * ui - 1 > X:
            break
        for jj in range(ii, len(P)):
            w = ui * P[jj] - 1
            if w > X:
                break
            z_vals.append(w)
    z_in = sum(1 for w in z_vals if member[w])
    z_coll = len(z_vals) - len(set(z_vals))
    lam = int(math.log(X, 2))
    prov_count = ((lam - 1) ** 2) // 4
    print(f"    Z-products (2^i+1)(2^j+1)-1 <= X (i<=j): generated {len(z_vals)}, "
          f"in A: {z_in}, collisions: {z_coll}")
    print(f"    proven counting formula floor((floor(log2 X)-1)^2/4) = {prov_count} "
          f"(<= actual {len(z_vals)})")
    lb_frac = len(z_vals) / F
    print(f"    lower bound achieved: {len(z_vals)} = {lb_frac:.6g} x F({X})")

    # mixed U x V products, V = orbit of 2 under x -> 3x-1 (injectivity COMPUTED)
    V = []
    v = 2
    while v <= 2 * X:
        V.append(v)
        v = 3 * v - 1                     # v_{j+1} = 3 v_j - 1, v_1 = 2
    U = P
    m_vals = []
    for ui in U:
        if 2 * ui - 1 > X:
            break
        for vj in V:
            w = ui * vj - 1
            if w > X:
                break
            m_vals.append(w)
    m_in = sum(1 for w in m_vals if member[w])
    m_coll = len(m_vals) - len(set(m_vals))
    c_pure2 = 1.0 / (4 * math.log(2) ** 2)
    c_mixed = 1.0 / (2 * math.log(2) * math.log(3))
    print(f"    mixed (2^i+1)((3^j+1)/2)-1 <= X: generated {len(m_vals)}, "
          f"in A: {m_in}, collisions: {m_coll}")
    print(f"    asymptotic constants: pure-2 (PROVEN) 1/(4 ln^2 2) = {c_pure2:.5f}, "
          f"mixed (if injective) 1/(2 ln2 ln3) = {c_mixed:.5f}")
    print(f"    ({time.time() - t0:.2f}s)")
    results["lemmaB"] = {
        "porbit_count": sum(1 for p in P if p <= X), "porbit_all_in_A": bool(p_ok),
        "z_generated": len(z_vals), "z_in_A": z_in, "z_collisions": z_coll,
        "z_proven_formula": prov_count,
        "mixed_generated": len(m_vals), "mixed_in_A": m_in,
        "mixed_collisions": m_coll,
        "const_pure2": c_pure2, "const_mixed": c_mixed,
    }

    # -- 6. residue census --------------------------------------------------
    t0 = time.time()
    pr = primes_below(500)
    Sp = {}
    proper_primes = []
    for p in pr:
        s = closed_residue_set(p)
        Sp[p] = sorted(s)
        if len(s) < p:
            proper_primes.append((p, len(s)))
    comp_proper = []
    for m in range(4, 501):
        s = closed_residue_set(m)
        if len(s) / m < 2.0 / 3.0 - 1e-12:
            comp_proper.append((m, len(s)))
    combined = 1.0
    for p, sz in proper_primes:
        combined *= sz / p
    best_single = min((sz / p for p, sz in proper_primes), default=1.0)
    T["residues"] = round(time.time() - t0, 2)
    print(f"[6] residue census, {len(pr)} primes <= 500 ({T['residues']}s):")
    print(f"    primes with PROPER S_p: {proper_primes or 'none'}")
    print(f"    composite moduli 4..500 beating 2/3: {comp_proper or 'none'}")
    print(f"    S_3 = {sorted(closed_residue_set(3))} (Lemma A), "
          f"|S_p| = p for all other primes p <= 500: "
          f"{all(len(Sp[p]) == p for p in pr if p != 3)}")
    print(f"    combined CRT bound over proper prime constraints: {combined:.6f} "
          f"(= proven 2/3 here); best single {best_single:.6f}")
    results["residues"] = {
        "primes_le_500": {p: len(Sp[p]) for p in pr},
        "proper_primes": proper_primes,
        "composite_beating_2_3": comp_proper,
        "combined_bound": combined,
        "S_3": sorted(closed_residue_set(3)),
    }

    # -- 7. growth exponent estimation ---------------------------------------
    print("[7] growth-exponent estimates:")
    ks = list(range(4, K + 1))
    xs = [math.log(10 ** k) for k in ks]
    ys = [math.log(decade_cum[k - 1]) for k in ks]
    beta, a0, r2 = ols_slope(xs, ys)
    print(f"    OLS log-log fit over k=4..{K}: alpha_hat = {beta:.5f} "
          f"(R^2 = {r2:.6f})")
    print(f"    top local exponent ln(F_{K}/F_{K-1})/ln 10 = {loc_exp[-1]:.5f}")
    H = math.fsum(dharm)
    print(f"    truncated harmonic sum H_X = sum_(b in A cap [1,{X}]) 1/b = {H:.6f}")
    alphas = [0.0, 0.25, 0.5, 0.75, 1.0]
    zgrid = {round(a, 2): zeta_trunc(a, small, bcount, lmid) for a in alphas}
    print("    truncated zeta grid: " +
          ", ".join(f"S({a})={v:.4f}" for a, v in zgrid.items()))
    astar, flo, fhi = solve_zeta(small, bcount, lmid)
    astar_corr = None
    tail_note = ""
    if astar is not None:
        res_at = zeta_trunc(astar, small, bcount, lmid)
        print(f"    solved S_X(alpha*) = 1: alpha*_trunc = {astar:.6f} "
          f"(residual {res_at - 1.0:+.2e})")
        # power-law tail correction  sum_{b>X} b^{-(1+a)} ~= c*a_loc*X^{a_loc-1-a}/(a+1-a_loc)
        a_loc = loc_exp[-1]
        c_fit = decade_cum[-2] / (10 ** (K - 1)) ** a_loc
        def g(a):
            return zeta_trunc(a, small, bcount, lmid) + \
                   c_fit * a_loc * X ** (a_loc - 1 - a) / (a + 1 - a_loc) - 1.0
        lo, hi = 1e-3, 3.0
        if g(lo) > 0 > g(hi):
            for _ in range(80):
                mid = 0.5 * (lo + hi)
                if g(mid) > 0:
                    lo = mid
                else:
                    hi = mid
                if hi - lo < 1e-10:
                    break
            astar_corr = 0.5 * (lo + hi)
            print(f"    tail-corrected (power-law c={c_fit:.4g}, a_loc={a_loc:.4f}): "
                  f"alpha*_corr = {astar_corr:.6f}")
    else:
        tail_note = "sign condition failed; no alpha*>0 from truncated equation"
        print(f"    truncated zeta equation has no root in [1e-3, 3]: {tail_note}")
    mf_pred = None
    if astar is not None:
        mf_pred = X ** astar
        print(f"    mean-field prediction F({X}) ~ X^alpha* = {mf_pred:.4g} "
              f"vs actual {F}  (ratio {F / mf_pred:.4g})")
    results["growth"] = {
        "alpha_ols": beta, "ols_R2": r2, "alpha_top_local": loc_exp[-1],
        "harmonic_trunc": H, "zeta_grid": zgrid,
        "alpha_star_trunc": astar, "alpha_star_corrected": astar_corr,
        "meanfield_prediction": mf_pred,
    }

    # -- 8. artifacts ----------------------------------------------------------
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    summary = {
        "problem": "GREEN-036 multiplicatively closed set density",
        "X": X, "F_X": F, "timings_s": T,
        **results,
    }
    jp = DATA_DIR / "census_summary.json"
    jp.write_text(json.dumps(summary, indent=2, default=str))
    csv_path = DATA_DIR / "census.csv.gz"
    cap = 1_000_000
    with gzip.open(csv_path, "wt", compresslevel=6) as fh:
        fh.write("n\n")
        w = 0
        for b in compress(range(2, X + 1), memoryview(member)[2:X + 1]):
            fh.write(f"{b}\n")
            w += 1
            if w >= cap:
                break
    T["artifacts"] = round(time.time() - t0, 2)
    print(f"[8] artifacts written in {T['artifacts']}s: {jp.name}, "
          f"census.csv.gz (first {min(cap, F)} elements)"
          f" sizes: {jp.stat().st_size}B, {csv_path.stat().st_size}B")

    # -- 9. PASS/FAIL block ------------------------------------------------------
    print("=" * 72)
    chk = []
    chk.append(("EXACTNESS",
                exact_match,
                f"DP set == naive fixpoint closure on [1,{Xn}] "
                f"(|A| = {len(dp_small)} both sides: {exact_match})"))
    chk.append(("LEMMA-A",
                viol == 0,
                f"{viol} violations of n ≡ 1 (mod 3) among {F} census elements"))
    chk.append(("PORBIT",
                p_ok,
                f"all {results['lemmaB']['porbit_count']} values 2^k+1 <= X lie in A"))
    chk.append(("LEMMA-B-Z",
                z_in == len(z_vals) and z_coll == 0 and prov_count <= len(z_vals),
                f"{z_in}/{len(z_vals)} Z-products in A, {z_coll} collisions, "
                f"proven formula {prov_count} <= actual"))
    chk.append(("LEMMA-B-MIXED",
                m_in == len(m_vals) and m_coll == 0,
                f"{m_in}/{len(m_vals)} mixed products in A, {m_coll} collisions "
                "(injectivity COMPUTED, not proven)"))
    chk.append(("RESIDUES",
                sorted(closed_residue_set(3)) == [0, 2] and len(proper_primes) >= 1
                and combined >= F / X - 1e-9,
                f"S_3 = {{0,2}}; proper-prime list {proper_primes}; combined bound "
                f"{combined:.6f} >= observed density {F / X:.6f}"))
    chk.append(("MONOTONE",
                all(decade_cum[i] < decade_cum[i + 1] for i in range(K - 1)),
                f"decade counts strictly increasing, e.g. {decade_cum[0]} -> "
                f"{decade_cum[-1]}"))
    chk.append(("ZETA-ROOT",
                astar is not None and abs(zeta_trunc(astar, small, bcount, lmid) - 1.0) < 1e-6,
                (f"S_X(alpha*) = 1 at alpha* = {astar:.6f}, residual "
                 f"{zeta_trunc(astar, small, bcount, lmid) - 1.0:+.2e}")
                if astar is not None else tail_note))
    chk.append(("DENSITY-TREND",
                decade_cum[-1] / 10 ** K > decade_cum[-2] / 10 ** (K - 1),
                f"F/N still rising: {decade_cum[-2] / 10 ** (K - 1):.4f} -> "
                f"{decade_cum[-1] / 10 ** K:.4f} (question OPEN)"))
    width = max(len(n) for n, _, _ in chk)
    npass = 0
    for name, ok, msg in chk:
        tag = "PASS" if ok else "FAIL"
        npass += ok
        print(f"[{tag}] {name:<{width}}  {msg}")
    print("-" * 72)
    print(f"{npass}/{len(chk)} checks passed.  Problem GREEN-036 remains OPEN; "
          "this run establishes computational evidence only.")
    return 0 if npass == len(chk) else 1


if __name__ == "__main__":
    sys.exit(main())
