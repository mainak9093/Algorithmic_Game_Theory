"""
Approach 15: (SR+), the steering rule with a minimum-bundle tie-break.

forced_states.py refuted the clean reduction of (SR-forced). Call a valid
incomplete state FORCED when it has valid successors but no valid BALANCED
one. It is not true that a forced state has only safe successors: 957 forced
states at chores n=3,m=4 and 362 at n=4,m=4 have a DEAD successor. So (SR) as
stated leaves a real choice at forced states, and that choice can be fatal.

But the same sweep found something sharp. Among every one of those forced
states, the successors obtained by inserting into a MINIMUM-SIZE bundle were
never dead -- 0 out of all of them, in every class and at every size. That is
the missing tie-break, and it is exactly the dual of BKNS's rule: goods go to
a maximally subsidised agent, chores go to the emptiest bundle.

    (SR+)  From a valid state:
             (1) if some move lands on a valid BALANCED state, take one;
             (2) else if some valid move inserts into a MINIMUM-SIZE bundle,
                 take one of those;
             (3) else take any valid move.

Step (1) is safe because no balanced state is dead (Fact F). Step (2) is the
new content. Step (3) is a fallback that should ideally never fire.

This script measures, in the strong form that a proof would need:

    (SR+ forced)  does EVERY maximal (SR+)-run end complete?
    step (3) usage  how often is the fallback reached at all?
    step (2) safety does a step-(2) move ever land on a dead state?

If (SR+ forced) holds and step (3) never fires, the rule is a complete
deterministic algorithm modulo which balanced or minimum-bundle move is taken,
and the conjecture becomes a statement about two clean cases.
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


def valid_p(vals, b):
    if not is_envy_freeable(vals, b):
        return None
    p = longest_paths(arc_weights(vals, b))
    return p if all(q <= 1 for q in p) else None


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


def moves(vals, s, n, m, perms, cache):
    """(successor, grew_a_minimum_bundle) for every valid landing."""
    out = []
    free = [k for k in range(m) if not allocated(s) & (1 << k)]
    z = sizes(s)
    lo = min(z)
    for g in free:
        for x in range(n):
            grown = tuple(y | (1 << g) if i == x else y
                          for i, y in enumerate(s))
            for perm in perms:
                t = tuple(grown[perm[i]] for i in range(n))
                if t not in cache:
                    cache[t] = valid_p(vals, t) is not None
                if cache[t]:
                    out.append((t, z[x] == lo))
    return out


def sr_plus(vals, s, n, m, perms, cache):
    """Returns (successors, which_step)."""
    mv = moves(vals, s, n, m, perms, cache)
    if not mv:
        return [], 0
    bal = [t for t, _ in mv if spread(t) <= 1]
    if bal:
        return bal, 1
    mins = [t for t, ismin in mv if ismin]
    if mins:
        return mins, 2
    return [t for t, _ in mv], 3


def analyse(vals, n, m, perms):
    cache = {}
    full = (1 << m) - 1
    empty = tuple([0] * n)
    if valid_p(vals, empty) is None:
        return None
    seen = {empty}
    q = deque([empty])
    dead_ends = 0
    step_use = {1: 0, 2: 0, 3: 0}
    step2_dead = 0
    while q:
        s = q.popleft()
        if allocated(s) == full:
            continue
        succ, step = sr_plus(vals, s, n, m, perms, cache)
        if not succ:
            dead_ends += 1
            continue
        step_use[step] += 1
        if step == 2:
            for t in succ:
                nxt, _ = sr_plus(vals, t, n, m, perms, cache)
                if not nxt and allocated(t) != full:
                    step2_dead += 1
        for t in succ:
            if t not in seen:
                seen.add(t)
                q.append(t)
    return dead_ends, step_use, step2_dead


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
    print("(SR+): balanced first, then minimum-size bundle, then anything")
    print()
    rng = random.Random(20260827)
    total_dead = 0
    for (n, m, sample) in ((3, 3, 5000), (3, 4, 800), (4, 4, 400)):
        for label, allowed in CLASSES:
            pool = pool_for(m, allowed)
            perms = list(itertools.permutations(range(n)))
            inst = de = s2d = 0
            use = {1: 0, 2: 0, 3: 0}
            for _ in range(sample):
                vals = tuple(rng.choice(pool) for _ in range(n))
                r = analyse(vals, n, m, perms)
                if r is None:
                    continue
                inst += 1
                d, su, s2 = r
                de += d
                s2d += s2
                for k in use:
                    use[k] += su[k]
            total_dead += de
            print("  %-18s n=%d m=%d : %d instances" % (label, n, m, inst))
            print("     (SR+ forced) dead ends        : %d" % de)
            print("     steps used  balanced/min/any  : %d / %d / %d"
                  % (use[1], use[2], use[3]))
            print("     step-(2) moves landing dead   : %d" % s2d)
        print()
    print("total (SR+) dead ends everywhere: %d" % total_dead)


if __name__ == "__main__":
    main()
