"""Same rule coverage, but under the P3 criterion, which is weaker.

which_move.py asked each rule to strictly reduce max ell, because that is what
Psi = P6 = (max ell, sum |B_i|^2) demands on a balanced partition.  No rule had
full coverage; R3 (source = the argmax-ell bundle) missed 2,304 of 7,416, so the
witnessing transfer need not even involve the envious agent.

But P3 = (max ell, #at max, sum |B_i|^2) also had zero stuck partitions, and on a
balanced partition it only asks that (max ell, #at max) drop lexicographically --
either the maximum falls, OR it stays and fewer agents attain it.  That is a
strictly weaker requirement, so the rules deserve a second hearing.  If some rule
is complete under the P3 criterion, it is the theorem to prove, and P3 rather
than P6 is the potential Approach 7 should be built on.

The reduction theorem thm:descent-suffices is indifferent to the choice: P3 takes
O(n m^3) values instead of O(m^3), still polynomially many.

Run:  python which_move_p3.py
"""
from itertools import product, permutations
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_17")
sys.path.insert(0, "../update_18")
from minimum_subsidy import rand_dicho, matrix_realising  # noqa: E402
from which_move import canon, max_path_endpoints, transfer, RULES  # noqa: E402


def key3(e):
    m = max(e)
    return (m, sum(1 for x in e if x == m))


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
        cur = key3(e)
        stats["crux"] += 1

        argmax_slots = {perm[i] for i in range(n) if e[i] == M}
        ends = max_path_endpoints(cs, bundles, n, perm, e)
        big = max(range(n), key=lambda j: len(bundles[j]))
        small = min(range(n), key=lambda j: len(bundles[j]))
        a = [[cs[i][bundles[perm[j]]] for j in range(n)] for i in range(n)]
        istar = max(range(n), key=lambda i: e[i])
        cheap_slot = perm[min(range(n), key=lambda j: a[istar][j])]

        allowed = {
            "R1": [(s, d) for s in argmax_slots for d in ends if s != d],
            "R2": [(s, cheap_slot) for s in argmax_slots if s != cheap_slot],
            "R3": [(s, d) for s in argmax_slots for d in range(n) if s != d],
            "R4": [(s, d) for s in range(n) for d in ends if s != d],
            "R5": [(big, small)] if big != small else [],
        }
        anyok = False
        for name in RULES:
            ok = False
            for (s, d) in allowed[name]:
                for g in bundles[s]:
                    ne, _ = get(transfer(bundles, s, d, g))
                    if ne is not None and key3(ne) < cur:
                        ok = True
                        break
                if ok:
                    break
            if ok:
                stats[name] += 1
                anyok = True
        # ALL transfers, the descent lemma itself under the P3 criterion
        allok = False
        for s in range(n):
            for g in bundles[s]:
                for d in range(n):
                    if d == s:
                        continue
                    ne, _ = get(transfer(bundles, s, d, g))
                    if ne is not None and key3(ne) < cur:
                        allok = True
                        break
                if allok:
                    break
            if allok:
                break
        if allok:
            stats["ALL"] += 1


def main():
    rng = random.Random(818181)          # same seed as which_move.py
    stats = Counter()
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
    print("=== rule coverage under the P3 criterion, %d crux partitions ===" % c)
    desc = {"R1": "argmax-ell bundle -> max-path endpoint",
            "R2": "argmax-ell bundle -> its cheapest bundle",
            "R3": "argmax-ell bundle -> anywhere",
            "R4": "anywhere -> max-path endpoint",
            "R5": "largest bundle -> smallest bundle"}
    print("  rule                                          covered   gaps")
    for name in RULES:
        print("  %-3s %-42s %7d   %d"
              % (name, desc[name], stats[name], c - stats[name]))
    print("  %-3s %-42s %7d   %d"
          % ("ALL", "every transfer (the descent lemma itself)",
             stats["ALL"], c - stats["ALL"]))
    print()
    full = [n for n in RULES if stats[n] == c]
    if full:
        for name in full:
            print("  *** %s is COMPLETE under the P3 criterion -- "
                  "candidate constructive rule ***" % name)
    else:
        print("  no named rule is complete even under the weaker P3 criterion")


if __name__ == "__main__":
    main()
