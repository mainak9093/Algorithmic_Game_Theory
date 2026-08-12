import itertools
AG=(0,1,2); PERMS=list(itertools.permutations(AG))
offdiag=[(i,j) for i in AG for j in AG if i!=j]
mukeys=[(i,e,j) for i in AG for e in (1,2) for j in AG if i!=j]
PAIRS=[(a,b) for a in AG for b in AG if a!=b]
best_over_instances=0   # min over target-pairs of (min-cost sum-of-excess); worst case over instances
for Cv in itertools.product(range(3),repeat=6):
    C=dict(zip(offdiag,Cv))
    for muv in itertools.product((0,1),repeat=12):
        mu=dict(zip(mukeys,muv))
        best_here=99
        for (m1,m2) in PAIRS:
            D={}
            for i in AG:
                for j in AG:
                    b=0 if i==j else C[(i,j)]
                    if j==m1: b += (1 if i==m1 else mu[(i,1,m1)])
                    if j==m2: b += (1 if i==m2 else mu[(i,2,m2)])
                    D[(i,j)]=b
            beta={a:min(D[(a,j)] for j in AG) for a in AG}
            mc=min(sum(D[(a,p[a])] for a in AG) for p in PERMS)
            best_here=min(best_here, mc - sum(beta.values()))
        best_over_instances=max(best_over_instances,best_here)
print("R=2: worst-case over instances of [best-over-target-pairs of min-cost excess-sum] =",best_over_instances)
