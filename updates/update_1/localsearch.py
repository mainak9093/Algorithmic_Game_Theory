from itertools import product
import random,sys
from fast import rand_dicho
from msw import ellvec

def score(cs,bd,n):
    e=ellvec(cs,bd,n)
    if e is None: return (10**9,10**9)
    return (max(e),sum(e))

m,n,T,seed=map(int,sys.argv[1:5])
rng=random.Random(seed)
stuck=0; total_bad_starts=0
for t in range(T):
    cs=[rand_dicho(m,rng) for _ in range(n)]
    best=10**9; allocs=[]
    for assign in product(range(n),repeat=m):
        bd=tuple(frozenset(g for g in range(m) if assign[g]==i) for i in range(n))
        tot=sum(cs[i][bd[i]] for i in range(n))
        if tot<best: best=tot; allocs=[bd]
        elif tot==best: allocs.append(bd)
    S=set(allocs)
    for bd in allocs:
        sc=score(cs,bd,n)
        if sc[0]<=1: continue
        total_bad_starts+=1
        # single-chore transfer staying MSW-optimal, strictly improving (max,sum) lexicographically
        improved=False
        for i in range(n):
            for g in bd[i]:
                for j in range(n):
                    if j==i: continue
                    nb=list(bd); nb[i]=bd[i]-{g}; nb[j]=bd[j]|{g}; nb=tuple(nb)
                    if nb in S and score(cs,nb,n)<sc: improved=True; break
                if improved: break
            if improved: break
        if not improved:
            stuck+=1
            if stuck<=1:
                print("LOCAL MIN that is bad, n=%d m=%d t=%d score=%s"%(n,m,t,sc),flush=True)
print("n=%d m=%d T=%d | bad MSW-opt starting points=%d | of which stuck (no improving 1-transfer)=%d"
      %(n,m,T,total_bad_starts,stuck))
