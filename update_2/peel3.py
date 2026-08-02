"""Clean fixed-point computation over the FULL peel state space of the Theorem E witness."""
from itertools import permutations, combinations, product
M=('a1','a2','g'); n=3
C=[lambda S: max(0,len(S)-1), lambda S: len(S), lambda S: len(S)]
def inv(W):
    A=[[C[i](W[i])-C[i](W[k]) if i!=k else 0 for k in range(n)] for i in range(n)]
    for r in range(2,n+1):
        for sub in combinations(range(n),r):
            for per in permutations(sub[1:]):
                cyc=(sub[0],)+per
                if sum(A[cyc[t]][cyc[(t+1)%r]] for t in range(r))>0: return False
    for s in range(n):
        for r in range(1,n):
            for sub in permutations([v for v in range(n) if v!=s],r):
                p=(s,)+sub
                if sum(A[p[t]][p[t+1]] for t in range(r))>1: return False
    return True
# state = tuple over types of the nonempty owner-candidate set S_j
NE=[frozenset(s) for r in range(1,n+1) for s in combinations(range(n),r)]
states=[st for st in product(NE,repeat=len(M))]
def toW(st): return [frozenset(M[t] for t in range(len(M)) if i in st[t]) for i in range(n)]
legal={st for st in states if inv(toW(st))}
term={st for st in legal if all(len(s)==1 for s in st)}
def succ(st):
    out=[]
    for t,s in enumerate(st):                                   # peels
        if len(s)>=2:
            for x in s:
                out.append(tuple(st[:t])+(frozenset(s-{x}),)+tuple(st[t+1:]))
    for sig in permutations(range(n)):                          # workload permutations
        if sig!=tuple(range(n)):
            out.append(tuple(frozenset(sig.index(i) for i in s) for s in st))
    return out
good=set(term); changed=True
while changed:
    changed=False
    for st in legal-good:
        if any(v in good for v in succ(st) if v in legal):
            good.add(st); changed=True
root=tuple(frozenset(range(n)) for _ in M)
dead=sorted(legal-good, key=lambda st:[sorted(s) for s in st])
print(f"total states                 : {len(states)}")
print(f"invariant-respecting states  : {len(legal)}")
print(f"terminal (partition) states  : {len(term)}   of which invariant-respecting: {len(term)}")
print(f"states that CAN reach a terminal within the invariant : {len(good)}")
print(f"invariant-respecting DEAD ENDS (peels AND permutations): {len(dead)}")
print(f"root is good                 : {root in good}")
print("\ndead ends (owner-candidate sets per type a1,a2,g -> workloads):")
for st in dead:
    W=toW(st); print("   ", [sorted(w) for w in W])
print("\nreachable terminal allocations:")
for st in sorted(term&good, key=str):
    W=toW(st); own={M[t]:list(st[t])[0] for t in range(len(M))}
    print("   ", [sorted(j for j in M if own[j]==i) for i in range(n)])
