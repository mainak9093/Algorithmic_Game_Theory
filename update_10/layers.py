"""A novel angle: decompose each cost function into LAYERS.

OBSERVATION.  Every dichotomous cost c (monotone, c(0)=0, unit increments) is a
sum of nested monotone Boolean indicators.  Put F_t := {S : c(S) >= t}.  Each
F_t is upward-closed, F_1 ⊇ F_2 ⊇ ... ⊇ F_K with K = c(M), and

        c(S) = #{ t : S in F_t } = sum_t 1[S in F_t].

Moreover every truncation min(c, k) is itself dichotomous.  So a dichotomous
cost is a stack of K monotone Boolean functions, and the stack can be peeled one
layer at a time WITHOUT leaving the class.

WHY THIS IS INTERESTING HERE.  A one-layer instance is exactly one where every
c_i is 0/1-valued, hence every bundle costs at most 1 to everybody -- which is
the hypothesis of the small-bundle theorem just proved.  So:

        K = 1  is already SOLVED, unconditionally, for every n.

That makes "induct on the number of layers K" a genuine proof strategy with a
proved base case, and one that has not been tried.  This script verifies the
decomposition facts and then probes the inductive step: how do good allocations
of the truncated instance min(c_i, K-1) relate to good allocations of the full
instance?

Run:  python layers.py
"""
from itertools import combinations, combinations_with_replacement, product
import random


def subsets(m):
    return [frozenset(s) for k in range(m + 1) for s in combinations(range(m), k)]


def gen_functions(m):
    subs = sorted(subsets(m), key=lambda s: (len(s), sorted(s)))
    res, val = [], {}

    def rec(i):
        if i == len(subs):
            res.append(dict(val)); return
        S = subs[i]
        if len(S) == 0:
            val[S] = 0; rec(i + 1); del val[S]; return
        lo, hi = 0, 10 ** 9
        for g in S:
            T = S - {g}
            lo = max(lo, val[T]); hi = min(hi, val[T] + 1)
        for x in range(lo, hi + 1):
            val[S] = x; rec(i + 1)
        del val[S]

    rec(0)
    return res


def is_dich(m, c):
    if c[frozenset()] != 0:
        return False
    for S in subsets(m):
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
                    new[i] = W[i][j] + e[j]; ch = True
        e = new
        if not ch:
            return e
    return None


def allocs(m, n):
    for a in product(range(n), repeat=m):
        yield [frozenset(g for g in range(m) if a[g] == i) for i in range(n)]


def good(cs, bd, n):
    e = ellvec(cs, bd, n)
    return e is not None and max(e) <= 1


def trunc(c, k):
    return {S: min(v, k) for S, v in c.items()}


def layers_of(m, c):
    """The nested upward-closed families F_t as a list of sets of subsets."""
    K = max(c.values())
    return [frozenset(S for S in subsets(m) if c[S] >= t) for t in range(1, K + 1)]


def main():
    m = 3
    F = gen_functions(m)
    print("dichotomous functions on %d items: %d" % (m, len(F)))

    # ---- 1. the decomposition is exact, layers nested and upward-closed ----
    bad = 0
    for c in F:
        L = layers_of(m, c)
        for S in subsets(m):
            if c[S] != sum(1 for Ft in L if S in Ft):
                bad += 1
        for t, Ft in enumerate(L):
            for S in Ft:                              # upward closed
                for g in range(m):
                    if S | {g} not in Ft:
                        bad += 1
            if t + 1 < len(L) and not (L[t + 1] <= Ft):   # nested
                bad += 1
    print("decomposition c = sum_t 1[. in F_t], nested & upward-closed : %d violations"
          % bad)

    # ---- 2. every truncation stays dichotomous ----
    bad = 0
    for c in F:
        for k in range(0, max(c.values()) + 1):
            if not is_dich(m, trunc(c, k)):
                bad += 1
    print("every truncation min(c,k) is dichotomous                    : %d violations"
          % bad)

    # ---- 3. K = 1 is exactly the small-bundle regime ----
    bad = 0
    for cs in combinations_with_replacement([c for c in F if max(c.values()) <= 1], 3):
        cs = list(cs)
        ok = any(good(cs, bd, 3) for bd in allocs(m, 3))
        if not ok:
            bad += 1
    print("K=1 instances (n=3): counterexamples                        : %d" % bad)

    # ---- 4. probe the inductive step ----
    # For instances of depth K, compare good allocations of the truncation
    # min(c_i, K-1) with good allocations of the full instance.
    print("\n--- probing the inductive step (n=3, m=3) ---")
    both = only_full = only_trunc = neither = 0
    shared = 0
    tot = 0
    rng = random.Random(0)
    pool = [c for c in F if max(c.values()) >= 2]
    for cs in combinations_with_replacement(pool, 3):
        cs = list(cs)
        K = max(max(c.values()) for c in cs)
        tr = [trunc(c, K - 1) for c in cs]
        gf = {tuple(sorted(tuple(sorted(b)) for b in bd))
              for bd in allocs(m, 3) if good(cs, bd, 3)}
        gt = {tuple(sorted(tuple(sorted(b)) for b in bd))
              for bd in allocs(m, 3) if good(tr, bd, 3)}
        tot += 1
        if gf & gt:
            shared += 1
        if gf and gt:
            both += 1
        elif gf:
            only_full += 1
        elif gt:
            only_trunc += 1
        else:
            neither += 1
    print("  instances of depth K>=2                    : %d" % tot)
    print("  both full and truncation solvable          : %d" % both)
    print("  full solvable, truncation not              : %d" % only_full)
    print("  truncation solvable, full not              : %d" % only_trunc)
    print("  neither                                    : %d" % neither)
    print("  share at least one COMMON good allocation  : %d  (%.1f%%)"
          % (shared, 100.0 * shared / tot))


if __name__ == "__main__":
    main()
