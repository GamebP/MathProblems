#!/usr/bin/env python3
"""Numerical probe: does M(d) for d(s)=e_p(s^3) decay or plateau as p grows past 7?

M(d) = sup over unimodular a,b,c of |E_{x,y in F_p} d(x-y) conj(a(x)) conj(b(y)) conj(c(x+y))|

Method: identical alternating phase-maximization to verify_solution.py CHECK 6
(update a, then b, then c, each to the phase of its optimal slice average;
iterate until max coordinate change < 1e-13 or max_sweeps), retuned for runtime:
p in {11,13,17}, restarts 300 (p<=13) / 120 (p=17), max_sweeps 250.
Control target: uniformly random exponents, same restart budget.

NOTE: this probe EXTENDS (not replaces) the deterministic CHECK 6 experiment
(data/experiment_p5_n1.txt, data/experiment_p7_n1.txt).
"""
import cmath
import math
import os
import random
import sys
import time

WORKDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(WORKDIR, "data", "probe_large_p.txt")
SEED = 20260826
MAX_SWEEPS = 250
TOL = 1e-13
PLAN = ((11, 300), (13, 300), (17, 120))


def build_trips(p):
    """Index schedules independent of a,b,c: (free-var, d-index, other-index)."""
    trip_a = [[(y, (x - y) % p, (x + y) % p) for y in range(p)] for x in range(p)]
    trip_b = [[(x, (x - y) % p, (x + y) % p) for x in range(p)] for y in range(p)]
    trip_c = [[(x, (s - x) % p, (2 * x - s) % p) for x in range(p)] for s in range(p)]
    return trip_a, trip_b, trip_c


def alt_optimize(dex, p, rng, trips, max_sweeps=MAX_SWEEPS):
    om = cmath.exp(2j * math.pi / p)
    d = [om ** (k % p) for k in dex]
    a = [om ** rng.randrange(p) for _ in range(p)]
    b = [om ** rng.randrange(p) for _ in range(p)]
    c = [om ** rng.randrange(p) for _ in range(p)]
    trip_a, trip_b, trip_c = trips
    sweeps_used = 0
    for it in range(max_sweeps):
        olda, oldb, oldc = a[:], b[:], c[:]
        cb = [v.conjugate() for v in b]
        cc = [v.conjugate() for v in c]
        for x in range(p):
            acc = 0j
            for i, di, ci in trip_a[x]:
                acc += d[di] * cb[i] * cc[ci]
            mag = abs(acc)
            a[x] = acc / mag if mag > 1e-12 else 1.0
        ca = [v.conjugate() for v in a]
        for y in range(p):
            acc = 0j
            for i, di, ci in trip_b[y]:
                acc += d[di] * ca[i] * cc[ci]
            mag = abs(acc)
            b[y] = acc / mag if mag > 1e-12 else 1.0
        cb = [v.conjugate() for v in b]
        for s in range(p):
            acc = 0j
            for i, j, di in trip_c[s]:
                acc += d[di] * ca[i] * cb[j]
            mag = abs(acc)
            c[s] = acc / mag if mag > 1e-12 else 1.0
        sweeps_used = it + 1
        delta = max(max(abs(a[i] - olda[i]) for i in range(p)),
                    max(abs(b[i] - oldb[i]) for i in range(p)),
                    max(abs(c[i] - oldc[i]) for i in range(p)))
        if delta < TOL:
            break
    ca = [v.conjugate() for v in a]
    cb = [v.conjugate() for v in b]
    cc = [v.conjugate() for v in c]
    corr = 0j
    for x in range(p):
        for y in range(p):
            corr += d[(x - y) % p] * ca[x] * cb[y] * cc[(x + y) % p]
    return abs(corr) / p ** 2, sweeps_used


def stats(vals):
    mu = sum(vals) / len(vals)
    var = sum((v - mu) ** 2 for v in vals) / len(vals)
    return max(vals), mu, math.sqrt(var)


def main():
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    out = open(OUT_PATH, "w")
    out.write("# probe_large_p: M(d)-decay probe for d(s)=e_p(s^3), p in {11,13,17}\n")
    out.write(f"# seed={SEED} restarts: 300 (p=11,13) / 120 (p=17); "
              f"max_sweeps={MAX_SWEEPS}; convergence_tol={TOL}; ties->phase 1\n")
    out.write("# Method: alternating phase-maximization identical to "
              "verify_solution.py CHECK 6 (alt_optimize), retuned for runtime.\n")
    out.write("# NOTE: this probe EXTENDS (not replaces) the deterministic CHECK 6 "
              "experiment (data/experiment_p5_n1.txt, data/experiment_p7_n1.txt).\n")
    out.write(f"# {'p':>3} {'cubic_best':>12} {'cubic_mean':>12} {'cubic_sd':>10} "
              f"{'rand_best':>12} {'rand_mean':>12} {'rand_sd':>10}\n")

    total_t0 = time.monotonic()
    for p, restarts in PLAN:
        trips = build_trips(p)
        dex_cubic = [(s ** 3) % p for s in range(p)]
        rng_c = random.Random(SEED + 600 + p)
        t0 = time.monotonic()
        vals_c = []
        sw_max = 0
        for r in range(restarts):
            v, sw = alt_optimize(dex_cubic, p, rng_c, trips)
            vals_c.append(v)
            sw_max = max(sw_max, sw)
            if (r + 1) % 50 == 0:
                print(f"  p={p} cubic restart {r + 1}/{restarts} "
                      f"best_so_far={max(vals_c):.6f}", flush=True)
        rng_d = random.Random(SEED + 700 + p)
        dex_rand = [rng_d.randrange(p) for _ in range(p)]
        rng_r = random.Random(SEED + 800 + p)
        vals_r = []
        for r in range(restarts):
            v, sw = alt_optimize(dex_rand, p, rng_r, trips)
            vals_r.append(v)
            sw_max = max(sw_max, sw)
            if (r + 1) % 50 == 0:
                print(f"  p={p} random restart {r + 1}/{restarts} "
                      f"best_so_far={max(vals_r):.6f}", flush=True)
        bc, mc, sc = stats(vals_c)
        br, mr, sr = stats(vals_r)
        elapsed = time.monotonic() - t0
        print(f"p={p}: cubic_best={bc:.9f} cubic_mean={mc:.9f} cubic_pstdev={sc:.9f} | "
              f"random_best={br:.9f} random_mean={mr:.9f} random_pstdev={sr:.9f} | "
              f"sweeps_max={sw_max} elapsed={elapsed:.1f}s", flush=True)
        out.write(f"# target_d=e_p(s^3) exponents={dex_cubic}\n")
        out.write(f"# control_random_d exponents={dex_rand}\n")
        out.write(f"{p:>4} {bc:>12.9f} {mc:>12.9f} {sc:>10.3e} "
                  f"{br:>12.9f} {mr:>12.9f} {sr:>10.3e}\n")
        out.write(f"# p={p} raw cubic finals={vals_c!r}\n")
        out.write(f"# p={p} raw random finals={vals_r!r}\n")
        out.flush()
    out.write(f"# total wall time {time.monotonic() - total_t0:.1f}s\n")
    out.close()
    print(f"DONE wrote {OUT_PATH}", flush=True)


if __name__ == "__main__":
    main()
