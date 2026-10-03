"""
Experiment 8: pure dichotomous goods, allocated BEFORE any subsidy by
source-SCC moves, then completed in one shot.

    python goods_only_check.py [n] [m] [trials] [seed] [variant]

variant INC: one good at a time, envy-free throughout, with any envy-free
             reassignment of the bundles (rules E1/E2 of eqgraph_maximal).
variant MAX: any envy-free extension (also pairs and handouts to several
             agents, with reassignment).

At the halt: leftover count; whether the leftovers inject into agents valuing
them at +1 (bundles as they are, or after an envy-free reassignment); whether
that one-shot completion has subsidy <= 1 (the goods completion lemma says it
must, whenever the injection exists); and whether ANY completion does.
"""
import itertools
import random
import sys
from collections import Counter

import eqgraph_signed as eg
import eqgraph_maximal as em


def inc_phase(v, n, m, rng):
    X, R = [0] * n, set(range(m))
    while R:
        perms = em.ef_perms(v, X, n)
        cand = []
        for perm in perms:
            Y = [X[perm[i]] for i in range(n)]
            for e in sorted(R):
                for a in range(n):
                    if em.try_add(v, Y, [(e, a)], n) is not None:
                        cand.append((perm, e, a))
            if cand:
                break
        if not cand:
            break
        perm, e, a = rng.choice(cand)
        X = [X[perm[i]] for i in range(n)]
        X[a] |= 1 << e
        R.discard(e)
    return X, R


def injection(v, X, R, n):
    return eg.sdr(sorted(R), list(range(n)), lambda g, t: eg.marg(v, t, g, X[t]) == 1)


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    m = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    trials = int(sys.argv[3]) if len(sys.argv) > 3 else 2000
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    variant = sys.argv[5] if len(sys.argv) > 5 else "INC"
    rng = random.Random(seed)
    tally, left = Counter(), Counter()
    for _ in range(trials):
        fam = rng.choice(["random", "additive"])
        v, cm = eg.random_instance(n, m, rng, "objective", fam, p_chore=0.0,
                                   p_one=rng.choice([0.3, 0.5, 0.7]))
        if variant == "INC":
            X, R = inc_phase(v, n, m, rng)
        else:
            X, R, _ = em.maximal_phase(v, n, m, cm, rng)
        if not R:
            tally["all goods placed, envy-free, no subsidy"] += 1
            continue
        left[len(R)] += 1
        inj = injection(v, X, R, n)
        if inj is None:
            for perm in em.ef_perms(v, X, n)[1:]:
                Y = [X[perm[i]] for i in range(n)]
                if injection(v, Y, R, n) is not None:
                    X, inj = Y, injection(v, Y, R, n)
                    break
        if inj is None:
            anyc = eg.exists_unit_completion(v, X, R, n, permute=True)
            tally["NO injection, even after reassignment | some completion: %s" % anyc] += 1
            continue
        A = list(X)
        for g, t in inj.items():
            A[t] |= 1 << g
        s = eg.max_min_subsidy(v, A, n)
        tally["injection exists -> one-shot completion %s" %
              ("OK" if s is not None and s <= 1 else "FAILS (lemma violated!)")] += 1
    print("n=%d m=%d trials=%d seed=%d variant=%s (pure goods)" % (n, m, trials, seed, variant))
    for k, c in sorted(tally.items(), key=lambda kv: -kv[1]):
        print("  %6d  %s" % (c, k))
    print("  leftover goods at halt:", dict(sorted(left.items())))


if __name__ == "__main__":
    main()
