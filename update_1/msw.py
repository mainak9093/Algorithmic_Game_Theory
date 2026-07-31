from itertools import product
import random,sys
from fast import rand_dicho

def ellvec(cs,bd,n):
    W=[[cs[i][bd[i]]-cs[i][bd[j]] for j in range(n)] for i in range(n)]
    e=[0]*n
    for _ in range(n+1):
        ch=False; new=list(e)
        for i in range(n):
            for j in range(n):
                if i!=j and W[i][j]+e[j]>new[i]: new[i]=W[i][j]+e[j]; ch=True
        e=new
        if not ch: return e
    return None

# The driver below used to run at module level, which meant that merely
# importing msw (tiebreak.py and localsearch.py import ellvec from here) parsed
# sys.argv and crashed unless four integer arguments happened to be present.
# That is why binadd.py carries its own inlined copy of ellvec.  Guarded now;
# behaviour when run as a script is unchanged.
def main():
    m,n,T,seed=map(int,sys.argv[1:5])
    rng=random.Random(seed)
    allMSWbad=0; someMSWgood=0; noMSWgood=0
    for t in range(T):
        cs=[rand_dicho(m,rng) for _ in range(n)]
        allocs=[]
        best=10**9
        for assign in product(range(n),repeat=m):
            bd=[frozenset(g for g in range(m) if assign[g]==i) for i in range(n)]
            tot=sum(cs[i][bd[i]] for i in range(n))
            if tot<best: best=tot; allocs=[bd]
            elif tot==best: allocs.append(bd)
        vals=[]
        for bd in allocs:
            e=ellvec(cs,bd,n)
            vals.append(10**9 if e is None else max(e))
        if min(vals)<=1: someMSWgood+=1
        else:
            noMSWgood+=1
            if noMSWgood<=2:
                print("MSW-optimal never suffices! n=%d m=%d trial=%d minmax=%d"%(n,m,t,min(vals)),flush=True)
                for i,c in enumerate(cs):
                    print("  agent",i,{tuple(sorted(k)):v for k,v in sorted(c.items(),key=lambda kv:(len(kv[0]),sorted(kv[0])))})
        if max(vals)>1: allMSWbad+=1
    print("n=%d m=%d T=%d | some MSW-opt alloc has subsidy<=1: %d | none does: %d | at least one MSW-opt alloc is bad: %d"
          %(n,m,T,someMSWgood,noMSWgood,allMSWbad))

if __name__=="__main__":
    main()
