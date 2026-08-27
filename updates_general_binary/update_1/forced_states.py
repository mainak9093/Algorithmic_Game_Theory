"""
Approach 15: reducing (SR-forced) to a statement about FORCED states.

An (SR)-run can only halt early at a DEAD state -- one with no valid successor
at all. And (SR) only ever lands on an unbalanced state when no balanced
landing exists. Call a valid incomplete state

    FORCED   if it has at least one valid successor but no valid BALANCED
             successor.

At a non-forced state (SR) moves to a balanced state, and no balanced state is
dead (Fact F). So the only way an (SR)-run can reach a dead state is out of a
forced state, where (SR) permits every valid successor. Hence

    (SR-forced)  <==  at every FORCED state, no valid successor is dead.

This script tests exactly that implication's hypothesis, which is far narrower
than the global reachability question, and profiles the forced states so the
structure can be read off rather than guessed:

  * how many forced states there are, and whether any has a dead successor;
  * whether the dead states are (SR)-reachable at all;
  * for each forced state: sizes, minimal subsidy, whether a +1 move is
    available, and how many of its successors are safe;
  * whether the refinement "at a forced state, insert into a MINIMUM-size
    bundle" is always available and always safe -- a candidate secondary rule
    that would make (SR) fully deterministic.

Both pure classes are controls: Fact G says balance is always maintainable
there, so they should report no forced states at all.
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


def sizes(b):
    return [bin(x).count("1") for x in b]


def spread(b):
    z = sizes(b)
    return max(z) - min(z)


def allocated(b):
    mask = 0
    for x in b:
        mask |= x
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


def has_plus_one(vals, b, n, m):
    alloc = allocated(b)
    for g in range(m):
        if alloc & (1 << g):
            continue
        for i in range(n):
            for j in range(n):
                if vals[i][b[j] | (1 << g)] - vals[i][b[j]] == 1:
                    return True
    return False


def build(vals, n, m, perms, states, full):
    """valid states, their successors, and which successors grow a min bundle"""
    pmap = {}
    for s in states:
        p = valid_p(vals, s)
        if p is not None:
            pmap[s] = p
    valid = set(pmap)

    succ, succ_min = {}, {}
    for s in valid:
        free = [k for k in range(m) if not allocated(s) & (1 << k)]
        z = sizes(s)
        lo = min(z)
        out, out_min = [], []
        for g in free:
            for x in range(n):
                grown = tuple(y | (1 << g) if i == x else y
                              for i, y in enumerate(s))
                for perm in perms:
                    t = tuple(grown[perm[i]] for i in range(n))
                    if t in valid:
                        out.append(t)
                        if z[x] == lo:
                            out_min.append(t)
        succ[s] = out
        succ_min[s] = out_min

    safe = {s for s in valid if allocated(s) == full}
    changed = True
    while changed:
        changed = False
        for s in valid:
            if s not in safe and any(t in safe for t in succ[s]):
                safe.add(s)
                changed = True
    return pmap, valid, succ, succ_min, safe


def sr_reachable(vals, n, m, perms, valid, succ, full):
    empty = tuple([0] * n)
    if empty not in valid:
        return set()
    seen = {empty}
    q = deque([empty])
    while q:
        s = q.popleft()
        if allocated(s) == full:
            continue
        bal = [t for t in succ[s] if spread(t) <= 1]
        for t in (bal if bal else succ[s]):
            if t not in seen:
                seen.add(t)
                q.append(t)
    return seen


def run(pool, n, m, label, sample, seed=20260827, dump=0):
    rng = random.Random(seed)
    perms = list(itertools.permutations(range(n)))
    states = all_partial(n, m)
    full = (1 << m) - 1

    n_forced = 0
    forced_with_dead_succ = 0
    forced_no_min_move = 0
    forced_min_move_dead = 0
    dead_total = 0
    dead_sr_reachable = 0
    dumped = 0

    for _ in range(sample):
        vals = tuple(rng.choice(pool) for _ in range(n))
        pmap, valid, succ, succ_min, safe = build(
            vals, n, m, perms, states, full)
        reach = sr_reachable(vals, n, m, perms, valid, succ, full)

        for s in valid:
            if allocated(s) == full:
                continue
            if not succ[s]:
                dead_total += 1
                if s in reach:
                    dead_sr_reachable += 1
                continue
            if any(spread(t) <= 1 for t in succ[s]):
                continue                      # not forced
            n_forced += 1
            dead_succ = [t for t in succ[s] if not succ[t]
                         and allocated(t) != full]
            if dead_succ:
                forced_with_dead_succ += 1
            if not succ_min[s]:
                forced_no_min_move += 1
            elif any(not succ[t] and allocated(t) != full
                     for t in succ_min[s]):
                forced_min_move_dead += 1
            if dumped < dump:
                dumped += 1
                print("     FORCED %s sizes=%s p=%s plus1=%s "
                      "succ=%d safe=%d min-moves=%d"
                      % (str(s), sizes(s), pmap[s],
                         has_plus_one(vals, s, n, m), len(succ[s]),
                         sum(1 for t in succ[s] if t in safe),
                         len(succ_min[s])))

    print("  %-18s n=%d m=%d : %d instances" % (label, n, m, sample))
    print("     forced states                         : %d" % n_forced)
    print("     ...with a DEAD successor              : %d"
          % forced_with_dead_succ)
    print("     ...with no minimum-bundle move at all : %d"
          % forced_no_min_move)
    print("     ...whose minimum-bundle move is dead  : %d"
          % forced_min_move_dead)
    print("     dead states                           : %d (%d SR-reachable)"
          % (dead_total, dead_sr_reachable))
    return forced_with_dead_succ, dead_sr_reachable


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
    print("(SR-forced) reduced: does any FORCED state have a DEAD successor?")
    print()
    bad = 0
    for (n, m, sample) in ((3, 3, 4000), (3, 4, 700), (4, 4, 350)):
        for label, allowed in CLASSES:
            d, _ = run(pool_for(m, allowed), n, m, label, sample,
                       dump=3 if allowed == {-1, 0, 1} else 0)
            bad += d
        print()
    print("forced states with a dead successor, everywhere: %d" % bad)


if __name__ == "__main__":
    main()
