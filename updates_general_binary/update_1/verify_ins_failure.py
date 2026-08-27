"""
Approach 15: independent re-check of the (INS) failure witness found by
test_insertion.py.

The claim being checked is a negative one, so it is re-verified here with the
envy-graph routines REIMPLEMENTED FROM SCRATCH rather than imported, so that a
bug in gb_valuations.py cannot produce the finding and then confirm it.

THE WITNESS. n = 3 agents, m = 3 chores {a, b, c}, all valuations negative
dichotomous (every marginal in {-1,0}):

    v_1(S) = -|S|
    v_2(S) = -|S|
    v_3: 0, a:-1, b:0, ab:-1, c:-1, ac:-1, bc:-1, abc:-2

State: agent 3 holds {a, c}; agents 1 and 2 hold nothing; chore b is
unallocated. That state is an envy-free solution whose MINIMAL subsidy is
(0, 0, 1), so it is exactly the kind of state (INS) quantifies over.

CLAIM. No recipient and no reassignment of the resulting bundles keeps the
minimal subsidy within {0,1}^3 once b is inserted. All 3 x 6 = 18 options are
printed with their verdicts.

WHY THIS IS NOT A COUNTEREXAMPLE TO THE CONJECTURE. The script also solves the
complete instance directly: some complete allocation of {a,b,c} does achieve
max subsidy 1. So the conjecture is untouched here -- what fails is the
INCREMENTAL ROUTE, the one-item-at-a-time induction that BKNS uses on goods.
The chores theorem is true but cannot be reached this way, which is consistent
with our own proof of it being one-shot (a partial allocation, then a
completion) rather than an induction on items.
"""
import itertools

N, M = 3, 3
A, B, C = 0, 1, 2


def unit(mask):
    return -bin(mask).count("1")


V = [
    [unit(S) for S in range(8)],
    [unit(S) for S in range(8)],
    [0, -1, 0, -1, -1, -1, -1, -2],
]


def check_negative_dichotomous(v):
    for S in range(8):
        for b in range(M):
            bit = 1 << b
            if not S & bit and v[S | bit] - v[S] not in (-1, 0):
                return False
    return True


# -------- envy-graph routines, written independently of gb_valuations -------

def welfare(bundles, order):
    """Welfare when agent i receives bundles[order[i]]."""
    return sum(V[i][bundles[order[i]]] for i in range(N))


def envy_freeable(bundles):
    """No reassignment of these bundles beats the identity (Halpern-Shah ii)."""
    base = welfare(bundles, (0, 1, 2))
    return all(welfare(bundles, p) <= base
               for p in itertools.permutations(range(N)))


def subsidy(bundles):
    """
    Minimal subsidy p*_i = heaviest directed path out of i, computed by
    explicit enumeration of every simple path in the complete digraph on 3
    vertices. Returns None if the allocation is not envy-freeable.
    """
    if not envy_freeable(bundles):
        return None

    def w(i, j):
        return V[i][bundles[j]] - V[i][bundles[i]]

    p = []
    for i in range(N):
        others = [j for j in range(N) if j != i]
        best = 0
        for j in others:
            best = max(best, w(i, j))
            for k in others:
                if k != j:
                    best = max(best, w(i, j) + w(j, k))
        p.append(best)
    return p


def show(mask):
    return "{" + ",".join("abc"[b] for b in range(M) if mask & (1 << b)) + "}"


def show_all(bundles):
    return " ".join("A%d=%-6s" % (i + 1, show(b)) for i, b in enumerate(bundles))


def main():
    print("valuations negative dichotomous:",
          [check_negative_dichotomous(v) for v in V])
    print()

    start = (0, 0, (1 << A) | (1 << C))
    p0 = subsidy(start)
    print("start   %s" % show_all(start))
    print("        envy-freeable = %s, minimal subsidy = %s, in {0,1}^n = %s"
          % (envy_freeable(start), p0,
             p0 is not None and all(q <= 1 for q in p0)))
    print("        chore b is unallocated")
    print()

    print("insert b -- every recipient, every reassignment:")
    good = []
    for x in range(N):
        grown = tuple(b | (1 << B) if i == x else b
                      for i, b in enumerate(start))
        for perm in itertools.permutations(range(N)):
            cand = tuple(grown[perm[i]] for i in range(N))
            p = subsidy(cand)
            if p is None:
                verdict = "not envy-freeable"
            elif all(q <= 1 for q in p):
                verdict = "OK"
                good.append((x, perm, cand, p))
            else:
                verdict = "subsidy %d" % max(p)
            print("   b->agent %d  perm %s  %s  %s"
                  % (x + 1, str(perm), show_all(cand), verdict))
    print()
    print("options keeping the subsidy in {0,1}^3: %d" % len(good))
    print("(INS) fails at this state: %s" % (len(good) == 0))
    print()

    print("but the COMPLETE instance is fine -- best over all 27 allocations:")
    best, best_bundles = None, None
    for assign in itertools.product(range(N), repeat=M):
        bundles = [0] * N
        for k, owner in enumerate(assign):
            bundles[owner] |= 1 << k
        bundles = tuple(bundles)
        p = subsidy(bundles)
        if p is None:
            continue
        if best is None or max(p) < best:
            best, best_bundles = max(p), bundles
    print("   %s  max subsidy = %d" % (show_all(best_bundles), best))
    print()
    print("so the conjecture holds on this instance; what fails is the")
    print("one-item-at-a-time induction, not the theorem.")


if __name__ == "__main__":
    main()
