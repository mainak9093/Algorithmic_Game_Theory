"""Phase B1: what distinguishes the move INTO a stuck state?

37 progress-stuck states are reachable but always avoided in practice.  Nobody has
asked what the avoiding choice looks like at their predecessors.  Phase A supplies
the natural hypothesis: by the comparability theorem a peel moves S_max along a
chain, so a stuck state should be entered by a particular kind of step.

For every stuck state T in the reachable restricted graph, this script finds its
predecessors -- states W admitting a legal balance-preserving peel to T -- and at
each predecessor compares the BAD move (into T) against the GOOD moves (into
non-stuck states), on features that a rule could read:

    dS       does S_max shrink / stay / grow across the move
    xInSmax  is the peeled agent in S_max(W)
    mu_x     the peeled agent's own marginal
    |Smax|   size of S_max before and after
    peelable how many chores remain peelable after the move

A feature that separates bad from good moves at EVERY predecessor is a candidate
for the invariant Phi.  A feature taking the same value on both is useless.

Run:  python predecessors.py
"""
from itertools import permutations
from collections import Counter, deque
import random
import sys

sys.path.insert(0, "../update_6")
sys.path.insert(0, "../update_32")
sys.path.insert(0, "../update_34")
sys.path.insert(0, "../update_35")
sys.path.insert(0, "../update_36")
from targetGbal import rand_dicho                             # noqa: E402
from peel_general import legal, cand, terminal, peels, make   # noqa: E402
from reachable_stuck import ok, restricted_reachable          # noqa: E402
from stuck_profile import progress_stuck                      # noqa: E402
from potential_set import admissible                          # noqa: E402


def smax(cs, W, n):
    P = admissible(cs, W, n)
    return frozenset.union(*P) if P else None


def feats(cs, W, s, x, n, m):
    A, B = smax(cs, W, n), smax(cs, s, n)
    if A is None or B is None:
        return None
    if A == B:
        dS = "equal"
    elif B < A:
        dS = "shrinks"
    elif A < B:
        dS = "grows"
    else:
        dS = "incomparable"
    S = cand(s, n, m)
    return dict(dS=dS,
                xInSmax=(x in A),
                mu_x=cs[x][W[x]] - cs[x][s[x]],
                dSize=len(B) - len(A),
                peelable=sum(1 for j in range(m) if len(S[j]) >= 2))


def main():
    rng = random.Random(778899)          # seed that produced the 37
    sep = Counter()
    npred = 0
    nstuck = 0
    bad_f = Counter()
    good_f = Counter()
    print("=== predecessors of progress-stuck states ===")
    for (n, m, T) in [(3, 4, 50), (3, 5, 20), (3, 6, 6),
                      (4, 3, 40), (4, 4, 12), (5, 3, 12)]:
        perms = list(permutations(range(n)))
        for _ in range(T):
            cs = [rand_dicho(m, rng) for _ in range(n)]
            if max(max(c.values()) for c in cs) < 1:
                continue
            R = restricted_reachable(cs, n, m, perms)
            stuck = [W for W in R
                     if not terminal(W, n, m) and progress_stuck(cs, W, n, m, perms)]
            if not stuck:
                continue
            nstuck += len(stuck)
            stuckset = set(stuck)
            for W in R:
                if terminal(W, n, m):
                    continue
                moves = [(mv, s) for mv, s in peels(W, n, m) if ok(cs, s, n, m)]
                bad = [(mv, s) for mv, s in moves if s in stuckset]
                good = [(mv, s) for mv, s in moves if s not in stuckset]
                if not bad:
                    continue
                npred += 1
                bf = [feats(cs, W, s, mv[0], n, m) for mv, s in bad]
                gf = [feats(cs, W, s, mv[0], n, m) for mv, s in good]
                bf = [f for f in bf if f]
                gf = [f for f in gf if f]
                for f in bf:
                    bad_f[(f["dS"], f["xInSmax"], f["mu_x"])] += 1
                for f in gf:
                    good_f[(f["dS"], f["xInSmax"], f["mu_x"])] += 1
                # does any single feature separate bad from good here?
                for key in ("dS", "xInSmax", "mu_x", "dSize", "peelable"):
                    bv = {f[key] for f in bf}
                    gv = {f[key] for f in gf}
                    if gf and not (bv & gv):
                        sep[key] += 1
                if not gf:
                    sep["NO GOOD MOVE"] += 1
    print("  stuck states found            : %d" % nstuck)
    print("  predecessors of a stuck state : %d" % npred)
    print()
    print("  feature separates bad from good, per predecessor:")
    for k in ("dS", "xInSmax", "mu_x", "dSize", "peelable", "NO GOOD MOVE"):
        print("     %-14s %d / %d" % (k, sep[k], npred))
    print()
    print("  BAD  moves (dS, x in Smax, mu_x) : %s"
          % dict(sorted(bad_f.items(), key=lambda z: -z[1])[:6]))
    print("  GOOD moves (dS, x in Smax, mu_x) : %s"
          % dict(sorted(good_f.items(), key=lambda z: -z[1])[:6]))
    print()
    full = [k for k in ("dS", "xInSmax", "mu_x", "dSize", "peelable")
            if sep[k] == npred and npred]
    if full:
        print("  *** separates at EVERY predecessor: %s -- candidate for Phi ***"
              % ", ".join(full))
    else:
        print("  no single feature separates at every predecessor;")
        print("  the avoiding choice is not read off any of these.")


if __name__ == "__main__":
    main()
