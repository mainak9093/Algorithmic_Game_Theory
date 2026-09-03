"""
A matching reformulation of validity, and a test of it.

Halpern-Shah says (A, p) is envy-free exactly when v_i(A_i) + p_i >= v_i(A_j) +
p_j for all i, j. Reading p as a PRICE attached to the bundle rather than to
the agent, that says precisely: every agent holds a bundle maximising
v_i(B) + q_B. So, for a fixed multiset of bundles:

    A multiset B = {B_1, ..., B_n} admits a valid assignment
      <=>
    there is a set Q of positions (the subsidised bundles) such that the
    DEMAND GRAPH -- agent i joined to every position maximising v_i(B_j) + q_j,
    with q_j = 1 iff j in Q -- has a perfect matching.

This removes envy graphs, longest paths and the assignment from the statement
entirely: validity of a bundle multiset becomes a Hall condition. This script
checks the equivalence against the envy-graph implementation on every balanced
allocation of the chores class, so that nothing downstream rests on it
untested.
"""
import itertools
import sys

from gb_valuations import (
    enumerate_class,
    arc_weights,
    is_envy_freeable,
    longest_paths,
)


def valid(vals, b):
    if not is_envy_freeable(vals, b):
        return False
    return all(q <= 1 for q in longest_paths(arc_weights(vals, b)))


def good_by_envygraph(vals, bundles, n):
    """Some assignment of these bundles to the agents is valid."""
    for perm in itertools.permutations(range(n)):
        if valid(vals, tuple(bundles[perm[i]] for i in range(n))):
            return True
    return False


def perfect_matching(adj, n):
    """Hopcroft-Karp is overkill at n <= 6; plain augmenting paths."""
    match = [-1] * n                      # position -> agent
    def try_assign(i, seen):
        for j in adj[i]:
            if not seen[j]:
                seen[j] = True
                if match[j] == -1 or try_assign(match[j], seen):
                    match[j] = i
                    return True
        return False
    count = 0
    for i in range(n):
        if try_assign(i, [False] * n):
            count += 1
    return count == n


def good_by_demand(vals, bundles, n):
    """Some price set Q in {0,1}^n makes the demand graph perfectly matchable."""
    for Qmask in range(1 << n):
        q = [(Qmask >> j) & 1 for j in range(n)]
        adj = []
        for i in range(n):
            score = [vals[i][bundles[j]] + q[j] for j in range(n)]
            top = max(score)
            adj.append([j for j in range(n) if score[j] == top])
        if perfect_matching(adj, n):
            return True
    return False


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    m = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    pool = enumerate_class(m, {-1, 0})
    print("chores valuations on m=%d: %d, tuples: %d"
          % (len(pool), m, len(pool) ** n))

    checked = agree = mismatch = both_good = 0
    bad = []
    for vals in itertools.product(pool, repeat=n):
        vals = list(vals)
        for assign in itertools.product(list(range(n)) + [None], repeat=m):
            b = [0] * n
            for k, owner in enumerate(assign):
                if owner is not None:
                    b[owner] |= 1 << k
            b = tuple(b)
            s = [bin(x).count("1") for x in b]
            if max(s) - min(s) > 1:
                continue
            checked += 1
            g1 = good_by_envygraph(vals, b, n)
            g2 = good_by_demand(vals, b, n)
            if g1 == g2:
                agree += 1
                both_good += 1 if g1 else 0
            else:
                mismatch += 1
                if len(bad) < 3:
                    bad.append((vals, b, g1, g2))
    print()
    print("balanced bundle multisets checked : %d" % checked)
    print("   the two definitions agree      : %d" % agree)
    print("   of those, good                 : %d" % both_good)
    print("   MISMATCHES                     : %d" % mismatch)
    for w in bad:
        print("   vals=%s bundles=%s envygraph=%s demand=%s" % w)


if __name__ == "__main__":
    main()
