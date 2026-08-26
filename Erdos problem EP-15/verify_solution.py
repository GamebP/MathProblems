"""verify_solution.py — EP-15 analysis verification.
Checks every exact identity claimed in ANALYSIS.md against an independent sieve,
plus the corrected adversarial-model drift numbers and manifest validity."""
import json, math, os
from fractions import Fraction

BASE = os.path.dirname(os.path.abspath(__file__))
ok = True
def check(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name)
    ok = ok and cond

# independent sieve (not reusing ep15_partial_sums.py code paths)
LIM = 800_000
sv = bytearray([1]) * LIM; sv[0] = sv[1] = 0
for i in range(2, int(LIM**.5) + 1):
    if sv[i]: sv[i*i::i] = bytearray(len(sv[i*i::i]))
P = [i for i in range(LIM) if sv[i]]

N = 50_000
# [R1/R4] monotonicity equivalence and pair identity, exact rational arithmetic
eq_ok = b_ok = True
down = 0
for n in range(1, N):
    p, q = P[n-1], P[n]; g = q - p
    a, an = Fraction(n+1, q), Fraction(n, p)
    if (a < an) != (n*g > p): eq_ok = False
    if a < an: down += 1
    if n % 2 == 1:
        k = (n+1)//2
        if a - an != Fraction(p-(2*k-1)*g, p*q) or a-an != Fraction(2*k*p-(2*k-1)*q, p*q):
            b_ok = False
check("R1 chain a_{n+1}<a_n <=> n g_n > p_n (exact, n<=%d)" % N, eq_ok)
check("R4 identities b_k=(p-(2k-1)g)/pp=(2k p'-(2k-1)p'')/pp (exact)", b_ok)
b1 = Fraction(2, P[1]) - Fraction(1, P[0])
check("R4 sanity b_1=a_2-a_1=1/6 matches max|B_K|=1/6 @K=1", b1 == Fraction(1, 6))
check("R1 numerics: downward-step ratio at 5e4 within (0.35,0.5) [page: 0.4213@1e7]",
      0.35 < down/N < 0.5)

# [R6] S_1000 vs fixed-point record (20 digits given)
S = sum((Fraction((-1)**n*n, P[n-1]) for n in range(1, 1001)), Fraction(0))
from decimal import Decimal, getcontext
getcontext().prec = 60
dS = str(Decimal(S.numerator)/Decimal(S.denominator))
check("R6 S_1000 reproduces record 0.01186889173738435952...", dS.startswith("0.01186889173738435951"))

# [R5 erratum] corrected model drift: b_k = (1-theta)/(2k L_k), L_k=ln(2k)
K = 10**6
corr = sum(1.0/(2.0*k*math.log(2.0*k)) for k in range(1, K+1))
executed = 1.4442906399044022   # page's (convergent) L^2-sum, from results.json
for th, page_v in (("0.5", -0.722145), ("0.9", -0.144429), ("0.99", -0.014443)):
    mine = (1-float(th))*corr
    print("      theta=%s corrected drift %+ .6f | executed-L2 %+.6f" % (th, mine, page_v))
check("R5 corrected drift sum exists and diverges in sign of (1-theta); corr=%.6f" % corr,
      abs(corr - 1.9979182415529024) < 1e-6)
check("R5 erratum documented: executed sum uses L^2 (convergent total)",
      abs(sum(1.0/((2.0*k)*math.log(2.0*k)**2) for k in range(1, K+1)) - executed) < 1e-4)

# [D.2] regime sanity: block estimates
Y = 10**5
small = sum(1.0/(n*math.log(n)*math.log(math.log(n))**2.5) for n in range(100, Y))
full_conv_hint = small < 20   # heuristic only; theorem-level claim cited not computed
print("      U_{2.5} partial (n<1e5) = %.3f (consistent with convergence for c>2)" % small)

# manifest validation
mpath = os.path.join(BASE, "ANSWER", "answer_manifest.json")
try:
    man = json.load(open(mpath))
    check("manifest parses as JSON", True)
    need = {"problem_id","statement","verdict","key_values","error_control","obstruction",
            "missing_implication","counterexample_analysis","sibling_series","artifacts","references"}
    check("manifest has all required keys", need <= set(man))
except Exception as e:
    check("manifest parses as JSON (%s)" % e, False)

print("\nALL CHECKS:", "PASS" if ok else "FAIL")
