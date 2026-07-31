from itertools import combinations, product
import random, sys

def rand_dicho(m,rng):
    subs=sorted([frozenset(s) for k in range(m+1) for s in combinations(range(m),k)],
                key=lambda s:(len(s),sorted(s)))
    val={frozenset():0}
    for S in subs:
        if not S: continue
        lo=0; hi=10**9
        for g in S:
            T=S-{g}; lo=max(lo,val[T]); hi=min(hi,val[T]+1)
        val[S]= hi if (lo!=hi and rng.random()<rng.random()) else lo
    return val

def ok(W,n,cap=1):
    """True iff no positive cycle and all longest paths <= cap."""
    ell=[0]*n
    for _ in range(n+1):
        ch=False; new=list(ell)
        for i in range(n):
            Wi=W[i]
            for j in range(n):
                if i!=j:
                    t=Wi[j]+ell[j]
                    if t>new[i]: new[i]=t; ch=True
        ell=new
        if max(ell)>cap: return False
        if not ch: return True
    return False

def solvable(cs,n,m,cap=1):
    for assign in product(range(n),repeat=m):
        bundles=[frozenset(g for g in range(m) if assign[g]==i) for i in range(n)]
        W=[]
        good=True
        for i in range(n):
            ci=cs[i]; own=ci[bundles[i]]
            row=[own-ci[b] for b in bundles]
            if max(row)>cap: good=False; break
            W.append(row)
        if not good: continue
        if ok(W,n,cap): return bundles
    return None

if __name__=="__main__":
    m,n,T,seed=map(int,sys.argv[1:5])
    rng=random.Random(seed); bad=0
    for t in range(T):
        cs=[rand_dicho(m,rng) for _ in range(n)]
        if solvable(cs,n,m) is None:
            bad+=1
            print("COUNTEREXAMPLE n=%d m=%d trial=%d"%(n,m,t),flush=True)
            for i,c in enumerate(cs):
                print("  agent",i,{tuple(sorted(k)):v for k,v in sorted(c.items(),key=lambda kv:(len(kv[0]),sorted(kv[0])))})
            break
    print("n=%d m=%d trials=%d counterexamples=%d"%(n,m,T,bad),flush=True)
