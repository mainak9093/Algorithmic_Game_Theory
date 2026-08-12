"""
Proves Theorem g2-r2 (approach_12.tex, Step 5): the "two leftover items,
doubly stuck" case -- the harder residual left after Lemma g2-free and
Theorem g2-r1 (prove_r1.py) have handled everything else.

Setting: an EF partial allocation (X1, X2, X3) with two leftover items
e1, e2, such that EVERY agent has marginal cost 1 for BOTH e1 and e2 on
their own original bundle (peeling either one off for free, as in
prove_r1.py's easy case, is impossible -- if it were, the leftover set
would shrink to 1 and Theorem g2-r1 would already finish the job).

Strategy tested: send e1 to one bundle and e2 to a DIFFERENT bundle (never
both to the same bundle -- this alone turns out to be enough, so that's all
that's checked here). By the saturation lemma, the question is decided by
the 6 base entries C[i][j] in {0,1,2} plus 12 independent marginal bits
mu[i][e][j] = cost_i(e | X_j) for i != j, e in {1,2} (mu[i][e][i] = 1
forced). This is the minimal, non-redundant parametrisation: each bit is a
genuinely independent query (different agent, different item, or different
target bundle), so no combination is checked twice and none is skipped.

Result: 0 failures out of 3^6 * 2^12 = 2,985,984 combinations, checked
against all 6 ordered choices of target bundles, all 6 permutations, and
all 8 subsidy vectors. Runtime ~20s. See verify_real.py for an independent
confirmation against genuine (non-abstract) random cost functions.
"""
import itertools

AGENTS = (0, 1, 2)
PERMS = list(itertools.permutations(AGENTS))
SUBSIDIES = list(itertools.product((0, 1), repeat=3))
TARGET_PAIRS = [(m1, m2) for m1 in AGENTS for m2 in AGENTS if m1 != m2]


def can_rescue(C, mu):
    def Cget(i, j):
        return 0 if i == j else C[(i, j)]

    def muget(i, e, j):
        return 1 if i == j else mu[(i, e, j)]

    for (m1, m2) in TARGET_PAIRS:
        D = {}
        for i in AGENTS:
            for j in AGENTS:
                val = Cget(i, j)
                if j == m1:
                    val += muget(i, 1, m1)
                if j == m2:
                    val += muget(i, 2, m2)
                D[(i, j)] = val
        for perm in PERMS:
            for p in SUBSIDIES:
                if all(D[(a, perm[a])] - p[a] <= D[(a, perm[b])] - p[b]
                       for a in AGENTS for b in AGENTS):
                    return True, (m1, m2), perm, p
    return False, None, None, None


def run(bound=2):
    offdiag = [(i, j) for i in AGENTS for j in AGENTS if i != j]
    mu_keys = [(i, e, j) for i in AGENTS for e in (1, 2) for j in AGENTS if i != j]
    vals = range(bound + 1)
    total = fails = 0
    for Cvals in itertools.product(vals, repeat=len(offdiag)):
        C = dict(zip(offdiag, Cvals))
        for muvals in itertools.product((0, 1), repeat=len(mu_keys)):
            mu = dict(zip(mu_keys, muvals))
            total += 1
            works, *_ = can_rescue(C, mu)
            if not works:
                fails += 1
                print("COUNTEREXAMPLE:", C, mu)
    print(f"BOUND={bound}: checked {total} combinations, {fails} failures.")
    return fails


if __name__ == "__main__":
    run(2)
