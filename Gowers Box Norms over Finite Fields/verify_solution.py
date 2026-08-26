#!/usr/bin/env python3
"""GREEN-028 analysis verification suite.

Python 3.12 stdlib only (math / cmath / random / fractions). No numpy.
Deterministic: every RNG stream derives from the fixed SEED below.
Run from inside this directory:
    python3 verify_solution.py
"""

import cmath
import math
import os
import random
import sys
from fractions import Fraction

TOL = 1e-9
SEED = 20260826

WORKDIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(WORKDIR, "data")


def make_group(p, n):
    """G = F_p^n as index lists; returns elems, addition table, dot table."""
    import itertools
    elems = list(itertools.product(range(p), repeat=n))
    m = len(elems)
    idx = {e: i for i, e in enumerate(elems)}
    add = [[idx[tuple((u[c] + v[c]) % p for c in range(n))] for v in elems]
           for u in elems]
    dot = [[sum(u[c] * v[c] for c in range(n)) % p for v in elems] for u in elems]
    return elems, add, dot, m


def ep(p, k):
    return cmath.exp(2j * math.pi * (k % p) / p)


# ----------------------------------------------------------------------
# CHECK 1 -- Proposition A spectral identity
#   E_h ||Delta_(h,h) f||_square^4  ==  sum_{xi in Xi0} |Bhat_f(xi)|^2
# ----------------------------------------------------------------------
def check1():
    print("=" * 76)
    print("CHECK 1 - Proposition A spectral identity")
    print("  E_h ||Delta_(h,h) f||_sq^4 == sum_{xi in Xi0} |Bhat_f(xi)|^2, f in {+-1}")
    all_ok = True
    for ci, (p, n) in enumerate([(3, 1), (3, 2), (5, 1)]):
        rng = random.Random(SEED + 101 + ci)
        elems, add, dot, m = make_group(p, n)
        f = {(i, j): rng.choice((1, -1)) for i in range(m) for j in range(m)}
        # LHS: exact rational accumulation of +-1 box sums
        total = Fraction(0)
        m4 = m ** 4
        for ih in range(m):
            g = [[f[(add[x][ih], add[y][ih])] * f[(x, y)] for y in range(m)]
                 for x in range(m)]
            s = 0
            for x1 in range(m):
                gx1 = g[x1]
                for x2 in range(m):
                    gx2 = g[x2]
                    for y1 in range(m):
                        a11 = gx1[y1]
                        a21 = gx2[y1]
                        row1 = gx1
                        row2 = gx2
                        for y2 in range(m):
                            s += a11 * a21 * row1[y2] * row2[y2]
            total += Fraction(s, m4)
        lhs = float(total / m)
        # RHS: B_f on G^4, direct Fourier transform axis-by-axis via char tables
        T = {}
        for x1 in range(m):
            for x2 in range(m):
                for y1 in range(m):
                    r11 = f[(x1, y1)]
                    r21 = f[(x2, y1)]
                    r12row = x1
                    for y2 in range(m):
                        T[(x1, x2, y1, y2)] = complex(
                            r11 * r21 * f[(x1, y2)] * f[(x2, y2)])
        cw = [[cmath.exp(-2j * math.pi * dot[u][v] / p) for v in range(m)]
              for u in range(m)]
        for axis in range(4):
            NT = {}
            get = NT.get
            for key, val in T.items():
                k = key[axis]
                head = key[:axis]
                tail = key[axis + 1:]
                for j in range(m):
                    nk = head + (j,) + tail
                    NT[nk] = get(nk, 0j) + val * cw[j][k]
            T = NT
        n4 = float(m ** 4)
        zero_elem = (0,) * n
        rhs = 0.0
        energy_all = 0.0
        for key, val in T.items():
            bh = val / n4
            e2 = abs(bh) ** 2
            energy_all += e2
            ssum = tuple(sum(elems[key[t]][c] for t in range(4)) % p
                         for c in range(n))
            if ssum == zero_elem:
                rhs += e2
        resid = abs(lhs - rhs)
        ok = resid <= TOL
        all_ok &= ok
        print(f"  (p={p},n={n}): LHS={lhs!r}  RHS={rhs!r}  "
              f"|LHS-RHS|={resid:.3e}  tol={TOL:g} -> {'PASS' if ok else 'FAIL'}")
        print(f"     [diagnostic] Parseval sum over ALL xi of |Bhat|^2 = {energy_all!r} (expect 1)")
    return all_ok


# ----------------------------------------------------------------------
# CHECK 2 -- Proposition B factorization, (p,n)=(3,1)
# ----------------------------------------------------------------------
def box_avg(g, p):
    tot = 0j
    for x1 in range(p):
        for x2 in range(p):
            for y1 in range(p):
                a11 = g[(x1, y1)]
                a21 = g[(x2, y1)].conjugate()
                for y2 in range(p):
                    tot += a11 * a21 * g[(x1, y2)].conjugate() * g[(x2, y2)]
    return tot / p ** 4


def u2_avg(w, p):
    tot = 0j
    for s in range(p):
        for t in range(p):
            for u in range(p):
                tot += (w[s] * w[(s + t) % p].conjugate()
                        * w[(s + u) % p].conjugate() * w[(s + t + u) % p])
    return tot / p ** 3


def check2():
    print("=" * 76)
    print("CHECK 2 - Proposition B factorization (p,n)=(3,1), random unimodular a,b,c")
    p = 3
    rng = random.Random(SEED + 202)
    om = cmath.exp(2j * math.pi / p)
    a = [om ** rng.randrange(p) for _ in range(p)]
    b = [om ** rng.randrange(p) for _ in range(p)]
    c = [om ** rng.randrange(p) for _ in range(p)]
    lhs = 0j
    for h in range(p):
        g = {}
        for x in range(p):
            for y in range(p):
                g[(x, y)] = (a[(x + h) % p] * b[(y + h) % p] * c[(x + y + h) % p]
                             * a[x].conjugate() * b[y].conjugate()
                             * c[(x + y) % p].conjugate())
        lhs += box_avg(g, p)
    lhs /= p
    rhs = 0j
    for h in range(p):
        w = [c[(s + h) % p] * c[s].conjugate() for s in range(p)]
        rhs += u2_avg(w, p)
    rhs /= p
    resid = abs(lhs - rhs)
    ok = resid <= TOL
    print(f"  LHS=E_h ||Delta_(h,h)[a(x)b(y)c(x+y)]||_sq^4 = {lhs.real!r} (imag part {lhs.imag:.1e})")
    print(f"  RHS=||c||_U3^8 via E_h ||Delta_h c||_U2^4   = {rhs.real!r}")
    print(f"  |LHS-RHS| = {resid:.3e}  tol={TOL:g} -> {'PASS' if ok else 'FAIL'}")
    return ok


# ----------------------------------------------------------------------
# CHECK 3 -- Quadratic absorption lemma over F_p
# ----------------------------------------------------------------------
def gauss_modp(rows, tgts, NU, p):
    aug = [[v % p for v in row] + [t % p] for row, t in zip(rows, tgts)]
    piv_cols = []
    r0 = 0
    for col in range(NU):
        piv = None
        for r in range(r0, len(aug)):
            if aug[r][col]:
                piv = r
                break
        if piv is None:
            continue
        aug[r0], aug[piv] = aug[piv], aug[r0]
        inv = pow(aug[r0][col], -1, p)
        aug[r0] = [(v * inv) % p for v in aug[r0]]
        for r in range(len(aug)):
            if r != r0 and aug[r][col]:
                fac = aug[r][col]
                aug[r] = [(aug[r][k] - fac * aug[r0][k]) % p for k in range(NU + 1)]
        piv_cols.append(col)
        r0 += 1
        if r0 == len(aug):
            break
    bad_rhs = None
    for row in aug[len(piv_cols):]:
        if all(v == 0 for v in row[:NU]) and row[NU]:
            bad_rhs = row[NU]
            break
    sol = [0] * NU
    for r in reversed(range(len(piv_cols))):
        c = piv_cols[r]
        s = aug[r][NU]
        for k in range(c + 1, NU):
            if aug[r][k]:
                s -= aug[r][k] * sol[k]
        sol[c] = s % p
    rank = len(piv_cols)
    if bad_rhs is not None:
        return False, None, rank, (
            f"inconsistent system mod {p}: reduced-echelon row with all-zero "
            f"coefficients but rhs={bad_rhs}; rank={rank} of {len(rows)} equations, "
            f"{NU} unknowns ({NU - rank} would-be free)")
    return True, sol, rank, f"consistent, rank={rank}/{len(rows)} eqs, {NU - rank} free vars"


def check3_case(p, n, mode, seed):
    rng = random.Random(seed)
    nq = n * (n + 1) // 2
    pairs = [(i, j) for i in range(n) for j in range(i, n)]
    pid = {pr: k for k, pr in enumerate(pairs)}
    off_al, off_bq, off_bl = nq, nq + n, 2 * nq + n
    off_gq, off_gl, off_k = 2 * nq + 2 * n, 3 * nq + 2 * n, 3 * nq + 3 * n
    NU = 3 * nq + 3 * n + 1

    A = {pr: rng.randrange(p) for pr in pairs}
    C = {pr: rng.randrange(p) for pr in pairs}
    B = [[rng.randrange(p) for _ in range(n)] for _ in range(n)]
    if mode == "sym":
        for i in range(n):
            for j in range(i, n):
                B[i][j] = B[j][i] = rng.randrange(p)
    else:
        if n >= 2:
            B[0][1] = rng.randrange(p)
            B[1][0] = (B[0][1] + 1 + rng.randrange(p - 1)) % p
    dvec = [rng.randrange(p) for _ in range(n)]
    evec = [rng.randrange(p) for _ in range(n)]
    c0 = rng.randrange(p)

    rows, tgts = [], []

    def add_row(coeffs, tgt):
        rows.append(coeffs)
        tgts.append(tgt)

    zerovec = lambda: [0] * NU  # ponytail: single-use closure, fine
    for (i, j) in pairs:  # x_i x_j and y_i y_j blocks
        v = zerovec()
        v[pid[(i, j)]] += 1
        v[off_gq + pid[(i, j)]] += 1
        add_row(v, A[(i, j)])
        v = zerovec()
        v[off_bq + pid[(i, j)]] += 1
        v[off_gq + pid[(i, j)]] += 1
        add_row(v, C[(i, j)])
    for i in range(n):  # cross monomials x_i y_j (all ordered pairs)
        for j in range(n):
            v = zerovec()
            if i == j:
                v[off_gq + pid[(i, i)]] += 2
            else:
                v[off_gq + pid[(min(i, j), max(i, j))]] += 1
            add_row(v, B[i][j])
    for i in range(n):  # linear blocks
        v = zerovec()
        v[off_al + i] += 1
        v[off_gl + i] += 1
        add_row(v, dvec[i])
        v = zerovec()
        v[off_bl + i] += 1
        v[off_gl + i] += 1
        add_row(v, evec[i])
    v = zerovec()  # constant
    v[off_k] += 1
    add_row(v, c0)

    ok, sol, rank, info = gauss_modp(rows, tgts, NU, p)

    def Qval(x, y):
        xs, ys = list(x), list(y)
        t = c0
        for (i, j) in pairs:
            t += A[(i, j)] * xs[i] * xs[j] + C[(i, j)] * ys[i] * ys[j]
        for i in range(n):
            for j in range(n):
                t += B[i][j] * xs[i] * ys[j]
            t += dvec[i] * xs[i] + evec[i] * ys[i]
        return t % p

    mism = None
    if ok:
        def decval(x, y):
            xs, ys = list(x), list(y)
            s = [(xs[i] + ys[i]) % p for i in range(n)]
            t = sol[off_k]
            for (i, j) in pairs:
                t += sol[pid[(i, j)]] * xs[i] * xs[j]
                t += sol[off_bq + pid[(i, j)]] * ys[i] * ys[j]
                t += sol[off_gq + pid[(i, j)]] * s[i] * s[j]
            for i in range(n):
                t += (sol[off_al + i] * xs[i] + sol[off_bl + i] * ys[i]
                      + sol[off_gl + i] * s[i])
            return t % p

        mism = 0
        for _ in range(24):
            x = tuple(rng.randrange(p) for _ in range(n))
            y = tuple(rng.randrange(p) for _ in range(n))
            if Qval(x, y) != decval(x, y):
                mism += 1
    asym = [(i, j) for i in range(n) for j in range(i + 1, n) if B[i][j] != B[j][i]]
    return ok, sol, rank, info, mism, asym, B, nq, n


def check3():
    print("=" * 76)
    print("CHECK 3 - Quadratic absorption Q == alpha(x)+beta(y)+gamma(x+y)+const' mod p")
    worst_same_index = 0
    obstruction_text = None
    case_no = 0
    for (p, n) in [(3, 1), (5, 1), (5, 2)]:
        case_no += 1
        ok, sol, rank, info, mism, asym, B, nq, nn = check3_case(
            p, n, "sym", SEED + 300 + case_no)
        if not ok or mism != 0:
            worst_same_index = max(worst_same_index, mism if mism else 10 ** 9)
        status = "PASS" if (ok and mism == 0) else "FAIL"
        print(f"  [{p},{n}] SYMMETRIC-CROSS B: {info}; pointwise 24 random (x,y): "
              f"mismatches={mism} -> {status}")
    # cross-coordinate stress only exists when n >= 2
    ok, sol, rank, info, mism, asym, B, nq, nn = check3_case(
        5, 2, "gen", SEED + 310)
    if not ok:
        (i, j) = asym[0]
        obstruction_text = (
            f"CROSS-COORDINATE OBSTRUCTION at (p,n)=(5,2): coefficient matchers force "
            f"gamma_quad[{min(i,j)},{max(i,j)}] to equal BOTH B[{i}][{j}]={B[i][j]} "
            f"(from x_{i} y_{j}) AND B[{j}][{i}]={B[j][i]} (from x_{j} y_{i}) mod 5; "
            f"B asymmetric so Gaussian elimination reports: {info}. Per-pair forms "
            f"(x_i+y_j)^2 lie outside span{{x-coords, y-coords, x+y coords}}, so "
            f"alpha/beta/gamma cannot absorb non-symmetric cross coefficients.")
        print(f"  [5,2] GENERIC-CROSS B (B01={B[0][1]}, B10={B[1][0]}, forced distinct):")
        print(f"    {info} -> system INCONSISTENT")
        print(f"    OBSTRUCTION (verbatim): {obstruction_text}")
    else:
        print(f"  [5,2] GENERIC-CROSS B: unexpectedly consistent: {info}, mismatches={mism}")
        worst_same_index = max(worst_same_index, mism or 0)
    return worst_same_index == 0, obstruction_text


# ----------------------------------------------------------------------
# CHECK 4 & 5 share the same seeded object f on F_5^2
# ----------------------------------------------------------------------
def build_check4_objects():
    p = 5
    rng = random.Random(SEED + 404)
    om = cmath.exp(2j * math.pi / p)
    a = [om ** rng.randrange(p) for _ in range(p)]
    b = [om ** rng.randrange(p) for _ in range(p)]
    dv = [om ** rng.randrange(p) for _ in range(p)]
    A, Bq, C, D, E, C0 = (rng.randrange(p) for _ in range(6))

    def Q(x, y):
        return (A * x * x + Bq * x * y + C * y * y + D * x + E * y + C0) % p

    def f(x, y):
        return a[x] * b[y] * dv[(x - y) % p] * om ** Q(x, y)

    return p, om, a, b, dv, (A, Bq, C, D, E, C0), Q, f


def check4():
    print("=" * 76)
    print("CHECK 4 - Theorem D sufficiency (p,n)=(5,1): "
          "Delta_(h,h) f == alpha_h(x) beta_h(y) pointwise")
    p, om, a, b, dv, (A, Bq, C, D, E, C0), Q, f = build_check4_objects()
    mixviol = 0
    for h in range(p):
        def inh(xx, yy, h=h):
            return (Q((xx + h) % p, (yy + h) % p) - Q(xx, yy)) % p
        for x in range(p):
            for y in range(p):
                d2 = (inh((x + 1) % p, (y + 1) % p) - inh((x + 1) % p, y)
                      - inh(x, (y + 1) % p) + inh(x, y)) % p
                if d2:
                    mixviol += 1
    print(f"  mixed xy-coefficient of increment Q(x+h,y+h)-Q(x,y): mixed second "
          f"difference violations = {mixviol} over all h,x,y (must be 0; "
          f"algebraically coeff = {Bq}*h - {Bq}*h = 0)")
    maxdev = 0.0
    ka = (2 * A + Bq) % p
    kb = (Bq + 2 * C) % p
    kc = (A + Bq + C) % p
    kd = (D + E) % p
    for h in range(p):
        alph = [a[(x + h) % p] * a[x].conjugate() * om ** ((ka * h * x) % p)
                for x in range(p)]
        betah = [b[(y + h) % p] * b[y].conjugate()
                 * om ** ((kb * h * y + kc * h * h + kd * h) % p)
                 for y in range(p)]
        for x in range(p):
            for y in range(p):
                df = f((x + h) % p, (y + h) % p) * f(x, y).conjugate()
                dev = abs(df - alph[x] * betah[y])
                if dev > maxdev:
                    maxdev = dev
    ok = maxdev < 1e-12 and mixviol == 0
    print(f"  alpha_h(x)=a(x+h)/a(x)*e_p({ka}hx); beta_h(y)=b(y+h)/b(y)"
          f"*e_p({kb}hy+{kc}h^2+{kd}h)")
    print(f"  max |Delta_(h,h) f - alpha_h beta_h| over all h,x,y = {maxdev:.3e} "
          f"(required < 1e-12) -> {'PASS' if ok else 'FAIL'}")
    return ok


def check5():
    print("=" * 76)
    print("CHECK 5 - negative perturbation: same f times e_p(x*y*y) (cubic mixed term)")
    p, om, a, b, dv, coeffs, Q, f = build_check4_objects()
    g = {}
    for x in range(p):
        for y in range(p):
            g[(x, y)] = f(x, y) * om ** ((x * y * y) % p)
    rngm = random.Random(SEED + 505)
    trials = 60
    per_h = []
    for h in range(p):
        D = {(x, y): g[((x + h) % p, (y + h) % p)] * g[(x, y)].conjugate()
             for x in range(p) for y in range(p)}
        bad = False
        for _ in range(trials):
            x1, y1, x2, y2 = (rngm.randrange(p) for _ in range(4))
            lhs = D[(x1, y1)] * D[(x2, y2)]
            rhs = D[(x1, y2)] * D[(x2, y1)]
            if abs(lhs - rhs) > 1e-9:
                bad = True
                break
        per_h.append(bad)
    fails = sum(per_h)
    frac = fails / p
    badh = [h for h in range(p) if per_h[h]]
    print(f"  rank-one test (2x2 minors, 60 random pairs/h, tol 1e-9): "
          f"failing h = {badh}; fraction of h with NO rank-one factorization = {frac}")
    print(f"  measured outcome (informational): cubic mixed perturbation breaks "
          f"rank-one structure for {fails}/{p} shifts")
    return frac


# ----------------------------------------------------------------------
# CHECK 6 -- counterexample experiment
# ----------------------------------------------------------------------
DOMINANCE = ("DOMINANCE STATEMENT: quadratic-phase factors are redundant under the "
             "reading (-1)^q = e_p(Q). By CHECK 3 (symmetric-cross case) any such "
             "e_p(Q(x,y)) factors as e_p(alpha(x))e_p(beta(y))e_p(gamma(x+y)), which "
             "absorbs into a,b,c. Hence M = sup over arbitrary unimodular a,b,c "
             "already dominates the sup over the full stated class.")


def alt_optimize(dex, p, rng, max_sweeps=300):
    om = cmath.exp(2j * math.pi / p)
    d = [om ** (k % p) for k in dex]
    a = [om ** rng.randrange(p) for _ in range(p)]
    b = [om ** rng.randrange(p) for _ in range(p)]
    c = [om ** rng.randrange(p) for _ in range(p)]

    def phase_of(acc):
        mag = abs(acc)
        return acc / mag if mag > 1e-12 else 1.0

    sweeps_used = 0
    for it in range(max_sweeps):
        olda, oldb, oldc = a[:], b[:], c[:]
        for x in range(p):
            acc = 0j
            for y in range(p):
                acc += d[(x - y) % p] * b[y].conjugate() * c[(x + y) % p].conjugate()
            a[x] = phase_of(acc)
        for y in range(p):
            acc = 0j
            for x in range(p):
                acc += d[(x - y) % p] * a[x].conjugate() * c[(x + y) % p].conjugate()
            b[y] = phase_of(acc)
        for s in range(p):
            acc = 0j
            for x in range(p):
                y = (s - x) % p
                acc += d[(2 * x - s) % p] * a[x].conjugate() * b[y].conjugate()
            c[s] = phase_of(acc)
        sweeps_used = it + 1
        delta = max(max(abs(a[i] - olda[i]) for i in range(p)),
                    max(abs(b[i] - oldb[i]) for i in range(p)),
                    max(abs(c[i] - oldc[i]) for i in range(p)))
        if delta < 1e-13:
            break
    corr = 0j
    for x in range(p):
        for y in range(p):
            corr += (d[(x - y) % p] * a[x].conjugate() * b[y].conjugate()
                     * c[(x + y) % p].conjugate())
    return abs(corr) / p ** 2, sweeps_used


def control_quadratic_exact(p, witness):
    """corr = |E d(x-y) abar bbar cbar| for d=e_p(2s^2) and a quadratic-phase
    triple (a,b,c). witness 'brief':  a=e_p(2x^2),b=e_p(2y^2),c=e_p(-s^2)
    (the literal factors named in the brief).
    witness 'solved': alpha=4x^2, beta=4y^2, gamma=-2s^2, solving
    alpha(x)+beta(y)+gamma(x+y) == 2(x-y)^2 mod p exactly, so
    a*b*c == d pointwise, d*conj(abc)==1 everywhere, corr must be exactly 1."""
    om = cmath.exp(2j * math.pi / p)
    if witness == "brief":
        ea_, eb_, ec_ = 2, 2, -1
    else:
        ea_, eb_, ec_ = 4, 4, -2
    a = [om ** ((ea_ * x * x) % p) for x in range(p)]
    b = [om ** ((eb_ * y * y) % p) for y in range(p)]
    c = [om ** ((ec_ * s * s) % p) for s in range(p)]
    d = [om ** ((2 * s * s) % p) for s in range(p)]
    corr = 0j
    for x in range(p):
        for y in range(p):
            corr += (d[(x - y) % p] * a[x].conjugate() * b[y].conjugate()
                     * c[(x + y) % p].conjugate())
    return abs(corr) / p ** 2


def check6():
    print("=" * 76)
    print("CHECK 6 - counterexample numerics: d(s)=e_p(s^3), G=F_p, p in {5,7}")
    print("  target M = sup_unimodular |E_xy d(x-y) conj(a(x)) conj(b(y)) conj(c(x+y))|")
    print("  " + DOMINANCE)
    os.makedirs(DATA_DIR, exist_ok=True)
    RESTARTS = 1000
    MAX_SWEEPS = 300

    def stats(vals):
        mu = sum(vals) / len(vals)
        var = sum((v - mu) ** 2 for v in vals) / len(vals)
        return max(vals), mu, math.sqrt(var)

    completed = True
    for p in (5, 7):
        dex_cubic = [(s ** 3) % p for s in range(p)]
        rngc = random.Random(SEED + 600 + p)
        vals_c = []
        sw_max = 0
        for _ in range(RESTARTS):
            v, sw = alt_optimize(dex_cubic, p, rngc, MAX_SWEEPS)
            vals_c.append(v)
            sw_max = max(sw_max, sw)
        rngd = random.Random(SEED + 700 + p)
        dex_rand = [rngd.randrange(p) for _ in range(p)]
        rngrr = random.Random(SEED + 800 + p)
        vals_r = []
        for _ in range(RESTARTS):
            v, sw = alt_optimize(dex_rand, p, rngrr, MAX_SWEEPS)
            vals_r.append(v)
            sw_max = max(sw_max, sw)
        bc, mc, sc = stats(vals_c)
        br, mr, sr = stats(vals_r)
        cq_solved = control_quadratic_exact(p, "solved")
        cq_brief = control_quadratic_exact(p, "brief")
        path = os.path.join(DATA_DIR, f"experiment_p{p}_n1.txt")
        with open(path, "w") as fh:
            fh.write("# GREEN-028 CHECK 6 raw experiment\n")
            fh.write(f"# p={p} n=1 seed={SEED} restarts={RESTARTS} "
                     f"max_sweeps={MAX_SWEEPS} convergence_tol=1e-13 ties->1\n")
            fh.write("# " + DOMINANCE + "\n")
            fh.write(f"target_d=e_p(s^3) exponents={dex_cubic}\n")
            fh.write(f"cubic_best={bc!r}\ncubic_mean={mc!r}\ncubic_pstdev={sc!r}\n")
            fh.write("cubic_finals=" + repr(vals_c) + "\n")
            fh.write(f"control_random_d exponents={dex_rand}\n")
            fh.write(f"randomd_best={br!r}\nrandomd_mean={mr!r}\nrandomd_pstdev={sr!r}\n")
            fh.write("randomd_finals=" + repr(vals_r) + "\n")
            fh.write(f"control_quadratic d(s)=e_p(2s^2), solved witness "
                     f"a=e_p(4x^2) b=e_p(4y^2) c=e_p(-2s^2): exact_corr={cq_solved!r} "
                     f"|corr-1|={abs(cq_solved - 1)!r}\n")
            fh.write(f"control_quadratic NOTE: brief's literal witness a=e_p(2x^2) "
                     f"b=e_p(2y^2) c=e_p(-s^2) gives corr={cq_brief!r} (= |Gauss sum|"
                     f"/p = 1/sqrt({p}) up to rounding, since d*conj(abc)=e_p((x-y)^2)), "
                     f"NOT 1; the solved witness above restores exact corr=1.\n")
            fh.write(f"max_sweeps_used_any_restart={sw_max}\n")
        print(f"  p={p}: cubic d(s)=e_p(s^3): best|corr|={bc:.9f}  "
              f"mean={mc:.9f}  pstdev={sc:.3e}")
        print(f"  p={p}: random d (exp={dex_rand}): best|corr|={br:.9f}  "
              f"mean={mr:.9f}  pstdev={sr:.3e}")
        print(f"  p={p}: control d(s)=e_p(2s^2), solved witness "
              f"a=e_p(4x^2) b=e_p(4y^2) c=e_p(-2s^2): corr={cq_solved!r}  "
              f"|corr-1|={abs(cq_solved - 1):.3e}")
        print(f"  p={p}: [erratum note] brief's literal witness (2x^2,2y^2,-s^2) "
              f"gives corr={cq_brief!r} (=1/sqrt({p})), not 1; see data file note")
        print(f"  wrote raw results -> {path}")
    return completed


# ----------------------------------------------------------------------
# CHECK 7 -- collapse law for the cubic-mixed twist (Check 5 family)
#   f = g * e_p(x0*y0^2),  g = a(x)b(y)d(x-y)e_p(Q)   (rigidity class)
#   Prediction: E_h ||Delta_(h,h) f||_square^4 = (2p-1)/p^2   (indep. of n)
#   h=0 and h0=0 directions keep rank-one increments -> box value 1;
#   h0 != 0 directions acquire e_p(2*h0*x0*y0) -> box value |E_{u,v} e_p(2 h0 u0 v0)| = 1/p.
#   Control: unperturbed g gives exactly 1 for every h.
# ----------------------------------------------------------------------
def check7():
    print("=" * 76)
    print("CHECK 7 - collapse law: f = g*e_p(x0*y0^2), prediction (2p-1)/p^2")
    all_ok = True
    lam = 1
    for ci, (p, n) in enumerate([(5, 1), (7, 1), (3, 2), (5, 2)]):
        rng = random.Random(SEED + 900 + 17 * ci)
        elems, add, dot, m = make_group(p, n)
        om = cmath.exp(2j * math.pi / p)
        a = [om ** rng.randrange(p) for _ in range(m)]
        b = [om ** rng.randrange(p) for _ in range(m)]
        dv = [om ** rng.randrange(p) for _ in range(m)]
        dmap = {}
        for xi in range(m):
            for yi in range(m):
                diff = tuple((elems[xi][c] - elems[yi][c]) % p for c in range(n))
                dmap[(xi, yi)] = dv[elems.index(diff)]
        pairs = [(i, j) for i in range(n) for j in range(i, n)]
        QA = {(i, j): rng.randrange(p) for (i, j) in pairs}
        QC = {(i, j): rng.randrange(p) for (i, j) in pairs}
        QB = [[rng.randrange(p) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                QB[j][i] = QB[i][j]
        lx = [rng.randrange(p) for _ in range(n)]
        ly = [rng.randrange(p) for _ in range(n)]
        k0 = rng.randrange(p)

        def Qval(xi, yi):
            x, y = elems[xi], elems[yi]
            t = k0
            for (i, j) in pairs:
                t += QA[(i, j)] * x[i] * x[j] + QC[(i, j)] * y[i] * y[j]
            for i in range(n):
                for j in range(n):
                    t += QB[i][j] * x[i] * y[j]
                t += lx[i] * x[i] + ly[i] * y[i]
            return t % p

        def gval(xi, yi):
            return a[xi] * b[yi] * dmap[(xi, yi)] * om ** Qval(xi, yi)

        def fval(xi, yi):
            x, y = elems[xi], elems[yi]
            return gval(xi, yi) * om ** ((lam * x[0] * y[0] * y[0]) % p)

        def avg_box(f):
            total = 0.0
            for ih in range(m):
                D = [[f[(add[x][ih], add[y][ih])] * f[(x, y)].conjugate()
                      for y in range(m)] for x in range(m)]
                s = 0j
                for x1 in range(m):
                    r1 = D[x1]
                    for x2 in range(m):
                        r2 = D[x2]
                        for y1 in range(m):
                            a11 = r1[y1]
                            a21 = r2[y1].conjugate()
                            for y2 in range(m):
                                s += a11 * a21 * r1[y2].conjugate() * r2[y2]
                total += s.real
            return total / (m ** 4 * m)

        ftab = {(xi, yi): fval(xi, yi) for xi in range(m) for yi in range(m)}
        gtab = {(xi, yi): gval(xi, yi) for xi in range(m) for yi in range(m)}
        lhs_twist = avg_box(ftab)
        lhs_plain = avg_box(gtab)
        pred = (2 * p - 1) / p ** 2
        resid = abs(lhs_twist - pred)
        ok = resid <= TOL and abs(lhs_plain - 1.0) <= TOL
        all_ok &= ok
        print(f"  (p={p},n={n}): E_h||Delta f||_sq^4 = {lhs_twist!r}  "
              f"prediction (2p-1)/p^2 = {pred!r}  |diff|={resid:.3e}"
              f" -> {'PASS' if ok else 'FAIL'}")
        print(f"     control unperturbed g: {lhs_plain!r} (expect 1)")
    return all_ok


def main():
    print(f"GREEN-028 verify_solution.py | seed={SEED} tol={TOL:g} | stdlib only")
    ok1 = check1()
    ok2 = check2()
    ok3, obstruction = check3()
    ok4 = check4()
    frac5 = check5()
    ok6 = check6()
    ok7 = check7()

    print("=" * 76)
    print("SUMMARY")
    print(f"  CHECK 1 Proposition A spectral identity : "
          f"{'PASS (all residuals <= 1e-9)' if ok1 else 'FAIL'}")
    print(f"  CHECK 2 Proposition B factorization     : {'PASS' if ok2 else 'FAIL'}")
    print(f"  CHECK 3 absorption, same-index          : "
          f"{'PASS (0 mismatches all cases)' if ok3 else 'FAIL'}"
          + ("" if obstruction is None else " | cross-coordinate obstruction reported verbatim above"))
    print(f"  CHECK 4 Theorem D sufficiency           : {'PASS (< 1e-12)' if ok4 else 'FAIL'}")
    print(f"  CHECK 5 negative perturbation           : MEASURED fraction failing h = {frac5}")
    print(f"  CHECK 6 counterexample experiment       : {'COMPLETED (raw data written to data/)' if ok6 else 'INCOMPLETE'}")
    print(f"  CHECK 7 collapse law (cubic twist)      : {'PASS ((2p-1)/p^2 confirmed)' if ok7 else 'FAIL'}")
    exit_ok = ok1 and ok2 and ok3 and ok4 and ok6 and ok7
    print(f"EXIT {'0' if exit_ok else '1'}")
    sys.exit(0 if exit_ok else 1)


if __name__ == "__main__":
    main()
