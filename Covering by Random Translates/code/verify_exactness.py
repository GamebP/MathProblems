#!/usr/bin/env python3
"""GREEN-081 -- exactness verification (mechanics-level ground truth).

(i) Bitset-vs-set mechanics: for p in [7, 13, 101], k=floor(sqrt(p)), 20
    seeded trials each: sequential numpy boolean-array coverage of a fixed
    translate sequence is compared against pure-Python set unions
    {(a+t) % p for a in A}; covered index sets must be IDENTICAL.
(ii) FFT-vs-brute-force greedy scoring: p=101, 20 trials, first 3 greedy
    steps each: round(Re(IFFT(FFT(u)*conj(FFT(1_A))))) compared elementwise
    to the O(p*k) recount brute(t) = sum_{a in A} u[(a+t) % p]; argmax and
    full score vector must coincide, max rounding error < 1e-6.

Verification-only seed streams (documented): SeedSequence(777).spawn for (i);
default_rng(888) for (ii). Prints PASS/FAIL lines plus the head of every CSV
produced by Scripts 1-2; exits nonzero on any failure.
"""

import csv
import math
import os

import numpy as np

BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
DATA = os.path.join(BASE, "data")
FAILURES = []


def check(name, cond, detail=""):
    print(f"{'PASS' if cond else 'FAIL'}: {name}" + (f" -- {detail}" if detail else ""))
    if not cond:
        FAILURES.append(name)


def part_i():
    for j, p in enumerate([7, 13, 101]):
        k = math.isqrt(p)
        rng = np.random.default_rng(np.random.SeedSequence(777).spawn(3)[j])
        T = int(math.ceil(math.sqrt(p) * (math.log(p) + 5.0)))
        ok = True
        bad = -1
        for trial in range(20):
            A = rng.choice(p, size=k, replace=False).astype(np.int64)
            seq = rng.integers(0, p, size=T)
            cov = np.zeros(p, dtype=bool)
            for t in seq:
                cov[(A + t) % p] = True
            s = set()
            for t in seq:
                s |= {(int(a) + int(t)) % p for a in A}
            np_idx = np.flatnonzero(cov)
            py_idx = np.array(sorted(s), dtype=np.int64)
            if not (np_idx.shape == py_idx.shape and np.array_equal(np_idx, py_idx)):
                ok = False
                bad = trial
                break
        check(f"(i) bitset == pure-Python set unions, p={p}, 20 trials",
              ok, f"{T} translates/trial" + ("" if ok else f", first mismatch trial={bad}"))


def part_ii():
    p, k = 101, math.isqrt(101)
    rng = np.random.default_rng(888)
    ok_val = True
    ok_arg = True
    max_err = 0.0
    for _ in range(20):
        A = rng.choice(p, size=k, replace=False).astype(np.int64)
        apad = np.zeros(p)
        apad[A] = 1.0
        fA = np.conj(np.fft.fft(apad))
        u = np.ones(p)
        u[A] = 0.0
        for _step in range(3):
            sc = np.fft.ifft(np.fft.fft(u) * fA).real
            brute = np.zeros(p)
            for a in A:
                brute += np.roll(u, -int(a))
            max_err = max(max_err, float(np.max(np.abs(sc - np.round(sc)))))
            # Decisions use the ROUNDED integer scores; raw-float argmax can
            # differ between summation orders on exact ties (~1e-14 noise),
            # so tie-break consistency is asserted on the integer vectors.
            sc_i = np.rint(sc)
            br_i = np.rint(brute)
            if not np.array_equal(sc_i, br_i):
                ok_val = False
            if int(np.argmax(sc_i)) != int(np.argmax(br_i)):
                ok_arg = False
            t = int(np.argmax(sc_i))
            u[(A + t) % p] = 0.0
    check("(ii) FFT greedy score == brute-force O(p*k) count, p=101, "
          "first 3 steps x 20 trials",
          ok_val and ok_arg and max_err < 1e-6,
          f"max_rounding_err={max_err:.2e}, argmax_match={ok_arg}")


def csv_head(name, nrows=5):
    print(f"--- head({name}) ---")
    path = os.path.join(DATA, name)
    if not os.path.exists(path):
        print("MISSING (run the sim scripts first)")
        return
    with open(path) as f:
        for i, line in enumerate(f):
            if i > nrows:
                break
            print(line.rstrip())


def main():
    part_i()
    part_ii()
    for nm in ("random_translates_threshold.csv", "gumbel_window.csv",
               "uncovered_counts.csv", "regime_100sqrtp.csv", "greedy_cover.csv"):
        csv_head(nm)
    csv_head("greedy_curve_p20011.csv", nrows=4)
    if FAILURES:
        raise SystemExit(f"VERIFICATION FAILED: {FAILURES}")
    print("ALL VERIFICATION CHECKS PASSED")


if __name__ == "__main__":
    main()
