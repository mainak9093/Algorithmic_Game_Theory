"""
Approach 15, secondary experiment: does the ONE-ITEM-AT-A-TIME insertion lemma
hold outside the goods class?

    (INS)  Let (A, p) be an envy-free solution on a partial allocation with
           minimal subsidy p in {0,1}^n, and let g be an unallocated item.
           Is there a recipient x and a permutation sigma of the resulting
           bundles such that the new allocation is envy-freeable with minimal
           subsidy again in {0,1}^n?

Why this matters. Barman-Krishna-Narahari-Sadhukhan prove Theorem 4 by
induction on the number of allocated goods, and the empty allocation is used
ONLY to seed t = 0 -- every later step reads nothing but the current
(A^t, p^t) and the new good. So their theorem IS (INS) restricted to the goods
class, and the goods column below must show zero failures or this harness is
wrong.

Our own chores theorem does NOT prove (INS) for chores: it is one-shot (a
Tao-Wu-Yu-Zhou partial allocation, then a completion), not incremental. And
check_f5.py shows BKNS's own algorithm cannot decide the chores case, since
its routing rule picks the wrong agent. So (INS) on chores is genuinely open,
and (INS) on general binary is what an incremental attack on the conjecture
would need. This script settles both by exhaustion at small (n, m).

It also measures a candidate ALGORITHM, not just the existence statement:

    (GREEDY)  give g to an agent maximising the marginal v_x(g | A_x),
              breaking ties toward a minimally subsidised agent, and do not
              permute at all.

The tie-break is the unification the facts suggest -- BKNS routes goods to a
maximally subsidised agent, check_f5.py shows chores must go to a minimally
subsidised one, and maximising the marginal is what the path-increment lemma
(F2) says keeps the increment at most 1. If (GREEDY) matched (INS) everywhere,
the next pass would have an algorithm to try to prove correct.
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
    bundles_from_assignment,
    partial_assignments,
)


def min_subsidy(vals, bundles):
    if not is_envy_freeable(vals, bundles):
        return None
    return longest_paths(arc_weights(vals, bundles))


def within_bound(p):
    return p is not None and all(q <= 1 for q in p)


def insertion_options(vals, bundles, g, n):
    """
    Every (recipient, permutation) whose result is envy-freeable with minimal
    subsidy in {0,1}^n. Returns the list of recipients that work with SOME
    permutation, and the list that work with the identity permutation.
    """
    any_perm, identity = [], []
    for x in range(n):
        grown = tuple(b | (1 << g) if i == x else b
                      for i, b in enumerate(bundles))
        if within_bound(min_subsidy(vals, grown)):
            identity.append(x)
            any_perm.append(x)
            continue
        for perm in itertools.permutations(range(n)):
            permuted = tuple(grown[perm[i]] for i in range(n))
            if within_bound(min_subsidy(vals, permuted)):
                any_perm.append(x)
                break
    return any_perm, identity


def greedy_choice(vals, bundles, g, p, n):
    """Maximise the marginal for the recipient; tie-break to minimal subsidy."""
    best, choice = None, None
    for x in range(n):
        marginal = vals[x][bundles[x] | (1 << g)] - vals[x][bundles[x]]
        key = (marginal, -p[x])
        if best is None or key > best:
            best, choice = key, x
    return choice


def run(pool, n, m, label, sample=None, seed=20260827):
    rng = random.Random(seed)
    states = 0
    ins_failures = []
    greedy_failures = []

    multisets = itertools.combinations_with_replacement(pool, n)
    if sample is not None:
        multisets = list(multisets)
        if len(multisets) > sample:
            multisets = rng.sample(multisets, sample)

    for vals in multisets:
        for assign in partial_assignments(n, m):
            unallocated = [k for k in range(m) if assign[k] is None]
            if not unallocated:
                continue
            bundles = bundles_from_assignment(assign, n, m)
            p = min_subsidy(vals, bundles)
            if not within_bound(p):
                continue                      # not a state (INS) speaks about
            for g in unallocated:
                states += 1
                any_perm, identity = insertion_options(vals, bundles, g, n)
                if not any_perm:
                    ins_failures.append((vals, assign, g))
                    continue
                if greedy_choice(vals, bundles, g, p, n) not in identity:
                    greedy_failures.append((vals, assign, g))

    tag = "exhaustive" if sample is None else "sampled %d multisets" % sample
    print("  %-22s n=%d m=%d : %d states (%s)" % (label, n, m, states, tag))
    print("       (INS) failures    : %d" % len(ins_failures))
    print("       (GREEDY) failures : %d" % len(greedy_failures))
    for name, fails in (("(INS)", ins_failures), ("(GREEDY)", greedy_failures)):
        for vals, assign, g in fails[:2]:
            print("       %s failure: assign=%s insert item %d"
                  % (name, str(assign), g))
            for i, v in enumerate(vals):
                print("           agent %d %s" % (i + 1, str(v)))
    return len(ins_failures), len(greedy_failures)


CLASSES = (
    ("control goods {0,1}", {0, 1}),
    ("chores {-1,0}", {-1, 0}),
    ("general {-1,0,1}", {-1, 0, 1}),
)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "small"
    print("Insertion lemma (INS) and the greedy routing rule")
    print()

    for (n, m, sample) in (((2, 2, None), (2, 3, None), (3, 2, None),
                            (3, 3, 400))
                           if mode == "small"
                           else ((2, 3, None), (3, 3, 3000), (2, 4, 2000))):
        for label, allowed in CLASSES:
            pool = (list(enumerate_general_binary(m)) if allowed == {-1, 0, 1}
                    else enumerate_class(m, allowed))
            run(pool, n, m, label, sample=sample)
        print()


if __name__ == "__main__":
    main()
