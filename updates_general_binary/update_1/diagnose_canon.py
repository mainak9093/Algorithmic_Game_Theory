"""
How much did the refutation of (CANON) actually kill?

hunt_canon3.py found instances where EVERY leximin-optimal welfare maximiser of
the spread-<=2 family is invalid. That refutes the canonical object proposed in
approach 16, but it does not say how deep the damage goes. Three nested
questions, from least to most serious:

  Q1  is some WELFARE MAXIMISER of the family valid?
        no  -> welfare maximisation is the wrong primary criterion, not just
               leximin the wrong tie-break
  Q2  is some allocation of the spread-<=2 family valid?
        no  -> (S2) itself is false, contradicting the section 18 table
  Q3  is ANY allocation at all valid, spread ignored?
        no  -> PS2 is false and the whole conjecture dies

The answers determine what survives. The script prints, for each witness, the
leximin set with its longest paths, and where in that chain the first "yes"
appears.
"""
import itertools
import sys

from gb_valuations import arc_weights, is_envy_freeable, longest_paths

N = 3

WITNESSES = [
    [(0,1,1,0,0,0,0,-1,1,2,2,1,0,1,1,0), (0,1,1,0,-1,0,0,0,1,2,1,1,0,1,1,0),
     (0,-1,1,0,-1,0,0,0,0,0,0,1,0,-1,-1,0)],
    [(0,-1,1,0,0,-1,0,-1,-1,-1,0,-1,-1,-1,-1,0), (0,1,1,1,1,2,0,1,1,0,2,1,1,1,1,0),
     (0,-1,1,0,-1,0,0,-1,-1,-1,0,-1,-2,-1,-1,0)],
    [(0,1,-1,0,0,0,0,-1,-1,0,0,0,0,-1,0,0), (0,0,-1,0,1,0,0,0,-1,0,-1,0,0,0,0,1),
     (0,0,-1,-1,1,0,0,0,-1,-1,-2,-1,0,0,-1,0)],
    [(0,1,0,0,0,1,0,0,0,0,-1,0,0,0,0,0), (0,1,0,0,1,2,0,1,-1,0,0,-1,0,1,-1,0),
     (0,-1,-1,-2,-1,-2,-1,-1,-1,-2,-2,-3,-2,-2,-2,-2)],
    [(0,0,0,1,-1,-1,-1,0,0,-1,1,0,-1,0,0,0), (0,1,1,2,0,0,0,1,1,0,1,1,0,1,1,0),
     (0,0,0,0,-1,0,-1,-1,1,0,0,-1,0,-1,0,0)],
    [(0,-1,1,0,1,0,1,1,1,0,1,0,2,1,1,1), (0,-1,-1,-2,1,0,0,-1,1,0,0,-1,2,1,1,0),
     (0,0,1,0,0,0,0,1,-1,0,0,1,0,1,1,2)],
    [(0,1,0,0,1,2,0,1,-1,0,-1,0,0,1,-1,0), (0,1,1,0,1,2,0,1,-1,0,0,-1,0,1,-1,0),
     (0,1,1,0,-1,0,0,0,0,0,0,-1,-1,0,-1,0)],
    [(0,0,0,0,-1,-1,-1,0,0,1,0,1,-1,0,0,1), (0,0,-1,0,-1,-1,-2,-1,-1,0,0,-1,-1,0,-1,-1),
     (0,1,1,0,0,0,0,-1,1,2,0,1,0,1,1,0)],
    [(0,-1,0,-1,0,-1,1,0,0,0,0,0,0,-1,1,0), (0,0,1,0,1,0,2,1,1,0,0,1,2,1,1,2),
     (0,0,-1,-1,0,0,-1,-1,1,0,0,0,0,-1,-1,0)],
    [(0,1,-1,0,1,2,0,1,0,0,-1,-1,0,1,-1,0), (0,0,-1,-1,0,0,-1,0,-1,0,-2,-1,0,1,-1,0),
     (0,1,-1,0,1,2,0,1,-1,0,-1,-1,0,1,0,0)],
]


def worst(vals, b):
    if not is_envy_freeable(vals, b):
        return None
    return max(longest_paths(arc_weights(vals, b)))


def allocs(m, K):
    out = []
    for assign in itertools.product(range(N), repeat=m):
        b = [0] * N
        for k, o in enumerate(assign):
            b[o] |= 1 << k
        s = [bin(x).count("1") for x in b]
        if K is None or max(s) - min(s) <= K:
            out.append((tuple(b), max(s) - min(s)))
    return out


def main():
    m = 4
    fam2 = [b for b, _ in allocs(m, 2)]
    every = allocs(m, None)
    agg = {"q1": 0, "q2": 0, "q3": 0}
    for idx, vals in enumerate(WITNESSES):
        best, bucket = None, []
        for b in fam2:
            costs = tuple(-vals[i][b[i]] for i in range(N))
            t = sum(costs)
            if best is None or t < best:
                best, bucket = t, [(b, costs)]
            elif t == best:
                bucket.append((b, costs))
        key = min(sorted(c, reverse=True) for _, c in bucket)
        lex = [(b, c) for b, c in bucket if sorted(c, reverse=True) == key]

        q1 = any(worst(vals, b) is not None and worst(vals, b) <= 1
                 for b, _ in bucket)
        q2 = [b for b in fam2
              if worst(vals, b) is not None and worst(vals, b) <= 1]
        q3 = [(b, sp) for b, sp in every
              if worst(vals, b) is not None and worst(vals, b) <= 1]
        agg["q1"] += 1 if q1 else 0
        agg["q2"] += 1 if q2 else 0
        agg["q3"] += 1 if q3 else 0

        print("witness %d: welfare max total cost %d, %d maximisers, %d leximin-optimal"
              % (idx + 1, best, len(bucket), len(lex)))
        print("   leximin set: %s"
              % [(b, c, worst(vals, b)) for b, c in lex])
        print("   Q1 some maximiser valid           : %s" % q1)
        print("   Q2 some spread<=2 allocation valid: %s  (%d of %d)"
              % (bool(q2), len(q2), len(fam2)))
        if q2:
            print("        e.g. %s cost=%s" %
                  (q2[0], tuple(-vals[i][q2[0][i]] for i in range(N))))
        print("   Q3 any allocation valid           : %s  (%d of %d, spreads %s)"
              % (bool(q3), len(q3), len(every),
                 sorted(set(sp for _, sp in q3))))
        print()
    print("SUMMARY over %d witnesses: Q1 %d, Q2 %d, Q3 %d"
          % (len(WITNESSES), agg["q1"], agg["q2"], agg["q3"]))


if __name__ == "__main__":
    main()
