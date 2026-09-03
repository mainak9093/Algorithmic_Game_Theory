"""
Stressing (INTERVAL), and setting up the Sperner argument it enables.

interval.py finds, exhaustively at m=3 and m=4, that for EVERY linear order on
the items some cut into three consecutive blocks has spread <= 1:

    (INTERVAL)  for any general binary v and any order g_1..g_m there are cuts
                0 <= a <= b <= m with
                max - min over { v(g_1..g_a), v(g_{a+1}..g_b), v(g_{b+1}..g_m) }
                at most 1.

That is the discrete shape of necklace splitting -- one measure, three parts,
two cuts -- and it makes the search space (m+1)(m+2)/2 instead of 3^m.

Part 1 climbs at it and samples m=5,6, since two claims in this line passed
random sampling and died to a climb.

Part 2 sets up the Sperner argument and reports whether its hypotheses hold.
The triangle of cuts has corners where one block is everything:
    P_1 = (m,m)   B_1 = M,   P_2 = (0,m)   B_2 = M,   P_3 = (0,0)   B_3 = M.
Labelling a cut by an index attaining the MAXIMUM value puts label j at corner
P_j whenever v(M) > 0, which is the Sperner corner condition. The boundary
condition is the question: on the edge where block j is empty, is the maximum
always attained OUTSIDE j? If it is, Sperner applies and a fully-labelled cell
exists, in which all three blocks are simultaneously maximal at neighbouring
cuts -- which with the one-step Lipschitz bound forces them within 1.
"""
import itertools
import random
import sys

from gb_valuations import masks_by_popcount, enumerate_general_binary


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


def cuts(m):
    return [(a, b) for a in range(m + 1) for b in range(a, m + 1)]


def blocks(a, b, m):
    B1 = ((1 << a) - 1)
    B2 = ((1 << b) - 1) & ~B1
    B3 = ((1 << m) - 1) & ~((1 << b) - 1)
    return B1, B2, B3


def ok(v, m, C):
    for (a, b) in C:
        B = blocks(a, b, m)
        if max(v[x] for x in B) - min(v[x] for x in B) <= 1:
            return True
    return False


def main():
    rng = random.Random(20260922)
    print("PART 1 -- sampling and climbing at (INTERVAL), natural order")
    for m, trials in ((5, 4000), (6, 1200), (7, 300)):
        C = cuts(m)
        good = sum(1 for _ in range(trials)
                   if ok(random_gb(m, rng), m, C))
        print("   m=%d : %d / %d   (%d cuts vs %d partitions)"
              % (m, good, trials, len(C), 3 ** m))

    for m, seeds, steps in ((5, 60, 300), (6, 30, 250)):
        C = cuts(m)
        refuted = 0
        for _ in range(seeds):
            cur = list(random_gb(m, rng))
            for _ in range(steps):
                S = rng.randrange(1, 1 << m)
                old = cur[S]
                cur[S] = old + rng.choice((-1, 1))
                if not legal(tuple(cur), m):
                    cur[S] = old
                    continue
                if not ok(tuple(cur), m, C):
                    refuted += 1
                    print("   (INTERVAL) REFUTED at m=%d: v=%s" % (m, tuple(cur)))
                    break
        print("   climbs at m=%d : %d, refutations %d%s"
              % (m, seeds, refuted, "   <-- holds" if not refuted else ""))

    print()
    print("PART 2 -- does the Sperner boundary condition hold?")
    for m in (3, 4):
        pool = list(enumerate_general_binary(m))
        C = cuts(m)
        corner_ok = edge_ok = tot = 0
        bad_edge = None
        for v in pool:
            if v[(1 << m) - 1] <= 0:
                continue                   # corner condition needs v(M) > 0
            tot += 1
            B = blocks(m, m, m)
            c1 = max(range(3), key=lambda t: v[B[t]]) == 0
            B = blocks(0, m, m)
            c2 = max(range(3), key=lambda t: v[B[t]]) == 1
            B = blocks(0, 0, m)
            c3 = max(range(3), key=lambda t: v[B[t]]) == 2
            if c1 and c2 and c3:
                corner_ok += 1
            good = True
            for (a, b) in C:
                B = blocks(a, b, m)
                for j in range(3):
                    if B[j] == 0:          # block j empty: is the max outside j?
                        if all(v[B[t]] <= v[B[j]] for t in range(3) if t != j) \
                                and any(v[B[t]] < v[B[j]] for t in range(3)
                                        if t != j):
                            good = False
            if good:
                edge_ok += 1
            elif bad_edge is None:
                bad_edge = v
        print("   m=%d, %d valuations with v(M) > 0" % (m, tot))
        print("      corner condition holds : %d / %d%s"
              % (corner_ok, tot, "   <-- always" if corner_ok == tot else ""))
        print("      boundary condition     : %d / %d%s"
              % (edge_ok, tot,
                 "   <-- always" if edge_ok == tot else "   <-- FAILS"))
        if bad_edge is not None:
            print("      a valuation breaking the boundary condition: %s"
                  % (bad_edge,))


if __name__ == "__main__":
    main()
