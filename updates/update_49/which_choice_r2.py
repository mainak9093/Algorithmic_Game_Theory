"""For R=2: does choosing the target pair suffice (then ANY min-cost perm works),
or does tie-breaking among min-cost perms also matter?"""
import itertools
from excess_theory import AG, longest_path, PERMS
offdiag=[(i,j) for i in AG for j in AG if i!=j]
mukeys=[(i,e,j) for i in AG for e in (1,2) for j in AG if i!=j]
PAIRS=[(a,b) for a in AG for b in AG if a!=b]
exists_pair_all_perms_ok=0
needs_tiebreak=0
total=0
for Cv in itertools.product(range(3),repeat=6):
    C=dict(zip(offdiag,Cv))
    for muv in itertools.product((0,1),repeat=12):
        mu=dict(zip(mukeys,muv))
        total+=1
        found_clean_pair=False; found_any=False
        for (m1,m2) in PAIRS:
            D={}
            for i in AG:
                for j in AG:
                    b=0 if i==j else C[(i,j)]
                    if j==m1: b += (1 if i==m1 else mu[(i,1,m1)])
                    if j==m2: b += (1 if i==m2 else mu[(i,2,m2)])
                    D[(i,j)]=b
            mc=min(sum(D[(a,p[a])] for a in AG) for p in PERMS)
            mcperms=[p for p in PERMS if sum(D[(a,p[a])] for a in AG)==mc]
            lps=[]
            for p in mcperms:
                lp=longest_path(D,p)
                lps.append(None if lp is None else max(lp.values()))
            good=[x for x in lps if x is not None and x<=1]
            if good: found_any=True
            if lps and all(x is not None and x<=1 for x in lps):
                found_clean_pair=True
        if found_clean_pair: exists_pair_all_perms_ok+=1
        elif found_any: needs_tiebreak+=1
print(f"total={total}")
print(f"  instances with a target pair where EVERY min-cost perm gives lp<=1: {exists_pair_all_perms_ok}")
print(f"  instances needing tie-break among min-cost perms: {needs_tiebreak}")
print(f"  instances with no valid choice at all: {total-exists_pair_all_perms_ok-needs_tiebreak}")
