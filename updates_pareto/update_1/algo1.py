"""
Algorithm 1 of report/sections/main_result.tex, implemented for arbitrary n,
together with the machinery needed to ask whether its output is Pareto optimal.

The n = 3 audit harness in updates_general_binary/update_1/audit_n3_proof.py
hard-codes three agents and stops at the terminal state; this module carries
the construction all the way through the completion and the subsidy set P, for
any n, so that the returned pair (A, p) is exactly what the paper's algorithm
returns.

MODEL. Chores, cost form. Each agent i has c_i : 2^M -> Z_{>=0} with
c_i(empty) = 0 and every marginal c_i(S + e) - c_i(S) in {0,1}. Costs are
represented as a tuple indexed by subset bitmask. Nothing is assumed beyond
binary marginals: not additivity, not submodularity, and no relation between
different agents' cost functions.

PARETO OPTIMALITY. For chores, allocation B Pareto dominates A when
c_i(B_i) <= c_i(A_i) for every agent i, with strict inequality for at least
one. A is Pareto optimal (PO) when no complete allocation dominates it. Note
this is a property of the ALLOCATION alone and ignores subsidies -- it is the
notion Tao et al. use when they prove EFX + PO for binary ADDITIVE chores, and
so the natural reading of the question "is our allocation PO?".
"""
import itertools


# --------------------------------------------------------------------------
# Instances
# --------------------------------------------------------------------------

def masks_by_popcount(m):
    return sorted(range(1 << m), key=lambda s: (bin(s).count("1"), s))


def random_cost(m, rng, weights=None):
    """
    A random monotone cost with c(empty)=0 and every marginal in {0,1}, built
    by walking the subset lattice: for each S the value must be within {0,1} of
    every single-bit deletion at once, so it lies in
    [max_b c(S-b), min_b c(S-b) + 1], an interval that is never empty.
    `weights` biases the choice of marginal 0 versus 1.
    """
    vals = [0] * (1 << m)
    for S in masks_by_popcount(m):
        if S == 0:
            continue
        bits = [1 << b for b in range(m) if S & (1 << b)]
        lo = max(vals[S ^ b] for b in bits)
        hi = min(vals[S ^ b] for b in bits) + 1
        if lo == hi:
            vals[S] = lo
        elif weights is None:
            vals[S] = rng.randint(lo, hi)
        else:
            vals[S] = rng.choices([lo, hi], weights=weights)[0]
    return tuple(vals)


def additive_cost(m, per_item):
    """c(S) = sum of per_item over S; per_item entries must be 0 or 1."""
    return tuple(sum(per_item[k] for k in range(m) if S & (1 << k))
                 for S in range(1 << m))


def is_valid_cost(c, m):
    if c[0] != 0:
        return False
    for S in range(1 << m):
        for k in range(m):
            bit = 1 << k
            if not S & bit and c[S | bit] - c[S] not in (0, 1):
                return False
    return True


# --------------------------------------------------------------------------
# Envy graph, envy-freeness, subsidies  (all in COST form)
# --------------------------------------------------------------------------

def is_ef(cs, X, n):
    """Envy-free with zero subsidy: c_i(X_i) <= c_i(X_j) for all i,j."""
    return all(cs[i][X[i]] <= cs[i][X[j]]
               for i in range(n) for j in range(n))


def equality_graph(cs, X, n):
    return {(i, j) for i in range(n) for j in range(n)
            if i != j and cs[i][X[i]] == cs[i][X[j]]}


def min_subsidy(cs, A, n):
    """
    Componentwise-minimal subsidy of an allocation, or None if it is not
    envy-freeable. Cost-form arc weight w(i,j) = c_i(A_i) - c_i(A_j);
    envy-freeable iff no positive-weight cycle; p*_i is the heaviest simple
    path out of i, the empty path included.
    """
    def w(i, j):
        return cs[i][A[i]] - cs[i][A[j]]

    # no positive cycle, over all simple cycles
    for r in range(2, n + 1):
        for cyc in itertools.permutations(range(n), r):
            if cyc[0] != min(cyc):
                continue
            tot = sum(w(cyc[t], cyc[(t + 1) % r]) for t in range(r))
            if tot > 0:
                return None

    out = []
    for i in range(n):
        others = [j for j in range(n) if j != i]
        best = 0
        for r in range(1, n):
            for path in itertools.permutations(others, r):
                tot, cur = 0, i
                for nxt in path:
                    tot += w(cur, nxt)
                    cur = nxt
                if tot > best:
                    best = tot
        out.append(best)
    return out


# --------------------------------------------------------------------------
# Tao-Wu-Yu-Zhou Algorithm 3
# --------------------------------------------------------------------------

def sccs_and_tail(edges, n):
    """Strongly connected components, and one with no equality arc leaving."""
    reach = {i: {i} for i in range(n)}
    changed = True
    while changed:
        changed = False
        for (i, j) in edges:
            if not reach[i] >= reach[j]:
                reach[i] |= reach[j]
                changed = True
    comps, seen = [], set()
    for i in range(n):
        if i in seen:
            continue
        comp = frozenset(k for k in range(n)
                         if k in reach[i] and i in reach[k])
        comps.append(comp)
        seen |= comp
    for comp in comps:
        if not any(i in comp and j not in comp for (i, j) in edges):
            return comps, comp
    return comps, comps[0]


def find_cycle_through(edges, i, j, n):
    """A simple path j -> ... -> i, which with the arc (i,j) closes a cycle."""
    if (i, j) not in edges:
        return None
    stack = [(j, [j])]
    while stack:
        cur, path = stack.pop()
        if cur == i:
            return path
        for k in range(n):
            if (cur, k) in edges and k not in path:
                stack.append((k, path + [k]))
    return None


def twyz(cs, n, m, cap=400, order=None):
    """
    Algorithm 3 of Tao et al. as restated in main_result.tex:
      (R1) a residual chore free for some agent goes to that agent;
      (R2) a residual chore free for i on X_j, for an equality arc (i,j) lying
           on a cycle, rotates the bundles along that cycle and assigns it to i;
      (R3) otherwise take a tail SCC S; if |R| >= |S| give one chore to each
           member of S, else halt.
    `order` permutes the chore scan order, which is one of the algorithm's
    free choices. Returns (X, R, S) with S the tail component at the halting
    (R3), or None if the run finished with R empty.
    """
    X = [0] * n
    R = set(range(m))
    scan = list(order) if order is not None else list(range(m))

    for _ in range(cap):
        if not R:
            return tuple(X), R, None

        done = False
        for e in [x for x in scan if x in R]:                       # (R1)
            for i in range(n):
                if cs[i][X[i] | (1 << e)] - cs[i][X[i]] == 0:
                    X[i] |= 1 << e
                    R.discard(e)
                    done = True
                    break
            if done:
                break
        if done:
            continue

        edges = equality_graph(cs, X, n)

        for e in [x for x in scan if x in R]:                       # (R2)
            for (i, j) in sorted(edges):
                if cs[i][X[j] | (1 << e)] - cs[i][X[j]] != 0:
                    continue
                cyc = find_cycle_through(edges, i, j, n)
                if cyc is None:
                    continue
                old = list(X)
                for t, a in enumerate(cyc):
                    X[a] = old[cyc[(t + 1) % len(cyc)]]
                X[i] |= 1 << e
                R.discard(e)
                done = True
                break
            if done:
                break
        if done:
            continue

        _, tail = sccs_and_tail(edges, n)                            # (R3)
        if len(R) >= len(tail):
            for a in sorted(tail):
                e = min(R)
                X[a] |= 1 << e
                R.discard(e)
            continue
        return tuple(X), R, tail

    return tuple(X), R, "CAP"


# --------------------------------------------------------------------------
# Algorithm 1: the completion and the subsidy set
# --------------------------------------------------------------------------

def algorithm1(cs, n, m, order=None, recipients=None):
    """
    Returns (A, p, info). `recipients` optionally fixes which r agents of the
    tail component S receive the residual chores -- the algorithm says "choose
    arbitrary distinct agents T subseteq S", so this is a genuine free choice
    and worth being able to vary.
    """
    X, R, S = twyz(cs, n, m, order=order)
    if S == "CAP":
        return None, None, {"status": "cap"}
    if not R:
        return X, [0] * n, {"status": "r0", "X": X, "R": (), "S": None}

    Rl = sorted(R)
    r = len(Rl)
    Sl = sorted(S)
    T = list(recipients) if recipients is not None else Sl[:r]
    assert len(set(T)) == r and set(T) <= set(Sl)

    A = list(X)
    for k, t in enumerate(T):
        A[t] = X[t] | (1 << Rl[k])
    A = tuple(A)

    E = equality_graph(cs, X, n)
    P = set(T)
    changed = True
    while changed:
        changed = False
        for i in range(n):
            if i in P or i in S:
                continue
            if any((i, j) in E for j in P):
                P.add(i)
                changed = True
    p = [1 if i in P else 0 for i in range(n)]
    return A, p, {"status": "r%d" % r, "X": X, "R": tuple(Rl),
                  "S": Sl, "T": T, "P": sorted(P)}


# --------------------------------------------------------------------------
# Pareto optimality
# --------------------------------------------------------------------------

def all_allocations(n, m):
    for assign in itertools.product(range(n), repeat=m):
        b = [0] * n
        for k, owner in enumerate(assign):
            b[owner] |= 1 << k
        yield tuple(b)


def dominates(cs, B, A, n):
    """B Pareto dominates A (chores: lower cost is better)."""
    if any(cs[i][B[i]] > cs[i][A[i]] for i in range(n)):
        return False
    return any(cs[i][B[i]] < cs[i][A[i]] for i in range(n))


def pareto_dominator(cs, A, n, m):
    """A dominating allocation if one exists, else None."""
    for B in all_allocations(n, m):
        if dominates(cs, B, A, n):
            return B
    return None


def is_po(cs, A, n, m):
    return pareto_dominator(cs, A, n, m) is None


def cost_profile(cs, A, n):
    return tuple(cs[i][A[i]] for i in range(n))
