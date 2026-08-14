import itertools, random, sys

def random_dichotomous(m, rng):
    c = {frozenset(): 0}
    for r in range(1, m + 1):
        for S in itertools.combinations(range(m), r):
            S = frozenset(S)
            lo = max(c[S - {b}] for b in S)
            hi = min(c[S - {b}] + 1 for b in S)
            c[S] = rng.randint(lo, hi)
    return c


def find_ef_partial(costs, m, max_leftover=2):
    """Brute force: find R (|R|<=max_leftover) and an EF 3-partition of the rest."""
    items = list(range(m))
    for rsize in range(0, max_leftover + 1):
        for R in itertools.combinations(items, rsize):
            Rset = frozenset(R)
            rest = [x for x in items if x not in Rset]
            # brute force 3-colourings of rest
            for coloring in itertools.product(range(3), repeat=len(rest)):
                X = [set() for _ in range(3)]
                for idx, col in zip(rest, coloring):
                    X[col].add(idx)
                Xf = [frozenset(x) for x in X]
                costvals = [[costs[i][Xf[j]] for j in range(3)] for i in range(3)]
                ef = all(costvals[i][i] <= costvals[i][j] for i in range(3) for j in range(3))
                if ef:
                    return Xf, Rset
    return None, None


def full_ef_exists(costs, m, subsidy_set=(0, 1)):
    """Ground truth brute force over ALL partitions & subsidies."""
    items = list(range(m))
    for coloring in itertools.product(range(3), repeat=m):
        X = [set() for _ in range(3)]
        for idx, col in zip(items, coloring):
            X[col].add(idx)
        Xf = [frozenset(x) for x in X]
        costvals = [[costs[i][Xf[j]] for j in range(3)] for i in range(3)]
        for p in itertools.product(subsidy_set, repeat=3):
            ok = True
            for i in range(3):
                for j in range(3):
                    if costvals[i][i] - p[i] > costvals[i][j] - p[j]:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                return True, Xf, p
    return False, None, None


def permuted_extension_works(costs, X, R, m):
    """Try: assign leftover items R to bundles (all ways), permute bundles to agents,
    apply subsidy in {0,1}^3. Return True if any combo achieves EF."""
    Rlist = list(R)
    k = len(Rlist)
    base = [set(x) for x in X]
    # all ways to distribute R among the 3 bundles
    for assign in itertools.product(range(3), repeat=k):
        Y = [set(b) for b in base]
        for item, dest in zip(Rlist, assign):
            Y[dest].add(item)
        Yf = [frozenset(y) for y in Y]
        for perm in itertools.permutations(range(3)):
            # agent i receives Y[perm[i]]
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
    rng = random.Random(12345)
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    fails = 0
    no_ground_truth = 0
    for t in range(trials):
        costs = [random_dichotomous(m, rng) for _ in range(3)]
        X, R = find_ef_partial(costs, m, max_leftover=2)
        if X is None:
            print(f"trial {t}: NO EF partial allocation with <=2 leftover found -- Theorem 5.1 violated?!")
            no_ground_truth += 1
            continue
        works, Yf, perm, p = permuted_extension_works(costs, X, R, m)
        if not works:
            fails += 1
            print(f"trial {t}: permuted extension FAILED. X={X}, R={R}")
            gt, Xg, pg = full_ef_exists(costs, m)
            print(f"   ground truth EF-with-subsidy exists: {gt}")
            if gt:
                print(f"   witness: {Xg} p={pg}")
    print(f"\nDone. {trials} trials at m={m}. permuted-extension failures: {fails}. no-partial-found: {no_ground_truth}")


if __name__ == "__main__":
    main()
