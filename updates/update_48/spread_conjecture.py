"""The candidate fifth theorem: minimum-spread family + maximum-weight matching.

residual_attack.py found that on all 92 residual instances exhibited so far --
the ones no solved case reaches -- the minimum spread over families is exactly 2,
and a minimum-spread family assigned by maximum-weight matching is good.  That
suggests

    (F5)  every instance admits a family of spread <= 2 whose maximum-weight
          matching has ell <= 1.

which would extend thm:balanced-class (the spread <= 1 case, where the bound is
read off cor:onestep) by exactly one unit, and would answer the question
rem:smallbundle-scope leaves open.

BUT the residual is a biased sample: those instances were selected for having no
spread-1 family.  A rule that works on 92 selected instances and fails elsewhere
is the LEXB failure mode again (rem:n3-rules-fail, 227 then 368).  So this
script tests (F5) on EVERYTHING, not on the residual, and separates the two
claims it bundles:

    (A) is the minimum spread always <= 2?
    (B) on a minimum-spread family, is the maximum-weight matching good?

(A) can fail without (B) failing and vice versa, and only their conjunction is
(F5).  Also reported, as the control: whether SOME family and SOME assignment is
good at all, which is Conjecture 2 itself.

Run:  python spread_conjecture.py
"""
from itertools import permutations, product
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_5")
sys.path.insert(0, "../update_17")
sys.path.insert(0, "../update_44")
sys.path.insert(0, "../update_47")
from routeA import partitions, ellvec                            # noqa: E402
from minimum_subsidy import subsets                              # noqa: E402
from counterexample_hunt import FAMILIES                         # noqa: E402
from cri_sweep import is_dichotomous                             # noqa: E402
from residual_map import show_costs                              # noqa: E402
from residual_hunt import cost_family                            # noqa: E402
from residual_attack import spread, matching_good                # noqa: E402


def analyse(cs, n, m):
    """Minimum spread, whether a min-spread family's matching is good, and
    whether the instance is good at all."""
    best = None
    fams = []
    conj2 = False
    for bd in partitions(m, n):
        s = spread(cs, bd, n)
        if best is None or s < best:
            best, fams = s, [bd]
        elif s == best:
            fams.append(bd)
        if not conj2:
            e = ellvec(cs, bd, n)
            if e is not None and max(e) <= 1:
                conj2 = True
    some = any(matching_good(cs, bd, n)[0] for bd in fams)
    return best, some, conj2


def main():
    rng = random.Random(555111)
    print("=== (F5): minimum-spread family + maximum-weight matching ===")
    print()
    print("  (A) min spread <= 2 ?      (B) its matching good ?"
          "      conj2 = control")
    print()
    gens = list(FAMILIES) + [("composed",
                              lambda m, n, r: [cost_family(m)
                                               [r.randrange(len(cost_family(m)))][1]
                                               for _ in range(n)])]
    SP = Counter()
    failA = failB = 0
    failc2 = 0
    tot = 0
    witA = witB = None
    print("  %-10s %-6s %6s   %-22s %8s %8s"
          % ("family", "n,m", "inst", "min-spread distribution",
             "(A) fail", "(B) fail"))
    for (n, m, T) in [(3, 4, 60), (3, 5, 40), (3, 6, 20), (3, 7, 8),
                      (4, 4, 40), (4, 5, 20), (4, 6, 8),
                      (5, 4, 20), (5, 5, 8)]:
        for name, gen in gens:
            loc = Counter()
            la = lb = 0
            cnt = 0
            for _ in range(T):
                cs = gen(m, n, rng)
                if max(max(c.values()) for c in cs) < 1:
                    continue
                assert all(is_dichotomous(c, m) for c in cs), name
                cnt += 1
                tot += 1
                s, some, conj2 = analyse(cs, n, m)
                loc[s] += 1
                SP[s] += 1
                if s > 2:
                    la += 1
                    failA += 1
                    if witA is None:
                        witA = (n, m, name, cs, s)
                if not some:
                    lb += 1
                    failB += 1
                    if witB is None:
                        witB = (n, m, name, cs, s)
                if not conj2:
                    failc2 += 1
                    print("  *** CONJECTURE 2 FAILS: n=%d m=%d %s" % (n, m, name))
            if cnt:
                print("  %-10s %-6s %6d   %-22s %8d %8d"
                      % (name, "%d,%d" % (n, m), cnt,
                         str(dict(sorted(loc.items()))), la, lb))

    print()
    print("  instances                       : %d" % tot)
    print("  minimum-spread distribution     : %s" % dict(sorted(SP.items())))
    print("  (A) instances with min spread > 2      : %d" % failA)
    print("  (B) min-spread family whose matching is not good : %d" % failB)
    print("  Conjecture 2 failures (control) : %d" % failc2)
    print()
    if failA == 0 and failB == 0:
        print("  *** (F5) SURVIVES on every instance tested.  Minimum spread is")
        print("      never more than 2, and a minimum-spread family assigned by")
        print("      maximum-weight matching is always good.  With")
        print("      thm:balanced-class as the spread-1 case, (F5) would close")
        print("      Conjecture 2. ***")
    else:
        if failA:
            n, m, name, cs, s = witA
            print("  (A) FAILS: an instance whose minimum spread is %d." % s)
            print("      n=%d m=%d family=%s" % (n, m, name))
            show_costs(cs, n, m)
            print()
        if failB:
            n, m, name, cs, s = witB
            print("  (B) FAILS: a min-spread family whose maximum-weight")
            print("      matching is not good.  n=%d m=%d family=%s min spread %d"
                  % (n, m, name, s))
            show_costs(cs, n, m)


if __name__ == "__main__":
    main()
