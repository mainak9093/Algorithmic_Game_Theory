"""Is there ROOM for a non-local argument?  Counting the good allocations.

Every local and decompositional route has failed (rem:cancellation-four), so the
remaining class is non-local: counting, averaging, probabilistic-method or
parity arguments that reason about all allocations at once rather than about arcs,
rounds, or path pieces.

Every such argument needs room.  A probabilistic-method proof needs the good
allocations to occupy a non-vanishing fraction under some distribution; a counting
or parity proof needs their number to be forced non-zero by an identity.  Both
collapse if hard instances have exactly one good allocation, since then nothing
short of exhibiting it can work -- and exhibiting it is precisely what the
constructive routes failed to do.

Measured per instance, exhaustively over all n^m allocations:
    good      = allocations with max_i ell_i <= 1  (Conjecture 2's witnesses)
    frac      = good / total
    ef        = exactly envy-free allocations (the easy witnesses)
and the same restricted to the EF-FREE instances, which are the residual class
that actually matters -- on instances admitting an exactly envy-free allocation
Conjecture 2 is trivial.

Reported: the MINIMUM count and fraction over instances, since a counting
argument is only as good as its worst case.

Run:  python counting_room.py
"""
from itertools import product, permutations
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_17")
sys.path.insert(0, "../update_18")
from minimum_subsidy import rand_dicho, matrix_realising    # noqa: E402
from localsearch_lemma import ell_vec                       # noqa: E402


def analyse(cs, m, n, perms):
    good = 0
    ef = 0
    total = 0
    for assign in product(range(n), repeat=m):
        bd = tuple(frozenset(g for g in range(m) if assign[g] == i)
                   for i in range(n))
        total += 1
        a = [[cs[i][bd[j]] for j in range(n)] for i in range(n)]
        if all(a[i][i] <= a[i][j] for i in range(n) for j in range(n)):
            ef += 1
        e = ell_vec(a, n)
        if e is not None and max(e) <= 1:
            good += 1
    return good, ef, total


def main():
    rng = random.Random(31313131)
    minfrac = None
    mincount = None
    worst = None
    hist = Counter()
    effree_hist = Counter()
    effree = 0
    tot = 0
    print("=== how many good allocations does an instance have? ===")
    print("   n   m   inst   min #good   min fraction   min #good on EF-free")
    for (n, m, T) in [(3, 4, 400), (3, 5, 250), (3, 6, 120),
                      (4, 4, 250), (4, 5, 120), (5, 5, 60)]:
        perms = list(permutations(range(n)))
        mc = None
        mf = None
        mce = None
        cnt = 0
        for _ in range(T):
            cs = (matrix_realising(m, n, rng, 3) if rng.random() < 0.5
                  else [rand_dicho(m, rng, rng.choice([0.0, 0.2, 0.5, 0.8, 1.0]))
                        for _ in range(n)])
            if max(max(x.values()) for x in cs) < 2:
                continue
            cnt += 1
            tot += 1
            good, ef, total = analyse(cs, m, n, perms)
            hist[good] += 1
            frac = good / total
            if mc is None or good < mc:
                mc = good
            if mf is None or frac < mf:
                mf = frac
            if mincount is None or good < mincount:
                mincount = good
                worst = (n, m, good, total, ef)
            if minfrac is None or frac < minfrac:
                minfrac = frac
            if ef == 0:
                effree += 1
                effree_hist[good] += 1
                if mce is None or good < mce:
                    mce = good
        print("  %2d  %2d  %5d   %9s   %12s   %s"
              % (n, m, cnt, mc, ("%.4f" % mf) if mf is not None else "-",
                 mce if mce is not None else "-"))
    print()
    print("  instances                       : %d  (EF-free: %d)" % (tot, effree))
    print("  minimum # good allocations      : %s" % mincount)
    print("  minimum fraction good           : %.5f" % (minfrac or 0))
    print("  worst instance (n,m,good,total,ef) : %s" % (worst,))
    print()
    print("  #good distribution, EF-FREE instances only : %s"
          % dict(sorted(effree_hist.items())[:12]))
    print()
    if mincount is not None and mincount <= 2:
        print("  *** Hard instances can have as few as %d good allocations." % mincount)
        print("      A probabilistic or counting argument has essentially no room:")
        print("      the good set can be a vanishing fraction, so any proof must")
        print("      effectively EXHIBIT the witness -- which is what every")
        print("      constructive route already failed to do. ***")
    else:
        print("  *** The good set never drops below %d allocations." % mincount)
        print("      There IS room for a counting or averaging argument. ***")


if __name__ == "__main__":
    main()
