"""(NS): is greedy insertion ever stuck?  This would settle BOTH clauses.

(INC) (incremental.py) says a good balanced allocation can be grown chore by
chore.  But it presupposes that a good allocation exists, so it structures the
witness rather than proving existence.  The statement that would prove existence
is stronger and self-contained:

  (NS)  if A is a good allocation of a PROPER subset T of the chores, then there
        are a chore g outside T and an agent i such that A with g added to
        bundle i is still good.

(NS) implies Conjecture 2 outright, by induction from the empty allocation --
which is good, all costs being 0 -- adding one chore at a time until every chore
is placed.  It also gives a polynomial algorithm: at each of m steps try all
O(mn) pairs (g,i), each test an O(n^3) longest-path computation, so O(m^2 n^4)
overall, with no search and no backtracking.

"Good" = the envy graph of the partial allocation (only assigned chores count)
has no positive cycle and max_i ell_i <= 1.  The assignment is FIXED: bundle i
belongs to agent i throughout, so no re-matching is used.  A variant permitting
re-matching is reported too, since it is a weaker and still algorithmic claim.

Tested exhaustively: every partial allocation of every instance, i.e. all
(n+1)^m maps from chores to agents-or-unassigned.

Run:  python nostuck.py
"""
from itertools import product, permutations
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_17")
sys.path.insert(0, "../update_18")
from minimum_subsidy import rand_dicho, matrix_realising  # noqa: E402
from localsearch_lemma import ell_vec  # noqa: E402


def good_fixed(cs, bundles, n):
    a = [[cs[i][bundles[j]] for j in range(n)] for i in range(n)]
    e = ell_vec(a, n)
    return e is not None and max(e) <= 1


def good_rematch(cs, bundles, n, perms):
    for perm in perms:
        a = [[cs[i][bundles[perm[j]]] for j in range(n)] for i in range(n)]
        e = ell_vec(a, n)
        if e is not None and max(e) <= 1:
            return True
    return False


def scan(cs, m, n, perms, stats):
    """Check (NS) at every good partial allocation."""
    for assign in product(range(n + 1), repeat=m):      # n = unassigned
        bundles = tuple(frozenset(g for g in range(m) if assign[g] == i)
                        for i in range(n))
        unass = [g for g in range(m) if assign[g] == n]
        if not unass:
            continue
        if not good_fixed(cs, bundles, n):
            continue
        stats["states"] += 1
        ok = False
        for g in unass:
            for i in range(n):
                nb = list(bundles)
                nb[i] = bundles[i] | {g}
                if good_fixed(cs, tuple(nb), n):
                    ok = True
                    break
            if ok:
                break
        if ok:
            stats["ns_fixed"] += 1
        else:
            stats["stuck_fixed"] += 1
            if "w" not in stats:
                stats["w"] = (cs, m, n, [sorted(b) for b in bundles], unass)
        # re-matching variant
        okr = False
        for g in unass:
            for i in range(n):
                nb = list(bundles)
                nb[i] = bundles[i] | {g}
                if good_rematch(cs, tuple(nb), n, perms):
                    okr = True
                    break
            if okr:
                break
        if not okr:
            stats["stuck_rematch"] += 1


def main():
    rng = random.Random(1357911)
    stats = Counter()
    for (n, m, T) in [(3, 4, 250), (3, 5, 180), (3, 6, 100), (3, 7, 40),
                      (4, 4, 150), (4, 5, 90), (4, 6, 30), (5, 5, 30)]:
        perms = list(permutations(range(n)))
        for _ in range(T):
            cs = (matrix_realising(m, n, rng, 3) if rng.random() < 0.5
                  else [rand_dicho(m, rng, rng.choice([0.0, 0.2, 0.5, 0.8, 1.0]))
                        for _ in range(n)])
            if max(max(x.values()) for x in cs) < 2:
                continue
            stats["inst"] += 1
            scan(cs, m, n, perms, stats)
    print("=== (NS) over %d instances ===" % stats["inst"])
    print("  good PARTIAL allocations examined (proper subsets) : %d" % stats["states"])
    print("  extendable, fixed assignment                       : %d" % stats["ns_fixed"])
    print("  STUCK, fixed assignment                            : %d" % stats["stuck_fixed"])
    print("  STUCK, re-matching allowed                         : %d" % stats["stuck_rematch"])
    print()
    if stats["stuck_fixed"] == 0:
        print("  *** (NS) HOLDS with a fixed assignment.  This would prove")
        print("      Conjecture 2 by induction and give an O(m^2 n^4) algorithm. ***")
    elif stats["stuck_rematch"] == 0:
        print("  *** (NS) holds only when re-matching is allowed. ***")
    else:
        cs, m, n, b, un = stats["w"]
        print("  (NS) FAILS.  first stuck state: n=%d m=%d bundles=%s unassigned=%s"
              % (n, m, b, un))
        for i in range(n):
            print("     agent %d singletons %s"
                  % (i, [cs[i][frozenset({g})] for g in range(m)]))
        print()
        print("  greedy insertion can paint itself into a corner, so an algorithm")
        print("  needs backtracking or a rule for WHICH chore to place next.")


if __name__ == "__main__":
    main()
