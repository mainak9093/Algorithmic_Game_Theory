"""
|R|=2, "doubly-stuck" case: every agent has marginal 1 for EVERY leftover item
on their OWN original bundle (else Lemma GG peels one item off for free and we
land in the already-proven |R|=1 theorem -- see exhaustive_r1.py).

Test SHAPE B: e1 -> bundle m1, e2 -> bundle m2, with m1 != m2 (both chosen
freely by the solver, 6 ordered pairs). Minimal free-parameter set (no
redundancy across choices of (m1,m2), unlike the first draft):

  C[i][j]      = c_i(X_j) for i != j, C[i][i] = 0 (shift), entries in {0,1,2}
                 (BOUND=2 -- independently verified sufficient for |R|=1, same
                 4-bucket saturation argument applies here).
  mu[(i,e,j)]  = c_i(e | X_j) for i != j, e in {1,2}  (i's marginal cost for
                 leftover item e when added to agent j's ORIGINAL bundle).
                 mu[(i,e,i)] = 1 is forced for all i,e (doubly-stuck).

This is the true minimal parametrization: 6 C-entries + 12 mu-bits, each
agent's cost function independent of the others', each (i,e,j) query
independent of every other since X_j's are disjoint sets not otherwise
constrained by monotonicity. Any failure found here should be checked for
realizability as an actual dichotomous cost function before being treated as
a genuine counterexample (belt and suspenders), but the parametrization is
designed to already be realizable by construction (threshold/AND gadgets, as
used for the hand-built witness in RESIDUAL.md 7.16.32).
"""
import itertools

BOUND = 2
AGENTS = (0, 1, 2)
PERMS = list(itertools.permutations(AGENTS))
SUBSIDIES = list(itertools.product((0, 1), repeat=3))
ORDERED_TARGET_PAIRS = [(m1, m2) for m1 in AGENTS for m2 in AGENTS if m1 != m2]


def solver_can_rescue_shapeB(C, mu):
    def Cget(i, j):
        return 0 if i == j else C[(i, j)]

    def muget(i, e, j):
        return 1 if i == j else mu[(i, e, j)]

    for (m1, m2) in ORDERED_TARGET_PAIRS:
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
                ok = True
                for a in AGENTS:
                    da = D[(a, perm[a])] - p[a]
                    for b in AGENTS:
                        if da > D[(a, perm[b])] - p[b]:
                            ok = False
                            break
                    if not ok:
                        break
                if ok:
                    return True, (m1, m2), perm, p
    return False, None, None, None


def main(limit_C=None):
    offdiag_pairs = [(i, j) for i in AGENTS for j in AGENTS if i != j]
    mu_keys = [(i, e, j) for i in AGENTS for e in (1, 2) for j in AGENTS if i != j]  # 12 keys
    vals = range(BOUND + 1)
    total = 0
    fails = 0
    fail_examples = []
    Cspace = list(itertools.product(vals, repeat=len(offdiag_pairs)))
    if limit_C:
        Cspace = Cspace[:limit_C]
    for Cvals in Cspace:
        C = dict(zip(offdiag_pairs, Cvals))
        for muvals in itertools.product((0, 1), repeat=len(mu_keys)):
            mu = dict(zip(mu_keys, muvals))
            total += 1
            works, *_ = solver_can_rescue_shapeB(C, mu)
            if not works:
                fails += 1
                if len(fail_examples) < 5:
                    fail_examples.append((dict(C), dict(mu)))
    print(f"BOUND={BOUND}, |C-space|={len(Cspace)}: total={total} fails={fails}")
    for ex in fail_examples:
        print("  FAIL:", ex)


if __name__ == "__main__":
    import sys
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    main(limit)
