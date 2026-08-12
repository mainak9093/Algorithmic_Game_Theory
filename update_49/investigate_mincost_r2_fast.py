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
    return best

def ef_works(D, perm):
    for p in SUBSIDIES:
        if all(D[(a,perm[a])]-p[a] <= D[(a,perm[b])]-p[b] for a in AGENTS for b in AGENTS):
            return True
    return False

def main():
    offdiag = [(i,j) for i in AGENTS for j in AGENTS if i!=j]
    mukeys = [(i,e,j) for i in AGENTS for e in (1,2) for j in AGENTS if i!=j]
    vals = range(BOUND+1)
    checked=0; mincost_fails=0
    for Cvals in itertools.product(vals, repeat=len(offdiag)):
        C = dict(zip(offdiag,Cvals))
        for muvals in itertools.product((0,1), repeat=len(mukeys)):
            mu = dict(zip(mukeys,muvals))
            checked+=1
            ok = False
            for (m1,m2) in ORDERED_TARGET_PAIRS:
                D = build_D(C,mu,m1,m2)
                for perm in min_cost_perm(D):
                    if ef_works(D,perm):
                        ok = True
                        break
                if ok: break
            if not ok:
                mincost_fails += 1
                if mincost_fails <= 5:
                    print("MIN-COST FAILS:", C, mu)
    print(f"checked={checked} mincost_fails={mincost_fails}")

if __name__=="__main__":
    main()
