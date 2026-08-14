"""Step 1-2 of the plan: NON-ADDITIVE EF-free instances, and whether the
additive-shaped characterisation survives there.

WHY.  R10's Set-Splitting family is binary ADDITIVE, so Conjecture 2 already
holds on it via [LMS26] and the characterisation found there -- universally
costly chores spread one per agent, paid set = their holders -- is just the
binary-additive theorem's shape reappearing.  The residual class that actually
matters is the NON-ADDITIVE EF-free instances, which that reduction cannot
produce and which nothing so far has looked at.

WHAT IS TESTED, on non-additive EF-free instances only:
  H0  does a chain witness exist at all?
  H1  paid set  <=  agents holding a universally costly chore
        (g universally costly := c_i({g}) >= 1 for every agent i)
  H2  paid set  ==  those agents
  H3  total subsidy constant across all witnesses of an instance
  H4  paid set  <=  argmax_i c_i(A_i)     (held 164/164 on the earlier residual)

Run:  python nonadditive_residual.py
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


def is_additive(m, c):
    for S in subsets(m):
        if c[S] != sum(c[frozenset({g})] for g in S):
            return False
    return True


def ell_ok(a, n, k):
    W = [[min(a[i][i], k) - min(a[i][j], k) for j in range(n)] for i in range(n)]
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
            return max(e) <= 1, e
    return False, None


def analyse(cs, m, n):
    K = max(max(c.values()) for c in cs)
    has_ef = False
    chain = []
    for assign in product(range(n), repeat=m):
        bd = [frozenset(g for g in range(m) if assign[g] == i) for i in range(n)]
        a = [[cs[i][bd[j]] for j in range(n)] for i in range(n)]
        if all(a[i][i] <= a[i][j] for i in range(n) for j in range(n)):
            has_ef = True
        if all(ell_ok(a, n, k)[0] for k in range(1, K + 1)):
            chain.append((bd, ell_ok(a, n, K)[1]))
    return has_ef, chain, K


def universally_costly(cs, m, n):
    return {g for g in range(m)
            if all(cs[i][frozenset({g})] >= 1 for i in range(n))}


def main():
    rng = random.Random(4242)
    stats = dict(found=0, nochain=0, h1=0, h2=0, h3=0, h4=0, tot_w=0)
    subsidy_spread = 0
    examples = []

    print("=== hunting NON-ADDITIVE EF-free instances ===")
    for (n, m, T) in [(3, 5, 6000), (3, 6, 3000), (4, 5, 4000), (4, 6, 1500)]:
        got = 0
        for _ in range(T):
            cs = (matrix_realising(m, n, rng, 3) if rng.random() < 0.6
                  else [rand_dicho(m, rng, rng.choice([0.0, 0.1, 0.5, 0.9, 1.0]))
                        for _ in range(n)])
            if max(max(c.values()) for c in cs) < 2:
                continue
            if all(is_additive(m, c) for c in cs):
                continue                      # want at least one non-additive
            has_ef, chain, K = analyse(cs, m, n)
            if has_ef:
                continue
            got += 1
            stats['found'] += 1
            if not chain:
                stats['nochain'] += 1
                print("  !! NO CHAIN WITNESS (non-additive, EF-free) n=%d m=%d"
                      % (n, m))
                continue
            UC = universally_costly(cs, m, n)
            tot = {sum(e) for _, e in chain}
            if len(tot) == 1:
                stats['h3'] += 1
            else:
                subsidy_spread += 1
            ok1 = ok2 = ok4 = True
            for bd, e in chain:
                stats['tot_w'] += 1
                paid = {i for i in range(n) if e[i] == 1}
                holders = {i for i in range(n) if bd[i] & UC}
                mx = max(cs[i][bd[i]] for i in range(n))
                argmx = {i for i in range(n) if cs[i][bd[i]] == mx}
                if not paid <= holders:
                    ok1 = False
                if paid != holders:
                    ok2 = False
                if not paid <= argmx:
                    ok4 = False
            stats['h1'] += ok1
            stats['h2'] += ok2
            stats['h4'] += ok4
            if not ok1 and len(examples) < 1:
                examples.append((cs, m, n, UC))
        print("  n=%d m=%d : %d non-additive EF-free instances" % (n, m, got))

    f = stats['found']
    print("\n=== results on %d non-additive EF-free instances "
          "(%d chain witnesses) ===" % (f, stats['tot_w']))
    print("  H0  no chain witness                       : %d" % stats['nochain'])
    print("  H1  paid <= universally-costly holders      : %d / %d" % (stats['h1'], f))
    print("  H2  paid == universally-costly holders     : %d / %d" % (stats['h2'], f))
    print("  H3  total subsidy constant per instance    : %d / %d" % (stats['h3'], f))
    print("  H4  paid <= argmax_i c_i(A_i)               : %d / %d" % (stats['h4'], f))

    if examples:
        cs, m, n, UC = examples[0]
        print("\n  first H1 violation (universally costly chores = %s):" % sorted(UC))
        for i, c in enumerate(cs):
            print("     agent", i, {tuple(sorted(k)): v for k, v in
                                    sorted(c.items(),
                                           key=lambda kv: (len(kv[0]), sorted(kv[0])))})


if __name__ == "__main__":
    main()
