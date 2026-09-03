"""
The window is D in {0,1}, and it cannot be skipped.

Along the balanced path a -> (a, b(a)) blocks 2 and 3 satisfy
|v(Mid) - v(R)| <= 1, so with mu(a) = min(v(Mid), v(R)) both of them lie in
{mu, mu+1}. Writing D(a) = v(L(a)) - mu(a):

    IF D(a) is 0 or 1 THEN v(L) is mu or mu+1 as well, so ALL THREE blocks lie
    in {mu, mu+1} and the spread is at most 1.

That is an implication, not a measurement -- and it is why |D| <= 1 was the
wrong window: D = -1 puts block 1 at mu-1 against a block at mu+1, a spread of
2. The right window is D in {0,1}.

The window also cannot be jumped. v(L(a+1)) - v(L(a)) is a single marginal, so
at most 1 in absolute value; if mu is 1-Lipschitz then D moves by at most 2 per
step, and going from D <= -1 to D >= 2 in one step would need a jump of 3. So D
can only enter the window, never step over it.

Two things are therefore measured here, and they are the whole proof:

    (L)  is mu 1-Lipschitz along the path?
    (W)  does D actually reach {0,1} -- i.e. does it either start there or
         straddle it?

Part 3 climbs at both, since in this class random sampling has twice endorsed a
false statement.
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


def path_stats(v, m):
    """Returns (mu 1-Lipschitz?, D reaches {0,1}?, window implies good?)."""
    mus, Ds, sp = [], [], []
    for a in range(m + 1):
        cand = [b for b in range(a, m + 1)
                if abs(v[blocks(a, b, m)[1]] - v[blocks(a, b, m)[2]]) <= 1]
        if not cand:
            return None
        b = cand[0]
        B = blocks(a, b, m)
        mu = min(v[B[1]], v[B[2]])
        mus.append(mu)
        Ds.append(v[B[0]] - mu)
        sp.append(max(v[x] for x in B) - min(v[x] for x in B))
    lip = all(abs(mus[t + 1] - mus[t]) <= 1 for t in range(m))
    win = [t for t, d in enumerate(Ds) if d in (0, 1)]
    implies = all(sp[t] <= 1 for t in win)
    return lip, bool(win), implies, Ds


def main():
    print("PART 1 -- exhaustive over the whole class")
    for m in (3, 4):
        pool = list(enumerate_general_binary(m))
        nlip = nwin = nimp = 0
        badlip = badwin = None
        for v in pool:
            r = path_stats(v, m)
            lip, win, implies, Ds = r
            nlip += lip
            nwin += win
            nimp += implies
            if not lip and badlip is None:
                badlip = v
            if not win and badwin is None:
                badwin = (v, Ds)
        n = len(pool)
        print("   m=%d, %d valuations" % (m, n))
        print("      (L) mu is 1-Lipschitz along the path : %d / %d%s"
              % (nlip, n, "   <-- ALWAYS" if nlip == n else "   <-- FAILS"))
        print("      (W) D reaches the window {0,1}       : %d / %d%s"
              % (nwin, n, "   <-- ALWAYS" if nwin == n else "   <-- FAILS"))
        print("      window implies spread <= 1           : %d / %d%s"
              % (nimp, n, "   <-- ALWAYS" if nimp == n else "   <-- FAILS"))
        if badwin:
            print("      a valuation whose D misses the window: %s  D=%s"
                  % (badwin[0], badwin[1]))

    print()
    print("PART 2 -- sampling at larger m")
    rng = random.Random(20260925)
    for m, trials in ((5, 3000), (6, 800), (7, 250), (8, 80)):
        nlip = nwin = nimp = 0
        for _ in range(trials):
            v = random_gb(m, rng)
            lip, win, implies, Ds = path_stats(v, m)
            nlip += lip
            nwin += win
            nimp += implies
        print("   m=%d (%d): (L) %d | (W) %d | window implies good %d"
              % (m, trials, nlip, nwin, nimp))

    print()
    print("PART 3 -- climbing at (L) and (W)")
    for m, seeds, steps in ((5, 70, 300), (6, 30, 250)):
        rl = rw = 0
        for _ in range(seeds):
            cur = list(random_gb(m, rng))
            for _ in range(steps):
                S = rng.randrange(1, 1 << m)
                old = cur[S]
                cur[S] = old + rng.choice((-1, 1))
                if not legal(tuple(cur), m):
                    cur[S] = old
                    continue
                lip, win, implies, Ds = path_stats(tuple(cur), m)
                if not lip:
                    rl += 1
                    print("   (L) REFUTED m=%d: v=%s" % (m, tuple(cur)))
                    break
                if not win:
                    rw += 1
                    print("   (W) REFUTED m=%d: v=%s  D=%s" % (m, tuple(cur), Ds))
                    break
        print("   m=%d : %d climbs, (L) refutations %d, (W) refutations %d%s"
              % (m, seeds, rl, rw, "   <-- both hold" if not (rl or rw) else ""))


if __name__ == "__main__":
    main()
