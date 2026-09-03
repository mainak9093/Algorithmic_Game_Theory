"""
(TRANSFER) two-sided: the arc can always be shrunk from one end or the other.

transfer_lemma.py refutes the one-directional version, and every witness has
A_2 empty -- there is simply no item to move that way. The move has to be
allowed in both directions, which is what (PAIR) says anyway. Writing
w = v(A_2) - v(A_1) for the gap:

  moving g from A_2 to A_1:  w' = w - [ v(g | A_2 - g) + v(g | A_1) ]
  moving h from A_1 to A_2:  w' = w + [ v(h | A_2) + v(h | A_1 - h) ]

so the gap drops by at least one exactly when some g has the first bracket
>= 1, or some h has the second <= -1. Hence:

  (TRANSFER-2)  Let v be general binary, A_1 and A_2 disjoint, and
                v(A_2) >= v(A_1) + 2. Then some g in A_2 has
                v(g | A_2 - g) + v(g | A_1) >= 1, or some h in A_1 has
                v(h | A_2) + v(h | A_1 - h) <= -1.

Lemma 3 says |A_1| + |A_2| >= 2 whenever the gap is at least 2, so at least one
of the two quantifiers ranges over a non-empty set and the statement is not
vacuous. Checked exhaustively over the whole class, and swept over the gap
threshold to see whether the constant 2 is what makes it work.
"""
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

    def show(x):
        return "{" + ",".join("abcd"[k] for k in range(m)
                              if x & (1 << k)) + "}"

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
                while g and not ok:
                    bit = g & -g
                    g ^= bit
                    if (v[a2] - v[a2 ^ bit]) + (v[a1 | bit] - v[a1]) >= 1:
                        ok = True
                h = a1
                while h and not ok:
                    bit = h & -h
                    h ^= bit
                    if (v[a2 | bit] - v[a2]) + (v[a1] - v[a1 ^ bit]) <= -1:
                        ok = True
                if not ok:
                    viol += 1
                    if wit is None:
                        wit = (v, a1, a2)
        print("   gap d=%d : %-9d hypotheses, %-7d violations%s"
              % (d, tested, viol,
                 "   <-- (TRANSFER-2) HOLDS" if not viol else ""))
        if wit:
            v, a1, a2 = wit
            print("      witness: A_1=%s v=%d   A_2=%s v=%d   gap=%d"
                  % (show(a1), v[a1], show(a2), v[a2], v[a2] - v[a1]))


if __name__ == "__main__":
    main()
