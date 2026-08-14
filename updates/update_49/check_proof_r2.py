"""CHECK (not proof) of the new logical argument for |R|=2.

Restrict the abstract model to instances that can actually arise when Tao et
al.'s Algorithm 3 halts with 2 unallocated items at n=3, i.e. impose:
  (S1) the indifference graph (edge i->j iff c_i(X_i)=c_i(X_j), i!=j) is
       STRONGLY CONNECTED on all 3 agents  [their tail-SCC stopping rule]
  (S2) for every edge (i,j) on a directed cycle, c_i(e|X_j)=1 for both items
       [their rotation rule did not fire]  -- in a strongly connected digraph
       every edge is on a cycle, so this applies to every edge
  (S3) c_i(e|X_i)=1 for all i, e  [their free-item rule did not fire]

Claim proved by hand: under (S1)-(S3), for ANY placement of the two items
into two DISTINCT bundles and ANY min-cost assignment, longest path <= 1.
"""
import itertools
from excess_theory import AG, longest_path, PERMS
offdiag=[(i,j) for i in AG for j in AG if i!=j]
mukeys=[(i,e,j) for i in AG for e in (1,2) for j in AG if i!=j]
PAIRS=[(a,b) for a in AG for b in AG if a!=b]

def strongly_connected(edges):
    def reach(s):
        seen={s}; st=[s]
        while st:
            u=st.pop()
            for v in AG:
                if v!=u and (u,v) in edges and v not in seen:
                    seen.add(v); st.append(v)
        return seen
    return all(reach(s)=={0,1,2} for s in AG)

total=0; checked=0; fails=0; ex=[]
for Cv in itertools.product(range(3),repeat=6):
    C=dict(zip(offdiag,Cv))
    edges={(i,j) for (i,j) in offdiag if C[(i,j)]==0}   # c_i(X_i)=0 diagonal, so indiff iff C=0
    if not strongly_connected(edges): continue
    for muv in itertools.product((0,1),repeat=12):
        mu=dict(zip(mukeys,muv)); total+=1
        # (S2): every edge is on a cycle (strongly connected) -> marginal must be 1
        if any(mu[(i,e,j)]!=1 for (i,j) in edges for e in (1,2)): continue
        checked+=1
        for (m1,m2) in PAIRS:
            D={}
            for i in AG:
                for j in AG:
                    b=0 if i==j else C[(i,j)]
                    if j==m1: b += (1 if i==m1 else mu[(i,1,m1)])
                    if j==m2: b += (1 if i==m2 else mu[(i,2,m2)])
                    D[(i,j)]=b
            mc=min(sum(D[(a,p[a])] for a in AG) for p in PERMS)
            for p in PERMS:
                if sum(D[(a,p[a])] for a in AG)!=mc: continue
                lp=longest_path(D,p)
                if lp is None or max(lp.values())>1:
                    fails+=1
                    if len(ex)<3: ex.append((dict(C),dict(mu),(m1,m2),p,None if lp is None else max(lp.values())))
print(f"instances with strongly-connected indifference graph: {total}")
print(f"  ...also satisfying the forced-marginal condition: {checked}")
print(f"  FAILURES of the claim (any distinct placement, any min-cost perm): {fails}")
for e in ex: print("  FAIL:",e)
