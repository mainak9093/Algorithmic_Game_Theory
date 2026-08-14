"""The extremal family, verified: U_n needs total subsidy exactly n-1.

tightness.py extracted, as the smallest instance attaining |S| = n-1 at n=3, the
instance "3 identical additive agents; chores of cost (0,1,1)".  Stripping the
free chore leaves the family

    U_n :  n agents, all identical and additive,
           m = n-1 chores, each of cost 1 to every agent.

These costs are dichotomous (c(S) = |S|, so every marginal is exactly 1).

CLAIM.  For U_n the minimum total subsidy over allocations with p in {0,1}^n is
exactly n-1, so the bound of Conjecture 1 is tight for every n.

REASON.  Any allocation gives agent i cost |A_i|, and sum_i |A_i| = n-1 < n, so
some agent h has A_h empty and cost 0.  Then w(i,h) = |A_i| - 0 = |A_i|, so
ell(i) >= |A_i|; keeping max ell <= 1 forces |A_i| <= 1 for all i, hence exactly
n-1 agents hold one chore each, and each of those has ell = 1.  Total = n-1.

Verified below by exhaustive search over all n^(n-1) allocations.

Run:  python tight_family.py
"""
from itertools import product
from minimum_subsidy import total_subsidy


def U(n):
    """Cost dicts for U_n: m = n-1 unit chores, all agents identical additive."""
    m = n - 1
    return [(lambda S: len(S)) for _ in range(n)], m


def verify(n, verbose=True):
    cs, m = U(n)
    bestS = None
    bestAny = None
    witness = None
    for assign in product(range(n), repeat=m):
        bd = [frozenset(g for g in range(m) if assign[g] == i) for i in range(n)]
        a = [[cs[i](bd[j]) for j in range(n)] for i in range(n)]
        t, e = total_subsidy(a, n)
        if t is None:
            continue
        if bestAny is None or t < bestAny:
            bestAny = t
        if max(e) <= 1 and (bestS is None or t < bestS):
            bestS, witness = t, (bd, e)
    if verbose:
        print("  U_%d : m=%d, %d allocations | min |S| over good = %s (n-1 = %d)%s"
              " | min total over all = %s"
              % (n, m, n ** m, bestS, n - 1,
                 "  MATCH" if bestS == n - 1 else "  *** MISMATCH ***", bestAny))
        if witness:
            bd, e = witness
            print("        witness bundles %s  p=%s"
                  % ([sorted(b) for b in bd], e))
    return bestS


def main():
    print("=== U_n : n identical additive agents, n-1 chores of cost 1 ===")
    print("    (dichotomous: c(S) = |S|, every marginal exactly 1)")
    print()
    allok = True
    for n in range(2, 8):
        got = verify(n)
        allok &= (got == n - 1)
    print()
    print("  bound n-1 attained for every n tested : %s" % allok)
    print()
    print("  => Conjecture 1's bound cannot be improved to any constant, nor to")
    print("     any function growing slower than n-1.  The remaining content of")
    print("     the conjecture is entirely the upper bound: some allocation has")
    print("     max_i ell_A(i) <= 1.")


if __name__ == "__main__":
    main()
