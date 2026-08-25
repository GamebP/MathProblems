#!/usr/bin/env python3
"""GREEN-036 attack iteration 2: targeted checks for attack2.md.

Every printed claim is FINITE EVIDENCE unless labeled PROVEN (the proofs live
in attack2.md; computation only spot-checks them). Stdlib only.
"""
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from attack_verify import build_census, is_prime  # reuse trusted DP

X = 2 * 10 ** 6
member, small = build_census(X)
F = lambda n: sum(member[1:n + 1])
assert F(10 ** 6) == 535585, "census cross-check failed"

print("GREEN-036 attack-2 checks — FINITE EVIDENCE unless stated PROVEN")
print("=" * 70)

# --- T2: 4q-1 family (PROVEN vacuous; check membership AND class) ---
cnt = bad = cls_ok = 0
for q in range(2, 20000):
    if is_prime(q) and q % 6 == 5:
        cnt += 1
        n = 4 * q - 1
        bad += bool(member[n])
        cls_ok += (n % 3 == 1)
print(f"[T2] 4q-1, q==5 mod 6, q<20000: {cnt} tested, {bad} in A "
      f"(PROVEN expect 0); all n==1 mod 3: {cls_ok == cnt}")

# --- T1: holes in reduced APs; instance M=5, r=2 ---
p = next(t for t in range(2, 200) if is_prime(t) and t % 15 == 1)
tot = holes = viol = inap = 0
sample = []
for qq in range(2, 60000):
    if is_prime(qq) and qq % 5 == 3:          # q == r+1 = 3 (mod 5)
        n = p * qq - 1
        assert n % 5 == 2
        m = bool(member[n])                   # n <= p*qq-1 < 31*6e4 < X
        tot += 1
        holes += (not m)
        viol += m
        if len(sample) < 8:
            sample.append(n)
print(f"[T1] M=5,r=2: p={p} (prime ==1 mod 15 => PROVEN notin A), "
      f"q prime ==3 mod 5 (<6e4): {tot} values pq-1, {holes} confirmed holes, "
      f"{viol} members (PROVEN expect 0).")
print(f"[T1] first holes: {sample[:8]}")

# --- rescue phenomenon + refuted blocking conjecture ---
print(f"[R] 116 in A: {bool(member[116])} (rescued via pair (3,39)); "
      f"39 in A: {bool(member[39])}; 13 in A: {bool(member[13])}")
print(f"[R] refuted-conjecture witness 364=7*13*4=14*26: sides 14,26 in A: "
      f"{bool(member[14])},{bool(member[26])}; 363 in A: {bool(member[363])}")

# --- T3 doubling recurrence sweep ---
ok = True
rows = []
for N in [10 ** k for k in range(3, 7)]:
    lhs = F(2 * N)
    pen = (2 * N) // 6 - N // 6
    rhs = F(N) + (F(N) - F(N // 2)) + (F(2 * N // 3) - F(N // 3)) - pen - 2
    ok &= lhs >= rhs
    rows.append((N, int(lhs - rhs)))
rel = all(F(2 * N) / (2 * N) >= 13 * (F(N) / N) / 12 - 1 / 8 - 1 / N
          for N in [10 ** 5, 10 ** 6])
print(f"[T3] doubling recurrence valid at N=1e3..1e6: {ok}, margins {rows}")
print(f"[T3] relative form delta(2N)>=13delta/12-1/8-O(1/N) at 1e5,1e6: {rel}")

# --- Lemma-A guard ---
violA = sum(1 for n in range(1, X + 1) if member[n] and n % 3 == 1)
print(f"[A] Lemma A violations in census to {X}: {violA}")

print("=" * 70)
print("done")
