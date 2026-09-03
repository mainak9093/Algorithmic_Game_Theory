"""
A necklace-splitting idea: can the three bundles be taken to be INTERVALS?

The two-bundle lemma (approach 19) works because a one-parameter walk through
partition space cannot jump: each step moves d = v(B_1) - v(B_2) by at most 2,
so it cannot skip [-1,1]. Three bundles need a TWO-parameter family, and there
is a canonical one that nothing in this project has used: fix a linear order on
the items and cut it into three consecutive blocks,

    B_1 = g_1..g_a,   B_2 = g_{a+1}..g_b,   B_3 = g_{b+1}..g_m,

for 0 <= a <= b <= m. The two cut positions are the two parameters, and moving
a cut by one step transfers ONE item between adjacent blocks, so two of the
three values change by at most 1 each. That is exactly the no-jump hypothesis a
Sperner or Tucker argument needs, and it is the discrete shape of necklace
splitting: one measure, three parts, two cuts.

The question this settles is whether the restriction costs anything:

    ANY-ORDER   for EVERY linear order, some interval 3-partition has
                spread <= 1   -- the strongest form, and what would make the
                argument order-free
    SOME-ORDER  for SOME order it does  -- still enough for a proof, since the
                order may be chosen after seeing v

There are only (m+1)(m+2)/2 interval partitions against 3^m in total -- 15
against 81 at m=4 -- so a positive answer is a large structural reduction as
well as a route to a proof.
"""
import itertools
import sys

from gb_valuations import enumerate_general_binary


def spread3(v, B):
    return max(v[b] for b in B) - min(v[b] for b in B)


def intervals(order, m):
    """Every cut of the given order into three consecutive blocks."""
    out = []
    for a in range(m + 1):
        for b in range(a, m + 1):
            B1 = 0
            for k in order[:a]:
                B1 |= 1 << k
            B2 = 0
            for k in order[a:b]:
                B2 |= 1 << k
            B3 = 0
            for k in order[b:]:
                B3 |= 1 << k
            out.append((B1, B2, B3))
    return out


def all_parts(m):
    out = []
    for o in itertools.product(range(3), repeat=m):
        b = [0, 0, 0]
        for k, i in enumerate(o):
            b[i] |= 1 << k
        out.append(tuple(b))
    return out


def main():
    for m in (3, 4):
        pool = list(enumerate_general_binary(m))
        orders = list(itertools.permutations(range(m)))
        ivs = {o: intervals(o, m) for o in orders}
        P = all_parts(m)
        n_any = n_some = n_bal = 0
        worst = None
        for v in pool:
            if any(spread3(v, c) <= 1 for c in P):
                n_bal += 1
            hits = [o for o in orders
                    if any(spread3(v, c) <= 1 for c in ivs[o])]
            if len(hits) == len(orders):
                n_any += 1
            if hits:
                n_some += 1
            elif worst is None:
                worst = v
        print("m=%d, ALL %d general binary valuations   (%d interval cuts per "
              "order, %d partitions in total)"
              % (m, len(pool), len(ivs[orders[0]]), len(P)))
        print("   (BAL-1) holds over all partitions      : %d / %d"
              % (n_bal, len(pool)))
        print("   ANY-ORDER  every order has a good cut  : %d / %d%s"
              % (n_any, len(pool),
                 "   <-- ORDER-FREE" if n_any == len(pool) else ""))
        print("   SOME-ORDER some order has a good cut   : %d / %d%s"
              % (n_some, len(pool),
                 "   <-- SUFFICES" if n_some == len(pool) else "   <-- FAILS"))
        if worst is not None:
            print("      a valuation with NO good interval cut in any order: %s"
                  % (worst,))
        print()


if __name__ == "__main__":
    main()
