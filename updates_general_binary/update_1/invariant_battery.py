"""
Approach 15: which invariant makes the incremental architecture close?

The architecture needs a predicate PHI on valid partial allocations with

    (i)   the empty allocation satisfies PHI;
    (ii)  SAFE-SUFFICIENT: no PHI state is dead (dead = cannot reach any
          complete valid state by adding items and reassigning bundles);
    (iii) MAINTAINABLE: from every PHI state with an unallocated item there is
          a move to another PHI state.

"Safe" itself trivially satisfies all three but is not checkable, so the point
is to find a PHI that is. This script measures (ii) and (iii) for a battery of
candidates on the same instances, per class, so the goods and chores columns
act as controls: whatever the true invariant is, it must hold in both pure
classes, since both theorems are true there.

Candidates, each suggested by an earlier finding:

  BAL      spread = max|A_i| - min|A_i| <= 1. analyse_safe.py found every dead
           state has spread >= 2.
  PLUS     some unallocated item has a +1 marginal for some agent at some
           current bundle -- the hypothesis under which fact A gives a safe
           insertion.
  BAL_OR_PLUS   the disjunction: balanced, or a +1 move is available.
  NOFAT    no bundle exceeds the ceiling of the average, |A_i| <= ceil(k/n)
           for k allocated items -- a one-sided version of balance.
  PAID_BIG every agent paid 1 holds a maximum-size bundle. In the dead
           witnesses the paid agent is the one carrying the overloaded bundle,
           so this asks whether that configuration is the real culprit.
"""
import itertools
import math
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


def sizes(bundles):
    return [bin(b).count("1") for b in bundles]


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


def has_plus_one(vals, bundles, n, m):
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


# ------------------------------ the candidates ----------------------------

def phi_bal(vals, s, p, n, m):
    z = sizes(s)
    return max(z) - min(z) <= 1


def phi_plus(vals, s, p, n, m):
    return has_plus_one(vals, s, n, m)


def phi_bal_or_plus(vals, s, p, n, m):
    return phi_bal(vals, s, p, n, m) or phi_plus(vals, s, p, n, m)


def phi_nofat(vals, s, p, n, m):
    z = sizes(s)
    k = sum(z)
    return max(z) <= math.ceil(k / n)


def phi_paid_big(vals, s, p, n, m):
    z = sizes(s)
    top = max(z)
    return all(z[i] == top for i in range(n) if p[i] == 1)


CANDIDATES = (
    ("BAL", phi_bal),
    ("PLUS", phi_plus),
    ("BAL_OR_PLUS", phi_bal_or_plus),
    ("NOFAT", phi_nofat),
    ("PAID_BIG", phi_paid_big),
)


def analyse_instance(vals, n, m, perms, states, full_mask):
    pmap = {}
    for s in states:
        p = min_subsidy(vals, s)
        if p is not None and all(q <= 1 for q in p):
            pmap[s] = p
    valid_states = set(pmap)

    succ = {}
    for s in valid_states:
        free = [k for k in range(m) if not allocated(s) & (1 << k)]
        out = []
        for g in free:
            for x in range(n):
                grown = tuple(b | (1 << g) if i == x else b
                              for i, b in enumerate(s))
                for perm in perms:
                    t = tuple(grown[perm[i]] for i in range(n))
                    if t in valid_states:
                        out.append(t)
        for perm in perms:
            t = tuple(s[perm[i]] for i in range(n))
            if t != s and t in valid_states:
                out.append(t)
        succ[s] = out

    safe = {s for s in valid_states if allocated(s) == full_mask}
    changed = True
    while changed:
        changed = False
        for s in valid_states:
            if s not in safe and any(t in safe for t in succ[s]):
                safe.add(s)
                changed = True
    return pmap, valid_states, safe, succ


def run(pool, n, m, label, sample=None, seed=20260827):
    rng = random.Random(seed)
    perms = list(itertools.permutations(range(n)))
    states = all_partial(n, m)
    full_mask = (1 << m) - 1

    multisets = itertools.combinations_with_replacement(pool, n)
    if sample is not None:
        multisets = list(multisets)
        if len(multisets) > sample:
            multisets = rng.sample(multisets, sample)

    unsafe_hits = {name: 0 for name, _ in CANDIDATES}
    unmaint_hits = {name: 0 for name, _ in CANDIDATES}
    holds = {name: 0 for name, _ in CANDIDATES}

    for vals in multisets:
        pmap, valid_states, safe, succ = analyse_instance(
            vals, n, m, perms, states, full_mask)
        for s in valid_states:
            p = pmap[s]
            incomplete = allocated(s) != full_mask
            for name, phi in CANDIDATES:
                if not phi(vals, s, p, n, m):
                    continue
                holds[name] += 1
                if s not in safe:
                    unsafe_hits[name] += 1
                if incomplete:
                    moved = any(
                        allocated(t) != allocated(s)
                        and phi(vals, t, pmap[t], n, m)
                        for t in succ[s])
                    if not moved:
                        unmaint_hits[name] += 1

    print("  %s  n=%d m=%d" % (label, n, m))
    print("     %-13s %10s %12s %14s"
          % ("candidate", "states", "dead ones", "no PHI-move"))
    for name, _ in CANDIDATES:
        print("     %-13s %10d %12d %14d"
              % (name, holds[name], unsafe_hits[name], unmaint_hits[name]))
    return {name: (unsafe_hits[name], unmaint_hits[name])
            for name, _ in CANDIDATES}


CLASSES = (
    ("control goods {0,1} ", {0, 1}),
    ("control chores{-1,0}", {-1, 0}),
    ("general  {-1,0,1}   ", {-1, 0, 1}),
)


def pool_for(m, allowed):
    if allowed == {-1, 0, 1}:
        return list(enumerate_general_binary(m))
    return enumerate_class(m, allowed)


def main():
    print("Invariant battery: safe-sufficiency and maintainability")
    print("(a candidate that closes the argument needs 0 in BOTH columns,")
    print(" in every class)")
    print()

    totals = {name: [0, 0] for name, _ in CANDIDATES}
    for (n, m, sample) in ((3, 3, 2500), (3, 4, 400)):
        for label, allowed in CLASSES:
            res = run(pool_for(m, allowed), n, m, label, sample=sample)
            for name in totals:
                totals[name][0] += res[name][0]
                totals[name][1] += res[name][1]
            print()

    print("TOTALS across all classes and sizes")
    print("     %-13s %12s %14s" % ("candidate", "dead ones", "no PHI-move"))
    for name, _ in CANDIDATES:
        u, mn = totals[name]
        verdict = "CLOSES" if (u == 0 and mn == 0) else ""
        print("     %-13s %12d %14d   %s" % (name, u, mn, verdict))


if __name__ == "__main__":
    main()
