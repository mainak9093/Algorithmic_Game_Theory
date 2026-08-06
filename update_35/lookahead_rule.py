"""The stuck states are all one move from the end.  Does one-step lookahead suffice?

stuck_profile.py characterised all 37 progress-stuck reachable states, and the
characterisation is uniform and sharp:

    exactly ONE peelable chore, with exactly TWO candidate owners,
    max ell = 1, workload size spread 1.

So a stuck state is a state in which every chore but one is committed and NEITHER
resolution of the last one is legal -- both induced allocations have max ell >= 2.
The failure mode is entirely terminal.  Two consequences.

  (1)  Stuck states are CHEAP TO RECOGNISE: after any candidate move, if exactly
       one chore remains peelable, test its two resolutions.  That is O(1)
       legality checks, so the following rule is polynomial:

           LOOKAHEAD RULE.  Among legal balance-preserving peels, never take one
           whose resulting state is stuck.

  (2)  A stuck state is only ever entered from a state with TWO peelable chores,
       so the rule only has to make a correct choice at those.

Tested here:
    (C)  does the characterisation hold on fresh seeds and larger sizes?
    (L)  does the lookahead rule always reach a terminal?
    (L0) does it ever have to reject ALL moves, i.e. is every move stuck-bound?

If (L) holds, the algorithm of prop:balance-rule-implies is complete with a
2-step lookahead, and conj:balance-rule reduces to the single statement that at a
state with two peelable chores some non-stuck-bound legal peel exists.

Run:  python lookahead_rule.py
"""
from itertools import permutations
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_6")
sys.path.insert(0, "../update_32")
sys.path.insert(0, "../update_34")
from targetGbal import rand_dicho                                # noqa: E402
from peel_general import legal, cand, terminal, peels, make      # noqa: E402
from deadend_char import admits_balanced                         # noqa: E402
from reachable_stuck import ok, restricted_reachable             # noqa: E402
from stuck_profile import progress_stuck, ell_vec                # noqa: E402


def peelable(W, n, m):
    S = cand(W, n, m)
    return [j for j in range(m) if len(S[j]) >= 2]


def is_stuck_cheap(cs, W, n, m, perms):
    """Cheap test justified by the characterisation: only 1-peelable states."""
    pk = peelable(W, n, m)
    if len(pk) != 1:
        return False
    return progress_stuck(cs, W, n, m, perms)


def lookahead_run(cs, n, m, perms, cap=400):
    """Greedy under the lookahead rule.  Returns 'ok', 'allstuck', or 'nomove'."""
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
                return "nomove"
        safe = [s for s in opts if not is_stuck_cheap(cs, s, n, m, perms)]
        if not safe:
            return "allstuck"
        W = safe[0]
    return "nomove"


def main():
    rng = random.Random(20260808)          # FRESH seed
    charac_bad = 0
    stuck_seen = 0
    res = Counter()
    print("=== (C) characterisation on a fresh seed, (L) the lookahead rule ===")
    print("   n   m   inst   stuck states   char. violations   rule outcome")
    for (n, m, T) in [(3, 4, 60), (3, 5, 25), (3, 6, 8), (3, 7, 4),
                      (4, 3, 50), (4, 4, 14), (5, 3, 14), (4, 5, 5)]:
        perms = list(permutations(range(n)))
        sc = cv = cnt = 0
        loc = Counter()
        for _ in range(T):
            cs = [rand_dicho(m, rng) for _ in range(n)]
            if max(max(c.values()) for c in cs) < 1:
                continue
            cnt += 1
            R = restricted_reachable(cs, n, m, perms)
            for W in R:
                if terminal(W, n, m):
                    continue
                if progress_stuck(cs, W, n, m, perms):
                    sc += 1
                    stuck_seen += 1
                    S = cand(W, n, m)
                    pk = peelable(W, n, m)
                    e = ell_vec(cs, W, n)
                    if not (len(pk) == 1 and max(len(S[j]) for j in pk) == 2
                            and max(e) == 1):
                        cv += 1
                        charac_bad += 1
            r = lookahead_run(cs, n, m, perms)
            loc[r] += 1
            res[r] += 1
        print("  %2d  %2d  %5d   %12d   %16d   %s"
              % (n, m, cnt, sc, cv, dict(loc)))
    print()
    print("  stuck states seen               : %d" % stuck_seen)
    print("  characterisation violations     : %d" % charac_bad)
    print("  lookahead-rule outcomes         : %s" % dict(res))
    print()
    if charac_bad == 0 and stuck_seen:
        print("  *** (C) holds on the fresh seed: every stuck state has exactly one")
        print("      peelable chore with two owners and max ell = 1. ***")
    if res["allstuck"] == 0 and res["nomove"] == 0:
        print("  *** (L) the LOOKAHEAD RULE is complete on every instance tested.")
        print("      conj:balance-rule then reduces to: at a state with two")
        print("      peelable chores, some legal peel is not stuck-bound. ***")
    else:
        print("  the rule failed: %s" % dict(res))


if __name__ == "__main__":
    main()
