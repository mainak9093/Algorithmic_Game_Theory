"""
Independent verification of the main finding: for negative dichotomous chores,
Pareto optimality is INCOMPATIBLE with the paper's subsidy guarantee.

Everything is recomputed from scratch here -- no import from algo1.py -- since
this is a negative claim about our own theorem.

THE INSTANCE. n = 2 agents, m = 3 chores {a, b, c}. Both agents have the same
cost function

    c(S) = min(|S|, 2).

That is: one chore costs 1, two chores cost 2, and a third is free once you
already hold two. Every marginal is 0 or 1, c(empty) = 0, and c is monotone, so
this is a legitimate instance of the paper's class. It is non-additive -- an
additive c would give c({a,b,c}) = 3.

WHY IT BITES. Because cost saturates at 2, it is socially cheapest to dump all
three chores on one agent: total cost 2 + 0 = 2. Any split pays 2 + 1 = 3. So
the only Pareto optimal allocations are the two that concentrate everything on
a single agent. But those are exactly the allocations that need a subsidy of 2:
the loaded agent values her own bundle at 2 and the empty bundle at 0, so she
must be paid 2 to stop envying.

The theorem caps the subsidy at 1 per agent. So it forces a split, and every
split is Pareto dominated.

CONSEQUENCE. No algorithm can achieve the theorem's guarantee and Pareto
optimality simultaneously. This is not a defect of our Algorithm 1 and cannot
be repaired by a better tie-breaking rule; the two objectives are simply
inconsistent on this instance.
"""
import itertools

N, M = 2, 3
NAMES = "abc"


def c(S):
    """The shared cost function: min(|S|, 2)."""
    return min(bin(S).count("1"), 2)


CS = [c, c]


def bundle(mask):
    return "{" + ",".join(NAMES[k] for k in range(M) if mask & (1 << k)) + "}"


def check_class():
    """c(empty) = 0, monotone, every marginal in {0,1}."""
    ok = (c(0) == 0)
    for S in range(1 << M):
        for k in range(M):
            bit = 1 << k
            if not S & bit:
                d = c(S | bit) - c(S)
                if d not in (0, 1):
                    ok = False
    return ok


def is_additive():
    singles = [c(1 << k) for k in range(M)]
    return all(c(S) == sum(singles[k] for k in range(M) if S & (1 << k))
               for S in range(1 << M))


def every_allocation():
    for assign in itertools.product(range(N), repeat=M):
        b = [0] * N
        for k, owner in enumerate(assign):
            b[owner] |= 1 << k
        yield tuple(b)


def profile(A):
    return tuple(CS[i](A[i]) for i in range(N))


def dominates(B, A):
    pa, pb = profile(A), profile(B)
    return (all(pb[i] <= pa[i] for i in range(N))
            and any(pb[i] < pa[i] for i in range(N)))


def is_po(A):
    return not any(dominates(B, A) for B in every_allocation())


def valid_subsidies(A):
    """All p in {0,1}^N making A envy-free: c_i(A_i) - p_i <= c_i(A_j) - p_j."""
    out = []
    for p in itertools.product((0, 1), repeat=N):
        if all(CS[i](A[i]) - p[i] <= CS[i](A[j]) - p[j]
               for i in range(N) for j in range(N)):
            out.append(p)
    return out


def min_subsidy_unbounded(A):
    """Smallest total subsidy over all non-negative integer p (cap 4)."""
    best = None
    for p in itertools.product(range(5), repeat=N):
        if all(CS[i](A[i]) - p[i] <= CS[i](A[j]) - p[j]
               for i in range(N) for j in range(N)):
            if best is None or sum(p) < sum(best):
                best = p
    return best


def main():
    print("instance: n = %d, m = %d, both agents share c(S) = min(|S|, 2)"
          % (N, M))
    print("   in the paper's class (c(empty)=0, marginals in {0,1}) : %s"
          % check_class())
    print("   additive : %s" % is_additive())
    print("   cost table by |S| : %s"
          % {k: c((1 << k) - 1) for k in range(M + 1)})
    print()

    rows = []
    for A in every_allocation():
        vs = valid_subsidies(A)
        rows.append((A, profile(A), is_po(A), vs, min_subsidy_unbounded(A)))

    print("   %-9s %-9s %-8s %-6s %-14s %s"
          % ("agent 1", "agent 2", "costs", "PO?", "p in {0,1}^2?", "cheapest p"))
    for A, prof, po, vs, mp in rows:
        print("   %-9s %-9s %-8s %-6s %-14s %s"
              % (bundle(A[0]), bundle(A[1]), prof, po,
                 "yes" if vs else "NO", mp))
    print()

    po_set = [r for r in rows if r[2]]
    valid_set = [r for r in rows if r[3]]
    both = [r for r in rows if r[2] and r[3]]

    print("   Pareto optimal allocations            : %d" % len(po_set))
    for A, prof, _, _, mp in po_set:
        print("      %s %s costs %s, cheapest subsidy %s (total %d)"
              % (bundle(A[0]), bundle(A[1]), prof, mp, sum(mp)))
    print("   allocations valid for the theorem     : %d" % len(valid_set))
    print("   BOTH Pareto optimal and valid         : %d" % len(both))
    print()

    tot_po = min(sum(r[1]) for r in po_set)
    tot_valid = min(sum(r[1]) for r in valid_set)
    print("   least total cost among PO allocations    : %d" % tot_po)
    print("   least total cost among valid allocations : %d" % tot_valid)
    print()

    assert len(both) == 0
    print("CONFIRMED: no allocation is simultaneously Pareto optimal and")
    print("envy-free with a subsidy of at most 1 per agent. The two PO")
    print("allocations both require a subsidy of 2, which the theorem")
    print("forbids; every allocation the theorem allows wastes one unit of")
    print("cost by splitting chores that one agent could absorb for free.")
    print()
    print("So Pareto optimality is not merely missed by Algorithm 1 -- it is")
    print("unattainable under the theorem's guarantee, and no change to the")
    print("algorithm can recover it.")


if __name__ == "__main__":
    main()
