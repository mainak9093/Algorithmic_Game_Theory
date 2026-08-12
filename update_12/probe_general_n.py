"""Test the S-placement construction for GENERAL n and ALL residue sizes.

Construction: place the k residual items into k distinct bundles indexed by
the tail SCC S; agents outside S keep their own bundles; agents in S receive
S-bundles by a min-cost matching WITHIN S. Then p = Halpern-Shah longest path.

Claim: p in {0,1}^n always.
"""
import itertools, random, sys
from probe_n4 import random_dichotomous, algorithm3, longest_paths

def test(N, m, trials, seed):
    rng = random.Random(seed)
    stats = {}; fails = 0; checked = 0
    for t in range(trials):
        costs = [random_dichotomous(m, rng) for _ in range(N)]
        X, R, S = algorithm3(costs, m, N)
        k = len(R)
        stats[k] = stats.get(k, 0) + 1
        if k == 0: continue
        assert S is not None and len(S) >= k+1, (len(S), k)
        Sl = sorted(S); out = [x for x in range(N) if x not in S]
        Rl = sorted(R)
        # every choice of k distinct S-bundles, every min-cost matching within S
        for T in itertools.permutations(Sl, k):
            Y = [set(b) for b in X]
            for e, j in zip(Rl, T): Y[j].add(e)
            Y = [frozenset(b) for b in Y]
            best = min(sum(costs[a][Y[sg[i]]] for i, a in enumerate(Sl))
                       for sg in itertools.permutations(Sl))
            for sg in itertools.permutations(Sl):
                if sum(costs[a][Y[sg[i]]] for i, a in enumerate(Sl)) != best: continue
                perm = list(range(N))
                for i, a in enumerate(Sl): perm[a] = sg[i]
                for x in out: perm[x] = x
                checked += 1
                p = longest_paths(costs, Y, perm, N)
                ok = all(costs[a][Y[perm[a]]] - p[a] <= costs[a][Y[perm[b]]] - p[b]
                         for a in range(N) for b in range(N))
                if max(p) > 1 or min(p) < 0 or not ok:
                    fails += 1
                    if fails <= 3:
                        print(f"  FAIL t={t} k={k} S={Sl} T={T} p={p} ef={ok}")
    print(f"n={N} m={m} trials={trials} seed={seed}")
    print(f"  residue sizes seen: {dict(sorted(stats.items()))}")
    print(f"  (placement,matching) combinations checked: {checked}   FAILURES: {fails}")
    return fails

if __name__ == "__main__":
    test(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
