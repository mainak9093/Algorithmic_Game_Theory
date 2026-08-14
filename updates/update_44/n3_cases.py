"""Track 1, work item 1: map the residual at n = 3.

By prop:zero-coordinate, Conjecture 2 is "some allocation has max ell <= 1", and
by the two-tier characterisation with thm:paidsets-lattice the paid set at n = 3
lies in a lattice inside 2^{1,2,3} with the empty set and the whole set giving the
same condition.  So there are exactly three cases:

    |S| = 0   exact envy-freeness
    |S| = 1   one paid agent x: the unpaid pair is exactly EF BETWEEN THEMSELVES,
              x envies each of them by at most 1, and each of them strictly
              prefers its own bundle to x's
    |S| = 2   the mirror image

NOTE, correcting the plan.  I had expected to bootstrap thm:n2-complete inside the
|S| = 1 case, on the grounds that the unpaid pair must be exactly EF.  That does
not follow: thm:n2-complete gives subsidy AT MOST ONE for two agents, not exact
envy-freeness, and ex:lowerbound at n = 2 already needs a dollar.  So the two-agent
theorem is the wrong tool here and the case must be attacked directly.

What this script establishes instead, as the factual base for that attack:
  - among n = 3 instances, the split of minimal |S| over 0 / 1 / 2;
  - restricted to the EF-FREE residual (|S| >= 1), how often |S| = 1 suffices
    and how often |S| = 2 is forced;
  - for the |S| = 1 instances, whether the paid agent is characterised (max own
    cost? the agent holding a largest bundle? unique?);
  - for the |S| = 2 instances, whether the single UNPAID agent is characterised.

A characterisation of the paid agent would turn each case into a statement about
a designated agent rather than an existential over three.

Run:  python n3_cases.py
"""
from itertools import product
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_17")
from minimum_subsidy import subsets, rand_dicho, total_subsidy   # noqa: E402
sys.path.insert(0, "../update_44")
from counterexample_hunt import (f_nested, f_mixed, f_capped,     # noqa: E402
                                 f_threshold, f_disjoint, f_uniform)

N = 3


def best_allocations(cs, m):
    """All allocations with max ell <= 1, with their paid sets."""
    out = []
    for assign in product(range(N), repeat=m):
        bd = [frozenset(g for g in range(m) if assign[g] == i) for i in range(N)]
        a = [[cs[i][bd[j]] for j in range(N)] for i in range(N)]
        t, e = total_subsidy(a, N)
        if t is None or max(e) > 1:
            continue
        out.append((bd, frozenset(i for i in range(N) if e[i] == 1), a))
    return out


def main():
    rng = random.Random(303031)
    gens = [f_uniform, f_nested, f_mixed, f_capped, f_threshold, f_disjoint]
    split = Counter()
    paid_char = Counter()
    unpaid_char = Counter()
    resid = 0
    tot = 0
    nogood = 0
    print("=== n = 3: the residual by minimal |S| ===")
    print("   m   inst   |S|=0   |S|=1   |S|=2   no good allocation")
    for (m, T) in [(4, 300), (5, 200), (6, 120), (7, 60), (8, 30)]:
        loc = Counter()
        cnt = 0
        for _ in range(T):
            cs = gens[rng.randrange(len(gens))](m, N, rng)
            if max(max(c.values()) for c in cs) < 1:
                continue
            cnt += 1
            tot += 1
            good = best_allocations(cs, m)
            if not good:
                nogood += 1
                loc["none"] += 1
                continue
            k = min(len(S) for _, S, _ in good)
            loc[k] += 1
            split[k] += 1
            if k == 0:
                continue
            resid += 1
            # characterise the paid / unpaid agent at minimal |S|
            for bd, S, a in good:
                if len(S) != k:
                    continue
                own = [a[i][i] for i in range(N)]
                sz = [len(b) for b in bd]
                if k == 1:
                    x = next(iter(S))
                    paid_char["max own cost" if own[x] == max(own) else "-"] += 1
                    paid_char["max bundle" if sz[x] == max(sz) else "-"] += 1
                    paid_char["min bundle" if sz[x] == min(sz) else "-"] += 1
                elif k == 2:
                    z = next(iter(set(range(N)) - S))
                    unpaid_char["min own cost" if own[z] == min(own) else "-"] += 1
                    unpaid_char["min bundle" if sz[z] == min(sz) else "-"] += 1
                break
        print("  %2d  %5d   %5d   %5d   %5d   %d"
              % (m, cnt, loc[0], loc[1], loc[2], loc["none"]))
    print()
    print("  instances                    : %d" % tot)
    print("  no good allocation           : %d" % nogood)
    print("  minimal |S| distribution     : %s" % dict(sorted(split.items())))
    print("  EF-free residual (|S| >= 1)  : %d  (%.1f%%)"
          % (resid, 100.0 * resid / max(tot, 1)))
    print()
    print("  |S| = 1, is the paid agent characterised?")
    for k in ("max own cost", "max bundle", "min bundle"):
        print("     %-14s %d of %d" % (k, paid_char[k], split[1]))
    print("  |S| = 2, is the unpaid agent characterised?")
    for k in ("min own cost", "min bundle"):
        print("     %-14s %d of %d" % (k, unpaid_char[k], split[2]))


if __name__ == "__main__":
    main()
