"""
Targeted probe at the configuration that breaks (TRANSFER-2).

transfer2.py shows the arc-shrinking mechanism fails at gap exactly 2. The
witness is a saturating valuation -- singletons 0, pairs -1, triples -2, the
whole set -2 -- with A_1 everything and A_2 empty. Moving one item leaves the
gap at 2 (the triple is still worth -2 and the singleton 0); only moving two
items closes it. Since Lemma 2 delivers gap exactly 2 and no more, this is
precisely the structure a proof of (PAIR) has to survive.

So rather than sampling the class, this builds instances AROUND that structure:
agent 1 gets the saturating valuation, agents 2 and 3 range over the class, and
the partition tested is the one that realises the obstruction. If (PAIR) or
(DESCENT-1) can fail anywhere, this is where.

Reported separately, because the consequences differ:
    PAIR fails      no arc of weight <= -2 has a descending move in its pair
    DESCENT fails   no one-item move descends at all -- would refute the
                    whole approach 17 route
"""
import itertools
import random
import sys

from gb_valuations import (
    masks_by_popcount, enumerate_general_binary,
    arc_weights, is_envy_freeable, longest_paths)

N = 3
PERMS = list(itertools.permutations(range(N)))


def saturating(m, cap):
    """v(S) = -min(|S|, cap): singletons 0 only if cap=0; general chores form."""
    return tuple(-min(bin(S).count("1"), cap) for S in range(1 << m))


def shifted_saturating(m, cap):
    """The transfer2 witness: 0,0,-1,-2,-2 by size -- flat then saturating."""
    def f(k):
        if k <= 1:
            return 0
        return -min(k - 1, cap)
    return tuple(f(bin(S).count("1")) for S in range(1 << m))


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


def main():
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
    rng = random.Random(20260910)

    v1 = shifted_saturating(m, 2)
    print("agent 1 fixed to the (TRANSFER-2) witness valuation:")
    print("   by bundle size: %s"
          % [v1[(1 << k) - 1] for k in range(m + 1)])

    allocs = []
    for o in itertools.product(range(N), repeat=m):
        b = [0] * N
        for k, i in enumerate(o):
            b[i] |= 1 << k
        allocs.append(tuple(b))

    st = {"inst": 0, "bad": 0, "pair_fail": 0, "descent_fail": 0,
          "gap2_states": 0}
    for _ in range(trials):
        vals = [v1, random_gb(m, rng), random_gb(m, rng)]
        st["inst"] += 1
        for b in allocs:
            val, arg = phi(vals, b)
            if arg is None:
                continue
            c, l = arg
            if max(l) <= 1:
                continue
            st["bad"] += 1
            w = arc_weights(vals, c)
            neg = [(y, x) for y in range(N) for x in range(N)
                   if y != x and w[y][x] <= -2]
            if any(w[y][x] == -2 for (y, x) in neg):
                st["gap2_states"] += 1

            def better(nb):
                p2, _ = phi(vals, nb)
                return p2 is not None and p2 < val

            pair_ok = False
            for (y, x) in neg:
                for src, dst in ((x, y), (y, x)):
                    for g in range(m):
                        if c[src] & (1 << g):
                            nb = list(c)
                            nb[src] &= ~(1 << g)
                            nb[dst] |= 1 << g
                            if better(tuple(nb)):
                                pair_ok = True
                                break
                    if pair_ok:
                        break
                if pair_ok:
                    break
            if pair_ok:
                continue
            st["pair_fail"] += 1
            any_ok = False
            for src in range(N):
                for dst in range(N):
                    if src == dst:
                        continue
                    for g in range(m):
                        if c[src] & (1 << g):
                            nb = list(c)
                            nb[src] &= ~(1 << g)
                            nb[dst] |= 1 << g
                            if better(tuple(nb)):
                                any_ok = True
            if not any_ok:
                st["descent_fail"] += 1
                print("   (DESCENT-1) REFUTED: bundles=%s l=%s" % (c, l))
                print("      vals=%s" % (vals,))
            else:
                print("   (PAIR) fails but descent survives: bundles=%s l=%s negarcs=%s"
                      % (c, l, neg))

    print()
    print("   instances                         : %d" % st["inst"])
    print("   states with max l >= 2            : %d" % st["bad"])
    print("   ... of which have an arc = -2     : %d" % st["gap2_states"])
    print("   (PAIR) failures                   : %d%s"
          % (st["pair_fail"], "   <-- holds" if not st["pair_fail"] else ""))
    print("   (DESCENT-1) failures              : %d%s"
          % (st["descent_fail"], "   <-- holds" if not st["descent_fail"] else ""))


if __name__ == "__main__":
    main()
