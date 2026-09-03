"""
A serious attempt to refute (CANON) at n = 3, before any proof is attempted.

(CANON) says: inside the spread-<=2 family, among the welfare maximisers, the
leximin-optimal allocation is valid. Approach 16 tested it on 2,000 instances
at m=3 and 250 at m=4. That is not enough to build a proof on, and there are
two separate things to check.

FIRST, whether the object is even well defined. Leximin can itself tie -- two
maximisers with the same sorted cost profile -- so the honest statement is
about EVERY leximin-optimal allocation, not a representative picked by
whichever one the code happened to see first. Both strengths are reported:

    ALL    every leximin-optimal maximiser is valid   (the robust statement)
    SOME   at least one is                            (what a proof could use)

SECOND, random sampling is weak evidence at these sizes. So the script also
hill-climbs: it starts from an instance whose leximin maximiser is TIGHT (some
agent's longest path already equals 1, so it is one step from failing) and
mutates single valuation entries, keeping any mutation that does not decrease
the worst longest path. That drives the search towards the boundary instead of
sampling the middle of the class.

Valuations at m >= 5 are generated directly rather than enumerated, since the
class is far too large to list.
"""
import itertools
import random
import sys

from gb_valuations import (
    masks_by_popcount,
    arc_weights,
    is_envy_freeable,
    longest_paths,
)

N = 3


def random_gb(m, rng):
    """A uniformly random general binary valuation on m items."""
    v = [0] * (1 << m)
    for S in masks_by_popcount(m):
        if S == 0:
            continue
        bits = [1 << b for b in range(m) if S & (1 << b)]
        lo = max(v[S ^ b] for b in bits) - 1
        hi = min(v[S ^ b] for b in bits) + 1
        v[S] = rng.randint(lo, hi)
    return tuple(v)


def legal(v, m):
    for S in range(1 << m):
        for b in range(m):
            if not S & (1 << b) and v[S | (1 << b)] - v[S] not in (-1, 0, 1):
                return False
    return v[0] == 0


def family(m, K):
    out = []
    for assign in itertools.product(range(N), repeat=m):
        b = [0] * N
        for k, owner in enumerate(assign):
            b[owner] |= 1 << k
        s = [bin(x).count("1") for x in b]
        if max(s) - min(s) <= K:
            out.append(tuple(b))
    return out


def worst_path(vals, b):
    """max_i l(i), or None if not envy-freeable."""
    if not is_envy_freeable(vals, b):
        return None
    return max(longest_paths(arc_weights(vals, b)))


def leximin_set(vals, fam):
    """Every leximin-optimal welfare maximiser of the family."""
    best, bucket = None, []
    for b in fam:
        costs = tuple(-vals[i][b[i]] for i in range(N))
        tot = sum(costs)
        if best is None or tot < best:
            best, bucket = tot, [(b, costs)]
        elif tot == best:
            bucket.append((b, costs))
    key = min(sorted(c, reverse=True) for _, c in bucket)
    return [b for b, c in bucket if sorted(c, reverse=True) == key]


def score(vals, fam):
    """(worst longest path over the leximin set, is any of them valid)."""
    lex = leximin_set(vals, fam)
    ws = []
    for b in lex:
        w = worst_path(vals, b)
        ws.append(99 if w is None else w)
    return max(ws), min(ws)


def main():
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
    climbs = int(sys.argv[3]) if len(sys.argv) > 3 else 300
    steps = int(sys.argv[4]) if len(sys.argv) > 4 else 400
    rng = random.Random(20260903)
    fam = family(m, 2)
    print("n=3, m=%d, spread<=2 family: %d allocations" % (m, len(fam)))
    print("random trials %d, hill climbs %d x %d steps" % (trials, climbs, steps))

    st = {"inst": 0, "all_bad": 0, "some_bad": 0, "tie": 0, "tight": 0}
    seeds = []
    for _ in range(trials):
        vals = [random_gb(m, rng) for _ in range(N)]
        st["inst"] += 1
        lex = leximin_set(vals, fam)
        if len(lex) > 1:
            st["tie"] += 1
        hi, lo = score(vals, fam)
        if lo > 1:
            st["some_bad"] += 1
            print("   REFUTED (random): vals=%s" % (vals,))
        elif hi > 1:
            st["all_bad"] += 1
        if hi == 1:
            st["tight"] += 1
            if len(seeds) < climbs:
                seeds.append(vals)

    print()
    print("   instances                                   : %d" % st["inst"])
    print("   leximin itself ties (>1 optimal allocation) : %d" % st["tie"])
    print("   leximin maximiser TIGHT (worst path = 1)    : %d" % st["tight"])
    print("   some leximin-optimal one INVALID (ALL fails): %d" % st["all_bad"])
    print("   every leximin-optimal one INVALID (REFUTES) : %d" % st["some_bad"])

    print()
    print("hill climbing from %d tight seeds..." % len(seeds))
    refuted = 0
    allbad = 0
    for vals in seeds:
        cur = [list(v) for v in vals]
        curhi, curlo = score([tuple(v) for v in cur], fam)
        for _ in range(steps):
            i = rng.randrange(N)
            S = rng.randrange(1, 1 << m)
            old = cur[i][S]
            cur[i][S] = old + rng.choice((-1, 1))
            if not legal(tuple(cur[i]), m):
                cur[i][S] = old
                continue
            hi, lo = score([tuple(v) for v in cur], fam)
            if lo > 1:
                refuted += 1
                print("   REFUTED (climb): vals=%s"
                      % ([tuple(v) for v in cur],))
                break
            if hi >= curhi:
                curhi, curlo = hi, lo
                if hi > 1:
                    allbad += 1
            else:
                cur[i][S] = old
    print("   climbs that refuted (CANON)                 : %d" % refuted)
    print("   climbs that broke the ALL form only         : %d" % allbad)


if __name__ == "__main__":
    main()
