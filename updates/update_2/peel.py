"""
peel.py -- verification for the replica/peel reformulation of PS1.

State: W = (W_1, ..., W_n), W_i subseteq M  ("agent i is still on the hook for W_i").
Arc weight  w_W(i,k) = c_i(W_i) - c_i(W_k).
ell_W(i)   = max weight of a directed path leaving i (0 if none positive).
Envy-freeable iff no positive-weight cycle.
Legal peel (x,j): j in W_x and |S_j| >= 2, where S_j = {i : j in W_i}.
Terminal: |S_j| = 1 for every j; owner(j) = the survivor; A_i = {j : owner(j)=i}.
"""
from itertools import permutations, combinations
import sys

# ---------- Theorem E witness instance ----------
M = ('a1', 'a2', 'g')
n = 3
def c1(S): return max(0, len(S) - 1)          # dichotomous, supermodular
def c2(S): return len(S)
def c3(S): return len(S)
C = [c1, c2, c3]

def arcs(W):
    return [[C[i](W[i]) - C[i](W[k]) if i != k else 0 for k in range(n)] for i in range(n)]

def longest_paths(W):
    """Return (ell, has_positive_cycle) via Bellman-Ford on negated weights /
    direct DP over simple paths -- n is tiny, so enumerate simple paths."""
    A = arcs(W)
    # positive cycle check: enumerate all simple cycles (n<=5 fine)
    pos_cycle = False
    for r in range(2, n + 1):
        for sub in combinations(range(n), r):
            for per in permutations(sub[1:]):
                cyc = (sub[0],) + per
                wt = sum(A[cyc[t]][cyc[(t + 1) % r]] for t in range(r))
                if wt > 0:
                    pos_cycle = True
    # longest simple path from each node (valid as ell when no positive cycle)
    ell = []
    for s in range(n):
        best = 0
        for r in range(1, n):
            for sub in permutations([v for v in range(n) if v != s], r):
                path = (s,) + sub
                wt = sum(A[path[t]][path[t + 1]] for t in range(r))
                best = max(best, wt)
        ell.append(best)
    return ell, pos_cycle

def S(W, j):
    return [i for i in range(n) if j in W[i]]

def invariant_ok(W):
    ell, pc = longest_paths(W)
    return (not pc) and all(e <= 1 for e in ell), ell, pc

def show(tag, W):
    ok, ell, pc = invariant_ok(W)
    print(f"{tag:<34} W={[sorted(w) for w in W]}  ell={tuple(ell)}  sum={sum(ell)}  "
          f"pos_cycle={pc}  invariant={'OK' if ok else 'VIOLATED'}")
    return ok

print("=" * 96)
print("(1) Initial state and the 6-step schedule")
print("=" * 96)
W = [set(M) for _ in range(n)]
show("init (everyone on the hook)", W)
schedule = [(0, 'g'), (1, 'g'), (2, 'a1'), (0, 'a2'), (1, 'a1'), (2, 'a2')]
allok = True
for step, (x, j) in enumerate(schedule, 1):
    assert j in W[x], f"illegal peel: {j} not in W_{x}"
    assert len(S(W, j)) >= 2, f"illegal peel: |S_{j}| < 2"
    hard = all(C[k](W[x]) - C[k](W[x] - {j}) == 1 for k in range(n))
    W[x] = W[x] - {j}
    surv = S(W, j)
    tag = f"step {step}: relieve {x+1} of {j}"
    if len(surv) == 1:
        tag += f"  [owner({j})={surv[0]+1}]"
    allok &= show(tag, W)
    if not hard:
        print("      (note: this peel was NOT the hard case)")
owner = {j: S(W, j)[0] for j in M}
A = [sorted(j for j in M if owner[j] == i) for i in range(n)]
print(f"\nterminal allocation A = {A}    all states respected invariant: {allok}")

print()
print("=" * 96)
print("(2) The Theorem E trap state, translated into peel coordinates")
print("=" * 96)
trap = [set(M), {'g'}, {'g'}]
show("trap: A=({a1,a2},{},{}) + g pending", trap)
print(f"      w(1,2) = c1({{a1,a2,g}}) - c1({{g}}) = {c1(set(M))} - {c1({'g'})} = {c1(set(M)) - c1({'g'})}")

print()
print("=" * 96)
print("(3) Exhaustive search over ALL peel schedules (no permutations used)")
print("=" * 96)
from functools import lru_cache
def key(W): return tuple(frozenset(w) for w in W)
seen, deadends, terminals = {}, [], []
def dfs(W):
    k = key(W)
    if k in seen: return seen[k]
    ok, ell, pc = invariant_ok(list(W))
    if not ok:
        seen[k] = False; return False
    moves = [(x, j) for x in range(n) for j in W[x] if len(S(list(W), j)) >= 2]
    if not moves:
        terminals.append(k); seen[k] = True; return True
    good = False
    for (x, j) in moves:
        W2 = [set(w) for w in W]; W2[x] = W2[x] - {j}
        if dfs(W2): good = True
    if not good: deadends.append(k)
    seen[k] = good
    return good
root = [set(M) for _ in range(n)]
res = dfs(root)
legal_states = sum(1 for v in seen.values() if v is not None)
print(f"invariant-respecting states reachable : {sum(1 for k,v in seen.items())}")
print(f"root can reach a terminal state       : {res}")
print(f"terminal states reached               : {len(set(terminals))}")
print(f"invariant-respecting DEAD ENDS (no legal continuation): {len(set(deadends))}")
for k in sorted(set(deadends))[:5]:
    print("   deadend:", [sorted(s) for s in k])
