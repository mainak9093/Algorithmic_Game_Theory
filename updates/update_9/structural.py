"""Two candidate theorems that avoid the exchange obstruction entirely.

(T1) SMALL-BUNDLE THEOREM.  If some envy-freeable allocation has every bundle
     costing at most 1 to every agent -- max_{v,i} c_v(A_i) <= 1 -- it is good.
     Proof idea: the cycle-closing bound gives
     ell(u) <= max_v [c_v(A_u) - c_v(A_v)] <= 1 - 0 = 1.
     No exchange property needed.  Corollary: the conjecture holds whenever
     m <= n, by taking a minimum-cost assignment of one chore per agent.

(T2) TWO-TYPE THEOREM (candidate).  Suppose the agents carry at most TWO
     distinct cost functions.  Does a good allocation always exist, and is
     there a clean rule producing it?  This class is genuinely outside the
     literature -- identical costs, additive costs and submodular costs are all
     covered elsewhere, "two types of agents" is not -- and it strictly
     generalises the identical-cost theorem.

Both are checked semantically against the true longest-path computation.

Run:  python structural.py
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


def allocs(m, n):
    for assign in product(range(n), repeat=m):
        yield [frozenset(g for g in range(m) if assign[g] == i) for i in range(n)]


def good(cs, bd, n):
    e = ellvec(cs, bd, n)
    return e is not None and max(e) <= 1


# ---------------------------------------------------------------- T1
def t1_hypothesis(cs, bd, n):
    return max(cs[v][bd[i]] for v in range(n) for i in range(n)) <= 1


def test_T1(cs, m, n):
    """Every envy-freeable allocation satisfying the hypothesis must be good."""
    for bd in allocs(m, n):
        if not t1_hypothesis(cs, bd, n):
            continue
        if ellvec(cs, bd, n) is None:
            continue                       # not envy-freeable; hypothesis idle
        if not good(cs, bd, n):
            return False, bd
    return True, None


def test_msmalln(cs, m, n):
    """m <= n corollary: min-cost one-chore-per-agent assignment is good."""
    best = None
    for assign in product(range(n), repeat=m):
        bd = [frozenset(g for g in range(m) if assign[g] == i) for i in range(n)]
        if max(len(b) for b in bd) > 1:
            continue
        tot = sum(cs[i][bd[i]] for i in range(n))
        if best is None or tot < best[0]:
            best = (tot, bd)
    return good(cs, best[1], n)


# ---------------------------------------------------------------- T2
def rule_balanced_minenvy(cs, m, n):
    """min total cost among cardinality-balanced, tie-broken by envy count."""
    best = None
    wins = []
    for bd in allocs(m, n):
        ss = sorted(len(b) for b in bd)
        if ss[-1] - ss[0] > 1:
            continue
        tot = sum(cs[i][bd[i]] for i in range(n))
        if best is None or tot < best:
            best = tot; wins = [bd]
        elif tot == best:
            wins.append(bd)
    ec = lambda bd: sum(1 for i in range(n) for j in range(n)
                        if i != j and cs[i][bd[i]] > cs[i][bd[j]])
    b2 = min(ec(bd) for bd in wins)
    return [bd for bd in wins if ec(bd) == b2]


def test_T2(cs, m, n):
    """(exists good alloc, rule always selects good)."""
    ex = any(good(cs, bd, n) for bd in allocs(m, n))
    sel = rule_balanced_minenvy(cs, m, n)
    return ex, all(good(cs, bd, n) for bd in sel)


def main():
    print("=== T1: small-bundle hypothesis (max_{v,i} c_v(A_i) <= 1) ===")
    bad = 0
    for m in (2, 3):
        F = gen_functions(m)
        for n in (2, 3):
            for cs in combinations_with_replacement(F, n):
                ok, w = test_T1(list(cs), m, n)
                if not ok:
                    bad += 1
    print("  exhaustive m<=3, n<=3 : %d violations" % bad)
    rng = random.Random(9)
    bad2 = 0
    for _ in range(3000):
        n = rng.choice([3, 4]); m = rng.choice([3, 4, 5])
        cs = [rand_dicho(m, rng, rng.choice([0.0, 0.3, 0.7, 1.0])) for _ in range(n)]
        ok, w = test_T1(cs, m, n)
        if not ok:
            bad2 += 1
    print("  randomised            : %d violations" % bad2)

    print("\n=== T1 corollary: m <= n ===")
    bad3 = 0; tot3 = 0
    for m in (1, 2, 3):
        F = gen_functions(m)
        for n in (m, m + 1, m + 2):
            for cs in combinations_with_replacement(F, n):
                tot3 += 1
                if not test_msmalln(list(cs), m, n):
                    bad3 += 1
    print("  exhaustive m<=3, n in {m,m+1,m+2}: %d failures / %d" % (bad3, tot3))

    print("\n=== T2: at most two distinct cost functions ===")
    for m in (3, 4):
        F = gen_functions(m)
        if m == 4:
            rng2 = random.Random(4)
            F = rng2.sample(F, 60)
        ex_bad = rule_bad = tot = 0
        for c1, c2 in combinations_with_replacement(F, 2):
            for n in (3, 4, 5):
                for k in range(1, n):          # k agents of type 1
                    cs = [c1] * k + [c2] * (n - k)
                    tot += 1
                    ex, ru = test_T2(cs, m, n)
                    if not ex:
                        ex_bad += 1
                    if not ru:
                        rule_bad += 1
        print("  m=%d : %6d two-type instances | no good alloc: %d | rule fails: %d"
              % (m, tot, ex_bad, rule_bad))


if __name__ == "__main__":
    main()
