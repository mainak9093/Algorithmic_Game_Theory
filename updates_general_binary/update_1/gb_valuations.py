"""
Approach 15, shared machinery: enumerate general binary valuations and compute
the Halpern-Shah quantities on them. Imported by the other scripts in this
folder; running it directly prints the size of the valuation class for small m
together with the m=2 hand count, as a sanity check on the enumerator.

A general binary valuation on m items is a map v : 2^[m] -> Z with v(empty)=0
and every marginal v(S + g) - v(S) in {-1,0,1}. We store one as a tuple of
length 2^m indexed by bitmask.

Enumeration. Process masks in order of increasing popcount. For a mask S with
bits b_1..b_k, the value v(S) is constrained by each single-bit deletion:

    v(S) - v(S - b) in {-1,0,1}   for every b in S,

so v(S) ranges over the intersection of [v(S-b)-1, v(S-b)+1] over all b in S.
That intersection is [max_b v(S-b) - 1, min_b v(S-b) + 1], which may be empty.
Every valuation is generated exactly once, since the value at each mask is
chosen once, in a fixed order.

Hand check at m=2. With v(a), v(b) each in {-1,0,1}, the number of admissible
v(ab) is 3 - |v(a) - v(b)| when that is positive. Summing over the 9 pairs:
3 pairs with |diff|=0 give 3 each, 4 pairs with |diff|=1 give 2 each, 2 pairs
with |diff|=2 give 1 each, so 9 + 8 + 2 = 19. The enumerator must report 19.

Envy-freeability. We use Halpern-Shah condition (ii) directly -- an allocation
is envy-freeable iff no reassignment of its own bundles among the agents raises
utilitarian welfare -- because for the n <= 4 used here checking all n!
permutations is exact and needs no cycle machinery. The minimal subsidy is
p*_i = l_A(i), the maximum weight of a directed path in the envy graph starting
at i (the empty path, of weight 0, included), computed by enumerating simple
paths; that is exact for these n and sidesteps any positive-cycle subtlety.
"""
import itertools
from functools import lru_cache


# --------------------------------------------------------------------------
# Valuation enumeration
# --------------------------------------------------------------------------

def masks_by_popcount(m):
    """All masks over m items, ordered by |S| then numerically."""
    return sorted(range(1 << m), key=lambda s: (bin(s).count("1"), s))


def enumerate_general_binary(m):
    """Every general binary valuation on m items, as a tuple indexed by mask."""
    order = [s for s in masks_by_popcount(m) if s != 0]
    values = [0] * (1 << m)          # values[0] = v(empty) = 0

    def rec(idx):
        if idx == len(order):
            yield tuple(values)
            return
        S = order[idx]
        bits = [1 << b for b in range(m) if S & (1 << b)]
        lo = max(values[S ^ b] for b in bits) - 1
        hi = min(values[S ^ b] for b in bits) + 1
        for val in range(lo, hi + 1):
            values[S] = val
            yield from rec(idx + 1)
        values[S] = 0

    yield from rec(0)


def marginals_within(v, m, allowed):
    """True iff every marginal of v lies in `allowed` (a set of ints)."""
    for S in range(1 << m):
        for b in range(m):
            bit = 1 << b
            if not S & bit:
                if v[S | bit] - v[S] not in allowed:
                    return False
    return True


def enumerate_class(m, allowed):
    """General binary valuations whose marginals all lie in `allowed`."""
    return [v for v in enumerate_general_binary(m)
            if marginals_within(v, m, allowed)]


# --------------------------------------------------------------------------
# Allocations and the envy graph
# --------------------------------------------------------------------------

def bundles_from_assignment(assign, n, m):
    """assign[k] = agent holding item k, or None if item k is unallocated."""
    b = [0] * n
    for k, owner in enumerate(assign):
        if owner is not None:
            b[owner] |= 1 << k
    return tuple(b)


def complete_assignments(n, m):
    """Every complete allocation of m items to n agents, as an owner tuple."""
    return itertools.product(range(n), repeat=m)


def partial_assignments(n, m):
    """Every partial allocation: each item to an agent, or unallocated."""
    return itertools.product(list(range(n)) + [None], repeat=m)


def arc_weights(vals, bundles):
    """w[i][j] = v_i(A_j) - v_i(A_i)."""
    n = len(bundles)
    return [[vals[i][bundles[j]] - vals[i][bundles[i]] for j in range(n)]
            for i in range(n)]


def is_envy_freeable(vals, bundles):
    """Halpern-Shah (ii): no reassignment of these bundles raises welfare."""
    n = len(bundles)
    base = sum(vals[i][bundles[i]] for i in range(n))
    for perm in itertools.permutations(range(n)):
        if sum(vals[i][bundles[perm[i]]] for i in range(n)) > base:
            return False
    return True


def longest_paths(w):
    """
    l(i) for every i: the maximum weight of a simple directed path starting at
    i in the envy graph, the empty path (weight 0) included. Only called on
    envy-freeable allocations, where no positive cycle exists and the maximum
    over walks is attained by a simple path.
    """
    n = len(w)
    best = [0] * n

    def walk(start, current, visited, weight):
        if weight > best[start]:
            best[start] = weight
        for j in range(n):
            if j != current and not visited & (1 << j):
                walk(start, j, visited | (1 << j), weight + w[current][j])

    for i in range(n):
        walk(i, i, 1 << i, 0)
    return best


def min_subsidy(vals, bundles):
    """
    The minimal subsidy vector of an allocation, or None if it is not
    envy-freeable.
    """
    if not is_envy_freeable(vals, bundles):
        return None
    return longest_paths(arc_weights(vals, bundles))


def best_over_allocations(vals, n, m):
    """
    min over complete allocations of max_i p*_i, together with a witnessing
    allocation. Returns (value, assignment). Value is None if no complete
    allocation is envy-freeable, which cannot happen (a welfare-maximising
    allocation always is) but is reported rather than assumed.
    """
    best, best_assign = None, None
    for assign in complete_assignments(n, m):
        bundles = bundles_from_assignment(assign, n, m)
        p = min_subsidy(vals, bundles)
        if p is None:
            continue
        worst = max(p)
        if best is None or worst < best:
            best, best_assign = worst, assign
            if best == 0:
                break
    return best, best_assign


# --------------------------------------------------------------------------

def main():
    print("General binary valuations (all marginals in {-1,0,1})")
    print()
    print("  m | count")
    print("  --+------")
    for m in range(1, 5):
        count = sum(1 for _ in enumerate_general_binary(m))
        print("  %d | %d" % (m, count))

    m2 = sum(1 for _ in enumerate_general_binary(2))
    print()
    print("m=2 hand count is 19; enumerator reports %d -> %s"
          % (m2, "OK" if m2 == 19 else "MISMATCH"))

    print()
    print("Sub-classes at m=3:")
    for name, allowed in (("goods only   {0,1}", {0, 1}),
                          ("chores only {-1,0}", {-1, 0}),
                          ("general  {-1,0,1}", {-1, 0, 1})):
        print("  %s : %d" % (name, len(enumerate_class(3, allowed))))


if __name__ == "__main__":
    main()
