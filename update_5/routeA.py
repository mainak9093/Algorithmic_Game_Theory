"""Route A, step 0: is the target of the agent-induction actually reachable?

REFORMULATION.  Call an unordered family of n disjoint bundles covering M
UNIFORMLY BALANCED if every agent values all n bundles within 1 of each other:

    max_B c_i(B) - min_B c_i(B) <= 1     for every agent i.

The condition does not mention who holds which bundle.  If it holds then, for
ANY assignment of the bundles to agents, every envy-graph arc satisfies
    w(i,j) = c_i(A_i) - c_i(A_j) >= -1 ,
so choosing the assignment by a maximum-weight matching makes the allocation
reassignment-stable (Halpern-Shah) and the cycle-closing bound then gives
ell(i) <= 1, hence p* in {0,1}^n and total <= n-1.

So:  "every instance admits a uniformly balanced partition"  ==>  Conjecture 1.

This script asks whether that premise is true.  It is a purely combinatorial,
schedule-free, coverage-free statement -- which is what makes it worth testing
before any proof is attempted.

Run:  python routeA.py              # exhaustive n=3 m=3, then randomised
      python routeA.py quick        # randomised only
"""
from itertools import combinations, product, permutations
import random
import sys


# ---------------------------------------------------------------- generators
def gen_functions(m):
    """All dichotomous cost functions on m items (monotone, c(0)=0, marginals 0/1)."""
    subs = sorted([frozenset(s) for k in range(m + 1) for s in combinations(range(m), k)],
                  key=lambda s: (len(s), sorted(s)))
    res, val = [], {}

    def rec(i):
        if i == len(subs):
            res.append(dict(val))
            return
        S = subs[i]
        if len(S) == 0:
            val[S] = 0
            rec(i + 1)
            del val[S]
            return
        lo, hi = 0, 10 ** 9
        for g in S:
            T = S - {g}
            lo = max(lo, val[T])
            hi = min(hi, val[T] + 1)
        for v in range(lo, hi + 1):
            val[S] = v
            rec(i + 1)
        del val[S]

    rec(0)
    return res


def rand_dicho(m, rng):
    subs = sorted([frozenset(s) for k in range(m + 1) for s in combinations(range(m), k)],
                  key=lambda s: (len(s), sorted(s)))
    val = {frozenset(): 0}
    for S in subs:
        if not S:
            continue
        lo, hi = 0, 10 ** 9
        for g in S:
            T = S - {g}
            lo = max(lo, val[T])
            hi = min(hi, val[T] + 1)
        val[S] = hi if (lo != hi and rng.random() < rng.random()) else lo
    return val


# ---------------------------------------------------------------- primitives
def ellvec(cs, bd, n):
    """Longest-path subsidies; None iff a positive-weight cycle exists."""
    W = [[cs[i][bd[i]] - cs[i][bd[j]] for j in range(n)] for i in range(n)]
    e = [0] * n
    for _ in range(n + 1):
        ch = False
        new = list(e)
        for i in range(n):
            for j in range(n):
                if i != j and W[i][j] + e[j] > new[i]:
                    new[i] = W[i][j] + e[j]
                    ch = True
        e = new
        if not ch:
            return e
    return None


def partitions(m, n):
    for assign in product(range(n), repeat=m):
        yield [frozenset(g for g in range(m) if assign[g] == i) for i in range(n)]


def uniformly_balanced(cs, bd, n):
    """Every agent values all n bundles within 1 of each other."""
    for ci in cs:
        vals = [ci[b] for b in bd]
        if max(vals) - min(vals) > 1:
            return False
    return True


def best_assignment(cs, bd, n):
    """Assign the bundles to agents by max total value (= min total cost),
    i.e. a maximum-weight matching, and return (ell vector, ordered bundles)."""
    best = None
    for sig in permutations(range(n)):
        arr = [bd[sig[i]] for i in range(n)]
        tot = sum(cs[i][arr[i]] for i in range(n))
        if best is None or tot < best[0]:
            best = (tot, arr)
    arr = best[1]
    return ellvec(cs, arr, n), arr


def has_good_allocation(cs, m, n):
    for bd in partitions(m, n):
        e = ellvec(cs, bd, n)
        if e is not None and max(e) <= 1:
            return True
    return False


def has_balanced_partition(cs, m, n):
    """Return an ordered representative of a uniformly balanced partition, or None."""
    for bd in partitions(m, n):
        if uniformly_balanced(cs, bd, n):
            return bd
    return None


# ---------------------------------------------------------------- the checks
def check(cs, m, n, verify_chain=True):
    """Returns (balanced_exists, good_exists, chain_ok)."""
    bd = has_balanced_partition(cs, m, n)
    if bd is None:
        return False, has_good_allocation(cs, m, n), True
    if not verify_chain:
        return True, True, True
    # The whole implication chain, end to end, on this instance.
    e, arr = best_assignment(cs, bd, n)
    chain_ok = (e is not None) and (max(e) <= 1)
    return True, True, chain_ok


def exhaustive_n3_m3():
    print("=== EXHAUSTIVE: n=3, m=3, all instances up to agent symmetry ===")
    F = gen_functions(3)
    print("    dichotomous functions on 3 items: %d" % len(F))
    total = nobal = chainbad = balnogood = 0
    firstfail = None
    for cs in combinations(F, 3):
        # combinations gives distinct triples; add the repeats separately below
        total += 1
        bal, good, chain = check(list(cs), 3, 3)
        if not bal:
            nobal += 1
            if firstfail is None:
                firstfail = (list(cs), good)
        if not chain:
            chainbad += 1
    # multisets with repeats
    from itertools import combinations_with_replacement
    total = 0
    nobal = chainbad = 0
    firstfail = None
    for cs in combinations_with_replacement(F, 3):
        total += 1
        bal, good, chain = check(list(cs), 3, 3)
        if not bal:
            nobal += 1
            if firstfail is None:
                firstfail = (list(cs), good)
        if not chain:
            chainbad += 1
    print("    instances checked                       : %d" % total)
    print("    with NO uniformly balanced partition    : %d" % nobal)
    print("    where the implication chain broke       : %d" % chainbad)
    if firstfail:
        cs, good = firstfail
        print("\n    first instance with no balanced partition (good alloc exists: %s):" % good)
        for i, c in enumerate(cs):
            print("      agent", i, {tuple(sorted(k)): v
                                     for k, v in sorted(c.items(),
                                                        key=lambda kv: (len(kv[0]), sorted(kv[0])))})
    return nobal, chainbad


def randomised():
    print("\n=== RANDOMISED ===")
    rng = random.Random(20260803)
    cfgs = [(3, 3, 400), (3, 4, 400), (3, 5, 250), (3, 6, 120),
            (4, 3, 300), (4, 4, 200), (4, 5, 80),
            (5, 4, 80), (5, 5, 40)]
    for n, m, T in cfgs:
        nobal = chainbad = balnogood = nogood = 0
        for _ in range(T):
            cs = [rand_dicho(m, rng) for _ in range(n)]
            bal, good, chain = check(cs, m, n)
            if not bal:
                nobal += 1
                if not good:
                    nogood += 1
            if not chain:
                chainbad += 1
        print("  n=%d m=%d T=%4d | no balanced partition: %3d | chain broke: %d"
              "  %s" % (n, m, T, nobal, chainbad,
                        "" if nobal == 0 else "(of those, no good allocation at all: %d)" % nogood))


if __name__ == "__main__":
    if "quick" not in sys.argv:
        exhaustive_n3_m3()
    randomised()
