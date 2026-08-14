"""Comparability of S_max across a peel: verification of the proof's case split.

obs:smax-comparable recorded that S_max(W) and S_max(W') were never incomparable.
That is now a THEOREM; this script is confirmatory only, checking the proof's
structure rather than the bare conclusion.

THE PROOF.  Let W be legal and W' = peel(x,j)(W) legal.
  * mu_x = 0: prop:smax-monotone-mu0 gives S_max(W') subset S_max(W).
  * mu_x = 1: lem:smax-mono-mu1 gives S_max(W) \\ {x} subset S_max(W').
      - x in S_max(W')                      => S_max(W) subset S_max(W')
      - x not in S_max(W'), x not in S_max(W) => same containment
      - x not in S_max(W'), x in S_max(W)   => CRITICAL CASE, claim
                                               S_max(W') = S_max(W) \\ {x}

  Critical case.  Suppose k not in S_max(W) but k in S_max(W'); note k != x.  By
  prop:smax-closed-form there is a simple path Q ending at k with w_W(Q) >= 1 and
  w_W'(Q) <= 0.  Only arcs at x changed, so Q meets x, once.  Splitting
  Q = Q1.Q2 at x gives w_W'(Q) = w_W(Q) + mu_{i'} - mu_x, forcing mu_{i'} = 0 and
  w_W(Q) = 1.  Since x in S_max(W), w_W(Q1) <= 0, so w_W(Q2) >= 1 and
  w_W'(Q2) = w_W(Q2) - 1 >= 0.  Since x not in S_max(W') there is P ending at x
  with w_W'(P) >= 1.  Then w_W'(P.Q2) >= 1; with no positive cycle in W' the
  heaviest walk equals the heaviest simple path, so ellstar_W'(k) >= 1,
  contradicting k in S_max(W').

CHECKED HERE, per peel:
  (C1) S_max(W) and S_max(W') comparable                     -- the conclusion
  (C2) mu_x = 0  =>  S_max(W') subset S_max(W)               -- the easy branch
  (C3) mu_x = 1  =>  S_max(W) \\ {x} subset S_max(W')         -- lem:smax-mono-mu1
  (C4) critical case => S_max(W') == S_max(W) \\ {x} exactly  -- the claim proved
and how often the critical case actually arises, since a case that never fires
would make the theorem vacuous where it matters.

Run:  python comparability.py
"""
from itertools import permutations
from collections import Counter, deque
import random
import sys

sys.path.insert(0, "../update_6")
sys.path.insert(0, "../update_32")
sys.path.insert(0, "../update_34")
sys.path.insert(0, "../update_36")
from targetGbal import rand_dicho                             # noqa: E402
from peel_general import legal, terminal, peels, make         # noqa: E402
from reachable_stuck import ok                                # noqa: E402
from potential_set import admissible                          # noqa: E402


def smax(cs, W, n):
    P = admissible(cs, W, n)
    return frozenset.union(*P) if P else None


def main():
    rng = random.Random(41414141)
    bad = Counter()
    cnt = Counter()
    print("=== comparability of S_max: the proof's case split ===")
    print("   n   m   peels     C1   C2   C3   C4   critical cases")
    for (n, m, T) in [(3, 4, 40), (3, 5, 18), (3, 6, 6), (3, 7, 3),
                      (4, 3, 30), (4, 4, 12), (4, 5, 4),
                      (5, 3, 12), (5, 4, 4), (6, 3, 6)]:
        perms = list(permutations(range(n)))
        loc = Counter()
        for _ in range(T):
            cs = [rand_dicho(m, rng) for _ in range(n)]
            if max(max(c.values()) for c in cs) < 1:
                continue
            root = tuple([make(m)] * n)
            seen = {root}
            q = deque([root])
            while q and len(seen) < 2500:
                W = q.popleft()
                A = smax(cs, W, n)
                if A is not None and not terminal(W, n, m):
                    for mv, s in peels(W, n, m):
                        x, j = mv
                        B = smax(cs, s, n)
                        if B is None:
                            continue
                        mu_x = cs[x][W[x]] - cs[x][s[x]]
                        cnt["peels"] += 1
                        loc["peels"] += 1
                        # (C1) conclusion
                        if not (A <= B or B <= A):
                            bad["C1"] += 1
                        # (C2) easy branch
                        if mu_x == 0 and not B <= A:
                            bad["C2"] += 1
                        # (C3) lem:smax-mono-mu1
                        if mu_x == 1 and not (A - {x}) <= B:
                            bad["C3"] += 1
                        # (C4) the critical case
                        if mu_x == 1 and x in A and x not in B:
                            cnt["critical"] += 1
                            loc["critical"] += 1
                            if B != (A - {x}):
                                bad["C4"] += 1
                for t in ([t for _, t in peels(W, n, m)]
                          + [tuple(W[p[i]] for i in range(n)) for p in perms]):
                    if t not in seen and ok(cs, t, n, m):
                        seen.add(t)
                        q.append(t)
        print("  %2d  %2d  %7d   %4d %4d %4d %4d   %d"
              % (n, m, loc["peels"], bad["C1"], bad["C2"], bad["C3"], bad["C4"],
                 loc["critical"]))
    print()
    print("  peels examined                : %d" % cnt["peels"])
    print("  critical cases encountered    : %d" % cnt["critical"])
    print()
    print("  (C1) S_max comparable                       : %d violations" % bad["C1"])
    print("  (C2) mu_x=0 => S_max(W') subset S_max(W)    : %d violations" % bad["C2"])
    print("  (C3) mu_x=1 => S_max(W)\\{x} subset S_max(W'): %d violations" % bad["C3"])
    print("  (C4) critical => S_max(W') = S_max(W)\\{x}   : %d violations" % bad["C4"])
    print()
    if not any(bad.values()):
        if cnt["critical"] == 0:
            print("  WARNING: the critical case never arose, so (C4) is untested.")
        else:
            print("  *** every step of the proof holds, and the critical case")
            print("      arises %d times -- the theorem is not vacuous there. ***"
                  % cnt["critical"])
    else:
        print("  *** VIOLATIONS FOUND: %s -- the proof is wrong somewhere. ***"
              % dict(bad))


if __name__ == "__main__":
    main()
