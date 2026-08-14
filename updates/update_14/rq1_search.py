"""
Approach 14 / Research Question 1 (RQ1).

For every POSITIVE dichotomous instance (v_i(empty)=0, marginals in {0,1}),
does there exist a complete allocation B and q in {0,1}^n with
  (i)   EF with subsidy:  v_i(B_i) + q_i >= v_i(B_j) + q_j  for all i,j
  (ii)  almost balanced:  | |B_i| - |B_j| | <= 1
  (iii) compatibility:    |B_i| > |B_j|  =>  q_i <= q_j
?

This script searches exhaustively over almost-balanced allocations and all
q in {0,1}^n, on randomly generated positive dichotomous instances.
"""
import itertools, random, sys


def random_dichotomous(m, rng):
    """v(empty)=0, all marginals in {0,1}: uniformly random within those constraints."""
    c = {frozenset(): 0}
    for r in range(1, m + 1):
        for S in itertools.combinations(range(m), r):
            S = frozenset(S)
            lo = max(c[S - {b}] for b in S)
            hi = min(c[S - {b}] + 1 for b in S)
            c[S] = rng.randint(lo, hi)
    return c


def almost_balanced_allocations(n, m):
    """All ordered allocations with every |B_i| in {k,k+1}, m = k n + r."""
    k, r = divmod(m, n)
    items = list(range(m))
    # choose which r agents get k+1
    for big in itertools.combinations(range(n), r):
        sizes = [k + 1 if i in big else k for i in range(n)]
        # distribute items into bundles of the given sizes
        for assign in _split(items, sizes):
            yield [frozenset(b) for b in assign]


def _split(items, sizes):
    if not sizes:
        yield []
        return
    first, rest = sizes[0], sizes[1:]
    for chosen in itertools.combinations(items, first):
        remaining = [x for x in items if x not in chosen]
        for tail in _split(remaining, rest):
            yield [list(chosen)] + tail


def rq1_holds(vals, n, m):
    """Return (B,q) satisfying (i)-(iii), or None."""
    for B in almost_balanced_allocations(n, m):
        sizes = [len(b) for b in B]
        for q in itertools.product((0, 1), repeat=n):
            # (iii) compatibility
            ok = True
            for i in range(n):
                for j in range(n):
                    if sizes[i] > sizes[j] and q[i] > q[j]:
                        ok = False; break
                if not ok: break
            if not ok:
                continue
            # (i) EF with subsidy, goods form
            for i in range(n):
                for j in range(n):
                    if vals[i][B[i]] + q[i] < vals[i][B[j]] + q[j]:
                        ok = False; break
                if not ok: break
            if ok:
                return B, q
    return None


def main(n, m, trials, seed):
    rng = random.Random(seed)
    bad = 0
    for t in range(trials):
        vals = [random_dichotomous(m, rng) for _ in range(n)]
        res = rq1_holds(vals, n, m)
        if res is None:
            bad += 1
            if bad <= 3:
                print(f"  COUNTEREXAMPLE trial {t} (n={n}, m={m}):")
                for i in range(n):
                    row = {tuple(sorted(S)): vals[i][S]
                           for S in map(frozenset, _all_subsets(m))}
                    print(f"    v_{i}: {row}")
    print(f"n={n} m={m} trials={trials} seed={seed}: RQ1 FAILURES = {bad}/{trials}")
    return bad


def _all_subsets(m):
    for r in range(m + 1):
        for S in itertools.combinations(range(m), r):
            yield S


if __name__ == "__main__":
    n = int(sys.argv[1]); m = int(sys.argv[2])
    tr = int(sys.argv[3]); sd = int(sys.argv[4])
    main(n, m, tr, sd)


def biased_dichotomous(m, rng, pbias):
    c = {frozenset(): 0}
    for r in range(1, m + 1):
        for S in itertools.combinations(range(m), r):
            S = frozenset(S)
            lo = max(c[S - {b}] for b in S)
            hi = min(c[S - {b}] + 1 for b in S)
            c[S] = hi if (lo != hi and rng.random() < pbias) else lo
    return c


def main_biased(n, m, trials, seed, pbias):
    rng = random.Random(seed)
    bad = 0
    first = None
    for t in range(trials):
        vals = [biased_dichotomous(m, rng, pbias) for _ in range(n)]
        if rq1_holds(vals, n, m) is None:
            bad += 1
            if first is None:
                first = vals
    print(f"n={n} m={m} bias={pbias} trials={trials} seed={seed}: RQ1 FAILURES = {bad}/{trials}")
    return bad, first
