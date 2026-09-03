"""
Attacking (L): is the balanced LEVEL of a suffix 1-Lipschitz?

(L) is the main open step of approach 20. For an ordered set S with a general
binary valuation, let t*(S) be the LEAST cut with |v(prefix) - v(suffix)| <= 1
-- it exists by the proved two-bundle lemma -- and let

    beta(S) = min( v(prefix), v(suffix) )   at that cut.

(L) says |beta(S) - beta(S minus its first element)| <= 1.

There is a structural relation to work from. Removing the first element s_1
shifts the cuts by one, and for every j the S'-cut at j and the S-cut at j+1
have the SAME suffix, while their prefixes differ by exactly s_1:

    Q_{j+1}(S) = Q'_j(S'),        P_{j+1}(S) = P'_j(S') + s_1,

so the two prefix values differ by a single marginal, at most 1. What that does
NOT give is a relation between the two BALANCED cuts, because a cut can be
balanced for one and not the other -- the imbalance transfers only up to 2.

So the level might be better defined some other way, and four candidates are
compared here. Each is tested for the Lipschitz property AND for whether the
rest of approach 20's argument still goes through with it -- a level that is
Lipschitz but breaks the window or the endpoints is no use.

    LEAST   the level at the least balanced cut          (approach 20's choice)
    GREAT   the level at the greatest balanced cut
    MAXLVL  the largest level over all balanced cuts
    MINLVL  the smallest level over all balanced cuts
"""
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


def legal(v, m):
    for S in range(1 << m):
        for b in range(m):
            if not S & (1 << b) and v[S | (1 << b)] - v[S] not in (-1, 0, 1):
                return False
    return v[0] == 0


def blocks(a, b, m):
    B1 = (1 << a) - 1
    B2 = ((1 << b) - 1) & ~B1
    B3 = ((1 << m) - 1) & ~((1 << b) - 1)
    return B1, B2, B3


def path(v, m, rule):
    """Returns (list of mu, list of D, list of spreads) along the path."""
    mus, Ds, sp = [], [], []
    for a in range(m + 1):
        cand = [b for b in range(a, m + 1)
                if abs(v[blocks(a, b, m)[1]] - v[blocks(a, b, m)[2]]) <= 1]
        if not cand:
            return None
        lv = [(b, min(v[blocks(a, b, m)[1]], v[blocks(a, b, m)[2]]))
              for b in cand]
        if rule == "LEAST":
            b, mu = lv[0]
        elif rule == "GREAT":
            b, mu = lv[-1]
        elif rule == "MAXLVL":
            b, mu = max(lv, key=lambda t: t[1])
        else:
            b, mu = min(lv, key=lambda t: t[1])
        B = blocks(a, b, m)
        mus.append(mu)
        Ds.append(v[B[0]] - mu)
        sp.append(max(v[x] for x in B) - min(v[x] for x in B))
    return mus, Ds, sp


def check(v, m, rule):
    r = path(v, m, rule)
    if r is None:
        return None
    mus, Ds, sp = r
    lip = all(abs(mus[t + 1] - mus[t]) <= 1 for t in range(m))
    win = [t for t, d in enumerate(Ds) if d in (0, 1)]
    implies = all(sp[t] <= 1 for t in win)
    d0, dm = Ds[0], Ds[-1]
    straddle = (d0 in (0, 1) or dm in (0, 1)
                or (d0 <= -1 and dm >= 2) or (d0 >= 2 and dm <= -1))
    return lip, bool(win), implies, straddle


RULES = ("LEAST", "GREAT", "MAXLVL", "MINLVL")


def main():
    print("PART 1 -- exhaustive, all valuations")
    for m in (3, 4):
        pool = list(enumerate_general_binary(m))
        n = len(pool)
        res = {r: [0, 0, 0, 0] for r in RULES}
        for v in pool:
            for r in RULES:
                lip, win, imp, st = check(v, m, r)
                res[r][0] += lip
                res[r][1] += win
                res[r][2] += imp
                res[r][3] += st
        print("   m=%d, %d valuations" % (m, n))
        for r in RULES:
            a, b, c, d = res[r]
            print("      %-7s : (L) %-7d (W) %-7d window=>good %-7d straddle %-7d%s"
                  % (r, a, b, c, d,
                     "   <-- all four hold" if a == b == c == d == n else ""))

    print()
    print("PART 2 -- climbing at (L), larger m, the LEAST rule")
    rng = random.Random(20260927)
    for m, seeds, steps in ((6, 50, 300), (7, 25, 250), (8, 12, 200)):
        bad = 0
        worst = 0
        for _ in range(seeds):
            cur = list(random_gb(m, rng))
            for _ in range(steps):
                S = rng.randrange(1, 1 << m)
                old = cur[S]
                cur[S] = old + rng.choice((-1, 1))
                if not legal(tuple(cur), m):
                    cur[S] = old
                    continue
                mus, Ds, sp = path(tuple(cur), m, "LEAST")
                j = max(abs(mus[t + 1] - mus[t]) for t in range(m))
                worst = max(worst, j)
                if j > 1:
                    bad += 1
                    print("   (L) REFUTED m=%d: v=%s  mu=%s" % (m, tuple(cur), mus))
                    break
        print("   m=%d : %d climbs, refutations %d, largest step of mu seen %d"
              % (m, seeds, bad, worst))


if __name__ == "__main__":
    main()
