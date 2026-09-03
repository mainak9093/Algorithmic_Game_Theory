"""
The hunt (PAIR) has not yet faced.

approach_17 section 6 records (PAIR) as verified 387 of 387 but NOT attacked by
a hill climb -- and (CANON) passed 2,250 random instances before dying to
exactly such a climb. This runs that attack.

    (PAIR)  Let A be envy-freeable with max_i l(i) >= 2. Lemma 2 forces some
            arc of weight <= -2. Then for a SUITABLE such arc (y,x), moving one
            item between A_x and A_y strictly decreases PHI.

For each state with max l >= 2, count the arcs of weight <= -2 whose pair
admits a descending one-item move -- call it the state's SUITABLE count.
(PAIR) says every such state has SUITABLE >= 1, so the climb drives the
scarcest state's SUITABLE towards 0, with more bad states as secondary
pressure. This is the same objective shape that broke (CANON).

Two outcomes are worth distinguishing, so both are reported:

    PAIR refuted    some bad state has SUITABLE = 0
    DESCENT too     that state also has no descending one-item move ANYWHERE,
                    which would refute (DESCENT-1) as well

If (PAIR) falls but (DESCENT-1) survives, the descent is still fine and only
the two-bundle reduction of section 6 needs replacing.
"""
import itertools
import random
import sys

from gb_valuations import (
    masks_by_popcount, arc_weights, is_envy_freeable, longest_paths)

N = 3
PERMS = list(itertools.permutations(range(N)))


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


def phi(vals, b):
    best, arg = None, None
    for p in PERMS:
        c = tuple(b[p[i]] for i in range(N))
        if not is_envy_freeable(vals, c):
            continue
        l = longest_paths(arc_weights(vals, c))
        # PSI is the SORTED vector, not the sum. verify_stuck.py shows the sum
        # is refuted: a bad state (0,0,2) sums to 2 while a valid state (1,1,1)
        # sums to 3, so the sum RISES on the way to a solution, and a descent
        # on it jams one item short of the answer. Lexicographic order on the
        # downward-sorted vector ranks (1,1,1) below (2,0,0) correctly.
        t = tuple(sorted(l, reverse=True))
        if best is None or t < best:
            best, arg = t, (c, l)
    return best, arg


def moves_between(c, x, y, m):
    for src, dst in ((x, y), (y, x)):
        for g in range(m):
            if c[src] & (1 << g):
                nb = list(c)
                nb[src] &= ~(1 << g)
                nb[dst] |= 1 << g
                yield tuple(nb)


def all_moves(c, m):
    for src in range(N):
        for dst in range(N):
            if src == dst:
                continue
            for g in range(m):
                if c[src] & (1 << g):
                    nb = list(c)
                    nb[src] &= ~(1 << g)
                    nb[dst] |= 1 << g
                    yield tuple(nb)


def scan(vals, allocs, m):
    """(min SUITABLE over bad states, #bad, refuting witness or None)."""
    worst = 99
    bad = 0
    wit = None
    for b in allocs:
        val, arg = phi(vals, b)
        if arg is None:
            continue
        c, l = arg
        if max(l) <= 1:
            continue
        bad += 1
        w = arc_weights(vals, c)
        neg = [(y, x) for y in range(N) for x in range(N)
               if y != x and w[y][x] <= -2]
        suitable = 0
        for (y, x) in neg:
            if any((phi(vals, nb)[0] is not None and phi(vals, nb)[0] < val)
                   for nb in moves_between(c, x, y, m)):
                suitable += 1
        if suitable < worst:
            worst = suitable
        if suitable == 0:
            anywhere = any((phi(vals, nb)[0] is not None
                            and phi(vals, nb)[0] < val)
                           for nb in all_moves(c, m))
            wit = (c, l, neg, anywhere)
    return worst, bad, wit


def main():
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    seeds = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    steps = int(sys.argv[3]) if len(sys.argv) > 3 else 200
    rng = random.Random(20260909)
    allocs = []
    for o in itertools.product(range(N), repeat=m):
        b = [0] * N
        for k, i in enumerate(o):
            b[i] |= 1 << k
        allocs.append(tuple(b))
    print("n=3, m=%d : %d partitions; %d climbs x %d steps"
          % (m, len(allocs), seeds, steps))

    refuted = descent_too = 0
    best = None
    for _ in range(seeds):
        cur = [list(random_gb(m, rng)) for _ in range(N)]
        wst, bad, wit = scan([tuple(v) for v in cur], allocs, m)
        score = (wst if bad else 99, -bad)
        for _ in range(steps):
            i = rng.randrange(N)
            S = rng.randrange(1, 1 << m)
            old = cur[i][S]
            cur[i][S] = old + rng.choice((-1, 1))
            if not legal(tuple(cur[i]), m):
                cur[i][S] = old
                continue
            vals = [tuple(v) for v in cur]
            w2, b2, wit2 = scan(vals, allocs, m)
            if wit2 is not None:
                refuted += 1
                c, l, neg, anywhere = wit2
                print("   (PAIR) REFUTED: bundles=%s l=%s negarcs=%s" % (c, l, neg))
                print("      descending move ANYWHERE? %s%s"
                      % (anywhere, "" if anywhere else "   <-- (DESCENT-1) TOO"))
                if not anywhere:
                    descent_too += 1
                print("      vals=%s" % (vals,))
                break
            s2 = (w2 if b2 else 99, -b2)
            if s2 <= score:
                score = s2
                if best is None or s2 < best[0]:
                    best = (s2, w2, b2)
            else:
                cur[i][S] = old

    print()
    print("   climbs refuting (PAIR)      : %d / %d" % (refuted, seeds))
    print("   ... which also refute (DESCENT-1) : %d" % descent_too)
    if best:
        print("   tightest reached: %d bad states; scarcest had %d suitable "
              "arcs (0 would refute)" % (best[2], best[1]))


if __name__ == "__main__":
    main()
