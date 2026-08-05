"""Does raw IMWPM (R11's iterated max-weight PERFECT matching, no repair)
already hit Target G-bal, with no local search needed?

Implementation: pad items with inert dummies (marginal 0 always) to a multiple
of n; in each of T = ceil(m/n) rounds, compute a max-weight PERFECT matching
between agents and remaining items using CURRENT-bundle MARGINAL weights
v_i(bundle_i U {item}) - v_i(bundle_i) (the natural non-additive generalisation
of R11's item-value weights, needed since valuations here need not be
additive); every agent takes exactly one item (possibly a dummy) each round.

Run:  python imwpm_raw.py
"""
from itertools import combinations, combinations_with_replacement, permutations
import random

from targetGbal import subsets, size_shift, gen_functions, rand_dicho, dump


def imwpm(v, items, n):
    m = len(items)
    T = -(-m // n)                      # ceil(m/n)
    pad = T * n - m
    # dummy items: fresh integer ids beyond the real item range, inert.
    dummies = list(range(10**6, 10**6 + pad))
    pool = list(items) + dummies
    bundles = [frozenset() for _ in range(n)]

    def val(i, S):
        # dummies have zero marginal / zero value always.
        real = frozenset(x for x in S if x < 10**6)
        return v[i][real]

    remaining = list(pool)
    for _ in range(T):
        # max-weight PERFECT matching agents <-> a size-n subset... actually
        # every agent takes exactly one item this round from `remaining`
        # (|remaining| == n * (rounds left)); we match against ALL remaining
        # items but each agent only takes ONE -- so this is an assignment of
        # n items (one per agent) out of the |remaining| available, chosen to
        # maximise total marginal.  With |remaining| = n*(T-t) this round has
        # more than n items available in general; the perfect-matching
        # framing in R11 assumes |remaining|=n each round precisely because
        # T = ceil(m/n) rounds consume all items at n per round -- so
        # |remaining| IS exactly n * (T - t), and this round consumes n of
        # them.  To stay faithful and keep this brute-forceable, we search
        # over all ways to pick n items (one bucket) -- for our small test
        # sizes this is fine since remaining shrinks by n each round and the
        # picks are typically small.
        # Simplify: since all dummies are interchangeable, only the choice of
        # which REAL items (if any) go this round matters combinatorially.
        best = None
        real_remaining = [x for x in remaining if x < 10**6]
        dummy_remaining = [x for x in remaining if x >= 10**6]
        take_reals = min(n, len(real_remaining))
        for r in range(0, take_reals + 1):
            if len(dummy_remaining) < n - r:
                continue
            for real_choice in combinations(real_remaining, r):
                dummy_choice = tuple(dummy_remaining[:n - r])
                batch = list(real_choice) + list(dummy_choice)
                for perm in permutations(batch):
                    tot = sum(val(i, bundles[i] | {perm[i]}) - val(i, bundles[i])
                              for i in range(n))
                    if best is None or tot > best[0]:
                        best = (tot, perm, real_choice, dummy_choice)
        _, perm, real_choice, dummy_choice = best
        for i in range(n):
            bundles[i] = bundles[i] | {perm[i]}
        for x in real_choice:
            remaining.remove(x)
        for x in dummy_choice:
            remaining.remove(x)

    # strip dummies for the final (real-item-only) allocation.
    final = [frozenset(x for x in b if x < 10**6) for b in bundles]
    return final


def compute_p(v, A, n):
    from targetGbal import longest_path
    W = [[v[i][A[j]] - v[i][A[i]] for j in range(n)] for i in range(n)]
    return longest_path(W, n)


def q_spread(v, A, n):
    p = compute_p(v, A, n)
    if p is None:
        return None, None, None
    q = [p[i] + len(A[i]) for i in range(n)]
    return max(q) - min(q), p, q


def main():
    print("=== EXHAUSTIVE n=3 m=3, raw IMWPM (no repair) ===")
    F = gen_functions(3)
    fail = 0
    dist = {}
    for cs in combinations_with_replacement(F, 3):
        v = [size_shift(c, 3) for c in cs]
        A = imwpm(v, list(range(3)), 3)
        sp, p, q = q_spread(v, A, 3)
        dist[sp] = dist.get(sp, 0) + 1
        if sp is None or sp > 1:
            fail += 1
    print("  failures : %d / 9880" % fail)
    print("  spread distribution: %s" % dict(sorted(dist.items(), key=lambda kv: (kv[0] is None, kv[0]))))

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
        A = imwpm(v, list(range(mm)), nn)
        sp, p, q = q_spread(v, A, nn)
        status = "OK" if sp is not None and sp <= 1 else "FAIL"
        print("  [%s] spread=%s %s  bundles=%s q=%s" %
              (name, sp, status, [sorted(b) for b in A], q))
        if not (sp is not None and sp <= 1):
            hardfail += 1

    print("\n=== RANDOMISED ===")
    rng = random.Random(555)
    randfail = 0
    total = 0
    for (nn, mm, T) in [(3, 4, 300), (3, 5, 150), (4, 4, 150), (4, 5, 80), (5, 5, 40)]:
        f = 0
        for _ in range(T):
            cs = [rand_dicho(mm, rng, rng.choice([0.0, 0.1, 0.5, 0.9, 1.0])) for _ in range(nn)]
            v = [size_shift(c, mm) for c in cs]
            A = imwpm(v, list(range(mm)), nn)
            sp, p, q = q_spread(v, A, nn)
            total += 1
            if not (sp is not None and sp <= 1):
                f += 1
        randfail += f
        print("  n=%d m=%d T=%d : %d failures" % (nn, mm, T, f))

    print("\n===============================================================")
    print("SUMMARY: exhaustive=%d/9880 | hard=%d/%d | random=%d/%d"
          % (fail, hardfail, len(cases), randfail, total))


if __name__ == "__main__":
    main()
