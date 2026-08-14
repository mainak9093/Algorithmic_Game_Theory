"""A targeted hunt for a RESIDUAL instance: one no solved case covers.

residual_map.py found the residual empty over 550 random instances, because S4
(a uniformly balanced family, thm:balanced-class) covered every single one.  The
only known instance without a uniformly balanced family is prop:no-balance's,
and that one is binary additive, hence inside S1.  Random search will not find a
residual instance, so this script constructs one.

THE IDEA.  Why is uniform balance so easy to satisfy, and why is prop:no-balance
additive?  Because for an ADDITIVE cost the total over any partition is fixed,

    sum_t c_i(B_t) = c_i(M),

so "every bundle within one unit" pins each bundle to c_i(M)/n exactly -- a rigid
discrepancy constraint with no slack.  For a non-additive cost the total varies
with the partition: supermodular costs get cheaper when split (so all bundles can
be made cheap, hence balanced), and submodular ones get dearer (so all bundles
can be made to cost the same nonzero amount).  Either way there is slack.
**Additivity is exactly what makes uniform balance hard**, which is why the one
known witness is additive -- and why it is already solved.

So a residual instance needs a cost function that keeps additivity's rigid
balance constraint while not being additive.  Capping does it: for
D = {g2,g3,g4} spread over three bundles, both |S & D| and min(|S & D|, 2) force
the pattern (1,1,1), but the second has a zero marginal and is not additive.

THE SEARCH SPACE.  Composed costs

    c_i(S) = f_i(|S & D_i|),        D_i subset of M,  f_i increments in {0,1},

which is dichotomous exactly when f_i has increments in {0,1}.  It contains
binary additive (f = identity), capped, threshold, and the mixtures in between,
and there are 3^m of them per agent -- small enough to enumerate exhaustively at
m = 4 and to sample heavily at m = 5.

Reported: any instance failing all four solved cases, with a check of whether
Conjecture 2 itself survives on it.

Run:  python residual_hunt.py
"""
from itertools import combinations, product
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_5")
sys.path.insert(0, "../update_17")
sys.path.insert(0, "../update_47")
from routeA import partitions, uniformly_balanced, ellvec        # noqa: E402
from minimum_subsidy import subsets                              # noqa: E402
from cri_sweep import is_dichotomous                             # noqa: E402
from residual_map import classify, show_costs, is_binary_additive  # noqa: E402

NAMES = "abcdefghij"


def composed(D, f, m):
    """c(S) = f(|S & D|), as a dict over all subsets."""
    return {S: f[len(S & D)] for S in subsets(m)}


def cost_family(m):
    """All (D, f) composed dichotomous costs on m items, as (label, dict)."""
    out = []
    for k in range(m + 1):
        for Dt in combinations(range(m), k):
            D = frozenset(Dt)
            for steps in product((0, 1), repeat=k):
                f = [0]
                for s in steps:
                    f.append(f[-1] + s)
                if f[-1] == 0 and k > 0:
                    continue                    # constant zero, keep just once
                lab = "D=%s f=%s" % ("".join(NAMES[g] for g in sorted(D)), f)
                out.append((lab, composed(D, f, m), D, tuple(f)))
    out.append(("zero", {S: 0 for S in subsets(m)}, frozenset(), (0,)))
    return out


def check_candidate(cs, n, m, tag):
    """Full classification, printed."""
    assert all(is_dichotomous(c, m) for c in cs), "not dichotomous"
    f = classify(cs, n, m)
    covered = any(f[k] for k in ("S1", "S2", "S3", "S4"))
    print("  %-46s S1=%-5s S2=%-5s S3=%-5s S4=%-5s conj2=%-5s  RESIDUAL=%s"
          % (tag, f["S1"], f["S2"], f["S3"], f["S4"], f["conj2"],
             not covered))
    return f, not covered


def hand_construction():
    """The construction the docstring describes, tested directly."""
    print("=== the hand construction ===")
    m, n = 4, 3
    D1, D2, D3 = frozenset({0, 1}), frozenset({0, 2, 3}), frozenset({1, 2, 3})

    print("  prop:no-balance itself (all three additive):")
    cs = [composed(D1, [0, 1, 2], m),
          composed(D2, [0, 1, 2, 3], m),
          composed(D3, [0, 1, 2, 3], m)]
    check_candidate(cs, n, m, "c_i = |S & D_i|")

    print("  agent 3 capped at 2 -- same balance constraint, not additive:")
    cs = [composed(D1, [0, 1, 2], m),
          composed(D2, [0, 1, 2, 3], m),
          composed(D3, [0, 1, 2, 2], m)]
    f, resid = check_candidate(cs, n, m, "c_3 = min(|S & D_3|, 2)")
    if resid:
        print()
        print("  *** RESIDUAL INSTANCE FOUND BY CONSTRUCTION ***")
        show_costs(cs, n, m)
    print()
    return cs if resid else None


def exhaustive_hunt(m, n, cap=None):
    """Every composed instance at this size, up to the cap on cost functions."""
    fam = cost_family(m)
    print("=== exhaustive hunt over composed costs: n=%d m=%d, %d cost"
          " functions ===" % (n, m, len(fam)))
    found = []
    cnt = Counter()
    tot = 0
    idx = range(len(fam))
    for combo in combinations_with_repl(idx, n):
        cs = [fam[i][1] for i in combo]
        if max(max(c.values()) for c in cs) < 1:
            continue
        tot += 1
        f = classify(cs, n, m)
        for k in ("S1", "S2", "S3", "S4", "conj2"):
            if f[k]:
                cnt[k] += 1
        if not any(f[k] for k in ("S1", "S2", "S3", "S4")):
            cnt["residual"] += 1
            if len(found) < 5:
                found.append(([fam[i][0] for i in combo], cs, f))
        if not f["conj2"]:
            cnt["CONJ2_FAILS"] += 1
            found.insert(0, (["*** CONJ2 FAILS ***"] +
                             [fam[i][0] for i in combo], cs, f))
    print("  instances %d | S1 %d  S2 %d  S3 %d  S4 %d | RESIDUAL %d |"
          " conj2 fails %d"
          % (tot, cnt["S1"], cnt["S2"], cnt["S3"], cnt["S4"],
             cnt["residual"], cnt["CONJ2_FAILS"]))
    return found, cnt, tot


def combinations_with_repl(it, n):
    from itertools import combinations_with_replacement
    return combinations_with_replacement(it, n)


def main():
    cand = hand_construction()

    found, cnt, tot = exhaustive_hunt(4, 3)
    print()
    if cnt["CONJ2_FAILS"]:
        print("  *** CONJECTURE 2 IS FALSE on a composed instance. ***")
    elif cnt["residual"]:
        print("  *** %d residual instances exist inside the composed family at"
              " n=3, m=4. ***" % cnt["residual"])
        print("      Conjecture 2 holds on every one of them.")
    else:
        print("  no residual instance at n=3, m=4 among composed costs.")

    if found:
        print()
        print("  witnesses:")
        for labs, cs, f in found[:4]:
            print()
            print("     %s" % " | ".join(labs))
            print("     S1=%s S2=%s S3=%s S4=%s conj2=%s"
                  % (f["S1"], f["S2"], f["S3"], f["S4"], f["conj2"]))
            show_costs(cs, 3, 4)


if __name__ == "__main__":
    main()
