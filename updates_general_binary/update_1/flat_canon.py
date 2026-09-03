"""
Efficiency is the wrong objective. Try flatness.

diagnose_canon.py kills (CANON) and more: in 5 of 10 witnesses NO welfare
maximiser of the spread-<=2 family is valid, so the problem is not the
tie-break but the primary criterion. Meanwhile 14 to 23 of the 54 allocations
in each witness ARE valid, so the targets are abundant and welfare
maximisation is steering away from them.

The witnesses say where to steer instead. In witness 7 the welfare maximiser
has cost profile (-2,-1,0) at total -3, while a valid allocation has (0,0,0) at
total 0: three units WORSE in welfare and perfectly FLAT. That is the same
phenomenon as the Pareto-optimality note -- a subsidy capped at one unit per
agent forbids exactly the concentration that efficiency rewards -- so the
criterion should minimise spread in the COST PROFILE rather than its sum.

Envy-freeability has to be imposed separately here. An allocation is
envy-freeable exactly when no reassignment of its own bundles beats it, and a
flatness criterion has no reason to respect that, so the candidates are drawn
from the envy-freeable allocations of the family only.

    FLAT   least (max cost - min cost), then least total
    LEX    least cost profile sorted descending, lexicographically
    MAXC   least largest individual cost
    SQ     least sum of squared costs
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
    v = [0] * (1 << m)
    for S in masks_by_popcount(m):
        if S == 0:
            continue
        bits = [1 << b for b in range(m) if S & (1 << b)]
        lo = max(v[S ^ b] for b in bits) - 1
        hi = min(v[S ^ b] for b in bits) + 1
        v[S] = rng.randint(lo, hi)
    return tuple(v)


def family(m, K):
    out = []
    for assign in itertools.product(range(N), repeat=m):
        b = [0] * N
        for k, o in enumerate(assign):
            b[o] |= 1 << k
        s = [bin(x).count("1") for x in b]
        if max(s) - min(s) <= K:
            out.append(tuple(b))
    return out


def worst(vals, b):
    if not is_envy_freeable(vals, b):
        return None
    return max(longest_paths(arc_weights(vals, b)))


def main():
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
    rng = random.Random(20260903)
    fam = family(m, 2)
    print("n=3, m=%d, spread<=2 family: %d allocations; %d instances"
          % (m, len(fam), trials))

    keys = {
        "FLAT": lambda c: (max(c) - min(c), sum(c), sorted(c, reverse=True)),
        "LEX": lambda c: sorted(c, reverse=True),
        "MAXC": lambda c: (max(c), sorted(c, reverse=True)),
        "SQ": lambda c: (sum(t * t for t in c), sum(c)),
    }
    st = {k: 0 for k in keys}
    st["inst"] = 0
    st["any"] = 0
    fails = {k: [] for k in keys}

    for _ in range(trials):
        vals = [random_gb(m, rng) for _ in range(N)]
        st["inst"] += 1
        ef = []
        anyvalid = False
        for b in fam:
            w = worst(vals, b)
            if w is None:
                continue
            costs = tuple(-vals[i][b[i]] for i in range(N))
            ef.append((b, costs, w))
            if w <= 1:
                anyvalid = True
        if anyvalid:
            st["any"] += 1
        if not ef:
            continue
        for name, key in keys.items():
            best = min(ef, key=lambda t: key(t[1]))
            if best[2] <= 1:
                st[name] += 1
            elif len(fails[name]) < 2:
                fails[name].append((vals, best))

    print()
    print("   instances                        : %d" % st["inst"])
    print("   (S2): some spread<=2 alloc valid : %d" % st["any"])
    for name in ("FLAT", "LEX", "MAXC", "SQ"):
        print("   %-5s optimal is valid           : %-6d%s"
              % (name, st[name],
                 "   <-- NEVER FAILED" if st[name] == st["inst"] else ""))
    for name in ("FLAT", "LEX", "MAXC", "SQ"):
        for vals, best in fails[name][:1]:
            print()
            print("   %s fails: bundles=%s costs=%s worstpath=%d"
                  % (name, best[0], best[1], best[2]))


if __name__ == "__main__":
    main()
