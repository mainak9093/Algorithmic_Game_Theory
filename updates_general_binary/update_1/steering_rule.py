"""
Approach 15: the first-excursion repair theorem is dead; is the STEERING rule
alive?

Mainak's argument (recorded in approach_15.md section 26) kills the repair
theorem outright. Two steps:

  (i) a balanced state plus one insertion can reach spread 2 only by growing a
      largest bundle, so the oversized bundle is unique -- first excursions are
      more rigid than arbitrary spread-2 states;

  (ii) but the Fact B dead state is itself a first excursion. In the pure-chore
       witness (v_1 = v_2 = -|S|, and v_3 with b free), the state
       (empty, empty, {a}) is balanced with sizes 0,0,1 and valid with minimal
       subsidy (0,0,1); inserting c into agent 3 gives (empty, empty, {a,c}),
       which is valid, has sizes 0,0,2 with a unique maximum -- and is dead.

So none of "valid + spread <= 2", "valid + spread <= 2 + unique maximum", or
"reachable from a balanced valid state by one valid insertion" is enough.

ONE REFINEMENT THIS SCRIPT ADDS. In that witness the departure from balance was
GRATUITOUS, not forced: from (empty, empty, {a}) the move "give c to agent 1"
lands on ({c}, empty, {a}), which is valid AND balanced. So the witness refutes
"any first excursion is repairable" but says nothing against the obvious
steering rule, which never leaves balance without cause:

    (SR)  from a valid state, if some move lands on a valid BALANCED state,
          take one of those; otherwise take any valid move.

This script tests (SR) in both strengths, since they are different theorems:

    (SR-exists)  following (SR), is a complete valid state still reachable?
    (SR-forced)  does EVERY maximal (SR)-run end complete, i.e. are there
                 (SR)-reachable states with no (SR)-successor and items left?

(SR-forced) is what a proof would need: it says the rule cannot be executed
badly. (SR-exists) only says the rule does not destroy all the good routes.

Also checks Mainak's subsidy-pattern table: for a valid state with minimal
p in {0,1}^n, envy weights obey w(i,j) <= p_i - p_j, so a positive arc runs
only from a PAID agent to an UNPAID one and has weight exactly 1.
"""
import itertools
import random
import sys
from collections import deque

from gb_valuations import (
    enumerate_class,
    enumerate_general_binary,
    arc_weights,
    is_envy_freeable,
    longest_paths,
)


def min_subsidy(vals, bundles):
    if not is_envy_freeable(vals, bundles):
        return None
    return longest_paths(arc_weights(vals, bundles))


def valid_p(vals, bundles):
    p = min_subsidy(vals, bundles)
    return p if (p is not None and all(q <= 1 for q in p)) else None


def sizes(bundles):
    return [bin(b).count("1") for b in bundles]


def spread(bundles):
    z = sizes(bundles)
    return max(z) - min(z)


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


def successors(vals, s, n, m, perms, cache):
    """Insertion moves: add one item to one bundle, then reassign bundles."""
    out = []
    free = [k for k in range(m) if not allocated(s) & (1 << k)]
    for g in free:
        for x in range(n):
            grown = tuple(b | (1 << g) if i == x else b
                          for i, b in enumerate(s))
            for perm in perms:
                t = tuple(grown[perm[i]] for i in range(n))
                if t not in cache:
                    cache[t] = valid_p(vals, t) is not None
                if cache[t]:
                    out.append(t)
    return out


def sr_successors(vals, s, n, m, perms, cache):
    """(SR): prefer balanced landings; fall back to any if none exist."""
    succ = successors(vals, s, n, m, perms, cache)
    bal = [t for t in succ if spread(t) <= 1]
    return bal if bal else succ


def analyse(vals, n, m, perms):
    cache = {}
    full = (1 << m) - 1
    empty = tuple([0] * n)
    if valid_p(vals, empty) is None:
        return None

    seen = {empty}
    queue = deque([empty])
    reach_complete = False
    sr_dead_ends = 0

    while queue:
        s = queue.popleft()
        if allocated(s) == full:
            reach_complete = True
            continue
        succ = sr_successors(vals, s, n, m, perms, cache)
        if not succ:
            sr_dead_ends += 1
            continue
        for t in succ:
            if t not in seen:
                seen.add(t)
                queue.append(t)
    return reach_complete, sr_dead_ends


def check_subsidy_table(vals, n, m, perms):
    """w(i,j) <= p_i - p_j; positive arcs run paid -> unpaid with weight 1."""
    bad = 0
    pos_wrong = 0
    for s in all_partial(n, m):
        p = valid_p(vals, s)
        if p is None:
            continue
        w = arc_weights(vals, s)
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                if w[i][j] > p[i] - p[j]:
                    bad += 1
                if w[i][j] > 0 and not (p[i] == 1 and p[j] == 0
                                        and w[i][j] == 1):
                    pos_wrong += 1
    return bad, pos_wrong


CLASSES = (
    ("goods {0,1}", {0, 1}),
    ("chores {-1,0}", {-1, 0}),
    ("general {-1,0,1}", {-1, 0, 1}),
)


def pool_for(m, allowed):
    if allowed == {-1, 0, 1}:
        return list(enumerate_general_binary(m))
    return enumerate_class(m, allowed)


def main():
    print("The steering rule (SR): never leave balance without cause")
    print()
    rng = random.Random(20260827)

    for (n, m, sample) in ((3, 3, 6000), (3, 4, 900), (4, 4, 500)):
        for label, allowed in CLASSES:
            pool = pool_for(m, allowed)
            perms = list(itertools.permutations(range(n)))
            inst = 0
            no_reach = 0
            dead_ends = 0
            inst_with_dead = 0
            witness = None
            for _ in range(sample):
                vals = tuple(rng.choice(pool) for _ in range(n))
                r = analyse(vals, n, m, perms)
                if r is None:
                    continue
                inst += 1
                ok, de = r
                if not ok:
                    no_reach += 1
                    if witness is None:
                        witness = vals
                if de:
                    dead_ends += de
                    inst_with_dead += 1
            print("  %-18s n=%d m=%d : %d instances" % (label, n, m, inst))
            print("     (SR-exists) failures  : %d" % no_reach)
            print("     (SR-forced) dead ends : %d states, in %d instances"
                  % (dead_ends, inst_with_dead))
            if witness:
                for i, v in enumerate(witness):
                    print("        agent %d %s" % (i + 1, str(v)))
        print()

    print("Mainak's subsidy-pattern table, checked over all valid states")
    print()
    for (n, m, sample) in ((3, 3, 800),):
        for label, allowed in CLASSES:
            pool = pool_for(m, allowed)
            perms = list(itertools.permutations(range(n)))
            bad = pos_wrong = 0
            for _ in range(sample):
                vals = tuple(rng.choice(pool) for _ in range(n))
                b, pw = check_subsidy_table(vals, n, m, perms)
                bad += b
                pos_wrong += pw
            print("  %-18s w(i,j) <= p_i - p_j violations: %d ; "
                  "positive arcs not paid->unpaid of weight 1: %d"
                  % (label, bad, pos_wrong))


if __name__ == "__main__":
    main()
