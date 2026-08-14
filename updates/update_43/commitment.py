"""Phase B2: drop balance, and test the commitment predicate as Phi.

conj:h1 -- "from every legal non-terminal state some legal move exists" -- is
already refuted (prop:deadends: 9 legal dead ends among 175 legal states of the
witness).  So dropping balance-admissibility does NOT remove the obstruction: the
graph is wider, but the dead ends are still there.

What rem:balance records is more useful.  All nine dead ends of the witness have
the same shape: ONE AGENT IS ALREADY COMMITTED TO A TWO-ELEMENT TERMINAL BUNDLE.
That suggests a predicate on the STATE ALONE -- which is what B1 showed a rule
cannot be if it reads the move as well.  Define the committed bundle

    C_i(W) := { j : S_j = {i} },

the chores whose owner is already decided, and put

    (COMMIT)   c_i(C_i(W)) <= 1   for every agent i.

Tested here, on the LEGAL-only graph (no balance restriction):

  (P1) is (COMMIT) sufficient for liveness?    dead & (COMMIT) should be empty
  (P2) does (COMMIT) hold at the root?         trivially, C_i = empty
  (P3) is (COMMIT) maintainable?               from every legal non-terminal state
       satisfying it, is there a legal peel to another state satisfying it?
  (P4) how much does dropping balance help?    stuck states with and without it

(P1)+(P2)+(P3) would give conj:h1prime -- and hence Conjecture 2 -- with Phi =
(COMMIT), a predicate needing no flow computation at all.

Run:  python commitment.py
"""
from itertools import permutations
from collections import Counter, deque
import random
import sys

sys.path.insert(0, "../update_6")
sys.path.insert(0, "../update_32")
from targetGbal import rand_dicho                             # noqa: E402
from peel_general import legal, cand, terminal, peels, make   # noqa: E402


def committed_ok(cs, W, n, m):
    """(COMMIT): every agent's already-decided bundle costs it at most 1."""
    S = cand(W, n, m)
    for i in range(n):
        C = frozenset(j for j in range(m) if S[j] == frozenset({i}))
        if cs[i][C] > 1:
            return False
    return True


def live_set_legal(cs, n, m, perms, cap=6000):
    """Reachable LEGAL states from the root, and which can reach a terminal."""
    root = tuple([make(m)] * n)
    if not legal(cs, root, n):
        return set(), set()
    seen = {root}
    q = deque([root])
    while q and len(seen) < cap:
        W = q.popleft()
        for s in ([s for _, s in peels(W, n, m)]
                  + [tuple(W[p[i]] for i in range(n)) for p in perms]):
            if s not in seen and legal(cs, s, n):
                seen.add(s)
                q.append(s)
    good = set(W for W in seen if terminal(W, n, m))
    changed = True
    while changed:
        changed = False
        for W in seen:
            if W in good:
                continue
            nxt = [s for _, s in peels(W, n, m)]
            nxt += [tuple(W[p[i]] for i in range(n)) for p in perms]
            if any(s in good for s in nxt):
                good.add(W)
                changed = True
    return seen, good


def main():
    rng = random.Random(43434343)
    cont = Counter()
    p3_bad = 0
    p3_tot = 0
    ex1 = ex3 = None
    print("=== (COMMIT) on the legal-only graph ===")
    print("   n   m   inst   states   dead&COMMIT   (P3) fails")
    for (n, m, T) in [(3, 4, 40), (3, 5, 18), (3, 6, 6),
                      (4, 3, 30), (4, 4, 12), (5, 3, 12)]:
        perms = list(permutations(range(n)))
        loc = Counter()
        f3 = cnt = 0
        for _ in range(T):
            cs = [rand_dicho(m, rng) for _ in range(n)]
            if max(max(c.values()) for c in cs) < 1:
                continue
            cnt += 1
            seen, good = live_set_legal(cs, n, m, perms)
            for W in seen:
                lv = W in good
                ck = committed_ok(cs, W, n, m)
                cont[(lv, ck)] += 1
                loc[(lv, ck)] += 1
                if (not lv) and ck and ex1 is None:
                    ex1 = (n, m, [sorted(x) for x in W])
                # (P3) maintainability
                if ck and not terminal(W, n, m):
                    p3_tot += 1
                    okmove = False
                    for _, s in peels(W, n, m):
                        if legal(cs, s, n) and committed_ok(cs, s, n, m):
                            okmove = True
                            break
                    if not okmove:
                        for p in perms:
                            V = tuple(W[p[i]] for i in range(n))
                            if not (legal(cs, V, n) and committed_ok(cs, V, n, m)):
                                continue
                            if any(legal(cs, s, n) and committed_ok(cs, s, n, m)
                                   for _, s in peels(V, n, m)):
                                okmove = True
                                break
                    if not okmove:
                        p3_bad += 1
                        f3 += 1
                        if ex3 is None:
                            ex3 = (n, m, [sorted(x) for x in W])
        print("  %2d  %2d  %5d   %6d   %11d   %10d"
              % (n, m, cnt, sum(loc.values()), loc[(False, True)], f3))
    tot = sum(cont.values())
    print()
    print("  legal reachable states examined : %d" % tot)
    print("  (live, COMMIT)   : %d" % cont[(True, True)])
    print("  (live, not)      : %d" % cont[(True, False)])
    print("  (dead, COMMIT)   : %d   <- violates (P1)" % cont[(False, True)])
    print("  (dead, not)      : %d" % cont[(False, False)])
    print()
    print("  (P1) COMMIT => live      : %s"
          % ("HOLDS" if cont[(False, True)] == 0 else "FAILS"))
    print("  (P3) COMMIT maintainable : %d / %d states have no COMMIT-preserving"
          " legal move" % (p3_bad, p3_tot))
    print()
    if cont[(False, True)] == 0 and p3_bad == 0:
        print("  *** (P1)+(P2)+(P3) hold: Phi = (COMMIT) would give conj:h1prime,")
        print("      hence Conjecture 2, with NO flow computation needed. ***")
    else:
        if cont[(False, True)] and ex1:
            print("  (P1) fails; first dead state satisfying COMMIT: n=%d m=%d W=%s" % ex1)
        if p3_bad and ex3:
            print("  (P3) fails; first COMMIT state with no COMMIT-preserving move:")
            print("       n=%d m=%d W=%s" % ex3)


if __name__ == "__main__":
    main()
