"""
Independent re-check of the two states that refute (DESCENT-1).

hunt_pair.py reports two partitions with max l = 2 from which no one-item move
strictly decreases PHI. That refutes the central claim of approach 17, so it is
re-verified here with the envy-graph routines re-derived from the definitions
rather than reused, and four separate questions are answered:

  1  is the state genuinely bad -- envy-freeable with max l = 2?
  2  is it genuinely stuck under ONE-item moves?
  3  does a TWO-item move descend?  (would repair the lemma, not the route)
  4  does the instance still admit a valid allocation at all?

Question 4 is the one that matters most. If yes, PS2 survives and only
(DESCENT-1) is wrong. If no, PS2 itself would be false for n=3.
"""
import itertools

N = 3
WIT = [
    ((8, 2, 5),
     [(0,-1,0,-1,0,-1,1,0,1,0,0,0,1,0,0,1),
      (0,-1,1,0,0,-1,1,0,0,0,1,0,-1,0,0,1),
      (0,-1,1,0,0,-1,0,-1,1,0,1,1,1,0,0,0)]),
    ((4, 1, 10),
     [(0,1,-1,0,1,1,0,0,-1,0,-2,-1,0,0,-1,0),
      (0,1,-1,0,0,0,0,0,-1,0,-1,-1,-1,0,-1,-1),
      (0,0,-1,0,1,1,0,0,-1,0,-1,-1,0,0,0,-1)]),
]
M = 4


def legal(v):
    for S in range(1 << M):
        for b in range(M):
            if not S & (1 << b) and v[S | (1 << b)] - v[S] not in (-1, 0, 1):
                return False
    return v[0] == 0


def welfare(vals, c):
    return sum(vals[i][c[i]] for i in range(N))


def envy_freeable(vals, c):
    base = welfare(vals, c)
    return all(sum(vals[i][c[p[i]]] for i in range(N)) <= base
               for p in itertools.permutations(range(N)))


def longest(vals, c):
    """l(i) by explicit enumeration of simple paths on 3 vertices."""
    def w(i, j):
        return vals[i][c[j]] - vals[i][c[i]]
    out = []
    for i in range(N):
        rest = [j for j in range(N) if j != i]
        best = 0
        for j in rest:
            best = max(best, w(i, j))
            for k in rest:
                if k != j:
                    best = max(best, w(i, j) + w(j, k))
        out.append(best)
    return out


def phi(vals, b, mode="SUM"):
    """SUM = sum of longest paths; SORTED = the vector sorted downwards."""
    best = None
    for p in itertools.permutations(range(N)):
        c = tuple(b[p[i]] for i in range(N))
        if not envy_freeable(vals, c):
            continue
        l = longest(vals, c)
        s = sum(l) if mode == "SUM" else tuple(sorted(l, reverse=True))
        if best is None or s < best:
            best = s
    return best


def owners(b):
    o = [None] * M
    for i in range(N):
        for k in range(M):
            if b[i] & (1 << k):
                o[k] = i
    return o


def from_owners(o):
    b = [0] * N
    for k, i in enumerate(o):
        b[i] |= 1 << k
    return tuple(b)


ALL = [from_owners(o) for o in itertools.product(range(N), repeat=M)]


def main():
    for idx, (b, vals) in enumerate(WIT):
        print("WITNESS %d: partition %s" % (idx + 1, b))
        print("   valuations legal (all marginals in {-1,0,1}) : %s"
              % all(legal(v) for v in vals))
        base = phi(vals, b)
        # best assignment and its l vector
        bestc, bestl = None, None
        for p in itertools.permutations(range(N)):
            c = tuple(b[p[i]] for i in range(N))
            if not envy_freeable(vals, c):
                continue
            l = longest(vals, c)
            if bestl is None or sum(l) < sum(bestl):
                bestc, bestl = c, l
        print("   1  PHI = %s, best assignment %s with l = %s  -> bad = %s"
              % (base, bestc, bestl, max(bestl) >= 2))

        o = owners(b)
        one = [c for c in ALL
               if sum(1 for k in range(M) if owners(c)[k] != o[k]) == 1]
        two = [c for c in ALL
               if sum(1 for k in range(M) if owners(c)[k] != o[k]) == 2]
        b1 = [c for c in one if phi(vals, c) is not None and phi(vals, c) < base]
        b2 = [c for c in two if phi(vals, c) is not None and phi(vals, c) < base]
        print("   2  one-item moves that descend, SUM    : %d of %d%s"
              % (len(b1), len(one), "   <-- STUCK" if not b1 else ""))
        sbase = phi(vals, b, "SORTED")
        s1 = [c for c in one if phi(vals, c, "SORTED") is not None
              and phi(vals, c, "SORTED") < sbase]
        print("   2b one-item moves that descend, SORTED : %d of %d   "
              "(PSI here = %s)%s"
              % (len(s1), len(one), sbase, "   <-- STUCK" if not s1 else ""))
        if s1:
            print("        e.g. %s PSI=%s" % (s1[0], phi(vals, s1[0], "SORTED")))
        print("   3  two-item moves that descend : %d of %d%s"
              % (len(b2), len(two),
                 ("   e.g. %s PHI=%d" % (b2[0], phi(vals, b2[0]))) if b2 else ""))

        valid = [c for c in ALL
                 if envy_freeable(vals, c) and max(longest(vals, c)) <= 1]
        print("   4  valid allocations in the instance : %d of %d%s"
              % (len(valid), len(ALL),
                 ("   e.g. %s" % (valid[0],)) if valid else "   <-- PS2 FAILS"))
        if valid:
            d = min(sum(1 for k in range(M) if owners(c)[k] != o[k])
                    for c in valid)
            print("      nearest valid allocation differs in %d item owners" % d)
        print()


if __name__ == "__main__":
    main()
