"""
Approach 21: an equality-graph method for signed dichotomous valuations.

Question (Mainak, 2026-10-03). Can the objective signed dichotomous case be
solved the way the chores case was, by maintaining an envy-free partial
allocation X together with its equality graph, sending chores to TAIL strongly
connected components (Tao-Wu-Yu-Zhou) and goods to SOURCE strongly connected
components, and completing the leftovers in one shot with unit subsidies?

MODEL. n agents, m items. Each agent i has v_i : 2^M -> Z with v_i(empty)=0.
Every item e has a sign for agent i: a GOOD for i (every marginal of e for i
lies in {0,1}) or a CHORE for i (every marginal lies in {-1,0}). OBJECTIVE
instances give every item the same sign for all agents; DOUBLY MONOTONE
instances let the sign depend on the agent. Valuations are generated as
v_i(S) = u_i(S) - |S n C_i| with u_i any monotone function with binary
marginals (C_i = the chores of agent i); every signed dichotomous valuation
arises this way, since u_i := v_i + |S n C_i| has binary marginals.

THE RULES (value form; E = equality arcs k -> j iff v_k(X_k) = v_k(X_j)).
They all keep X envy-free; apply_move re-checks that after every move.

  F    free insertion   item e to agent i when v_i(e|X_i) >= 0 and every k
                        with k -> i has v_k(e|X_i) <= 0.          [Tao R1, BKNS-free]
  ROT  free after       some k -> j on a cycle of E: rotate the bundles
       rotation         along the cycle so k holds X_j, then add e, when
                        v_k(e|X_j) >= 0 and every OTHER agent tied to X_j
                        after the rotation (old in-neighbours of j, and j
                        itself) has marginal <= 0 for e on X_j.   [Tao R2]
  TAIL chores to a      a tail SCC S (no arc leaves it): if at least |S|
       tail SCC         leftover chores-for-everyone remain, one to each
                        member.                                    [Tao R3]
  SRC  goods to a       a source SCC S (no arc enters it): if the leftover
       source SCC       items admit an assignment giving each member of S a
                        distinct item worth exactly +1 to it on its own
                        bundle, hand them out.                     [the mirror]

F and ROT are sign-agnostic; only the two batch rules care about signs.

COMPLETIONS of a halting state, tested against the Halpern-Shah optimum:
  K-SYM   leftover chores to distinct members of the halting tail SCC, and
          leftover goods to distinct agents each valuing its good at +1
          (preferring agents outside that SCC); payments = Halpern-Shah.
  BF      brute force: some assignment of the leftovers (optionally with a
          reassignment of the bundles) has maximum minimal subsidy <= 1.
"""
import itertools
import random


# --------------------------------------------------------------------------
# Valuations
# --------------------------------------------------------------------------

def masks_by_popcount(m):
    return sorted(range(1 << m), key=lambda s: (bin(s).count("1"), s))


def random_binary_monotone(m, rng, p_one=0.5):
    """A monotone u with u(empty)=0 and binary marginals (lattice walk)."""
    u = [0] * (1 << m)
    for S in masks_by_popcount(m):
        if S == 0:
            continue
        bits = [1 << b for b in range(m) if S >> b & 1]
        lo = max(u[S ^ b] for b in bits)
        hi = min(u[S ^ b] for b in bits) + 1
        u[S] = lo if lo == hi else (hi if rng.random() < p_one else lo)
    return u


def additive_binary(m, rng, p_one=0.5):
    w = [1 if rng.random() < p_one else 0 for _ in range(m)]
    return [sum(w[b] for b in range(m) if S >> b & 1) for S in range(1 << m)]


def signed_from_u(u, m, chore_mask):
    return tuple(u[S] - bin(S & chore_mask).count("1") for S in range(1 << m))


def random_instance(n, m, rng, mode="objective", family="random",
                    p_chore=0.5, p_one=0.5):
    """
    Returns (v, cmask): v[i] a tuple indexed by mask, cmask[i] the mask of
    agent i's chores. mode 'objective' shares one chore mask; 'doubly' draws
    one per agent.
    """
    if mode == "objective":
        cm = sum(1 << b for b in range(m) if rng.random() < p_chore)
        cmask = [cm] * n
    else:
        cmask = [sum(1 << b for b in range(m) if rng.random() < p_chore)
                 for _ in range(n)]
    gen = random_binary_monotone if family == "random" else additive_binary
    v = [signed_from_u(gen(m, rng, p_one), m, cmask[i]) for i in range(n)]
    for i in range(n):
        assert is_signed_dichotomous(v[i], m, cmask[i])
    return v, cmask


def is_signed_dichotomous(vi, m, chore_mask):
    if vi[0] != 0:
        return False
    for S in range(1 << m):
        for b in range(m):
            if S >> b & 1:
                continue
            d = vi[S | 1 << b] - vi[S]
            ok = (-1, 0) if chore_mask >> b & 1 else (0, 1)
            if d not in ok:
                return False
    return True


# --------------------------------------------------------------------------
# Envy-freeness, equality graph, SCCs
# --------------------------------------------------------------------------

def marg(v, i, e, S):
    return v[i][S | 1 << e] - v[i][S]


def is_ef(v, X, n):
    return all(v[i][X[i]] >= v[i][X[j]] for i in range(n) for j in range(n))


def eq_graph(v, X, n):
    return frozenset((i, j) for i in range(n) for j in range(n)
                     if i != j and v[i][X[i]] == v[i][X[j]])


def reach_sets(E, n):
    reach = [{i} for i in range(n)]
    changed = True
    while changed:
        changed = False
        for (i, j) in E:
            if not reach[i] >= reach[j]:
                reach[i] |= reach[j]
                changed = True
    return reach


def sccs(E, n):
    reach = reach_sets(E, n)
    comps, seen = [], set()
    for i in range(n):
        if i in seen:
            continue
        c = frozenset(k for k in range(n) if k in reach[i] and i in reach[k])
        comps.append(c)
        seen |= c
    return comps


def tail_sccs(E, comps):
    return [c for c in comps if not any(i in c and j not in c for (i, j) in E)]


def source_sccs(E, comps):
    return [c for c in comps if not any(j in c and i not in c for (i, j) in E)]


def path(E, a, b, n):
    """A simple path a -> ... -> b in E (list of agents), or None."""
    stack = [(a, [a])]
    while stack:
        cur, p = stack.pop()
        if cur == b:
            return p
        for k in range(n):
            if (cur, k) in E and k not in p:
                stack.append((k, p + [k]))
    return None


def rotate(X, k, j, cyc):
    """cyc = [j, ..., k] closes with the arc k -> j; everyone on the cycle
    takes the bundle of its successor, so k ends up holding X_j."""
    Y = list(X)
    L = len(cyc)
    for t, a in enumerate(cyc):
        Y[a] = X[cyc[(t + 1) % L]]
    return Y


# --------------------------------------------------------------------------
# The four rules
# --------------------------------------------------------------------------

def in_nbrs(E, j):
    return [k for (k, jj) in E if jj == j]


def moves_F(v, X, R, E, n):
    for e in sorted(R):
        for i in range(n):
            if marg(v, i, e, X[i]) >= 0 and all(
                    marg(v, k, e, X[i]) <= 0 for k in in_nbrs(E, i)):
                yield ("F", e, i)


def moves_ROT(v, X, R, E, n):
    for e in sorted(R):
        for j in range(n):
            tied = set(in_nbrs(E, j)) | {j}
            for k in in_nbrs(E, j):
                if marg(v, k, e, X[j]) < 0:
                    continue
                if any(marg(v, l, e, X[j]) > 0 for l in tied - {k}):
                    continue
                cyc = path(E, j, k, n)          # j -> ... -> k, closed by k -> j
                if cyc is not None:
                    yield ("ROT", e, k, j, tuple(cyc))


def pure_chores(R, cmask, n):
    return sorted(e for e in R if all(cmask[i] >> e & 1 for i in range(n)))


def moves_TAIL(v, X, R, E, n, cmask, comps):
    chores = pure_chores(R, cmask, n)
    tails = sorted(tail_sccs(E, comps), key=lambda c: (len(c), min(c)))
    for S in tails:
        if len(chores) >= len(S):
            gave = tuple(zip(chores, sorted(S)))
            yield ("TAIL", tuple(sorted(S)), gave)
            return


def sdr(members, items, ok, rng=None):
    """Matching saturating `members`; ok(s, e) says s may take e."""
    match = {}                                   # item -> member

    def aug(s, seen):
        cand = list(items)
        if rng is not None:
            rng.shuffle(cand)
        for e in cand:
            if e in seen or not ok(s, e):
                continue
            seen.add(e)
            if e not in match or aug(match[e], seen):
                match[e] = s
                return True
        return False

    for s in members:
        if not aug(s, set()):
            return None
    return {s: e for e, s in match.items()}


def moves_SRC(v, X, R, E, n, comps, rng=None):
    sources = sorted(source_sccs(E, comps), key=lambda c: (len(c), min(c)))
    items = sorted(R)
    for S in sources:
        m = sdr(sorted(S), items, lambda s, e: marg(v, s, e, X[s]) == 1, rng)
        if m is not None:
            yield ("SRC", tuple(sorted(S)), tuple(sorted((e, s) for s, e in m.items())))
            return


def apply_move(v, X, R, mv, n):
    X, R = list(X), set(R)
    kind = mv[0]
    if kind == "F":
        _, e, i = mv
        X[i] |= 1 << e
        R.discard(e)
    elif kind == "ROT":
        _, e, k, j, cyc = mv
        X = rotate(X, k, j, list(cyc))
        X[k] |= 1 << e
        R.discard(e)
    else:                                         # TAIL / SRC
        for e, s in mv[2]:
            X[s] |= 1 << e
            R.discard(e)
    assert is_ef(v, X, n), ("move broke envy-freeness", mv)
    return X, R


ORDERS = {
    "F-ROT-TAIL-SRC": ("F", "ROT", "TAIL", "SRC"),
    "F-ROT-SRC-TAIL": ("F", "ROT", "SRC", "TAIL"),
}


def ef_phase(v, n, m, cmask, order=("F", "ROT", "TAIL", "SRC"),
             rng=None, cap=500):
    """
    Run the rules to a halt. With rng, a uniformly random applicable move of
    the highest-priority applicable rule is taken; without, the first one.
    Returns (X, R, trace).
    """
    X, R = [0] * n, set(range(m))
    trace = []
    for _ in range(cap):
        if not R:
            break
        E = eq_graph(v, X, n)
        comps = sccs(E, n)
        mv = None
        for rule in order:
            if rule == "F":
                cand = list(moves_F(v, X, R, E, n))
            elif rule == "ROT":
                cand = list(moves_ROT(v, X, R, E, n))
            elif rule == "TAIL":
                cand = list(moves_TAIL(v, X, R, E, n, cmask, comps))
            else:
                cand = list(moves_SRC(v, X, R, E, n, comps, rng))
            if cand:
                mv = rng.choice(cand) if rng is not None else cand[0]
                break
        if mv is None:
            break
        X, R = apply_move(v, X, R, mv, n)
        trace.append(mv)
    return X, R, trace


# --------------------------------------------------------------------------
# Halpern-Shah: envy-freeability and the largest minimal subsidy
# --------------------------------------------------------------------------

def max_min_subsidy(v, A, n):
    """
    For a complete allocation A (agent i holds A[i]): None if not
    envy-freeable, else max_i p*_i (longest path out of i, Floyd-Warshall).
    """
    NEG = -10 ** 9
    d = [[(v[i][A[j]] - v[i][A[i]]) if i != j else 0 for j in range(n)]
         for i in range(n)]
    for k in range(n):
        dk = d[k]
        for i in range(n):
            dik = d[i][k]
            if dik == NEG:
                continue
            di = d[i]
            for j in range(n):
                if dik + dk[j] > di[j]:
                    di[j] = dik + dk[j]
    if any(d[i][i] > 0 for i in range(n)):
        return None
    return max(max(row) for row in d)


def best_matching_alloc(v, bundles, n):
    """Agents to bundles maximising welfare (envy-freeable by Halpern-Shah)."""
    best, arg = None, None
    for perm in itertools.permutations(range(n)):
        w = sum(v[i][bundles[perm[i]]] for i in range(n))
        if best is None or w > best:
            best, arg = w, perm
    return [bundles[arg[i]] for i in range(n)]


def exists_unit_completion(v, X, R, n, permute):
    """Some placement of the leftovers R into the bundles of X (and, if
    permute, some reassignment of the bundles) with max minimal subsidy <= 1."""
    items = sorted(R)
    for owners in itertools.product(range(n), repeat=len(items)):
        B = list(X)
        for e, o in zip(items, owners):
            B[o] |= 1 << e
        A = best_matching_alloc(v, B, n) if permute else B
        s = max_min_subsidy(v, A, n)
        if s is not None and s <= 1:
            return True
    return False


# --------------------------------------------------------------------------
# Halting-state analysis and the symmetric completion
# --------------------------------------------------------------------------

def halting_report(v, X, R, n, cmask):
    E = eq_graph(v, X, n)
    comps = sccs(E, n)
    tails = sorted(tail_sccs(E, comps), key=lambda c: (len(c), min(c)))
    srcs = sorted(source_sccs(E, comps), key=lambda c: (len(c), min(c)))
    chores = pure_chores(R, cmask, n)
    goods = sorted(set(R) - set(chores))
    return dict(E=E, comps=comps, tails=tails, sources=srcs,
                chores=chores, goods=goods)


def symmetric_completion(v, X, R, n, cmask):
    """
    K-SYM. Chores to distinct members of the smallest tail SCC; goods to
    distinct agents valuing each at +1 on the bundle it lands in, agents
    outside that SCC first. Returns (status, A) with status in
    {'ok', 'fail', 'unmatchable', 'chores-overflow'}.
    """
    h = halting_report(v, X, R, n, cmask)
    chores, goods = h["chores"], h["goods"]
    A = list(X)
    SC = sorted(h["tails"][0]) if h["tails"] else []
    if chores:
        if len(chores) >= len(SC):
            return "chores-overflow", None
        for c, t in zip(chores, SC):
            A[t] |= 1 << c
    if goods:
        outside = [i for i in range(n) if i not in SC]
        m = None
        for pool in (outside, list(range(n))):
            m = sdr(goods, pool, lambda g, t: marg(v, t, g, A[t]) == 1)
            if m is not None:
                break
        if m is None:
            return "unmatchable", None
        for g, t in m.items():
            A[t] |= 1 << g
    s = max_min_subsidy(v, A, n)
    return ("ok" if s is not None and s <= 1 else "fail"), A
