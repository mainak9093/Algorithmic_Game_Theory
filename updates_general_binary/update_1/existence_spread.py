"""
Approach 15: the target as a pure EXISTENCE statement.

Everything measured so far points at one clean strengthening of the conjecture,
with no algorithm and no reachability in it:

  (S2)  every GENERAL BINARY instance admits an envy-freeable allocation with
        minimal subsidy in {0,1}^n whose bundle-size spread is at most 2;

  (S1)  every DICHOTOMOUS GOODS instance, and every NEGATIVE DICHOTOMOUS
        instance, admits such an allocation that is BALANCED (spread <= 1).

(S2) implies the main conjecture, and is strictly more structured, which is
what makes it a better induction target. (S1) is the pure-class analogue and is
interesting on its own: BKNS's Theorem 4 says nothing about balance -- their
concluding section notes their allocation need not even be EF1 -- so (S1)
restricted to goods would strengthen a published theorem. Brustle et al. proved
balanced-and-EF1 for ADDITIVE valuations; the dichotomous non-additive case is
a different class.

The n=3, m=3 sweep is EXHAUSTIVE over the whole valuation class, reusing the
specialised inner loop that hunt_n3m3.py cross-validated against the readable
implementation. At n=3, m=3 the 27 allocations have size multisets (3,0,0),
(2,1,0) and (1,1,1), so spread <= 2 drops exactly the three allocations that
pile everything on one agent, and spread <= 1 keeps only the six perfectly
balanced ones.
"""
import itertools
import random
import sys
import time

from gb_valuations import (
    enumerate_general_binary,
    enumerate_class,
    arc_weights,
    is_envy_freeable,
    longest_paths,
    bundles_from_assignment,
)
from hunt_n3m3 import worst_subsidy_fast, ALLOCS, N, M


def spread_of(bundles):
    z = [bin(b).count("1") for b in bundles]
    return max(z) - min(z)


SPREADS = [spread_of(b) for b in ALLOCS]


def sweep_n3m3(pool, label, K):
    """Exhaustive n=3, m=3: does a valid allocation of spread <= K exist?"""
    idx = [k for k in range(len(ALLOCS)) if SPREADS[k] <= K]
    table = [[(v[b[0]], v[b[1]], v[b[2]]) for b in ALLOCS] for v in pool]
    npool = len(pool)
    total = fails = 0
    witness = None
    t0 = time.time()

    for a in range(npool):
        ta = table[a]
        for b in range(a, npool):
            tb = table[b]
            for c in range(b, npool):
                tc = table[c]
                total += 1
                ok = False
                for k in idx:
                    val = worst_subsidy_fast(ta[k], tb[k], tc[k])
                    if val is not None and val <= 1:
                        ok = True
                        break
                if not ok:
                    fails += 1
                    if witness is None:
                        witness = (pool[a], pool[b], pool[c])

    print("     %-22s K=%d : %d instances, %d without one  (%.0fs)"
          % (label, K, total, fails, time.time() - t0))
    if witness:
        for i, v in enumerate(witness):
            print("        agent %d %s" % (i + 1, str(v)))
    return fails


def min_subsidy(vals, bundles):
    if not is_envy_freeable(vals, bundles):
        return None
    return longest_paths(arc_weights(vals, bundles))


def sweep_general(pool, n, m, label, K, sample, seed=20260827):
    """`pool` is either a list of valuations or a callable drawing one."""
    rng = random.Random(seed)
    draw = pool if callable(pool) else (lambda r: r.choice(pool))
    allocs = []
    for assign in itertools.product(range(n), repeat=m):
        b = bundles_from_assignment(assign, n, m)
        if spread_of(b) <= K:
            allocs.append(b)

    fails = 0
    witness = None
    for _ in range(sample):
        vals = tuple(draw(rng) for _ in range(n))
        ok = False
        for b in allocs:
            p = min_subsidy(vals, b)
            if p is not None and max(p) <= 1:
                ok = True
                break
        if not ok:
            fails += 1
            if witness is None:
                witness = vals

    print("     %-22s K=%d : %d sampled, %d without one"
          % (label, K, sample, fails))
    if witness:
        for i, v in enumerate(witness):
            print("        agent %d %s" % (i + 1, str(v)))
    return fails


CLASSES = (
    ("goods {0,1}", {0, 1}),
    ("chores {-1,0}", {-1, 0}),
    ("general {-1,0,1}", {-1, 0, 1}),
)


def pool_for(m, allowed):
    # At m >= 5 the class is far too large to enumerate, so valuations are
    # drawn on the fly instead: walk the subset lattice and pick each value
    # uniformly inside its admissible window, rejecting the ones outside the
    # class being sampled.
    if m >= 5:
        from gb_valuations import masks_by_popcount
        lo_d, hi_d = min(allowed), max(allowed)
        order = [s for s in masks_by_popcount(m) if s != 0]

        def draw(rng):
            # Walk the lattice by popcount. For a mask S the value must sit
            # within `allowed` of every single-bit deletion at once, and since
            # `allowed` is a contiguous range that intersection is the interval
            # [max_b v(S-b) + lo_d, min_b v(S-b) + hi_d], which is never empty.
            values = [0] * (1 << m)
            for S in order:
                bits = [1 << b for b in range(m) if S & (1 << b)]
                lo = max(values[S ^ b] for b in bits) + lo_d
                hi = min(values[S ^ b] for b in bits) + hi_d
                values[S] = rng.randint(lo, hi)
            return tuple(values)
        return draw

    if allowed == {-1, 0, 1}:
        return list(enumerate_general_binary(m))
    return enumerate_class(m, allowed)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "exhaustive"

    if mode == "exhaustive":
        print("EXHAUSTIVE n=3, m=3 -- does a valid allocation of spread <= K "
              "exist?")
        print()
        for label, allowed in CLASSES:
            pool = pool_for(3, allowed)
            for K in (1, 2):
                sweep_n3m3(pool, label, K)
            print()
    else:
        # One size per invocation: the background runner does not survive a
        # session boundary, and a foreground run has to finish inside its
        # timeout, so each (n, m) is driven separately from the command line.
        n, m, sample = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
        print("SAMPLED  n=%d m=%d, %d instances per class" % (n, m, sample),
              flush=True)
        for label, allowed in CLASSES:
            pool = pool_for(m, allowed)
            for K in (1, 2):
                sweep_general(pool, n, m, label, K, sample)
                sys.stdout.flush()


if __name__ == "__main__":
    main()
