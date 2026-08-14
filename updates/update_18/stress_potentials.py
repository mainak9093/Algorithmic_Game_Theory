"""Stress the two surviving potentials, and look for a simpler one.

potentials.py found zero stuck partitions for
    P2 = (max ell, #at max, max_i |A_i|)
    P3 = (max ell, #at max, sum_i |A_i|^2)
over 1,732 random instances, while the cost-minimising P1 failed.  Two things
must happen before that is worth a proof attempt.

(a) HARDER INPUTS.  Random instances are 95% exactly envy-free and so mostly
    vacuous here.  This run concentrates on the residual: EF-FREE instances,
    non-additive instances, and the certified-hard Set-Splitting family of R10,
    plus larger n.

(b) A SIMPLER POTENTIAL.  P2/P3 have three components; a two-component potential
    would be markedly easier to prove.  Added candidates:
        P6  (max ell, sum |A_i|^2)              -- drop the tie-count
        P7  (max ell, max_i |A_i|)              -- drop it, size version
        P8  (sum_i ell_i, sum |A_i|^2)          -- total envy instead of max
        P9  (max ell, #at max, sum |A_i|^2, total cost)   -- refinement of P3

(L_P) = every partition with max ell >= 2 admits a single-chore transfer
strictly decreasing P.  Any P with no stuck partition implies Conjecture 2.

Run:  python stress_potentials.py
"""
from itertools import product, permutations, combinations
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_17")
sys.path.insert(0, "../update_14")
from minimum_subsidy import rand_dicho, matrix_realising, subsets  # noqa: E402
from localsearch_lemma import ell_vec, moves  # noqa: E402

NAMES = ["P2", "P3", "P6", "P7", "P8", "P9"]


def psi(name, e, tot, bundles):
    mx = max(e)
    cnt = sum(1 for x in e if x == mx)
    mxsize = max(len(b) for b in bundles)
    sq = sum(len(b) ** 2 for b in bundles)
    return {"P2": (mx, cnt, mxsize),
            "P3": (mx, cnt, sq),
            "P6": (mx, sq),
            "P7": (mx, mxsize),
            "P8": (sum(e), sq),
            "P9": (mx, cnt, sq, tot)}[name]


def state(cs, bundles, n):
    best = None
    for perm in permutations(range(n)):
        t = sum(cs[i][bundles[perm[i]]] for i in range(n))
        if best is None or t < best[0]:
            best = (t, perm)
    t, perm = best
    a = [[cs[i][bundles[perm[j]]] for j in range(n)] for i in range(n)]
    return ell_vec(a, n), t


def test(cs, m, n, sample=None, rng=None):
    memo = {}

    def get(b):
        k = tuple(sorted(tuple(sorted(x)) for x in b))
        if k not in memo:
            memo[k] = state(cs, b, n)
        return memo[k]

    if sample is None:
        it = product(range(n), repeat=m)
    else:
        it = ([rng.randrange(n) for _ in range(m)] for _ in range(sample))
    stuck = Counter()
    has_good = False
    for assign in it:
        bundles = tuple(frozenset(g for g in range(m) if assign[g] == i)
                        for i in range(n))
        e, t = get(bundles)
        if e is None:
            continue
        if max(e) <= 1:
            has_good = True
            continue
        nbrs = [(nb,) + get(nb) for nb in moves(bundles, n, m, swaps=False)]
        for name in NAMES:
            cur = psi(name, e, t, bundles)
            if not any(ne is not None and psi(name, ne, nt, nb) < cur
                       for nb, ne, nt in nbrs):
                stuck[name] += 1
    return stuck, has_good


def setsplit_instances():
    """R10's certified-hard family: EF-free by construction."""
    from setsplit_family import build, costs_from_D
    out = []
    for U, F in [(["a"], [["a"]]),
                 (["a", "b"], [["a"], ["b"]]),
                 (["a", "b"], [["a"], ["a", "b"]]),
                 (["a", "b", "c"], [["a"], ["b", "c"]])]:
        n, m, D, _, _, _ = build(U, F)
        if n ** m > 200000:
            continue
        out.append((costs_from_D(m, n, D), m, n))
    return out


def main():
    rng = random.Random(777001)
    fails = Counter()
    stuckparts = Counter()
    tot = 0
    effree = 0

    print("=== (a) EF-free and non-additive instances, exhaustive ===")
    for (n, m, T) in [(3, 4, 1200), (3, 5, 800), (3, 6, 200),
                      (4, 4, 800), (4, 5, 250), (5, 4, 200), (5, 5, 60)]:
        for _ in range(T):
            cs = (matrix_realising(m, n, rng, 3) if rng.random() < 0.5
                  else [rand_dicho(m, rng, rng.choice([0.0, 0.15, 0.5, 0.85, 1.0]))
                        for _ in range(n)])
            if max(max(c.values()) for c in cs) < 2:
                continue
            # keep only instances with NO exactly envy-free allocation
            ef = any(all(cs[i][bd[i]] <= cs[i][bd[j]]
                         for i in range(n) for j in range(n))
                     for bd in [tuple(frozenset(g for g in range(m) if a[g] == i)
                                      for i in range(n))
                                for a in product(range(n), repeat=m)])
            if ef:
                continue
            effree += 1
            tot += 1
            st, _ = test(cs, m, n)
            for name in NAMES:
                if st[name]:
                    fails[name] += 1
                    stuckparts[name] += st[name]
    print("  EF-free instances tested: %d" % effree)

    print()
    print("=== (b) R10 Set-Splitting family (certified hard) ===")
    for cs, m, n in setsplit_instances():
        tot += 1
        st, good = test(cs, m, n)
        print("  n=%d m=%d : good allocation exists=%s ; stuck %s"
              % (n, m, good, {k: st[k] for k in NAMES if st[k]} or "none"))
        for name in NAMES:
            if st[name]:
                fails[name] += 1
                stuckparts[name] += st[name]

    print()
    print("=== summary over %d hard instances ===" % tot)
    print("  potential   instances with stuck partition   stuck partitions")
    for name in NAMES:
        print("    %-4s      %6d                            %d"
              % (name, fails[name], stuckparts[name]))
    print()
    surv = [n for n in NAMES if fails[n] == 0]
    print("  surviving: %s" % (", ".join(surv) if surv else "NONE"))


if __name__ == "__main__":
    main()
