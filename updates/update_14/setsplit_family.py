"""R10's Set-Splitting reduction as a FAMILY, and the form of its chain witnesses.

THE REDUCTION (Bhaskar-Sricharan-Vaish, Theorem 2).  From a hypergraph
(U, F) with q = |U|, r = |F|, r' = max(q, r):
    chores  : r' dummies  +  q vertex chores          (m = r' + q)
    agents  : r' edge agents  +  2 colour agents      (n = r' + 2)
    costs   : binary additive; every dummy costs 1 to everyone;
              vertex chore V_j costs 1 to edge agent e_i iff v_j in E_i,
              and 0 to both colour agents.
An exactly envy-free allocation exists iff (U,F) is a YES instance of Set
Splitting, i.e. iff U admits a 2-colouring with no monochromatic edge.  So NO
instances give EF-free instances BY CONSTRUCTION -- the only certified source of
the residual class.

QUESTION.  On this family, do the chain witnesses have a form describable in
terms of the hypergraph?  A construction here would cover an infinite certified
-hard family rather than one instance.

CANDIDATE FORM (from the witness recorded in update_3): every edge agent takes
one dummy plus the vertex chores it does NOT contain; the two colour agents take
nothing; p = (1,...,1,0,0).

Run:  python setsplit_family.py
"""
from itertools import combinations, product


def build(U, F):
    """Return (n, m, cost dicts, description) for the reduction of (U,F)."""
    q, r = len(U), len(F)
    rp = max(q, r)
    m = rp + q
    n = rp + 2
    dummies = list(range(rp))               # chores 0 .. rp-1
    verts = list(range(rp, rp + q))         # chores rp .. rp+q-1
    vidx = {v: rp + i for i, v in enumerate(U)}

    D = []
    for i in range(rp):                     # edge agents
        S = set(dummies)
        if i < r:
            S |= {vidx[v] for v in F[i]}
        else:
            # R10, proof of Theorem 2: the padding agents e_{r+1..r'} are
            # "imaginary hyperedges adjacent to the ENTIRE set of vertices",
            # so they cost 1 on every vertex chore -- not zero.
            S |= set(verts)
        D.append(frozenset(S))
    for _ in range(2):                      # colour agents
        D.append(frozenset(dummies))
    return n, m, D, dummies, verts, vidx


def costs_from_D(m, n, D):
    subs = [frozenset(s) for k in range(m + 1) for s in combinations(range(m), k)]
    return [{S: len(S & D[i]) for S in subs} for i in range(n)]


def ell_ok(a, n, k):
    W = [[min(a[i][i], k) - min(a[i][j], k) for j in range(n)] for i in range(n)]
    e = [0] * n
    for _ in range(n + 1):
        ch = False
        new = list(e)
        for i in range(n):
            for j in range(n):
                if i != j and W[i][j] + e[j] > new[i]:
                    new[i] = W[i][j] + e[j]; ch = True
        e = new
        if not ch:
            return max(e) <= 1, e
    return False, None


def splittable(U, F):
    """Is there a 2-colouring of U with no monochromatic edge?"""
    for bits in product([0, 1], repeat=len(U)):
        col = dict(zip(U, bits))
        if all(len({col[v] for v in E}) == 2 for E in F):
            return True
    return False


def analyse(U, F, verbose=True):
    n, m, D, dummies, verts, vidx = build(U, F)
    cs = costs_from_D(m, n, D)
    K = max(max(c.values()) for c in cs)

    has_ef = False
    chain = []
    top = []
    for assign in product(range(n), repeat=m):
        bd = [frozenset(g for g in range(m) if assign[g] == i) for i in range(n)]
        a = [[cs[i][bd[j]] for j in range(n)] for i in range(n)]
        if all(a[i][i] <= a[i][j] for i in range(n) for j in range(n)):
            has_ef = True
        okK, eK = ell_ok(a, n, K)
        if okK:
            top.append((bd, eK))
            if all(ell_ok(a, n, k)[0] for k in range(1, K + 1)):
                chain.append((bd, eK))

    sp = splittable(U, F)
    if verbose:
        print("  U=%-14s |F|=%d  ->  n=%d m=%d K=%d | splittable=%-5s "
              "exactlyEF=%-5s | chain=%-6d top=%-6d"
              % (str(U), len(F), n, m, K, sp, has_ef, len(chain), len(top)))
        assert sp == has_ef, "reduction correctness violated!"
    return n, m, D, dummies, verts, vidx, cs, chain, top, sp, has_ef


def r10_witness(U, F, colouring=None):
    """R10's own EF construction, which only exists on YES instances: one dummy
    to each edge agent, and vertex chore V_j to the colour agent matching v_j's
    colour.  On NO instances there is no valid colouring, so this returns None
    and the question becomes what a CHAIN witness looks like instead."""
    n, m, D, dummies, verts, vidx = build(U, F)
    q, r = len(U), len(F)
    rp = max(q, r)
    if colouring is None:
        for bits in product([0, 1], repeat=len(U)):
            col = dict(zip(U, bits))
            if all(len({col[v] for v in E}) == 2 for E in F):
                colouring = col
                break
        else:
            return None
    bundles = [set() for _ in range(n)]
    for i in range(rp):
        bundles[i].add(dummies[i])
    for v in U:
        bundles[rp + colouring[v]].add(vidx[v])
    return [frozenset(b) for b in bundles]


def main():
    print("=== the reduction is correct: exactly-EF exists iff splittable ===")
    cases = [
        (["a"], [["a"]]),                                   # NO  (size-1 edge)
        (["a", "b"], [["a"], ["b"]]),                        # NO
        (["a", "b"], [["a"], ["a", "b"]]),                   # NO
        (["a", "b"], [["a", "b"]]),                          # YES
        (["a", "b", "c"], [["a"], ["b", "c"]]),              # NO
        (["a", "b", "c"], [["a", "b"], ["a", "c"], ["b", "c"]]),   # NO triangle
        (["a", "b", "c"], [["a", "b"], ["b", "c"]]),         # YES path
    ]
    hard = []
    for U, F in cases:
        res = analyse(U, F)
        if not res[10]:                      # has_ef False -> EF-free
            hard.append((U, F, res))

    print("\n=== structure of chain witnesses on the EF-free (NO) instances ===")
    for U, F, res in hard:
        n, m, D, dummies, verts, vidx, cs, chain, top, sp, has_ef = res
        sizes = {}
        subs = {}
        for bd, e in chain:
            sizes[tuple(sorted(len(b) for b in bd))] = \
                sizes.get(tuple(sorted(len(b) for b in bd)), 0) + 1
            subs[tuple(e)] = subs.get(tuple(e), 0) + 1
        print("  U=%-14s |F|=%d : %d chain witnesses" % (str(U), len(F), len(chain)))
        print("      subsidy vectors (top 3): %s"
              % sorted(subs.items(), key=lambda kv: -kv[1])[:3])
        print("      total subsidy always = %s"
              % sorted({sum(k) for k in subs}))
        cand = r10_witness(U, F)
        if cand is None:
            print("      candidate form: not constructible")
        else:
            keys = {tuple(tuple(sorted(b)) for b in bd) for bd, _ in chain}
            ck = tuple(tuple(sorted(b)) for b in cand)
            print("      candidate form %s a chain witness  (bundles %s)"
                  % ("IS" if ck in keys else "is NOT",
                     [sorted(b) for b in cand]))


if __name__ == "__main__":
    main()
