"""Can a good BALANCED allocation be built one chore at a time, staying good?

This is the induction the balance lemma (conj:balance) invites, and it would
serve both open clauses at once: an inductive proof of existence, and a greedy
insertion algorithm.  Precisely, the property tested is

  (INC)  there is a good balanced allocation A, with its assignment FIXED, and an
         ordering g_1,...,g_m of the chores such that for every k the partial
         allocation A restricted to {g_1,...,g_k} is good.

"Good" for a partial allocation means: on the sub-instance of assigned chores,
with the same agent-to-bundle assignment, the envy graph has no positive cycle
and max_i ell_i <= 1.  Restrictions of dichotomous cost functions to a subset of
chores are again dichotomous, so each prefix is a legitimate smaller instance and
(INC) is exactly an induction on m.

Testing is by reachability over subsets: for a fixed allocation A,
    reach(T) = good(A|T) and (T = {} or some g in T has reach(T - g)),
and the instance passes if reach(all chores) holds for SOME good balanced A.

Note (INC) fixes the assignment across prefixes, which is what an induction
needs; it does not allow re-matching at each step.  A weaker variant allowing
re-matching is reported alongside, since if the strict version fails it matters
whether re-matching rescues it.

Run:  python incremental.py
"""
from itertools import product, permutations
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_17")
sys.path.insert(0, "../update_18")
from minimum_subsidy import rand_dicho, matrix_realising  # noqa: E402
from localsearch_lemma import ell_vec  # noqa: E402


def good_fixed(cs, bundles, n, T):
    """Is A|T good under the FIXED assignment (agent i holds bundles[i])?"""
    a = [[cs[i][bundles[j] & T] for j in range(n)] for i in range(n)]
    e = ell_vec(a, n)
    return e is not None and max(e) <= 1


def good_rematch(cs, bundles, n, T, perms):
    """Is A|T good under SOME assignment (re-matching allowed)?"""
    for perm in perms:
        a = [[cs[i][bundles[perm[j]] & T] for j in range(n)] for i in range(n)]
        e = ell_vec(a, n)
        if e is not None and max(e) <= 1:
            return True
    return False


def incremental_ok(cs, bundles, n, m, rematch, perms):
    """Reachability of the full set under one-chore-at-a-time growth."""
    full = frozenset(range(m))
    memo = {}

    def gd(T):
        if T not in memo:
            memo[T] = (good_rematch(cs, bundles, n, T, perms) if rematch
                       else good_fixed(cs, bundles, n, T))
        return memo[T]

    if not gd(full):
        return False
    reach = {frozenset(): True}
    order = sorted((frozenset(s) for k in range(m + 1)
                    for s in __import__("itertools").combinations(range(m), k)),
                   key=len)
    for T in order:
        if not T:
            continue
        if not gd(T):
            reach[T] = False
            continue
        reach[T] = any(reach[T - {g}] for g in T)
    return reach[full]


def analyse(cs, m, n, perms):
    """(inc_fixed, inc_rematch, has_good_balanced)."""
    q, r = divmod(m, n)
    sizes_ok = lambda b: max(len(x) for x in b) - min(len(x) for x in b) <= 1
    has_good = False
    inc_f = inc_r = False
    for assign in product(range(n), repeat=m):
        bundles = tuple(frozenset(g for g in range(m) if assign[g] == i)
                        for i in range(n))
        if not sizes_ok(bundles):
            continue
        a = [[cs[i][bundles[j]] for j in range(n)] for i in range(n)]
        e = ell_vec(a, n)
        if e is None or max(e) > 1:
            continue
        has_good = True
        if not inc_f and incremental_ok(cs, bundles, n, m, False, perms):
            inc_f = True
        if not inc_r and incremental_ok(cs, bundles, n, m, True, perms):
            inc_r = True
        if inc_f and inc_r:
            break
    return inc_f, inc_r, has_good


def main():
    rng = random.Random(97531)
    tot = 0
    nogood = 0
    fail_f = 0
    fail_r = 0
    first = None
    print("=== (INC): can a good balanced allocation be grown chore by chore? ===")
    print("   n   m   instances   fixed-assignment fails   re-matching fails")
    for (n, m, T) in [(3, 4, 300), (3, 5, 220), (3, 6, 150), (3, 7, 70),
                      (4, 4, 200), (4, 5, 120), (4, 6, 50), (5, 5, 40)]:
        perms = list(permutations(range(n)))
        ff = fr = cnt = 0
        for _ in range(T):
            cs = (matrix_realising(m, n, rng, 3) if rng.random() < 0.5
                  else [rand_dicho(m, rng, rng.choice([0.0, 0.2, 0.5, 0.8, 1.0]))
                        for _ in range(n)])
            if max(max(x.values()) for x in cs) < 2:
                continue
            cnt += 1
            tot += 1
            f, r_, hg = analyse(cs, m, n, perms)
            if not hg:
                nogood += 1
            if not f:
                ff += 1
                fail_f += 1
                if first is None:
                    first = (cs, m, n)
            if not r_:
                fr += 1
                fail_r += 1
        print("  %2d  %2d   %7d   %20d   %17d" % (n, m, cnt, ff, fr))
    print()
    print("  instances                              : %d" % tot)
    print("  with no good balanced allocation       : %d" % nogood)
    print("  (INC) fails, fixed assignment          : %d" % fail_f)
    print("  (INC) fails, re-matching allowed       : %d" % fail_r)
    if fail_f == 0:
        print("\n  *** (INC) holds with a FIXED assignment -- induction on m is available ***")
    elif fail_r == 0:
        print("\n  *** (INC) holds only when re-matching is allowed ***")
    elif first:
        cs, m, n = first
        print("\n  first failure: n=%d m=%d" % (n, m))
        for i in range(n):
            print("     agent %d singletons %s"
                  % (i, [cs[i][frozenset({g})] for g in range(m)]))


if __name__ == "__main__":
    main()
