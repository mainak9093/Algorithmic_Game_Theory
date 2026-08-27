"""
Approach 15: how far must an algorithm leave balance?

Where things stand. Every dead state is unbalanced (spread >= 2) and has no +1
move; equivalently, BALANCED or PLUS implies SAFE, with zero counterexamples in
over 1.5 million valid states. But balance is not maintainable in mixed
instances: there are valid balanced states from which every legal move breaks
balance (81 of 34226 at n=3, m=3; zero in both pure classes).

Note that "balanced implies safe" is not a stepping stone to the conjecture --
it IS the conjecture and then some, because the empty allocation is balanced,
so safety of balanced states already yields a complete valid allocation. That
is the point: it is a STRENGTHENED form with an inductive shape, which is the
usual way to get an induction through when the bare statement resists it.

For that strengthening to be usable the excursions away from balance have to be
controlled. This script measures them. From each valid balanced state that
cannot stay balanced, it computes

    EXCURSION DEPTH = the least number of moves needed to get back to a
                      balanced state (0 if some move is already balanced),

and the largest spread encountered along the way. If depth is always 1 and the
spread never exceeds 2, the invariant becomes "spread <= 2, and balanced after
every second insertion", which is a clean thing to try to prove. If depths are
unbounded, the balance framing is the wrong handle and should be abandoned.
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


def build(vals, n, m, perms, states):
    pmap = {}
    for s in states:
        p = min_subsidy(vals, s)
        if p is not None and all(q <= 1 for q in p):
            pmap[s] = p
    valid = set(pmap)
    succ = {}
    for s in valid:
        free = [k for k in range(m) if not allocated(s) & (1 << k)]
        out = []
        for g in free:
            for x in range(n):
                grown = tuple(b | (1 << g) if i == x else b
                              for i, b in enumerate(s))
                for perm in perms:
                    t = tuple(grown[perm[i]] for i in range(n))
                    if t in valid:
                        out.append(t)
        succ[s] = out          # insertion moves only; permutations do not
    return valid, succ         # change sizes, so they cannot restore balance


def excursion(s, succ, full_mask):
    """
    Least number of insertions from s to reach a balanced state again, and the
    worst spread on that path. Returns (depth, worst_spread) or None if no
    balanced state is ever reachable.
    """
    seen = {s}
    frontier = [(s, 0, spread(s))]
    completed = False
    while frontier:
        nxt = []
        for state, d, worst in frontier:
            for t in succ[state]:
                if t in seen:
                    continue
                seen.add(t)
                w = max(worst, spread(t))
                if spread(t) <= 1:
                    return d + 1, w, "balanced again"
                if allocated(t) == full_mask:
                    # A complete valid allocation is a SUCCESS even though it
                    # is unbalanced; it must not be scored as a dead end.
                    completed = True
                    continue
                nxt.append((t, d + 1, w))
        frontier = nxt
    return None, None, ("completed while unbalanced" if completed
                        else "dead end")


def run(pool, n, m, label, sample, seed=20260827):
    rng = random.Random(seed)
    perms = list(itertools.permutations(range(n)))
    states = all_partial(n, m)
    full_mask = (1 << m) - 1

    multisets = (tuple(sorted(rng.choice(pool) for _ in range(n)))
                 for _ in range(sample))

    forced = 0
    depths = {}
    worst_spread = 0
    outcomes = {}

    for vals in multisets:
        valid, succ = build(vals, n, m, perms, states)
        for s in valid:
            if spread(s) > 1 or allocated(s) == full_mask:
                continue
            ins = [t for t in succ[s] if allocated(t) != allocated(s)]
            if not ins:
                continue
            if any(spread(t) <= 1 for t in ins):
                continue                      # balance can be kept here
            forced += 1
            d, w, how = excursion(s, succ, full_mask)
            outcomes[how] = outcomes.get(how, 0) + 1
            if d is None:
                continue
            depths[d] = depths.get(d, 0) + 1
            worst_spread = max(worst_spread, w)

    print("  %-22s n=%d m=%d : %d forced excursions" % (label, n, m, forced))
    if forced:
        print("       depth distribution : %s"
              % ", ".join("%d moves: %d" % (d, c)
                          for d, c in sorted(depths.items())))
        print("       worst spread seen  : %d" % worst_spread)
        for how, c in sorted(outcomes.items()):
            print("       outcome: %-28s %d" % (how, c))
    return forced, worst_spread


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
    print("Forced excursions away from balance: how deep, how wide?")
    print()
    for (n, m, sample) in ((3, 3, 4000), (3, 4, 700)):
        for label, allowed in CLASSES:
            run(pool_for(m, allowed), n, m, label, sample)
        print()


if __name__ == "__main__":
    main()
