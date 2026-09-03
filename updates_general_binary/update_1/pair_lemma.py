"""
The unified pair lemma: descend inside the pair joined by a very negative arc.

case_split.py shows the two n=3 cases are settled by moves between different
pairs of bundles -- but the SAME pair in structural terms. In case A the arc
w(1,2) >= 2 forces w(2,1) <= -2 by the 2-cycle condition, and the move is
between A_1 and A_2. In case B the path w(1,2) = w(2,3) = 1 forces w(3,1) <= -2
by the 3-cycle condition, and the move is between A_1 and A_3. Both times the
move happens inside the pair joined by an arc of weight <= -2.

    (PAIR)  Let A be envy-freeable with max_i l(i) >= 2. Then some arc has
            weight <= -2, and for a suitable such arc (y,x), moving ONE item
            between A_x and A_y strictly decreases PHI.

This is worth isolating because it is a statement about TWO bundles. If it is
true, the n=3 proof reduces to a two-agent argument, with the third agent
entering only through the cycle condition that produces the arc -- and w(y,x)
<= -2 says exactly that agent y values her own bundle at least 2 above A_x,
which with marginals in {-1,0,1} forces at least two items to separate them.

Reported in both strengths, since a proof would prefer the second:
    SUITABLE  some arc of weight <= -2 admits a descending move in its pair
    EVERY     every such arc does
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


def phi(vals, b):
    best, arg = None, None
    for p in PERMS:
        c = tuple(b[p[i]] for i in range(N))
        if not is_envy_freeable(vals, c):
            continue
        l = longest_paths(arc_weights(vals, c))
        if best is None or sum(l) < best:
            best, arg = sum(l), (c, l)
    return best, arg


def descends_in_pair(vals, c, val, x, y, m):
    for src, dst in ((x, y), (y, x)):
        for g in range(m):
            if not c[src] & (1 << g):
                continue
            nb = list(c)
            nb[src] &= ~(1 << g)
            nb[dst] |= 1 << g
            v2, _ = phi(vals, tuple(nb))
            if v2 is not None and v2 < val:
                return True
    return False


def main():
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 250
    rng = random.Random(20260908)
    allocs = []
    for o in itertools.product(range(N), repeat=m):
        b = [0] * N
        for k, i in enumerate(o):
            b[i] |= 1 << k
        allocs.append(tuple(b))

    st = {"bad": 0, "no_neg_arc": 0, "suitable": 0, "every": 0,
          "negarcs": 0}
    for _ in range(trials):
        vals = [random_gb(m, rng) for _ in range(N)]
        for b in allocs:
            val, arg = phi(vals, b)
            c, l = arg
            if max(l) <= 1:
                continue
            st["bad"] += 1
            w = arc_weights(vals, c)
            neg = [(y, x) for y in range(N) for x in range(N)
                   if y != x and w[y][x] <= -2]
            if not neg:
                st["no_neg_arc"] += 1
                continue
            st["negarcs"] += len(neg)
            oks = [descends_in_pair(vals, c, val, x, y, m) for (y, x) in neg]
            if any(oks):
                st["suitable"] += 1
            if all(oks):
                st["every"] += 1

    bad = st["bad"]
    print("n=3, m=%d, %d instances" % (m, trials))
    print("   states with max l >= 2                       : %d" % bad)
    print("   ... having NO arc of weight <= -2            : %d%s"
          % (st["no_neg_arc"],
             "   <-- such an arc always exists" if not st["no_neg_arc"] else ""))
    print("   arcs of weight <= -2 per state (avg)         : %.2f"
          % (st["negarcs"] / bad if bad else 0))
    print("   SUITABLE: some such pair admits a descent    : %d / %d%s"
          % (st["suitable"], bad,
             "   <-- (PAIR) HOLDS" if st["suitable"] == bad else ""))
    print("   EVERY:    every such pair admits a descent   : %d / %d%s"
          % (st["every"], bad,
             "   <-- even the strong form" if st["every"] == bad else ""))


if __name__ == "__main__":
    main()
