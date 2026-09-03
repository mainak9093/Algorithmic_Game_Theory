"""
Collapsing (INTERVAL) to a ONE-parameter walk.

The two-bundle lemma is proved because a one-parameter walk cannot jump. Three
blocks need the triangle 0 <= a <= b <= m, and a Sperner argument on it fails
(approach 19 section 5). So instead: pick a one-parameter PATH through the
triangle along which two of the three blocks are already balanced, and hope the
third joins them by an intermediate-value argument.

The natural path. For each first cut a, apply the PROVED two-bundle lemma to
the suffix g_{a+1}..g_m -- it is a general binary valuation on that ground set,
so the lemma applies verbatim -- and let b(a) be a cut making the middle and
right blocks balanced:

    | v(Mid(a, b(a))) - v(R(b(a))) | <= 1     for every a.

Along the path a -> (a, b(a)) blocks 2 and 3 are permanently within 1 of each
other, and only block 1 has to be brought in. Its endpoints are informative:

    a = 0   L is empty, so v(L) = 0
    a = m   L = M, Mid = R = empty, so the triple is (v(M), 0, 0)

For an intermediate-value argument two things must hold, and both are tested
here rather than assumed:

  (J)  b(a) must not JUMP -- if it moves far when a moves by one, the values
       along the path are not Lipschitz and no IVT is available;
  (H)  the path must actually CONTAIN a good cut.

(H) is the substantive question. (J) decides whether the argument can be an IVT
at all or needs something else. Both are measured against the exhaustive class
at m=3,4 and by sampling above that.
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


def spread(v, B):
    return max(v[x] for x in B) - min(v[x] for x in B)


def path_b(v, a, m, mode="small"):
    """b(a): a cut balancing Mid against R, guaranteed to exist."""
    cand = [b for b in range(a, m + 1)
            if abs(v[blocks(a, b, m)[1]] - v[blocks(a, b, m)[2]]) <= 1]
    if not cand:
        return None
    return cand[0] if mode == "small" else cand[-1]


def analyse(v, m, mode):
    bs, good, jump = [], False, 0
    for a in range(m + 1):
        b = path_b(v, a, m, mode)
        if b is None:
            return None, None, None      # would refute the two-bundle lemma
        bs.append(b)
        if spread(v, blocks(a, b, m)) <= 1:
            good = True
    for t in range(m):
        jump = max(jump, abs(bs[t + 1] - bs[t]))
    return good, jump, bs


def main():
    print("PART 1 -- exhaustive over the whole class")
    for m in (3, 4):
        pool = list(enumerate_general_binary(m))
        for mode in ("small", "large"):
            ok = tot = 0
            worst_jump = 0
            bad = None
            for v in pool:
                g, j, bs = analyse(v, m, mode)
                if g is None:
                    print("   two-bundle lemma failed -- impossible")
                    return
                tot += 1
                ok += 1 if g else 0
                worst_jump = max(worst_jump, j)
                if not g and bad is None:
                    bad = v
            print("   m=%d, b(a)=%-5s : path contains a good cut %d / %d%s"
                  "   | largest jump in b(a): %d"
                  % (m, mode, ok, tot,
                     "   <-- ALWAYS" if ok == tot else "   <-- FAILS",
                     worst_jump))
            if bad is not None:
                print("      a valuation whose path misses: %s" % (bad,))

    print()
    print("PART 2 -- sampling at larger m")
    rng = random.Random(20260923)
    for m, trials in ((5, 3000), (6, 800), (7, 200)):
        for mode in ("small", "large"):
            ok = 0
            worst_jump = 0
            for _ in range(trials):
                v = random_gb(m, rng)
                g, j, bs = analyse(v, m, mode)
                ok += 1 if g else 0
                worst_jump = max(worst_jump, j)
            print("   m=%d, b(a)=%-5s : %d / %d%s   | largest jump %d"
                  % (m, mode, ok, trials,
                     "   <-- always" if ok == trials else "   <-- FAILS",
                     worst_jump))


if __name__ == "__main__":
    main()
