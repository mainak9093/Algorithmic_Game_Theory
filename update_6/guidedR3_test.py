"""Does greedy-guided R3 hit Target G's q-spread <= 1?

Tests, in order of ambition:
  1. Exhaustive n=m=3 (9880 instances), single fixed item order.
  2. Same family, best over all m! orders (m=3 => 6 orders, cheap).
  3. The named adversarial hard instances that killed earlier methods,
     best over all item orders.
  4. Randomised sweep at larger n, m (order sampled, not exhaustive).

Run:  python guidedR3_test.py
"""
from itertools import combinations, combinations_with_replacement
import random
import sys

from guidedR3 import size_shift, greedy_run, best_over_orders, q_spread


def subsets(m):
    return [frozenset(s) for k in range(m + 1) for s in combinations(range(m), k)]


def gen_functions(m):
    subs = sorted(subsets(m), key=lambda s: (len(s), sorted(s)))
    res, val = [], {}

    def rec(i):
        if i == len(subs):
            res.append(dict(val)); return
        S = subs[i]
        if len(S) == 0:
            val[S] = 0; rec(i + 1); del val[S]; return
        lo, hi = 0, 10 ** 9
        for g in S:
            T = S - {g}
            lo = max(lo, val[T]); hi = min(hi, val[T] + 1)
        for x in range(lo, hi + 1):
            val[S] = x; rec(i + 1)
        del val[S]

    rec(0)
    return res


def rand_dicho(m, rng, hi_prob=None):
    subs = sorted(subsets(m), key=lambda s: (len(s), sorted(s)))
    val = {frozenset(): 0}
    for S in subs:
        if not S:
            continue
        lo, hi = 0, 10 ** 9
        for g in S:
            T = S - {g}
            lo = max(lo, val[T]); hi = min(hi, val[T] + 1)
        pr = rng.random() if hi_prob is None else hi_prob
        val[S] = hi if (lo != hi and rng.random() < pr) else lo
    return val


def dump(cs, m, n):
    for i, c in enumerate(cs):
        print("     agent", i, {tuple(sorted(k)): v for k, v in
                                sorted(c.items(), key=lambda kv: (len(kv[0]), sorted(kv[0])))})


def main():
    n, m = 3, 3
    F = gen_functions(m)
    print("=== EXHAUSTIVE n=3 m=3, FIXED item order 0,1,2 ===")
    fixed_fail = 0
    for cs in combinations_with_replacement(F, n):
        v = [size_shift(c, m) for c in cs]
        A, p = greedy_run(v, list(range(m)), n)
        sp, _, _ = q_spread(v, A, n)
        if sp > 1:
            fixed_fail += 1
    print("  q-spread > 1 with fixed order          : %d / 9880" % fixed_fail)

    print("\n=== EXHAUSTIVE n=3 m=3, BEST over all %d orders ===" % 6)
    best_fail = 0
    firstfail = None
    for cs in combinations_with_replacement(F, n):
        v = [size_shift(c, m) for c in cs]
        sp, order, A, p, q = best_over_orders(v, list(range(m)), n)
        if sp > 1:
            best_fail += 1
            if firstfail is None:
                firstfail = (list(cs), sp, order, A, q)
    print("  q-spread > 1 even with best order       : %d / 9880" % best_fail)
    if firstfail:
        cs, sp, order, A, q = firstfail
        print("  first failure: spread=%d order=%s bundles=%s q=%s"
              % (sp, order, [sorted(b) for b in A], q))
        dump(cs, m, n)

    print("\n=== NAMED HARD INSTANCES, best over all item orders ===")
    cases = []
    D = [frozenset({0, 1}), frozenset({0, 2, 3}), frozenset({1, 2, 3})]
    cases.append(("discrepancy cex (killed Approach 5)", 4, 3,
                  [{S: len(S & Ds) for S in subsets(4)} for Ds in D]))
    cases.append(("insertion obstruction witness", 3, 3,
                  [{S: max(0, len(S) - 1) for S in subsets(3)},
                   {S: len(S) for S in subsets(3)},
                   {S: len(S) for S in subsets(3)}]))
    cases.append(("W4 no-go instance", 2, 3,
                  [{S: len(S) for S in subsets(2)}] * 3))
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
        sp, order, A, p, q = best_over_orders(v, list(range(mm)), nn)
        status = "OK" if sp <= 1 else "FAIL"
        print("  [%s] n=%d m=%d  best spread=%d  %s   bundles=%s q=%s"
              % (name, nn, mm, sp, status, [sorted(b) for b in A], q))
        if sp > 1:
            hardfail += 1

    print("\n=== RANDOMISED, larger n/m, order sampled not exhaustive ===")
    rng = random.Random(2024)
    randfail = 0
    total = 0
    for (nn, mm, T) in [(3, 4, 300), (3, 5, 150), (4, 4, 150), (4, 5, 80), (5, 5, 40)]:
        f = 0
        for _ in range(T):
            cs = [rand_dicho(mm, rng, rng.choice([0.0, 0.1, 0.5, 0.9, 1.0])) for _ in range(nn)]
            v = [size_shift(c, mm) for c in cs]
            sp, order, A, p, q = best_over_orders(v, list(range(mm)), nn, max_orders=24)
            total += 1
            if sp > 1:
                f += 1
        randfail += f
        print("  n=%d m=%d T=%d : %d failures (order-sampled, max 24 orders tried)"
              % (nn, mm, T, f))

    print("\n===============================================================")
    print("SUMMARY")
    print("  exhaustive n=m=3, fixed order   : %d/9880 fail" % fixed_fail)
    print("  exhaustive n=m=3, best of 6     : %d/9880 fail" % best_fail)
    print("  named hard instances            : %d/%d fail" % (hardfail, len(cases)))
    print("  randomised (order-sampled)      : %d/%d fail" % (randfail, total))


if __name__ == "__main__":
    main()
