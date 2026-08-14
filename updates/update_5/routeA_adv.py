"""Route A, step 1: adversarial hunt for an instance with NO uniformly balanced
partition.

The uniform sampler of fast.py flips a fair coin at each free choice and so
essentially never produces endpoint-constant / structured extremal functions --
the kind from which every obstruction in this project has been built.  This
script deliberately samples those instead, and additionally hits every hard
instance the project has accumulated.

For additive costs the statement specialises to a hypergraph-discrepancy
question ("split every D_i evenly across n parts"), which is where a
counterexample would be expected to live if one exists, so those families are
over-represented.

Run:  python routeA_adv.py
"""
from itertools import combinations, product, permutations
import random

from routeA import (gen_functions, ellvec, partitions, uniformly_balanced,
                    has_balanced_partition, has_good_allocation, best_assignment)


def as_dict(m, f):
    """Materialise a callable cost function on subsets of [m] as a dict."""
    out = {}
    for k in range(m + 1):
        for s in combinations(range(m), k):
            out[frozenset(s)] = f(frozenset(s))
    return out


def is_dichotomous(m, c):
    if c[frozenset()] != 0:
        return False
    for k in range(m + 1):
        for s in combinations(range(m), k):
            S = frozenset(s)
            for g in range(m):
                if g in S:
                    continue
                if c[S | {g}] - c[S] not in (0, 1):
                    return False
    return True


# ------------------------------------------------------- structured families
def families(m, rng):
    """A pool of structured dichotomous cost functions on m items."""
    pool = []
    univ = frozenset(range(m))

    # supermodular thresholds  max(0,|S|-k)      (the obstruction family)
    for k in range(0, m):
        pool.append(as_dict(m, lambda S, k=k: max(0, len(S) - k)))
    # saturating  min(|S|,k)
    for k in range(1, m + 1):
        pool.append(as_dict(m, lambda S, k=k: min(len(S), k)))
    # binary additive on a subset D
    for r in range(0, m + 1):
        for D in combinations(range(m), r):
            Ds = frozenset(D)
            pool.append(as_dict(m, lambda S, Ds=Ds: len(S & Ds)))
    # unit demand on a subset D
    for r in range(1, m + 1):
        for D in combinations(range(m), r):
            Ds = frozenset(D)
            pool.append(as_dict(m, lambda S, Ds=Ds: min(len(S & Ds), 1)))
    # thresholded on a subset:  max(0,|S n D| - k)
    for r in range(2, m + 1):
        for D in combinations(range(m), r):
            Ds = frozenset(D)
            for k in range(1, r):
                pool.append(as_dict(m, lambda S, Ds=Ds, k=k: max(0, len(S & Ds) - k)))
    return [c for c in pool if is_dichotomous(m, c)]


def endpoint_constant(m, rng, hi_prob):
    """Dichotomous function built by taking the SAME endpoint at (almost) every
    subset -- exactly the shape the uniform sampler cannot reach."""
    subs = sorted([frozenset(s) for k in range(m + 1) for s in combinations(range(m), k)],
                  key=lambda s: (len(s), sorted(s)))
    val = {frozenset(): 0}
    for S in subs:
        if not S:
            continue
        lo, hi = 0, 10 ** 9
        for g in S:
            T = S - {g}
            lo = max(lo, val[T])
            hi = min(hi, val[T] + 1)
        val[S] = hi if (lo != hi and rng.random() < hi_prob) else lo
    return val


def report(tag, cs, m, n):
    bd = has_balanced_partition(cs, m, n)
    if bd is not None:
        return True
    good = has_good_allocation(cs, m, n)
    print("  !! NO uniformly balanced partition  [%s]  n=%d m=%d" % (tag, n, m))
    print("     a good allocation exists anyway: %s" % good)
    for i, c in enumerate(cs):
        print("     agent", i, {tuple(sorted(k)): v
                                for k, v in sorted(c.items(),
                                                   key=lambda kv: (len(kv[0]), sorted(kv[0])))})
    return False


def main():
    rng = random.Random(5150)
    fails = 0

    # ---- 1. every hard instance the project has accumulated -----------------
    print("=== named hard instances ===")
    w = [as_dict(3, lambda S: max(0, len(S) - 1)),
         as_dict(3, lambda S: len(S)),
         as_dict(3, lambda S: len(S))]
    fails += not report("obstruction witness", w, 3, 3)

    u = [as_dict(2, lambda S: len(S))] * 3
    fails += not report("W4 no-go instance", u, 2, 3)

    RAW = [
        {(): 0, (0,): 1, (1,): 1, (2,): 1, (3,): 1,
         (0, 1): 2, (0, 2): 1, (0, 3): 2, (1, 2): 1, (1, 3): 2, (2, 3): 2,
         (0, 1, 2): 2, (0, 1, 3): 3, (0, 2, 3): 2, (1, 2, 3): 2, (0, 1, 2, 3): 3},
        {(): 0, (0,): 1, (1,): 1, (2,): 1, (3,): 1,
         (0, 1): 2, (0, 2): 2, (0, 3): 2, (1, 2): 2, (1, 3): 2, (2, 3): 1,
         (0, 1, 2): 3, (0, 1, 3): 2, (0, 2, 3): 2, (1, 2, 3): 2, (0, 1, 2, 3): 3},
        {(): 0, (0,): 1, (1,): 1, (2,): 0, (3,): 1,
         (0, 1): 2, (0, 2): 1, (0, 3): 2, (1, 2): 1, (1, 3): 2, (2, 3): 1,
         (0, 1, 2): 2, (0, 1, 3): 2, (0, 2, 3): 2, (1, 2, 3): 2, (0, 1, 2, 3): 3},
    ]
    mc = [{frozenset(k): v for k, v in d.items()} for d in RAW]
    fails += not report("mswcex (kills utilitarian optimality)", mc, 4, 3)

    # set-splitting instance from update_3: n=5, m=6, binary additive
    D = [frozenset({0, 1, 2, 3, 4}), frozenset({0, 1, 2, 3, 5}), frozenset({0, 1, 2, 4, 5}),
         frozenset({0, 1, 2}), frozenset({0, 1, 2})]
    ss = [as_dict(6, lambda S, Ds=Ds: len(S & Ds)) for Ds in D]
    fails += not report("set-splitting certified-hard", ss, 6, 5)
    print("   (all named instances passed)" if fails == 0 else "")

    # ---- 2. exhaustive over structured families -----------------------------
    print("\n=== exhaustive over structured families ===")
    for m in (2, 3, 4):
        pool = families(m, rng)
        # dedupe
        seen, uniq = set(), []
        for c in pool:
            key = tuple(sorted((tuple(sorted(k)), v) for k, v in c.items()))
            if key not in seen:
                seen.add(key)
                uniq.append(c)
        for n in (2, 3):
            bad = 0
            cnt = 0
            for cs in combinations(uniq, n) if n <= len(uniq) else []:
                cnt += 1
                if has_balanced_partition(list(cs), m, n) is None:
                    bad += 1
                    if bad == 1:
                        report("structured m=%d n=%d" % (m, n), list(cs), m, n)
            print("  m=%d n=%d : %6d structured instances, %d with no balanced partition"
                  % (m, n, cnt, bad))
            fails += bad

    # ---- 3. endpoint-constant random sweeps ---------------------------------
    print("\n=== endpoint-constant random sweeps (the sampler's blind spot) ===")
    for (n, m, T) in [(3, 3, 3000), (3, 4, 2000), (3, 5, 800), (3, 6, 300),
                      (4, 4, 800), (4, 5, 300), (5, 5, 150), (5, 6, 80)]:
        bad = 0
        for _ in range(T):
            hp = rng.choice([0.0, 0.05, 0.5, 0.95, 1.0])
            cs = [endpoint_constant(m, rng, rng.choice([0.0, 0.1, 0.9, 1.0, hp]))
                  for _ in range(n)]
            if has_balanced_partition(cs, m, n) is None:
                bad += 1
                if bad == 1:
                    report("endpoint-constant", cs, m, n)
        print("  n=%d m=%d T=%5d : %d with no balanced partition" % (n, m, T, bad))
        fails += bad

    print("\n===============================================================")
    print("TOTAL instances with no uniformly balanced partition: %d" % fails)


if __name__ == "__main__":
    main()
