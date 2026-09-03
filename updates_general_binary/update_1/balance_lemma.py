"""
(TWO-BALANCE) as a statement about two valuations, and its one-agent base.

two_balance.py splits (AVOID-1ROW) and finds that some PAIR of agents can
always be balanced to value spread <= 1, with the third then within 2. If that
pair statement holds for EVERY pair, the three-agent structure drops out
entirely and what is left is:

    (BAL-2)  any two general binary valuations on M admit a partition
             M = B_1 + B_2 + B_3 with max_j v_i(B_j) - min_j v_i(B_j) <= 1
             for both i.

    (BAL-1)  the same for a single valuation -- the base case.

These are simultaneous near-balancing statements with no fair division in them
at all: no envy, no subsidy, no prices. That is the point -- it is the form a
discrepancy or consensus-splitting argument can attack, and nothing in
approaches 15 to 18 is of that shape.

Three strengths are measured for the pair version, since they are different
theorems:

    SOME-PAIR   some pair of the three agents can be balanced   (what
                (AVOID-1ROW) actually needs)
    EVERY-PAIR  every pair can be                               (the clean
                two-valuation theorem)

and each is then climbed at, because in this class random sampling has twice
endorsed a false statement.
"""
import itertools
import random
import sys

from gb_valuations import masks_by_popcount

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


def legal(v, m):
    for S in range(1 << m):
        for b in range(m):
            if not S & (1 << b) and v[S | (1 << b)] - v[S] not in (-1, 0, 1):
                return False
    return v[0] == 0


def parts(m):
    out = []
    for o in itertools.product(range(N), repeat=m):
        b = [0] * N
        for k, i in enumerate(o):
            b[i] |= 1 << k
        out.append(tuple(b))
    return out


def spread(v, c):
    return max(v[c[j]] for j in range(N)) - min(v[c[j]] for j in range(N))


def bal1(v, P):
    return any(spread(v, c) <= 1 for c in P)


def bal2(v1, v2, P):
    return any(spread(v1, c) <= 1 and spread(v2, c) <= 1 for c in P)


def main():
    rng = random.Random(20260921)
    print("PART 1 -- sampling")
    for m, trials in ((3, 4000), (4, 1000), (5, 250), (6, 60)):
        P = parts(m)
        b1 = b2every = b2some = 0
        for _ in range(trials):
            vs = [random_gb(m, rng) for _ in range(N)]
            if all(bal1(v, P) for v in vs):
                b1 += 1
            pairs = list(itertools.combinations(range(N), 2))
            oks = [bal2(vs[a], vs[b], P) for a, b in pairs]
            if all(oks):
                b2every += 1
            if any(oks):
                b2some += 1
        print("   m=%d (%d) : (BAL-1) all agents %d | (BAL-2) EVERY pair %d | "
              "SOME pair %d" % (m, trials, b1, b2every, b2some))

    print()
    print("PART 2 -- climbing at (BAL-2), every-pair form")
    for m, seeds, steps in ((4, 60, 300), (5, 25, 200)):
        P = parts(m)
        refuted = 0
        for _ in range(seeds):
            cur = [list(random_gb(m, rng)) for _ in range(2)]
            def ok(c2):
                return bal2(tuple(c2[0]), tuple(c2[1]), P)
            for _ in range(steps):
                i = rng.randrange(2)
                S = rng.randrange(1, 1 << m)
                old = cur[i][S]
                cur[i][S] = old + rng.choice((-1, 1))
                if not legal(tuple(cur[i]), m):
                    cur[i][S] = old
                    continue
                if not ok(cur):
                    refuted += 1
                    print("   (BAL-2) REFUTED at m=%d:" % m)
                    print("      v1=%s" % (tuple(cur[0]),))
                    print("      v2=%s" % (tuple(cur[1]),))
                    break
                # random walk among legal pairs, looking for a failure
            else:
                continue
        print("   m=%d : %d climbs, refutations %d%s"
              % (m, seeds, refuted, "   <-- (BAL-2) holds" if not refuted else ""))

    print()
    print("PART 3 -- climbing at (BAL-1), the single-valuation base")
    for m, seeds, steps in ((4, 60, 300), (6, 20, 200)):
        P = parts(m)
        refuted = 0
        for _ in range(seeds):
            cur = list(random_gb(m, rng))
            for _ in range(steps):
                S = rng.randrange(1, 1 << m)
                old = cur[S]
                cur[S] = old + rng.choice((-1, 1))
                if not legal(tuple(cur), m):
                    cur[S] = old
                    continue
                if not bal1(tuple(cur), P):
                    refuted += 1
                    print("   (BAL-1) REFUTED at m=%d: v=%s" % (m, tuple(cur)))
                    break
        print("   m=%d : %d climbs, refutations %d%s"
              % (m, seeds, refuted, "   <-- (BAL-1) holds" if not refuted else ""))


if __name__ == "__main__":
    main()
