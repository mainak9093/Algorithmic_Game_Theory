"""
A global route to (S1): is a MINIMUM-COST balanced allocation always valid?

The incremental route proves (S1) by inserting chores one at a time. A global
route would skip all of that: pick the balanced complete allocation of least
total cost and show it is already valid. Such an allocation is automatically
envy-freeable -- no reassignment of its own bundles can beat it, or it would
not be of least cost -- so the whole question is whether its longest envy path
can reach 2.

Two strengths, because they give different theorems:

    ALL   every minimum-cost balanced allocation is valid
    SOME  at least one is

SOME is all (S1) needs. ALL would be stronger and would remove tie-breaking
from any proof. Section 24 records that the analogous claim for spread-2
welfare maximisers in the GENERAL binary class is false, so the question is
whether the pure classes behave better -- which is exactly where (S1) lives.
"""
import itertools
import random
import sys

from gb_valuations import (
    enumerate_class,
    arc_weights,
    is_envy_freeable,
    longest_paths,
)


def valid(vals, b):
    if not is_envy_freeable(vals, b):
        return False
    return all(t <= 1 for t in longest_paths(arc_weights(vals, b)))


def balanced_allocations(n, m):
    """Every complete allocation whose bundle sizes have spread at most 1."""
    for assign in itertools.product(range(n), repeat=m):
        b = [0] * n
        for k, owner in enumerate(assign):
            b[owner] |= 1 << k
        s = [bin(x).count("1") for x in b]
        if max(s) - min(s) <= 1:
            yield tuple(b)


def run(n, m, k, allowed, label):
    pool = enumerate_class(m, allowed)
    rng = random.Random(20260903)
    allocs = list(balanced_allocations(n, m))
    st = {"inst": 0, "all_ok": 0, "some_ok": 0, "none_ok": 0, "exists_bal": 0}
    for _ in range(k):
        vals = [rng.choice(pool) for _ in range(n)]
        st["inst"] += 1
        best = None
        bucket = []
        for b in allocs:
            tot = sum(-vals[i][b[i]] for i in range(n))     # cost = -value
            if best is None or tot < best:
                best, bucket = tot, [b]
            elif tot == best:
                bucket.append(b)
        oks = [valid(vals, b) for b in bucket]
        if all(oks):
            st["all_ok"] += 1
        if any(oks):
            st["some_ok"] += 1
        else:
            st["none_ok"] += 1
        if any(valid(vals, b) for b in allocs):
            st["exists_bal"] += 1
    print("   %-24s instances %-6d | min-cost balanced: ALL valid %-6d "
          "SOME valid %-6d NONE %-5d | (S1) holds %d"
          % (label, st["inst"], st["all_ok"], st["some_ok"],
             st["none_ok"], st["exists_bal"]))


def main():
    print("min-cost balanced allocation: is it valid?")
    print()
    jobs = [(3, 3, 3000), (3, 4, 1500), (3, 5, 400), (4, 4, 800),
            (4, 5, 250), (5, 5, 120), (3, 6, 150)]
    if len(sys.argv) > 3:
        jobs = [(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))]
    for (n, m, k) in jobs:
        for allowed, name in (({-1, 0}, "chores"), ({0, 1}, "goods")):
            run(n, m, k, allowed, "n=%d m=%d %s" % (n, m, name))


if __name__ == "__main__":
    main()
