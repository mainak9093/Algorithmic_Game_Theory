"""Two questions in one adversarial sweep.

(Q1)  Is Conjecture 1 itself false?  Five approaches have now failed or stalled,
      which is weak evidence there may be nothing to prove.  Binary additive is
      settled by [LMS26], so a counterexample must be NON-ADDITIVE; the search
      is restricted accordingly.

(Q2)  For the two-tier route: for each instance collect the set of paid-sets
      S = {i : p*_i = 1} realised by good allocations.  If some easily described
      S always works, that is the construction rule the route needs.

Run:  python twotier.py
"""
from itertools import combinations, product
import random
import sys


# --------------------------------------------------------------- primitives
def as_dict(m, f):
    out = {}
    for k in range(m + 1):
        for s in combinations(range(m), k):
            out[frozenset(s)] = f(frozenset(s))
    return out


def is_dichotomous(m, c):
    if c[frozenset()] != 0:
        return False
    for k in range(m + 1):
        for s in combinations(range(m), k):
            S = frozenset(s)
            for g in range(m):
                if g not in S and c[S | {g}] - c[S] not in (0, 1):
                    return False
    return True


def is_additive(m, c):
    for k in range(m + 1):
        for s in combinations(range(m), k):
            S = frozenset(s)
            if c[S] != sum(c[frozenset({g})] for g in S):
                return False
    return True


def ellvec(cs, bd, n):
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


def analyse(cs, m, n):
    """Return (good_exists, set of frozenset paid-sets realised)."""
    tiers = set()
    for assign in product(range(n), repeat=m):
        bd = [frozenset(g for g in range(m) if assign[g] == i) for i in range(n)]
        e = ellvec(cs, bd, n)
        if e is not None and max(e) <= 1:
            tiers.add(frozenset(i for i in range(n) if e[i] == 1))
    return (len(tiers) > 0), tiers


# ------------------------------------------------------- structured families
def nonadditive_pool(m):
    """Structured NON-ADDITIVE dichotomous costs on m items."""
    pool = []
    for r in range(1, m + 1):
        for D in combinations(range(m), r):
            Ds = frozenset(D)
            for k in range(1, r):                       # supermodular threshold
                pool.append(as_dict(m, lambda S, Ds=Ds, k=k: max(0, len(S & Ds) - k)))
            for k in range(1, r):                       # saturating
                pool.append(as_dict(m, lambda S, Ds=Ds, k=k: min(len(S & Ds), k)))
    # dedupe, keep dichotomous non-additive only
    seen, uniq = set(), []
    for c in pool:
        if not is_dichotomous(m, c) or is_additive(m, c):
            continue
        key = tuple(sorted((tuple(sorted(k)), v) for k, v in c.items()))
        if key not in seen:
            seen.add(key)
            uniq.append(c)
    return uniq


def endpoint_constant(m, rng, hi_prob):
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
        val[S] = hi if (lo != hi and rng.random() < hi_prob) else lo
    return val


def dump(cs, m, n):
    for i, c in enumerate(cs):
        print("     agent", i, {tuple(sorted(k)): v
                                for k, v in sorted(c.items(),
                                                   key=lambda kv: (len(kv[0]), sorted(kv[0])))})


# ------------------------------------------------------------------ sweeps
def main():
    rng = random.Random(90210)
    cex = 0
    tierstats = {}

    def record(tiers):
        key = tuple(sorted(len(t) for t in tiers))
        tierstats[key] = tierstats.get(key, 0) + 1

    print("=== Q1/Q2: exhaustive over structured NON-ADDITIVE triples ===")
    for m in (3, 4):
        pool = nonadditive_pool(m)
        print("  m=%d : %d structured non-additive functions" % (m, len(pool)))
        for n in (3,):
            cnt = 0
            for cs in combinations(pool, n):
                cnt += 1
                good, tiers = analyse(list(cs), m, n)
                record(tiers)
                if not good:
                    cex += 1
                    if cex <= 2:
                        print("  !! NO GOOD ALLOCATION  n=%d m=%d" % (n, m))
                        dump(list(cs), m, n)
            print("    n=%d : %d instances, %d with no good allocation" % (n, cnt, cex))

    print("\n=== Q1: endpoint-constant sweeps, non-additive-biased ===")
    for (n, m, T) in [(3, 4, 4000), (3, 5, 1500), (3, 6, 500),
                      (4, 4, 1500), (4, 5, 600), (5, 5, 250), (5, 6, 120)]:
        bad = 0
        for _ in range(T):
            cs = [endpoint_constant(m, rng, rng.choice([0.0, 0.1, 0.5, 0.9, 1.0]))
                  for _ in range(n)]
            good, tiers = analyse(cs, m, n)
            record(tiers)
            if not good:
                bad += 1
                if bad == 1:
                    print("  !! NO GOOD ALLOCATION  n=%d m=%d" % (n, m))
                    dump(cs, m, n)
        cex += bad
        print("  n=%d m=%d T=%5d : %d with no good allocation" % (n, m, T, bad))

    print("\n===============================================================")
    print("Q1  instances with NO good allocation (counterexamples to Conj 1): %d" % cex)

    print("\nQ2  distribution of realised paid-set SIZES (multiset -> count):")
    for key in sorted(tierstats, key=lambda k: -tierstats[k])[:12]:
        print("      sizes %-22s : %d instances" % (str(list(key)), tierstats[key]))

    # Q2 sharpened: is a paid set of some fixed size ALWAYS available?
    print("\nQ2  is some paid-set size always realisable?")
    for k in range(0, 6):
        miss = sum(v for key, v in tierstats.items() if k not in key)
        tot = sum(tierstats.values())
        if tot:
            print("      |S| = %d : unavailable in %d of %d instances" % (k, miss, tot))


if __name__ == "__main__":
    main()
