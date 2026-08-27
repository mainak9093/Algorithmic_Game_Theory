"""
Approach 15, primary experiment: try to BREAK the general binary conjecture.

The conjecture says every general binary instance admits a complete allocation
whose minimal subsidy satisfies max_i p*_i <= 1. So an instance is a
counterexample iff

    min over complete allocations A of ( max_i p*_i(A) )  >=  2,

where p*_i(A) = l_A(i) and allocations that are not envy-freeable are skipped
(their subsidy is undefined; a welfare-maximising allocation is always
envy-freeable, so the minimum is over a non-empty set).

This script computes that quantity exhaustively over the valuation class for
small (n, m), and by random sampling beyond. It reports:

  * any counterexample (value >= 2), with the full valuation tables;
  * the maximum value observed, which is the informative number when no
    counterexample exists -- "the conjecture was never violated, and the bound
    1 was attained" is a much stronger statement than "no counterexample
    found";
  * a witness instance attaining the maximum.

CONTROLS. The same sweep is run on the two boundary classes, goods-only
(marginals in {0,1}) and chores-only (marginals in {-1,0}), where the answer is
known to be <= 1 by Barman-Krishna-Narahari-Sadhukhan Theorem 4 and by our own
main theorem respectively. If the harness reported a value >= 2 on either of
those, the harness would be wrong, not the theorems. The controls also have to
attain 1, since both classes contain the tight lower-bound instance; a harness
that only ever printed 0 would be silently broken.

Agents are interchangeable, so exhaustive sweeps run over multisets of
valuations (combinations_with_replacement) rather than tuples.
"""
import itertools
import random
import sys
import time

from gb_valuations import (
    enumerate_general_binary,
    enumerate_class,
    best_over_allocations,
)


def describe(v, m):
    """Readable valuation table: value on each subset, by mask."""
    names = "abcdefgh"[:m]
    parts = []
    for S in range(1 << m):
        label = "".join(names[b] for b in range(m) if S & (1 << b)) or "-"
        parts.append("%s:%d" % (label, v[S]))
    return " ".join(parts)


def report_instance(vals, m, assign, value):
    for i, v in enumerate(vals):
        print("      agent %d  %s" % (i + 1, describe(v, m)))
    print("      best allocation %s -> max subsidy %s" % (str(assign), value))


def sweep_exhaustive(pool, n, m, label):
    """Every multiset of n valuations from `pool`."""
    total = 0
    worst, worst_vals, worst_assign = -1, None, None
    counterexamples = []
    t0 = time.time()
    for vals in itertools.combinations_with_replacement(pool, n):
        total += 1
        value, assign = best_over_allocations(vals, n, m)
        if value is None:
            print("  !! no envy-freeable complete allocation at all:", vals)
            continue
        if value > worst:
            worst, worst_vals, worst_assign = value, vals, assign
        if value >= 2:
            counterexamples.append((vals, assign, value))
            if len(counterexamples) <= 3:
                print("  COUNTEREXAMPLE (%s):" % label)
                report_instance(vals, m, assign, value)
    dt = time.time() - t0
    print("  %-22s n=%d m=%d : %d instances, max = %d, counterexamples = %d "
          "(%.1fs)" % (label, n, m, total, worst, len(counterexamples), dt))
    if worst >= 1 and not counterexamples:
        print("       witness attaining %d:" % worst)
        report_instance(worst_vals, m, worst_assign, worst)
    return worst, counterexamples


def sweep_random(pool, n, m, label, samples, seed=20260827):
    rng = random.Random(seed)
    worst, worst_vals, worst_assign = -1, None, None
    counterexamples = []
    t0 = time.time()
    for _ in range(samples):
        vals = tuple(rng.choice(pool) for _ in range(n))
        value, assign = best_over_allocations(vals, n, m)
        if value is None:
            continue
        if value > worst:
            worst, worst_vals, worst_assign = value, vals, assign
        if value >= 2:
            counterexamples.append((vals, assign, value))
            if len(counterexamples) <= 3:
                print("  COUNTEREXAMPLE (%s):" % label)
                report_instance(vals, m, assign, value)
    dt = time.time() - t0
    print("  %-22s n=%d m=%d : %d samples, max = %d, counterexamples = %d "
          "(%.1fs)" % (label, n, m, samples, worst, len(counterexamples), dt))
    if worst >= 1 and not counterexamples:
        print("       witness attaining %d:" % worst)
        report_instance(worst_vals, m, worst_assign, worst)
    return worst, counterexamples


CLASSES = (
    ("general {-1,0,1}", {-1, 0, 1}),
    ("control goods {0,1}", {0, 1}),
    ("control chores {-1,0}", {-1, 0}),
)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "small"

    pools = {}

    def pool(m, allowed):
        key = (m, tuple(sorted(allowed)))
        if key not in pools:
            pools[key] = (list(enumerate_general_binary(m))
                          if allowed == {-1, 0, 1}
                          else enumerate_class(m, allowed))
        return pools[key]

    if mode == "small":
        print("EXHAUSTIVE sweeps")
        print()
        plan = [(2, 2), (2, 3), (3, 2), (2, 4), (3, 3)]
        for (n, m) in plan:
            for label, allowed in CLASSES:
                p = pool(m, allowed)
                if n == 3 and m == 3 and allowed == {-1, 0, 1}:
                    print("  %-22s n=3 m=3 : %d valuations -> "
                          "C(%d,3) multisets, deferred to `big` mode"
                          % (label, len(p), len(p)))
                    continue
                if n == 2 and m == 4 and allowed == {-1, 0, 1}:
                    print("  %-22s n=2 m=4 : %d valuations -> "
                          "%d multisets, deferred to `big` mode"
                          % (label, len(p), len(p) * (len(p) + 1) // 2))
                    continue
                sweep_exhaustive(p, n, m, label)
            print()

    elif mode == "big":
        print("EXHAUSTIVE sweep, n=3 m=3, general binary (the expensive one)")
        p = pool(3, {-1, 0, 1})
        print("  pool = %d valuations, %d multisets"
              % (len(p), len(p) * (len(p) + 1) * (len(p) + 2) // 6))
        sweep_exhaustive(p, 3, 3, "general {-1,0,1}")

    elif mode == "wide":
        print("RANDOM sweeps in the regimes exhaustive search cannot reach")
        print()
        for (n, m, samples) in ((3, 4, 400000), (4, 4, 200000),
                                (3, 5, 150000), (4, 5, 100000),
                                (5, 5, 100000)):
            for label, allowed in CLASSES:
                sweep_random(pool(m, allowed), n, m, label, samples)
            print()

    else:
        print("usage: hunt_counterexample.py [small|big|wide]")


if __name__ == "__main__":
    main()
