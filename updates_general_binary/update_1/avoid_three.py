"""
A sufficient condition for validity, and whether it can always be met.

gap_matrix.py reduces validity to the 3x3 matrix ghat_i(j) = min(g_i(j), 2)
with g_i(j) = max_k v_i(B_k) - v_i(B_j). gap_minimal.py shows every FORBIDDEN
pattern dominates one of three canonical ones, up to relabelling agents and
bundles:

    C   [(0,0,2),(0,0,2),(0,0,2)]   all three agents rank one bundle >= 2
                                    below their best -- nobody can take it
    A   [(0,0,0),(0,2,2),(0,2,2)]   two agents rank one bundle >= 2 above both
                                    others -- both must have it
    B   [(0,0,1),(0,1,2),(0,1,2)]   the mixed case

Domination is necessary for invalidity but NOT sufficient -- 90 valid patterns
also dominate one -- which is exactly the useful direction:

    AN ALLOCATION WHOSE GAP MATRIX DOMINATES NONE OF C, A, B IS VALID.

That is a sufficient condition written directly in the valuations, with no
envy graph, no longest path and no price vector in it. If every instance admits
such an allocation, PS2 for n=3 follows immediately.

So the question this script answers is exactly that: how often does an instance
admit an obstruction-free allocation, and when it does not, does it still admit
a valid one (i.e. is the sufficient condition merely not necessary, or is the
route blocked)?
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


def good_multiset(vals, b):
    """
    Both the gap matrix and the pattern test are functions of the bundle LIST,
    and say whether SOME assignment of those bundles is valid. Comparing them
    against one fixed assignment is the mistake that made the first run of this
    script report zero soundness.
    """
    return any(valid(vals, tuple(b[p[i]] for i in range(N)))
               for p in itertools.permutations(range(N)))


BASE = [((0, 0, 2), (0, 0, 2), (0, 0, 2)),
        ((0, 0, 0), (0, 2, 2), (0, 2, 2)),
        ((0, 0, 1), (0, 1, 2), (0, 1, 2))]


def orbit(p):
    out = set()
    for rp in itertools.permutations(range(N)):
        for cp in itertools.permutations(range(N)):
            out.add(tuple(tuple(p[rp[i]][cp[j]] for j in range(N))
                          for i in range(N)))
    return out


OBS = set()
for p in BASE:
    OBS |= orbit(p)


def clean(G):
    """True iff G dominates none of the three obstructions."""
    for o in OBS:
        if all(G[i][j] >= o[i][j] for i in range(N) for j in range(N)):
            return False
    return True


def main():
    rng = random.Random(20260916)
    print("obstruction orbit size: %d patterns" % len(OBS))
    print()
    for m, trials in ((3, 2000), (4, 600), (5, 150)):
        allocs = []
        for o in itertools.product(range(N), repeat=m):
            b = [0] * N
            for k, i in enumerate(o):
                b[i] |= 1 << k
            allocs.append(tuple(b))
        st = {"inst": 0, "clean": 0, "ps2": 0, "sound": 0}
        for _ in range(trials):
            vals = [random_gb(m, rng) for _ in range(N)]
            st["inst"] += 1
            cl = [c for c in allocs if clean(ghat(vals, c))]
            if cl:
                st["clean"] += 1
                if all(good_multiset(vals, c) for c in cl):
                    st["sound"] += 1
            else:
                st["sound"] += 1        # vacuous
            if any(good_multiset(vals, c) for c in allocs):
                st["ps2"] += 1
        print("   m=%d (%d instances): admits an obstruction-free allocation %d"
              "  | PS2 holds %d  | every clean allocation really is valid %d%s"
              % (m, st["inst"], st["clean"], st["ps2"], st["sound"],
                 "" if st["clean"] == st["inst"] else
                 "   <-- NOT always obstruction-free"))


if __name__ == "__main__":
    main()
