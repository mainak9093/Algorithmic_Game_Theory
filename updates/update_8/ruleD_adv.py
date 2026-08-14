"""Adversarial test of the deterministic rule:

    RULE.  Among cardinality-balanced allocations of minimum total cost,
           take one minimising the number of envious ordered pairs
           #{(i,j) : c_i(A_i) > c_i(A_j)}.

Tested in the STRONG form: every allocation the rule can select must be good.
The adversary is the one that refuted uniform balance in a single run.

Run:  python ruleD_adv.py
"""
from itertools import combinations, product
import random

from balanced_msw import (subsets, rand_dicho, ellvec, balanced, as_dict,
                          gen_functions)
from tiebreak_balanced import winners, good


def envy_count(cs, bd, n):
    return sum(1 for i in range(n) for j in range(n)
               if i != j and cs[i][bd[i]] > cs[i][bd[j]])


def rule_ok(cs, m, n):
    ws = winners(cs, m, n)
    if not ws:
        return None
    best = min(envy_count(cs, bd, n) for bd in ws)
    sel = [bd for bd in ws if envy_count(cs, bd, n) == best]
    return all(good(cs, bd, n) for bd in sel)


def is_dich(m, c):
    if c[frozenset()] != 0:
        return False
    for S in subsets(m):
        for g in range(m):
            if g not in S and c[S | {g}] - c[S] not in (0, 1):
                return False
    return True


def families(m):
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


def dump(cs, m, n):
    for i, c in enumerate(cs):
        print("     agent", i, {tuple(sorted(k)): v for k, v in
                                sorted(c.items(), key=lambda kv:
                                       (len(kv[0]), sorted(kv[0])))})


def main():
    bad = 0

    print("=== exhaustive over structured families, n=3 ===")
    for m in (3, 4):
        pool = families(m)
        cnt = f = 0
        for cs in combinations(pool, 3):
            cnt += 1
            r = rule_ok(list(cs), m, 3)
            if r is False:
                f += 1
                if f == 1:
                    print("  !! RULE FAILS  m=%d" % m)
                    dump(list(cs), m, 3)
        print("  m=%d : %6d instances, %d failures" % (m, cnt, f))
        bad += f

    print("\n=== exhaustive all dichotomous triples, n=3, m=3 ===")
    F = gen_functions(3)
    from itertools import combinations_with_replacement
    f = 0
    for cs in combinations_with_replacement(F, 3):
        if rule_ok(list(cs), 3, 3) is False:
            f += 1
    print("  9880 instances, %d failures" % f)
    bad += f

    print("\n=== endpoint-constant sweeps ===")
    rng = random.Random(1618)
    for (n, m, T) in [(3, 4, 6000), (3, 5, 2000), (3, 6, 600),
                      (4, 4, 1500), (4, 5, 500), (5, 5, 200), (5, 6, 100)]:
        f = 0
        for _ in range(T):
            cs = [rand_dicho(m, rng, rng.choice([0.0, 0.05, 0.5, 0.95, 1.0]))
                  for _ in range(n)]
            r = rule_ok(cs, m, n)
            if r is False:
                f += 1
                if f == 1:
                    print("  !! RULE FAILS  n=%d m=%d" % (n, m))
                    dump(cs, m, n)
        print("  n=%d m=%d T=%5d : %d failures" % (n, m, T, f))
        bad += f

    print("\n===============================================================")
    print("TOTAL rule failures: %d" % bad)


if __name__ == "__main__":
    main()
