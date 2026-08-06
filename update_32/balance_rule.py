"""The balance rule: can it be followed from the root all the way to a terminal?

deadend_char.py found, over 1,192,108 reachable legal states, that the cell
(dead, admits-a-balanced-terminal) is EMPTY.  So

    admits a balanced terminal  ==>  live,

a sufficient condition for liveness that is decidable by degree-constrained
bipartite feasibility, i.e. by flow.  That suggests the peel rule sec:h1prime
says is missing:

    THE BALANCE RULE.  Never peel in a way that destroys the existence of a
    balanced terminal.

The root admits one trivially (every S_j is all of N), so the rule can start.
What remains is whether it can be FOLLOWED: restrict the state graph to states
that are both legal and balance-admitting, and ask whether a terminal is still
reachable from the root inside that restricted set.  If yes on every instance,
the rule is complete and gives:

  - a proof strategy for Conjecture 2 via conj:h1prime, since every state visited
    is legal and the terminal reached is legal, hence a good allocation;
  - a polynomial algorithm, since each step tests balance-feasibility by flow
    rather than searching.

Recorded separately: how much the restriction costs, i.e. how many legal states
survive it, since a rule that prunes almost everything may be reachable but
fragile.

Run:  python balance_rule.py
"""
from itertools import permutations
from collections import Counter, deque
import random
import sys

sys.path.insert(0, "../update_6")
from targetGbal import rand_dicho                                   # noqa: E402
from peel_general import (legal, cand, terminal, peels, make)       # noqa: E402
from deadend_char import admits_balanced                            # noqa: E402


def rule_reaches_terminal(cs, n, m, perms):
    """BFS restricted to states that are legal AND balance-admitting."""
    root = tuple([make(m)] * n)
    if not (legal(cs, root, n) and admits_balanced(root, n, m)):
        return False, 0, False
    seen = {root}
    q = deque([root])
    hit = False
    while q:
        W = q.popleft()
        if terminal(W, n, m):
            hit = True
            break
        nxt = [s for _, s in peels(W, n, m)]
        nxt += [tuple(W[p[i]] for i in range(n)) for p in perms]
        for s in nxt:
            if s in seen:
                continue
            if legal(cs, s, n) and admits_balanced(s, n, m):
                seen.add(s)
                q.append(s)
    return hit, len(seen), True


def main():
    rng = random.Random(777888)
    tot = fail = 0
    ratio = []
    firstfail = None
    print("=== can the balance rule be followed from root to terminal? ===")
    print("   n   m   inst   rule fails   mean states kept")
    for (n, m, T) in [(3, 4, 100), (3, 5, 50), (3, 6, 15),
                      (4, 3, 80), (4, 4, 30), (5, 3, 30), (5, 4, 8)]:
        perms = list(permutations(range(n)))
        f = cnt = 0
        keep = []
        for _ in range(T):
            cs = [rand_dicho(m, rng) for _ in range(n)]
            if max(max(c.values()) for c in cs) < 1:
                continue
            cnt += 1
            tot += 1
            hit, nst, started = rule_reaches_terminal(cs, n, m, perms)
            keep.append(nst)
            if not hit:
                f += 1
                fail += 1
                if firstfail is None:
                    firstfail = (n, m, cs)
        ratio += keep
        print("  %2d  %2d  %5d   %10d   %17.1f"
              % (n, m, cnt, f, (sum(keep) / len(keep)) if keep else 0))
    print()
    print("  instances                        : %d" % tot)
    print("  BALANCE RULE FAILURES            : %d" % fail)
    print()
    if fail == 0:
        print("  *** THE BALANCE RULE IS COMPLETE on every instance tested.")
        print("      Every state it visits is legal, so the terminal it reaches is")
        print("      a good allocation: this is conj:h1prime with an explicit,")
        print("      flow-checkable rule, and hence Conjecture 2 on these")
        print("      instances -- with a polynomial procedure. ***")
        print()
        print("      What must now be PROVED, and it is a single statement:")
        print("      from any legal state admitting a balanced terminal, some legal")
        print("      peel leads to another state admitting a balanced terminal.")
    else:
        n, m, cs = firstfail
        print("  *** the rule FAILS on %d instances; first at n=%d m=%d:" % (fail, n, m))
        for i, c in enumerate(cs):
            print("      agent %d singletons %s"
                  % (i, [c[frozenset({g})] for g in range(m)]))
        print("      so balance-admitting is not maintainable, and the rule needs")
        print("      a further condition.")


if __name__ == "__main__":
    main()
