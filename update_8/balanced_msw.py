"""Candidate rule for n=3: minimise total cost AMONG CARDINALITY-BALANCED
partitions.

Why this is worth testing.  Route D died because the unrestricted
utilitarian-optimal set can be a bad singleton (Proposition prop:msw-false).
But that counterexample's unique optimum has bundle sizes (0,3,1) -- it is NOT
balanced.  Restricting the optimisation to balanced partitions may therefore
evade the whole obstruction, and it would be a single optimisation with no
local search, no restarts and no schedule.

A cost-minimising balanced allocation is automatically envy-freeable: any
reassignment of its own bundles is another balanced allocation, so cannot have
lower cost.  So only ell <= 1 has to be checked.

If this holds, the proof obligation is clean and exchange-shaped: show that a
balanced allocation with ell(u) >= 2 admits a balanced modification of strictly
smaller total cost.

Run:  python balanced_msw.py
"""
from itertools import combinations, combinations_with_replacement, product
import random


def subsets(m):
    return [frozenset(s) for k in range(m + 1) for s in combinations(range(m), k)]


def gen_functions(m):
    subs = sorted(subsets(m), key=lambda s: (len(s), sorted(s)))
    res, val = [], {}

    def rec(i):
        if i == len(subs):
            res.append(dict(val)); return
        S = subs[i]
        if len(S) == 0:
            val[S] = 0; rec(i + 1); del val[S]; return
        lo, hi = 0, 10 ** 9
        for g in S:
            T = S - {g}
            lo = max(lo, val[T]); hi = min(hi, val[T] + 1)
        for x in range(lo, hi + 1):
            val[S] = x; rec(i + 1)
        del val[S]

    rec(0)
    return res


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


def ellvec(cs, bd, n):
    W = [[cs[i][bd[i]] - cs[i][bd[j]] for j in range(n)] for i in range(n)]
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
            return e
    return None


def balanced(bd, m, n):
    ss = sorted(len(b) for b in bd)
    return ss[-1] - ss[0] <= 1


def rule_min_cost_balanced(cs, m, n):
    """Return (best_cost, list of ell-vectors of ALL cost-minimising balanced
    allocations)."""
    best = None
    wins = []
    for assign in product(range(n), repeat=m):
        bd = [frozenset(g for g in range(m) if assign[g] == i) for i in range(n)]
        if not balanced(bd, m, n):
            continue
        tot = sum(cs[i][bd[i]] for i in range(n))
        if best is None or tot < best:
            best = tot; wins = [bd]
        elif tot == best:
            wins.append(bd)
    out = []
    for bd in wins:
        e = ellvec(cs, bd, n)
        out.append((bd, e))
    return best, out


def any_good_overall(cs, m, n):
    for assign in product(range(n), repeat=m):
        bd = [frozenset(g for g in range(m) if assign[g] == i) for i in range(n)]
        e = ellvec(cs, bd, n)
        if e is not None and max(e) <= 1:
            return True
    return False


def check(cs, m, n):
    """Returns (some_winner_good, every_winner_good)."""
    _, wins = rule_min_cost_balanced(cs, m, n)
    ok = [e is not None and max(e) <= 1 for _, e in wins]
    return any(ok), all(ok)


def as_dict(m, f):
    return {S: f(S) for S in subsets(m)}


def main():
    print("=== EXHAUSTIVE n=3, m=3 (all 9880 instances) ===")
    F = gen_functions(3)
    some_bad = every_bad = 0
    for cs in combinations_with_replacement(F, 3):
        s, e = check(list(cs), 3, 3)
        if not s:
            some_bad += 1
        if not e:
            every_bad += 1
    print("  no cost-min balanced allocation is good : %d" % some_bad)
    print("  some cost-min balanced allocation is bad: %d" % every_bad)

    print("\n=== named hard instances ===")
    D = [frozenset({0, 1}), frozenset({0, 2, 3}), frozenset({1, 2, 3})]
    disc = [as_dict(4, lambda S, Ds=Ds: len(S & Ds)) for Ds in D]
    RAW = [
        {(): 0, (0,): 1, (1,): 1, (2,): 1, (3,): 1, (0, 1): 2, (0, 2): 1, (0, 3): 2,
         (1, 2): 1, (1, 3): 2, (2, 3): 2, (0, 1, 2): 2, (0, 1, 3): 3, (0, 2, 3): 2,
         (1, 2, 3): 2, (0, 1, 2, 3): 3},
        {(): 0, (0,): 1, (1,): 1, (2,): 1, (3,): 1, (0, 1): 2, (0, 2): 2, (0, 3): 2,
         (1, 2): 2, (1, 3): 2, (2, 3): 1, (0, 1, 2): 3, (0, 1, 3): 2, (0, 2, 3): 2,
         (1, 2, 3): 2, (0, 1, 2, 3): 3},
        {(): 0, (0,): 1, (1,): 1, (2,): 0, (3,): 1, (0, 1): 2, (0, 2): 1, (0, 3): 2,
         (1, 2): 1, (1, 3): 2, (2, 3): 1, (0, 1, 2): 2, (0, 1, 3): 2, (0, 2, 3): 2,
         (1, 2, 3): 2, (0, 1, 2, 3): 3},
    ]
    msw = [{frozenset(k): v for k, v in d.items()} for d in RAW]
    wit = [as_dict(3, lambda S: max(0, len(S) - 1)),
           as_dict(3, lambda S: len(S)), as_dict(3, lambda S: len(S))]
    for tag, cs, m in (("discrepancy cex", disc, 4), ("mswcex", msw, 4),
                       ("insertion witness", wit, 3)):
        s, e = check(cs, m, 3)
        print("  %-20s some winner good: %-5s | every winner good: %s" % (tag, s, e))

    print("\n=== structured + endpoint-constant sweeps ===")
    rng = random.Random(2718)
    for (n, m, T) in [(3, 4, 3000), (3, 5, 1200), (3, 6, 400),
                      (4, 4, 800), (4, 5, 300), (5, 5, 150)]:
        sb = eb = 0
        for _ in range(T):
            cs = [rand_dicho(m, rng, rng.choice([0.0, 0.1, 0.5, 0.9, 1.0]))
                  for _ in range(n)]
            s, e = check(cs, m, n)
            if not s:
                sb += 1
                if sb == 1:
                    print("  !! RULE FAILS  n=%d m=%d (conjecture still holds: %s)"
                          % (n, m, any_good_overall(cs, m, n)))
                    for i, c in enumerate(cs):
                        print("     agent", i, {tuple(sorted(k)): v for k, v in
                                                sorted(c.items(), key=lambda kv:
                                                       (len(kv[0]), sorted(kv[0])))})
            if not e:
                eb += 1
        print("  n=%d m=%d T=%4d | rule fails (no good winner): %3d | "
              "some winner bad: %d" % (n, m, T, sb, eb))


if __name__ == "__main__":
    main()
