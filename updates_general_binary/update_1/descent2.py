"""
The descent lemma with two-item moves, over PARTITIONS.

stuck.py shows every state where single-item descent jams is cleared by a move
that changes the owner of TWO items. So the candidate is:

    (DESCENT-2)  Let A be any allocation with max_i l_A(i) > 1, or one that is
                 not envy-freeable. Then some allocation differing from A in
                 the owners of at most two items has a strictly smaller PSI,
                 where PSI(A) is the vector (l_A(i))_i sorted downwards,
                 compared lexicographically, and +infinity when A is not
                 envy-freeable.

PSI takes finitely many values and every step decreases it strictly, so
iterating must terminate, and it can only stop where max_i l <= 1. (DESCENT-2)
therefore proves PS2 for n = 3 outright -- not (S2), not a warm-up, the thing
itself -- and it does so constructively, with a two-item local search.

Every allocation of every sampled instance is tested, not just the reachable
ones, so the lemma is checked in the strong form a proof would need. The
1-move column is kept alongside to show the second item is doing real work.
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


def psi_one(vals, b):
    if not is_envy_freeable(vals, b):
        return INF
    return tuple(sorted(longest_paths(arc_weights(vals, b)), reverse=True))


def psi(vals, b):
    """
    Section 1 of approach 16: validity is a property of the bundle MULTISET,
    not of the assignment. So the state of the descent is the partition, and
    its potential is the best any assignment of those bundles achieves. A
    partition whose bundles admit an envy-freeable assignment therefore never
    scores INF, which is what stopped the previous version: it treated every
    non-envy-freeable ALLOCATION as equally bad and let the descent jam among
    them.
    """
    return min(psi_one(vals, tuple(b[p[i]] for i in range(N)))
               for p in itertools.permutations(range(N)))


def main():
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 800
    rng = random.Random(20260904)

    owners = list(itertools.product(range(N), repeat=m))
    def bundles(o):
        b = [0] * N
        for k, i in enumerate(o):
            b[i] |= 1 << k
        return tuple(b)
    allocs = [bundles(o) for o in owners]

    nbr1, nbr2 = [], []
    for a, o in enumerate(owners):
        n1, n2 = [], []
        for idx in range(len(owners)):
            d = sum(1 for k in range(m) if owners[idx][k] != o[k])
            if d == 1:
                n1.append(idx)
            elif d == 2:
                n2.append(idx)
        nbr1.append(n1)
        nbr2.append(n1 + n2)

    st = {"inst": 0, "states": 0, "bad": 0, "stuck1": 0, "stuck2": 0,
          "solved": 0}
    ex = []
    for _ in range(trials):
        vals = [random_gb(m, rng) for _ in range(N)]
        st["inst"] += 1
        P = [psi(vals, b) for b in allocs]
        if any(p != INF and p[0] <= 1 for p in P):
            st["solved"] += 1
        for a in range(len(allocs)):
            st["states"] += 1
            p = P[a]
            if p != INF and p[0] <= 1:
                continue
            st["bad"] += 1
            if not any(P[c] < p for c in nbr1[a]):
                st["stuck1"] += 1
            if not any(P[c] < p for c in nbr2[a]):
                st["stuck2"] += 1
                if len(ex) < 3:
                    ex.append((vals, allocs[a], p))

    print("n=3, m=%d : %d instances, %d allocations each" % (m, trials, len(allocs)))
    print()
    print("   states examined                        : %d" % st["states"])
    print("   PS2 holds (some valid allocation)      : %d / %d" % (st["solved"], st["inst"]))
    print("   states needing descent (max l > 1)     : %d" % st["bad"])
    print("   ... stuck under ONE-item moves         : %d" % st["stuck1"])
    print("   ... stuck under TWO-item moves         : %d%s"
          % (st["stuck2"],
             "   <-- (DESCENT-2) HOLDS" if not st["stuck2"] else "   <-- REFUTED"))
    for vals, b, p in ex:
        print("      stuck: bundles=%s psi=%s vals=%s" % (b, p, vals))


if __name__ == "__main__":
    main()
