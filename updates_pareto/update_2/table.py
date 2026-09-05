"""
The table for Appendix B: Pareto optimality against the unit-subsidy bound.

Two agents, three chores, both agents sharing c(S) = min(|S|, 2). For every one
of the eight complete allocations this prints the cost profile, the pointwise
minimal subsidy, whether that subsidy is within the unit bound, and whether the
allocation is Pareto optimal.

Pareto optimality is the standard notion of Chakraborty, Igarashi, Suksompong
and Zick specialised to costs: B dominates A when c_i(B_i) <= c_i(A_i) for every
i with strict inequality for some i, over COMPLETE allocations -- for chores the
quantifier must be over complete allocations, since withholding a chore weakly
helps everyone and would make the notion vacuous.
"""
import itertools

N, M = 2, 3
NAMES = "abc"


def c(S):
    return min(bin(S).count("1"), 2)


def show(S):
    return "\emptyset" if S == 0 else "\set{" + ",".join(
        NAMES[k] for k in range(M) if S & (1 << k)) + "}"


def subsidy(X):
    """Minimal subsidy for two agents sharing c; None if not envy-freeable."""
    base = -c(X[0]) - c(X[1])
    if -c(X[1]) - c(X[0]) > base:
        return None
    w01 = c(X[0]) - c(X[1])
    w10 = c(X[1]) - c(X[0])
    if w01 + w10 > 0:
        return None
    return [max(0, w01), max(0, w10)]


def main():
    allocs = []
    for o in itertools.product(range(N), repeat=M):
        b = [0] * N
        for k, i in enumerate(o):
            b[i] |= 1 << k
        allocs.append(tuple(b))
    prof = {X: (c(X[0]), c(X[1])) for X in allocs}

    def po(X):
        a = prof[X]
        return not any(Y != X and prof[Y][0] <= a[0] and prof[Y][1] <= a[1]
                       and (prof[Y][0] < a[0] or prof[Y][1] < a[1])
                       for Y in allocs)

    print("%-12s %-12s %-10s %-10s %-8s %s"
          % ("A_1", "A_2", "costs", "p*", "p*<=1?", "PO?"))
    for X in allocs:
        p = subsidy(X)
        print("%-12s %-12s %-10s %-10s %-8s %s"
              % (show(X[0]), show(X[1]), prof[X], p,
                 "yes" if max(p) <= 1 else "NO", "YES" if po(X) else "no"))
    print()
    print("LaTeX rows:")
    for X in allocs:
        p = subsidy(X)
        print("$%s$ & $%s$ & $(%d,%d)$ & $(%d,%d)$ & %s & %s \\\\"
              % (show(X[0]), show(X[1]), prof[X][0], prof[X][1], p[0], p[1],
                 "yes" if max(p) <= 1 else "\textbf{no}",
                 "\textbf{yes}" if po(X) else "no"))
    print()
    nboth = sum(1 for X in allocs if po(X) and max(subsidy(X)) <= 1)
    print("allocations that are both PO and within the unit bound: %d" % nboth)
    print("total cost of the cheapest PO allocation      : %d"
          % min(sum(prof[X]) for X in allocs if po(X)))
    print("total cost of the cheapest admissible one     : %d"
          % min(sum(prof[X]) for X in allocs if max(subsidy(X)) <= 1))


if __name__ == "__main__":
    main()
