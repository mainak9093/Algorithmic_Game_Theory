"""
Decomposing (AVOID-1ROW), and characterising the hard instances.

(AVOID-1ROW) asks for a partition into three bundles that at least TWO agents
each see as equal to within one, with the third within two. Two natural pieces:

  (TWO-BALANCE)  for some pair of agents, a partition exists giving BOTH of
                 them value spread <= 1;
  (THIRD)        on such a partition the remaining agent has spread <= 2.

If (TWO-BALANCE) always holds, it is a statement about two valuations only --
the three-agent structure drops out -- and that is exactly the shape a
discrepancy or consensus-splitting argument can attack. (THIRD) is then the
part that still couples all three.

Also measured: the "all three at spread <= 1" case is free (approach 18 section
6), so the hard instances are those where it fails. They are about 1% at m=3,
and this collects them to look for a common structure -- in particular whether
some agent must carry both a +1 and a -1 singleton, which would make the
one-item-each partition unusable for her.
"""
import itertools
import random
import sys

from gb_valuations import masks_by_popcount

N = 3


def random_gb(m, rng):
    v = [0] * (1 << m)
    for S in masks_by_popcount(m):
        if S == 0:
            continue
        bits = [1 << b for b in range(m) if S & (1 << b)]
        v[S] = rng.randint(max(v[S ^ b] for b in bits) - 1,
                           min(v[S ^ b] for b in bits) + 1)
    return tuple(v)


def spreads(vals, c):
    return [max(vals[i][c[j]] for j in range(N))
            - min(vals[i][c[j]] for j in range(N)) for i in range(N)]


def allocs_for(m):
    out = []
    for o in itertools.product(range(N), repeat=m):
        b = [0] * N
        for k, i in enumerate(o):
            b[i] |= 1 << k
        out.append(tuple(b))
    return out


def main():
    rng = random.Random(20260920)
    for m, trials in ((3, 4000), (4, 1000), (5, 250)):
        A = allocs_for(m)
        st = {"inst": 0, "all3": 0, "two": 0, "onerow": 0,
              "two_but_third_big": 0}
        hard_mixed = 0
        hard = 0
        for _ in range(trials):
            vals = [random_gb(m, rng) for _ in range(N)]
            st["inst"] += 1
            sp = [(c, spreads(vals, c)) for c in A]
            if any(max(s) <= 1 for c, s in sp):
                st["all3"] += 1
            else:
                hard += 1
                # does some agent carry both a +1 and a -1 singleton?
                for i in range(N):
                    sing = [vals[i][1 << k] for k in range(m)]
                    if 1 in sing and -1 in sing:
                        hard_mixed += 1
                        break
            # (TWO-BALANCE): some pair balanced to <= 1
            twob = [(c, s) for c, s in sp
                    if sum(1 for t in s if t <= 1) >= 2]
            if twob:
                st["two"] += 1
                if not any(max(s) <= 2 for c, s in twob):
                    st["two_but_third_big"] += 1
            # (AVOID-1ROW): two at <=1 and the third at <=2
            if any(sum(1 for t in s if t <= 1) >= 2 and max(s) <= 2
                   for c, s in sp):
                st["onerow"] += 1

        print("   m=%d (%d instances)" % (m, st["inst"]))
        print("      all three agents at spread <= 1 (free case) : %d"
              % st["all3"])
        print("      hard instances (that fails)                 : %d%s"
              % (hard, "   of which some agent has both a +1 and a -1 "
                       "singleton: %d" % hard_mixed if hard else ""))
        print("      (TWO-BALANCE) some pair at spread <= 1      : %d%s"
              % (st["two"], "" if st["two"] == st["inst"] else "   <-- FAILS"))
        print("      ... but no such partition has the third <=2 : %d"
              % st["two_but_third_big"])
        print("      (AVOID-1ROW) two at <=1 and third at <=2    : %d%s"
              % (st["onerow"],
                 "" if st["onerow"] == st["inst"] else "   <-- FAILS"))


if __name__ == "__main__":
    main()
