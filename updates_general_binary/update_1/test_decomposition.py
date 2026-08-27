"""
Approach 15: audit of the signed-binary DECOMPOSITION LEMMA and a direct test
of the coupled target it is meant to serve.

THE LEMMA. For v with v(empty)=0 and every marginal in {-1,0,1}, set

    h(S) = (|S| - v(S)) / 2,   c(S) = floor(h(S)),   u(S) = v(S) + c(S).

Then c and u are both positive dichotomous (all marginals in {0,1}) and
v = u - c exactly. Part 1 below checks this on every valuation at m=3 and a
sample at m=4, so the lemma is confirmed by machine and not just on paper.

Part 1 also checks the two closed forms. c(S) = floor((|S|-v(S))/2) is the
definition. The companion form was stated as u(S) = ceil((|S|+v(S))/2), but
since v(S) is an integer,

    u(S) = v(S) + floor((|S|-v(S))/2) = floor((|S|+v(S))/2),

a FLOOR, and the two disagree exactly when |S|+v(S) is odd -- e.g. |S|=3,
v(S)=0 gives u=1 but ceil(3/2)=2. Part 1 counts the disagreements.

THE COUPLED TARGET. The bridge is: if one allocation A carries a goods
certificate q for u and a chores certificate r for c, then p = q + r is a valid
subsidy for v. Naively p in {0,1,2}, so the bridge is only useful if some
allocation achieves q_i + r_i <= 1 for every i.

Part 2 tests exactly that, and the test is exact rather than heuristic. By
Halpern-Shah, the minimal certificates q*, r* are pointwise below every valid
certificate, so

    some valid (q, r) has q_i + r_i <= 1 for all i
      <=>  the minimal ones do.

So for each instance we ask whether ANY complete allocation is envy-freeable
for u and for c simultaneously with max_i (q*_i + r*_i) <= 1, and compare that
against the direct question, whether any allocation gives max_i p*_i <= 1 for v
itself. The gap between the two columns is the cost of routing through the
decomposition.
"""
import itertools
import random
import sys

from gb_valuations import (
    enumerate_general_binary,
    arc_weights,
    is_envy_freeable,
    longest_paths,
    bundles_from_assignment,
    complete_assignments,
)


def popcount(S):
    return bin(S).count("1")


def decompose(v, m):
    """c(S) = floor((|S|-v(S))/2), u(S) = v(S) + c(S)."""
    c = [ (popcount(S) - v[S]) // 2 for S in range(1 << m) ]
    u = [ v[S] + c[S] for S in range(1 << m) ]
    return tuple(u), tuple(c)


def marginals(v, m):
    out = []
    for S in range(1 << m):
        for b in range(m):
            bit = 1 << b
            if not S & bit:
                out.append(v[S | bit] - v[S])
    return out


def check_lemma(pool, m, label):
    bad_c = bad_u = bad_id = bad_zero = 0
    ceil_disagree = 0
    for v in pool:
        u, c = decompose(v, m)
        if any(d not in (0, 1) for d in marginals(c, m)):
            bad_c += 1
        if any(d not in (0, 1) for d in marginals(u, m)):
            bad_u += 1
        if any(u[S] - c[S] != v[S] for S in range(1 << m)):
            bad_id += 1
        if u[0] != 0 or c[0] != 0:
            bad_zero += 1
        for S in range(1 << m):
            num = popcount(S) + v[S]
            ceil_val = -((-num) // 2)
            if ceil_val != u[S]:
                ceil_disagree += 1
                break
    n = len(pool)
    print("  %-28s %d valuations" % (label, n))
    print("     c positive dichotomous  : %d violations" % bad_c)
    print("     u positive dichotomous  : %d violations" % bad_u)
    print("     v = u - c               : %d violations" % bad_id)
    print("     u(empty)=c(empty)=0     : %d violations" % bad_zero)
    print("     valuations where ceil((|S|+v)/2) != u : %d of %d"
          % (ceil_disagree, n))


def min_subsidy(vals, bundles):
    if not is_envy_freeable(vals, bundles):
        return None
    return longest_paths(arc_weights(vals, bundles))


def direct_ok(vals, n, m):
    """Some allocation gives max_i p*_i <= 1 for v itself."""
    for assign in complete_assignments(n, m):
        b = bundles_from_assignment(assign, n, m)
        p = min_subsidy(vals, b)
        if p is not None and max(p) <= 1:
            return True
    return False


def bridge_ok(us, negcs, n, m):
    """
    Some allocation is envy-freeable for u and for c at once, with
    max_i (q*_i + r*_i) <= 1. `negcs` holds -c, since the chores certificate is
    the subsidy of the valuation -c.
    """
    for assign in complete_assignments(n, m):
        b = bundles_from_assignment(assign, n, m)
        q = min_subsidy(us, b)
        if q is None:
            continue
        r = min_subsidy(negcs, b)
        if r is None:
            continue
        if all(q[i] + r[i] <= 1 for i in range(n)):
            return True
    return False


def test_bridge(pool, n, m, label, sample=None, seed=20260827):
    rng = random.Random(seed)
    decomp = {}
    for v in pool:
        u, c = decompose(v, m)
        decomp[v] = (u, tuple(-x for x in c))

    multisets = itertools.combinations_with_replacement(pool, n)
    if sample is not None:
        multisets = list(multisets)
        if len(multisets) > sample:
            multisets = rng.sample(multisets, sample)

    total = direct = bridge = both = 0
    witness = None
    for vals in multisets:
        total += 1
        d = direct_ok(vals, n, m)
        us = tuple(decomp[v][0] for v in vals)
        ncs = tuple(decomp[v][1] for v in vals)
        b = bridge_ok(us, ncs, n, m)
        direct += d
        bridge += b
        both += (d and b)
        if d and not b and witness is None:
            witness = vals

    print("  %-20s n=%d m=%d : %d instances" % (label, n, m, total))
    print("     conjecture satisfied directly (max p* <= 1) : %d (%.1f%%)"
          % (direct, 100.0 * direct / total))
    print("     reachable through the decomposition bridge  : %d (%.1f%%)"
          % (bridge, 100.0 * bridge / total))
    print("     bridge LOSES these instances                : %d"
          % (direct - both))
    if witness is not None:
        print("     first instance the bridge cannot reach:")
        for i, v in enumerate(witness):
            u, c = decompose(v, m)
            print("        agent %d  v=%s" % (i + 1, str(v)))
            print("                 u=%s  c=%s" % (str(u), str(c)))


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    print("PART 1 -- the decomposition lemma")
    print()
    pool3 = list(enumerate_general_binary(3))
    check_lemma(pool3, 3, "m=3, exhaustive")
    rng = random.Random(20260827)
    pool4 = list(enumerate_general_binary(4))
    check_lemma(rng.sample(pool4, 20000), 4, "m=4, 20000 sampled")
    print()

    if mode == "lemma":
        return

    print("PART 2 -- the coupled target q_i + r_i <= 1")
    print()
    for (n, m, sample) in ((2, 2, None), (2, 3, 20000), (3, 3, 8000)):
        pool = list(enumerate_general_binary(m))
        test_bridge(pool, n, m, "general {-1,0,1}", sample=sample)
        print()


if __name__ == "__main__":
    main()
