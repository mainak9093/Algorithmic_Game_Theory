"""The instances that genuinely need a subsidy.

twotier.py found that across ~14.5k adversarial non-additive instances an
EXACTLY envy-free allocation (S = empty, zero subsidy) exists in about 98.7% of
them.  So the two-tier construction question is really a question about the
remaining ~1.3%.  This script isolates those and asks what the paid set looks
like there.

Run:  python hardcases.py
"""
from itertools import combinations, product
import random

from twotier import (as_dict, is_dichotomous, is_additive, ellvec,
                     nonadditive_pool, endpoint_constant, dump)


def analyse(cs, m, n):
    tiers = set()
    best = None
    for assign in product(range(n), repeat=m):
        bd = [frozenset(g for g in range(m) if assign[g] == i) for i in range(n)]
        e = ellvec(cs, bd, n)
        if e is not None and max(e) <= 1:
            S = frozenset(i for i in range(n) if e[i] == 1)
            tiers.add(S)
            if best is None or len(S) < len(best[0]):
                best = (S, bd, e)
    return tiers, best


def own_cost_profile(cs, bd, n):
    return tuple(cs[i][bd[i]] for i in range(n))


def main():
    rng = random.Random(31337)
    hard = []          # instances with no exactly-EF allocation
    total = 0

    # exhaustive structured non-additive, m=4, n=3
    pool = nonadditive_pool(4)
    for cs in combinations(pool, 3):
        total += 1
        tiers, best = analyse(list(cs), 4, 3)
        if frozenset() not in tiers:
            hard.append((list(cs), 4, 3, tiers, best))

    # endpoint-constant sweeps
    for (n, m, T) in [(3, 4, 3000), (3, 5, 1200), (4, 4, 1200), (4, 5, 500)]:
        for _ in range(T):
            cs = [endpoint_constant(m, rng, rng.choice([0.0, 0.1, 0.5, 0.9, 1.0]))
                  for _ in range(n)]
            total += 1
            tiers, best = analyse(cs, m, n)
            if tiers and frozenset() not in tiers:
                hard.append((cs, m, n, tiers, best))

    print("instances examined                          : %d" % total)
    print("instances with NO exactly-EF allocation     : %d  (%.2f%%)"
          % (len(hard), 100.0 * len(hard) / total))

    if not hard:
        return

    # minimum paid-set size among the hard instances
    dist = {}
    for _, _, n, tiers, best in hard:
        k = min(len(S) for S in tiers)
        dist[(n, k)] = dist.get((n, k), 0) + 1
    print("\nminimum |S| needed, by (n, |S|):")
    for key in sorted(dist):
        print("   n=%d  min|S| = %d : %d instances" % (key[0], key[1], dist[key]))

    # is the minimum always 1?
    worst = max(min(len(S) for S in t) for _, _, _, t, _ in hard)
    print("\nlargest minimum |S| over all hard instances  : %d" % worst)

    # in the minimum-|S| witness, is the paid agent the one with the
    # strictly-largest own cost?  (a candidate selection rule)
    agree = disagree = 0
    for cs, m, n, tiers, best in hard:
        S, bd, e = best
        prof = own_cost_profile(cs, bd, n)
        mx = max(prof)
        argmax = {i for i in range(n) if prof[i] == mx}
        if S and S <= argmax:
            agree += 1
        else:
            disagree += 1
    print("\ncandidate rule: 'the paid agents are among those of maximum own cost'")
    print("   holds in the minimum witness : %d" % agree)
    print("   fails                        : %d" % disagree)

    # show a couple of hard instances
    print("\n--- two hard instances ---")
    for cs, m, n, tiers, best in hard[:2]:
        S, bd, e = best
        print("\n  n=%d m=%d   realisable paid sets: %s"
              % (n, m, sorted(tuple(sorted(t)) for t in tiers)))
        print("  minimum witness: bundles %s  ell=%s  own costs %s"
              % ([sorted(b) for b in bd], e, own_cost_profile(cs, bd, n)))
        dump(cs, m, n)


if __name__ == "__main__":
    main()
