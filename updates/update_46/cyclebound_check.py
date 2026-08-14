"""Rechecking the cycle-closing bound (Theorem 33 of the working draft).

    thm:cyclebound.  For any envy-freeable allocation A and any agent u,
        ell_A(u) <= max( 0, max_{v != u} [ c_v(A_u) - c_v(A_v) ] ).

The STATEMENT is what is being checked here.  Its proof in the working draft is
under-argued and is being rewritten separately; three gaps:

  (1) ell_A(u) is the MAXIMUM over paths from u, and the proof bounds one path
      without taking the maximum or arguing it is attained;
  (2) it assumes the path ends at some v != u, though a walk from u may return
      to u;
  (3) "appending (v,u) closes a directed cycle" holds for a SIMPLE path; for a
      walk it closes a closed walk, and thm:hs-characterisation(iii) forbids
      positive CYCLES, not closed walks.

The corrected proof takes P* to be a maximum-weight SIMPLE path (legitimate
because with no positive cycle every walk is dominated by a simple path, and
there are finitely many), notes a simple path from u cannot revisit u so its
terminal v differs from u, and closes it into a genuine simple cycle.

Two things are measured, both against the project's real longest-path routine
(minimum_subsidy.total_subsidy) rather than a re-implementation:

  (A) the inequality itself, over every allocation of every instance;
  (B) the SLACK, right-hand side minus ell_A(u).  The bound discards everything
      about the path but its endpoint, so it should be strictly lossy -- if the
      slack were always 0 the two quantities would be equivalent, which they are
      not.

Run:  python cyclebound_check.py
"""
from itertools import product
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_17")
sys.path.insert(0, "../update_44")
from minimum_subsidy import total_subsidy                       # noqa: E402
from counterexample_hunt import (f_uniform, f_nested, f_capped,  # noqa: E402
                                 f_threshold, f_disjoint, f_mixed)


def main():
    rng = random.Random(46464646)
    gens = [f_uniform, f_nested, f_capped, f_threshold, f_disjoint, f_mixed]
    viol = 0
    checks = 0
    slack = Counter()
    tight_only = 0
    insts = 0
    print("=== thm:cyclebound, checked against the true longest-path value ===")
    print("   n   m   inst   (u, allocation) pairs   violations")
    for (n, m, T) in [(3, 4, 200), (3, 5, 90), (3, 6, 30),
                      (4, 3, 150), (4, 4, 60), (4, 5, 20),
                      (5, 3, 60), (5, 4, 15)]:
        loc = 0
        locv = 0
        cnt = 0
        for _ in range(T):
            cs = gens[rng.randrange(len(gens))](m, n, rng)
            if max(max(c.values()) for c in cs) < 1:
                continue
            cnt += 1
            insts += 1
            for assign in product(range(n), repeat=m):
                bd = [frozenset(g for g in range(m) if assign[g] == i)
                      for i in range(n)]
                a = [[cs[i][bd[j]] for j in range(n)] for i in range(n)]
                t, e = total_subsidy(a, n)
                if t is None:          # not envy-freeable; theorem does not apply
                    continue
                for u in range(n):
                    # right-hand side: max(0, max_{v != u} [ c_v(A_u) - c_v(A_v) ])
                    rhs = max([0] + [a[v][u] - a[v][v]
                                     for v in range(n) if v != u])
                    checks += 1
                    loc += 1
                    if e[u] > rhs:
                        viol += 1
                        locv += 1
                    slack[rhs - e[u]] += 1
        print("  %2d  %2d  %5d   %21d   %10d" % (n, m, cnt, loc, locv))
    print()
    print("  instances                       : %d" % insts)
    print("  (agent, allocation) pairs tested: %d" % checks)
    print("  VIOLATIONS of the bound         : %d" % viol)
    print()
    print("  slack distribution (rhs - ell)  : %s"
          % dict(sorted(slack.items())[:10]))
    exact = slack[0]
    print("  bound exact (slack 0)           : %d of %d  (%.1f%%)"
          % (exact, checks, 100.0 * exact / max(checks, 1)))
    print("  maximum slack observed          : %d" % max(slack))
    print()
    if viol == 0:
        print("  *** the statement holds. ***")
    else:
        print("  *** THE STATEMENT IS FALSE: %d violations. ***" % viol)
    if exact < checks:
        print("  *** and the bound is NOT equivalent to ell_A: it is strictly")
        print("      lossy on %d of %d pairs, so it over-estimates the maximum"
              % (checks - exact, checks))
        print("      path weight and must not be read as computing it. ***")


if __name__ == "__main__":
    main()
