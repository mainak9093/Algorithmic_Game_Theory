"""Stress the min-total-spread rule before believing it.

spread_rule.py produced a candidate with no false positives:

    (F5*)  let B minimise  sum_i [ max_t c_i(B_t) - min_t c_i(B_t) ]
           over all families; assign B by a maximum-weight matching.
           Then ell <= 1.

It is constructive, it always applies (a minimiser exists by definition), and on
the sample it was tested against, EVERY minimiser worked -- 4,770 families, 0
failures, and 6,666 for the sibling rule minimising the NUMBER of agents at
spread 2.  It also explains why thm:balanced-class works, since a uniformly
balanced family has small total spread.

That is exactly the profile of a rule this project has been burned by twice.
LEXB was perfect on 227 residual instances and died on 368
(rem:n3-rules-fail).  conj:balance-rule survived 305 instances from one uniform
sampler and its certificate then failed outright in the CR frame.  And
spread_rule.py's sample was doubly selected: only instances of MINIMUM spread 2,
only n <= 4, only m <= 6.

So before (F5*) is written down as promising it is tested where it was not:

  - on ALL instances, not only the minimum-spread-2 ones.  The rule is defined
    everywhere, so it must hold everywhere;
  - at larger n and m;
  - on every generator, including the composed family where the residual lives;
  - in its strong form -- EVERY minimiser works -- since a rule that needs the
    right minimiser is not constructive.

Both siblings are tracked, and so is the control: whether the instance has a
good allocation at all.

Run:  python minsum_stress.py
"""
from itertools import product
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_5")
sys.path.insert(0, "../update_17")
sys.path.insert(0, "../update_44")
sys.path.insert(0, "../update_47")
from routeA import ellvec                                        # noqa: E402
from counterexample_hunt import FAMILIES                         # noqa: E402
from cri_sweep import is_dichotomous                             # noqa: E402
from residual_map import show_costs                              # noqa: E402
from residual_attack import matching_good                        # noqa: E402
from spread_hardcore import GENS as HARD                         # noqa: E402


def analyse(cs, n, m):
    """Minimisers of total spread and of binding count; are they all good?"""
    best_sum = None
    best_bind = None
    rows = []
    for assign in product(range(n), repeat=m):
        bd = [frozenset(g for g in range(m) if assign[g] == i)
              for i in range(n)]
        sp = [max(cs[i][b] for b in bd) - min(cs[i][b] for b in bd)
              for i in range(n)]
        ssum = sum(sp)
        mx = max(sp)
        bind = sum(1 for v in sp if v == mx) if mx else 0
        rows.append((bd, ssum, mx, bind))
        if best_sum is None or ssum < best_sum:
            best_sum = ssum
        key = (mx, bind)
        if best_bind is None or key < best_bind:
            best_bind = key

    sum_all = sum_any = True
    bind_all = bind_any = True
    sum_bad = bind_bad = None
    got_sum = got_bind = False
    for bd, ssum, mx, bind in rows:
        if ssum == best_sum:
            ok = matching_good(cs, bd, n)[0]
            got_sum = True
            if not ok:
                sum_all = False
                if sum_bad is None:
                    sum_bad = bd
        if (mx, bind) == best_bind:
            ok = matching_good(cs, bd, n)[0]
            got_bind = True
            if not ok:
                bind_all = False
                if bind_bad is None:
                    bind_bad = bd
    # "any" forms
    sum_any = any(matching_good(cs, bd, n)[0]
                  for bd, ssum, mx, bind in rows if ssum == best_sum)
    bind_any = any(matching_good(cs, bd, n)[0]
                   for bd, ssum, mx, bind in rows if (mx, bind) == best_bind)
    conj2 = any(ellvec(cs, bd, n) is not None
                and max(ellvec(cs, bd, n)) <= 1 for bd, _, _, _ in rows)
    return dict(sum_all=sum_all, sum_any=sum_any, bind_all=bind_all,
                bind_any=bind_any, conj2=conj2, sum_bad=sum_bad,
                bind_bad=bind_bad, best_sum=best_sum)


def main():
    rng = random.Random(31415926)
    gens = list(FAMILIES) + list(HARD)
    print("=== stressing (F5*): minimise total spread, then match ===")
    print()
    print("  %-10s %-6s %6s %9s %9s %9s %9s"
          % ("gen", "n,m", "inst", "minsum-ALL", "minsum-ANY",
             "minbind-ALL", "conj2"))
    tot = 0
    F = Counter()
    wit = {}
    for (n, m, T) in [(3, 5, 60), (3, 6, 40), (3, 7, 20), (3, 8, 10),
                      (4, 5, 40), (4, 6, 20), (4, 7, 8),
                      (5, 5, 20), (5, 6, 8), (6, 5, 8)]:
        for name, gen in gens:
            cnt = Counter()
            c = 0
            for _ in range(T):
                cs = gen(m, n, rng)
                if max(max(c2.values()) for c2 in cs) < 1:
                    continue
                if not all(is_dichotomous(c2, m) for c2 in cs):
                    continue
                c += 1
                tot += 1
                r = analyse(cs, n, m)
                for k in ("sum_all", "sum_any", "bind_all", "conj2"):
                    if not r[k]:
                        cnt[k] += 1
                        F[k] += 1
                        if k not in wit:
                            wit[k] = (n, m, name, cs, r)
            if c:
                print("  %-10s %-6s %6d %9d %9d %9d %9d"
                      % (name, "%d,%d" % (n, m), c, cnt["sum_all"],
                         cnt["sum_any"], cnt["bind_all"], cnt["conj2"]))

    print()
    print("  instances                              : %d" % tot)
    print("  minsum, EVERY minimiser good  -- failures : %d" % F["sum_all"])
    print("  minsum, SOME minimiser good   -- failures : %d" % F["sum_any"])
    print("  minbind, EVERY minimiser good -- failures : %d" % F["bind_all"])
    print("  Conjecture 2 (control)        -- failures : %d" % F["conj2"])
    print()

    if F["conj2"]:
        n, m, name, cs, r = wit["conj2"]
        print("  *** CONJECTURE 2 FAILS: n=%d m=%d gen=%s ***" % (n, m, name))
        show_costs(cs, n, m)
        return

    if F["sum_all"] == 0:
        print("  *** (F5*) SURVIVES in its STRONG form: every minimiser of the")
        print("      total spread has a good maximum-weight matching, over %d"
              % tot)
        print("      instances at n up to 6 and m up to 8, on all %d"
              % len(gens))
        print("      generators.  It is constructive and always applies. ***")
    elif F["sum_any"] == 0:
        n, m, name, cs, r = wit["sum_all"]
        print("  *** (F5*) FAILS in its strong form (%d instances) but survives"
              % F["sum_all"])
        print("      in the weak one: SOME minimiser always works.  So the rule")
        print("      needs a tie-break among minimisers and is not yet")
        print("      constructive.  First witness n=%d m=%d gen=%s:"
              % (n, m, name))
        show_costs(cs, n, m)
        print("      failing minimiser: %s"
              % [sorted(b) for b in r["sum_bad"]])
    else:
        n, m, name, cs, r = wit["sum_any"]
        print("  *** (F5*) IS REFUTED: on %d instances NO minimiser of the total"
              % F["sum_any"])
        print("      spread has a good maximum-weight matching, so minimising")
        print("      total spread is the wrong rule.  Same failure mode as LEXB")
        print("      and the balance rule.  First witness n=%d m=%d gen=%s:"
              % (n, m, name))
        show_costs(cs, n, m)
        print("      Conjecture 2 still holds on it: %s" % r["conj2"])


if __name__ == "__main__":
    main()
