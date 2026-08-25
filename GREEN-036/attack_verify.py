#!/usr/bin/env python3
"""GREEN-036 attack iteration: targeted structural checks (next.md policy).

Every printed claim is FINITE EVIDENCE, not an asymptotic theorem.
Stdlib only, deterministic.
"""
import sys
from itertools import count

LIMIT_HINT = int(sys.argv[1]) if len(sys.argv) > 1 else 10**6


def build_census(X):
    """Exact A cap [1,X], increasing-order DP per notes.md section 2."""
    import heapq
    member = bytearray(X + 1)
    member[2] = member[3] = 1
    heap = [2, 3]
    small = []
    while heap:
        m = heapq.heappop(heap)
        small.append(m)
        lim = min(m, X // m)
        for a in small:
            if a > lim:
                break
            n = m * a - 1
            if n <= X and not member[n]:
                member[n] = 1
                heapq.heappush(heap, n)
    return member, small


MEMO = {}


def in_A(n, member=None):
    """Exact membership by well-founded recursion:
    n in A  <=>  n in {2,3}  or  exists divisor pair (a,b) of n+1 with a,b in A.
    Every generating factor is < n, so recursion terminates. Prunes 1 mod 3 (Lemma A).
    """
    if n in (2, 3):
        return True
    if n < 2 or n % 3 == 1:
        return False
    if n in MEMO:
        return MEMO[n]
    m = n + 1
    ok = False
    d = 2
    while d * d <= m:
        if m % d == 0:
            a, b = d, m // d
            if a % 3 != 1 and b % 3 != 1 and _mem(a, member) and _mem(b, member):
                ok = True
                break
        d += 1
    MEMO[n] = ok
    return ok


def _mem(x, member):
    if member is not None and x < len(member):
        return bool(member[x])
    return in_A(x, member)


def is_prime(k):
    if k < 2:
        return False
    d = 2
    while d * d <= k:
        if k % d == 0:
            return False
        d += 1
    return True


def main():
    print("GREEN-036 attack checks — every output below is FINITE EVIDENCE")
    print("=" * 70)

    member, small = build_census(LIMIT_HINT)
    F = lambda n: sum(member[1:n + 1])
    print(f"[0] census rebuilt to X={LIMIT_HINT}: F(X)={F(LIMIT_HINT)}")
    assert LIMIT_HINT >= 10 ** 6 and F(10 ** 6) == 535585, "census cross-check failed"

    # (i) powers of 2 membership, k <= 40
    ks = [k for k in range(1, 41) if in_A(2 ** k, member)]
    print(f"(i) 2^k in A for k<=40: k in {ks}   (FINITE EVIDENCE, k range 1..40)")
    for k in range(1, 41):
        if k not in ks:
            in_A(2 ** k, member)  # ensure MEMO populated

    # (ii) anchor hole 11 and propagation family
    print(f"(ii) 11 in A: {in_A(11, member)}")
    bad = 0
    cnt = 0
    for q in range(2, 10 ** 5 + 1):
        if is_prime(q):
            cnt += 1
            if in_A(11 * q - 1, member):
                bad += 1
    print(f"(ii) holes 11q-1 (q prime <= 1e5): {cnt} tested, {bad} members of A "
          f"(expect 0)   (FINITE EVIDENCE)")

    # (iii) lcm intersection bound: |(b1 A -1) n (b2 A -1) n [1,X]| <= floor((X+1)/lcm)
    # intersection elements satisfy n = b1*a1 - 1 = b2*a2 - 1, i.e. n+1 is a common
    # multiple of b1,b2 (multiple of lcm) -- nothing more is asserted.
    from math import gcd
    X = LIMIT_HINT
    for b1, b2 in [(2, 3), (2, 5), (3, 5), (8, 9)]:
        L = b1 * b2 // gcd(b1, b2)
        inter = sum(1 for n in range(1, X + 1)
                    if member[n] and (n + 1) % L == 0)
        bound = (X + 1) // L
        status = "OK" if inter <= bound else "VIOLATED"
        print(f"(iii) b=({b1},{b2}) lcm={L}: |intersection|={inter} <= floor((X+1)/lcm)={bound}  [{status}]"
              f"   (FINITE EVIDENCE)")

    # (iv) chain claims
    for n in (19, 25, 205, 1024):
        print(f"(iv) {n} in A: {in_A(n, member)} (expect False)   (FINITE EVIDENCE)")
    print("(iv) support facts: 41 in A: {} ; 14 in A: {} ; 13 mod 3 = {}; 103 mod 3 = {}".format(
        in_A(41, member), in_A(14, member), 13 % 3, 103 % 3))

    print("=" * 70)
    print("done")


if __name__ == "__main__":
    main()
