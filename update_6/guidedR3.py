"""Guided-R3: a constructive attempt at Target G.

IDEA.  R3's own correctness proofs (Lemmas 3, 7, 8, 9, 10, 11 of Reading_3) are
generic over WHICH valid choice EXTEND / FINDSINK make at each insertion step:
  - EXTEND may return ANY (rho, k) satisfying its welfare test, not just the
    first one found;
  - FINDSINK may start from ANY s0 in M(p), not just an arbitrary fixed one.
So exploring / choosing among R3-legal options preserves p in {0,1}^n "for
free" -- that part needs no new proof, it IS R3's theorem.  What is new is
whether SOME legal choice also controls bundle size, i.e. hits Target G's
q_i = p_i + |A_i| spread <= 1.

This module implements ALG/EXTEND/FINDSINK faithfully (re-derived from the
paper text, not copied), on the SIZE-SHIFTED GOODS instance vtilde_i(S) =
|S| - c_i(S), and a GREEDY driver that at each step picks the legal choice
minimizing the resulting q-spread.

Run:  python guidedR3.py
"""
from itertools import combinations, permutations


# --------------------------------------------------------------- primitives
def size_shift(c, m):
    """c: dict frozenset(subset of range(m)) -> int.  Returns vtilde dict."""
    return {S: len(S) - c[S] for S in c}


def longest_path(W, n):
    e = [0] * n
    for _ in range(n + 1):
        ch = False
        new = list(e)
        for i in range(n):
            for j in range(n):
                if i != j and W[i][j] + e[j] > new[i]:
                    new[i] = W[i][j] + e[j]
                    ch = True
        e = new
        if not ch:
            return e
    return None


def compute_p(v, A, n):
    W = [[v[i][A[j]] - v[i][A[i]] for j in range(n)] for i in range(n)]
    return longest_path(W, n)


def M_of_p(p, n):
    mx = max(p)
    return [i for i in range(n) if p[i] == mx]


def marginal(v, i, S, g):
    return v[i][S | {g}] - v[i][S]


# --------------------------------------------------- EXTEND, faithful to R3
def extend_options(v, A, p, g, n):
    """All (rho, k) pairs satisfying R3 Algorithm 2's validity test.
    rho: dict i -> j meaning "agent i receives bundle A_j"."""
    opts = []
    Mp = M_of_p(p, n)
    base_val = sum(v[i][A[i]] for i in range(n))
    for k in range(n):
        for l in Mp:
            if marginal(v, k, A[l], g) != 1:
                continue
            others_from = [i for i in range(n) if i != k]
            others_to = [j for j in range(n) if j != l]
            best_map, best_val = None, None
            for perm in permutations(others_to):
                mapping = dict(zip(others_from, perm))
                val = sum(v[i][A[mapping[i]]] for i in others_from)
                if best_val is None or val > best_val:
                    best_val, best_map = val, mapping
            rho = dict(best_map)
            rho[k] = l
            new_val = sum(v[i][A[rho[i]]] for i in range(n))
            if new_val >= base_val:
                opts.append((rho, k))
    return opts


def apply_extend(A, rho, k, g, n):
    B = [A[rho[i]] for i in range(n)]
    B[k] = B[k] | {g}
    return B


# -------------------------------------------------- FINDSINK, faithful to R3
def findsink_run(v, A, p, g, n, s0):
    s = s0
    X = list(A)
    X[s] = X[s] | {g}
    phi = compute_p(v, X, n)
    guard = 0
    while max(phi) >= 2:
        j = next(jj for jj in range(n) if phi[jj] >= 2)
        s = j
        X = list(A)
        X[s] = X[s] | {g}
        phi = compute_p(v, X, n)
        guard += 1
        if guard > n + 2:
            raise RuntimeError("FINDSINK did not terminate -- bug")
    return s


def apply_findsink(A, s, g):
    B = list(A)
    B[s] = B[s] | {g}
    return B


# ------------------------------------------------------------------ drivers
def q_spread(v, A, n):
    p = compute_p(v, A, n)
    q = [p[i] + len(A[i]) for i in range(n)]
    return max(q) - min(q), p, q


def greedy_run(v, items, n):
    """One pass, processing `items` in the given order, always taking the
    legal choice that minimises the resulting q-spread."""
    A = [frozenset() for _ in range(n)]
    p = [0] * n
    for g in items:
        opts = extend_options(v, A, p, g, n)
        candidates = []
        if opts:
            for (rho, k) in opts:
                B = apply_extend(A, rho, k, g, n)
                sp, _, _ = q_spread(v, B, n)
                candidates.append((sp, B))
        else:
            for s0 in M_of_p(p, n):
                s = findsink_run(v, A, p, g, n, s0)
                B = apply_findsink(A, s, g)
                sp, _, _ = q_spread(v, B, n)
                candidates.append((sp, B))
        candidates.sort(key=lambda x: x[0])
        A = candidates[0][1]
        p = compute_p(v, A, n)
        if p is None or max(p) > 1:
            raise RuntimeError("R3 invariant broken -- reimplementation bug")
    return A, p


def best_over_orders(v, items, n, max_orders=None):
    """Try (a sample of) item orders and report the best final q-spread."""
    from itertools import permutations as perms
    import random
    orders = list(perms(items))
    if max_orders is not None and len(orders) > max_orders:
        rng = random.Random(0)
        orders = rng.sample(orders, max_orders)
    best = None
    for order in orders:
        A, p = greedy_run(v, order, n)
        sp, _, q = q_spread(v, A, n)
        if best is None or sp < best[0]:
            best = (sp, order, A, p, q)
        if sp <= 1:
            break
    return best


# --------------------------------------------------------------- self-test
def _selftest():
    """Sanity check: on a hand-built instance, does our EXTEND/FINDSINK
    reimplementation reproduce a known-good p in {0,1}?"""
    n, m = 3, 3
    subs = [frozenset(s) for k in range(m + 1) for s in combinations(range(m), k)]
    v = [{S: len(S) for S in subs} for _ in range(n)]   # additive unit-value goods
    A, p = greedy_run(v, list(range(m)), n)
    print("selftest: additive unit-value goods, n=3,m=3 -> p =", p,
          " (expect all entries in {0,1})")
    assert all(x in (0, 1) for x in p)
    print("selftest passed.")


if __name__ == "__main__":
    _selftest()
