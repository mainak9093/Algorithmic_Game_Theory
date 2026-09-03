"""
Hunting the obstruction-free existence claim, before it is claimed.

avoid_three.py finds an obstruction-free allocation in every sampled instance,
and soundness -- obstruction-free implies valid -- follows from the verified
reduction rather than from sampling. So the only open half is existence:

    (AVOID)  every general binary instance with n=3 admits an allocation whose
             gap matrix dominates none of the 30 minimal obstruction patterns.

(AVOID) plus soundness gives PS2 for n=3.

Random sampling is worth little in this class -- (CANON) and the SUM potential
both passed thousands of instances and died to a climb -- so this hill-climbs
directly at it. The objective is the number of obstruction-free allocations an
instance admits, driven towards zero.
"""
import itertools
import random
import sys

from gb_valuations import (
    masks_by_popcount, arc_weights, is_envy_freeable, longest_paths)

N = 3


def random_gb(m, rng):
    v = [0] * (1 << m)
    for S in masks_by_popcount(m):
        if S == 0:
            continue
        bits = [1 << b for b in range(m) if S & (1 << b)]
        v[S] = rng.randint(max(v[S ^ b] for b in bits) - 1,
                           min(v[S ^ b] for b in bits) + 1)
    return tuple(v)


def legal(v, m):
    for S in range(1 << m):
        for b in range(m):
            if not S & (1 << b) and v[S | (1 << b)] - v[S] not in (-1, 0, 1):
                return False
    return v[0] == 0


def ghat(vals, c):
    G = []
    for i in range(N):
        best = max(vals[i][c[j]] for j in range(N))
        G.append(tuple(min(best - vals[i][c[j]], 2) for j in range(N)))
    return tuple(G)


def valid(vals, c):
    if not is_envy_freeable(vals, c):
        return False
    return max(longest_paths(arc_weights(vals, c))) <= 1


BASE = [((0, 0, 2), (0, 0, 2), (0, 0, 2)),
        ((0, 0, 0), (0, 2, 2), (0, 2, 2)),
        ((0, 0, 1), (0, 1, 2), (0, 1, 2))]
OBS = set()
for p in BASE:
    for rp in itertools.permutations(range(N)):
        for cp in itertools.permutations(range(N)):
            OBS.add(tuple(tuple(p[rp[i]][cp[j]] for j in range(N))
                          for i in range(N)))


def clean(G):
    return not any(all(G[i][j] >= o[i][j] for i in range(N) for j in range(N))
                   for o in OBS)


def count_clean(vals, allocs):
    return sum(1 for c in allocs if clean(ghat(vals, c)))


def main():
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    seeds = int(sys.argv[2]) if len(sys.argv) > 2 else 80
    steps = int(sys.argv[3]) if len(sys.argv) > 3 else 300
    rng = random.Random(20260917)
    allocs = []
    for o in itertools.product(range(N), repeat=m):
        b = [0] * N
        for k, i in enumerate(o):
            b[i] |= 1 << k
        allocs.append(tuple(b))
    print("n=3, m=%d : %d allocations; %d climbs x %d steps"
          % (m, len(allocs), seeds, steps))

    refuted = 0
    fewest = 10 ** 9
    for _ in range(seeds):
        cur = [list(random_gb(m, rng)) for _ in range(N)]
        cnt = count_clean([tuple(v) for v in cur], allocs)
        for _ in range(steps):
            i = rng.randrange(N)
            S = rng.randrange(1, 1 << m)
            old = cur[i][S]
            cur[i][S] = old + rng.choice((-1, 1))
            if not legal(tuple(cur[i]), m):
                cur[i][S] = old
                continue
            vals = [tuple(v) for v in cur]
            c2 = count_clean(vals, allocs)
            if c2 == 0:
                refuted += 1
                ps2 = any(valid(vals, tuple(b[p[i]] for i in range(N)))
                          for b in allocs
                          for p in itertools.permutations(range(N)))
                print("   (AVOID) REFUTED: no obstruction-free allocation; "
                      "PS2 still holds for it: %s" % ps2)
                print("      vals=%s" % (vals,))
                break
            if c2 <= cnt:
                cnt = c2
                fewest = min(fewest, c2)
            else:
                cur[i][S] = old

    print()
    print("   climbs refuting (AVOID)              : %d / %d" % (refuted, seeds))
    print("   fewest obstruction-free allocations  : %d  (0 would refute)"
          % fewest)


if __name__ == "__main__":
    main()
