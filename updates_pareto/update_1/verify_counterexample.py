"""
Independent verification that Algorithm 1 does not return a Pareto optimal
allocation.

This is a negative claim about our own theorem, so everything below is
recomputed from scratch: the cost tables are written out by hand, and the
envy-graph, envy-freeness and domination checks are implemented here rather
than imported from algo1.py. A bug in that module therefore cannot both
produce this witness and confirm it.

THE INSTANCE. n = 3 agents, m = 3 chores {a, b, c}.

    c_1 : additive, a and c cost 1 each, b is free.
    c_2 : a, b, c each cost 1 alone, but c_2({a,c}) = 1 -- taking a and c
          together costs no more than taking either alone. Non-additive, and
          the only non-additivity in the instance.
    c_3 = c_1.

Every marginal of every c_i lies in {0,1}, so this is a legitimate instance of
the paper's class.

WHAT ALGORITHM 1 RETURNS.  A = ({a,b}, {c}, {}) with p = (1,1,0), giving cost
profile (1, 1, 0) and total subsidy 2 = n - 1. That is a correct output: the
pair is envy-free and p lies in {0,1}^3, exactly as the main theorem promises.

WHY IT IS NOT PARETO OPTIMAL.  B = ({b}, {a,c}, {}) has cost profile (0, 1, 0).
Agent 1 is strictly better off and nobody is worse off, because agent 2 absorbs
a at no extra cost on top of c. So B Pareto dominates A.

THE STING.  B is not merely better for the agents -- it also satisfies the
paper's own guarantee, and does so more cheaply: B is envy-free with
p = (0,1,0), a total subsidy of 1 rather than 2. So on this instance the
algorithm returns an outcome that is Pareto dominated by another outcome which
is itself feasible for the theorem and costs the sponsor less.
"""
import itertools

N, M = 3, 3
A_, B_, C_ = 0, 1, 2
NAMES = "abc"


def cost_from_items(weights):
    """Additive cost from per-item weights."""
    return tuple(sum(weights[k] for k in range(M) if S & (1 << k))
                 for S in range(1 << M))


# agents 1 and 3: additive, a and c cost 1, b free
C1 = cost_from_items([1, 0, 1])
C3 = C1

# agent 2: singletons cost 1, but {a,c} costs only 1 -- the one non-additivity
C2 = [0] * 8
C2[0b000] = 0
C2[0b001] = 1          # {a}
C2[0b010] = 1          # {b}
C2[0b011] = 2          # {a,b}
C2[0b100] = 1          # {c}
C2[0b101] = 1          # {a,c}   <-- a is free once c is held
C2[0b110] = 2          # {b,c}
C2[0b111] = 2          # {a,b,c}
C2 = tuple(C2)

CS = [C1, C2, C3]


def bundle(mask):
    return "{" + ",".join(NAMES[k] for k in range(M) if mask & (1 << k)) + "}"


def marginals_ok(c):
    """c(empty) = 0 and every marginal in {0,1}."""
    if c[0] != 0:
        return False
    for S in range(1 << M):
        for k in range(M):
            bit = 1 << k
            if not S & bit and c[S | bit] - c[S] not in (0, 1):
                return False
    return True


def ef_with(p, A):
    """c_i(A_i) - p_i <= c_i(A_j) - p_j for all i, j."""
    return all(CS[i][A[i]] - p[i] <= CS[i][A[j]] - p[j]
               for i in range(N) for j in range(N))


def cheapest_valid_subsidy(A):
    """The cheapest p in {0,1}^n making A envy-free, or None."""
    best = None
    for p in itertools.product((0, 1), repeat=N):
        if ef_with(p, A) and (best is None or sum(p) < sum(best)):
            best = p
    return best


def profile(A):
    return tuple(CS[i][A[i]] for i in range(N))


def dominates(B, A):
    return (all(CS[i][B[i]] <= CS[i][A[i]] for i in range(N))
            and any(CS[i][B[i]] < CS[i][A[i]] for i in range(N)))


def every_allocation():
    for assign in itertools.product(range(N), repeat=M):
        b = [0] * N
        for k, owner in enumerate(assign):
            b[owner] |= 1 << k
        yield tuple(b)


def show(A):
    return " ".join("%-7s" % bundle(x) for x in A)


def main():
    print("cost tables valid (c(empty)=0, marginals in {0,1}):",
          [marginals_ok(c) for c in CS])
    for i in range(N):
        print("   agent %d : %s" % (i + 1, str(CS[i])))
    print()

    A = (0b011, 0b100, 0b000)          # ({a,b}, {c}, {})
    B = (0b010, 0b101, 0b000)          # ({b}, {a,c}, {})

    pA = cheapest_valid_subsidy(A)
    pB = cheapest_valid_subsidy(B)

    print("Algorithm 1 output")
    print("   A = %s  costs = %s" % (show(A), profile(A)))
    print("   cheapest p in {0,1}^3 making A envy-free : %s, total %d"
          % (pA, sum(pA)))
    print()
    print("The dominating allocation")
    print("   B = %s  costs = %s" % (show(B), profile(B)))
    print("   cheapest p in {0,1}^3 making B envy-free : %s, total %d"
          % (pB, sum(pB)))
    print()
    print("   B dominates A : %s" % dominates(B, A))
    print("   agent 1 strictly better: %d -> %d ; agents 2,3 unchanged"
          % (CS[0][A[0]], CS[0][B[0]]))
    print()

    dom = [D for D in every_allocation() if dominates(D, A)]
    print("all allocations dominating A (%d found):" % len(dom))
    for D in dom:
        p = cheapest_valid_subsidy(D)
        print("   %s costs = %s   cheapest valid p = %s"
              % (show(D), profile(D), p))
    print()

    po_and_valid = []
    for D in every_allocation():
        p = cheapest_valid_subsidy(D)
        if p is None:
            continue
        if not any(dominates(E, D) for E in every_allocation()):
            po_and_valid.append((D, p))
    print("allocations that are BOTH Pareto optimal and feasible for the")
    print("theorem (%d found):" % len(po_and_valid))
    for D, p in po_and_valid:
        print("   %s costs = %s   p = %s total %d"
              % (show(D), profile(D), p, sum(p)))
    print()
    print("CONFIRMED: Algorithm 1's output is not Pareto optimal, and the")
    print("instance does admit outcomes that are simultaneously Pareto")
    print("optimal and within the theorem's guarantee -- so PO is not")
    print("impossible here, the algorithm simply does not find it.")


if __name__ == "__main__":
    main()
