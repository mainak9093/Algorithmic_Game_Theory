"""
Probe Conjecture 2 at n >= 4, residue sizes 2 <= k <= n-2.

Implements TWYZ Algorithm 3 for general n, runs to a halting state, and for
states with 2 <= |R| <= n-2 asks: does SOME placement of R into bundles plus
SOME min-cost assignment give a subsidy in {0,1}^n?

Also records whether condition (P) -- every augmented bundle costs every agent
at least their own bundle plus one -- holds, and whether it holds when the
items are placed only into bundles indexed by the tail SCC S.
"""
import itertools
import random
import sys


def random_dichotomous(m, rng):
    c = {frozenset(): 0}
    for r in range(1, m + 1):
        for S in itertools.combinations(range(m), r):
            S = frozenset(S)
            lo = max(c[S - {b}] for b in S)
            hi = min(c[S - {b}] + 1 for b in S)
            c[S] = rng.randint(lo, hi)
    return c


def marg(c, e, S):
    return c[frozenset(S) | {e}] - c[frozenset(S)]


def envy_graph(costs, X, N):
    return {(i, j) for i in range(N) for j in range(N)
            if i != j and costs[i][frozenset(X[i])] == costs[i][frozenset(X[j])]}


def reach(edges, s, N):
    seen, st = {s}, [s]
    while st:
        u = st.pop()
        for v in range(N):
            if v != u and (u, v) in edges and v not in seen:
                seen.add(v); st.append(v)
    return seen


def path_between(edges, s, t, N):
    if s == t:
        return [s]
    prev, seen, q = {}, {s}, [s]
    while q:
        u = q.pop(0)
        for v in range(N):
            if v != u and (u, v) in edges and v not in seen:
                seen.add(v); prev[v] = u
                if v == t:
                    p, cur = [t], t
                    while cur != s:
                        cur = prev[cur]; p.append(cur)
                    return p[::-1]
                q.append(v)
    return None


def on_cycle(edges, i, j, N):
    return path_between(edges, j, i, N) is not None


def sccs(edges, N):
    comps, un = [], set(range(N))
    while un:
        s = next(iter(un))
        f = reach(edges, s, N)
        r = {v for v in range(N) if s in reach(edges, v, N)}
        comp = (f & r) | {s}
        comps.append(comp); un -= comp
    return comps


def tail_scc(edges, N):
    for comp in sccs(edges, N):
        if not any((u, v) in edges for u in comp for v in range(N) if v not in comp):
            return comp
    return None


def algorithm3(costs, m, N):
    X = [set() for _ in range(N)]
    R = set(range(m))
    while R:
        E = envy_graph(costs, X, N)
        fired = False
        for e in sorted(R):
            for i in range(N):
                if marg(costs[i], e, X[i]) == 0:
                    X[i].add(e); R.discard(e); fired = True; break
            if fired: break
        if fired: continue
        for e in sorted(R):
            for (i, j) in sorted(E):
                if not on_cycle(E, i, j, N): continue
                if marg(costs[i], e, X[j]) == 0:
                    cyc = [i] + path_between(E, j, i, N)[:-1]
                    old = [set(b) for b in X]
                    for t, u in enumerate(cyc):
                        X[u] = set(old[cyc[(t + 1) % len(cyc)]])
                    X[i].add(e); R.discard(e); fired = True; break
            if fired: break
        if fired: continue
        S = tail_scc(E, N)
        if len(R) >= len(S):
            for a in sorted(S):
                e = sorted(R)[0]; X[a].add(e); R.discard(e)
            continue
        return [frozenset(b) for b in X], frozenset(R), S
    return [frozenset(b) for b in X], frozenset(R), None


def longest_paths(costs, Y, perm, N):
    W = {(x, y): costs[x][Y[perm[x]]] - costs[x][Y[perm[y]]]
         for x in range(N) for y in range(N) if x != y}
    p = []
    for s in range(N):
        best = 0
        for r in range(1, N):
            for rest in itertools.permutations([v for v in range(N) if v != s], r):
                path = (s,) + rest
                best = max(best, sum(W[(path[t], path[t + 1])] for t in range(len(path) - 1)))
        p.append(best)
    return p


def works(costs, Y, perm, N):
    p = longest_paths(costs, Y, perm, N)
    if max(p) > 1:
        return False, p
    ok = all(costs[a][Y[perm[a]]] - p[a] <= costs[a][Y[perm[b]]] - p[b]
             for a in range(N) for b in range(N))
    return ok, p


def main(N=4, m=5, trials=400, seed=1):
    rng = random.Random(seed)
    found = 0
    no_solution = 0
    P_holds_any = 0
    P_holds_S = 0
    for t in range(trials):
        costs = [random_dichotomous(m, rng) for _ in range(N)]
        X, R, S = algorithm3(costs, m, N)
        k = len(R)
        if not (2 <= k <= N - 2):
            continue
        found += 1
        Rl = sorted(R)

        # does SOME placement + min-cost assignment work?
        solved = False
        for place in itertools.product(range(N), repeat=k):
            Y = [set(b) for b in X]
            for e, d in zip(Rl, place):
                Y[d].add(e)
            Y = [frozenset(b) for b in Y]
            best = min(sum(costs[a][Y[pm[a]]] for a in range(N))
                       for pm in itertools.permutations(range(N)))
            for pm in itertools.permutations(range(N)):
                if sum(costs[a][Y[pm[a]]] for a in range(N)) != best:
                    continue
                ok, p = works(costs, Y, pm, N)
                if ok:
                    solved = True; break
            if solved: break
        if not solved:
            no_solution += 1
            print(f"  trial {t}: NO placement/assignment works!  |R|={k} S={S}")
            print(f"    X={[sorted(b) for b in X]} R={Rl}")

        # condition (P) for distinct-bundle placements
        def P_for(idxs):
            return all(costs[a][X[j] | {e}] >= costs[a][X[a]] + 1
                       for a in range(N) for j in idxs for e in R)
        anyP = any(P_for(idx) for idx in itertools.combinations(range(N), k))
        if anyP: P_holds_any += 1
        if S is not None and len(S) >= k:
            if any(P_for(idx) for idx in itertools.combinations(sorted(S), k)):
                P_holds_S += 1
    print(f"n={N} m={m} trials={trials} seed={seed}")
    print(f"  halting states with 2<=|R|<=n-2: {found}")
    print(f"  of those, NO placement+assignment achieves p in {{0,1}}^n: {no_solution}")
    print(f"  (P) holds for some choice of k distinct bundles: {P_holds_any}/{found}")
    print(f"  (P) holds for some k bundles inside S:          {P_holds_S}/{found}")
    return no_solution


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    m = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    tr = int(sys.argv[3]) if len(sys.argv) > 3 else 400
    sd = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    main(N, m, tr, sd)
