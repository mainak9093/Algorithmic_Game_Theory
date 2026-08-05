"""Does multi-restart (shuffled starting order) recover the 14 round-robin
local-search failures found at m=5, n=3?

Run:  python restart_check.py
"""
from itertools import combinations
import random

from targetGbal import size_shift
from targetGbal_local import local_search
from targetGbal_stress import structured_pool
from classify_failures import full_unrestricted_check


def shuffled_local_search(v, items, n, rng, restarts=10):
    from targetGbal_local import round_robin_partition, score
    best = None
    order = list(items)
    for r in range(restarts):
        if r > 0:
            rng.shuffle(order)
        groups = round_robin_partition(order, n)
        key, _ = score(v, groups, n)
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
            return best, r + 1
    return best, restarts


def main():
    m, n = 5, 3
    pool = structured_pool(m)
    rng = random.Random(1)

    found = fixed = 0
    for cs in combinations(pool, n):
        v = [size_shift(c, m) for c in cs]
        success, sp, groups, reason = local_search(v, list(range(m)), n)
        if success:
            continue
        found += 1
        best, restarts_used = shuffled_local_search(v, list(range(m)), n, rng, restarts=10)
        status = "RECOVERED" if best is not None and best <= 1 else "STILL STUCK"
        print("  failure %2d: round-robin spread=%s -> multi-restart spread=%s "
              "(%s, used %d restarts)" % (found, sp, best, status, restarts_used))
        if best is not None and best <= 1:
            fixed += 1

    print("\n%d / %d round-robin failures recovered by multi-restart (<=10 restarts)"
          % (fixed, found))


if __name__ == "__main__":
    main()
