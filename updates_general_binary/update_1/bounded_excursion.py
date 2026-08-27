"""
Approach 15: testing the bounded-excursion conjecture directly.

The conjecture asks for an algorithm that keeps every intermediate allocation
valid and never lets the bundle-size spread exceed 2. That splits into two
questions, each decidable outright:

  (E1) EXISTENCE   is there a COMPLETE valid allocation with spread <= K?
  (E2) REACHABILITY  is such an allocation reachable from the empty one
                     through valid states that ALL have spread <= K?

(E2) implies (E1). Both are measured for K = 1 and K = 2. K = 1 is expected to
fail -- test_balance_invariant.py already found balanced states with no
balanced continuation -- and the whole point of the conjecture is that K = 2
does not.

A failure of (E1) at K = 2 would refute the conjecture outright and for a dull
reason (no target allocation of that shape exists). A failure of (E2) with (E1)
holding would be the interesting case: the right allocation exists but cannot
be built without a wider detour, which would say the bound 2 is simply the
wrong constant.

Both pure classes are run as controls. Balance is maintainable in each of them,
so both must pass at K = 1, and a failure there would indicate a bug rather
than a discovery.
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


def analyse(vals, n, m, perms, states, full_mask, K):
    """(E1, E2) for this instance at width K."""
    cache = {}

    def ok(s):
        if s not in cache:
            p = min_subsidy(vals, s)
            cache[s] = p is not None and all(q <= 1 for q in p)
        return cache[s]

    exists = any(allocated(s) == full_mask and spread(s) <= K and ok(s)
                 for s in states)
    if not exists:
        return False, False

    empty = tuple([0] * n)
    seen = {empty}
    queue = deque([empty])
    while queue:
        s = queue.popleft()
        if allocated(s) == full_mask:
            return True, True
        free = [k for k in range(m) if not allocated(s) & (1 << k)]
        for g in free:
            for x in range(n):
                grown = tuple(b | (1 << g) if i == x else b
                              for i, b in enumerate(s))
                if spread(grown) > K:
                    continue
                for perm in perms:
                    t = tuple(grown[perm[i]] for i in range(n))
                    if t not in seen and ok(t):
                        seen.add(t)
                        queue.append(t)
        for perm in perms:
            t = tuple(s[perm[i]] for i in range(n))
            if t not in seen and ok(t):
                seen.add(t)
                queue.append(t)
    return True, False


def run(pool, n, m, label, sample, seed=20260827):
    rng = random.Random(seed)
    perms = list(itertools.permutations(range(n)))
    states = all_partial(n, m)
    full_mask = (1 << m) - 1

    multisets = [tuple(sorted(rng.choice(pool) for _ in range(n)))
                 for _ in range(sample)]

    res = {}
    for K in (1, 2):
        e1 = e2 = 0
        w1 = w2 = None
        for vals in multisets:
            a, b = analyse(vals, n, m, perms, states, full_mask, K)
            e1 += a
            e2 += b
            if not a and w1 is None:
                w1 = vals
            if a and not b and w2 is None:
                w2 = vals
        res[K] = (e1, e2, w1, w2)

    print("  %-22s n=%d m=%d : %d instances" % (label, n, m, len(multisets)))
    for K in (1, 2):
        e1, e2, w1, w2 = res[K]
        print("     K=%d  complete alloc with spread<=K exists : %d/%d"
              % (K, e1, len(multisets)))
        print("          and reachable staying within K       : %d/%d"
              % (e2, len(multisets)))
        if w2 is not None:
            print("          witness: exists but NOT reachable within K:")
            for i, v in enumerate(w2):
                print("             agent %d %s" % (i + 1, str(v)))
        elif w1 is not None and K == 2:
            print("          witness: no complete allocation of spread<=2:")
            for i, v in enumerate(w1):
                print("             agent %d %s" % (i + 1, str(v)))
    return res


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
    print("Bounded-excursion conjecture: is spread <= 2 always enough?")
    print()
    plan = (((3, 3, 3000), (3, 4, 600)) if mode == "small"
            else ((4, 4, 250), (3, 5, 250)))
    for (n, m, sample) in plan:
        for label, allowed in CLASSES:
            run(pool_for(m, allowed), n, m, label, sample)
        print()


if __name__ == "__main__":
    main()
