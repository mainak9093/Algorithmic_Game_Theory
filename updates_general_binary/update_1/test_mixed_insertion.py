"""
Approach 15, the decisive experiment for the one route still standing.

test_insertion.py shows the insertion lemma (INS) is FALSE when the inserted
item is a chore, so "insert every item one at a time" cannot prove the
conjecture. But that does not kill the asymmetric route:

    PHASE 1  allocate the chores in ONE SHOT with our own theorem, obtaining a
             complete allocation of the chores with subsidy in {0,1}^n;
    PHASE 2  insert the goods ONE AT A TIME, BKNS-style, into that state.

Phase 2 only ever inserts goods, so the chore-insertion failure does not touch
it. What phase 2 needs is a strictly weaker statement than (INS):

    (INS-G)  Let (A, p) be an envy-free solution with minimal subsidy in
             {0,1}^n, over bundles that may contain ANYTHING (chores included),
             and let g be an unallocated item that is a good for every agent
             at every set -- every marginal of g in {0,1}. Is there a recipient
             and a reassignment keeping the minimal subsidy in {0,1}^n?

BKNS prove (INS-G) when the whole instance is dichotomous, so the bundles are
made of goods too. The question here is whether it survives bundles full of
chores. Fact F2 (the path-increment lemma) predicts it should: adding g to
bundle A_x moves a path's weight by v_i(g | A_x) - v_x(g | A_x), and when g is
a good for everyone that is at most 1 - 0 = 1, exactly as in the pure goods
case, no matter what the bundles contain.

This script tests that prediction by exhaustion. Instances have item m-1 a
universal good (all its marginals in {0,1}) and the remaining items arbitrary
general binary; states are the partial allocations in which every non-good item
is already allocated -- i.e. phase 1 has finished -- and the good is not.

The control is the same sweep restricted to fully dichotomous instances, where
BKNS's theorem says the answer must be zero failures.
"""
import itertools
import random
import sys

from gb_valuations import (
    enumerate_general_binary,
    arc_weights,
    is_envy_freeable,
    longest_paths,
    bundles_from_assignment,
)


def min_subsidy(vals, bundles):
    if not is_envy_freeable(vals, bundles):
        return None
    return longest_paths(arc_weights(vals, bundles))


def within_bound(p):
    return p is not None and all(q <= 1 for q in p)


def item_is_universal_good(v, m, g):
    """Every marginal of item g lies in {0,1}, at every set."""
    bit = 1 << g
    for S in range(1 << m):
        if not S & bit and v[S | bit] - v[S] not in (0, 1):
            return False
    return True


def all_marginals_in(v, m, allowed):
    for S in range(1 << m):
        for b in range(m):
            bit = 1 << b
            if not S & bit and v[S | bit] - v[S] not in allowed:
                return False
    return True


def insertion_works(vals, bundles, g, n):
    """Some recipient and reassignment keeps the minimal subsidy in {0,1}^n."""
    for x in range(n):
        grown = tuple(b | (1 << g) if i == x else b
                      for i, b in enumerate(bundles))
        for perm in itertools.permutations(range(n)):
            cand = tuple(grown[perm[i]] for i in range(n))
            if within_bound(min_subsidy(vals, cand)):
                return True
    return False


def safe_recipient_works(vals, bundles, g, n):
    """
    F2's prediction, sharpened: does a recipient x with a NON-NEGATIVE own
    marginal for g -- the ones the path-increment lemma calls safe -- already
    suffice, with no reassignment at all?
    """
    for x in range(n):
        if vals[x][bundles[x] | (1 << g)] - vals[x][bundles[x]] < 0:
            continue
        grown = tuple(b | (1 << g) if i == x else b
                      for i, b in enumerate(bundles))
        if within_bound(min_subsidy(vals, grown)):
            return True
    return False


def run(n, m, label, pool, sample=None, seed=20260827):
    rng = random.Random(seed)
    g = m - 1                                   # the good being inserted
    states = 0
    failures = []
    safe_failures = 0

    multisets = itertools.combinations_with_replacement(pool, n)
    if sample is not None:
        multisets = list(multisets)
        if len(multisets) > sample:
            multisets = rng.sample(multisets, sample)

    for vals in multisets:
        # phase 1 has finished: every non-good item allocated, the good not
        for assign in itertools.product(range(n), repeat=m - 1):
            full = tuple(list(assign) + [None])
            bundles = bundles_from_assignment(full, n, m)
            p = min_subsidy(vals, bundles)
            if not within_bound(p):
                continue
            states += 1
            if not insertion_works(vals, bundles, g, n):
                failures.append((vals, full))
            elif not safe_recipient_works(vals, bundles, g, n):
                safe_failures += 1

    tag = "exhaustive" if sample is None else "sampled %d multisets" % sample
    print("  %-30s n=%d m=%d : %d states (%s)" % (label, n, m, states, tag))
    print("       (INS-G) failures                 : %d" % len(failures))
    print("       safe-recipient-alone failures    : %d" % safe_failures)
    for vals, full in failures[:2]:
        print("       failure: assign=%s" % str(full))
        for i, v in enumerate(vals):
            print("           agent %d %s" % (i + 1, str(v)))
    return len(failures)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "small"
    print("(INS-G): inserting a universal GOOD into arbitrary general binary "
          "bundles")
    print()

    for m in (3, 4) if mode == "wide" else (3,):
        base = list(enumerate_general_binary(m))
        g = m - 1
        mixed = [v for v in base if item_is_universal_good(v, m, g)]
        dich = [v for v in base if all_marginals_in(v, m, {0, 1})]
        print("m=%d : %d general binary valuations, %d with item %d a "
              "universal good, %d fully dichotomous"
              % (m, len(base), len(mixed), g, len(dich)))
        print()
        for n in (2, 3):
            sample = None if (m == 3 and n <= 3) else 1500
            run(n, m, "control fully dichotomous", dich, sample=sample)
            run(n, m, "mixed (chores in the bundles)", mixed, sample=sample)
            print()


if __name__ == "__main__":
    main()
