"""
Approach 15: is BALANCE the invariant that makes the incremental architecture
work?

analyse_safe.py found that every DEAD state -- valid, but unable to reach any
complete valid state -- has bundle-size spread at least 2, and that not one
balanced valid state was dead, across roughly 1.2 million valid states. That
suggests the missing selection rule is simply: keep the bundles balanced.

Write

    BAL(A)   max_i |A_i| - min_i |A_i| <= 1.

The empty allocation satisfies BAL and is valid. If, from every valid BAL state
with an unallocated item, some move lands on a valid BAL state, then induction
gives a complete valid allocation and the conjecture follows. So the whole
architecture reduces to one step, which this script tests directly:

    (BAL-STEP)  from every valid state with BAL and an unallocated item, is
                there a move to a valid state with BAL?

A move adds one item to one bundle and reassigns the bundles to the agents,
with only the result required to be valid.

Two versions are measured, because a constructive rule is worth more than an
existence statement:

    (a) EXISTENTIAL   some move lands valid and balanced;
    (b) CONSTRUCTIVE  some move that puts the item in a MINIMUM-SIZE bundle
                      lands valid. Since a balanced state has every bundle at
                      the minimum or one above, growing a minimum bundle
                      always preserves BAL, so (b) implies (a) and names the
                      rule.

The goods and chores columns are controls: both known theorems must be
compatible with a rule that proves them, so a failure there would indicate the
invariant is simply too strong rather than that the conjecture is false.
"""
import itertools
import random
import sys

from gb_valuations import (
    enumerate_general_binary,
    enumerate_class,
    arc_weights,
    is_envy_freeable,
    longest_paths,
)


def min_subsidy(vals, bundles):
    if not is_envy_freeable(vals, bundles):
        return None
    return longest_paths(arc_weights(vals, bundles))


def valid(vals, bundles):
    p = min_subsidy(vals, bundles)
    return p is not None and all(q <= 1 for q in p)


def sizes(bundles):
    return [bin(b).count("1") for b in bundles]


def balanced(bundles):
    s = sizes(bundles)
    return max(s) - min(s) <= 1


def allocated(bundles):
    mask = 0
    for b in bundles:
        mask |= b
    return mask


def all_partial(n, m):
    out = set()
    for assign in itertools.product(list(range(n)) + [None], repeat=m):
        b = [0] * n
        for k, owner in enumerate(assign):
            if owner is not None:
                b[owner] |= 1 << k
        out.add(tuple(b))
    return sorted(out)


def step_options(vals, state, n, m, perms, only_min_bundle):
    """Moves from `state` landing on a valid balanced state."""
    free = [k for k in range(m) if not allocated(state) & (1 << k)]
    s = sizes(state)
    lo = min(s)
    out = []
    for g in free:
        for x in range(n):
            if only_min_bundle and s[x] != lo:
                continue
            grown = tuple(b | (1 << g) if i == x else b
                          for i, b in enumerate(state))
            for perm in perms:
                t = tuple(grown[perm[i]] for i in range(n))
                if balanced(t) and valid(vals, t):
                    out.append(t)
                    break
            if out and only_min_bundle:
                return out
    return out


def run(pool, n, m, label, sample=None, seed=20260827):
    rng = random.Random(seed)
    perms = list(itertools.permutations(range(n)))
    states = all_partial(n, m)

    multisets = itertools.combinations_with_replacement(pool, n)
    if sample is not None:
        multisets = list(multisets)
        if len(multisets) > sample:
            multisets = rng.sample(multisets, sample)

    tested = 0
    fail_exist = []
    fail_constr = 0

    for vals in multisets:
        for st in states:
            if allocated(st) == (1 << m) - 1:
                continue
            if not balanced(st) or not valid(vals, st):
                continue
            tested += 1
            if not step_options(vals, st, n, m, perms, False):
                fail_exist.append((vals, st))
            elif not step_options(vals, st, n, m, perms, True):
                fail_constr += 1

    print("  %-22s n=%d m=%d : %d valid balanced states tested"
          % (label, n, m, tested))
    print("       (a) EXISTENTIAL failures  : %d" % len(fail_exist))
    print("       (b) CONSTRUCTIVE failures : %d" % fail_constr)
    for vals, st in fail_exist[:2]:
        print("       failure at state %s sizes=%s" % (str(st), sizes(st)))
        for i, v in enumerate(vals):
            print("          agent %d %s" % (i + 1, str(v)))
    return len(fail_exist), fail_constr


CLASSES = (
    ("control goods {0,1}", {0, 1}),
    ("control chores {-1,0}", {-1, 0}),
    ("general {-1,0,1}", {-1, 0, 1}),
)


def pool_for(m, allowed):
    if allowed == {-1, 0, 1}:
        return list(enumerate_general_binary(m))
    return enumerate_class(m, allowed)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "small"
    print("(BAL-STEP): can balance always be maintained?")
    print()

    plan = (((2, 2, None), (2, 3, None), (3, 2, None), (3, 3, 3000))
            if mode == "small" else ((3, 3, 30000), (3, 4, 800), (4, 4, 400)))

    tot_e = tot_c = 0
    for (n, m, sample) in plan:
        for label, allowed in CLASSES:
            pool = pool_for(m, allowed)
            s = sample
            if allowed == {-1, 0, 1} and m >= 3 and sample is None:
                s = 30000
            e, c = run(pool, n, m, label, sample=s)
            tot_e += e
            tot_c += c
        print()
    print("TOTAL existential failures  : %d" % tot_e)
    print("TOTAL constructive failures : %d" % tot_c)
    if tot_e == 0:
        print()
        print("-> balance can always be maintained; the invariant survives.")


if __name__ == "__main__":
    main()
