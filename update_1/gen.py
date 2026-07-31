from itertools import combinations, product
import sys

def gen_functions(m):
    subs = sorted([frozenset(s) for k in range(m+1) for s in combinations(range(m),k)],
                  key=lambda s:(len(s),sorted(s)))
    res=[]
    val={}
    def rec(i):
        if i==len(subs):
            res.append(dict(val)); return
        S=subs[i]
        if len(S)==0:
            val[S]=0; rec(i+1); del val[S]; return
        lo=0; hi=10**9
        for g in S:
            T=S-{g}
            lo=max(lo,val[T]); hi=min(hi,val[T]+1)
        for v in range(lo,hi+1):
            val[S]=v; rec(i+1)
        del val[S]
    rec(0)
    return res

for m in range(1,5):
    f=gen_functions(m)
    print(m, len(f))
