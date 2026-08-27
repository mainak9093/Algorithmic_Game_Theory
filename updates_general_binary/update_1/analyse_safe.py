"""
Approach 15: what separates the safe states from the dead ends?

reachability.py established that a complete valid state is always REACHABLE,
so the incremental architecture survives; but stuck states do exist and are
themselves reachable, so a correct algorithm must steer around them. The
question is what the steering rule is.

    VALID  partial allocation, envy-freeable, minimal subsidy p_i <= 1 for all i
    MOVE   permute the bundles, or add one unallocated item to one bundle,
           landing valid either way
    SAFE   a valid state from which some complete valid state is reachable
    DEAD   a valid state that is not safe

This script computes SAFE exactly, by a fixpoint over the move graph (backward
from the complete valid states, which handles the cycles that permutation moves
create), and then tests candidate characterisations of DEAD against the data.

The candidates are the ones the earlier facts suggest:

  BAL    max_i |A_i| - min_i |A_i| <= 1, i.e. no bundle runs ahead of another by
         more than one item. The witness in approach_15.md section 8 became
         stuck precisely by piling two chores on one agent while two agents
         held nothing, and its escape route was the balanced allocation, so
         balance is the first thing to test. It also connects to the project's
         existing docs/BALANCE_RULE.md.

  PLUS   some unallocated item has a +1 marginal for some agent at some current
         bundle -- the hypothesis under which fact A guarantees a safe move.

  ZERO   the state has an agent with subsidy 0 holding a smallest bundle.

A characterisation that is exactly right would be an invariant to then prove:
if every BAL state is safe, and BAL can always be maintained, the architecture
closes.
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


def all_partial(n, m):
    out = set()
    for assign in itertools.product(list(range(n)) + [None], repeat=m):
        b = [0] * n
        for k, owner in enumerate(assign):
            if owner is not None:
                b[owner] |= 1 << k
        out.add(tuple(b))
    return sorted(out)


def allocated(bundles):
    mask = 0
    for b in bundles:
        mask |= b
    return mask


def sizes(bundles):
    return [bin(b).count("1") for b in bundles]


def spread(bundles):
    s = sizes(bundles)
    return max(s) - min(s)


def has_plus_one(vals, bundles, n, m):
    """Some unallocated item has a +1 marginal at some current bundle."""
    alloc = allocated(bundles)
    for g in range(m):
        if alloc & (1 << g):
            continue
        for i in range(n):
            for j in range(n):
                b = bundles[j]
                if vals[i][b | (1 << g)] - vals[i][b] == 1:
                    return True
    return False


def analyse_instance(vals, n, m, perms, states, full_mask):
    """Returns (valid states, safe set, dead set)."""
    pmap = {}
    for s in states:
        p = min_subsidy(vals, s)
        if p is not None and all(q <= 1 for q in p):
            pmap[s] = p
    valid_states = set(pmap)

    # A move adds one item to one bundle AND reassigns the resulting bundles
    # to the agents, requiring only the RESULT to be valid. Insisting that the
    # intermediate (inserted but not yet reassigned) be valid would be wrong:
    # from ({a},{c}) inserting b, the allocation ({c},{a,b}) can be valid while
    # ({a,b},{c}) is not, and only the former is the move actually taken.
    succ = {s: [] for s in valid_states}
    for s in valid_states:
        free = [k for k in range(m) if not allocated(s) & (1 << k)]
        for g in free:
            for x in range(n):
                grown = tuple(b | (1 << g) if i == x else b
                              for i, b in enumerate(s))
                for perm in perms:
                    t = tuple(grown[perm[i]] for i in range(n))
                    if t in valid_states:
                        succ[s].append(t)
        for perm in perms:
            t = tuple(s[perm[i]] for i in range(n))
            if t != s and t in valid_states:
                succ[s].append(t)

    safe = {s for s in valid_states if allocated(s) == full_mask}
    changed = True
    while changed:
        changed = False
        for s in valid_states:
            if s in safe:
                continue
            if any(t in safe for t in succ[s]):
                safe.add(s)
                changed = True

    dead = valid_states - safe
    return pmap, valid_states, safe, dead


def run(pool, n, m, label, sample=None, seed=20260827, dump=0):
    rng = random.Random(seed)
    perms = list(itertools.permutations(range(n)))
    states = all_partial(n, m)
    full_mask = (1 << m) - 1

    # Sample multisets directly rather than materialising every one: at m=4 the
    # pool has 197547 valuations and the full list does not fit in memory.
    if sample is None:
        multisets = itertools.combinations_with_replacement(pool, n)
    else:
        multisets = (tuple(sorted(rng.choice(pool) for _ in range(n)))
                     for _ in range(sample))

    n_inst = tot_valid = tot_dead = 0
    dead_bal = dead_plus = 0
    bal_total = bal_dead = 0
    dumped = 0

    for vals in multisets:
        n_inst += 1
        pmap, valid_states, safe, dead = analyse_instance(
            vals, n, m, perms, states, full_mask)
        tot_valid += len(valid_states)
        tot_dead += len(dead)

        for s in valid_states:
            b = spread(s) <= 1
            if b:
                bal_total += 1
                if s in dead:
                    bal_dead += 1
        for s in dead:
            if spread(s) <= 1:
                dead_bal += 1
            if has_plus_one(vals, s, n, m):
                dead_plus += 1
            if dumped < dump:
                dumped += 1
                print("     DEAD state %s  sizes=%s spread=%d p=%s plus1=%s"
                      % (str(s), sizes(s), spread(s), pmap[s],
                         has_plus_one(vals, s, n, m)))
                for i, v in enumerate(vals):
                    print("        agent %d %s" % (i + 1, str(v)))

    print("  %-22s n=%d m=%d : %d instances, %d valid states, %d dead"
          % (label, n, m, n_inst, tot_valid, tot_dead))
    if tot_dead:
        print("       dead states that are BALANCED (spread<=1) : %d of %d"
              % (dead_bal, tot_dead))
        print("       dead states with a +1 move available      : %d of %d"
              % (dead_plus, tot_dead))
    print("       BALANCED valid states that are dead        : %d of %d"
          % (bal_dead, bal_total))
    return tot_dead, bal_dead


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
    print("Safe vs dead states, and what characterises the dead ones")
    print()

    plan = ((2, 3, 30000), (3, 3, 3000)) if mode == "small" else ((3, 4, 600),)

    total_bal_dead = 0
    for (n, m, sample) in plan:
        for label, allowed in CLASSES:
            _, bd = run(pool_for(m, allowed), n, m, label, sample=sample,
                        dump=2 if allowed == {-1, 0, 1} else 0)
            total_bal_dead += bd
        print()
    print("BALANCED states that are dead, across everything: %d"
          % total_bal_dead)
    if total_bal_dead == 0:
        print("-> every balanced valid state is safe, in all data so far.")


if __name__ == "__main__":
    main()
