"""(NSB): no-stuck WITHIN the balanced region.  Both clauses, if it holds.

(NS) failed (nostuck.py): 846 of 502,528 good partial allocations admit no
good one-chore extension.  But the first stuck state was

    bundles = [[], [0,1,2], []],  unassigned = [3]

-- three chores piled on one agent and two empty.  That is exactly the kind of
state the balance lemma says to avoid, and a construction that keeps the partial
allocation balanced would never reach it.  So the two findings combine:

  (NSB)  if A is a good BALANCED partial allocation of a proper subset of the
         chores, then some unassigned chore can be added to some MINIMUM-size
         bundle leaving the allocation good (and balanced, automatically).

Adding to a minimum-size bundle preserves balance: if sizes lie in {q,q+1}, the
new sizes lie in {q,q+1} as well.  So (NSB) is an induction that stays inside the
balanced region, and it would give:

  - EXISTENCE: from the empty allocation, which is good and balanced, place all m
    chores one at a time, ending at a good balanced allocation -- Conjecture 2
    and the balance lemma together;
  - an ALGORITHM: at each of m steps try all O(mn) pairs (chore, min-size
    bundle), each an O(n^3) test, so O(m^2 n^4), no search, no backtracking.

Reported alongside: whether restricting to minimum-size bundles is essential, by
also allowing insertion into ANY bundle that keeps the result balanced.

Run:  python nostuck_balanced.py
"""
from itertools import product
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


def balanced(bundles):
    sz = [len(b) for b in bundles]
    return max(sz) - min(sz) <= 1


def scan(cs, m, n, stats):
    for assign in product(range(n + 1), repeat=m):
        bundles = tuple(frozenset(g for g in range(m) if assign[g] == i)
                        for i in range(n))
        unass = [g for g in range(m) if assign[g] == n]
        if not unass or not balanced(bundles):
            continue
        if not good_fixed(cs, bundles, n):
            continue
        stats["states"] += 1
        lo = min(len(b) for b in bundles)
        minslots = [i for i in range(n) if len(bundles[i]) == lo]

        ok_min = False
        for g in unass:
            for i in minslots:
                nb = list(bundles)
                nb[i] = bundles[i] | {g}
                if good_fixed(cs, tuple(nb), n):
                    ok_min = True
                    break
            if ok_min:
                break
        if ok_min:
            stats["ok_min"] += 1
        else:
            stats["stuck_min"] += 1
            if "w" not in stats:
                stats["w"] = (cs, m, n, [sorted(b) for b in bundles], unass)

        ok_any = False
        for g in unass:
            for i in range(n):
                nb = list(bundles)
                nb[i] = bundles[i] | {g}
                if balanced(tuple(nb)) and good_fixed(cs, tuple(nb), n):
                    ok_any = True
                    break
            if ok_any:
                break
        if not ok_any:
            stats["stuck_any"] += 1


def main():
    rng = random.Random(1357911)          # same seed as nostuck.py
    stats = Counter()
    for (n, m, T) in [(3, 4, 250), (3, 5, 180), (3, 6, 100), (3, 7, 40),
                      (4, 4, 150), (4, 5, 90), (4, 6, 30), (5, 5, 30)]:
        for _ in range(T):
            cs = (matrix_realising(m, n, rng, 3) if rng.random() < 0.5
                  else [rand_dicho(m, rng, rng.choice([0.0, 0.2, 0.5, 0.8, 1.0]))
                        for _ in range(n)])
            if max(max(x.values()) for x in cs) < 2:
                continue
            stats["inst"] += 1
            scan(cs, m, n, stats)
    print("=== (NSB) over %d instances ===" % stats["inst"])
    print("  good BALANCED partial allocations examined : %d" % stats["states"])
    print("  extendable into a minimum-size bundle      : %d" % stats["ok_min"])
    print("  STUCK (minimum-size bundles only)          : %d" % stats["stuck_min"])
    print("  STUCK (any balance-preserving bundle)      : %d" % stats["stuck_any"])
    print()
    if stats["stuck_min"] == 0:
        print("  *** (NSB) HOLDS.  Induction stays inside the balanced region:")
        print("      it would prove Conjecture 2 AND the balance lemma, and give")
        print("      an O(m^2 n^4) algorithm with no backtracking. ***")
    elif stats["stuck_any"] == 0:
        print("  *** (NSB) holds when insertion may go into ANY balance-preserving")
        print("      bundle, but not into minimum-size bundles only. ***")
    else:
        cs, m, n, b, un = stats["w"]
        print("  (NSB) FAILS. first stuck: n=%d m=%d bundles=%s unassigned=%s"
              % (n, m, b, un))
        for i in range(n):
            print("     agent %d singletons %s"
                  % (i, [cs[i][frozenset({g})] for g in range(m)]))


if __name__ == "__main__":
    main()
