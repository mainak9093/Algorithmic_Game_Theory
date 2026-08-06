"""What do the 37 progress-stuck reachable states look like?

obs:peel-residual: of 522,117 reachable non-terminal states, 37 admit no legal
balance-preserving peel at all, even after a permutation.  Free-first greedy
avoids them on every instance tested, but nothing proves it must.  If they share
a structural feature -- as the dead states did, where death turned out to be
over-commitment to one agent -- the avoidance rule reads off it.

Collected here for every stuck state:
    W                 the workload profile
    |S_j|             candidate-set sizes, and how many chores are still peelable
    c_i(W_i)          own costs
    ell               the subsidy vector
    |W_i|             workload sizes
    peelable-owner    for each peelable chore, which agents still hold it

and then aggregated, to see which of these is constant across the 37.

The question a rule needs answered: is there a cheap predicate, checkable at the
PREDECESSOR of a stuck state, that forbids the step into it?

Run:  python stuck_profile.py
"""
from itertools import permutations
from collections import Counter, deque
import random
import sys

sys.path.insert(0, "../update_6")
sys.path.insert(0, "../update_32")
sys.path.insert(0, "../update_34")
from targetGbal import rand_dicho                                # noqa: E402
from peel_general import legal, cand, terminal, peels, make      # noqa: E402
from deadend_char import admits_balanced                         # noqa: E402
from reachable_stuck import ok, restricted_reachable             # noqa: E402


def ell_vec(cs, W, n):
    a = [[cs[i][W[k]] for k in range(n)] for i in range(n)]
    Wt = [[a[i][i] - a[i][k] for k in range(n)] for i in range(n)]
    e = [0] * n
    for _ in range(n + 1):
        ch = False
        new = list(e)
        for i in range(n):
            for k in range(n):
                if i != k and Wt[i][k] + e[k] > new[i]:
                    new[i] = Wt[i][k] + e[k]; ch = True
        e = new
        if not ch:
            return e
    return None


def progress_stuck(cs, W, n, m, perms):
    """No legal balance-preserving peel from W or any legal permutation of it."""
    for p in perms:
        V = tuple(W[p[i]] for i in range(n))
        if not ok(cs, V, n, m):
            continue
        for _, s in peels(V, n, m):
            if ok(cs, s, n, m):
                return False
    return True


def main():
    rng = random.Random(778899)          # same seed as the counting run
    found = []
    scanned = 0
    print("=== collecting progress-stuck reachable states ===")
    for (n, m, T) in [(3, 4, 50), (3, 5, 20), (3, 6, 6),
                      (4, 3, 40), (4, 4, 12), (5, 3, 12)]:
        perms = list(permutations(range(n)))
        for _ in range(T):
            cs = [rand_dicho(m, rng) for _ in range(n)]
            if max(max(c.values()) for c in cs) < 1:
                continue
            R = restricted_reachable(cs, n, m, perms)
            for W in R:
                if terminal(W, n, m):
                    continue
                scanned += 1
                if progress_stuck(cs, W, n, m, perms):
                    S = cand(W, n, m)
                    found.append(dict(
                        n=n, m=m,
                        W=[sorted(x) for x in W],
                        S=[len(s) for s in S],
                        peelable=[j for j in range(m) if len(S[j]) >= 2],
                        own=[cs[i][W[i]] for i in range(n)],
                        ell=ell_vec(cs, W, n),
                        sizes=sorted(len(x) for x in W),
                    ))
    print("  reachable non-terminal states scanned : %d" % scanned)
    print("  progress-stuck found                  : %d" % len(found))
    print()
    if not found:
        print("  none found at this seed/sizes")
        return
    for k, d in enumerate(found[:8]):
        print("  [%d] n=%d m=%d  W=%s" % (k, d["n"], d["m"], d["W"]))
        print("      |S_j|=%s peelable=%s own=%s ell=%s |W_i|(sorted)=%s"
              % (d["S"], d["peelable"], d["own"], d["ell"], d["sizes"]))
    print()
    print("=== aggregates over all %d ===" % len(found))
    def agg(key, f):
        c = Counter(f(d) for d in found)
        print("  %-26s %s" % (key, dict(sorted(c.items(), key=lambda z: str(z[0])))))
    agg("max ell", lambda d: max(d["ell"]))
    agg("# peelable chores", lambda d: len(d["peelable"]))
    agg("min |S_j|", lambda d: min(d["S"]))
    agg("max |S_j|", lambda d: max(d["S"]))
    agg("max own cost", lambda d: max(d["own"]))
    agg("own-cost spread", lambda d: max(d["own"]) - min(d["own"]))
    agg("workload size spread", lambda d: d["sizes"][-1] - d["sizes"][0])
    agg("# agents at ell=1", lambda d: sum(1 for x in d["ell"] if x == 1))
    print()
    print("  A predicate constant across all 37 is a candidate for the")
    print("  avoidance rule; one that varies is not.")


if __name__ == "__main__":
    main()
