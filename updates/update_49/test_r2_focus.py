import itertools, random, sys
from test_permuted_extension import random_dichotomous, permuted_extension_works, full_ef_exists


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
                out.append((Xf, Rset))
    return out


def main():
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 777
    rng = random.Random(seed)
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    global_fail = 0
    checked = 0
    for t in range(trials):
        costs = [random_dichotomous(m, rng) for _ in range(3)]
        partials = ef_partials_exact_r(costs, m, 2)
        if not partials:
            continue  # this instance has no |R|=2 EF partial; irrelevant to this focused test
        checked += 1
        any_works = False
        for X, R in partials:
            works, *_ = permuted_extension_works(costs, X, R, m)
            if works:
                any_works = True
                break
        if not any_works:
            global_fail += 1
            print(f"trial {t}: ALL {len(partials)} |R|=2 EF partials FAIL permuted extension!")
            gt, Xg, pg = full_ef_exists(costs, m)
            print(f"   ground truth: {gt} witness={Xg} p={pg}")
    print(f"\nDone. {trials} trials (m={m}, seed={seed}); {checked} had an |R|=2 partial; failures: {global_fail}")


if __name__ == "__main__":
    main()
