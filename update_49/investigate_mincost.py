"""
Investigate: among the 1755 |R|=1 "needs-permutation" cases (BOUND=2), is it
ALWAYS the case that the MINIMUM TOTAL COST assignment achieves the EF+{0,1}
subsidy rescue? If so, that's a clean, n-general PRINCIPLE (competitive
equilibrium of the optimal assignment) rather than "try all permutations."
"""
import itertools
from exhaustive_r1 import AGENTS, PERMS, SUBSIDIES

BOUND = 2

def Cget(C,i,j): return 0 if i==j else C[(i,j)]
def muget(mu,i,j): return 1 if i==j else mu[(i,j)]

def build_D(C, mu, m):
    return {(i,j): Cget(C,i,j) + (muget(mu,i,m) if j==m else 0) for i in AGENTS for j in AGENTS}

def min_cost_perm(D):
    best = None; bestcost = None
    for perm in PERMS:
        cost = sum(D[(a,perm[a])] for a in AGENTS)
        if bestcost is None or cost < bestcost:
            bestcost = cost; best = [perm]
        elif cost == bestcost:
            best.append(perm)
    return best, bestcost

def ef_works_for_perm(D, perm):
    for p in SUBSIDIES:
        if all(D[(a,perm[a])] - p[a] <= D[(a,perm[b])] - p[b] for a in AGENTS for b in AGENTS):
            return True, p
    return False, None

def main():
    offdiag = [(i,j) for i in AGENTS for j in AGENTS if i!=j]
    vals = range(BOUND+1)
    total_needing_perm = 0
    mincost_suffices = 0
    mincost_fails_but_other_works = 0
    examples_fail = []
    for Cvals in itertools.product(vals, repeat=len(offdiag)):
        C = dict(zip(offdiag, Cvals))
        for muvals in itertools.product((0,1), repeat=len(offdiag)):
            mu = dict(zip(offdiag, muvals))
            # does identity+subsidy(any m) work? (the "easy" cases, skip)
            identity_works = False
            for m in AGENTS:
                D = build_D(C, mu, m)
                ok,_ = ef_works_for_perm(D, (0,1,2))
                if ok: identity_works = True; break
            if identity_works:
                continue
            total_needing_perm += 1
            # now check: does the min-cost permutation (for SOME m) work?
            found_mincost = False
            found_any = False
            for m in AGENTS:
                D = build_D(C, mu, m)
                bestperms, bestcost = min_cost_perm(D)
                for perm in bestperms:
                    ok,_ = ef_works_for_perm(D, perm)
                    if ok:
                        found_mincost = True
                for perm in PERMS:
                    ok,_ = ef_works_for_perm(D, perm)
                    if ok:
                        found_any = True
            if found_mincost:
                mincost_suffices += 1
            elif found_any:
                mincost_fails_but_other_works += 1
                if len(examples_fail) < 5:
                    examples_fail.append((dict(C), dict(mu)))
    print(f"cases needing permutation: {total_needing_perm}")
    print(f"  min-cost assignment (for some m) suffices: {mincost_suffices}")
    print(f"  min-cost fails but SOME other perm works: {mincost_fails_but_other_works}")
    for ex in examples_fail:
        print("   counterexample to min-cost principle:", ex)

if __name__ == "__main__":
    main()
