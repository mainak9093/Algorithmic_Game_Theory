"""
A targeted attempt to refute (DESCENT-1), before it is claimed.

(CANON) survived 2,000 random instances and then died to a hill climb, so the
same discipline is applied here first. (DESCENT-1) is:

    Let PSI(pi) be the vector (l(i))_i sorted downwards, minimised over the
    assignments of the partition pi's bundles, +infinity if none is
    envy-freeable. If PSI(pi) has maximum > 1, some partition differing from pi
    in the owner of ONE item has strictly smaller PSI.

The climb searches valuation space for a stuck partition. Its objective is the
number of partitions that are BAD (maximum > 1) and have few strictly improving
one-item neighbours, so it is driven towards states on the edge of jamming
rather than towards the middle of the class. Any state with zero improving
neighbours refutes the lemma and is printed.
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


def legal(v, m):
    for S in range(1 << m):
        for b in range(m):
            if not S & (1 << b) and v[S | (1 << b)] - v[S] not in (-1, 0, 1):
                return False
    return v[0] == 0


def build(m):
    owners = list(itertools.product(range(N), repeat=m))
    allocs = []
    for o in owners:
        b = [0] * N
        for k, i in enumerate(o):
            b[i] |= 1 << k
        allocs.append(tuple(b))
    nbr = []
    for a, o in enumerate(owners):
        nbr.append([c for c in range(len(owners))
                    if sum(1 for k in range(m) if owners[c][k] != o[k]) == 1])
    return allocs, nbr


PERMS = list(itertools.permutations(range(N)))


def psi(vals, b):
    best = INF
    for p in PERMS:
        c = tuple(b[p[i]] for i in range(N))
        if not is_envy_freeable(vals, c):
            continue
        t = tuple(sorted(longest_paths(arc_weights(vals, c)), reverse=True))
        if t < best:
            best = t
    return best


def tightness(vals, allocs, nbr):
    """(#stuck, #bad, slack) -- slack counts improving neighbours on bad states."""
    P = [psi(vals, b) for b in allocs]
    stuck = bad = slack = 0
    worst = None
    tight = 99
    for a in range(len(allocs)):
        p = P[a]
        if p != INF and p[0] <= 1:
            continue
        bad += 1
        imp = sum(1 for c in nbr[a] if P[c] < p)
        slack += imp
        tight = min(tight, imp)
        if imp == 0:
            stuck += 1
            worst = allocs[a]
    return stuck, bad, slack, worst, tight


def main():
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    seeds = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    steps = int(sys.argv[3]) if len(sys.argv) > 3 else 250
    rng = random.Random(20260905)
    allocs, nbr = build(m)
    print("n=3, m=%d : %d partitions; %d climbs x %d steps"
          % (m, len(allocs), seeds, steps))

    refuted = 0
    best_seen = None
    for s in range(seeds):
        cur = [list(random_gb(m, rng)) for _ in range(N)]
        st, bd, sl, w, tg = tightness([tuple(v) for v in cur], allocs, nbr)
        # drive the SCARCEST bad state towards zero improving neighbours;
        # prefer more bad states as a secondary pressure
        score = (tg, -bd)
        for _ in range(steps):
            i = rng.randrange(N)
            S = rng.randrange(1, 1 << m)
            old = cur[i][S]
            cur[i][S] = old + rng.choice((-1, 1))
            if not legal(tuple(cur[i]), m):
                cur[i][S] = old
                continue
            vals = [tuple(v) for v in cur]
            st2, bd2, sl2, w2, tg2 = tightness(vals, allocs, nbr)
            if st2 > 0:
                refuted += 1
                print("   REFUTED: stuck partition %s" % (w2,))
                print("      vals=%s" % (vals,))
                break
            sc2 = (tg2 if bd2 else 99, -bd2)
            if sc2 <= score:
                score = sc2
                if best_seen is None or sc2 < best_seen[0]:
                    best_seen = (sc2, bd2, tg2)
            else:
                cur[i][S] = old
    print()
    print("   climbs that refuted (DESCENT-1) : %d / %d" % (refuted, seeds))
    if best_seen:
        print("   tightest reached: %d bad states; scarcest had %d improving "
              "one-item neighbours (0 would refute)"
              % (best_seen[1], best_seen[2]))


if __name__ == "__main__":
    main()
