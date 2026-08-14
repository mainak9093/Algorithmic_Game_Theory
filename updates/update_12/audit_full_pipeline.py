"""
END-TO-END AUDIT of the n=3 proof (approach_12 / approach_13).

This does NOT assume any part of the proof. It:
  1. implements Tao-Wu-Yu-Zhou Algorithm 3 verbatim from the paper,
  2. runs it on random dichotomous instances,
  3. checks the structural claims of the halting lemma independently,
  4. applies the construction the proof prescribes,
  5. verifies the OUTPUT is envy-free with p in {0,1}^3,
     computing p by the Halpern-Shah longest-path formula and ALSO by brute
     force over all p in {0,1}^3, and cross-checking the two.

Any disagreement anywhere is printed.
"""
import itertools
import random
import sys

N = 3
AGENTS = tuple(range(N))


# ---------------------------------------------------------------- instances

def random_dichotomous(m, rng):
    """Uniformly random dichotomous cost function on m items."""
    c = {frozenset(): 0}
    for r in range(1, m + 1):
        for S in itertools.combinations(range(m), r):
            S = frozenset(S)
            lo = max(c[S - {b}] for b in S)
            hi = min(c[S - {b}] + 1 for b in S)
            c[S] = rng.randint(lo, hi)
    return c


def marginal(c, e, S):
    return c[frozenset(S) | {e}] - c[frozenset(S)]


# ------------------------------------------------- TWYZ Algorithm 3 verbatim

def envy_graph(costs, X):
    """arc (i,j), i != j, iff c_i(X_i) == c_i(X_j)."""
    return {(i, j) for i in AGENTS for j in AGENTS
            if i != j and costs[i][frozenset(X[i])] == costs[i][frozenset(X[j])]}


def reachable(edges, s):
    seen, stack = {s}, [s]
    while stack:
        u = stack.pop()
        for v in AGENTS:
            if v != u and (u, v) in edges and v not in seen:
                seen.add(v)
                stack.append(v)
    return seen


def path_between(edges, s, t):
    """a simple directed path s -> ... -> t, or None."""
    if s == t:
        return [s]
    prev, seen, stack = {}, {s}, [s]
    while stack:
        u = stack.pop(0)
        for v in AGENTS:
            if v != u and (u, v) in edges and v not in seen:
                seen.add(v)
                prev[v] = u
                if v == t:
                    path, cur = [t], t
                    while cur != s:
                        cur = prev[cur]
                        path.append(cur)
                    return path[::-1]
                stack.append(v)
    return None


def arc_on_cycle(edges, i, j):
    """arc (i,j) lies on a directed cycle iff there is a path j -> ... -> i."""
    return (i, j) in edges and path_between(edges, j, i) is not None


def sccs(edges):
    comps, unassigned = [], set(AGENTS)
    while unassigned:
        s = next(iter(unassigned))
        fwd = reachable(edges, s)
        rev = {v for v in AGENTS if s in reachable(edges, v)}
        comp = (fwd & rev) | {s}
        comps.append(comp)
        unassigned -= comp
    return comps


def tail_scc(edges):
    """an SCC with no arc leaving it."""
    for comp in sccs(edges):
        if not any((u, v) in edges for u in comp for v in AGENTS if v not in comp):
            return comp
    return None


def twyz_algorithm3(costs, m, rng):
    """Returns (X, R, halted_via_break)."""
    X = [set() for _ in AGENTS]
    R = set(range(m))
    while R:
        E = envy_graph(costs, X)

        # Rule 1
        fired = False
        for e in sorted(R):
            for i in AGENTS:
                if marginal(costs[i], e, X[i]) == 0:
                    X[i].add(e)
                    R.discard(e)
                    fired = True
                    break
            if fired:
                break
        if fired:
            continue

        # Rule 2
        for e in sorted(R):
            for (i, j) in sorted(E):
                if not arc_on_cycle(E, i, j):
                    continue
                if marginal(costs[i], e, X[j]) == 0:
                    cyc = [i] + path_between(E, j, i)[:-1]   # i -> j -> ... -> (back to i)
                    old = [set(b) for b in X]
                    for t, u in enumerate(cyc):
                        v = cyc[(t + 1) % len(cyc)]
                        X[u] = set(old[v])
                    X[i].add(e)
                    R.discard(e)
                    fired = True
                    break
            if fired:
                break
        if fired:
            continue

        # Rule 3
        S = tail_scc(E)
        if len(R) >= len(S):
            for a in sorted(S):
                e = sorted(R)[0]
                X[a].add(e)
                R.discard(e)
            continue
        return [frozenset(b) for b in X], frozenset(R), True
    return [frozenset(b) for b in X], frozenset(R), False


# ------------------------------------------------------ the proof's construction

def is_ef_partial(costs, X):
    return all(costs[i][X[i]] <= costs[i][X[j]] for i in AGENTS for j in AGENTS)


def min_cost_assignments(costs, Y):
    best, out = None, []
    for perm in itertools.permutations(AGENTS):
        tot = sum(costs[a][Y[perm[a]]] for a in AGENTS)
        if best is None or tot < best:
            best, out = tot, [perm]
        elif tot == best:
            out.append(perm)
    return out, best


def hs_longest_path(costs, Y, perm):
    """p_i = max weight of a simple path from i; w(x,y)=c_x(Y_perm[x])-c_x(Y_perm[y])."""
    W = {(x, y): costs[x][Y[perm[x]]] - costs[x][Y[perm[y]]]
         for x in AGENTS for y in AGENTS if x != y}
    p = {}
    for s in AGENTS:
        best = 0
        for r in (1, 2):
            for rest in itertools.permutations([v for v in AGENTS if v != s], r):
                path = (s,) + rest
                best = max(best, sum(W[(path[t], path[t + 1])] for t in range(len(path) - 1)))
        p[s] = best
    return [p[a] for a in AGENTS]


def check_ef_with_subsidy(costs, Y, perm, p):
    return all(costs[a][Y[perm[a]]] - p[a] <= costs[a][Y[perm[b]]] - p[b]
               for a in AGENTS for b in AGENTS)


def brute_force_subsidy_exists(costs, Y, perm):
    for p in itertools.product((0, 1), repeat=N):
        if check_ef_with_subsidy(costs, Y, perm, list(p)):
            return True
    return False


# ------------------------------------------------------------------- audit

def audit(m, trials, seed):
    rng = random.Random(seed)
    stats = {"R0": 0, "R1": 0, "R2": 0}
    problems = []

    for t in range(trials):
        costs = [random_dichotomous(m, rng) for _ in AGENTS]
        X, R, broke = twyz_algorithm3(costs, m, rng)

        # -- the algorithm's own guarantees
        if not is_ef_partial(costs, X):
            problems.append((t, "Algorithm 3 output is NOT envy-free"))
            continue
        if len(R) > N - 1:
            problems.append((t, f"Algorithm 3 left {len(R)} > n-1 items"))
            continue

        stats[f"R{len(R)}"] += 1

        if len(R) == 0:
            if not check_ef_with_subsidy(costs, X, (0, 1, 2), [0, 0, 0]):
                problems.append((t, "|R|=0 but p=0 fails"))
            continue

        # -- structural claims of the halting lemma, checked independently
        if len(R) == N - 1:
            E = envy_graph(costs, X)
            if any(reachable(E, s) != set(AGENTS) for s in AGENTS):
                problems.append((t, "|R|=n-1 but envy graph NOT strongly connected"))
            for i in AGENTS:
                for e in R:
                    if marginal(costs[i], e, X[i]) != 1:
                        problems.append((t, f"c_{i}(e|X_{i}) != 1"))
            for (i, j) in E:
                for e in R:
                    if marginal(costs[i], e, X[j]) != 1:
                        problems.append((t, f"arc ({i},{j}): c_i(e|X_j) != 1"))
            # Lemma "augmented bundles are strictly expensive"
            for a in AGENTS:
                for j in AGENTS:
                    for e in R:
                        if costs[a][X[j] | {e}] < costs[a][X[a]] + 1:
                            problems.append((t, "expensive-lemma VIOLATED"))

        # -- the construction the proof prescribes
        Rl = sorted(R)
        if len(R) == 1:
            placements = [(mm,) for mm in AGENTS]                       # any bundle
        else:
            placements = [(m1, m2) for m1 in AGENTS for m2 in AGENTS if m1 != m2]

        for place in placements:
            Y = [set(b) for b in X]
            for e, dest in zip(Rl, place):
                Y[dest].add(e)
            Y = [frozenset(b) for b in Y]

            perms, _ = min_cost_assignments(costs, Y)
            for perm in perms:
                p = hs_longest_path(costs, Y, perm)
                if any(pi < 0 or pi > 1 for pi in p):
                    problems.append((t, f"subsidy {p} outside {{0,1}} (place={place}, perm={perm})"))
                if not check_ef_with_subsidy(costs, Y, perm, p):
                    problems.append((t, f"HS subsidy {p} does NOT give EF (place={place})"))
                if not brute_force_subsidy_exists(costs, Y, perm):
                    problems.append((t, f"brute force finds NO valid p (place={place}, perm={perm})"))

    print(f"m={m} trials={trials} seed={seed}")
    print(f"  residue sizes: |R|=0 in {stats['R0']}, |R|=1 in {stats['R1']}, |R|=2 in {stats['R2']}")
    print(f"  PROBLEMS: {len(problems)}")
    for p in problems[:10]:
        print("   ", p)
    return len(problems)


if __name__ == "__main__":
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    sys.exit(1 if audit(m, trials, seed) else 0)
