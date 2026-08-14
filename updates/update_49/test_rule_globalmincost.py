"""Candidate RULE for R=2: among ALL placements of e1,e2 into bundles AND all
assignments, take a globally minimum-total-cost one. Does it always give lp<=1?
(Includes same-bundle placements, so 9 placements x 6 perms.)"""
import itertools
from excess_theory import AG, longest_path, PERMS
offdiag=[(i,j) for i in AG for j in AG if i!=j]
mukeys=[(i,e,j) for i in AG for e in (1,2) for j in AG if i!=j]
PLACE=[(m1,m2) for m1 in AG for m2 in AG]   # includes m1==m2
fails=0; total=0; ex=[]
for Cv in itertools.product(range(3),repeat=6):
    C=dict(zip(offdiag,Cv))
    for muv in itertools.product((0,1),repeat=12):
        mu=dict(zip(mukeys,muv))
        total+=1
        cands=[]
        for (m1,m2) in PLACE:
            D={}
            for i in AG:
                for j in AG:
                    b=0 if i==j else C[(i,j)]
                    if m1==m2:
                        if j==m1:
                            # both items into same bundle: marginal for 2 items, bounded by sum
                            b += (2 if i==m1 else mu[(i,1,m1)]+mu[(i,2,m2)])
                    else:
                        if j==m1: b += (1 if i==m1 else mu[(i,1,m1)])
                        if j==m2: b += (1 if i==m2 else mu[(i,2,m2)])
                    D[(i,j)]=b
            for p in PERMS:
                cands.append((sum(D[(a,p[a])] for a in AG), D, p))
        best=min(c[0] for c in cands)
        lps=[]
        for cost,D,p in cands:
            if cost!=best: continue
            lp=longest_path(D,p)
            lps.append(None if lp is None else max(lp.values()))
        good=[x for x in lps if x is not None and x<=1]
        allgood=lps and all(x is not None and x<=1 for x in lps)
        if not good:
            fails+=1
            if len(ex)<2: ex.append((dict(C),dict(mu)))
print(f"total={total}  global-min-cost rule FAILS on {fails}")
for e in ex: print("  fail:",e)
