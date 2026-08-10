"""Which spread-2 family works?  The statement (F5) should actually have.

(F5) has been tested only in its existential form -- SOME minimum-spread family
has a good maximum-weight matching -- which held 91/91 and 92/92.  But an
existential over families is not a theorem one can use: thm:balanced-class works
because ANY uniformly balanced family does, with the assignment supplied by a
matching.  So the question that decides the shape of (F5) is:

    over all families of spread <= 2, does the maximum-weight matching give
    ell <= 1 for EVERY one of them, or only for some?

  - EVERY  =>  the clean statement "spread <= 2 + maximum-weight matching is
               good" is the direct one-unit extension of thm:balanced-class, and
               minimality plays no role at all.
  - ONLY SOME => the theorem needs a SELECTION rule on top of the spread bound,
               and the interesting object is what distinguishes the families
               that work.  In that case this script reports what does.

Candidate distinguishing features measured on the families that fail, if any:
  minimality   is the family of minimum spread?
  perfect      does some agent see all bundles equal?
  hitting      how many agents actually attain spread 2 on it
  sizes        are the bundle cardinalities balanced

Only instances of MINIMUM spread exactly 2 are used, since those are the ones
where thm:balanced-class does not already apply.

Run:  python spread_which.py
"""
from itertools import product
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_5")
sys.path.insert(0, "../update_17")
sys.path.insert(0, "../update_47")
from routeA import ellvec                                        # noqa: E402
from cri_sweep import is_dichotomous                             # noqa: E402
from residual_map import show_costs                              # noqa: E402
from residual_attack import matching_good                        # noqa: E402
from spread_hardcore import gen_hardcore, GENS                   # noqa: E402
from spread_scale import spread_of                               # noqa: E402


def all_families(n, m):
    for assign in product(range(n), repeat=m):
        yield [frozenset(g for g in range(m) if assign[g] == i)
               for i in range(n)]


def profile(cs, bd, n):
    """Per-agent spreads, and bundle sizes."""
    sp = [max(cs[i][b] for b in bd) - min(cs[i][b] for b in bd)
          for i in range(n)]
    return sp, sorted(len(b) for b in bd)


def main():
    rng = random.Random(4242424)
    print("=== which spread-2 families have a good maximum-weight matching? ===")
    print()

    inst = []
    tries = 0
    want = 60
    while len(inst) < want and tries < 60000:
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
    print("  instances of minimum spread exactly 2 collected: %d"
          " (from %d draws)" % (len(inst), tries))
    print()

    tot_fam = good_fam = 0
    bad_examples = []
    per_inst_all = 0
    feat = Counter()
    for (n, m, name, cs) in inst:
        allgood = True
        for bd in all_families(n, m):
            if spread_of(cs, bd, n) > 2:
                continue
            tot_fam += 1
            ok_some, ok_all = matching_good(cs, bd, n)
            if ok_some:
                good_fam += 1
            else:
                allgood = False
                sp, sizes = profile(cs, bd, n)
                feat[("agents at spread 2", sum(1 for v in sp if v == 2))] += 1
                feat[("size range", max(sizes) - min(sizes))] += 1
                if len(bad_examples) < 3:
                    bad_examples.append((n, m, name, cs, bd, sp, sizes))
        per_inst_all += allgood

    print("  spread-<=2 families examined            : %d" % tot_fam)
    print("  of them, maximum-weight matching good   : %d (%.2f%%)"
          % (good_fam, 100.0 * good_fam / max(tot_fam, 1)))
    print("  instances where EVERY spread-2 family works : %d / %d"
          % (per_inst_all, len(inst)))
    print()

    if good_fam == tot_fam:
        print("  *** EVERY family of spread <= 2 has a good maximum-weight")
        print("      matching.  So (F5) needs no selection rule and reads")
        print()
        print("        take any family of spread <= 2 and assign it by a")
        print("        maximum-weight matching; the result has ell <= 1,")
        print()
        print("      which is thm:balanced-class with 1 replaced by 2.  That is")
        print("      a clean statement and the right thing to try to prove. ***")
    else:
        print("  *** NOT every spread-2 family works: %d of %d fail."
              % (tot_fam - good_fam, tot_fam))
        print("      So (F5) is NOT simply thm:balanced-class with a 2, and a")
        print("      SELECTION rule is part of the theorem.  Features of the")
        print("      failing families:")
        for k, v in sorted(feat.items(), key=lambda z: str(z[0])):
            print("        %-28s %d" % (str(k), v))
        n, m, name, cs, bd, sp, sizes = bad_examples[0]
        print()
        print("      first failing family: n=%d m=%d gen=%s" % (n, m, name))
        print("        bundles %s   per-agent spread %s   sizes %s"
              % ([sorted(b) for b in bd], sp, sizes))
        show_costs(cs, n, m)


if __name__ == "__main__":
    main()
