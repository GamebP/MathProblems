#!/usr/bin/env python3
"""GREEN-081 -- Covering by Random Translates (Script 1).

Model: A uniform random k-subset of Z_p with k = floor(sqrt(p)); translates
t_1, t_2, ... i.i.d. uniform on Z_p; exact boolean covered[] array updated by
numpy fancy indexing cov[(A+t) % p] = True. m* = first m with all p points
covered; cap = ceil(sqrt(p)*(ln p + 7)); if uncovered at cap record m* = cap
and flag = 1 (theory: P(flag) ~ e^{-e^7}). All coverage decisions are exact
(boolean arrays / integer counts); no floating-point thresholds.

Reproducibility: master numpy.random.SeedSequence(12345); child streams
spawned per part: part A (threshold + Gumbel window) <- spawn(0),
part C (uncovered counts) <- spawn(1), part D (regime) <- spawn(2).

Outputs in ../data (relative to this file):
  random_translates_threshold.csv   (a)
  gumbel_window.csv                 (b)
  uncovered_counts.csv              (c)
  regime_100sqrtp.csv               (d)
"""

import csv
import math
import os

import numpy as np

PRIMES = [101, 199, 401, 599, 797, 997, 1999, 4003, 5003, 10007, 20011]
BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
DATA = os.path.join(BASE, "data")


def trials_for(p):
    return 400 if p <= 1100 else (150 if p <= 5100 else 50)


def subset_matrix(rng, p, k, n):
    """n independent uniform k-subsets of Z_p (argsort of i.i.d. uniform keys)."""
    return np.argsort(rng.random((n, p)), axis=1)[:, :k].astype(np.int64)


def write_csv(name, header, rows):
    path = os.path.join(DATA, name)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def f6(x):
    return f"{x:.6f}"


def part_a(ss):
    rng = np.random.default_rng(ss.spawn(1)[0])
    thr, gum = [], []
    cs = (-3, -2, -1, 0, 1, 2, 3)
    for p in PRIMES:
        k = math.isqrt(p)
        n = trials_for(p)
        s = math.sqrt(p)
        L = math.log(p)
        cap = math.ceil(s * (L + 7.0))
        A = subset_matrix(rng, p, k, n)
        cov = np.zeros((n, p), dtype=bool)
        mstar = np.full(n, cap, dtype=np.int64)
        done = np.zeros(n, dtype=bool)
        for m in range(1, cap + 1):
            t = rng.integers(0, p, size=n)
            idx = (A + t[:, None]) % p
            np.put_along_axis(cov, idx, True, axis=1)
            full = cov.all(axis=1)
            mstar[full & ~done] = m
            done = full
            if done.all():
                break
        flags = int((~done).sum())
        mm = float(mstar.mean())
        denom = s * L
        thr.append([p, k, n, f6(mm), f6(float(mstar.std())),
                    int(np.median(mstar)), int(mstar.min()), int(mstar.max()),
                    flags, f6(mm / denom), f6(denom), f6(s)])
        freqs = {}
        for c in cs:
            thc = math.ceil(s * (L + c))          # exact integer threshold
            fr = float((mstar <= thc).mean())     # exact boolean comparison
            freqs[c] = fr
            gum.append([p, c, n, f6(fr), f6(math.exp(-math.exp(-c))),
                        f6(math.exp(-math.exp(-c)))])
        print(f"[A] p={p:6d} n={n:3d} cap={cap} m_mean={mm:9.2f} "
              f"m_med={int(np.median(mstar)):5d} ratio={mm / denom:.4f} flags={flags}")
        print(f"     freq c=-3..3 = [{', '.join(f6(freqs[c]) for c in cs)}]")
    write_csv("random_translates_threshold.csv",
              ["p", "k", "trials", "m_mean", "m_std", "m_median", "m_min",
               "m_max", "flag_count", "ratio_mean_over_sqrtp_lnp",
               "theory_sqrtp_lnp", "sqrtp"], thr)
    write_csv("gumbel_window.csv",
              ["p", "c", "n_trials", "freq_success", "pred_gumbel",
               "pred_poisson_zero"], gum)


def uncover_at_budget(rng, p, k, mc, n):
    """Exact integer uncovered counts X after exactly mc translates, n trials."""
    A = subset_matrix(rng, p, k, n)
    cov = np.zeros((n, p), dtype=bool)
    for _ in range(mc):
        t = rng.integers(0, p, size=n)
        idx = (A + t[:, None]) % p
        np.put_along_axis(cov, idx, True, axis=1)
    return p - cov.sum(axis=1, dtype=np.int64)


def part_c(ss):
    rng = np.random.default_rng(ss.spawn(1)[0])
    rows = []
    for p in PRIMES:
        k = math.isqrt(p)
        s = math.sqrt(p)
        L = math.log(p)
        parts = []
        for c in (0, 1, 2):
            mc = int(round(s * (L + c)))
            X = uncover_at_budget(rng, p, k, mc, 300)
            mean_x = float(X.mean())
            f0 = float((X == 0).mean())
            rows.append([p, c, mc, f6(mean_x), f6(float(X.var())), f6(f0),
                         f6(math.exp(-c)), f6(math.exp(-math.exp(-c)))])
            parts.append(f"c={c}: meanX={mean_x:.3f}(e^-c={math.exp(-c):.3f}) "
                         f"fX0={f0:.3f}(exp(-e^-c)={math.exp(-math.exp(-c)):.3f})")
        print(f"[C] p={p:6d} " + " | ".join(parts))
    write_csv("uncovered_counts.csv",
              ["p", "c", "m_used", "mean_X", "var_X", "freq_X_eq_0",
               "pred_mean_exp_neg_c", "pred_gumbel"], rows)


def part_d(ss):
    rng = np.random.default_rng(ss.spawn(1)[0])
    rows = []
    for p in (997, 10007):
        k = math.isqrt(p)
        s = math.sqrt(p)
        mc = int(round(100.0 * s))
        X = uncover_at_budget(rng, p, k, mc, 100)
        mu = p * math.exp(mc * math.log1p(-1.0 / s))
        rows.append([p, mc, 100, int(X.max()), f"{mu:.6e}"])
        print(f"[D] p={p} m={mc} trials=100 max_X_observed={int(X.max())} "
              f"theory_mu={mu:.6e}")
    write_csv("regime_100sqrtp.csv",
              ["p", "m_used", "trials", "max_X_observed", "theory_mu"], rows)


def main():
    os.makedirs(DATA, exist_ok=True)
    ss = np.random.SeedSequence(12345)
    part_a(ss)
    part_c(ss)
    part_d(ss)
    print("Script 1 complete.")


if __name__ == "__main__":
    main()
