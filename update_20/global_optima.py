"""Which GLOBAL optimum is always good?  (existence without local search)

Approach 7 stalled because the descent lemma is strictly stronger than
Conjecture 2 -- it forbids bad LOCAL minima -- and the repairing transfer turned
out not to be local to the envy.  The global route asks instead: is there an
objective whose GLOBAL optimum is always a good allocation?  That would give
existence directly, and the polynomial-time clause becomes a separate question
about computing (or approximating) the optimum.

Candidates, each over all partitions in canonical form (min-cost matching, hence
envy-freeable, so ell is finite):

  U   utilitarian     minimise sum_i c_i(B_i)                    [control: known
                      not to be good in general -- Approach 6]
  E   egalitarian     minimise max_i c_i(B_i)
  L   leximax cost    minimise the cost vector sorted DESCENDING, lexicographically
  B   balance         minimise sum_i |B_i|^2
  EB  (E, B)          egalitarian, ties broken by balance
  LB  (L, B)          leximax, ties broken by balance
  BU  (B, U)          balance, ties broken by utilitarian cost
  SP  spread          minimise max_i c_i(B_i) - min_i c_i(B_i)

For each objective two things are reported:
    ALL   every optimum is good  (the clean theorem: "any optimum works")
    SOME  at least one optimum is good  (needs a tie-break to be a theorem)

Run:  python global_optima.py
"""
from itertools import product, permutations
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_17")
sys.path.insert(0, "../update_18")
from minimum_subsidy import rand_dicho, matrix_realising  # noqa: E402
from localsearch_lemma import ell_vec  # noqa: E402

OBJ = ["U", "E", "L", "B", "EB", "LB", "BU", "SP"]


def canon(cs, bundles, n, perms):
    best = None
    for perm in perms:
        t = sum(cs[i][bundles[perm[i]]] for i in range(n))
        if best is None or t < best[0]:
            best = (t, perm)
    tot, perm = best
    a = [[cs[i][bundles[perm[j]]] for j in range(n)] for i in range(n)]
    e = ell_vec(a, n)
    costs = [a[i][i] for i in range(n)]
    return e, costs, tot


def objective(name, costs, tot, bundles):
    sq = sum(len(b) ** 2 for b in bundles)
    srt = tuple(sorted(costs, reverse=True))
    return {"U": (tot,),
            "E": (max(costs),),
            "L": srt,
            "B": (sq,),
            "EB": (max(costs), sq),
            "LB": srt + (sq,),
            "BU": (sq, tot),
            "SP": (max(costs) - min(costs),)}[name]


def analyse(cs, m, n, perms):
    """Return dict name -> (all_good, some_good) plus whether any allocation is good."""
    recs = []
    any_good = False
    for assign in product(range(n), repeat=m):
        bundles = tuple(frozenset(g for g in range(m) if assign[g] == i)
                        for i in range(n))
        e, costs, tot = canon(cs, bundles, n, perms)
        if e is None:
            continue
        good = max(e) <= 1
        any_good |= good
        recs.append((bundles, costs, tot, good))
    out = {}
    for name in OBJ:
        best = None
        for bundles, costs, tot, good in recs:
            v = objective(name, costs, tot, bundles)
            if best is None or v < best:
                best = v
        allg = someg = None
        for bundles, costs, tot, good in recs:
            if objective(name, costs, tot, bundles) == best:
                allg = good if allg is None else (allg and good)
                someg = good if someg is None else (someg or good)
        out[name] = (allg, someg)
    return out, any_good


def main():
    rng = random.Random(313131)
    allfail = Counter()
    somefail = Counter()
    tot = 0
    nogood = 0
    firstfail = {}
    for (n, m, T) in [(3, 4, 500), (3, 5, 350), (3, 6, 200), (3, 7, 90),
                      (4, 4, 300), (4, 5, 200), (4, 6, 80),
                      (5, 5, 70)]:
        perms = list(permutations(range(n)))
        for _ in range(T):
            cs = (matrix_realising(m, n, rng, 3) if rng.random() < 0.5
                  else [rand_dicho(m, rng, rng.choice([0.0, 0.2, 0.5, 0.8, 1.0]))
                        for _ in range(n)])
            if max(max(x.values()) for x in cs) < 2:
                continue
            tot += 1
            res, any_good = analyse(cs, m, n, perms)
            if not any_good:
                nogood += 1
            for name in OBJ:
                allg, someg = res[name]
                if not allg:
                    allfail[name] += 1
                if not someg:
                    somefail[name] += 1
                    if name not in firstfail:
                        firstfail[name] = (m, n)
    print("=== global optima over %d instances (0 lacking a good allocation: %d) ==="
          % (tot, nogood))
    print("  obj  description                              ALL-optima-good  SOME-optimum-good")
    desc = {"U": "min total cost (control)",
            "E": "min max cost (egalitarian)",
            "L": "leximax cost vector",
            "B": "min sum |B_i|^2 (most balanced)",
            "EB": "egalitarian, balance tie-break",
            "LB": "leximax, balance tie-break",
            "BU": "balance, cost tie-break",
            "SP": "min cost spread"}
    for name in OBJ:
        print("  %-3s  %-40s  %6d fail      %6d fail"
              % (name, desc[name], allfail[name], somefail[name]))
    print()
    for name in OBJ:
        if somefail[name] == 0:
            star = "ALL" if allfail[name] == 0 else "SOME"
            print("  *** %s : every instance has a good optimum (%s) ***" % (name, star))
    if all(somefail[n] for n in OBJ):
        print("  every objective has an instance whose optima are all bad")


if __name__ == "__main__":
    main()
