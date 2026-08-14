"""How much subsidy does a dichotomous chores instance actually NEED?

Conjecture 1 asserts p in {0,1}^n with total <= n-1.  Everything so far has
aimed at that bound.  But the two-tier characterisation says a good allocation
is exactly a partition A plus a bipartition S with

    c_i(A_j) >= c_i(A_i) - [i in S] + [j in S],

and |S| is the total subsidy.  So the real question is: how large must |S| be?
If the answer is always <= 1, the true theorem is far stronger than Conjecture 1
and the target should change.

Measured per instance:
    minsub  = min over ALL allocations of the total subsidy sum_i p*_i
              (p* = longest path; +inf if the allocation is not envy-freeable)
    ef      = does an exactly envy-free allocation exist (minsub = 0)?

Run:  python minimum_subsidy.py
"""
from itertools import combinations, product
import random


def subsets(m):
    return [frozenset(s) for k in range(m + 1) for s in combinations(range(m), k)]


def rand_dicho(m, rng, hi_prob=None):
    subs = sorted(subsets(m), key=lambda s: (len(s), sorted(s)))
    val = {frozenset(): 0}
    for S in subs:
        if not S:
            continue
        lo, hi = 0, 10 ** 9
        for g in S:
            T = S - {g}
            lo = max(lo, val[T]); hi = min(hi, val[T] + 1)
        pr = rng.random() if hi_prob is None else hi_prob
        val[S] = hi if (lo != hi and rng.random() < pr) else lo
    return val


def matrix_realising(m, n, rng, maxa):
    lab = [rng.randrange(n) for _ in range(m)]
    B = [frozenset(g for g in range(m) if lab[g] == j) for j in range(n)]
    a = [[rng.randint(0, maxa) for _ in range(n)] for _ in range(n)]
    return [{S: sum(min(len(S & B[j]), a[i][j]) for j in range(n))
             for S in subsets(m)} for i in range(n)]


def total_subsidy(a, n):
    """sum of longest-path subsidies, or None if a positive cycle exists."""
    W = [[a[i][i] - a[i][j] for j in range(n)] for i in range(n)]
    e = [0] * n
    for _ in range(n + 1):
        ch = False
        new = list(e)
        for i in range(n):
            for j in range(n):
                if i != j and W[i][j] + e[j] > new[i]:
                    new[i] = W[i][j] + e[j]; ch = True
        e = new
        if not ch:
            return sum(e), e
    return None, None


def analyse(cs, m, n):
    best = None; bestvec = None
    for assign in product(range(n), repeat=m):
        bd = [frozenset(g for g in range(m) if assign[g] == i) for i in range(n)]
        a = [[cs[i][bd[j]] for j in range(n)] for i in range(n)]
        t, e = total_subsidy(a, n)
        if t is not None and (best is None or t < best):
            best, bestvec = t, e
            if t == 0:
                break
    return best, bestvec


def main():
    rng = random.Random(90210)
    from collections import Counter
    hist = Counter(); efhist = Counter()
    worst = {}
    unbounded = 0
    tot = 0
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
            best, vec = analyse(cs, m, n)
            if best is None:
                unbounded += 1
                continue
            hist[best] += 1
            efhist[(n, best)] += 1
            if best > worst.get(n, (-1,))[0]:
                worst[n] = (best, m, [dict((tuple(sorted(k)), v) for k, v in c.items()
                                           if len(k) <= 1) for c in cs], vec)
    print("=== minimum total subsidy over ALL allocations, %d instances ===" % tot)
    print("  no envy-freeable allocation at all : %d" % unbounded)
    for k in sorted(hist):
        print("  min total subsidy = %d : %6d  (%.2f%%)" % (k, hist[k], 100.0 * hist[k] / tot))
    print()
    print("=== worst case seen, per n  (Conjecture 1 allows n-1) ===")
    for n in sorted(worst):
        b, m, _, vec = worst[n]
        print("  n=%d : max over instances of min total subsidy = %d   (bound n-1 = %d)   witness p=%s"
              % (n, b, n - 1, vec))
    print()
    print("=== breakdown by n ===")
    for n in sorted({k[0] for k in efhist}):
        row = {k[1]: v for k, v in efhist.items() if k[0] == n}
        s = sum(row.values())
        print("  n=%d (%5d inst): %s" % (n, s, {k: row[k] for k in sorted(row)}))


if __name__ == "__main__":
    main()
