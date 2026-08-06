"""Track 2: an adversarial hunt for a COUNTEREXAMPLE to Conjecture 2.

Every sweep in this project has aimed at confirming the conjecture.  None has
tried to break it.  If it is false, the whole programme is misdirected and the
counterexample is itself the result -- arguably a larger one than the affirmative.

A counterexample is an instance with NO allocation having max_i ell_A(i) <= 1.
Confirming that requires exhaustive search over all n^m allocations, so the sizes
here are chosen to keep that feasible; nothing is sampled and nothing is capped,
per the verification rule that a sweep must enumerate completely or discard.

FAMILIES, chosen from the regimes this project found tightest:
  uniform      the standard dichotomous sampler, as a control
  disjoint     each agent cares only about its own block -- maximal disagreement
  nested       agent i cares about the first b_i chores, a chain of inclusions
  one-heavy    one agent finds everything costly, the rest almost nothing
  capped       c(S) = min(|S|, k): the capping that drives the compensation in
               prop:bdnsv-fails-dichotomous
  threshold    c(S) = max(0, |S| - t): zero marginal until a threshold, the
               family behind the failure of (F2) and of free peels
  mixed        one agent from each of the above

Also reported: the minimum over allocations of max ell, since an instance whose
minimum is exactly 1 is one step from being a counterexample, and the census of
those is the useful negative result if no counterexample exists.

Run:  python counterexample_hunt.py
"""
from itertools import combinations, product
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_17")
from minimum_subsidy import subsets, rand_dicho, total_subsidy   # noqa: E402


def f_disjoint(m, n, rng):
    blocks = [[] for _ in range(n)]
    for g in range(m):
        blocks[rng.randrange(n)].append(g)
    return [{S: len(S & frozenset(blocks[i])) for S in subsets(m)}
            for i in range(n)]


def f_nested(m, n, rng):
    cuts = sorted(rng.randrange(1, m + 1) for _ in range(n))
    return [{S: len(S & frozenset(range(cuts[i]))) for S in subsets(m)}
            for i in range(n)]


def f_oneheavy(m, n, rng):
    out = [{S: len(S) for S in subsets(m)}]
    for _ in range(n - 1):
        k = rng.randrange(0, 2)
        out.append({S: min(len(S), k) for S in subsets(m)})
    return out


def f_capped(m, n, rng):
    return [{S: min(len(S), rng.randrange(1, max(2, m // 2 + 1)))
             for S in subsets(m)} for _ in range(n)]


def f_threshold(m, n, rng):
    return [{S: max(0, len(S) - rng.randrange(0, max(1, m // 2)))
             for S in subsets(m)} for _ in range(n)]


def f_uniform(m, n, rng):
    return [rand_dicho(m, rng) for _ in range(n)]


def f_mixed(m, n, rng):
    gens = [f_disjoint, f_nested, f_oneheavy, f_capped, f_threshold, f_uniform]
    out = []
    for i in range(n):
        out.append(gens[rng.randrange(len(gens))](m, 1, rng)[0])
    return out


FAMILIES = [("uniform", f_uniform), ("disjoint", f_disjoint),
            ("nested", f_nested), ("one-heavy", f_oneheavy),
            ("capped", f_capped), ("threshold", f_threshold),
            ("mixed", f_mixed)]


def min_max_ell(cs, m, n):
    """Minimum over ALL allocations of max_i ell; exhaustive."""
    best = None
    for assign in product(range(n), repeat=m):
        bd = [frozenset(g for g in range(m) if assign[g] == i) for i in range(n)]
        a = [[cs[i][bd[j]] for j in range(n)] for i in range(n)]
        t, e = total_subsidy(a, n)
        if t is None:
            continue
        v = max(e)
        if best is None or v < best:
            best = v
            if best <= 0:
                return 0
    return best


def main():
    rng = random.Random(20260809)
    hist = Counter()
    byfam = Counter()
    counterexamples = []
    tot = 0
    print("=== adversarial counterexample hunt (exhaustive over allocations) ===")
    print("   n   m   inst   min-max-ell distribution        counterexamples")
    for (n, m, T) in [(3, 8, 60), (3, 9, 40), (3, 10, 20), (3, 11, 8),
                      (4, 7, 40), (4, 8, 20), (4, 9, 8),
                      (5, 6, 30), (5, 7, 14), (5, 8, 6),
                      (6, 6, 12), (6, 7, 5)]:
        loc = Counter()
        cnt = ce = 0
        for _ in range(T):
            name, gen = FAMILIES[rng.randrange(len(FAMILIES))]
            cs = gen(m, n, rng)
            if max(max(c.values()) for c in cs) < 1:
                continue
            cnt += 1
            tot += 1
            v = min_max_ell(cs, m, n)
            if v is None:
                continue
            loc[v] += 1
            hist[v] += 1
            byfam[(name, v)] += 1
            if v >= 2:
                ce += 1
                counterexamples.append((n, m, name, v, cs))
        print("  %2d  %2d  %5d   %-30s %d"
              % (n, m, cnt, dict(sorted(loc.items())), ce))
    print()
    print("  instances searched exhaustively : %d" % tot)
    print("  min over allocations of max ell : %s" % dict(sorted(hist.items())))
    print()
    print("  COUNTEREXAMPLES (min max ell >= 2) : %d" % len(counterexamples))
    if counterexamples:
        n, m, name, v, cs = counterexamples[0]
        print()
        print("  *** CONJECTURE 2 IS FALSE ***")
        print("  witness: n=%d m=%d family=%s, min over all allocations of"
              " max ell = %d" % (n, m, name, v))
        for i in range(n):
            print("     agent %d singletons %s"
                  % (i, [cs[i][frozenset({g})] for g in range(m)]))
    else:
        print("  no counterexample found.")
        print()
        print("  instances one step away (min max ell == 1), by family:")
        for k in sorted(byfam, key=lambda z: (z[0], z[1])):
            if k[1] == 1:
                print("     %-10s %d" % (k[0], byfam[k]))


if __name__ == "__main__":
    main()
