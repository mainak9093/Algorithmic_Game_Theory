"""Adversarial hunt for the instance that kills the layer induction.

THE KILL CONDITION.  A depth->=2 instance whose good allocations are DISJOINT
from its truncation's:  G_full ∩ G_trunc = empty.  If one exists the induction
cannot carry a witness across a layer, in that peeling direction.

Two peeling directions, both of which stay inside the dichotomous class:
    TOP    c |-> min(c, K-1)          (drop the highest layer F_K)
    BOTTOM c |-> max(c - 1, 0)        (drop the lowest layer F_1)

Also measured, because the induction needs more than non-emptiness: what
FRACTION of the truncation's good allocations remain good for the full
instance?  If that is always 100% the induction is immediate; if it is a
specific subset, the job is to characterise it.

Adversary: the generator that refuted uniform balance in one run, plus a
deliberate high-depth bias (deep instances are exactly where a truncation
changes the most).

Run:  python layer_hunt.py
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
    for a in product(range(n), repeat=m):
        yield [frozenset(g for g in range(m) if a[g] == i) for i in range(n)]


def goodset(cs, m, n):
    out = set()
    for bd in allocs(m, n):
        e = ellvec(cs, bd, n)
        if e is not None and max(e) <= 1:
            out.add(tuple(tuple(sorted(b)) for b in bd))
    return out


def top_trunc(cs):
    K = max(max(c.values()) for c in cs)
    return [{S: min(v, K - 1) for S, v in c.items()} for c in cs], K


def bot_trunc(cs):
    return [{S: max(v - 1, 0) for S, v in c.items()} for c in cs]


def depth(cs):
    return max(max(c.values()) for c in cs)


def analyse(cs, m, n):
    """Return (kill_top, kill_bot, frac_top, frac_bot) or None if depth < 2."""
    if depth(cs) < 2:
        return None
    gf = goodset(cs, m, n)
    tt, _ = top_trunc(cs)
    gtt = goodset(tt, m, n)
    gbb = goodset(bot_trunc(cs), m, n)
    kill_top = bool(gtt) and bool(gf) and not (gf & gtt)
    kill_bot = bool(gbb) and bool(gf) and not (gf & gbb)
    ft = len(gf & gtt) / len(gtt) if gtt else None
    fb = len(gf & gbb) / len(gbb) if gbb else None
    return kill_top, kill_bot, ft, fb


def as_dict(m, f):
    return {S: f(S) for S in subsets(m)}


def is_dich(m, c):
    if c[frozenset()] != 0:
        return False
    for S in subsets(m):
        for g in range(m):
            if g not in S and c[S | {g}] - c[S] not in (0, 1):
                return False
    return True


def structured(m):
    pool = []
    for r in range(0, m + 1):
        for D in combinations(range(m), r):
            Ds = frozenset(D)
            pool.append(as_dict(m, lambda S, Ds=Ds: len(S & Ds)))
            if r >= 1:
                pool.append(as_dict(m, lambda S, Ds=Ds: min(len(S & Ds), 1)))
            for k in range(1, max(r, 1)):
                pool.append(as_dict(m, lambda S, Ds=Ds, k=k: max(0, len(S & Ds) - k)))
                pool.append(as_dict(m, lambda S, Ds=Ds, k=k: min(len(S & Ds), k)))
    seen, uniq = set(), []
    for c in pool:
        if not is_dich(m, c):
            continue
        key = tuple(sorted((tuple(sorted(k)), v) for k, v in c.items()))
        if key not in seen:
            seen.add(key); uniq.append(c)
    return uniq


def report(tag, cs, m, n, res):
    kt, kb, ft, fb = res
    print("  !! LAYER INDUCTION KILLED [%s] n=%d m=%d  top=%s bot=%s"
          % (tag, n, m, kt, kb))
    for i, c in enumerate(cs):
        print("     agent", i, {tuple(sorted(k)): v for k, v in
                                sorted(c.items(), key=lambda kv:
                                       (len(kv[0]), sorted(kv[0])))})


def sweep(tag, gen, m, n, cap=None):
    kt = kb = tot = 0
    mnt = mnb = 1.0
    shown = False
    for cs in gen:
        r = analyse(list(cs), m, n)
        if r is None:
            continue
        tot += 1
        if r[0]:
            kt += 1
        if r[1]:
            kb += 1
        if r[2] is not None:
            mnt = min(mnt, r[2])
        if r[3] is not None:
            mnb = min(mnb, r[3])
        if (r[0] or r[1]) and not shown:
            report(tag, list(cs), m, n, r); shown = True
        if cap and tot >= cap:
            break
    print("  %-34s n=%d m=%d | %6d depth>=2 | kill(top)=%d kill(bot)=%d | "
          "min frac carried: top %.2f bot %.2f"
          % (tag, n, m, tot, kt, kb, mnt, mnb))
    return kt + kb


def main():
    bad = 0
    rng = random.Random(24601)

    print("=== exhaustive, all dichotomous triples ===")
    F3 = gen_functions(3)
    bad += sweep("all triples m=3", combinations_with_replacement(F3, 3), 3, 3)

    print("\n=== exhaustive over structured families ===")
    for m in (3, 4):
        pool = structured(m)
        bad += sweep("structured m=%d" % m, combinations(pool, 3), m, 3)

    print("\n=== endpoint-constant + high-depth bias ===")
    def gen_rand(n, m, T, deep):
        for _ in range(T):
            if deep:
                # bias hard toward maximal depth: mostly 'hi' choices
                yield [rand_dicho(m, rng, rng.choice([0.9, 0.95, 1.0]))
                       for _ in range(n)]
            else:
                yield [rand_dicho(m, rng, rng.choice([0.0, 0.05, 0.5, 0.95, 1.0]))
                       for _ in range(n)]
    for (n, m, T) in [(3, 4, 4000), (3, 5, 1200), (3, 6, 400),
                      (4, 4, 1200), (4, 5, 400), (5, 5, 150)]:
        bad += sweep("endpoint-const n=%d" % n, gen_rand(n, m, T, False), m, n)
        bad += sweep("HIGH DEPTH   n=%d" % n, gen_rand(n, m, T, True), m, n)

    print("\n===============================================================")
    print("TOTAL layer-induction kills: %d" % bad)


if __name__ == "__main__":
    main()
