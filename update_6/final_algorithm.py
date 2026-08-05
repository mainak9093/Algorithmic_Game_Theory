"""THE algorithm: IMWPM (warm start) + single-item-swap local search (repair),
with restarts as a last resort.  Final combined test.

Run:  python final_algorithm.py
"""
from itertools import combinations, combinations_with_replacement
import random

from targetGbal import subsets, size_shift, gen_functions, rand_dicho, dump
from targetGbal_local import score
from imwpm_raw import imwpm, q_spread


def repair(v, groups, n, max_iters=300):
    key, _ = score(v, groups, n)
    for _ in range(max_iters):
        if key[0] <= 1:
            return True, key[0]
        best_move = None
        for a in range(n):
            for b in range(n):
                if a == b:
                    continue
                for x in groups[a]:
                    trial = list(groups)
                    trial[a] = groups[a] - {x}
                    trial[b] = groups[b] | {x}
                    sizes = [len(g) for g in trial]
                    if max(sizes) - min(sizes) > 1:
                        continue
                    k2, _ = score(v, trial, n)
                    if k2 < key and (best_move is None or k2 < best_move[0]):
                        best_move = (k2, trial)
        if best_move is None:
            return False, key[0]
        key, groups = best_move[0], best_move[1]
    return False, key[0]


def solve(v, items, n, rng, restarts=10):
    """IMWPM warm start, repaired by local search; on failure, restart from
    shuffled round-robin partitions."""
    A = imwpm(v, items, n)
    ok, sp = repair(v, list(A), n)
    if ok:
        return True, sp, 0
    from targetGbal_local import round_robin_partition
    order = list(items)
    for r in range(restarts):
        rng.shuffle(order)
        groups = round_robin_partition(order, n)
        ok, sp = repair(v, groups, n)
        if ok:
            return True, sp, r + 1
    return False, sp, restarts


def main():
    rng = random.Random(8675309)

    print("=== EXHAUSTIVE n=3 m=3 ===")
    F = gen_functions(3)
    fail = 0
    for cs in combinations_with_replacement(F, 3):
        v = [size_shift(c, 3) for c in cs]
        ok, sp, r = solve(v, list(range(3)), 3, rng)
        if not ok:
            fail += 1
    print("  failures: %d / 9880" % fail)

    print("\n=== structured non-additive families, exhaustive triples ===")
    from targetGbal_stress import structured_pool
    tot = badtot = 0
    for m in (3, 4, 5):
        pool = structured_pool(m)
        cnt = bad = 0
        for cs in combinations(pool, 3):
            cnt += 1
            v = [size_shift(c, m) for c in cs]
            ok, sp, r = solve(v, list(range(m)), 3, rng)
            if not ok:
                bad += 1
        print("  m=%d: %d instances, %d failures" % (m, cnt, bad))
        tot += cnt; badtot += bad

    print("\n=== named hard instances ===")
    cases = []
    D = [frozenset({0, 1}), frozenset({0, 2, 3}), frozenset({1, 2, 3})]
    cases.append(("discrepancy cex", 4, 3, [{S: len(S & Ds) for S in subsets(4)} for Ds in D]))
    cases.append(("insertion witness", 3, 3,
                  [{S: max(0, len(S) - 1) for S in subsets(3)},
                   {S: len(S) for S in subsets(3)}, {S: len(S) for S in subsets(3)}]))
    cases.append(("W4 no-go", 2, 3, [{S: len(S) for S in subsets(2)}] * 3))
    RAW = [
        {(): 0, (0,): 1, (1,): 1, (2,): 1, (3,): 1, (0, 1): 2, (0, 2): 1, (0, 3): 2,
         (1, 2): 1, (1, 3): 2, (2, 3): 2, (0, 1, 2): 2, (0, 1, 3): 3, (0, 2, 3): 2,
         (1, 2, 3): 2, (0, 1, 2, 3): 3},
        {(): 0, (0,): 1, (1,): 1, (2,): 1, (3,): 1, (0, 1): 2, (0, 2): 2, (0, 3): 2,
         (1, 2): 2, (1, 3): 2, (2, 3): 1, (0, 1, 2): 3, (0, 1, 3): 2, (0, 2, 3): 2,
         (1, 2, 3): 2, (0, 1, 2, 3): 3},
        {(): 0, (0,): 1, (1,): 1, (2,): 0, (3,): 1, (0, 1): 2, (0, 2): 1, (0, 3): 2,
         (1, 2): 1, (1, 3): 2, (2, 3): 1, (0, 1, 2): 2, (0, 1, 3): 2, (0, 2, 3): 2,
         (1, 2, 3): 2, (0, 1, 2, 3): 3},
    ]
    cases.append(("mswcex", 4, 3, [{frozenset(k): v for k, v in d.items()} for d in RAW]))
    hardfail = 0
    for name, mm, nn, cs in cases:
        v = [size_shift(c, mm) for c in cs]
        ok, sp, r = solve(v, list(range(mm)), nn, rng)
        print("  [%s] %s spread=%s restarts=%d" % (name, "OK" if ok else "FAIL", sp, r))
        if not ok:
            hardfail += 1

    print("\n=== randomised, up to n=8 m=10 ===")
    randfail = 0; randtot = 0
    for (nn, mm, T) in [(3, 4, 400), (3, 5, 200), (3, 6, 100), (4, 4, 200),
                        (4, 5, 100), (5, 5, 60), (6, 6, 40), (6, 8, 20),
                        (7, 7, 20), (8, 8, 15)]:
        f = 0
        for _ in range(T):
            cs = [rand_dicho(mm, rng, rng.choice([0.0, 0.1, 0.5, 0.9, 1.0])) for _ in range(nn)]
            v = [size_shift(c, mm) for c in cs]
            ok, sp, r = solve(v, list(range(mm)), nn, rng)
            if not ok:
                f += 1
        randfail += f; randtot += T
        print("  n=%d m=%d T=%d : %d failures" % (nn, mm, T, f))

    print("\n===============================================================")
    print("GRAND TOTAL FAILURES: exhaustive n=m=3: %d/9880 | structured: %d/%d | "
          "hard: %d/%d | random: %d/%d"
          % (fail, badtot, tot, hardfail, len(cases), randfail, randtot))
    print("OVERALL: %d / %d"
          % (fail + badtot + hardfail + randfail, 9880 + tot + len(cases) + randtot))


if __name__ == "__main__":
    main()
