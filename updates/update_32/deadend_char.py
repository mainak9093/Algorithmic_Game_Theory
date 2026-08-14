"""Characterising the peel dead ends: is BALANCE the missing rule?

peel_general.py established that conj:h1prime holds at every size tested (0 bad
roots) while all three named greedy rules deadlock.  So a terminal is always
reachable from the root, but not by any local rule yet tried, and sec:h1prime's
missing ingredient -- "a peel rule that provably never enters a deadlock" -- is
exactly the gap.

rem:balance is the standing guess at its shape: that every dead end is a state
already committed to an UNBALANCED terminal.  This script tests it.

From a state W the terminals reachable by peels alone (ignoring legality) are
exactly the choice functions f assigning each chore j an owner from its candidate
set S_j; the induced bundle sizes are |A_i| = #{j : f(j) = i}.  Say W ADMITS A
BALANCED TERMINAL if some such f has max_i |A_i| - min_i |A_i| <= 1.

Two hypotheses, tested as a 2x2 contingency over every reachable legal state:

    (B1)  dead  ==>  admits no balanced terminal      (rem:balance's guess)
    (B2)  admits a balanced terminal  ==>  live       (the converse)

If both hold, "live" and "admits a balanced terminal" coincide, and the missing
rule is simply: never peel in a way that destroys the existence of a balanced
terminal.  That is a degree-constrained bipartite feasibility question, decidable
by flow in polynomial time -- so it would be a genuine RULE, not another
existence statement.

Run:  python deadend_char.py
"""
from itertools import permutations, product
from collections import Counter, deque
import random
import sys

sys.path.insert(0, "../update_6")
from targetGbal import rand_dicho                                   # noqa: E402
from peel_general import (ell, legal, cand, terminal, peels, make)  # noqa: E402


def admits_balanced(W, n, m):
    """Is some choice function from the candidate sets cardinality-balanced?"""
    S = cand(W, n, m)
    for f in product(*[sorted(s) for s in S]):
        sz = [0] * n
        for owner in f:
            sz[owner] += 1
        if max(sz) - min(sz) <= 1:
            return True
    return False


def live_set(cs, n, m, perms):
    """Reachable legal states, and which of them can still reach a terminal."""
    root = tuple([make(m)] * n)
    if not legal(cs, root, n):
        return set(), set()
    seen = {root}
    q = deque([root])
    while q:
        W = q.popleft()
        nxt = [s for _, s in peels(W, n, m)]
        nxt += [tuple(W[p[i]] for i in range(n)) for p in perms]
        for s in nxt:
            if s not in seen and legal(cs, s, n):
                seen.add(s)
                q.append(s)
    good = set(s for s in seen if terminal(s, n, m))
    changed = True
    while changed:
        changed = False
        for W in seen:
            if W in good:
                continue
            nxt = [s for _, s in peels(W, n, m)]
            nxt += [tuple(W[p[i]] for i in range(n)) for p in perms]
            if any(s in good for s in nxt):
                good.add(W); changed = True
    return seen, good


def main():
    rng = random.Random(4242)
    cont = Counter()          # (live, admits_balanced) -> count
    tot = 0
    ex_b1 = ex_b2 = None
    print("=== dead-end characterisation: live vs admits-balanced-terminal ===")
    print("   n   m   inst   states   (live,bal)  (live,unbal)  (dead,bal)  (dead,unbal)")
    for (n, m, T) in [(3, 4, 90), (3, 5, 40), (3, 6, 12),
                      (4, 3, 70), (4, 4, 25), (5, 3, 25)]:
        perms = list(permutations(range(n)))
        loc = Counter()
        cnt = st = 0
        for _ in range(T):
            cs = [rand_dicho(m, rng) for _ in range(n)]
            if max(max(c.values()) for c in cs) < 1:
                continue
            cnt += 1
            tot += 1
            seen, good = live_set(cs, n, m, perms)
            for W in seen:
                st += 1
                lv = W in good
                bal = admits_balanced(W, n, m)
                loc[(lv, bal)] += 1
                cont[(lv, bal)] += 1
                if (not lv) and bal and ex_b1 is None:
                    ex_b1 = (n, m, [sorted(x) for x in W])
                if lv and (not bal) and ex_b2 is None:
                    ex_b2 = (n, m, [sorted(x) for x in W])
        print("  %2d  %2d  %5d   %6d   %10d  %12d  %10d  %12d"
              % (n, m, cnt, st, loc[(True, True)], loc[(True, False)],
                 loc[(False, True)], loc[(False, False)]))
    print()
    print("  states examined      : %d" % sum(cont.values()))
    print("  (live, balanced)     : %d" % cont[(True, True)])
    print("  (live, unbalanced)   : %d" % cont[(True, False)])
    print("  (dead, balanced)     : %d   <- violates (B1)" % cont[(False, True)])
    print("  (dead, unbalanced)   : %d" % cont[(False, False)])
    print()
    b1 = cont[(False, True)] == 0
    b2 = cont[(False, True)] == 0
    print("  (B1) dead => no balanced terminal : %s" % ("HOLDS" if b1 else "FAILS"))
    print("  (B2) balanced terminal => live    : %s" % ("HOLDS" if b2 else "FAILS"))
    if cont[(True, False)]:
        print("  note: %d live states admit no balanced terminal, so 'live' is"
              % cont[(True, False)])
        print("        STRICTLY WEAKER than 'admits a balanced terminal'.")
    print()
    if b1:
        print("  *** Maintaining the existence of a balanced terminal is SUFFICIENT")
        print("      to stay live.  That is a degree-constrained bipartite")
        print("      feasibility test, decidable by flow -- a genuine peel RULE. ***")
    elif ex_b1:
        print("  (B1) fails; first dead state admitting a balanced terminal:")
        print("     n=%d m=%d W=%s" % ex_b1)


if __name__ == "__main__":
    main()
