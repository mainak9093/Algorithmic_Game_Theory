"""
A single-agent lemma that would give the arc-decrease half of case A.

In case A both agents rank A_2 at least 2 above A_1. Moving g from A_2 to A_1
changes agent 1's envy arc by

    w'(1,2) = v(A_2 - g) - v(A_1 + g)
            = w(1,2) - [ v(g | A_2 - g) + v(g | A_1) ],

so the arc drops by at least 1 exactly when the bracket is at least 1. Hence:

    (TRANSFER)  Let v be general binary, A_1 and A_2 disjoint, and
                v(A_2) >= v(A_1) + 2. Then some g in A_2 has
                v(g | A_2 - g) + v(g | A_1) >= 1.

This is a statement about ONE valuation and two disjoint sets -- no envy graph,
no third agent, no allocation -- so it is exhaustively checkable and, if true,
provable by hand. It is checked here over the whole general binary class for
every disjoint pair.

The gap threshold is swept too: the same statement with the hypothesis
v(A_2) >= v(A_1) + d for d = 1, 2, 3. If it fails at d = 1 but holds at d = 2
then the constant 2 -- which is exactly what Lemma 2 delivers -- is doing real
work, and that is worth knowing before trying to prove it.
"""
import itertools
import sys

from gb_valuations import enumerate_general_binary


def main():
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    pool = list(enumerate_general_binary(m))
    print("general binary on m=%d: %d valuations" % (m, len(pool)))

    pairs = []
    for a1 in range(1 << m):
        rest = ((1 << m) - 1) & ~a1
        s = rest
        while True:
            pairs.append((a1, s))
            if s == 0:
                break
            s = (s - 1) & rest
    print("disjoint (A_1, A_2) pairs: %d" % len(pairs))

    for d in (1, 2, 3):
        tested = viol = 0
        wit = None
        for v in pool:
            for (a1, a2) in pairs:
                if v[a2] - v[a1] < d:
                    continue
                tested += 1
                ok = False
                g = a2
                while g:
                    bit = g & -g
                    g ^= bit
                    mu = v[a2] - v[a2 ^ bit]          # v(g | A_2 - g)
                    nu = v[a1 | bit] - v[a1]          # v(g | A_1)
                    if mu + nu >= 1:
                        ok = True
                        break
                if not ok:
                    viol += 1
                    if wit is None:
                        wit = (v, a1, a2)
        print("   gap d=%d : %-9d hypotheses, %-7d violations%s"
              % (d, tested, viol, "   <-- (TRANSFER) HOLDS" if not viol else ""))
        if wit:
            v, a1, a2 = wit
            def show(x):
                return "{" + ",".join("abcd"[k] for k in range(m)
                                      if x & (1 << k)) + "}"
            print("      witness: A_1=%s v=%d  A_2=%s v=%d"
                  % (show(a1), v[a1], show(a2), v[a2]))
            g = a2
            while g:
                bit = g & -g
                g ^= bit
                print("         g=%s  v(g|A_2-g)=%d  v(g|A_1)=%d  sum=%d"
                      % (show(bit), v[a2] - v[a2 ^ bit], v[a1 | bit] - v[a1],
                         (v[a2] - v[a2 ^ bit]) + (v[a1 | bit] - v[a1])))


if __name__ == "__main__":
    main()
