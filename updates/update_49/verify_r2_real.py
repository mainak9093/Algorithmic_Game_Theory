import itertools, random, sys
from test_permuted_extension import random_dichotomous, full_ef_exists


def ef_partials_exact_r(costs, m, rsize):
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
            ef = all(costvals[i][i] <= costvals[i][j] for i in range(3) for j in range(3))
            if ef:
                out.append((Xf, tuple(sorted(R))))
    return out


def is_doubly_stuck(costs, X, R):
    """every agent i has marginal cost 1 for EVERY leftover item on their OWN bundle X[i]"""
    for i in range(3):
        for e in R:
            marg = costs[i][X[i] | {e}] - costs[i][X[i]]
            if marg == 0:
                return False
    return True


def shapeB_rescue(costs, X, R, m):
    """try: e1 -> bundle m1, e2 -> bundle m2 (m1 != m2), all 6 target pairs,
       all 6 perms, all 8 subsidies. R must have exactly 2 items."""
    e1, e2 = R
    for m1 in range(3):
        for m2 in range(3):
            if m1 == m2:
                continue
            Y = [set(x) for x in X]
            Y[m1] = Y[m1] | {e1}
            Y[m2] = Y[m2] | {e2}
            Yf = [frozenset(y) for y in Y]
            for perm in itertools.permutations(range(3)):
                costvals = [[costs[i][Yf[perm[j]]] for j in range(3)] for i in range(3)]
                for p in itertools.product((0, 1), repeat=3):
                    ok = True
                    for i in range(3):
                        for j in range(3):
                            if costvals[i][i] - p[i] > costvals[i][j] - p[j]:
                                ok = False
                                break
                        if not ok:
                            break
                    if ok:
                        return True, Yf, perm, p
    return False, None, None, None


def main():
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 2024
    rng = random.Random(seed)
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 500
    doubly_stuck_found = 0
    shapeB_failures = 0
    for t in range(trials):
        costs = [random_dichotomous(m, rng) for _ in range(3)]
        partials = ef_partials_exact_r(costs, m, 2)
        stuck_here = False
        for X, R in partials:
            if is_doubly_stuck(costs, X, R):
                stuck_here = True
                doubly_stuck_found += 1
                works, *_ = shapeB_rescue(costs, X, R, m)
                if not works:
                    shapeB_failures += 1
                    print(f"trial {t}: SHAPE-B FAILED on a real doubly-stuck instance!")
                    print(f"   X={X} R={R}")
                    gt, Xg, pg = full_ef_exists(costs, m)
                    print(f"   ground truth exists: {gt} witness={Xg} p={pg}")
        if t % 50 == 0:
            print(f"...trial {t}, doubly-stuck found so far: {doubly_stuck_found}, shapeB failures: {shapeB_failures}")
    print(f"\nDone. {trials} trials at m={m}. doubly-stuck instances found: {doubly_stuck_found}. shapeB failures: {shapeB_failures}")


if __name__ == "__main__":
    main()
