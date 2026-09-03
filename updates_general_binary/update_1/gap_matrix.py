"""
A finite reduction: validity depends only on a 3x3 matrix over {0,1,2+}.

Start from the verified reformulation (approach 16 section 1): an allocation is
valid iff for some price vector q in {0,1}^3 every agent holds a bundle
maximising v_i(B_j) + q_j. Write

    g_i(j) = max_k v_i(B_k) - v_i(B_j)  >= 0,

agent i's GAP from her best bundle to bundle j. Every row of G has a zero.
Since v_i(B_j) + q_j = (max_k v_i(B_k)) - g_i(j) + q_j, agent i demands the j
maximising q_j - g_i(j), and that quantity lies in {1, 0, -1, ...} with the
maximum always at least 0 (take j with g_i(j) = 0). So

    if some j has g_i(j) = 0 and q_j = 1:  D_i = { j : g_i(j)=0, q_j=1 }
    otherwise:                             D_i = { j : g_i(j)=0 }
                                                 u { j : g_i(j)=1, q_j=1 }

In both branches only whether g_i(j) is 0, 1, or AT LEAST 2 is ever consulted.
Therefore:

    VALIDITY OF AN ALLOCATION IS A FUNCTION OF THE 3x3 MATRIX
    ghat_i(j) = min(g_i(j), 2), each of whose rows contains a zero.

There are only 19 possible rows (27 vectors over {0,1,2} minus the 8 with no
zero), so 19^3 = 6859 matrices in all. The whole question becomes finite: which
of those 6859 patterns are valid, and which must be avoided.

This script derives the classification and then CHECKS it against the
envy-graph implementation on random instances -- if any allocation's validity
disagrees with its pattern's verdict, the reduction is wrong.
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


def perfect_matching(adj):
    match = [-1] * N
    def go(i, seen):
        for j in adj[i]:
            if not seen[j]:
                seen[j] = True
                if match[j] == -1 or go(match[j], seen):
                    match[j] = i
                    return True
        return False
    return sum(1 for i in range(N) if go(i, [False] * N)) == N


def pattern_valid(G):
    """G is a 3x3 tuple over {0,1,2}, each row containing a 0."""
    for mask in range(1 << N):
        q = [(mask >> j) & 1 for j in range(N)]
        adj = []
        for i in range(N):
            hit = [j for j in range(N) if G[i][j] == 0 and q[j] == 1]
            if hit:
                adj.append(hit)
            else:
                adj.append([j for j in range(N)
                            if G[i][j] == 0 or (G[i][j] == 1 and q[j] == 1)])
        if perfect_matching(adj):
            return True
    return False


def ghat(vals, c):
    G = []
    for i in range(N):
        best = max(vals[i][c[j]] for j in range(N))
        G.append(tuple(min(best - vals[i][c[j]], 2) for j in range(N)))
    return tuple(G)


def valid_envygraph(vals, c):
    if not is_envy_freeable(vals, c):
        return False
    return max(longest_paths(arc_weights(vals, c))) <= 1


def good_multiset(vals, b):
    """
    The pattern test asks whether SOME assignment of these bundles is valid --
    validity is a property of the multiset, not of the assignment (approach 16
    section 1). The gap matrix is likewise a function of the bundle list alone.
    So the honest comparison quantifies over assignments on both sides.
    """
    return any(valid_envygraph(vals, tuple(b[p[i]] for i in range(N)))
               for p in itertools.permutations(range(N)))


def main():
    rows = [r for r in itertools.product((0, 1, 2), repeat=N) if 0 in r]
    print("possible rows (a zero in each): %d" % len(rows))
    pats = list(itertools.product(rows, repeat=N))
    print("possible gap patterns          : %d" % len(pats))

    good = {p for p in pats if pattern_valid(p)}
    print("   valid patterns              : %d" % len(good))
    print("   FORBIDDEN patterns          : %d" % (len(pats) - len(good)))

    # cross-check against the envy graph
    rng = random.Random(20260915)
    checked = mismatch = 0
    bad = []
    for m, trials in ((3, 1500), (4, 400), (5, 120)):
        allocs = []
        for o in itertools.product(range(N), repeat=m):
            b = [0] * N
            for k, i in enumerate(o):
                b[i] |= 1 << k
            allocs.append(tuple(b))
        for _ in range(trials):
            vals = [random_gb(m, rng) for _ in range(N)]
            for c in allocs:
                checked += 1
                if good_multiset(vals, c) != (ghat(vals, c) in good):
                    mismatch += 1
                    if len(bad) < 3:
                        bad.append((m, vals, c, ghat(vals, c)))
    print()
    print("cross-check against the envy-graph implementation")
    print("   allocations checked : %d" % checked)
    print("   MISMATCHES          : %d%s"
          % (mismatch, "   <-- reduction verified" if not mismatch else ""))
    for w in bad:
        print("      m=%d bundles=%s pattern=%s" % (w[0], w[2], w[3]))

    # what do the forbidden patterns look like?
    forb = [p for p in pats if p not in good]
    print()
    print("shape of the forbidden patterns:")
    byzeros = {}
    for p in forb:
        z = sum(1 for i in range(N) for j in range(N) if p[i][j] == 0)
        byzeros[z] = byzeros.get(z, 0) + 1
    print("   by number of zero entries: %s" % dict(sorted(byzeros.items())))
    print("   examples:")
    for p in forb[:6]:
        print("      %s" % (p,))


if __name__ == "__main__":
    main()
