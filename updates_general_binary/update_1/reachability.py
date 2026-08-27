"""
Approach 15: is the conjecture provable by ANY incremental algorithm?

test_insertion.py found a state from which no single insertion keeps the
subsidy within {0,1}^n. That refutes particular algorithms, but not the
incremental ARCHITECTURE, because a stuck state may simply be avoidable: on
that very witness the instance is solved by the path

    (,,)  ->  ({a},,)  ->  ({a},{c},)  ->  ({a},{c},{b})

every step of which is legal. So the question that actually decides the
architecture is reachability, not local stuckness.

    VALID STATE   a partial allocation that is envy-freeable and whose
                  MINIMAL subsidy satisfies p_i <= 1 for every i.

    MOVES         (a) add one unallocated item to one bundle;
                  (b) permute the bundles among the agents.
                  Both must land on a valid state.

    QUESTION      starting from the empty allocation -- always valid, p = 0 --
                  is a COMPLETE valid state always reachable?

Permutation moves are free rather than bundled into the insertion, which only
makes the reachable set larger, so this is the most generous possible test of
the architecture. If some instance has a complete valid state that is NOT
reachable, then no incremental algorithm whatsoever can work and the one-shot
route is forced. If completions are always reachable, the architecture is
viable and the remaining work is the selection rule.

The script also records, for the states where NO +1-insertion is available --
the residual states of the hybrid -- which moves do succeed, so the missing
rule can be read off the data rather than guessed.
"""
import itertools
import random
import sys
from collections import deque

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
    return p if (p is not None and all(q <= 1 for q in p)) else None


def all_states(n, m):
    """Every partial allocation, as a tuple of bundle masks."""
    out = []
    for assign in itertools.product(list(range(n)) + [None], repeat=m):
        b = [0] * n
        for k, owner in enumerate(assign):
            if owner is not None:
                b[owner] |= 1 << k
        out.append(tuple(b))
    return sorted(set(out))


def allocated(bundles):
    mask = 0
    for b in bundles:
        mask |= b
    return mask


def analyse(vals, n, m, perms, full_mask, collect=None):
    """
    BFS from the empty state. Returns
      (a complete valid state exists, a complete valid state is reachable,
       stuck states encountered).
    """
    valid_cache = {}

    def ok(state):
        if state not in valid_cache:
            valid_cache[state] = valid(vals, state)
        return valid_cache[state]

    empty = tuple([0] * n)
    seen = {empty}
    queue = deque([empty])
    reachable_complete = False
    stuck = []

    while queue:
        state = queue.popleft()
        free = [k for k in range(m) if not allocated(state) & (1 << k)]
        if not free:
            reachable_complete = True
            continue

        # One move = add an item to a bundle AND reassign the bundles to the
        # agents, with only the RESULT required to be valid. Requiring the
        # un-reassigned intermediate to be valid would wrongly forbid real
        # moves: from ({a},{c}) inserting b, ({c},{a,b}) can be valid while
        # ({a,b},{c}) is not.
        successors = []
        for g in free:
            for x in range(n):
                grown = tuple(b | (1 << g) if i == x else b
                              for i, b in enumerate(state))
                for perm in perms:
                    nxt = tuple(grown[perm[i]] for i in range(n))
                    if ok(nxt) is not None:
                        successors.append(nxt)
        for perm in perms:
            nxt = tuple(state[perm[i]] for i in range(n))
            if nxt != state and ok(nxt) is not None:
                successors.append(nxt)

        # A state counts as STUCK only if no item can be allocated even after
        # first permuting the bundles -- BKNS's EXTEND permutes and then
        # inserts, and their Lemma 3 makes the permuted state valid whenever
        # the original is, so permute-then-insert is a single legal move.
        # Testing bare insertions alone would flag states BKNS handles
        # comfortably, and the goods column would then contradict their
        # Theorem 4.
        can_allocate = any(allocated(s) != allocated(state) for s in successors)
        if not can_allocate:
            stuck.append(state)
            if collect is not None:
                collect.append((vals, state))

        for nxt in successors:
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)

    exists_complete = False
    for state in all_states(n, m):
        if allocated(state) == full_mask and ok(state) is not None:
            exists_complete = True
            break

    return exists_complete, reachable_complete, stuck


def run(pool, n, m, label, sample=None, seed=20260827, show_stuck=0):
    rng = random.Random(seed)
    perms = list(itertools.permutations(range(n)))
    full_mask = (1 << m) - 1

    multisets = itertools.combinations_with_replacement(pool, n)
    if sample is not None:
        multisets = list(multisets)
        if len(multisets) > sample:
            multisets = rng.sample(multisets, sample)

    total = exists = reachable = 0
    unreachable_witnesses = []
    with_stuck = 0
    stuck_examples = []

    for vals in multisets:
        total += 1
        e, r, stuck = analyse(vals, n, m, perms, full_mask,
                              collect=stuck_examples if show_stuck else None)
        exists += e
        reachable += r
        if stuck:
            with_stuck += 1
        if e and not r:
            unreachable_witnesses.append(vals)

    tag = "exhaustive" if sample is None else "sampled %d" % sample
    print("  %-22s n=%d m=%d : %d instances (%s)" % (label, n, m, total, tag))
    print("     complete valid state EXISTS    : %d" % exists)
    print("     complete valid state REACHABLE : %d" % reachable)
    print("     instances with >=1 stuck state : %d" % with_stuck)
    print("     ARCHITECTURE REFUTED BY        : %d instances"
          % len(unreachable_witnesses))
    for vals in unreachable_witnesses[:2]:
        print("       witness:")
        for i, v in enumerate(vals):
            print("         agent %d %s" % (i + 1, str(v)))
    return len(unreachable_witnesses)


CLASSES = (
    ("control goods {0,1}", {0, 1}),
    ("chores {-1,0}", {-1, 0}),
    ("general {-1,0,1}", {-1, 0, 1}),
)


def pool_for(m, allowed):
    if allowed == {-1, 0, 1}:
        return list(enumerate_general_binary(m))
    return enumerate_class(m, allowed)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "small"
    print("Is a complete valid state always REACHABLE from the empty one?")
    print()

    if mode == "small":
        plan = ((2, 2, None), (2, 3, None), (3, 2, None), (3, 3, 4000))
    else:
        plan = ((3, 3, 40000), (3, 4, 4000), (4, 4, 2000))

    bad = 0
    for (n, m, sample) in plan:
        for label, allowed in CLASSES:
            pool = pool_for(m, allowed)
            s = sample
            if allowed == {-1, 0, 1} and m >= 3 and sample is None:
                s = 40000
            bad += run(pool, n, m, label, sample=s)
        print()
    print("total instances refuting the incremental architecture: %d" % bad)


if __name__ == "__main__":
    main()
