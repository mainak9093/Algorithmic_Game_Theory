"""How large must the PAID SET S be?  (the quantity Conjecture 1 bounds)

Correcting update_17/minimum_subsidy.py, which minimised the total subsidy over
ALL allocations and so returned spikes (p = [2,0,0], [3,0,0,0]) -- cheap in
total but outside {0,1}^n, hence irrelevant to Conjecture 1.

Conjecture 1 needs p in {0,1}^n, i.e. max_i p_i <= 1.  By the two-tier
characterisation such an allocation is a partition A plus a bipartition S with
    c_i(A_j) >= c_i(A_i) - [i in S] + [j in S],
and then total subsidy = |S|.  So the right measurement is

    minS(I) = min { |S| : some allocation of I is good with paid set S }

Conjecture 1 says minS <= n-1.  If minS is always <= 1 the true statement is
much stronger and the target should change.  Also recorded: the SPIKE gap,
i.e. instances where a cheap non-{0,1} vector beats every {0,1} one.

Run:  python minimal_S.py
"""
from itertools import product
from collections import Counter
import random
from minimum_subsidy import rand_dicho, matrix_realising, total_subsidy


def analyse(cs, m, n):
    """(minS over good allocations, min total over all allocations, witness)."""
    bestS = None
    bestAny = None
    witness = None
    for assign in product(range(n), repeat=m):
        bd = [frozenset(g for g in range(m) if assign[g] == i) for i in range(n)]
        a = [[cs[i][bd[j]] for j in range(n)] for i in range(n)]
        t, e = total_subsidy(a, n)
        if t is None:
            continue
        if bestAny is None or t < bestAny:
            bestAny = t
        if max(e) <= 1 and (bestS is None or t < bestS):
            bestS, witness = t, (bd, e)
    return bestS, bestAny, witness


def main():
    rng = random.Random(90210)
    hist = Counter()
    byn = Counter()
    nogood = 0
    spike = 0
    tot = 0
    worst = {}
    for (n, m, T) in [(3, 4, 3000), (3, 5, 2500), (3, 6, 1200),
                      (4, 4, 2000), (4, 5, 1500), (4, 6, 500),
                      (5, 5, 500)]:
        for _ in range(T):
            cs = (matrix_realising(m, n, rng, 3) if rng.random() < 0.55
                  else [rand_dicho(m, rng, rng.choice([0.0, 0.15, 0.5, 0.85, 1.0]))
                        for _ in range(n)])
            if max(max(c.values()) for c in cs) < 1:
                continue
            tot += 1
            bestS, bestAny, w = analyse(cs, m, n)
            if bestS is None:
                nogood += 1
                print("  !! NO allocation with p in {0,1}^n : n=%d m=%d" % (n, m))
                continue
            if bestS > bestAny:
                spike += 1
            hist[bestS] += 1
            byn[(n, bestS)] += 1
            if bestS > worst.get(n, (-1,))[0]:
                worst[n] = (bestS, m, w)

    print("=== minimal paid-set size |S| over GOOD allocations, %d instances ===" % tot)
    print("  instances with NO good allocation (would refute Conj. 1) : %d" % nogood)
    print("  instances where a cheaper non-{0,1} spike exists         : %d" % spike)
    for k in sorted(hist):
        print("  minimal |S| = %d : %6d  (%.2f%%)" % (k, hist[k], 100.0 * hist[k] / tot))
    print()
    print("=== worst case per n  (Conjecture 1 allows n-1) ===")
    for n in sorted(worst):
        b, m, w = worst[n]
        print("  n=%d : max minimal |S| = %d   (bound n-1 = %d)   p=%s"
              % (n, b, n - 1, w[1] if w else None))
    print()
    for n in sorted({k[0] for k in byn}):
        row = {k[1]: v for k, v in byn.items() if k[0] == n}
        print("  n=%d (%5d inst): %s"
              % (n, sum(row.values()), {k: row[k] for k in sorted(row)}))


if __name__ == "__main__":
    main()
