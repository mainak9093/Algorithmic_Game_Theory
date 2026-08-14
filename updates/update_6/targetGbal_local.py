"""Can a cheap SINGLE-ITEM-SWAP local search find a good balanced partition,
instead of the exhaustive enumeration in targetGbal.py?

Start from an arbitrary balanced partition (round-robin by item index), take
its optimal (max-weight) matching to agents, and repeatedly swap one item
between two groups whenever a swap strictly improves (spread, -welfare)
lexicographically, re-optimizing the matching after each swap.  Report whether
this always reaches spread <= 1, or gets stuck the way single-transfer local
search did on the utilitarian-optimal set in Approach 2.

Run:  python targetGbal_local.py
"""
from itertools import combinations, combinations_with_replacement, permutations
import random

from targetGbal import (subsets, gen_functions, rand_dicho, size_shift,
                        q_of, best_matching, dump)


def round_robin_partition(items, n):
    groups = [[] for _ in range(n)]
    for idx, g in enumerate(items):
        groups[idx % n].append(g)
    return [frozenset(g) for g in groups]


def score(v, groups, n):
    res = best_matching(v, groups, n)
    if res is None:
        return (10 ** 9, 10 ** 9), None
    sp, matched_groups, p, q = res
    welfare = sum(v[i][matched_groups[i]] for i in range(n))
    return (sp, -welfare), (matched_groups, p, q)


def local_search(v, items, n, max_iters=200):
    groups = round_robin_partition(items, n)
    key, info = score(v, groups, n)
    for _ in range(max_iters):
        if key[0] <= 1:
            return True, key[0], groups, 0
        improved = False
        best_move = None
        for a in range(n):
            for b in range(n):
                if a == b:
                    continue
                for x in groups[a]:
                    trial = list(groups)
                    trial[a] = groups[a] - {x}
                    trial[b] = groups[b] | {x}
                    # keep sizes within 1 of each other (stay "balanced enough")
                    sizes = [len(g) for g in trial]
                    if max(sizes) - min(sizes) > 1:
                        continue
                    k2, info2 = score(v, trial, n)
                    if k2 < key:
                        if best_move is None or k2 < best_move[0]:
                            best_move = (k2, trial)
        if best_move is None:
            return False, key[0], groups, 1     # stuck: local optimum, not good enough
        key, groups = best_move[0], best_move[1]
    return False, key[0], groups, 2              # ran out of iterations


def main():
    print("=== EXHAUSTIVE n=3 m=3, local search from round-robin start ===")
    F = gen_functions(3)
    ok = stuck = timeout = 0
    stuck_example = None
    for cs in combinations_with_replacement(F, 3):
        v = [size_shift(c, 3) for c in cs]
        success, sp, groups, reason = local_search(v, list(range(3)), 3)
        if success:
            ok += 1
        elif reason == 1:
            stuck += 1
            if stuck_example is None:
                stuck_example = (list(cs), sp, groups)
        else:
            timeout += 1
    print("  reached spread<=1 : %d / 9880" % ok)
    print("  stuck at local optimum with spread>1 : %d" % stuck)
    print("  exhausted iteration budget : %d" % timeout)
    if stuck_example:
        cs, sp, groups = stuck_example
        print("\n  first stuck instance: spread=%d groups=%s" % (sp, [sorted(g) for g in groups]))
        dump(cs, 3, 3)

    print("\n=== NAMED HARD INSTANCES ===")
    cases = []
    D = [frozenset({0, 1}), frozenset({0, 2, 3}), frozenset({1, 2, 3})]
    cases.append(("discrepancy cex", 4, 3, [{S: len(S & Ds) for S in subsets(4)} for Ds in D]))
    cases.append(("insertion witness", 3, 3,
                  [{S: max(0, len(S) - 1) for S in subsets(3)},
                   {S: len(S) for S in subsets(3)}, {S: len(S) for S in subsets(3)}]))
    cases.append(("W4 no-go", 2, 3, [{S: len(S) for S in subsets(2)}] * 3))
    cases.append(("guidedR3 reachability-gap instance", 3, 3,
                  [{frozenset(): 0, frozenset({0}): 0, frozenset({1}): 0, frozenset({2}): 0,
                    frozenset({0, 1}): 0, frozenset({0, 2}): 0, frozenset({1, 2}): 0,
                    frozenset({0, 1, 2}): 0},
                   {frozenset(): 0, frozenset({0}): 0, frozenset({1}): 0, frozenset({2}): 0,
                    frozenset({0, 1}): 1, frozenset({0, 2}): 1, frozenset({1, 2}): 1,
                    frozenset({0, 1, 2}): 1},
                   {frozenset(): 0, frozenset({0}): 1, frozenset({1}): 1, frozenset({2}): 1,
                    frozenset({0, 1}): 2, frozenset({0, 2}): 2, frozenset({1, 2}): 2,
                    frozenset({0, 1, 2}): 2}]))
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
        success, sp, groups, reason = local_search(v, list(range(mm)), nn)
        status = "OK" if success else ("STUCK" if reason == 1 else "TIMEOUT")
        print("  [%s] n=%d m=%d  spread=%d  %s" % (name, nn, mm, sp, status))
        if not success:
            hardfail += 1

    print("\n=== RANDOMISED sweep ===")
    rng = random.Random(999)
    randfail = 0
    total = 0
    for (nn, mm, T) in [(3, 4, 500), (3, 5, 300), (3, 6, 150), (4, 4, 300),
                        (4, 5, 150), (5, 5, 80), (5, 6, 40)]:
        f = 0
        for _ in range(T):
            cs = [rand_dicho(mm, rng, rng.choice([0.0, 0.1, 0.5, 0.9, 1.0])) for _ in range(nn)]
            v = [size_shift(c, mm) for c in cs]
            success, sp, groups, reason = local_search(v, list(range(mm)), nn)
            total += 1
            if not success:
                f += 1
                if f == 1:
                    print("  !! %s n=%d m=%d spread=%d" %
                          ("STUCK" if reason == 1 else "TIMEOUT", nn, mm, sp))
                    dump(cs, mm, nn)
        randfail += f
        print("  n=%d m=%d T=%d : %d failures" % (nn, mm, T, f))

    print("\n===============================================================")
    print("SUMMARY: exhaustive n=m=3: ok=%d stuck=%d timeout=%d / 9880 | "
          "hard=%d/%d | random=%d/%d"
          % (ok, stuck, timeout, hardfail, len(cases), randfail, total))


if __name__ == "__main__":
    main()
