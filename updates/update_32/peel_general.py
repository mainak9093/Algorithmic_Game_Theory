"""Peel reachability beyond n = m = 3, and the search for a peel RULE.

peel_sweep.py settled conj:h1prime on the full exhaustive n = m = 3 family: 0 bad
roots in 9,880 instances.  Two things follow directly.

(1) DOES IT SURVIVE LARGER SIZES?  The state space is (2^m)^n, so exhaustive
    reachability is still feasible a little way out.  A single bad root anywhere
    refutes conj:h1prime and kills Approach 3.

(2) IS THERE A RULE?  sec:h1prime says what is missing is "a peel rule that
    provably never enters a deadlock", and prop:deadends shows the state space
    genuinely has dead ends -- legal states from which no legal terminal is
    reachable.  Reachability from the ROOT holding does not mean a greedy peeler
    is safe: it may walk into a dead end.  Measured here:
      - the fraction of reachable legal states that are dead ends;
      - whether named greedy rules reach a terminal without backtracking.

Rules tested (each picks one legal peel(x,j) from the current state):
    R-maxell   x attains max ell; j arbitrary among legal
    R-bigS     j with the largest owner-candidate set |S_j|
    R-mincost  x maximising c_x(W_x); the most burdened residual workload
    R-any      any legal peel (worst case over the search: does SOME greedy
               choice always work, i.e. are dead ends avoidable at all)
A rule that never deadlocks over the sweep is a candidate for the missing
ingredient.

Run:  python peel_general.py
"""
from itertools import permutations, product
from collections import Counter, deque
import random
import sys

sys.path.insert(0, "../update_6")
from targetGbal import rand_dicho                      # noqa: E402


def make(m):
    return frozenset(range(m))


def ell(cs, W, n):
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


def legal(cs, W, n):
    e = ell(cs, W, n)
    return e is not None and max(e) <= 1


def cand(W, n, m):
    return [frozenset(i for i in range(n) if j in W[i]) for j in range(m)]


def terminal(W, n, m):
    return all(len(s) == 1 for s in cand(W, n, m))


def peels(W, n, m):
    S = cand(W, n, m)
    out = []
    for x in range(n):
        for j in W[x]:
            if len(S[j]) >= 2:
                nw = list(W)
                nw[x] = W[x] - {j}
                out.append(((x, j), tuple(nw)))
    return out


def explore(cs, n, m, perms):
    """Full reachability from the root.  Returns (reached, live set, dead ends)."""
    root = tuple([make(m)] * n)
    if not legal(cs, root, n):
        return False, set(), 0
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
    # which legal states can still reach a terminal
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
    dead = len(seen) - len(good)
    return (root in good), seen, dead


def greedy(cs, n, m, rule, perms, cap=200):
    """Follow a named rule from the root; True if it reaches a terminal."""
    W = tuple([make(m)] * n)
    for _ in range(cap):
        if terminal(W, n, m):
            return True
        opts = [(mv, s) for mv, s in peels(W, n, m) if legal(cs, s, n)]
        if not opts:
            return False
        if rule == "R-maxell":
            e = ell(cs, W, n)
            mx = max(e)
            pref = [o for o in opts if e[o[0][0]] == mx]
            opts = pref or opts
        elif rule == "R-bigS":
            S = cand(W, n, m)
            best = max(len(S[mv[1]]) for mv, _ in opts)
            opts = [o for o in opts if len(S[o[0][1]]) == best]
        elif rule == "R-mincost":
            best = max(cs[mv[0]][W[mv[0]]] for mv, _ in opts)
            opts = [o for o in opts if cs[o[0][0]][W[o[0][0]]] == best]
        W = opts[0][1]
    return False


def main():
    rng = random.Random(32323232)
    RULES = ["R-maxell", "R-bigS", "R-mincost"]
    print("=== peel reachability and greedy rules beyond n=m=3 ===")
    print("   n   m   inst   bad roots   dead-end states   " + "  ".join(RULES))
    grand_bad = 0
    grand_dead = 0
    rulefail = Counter()
    tot = 0
    for (n, m, T) in [(3, 4, 120), (3, 5, 60), (3, 6, 20),
                      (4, 3, 100), (4, 4, 40), (5, 3, 40), (5, 4, 12)]:
        perms = list(permutations(range(n)))
        bad = dead = cnt = 0
        rf = Counter()
        for _ in range(T):
            cs = [rand_dicho(m, rng) for _ in range(n)]
            if max(max(c.values()) for c in cs) < 1:
                continue
            cnt += 1
            tot += 1
            ok, seen, d = explore(cs, n, m, perms)
            if not ok:
                bad += 1
                grand_bad += 1
            dead += d
            grand_dead += d
            for r in RULES:
                if not greedy(cs, n, m, r, perms):
                    rf[r] += 1
                    rulefail[r] += 1
        print("  %2d  %2d  %5d   %9d   %15d   %s"
              % (n, m, cnt, bad, dead,
                 "  ".join("%9d" % rf[r] for r in RULES)))
    print()
    print("  instances                      : %d" % tot)
    print("  BAD ROOTS (refute conj:h1prime): %d" % grand_bad)
    print("  dead-end legal states total    : %d" % grand_dead)
    print("  greedy rule failures           : %s" % dict(rulefail))
    print()
    if grand_bad == 0:
        print("  *** conj:h1prime survives every size tested. ***")
    else:
        print("  *** conj:h1prime REFUTED at these sizes. ***")
    surv = [r for r in RULES if rulefail[r] == 0]
    if surv:
        print("  *** rules that never deadlocked: %s" % ", ".join(surv))
        print("      a deadlock-free peel rule is exactly what sec:h1prime says")
        print("      is missing. ***")
    else:
        print("  every named greedy rule deadlocks somewhere: reachability holds")
        print("  but is not achieved by any of these local rules.")


if __name__ == "__main__":
    main()
