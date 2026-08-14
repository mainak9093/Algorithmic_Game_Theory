"""Why does balance-admitting imply live?  Decomposing conj:balance-rule.

obs:balance-characterises found, over 1,192,108 states, that a state admitting a
balanced terminal is never dead.  That is empirical; a proof needs the mechanism.
The natural explanation splits into two checkable pieces.

  (Q1)  every legal state admitting a balanced terminal admits one that is
        itself LEGAL, i.e. the induced allocation has max ell <= 1;
  (Q2)  the peels realising such a terminal can be ORDERED so that every
        intermediate state stays legal.

(Q1) and (Q2) together give liveness directly, and hence conj:balance-rule.
They are worth separating because they are different kinds of statement: (Q1) is
about the sub-instance a state defines -- essentially a conditional form of the
balance lemma of Approach 8 -- while (Q2) is a scheduling statement of the kind
(INC) already established for a different frame.

Note the subtlety (Q1) resolves: "admits a balanced terminal" is a statement
about CANDIDATE SETS only and ignores costs entirely, yet it implies a statement
about the envy graph.  If (Q1) holds, the reason is that the candidate sets carry
enough freedom to place the chores well, and that is a provable-looking claim.

Measured over every reachable legal balance-admitting state:
    Q1 holds / fails
    among Q1-successes, whether some legal ordering of the required peels exists

Run:  python why_balance_works.py
"""
from itertools import permutations, product
from collections import Counter, deque
import random
import sys

sys.path.insert(0, "../update_6")
sys.path.insert(0, "../update_32")
from targetGbal import rand_dicho                                  # noqa: E402
from peel_general import legal, cand, terminal, peels, make        # noqa: E402
from deadend_char import admits_balanced                           # noqa: E402


def balanced_terminals(W, n, m):
    """All terminals below W with balanced bundle sizes, as owner tuples."""
    S = cand(W, n, m)
    out = []
    for f in product(*[sorted(s) for s in S]):
        sz = [0] * n
        for o in f:
            sz[o] += 1
        if max(sz) - min(sz) <= 1:
            out.append(f)
    return out


def state_of(f, n, m):
    return tuple(frozenset(j for j in range(m) if f[j] == i) for i in range(n))


def ordering_exists(cs, W, f, n, m):
    """Can the peels from W down to terminal f be ordered keeping legality?"""
    target = state_of(f, n, m)
    # required removals: (i,j) with j in W_i but i != f(j)
    req = [(i, j) for i in range(n) for j in W[i] if f[j] != i]
    if not req:
        return legal(cs, W, n)
    start = W
    seen = {start}
    q = deque([start])
    while q:
        cur = q.popleft()
        if cur == target:
            return True
        for (i, j) in req:
            if j in cur[i]:
                nw = list(cur)
                nw[i] = cur[i] - {j}
                nw = tuple(nw)
                if nw not in seen and legal(cs, nw, n):
                    seen.add(nw)
                    q.append(nw)
    return False


def reachable_legal(cs, n, m, perms, cap=4000):
    root = tuple([make(m)] * n)
    if not legal(cs, root, n):
        return []
    seen = {root}
    q = deque([root])
    while q and len(seen) < cap:
        W = q.popleft()
        nxt = [s for _, s in peels(W, n, m)]
        nxt += [tuple(W[p[i]] for i in range(n)) for p in perms]
        for s in nxt:
            if s not in seen and legal(cs, s, n):
                seen.add(s); q.append(s)
    return list(seen)


def main():
    rng = random.Random(33333)
    q1_ok = q1_bad = q2_ok = q2_bad = 0
    states = 0
    ex1 = ex2 = None
    print("=== (Q1) legal balanced terminal, (Q2) legal ordering to it ===")
    print("   n   m   inst   states   Q1 fails   Q2 fails")
    for (n, m, T) in [(3, 4, 60), (3, 5, 25), (3, 6, 8),
                      (4, 3, 50), (4, 4, 18), (5, 3, 18)]:
        perms = list(permutations(range(n)))
        f1 = f2 = cnt = st = 0
        for _ in range(T):
            cs = [rand_dicho(m, rng) for _ in range(n)]
            if max(max(c.values()) for c in cs) < 1:
                continue
            cnt += 1
            for W in reachable_legal(cs, n, m, perms):
                if not admits_balanced(W, n, m):
                    continue
                st += 1
                states += 1
                bts = balanced_terminals(W, n, m)
                good = [f for f in bts
                        if legal(cs, state_of(f, n, m), n)]
                if good:
                    q1_ok += 1
                    if any(ordering_exists(cs, W, f, n, m) for f in good):
                        q2_ok += 1
                    else:
                        q2_bad += 1; f2 += 1
                        if ex2 is None:
                            ex2 = (n, m, [sorted(x) for x in W])
                else:
                    q1_bad += 1; f1 += 1
                    if ex1 is None:
                        ex1 = (n, m, [sorted(x) for x in W])
        print("  %2d  %2d  %5d   %6d   %8d   %8d" % (n, m, cnt, st, f1, f2))
    print()
    print("  balance-admitting legal states examined : %d" % states)
    print("  (Q1) has a LEGAL balanced terminal      : %d ok, %d fail"
          % (q1_ok, q1_bad))
    print("  (Q2) legal ordering down to one of them : %d ok, %d fail"
          % (q2_ok, q2_bad))
    print()
    if q1_bad == 0 and q2_bad == 0:
        print("  *** BOTH HOLD.  conj:balance-rule decomposes into two statements,")
        print("      each provable-looking on its own:")
        print("        (Q1) candidate sets rich enough for balance force a legal")
        print("             balanced terminal to exist;")
        print("        (Q2) the peels to it can be scheduled legally. ***")
    else:
        if q1_bad and ex1:
            print("  (Q1) FAILS: n=%d m=%d W=%s" % ex1)
            print("       so balance-admitting does NOT give a legal balanced")
            print("       terminal; liveness must come from elsewhere.")
        if q2_bad and ex2:
            print("  (Q2) FAILS: n=%d m=%d W=%s" % ex2)
            print("       a legal balanced terminal exists but no legal ordering")
            print("       reaches it; the schedule matters, not just the target.")


if __name__ == "__main__":
    main()
