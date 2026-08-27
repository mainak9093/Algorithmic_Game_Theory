"""
Approach 15: the two halves of (S1) are the SAME statement.

(S1) claims that every dichotomous-goods instance, and every negative-
dichotomous (chores) instance, admits a valid BALANCED allocation -- one with
subsidy at most 1 per agent and bundle sizes differing by at most one. The two
halves are not independent conjectures. They are equivalent, by a duality that
only works on balanced allocations.

THE DUALITY. Let v be dichotomous (every marginal in {0,1}) and set

    c(S) := |S| - v(S).

Then c has marginals 1 - (marginal of v) in {0,1}, so c is a dichotomous COST
function, i.e. the chores model. For any allocation A,

    w^v_A(i,j) = v_i(A_j) - v_i(A_i)
               = (|A_j| - |A_i|) + (c_i(A_i) - c_i(A_j))
               = (|A_j| - |A_i|) + w^c_A(i,j).

So the size-shift changes every arc weight by exactly the bundle-size
difference. On an allocation where all bundles have the SAME cardinality that
term vanishes and the two envy graphs are IDENTICAL -- same weights, same
cycles, same longest paths, hence the same envy-freeability and the same
minimal subsidy. That is why the transform is not a free reduction in general
but is one here.

FROM EXACTLY BALANCED TO BALANCED. If n does not divide m, pad with dummy
items whose marginal is 0 for every agent. Dummies leave v unchanged, so they
leave every envy graph unchanged, and they can be redistributed among the
agents at will for the same reason. Padding to the next multiple of n adds
s < n dummies; solve the padded instance exactly balanced, redistribute the
dummies so no agent holds more than one, then delete them. Sizes drop by 0 or
1, so the result is balanced, and the envy graph never moved.

Hence  (S1)-goods for all m  <=>  (S1)-goods for n | m
                              <=>  (S1)-chores for n | m  <=>  (S1)-chores for all m.

This script checks all of it: the arc-weight identity, the equality of envy
graphs and minimal subsidies on equal-cardinality allocations, the failure of
the identity when cardinalities differ, and the dummy-padding step.
"""
import itertools
import random

from gb_valuations import (
    enumerate_class,
    arc_weights,
    is_envy_freeable,
    longest_paths,
    bundles_from_assignment,
)


def popcount(x):
    return bin(x).count("1")


def dual(v, m):
    """c(S) = |S| - v(S); dichotomous goods -> dichotomous costs."""
    return tuple(popcount(S) - v[S] for S in range(1 << m))


def cost_arc_weights(cs, bundles):
    """Chores-form arc weights w(i,j) = c_i(A_i) - c_i(A_j)."""
    n = len(bundles)
    return [[cs[i][bundles[i]] - cs[i][bundles[j]] for j in range(n)]
            for i in range(n)]


def min_subsidy_from(w, freeable):
    return longest_paths(w) if freeable else None


def cost_envy_freeable(cs, bundles):
    """Halpern-Shah (ii) in cost form: no reassignment lowers total cost."""
    n = len(bundles)
    base = sum(cs[i][bundles[i]] for i in range(n))
    for perm in itertools.permutations(range(n)):
        if sum(cs[i][bundles[perm[i]]] for i in range(n)) < base:
            return False
    return True


def main():
    rng = random.Random(20260827)

    print("PART 1 -- the arc-weight identity and its consequence")
    print()
    for (n, m) in ((3, 3), (3, 4), (4, 4)):
        pool = enumerate_class(m, {0, 1})
        equal_checked = equal_bad = 0
        unequal_checked = unequal_differ = 0
        identity_bad = 0

        for _ in range(4000):
            vs = tuple(rng.choice(pool) for _ in range(n))
            cs = tuple(dual(v, m) for v in vs)
            assign = tuple(rng.randrange(n) for _ in range(m))
            b = bundles_from_assignment(assign, n, m)

            wv = arc_weights(vs, b)
            wc = cost_arc_weights(cs, b)
            sizes = [popcount(x) for x in b]

            # the identity, on every allocation
            for i in range(n):
                for j in range(n):
                    if wv[i][j] != (sizes[j] - sizes[i]) + wc[i][j]:
                        identity_bad += 1

            if len(set(sizes)) == 1:
                equal_checked += 1
                fv = is_envy_freeable(vs, b)
                fc = cost_envy_freeable(cs, b)
                pv = min_subsidy_from(wv, fv)
                pc = min_subsidy_from(wc, fc)
                if wv != wc or fv != fc or pv != pc:
                    equal_bad += 1
            else:
                unequal_checked += 1
                if wv != wc:
                    unequal_differ += 1

        print("  n=%d m=%d : arc-weight identity violations: %d"
              % (n, m, identity_bad))
        print("     equal-cardinality allocations   : %d checked, "
              "%d where the two envy graphs or subsidies differ"
              % (equal_checked, equal_bad))
        print("     unequal-cardinality allocations : %d checked, "
              "%d where they differ (expected: most)"
              % (unequal_checked, unequal_differ))
    print()

    print("PART 2 -- dummy padding leaves the envy graph alone")
    print()
    n, m = 3, 4
    pool = enumerate_class(m, {0, 1})
    bad_pad = 0
    for _ in range(3000):
        vs = tuple(rng.choice(pool) for _ in range(n))
        # extend each valuation to m+1 items, the last one a dummy (marginal 0)
        vs_pad = tuple(tuple(v[S & ((1 << m) - 1)] for S in range(1 << (m + 1)))
                       for v in vs)
        # dummy marginals must be 0 everywhere
        for v in vs_pad:
            for S in range(1 << (m + 1)):
                if not S & (1 << m) and v[S | (1 << m)] != v[S]:
                    bad_pad += 1
        assign = tuple(rng.randrange(n) for _ in range(m))
        b = bundles_from_assignment(assign, n, m)
        for holder in range(n):
            bp = tuple(x | (1 << m) if i == holder else x
                       for i, x in enumerate(b))
            if arc_weights(vs_pad, bp) != arc_weights(vs, b):
                bad_pad += 1
    print("  violations (dummy changes a marginal or an arc weight): %d"
          % bad_pad)
    print()
    print("So the dummy may be handed to any agent without moving the envy")
    print("graph, which is what lets the padding be redistributed evenly")
    print("before it is deleted.")


if __name__ == "__main__":
    main()
