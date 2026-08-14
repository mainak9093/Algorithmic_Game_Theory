"""Characterise the chain-good MATRICES, exhaustively.

The induction needs to know what set it is aiming at.  Since level-k goodness
depends only on a_ij = c_i(A_j), and every non-negative integer matrix is
realisable, "which matrices are chain-good" is decidable by enumeration.

CANDIDATE (the one that would make the induction work).  By the two-tier
characterisation, good at level k means there is a bipartition S_k of the agents
with

    i,j same side      :  min(a_ii,k) <= min(a_ij,k)
    i in S_k, j out    :  min(a_ii,k) <= min(a_ij,k) + 1
    i out,  j in S_k   :  min(a_ii,k) + 1 <= min(a_ij,k)

Chain-good only asks for SOME S_k at each level.  If a SINGLE S works at every
level, the induction has something concrete to carry: a bipartition, fixed once,
valid all the way up the layer stack.

Tested here:
  Q1  chain-good  <=>  exists one S valid at every level?
  Q2  is the canonical tier set S_k = {i : ell^(k)(i) = 1} constant in k?
  Q3  does checking k only at the distinct entries of a suffice?

Run:  python chain_matrices.py [maxentry]
"""
from itertools import product
import sys


def levels(a, n, K):
    out = []
    for k in range(1, K + 1):
        W = [[min(a[i][i], k) - min(a[i][j], k) for j in range(n)]
             for i in range(n)]
        e = [0] * n
        ok = True
        for _ in range(n + 1):
            ch = False
            new = list(e)
            for i in range(n):
                for j in range(n):
                    if i != j and W[i][j] + e[j] > new[i]:
                        new[i] = W[i][j] + e[j]; ch = True
            e = new
            if not ch:
                break
        else:
            ok = False
        out.append((ok and max(e) <= 1, tuple(e) if ok else None))
    return out


def tier_ok(a, n, k, S):
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            x, y = min(a[i][i], k), min(a[i][j], k)
            if (i in S) == (j in S):
                if x > y:
                    return False
            elif i in S:
                if x > y + 1:
                    return False
            else:
                if x + 1 > y:
                    return False
    return True


def single_S(a, n, K):
    """Is there ONE bipartition valid at every level?  Return it or None."""
    for bits in product([0, 1], repeat=n):
        S = {i for i in range(n) if bits[i]}
        if all(tier_ok(a, n, k, S) for k in range(1, K + 1)):
            return S
    return None


def main():
    V = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    n = 3
    tot = chain = q1_bad = q2_bad = q3_bad = 0
    ex = None
    for flat in product(range(V + 1), repeat=n * n):
        a = [list(flat[i * n:(i + 1) * n]) for i in range(n)]
        K = max(max(r) for r in a)
        if K < 2:
            continue
        tot += 1
        L = levels(a, n, K)
        cg = all(g for g, _ in L)
        if not cg:
            # Q1 reverse direction: no single S may exist either
            if single_S(a, n, K) is not None:
                q1_bad += 1
            continue
        chain += 1

        # Q1: chain-good => a single bipartition works at every level
        S = single_S(a, n, K)
        if S is None:
            q1_bad += 1
            if ex is None:
                ex = (a, L)

        # Q2: canonical tier sets constant across levels
        tiers = {tuple(sorted(i for i in range(n) if e[i] == 1)) for _, e in L}
        if len(tiers) > 1:
            q2_bad += 1

        # Q3: checking only at distinct entries suffices
        pts = sorted({v for r in a for v in r if v >= 1} | {K})
        if all(levels(a, n, K)[k - 1][0] for k in pts) != cg:
            q3_bad += 1

    print("n=%d, entries 0..%d" % (n, V))
    print("  matrices with K>=2                        : %d" % tot)
    print("  chain-good                                : %d" % chain)
    print("  Q1  chain-good  <=>  one S for all levels : %d mismatches" % q1_bad)
    print("  Q2  canonical tier set constant in k      : %d violations" % q2_bad)
    print("  Q3  breakpoints suffice                   : %d violations" % q3_bad)
    if ex:
        a, L = ex
        print("\n  chain-good but NO single bipartition:")
        for r in a:
            print("     ", r)
        print("   per-level subsidies:", [e for _, e in L])


if __name__ == "__main__":
    main()
