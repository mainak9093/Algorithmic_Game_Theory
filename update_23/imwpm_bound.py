"""Stress the structural claim: does IMWPM always start at q-spread <= 2?

warmstart.py found the IMWPM warm start never exceeds q-spread 2, over 357,760
structured instances at m=5 -- the family containing all 14 known bad local
optima -- and random instances up to n=6, m=9.  Everything now rests on that
bound, because it collapses conj:warmstart from a descent along an arbitrarily
long chain to a single rung:

    IMWPM STARTS AT SPREAD <= 2   (structural claim, stressed here)
    +  every IMWPM output at spread 2 repairs to spread <= 1   (one rung)
    =>  conj:warmstart  =>  conj:algorithm-succeeds  =>  Conjecture 2.

Moreover 98.5% of the structured instances already start at spread <= 1, i.e.
IMWPM alone solves them and repair is never invoked.

Stressed here on the inputs most likely to break a matching-based bound:
  - larger n and m, where more rounds accumulate;
  - the named hard instances of Approach 6 (discrepancy counterexample,
    insertion witness, W4 no-go, mswcex);
  - structured non-additive pools at m=6;
  - instances built to make agents disagree maximally (disjoint interest sets).

Also recorded: among starts at spread 2, how many repair steps are actually
needed, since "one rung" is only useful if the rung is short.

Run:  python imwpm_bound.py
"""
from itertools import combinations
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_6")
from targetGbal import subsets, size_shift, rand_dicho     # noqa: E402
from targetGbal_local import score                          # noqa: E402
from imwpm_raw import imwpm                                 # noqa: E402
from final_algorithm import repair                          # noqa: E402
from warmstart import spread_of                             # noqa: E402


def steps_to_repair(v, groups, n, cap=200):
    """Number of improving moves repair consumes; None if it stalls."""
    key, _ = score(v, groups, n)
    g = list(groups)
    for t in range(cap):
        if key[0] <= 1:
            return t
        best = None
        for a in range(n):
            for b in range(n):
                if a == b:
                    continue
                for x in g[a]:
                    trial = list(g)
                    trial[a] = g[a] - {x}
                    trial[b] = g[b] | {x}
                    sz = [len(y) for y in trial]
                    if max(sz) - min(sz) > 1:
                        continue
                    k2, _ = score(v, trial, n)
                    if k2 < key and (best is None or k2 < best[0]):
                        best = (k2, trial)
        if best is None:
            return None
        key, g = best[0], best[1]
    return None


def disjoint_interest(m, n, rng):
    """Agents caring about disjoint blocks -- maximal disagreement."""
    blocks = [[] for _ in range(n)]
    for g in range(m):
        blocks[rng.randrange(n)].append(g)
    out = []
    for i in range(n):
        Bi = frozenset(blocks[i])
        out.append({S: len(S & Bi) for S in subsets(m)})
    return out


def main():
    rng = random.Random(60130)
    H = Counter()
    steps = Counter()
    fail = 0
    tot = 0

    def feed(v, m, n, tag):
        nonlocal fail, tot
        A = list(imwpm(v, list(range(m)), n))
        sp = spread_of(v, A, n)
        H[sp] += 1
        tot += 1
        if sp >= 2:
            s = steps_to_repair(v, A, n)
            steps[s if s is not None else "STALLED"] += 1
            if s is None:
                fail += 1
                print("  !! warm start STALLED at spread %d (%s, n=%d m=%d)"
                      % (sp, tag, n, m))
        return sp

    print("=== larger n, m ===")
    for (n, m, T) in [(3, 9, 120), (3, 10, 60), (4, 9, 80), (5, 9, 50),
                      (6, 10, 30), (7, 10, 20), (8, 12, 12)]:
        mx = 0
        for _ in range(T):
            cs = [rand_dicho(m, rng) for _ in range(n)]
            if max(max(c.values()) for c in cs) < 1:
                continue
            v = [size_shift(c, m) for c in cs]
            mx = max(mx, feed(v, m, n, "random"))
        print("  n=%2d m=%2d : max starting spread %d" % (n, m, mx))

    print()
    print("=== disjoint-interest (maximal disagreement) ===")
    for (n, m, T) in [(3, 9, 150), (4, 10, 80), (5, 10, 50), (6, 12, 30)]:
        mx = 0
        for _ in range(T):
            cs = disjoint_interest(m, n, rng)
            v = [size_shift(c, m) for c in cs]
            mx = max(mx, feed(v, m, n, "disjoint"))
        print("  n=%2d m=%2d : max starting spread %d" % (n, m, mx))

    print()
    print("=== named hard instances of Approach 6 ===")
    D = [frozenset({0, 1}), frozenset({0, 2, 3}), frozenset({1, 2, 3})]
    cases = [("discrepancy cex", 4, 3,
              [{S: len(S & Ds) for S in subsets(4)} for Ds in D]),
             ("insertion witness", 3, 3,
              [{S: max(0, len(S) - 1) for S in subsets(3)},
               {S: len(S) for S in subsets(3)}, {S: len(S) for S in subsets(3)}]),
             ("W4 no-go", 2, 3, [{S: len(S) for S in subsets(2)}] * 3)]
    for name, mm, nn, cs in cases:
        v = [size_shift(c, mm) for c in cs]
        sp = feed(v, mm, nn, name)
        print("  [%-18s] starting spread %d" % (name, sp))

    print()
    print("=== structured non-additive pool, m=6 (sampled triples) ===")
    from targetGbal_stress import structured_pool
    pool = structured_pool(6)
    mx = 0
    for _ in range(4000):
        cs = rng.sample(pool, 3)
        v = [size_shift(x, 6) for x in cs]
        mx = max(mx, feed(v, 6, 3, "structured6"))
    print("  max starting spread %d over 4000 triples" % mx)

    print()
    print("=== summary over %d instances ===" % tot)
    print("  IMWPM starting q-spread : %s" % dict(sorted(H.items())))
    print("  maximum starting spread : %d" % max(H))
    print("  warm-start stalls       : %d" % fail)
    print("  repair steps used from spread-2 starts : %s"
          % dict(sorted(steps.items(), key=lambda kv: (kv[0] == "STALLED", kv[0]))))


if __name__ == "__main__":
    main()
