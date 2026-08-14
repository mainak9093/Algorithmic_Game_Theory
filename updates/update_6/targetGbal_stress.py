"""Push the local-search algorithm harder: larger n/m, structured adversarial
families (not just endpoint-constant random), and multiple random restarts to
check sensitivity to the starting partition.

Run:  python targetGbal_stress.py
"""
from itertools import combinations
import random

from targetGbal import subsets, size_shift, rand_dicho
from targetGbal_local import local_search, round_robin_partition


def as_dict(m, f):
    return {S: f(S) for S in subsets(m)}


def is_dich(m, c):
    if c[frozenset()] != 0:
        return False
    for S in subsets(m):
        for g in range(m):
            if g not in S and c[S | {g}] - c[S] not in (0, 1):
                return False
    return True


def structured_pool(m):
    pool = []
    for r in range(0, m + 1):
        for D in combinations(range(m), r):
            Ds = frozenset(D)
            pool.append(as_dict(m, lambda S, Ds=Ds: len(S & Ds)))
            if r >= 1:
                pool.append(as_dict(m, lambda S, Ds=Ds: min(len(S & Ds), 1)))
            for k in range(1, max(r, 1)):
                pool.append(as_dict(m, lambda S, Ds=Ds, k=k: max(0, len(S & Ds) - k)))
                pool.append(as_dict(m, lambda S, Ds=Ds, k=k: min(len(S & Ds), k)))
    seen, uniq = set(), []
    for c in pool:
        if not is_dich(m, c):
            continue
        key = tuple(sorted((tuple(sorted(k)), v) for k, v in c.items()))
        if key not in seen:
            seen.add(key); uniq.append(c)
    return uniq


def multi_start_local_search(v, items, n, rng, restarts=5):
    """Round-robin start plus a few random-shuffle starts; report the best."""
    best = None
    order = list(items)
    for r in range(restarts):
        if r > 0:
            rng.shuffle(order)
        groups0 = round_robin_partition(order, n)
        # reuse local_search's engine by monkey-starting from groups0
        from targetGbal_local import score
        key, info = score(v, groups0, n)
        groups = groups0
        for _ in range(300):
            if key[0] <= 1:
                break
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
                break
            key, groups = best_move[0], best_move[1]
        if best is None or key[0] < best:
            best = key[0]
        if best <= 1:
            return best
    return best


def main():
    rng = random.Random(24601)

    print("=== structured non-additive families, exhaustive triples ===")
    fails = 0
    total = 0
    for m in (3, 4, 5):
        pool = structured_pool(m)
        print("  m=%d: %d structured functions" % (m, len(pool)))
        cnt = bad = 0
        for cs in combinations(pool, 3):
            cnt += 1
            v = [size_shift(c, m) for c in cs]
            success, sp, groups, reason = local_search(v, list(range(m)), 3)
            if not success:
                bad += 1
        print("    n=3: %d instances, %d local-search failures" % (cnt, bad))
        fails += bad
        total += cnt

    print("\n=== larger n, larger m, endpoint-constant random ===")
    for (n, m, T) in [(6, 6, 60), (6, 8, 30), (7, 7, 30), (8, 8, 15), (5, 10, 20)]:
        bad = 0
        for _ in range(T):
            cs = [rand_dicho(m, rng, rng.choice([0.0, 0.1, 0.5, 0.9, 1.0])) for _ in range(n)]
            v = [size_shift(c, m) for c in cs]
            success, sp, groups, reason = local_search(v, list(range(m)), n)
            if not success:
                bad += 1
        fails += bad
        total += T
        print("  n=%d m=%d T=%d : %d failures" % (n, m, T, bad))

    print("\n=== sensitivity to starting partition (multi-restart), n=4,m=6 ===")
    single_fail = multi_fail = 0
    T = 200
    for _ in range(T):
        cs = [rand_dicho(6, rng, rng.choice([0.0, 0.1, 0.5, 0.9, 1.0])) for _ in range(4)]
        v = [size_shift(c, 6) for c in cs]
        success, sp, groups, reason = local_search(v, list(range(6)), 4)
        if not success:
            single_fail += 1
            best = multi_start_local_search(v, list(range(6)), 4, rng, restarts=5)
            if best is None or best > 1:
                multi_fail += 1
    print("  round-robin-only failures : %d / %d" % (single_fail, T))
    print("  still failing after 5 restarts : %d / %d" % (multi_fail, T))

    print("\n===============================================================")
    print("TOTAL local-search failures across this stress run: %d / %d" % (fails, total))


if __name__ == "__main__":
    main()
