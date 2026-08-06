"""The n-1 bound of Conjecture 1 is TIGHT: an explicit extremal family.

minimal_S.py found, for every n in {3,4,5}, instances whose minimal paid set has
size exactly n-1, always with witness p = (1,...,1,0).  Two things follow and are
checked here.

(A)  REDUNDANCY.  p* = ell_A is a longest-path potential, so p* >= 0 and the
     endpoint of a maximum-weight path has ell = 0.  Hence min_i p*_i = 0 for
     EVERY envy-freeable allocation, and

         p in {0,1}^n   ==>   total = |S| <= n-1   automatically.

     So the "total <= n-1" clause of Conjecture 1 is not a second requirement:
     Conjecture 1 is exactly  "some allocation has max_i ell_A(i) <= 1".
     Checked here on every allocation of every instance generated.

(B)  TIGHTNESS.  A minimal certified instance attaining |S| = n-1 is extracted
     and re-verified exhaustively, so the bound cannot be improved to any
     constant.  Reported in the smallest form found (fewest chores, then
     smallest costs).

Run:  python tightness.py
"""
from itertools import product
import random
from minimum_subsidy import rand_dicho, matrix_realising, total_subsidy
from minimal_S import analyse


def check_min_zero(cs, m, n):
    """(A): does every envy-freeable allocation have min_i ell(i) = 0?"""
    for assign in product(range(n), repeat=m):
        bd = [frozenset(g for g in range(m) if assign[g] == i) for i in range(n)]
        a = [[cs[i][bd[j]] for j in range(n)] for i in range(n)]
        t, e = total_subsidy(a, n)
        if t is not None and min(e) != 0:
            return False, (bd, e)
    return True, None


def singletons(c, m):
    return [c[frozenset({g})] for g in range(m)]


def report(cs, m, n, w):
    bd, e = w
    print("    chores m=%d, agents n=%d ; witness bundles %s ; p=%s"
          % (m, n, [sorted(b) for b in bd], e))
    print("    cost matrix a_ij = c_i(A_j):")
    for i in range(n):
        print("       ", [cs[i][bd[j]] for j in range(n)])
    print("    singleton costs c_i({g}):")
    for i in range(n):
        print("        agent %d: %s   (additive: %s)"
              % (i, singletons(cs[i], m),
                 all(cs[i][S] == sum(cs[i][frozenset({g})] for g in S)
                     for S in [frozenset(t) for k in range(m + 1)
                               for t in __import__('itertools').combinations(range(m), k)])))


def main():
    rng = random.Random(31337)
    print("=== (A) min_i ell(i) = 0 on every envy-freeable allocation ===")
    bad = 0
    tested = 0
    for (n, m, T) in [(3, 4, 400), (3, 5, 250), (4, 4, 250), (4, 5, 120), (5, 4, 60)]:
        for _ in range(T):
            cs = (matrix_realising(m, n, rng, 3) if rng.random() < 0.55
                  else [rand_dicho(m, rng, rng.choice([0.0, 0.5, 1.0]))
                        for _ in range(n)])
            if max(max(c.values()) for c in cs) < 1:
                continue
            tested += 1
            ok, ex = check_min_zero(cs, m, n)
            if not ok:
                bad += 1
                print("  !! violation:", ex)
    print("  instances tested: %d ; violations: %d" % (tested, bad))
    print("  => 'total <= n-1' is implied by 'p in {0,1}^n'; the conjecture is")
    print("     exactly:  some allocation has max_i ell_A(i) <= 1.")

    print()
    print("=== (B) smallest instances attaining |S| = n-1 ===")
    rng = random.Random(2718)
    best = {}
    for (n, m, T) in [(3, 3, 4000), (3, 4, 4000), (3, 5, 1500),
                      (4, 4, 3000), (4, 5, 1200)]:
        for _ in range(T):
            cs = (matrix_realising(m, n, rng, 3) if rng.random() < 0.55
                  else [rand_dicho(m, rng, rng.choice([0.0, 0.15, 0.5, 0.85, 1.0]))
                        for _ in range(n)])
            if max(max(c.values()) for c in cs) < 1:
                continue
            bestS, bestAny, w = analyse(cs, m, n)
            if bestS != n - 1 or w is None:
                continue
            key = (m, max(max(c.values()) for c in cs))
            if n not in best or key < best[n][0]:
                best[n] = (key, cs, m, w, bestAny)
    for n in sorted(best):
        key, cs, m, w, bestAny = best[n]
        print("  n=%d : minimal |S| = %d = n-1  (min total over ALL allocations = %d)"
              % (n, n - 1, bestAny))
        report(cs, m, n, w)
        print()
    if not best:
        print("  none found at these sizes")


if __name__ == "__main__":
    main()
