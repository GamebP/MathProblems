#!/usr/bin/env python3
"""
Verification script for Erdos Problem 7 — odd distinct covering system.
Computes candidate L tables, divisor data, reciprocal sums, abundant checks,
CNF/ILP dimensions, subset counts, and verifies covering condition.

No hardcoding of theorems; all derived via sympy exact arithmetic.
"""
import sympy as sp
import math, itertools

def divisors_gt1(L):
    return [d for d in sp.divisors(L) if d>1]

def reciprocal_sum(L):
    divs = divisors_gt1(L)
    return sum(sp.Rational(1,d) for d in divs)

def analyze_L(L):
    fac = sp.factorint(L)
    divs = divisors_gt1(L)
    tau = sp.divisor_count(L)
    sigma = sp.divisor_sigma(L,1)
    rec = reciprocal_sum(L)
    V = sum(divs)
    log10prod = sum(math.log10(d) for d in divs)
    # odd divisors count (here all since L odd)
    odd_divs = [d for d in divs if d%2==1]
    return {
        "L": L, "factorization": fac, "tau": tau, "num_proper_divs": len(divs),
        "odd_divs": len(odd_divs), "V": V, "log10prod": log10prod,
        "sum_recip": rec, "sum_recip_float": float(rec),
        "sigma": sigma, "sigma_over_L": float(sp.Rational(sigma, L)),
        "abundant": sigma >= 2*L,
        "divs": divs
    }

def subset_counts(L):
    divs = divisors_gt1(L)
    n = len(divs)
    cnt = 0
    min_k = n+1
    min_example = None
    for mask in range(1<<n):
        s = sum(sp.Rational(1, divs[i]) for i in range(n) if (mask>>i)&1)
        if s >= 1:
            cnt += 1
            k = bin(mask).count("1")
            if k < min_k:
                min_k = k
                min_example = [divs[i] for i in range(n) if (mask>>i)&1]
    return cnt, 1<<n, min_k, min_example

def verify_covering(system, L):
    """
    system: list of (a,d)
    L: period
    Returns (covered_count, uncovered_list, ok)
    """
    covered = set()
    for a,d in system:
        for r in range(0, L, d):
            covered.add((a + r) % L)
    uncovered = [n for n in range(L) if n not in covered]
    return len(covered), uncovered, len(covered)==L

def main():
    print("="*70)
    print("Erdos Problem 7 — Verification: candidate L analysis")
    print("="*70)
    candidates = [945,1575,2205,2835,3465,4095,4725]
    # Also test odd L <945 for abundancy
    print("\n--- Odd abundant check L < 945 ---")
    odd_abund_small = [n for n in range(1,946,2) if sp.divisor_sigma(n,1) >= 2*n]
    print("Odd abundant n<945:", odd_abund_small[:10], "count", len(odd_abund_small))
    print("Smallest odd abundant:", odd_abund_small[0] if odd_abund_small else None)
    assert odd_abund_small[0]==945, "945 must be smallest odd abundant"

    print("\n--- Candidate L tables ---")
    rows = []
    for L in candidates:
        info = analyze_L(L)
        rows.append(info)
        print(f"\nL={L} = {info['factorization']}")
        print(f"  tau={info['tau']}  |D|={info['num_proper_divs']} odd|D|={info['odd_divs']} V=sumD={info['V']} log10(prod D)={info['log10prod']:.2f}")
        print(f"  divs: {info['divs']}")
        print(f"  sum_{{d|L,d>1}} 1/d = {info['sum_recip']} = {info['sum_recip_float']:.12f}")
        print(f"  sigma={info['sigma']} sigma/L={info['sigma_over_L']:.6f} abundant={info['abundant']}  9|L={L%9==0} 15|L={L%15==0}")

    # Verify folklore: sum 1/d >=1 iff sigma >=2L
    print("\n--- Folklore abundant equivalence check ---")
    for info in rows:
        L = info["L"]
        lhs = info["sum_recip"] + 1  # includes d=L? Actually sum_{d|L}1/d =1 + sum_{d|L,d>1,d<L? Wait careful
        # Full divisor sum: sum_{d|L}1/d = sigma/L
        full_sum = sum(sp.Rational(1,d) for d in sp.divisors(L))
        sigma_over_L = sp.Rational(info["sigma"], L)
        print(f"L={L}: sum_{{d|L}}1/d = {full_sum} = sigma/L = {sigma_over_L}  equal? {full_sum==sigma_over_L}")
        assert full_sum == sigma_over_L
        # sum_{d|L,d>1}1/d = sigma/L -1
        assert info["sum_recip"] == sigma_over_L - 1

    # Verify distinctness: need sum_{selected}1/d >=1 is necessary for covering [0,L-1]
    print("\n--- Reciprocal threshold necessary condition ---")
    for L in [945,1575,2205,2835]:
        divs = divisors_gt1(L)
        full = reciprocal_sum(L)
        print(f"L={L} full sum {float(full):.6f} {'PASS >=1' if full>=1 else 'FAIL'}")

    # Subset counts
    print("\n--- Subset counts with sum>=1 (pruning power) ---")
    for L in [945,1575,2205,2835]:
        cnt, total, min_k, example = subset_counts(L)
        frac = cnt/total*100
        print(f"L={L}: {cnt}/{total} = {frac:.4f}%  min_k={min_k} example={example}")
        # Verify elimination >99.7% for smallest?
        # compute pairwise AMO etc
        divs = divisors_gt1(L)
        pairwise = sum(d*(d-1)//2 for d in divs)
        seq = 3*sum(divs)
        print(f"  pairwise AMO clauses {pairwise}  sequential ~{seq}  cover clauses {L}  |D|={len(divs)}")

    # Odd L <945: verify none meets sum>=1? Actually check
    print("\n--- Exhaustive: smallest odd L with sum>=1 is 945? ---")
    # Check all odd L <945 with sum_{d|L,d>1}1/d >=1 must be abundant
    # Already odd abundant minimal is 945, so none <945 passes. Verify brute
    fails=[]
    for L in range(3,945,2):
        if reciprocal_sum(L) >=1:
            fails.append(L)
    print("Odd L<945 with sum>=1:", fails[:10], "len", len(fails))
    assert len(fails)==0, "No odd L<945 should reach threshold"

    # Verify covering example (known distinct covering with even modulus)
    print("\n--- Verify classic Erdos covering system (even modulus) ---")
    erdos_example = [(0,2),(0,3),(1,4),(1,6),(11,12)]
    L_erdos = 12
    cov_count, uncovered, ok = verify_covering(erdos_example, L_erdos)
    print(f"Classic system {erdos_example} L={L_erdos} covered {cov_count}/{L_erdos} ok={ok} uncovered={uncovered}")
    assert ok, "Classic example must cover Z_12"
    # Check distinct odd attempt fails trivially
    print("\n--- Test trivial odd candidate fails ---")
    # Try small odd set: {0 mod3,1 mod5,2 mod7} cannot cover mod 105
    small_system = [(0,3),(1,5),(2,7)]
    L_small = 105
    cov_count2, uncovered2, ok2 = verify_covering(small_system, L_small)
    print(f"Small odd system {small_system} L={L_small} covered {cov_count2}/{L_small} ok={ok2} uncovered sample {uncovered2[:20]}")
    assert not ok2

    # Verify exact BBMST c0*prod heuristic numbers (approx)
    print("\n--- BBMST numeric sanity check ---")
    c0 = 0.0979
    # Simulate product for squarefree primes >73. Using s_k = p_k-1 with delta_k from BBMST table approximated.
    # We won't reproduce exact delta, just show product >1 but c0*product <1.
    # Example: product for p=79.. ~500th prime approx 6.25 to get cN~0.612
    # Compute mock product with s=p-1 and delta=0.1 for illustration (not exact BBMST)
    # The point: individual factors >1, but c0 small makes product <1 feasible.
    import math as m
    primes = list(sp.primerange(3, 500))  # first ~95 primes, includes tail
    # For squarefree, BBMST product tail roughly
    mock_factors = [1+1/((1-0.1)*(p-1)) for p in primes[5:]]  # skip first 5 as c0 LP region
    mock_prod = 1.0
    for f in mock_factors[:30]:
        mock_prod *= f
    print(f"Mock: c0={c0}  product(30 primes tail)={mock_prod:.3f}  c0*prod={c0*mock_prod:.3f}")
    # Show sieveProd without c0 >1
    from functools import reduce
    import operator
    sieveProd = 1.0
    for p in primes[:5]:
        sieveProd *= (1+1/(p-1))
    print(f"Naive sieveProd without c0 (p=3,5,7,11,13): {sieveProd:.3f} >1 always")
    assert sieveProd>1
    # With c0, <1 possible
    cN_mock = c0 * sieveProd
    print(f"c0 * sieveProd(5 primes) = {cN_mock:.3f}")

    # ILP dimensions per L
    print("\n--- CNF/ILP dimensions (exact) ---")
    for L in [945,1575,2205,2835]:
        divs = divisors_gt1(L)
        V = sum(divs)
        pairwise = sum(d*(d-1)//2 for d in divs)
        t = len(divs)
        print(f"L={L}: V={V} (+{t} y) pairwise AMO={pairwise} seq~{3*V} cover clauses={L} width={t} literals_cover={L*t} ILP vars={V+t} ILP cons={t+L}")

    print("\n" + "="*70)
    print("All verification checks PASSED.")
    print("Residuals: sum_{d|L,d>1}1/d - (sigma/L -1) = 0 exactly for all L")
    print("Smallest odd abundant =945 verified, no odd L<945 passes threshold.")
    print("Classic covering verified, odd small system correctly fails.")
    print("="*70)

if __name__=="__main__":
    main()
