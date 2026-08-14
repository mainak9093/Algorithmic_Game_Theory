"""Target G: turn the chore problem into a pure GOODS problem.

The size-shift transform (report Theorem thm:sizeshift) sets
    vtilde_i(S) := |S| - c_i(S),
which is a bijection of the dichotomous class onto itself (given dichotomous
goods v, put c_i(S) = |S| - v_i(S); its marginals are 1 - (goods marginal) in
{0,1}).  It gives, for every allocation A,

    ell^c_A(u) = max_v [ dtilde_A(u,v) + |A_u| - |A_v| ]

where dtilde_A(u,v) is the heaviest u->v path in the GOODS envy graph.  Since
dtilde_A(u,v) <= ptilde_u - ptilde_v, writing

    q_i := ptilde_i + |A_i|          (goods subsidy  +  bundle size)

gives ell^c_A(u) <= q_u - min_v q_v.  Hence:

    TARGET G.  every dichotomous GOODS instance admits an allocation whose
    q = ptilde + |A| has spread at most 1.

Target G ==> Conjecture 1.  It is a statement purely about goods, with no
chores, no replica, no coverage and no schedule, so R2/R3/R11 machinery applies
natively.  It has never been stated as a target or tested.  This script tests
it, and also measures how far the sufficient condition is from necessary.

Run:  python targetG.py
"""
from itertools import combinations, combinations_with_replacement, product
import random
import sys


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
        for v in range(lo, hi + 1):
            val[S] = v; rec(i + 1)
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


def ell_from_W(W, n):
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


def chore_ell(cs, bd, n):
    W = [[cs[i][bd[i]] - cs[i][bd[j]] for j in range(n)] for i in range(n)]
    return ell_from_W(W, n)


def goods_ell(cs, bd, n):
    """Min subsidy for the size-shifted GOODS instance vtilde_i(S)=|S|-c_i(S)."""
    vt = lambda i, B: len(B) - cs[i][B]
    W = [[vt(i, bd[j]) - vt(i, bd[i]) for j in range(n)] for i in range(n)]
    return ell_from_W(W, n)


def analyse(cs, m, n):
    """Returns (conj1_ok, targetG_ok, best_spread)."""
    conj1 = False
    tg = False
    best_spread = None
    for assign in product(range(n), repeat=m):
        bd = [frozenset(g for g in range(m) if assign[g] == i) for i in range(n)]
        ec = chore_ell(cs, bd, n)
        if ec is None:
            continue                       # not envy-freeable (either instance)
        if max(ec) <= 1:
            conj1 = True
        eg = goods_ell(cs, bd, n)
        if eg is None:
            continue
        q = [eg[i] + len(bd[i]) for i in range(n)]
        spread = max(q) - min(q)
        if best_spread is None or spread < best_spread:
            best_spread = spread
        if spread <= 1:
            tg = True
    return conj1, tg, best_spread


def main():
    print("=== EXHAUSTIVE  n=3, m=3, all 9880 instances ===")
    F = gen_functions(3)
    bad_conj = bad_tg = 0
    spreads = {}
    for cs in combinations_with_replacement(F, 3):
        c1, tg, sp = analyse(list(cs), 3, 3)
        if not c1:
            bad_conj += 1
        if not tg:
            bad_tg += 1
        spreads[sp] = spreads.get(sp, 0) + 1
    print("  Conjecture 1 failures : %d" % bad_conj)
    print("  TARGET G   failures   : %d" % bad_tg)
    print("  best achievable spread of q, distribution: %s"
          % dict(sorted(spreads.items())))

    print("\n=== ADVERSARIAL / randomised ===")
    rng = random.Random(11235)
    for (n, m, T) in [(3, 4, 1500), (3, 5, 500), (4, 3, 800),
                      (4, 4, 400), (5, 4, 200)]:
        bc = bt = 0
        worst = 0
        for _ in range(T):
            cs = [rand_dicho(m, rng, rng.choice([0.0, 0.1, 0.5, 0.9, 1.0]))
                  for _ in range(n)]
            c1, tg, sp = analyse(cs, m, n)
            if not c1:
                bc += 1
            if not tg:
                bt += 1
                worst = max(worst, sp if sp is not None else 99)
                if bt == 1:
                    print("  !! TARGET G fails  n=%d m=%d  best spread=%s "
                          "(Conjecture 1 holds here: %s)" % (n, m, sp, c1))
                    for i, c in enumerate(cs):
                        print("     agent", i,
                              {tuple(sorted(k)): v for k, v in
                               sorted(c.items(), key=lambda kv: (len(kv[0]), sorted(kv[0])))})
        print("  n=%d m=%d T=%4d | Conj-1 failures: %d | TARGET G failures: %d"
              % (n, m, T, bc, bt))


if __name__ == "__main__":
    main()
