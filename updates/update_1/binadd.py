import random, sys
from itertools import product
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

def build(n,m,D):
    """D[i] = set of chores bad for agent i.  Algorithm:
       every non-universally-bad chore -> some agent who finds it free;
       universally-bad chores -> split as evenly as possible."""
    univ=[g for g in range(m) if all(g in D[i] for i in range(n))]
    rest=[g for g in range(m) if g not in univ]
    A=[set() for _ in range(n)]
    for g in rest:
        free=[i for i in range(n) if g not in D[i]]
        A[random.choice(free)].add(g)
    for k,g in enumerate(univ): A[k%n].add(g)
    return [frozenset(a) for a in A]

def costfn(Di):
    return lambda S: len(S & Di)

random.seed(7); worst=0; T=200000
for t in range(T):
    n=random.randint(2,5); m=random.randint(1,7)
    D=[frozenset(g for g in range(m) if random.random()<0.6) for _ in range(n)]
    A=build(n,m,D)
    cs=[{} for _ in range(n)]
    # build dict lookups only for the bundles we need
    cache=[dict() for _ in range(n)]
    for i in range(n):
        for b in A: cache[i][b]=len(b & D[i])
    e=ellvec(cache,A,n)
    if e is None: print("NOT envy-freeable!",D,A); break
    worst=max(worst,max(e))
    if max(e)>1:
        print("FAILURE",D,[sorted(a) for a in A],e); break
else:
    print("binary-additive construction: %d random instances, max per-agent subsidy ever = %d"%(T,worst))
