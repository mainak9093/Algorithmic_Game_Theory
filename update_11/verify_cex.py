"""Verify the counterexample to claims (I) and (II) as a genuine dichotomous
instance, and then ask whether the CHAIN CONJECTURE itself survives.

The matrix found by matrix_interval.py:

        a = c_i(A_j) =  [0, 0, 0]
                        [2, 2, 1]
                        [3, 3, 2]

is good at levels 1 and 3 but NOT at level 2, refuting both claims.  It needs
bundle sizes (3,3,2), i.e. m = 8 -- beyond every instance sweep run so far,
which is why those found nothing.

IMPORTANT DISTINCTION.  (I) and (II) are about ONE allocation's set of good
levels.  The chain conjecture is about the EXISTENCE of some allocation good at
every level.  Refuting (I)/(II) therefore does NOT refute the chain conjecture;
it only invalidates the two-level reduction.  This script checks both.

Run:  python verify_cex.py
"""
from itertools import product
import random


def make_instance():
    """n=3, m=8, bundles A1={0,1,2}, A2={3,4,5}, A3={6,7}."""
    A = [frozenset({0, 1, 2}), frozenset({3, 4, 5}), frozenset({6, 7})]
    a = [[0, 0, 0],
         [2, 2, 1],
         [3, 3, 2]]

    def mk(i):
        def c(S):
            return sum(min(len(S & A[j]), a[i][j]) for j in range(3))
        return c

    return A, a, [mk(i) for i in range(3)]


def as_dict(m, f):
    from itertools import combinations
    out = {}
    for k in range(m + 1):
        for s in combinations(range(m), k):
            S = frozenset(s)
            out[S] = f(S)
    return out


def is_dich(m, c):
    from itertools import combinations
    if c[frozenset()] != 0:
        return False
    for k in range(m + 1):
        for s in combinations(range(m), k):
            S = frozenset(s)
            for g in range(m):
                if g not in S and c[S | {g}] - c[S] not in (0, 1):
                    return False
    return True


def ellvec(cs, bd, n):
    W = [[cs[i][bd[i]] - cs[i][bd[j]] for j in range(n)] for i in range(n)]
    e = [0] * n
    for _ in range(n + 1):
        ch = False
        new = list(e)
        for i in range(n):
            for j in range(n):
                if i != j and W[i][j] + e[j] > new[i]:
                    new[i] = W[i][j] + e[j]
                    ch = True
        e = new
        if not ch:
            return e
    return None


def lvl(cs, k):
    return [{S: min(v, k) for S, v in c.items()} for c in cs]


def good(cs, bd, n):
    e = ellvec(cs, bd, n)
    return e is not None and max(e) <= 1


def main():
    m, n = 8, 3
    A, a, fs = make_instance()
    cs = [as_dict(m, f) for f in fs]

    print("=== the instance is legal ===")
    for i in range(n):
        print("  c_%d dichotomous: %s" % (i + 1, is_dich(m, cs[i])))
    print("  cost matrix c_i(A_j):")
    for i in range(n):
        print("    ", [cs[i][A[j]] for j in range(n)], " (target", a[i], ")")

    K = max(max(c.values()) for c in cs)
    print("\n=== the allocation A = (A1,A2,A3) across levels (K=%d) ===" % K)
    flags = []
    for k in range(1, K + 1):
        g = good(lvl(cs, k), A, n)
        e = ellvec(lvl(cs, k), A, n)
        flags.append(g)
        print("  level %d: good=%-5s  ell=%s" % (k, g, e))
    print("  => good-level set: %s   an interval? %s"
          % ([i + 1 for i, v in enumerate(flags) if v],
             "NO -- claims (I) and (II) are FALSE" if (flags[0] and flags[-1]
             and not all(flags)) else "yes"))

    print("\n=== does the CHAIN CONJECTURE survive on this instance? ===")
    # search all partitions of 8 items into 3 bundles for one good at every level
    lv = [lvl(cs, k) for k in range(1, K + 1)]
    found = None
    best_levels = -1
    for assign in product(range(n), repeat=m):
        bd = [frozenset(g for g in range(m) if assign[g] == i) for i in range(n)]
        cnt = 0
        allgood = True
        for L in lv:
            if good(L, bd, n):
                cnt += 1
            else:
                allgood = False
        if cnt > best_levels:
            best_levels = cnt
        if allgood:
            found = bd
            break
    if found:
        print("  YES -- chain witness exists:", [sorted(b) for b in found])
        for k, L in enumerate(lv, start=1):
            print("     level %d: ell=%s" % (k, ellvec(L, found, n)))
    else:
        print("  NO chain witness. best simultaneous levels = %d of %d"
              % (best_levels, K))
        print("  => the CHAIN CONJECTURE IS FALSE on this instance.")


if __name__ == "__main__":
    main()
