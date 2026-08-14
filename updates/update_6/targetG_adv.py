"""Target G against the adversary that killed uniform balance.

Uniform balance also passed exhaustive n=m=3 and thousands of random instances,
then died on the first structured adversarial run.  So Target G gets the same
treatment before anything is claimed: the named hard instances, then exhaustive
sweeps over the structured families, then endpoint-constant sweeps.

Run:  python targetG_adv.py
"""
from itertools import combinations, product
import random

from targetG import subsets, analyse, rand_dicho, chore_ell, goods_ell


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


def families(m):
    pool = []
    for r in range(0, m + 1):
        for D in combinations(range(m), r):
            Ds = frozenset(D)
            pool.append(as_dict(m, lambda S, Ds=Ds: len(S & Ds)))          # binary additive
            if r >= 1:
                pool.append(as_dict(m, lambda S, Ds=Ds: min(len(S & Ds), 1)))  # unit demand
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


def report(tag, cs, m, n):
    c1, tg, sp = analyse(cs, m, n)
    if tg:
        return True
    print("  !! TARGET G FAILS  [%s]  n=%d m=%d   best spread of q = %s" % (tag, n, m, sp))
    print("     Conjecture 1 still holds on this instance: %s" % c1)
    for i, c in enumerate(cs):
        print("     agent", i, {tuple(sorted(k)): v for k, v in
                                sorted(c.items(), key=lambda kv: (len(kv[0]), sorted(kv[0])))})
    return False


def main():
    fails = 0

    print("=== named hard instances ===")
    # the discrepancy counterexample that killed uniform balance
    D = [frozenset({0, 1}), frozenset({0, 2, 3}), frozenset({1, 2, 3})]
    disc = [as_dict(4, lambda S, Ds=Ds: len(S & Ds)) for Ds in D]
    fails += not report("discrepancy cex (killed Approach 5)", disc, 4, 3)

    # the insertion obstruction witness
    w = [as_dict(3, lambda S: max(0, len(S) - 1)),
         as_dict(3, lambda S: len(S)), as_dict(3, lambda S: len(S))]
    fails += not report("insertion obstruction witness", w, 3, 3)

    # the W4 no-go instance
    fails += not report("W4 no-go", [as_dict(2, lambda S: len(S))] * 3, 2, 3)

    # mswcex
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
    mc = [{frozenset(k): v for k, v in d.items()} for d in RAW]
    fails += not report("mswcex", mc, 4, 3)
    if fails == 0:
        print("   all named instances passed")

    print("\n=== exhaustive over structured families ===")
    for m in (2, 3, 4):
        pool = families(m)
        for n in (3,):
            bad = cnt = 0
            for cs in combinations(pool, n):
                cnt += 1
                _, tg, sp = analyse(list(cs), m, n)
                if not tg:
                    bad += 1
                    if bad == 1:
                        report("structured m=%d" % m, list(cs), m, n)
            print("  m=%d n=%d : %6d instances, %d TARGET G failures" % (m, n, cnt, bad))
            fails += bad

    print("\n=== endpoint-constant sweeps ===")
    rng = random.Random(777)
    for (n, m, T) in [(3, 4, 2500), (3, 5, 800), (4, 4, 800), (4, 5, 300), (5, 5, 120)]:
        bad = 0
        for _ in range(T):
            cs = [rand_dicho(m, rng, rng.choice([0.0, 0.05, 0.5, 0.95, 1.0]))
                  for _ in range(n)]
            _, tg, sp = analyse(cs, m, n)
            if not tg:
                bad += 1
                if bad == 1:
                    report("endpoint-constant", cs, m, n)
        print("  n=%d m=%d T=%5d : %d TARGET G failures" % (n, m, T, bad))
        fails += bad

    print("\n===============================================================")
    print("TOTAL Target G failures: %d" % fails)


if __name__ == "__main__":
    main()
