"""
Proves Theorem g2-r1 (approach_12.tex, Step 4): the "one leftover item" case.

Setting: an EF partial allocation (X1, X2, X3) for 3 agents, with a single
leftover item e such that every agent has marginal cost 1 for e on their own
bundle (the "stuck" case -- otherwise Lemma g2-free settles it trivially).

By the saturation lemma (approach_12.tex, Step 3), the only thing that
matters about the cost table is, after shifting each row so the diagonal is
0: the 6 off-diagonal base entries C[i][j] = cost_i(X_j), confined to
{0,1,2} (sufficient range -- see the lemma's proof), and 6 marginal bits
mu[i][j] = cost_i(e | X_j) for i != j (mu[i][i] = 1 is forced by the stuck
case). This script exhaustively enumerates all 3^6 * 2^6 = 46,656 such
combinations and checks, for each, whether SOME choice of (i) which bundle
absorbs e, (ii) a permutation of the 3 resulting bundles to the 3 agents,
and (iii) a subsidy vector in {0,1}^3, gives an envy-free allocation.

Result: 0 failures out of 46,656 -- a complete proof, not a sample, given
the saturation lemma. Also cross-checked with BOUND=3 and BOUND=4 (strictly
more cases, same zero-failure result), confirming BOUND=2 was already enough.
"""
import itertools

AGENTS = (0, 1, 2)
PERMS = list(itertools.permutations(AGENTS))
SUBSIDIES = list(itertools.product((0, 1), repeat=3))


def can_rescue(C, mu):
    """C[(i,j)] = cost_i(X_j) for i != j, diagonal 0 implicit.
       mu[(i,j)] = cost_i(e | X_j) for i != j, mu[i][i] = 1 implicit."""
    def Cget(i, j):
        return 0 if i == j else C[(i, j)]

    def muget(i, j):
        return 1 if i == j else mu[(i, j)]

    for m in AGENTS:  # which bundle absorbs e
        D = {(i, j): Cget(i, j) + (muget(i, m) if j == m else 0)
             for i in AGENTS for j in AGENTS}
        for perm in PERMS:  # agent a receives bundle perm[a]
            for p in SUBSIDIES:
                if all(D[(a, perm[a])] - p[a] <= D[(a, perm[b])] - p[b]
                       for a in AGENTS for b in AGENTS):
                    return True, m, perm, p
    return False, None, None, None


def run(bound):
    offdiag = [(i, j) for i in AGENTS for j in AGENTS if i != j]
    vals = range(bound + 1)
    total = fails = 0
    for Cvals in itertools.product(vals, repeat=len(offdiag)):
        C = dict(zip(offdiag, Cvals))
        for muvals in itertools.product((0, 1), repeat=len(offdiag)):
            mu = dict(zip(offdiag, muvals))
            total += 1
            works, *_ = can_rescue(C, mu)
            if not works:
                fails += 1
                print("COUNTEREXAMPLE:", C, mu)
    print(f"BOUND={bound}: checked {total} combinations, {fails} failures.")
    return fails


if __name__ == "__main__":
    for b in (2, 3, 4):
        run(b)
