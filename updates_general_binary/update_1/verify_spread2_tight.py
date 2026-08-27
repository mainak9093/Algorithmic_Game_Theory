"""
Approach 15: the constant 2 is TIGHT -- a hand-checkable proof.

existence_spread.py verifies, exhaustively over all 20,337,240 instances at
n=3, m=3, that every general binary instance admits an envy-freeable allocation
with minimal subsidy in {0,1}^n and bundle-size spread at most 2, and that
spread at most 1 fails for 98,931 of them. This script isolates one of those
98,931 and checks it independently, with every routine rewritten from scratch.

THE INSTANCE. n = 3 agents, m = 3 items {a, b, c}.

    a and b are unit chores for everyone.
    c is a unit chore for agent 1 and a unit GOOD for agents 2 and 3.

Concretely v_1(S) = -|S|, and for i in {2,3},

    v_i(S) = -|S cap {a,b}| + [c in S].

Every marginal is in {-1,0,1}, so this is a general binary instance.

WHY NO BALANCED ALLOCATION WORKS -- the argument in one line. At n = 3, m = 3 a
balanced allocation gives every agent exactly one item, so exactly one agent
holds c and the other two hold a chore. At least one of agents 2 and 3 does not
hold c; call her i. She values her own bundle at -1 and the bundle holding c at
+1, so w(i, holder of c) = 1 - (-1) = 2, and her subsidy is at least 2.
Whoever holds c -- agent 1, agent 2 or agent 3 -- some agent of {2,3} is left
holding a chore, so all six balanced allocations fail.

WHY SPREAD 2 SUFFICES HERE. The allocation A_1 = {a}, A_2 = {b,c}, A_3 = {} has
sizes (1,2,0), spread 2, and minimal subsidy (1,0,0).

Both halves are checked below over all 27 allocations, so the claim does not
rest on the prose.
"""
import itertools

N, M = 3, 3
A, B, C = 0, 1, 2
NAMES = "abc"


def v1(S):
    return -bin(S).count("1")


def vi(S):
    """Agents 2 and 3: a and b are chores, c is a good."""
    chores = bin(S & ((1 << A) | (1 << B))).count("1")
    return -chores + (1 if S & (1 << C) else 0)


V = [[v1(S) for S in range(8)],
     [vi(S) for S in range(8)],
     [vi(S) for S in range(8)]]


def marginals_ok(v):
    for S in range(1 << M):
        for k in range(M):
            bit = 1 << k
            if not S & bit and v[S | bit] - v[S] not in (-1, 0, 1):
                return False
    return True


def welfare(bundles, order):
    return sum(V[i][bundles[order[i]]] for i in range(N))


def envy_freeable(bundles):
    base = welfare(bundles, (0, 1, 2))
    return all(welfare(bundles, p) <= base
               for p in itertools.permutations(range(N)))


def subsidy(bundles):
    if not envy_freeable(bundles):
        return None

    def w(i, j):
        return V[i][bundles[j]] - V[i][bundles[i]]

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


def sizes(bundles):
    return [bin(b).count("1") for b in bundles]


def spread(bundles):
    z = sizes(bundles)
    return max(z) - min(z)


def show(mask):
    return "{" + ",".join(NAMES[k] for k in range(M) if mask & (1 << k)) + "}"


def main():
    print("marginals in {-1,0,1}:", [marginals_ok(v) for v in V])
    print()
    for i in range(N):
        print("   agent %d  %s" % (i + 1, str(tuple(V[i]))))
    print()

    print("all 27 allocations:")
    balanced_ok = []
    spread2_ok = []
    for assign in itertools.product(range(N), repeat=M):
        bundles = [0] * N
        for k, owner in enumerate(assign):
            bundles[owner] |= 1 << k
        bundles = tuple(bundles)
        p = subsidy(bundles)
        ok = p is not None and max(p) <= 1
        sp = spread(bundles)
        if ok and sp <= 1:
            balanced_ok.append(bundles)
        if ok and sp <= 2:
            spread2_ok.append(bundles)
        if sp <= 1 or ok:
            print("   %-8s %-8s %-8s  spread=%d  subsidy=%-12s %s"
                  % (show(bundles[0]), show(bundles[1]), show(bundles[2]),
                     sp, "none" if p is None else str(p),
                     "VALID" if ok else ""))
    print()
    print("valid allocations with spread <= 1 : %d" % len(balanced_ok))
    print("valid allocations with spread <= 2 : %d" % len(spread2_ok))
    print()
    if not balanced_ok and spread2_ok:
        print("CONFIRMED: no balanced allocation achieves subsidy <= 1 per")
        print("agent, while spread 2 does. The constant 2 cannot be lowered")
        print("to 1.")


if __name__ == "__main__":
    main()
