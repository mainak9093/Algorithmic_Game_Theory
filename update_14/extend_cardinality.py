"""Does BKNS EXTEND ever choose to grow a bundle that is NOT of minimum
cardinality, even when a min-cardinality bundle is available in M(q) with a
valid marginal-1 option? Search over random positive dichotomous instances,
build a partial allocation, and inspect ALL extend_options."""
import itertools, random, sys
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'update_6'))
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
    found = 0
    for t in range(trials):
        v = [random_dichotomous(m, rng) for _ in range(n)]
        items = list(range(m))
        rng.shuffle(items)
        # build a partial allocation by naive greedy extend on a random prefix
        A = [frozenset() for _ in range(n)]
        p = [0] * n
        k_used = rng.randint(1, m - 1)
        placed = []
        for g in items[:k_used]:
            opts = extend_options(v, A, p, g, n)
            if not opts:
                break
            rho, kk = rng.choice(opts)
            A = [A[rho[i]] for i in range(n)]
            A[kk] = A[kk] | {g}
            p = compute_p(v, A, n)
            placed.append(g)
        if len(placed) < 1:
            continue
        g = items[len(placed)] if len(placed) < m else None
        if g is None:
            continue
        opts = extend_options(v, A, p, g, n)
        if not opts:
            continue
        sizes = [len(b) for b in A]
        min_size = min(sizes)
        Mp = set(M_of_p(p, n))
        # is there a min-cardinality agent in M(q) with SOME valid option?
        min_in_Mp_with_option = any(
            (kk == l or True) and sizes[l] == min_size and l in Mp
            for (rho, kk) in opts for l in [rho[kk]]
        )
        # does EVERY option target a min-cardinality bundle?
        all_targets_min = all(sizes[rho[kk]] == min_size for (rho, kk) in opts)
        if not all_targets_min:
            found += 1
            if found <= 3:
                print(f"  trial {t}: EXTEND has options NOT targeting min-cardinality bundle")
                print(f"    sizes={sizes} min_size={min_size} M(q)={sorted(Mp)}")
                for (rho, kk) in opts:
                    print(f"      option: agent {kk} grows bundle {rho[kk]} (size {sizes[rho[kk]]})")
    print(f"n={n} m={m} trials={trials} seed={seed}: cases with a non-min-cardinality EXTEND option = {found}")


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
