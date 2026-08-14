"""
Independent, non-abstract check of approach_12.tex's proof: generates real
dichotomous cost functions (not the bounded {0,1,2}-entry model used by
prove_r1.py / prove_r2.py), finds genuine EF partial allocations with 1 or 2
leftover items, and confirms the rescue strategy actually works on them.

This does not replace prove_r1.py / prove_r2.py as the proof -- those are
exhaustive over every case the saturation lemma says can occur, which is
already complete. This script is a sanity check that nothing was lost in
translating the real (unbounded) problem into the bounded abstract model.
"""
import itertools
import random


def random_dichotomous(m, rng):
    """A uniformly random dichotomous cost function on m items: c(S) is
    chosen, in increasing order of |S|, uniformly in the range forced by
    monotonicity and unit marginals from the already-chosen subsets."""
    c = {frozenset(): 0}
    for r in range(1, m + 1):
        for S in itertools.combinations(range(m), r):
            S = frozenset(S)
            lo = max(c[S - {b}] for b in S)
            hi = min(c[S - {b}] + 1 for b in S)
            c[S] = rng.randint(lo, hi)
    return c


def ef_partials_with_leftover(costs, m, rsize):
    """All EF partial allocations (X1,X2,X3) leaving exactly `rsize` items unallocated."""
    items = list(range(m))
    out = []
    for R in itertools.combinations(items, rsize):
        Rset = frozenset(R)
        rest = [x for x in items if x not in Rset]
        for coloring in itertools.product(range(3), repeat=len(rest)):
            X = [set() for _ in range(3)]
            for idx, col in zip(rest, coloring):
                X[col].add(idx)
            Xf = [frozenset(x) for x in X]
            costvals = [[costs[i][Xf[j]] for j in range(3)] for i in range(3)]
            if all(costvals[i][i] <= costvals[i][j] for i in range(3) for j in range(3)):
                out.append((Xf, tuple(sorted(R))))
    return out


def is_stuck(costs, X, R):
    """every agent has marginal cost 1 for every leftover item on their OWN bundle"""
    return all(costs[i][X[i] | {e}] - costs[i][X[i]] == 1 for i in range(3) for e in R)


def rescue_r1(costs, X, e, m):
    """placement of e + permutation + subsidy, matching Theorem g2-r1's proof"""
    for target in range(3):
        Y = [set(x) for x in X]
        Y[target] |= {e}
        Yf = [frozenset(y) for y in Y]
        for perm in itertools.permutations(range(3)):
            vals = [[costs[i][Yf[perm[j]]] for j in range(3)] for i in range(3)]
            for p in itertools.product((0, 1), repeat=3):
                if all(vals[i][i] - p[i] <= vals[i][j] - p[j] for i in range(3) for j in range(3)):
                    return True
    return False


def rescue_r2(costs, X, e1, e2, m):
    """e1, e2 -> two DIFFERENT bundles + permutation + subsidy, matching Theorem g2-r2's proof"""
    for m1 in range(3):
        for m2 in range(3):
            if m1 == m2:
                continue
            Y = [set(x) for x in X]
            Y[m1] |= {e1}
            Y[m2] |= {e2}
            Yf = [frozenset(y) for y in Y]
            for perm in itertools.permutations(range(3)):
                vals = [[costs[i][Yf[perm[j]]] for j in range(3)] for i in range(3)]
                for p in itertools.product((0, 1), repeat=3):
                    if all(vals[i][i] - p[i] <= vals[i][j] - p[j] for i in range(3) for j in range(3)):
                        return True
    return False


def main(m=7, trials=300, seed=42):
    rng = random.Random(seed)
    r1_stuck_found = r1_failures = 0
    r2_stuck_found = r2_failures = 0
    for t in range(trials):
        costs = [random_dichotomous(m, rng) for _ in range(3)]

        for X, R in ef_partials_with_leftover(costs, m, 1):
            if is_stuck(costs, X, R):
                r1_stuck_found += 1
                if not rescue_r1(costs, X, R[0], m):
                    r1_failures += 1
                    print(f"trial {t}: Theorem g2-r1 FAILED on X={X} e={R[0]}")

        for X, R in ef_partials_with_leftover(costs, m, 2):
            if is_stuck(costs, X, R):
                r2_stuck_found += 1
                if not rescue_r2(costs, X, R[0], R[1], m):
                    r2_failures += 1
                    print(f"trial {t}: Theorem g2-r2 FAILED on X={X} R={R}")

    print(f"\n{trials} trials at m={m}.")
    print(f"  |R|=1 stuck instances found: {r1_stuck_found}, failures: {r1_failures}")
    print(f"  |R|=2 stuck instances found: {r2_stuck_found}, failures: {r2_failures}")


if __name__ == "__main__":
    import sys
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    main(m, trials)
