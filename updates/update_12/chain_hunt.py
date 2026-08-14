"""Is the CHAIN CONJECTURE true at the sizes where things actually break?

Every previous chain test stopped at m = 6.  The counterexample that refuted
claims (I) and (II) lives at m = 8.  So the chain conjecture has never been
tested past the frontier where the level structure is known to misbehave.

SPEED.  Goodness at every level depends only on the cost matrix
a_ij = c_i(A_j), so per partition we compute a once (n^2 oracle calls) and then
decide all K levels from a alone.  No cost function is ever re-evaluated per
level.

ADVERSARY.  Besides endpoint-constant sampling, the generator includes the
matrix-realising family
        c_i(S) = sum_j min(|S ∩ B_j|, a_ij)
over random reference partitions B and random matrices a.  That family is
exactly what produced the (I)/(II) counterexample, so it is the sharpest
adversary currently known for level-structure questions.

Run:  python chain_hunt.py
"""
from itertools import combinations, product
import random
import sys


def ell_ok(a, n, k):
    """Is the level-k graph of cost matrix a good?"""
    W = [[min(a[i][i], k) - min(a[i][j], k) for j in range(n)] for i in range(n)]
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
            return max(e) <= 1
    return False                        # positive cycle


def chain_good(a, n, K):
    return all(ell_ok(a, n, k) for k in range(1, K + 1))


def top_good(a, n, K):
    return ell_ok(a, n, K)


def scan(cs, m, n):
    """Return (chain witness exists, top-good witness exists)."""
    K = max(max(c.values()) for c in cs)
    if K < 2:
        return None
    ch = tp = False
    for assign in product(range(n), repeat=m):
        bd = [frozenset(g for g in range(m) if assign[g] == i) for i in range(n)]
        a = [[cs[i][bd[j]] for j in range(n)] for i in range(n)]
        if not tp and top_good(a, n, K):
            tp = True
        if not ch and chain_good(a, n, K):
            ch = True
        if ch and tp:
            break
    return ch, tp


# ------------------------------------------------------------- generators
def subsets(m):
    return [frozenset(s) for k in range(m + 1) for s in combinations(range(m), k)]


def rand_dicho(m, rng, hi_prob=None):
    subs = sorted(subsets(m), key=lambda s: (len(s), sorted(s)))
    val = {frozenset(): 0}
    for S in subs:
        if not S:
            continue
        lo, hi = 0, 10 ** 9
        for g in S:
            T = S - {g}
            lo = max(lo, val[T])
            hi = min(hi, val[T] + 1)
        pr = rng.random() if hi_prob is None else hi_prob
        val[S] = hi if (lo != hi and rng.random() < pr) else lo
    return val


def matrix_realising(m, n, rng, maxa):
    """c_i(S) = sum_j min(|S ∩ B_j|, a_ij) for a random reference partition B
    and random matrix a -- the family that produced the (I)/(II) counterexample."""
    lab = [rng.randrange(n) for _ in range(m)]
    B = [frozenset(g for g in range(m) if lab[g] == j) for j in range(n)]
    a = [[rng.randint(0, maxa) for _ in range(n)] for _ in range(n)]
    out = []
    for i in range(n):
        d = {}
        for S in subsets(m):
            d[S] = sum(min(len(S & B[j]), a[i][j]) for j in range(n))
        out.append(d)
    return out


def dump(cs, m, n):
    for i, c in enumerate(cs):
        print("     agent", i, {tuple(sorted(k)): v for k, v in
                                sorted(c.items(),
                                       key=lambda kv: (len(kv[0]), sorted(kv[0])))})


def sweep(tag, gen, m, n, T):
    nochain = notop = tot = 0
    shown = False
    for _ in range(T):
        cs = gen()
        r = scan(cs, m, n)
        if r is None:
            continue
        ch, tp = r
        tot += 1
        if not ch:
            nochain += 1
            if not shown:
                print("  !! NO CHAIN WITNESS  [%s] n=%d m=%d  (top-good exists: %s)"
                      % (tag, n, m, tp))
                dump(cs, m, n)
                shown = True
        if not tp:
            notop += 1
    print("  %-26s n=%d m=%d | %5d depth>=2 | no chain: %3d | no top-good: %d"
          % (tag, n, m, tot, nochain, notop))
    return nochain, notop


def main():
    rng = random.Random(20260806)
    tot_nochain = tot_notop = 0

    print("=== past the frontier: m = 7, 8, 9 ===")
    for m in (7, 8, 9):
        T = {7: 500, 8: 220, 9: 60}[m]
        a, b = sweep("endpoint-constant", lambda: [
            rand_dicho(m, rng, rng.choice([0.0, 0.05, 0.5, 0.95, 1.0]))
            for _ in range(3)], m, 3, T)
        tot_nochain += a; tot_notop += b
        a, b = sweep("matrix-realising", lambda: matrix_realising(m, 3, rng, 4),
                     m, 3, T)
        tot_nochain += a; tot_notop += b
        a, b = sweep("matrix-realising deep", lambda: matrix_realising(m, 3, rng, 6),
                     m, 3, T)
        tot_nochain += a; tot_notop += b

    print("\n=== more agents ===")
    for (n, m, T) in [(4, 7, 120), (4, 8, 60), (5, 7, 50)]:
        a, b = sweep("matrix-realising", lambda: matrix_realising(m, n, rng, 4),
                     m, n, T)
        tot_nochain += a; tot_notop += b

    print("\n===============================================================")
    print("instances with NO chain witness : %d" % tot_nochain)
    print("instances with NO top-good alloc: %d   (would refute Conjecture 1)"
          % tot_notop)


if __name__ == "__main__":
    main()
