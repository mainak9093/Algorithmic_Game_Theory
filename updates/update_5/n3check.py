"""Verify the n=3 characterisation and the pairing claim underneath it.

CLAIM 1.  For n = 3 an allocation is good (envy-freeable with ell <= 1) iff
          every cycle has weight <= 0, every arc <= 1, and every 2-path <= 1.
          (Simple paths in a 3-node digraph have length 0, 1 or 2.)

CLAIM 2.  Given no positive 3-cycle, the 2-path i -> j -> k has weight
          <= -w(k,i).  As (i,j,k) runs over the 6 orderings of {1,2,3}, the
          closing arc (k,i) runs over all 6 ordered pairs exactly once.  So only
          the 2-paths whose closing arc is < -1 ever need separate checking, and
          there is exactly one such path per offending arc.

Both are checked by brute force against the true longest-path computation over
every dichotomous instance at n=3, m=3 and randomised larger ones.

Run:  python n3check.py
"""
from itertools import combinations, permutations, product, combinations_with_replacement
import random

from routeA import gen_functions, rand_dicho, ellvec, partitions


def arcs(cs, bd, n=3):
    return [[cs[i][bd[i]] - cs[i][bd[j]] for j in range(n)] for i in range(n)]


def good_by_definition(cs, bd, n=3):
    e = ellvec(cs, bd, n)
    return e is not None and max(e) <= 1


def good_by_claim1(cs, bd, n=3):
    W = arcs(cs, bd, n)
    idx = range(n)
    # cycles (2- and 3-)
    for r in (2, 3):
        for sub in combinations(idx, r):
            for per in permutations(sub[1:]):
                cyc = (sub[0],) + per
                if sum(W[cyc[t]][cyc[(t + 1) % r]] for t in range(r)) > 0:
                    return False
    # arcs
    for i in idx:
        for j in idx:
            if i != j and W[i][j] > 1:
                return False
    # 2-paths
    for i, j, k in permutations(idx, 3):
        if W[i][j] + W[j][k] > 1:
            return False
    return True


def claim2_pairing():
    """The closing arc of the 6 two-paths hits all 6 ordered pairs once."""
    seen = []
    for i, j, k in permutations(range(3), 3):
        seen.append((k, i))
    return sorted(seen) == sorted((a, b) for a in range(3) for b in range(3) if a != b)


def claim2_sufficiency(cs, bd, n=3):
    """If reassignment-stable and every arc in [-1,1], the allocation is good."""
    W = arcs(cs, bd, n)
    off = [W[i][j] for i in range(n) for j in range(n) if i != j]
    if not all(-1 <= w <= 1 for w in off):
        return None                      # hypothesis does not apply
    for r in (2, 3):
        for sub in combinations(range(n), r):
            for per in permutations(sub[1:]):
                cyc = (sub[0],) + per
                if sum(W[cyc[t]][cyc[(t + 1) % r]] for t in range(r)) > 0:
                    return None
    return good_by_definition(cs, bd, n)


def main():
    print("claim 2 pairing (6 two-paths <-> 6 ordered pairs):", claim2_pairing())

    bad1 = bad2 = tested = applied = 0

    F = gen_functions(3)
    for cs in combinations_with_replacement(F, 3):
        cs = list(cs)
        for bd in partitions(3, 3):
            tested += 1
            if good_by_definition(cs, bd) != good_by_claim1(cs, bd):
                bad1 += 1
            r = claim2_sufficiency(cs, bd)
            if r is not None:
                applied += 1
                if r is not True:
                    bad2 += 1
    print("exhaustive n=3 m=3: %d (instance, allocation) pairs" % tested)
    print("   claim 1 mismatches                        : %d" % bad1)
    print("   claim 2 hypothesis applied / failures     : %d / %d" % (applied, bad2))

    rng = random.Random(4242)
    tested = bad1 = bad2 = applied = 0
    for m in (4, 5, 6):
        for _ in range(300):
            cs = [rand_dicho(m, rng) for _ in range(3)]
            for bd in partitions(m, 3):
                tested += 1
                if good_by_definition(cs, bd) != good_by_claim1(cs, bd):
                    bad1 += 1
                r = claim2_sufficiency(cs, bd)
                if r is not None:
                    applied += 1
                    if r is not True:
                        bad2 += 1
    print("randomised m=4,5,6: %d pairs" % tested)
    print("   claim 1 mismatches                        : %d" % bad1)
    print("   claim 2 hypothesis applied / failures     : %d / %d" % (applied, bad2))


if __name__ == "__main__":
    main()
