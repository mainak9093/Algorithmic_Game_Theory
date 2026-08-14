"""Which final SIZE PROFILES are reachable by any legal R3 execution on the
obstruction instance? RQ1 (approach 14) needs an almost-balanced one."""
from itertools import permutations
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "update_6"))
from guidedR3 import (size_shift, extend_options, apply_extend,
                      findsink_run, apply_findsink, compute_p, M_of_p, q_spread)

m, n = 3, 3
c = [
    {frozenset(): 0, frozenset({0}): 0, frozenset({1}): 0, frozenset({2}): 0,
     frozenset({0,1}): 0, frozenset({0,2}): 0, frozenset({1,2}): 0, frozenset({0,1,2}): 0},
    {frozenset(): 0, frozenset({0}): 0, frozenset({1}): 0, frozenset({2}): 0,
     frozenset({0,1}): 1, frozenset({0,2}): 1, frozenset({1,2}): 1, frozenset({0,1,2}): 1},
    {frozenset(): 0, frozenset({0}): 1, frozenset({1}): 1, frozenset({2}): 1,
     frozenset({0,1}): 2, frozenset({0,2}): 2, frozenset({1,2}): 2, frozenset({0,1,2}): 2},
]
v = [size_shift(ci, m) for ci in c]

profiles = {}
def rec(remaining, A, p):
    if not remaining:
        prof = tuple(sorted(len(b) for b in A))
        sp, _, q = q_spread(v, A, n)
        cur = profiles.get(prof)
        if cur is None or sp < cur: profiles[prof] = sp
        return
    g, rest = remaining[0], remaining[1:]
    opts = extend_options(v, A, p, g, n)
    if opts:
        for (rho, k) in opts:
            B = apply_extend(A, rho, k, g, n); rec(rest, B, compute_p(v, B, n))
    else:
        for s0 in M_of_p(p, n):
            s = findsink_run(v, A, p, g, n, s0)
            B = apply_findsink(A, s, g); rec(rest, B, compute_p(v, B, n))

for order in permutations(range(m)):
    rec(list(order), [frozenset() for _ in range(n)], [0]*n)

print("reachable final size profiles (sorted) -> best q-spread:")
for prof in sorted(profiles):
    ab = "ALMOST-BALANCED" if max(prof)-min(prof) <= 1 else ""
    print(f"   {prof}  best q-spread={profiles[prof]}   {ab}")
print()
print("almost-balanced profile (1,1,1) reachable?", (1,1,1) in profiles)
