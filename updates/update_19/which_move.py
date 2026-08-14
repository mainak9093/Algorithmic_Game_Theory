"""WHICH transfer witnesses the crux?  Toward a constructive proof.

The crux (hard half of conj:descent): a balanced partition with M := max_i ell_i
>= 2 admits a transfer strictly reducing max ell.  5,724 such partitions have
been checked and all pass, but "some transfer exists" is not a proof.  A proof
needs a RULE.  Two mechanisms could reduce an arc w(i,j) = c_i(A_i) - c_i(A_j):
lower c_i(A_i) by removing a chore, or raise c_i(A_j) by adding one.  Both can
fail outright under dichotomous costs, which cap:

    c(S) = max(|S|-1, 0)  has NO single chore whose addition raises c from the
    empty set, and c(S) = min(|S|,1) has no single chore whose removal lowers c
    from a 2-set.

So the witnessing move must be identified.  Candidate rules, each restricting the
transfer to something a proof could name:

  R1  source = a bundle of an agent attaining max ell ; target = the endpoint of
      a maximum-weight path out of it (which has ell = 0)
  R2  source = argmax ell ; target = argmin_j c_{i*}(A_j)
  R3  source = argmax ell ; target = ANY bundle
  R4  source = ANY bundle ; target = the endpoint of a maximum path
  R5  source = largest bundle ; target = smallest bundle

For each rule: over crux partitions, does SOME transfer allowed by the rule
strictly reduce max ell?  A rule with 100% coverage is the theorem to prove.

Run:  python which_move.py
"""
from itertools import product, permutations
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_17")
sys.path.insert(0, "../update_18")
from minimum_subsidy import rand_dicho, matrix_realising  # noqa: E402
from localsearch_lemma import ell_vec  # noqa: E402


def canon(cs, bundles, n, perms):
    """Return (ell vector, perm) for the min-cost assignment."""
    best = None
    for perm in perms:
        t = sum(cs[i][bundles[perm[i]]] for i in range(n))
        if best is None or t < best[0]:
            best = (t, perm)
    _, perm = best
    a = [[cs[i][bundles[perm[j]]] for j in range(n)] for i in range(n)]
    return ell_vec(a, n), perm


def max_path_endpoints(cs, bundles, n, perm, e):
    """Slots that end a maximum-weight path from some argmax-ell agent.

    Agent i holds bundle slot perm[i].  Arc weights are on agents; we return the
    SLOT indices of the endpoints, since transfers act on bundles.
    """
    a = [[cs[i][bundles[perm[j]]] for j in range(n)] for i in range(n)]
    W = [[a[i][i] - a[i][j] for j in range(n)] for i in range(n)]
    M = max(e)
    ends = set()
    for src in (i for i in range(n) if e[i] == M):
        # walk a maximum path greedily: ell(i) = max_j W[i][j] + ell(j)
        cur = src
        seen = {cur}
        while True:
            nxt = None
            for j in range(n):
                if j != cur and j not in seen and W[cur][j] + e[j] == e[cur]:
                    nxt = j
                    break
            if nxt is None:
                break
            cur = nxt
            seen.add(cur)
        ends.add(perm[cur])
    return ends


def transfer(bundles, src, dst, g):
    nb = list(bundles)
    nb[src] = bundles[src] - {g}
    nb[dst] = bundles[dst] | {g}
    return tuple(nb)


RULES = ["R1", "R2", "R3", "R4", "R5"]


def scan(cs, m, n, perms, stats):
    memo = {}

    def get(b):
        k = tuple(sorted(tuple(sorted(x)) for x in b))
        if k not in memo:
            memo[k] = canon(cs, b, n, perms)
        return memo[k]

    for assign in product(range(n), repeat=m):
        bundles = tuple(frozenset(g for g in range(m) if assign[g] == i)
                        for i in range(n))
        sz = [len(b) for b in bundles]
        if max(sz) - min(sz) > 1:
            continue
        e, perm = get(bundles)
        if e is None or max(e) <= 1:
            continue
        M = max(e)
        stats["crux"] += 1

        argmax_slots = {perm[i] for i in range(n) if e[i] == M}
        ends = max_path_endpoints(cs, bundles, n, perm, e)
        big = max(range(n), key=lambda j: len(bundles[j]))
        small = min(range(n), key=lambda j: len(bundles[j]))
        a = [[cs[i][bundles[perm[j]]] for j in range(n)] for i in range(n)]
        istar = max(range(n), key=lambda i: e[i])
        cheapest = min(range(n), key=lambda j: a[istar][j])
        cheap_slot = perm[cheapest]

        allowed = {
            "R1": [(s, d) for s in argmax_slots for d in ends if s != d],
            "R2": [(s, cheap_slot) for s in argmax_slots if s != cheap_slot],
            "R3": [(s, d) for s in argmax_slots for d in range(n) if s != d],
            "R4": [(s, d) for s in range(n) for d in ends if s != d],
            "R5": [(big, small)] if big != small else [],
        }
        for name in RULES:
            ok = False
            for (s, d) in allowed[name]:
                for g in bundles[s]:
                    ne, _ = get(transfer(bundles, s, d, g))
                    if ne is not None and max(ne) < M:
                        ok = True
                        break
                if ok:
                    break
            if ok:
                stats[name] += 1
            elif name not in stats["firstfail"]:
                stats["firstfail"][name] = (
                    [sorted(b) for b in bundles], e, M)


def main():
    rng = random.Random(818181)
    stats = Counter()
    stats["firstfail"] = {}
    for (n, m, T) in [(3, 4, 300), (3, 6, 200), (3, 7, 120), (3, 9, 40),
                      (4, 6, 100), (4, 8, 25), (5, 6, 35)]:
        perms = list(permutations(range(n)))
        for _ in range(T):
            cs = (matrix_realising(m, n, rng, 3) if rng.random() < 0.5
                  else [rand_dicho(m, rng, rng.choice([0.0, 0.2, 0.5, 0.8, 1.0]))
                        for _ in range(n)])
            if max(max(x.values()) for x in cs) < 2:
                continue
            scan(cs, m, n, perms, stats)
    c = stats["crux"]
    print("=== which transfer witnesses the crux?  %d crux partitions ===" % c)
    print("  rule                                          covered   gaps")
    desc = {"R1": "argmax-ell bundle -> max-path endpoint",
            "R2": "argmax-ell bundle -> its cheapest bundle",
            "R3": "argmax-ell bundle -> anywhere",
            "R4": "anywhere -> max-path endpoint",
            "R5": "largest bundle -> smallest bundle"}
    for name in RULES:
        print("  %-3s %-42s %7d   %d"
              % (name, desc[name], stats[name], c - stats[name]))
    print()
    for name in RULES:
        if stats[name] == c:
            print("  *** %s has FULL coverage -- candidate constructive rule ***" % name)
    for name in RULES:
        if name in stats["firstfail"]:
            b, e, M = stats["firstfail"][name]
            print("  %s first gap: bundles=%s ell=%s M=%d" % (name, b, e, M))


if __name__ == "__main__":
    main()
