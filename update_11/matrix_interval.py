"""Claim (I) as a pure matrix statement, searched exhaustively.

REDUCTION.  For a fixed allocation the level-k envy graph depends only on the
cost matrix a_ij = c_i(A_j):

        w^(k)(i,j) = min(a_ii,k) - min(a_ij,k).

Every non-negative integer matrix is realisable by a dichotomous instance: put
c_i(S) := sum_j min(|S ∩ A_j|, a_ij).  Each marginal is 0 or 1, c_i(empty)=0,
and c_i(A_j) = a_ij whenever a_ij <= |A_j|, which we can always arrange by
taking the bundles large enough.  So

    Claim (I) for dichotomous instances  <=>  Claim (I) for ALL such matrices,

and the matrix version can be enumerated exhaustively rather than sampled.

CLAIM (I).  For every matrix, { k : the level-k graph is good } is an interval.
CLAIM (II). good at level 1 and level K  =>  good at every level between.
            (II) follows from (I), so a counterexample to (II) is one to (I).

Run:  python matrix_interval.py [maxentry]
"""
from itertools import product
import sys


def levels_good(a, n, K):
    """Return the list of booleans: good at level k, for k = 1..K."""
    out = []
    for k in range(1, K + 1):
        W = [[min(a[i][i], k) - min(a[i][j], k) for j in range(n)]
             for i in range(n)]
        # Bellman-Ford for longest walks; None on a positive cycle
        e = [0] * n
        ok = True
        for _ in range(n + 1):
            ch = False
            new = list(e)
            for i in range(n):
                for j in range(n):
                    if i != j and W[i][j] + e[j] > new[i]:
                        new[i] = W[i][j] + e[j]
                        ch = True
            e = new
            if not ch:
                break
        else:
            ok = False                      # still improving: positive cycle
        out.append(ok and max(e) <= 1)
    return out


def is_interval(flags):
    idx = [i for i, v in enumerate(flags) if v]
    return (not idx) or idx == list(range(idx[0], idx[-1] + 1))


def realise(a, n):
    """Explicit dichotomous witness for a matrix, as a sanity check:
    bundles A_j of size max_i a_ij, c_i(S) = sum_j min(|S ∩ A_j|, a_ij)."""
    sizes = [max(a[i][j] for i in range(n)) for j in range(n)]
    return sizes


def main():
    V = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    for n in (3, 4):
        if n == 4 and V > 2:
            Vn = 2
        else:
            Vn = V
        tot = bad1 = bad2 = 0
        worst = None
        for flat in product(range(Vn + 1), repeat=n * n):
            a = [list(flat[i * n:(i + 1) * n]) for i in range(n)]
            K = max(max(r) for r in a)
            if K < 2:
                continue                    # nothing to interpolate
            tot += 1
            flags = levels_good(a, n, K)
            if not is_interval(flags):
                bad1 += 1
                if worst is None:
                    worst = (a, flags)
            if flags[0] and flags[-1] and not all(flags):
                bad2 += 1
        print("n=%d, entries 0..%d : %9d matrices with K>=2 | "
              "(I) interval violations: %d | (II) endpoint violations: %d"
              % (n, Vn, tot, bad1, bad2))
        if worst:
            a, flags = worst
            print("   first (I) counterexample matrix a_ij = c_i(A_j):")
            for r in a:
                print("      ", r)
            print("   good at levels 1..K :", flags)
            print("   realisable with bundle sizes", realise(a, n))


if __name__ == "__main__":
    main()
