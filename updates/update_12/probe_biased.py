"""Same construction test, but with a generator biased toward marginal 1,
which makes Algorithm 3 halt with LARGER residues (the uncovered range)."""
import itertools, random, sys
from probe_n4 import algorithm3, longest_paths

def biased_dichotomous(m, rng, pbias):
    c = {frozenset(): 0}
    for r in range(1, m+1):
        for S in itertools.combinations(range(m), r):
            S = frozenset(S)
            lo = max(c[S-{b}] for b in S); hi = min(c[S-{b}]+1 for b in S)
            c[S] = hi if (lo != hi and rng.random() < pbias) else lo
    return c

def test(N, m, trials, seed, pbias):
    rng = random.Random(seed)
    stats={}; fails=0; checked=0
    for t in range(trials):
        costs=[biased_dichotomous(m,rng,pbias) for _ in range(N)]
        X,R,S=algorithm3(costs,m,N); k=len(R)
        stats[k]=stats.get(k,0)+1
        if k==0: continue
        assert len(S)>=k+1
        Sl=sorted(S); out=[x for x in range(N) if x not in S]; Rl=sorted(R)
        for T in itertools.permutations(Sl,k):
            Y=[set(b) for b in X]
            for e,j in zip(Rl,T): Y[j].add(e)
            Y=[frozenset(b) for b in Y]
            best=min(sum(costs[a][Y[sg[i]]] for i,a in enumerate(Sl))
                     for sg in itertools.permutations(Sl))
            for sg in itertools.permutations(Sl):
                if sum(costs[a][Y[sg[i]]] for i,a in enumerate(Sl))!=best: continue
                perm=list(range(N))
                for i,a in enumerate(Sl): perm[a]=sg[i]
                for x in out: perm[x]=x
                checked+=1
                p=longest_paths(costs,Y,perm,N)
                ok=all(costs[a][Y[perm[a]]]-p[a] <= costs[a][Y[perm[b]]]-p[b]
                       for a in range(N) for b in range(N))
                if max(p)>1 or min(p)<0 or not ok:
                    fails+=1
                    if fails<=3: print(f"  FAIL k={k} S={Sl} T={T} p={p} ef={ok}")
    print(f"n={N} m={m} bias={pbias} trials={trials} seed={seed}")
    print(f"  residue sizes: {dict(sorted(stats.items()))}")
    print(f"  combos checked: {checked}  FAILURES: {fails}")
    return fails

if __name__=="__main__":
    test(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),float(sys.argv[5]))
