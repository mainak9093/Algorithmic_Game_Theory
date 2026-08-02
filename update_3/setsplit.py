import itertools, math
# R10 (Bhaskar-Sricharan-Vaish) Set-Splitting reduction, NO-instance:
# U={v1,v2,v3}, F={{v1,v2},{v1,v3},{v2,v3}}  (K3: not 2-colourable) => no EF allocation.
# q=3, r=3, r'=3  =>  n = r'+2 = 5 agents, m = r'+q = 6 chores.
# agents: e1,e2,e3 (edge agents), c1,c2 (colour agents)
# chores: D1,D2,D3 (dummies), V1,V2,V3 (vertex chores)
names_ag = ['e1','e2','e3','c1','c2']
names_ch = ['D1','D2','D3','V1','V2','V3']
E = [{0,1},{0,2},{1,2}]          # hyperedges over vertices 0,1,2
V = [[0]*6 for _ in range(5)]
for i in range(5):
    for j in range(3): V[i][j] = -1          # dummies: -1 for everyone
for i in range(3):
    for j in range(3):
        V[i][3+j] = -1 if j in E[i] else 0   # edge agent i vs vertex chore j
# colour agents value all vertex chores at 0 (already set)

n,m = 5,6
NEG = -10**9
def analyse(alloc):
    bundle_val = [[0]*n for _ in range(n)]    # bundle_val[i][k] = v_i(A_k)
    for j,owner in enumerate(alloc):
        for i in range(n): bundle_val[i][owner] += V[i][j]
    w = [[bundle_val[i][k]-bundle_val[i][i] for k in range(n)] for i in range(n)]
    # longest path (max-weight) via Floyd-Warshall on w, allowing empty path
    d = [[w[i][k] if i!=k else 0 for k in range(n)] for i in range(n)]
    for t in range(n):
        for i in range(n):
            for k in range(n):
                if d[i][t]+d[t][k] > d[i][k]: d[i][k] = d[i][t]+d[t][k]
    for i in range(n):
        if d[i][i] > 0: return None            # positive cycle -> not envy-freeable
    ell = [max(0, max(d[i])) for i in range(n)]
    return ell

best_tot, best_max, best = math.inf, math.inf, None
counts = {}
ef_exists = False
for alloc in itertools.product(range(n), repeat=m):
    ell = analyse(alloc)
    if ell is None: continue
    tot, mx = sum(ell), max(ell)
    counts[tot] = counts.get(tot,0)+1
    if tot == 0: ef_exists = True
    if (mx,tot) < (best_max,best_tot):
        best_max, best_tot, best = mx, tot, (alloc, ell)

print("value matrix (rows=agents, cols=chores):")
print("      " + "  ".join(f"{c:>3}" for c in names_ch))
for i,a in enumerate(names_ag): print(f"  {a}: " + "  ".join(f"{V[i][j]:>3}" for j in range(m)))
print()
print("envy-free (zero-subsidy) allocation exists:", ef_exists)
print("min total subsidy over all allocations:", best_tot, " min max-per-agent:", best_max)
alloc, ell = best
print("witness allocation:")
for i,a in enumerate(names_ag):
    print(f"   {a}: {[names_ch[j] for j in range(m) if alloc[j]==i]}   p={ell[i]}")
print("distribution of total subsidy over envy-freeable allocations:",
      dict(sorted(counts.items())[:6]))
