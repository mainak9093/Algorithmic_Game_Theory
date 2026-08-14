"""Sharper test: does there exist a partial-allocation state where EXTEND has
at least one valid option, but NONE of them target a minimum-cardinality
bundle? This is the case where Step 1's restriction ("assign only to a
min-cardinality bundle when unbalanced") has NOTHING legal to choose --
not a suboptimal choice, an EMPTY choice set."""
import itertools, random, sys
from guidedR3 import extend_options, M_of_p, compute_p


def random_dichotomous(m, rng):
    c = {frozenset(): 0}
    for r in range(1, m + 1):
        for S in itertools.combinations(range(m), r):
            S = frozenset(S)
            lo = max(c[S - {b}] for b in S)
            hi = min(c[S - {b}] + 1 for b in S)
            c[S] = rng.randint(lo, hi)
    return c


def main(n, m, trials, seed):
    rng = random.Random(seed)
    forced = 0
    for t in range(trials):
        v = [random_dichotomous(m, rng) for _ in range(n)]
        items = list(range(m))
        rng.shuffle(items)
        A = [frozenset() for _ in range(n)]
        p = [0] * n
        for step, g in enumerate(items[:-1]):
            opts = extend_options(v, A, p, g, n)
            if not opts:
                break
            sizes = [len(b) for b in A]
            min_size = min(sizes)
            opts_to_min = [(rho, kk) for (rho, kk) in opts if len(A[rho[kk]]) == min_size]
            if not opts_to_min and any(len(b) != sizes[0] for b in A):
                forced += 1
                if forced <= 3:
                    print(f"  trial {t} step {step}: NO extend option targets a min-cardinality bundle!")
                    print(f"    sizes={sizes}  options target sizes={[len(A[rho[kk]]) for rho,kk in opts]}")
            rho, kk = rng.choice(opts)
            A = [A[rho[i]] for i in range(n)]
            A[kk] = A[kk] | {g}
            p = compute_p(v, A, n)
    print(f"n={n} m={m} trials={trials} seed={seed}: states where EXTEND is FORCED off min-cardinality = {forced}")


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
