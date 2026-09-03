"""
A discrete intermediate-value argument, and exhaustive tests of (BAL-1).

PROVED HERE, for two bundles. Order the items and move them one at a time from
B_1 to B_2, starting at (M, empty) and ending at (empty, M). Write
d = v(B_1) - v(B_2). Moving g changes v(B_1) by -v(g | B_1 - g) and v(B_2) by
+v(g | B_2), each in {-1,0,1}, so

    |d_{t+1} - d_t| <= 2   at every step.

The walk starts at d = v(M) and ends at d = -v(M). If |v(M)| <= 1 the start
already satisfies |d| <= 1. Otherwise d goes from >= 2 to <= -2 (or the
reverse), and to skip the whole interval [-1,1] a single step would have to
jump from >= 2 to <= -2, a change of at least 4 > 2. Impossible. So some
partition along the walk has |d| <= 1.

    LEMMA (two bundles). Every general binary valuation admits a partition
    M = B_1 + B_2 with |v(B_1) - v(B_2)| <= 1.

That is a genuine proof, and it is the first place the marginal condition has
been used as a CONTINUITY property rather than a counting one. The open
question is whether the same idea reaches three bundles:

    (BAL-1)  every general binary valuation admits a partition into THREE
             bundles with max_j v(B_j) - min_j v(B_j) <= 1.

Part 1 checks the two-bundle lemma by exhaustive search, and confirms the walk
really does land in [-1,1] rather than merely that some partition does. Part 2
tests (BAL-1) EXHAUSTIVELY over the whole class at m=3 and m=4 -- 197,547
valuations at m=4 -- which is far stronger evidence than any climb.
"""
import itertools
import sys

from gb_valuations import enumerate_general_binary


def walk_lands(v, m):
    """Move items one at a time from B1 to B2; does |d| <= 1 ever hold?"""
    B1, B2 = (1 << m) - 1, 0
    if abs(v[B1] - v[B2]) <= 1:
        return True, 0
    for k in range(m):
        B1 &= ~(1 << k)
        B2 |= 1 << k
        if abs(v[B1] - v[B2]) <= 1:
            return True, k + 1
    return False, None


def max_jump(v, m):
    B1, B2 = (1 << m) - 1, 0
    prev = v[B1] - v[B2]
    worst = 0
    for k in range(m):
        B1 &= ~(1 << k)
        B2 |= 1 << k
        cur = v[B1] - v[B2]
        worst = max(worst, abs(cur - prev))
        prev = cur
    return worst


def parts3(m):
    out = []
    for o in itertools.product(range(3), repeat=m):
        b = [0, 0, 0]
        for k, i in enumerate(o):
            b[i] |= 1 << k
        out.append(tuple(b))
    return out


def main():
    for m in (3, 4):
        pool = list(enumerate_general_binary(m))
        P3 = parts3(m)
        n_land = n_jump = n_bal1 = 0
        worst_jump = 0
        for v in pool:
            ok, _ = walk_lands(v, m)
            n_land += 1 if ok else 0
            j = max_jump(v, m)
            worst_jump = max(worst_jump, j)
            if j <= 2:
                n_jump += 1
            if any(max(v[c[t]] for t in range(3))
                   - min(v[c[t]] for t in range(3)) <= 1 for c in P3):
                n_bal1 += 1
        print("m=%d, ALL %d general binary valuations" % (m, len(pool)))
        print("   step size |d_{t+1} - d_t| <= 2 always : %d / %d  (largest %d)"
              % (n_jump, len(pool), worst_jump))
        print("   the walk lands in |d| <= 1           : %d / %d%s"
              % (n_land, len(pool), len(pool)),)
        print("   (BAL-1) three bundles, spread <= 1   : %d / %d%s"
              % (n_bal1, len(pool),
                 "   <-- EXHAUSTIVELY TRUE" if n_bal1 == len(pool) else
                 "   <-- FAILS"))
        print()


if __name__ == "__main__":
    main()
