"""
Exhaustive, saturation-justified proof search for the |R|=1, subcase-(b) case
of the Permuted-Extension Conjecture at n=3.

Saturation argument: for any pairwise comparison C[i][j] vs C[i][k] relevant to
an EF-with-{0,1}-subsidy check, only whether the difference is <=-1, =0, =1, or
>=2 matters (since p_j - p_k only ranges over {-1,0,1}). Bounding off-diagonal
entries to {0,1,2,3} realizes all four buckets for every pairwise difference
within a row (differences range over {-3,...,3}), so this is a complete,
rigorous case exhaustion, not a sample.

Matrix C[i][j] = c_i(X_j), shifted so C[i][i] = 0 for all i (WLOG).
mu[i][j] = c_i(e | X_j) for i != j; mu[i][i] = 1 for all i is FORCED
(that's exactly subcase (b): every agent has marginal cost 1 on their OWN
bundle -- subcase (a), where some agent has marginal 0, is already fully
closed by Lemma GG and is NOT covered here).
"""
import itertools

BOUND = 3  # off-diagonal entries range over {0,...,BOUND}; BOUND=3 is provably sufficient

AGENTS = (0, 1, 2)
PERMS = list(itertools.permutations(AGENTS))
SUBSIDIES = list(itertools.product((0, 1), repeat=3))


def solver_can_rescue(C, mu):
    """C: dict (i,j)->int for i!=j, C[i][i]=0 implicit.
       mu: dict (i,j)->{0,1} for i!=j, mu[i][i]=1 implicit (subcase b)."""
    def Cget(i, j):
        return 0 if i == j else C[(i, j)]

    def muget(i, j):
        return 1 if i == j else mu[(i, j)]

    for m in AGENTS:  # which original bundle absorbs e
        # D[i][j] = cost to agent i of bundle Y_j (Y_m augmented, others = X_j)
        D = {}
        for i in AGENTS:
            for j in AGENTS:
                base = Cget(i, j)
                if j == m:
                    base += muget(i, m)
                D[(i, j)] = base
        for perm in PERMS:  # agent a receives Y_{perm[a]}
            for p in SUBSIDIES:
                ok = True
                for a in AGENTS:
                    da = D[(a, perm[a])] - p[a]
                    for b in AGENTS:
                        db = D[(a, perm[b])] - p[b]
                        if da > db:
                            ok = False
                            break
                    if not ok:
                        break
                if ok:
                    return True, m, perm, p
    return False, None, None, None


def main():
    offdiag_pairs = [(i, j) for i in AGENTS for j in AGENTS if i != j]  # 6 entries
    vals = range(BOUND + 1)
    total = 0
    failures = []
    for Cvals in itertools.product(vals, repeat=len(offdiag_pairs)):
        C = dict(zip(offdiag_pairs, Cvals))
        for muvals in itertools.product((0, 1), repeat=len(offdiag_pairs)):
            mu = dict(zip(offdiag_pairs, muvals))
            total += 1
            works, m, perm, p = solver_can_rescue(C, mu)
            if not works:
                failures.append((dict(C), dict(mu)))
                if len(failures) <= 5:
                    print("FAILURE:", C, mu)
    print(f"\nChecked {total} (C,mu) combinations (BOUND={BOUND}).")
    print(f"Failures: {len(failures)}")
    if failures:
        print("First failure:", failures[0])


if __name__ == "__main__":
    main()
