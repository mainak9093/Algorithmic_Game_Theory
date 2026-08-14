"""Two questions raised by global_optima.py.

(1) THE BALANCE LEMMA.  The optima of the objective "minimise sum_i |B_i|^2" are
    exactly the BALANCED partitions (all bundle sizes within 1 of each other).
    "Some optimum is good" therefore reads

        every instance has a good balanced allocation,

    with zero failures over 1,760 instances.  If true this is a clean structural
    restriction -- it says Conjecture 2 may be proved on balanced partitions
    alone, where every bundle has size floor(m/n) or ceil(m/n).  Stressed here on
    larger m and on EF-free instances, where the claim is not vacuous.

(2) A COMPLETE TIE-BREAK.  "Some optimum is good" is not yet a theorem; one wants
    a lexicographic chain of objectives whose optima are ALL good, so that the
    rule names a specific allocation.  Chains tested below.

Objectives:  B = sum|B_i|^2,  U = total cost,  E = max cost,  L = cost vector
sorted descending,  S = max cost - min cost,  N = #agents attaining max cost.

Run:  python balance_lemma.py
"""
from itertools import product, permutations
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_17")
sys.path.insert(0, "../update_18")
from minimum_subsidy import rand_dicho, matrix_realising  # noqa: E402
from localsearch_lemma import ell_vec  # noqa: E402

CHAINS = [("B",), ("B", "U"), ("B", "E"), ("B", "E", "U"), ("B", "U", "E"),
          ("B", "L"), ("B", "L", "U"), ("E", "B"), ("E", "B", "U"),
          ("B", "S"), ("B", "N", "U"), ("B", "E", "L", "U")]


def canon(cs, bundles, n, perms):
    best = None
    for perm in perms:
        t = sum(cs[i][bundles[perm[i]]] for i in range(n))
        if best is None or t < best[0]:
            best = (t, perm)
    tot, perm = best
    a = [[cs[i][bundles[perm[j]]] for j in range(n)] for i in range(n)]
    return ell_vec(a, n), [a[i][i] for i in range(n)], tot


def comp(name, costs, tot, bundles):
    if name == "B":
        return (sum(len(b) ** 2 for b in bundles),)
    if name == "U":
        return (tot,)
    if name == "E":
        return (max(costs),)
    if name == "L":
        return tuple(sorted(costs, reverse=True))
    if name == "S":
        return (max(costs) - min(costs),)
    if name == "N":
        return (sum(1 for c in costs if c == max(costs)),)
    raise ValueError(name)


def key(chain, costs, tot, bundles):
    k = ()
    for name in chain:
        k = k + comp(name, costs, tot, bundles)
    return k


def analyse(cs, m, n, perms):
    recs = []
    for assign in product(range(n), repeat=m):
        bundles = tuple(frozenset(g for g in range(m) if assign[g] == i)
                        for i in range(n))
        e, costs, tot = canon(cs, bundles, n, perms)
        if e is None:
            continue
        recs.append((bundles, costs, tot, max(e) <= 1))
    # (1) balance lemma
    bal = [r for r in recs
           if max(len(b) for b in r[0]) - min(len(b) for b in r[0]) <= 1]
    bal_ok = any(r[3] for r in bal)
    # (2) chains
    out = {}
    for ch in CHAINS:
        best = min(key(ch, c, t, b) for b, c, t, _ in recs)
        opt = [g for b, c, t, g in recs if key(ch, c, t, b) == best]
        out[ch] = (all(opt), any(opt))
    return bal_ok, len(bal), out


def main():
    rng = random.Random(4242424)
    tot = 0
    bal_fail = 0
    bal_pop = 0
    effree = 0
    eff_bal_fail = 0
    allfail = Counter()
    somefail = Counter()
    for (n, m, T) in [(3, 5, 300), (3, 6, 220), (3, 7, 130), (3, 8, 60),
                      (4, 5, 200), (4, 6, 90), (4, 7, 35), (5, 5, 60)]:
        perms = list(permutations(range(n)))
        for _ in range(T):
            cs = (matrix_realising(m, n, rng, 3) if rng.random() < 0.5
                  else [rand_dicho(m, rng, rng.choice([0.0, 0.2, 0.5, 0.8, 1.0]))
                        for _ in range(n)])
            if max(max(x.values()) for x in cs) < 2:
                continue
            tot += 1
            ok, npop, chains = analyse(cs, m, n, perms)
            bal_pop += npop
            if not ok:
                bal_fail += 1
                print("  !! NO good BALANCED allocation: n=%d m=%d" % (n, m))
            # EF-free subpopulation
            ef = any(all(cs[i][bd[i]] <= cs[i][bd[j]]
                         for i in range(n) for j in range(n))
                     for bd in [tuple(frozenset(g for g in range(m) if a[g] == i)
                                      for i in range(n))
                                for a in product(range(n), repeat=m)])
            if not ef:
                effree += 1
                if not ok:
                    eff_bal_fail += 1
            for ch in CHAINS:
                a, s = chains[ch]
                if not a:
                    allfail[ch] += 1
                if not s:
                    somefail[ch] += 1
    print("=== (1) balance lemma over %d instances ===" % tot)
    print("  balanced partitions examined      : %d" % bal_pop)
    print("  instances with NO good balanced allocation : %d" % bal_fail)
    print("  of which EF-free instances (%d tested)      : %d"
          % (effree, eff_bal_fail))
    print()
    print("=== (2) lexicographic chains: are ALL optima good? ===")
    print("  chain                        ALL fail   SOME fail")
    for ch in CHAINS:
        print("  %-28s %6d     %6d"
              % ("->".join(ch), allfail[ch], somefail[ch]))
    print()
    win = [ch for ch in CHAINS if allfail[ch] == 0]
    if win:
        for ch in win:
            print("  *** %s : EVERY optimum is good -- candidate theorem ***"
                  % "->".join(ch))
    else:
        print("  no chain tested has all optima good")


if __name__ == "__main__":
    main()
