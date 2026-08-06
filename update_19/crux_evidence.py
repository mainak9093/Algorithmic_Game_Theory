"""How much evidence does the HARD HALF of the descent lemma actually have?

lem:balance-dichotomy splits Conjecture conj:descent in two.  On a balanced
partition (all bundle sizes within 1) no transfer can decrease sum |B_i|^2, so
the descent lemma must strictly decrease max_i ell_i by a single transfer.  That
is the crux.

The "zero stuck partitions" evidence in Approach 7 is over ALL partitions, and
says nothing on its own about how many of them were balanced WITH max ell >= 2.
If that subpopulation is thin, the crux is essentially untested and a proof
attempt is premature.  Measured here:

    - number of partitions that are balanced and have max ell >= 2  (the crux
      population), broken down by (n, m);
    - among those, how many admit a transfer strictly reducing max ell;
    - m = n and m = 2n are singled out: when m = n a balanced partition gives
      every agent exactly one chore, the most rigid case of all.

Balanced := max_i |B_i| - min_i |B_i| <= 1.

Run:  python crux_evidence.py
"""
from itertools import product, permutations
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_17")
sys.path.insert(0, "../update_18")
from minimum_subsidy import rand_dicho, matrix_realising  # noqa: E402
from localsearch_lemma import ell_vec, moves  # noqa: E402


def state(cs, bundles, n, perms):
    best = None
    for perm in perms:
        t = sum(cs[i][bundles[perm[i]]] for i in range(n))
        if best is None or t < best[0]:
            best = (t, perm)
    t, perm = best
    a = [[cs[i][bundles[perm[j]]] for j in range(n)] for i in range(n)]
    return ell_vec(a, n)


def balanced(bundles):
    sz = [len(b) for b in bundles]
    return max(sz) - min(sz) <= 1


def scan(cs, m, n, perms):
    memo = {}

    def get(b):
        k = tuple(sorted(tuple(sorted(x)) for x in b))
        if k not in memo:
            memo[k] = state(cs, b, n, perms)
        return memo[k]

    crux = 0
    crux_fail = 0
    witness = None
    for assign in product(range(n), repeat=m):
        bundles = tuple(frozenset(g for g in range(m) if assign[g] == i)
                        for i in range(n))
        if not balanced(bundles):
            continue
        e = get(bundles)
        if e is None or max(e) <= 1:
            continue
        crux += 1
        mx = max(e)
        ok = False
        for nb in moves(bundles, n, m, swaps=False):
            ne = get(nb)
            if ne is not None and max(ne) < mx:
                ok = True
                break
        if not ok:
            crux_fail += 1
            if witness is None:
                witness = (bundles, e)
    return crux, crux_fail, witness


def main():
    rng = random.Random(606060)
    print("=== crux population: BALANCED partitions with max ell >= 2 ===")
    print("   n   m   instances    crux partitions   no max-ell-reducing transfer")
    grand = grandfail = 0
    firstw = None
    for (n, m, T) in [(3, 3, 500), (3, 4, 400), (3, 6, 250), (3, 9, 60),
                      (4, 4, 400), (4, 6, 120), (4, 8, 30),
                      (5, 5, 120), (5, 6, 40)]:
        perms = list(permutations(range(n)))
        c = f = cnt = 0
        for _ in range(T):
            cs = (matrix_realising(m, n, rng, 3) if rng.random() < 0.5
                  else [rand_dicho(m, rng, rng.choice([0.0, 0.2, 0.5, 0.8, 1.0]))
                        for _ in range(n)])
            if max(max(x.values()) for x in cs) < 2:
                continue
            cnt += 1
            a, b, w = scan(cs, m, n, perms)
            c += a
            f += b
            if b and firstw is None:
                firstw = (cs, m, n, w)
        grand += c
        grandfail += f
        print("  %2d  %2d   %7d    %13d   %s"
              % (n, m, cnt, c, f if f else "0"))
    print()
    print("  crux partitions examined : %d" % grand)
    print("  with NO max-ell-reducing transfer : %d" % grandfail)
    if firstw:
        cs, m, n, w = firstw
        bundles, e = w
        print("\n  *** CRUX FAILURE (refutes conj:descent) ***")
        print("  n=%d m=%d bundles=%s ell=%s"
              % (n, m, [sorted(b) for b in bundles], e))
        for i in range(n):
            print("     agent %d singletons %s"
                  % (i, [cs[i][frozenset({g})] for g in range(m)]))
    else:
        print("  no crux failure found")


if __name__ == "__main__":
    main()
