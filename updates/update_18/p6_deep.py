"""Push the two-component potential P6 to larger m.

P6 = (max_i ell_i, sum_i |A_i|^2), lexicographic, on top of the canonical
min-cost reassignment.  It survived 253 EF-free instances and R10's certified
family with zero stuck partitions.  The obvious way for a SIZE-based potential to
fail is large bundles: sum |A_i|^2 strictly decreases only when a chore moves
from a bundle of size s to one of size t with t < s-1, and dichotomous costs cap,
so a huge bundle can be cheap.  That failure mode needs m well above n, which the
earlier runs (m <= 6) barely reached.

Tested here, exhaustively over all n^m partitions:
    n=3, m up to 9 ;  n=4, m up to 7 ;  n=5, m up to 6.
Reported per (n,m) so any threshold effect in m is visible rather than averaged
away.  P3 is carried along as a control.

Run:  python p6_deep.py
"""
from itertools import product, permutations
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_17")
from minimum_subsidy import rand_dicho, matrix_realising  # noqa: E402
from localsearch_lemma import ell_vec, moves  # noqa: E402


def psi6(e, bundles):
    return (max(e), sum(len(b) ** 2 for b in bundles))


def psi3(e, bundles):
    mx = max(e)
    return (mx, sum(1 for x in e if x == mx), sum(len(b) ** 2 for b in bundles))


def state(cs, bundles, n, perms):
    best = None
    for perm in perms:
        t = sum(cs[i][bundles[perm[i]]] for i in range(n))
        if best is None or t < best[0]:
            best = (t, perm)
    t, perm = best
    a = [[cs[i][bundles[perm[j]]] for j in range(n)] for i in range(n)]
    return ell_vec(a, n)


def test(cs, m, n, perms):
    memo = {}

    def get(b):
        k = tuple(sorted(tuple(sorted(x)) for x in b))
        if k not in memo:
            memo[k] = state(cs, b, n, perms)
        return memo[k]

    s6 = s3 = 0
    good = False
    worst = None
    for assign in product(range(n), repeat=m):
        bundles = tuple(frozenset(g for g in range(m) if assign[g] == i)
                        for i in range(n))
        e = get(bundles)
        if e is None:
            continue
        if max(e) <= 1:
            good = True
            continue
        nbrs = []
        for nb in moves(bundles, n, m, swaps=False):
            ne = get(nb)
            if ne is not None:
                nbrs.append((nb, ne))
        if not any(psi6(ne, nb) < psi6(e, bundles) for nb, ne in nbrs):
            s6 += 1
            if worst is None:
                worst = (bundles, e)
        if not any(psi3(ne, nb) < psi3(e, bundles) for nb, ne in nbrs):
            s3 += 1
    return s6, s3, good, worst


def main():
    rng = random.Random(5150)
    print("=== P6 = (max ell, sum |A_i|^2) at larger m ===")
    print("   n   m   instances   P6 stuck   P3 stuck   no-good")
    grand6 = grand3 = 0
    firstbad = None
    for (n, m, T) in [(3, 5, 300), (3, 6, 220), (3, 7, 150),
                      (3, 8, 90), (3, 9, 40),
                      (4, 5, 150), (4, 6, 90), (4, 7, 40),
                      (5, 5, 50), (5, 6, 25)]:
        perms = list(permutations(range(n)))
        t6 = t3 = cnt = nogood = 0
        for _ in range(T):
            cs = (matrix_realising(m, n, rng, 3) if rng.random() < 0.5
                  else [rand_dicho(m, rng, rng.choice([0.0, 0.2, 0.5, 0.8, 1.0]))
                        for _ in range(n)])
            if max(max(c.values()) for c in cs) < 2:
                continue
            cnt += 1
            s6, s3, good, worst = test(cs, m, n, perms)
            t6 += s6
            t3 += s3
            if not good:
                nogood += 1
            if s6 and firstbad is None:
                firstbad = (cs, m, n, worst)
        grand6 += t6
        grand3 += t3
        print("  %2d  %2d   %7d   %8d   %8d   %6d" % (n, m, cnt, t6, t3, nogood))
    print()
    print("  total stuck partitions:  P6 = %d,  P3 = %d" % (grand6, grand3))
    if firstbad:
        cs, m, n, worst = firstbad
        bundles, e = worst
        print("\n  first P6-stuck partition: n=%d m=%d bundles=%s ell=%s"
              % (n, m, [sorted(b) for b in bundles], e))
        for i in range(n):
            print("     agent %d singletons %s"
                  % (i, [cs[i][frozenset({g})] for g in range(m)]))
    else:
        print("  no P6-stuck partition found at any size tested")


if __name__ == "__main__":
    main()
