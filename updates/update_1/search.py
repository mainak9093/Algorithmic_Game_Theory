from itertools import combinations, combinations_with_replacement, product
import random, sys

def gen_functions(m):
    subs = sorted([frozenset(s) for k in range(m+1) for s in combinations(range(m),k)],
                  key=lambda s:(len(s),sorted(s)))
    res=[]; val={}
    def rec(i):
        if i==len(subs):
            res.append(dict(val)); return
        S=subs[i]
        if len(S)==0:
            val[S]=0; rec(i+1); del val[S]; return
        lo=0; hi=10**9
        for g in S:
            T=S-{g}; lo=max(lo,val[T]); hi=min(hi,val[T]+1)
        for v in range(lo,hi+1):
            val[S]=v; rec(i+1)
        del val[S]
    rec(0); return res

def longest_paths(W,n):
    """W[i][j] arc weights. Return None if a positive-weight cycle exists,
    else vector ell[i] = max weight of a simple path starting at i (>=0, empty path)."""
    # Bellman-Ford style on max-weight walks; positive cycle -> unbounded
    ell=[0]*n
    for it in range(n+1):
        changed=False
        new=list(ell)
        for i in range(n):
            for j in range(n):
                if i==j: continue
                if W[i][j]+ell[j] > new[i]:
                    new[i]=W[i][j]+ell[j]; changed=True
        ell=new
        if not changed: break
    else:
        return None   # still improving after n+1 rounds -> positive cycle
    return ell

def best_subsidy(cs, n, m):
    """min over allocations of max_i ell_i ; returns (best, argbest)"""
    best=10**9; arg=None
    for assign in product(range(n), repeat=m):
        bundles=[frozenset(g for g in range(m) if assign[g]==i) for i in range(n)]
        W=[[0]*n for _ in range(n)]
        for i in range(n):
            ci=cs[i]; own=ci[bundles[i]]
            for j in range(n):
                W[i][j]= own - ci[bundles[j]]
        ell=longest_paths(W,n)
        if ell is None: continue           # not envy-freeable
        v=max(ell)
        if v<best:
            best=v; arg=(bundles,list(ell))
            if best==0: break
    return best,arg

if __name__=="__main__":
    m=int(sys.argv[1]); n=int(sys.argv[2])
    F=gen_functions(m); print("num functions",len(F))
    worst=-1; worstinst=None; cnt=0
    for cs in combinations_with_replacement(F,n):
        cnt+=1
        b,_=best_subsidy(list(cs),n,m)
        if b>worst:
            worst=b; worstinst=cs
            print("new worst",worst,flush=True)
    print("checked",cnt,"instances; worst-case minimum max-subsidy =",worst)
