"""
The stuck states of the descent, and whether a richer move set clears them.

descent.py leaves 3 states out of ~1161 with max l > 1 and no improving single
move. Three is few enough to look at individually. For each, the script prints
the envy matrix and asks whether the state is cleared by widening the moves:

    1-MOVE   transfer one item, swap two, or reassign      (what descent used)
    2-MOVE   any change to at most two items' owners
    3-MOVE   any change to at most three items' owners

If 2-MOVE clears them, the descent lemma survives with a slightly larger step
and the proof architecture stands. If nothing clears them, they are genuine
local minima of PSI and the potential itself has to change.

The instance is also solved by brute force so the gap between the stuck state
and a valid one can be read directly.
"""
import itertools
import random
import sys

from gb_valuations import (
    masks_by_popcount,
    arc_weights,
    is_envy_freeable,
    longest_paths,
)

N = 3
INF = (99,) * N


def random_gb(m, rng):
    v = [0] * (1 << m)
    for S in masks_by_popcount(m):
        if S == 0:
            continue
        bits = [1 << b for b in range(m) if S & (1 << b)]
        lo = max(v[S ^ b] for b in bits) - 1
        hi = min(v[S ^ b] for b in bits) + 1
        v[S] = rng.randint(lo, hi)
    return tuple(v)


def psi(vals, b):
    if not is_envy_freeable(vals, b):
        return INF
    return tuple(sorted(longest_paths(arc_weights(vals, b)), reverse=True))


def owners(b, m):
    o = [None] * m
    for i in range(N):
        for k in range(m):
            if b[i] & (1 << k):
                o[k] = i
    return o


def from_owners(o, m):
    b = [0] * N
    for k, i in enumerate(o):
        b[i] |= 1 << k
    return tuple(b)


def within(b, m, r):
    """Allocations differing from b in the owner of at most r items."""
    o = owners(b, m)
    seen = set()
    for size in range(1, r + 1):
        for idx in itertools.combinations(range(m), size):
            for new in itertools.product(range(N), repeat=size):
                o2 = list(o)
                for t, k in enumerate(idx):
                    o2[k] = new[t]
                c = from_owners(o2, m)
                if c != b:
                    seen.add(c)
    return seen


def main():
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 1200
    rng = random.Random(20260903)
    allocs = [from_owners(o, m) for o in itertools.product(range(N), repeat=m)]

    found = 0
    for _ in range(trials):
        vals = [random_gb(m, rng) for _ in range(N)]
        for b in allocs:
            p = psi(vals, b)
            if p == INF or p[0] <= 1:
                continue
            if any(psi(vals, c) < p for c in within(b, m, 1)
                   if sum(1 for k in range(m)
                          if owners(b, m)[k] != owners(c, m)[k]) <= 1
                   or c in within(b, m, 1)):
                continue
            # confirm stuck under the descent move set
            if any(psi(vals, c) < p for c in within(b, m, 1)):
                continue
            found += 1
            w = arc_weights(vals, b)
            print("STUCK STATE %d: bundles=%s psi=%s" % (found, b, p))
            print("   own values   : %s" % ([vals[i][b[i]] for i in range(N)],))
            print("   envy matrix w(i,j)=v_i(A_j)-v_i(A_i):")
            for i in range(N):
                print("      %s" % (w[i],))
            for r in (1, 2, 3):
                better = [c for c in within(b, m, r) if psi(vals, c) < p]
                print("   %d-MOVE improves : %s%s"
                      % (r, bool(better),
                         ("  e.g. %s psi=%s" % (better[0], psi(vals, better[0])))
                         if better else ""))
            valid = [c for c in allocs
                     if psi(vals, c) != INF and psi(vals, c)[0] <= 1]
            print("   valid allocations in this instance: %d of %d, e.g. %s"
                  % (len(valid), len(allocs), valid[0] if valid else None))
            if valid:
                d = sum(1 for k in range(m)
                        if owners(b, m)[k] != owners(valid[0], m)[k])
                print("   nearest valid differs in %d item owners"
                      % min(sum(1 for k in range(m)
                                if owners(b, m)[k] != owners(v, m)[k])
                            for v in valid))
            print()
            if found >= 3:
                return


if __name__ == "__main__":
    main()
