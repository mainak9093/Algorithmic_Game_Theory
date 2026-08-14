"""The counterexample to uniform balance, isolated, plus an analysis of what the
surviving good allocations look like.

Instance (n=3, m=4, BINARY ADDITIVE):
    D_1 = {g1,g2},  D_2 = {g1,g3,g4},  D_3 = {g2,g3,g4},   c_i(S) = |S n D_i|.

Why no uniformly balanced partition exists, by hand:
  |D_2| = 3 and any 3 items split over 3 parts must go (1,1,1) to have range <=1,
  so g1,g3,g4 occupy three DIFFERENT parts -- one each.
  Likewise |D_3| = 3 forces g2,g3,g4 into three different parts, so g2 must sit
  in the one part free of g3,g4, which is g1's part.
  But |D_1| = 2 forces g1,g2 into DIFFERENT parts.  Contradiction.

The instance is binary additive, hence already settled by [LMS26]; it is a
counterexample to the METHOD, not to the conjecture.

Run:  python routeA_cex.py
"""
from itertools import product, permutations

M = 4
N = 3
D = [frozenset({0, 1}), frozenset({0, 2, 3}), frozenset({1, 2, 3})]
C = [lambda S, Ds=Ds: len(S & Ds) for Ds in D]


def arcs(bd):
    return [[C[i](bd[i]) - C[i](bd[j]) for j in range(N)] for i in range(N)]


def ellvec(bd):
    W = arcs(bd)
    e = [0] * N
    for _ in range(N + 1):
        ch = False
        new = list(e)
        for i in range(N):
            for j in range(N):
                if i != j and W[i][j] + e[j] > new[i]:
                    new[i] = W[i][j] + e[j]
                    ch = True
        e = new
        if not ch:
            return e
    return None


def show(bd):
    return [sorted(g + 1 for g in b) for b in bd]


def main():
    print("instance: D1=%s D2=%s D3=%s  (1-indexed)"
          % tuple([sorted(g + 1 for g in d) for d in D]))

    # 1. confirm no uniformly balanced partition
    bal = []
    for assign in product(range(N), repeat=M):
        bd = [frozenset(g for g in range(M) if assign[g] == i) for i in range(N)]
        if all(max(c(b) for b in bd) - min(c(b) for b in bd) <= 1 for c in C):
            bal.append(bd)
    print("\nuniformly balanced partitions: %d   <-- the Route A target is unreachable"
          % len(bal))

    # 2. the good allocations that do exist
    good = []
    for assign in product(range(N), repeat=M):
        bd = [frozenset(g for g in range(M) if assign[g] == i) for i in range(N)]
        e = ellvec(bd)
        if e is not None and max(e) <= 1:
            good.append((bd, e))
    print("good allocations (ell <= 1, no positive cycle): %d of %d"
          % (len(good), N ** M))

    minarc_overall = 99
    print("\n  bundles                        ell        arc range   min arc")
    seen = set()
    for bd, e in good:
        key = tuple(sorted(tuple(sorted(b)) for b in bd))
        if key in seen:
            continue
        seen.add(key)
        W = arcs(bd)
        off = [W[i][j] for i in range(N) for j in range(N) if i != j]
        minarc_overall = min(minarc_overall, min(off))
        print("  %-30s %-10s [%d, %d]      %d"
              % (show(bd), e, min(off), max(off), min(off)))

    print("\nminimum arc weight over all good allocations: %d" % minarc_overall)
    if minarc_overall < -1:
        print("=> every good allocation here has an arc BELOW -1, so the")
        print("   cycle-closing sufficient condition cannot certify any of them.")
        print("   A correct invariant must use the PATH bound, not the arc bound.")
    else:
        print("=> some good allocation has all arcs >= -1 after all.")


if __name__ == "__main__":
    main()
