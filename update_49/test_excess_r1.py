import itertools
from excess_theory import AG, analyze
BOUND=2
offdiag=[(i,j) for i in AG for j in AG if i!=j]
max_eps=0; max_lp=0; bad=0
for Cv in itertools.product(range(BOUND+1),repeat=6):
    C=dict(zip(offdiag,Cv))
    for muv in itertools.product((0,1),repeat=6):
        mu=dict(zip(offdiag,muv))
        for m in AG:
            D={}
            for i in AG:
                for j in AG:
                    base=0 if i==j else C[(i,j)]
                    if j==m: base += (1 if i==m else mu[(i,m)])
                    D[(i,j)]=base
            res=analyze(D)
            ok=False
            for eps,lp in res:
                max_eps=max(max_eps,eps)
                if lp is not None:
                    max_lp=max(max_lp,lp)
                    if lp<=1: ok=True
            if not ok: bad+=1
print(f"R=1: max sum-of-excess at mincost = {max_eps}; max longest-path = {max_lp}; failures = {bad}")
