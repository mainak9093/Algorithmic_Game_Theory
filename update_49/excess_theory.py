"""Test the epsilon-excess theory: sum of excesses at min-cost assignment,
and the resulting longest-path bound, for R=1 and R=2."""
import itertools
AG=(0,1,2); PERMS=list(itertools.permutations(AG))

def longest_path(D, perm):
    """arc w(a,b) = D[a][perm[a]] - D[a][perm[b]]; longest simple path from each node.
    Returns None if a positive cycle exists (detected via simple-path enumeration blowup proxy)."""
    W = {(a,b): D[(a,perm[a])]-D[(a,perm[b])] for a in AG for b in AG if a!=b}
    # positive cycle check over all simple cycles (n=3: 2-cycles and 3-cycles)
    for a,b in itertools.permutations(AG,2):
        if W[(a,b)]+W[(b,a)] > 0: return None
    for a,b,c in itertools.permutations(AG,3):
        if W[(a,b)]+W[(b,c)]+W[(c,a)] > 0: return None
    best={}
    for start in AG:
        m=0
        for r in (1,2):
            for rest in itertools.permutations([x for x in AG if x!=start], r):
                path=(start,)+rest
                m=max(m,sum(W[(path[t],path[t+1])] for t in range(len(path)-1)))
        best[start]=m
    return best

def analyze(D):
    beta={a:min(D[(a,j)] for j in AG) for a in AG}
    mincost=min(sum(D[(a,p[a])] for a in AG) for p in PERMS)
    out=[]
    for p in PERMS:
        if sum(D[(a,p[a])] for a in AG)!=mincost: continue
        eps=sum(D[(a,p[a])]-beta[a] for a in AG)
        lp=longest_path(D,p)
        out.append((eps, None if lp is None else max(lp.values())))
    return out
