import itertools
from excess_theory import AG, analyze
BOUND=2
offdiag=[(i,j) for i in AG for j in AG if i!=j]
mukeys=[(i,e,j) for i in AG for e in (1,2) for j in AG if i!=j]
PAIRS=[(a,b) for a in AG for b in AG if a!=b]
max_eps=0; max_lp=0; bad=0; eps2_count=0
for Cv in itertools.product(range(BOUND+1),repeat=6):
    C=dict(zip(offdiag,Cv))
    for muv in itertools.product((0,1),repeat=12):
        mu=dict(zip(mukeys,muv))
        ok_any=False
        for (m1,m2) in PAIRS:
            D={}
            for i in AG:
                for j in AG:
                    base=0 if i==j else C[(i,j)]
                    if j==m1: base += (1 if i==m1 else mu[(i,1,m1)])
                    if j==m2: base += (1 if i==m2 else mu[(i,2,m2)])
                    D[(i,j)]=base
            for eps,lp in analyze(D):
                max_eps=max(max_eps,eps)
                if eps>=2: eps2_count+=1
                if lp is not None:
                    max_lp=max(max_lp,lp)
                    if lp<=1: ok_any=True
        if not ok_any: bad+=1
print(f"R=2: max sum-of-excess at mincost = {max_eps}; max longest-path over mincost assignments = {max_lp}")
print(f"     instances where NO (target-pair, mincost-perm) gives lp<=1: {bad}")
print(f"     (count of mincost assignments with excess>=2: {eps2_count})")
