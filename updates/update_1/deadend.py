from itertools import combinations, product
from fast import ok
import sys

# ---- hand-built candidate dead-end instance -------------------------------
# items 0=a1, 1=a2, 2=g ; X = all three
def c_super(S):   # agent 1: max(0,|S|-1)   (supermodular, dichotomous)
    return max(0,len(S)-1)
def c_add(S):     # agents 2,3: |S|
    return len(S)
m=3; n=3
cs=[c_super,c_add,c_add]

def envy(bundles):
    return [[cs[i](bundles[i])-cs[i](bundles[j]) for j in range(n)] for i in range(n)]

def ell(W,cap=99):
    e=[0]*n
    for _ in range(n+1):
        ch=False; new=list(e)
        for i in range(n):
            for j in range(n):
                if i!=j and W[i][j]+e[j]>new[i]: new[i]=W[i][j]+e[j]; ch=True
        e=new
        if not ch: return e
    return None  # positive cycle

print("=== partial state: A1={a1,a2}, A2=A3=empty, chore g unallocated ===")
B=[frozenset({0,1}),frozenset(),frozenset()]
W=envy(B); e=ell(W)
print(" envy matrix",W," subsidies",e," -> valid state:", e is not None and max(e)<=1)
print(" marginals of g on own bundle:",[cs[i](B[i]|{2})-cs[i](B[i]) for i in range(n)])
for x in range(n):
    Z=[b|{2} if i==x else b for i,b in enumerate(B)]
    W2=envy(Z); e2=ell(W2)
    print("  insert g into agent %d -> subsidies %s  ok=%s"%(x,e2, e2 is not None and max(e2)<=1))

print("\n=== full instance M={a1,a2,g}: best allocation ===")
best=None
for assign in product(range(n),repeat=m):
    bd=[frozenset(g for g in range(m) if assign[g]==i) for i in range(n)]
    e2=ell(envy(bd))
    if e2 is None: continue
    v=max(e2)
    if best is None or v<best[0]: best=(v,[sorted(b) for b in bd],e2)
print(" min achievable max-subsidy =",best[0]," at allocation",best[1]," subsidies",best[2])
