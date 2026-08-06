"""Is the root-reachable restricted subgraph free of stuck states?

rem:balance-rule-pointwise-false showed 5 legal balance-admitting states admit no
legal balance-preserving move.  conj:balance-rule survives only because those
states are never REACHED from the root along the restricted graph.  That has to
be checked rather than assumed, and it is the difference between an algorithm
that needs backtracking and one that does not.

Let R be the set of states reachable from the root by moves that keep the state
both legal and balance-admitting.  Three questions:

  (S1)  does every non-terminal W in R have a move staying in R?
        If yes, the rule is greedy-safe: no backtracking, and the algorithm of
        prop:balance-rule-implies runs as stated.
  (S2)  are any of the 5 known stuck states in R?
  (S3)  is the simpler strategy "always take a FREE peel when one exists,
        otherwise any legal balance-preserving peel" already complete?
        A free peel is one where no arc into the peeled agent rises, so
        legality is automatic by lem:peel -- if free peels alone suffice, the
        rule needs no legality test at all.

Run:  python reachable_stuck.py
"""
from itertools import permutations
from collections import Counter, deque
import random
import sys

sys.path.insert(0, "../update_6")
sys.path.insert(0, "../update_32")
from targetGbal import rand_dicho                                # noqa: E402
from peel_general import legal, cand, terminal, peels, make      # noqa: E402
from deadend_char import admits_balanced                         # noqa: E402


def ok(cs, W, n, m):
    return legal(cs, W, n) and admits_balanced(W, n, m)


def is_free(cs, W, s, x, n):
    """No arc into the peeled agent x rises: c_k(W_x) == c_k(s_x) for all k."""
    return all(cs[k][W[x]] == cs[k][s[x]] for k in range(n) if k != x)


def restricted_reachable(cs, n, m, perms):
    root = tuple([make(m)] * n)
    if not ok(cs, root, n, m):
        return set()
    seen = {root}
    q = deque([root])
    while q:
        W = q.popleft()
        nxt = [s for _, s in peels(W, n, m)]
        nxt += [tuple(W[p[i]] for i in range(n)) for p in perms]
        for s in nxt:
            if s not in seen and ok(cs, s, n, m):
                seen.add(s); q.append(s)
    return seen


def free_greedy(cs, n, m, perms, cap=400):
    """Prefer a free legal balance-preserving peel; else any legal one."""
    W = tuple([make(m)] * n)
    for _ in range(cap):
        if terminal(W, n, m):
            return True
        opts = [(mv, s) for mv, s in peels(W, n, m) if ok(cs, s, n, m)]
        if not opts:
            for p in perms:
                V = tuple(W[p[i]] for i in range(n))
                if not ok(cs, V, n, m):
                    continue
                o2 = [(mv, s) for mv, s in peels(V, n, m) if ok(cs, s, n, m)]
                if o2:
                    W = V; opts = o2; break
            if not opts:
                return False
        fr = [o for o in opts if is_free(cs, W, o[1], o[0][0], n)]
        W = (fr or opts)[0][1]
    return False


def main():
    rng = random.Random(343434)
    stuck_in_R = 0
    statesR = 0
    freegreedy_fail = 0
    tot = 0
    exs = None
    hist = Counter()
    print("=== stuck states inside the root-reachable restricted subgraph ===")
    print("   n   m   inst   |R|      stuck in R   free-greedy fails")
    for (n, m, T) in [(3, 4, 70), (3, 5, 30), (3, 6, 10),
                      (4, 3, 60), (4, 4, 16), (5, 3, 16), (5, 4, 5)]:
        perms = list(permutations(range(n)))
        sR = st = cnt = fg = 0
        for _ in range(T):
            cs = [rand_dicho(m, rng) for _ in range(n)]
            if max(max(c.values()) for c in cs) < 1:
                continue
            cnt += 1
            tot += 1
            R = restricted_reachable(cs, n, m, perms)
            st += len(R)
            statesR += len(R)
            for W in R:
                if terminal(W, n, m):
                    continue
                moves = [s for _, s in peels(W, n, m)]
                moves += [tuple(W[p[i]] for i in range(n)) for p in perms]
                if not any(s in R for s in moves):
                    sR += 1
                    stuck_in_R += 1
                    if exs is None:
                        exs = (n, m, [sorted(x) for x in W])
            if not free_greedy(cs, n, m, perms):
                fg += 1
                freegreedy_fail += 1
        print("  %2d  %2d  %5d   %8d   %10d   %14d" % (n, m, cnt, st, sR, fg))
    print()
    print("  instances                                : %d" % tot)
    print("  states in the restricted reachable set   : %d" % statesR)
    print("  (S1/S2) STUCK states inside that set     : %d" % stuck_in_R)
    print("  (S3) free-first greedy failures          : %d" % freegreedy_fail)
    print()
    if stuck_in_R == 0:
        print("  *** (S1) HOLDS: every reachable state has a move staying inside.")
        print("      The rule is greedy-safe -- no backtracking -- so the algorithm")
        print("      of prop:balance-rule-implies runs exactly as stated, and the 5")
        print("      pointwise counterexamples are unreachable from the root. ***")
    else:
        print("  (S1) fails: %d reachable states are stuck; first %s" % (stuck_in_R, exs))
        print("      the algorithm needs backtracking, or a finer rule.")
    if freegreedy_fail == 0:
        print()
        print("  *** (S3) free-first greedy is COMPLETE on every instance tested:")
        print("      a rule needing no lookahead beyond one legality test. ***")


if __name__ == "__main__":
    main()
