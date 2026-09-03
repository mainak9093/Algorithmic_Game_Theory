"""
Which minimum-cost balanced allocation is the valid one?

mincost_balanced.py shows SOME minimum-cost balanced allocation is always
valid, but not every one is, so (S1) needs a tie-break. A tie-break that always
lands on a valid allocation turns (S1) into a statement about one canonical
object, which is what a proof needs.

Minimum cost alone cannot be the whole story, and the reason is structural: a
least-cost allocation is exactly one with no positive CYCLE in its envy graph,
whereas validity also forbids a PATH of weight 2, and a path is not a
permutation, so no amount of reassignment sees it. The tie-break therefore has
to be something that flattens the cost profile rather than lowering its sum.
Four candidates, all restricted to the minimum-cost balanced allocations:

    LEX     leximin -- sort each cost profile descending, take the least
    MAX     least largest individual cost
    SQ      least sum of squared costs
    SPREAD  least (max cost - min cost)

The failing allocations are printed alongside a valid one at the same cost, so
the difference between them can be read off directly.
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
    out = []
    for assign in itertools.product(range(n), repeat=m):
        b = [0] * n
        for k, owner in enumerate(assign):
            b[owner] |= 1 << k
        s = [bin(x).count("1") for x in b]
        if max(s) - min(s) <= 1:
            out.append(tuple(b))
    return out


def run(n, m, k, allowed, label, show=0):
    pool = enumerate_class(m, allowed)
    rng = random.Random(20260903)
    allocs = balanced_allocations(n, m)
    st = {"inst": 0, "lex": 0, "mx": 0, "sq": 0, "spread": 0}
    shown = 0
    for _ in range(k):
        vals = [rng.choice(pool) for _ in range(n)]
        st["inst"] += 1
        best, bucket = None, []
        for b in allocs:
            costs = tuple(-vals[i][b[i]] for i in range(n))
            tot = sum(costs)
            if best is None or tot < best:
                best, bucket = tot, [(b, costs)]
            elif tot == best:
                bucket.append((b, costs))

        def pick(key):
            return min(bucket, key=lambda t: key(t[1]))[0]

        cand = {
            "lex": pick(lambda c: sorted(c, reverse=True)),
            "mx": pick(lambda c: (max(c), sorted(c, reverse=True))),
            "sq": pick(lambda c: sum(t * t for t in c)),
            "spread": pick(lambda c: (max(c) - min(c), max(c))),
        }
        for key, b in cand.items():
            if valid(vals, b):
                st[key] += 1
            elif shown < show and key == "lex":
                shown += 1
                ok = [t for t in bucket if valid(vals, t[0])]
                print("      LEX FAILS: bundles=%s costs=%s  |  a valid one at "
                      "the same total: bundles=%s costs=%s"
                      % (b, tuple(-vals[i][b[i]] for i in range(n)),
                         ok[0][0] if ok else None, ok[0][1] if ok else None))
    print("   %-24s inst %-6d | LEX %-6d MAX %-6d SQ %-6d SPREAD %-6d"
          % (label, st["inst"], st["lex"], st["mx"], st["sq"], st["spread"]))


def main():
    print("tie-breaks among the minimum-cost balanced allocations")
    print("(a number equal to `inst` means that tie-break never failed)")
    print()
    jobs = [(3, 3, 2000), (3, 4, 800), (4, 4, 400)]
    if len(sys.argv) > 3:
        jobs = [(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))]
    for (n, m, k) in jobs:
        for allowed, name in (({-1, 0}, "chores"), ({0, 1}, "goods")):
            run(n, m, k, allowed, "n=%d m=%d %s" % (n, m, name), show=2)


if __name__ == "__main__":
    main()
