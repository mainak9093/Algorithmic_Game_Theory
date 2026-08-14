"""The residual class: instances with NO exactly envy-free allocation.

By Corollary cor:chain-residual the chain conjecture is equivalent to its own
restriction to these.  They are ~1.4% of instances and coincide with the class
on which deciding envy-freeness is NP-complete (R10), so they must be generated
deliberately rather than sampled.

Three sources:
  (a) rejection sampling from the endpoint-constant and matrix-realising families;
  (b) R10's Set-Splitting reduction, which is EF-free by construction on NO
      instances of Set Splitting (a hypergraph with no proper 2-colouring);
  (c) small hand families built to force envy.

For each EF-free instance found we ask:
  Q1  does a chain witness exist at all?
  Q2  is the min-cost-balanced / min-envy-count rule one of the witnesses?
  Q3  what do the witnesses look like -- subsidy vector, tier size, bundle sizes?

Run:  python residual.py
"""
from itertools import combinations, product
import random


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
            lo = max(lo, val[T]); hi = min(hi, val[T] + 1)
        pr = rng.random() if hi_prob is None else hi_prob
        val[S] = hi if (lo != hi and rng.random() < pr) else lo
    return val


def matrix_realising(m, n, rng, maxa):
    lab = [rng.randrange(n) for _ in range(m)]
    B = [frozenset(g for g in range(m) if lab[g] == j) for j in range(n)]
    a = [[rng.randint(0, maxa) for _ in range(n)] for _ in range(n)]
    return [{S: sum(min(len(S & B[j]), a[i][j]) for j in range(n))
             for S in subsets(m)} for i in range(n)]


def binary_additive(m, n, D):
    return [{S: len(S & D[i]) for S in subsets(m)} for i in range(n)]


# ---------------------------------------------------------------- primitives
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


def analyse(cs, m, n):
    K = max(max(c.values()) for c in cs)
    parts = []
    for assign in product(range(n), repeat=m):
        bd = [frozenset(g for g in range(m) if assign[g] == i) for i in range(n)]
        a = [[cs[i][bd[j]] for j in range(n)] for i in range(n)]
        parts.append((bd, a))

    has_ef = any(all(a[i][i] <= a[i][j] for i in range(n) for j in range(n))
                 for _, a in parts)
    chain = []
    top = []
    for bd, a in parts:
        okK, eK = ell_ok(a, n, K)
        if okK:
            top.append((bd, a, eK))
        if all(ell_ok(a, n, k)[0] for k in range(1, K + 1)):
            chain.append((bd, a, eK))
    return has_ef, chain, top, K


def rule_pick(cs, m, n):
    """min total cost among cardinality-balanced, tie-broken by envy count."""
    best = None; wins = []
    for assign in product(range(n), repeat=m):
        bd = [frozenset(g for g in range(m) if assign[g] == i) for i in range(n)]
        ss = sorted(len(b) for b in bd)
        if ss[-1] - ss[0] > 1:
            continue
        tot = sum(cs[i][bd[i]] for i in range(n))
        if best is None or tot < best:
            best = tot; wins = [bd]
        elif tot == best:
            wins.append(bd)
    ec = lambda bd: sum(1 for i in range(n) for j in range(n)
                        if i != j and cs[i][bd[i]] > cs[i][bd[j]])
    b2 = min(ec(bd) for bd in wins)
    return [bd for bd in wins if ec(bd) == b2]


def key(bd):
    return tuple(tuple(sorted(b)) for b in bd)


def main():
    rng = random.Random(777)
    found = []

    print("=== (a) rejection sampling for EF-free instances ===")
    tries = 0
    for (n, m, T) in [(3, 5, 4000), (3, 6, 2500), (4, 5, 2500), (4, 6, 1200)]:
        got = 0
        for _ in range(T):
            tries += 1
            cs = (matrix_realising(m, n, rng, 3) if rng.random() < 0.5
                  else [rand_dicho(m, rng, rng.choice([0.0, 0.1, 0.5, 0.9, 1.0]))
                        for _ in range(n)])
            K = max(max(c.values()) for c in cs)
            if K < 2:
                continue
            has_ef, chain, top, K = analyse(cs, m, n)
            if not has_ef:
                got += 1
                found.append((cs, m, n, chain, top, K))
        print("  n=%d m=%d : %d EF-free instances found" % (n, m, got))

    print("\n=== (b) R10 Set-Splitting family (EF-free by construction) ===")
    # triangle: U={v1,v2,v3}, F={ {v1,v2},{v1,v3},{v2,v3} } has no proper 2-colouring
    # reduction: n = r'+2 = 5 agents, m = r'+q = 6 chores, binary additive
    D = [frozenset({0, 1, 2, 3, 4}), frozenset({0, 1, 2, 3, 5}),
         frozenset({0, 1, 2, 4, 5}), frozenset({0, 1, 2}), frozenset({0, 1, 2})]
    ss = binary_additive(6, 5, D)
    has_ef, chain, top, K = analyse(ss, 6, 5)
    print("  set-splitting n=5 m=6 : exactly-EF exists = %s | chain witnesses = %d"
          " | top-good = %d | K = %d" % (has_ef, len(chain), len(top), K))
    if not has_ef:
        found.append((ss, 6, 5, chain, top, K))

    print("\n=== analysis of the residual class ===")
    print("  EF-free instances collected : %d" % len(found))
    nochain = 0
    rule_hits = rule_tot = 0
    tiers = {}
    for cs, m, n, chain, top, K in found:
        if not chain:
            nochain += 1
            print("  !! NO CHAIN WITNESS  n=%d m=%d" % (n, m))
            for i, c in enumerate(cs):
                print("     agent", i, {tuple(sorted(k)): v for k, v in
                                        sorted(c.items(),
                                               key=lambda kv: (len(kv[0]), sorted(kv[0])))})
            continue
        cw = {key(bd) for bd, _, _ in chain}
        sel = rule_pick(cs, m, n)
        rule_tot += 1
        if any(key(bd) in cw for bd in sel):
            rule_hits += 1
        for bd, a, e in chain:
            t = sum(1 for v in e if v == 1)
            tiers[t] = tiers.get(t, 0) + 1
    print("  with NO chain witness       : %d" % nochain)
    print("  rule selects a chain witness: %d / %d" % (rule_hits, rule_tot))
    print("  chain witnesses by |paid set|: %s" % dict(sorted(tiers.items())))
    print("  fraction of chain witnesses that are zero-subsidy: %.3f"
          % (tiers.get(0, 0) / max(1, sum(tiers.values()))))


if __name__ == "__main__":
    main()
