"""Target G-bal: does a CARDINALITY-balanced partition, optimally reassigned,
always suffice for Target G?

Motivation.  guidedR3_full.py found a genuine reachability obstruction: R3's
own insertion template, with full choice freedom, cannot always reach a good
allocation -- even one that is itself perfectly cardinality-balanced.  The
obstruction is specifically about insertion ORDER rigidity (bundle identity is
fixed the moment an item is dropped into it, and growth is monotone).  This
script removes that rigidity entirely: instead of building bundles one item at
a time, fix a partition of the items into n groups of sizes differing by at
most 1 FIRST (ignoring which agent gets which), then assign groups to agents by
a single max-weight matching (Halpern-Shah / R1's own characterization).

TARGET G-BAL.  Every dichotomous goods instance admits a partition of the items
into n groups with sizes differing by at most 1, such that the max-weight
matching of groups to agents gives q = ptilde + |A_i| spread <= 1.

If true, this is a genuinely constructive target: cardinality-balanced groups
are cheap to enumerate/construct (R2's iterated-matching machinery already
produces them), and the only new content needed is CHOOSING WHICH ITEMS GO
TOGETHER, which is a much smaller search than the full item-by-item insertion
process.

Run:  python targetGbal.py
"""
from itertools import combinations, combinations_with_replacement, permutations, product
import random


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


def size_shift(c, m):
    return {S: len(S) - c[S] for S in c}


def longest_path(W, n):
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
            return e
    return None


def q_of(v, groups, n):
    """groups: list of n frozensets (already assigned to specific agents
    via a max-weight matching).  Returns (spread, p, q) or (None, None, None)
    if not envy-freeable."""
    W = [[v[i][groups[j]] - v[i][groups[i]] for j in range(n)] for i in range(n)]
    p = longest_path(W, n)
    if p is None:
        return None, None, None
    q = [p[i] + len(groups[i]) for i in range(n)]
    return max(q) - min(q), p, q


def best_matching(v, unlabeled_groups, n):
    """Try all n! assignments of the n unlabeled groups to agents, return the
    one with smallest q-spread (ties broken by max welfare, Halpern-Shah)."""
    best = None
    for perm in permutations(range(n)):
        groups = [unlabeled_groups[perm[i]] for i in range(n)]
        sp, p, q = q_of(v, groups, n)
        if sp is None:
            continue
        welfare = sum(v[i][groups[i]] for i in range(n))
        key = (sp, -welfare)
        if best is None or key < best[0]:
            best = (key, sp, groups, p, q)
    if best is None:
        return None
    return best[1], best[2], best[3], best[4]


def balanced_partitions(items, n):
    """All partitions of `items` into n labelled groups whose sizes differ by
    at most 1 (i.e. sizes are floor(m/n) or ceil(m/n))."""
    m = len(items)
    lo, hi = m // n, -(-m // n)
    extra = m - lo * n            # number of groups that must have size hi
    sizes_list = set()

    def size_seqs(remaining_slots, remaining_extra, remaining_items):
        if remaining_slots == 0:
            if remaining_items == 0:
                yield ()
            return
        for take_extra in ([1, 0] if remaining_extra > 0 else [0]):
            sz = hi if take_extra else lo
            if sz > remaining_items:
                continue
            for rest in size_seqs(remaining_slots - 1, remaining_extra - take_extra,
                                  remaining_items - sz):
                yield (sz,) + rest

    for sizes in size_seqs(n, extra, m):
        # Now partition `items` into ordered groups with these sizes.
        def assign(pool, sizes):
            if not sizes:
                yield ()
                return
            sz = sizes[0]
            for combo in combinations(pool, sz):
                rest = [x for x in pool if x not in combo]
                for tail in assign(rest, sizes[1:]):
                    yield (frozenset(combo),) + tail
        for grouping in assign(list(items), sizes):
            yield grouping


def best_over_balanced(v, items, n):
    best = None
    for grouping in balanced_partitions(items, n):
        res = best_matching(v, list(grouping), n)
        if res is None:
            continue
        sp, groups, p, q = res
        if best is None or sp < best[0]:
            best = (sp, groups, p, q)
        if sp <= 1:
            break
    return best


def dump(cs, m, n):
    for i, c in enumerate(cs):
        print("     agent", i, {tuple(sorted(k)): v for k, v in
                                sorted(c.items(), key=lambda kv: (len(kv[0]), sorted(kv[0])))})


def main():
    print("=== EXHAUSTIVE n=3 m=3 ===")
    F = gen_functions(3)
    fail = 0
    dist = {}
    for cs in combinations_with_replacement(F, 3):
        v = [size_shift(c, 3) for c in cs]
        best = best_over_balanced(v, list(range(3)), 3)
        sp = best[0] if best else None
        dist[sp] = dist.get(sp, 0) + 1
        if best is None or best[0] > 1:
            fail += 1
    print("  failures (no balanced partition reaches spread<=1): %d / 9880" % fail)
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
        best = best_over_balanced(v, list(range(mm)), nn)
        status = "OK" if best and best[0] <= 1 else "FAIL"
        print("  [%s] n=%d m=%d  best spread=%s  %s   groups=%s q=%s"
              % (name, nn, mm, best[0] if best else None, status,
                 [sorted(g) for g in best[1]] if best else None, best[3] if best else None))
        if not (best and best[0] <= 1):
            hardfail += 1

    print("\n=== RANDOMISED / adversarial-flavoured sweep ===")
    rng = random.Random(31415)
    randfail = 0
    total = 0
    for (nn, mm, T) in [(3, 4, 400), (3, 5, 150), (3, 6, 60), (4, 4, 150), (4, 5, 60), (5, 5, 30)]:
        f = 0
        for _ in range(T):
            cs = [rand_dicho(mm, rng, rng.choice([0.0, 0.1, 0.5, 0.9, 1.0])) for _ in range(nn)]
            v = [size_shift(c, mm) for c in cs]
            best = best_over_balanced(v, list(range(mm)), nn)
            total += 1
            if not (best and best[0] <= 1):
                f += 1
                if f == 1:
                    print("  !! FAIL n=%d m=%d  best=%s" % (nn, mm, best))
                    dump(cs, mm, nn)
        randfail += f
        print("  n=%d m=%d T=%d : %d failures" % (nn, mm, T, f))

    print("\n===============================================================")
    print("SUMMARY: exhaustive n=m=3 failures=%d/9880 | hard instances=%d/%d | "
          "random=%d/%d" % (fail, hardfail, len(cases), randfail, total))


if __name__ == "__main__":
    main()
