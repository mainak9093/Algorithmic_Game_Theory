"""
Witnesses for the section on why the size shift does not transfer BKNS.

The size shift vt_i(S) = |S| - c_i(S) is a bijection of the dichotomous COST
class onto the dichotomous GOODS class. It does NOT preserve the envy graph:
for any allocation A,

    w^{vt}_A(i,j) = ( |A_j| - |A_i| ) + w^{c}_A(i,j),

so the two graphs agree edge by edge exactly when all bundles have the same
cardinality. This script produces the two facts the section needs.

  (a) an allocation whose size-shifted GOODS instance needs subsidy at most 1
      per agent while the underlying CHORES instance needs 2 or more, so the
      guarantee is not inherited allocation by allocation;

  (b) an instance in which EVERY allocation that is optimal for the goods
      instance -- least maximum subsidy -- needs 2 or more for chores, so the
      failure is not repaired by choosing a better goods-optimal allocation.

Everything is computed from the definitions: Halpern-Shah says an allocation is
envy-freeable iff no reassignment of its own bundles raises welfare, and the
minimum subsidy is then the longest path in the envy graph.
"""
import itertools
import sys


def subsets(m):
    return list(range(1 << m))


def dich_costs(m):
    """Every dichotomous cost function on m items: c(empty)=0, marginals 0/1."""
    order = sorted(range(1 << m), key=lambda s: (bin(s).count("1"), s))
    val = [0] * (1 << m)

    def rec(i):
        if i == len(order):
            yield tuple(val)
            return
        S = order[i]
        if S == 0:
            yield from rec(i + 1)
            return
        bits = [1 << b for b in range(m) if S & (1 << b)]
        lo = max(val[S ^ b] for b in bits)
        hi = min(val[S ^ b] for b in bits) + 1
        for x in range(lo, hi + 1):
            val[S] = x
            yield from rec(i + 1)
        val[S] = 0

    yield from rec(0)


def allocations(n, m):
    out = []
    for o in itertools.product(range(n), repeat=m):
        b = [0] * n
        for k, i in enumerate(o):
            b[i] |= 1 << k
        out.append(tuple(b))
    return out


def min_subsidy(val, A, n, sign):
    """
    sign=-1 : costs, utility -c ; sign=+1 : goods, utility v.
    Returns the minimum subsidy vector, or None if not envy-freeable.
    """
    u = [[sign * val[i][A[j]] for j in range(n)] for i in range(n)]
    base = sum(u[i][i] for i in range(n))
    for p in itertools.permutations(range(n)):
        if sum(u[i][p[i]] for i in range(n)) > base:
            return None
    w = [[u[i][j] - u[i][i] for j in range(n)] for i in range(n)]
    best = [0] * n
    def walk(s, cur, seen, tot):
        if tot > best[s]:
            best[s] = tot
        for j in range(n):
            if j != cur and not seen & (1 << j):
                walk(s, j, seen | (1 << j), tot + w[cur][j])
    for i in range(n):
        walk(i, i, 1 << i, 0)
    return best


def show(m, x):
    return "\{" + ",".join("abcd"[k] for k in range(m) if x & (1 << k)) + "\}"


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    m = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    pool = list(dich_costs(m))
    A = allocations(n, m)
    print("dichotomous cost functions on m=%d: %d ; allocations: %d"
          % (m, len(pool), len(A)))

    caseA = caseB = None
    nA = nB = 0
    for cs in itertools.product(pool, repeat=n):
        cs = list(cs)
        vt = [tuple(bin(S).count("1") - c[S] for S in range(1 << m))
              for c in cs]
        gres, cres = {}, {}
        for a in A:
            g = min_subsidy(vt, a, n, +1)
            c = min_subsidy(cs, a, n, -1)
            gres[a] = g
            cres[a] = c
            if g is not None and max(g) <= 1 and (c is None or max(c) >= 2):
                nA += 1
                if caseA is None:
                    caseA = (cs, vt, a, g, c)
        okg = [a for a in A if gres[a] is not None]
        if okg:
            best = min(max(gres[a]) for a in okg)
            opt = [a for a in okg if max(gres[a]) == best]
            if best <= 1 and all(cres[a] is None or max(cres[a]) >= 2
                                 for a in opt):
                nB += 1
                if caseB is None:
                    caseB = (cs, vt, opt, best)

    print()
    print("(a) allocations good for the shifted goods instance, bad for chores : %d" % nA)
    if caseA:
        cs, vt, a, g, c = caseA
        print("    costs   c_i by subset (a,b,c order): %s" % (cs,))
        print("    shifted vt_i:                        %s" % (vt,))
        print("    allocation %s  sizes %s"
              % ([show(m, x) for x in a], [bin(x).count("1") for x in a]))
        print("    goods min subsidy  %s   (max %d)" % (g, max(g)))
        print("    chores min subsidy %s" % (c,))
    print()
    print("(b) instances where EVERY goods-optimal allocation is bad for chores : %d" % nB)
    if caseB:
        cs, vt, opt, best = caseB
        print("    costs c_i: %s" % (cs,))
        print("    goods optimum max-subsidy %d, attained by %d allocations"
              % (best, len(opt)))
        for a in opt[:4]:
            print("       %s  sizes %s"
                  % ([show(m, x) for x in a], [bin(x).count("1") for x in a]))


if __name__ == "__main__":
    main()
