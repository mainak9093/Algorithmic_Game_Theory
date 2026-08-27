"""
Approach 15: independent re-check that the decomposition BRIDGE is lossy.

The bridge says: if one allocation A carries a goods certificate q in {0,1}^n
for u and a chores certificate r in {0,1}^n for c, then p = q + r is a valid
subsidy for v = u - c. For the bridge to prove the conjecture it would need
some allocation with q_i + r_i <= 1 for every i.

test_decomposition.py reports instances where the conjecture HOLDS but no
allocation carries both certificates within that budget. That is a negative
claim, so it is re-verified here with everything reimplemented from scratch --
the decomposition, the envy-graph, the welfare test and the longest paths --
so that a bug in gb_valuations.py could not both produce and confirm it.

THE WITNESS. n = 2 agents, m = 3 items:

    v_1 = (0, -1, -1, -1, -1, -1, -1, -2)     indexed by subset bitmask
    v_2 = (0,  0,  0,  0,  0,  0,  0, -1)

Both have every marginal in {-1,0,1}. The script prints, for all 8 complete
allocations, the minimal subsidy for v itself and the minimal certificates for
u and for -c, so the two columns can be compared directly.

Note on exactness. Halpern-Shah gives that the minimal certificate is pointwise
below every valid one, so "some valid (q,r) has q_i + r_i <= 1" holds if and
only if the MINIMAL q*, r* do. Checking the minimal ones is therefore a
complete test, not a heuristic.
"""
import itertools

N, M = 2, 3

V = [
    (0, -1, -1, -1, -1, -1, -1, -2),
    (0, 0, 0, 0, 0, 0, 0, -1),
]


def popcount(S):
    return bin(S).count("1")


def marginals_ok(v):
    for S in range(1 << M):
        for b in range(M):
            bit = 1 << b
            if not S & bit and v[S | bit] - v[S] not in (-1, 0, 1):
                return False
    return True


def decompose(v):
    c = tuple((popcount(S) - v[S]) // 2 for S in range(1 << M))
    u = tuple(v[S] + c[S] for S in range(1 << M))
    return u, c


def dichotomous(v):
    for S in range(1 << M):
        for b in range(M):
            bit = 1 << b
            if not S & bit and v[S | bit] - v[S] not in (0, 1):
                return False
    return True


def subsidy(vals, bundles):
    """Minimal subsidy, or None if the allocation is not envy-freeable."""
    base = sum(vals[i][bundles[i]] for i in range(N))
    for perm in itertools.permutations(range(N)):
        if sum(vals[i][bundles[perm[i]]] for i in range(N)) > base:
            return None

    def w(i, j):
        return vals[i][bundles[j]] - vals[i][bundles[i]]

    out = []
    for i in range(N):
        others = [j for j in range(N) if j != i]
        best = 0
        for j in others:
            best = max(best, w(i, j))
            for k in others:
                if k != j:
                    best = max(best, w(i, j) + w(j, k))
        out.append(best)
    return out


def show(mask):
    return "{" + ",".join("abc"[b] for b in range(M) if mask & (1 << b)) + "}"


def main():
    print("marginals of v in {-1,0,1}:", [marginals_ok(v) for v in V])

    U, C = zip(*(decompose(v) for v in V))
    NEG_C = tuple(tuple(-x for x in c) for c in C)

    print("u dichotomous:", [dichotomous(u) for u in U])
    print("c dichotomous:", [dichotomous(c) for c in C])
    print("v = u - c    :",
          [all(U[i][S] - C[i][S] == V[i][S] for S in range(1 << M))
           for i in range(N)])
    print()
    for i in range(N):
        print("  agent %d  v=%s" % (i + 1, str(V[i])))
        print("           u=%s" % str(U[i]))
        print("           c=%s" % str(C[i]))
    print()

    print("every complete allocation:")
    print("   bundles                 p*(v)      q*(u)    r*(-c)   q*+r*")
    direct_ok = bridge_ok = False
    for assign in itertools.product(range(N), repeat=M):
        bundles = [0] * N
        for k, owner in enumerate(assign):
            bundles[owner] |= 1 << k
        bundles = tuple(bundles)

        p = subsidy(V, bundles)
        q = subsidy(U, bundles)
        r = subsidy(NEG_C, bundles)

        if p is not None and max(p) <= 1:
            direct_ok = True
        s = None
        if q is not None and r is not None:
            s = [q[i] + r[i] for i in range(N)]
            if max(s) <= 1:
                bridge_ok = True

        print("   %-10s %-10s  %-9s  %-7s  %-7s  %s"
              % (show(bundles[0]), show(bundles[1]),
                 "-" if p is None else str(p),
                 "-" if q is None else str(q),
                 "-" if r is None else str(r),
                 "-" if s is None else str(s)))
    print()
    print("conjecture holds directly (some allocation with max p* <= 1) : %s"
          % direct_ok)
    print("bridge reaches it (some allocation with max (q*+r*) <= 1)    : %s"
          % bridge_ok)
    print()
    if direct_ok and not bridge_ok:
        print("CONFIRMED: the conjecture is true on this instance but the")
        print("goods-certificate-plus-chores-certificate bridge cannot")
        print("certify it. The coupled target q_i + r_i <= 1 is not")
        print("achievable in general.")


if __name__ == "__main__":
    main()
