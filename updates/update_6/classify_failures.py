"""Classify the 14 local-search failures found at m=5, n=3 in
targetGbal_stress.py: are they (a) local search getting stuck although Target
G-bal holds, or (b) genuine failures of Target G-bal itself (no BALANCED
partition works), or even (c) failures of Target G / Conjecture 1 (no
allocation at all works, balanced or not)?

Run:  python classify_failures.py
"""
from itertools import combinations, combinations_with_replacement, product

from targetGbal import subsets, size_shift, best_over_balanced, dump
from targetGbal_local import local_search
from targetGbal_stress import structured_pool


def full_unrestricted_check(v, m, n):
    """True unrestricted search over ALL partitions (not just balanced)."""
    best = None
    for assign in product(range(n), repeat=m):
        bd = [frozenset(g for g in range(m) if assign[g] == i) for i in range(n)]
        W = [[v[i][bd[j]] - v[i][bd[i]] for j in range(n)] for i in range(n)]
        e = [0] * n
        for _ in range(n + 1):
            ch = False
            new = list(e)
            for i in range(n):
                for j in range(n):
                    if i != j and W[i][j] + e[j] > new[i]:
                        new[i] = W[i][j] + e[j]; ch = True
            e = new
            if not ch:
                break
        else:
            continue
        q = [e[i] + len(bd[i]) for i in range(n)]
        sp = max(q) - min(q)
        if best is None or sp < best:
            best = sp
    return best


def main():
    m, n = 5, 3
    pool = structured_pool(m)
    print("m=%d structured functions: %d" % (m, len(pool)))

    found = 0
    for cs in combinations(pool, n):
        v = [size_shift(c, m) for c in cs]
        success, sp_local, groups, reason = local_search(v, list(range(m)), n)
        if success:
            continue
        found += 1
        # (a) does EXHAUSTIVE balanced-partition search do better?
        best_bal = best_over_balanced(v, list(range(m)), n)
        sp_bal = best_bal[0] if best_bal else None
        # (b) does the fully UNRESTRICTED search (any partition) do better?
        sp_all = full_unrestricted_check(v, m, n)

        tag = ("LOCAL-SEARCH-STUCK" if sp_bal is not None and sp_bal <= 1
               else "TARGET-G-BAL FAILS" if sp_all is not None and sp_all <= 1
               else "CONJECTURE 1 ITSELF FAILS" if sp_all is not None
               else "NOT EVEN ENVY-FREEABLE ANYWHERE (?)")

        print("\n--- failure %d ---" % found)
        print("  local search spread : %s" % sp_local)
        print("  exhaustive BALANCED : %s" % sp_bal)
        print("  exhaustive ALL      : %s" % sp_all)
        print("  => %s" % tag)
        dump(list(cs), m, n)

        if found >= 20:
            break

    print("\ntotal classified: %d" % found)


if __name__ == "__main__":
    main()
