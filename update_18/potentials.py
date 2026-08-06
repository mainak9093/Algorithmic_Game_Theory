"""Which lexicographic potential makes the local-search lemma true?

localsearch_lemma.py refuted (L) for
    Psi = (max ell, #at max, total cost),
and the witness says why: at bundles [[0,1,2,3],[],[]] with capped costs, every
single transfer leaves max ell = 2 and RAISES the total cost, so the third
component pins the search at a utilitarian optimum -- exactly the class already
known not to be good.  The diagnosis is that the tie-break must reward
SPREADING chores out, not minimising their total cost.

Candidate potentials, all lexicographic, all on top of the canonical min-cost
reassignment (which is what makes every partition envy-freeable):

    P1  (max ell, #at max, total cost)          -- refuted, kept as control
    P2  (max ell, #at max, max bundle size)
    P3  (max ell, #at max, sum |A_i|^2)
    P4  (max ell, sum ell, sum |A_i|^2)
    P5  (sorted ell descending, sum |A_i|^2)

For each, (L_P) is: every partition with max ell >= 2 admits a single-chore
transfer strictly decreasing P.  (L_P) implies Conjecture 2, since P is bounded
below and strictly decreases, so descent terminates only at max ell <= 1.

Run:  python potentials.py
"""
from itertools import product, permutations
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_17")
from minimum_subsidy import rand_dicho, matrix_realising  # noqa: E402
from localsearch_lemma import ell_vec, moves  # noqa: E402


def state(cs, bundles, n):
    """Canonical min-cost reassignment; return (ell, total cost)."""
    best = None
    for perm in permutations(range(n)):
        tot = sum(cs[i][bundles[perm[i]]] for i in range(n))
        if best is None or tot < best[0]:
            best = (tot, perm)
    tot, perm = best
    a = [[cs[i][bundles[perm[j]]] for j in range(n)] for i in range(n)]
    return ell_vec(a, n), tot


POTENTIALS = ["P1", "P2", "P3", "P4", "P5"]


def psi(name, e, tot, bundles):
    mx = max(e)
    cnt = sum(1 for x in e if x == mx)
    sizes = sorted((len(b) for b in bundles), reverse=True)
    sq = sum(len(b) ** 2 for b in bundles)
    if name == "P1":
        return (mx, cnt, tot)
    if name == "P2":
        return (mx, cnt, sizes[0])
    if name == "P3":
        return (mx, cnt, sq)
    if name == "P4":
        return (mx, sum(e), sq)
    if name == "P5":
        return (tuple(sorted(e, reverse=True)), sq)
    raise ValueError(name)


def test(cs, m, n):
    """For each potential, count partitions with max ell >= 2 and no improving move."""
    memo = {}

    def get(bundles):
        key = tuple(sorted(tuple(sorted(b)) for b in bundles))
        if key not in memo:
            memo[key] = state(cs, bundles, n)
        return memo[key]

    stuck = Counter()
    for assign in product(range(n), repeat=m):
        bundles = tuple(frozenset(g for g in range(m) if assign[g] == i)
                        for i in range(n))
        e, tot = get(bundles)
        if e is None or max(e) <= 1:
            continue
        nbrs = [(nb,) + get(nb) for nb in moves(bundles, n, m, swaps=False)]
        for name in POTENTIALS:
            cur = psi(name, e, tot, bundles)
            if not any(ne is not None and psi(name, ne, nt, nb) < cur
                       for nb, ne, nt in nbrs):
                stuck[name] += 1
    return stuck


def main():
    rng = random.Random(24680)
    tot = 0
    fails = Counter()
    stuckparts = Counter()
    first = {}
    for (n, m, T) in [(3, 4, 700), (3, 5, 400), (3, 6, 120),
                      (4, 4, 400), (4, 5, 120)]:
        for _ in range(T):
            cs = (matrix_realising(m, n, rng, 3) if rng.random() < 0.55
                  else [rand_dicho(m, rng, rng.choice([0.0, 0.15, 0.5, 0.85, 1.0]))
                        for _ in range(n)])
            if max(max(c.values()) for c in cs) < 1:
                continue
            tot += 1
            st = test(cs, m, n)
            for name in POTENTIALS:
                if st[name]:
                    fails[name] += 1
                    stuckparts[name] += st[name]
                    if name not in first:
                        first[name] = (cs, m, n)
    print("=== lemma (L_P) over %d instances ===" % tot)
    print("  potential   instances with a stuck partition   stuck partitions")
    for name in POTENTIALS:
        print("    %-4s      %6d  (%.2f%%)                    %d"
              % (name, fails[name], 100.0 * fails[name] / tot, stuckparts[name]))
    print()
    for name in POTENTIALS:
        if fails[name] == 0:
            print("  *** %s : NO stuck partition -- (L_%s) survives; this would"
                  " prove Conjecture 2 if provable ***" % (name, name))
    if all(fails[name] for name in POTENTIALS):
        print("  every candidate potential has stuck partitions")


if __name__ == "__main__":
    main()
