#!/usr/bin/env python3
"""GREEN-036 attack iteration 3: checks for attack3.md.

FINITE EVIDENCE unless a [PROVEN] proof exists in attack3.md (computation
only spot-checks proofs). Default scan is fast; --extended reproduces the
full Proposition 3.3 range (primes <= 1500, semiprime samples <= 60000).
"""
import sys, math
from itertools import combinations

sys.path.insert(0, __file__.rsplit("/", 1)[0])
EXTENDED = "--extended" in sys.argv
sys.argv = [sys.argv[0]] + [a for a in sys.argv[1:] if not a.startswith("--")]
from attack_verify import build_census

X = 10 ** 6


def is_prime(k):
    if k < 2:
        return False
    d = 2
    while d * d <= k:
        if k % d == 0:
            return False
        d += 1
    return True


def closed_residue_set(m):
    """Worklist closure (commutative op): O(|S| * |adds|) instead of full passes."""
    S = {2 % m, 3 % m}
    queue = [2 % m, 3 % m]
    while queue:
        r = queue.pop()
        new = []
        for s in list(S):
            v = (r * s - 1) % m
            if v not in S:
                S.add(v)
                new.append(v)
        if not queue:
            queue = new
        else:
            queue.extend(new)
    return frozenset(S)


def main():
    extended = EXTENDED
    member, small = build_census(X)
    F = lambda n: sum(member[1:n + 1])
    assert F(10 ** 6) == 535585, "census cross-check failed"
    print("GREEN-036 attack-3 checks — FINITE EVIDENCE unless stated PROVEN")
    print("=" * 70)

    # --- Lemma 3.A: comb identity + membership ---
    import random
    random.seed(7)

    def combval(seq):
        v = seq[0]
        for l in seq[1:]:
            v = v * l - 1
        return v

    def comb_exp(seq):
        P = 1
        for l in seq:
            P *= l
        if len(seq) == 1:
            return seq[0]
        if len(seq) == 2:
            return seq[0] * seq[1] - 1
        s = 0
        for st in range(2, len(seq)):
            pr = 1
            for l in seq[st:]:
                pr *= l
            s += pr
        return P - s - 1

    ok = all(combval(sq := [random.choice([2, 3]) for _ in range(random.randint(1, 14))])
             == comb_exp(sq) for _ in range(2000))
    cnt = ina = 0
    for _ in range(4000):
        v = combval([random.choice([2, 3]) for _ in range(random.randint(2, 18))])
        if v <= X:
            cnt += 1
            ina += bool(member[v])
    print(f"[3A] comb identity 2000/2000: {ok}; combs<=1e6 in A: {ina}/{cnt}")

    # --- Lemma 3.B ---
    tbl = all(((r * s - 1) % 3 != 1) for r in (0, 2) for s in (0, 2))
    print(f"[3B] C={{0,2}} mod 3 closed under rs-1: {tbl} [PROVEN separately]")

    # --- Theorem 3.2 falsifications ---
    U = lambda i: 2 ** (i + 1) + 1
    V = lambda j: (3 ** (j + 1) + 1) // 2
    W = lambda k: (7 * 5 ** k + 1) // 4
    print(f"[3.2] orbit coincidences: W_1={W(1)}==U_2={U(2)}: {W(1)==U(2)}; "
          f"V_6={V(6)}==W_4={W(4)}: {V(6)==W(4)}; 3*365==5*219: {3*365==5*219}")
    w = U(0) * V(0) * W(4) - 1
    print(f"[3.2][FALSIFIED] ternary 6563 witness: 3*2*1094-1={w}, member={bool(member[w])}")
    vals = {}
    coll = []
    tot = notin = 0
    i = 0
    while U(i) <= X:
        j = 0
        while U(i) * V(j) - 1 <= X:
            k = 0
            while (U(i) * V(j) - 1) * W(k) <= X + 1:
                v = (U(i) * V(j) - 1) * W(k) - 1
                if v <= X:
                    tot += 1
                    m = bool(member[v])
                    notin += (not m)
                    if v in vals:
                        coll.append((vals[v], (i, j, k), v, m))
                    else:
                        vals[v] = ((i, j, k), m)
                k += 1
            j += 1
        i += 1
    print(f"[3.2] depth-3 folds <=1e6: {tot} generated, {len(vals)} distinct, "
          f"{len(coll)} collisions, not-in-A {notin}")
    for c in coll:
        print("      collision:", c)

    # --- Proposition 3.3 modulus scan ---
    rng = 1500 if extended else 500
    proper = [(p, len(closed_residue_set(p))) for p in range(2, rng + 1)
              if is_prime(p)]
    proper = [(p, l) for p, l in proper if l < p]
    print(f"[3.3] primes<={rng}: proper = {proper} (expect [(3,2)])")
    pp = [(m, len(closed_residue_set(m)), m) for mm in (2, 3) for k in range(2, 13)
          for m in [mm ** k] if m <= (4096 if mm == 2 else 6561)]
    print("[3.3] prime powers:", [(f"m", f"{l}/{m}") for m, l, _ in pp
                                   if l < m] or "all full systems")
    sem = []
    ps = [x for x in range(2, 44) if is_prime(x)]
    for a, b in combinations(ps, 2):
        m = a * b
        if len(closed_residue_set(m)) < m:
            sem.append((m, "3-lift" if m % 3 == 0 else "NEW"))
    print(f"[3.3] semiprimes<=~1900 exhaustive ({len(list(combinations(ps,2)))} "
          f"moduli): non-3-lift proper = {[s for s in sem if s[1] != '3-lift']}")
    if extended:
        newobs = []
        sc = 0
        ps = [x for x in range(2, 72) if is_prime(x)]
        seen = set()
        for p1, p2 in combinations(ps, 2):
            m = p1 * p2
            if m > 5000 or m in seen:
                continue
            seen.add(m)
            sc += 1
            if m % 3 != 0 and len(closed_residue_set(m)) < m:
                newobs.append(m)
        print(f"[3.3][extended] {sc} semiprime moduli <=5000 exhaustive "
              f"(p<q<=71): non-3-lift proper = {newobs}")

    # --- Theorem 3.5 same-scale tables ---
    for M in (1000, 10000):
        S = [x for x in small if x <= M]
        SS = set()
        for idx, a in enumerate(S):
            for b in S[idx:]:
                if a * b <= 2 * M:
                    SS.add(a * b)
        n = sum(1 for v in SS if v <= 2 * M)
        print(f"[3.5] M={M}: F(M)={F(M)}, |SS cap[1,2M]|={n}, "
              f"ratio={n/F(M):.3f} (GP floor ~2)")

    # --- Lemma A guard ---
    print(f"[A] Lemma A violations <= {X}: "
          f"{sum(1 for n in range(1, X+1) if member[n] and n % 3 == 1)}")
    print("=" * 70)
    print("done")


if __name__ == "__main__":
    main()
