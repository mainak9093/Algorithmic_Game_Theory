"""
Do sections 12, 13 and 27 really rule out local moves?

PS3_n3_current_state_from_scratch.md concludes (section 27) that "the eventual
proof must permit GLOBAL redistribution, not just bounded-size local moves",
on the strength of two counterexamples:

  section 12  allocations that are locally WELFARE-maximal under every
              single-item transfer yet still need subsidy 2;
  section 13  the pure-chores allocation ({a,b,c}, {}, {}) with v_i(S) = -|S|,
              which needs subsidy 3 and is not repaired by one transfer or one
              swap REACHING the answer.

Neither refutes local moves as such. Both refute a particular OBJECTIVE:
section 12 refutes hill-climbing on welfare, and section 13 refutes expecting a
single move to land on a valid allocation outright. Approach 17 uses a
different potential,

    PSI(pi) = the vector (l(i))_i sorted downwards, MINIMISED over the
              assignments of the partition's bundles, compared
              lexicographically,

and asks only that one item move strictly DECREASES it -- not that it reaches
the answer, and not that it improves welfare. This script checks whether PSI
descends at exactly the states sections 12 and 13 exhibit.

Note the potential must be the sorted vector: the sum version is refuted (see
verify_stuck.py), because l = (0,0,2) sums to 2 while l = (1,1,1) sums to 3, so
the sum rises on the way to a solution.
"""
import itertools
import sys

from gb_valuations import arc_weights, is_envy_freeable, longest_paths

N = 3
PERMS = list(itertools.permutations(range(N)))


def psi(vals, b):
    best = None
    for p in PERMS:
        c = tuple(b[p[i]] for i in range(N))
        if not is_envy_freeable(vals, c):
            continue
        t = tuple(sorted(longest_paths(arc_weights(vals, c)), reverse=True))
        if best is None or t < best:
            best = t
    return best


def welfare(vals, c):
    return sum(vals[i][c[i]] for i in range(N))


def one_moves(c, m):
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


def allocs(m):
    out = []
    for o in itertools.product(range(N), repeat=m):
        b = [0] * N
        for k, i in enumerate(o):
            b[i] |= 1 << k
        out.append(tuple(b))
    return out


def report(tag, vals, c, m):
    p = psi(vals, c)
    desc = [nb for nb in one_moves(c, m) if psi(vals, nb) is not None
            and psi(vals, nb) < p]
    wel = welfare(vals, c)
    wbetter = [nb for nb in one_moves(c, m) if welfare(vals, nb) > wel]
    print("   %s" % tag)
    print("      PSI = %s   (needs subsidy %d)" % (p, p[0]))
    print("      one-item moves improving WELFARE : %d%s"
          % (len(wbetter), "   <-- locally welfare-maximal" if not wbetter else ""))
    print("      one-item moves decreasing PSI    : %d%s"
          % (len(desc), "   <-- PSI DESCENDS" if desc else "   <-- stuck"))
    if desc:
        print("         e.g. %s  PSI %s -> %s"
              % (desc[0], p, psi(vals, desc[0])))
    return bool(desc)


def main():
    # ---- section 13's example: pure chores, everything on one agent
    m = 3
    v = tuple(-bin(S).count("1") for S in range(1 << m))
    vals = [v, v, v]
    print("SECTION 13 -- v_i(S) = -|S|, A = ({a,b,c}, {}, {})")
    report("state", vals, (0b111, 0, 0), m)
    print()

    # ---- section 12's class: locally welfare-maximal but invalid, searched for
    print("SECTION 12 -- states locally welfare-maximal under every one-item")
    print("transfer, yet needing subsidy >= 2. Sweeping the m=3 chores class")
    print("and a mixed class for such states, then testing PSI on each:")
    from gb_valuations import enumerate_class
    pool = enumerate_class(m, {-1, 0, 1})
    A = allocs(m)
    found = psi_ok = 0
    examples = []
    import random
    rng = random.Random(20260914)
    sample = [tuple(rng.choice(pool) for _ in range(N)) for _ in range(4000)]
    for vals in sample:
        vals = list(vals)
        for c in A:
            p = psi(vals, c)
            if p is None or p[0] <= 1:
                continue
            wel = welfare(vals, c)
            if any(welfare(vals, nb) > wel for nb in one_moves(c, m)):
                continue                       # not locally welfare-maximal
            found += 1
            if any(psi(vals, nb) is not None and psi(vals, nb) < p
                   for nb in one_moves(c, m)):
                psi_ok += 1
            elif len(examples) < 3:
                examples.append((vals, c, p))
    print("      locally welfare-maximal states needing subsidy >= 2 : %d" % found)
    print("      ... of which PSI still descends by ONE item move    : %d%s"
          % (psi_ok, "   <-- ALL of them" if psi_ok == found else ""))
    for vals, c, p in examples:
        print("      PSI-stuck example: bundles=%s PSI=%s vals=%s" % (c, p, vals))


if __name__ == "__main__":
    main()
