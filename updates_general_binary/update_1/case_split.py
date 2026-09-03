"""
The n=3 case split, and which move settles each case.

For a proof we need to know not just THAT a descending move exists but WHICH,
in terms of the structure that forces l(i) >= 2. At n=3 the envy graph has
three vertices, so a path of weight >= 2 out of agent 1 is either

    CASE A   a single arc, w(1,2) >= 2.  No positive 2-cycle then forces
             w(2,1) <= -2, so agents 1 and 2 BOTH prefer A_2 to A_1 by >= 2.
    CASE B   a two-arc path with w(1,2) = w(2,3) = 1 and every arc <= 1. No
             positive 3-cycle then forces w(3,1) <= -2.

The script confirms the split is exhaustive and then reports, for each case,
which single-item move descends: the pair of bundles the item moves between,
named RELATIVE to the case (so "1->2" means from the envier's bundle to the
envied one). If one relative move always works, that is the rule a proof has to
justify, and the proof reduces to a statement about two bundles instead of all
three.

Potential is SUM -- the sum of longest paths, minimised over assignments -- as
potentials.py shows the descent survives with it.
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
    best = None
    arg = None
    for p in PERMS:
        c = tuple(b[p[i]] for i in range(N))
        if not is_envy_freeable(vals, c):
            continue
        l = longest_paths(arc_weights(vals, c))
        if best is None or sum(l) < best:
            best, arg = sum(l), (c, l)
    return best, arg


def classify(vals, c, l):
    """Return ('A', i, j) or ('B', i, j, k) for a witnessing configuration."""
    w = arc_weights(vals, c)
    for i in range(N):
        if l[i] < 2:
            continue
        for j in range(N):
            if j != i and w[i][j] >= 2:
                return ("A", i, j, None)
        for j in range(N):
            for k in range(N):
                if len({i, j, k}) == 3 and w[i][j] + w[j][k] >= 2:
                    return ("B", i, j, k)
    return None


def main():
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    rng = random.Random(20260907)
    owners = list(itertools.product(range(N), repeat=m))
    allocs = []
    for o in owners:
        b = [0] * N
        for k, i in enumerate(o):
            b[i] |= 1 << k
        allocs.append(tuple(b))

    st = {"bad": 0, "A": 0, "B": 0, "none": 0}
    hits = {"A": {}, "B": {}}
    for _ in range(trials):
        vals = [random_gb(m, rng) for _ in range(N)]
        P = [phi(vals, b) for b in allocs]
        for a, b in enumerate(allocs):
            val, arg = P[a]
            c, l = arg
            if max(l) <= 1:
                continue
            st["bad"] += 1
            cl = classify(vals, c, l)
            if cl is None:
                st["none"] += 1
                continue
            kind, i, j, k = cl
            st[kind] += 1
            # which relative single-item move descends?
            names = {i: "envier", j: "envied", k: "third"}
            good = set()
            for src in range(N):
                for g in range(m):
                    if not c[src] & (1 << g):
                        continue
                    for dst in range(N):
                        if dst == src:
                            continue
                        nb = list(c)
                        nb[src] &= ~(1 << g)
                        nb[dst] |= 1 << g
                        v2, _ = phi(vals, tuple(nb))
                        if v2 is not None and v2 < val:
                            good.add("%s->%s" % (names.get(src, "third"),
                                                 names.get(dst, "third")))
            key = tuple(sorted(good))
            hits[kind][key] = hits[kind].get(key, 0) + 1

    print("n=3, m=%d, %d instances" % (m, trials))
    print("   states with max l >= 2      : %d" % st["bad"])
    print("   CASE A (an arc >= 2)        : %d" % st["A"])
    print("   CASE B (a 2-path of 1+1)    : %d" % st["B"])
    print("   unclassified (would be a bug): %d" % st["none"])
    for kind in ("A", "B"):
        print()
        print("   CASE %s -- which relative moves descend (top 6):" % kind)
        for key, n in sorted(hits[kind].items(), key=lambda t: -t[1])[:6]:
            print("      %-6d %s" % (n, ", ".join(key) if key else "NONE"))
        always = None
        for cand in ("envied->envier", "envier->envied", "envied->third",
                     "third->envier", "third->envied", "envier->third"):
            if all(cand in key for key in hits[kind]):
                always = cand if always is None else always + " / " + cand
        print("      move present in EVERY case: %s" % (always or "none"))


if __name__ == "__main__":
    main()
