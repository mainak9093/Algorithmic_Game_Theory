"""
Which potential makes the descent easiest to PROVE?

(DESCENT-1) uses PSI = the longest-path vector sorted downwards, compared
lexicographically. That is awkward to argue with. A potential that is a single
integer would be far easier, so this checks whether the descent survives with
weaker ones:

    SUM     sum_i l(i)
    MAXSUM  (max_i l(i), sum_i l(i))
    SORTED  the sorted vector, lexicographically      (known to work)

all minimised over the assignments of the partition's bundles, as in
approach 17 section 4. A potential with plateaus will show up as stuck states.

Also checks n=2, where the base case may be clean: is every welfare-maximal
allocation of a two-agent instance already valid? If so the induction has
somewhere to start.
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


def random_gb(m, rng):
    v = [0] * (1 << m)
    for S in masks_by_popcount(m):
        if S == 0:
            continue
        bits = [1 << b for b in range(m) if S & (1 << b)]
        lo = max(v[S ^ b] for b in bits) - 1
        hi = min(v[S ^ b] for b in bits) + 1
        v[S] = rng.randint(lo, hi)
    return tuple(v)


def lvec(vals, b, N):
    if not is_envy_freeable(vals, b):
        return None
    return longest_paths(arc_weights(vals, b))


def pots(vals, b, N):
    """(SUM, MAXSUM, SORTED) minimised over assignments; None if impossible."""
    best = {}
    for p in itertools.permutations(range(N)):
        c = tuple(b[p[i]] for i in range(N))
        l = lvec(vals, c, N)
        if l is None:
            continue
        s, mx = sum(l), max(l)
        srt = tuple(sorted(l, reverse=True))
        for k, val in (("SUM", s), ("MAXSUM", (mx, s)), ("SORTED", srt)):
            if k not in best or val < best[k]:
                best[k] = val
        if "MX" not in best or mx < best["MX"]:
            best["MX"] = mx
    return best


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    m = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    trials = int(sys.argv[3]) if len(sys.argv) > 3 else 400
    rng = random.Random(20260906)

    owners = list(itertools.product(range(N), repeat=m))
    allocs = []
    for o in owners:
        b = [0] * N
        for k, i in enumerate(o):
            b[i] |= 1 << k
        allocs.append(tuple(b))
    nbr = [[c for c in range(len(owners))
            if sum(1 for k in range(m) if owners[c][k] != owners[a][k]) == 1]
           for a in range(len(owners))]

    st = {k: 0 for k in ("SUM", "MAXSUM", "SORTED")}
    bad = 0
    wmax_bad = 0
    for _ in range(trials):
        vals = [random_gb(m, rng) for _ in range(N)]
        P = [pots(vals, b, N) for b in allocs]

        # n=2 base case: is a welfare-maximal allocation always valid?
        bw = max(sum(vals[i][b[i]] for i in range(N)) for b in allocs)
        for a, b in enumerate(allocs):
            if sum(vals[i][b[i]] for i in range(N)) == bw and P[a]["MX"] > 1:
                wmax_bad += 1
                break

        for a in range(len(allocs)):
            if P[a]["MX"] <= 1:
                continue
            bad += 1
            for k in st:
                if not any(P[c][k] < P[a][k] for c in nbr[a]):
                    st[k] += 1

    print("n=%d, m=%d, %d instances" % (N, m, trials))
    print("   states needing descent            : %d" % bad)
    for k in ("SUM", "MAXSUM", "SORTED"):
        print("   stuck under %-7s              : %-6d%s"
              % (k, st[k], "   <-- descent holds" if not st[k] else ""))
    print("   instances where SOME welfare-maximal allocation is invalid : %d / %d"
          % (wmax_bad, trials))


if __name__ == "__main__":
    main()
