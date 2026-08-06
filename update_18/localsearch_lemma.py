"""Is Conjecture 2 provable by local search on a lexicographic potential?

REFORMULATION (update_17).  Writing delta_j = [j in S], the two-tier condition is
    c_i(A_i) - delta_i  <=  c_i(A_j) - delta_j     for all i,j,
so a good allocation is one where every agent holds a bundle minimising the
DISCOUNTED cost  c_i(B_j) - delta_j,  the discount depending only on the slot.

CANONICAL FORM.  By Halpern-Shah, an allocation is envy-freeable iff it maximises
welfare over reassignments of its own bundles.  So for an unordered partition B
the canonical assignment is the min-cost perfect matching; every partition then
becomes envy-freeable and ell is finite.  The search space is therefore the set
of PARTITIONS, with the matching determined.

THE POTENTIAL.  Lexicographically,
    Psi(B) = ( max_i ell(i),  #{i : ell(i) = max},  sum_i c_i(B_i) ).
Conjecture 2 says some B has max ell <= 1.

THE LEMMA A PROOF WOULD NEED (tested here, call it (L)):
    every partition with max ell >= 2 admits a SINGLE-CHORE move
    (transfer one chore between bundles) that strictly decreases Psi.
(L) implies Conjecture 2 immediately: Psi is bounded below and strictly
decreasing, so local search terminates, and it can only stop at max ell <= 1.

Two tests:
  (L) exhaustively over ALL partitions of small instances -- this is the lemma
      itself, and a single stuck partition refutes it;
  (LS) local search from random starts, which is the weaker practical claim.

Also reported: whether adding SWAP moves (exchange two chores) rescues any
partition that transfers alone cannot.

Run:  python localsearch_lemma.py
"""
from itertools import product, permutations
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_17")
from minimum_subsidy import rand_dicho, matrix_realising  # noqa: E402


def ell_vec(a, n):
    """Longest-path subsidies, or None if a positive cycle exists."""
    W = [[a[i][i] - a[i][j] for j in range(n)] for i in range(n)]
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
            return e
    return None


def canonical(cs, bundles, n, memo):
    """Assign bundles to agents by min total cost; return (Psi, ell)."""
    key = tuple(sorted(tuple(sorted(b)) for b in bundles))
    if key in memo:
        return memo[key]
    best = None
    for perm in permutations(range(n)):
        # agent i receives bundles[perm[i]]
        tot = sum(cs[i][bundles[perm[i]]] for i in range(n))
        if best is None or tot < best[0]:
            best = (tot, perm)
    tot, perm = best
    a = [[cs[i][bundles[perm[j]]] for j in range(n)] for i in range(n)]
    e = ell_vec(a, n)
    if e is None:                      # cannot happen at a min-cost matching
        res = ((10 ** 6, 10 ** 6, tot), None)
    else:
        mx = max(e)
        res = ((mx, sum(1 for x in e if x == mx), tot), e)
    memo[key] = res
    return res


def moves(bundles, n, m, swaps=False):
    """Single-chore transfers (and optionally swaps) as new bundle tuples."""
    out = []
    for src in range(n):
        for g in bundles[src]:
            for dst in range(n):
                if dst == src:
                    continue
                nb = list(bundles)
                nb[src] = bundles[src] - {g}
                nb[dst] = bundles[dst] | {g}
                out.append(tuple(nb))
    if swaps:
        for i in range(n):
            for j in range(i + 1, n):
                for g in bundles[i]:
                    for h in bundles[j]:
                        nb = list(bundles)
                        nb[i] = (bundles[i] - {g}) | {h}
                        nb[j] = (bundles[j] - {h}) | {g}
                        out.append(tuple(nb))
    return out


def test_lemma(cs, m, n):
    """(stuck_transfer, stuck_with_swaps, any_good) over ALL partitions."""
    memo = {}
    stuck_t = stuck_s = 0
    any_good = False
    worst = None
    for assign in product(range(n), repeat=m):
        bundles = tuple(frozenset(g for g in range(m) if assign[g] == i)
                        for i in range(n))
        psi, e = canonical(cs, bundles, n, memo)
        if psi[0] <= 1:
            any_good = True
            continue
        better_t = any(canonical(cs, nb, n, memo)[0] < psi
                       for nb in moves(bundles, n, m, swaps=False))
        if not better_t:
            stuck_t += 1
            better_s = any(canonical(cs, nb, n, memo)[0] < psi
                           for nb in moves(bundles, n, m, swaps=True))
            if not better_s:
                stuck_s += 1
                if worst is None:
                    worst = (bundles, psi, e)
    return stuck_t, stuck_s, any_good, worst


def local_search(cs, m, n, rng, tries=8):
    """Does descent from random starts reach max ell <= 1?"""
    memo = {}
    for _ in range(tries):
        bundles = [set() for _ in range(n)]
        for g in range(m):
            bundles[rng.randrange(n)].add(g)
        bundles = tuple(frozenset(b) for b in bundles)
        for _ in range(200):
            psi, _ = canonical(cs, bundles, n, memo)
            if psi[0] <= 1:
                return True
            best = None
            for nb in moves(bundles, n, m, swaps=True):
                q, _ = canonical(cs, nb, n, memo)
                if q < psi and (best is None or q < best[0]):
                    best = (q, nb)
            if best is None:
                break
            bundles = best[1]
        else:
            break
    return False


def main():
    rng = random.Random(1234567)
    tot = 0
    lemma_fail = 0
    lemma_fail_swaps = 0
    ls_fail = 0
    nogood = 0
    examples = []
    stuck_hist = Counter()
    for (n, m, T) in [(3, 4, 700), (3, 5, 400), (3, 6, 120),
                      (4, 4, 400), (4, 5, 120)]:
        for _ in range(T):
            cs = (matrix_realising(m, n, rng, 3) if rng.random() < 0.55
                  else [rand_dicho(m, rng, rng.choice([0.0, 0.15, 0.5, 0.85, 1.0]))
                        for _ in range(n)])
            if max(max(c.values()) for c in cs) < 1:
                continue
            tot += 1
            st, ss, good, worst = test_lemma(cs, m, n)
            if not good:
                nogood += 1
                print("  !! NO good allocation (refutes Conjecture 2): n=%d m=%d" % (n, m))
            if st:
                lemma_fail += 1
                stuck_hist[st] += 1
            if ss:
                lemma_fail_swaps += 1
                if len(examples) < 2:
                    examples.append((cs, m, n, worst))
            if not local_search(cs, m, n, rng):
                ls_fail += 1
    print("=== local-search lemma, %d instances ===" % tot)
    print("  instances with NO good allocation                  : %d" % nogood)
    print("  (L) partitions stuck under TRANSFERS  -- instances : %d" % lemma_fail)
    print("  (L) partitions stuck under TRANSFERS+SWAPS         : %d" % lemma_fail_swaps)
    print("  (LS) descent failed to reach max ell <= 1          : %d" % ls_fail)
    if stuck_hist:
        print("  stuck partitions per affected instance:",
              dict(sorted(stuck_hist.items())[:8]))
    for cs, m, n, worst in examples:
        bundles, psi, e = worst
        print("\n  stuck even with swaps: n=%d m=%d bundles=%s Psi=%s ell=%s"
              % (n, m, [sorted(b) for b in bundles], psi, e))
        for i in range(n):
            print("      agent %d singletons %s"
                  % (i, [cs[i][frozenset({g})] for g in range(m)]))


if __name__ == "__main__":
    main()
