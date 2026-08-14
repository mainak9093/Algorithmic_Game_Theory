"""
Same check for the |R|=2 doubly-stuck case: does the MINIMUM TOTAL COST
assignment (over the choice of which two distinct bundles absorb e1,e2)
always achieve the {0,1}-subsidy rescue?
"""
import itertools
from exhaustive_r2_shapeB import AGENTS, PERMS, SUBSIDIES, ORDERED_TARGET_PAIRS

BOUND = 2

def Cget(C,i,j): return 0 if i==j else C[(i,j)]
def muget(mu,i,e,j): return 1 if i==j else mu[(i,e,j)]

def build_D(C, mu, m1, m2):
    D = {}
    for i in AGENTS:
        for j in AGENTS:
            val = Cget(C,i,j)
            if j==m1: val += muget(mu,i,1,m1)
            if j==m2: val += muget(mu,i,2,m2)
            D[(i,j)] = val
    return D

def min_cost_perm(D):
    best=None; bestcost=None
    for perm in PERMS:
        cost = sum(D[(a,perm[a])] for a in AGENTS)
        if bestcost is None or cost<bestcost:
            bestcost=cost; best=[perm]
        elif cost==bestcost:
            best.append(perm)
    return best,bestcost

def ef_works(D, perm):
    for p in SUBSIDIES:
        if all(D[(a,perm[a])]-p[a] <= D[(a,perm[b])]-p[b] for a in AGENTS for b in AGENTS):
            return True
    return False

def main():
    offdiag = [(i,j) for i in AGENTS for j in AGENTS if i!=j]
    mukeys = [(i,e,j) for i in AGENTS for e in (1,2) for j in AGENTS if i!=j]
    vals = range(BOUND+1)
    checked=0; mincost_suffices=0; mincost_fails_other_works=0
    fails=[]
    for Cvals in itertools.product(vals, repeat=len(offdiag)):
        C = dict(zip(offdiag,Cvals))
        for muvals in itertools.product((0,1), repeat=len(mukeys)):
            mu = dict(zip(mukeys,muvals))
            checked+=1
            found_mincost=False; found_any=False
            for (m1,m2) in ORDERED_TARGET_PAIRS:
                D = build_D(C,mu,m1,m2)
                bestperms,_ = min_cost_perm(D)
                for perm in bestperms:
                    if ef_works(D,perm): found_mincost=True
                for perm in PERMS:
                    if ef_works(D,perm): found_any=True
            if found_mincost: mincost_suffices+=1
            elif found_any:
                mincost_fails_other_works+=1
                if len(fails)<5: fails.append((dict(C),dict(mu)))
    print(f"checked={checked} mincost_suffices={mincost_suffices} mincost_fails_but_other_works={mincost_fails_other_works}")
    for f in fails: print("  counterexample:", f)

if __name__=="__main__":
    main()
