#!/usr/bin/env python3
# EP-15 numerical experiment: does S = sum_{n>=1} (-1)^n n/p_n converge?
# Exact fixed-point partial sums to N=10^7 plus diagnostics. Stdlib only.
import os
import sys
import time
import json
import math
from array import array
from itertools import compress
from math import isqrt
from fractions import Fraction

T0 = time.time()
TARGET_DIR = "/mnt/c/Users/SkyD/Desktop/skydash_xyz/math-problem-1/Erdos problem EP-15"
N_MAX = 10**7
P6, P7 = 15485863, 179424673          # p_(10^6), p_(10^7)
CHECKPOINTS = [1000, 10_000, 100_000, 1_000_000, 10_000_000]
HALF_NS = {500, 5000, 50_000, 500_000, 5_000_000}
SNAPSET = frozenset(CHECKPOINTS) | HALF_NS
CSET = frozenset((500_000, 1_000_000, 5_000_000, 10_000_000))

LINES = []
J = {}
def out(line=""):
    print(line, flush=True)
    LINES.append(line)

def prog(line):
    print("[progress] " + line, file=sys.stderr)

def fail(msg):
    out("FATAL: " + msg)
    raise SystemExit(1)

def decstr(scaled, exp, frac):
    if scaled == 0:
        return "0." + "0"*frac
    neg = scaled < 0
    q, r = divmod(-scaled if neg else scaled, 10**exp)
    s = f"{q}.{str(r).zfill(exp)[:frac]}"
    return "-" + s if neg else s

def sigdig(dec, n=40):
    d = dec.lstrip("-").replace(".", "").lstrip("0")
    return d[:n] if d else "0"

def build_primes(limit, need):
    """Odds-only sieve of [1, limit] -> array P with P[n]=p_n (n>=1).
    Segment-wise extension past limit until len(P) >= need."""
    half = ((limit + 1) >> 1)
    sv = bytearray(b"\x01") * half
    sv[0] = 0
    i = 1
    while True:
        p = 2*i + 1
        if p*p > limit:
            break
        if sv[i]:
            st = (p*p) >> 1
            cnt = ((half - st) + p - 1) // p
            sv[st::p] = bytes(cnt)
        i += 1
    P = array("Q", [0, 2])
    P.extend(compress(range(1, limit + 1, 2), sv))
    del sv
    if len(P) < need:
        lo = limit + 1
        while len(P) < need:
            hi = lo + (1 << 16)
            rt = isqrt(hi - 1)
            base = []
            j = 1
            while True:
                q = P[j]
                if q > rt:
                    break
                base.append(q)
                j += 1
            size = hi - lo
            seg = bytearray(b"\x01") * size
            for q in base:
                qq = q*q
                if qq >= hi:
                    break
                st = max(qq, ((lo + q - 1)//q)*q)
                if st < hi:
                    cnt = ((hi - st) + q - 1) // q
                    seg[st - lo::q] = bytes(cnt)
            P.extend(compress(range(lo, hi), seg))
            lo = hi
    return P

def main():
    out("=== EP-15 experiment: S_N = sum_{n<=N} (-1)^n n/p_n ===")
    prog(f"sieving to {P7} ...")
    P = build_primes(P7, N_MAX + 2)     # need p_(10^7+1) too (gap/C diagnostics)
    if P[10**6] != P6:
        fail(f"p_(10^6) check failed: got {P[10**6]}, expected {P6}")
    if P[N_MAX] != P7:
        fail(f"p_(10^7) check failed: got {P[N_MAX]}, expected {P7}")
    out(f"p-checks passed: p_(10^6)={P[10**6]} ; p_(10^7)={P[N_MAX]} ; primes stored={len(P)-1}")
    J["p_checks"] = "passed"
    J["p_1e6"] = str(P[10**6])
    J["p_1e7"] = str(P[N_MAX])

    M_EXP = 60
    M = 10**M_EXP
    S = 0
    snaps = {}
    cnt_down = 0
    TV = tv6 = TVpair = 0
    B = maxB = tvp_at_max = 0
    kmax = 0
    hist = {}
    twos = 0
    mingap = None
    C = 0.0
    c_at = {}
    pl = P
    mn = M
    sn = SNAPSET
    prog("main loop n=1..10^7 ...")
    for n in range(1, N_MAX + 1):
        pn = pl[n]
        t = (2*n*mn + pn)//(2*pn)          # round-to-nearest of n*M/p_n
        S += -t if n & 1 else t
        if n in sn:
            snaps[n] = S
        if not n & 1:
            pm = pl[n-1]
            num = n*pm - (n-1)*pn          # pair term a_n - a_{n-1} = num/(pm*pn)
            den = pm*pn
            b = num*mn//den
            B += b
            ab = -b if b < 0 else b
            anum = num if num >= 0 else -num
            TVpair += anum*mn//den
            if ab > maxB:
                maxB = ab
                tvp_at_max = TVpair
                kmax = n >> 1
        g = pl[n+1] - pn                   # valid up to n=N_MAX thanks to p_(N_MAX+1)
        if n*g > pn:
            cnt_down += 1                  # a_{n+1} < a_n
        if g <= 300:
            hist[g] = hist.get(g, 0) + 1
            if g == 2:
                twos += 1
            if n > 1000 and (mingap is None or g < mingap):
                mingap = g
        C += 1.0/(n*g) if not n & 1 else -1.0/(n*g)
        if n in CSET:
            c_at[n] = C
        if n < N_MAX:
            d = n*g - pn
            if d < 0:
                d = -d
            TV += d*mn//(pn*pl[n+1])
        if n == 1_000_000:
            tv6 = TV
        if n % 1_000_000 == 0:
            prog(f"n={n} elapsed={time.time()-T0:.0f}s")

    out("")
    out("-- exact fixed-point partial sums (M=1e60, per-term round-half-up, rigorous accumulated rounding err <= N/(2M)) --")
    out(f"{'N':>9}  {'S_N (40 frac digits)':<63} {'a_N':>12} {'err_bound':>10}  Delta_N=S_N-S_(N/2) (25 fr)")
    J["partial_sums"] = {}
    for N in CHECKPOINTS:
        s_dec = decstr(snaps[N], M_EXP, 40)
        dlt = decstr(snaps[N] - snaps[N // 2], M_EXP, 25)
        aN = N/pl[N]
        eb = f"{N/(2.0*1e60):.3e}"
        out(f"{N:>9}  {s_dec:<63} {aN:>12.6f} {eb:>10}  {dlt}")
        J["partial_sums"][str(N)] = {"S": s_dec, "a_N": repr(aN), "err_bound": eb, "Delta": dlt}

    # independent second-scale pass to 10^6 with M2 = 1e50
    M2_EXP = 50
    M2 = 10**M2_EXP
    S2 = 0
    for n in range(1, 10**6 + 1):
        pn = pl[n]
        t = (2*n*M2 + pn)//(2*pn)
        S2 += -t if n & 1 else t
    d1 = decstr(snaps[10**6], M_EXP, 60)
    d2 = decstr(S2, M2_EXP, 50)
    agree = sigdig(d1) == sigdig(d2)
    out("")
    out(f"cross-scale check at N=10^6:  M=1e60 -> {d1}")
    out(f"                              M2=1e50 -> {d2}")
    out(f"first 40 significant digits: {'AGREE' if agree else 'DISAGREE'}")
    if not agree:
        fail("cross-scale 40-significant-digit agreement failed")
    J["cross_scale"] = {"agree40": agree, "S_M1e60": d1, "S_M2e50": d2}

    # validation against exact Fractions at N=5000
    Nv = 5000
    SF = sum(Fraction(-n if n & 1 else n, pl[n]) for n in range(1, Nv + 1))
    adiff = SF - Fraction(snaps[Nv], M)
    if adiff < 0:
        adiff = -adiff
    ok = adiff < Fraction(1, 10**45)
    out("")
    out(f"-- validation vs exact rational arithmetic at N={Nv} --")
    out(f"exact   S_5000 ~= {float(SF):.18f}")
    out(f"fixedpt S_5000 = {decstr(snaps[Nv], M_EXP, 40)}")
    out(f"|diff| = {float(adiff):.3e}   (< 1e-45: {'OK' if ok else 'FAIL'})")
    if not ok:
        fail("Fraction validation failed")
    J["fraction_validation"] = {"abs_diff": float(adiff), "ok": ok}

    ll6 = math.log(math.log(1e6))
    ll7 = math.log(math.log(1e7))
    out("")
    out("-- diagnostics over n<=10^7 --")
    out(f"cnt_down/N = {cnt_down/N_MAX:.6f}    (crude Exp(mean ln p) heuristic: 1-1/e = 0.632121; refined Cramér exp(-(p_n/n)/ln p_n) ~ 0.389 at n=1e7, -> e^-1 only as N->inf)")
    out(f"TV(1e6) = {decstr(tv6, M_EXP, 25)} ; TV(1e6)/lnln(1e6) = {float(tv6)/1e60/ll6:.6f}")
    out(f"TV(1e7) = {decstr(TV, M_EXP, 25)} ; TV(1e7)/lnln(1e7) = {float(TV)/1e60/ll7:.6f}    (theory -> 2/e = 0.735759)")
    out(f"pair drift: max_|B_K| (K<=5e6) = {decstr(maxB, M_EXP, 25)} at K={kmax}")
    out(f"TV_pair(2*K_max) = {decstr(tvp_at_max, M_EXP, 25)} ; TV_pair(1e7, full) = {decstr(TVpair, M_EXP, 25)}")
    out(f"cancellation ratio max|B_K|/TV_pair(2*K_max) = {(float(maxB)/1e60)/(float(tvp_at_max)/1e60):.6e} ; max|B_K|/TV_pair(1e7) = {(float(maxB)/1e60)/(float(TVpair)/1e60):.6e}")
    c6, c7, c5, c50 = c_at[1_000_000], c_at[N_MAX], c_at[500_000], c_at[5_000_000]
    dA, dB = abs(c6 - c5), abs(c7 - c50)
    out(f"companion C_N = sum (-1)^n/(n*g_n): C(1e6)={c6:.15f} ; C(1e7)={c7:.15f}")
    out(f"|C(1e6)-C(5e5)|={dA:.3e} ; |C(1e7)-C(5e6)|={dB:.3e} ; max={max(dA,dB):.3e}")
    modal_g = max(range(2, 301, 2), key=lambda g: hist.get(g, 0))
    out(f"divergence certificate for sum (-1)^n/g_n: #{{n<=1e7 : g_n<=300}} = {sum(hist.values())}")
    out(f"  modal even gap in [2,300]: g={modal_g}, count={hist.get(modal_g,0)}")
    out(f"  min gap seen for n>1000: {mingap} ; #{{n<=1e7 : g_n=2}} = {twos}")
    J["diagnostics"] = {
        "cnt_down_ratio": repr(cnt_down/N_MAX),
        "TV_1e6": decstr(tv6, M_EXP, 25), "TV_1e6_over_lnln": repr(float(tv6)/1e60/ll6),
        "TV_1e7": decstr(TV, M_EXP, 25), "TV_1e7_over_lnln": repr(float(TV)/1e60/ll7),
        "max_abs_B": decstr(maxB, M_EXP, 25), "argmax_K": str(kmax),
        "TVpair_at_maxB": decstr(tvp_at_max, M_EXP, 25), "TVpair_1e7": decstr(TVpair, M_EXP, 25),
        "cancellation_ratio_argmax": repr((float(maxB)/1e60)/(float(tvp_at_max)/1e60)),
        "cancellation_ratio_full": repr((float(maxB)/1e60)/(float(TVpair)/1e60)),
        "C_1e6": repr(c6), "C_1e7": repr(c7),
        "C_diff_max": repr(max(dA, dB)),
        "count_g_le_300": str(sum(hist.values())),
        "modal_even_gap": str(modal_g), "modal_count": str(hist.get(modal_g, 0)),
        "min_gap_n_gt_1000": str(mingap), "count_g_eq_2": str(twos),
    }

    # adversarial parity-bias probe: modeled world W(theta), pair drift at K=1e6
    # ERRATUM (superseded): this executed L^2-form has a CONVERGENT total and its sign
    # convention is inverted vs the exact pair identity; corrected model law is
    #   drift = (1-theta)*sum_{k<=K} 1/(2k L_k) ~ ((1-theta)/2)*ln ln K,
    # see ANALYSIS.md R5 erratum / ANSWER/answer_manifest.json. Probe kept for provenance only.
    K = 10**6
    ss = 0.0
    for k in range(1, K + 1):
        Lk = math.log(2.0*k)
        ss += 1.0/(2.0*k*Lk*Lk)
    ref = math.log(math.log(2*K))/2
    out("")
    out("-- adversarial parity-bias probe: modeled drift sum_{k<=K} b_k, b_k=(g_{2k-1}-L_k)/(2k L_k^2), K=1e6 --")
    out(f"sum_(k<=K) 1/(2k L_k^2) = {ss:.9f} ; closed-form reference (ln ln 2K)/2 = {ref:.9f}")
    J["adversarial"] = {"sum_inv": repr(ss), "ref_lnln_over2": repr(ref)}
    for th in (0.5, 0.9, 0.99):
        dv = (th - 1.0)*ss
        out(f"theta={th:.2f}: modeled drift = ({th}-1)*{ss:.9f} = {dv:+.9f}   (negative => diverging pair sums despite PNT mean gap)")
        J["adversarial"][f"drift_theta_{th}"] = repr(dv)

    wt = time.time() - T0
    out("")
    out(f"wall time: {wt:.1f} s")
    J["wall_seconds"] = f"{wt:.1f}"
    with open(os.path.join(TARGET_DIR, "results.json"), "w") as f:
        json.dump(J, f, indent=1)
    prog(f"done; results.json written; wall={wt:.1f}s")

if __name__ == "__main__":
    main()
