"""Test Conjecture D (double refinement, PS1_note_next_routes.md Route D) against
the instance that already refutes the utilitarian-optimality conjecture --
update_1/mswcex.py, i.e. Proposition "prop:msw-false" in the report.

Conjecture D: let U = argmin over partitions of sum_i c_i(A_i); refine to those
lexicographically minimising the descending-sorted cardinality vector, then the
descending-sorted own-cost vector.  Claim: every survivor has ell(i) <= 1.

Logical worry: on that instance U is a SINGLETON whose unique member needs
subsidy 2.  Refinements only shrink a set, so they cannot rescue it.

Run:  python checkD.py
"""
from itertools import combinations, product

M = 4
N = 3

RAW = [
    {(): 0, (0,): 1, (1,): 1, (2,): 1, (3,): 1,
     (0, 1): 2, (0, 2): 1, (0, 3): 2, (1, 2): 1, (1, 3): 2, (2, 3): 2,
     (0, 1, 2): 2, (0, 1, 3): 3, (0, 2, 3): 2, (1, 2, 3): 2, (0, 1, 2, 3): 3},
    {(): 0, (0,): 1, (1,): 1, (2,): 1, (3,): 1,
     (0, 1): 2, (0, 2): 2, (0, 3): 2, (1, 2): 2, (1, 3): 2, (2, 3): 1,
     (0, 1, 2): 3, (0, 1, 3): 2, (0, 2, 3): 2, (1, 2, 3): 2, (0, 1, 2, 3): 3},
    {(): 0, (0,): 1, (1,): 1, (2,): 0, (3,): 1,
     (0, 1): 2, (0, 2): 1, (0, 3): 2, (1, 2): 1, (1, 3): 2, (2, 3): 1,
     (0, 1, 2): 2, (0, 1, 3): 2, (0, 2, 3): 2, (1, 2, 3): 2, (0, 1, 2, 3): 3},
]
CS = [{frozenset(k): v for k, v in d.items()} for d in RAW]


def ellvec(cs, bd, n):
    """Longest-path subsidies; None iff a positive-weight cycle exists."""
    W = [[cs[i][bd[i]] - cs[i][bd[j]] for j in range(n)] for i in range(n)]
    e = [0] * n
    for _ in range(n + 1):
        ch = False
        new = list(e)
        for i in range(n):
            for j in range(n):
                if i != j and W[i][j] + e[j] > new[i]:
                    new[i] = W[i][j] + e[j]
                    ch = True
        e = new
        if not ch:
            return e
    return None


def maxsub(cs, bd, n):
    e = ellvec(cs, bd, n)
    return None if e is None else max(e)


def main():
    parts = []
    for assign in product(range(N), repeat=M):
        bd = [frozenset(g for g in range(M) if assign[g] == i) for i in range(N)]
        parts.append(bd)

    # Step 1: utilitarian optimum.
    cost = lambda bd: sum(CS[i][bd[i]] for i in range(N))
    best = min(cost(bd) for bd in parts)
    U = [bd for bd in parts if cost(bd) == best]
    print("min total cost                     : %d" % best)
    print("|U| (utilitarian-optimal set)      : %d" % len(U))

    # Step 2: descending-sorted cardinality vector, lexicographically minimal.
    card = lambda bd: tuple(sorted((len(b) for b in bd), reverse=True))
    kmin = min(card(bd) for bd in U)
    U2 = [bd for bd in U if card(bd) == kmin]
    print("after cardinality-balance refinement: %d  (key %s)" % (len(U2), kmin))

    # Step 3: descending-sorted own-cost vector, lexicographically minimal.
    cvec = lambda bd: tuple(sorted((CS[i][bd[i]] for i in range(N)), reverse=True))
    lmin = min(cvec(bd) for bd in U2)
    U3 = [bd for bd in U2 if cvec(bd) == lmin]
    print("after cost-leximin refinement      : %d  (key %s)" % (len(U3), lmin))

    print()
    bad = []
    for bd in U3:
        v = maxsub(CS, bd, N)
        print("   selected %s  cost=%d  max ell=%s"
              % ([sorted(b) for b in bd], cost(bd), v))
        if v is None or v > 1:
            bad.append(bd)

    # For contrast: the best any allocation can do.
    allbest = min(v for v in (maxsub(CS, bd, N) for bd in parts) if v is not None)
    print("\nbest max-ell over ALL allocations   : %d" % allbest)

    print()
    if bad:
        print("VERDICT: Conjecture D is FALSE on this instance --")
        print("         every selected allocation needs subsidy >= 2,")
        print("         while some allocation elsewhere achieves %d." % allbest)
    else:
        print("VERDICT: Conjecture D survives here.")


if __name__ == "__main__":
    main()
