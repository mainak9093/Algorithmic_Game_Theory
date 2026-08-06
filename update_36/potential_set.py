"""Peel dynamics on the SET of admissible potentials, not on ell alone.

prop:lemmas-insufficient showed that reasoning about p = ell alone cannot carry a
schedule: both safety lemmas are blind at the root, where every arc is 0 and
every arc is therefore tight.  The object that is not blind there is the whole
set of admissible potentials,

    P(W) = { p in {0,1}^n : w_W(i,k) <= p_i - p_k for all i != k },

equivalently, identifying p with S = {i : p_i = 1}, the set of admissible PAID
SETS: S is admissible iff
    w(i,k) <=  0   when i,k lie on the same side of S,
    w(i,k) <=  1   when i in S, k not in S,
    w(i,k) <= -1   when i not in S, k in S.
W is legal iff P(W) is non-empty (lem:potential-form).

Two sanity checks the framework must pass, both known independently:
  - at the root every arc is 0, so the third condition kills every proper S and
    P(root) = {empty, N};
  - after peel(x,j) from the root, S = N \ {x} is admissible iff mu_x >= 1,
    which is prop:first-peel.

The question here is whether P is a usable invariant.  Peeling raises the arcs
INTO x and lowers those out of it, and putting x outside S relaxes exactly the
constraints that got harder -- so the natural greedy is to keep P large.  Tested:

    (R1) max-|P| greedy   : among legal balance-preserving peels take one
                            maximising |P(W')|
    (R2) max-|P| with tie-break on free peels
    (R3) min-|P| greedy   : the control, to check that |P| is doing the work

A rule that always terminates makes "P never empties" the target theorem, and
that is a statement about a set with an explicit description rather than about a
search.

Run:  python potential_set.py
"""
from itertools import permutations
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_6")
sys.path.insert(0, "../update_32")
sys.path.insert(0, "../update_34")
from targetGbal import rand_dicho                               # noqa: E402
from peel_general import legal, cand, terminal, peels, make     # noqa: E402
from reachable_stuck import ok                                  # noqa: E402


def arcs(cs, W, n):
    return [[cs[i][W[i]] - cs[i][W[k]] for k in range(n)] for i in range(n)]


def admissible(cs, W, n):
    """All admissible paid sets S, as frozensets."""
    A = arcs(cs, W, n)
    out = []
    for bits in range(1 << n):
        S = frozenset(i for i in range(n) if bits >> i & 1)
        good = True
        for i in range(n):
            for k in range(n):
                if i == k:
                    continue
                if (i in S) == (k in S):
                    lim = 0
                elif i in S:
                    lim = 1
                else:
                    lim = -1
                if A[i][k] > lim:
                    good = False
                    break
            if not good:
                break
        if good:
            out.append(S)
    return out


def run(cs, n, m, perms, mode, cap=400):
    W = tuple([make(m)] * n)
    for _ in range(cap):
        if terminal(W, n, m):
            return "ok"
        opts = [s for _, s in peels(W, n, m) if ok(cs, s, n, m)]
        if not opts:
            moved = False
            for p in perms:
                V = tuple(W[p[i]] for i in range(n))
                if not ok(cs, V, n, m):
                    continue
                o2 = [s for _, s in peels(V, n, m) if ok(cs, s, n, m)]
                if o2:
                    W = V; opts = o2; moved = True; break
            if not moved:
                return "stuck"
        key = (lambda s: len(admissible(cs, s, n)))
        if mode == "min":
            W = min(opts, key=key)
        else:
            W = max(opts, key=key)
    return "cap"


def main():
    rng = random.Random(36363636)
    res = {r: Counter() for r in ("R1", "R3")}
    psize = Counter()
    root_ok = 0
    inst = 0
    print("=== peel dynamics on the admissible-potential set ===")
    print("   n   m   inst   max-|P| greedy      min-|P| control")
    for (n, m, T) in [(3, 4, 50), (3, 5, 25), (3, 6, 10), (3, 7, 5),
                      (4, 3, 40), (4, 4, 14), (4, 5, 6), (5, 3, 14), (5, 4, 5)]:
        perms = list(permutations(range(n)))
        loc = {r: Counter() for r in ("R1", "R3")}
        cnt = 0
        for _ in range(T):
            cs = [rand_dicho(m, rng) for _ in range(n)]
            if max(max(c.values()) for c in cs) < 1:
                continue
            cnt += 1
            inst += 1
            root = tuple([make(m)] * n)
            P0 = admissible(cs, root, n)
            psize[len(P0)] += 1
            if set(P0) == {frozenset(), frozenset(range(n))}:
                root_ok += 1
            a = run(cs, n, m, perms, "max"); loc["R1"][a] += 1; res["R1"][a] += 1
            b = run(cs, n, m, perms, "min"); loc["R3"][b] += 1; res["R3"][b] += 1
        print("  %2d  %2d  %5d   %-18s %s"
              % (n, m, cnt, dict(loc["R1"]), dict(loc["R3"])))
    print()
    print("  instances                          : %d" % inst)
    print("  P(root) = {empty, N} as predicted  : %d / %d" % (root_ok, inst))
    print("  |P(root)| distribution             : %s" % dict(sorted(psize.items())))
    print()
    print("  (R1) max-|P| greedy : %s" % dict(res["R1"]))
    print("  (R3) min-|P| control: %s" % dict(res["R3"]))
    print()
    if res["R1"]["stuck"] == 0 and res["R1"]["cap"] == 0:
        print("  *** max-|P| greedy terminates on every instance.  The target")
        print("      theorem becomes: under this rule P never empties -- a claim")
        print("      about an explicitly described set, not about a search. ***")
    else:
        print("  max-|P| greedy fails on %d instances" % (res["R1"]["stuck"]
                                                          + res["R1"]["cap"]))


if __name__ == "__main__":
    main()
