from itertools import product
import random,sys
from fast import rand_dicho
from msw import ellvec

m,n,T,seed=map(int,sys.argv[1:5])
rng=random.Random(seed)
fail_psi=0; fail_maxperc=0
for t in range(T):
    cs=[rand_dicho(m,rng) for _ in range(n)]
    best=10**9; allocs=[]
    for assign in product(range(n),repeat=m):
        bd=[frozenset(g for g in range(m) if assign[g]==i) for i in range(n)]
        tot=sum(cs[i][bd[i]] for i in range(n))
        if tot<best: best=tot; allocs=[bd]
        elif tot==best: allocs.append(bd)
    # tie-break 1: minimise Psi = sum_i sum_j c_j(A_i)  (total perceived load)
    def psi(bd): return sum(cs[j][bd[i]] for i in range(n) for j in range(n))
    mp=min(psi(bd) for bd in allocs)
    cand=[bd for bd in allocs if psi(bd)==mp]
    if all((lambda e: e is None or max(e)>1)(ellvec(cs,bd,n)) for bd in cand):
        fail_psi+=1
        if fail_psi<=1:
            print("Psi tie-break FAILS, n=%d m=%d t=%d"%(n,m,t),flush=True)
            for i,c in enumerate(cs):
                print("  agent",i,{tuple(sorted(k)):v for k,v in sorted(c.items(),key=lambda kv:(len(kv[0]),sorted(kv[0])))})
    # tie-break 2: lexicographically minimise sorted-descending vector of perceived loads max_j c_j(A_i)
    def key2(bd): return tuple(sorted((max(cs[j][bd[i]] for j in range(n)) for i in range(n)),reverse=True))
    mk=min(key2(bd) for bd in allocs)
    cand2=[bd for bd in allocs if key2(bd)==mk]
    if all((lambda e: e is None or max(e)>1)(ellvec(cs,bd,n)) for bd in cand2): fail_maxperc+=1
print("n=%d m=%d T=%d | Psi-tiebreak failures=%d | leximin-perceived-load failures=%d"%(n,m,T,fail_psi,fail_maxperc))
