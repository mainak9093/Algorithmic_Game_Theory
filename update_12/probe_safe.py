"""Is there always a matching of residual items to DISTINCT 'safe' bundles?
(e,j) safe  iff  for all agents x: c_x(X_j + e) >= c_x(X_x) + 1."""
import itertools, random, sys
from probe_n4 import random_dichotomous, algorithm3

def safe(costs, X, N, e, j):
    return all(costs[x][X[j] | {e}] >= costs[x][X[x]] + 1 for x in range(N))

def matching_exists(costs, X, N, R):
    Rl = sorted(R); k = len(Rl)
    for tgt in itertools.permutations(range(N), k):
        if all(safe(costs, X, N, e, j) for e, j in zip(Rl, tgt)):
            return True, tgt
    return False, None

def main(N, m, trials, seed):
    rng = random.Random(seed)
    tot = 0; nomatch = 0; safecounts = {}
    for t in range(trials):
        costs = [random_dichotomous(m, rng) for _ in range(N)]
        X, R, S = algorithm3(costs, m, N)
        k = len(R)
        if not (2 <= k <= N-2): continue
        tot += 1
        ok, tgt = matching_exists(costs, X, N, R)
        if not ok:
            nomatch += 1
            print(f"  trial {t}: NO safe matching! |R|={k} |S|={len(S)}")
            print(f"    X={[sorted(b) for b in X]} R={sorted(R)}")
            for e in sorted(R):
                print(f"      item {e}: safe bundles = {[j for j in range(N) if safe(costs,X,N,e,j)]}")
        else:
            # record min number of safe bundles over items
            mn = min(sum(1 for j in range(N) if safe(costs,X,N,e,j)) for e in R)
            safecounts[mn] = safecounts.get(mn,0)+1
    print(f"n={N} m={m} trials={trials} seed={seed}: states with 2<=|R|<=n-2: {tot}, NO safe matching: {nomatch}")
    print(f"  distribution of (min over items of #safe bundles): {dict(sorted(safecounts.items()))}")
    return nomatch

if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
