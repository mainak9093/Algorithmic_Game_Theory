"""What selects the spread-2 families that work?

spread_which.py settled the shape of (F5) and the answer was unwelcome.  On
instances of MINIMUM spread 2, every family of spread <= 2 is a minimum-spread
family, and only 85.8% of them have a good maximum-weight matching -- 6,063 of
42,711 fail.  So:

  - (F5) is NOT thm:balanced-class with 1 replaced by 2.  There, ANY uniformly
    balanced family works and the matching supplies the assignment.  Here most
    families work and some do not.
  - minimality of the spread is NOT the selector, since every family in that
    experiment was already minimum-spread.

So (F5) is currently a bare EXISTENCE claim with no construction, which is much
weaker than thm:balanced-class and not yet a usable theorem.  This script looks
for the missing predicate.

The failing families looked degenerate -- the first had bundle sizes (0,1,3) and
all three agents at spread 2 -- so the candidates are about balance and about how
many agents the spread bound actually binds on.  Each is tested as a two-way
contingency against "the maximum-weight matching is good":

  nonempty     every bundle is nonempty
  balanced     bundle sizes differ by at most 1        <- the rem:balance signal
  bal+ne       both of the above
  fewbind      at most one agent attains spread 2
  minbind      the family minimises the number of agents attaining spread 2
  minsum       the family minimises the sum of the per-agent spreads

A predicate with NO false positives -- P and yet not good never happens -- is a
sufficient condition, which is what a theorem needs.  Its coverage then says
whether it is also non-vacuous, and whether at least one such family exists on
every instance.

Run:  python spread_rule.py
"""
from itertools import product
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_5")
sys.path.insert(0, "../update_17")
sys.path.insert(0, "../update_47")
from cri_sweep import is_dichotomous                             # noqa: E402
from residual_map import show_costs                              # noqa: E402
from residual_attack import matching_good                        # noqa: E402
from spread_hardcore import GENS                                 # noqa: E402
from spread_scale import spread_of                               # noqa: E402
from spread_which import all_families                            # noqa: E402


def collect(rng, want=70, cap=90000):
    inst = []
    tries = 0
    while len(inst) < want and tries < cap:
        tries += 1
        n = rng.choice([3, 3, 4])
        m = rng.choice([4, 5, 5, 6])
        name, gen = GENS[rng.randrange(len(GENS))]
        cs = gen(m, n, rng)
        if max(max(c.values()) for c in cs) < 1:
            continue
        if not all(is_dichotomous(c, m) for c in cs):
            continue
        best = None
        for bd in all_families(n, m):
            s = spread_of(cs, bd, n)
            if best is None or s < best:
                best = s
                if best <= 1:
                    break
        if best == 2:
            inst.append((n, m, name, cs))
    return inst, tries


def features(cs, bd, n):
    sp = [max(cs[i][b] for b in bd) - min(cs[i][b] for b in bd)
          for i in range(n)]
    sizes = [len(b) for b in bd]
    return {
        "bind": sum(1 for v in sp if v == 2),
        "sumsp": sum(sp),
        "nonempty": min(sizes) >= 1,
        "balanced": max(sizes) - min(sizes) <= 1,
    }


def main():
    rng = random.Random(77007700)
    print("=== what selects a working spread-2 family? ===")
    print()
    inst, tries = collect(rng)
    print("  min-spread-2 instances: %d (from %d draws)" % (len(inst), tries))
    print()

    PRED = ["nonempty", "balanced", "bal+ne", "fewbind", "minbind", "minsum"]
    cont = {p: Counter() for p in PRED}
    exists = Counter()
    firstbad = {}

    for (n, m, name, cs) in inst:
        rows = []
        for bd in all_families(n, m):
            if spread_of(cs, bd, n) > 2:
                continue
            f = features(cs, bd, n)
            f["good"] = matching_good(cs, bd, n)[0]
            rows.append((bd, f))
        if not rows:
            continue
        minbind = min(r[1]["bind"] for r in rows)
        minsum = min(r[1]["sumsp"] for r in rows)
        have = Counter()
        for bd, f in rows:
            p = {
                "nonempty": f["nonempty"],
                "balanced": f["balanced"],
                "bal+ne": f["balanced"] and f["nonempty"],
                "fewbind": f["bind"] <= 1,
                "minbind": f["bind"] == minbind,
                "minsum": f["sumsp"] == minsum,
            }
            for k in PRED:
                cont[k][(p[k], f["good"])] += 1
                if p[k]:
                    have[k] += 1
                if p[k] and not f["good"] and k not in firstbad:
                    firstbad[k] = (n, m, name, cs, bd, f)
        for k in PRED:
            if have[k]:
                exists[k] += 1

    print("  %-9s %8s %8s %8s %8s   %-9s %s"
          % ("predicate", "P&good", "P&bad", "~P&good", "~P&bad",
             "sufficient", "instances with such a family"))
    winners = []
    for k in PRED:
        c = cont[k]
        suff = c[(True, False)] == 0
        if suff and c[(True, True)]:
            winners.append(k)
        print("  %-9s %8d %8d %8d %8d   %-9s %d / %d"
              % (k, c[(True, True)], c[(True, False)], c[(False, True)],
                 c[(False, False)], "YES" if suff else "no", exists[k],
                 len(inst)))

    print()
    if winners:
        for k in winners:
            print("  *** '%s' is SUFFICIENT: no family satisfying it ever has a"
                  % k)
            print("      bad maximum-weight matching, over %d families."
                  % cont[k][(True, True)])
            if exists[k] == len(inst):
                print("      And such a family exists on every one of the %d"
                      % len(inst))
                print("      instances, so (F5) becomes a CONSTRUCTIVE claim:")
                print("        take a spread-<=2 family that is also '%s'," % k)
                print("        assign it by a maximum-weight matching.")
                print("      That is the statement to try to prove. ***")
            else:
                print("      But such a family exists on only %d of %d"
                      " instances," % (exists[k], len(inst)))
                print("      so it is sufficient and NOT always available. ***")
    else:
        print("  *** No candidate predicate is sufficient.  Each admits a")
        print("      family that satisfies it and still fails, so none of")
        print("      balance, nonemptiness or minimal binding is the rule. ***")
        for k in PRED:
            if k in firstbad:
                n, m, name, cs, bd, f = firstbad[k]
                print()
                print("      '%s' counterexample: n=%d m=%d gen=%s" % (k, n, m, name))
                print("        bundles %s  features %s"
                      % ([sorted(b) for b in bd],
                         {a: f[a] for a in ("bind", "sumsp", "nonempty",
                                            "balanced")}))
                show_costs(cs, n, m)
                break


if __name__ == "__main__":
    main()
