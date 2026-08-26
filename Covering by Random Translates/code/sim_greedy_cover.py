#!/usr/bin/env python3
r"""GREEN-081 -- Reading-B experiment (Script 2): greedy chosen translates.

Greedy set cover of Z_p by translates of a uniform random k-subset,
k = floor(sqrt(p)): at each step pick t maximizing |(A+t) \cap uncovered|;
g(A) = number of steps until full cover.

Scoring is EXACT-INTEGER via FFT:
    score(t) = Re(IFFT(FFT(u) * conj(FFT(1_A))))  with u = uncovered indicator,
mathematically equal to sum_{a in A} u[(a+t) mod p]. Every step asserts
max |score - round(score)| < 1e-6; the rounded integer scores drive all
decisions. Uncovered bookkeeping via count_nonzero on an exact 0/1 array --
no floating-point thresholds anywhere.

Reproducibility: single stream numpy.random.default_rng(12345), consumed in
the fixed prime order below; the FIRST trial at p=20011 additionally records
its covered-fraction curve.

Outputs in ../data:
  greedy_cover.csv         per-prime statistics of g(A)
  greedy_curve_p20011.csv  step, covered_frac for one representative trial
"""

import csv
import math
import os

import numpy as np

SPEC = [(101, 200), (199, 150), (401, 100), (599, 80), (797, 80), (997, 60),
        (1999, 40), (4003, 25), (5003, 25), (10007, 12), (20011, 8)]
BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
DATA = os.path.join(BASE, "data")


def greedy_once(rng, p, k, want_curve=False):
    A = np.argsort(rng.random(p))[:k].astype(np.int64)
    apad = np.zeros(p, dtype=np.float64)
    apad[A] = 1.0
    fA = np.conj(np.fft.fft(apad))
    u = np.ones(p, dtype=np.float64)
    u[A] = 0.0
    covered = 0
    steps = 0
    curve = []
    while covered < p:
        scores = np.fft.ifft(np.fft.fft(u) * fA).real
        err = float(np.max(np.abs(scores - np.round(scores))))
        assert err < 1e-6, f"non-integral FFT score (err={err:g}, p={p})"
        t = int(np.argmax(scores))
        u[(A + t) % p] = 0.0
        covered = p - int(np.count_nonzero(u))
        steps += 1
        if want_curve:
            curve.append(covered / p)
    return steps, curve


def f6(x):
    return f"{x:.6f}"


def main():
    os.makedirs(DATA, exist_ok=True)
    rng = np.random.default_rng(12345)
    rows = []
    curve_rows = None
    for p, n in SPEC:
        k = math.isqrt(p)
        gs = []
        for i in range(n):
            g, curve = greedy_once(rng, p, k, want_curve=(p == 20011 and i == 0))
            gs.append(g)
            if curve:
                curve_rows = [(j + 1, f6(cf)) for j, cf in enumerate(curve)]
        arr = np.asarray(gs, dtype=np.int64)
        s = math.sqrt(p)
        L = math.log(p)
        denom = s * L
        gm = float(arr.mean())
        lovasz = (p / k) * (1.0 + math.log(k))
        rows.append([p, k, n, f6(gm), int(np.median(arr)), f6(float(arr.std())),
                     int(arr.min()), int(arr.max()), f6(gm / denom),
                     f6(gm / (0.5 * denom)), f6(gm / s), f6(lovasz), f6(denom)])
        print(f"[greedy] p={p:6d} n={n:3d} g_mean={gm:8.2f} med={int(np.median(arr)):5d} "
              f"g/(sqrtp*lnp)={gm / denom:.4f} g/(half)={gm / (0.5 * denom):.4f} "
              f"g/sqrtp={gm / s:.4f} min={arr.min()} max={arr.max()}")
    with open(os.path.join(DATA, "greedy_cover.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["p", "k", "trials", "g_mean", "g_median", "g_std", "g_min",
                    "g_max", "ratio_over_sqrtp_lnp", "ratio_over_half_sqrtp_lnp",
                    "ratio_over_sqrtp", "theory_lovasz_stein", "sqrtp_lnp"])
        w.writerows(rows)
    if curve_rows is not None:
        with open(os.path.join(DATA, "greedy_curve_p20011.csv"), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["step", "covered_frac"])
            w.writerows(curve_rows)
    print("Script 2 complete.")


if __name__ == "__main__":
    main()
