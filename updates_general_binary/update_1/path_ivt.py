"""
Is the balanced path Lipschitz in the VALUES, even though b(a) jumps?

path.py shows the one-parameter path a -> (a, b(a)), with b(a) chosen so that
blocks 2 and 3 are balanced, always contains a good cut -- exhaustively at
m=3,4. But b(a) jumps by up to 5, so the path is not Lipschitz in b, and a
naive intermediate-value argument is unavailable.

The values may still be well behaved, and that is what matters. Along the path
blocks 2 and 3 are permanently within 1 of each other, so write

    mu(a) = min( v(Mid), v(R) )        the common level of blocks 2 and 3
    D(a)  = v(L(a)) - mu(a)            how far block 1 sits from that level

Block 1 grows one item at a time, so v(L(a)) moves by at most 1. If mu is also
Lipschitz with some constant c, then D moves by at most 1 + c per step. Its
endpoints are computable:

    D(0) = -mu(0)      (block 1 empty)
    D(m) = v(M)        (blocks 2 and 3 empty, so mu(m) = 0)

so when those have opposite signs D must cross, and a small enough step bound
puts it inside the good window. This measures c, whether D changes sign, and --
the real question -- whether a crossing of D actually coincides with a cut of
spread <= 1.

Two selection rules for b(a) are compared, since the choice is ours to make:
SMALL takes the least valid b, NEAR takes the valid b closest to the previous
one, which is the natural attempt at a continuous selection.
"""
import itertools
import random
import sys

from gb_valuations import masks_by_popcount, enumerate_general_binary


def random_gb(m, rng):
    v = [0] * (1 << m)
    for S in masks_by_popcount(m):
        if S == 0:
            continue
        bits = [1 << b for b in range(m) if S & (1 << b)]
        v[S] = rng.randint(max(v[S ^ b] for b in bits) - 1,
                           min(v[S ^ b] for b in bits) + 1)
    return tuple(v)


def blocks(a, b, m):
    B1 = (1 << a) - 1
    B2 = ((1 << b) - 1) & ~B1
    B3 = ((1 << m) - 1) & ~((1 << b) - 1)
    return B1, B2, B3


def valid_bs(v, a, m):
    return [b for b in range(a, m + 1)
            if abs(v[blocks(a, b, m)[1]] - v[blocks(a, b, m)[2]]) <= 1]


def build(v, m, rule):
    path, prev = [], 0
    for a in range(m + 1):
        cand = valid_bs(v, a, m)
        if not cand:
            return None
        b = cand[0] if rule == "SMALL" else min(cand, key=lambda t: abs(t - prev))
        prev = b
        path.append((a, b))
    return path


def stats(v, m, path):
    mus, Ds, spreads = [], [], []
    for (a, b) in path:
        B = blocks(a, b, m)
        mu = min(v[B[1]], v[B[2]])
        mus.append(mu)
        Ds.append(v[B[0]] - mu)
        spreads.append(max(v[x] for x in B) - min(v[x] for x in B))
    jmu = max(abs(mus[t + 1] - mus[t]) for t in range(len(mus) - 1))
    jD = max(abs(Ds[t + 1] - Ds[t]) for t in range(len(Ds) - 1))
    good = [t for t, s in enumerate(spreads) if s <= 1]
    # does D cross the window [-1, 1]?
    crossed = any(-1 <= d <= 1 for d in Ds)
    signflip = any(Ds[t] * Ds[t + 1] <= 0 for t in range(len(Ds) - 1))
    # is every point where |D| <= 1 actually a good cut?
    dwin = [t for t, d in enumerate(Ds) if -1 <= d <= 1]
    implies = all(spreads[t] <= 1 for t in dwin)
    return jmu, jD, bool(good), crossed, signflip, implies, bool(dwin)


def main():
    print("PART 1 -- exhaustive over the whole class")
    for m in (3, 4):
        pool = list(enumerate_general_binary(m))
        for rule in ("SMALL", "NEAR"):
            JM = JD = 0
            tot = ngood = ncross = nflip = nimp = nwin = 0
            for v in pool:
                p = build(v, m, rule)
                jmu, jD, good, crossed, flip, implies, haswin = stats(v, m, p)
                tot += 1
                JM = max(JM, jmu)
                JD = max(JD, jD)
                ngood += good
                ncross += crossed
                nflip += flip
                nimp += implies
                nwin += haswin
            print("   m=%d %-5s : max step of mu %d, of D %d | good cut on path "
                  "%d/%d | |D|<=1 occurs %d/%d | that implies a good cut %d/%d%s"
                  % (m, rule, JM, JD, ngood, tot, nwin, tot, nimp, tot,
                     "   <-- D-window IS the criterion" if nimp == tot else ""))

    print()
    print("PART 2 -- sampling")
    rng = random.Random(20260924)
    for m, trials in ((5, 2000), (6, 600)):
        for rule in ("SMALL", "NEAR"):
            JM = JD = 0
            ngood = nimp = nwin = 0
            for _ in range(trials):
                v = random_gb(m, rng)
                p = build(v, m, rule)
                jmu, jD, good, crossed, flip, implies, haswin = stats(v, m, p)
                JM = max(JM, jmu)
                JD = max(JD, jD)
                ngood += good
                nimp += implies
                nwin += haswin
            print("   m=%d %-5s : max step of mu %d, of D %d | good cut %d/%d | "
                  "|D|<=1 occurs %d/%d | implies good %d/%d"
                  % (m, rule, JM, JD, ngood, trials, nwin, trials, nimp, trials))


if __name__ == "__main__":
    main()
