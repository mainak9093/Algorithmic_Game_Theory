"""RULE CANDIDATE: among the 6 ordered distinct target pairs, pick one whose
resulting min-cost total is smallest. Does every min-cost perm then give lp<=1?"""
import itertools
from excess_theory import AG, longest_path, PERMS
offdiag=[(i,j) for i in AG for j in AG if i!=j]
mukeys=[(i,e,j) for i in AG for e in (1,2) for j in AG if i!=j]
PAIRS=[(a,b) for a in AG for b in AG if a!=b]
def buildD(C,mu,m1,m2):
    D={}
    for i in AG:
        for j in AG:
            b=0 if i==j else C[(i,j)]
            if j==m1: b += (1 if i==m1 else mu[(i,1,m1)])
            if j==m2: b += (1 if i==m2 else mu[(i,2,m2)])
            D[(i,j)]=b
    return D
fails=0; total=0; ex=[]
for Cv in itertools.product(range(3),repeat=6):
    C=dict(zip(offdiag,Cv))
    for muv in itertools.product((0,1),repeat=12):
        mu=dict(zip(mukeys,muv)); total+=1
        scored=[]
        for pr in PAIRS:
            D=buildD(C,mu,*pr)
            mc=min(sum(D[(a,p[a])] for a in AG) for p in PERMS)
            scored.append((mc,pr,D))
        best=min(s[0] for s in scored)
        # rule picks ANY cheapest pair -> require ALL cheapest pairs to work (strict test)
        ok_all=True
        for mc,pr,D in scored:
            if mc!=best: continue
            for p in PERMS:
                if sum(D[(a,p[a])] for a in AG)!=mc: continue
                lp=longest_path(D,p)
                if lp is None or max(lp.values())>1: ok_all=False
        if not ok_all:
            fails+=1
            if len(ex)<3: ex.append((dict(C),dict(mu)))
print(f"total={total}  cheapest-pair rule fails (strict, all cheapest pairs): {fails}")
for e in ex: print("  fail:",e)
