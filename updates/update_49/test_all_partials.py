import itertools, random, sys
from test_permuted_extension import random_dichotomous, permuted_extension_works, full_ef_exists


def all_ef_partials(costs, m, max_leftover=2):
    items = list(range(m))
    out = []
    for rsize in range(0, max_leftover + 1):
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
    rng = random.Random(999)
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    global_fail = 0
    for t in range(trials):
        costs = [random_dichotomous(m, rng) for _ in range(3)]
        partials = all_ef_partials(costs, m, max_leftover=2)
        if not partials:
            print(f"trial {t}: no EF partial with <=2 leftover -- THM 5.1 VIOLATED")
            continue
        any_works = False
        for X, R in partials:
            works, *_ = permuted_extension_works(costs, X, R, m)
            if works:
                any_works = True
                break
        if not any_works:
            global_fail += 1
            print(f"trial {t}: ALL {len(partials)} EF partial allocations (<=2 leftover) FAIL permuted extension!")
            gt, Xg, pg = full_ef_exists(costs, m)
            print(f"   ground truth EF-with-subsidy exists at all: {gt}  witness={Xg} p={pg}")
    print(f"\nDone. {trials} trials at m={m}. instances where EVERY partial allocation fails: {global_fail}")


if __name__ == "__main__":
    main()
