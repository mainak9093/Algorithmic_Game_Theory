"""
The incompatibility witness, written out inequality by inequality, so that
every number in the explanation can be checked by hand.

Instance: n = 2 agents, m = 3 chores {a, b, c}, both agents sharing

    c(S) = min(|S|, 2)

For each of the eight allocations this prints the two envy inequalities, the
exact constraint they place on the subsidy vector, whether p in {0,1}^2 can
satisfy them, and whether the allocation is Pareto optimal.
"""
import itertools

N, M = 2, 3
NAMES = "abc"


def c(S):
    return min(bin(S).count("1"), 2)


def bundle(mask):
    return "{" + ",".join(NAMES[k] for k in range(M) if mask & (1 << k)) + "}"


def allocations():
    for assign in itertools.product(range(N), repeat=M):
        b = [0] * N
        for k, owner in enumerate(assign):
            b[owner] |= 1 << k
        yield tuple(b)


def main():
    print("COST FUNCTION  c(S) = min(|S|, 2), shared by both agents")
    print()
    for k in range(M + 1):
        S = (1 << k) - 1
        print("   |S| = %d  ->  c(S) = %d" % (k, c(S)))
    print()
    print("   marginals, in order of bundle size:")
    for k in range(M):
        S = (1 << k) - 1
        print("      adding a chore to a bundle of size %d : %d -> %d, "
              "marginal %d" % (k, c(S), c(S | (1 << k)), c(S | (1 << k)) - c(S)))
    print("   every marginal is 0 or 1, c(empty) = 0, c is monotone: in class.")
    print("   additive would need c({a,b,c}) = 3, but it is 2: NON-additive.")
    print()

    allocs = list(allocations())
    profs = {A: (c(A[0]), c(A[1])) for A in allocs}

    print("THE EIGHT ALLOCATIONS")
    print()
    print("   %-9s %-9s %-8s %-38s %-8s %s"
          % ("agent 1", "agent 2", "costs", "envy constraints on (p1,p2)",
             "p in 01?", "PO?"))

    for A in allocs:
        c1own, c1other = c(A[0]), c(A[1])
        c2own, c2other = c(A[1]), c(A[0])
        # agent 1: c1(A1) - p1 <= c1(A2) - p2  =>  p1 - p2 >= c1own - c1other
        lo = c1own - c1other
        # agent 2: c2(A2) - p2 <= c2(A1) - p1  =>  p1 - p2 <= c2other - c2own
        hi = c2other - c2own
        constraint = "%d <= p1 - p2 <= %d" % (lo, hi)

        feasible = [p for p in itertools.product((0, 1), repeat=2)
                    if lo <= p[0] - p[1] <= hi]
        pa = profs[A]
        po = not any(B != A
                     and profs[B][0] <= pa[0] and profs[B][1] <= pa[1]
                     and (profs[B][0] < pa[0] or profs[B][1] < pa[1])
                     for B in allocs)
        print("   %-9s %-9s %-8s %-38s %-8s %s"
              % (bundle(A[0]), bundle(A[1]), pa, constraint,
                 "yes" if feasible else "NO", "YES" if po else "no"))
    print()

    print("THE TWO PARETO OPTIMAL ALLOCATIONS, IN DETAIL")
    for A in allocs:
        pa = profs[A]
        po = not any(B != A
                     and profs[B][0] <= pa[0] and profs[B][1] <= pa[1]
                     and (profs[B][0] < pa[0] or profs[B][1] < pa[1])
                     for B in allocs)
        if not po:
            continue
        print()
        print("   A = (%s, %s), costs %s" % (bundle(A[0]), bundle(A[1]), pa))
        loaded = 0 if c(A[0]) > c(A[1]) else 1
        other = 1 - loaded
        print("      agent %d holds everything and values it at %d;"
              % (loaded + 1, c(A[loaded])))
        print("      agent %d holds nothing, valued at %d."
              % (other + 1, c(A[other])))
        print("      so agent %d envies agent %d by %d - %d = %d,"
              % (loaded + 1, other + 1, c(A[loaded]), c(A[other]),
                 c(A[loaded]) - c(A[other])))
        print("      and needs p_%d >= %d. The theorem allows at most 1."
              % (loaded + 1, c(A[loaded]) - c(A[other])))
    print()

    print("WHY EVERY FEASIBLE ALLOCATION IS DOMINATED")
    print()
    for A in allocs:
        pa = profs[A]
        feas = any(True for p in itertools.product((0, 1), repeat=2)
                   if c(A[0]) - p[0] <= c(A[1]) - p[1]
                   and c(A[1]) - p[1] <= c(A[0]) - p[0])
        lo = c(A[0]) - c(A[1])
        hi = c(A[0]) - c(A[1])
        feasible = [p for p in itertools.product((0, 1), repeat=2)
                    if lo <= p[0] - p[1] <= hi]
        if not feasible:
            continue
        doms = [B for B in allocs
                if B != A and profs[B][0] <= pa[0] and profs[B][1] <= pa[1]
                and (profs[B][0] < pa[0] or profs[B][1] < pa[1])]
        print("   (%s, %s) costs %s  -- dominated by %s"
              % (bundle(A[0]), bundle(A[1]), pa,
                 ", ".join("(%s, %s) costs %s"
                           % (bundle(B[0]), bundle(B[1]), profs[B])
                           for B in doms)))
    print()

    print("TOTAL SOCIAL COST")
    po_costs, feas_costs = [], []
    for A in allocs:
        pa = profs[A]
        lo = hi = c(A[0]) - c(A[1])
        feasible = [p for p in itertools.product((0, 1), repeat=2)
                    if lo <= p[0] - p[1] <= hi]
        po = not any(B != A
                     and profs[B][0] <= pa[0] and profs[B][1] <= pa[1]
                     and (profs[B][0] < pa[0] or profs[B][1] < pa[1])
                     for B in allocs)
        if po:
            po_costs.append(sum(pa))
        if feasible:
            feas_costs.append(sum(pa))
    print("   cheapest Pareto optimal allocation : %d" % min(po_costs))
    print("   cheapest feasible allocation       : %d" % min(feas_costs))
    print("   the bound costs society            : %d extra unit(s)"
          % (min(feas_costs) - min(po_costs)))


if __name__ == "__main__":
    main()
