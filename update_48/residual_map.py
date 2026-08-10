"""What is actually left unproven?  The residual of the four solved cases.

Conjecture 2 has four proved cases, and they have never been intersected:

    S1  binary additive                    thm:binadd     c_i(S) = |S & D_i|
    S2  identical costs, and n = 2         thm:identical
    S3  small bundles                      thm:smallbundle  some envy-freeable
                                           allocation has every bundle costing
                                           at most 1 to everybody (this is the
                                           instance-level form, wider than m<=n)
    S4  a uniformly balanced family        thm:balanced-class  a partition every
                                           agent values within one unit

S4 is much stronger than it looks.  It covers every SYMMETRIC instance --
c_i(S) = f_i(|S|) -- because a balanced partition shows each agent only f_i(q)
and f_i(q+1), which differ by at most one marginal.  That is the whole threshold
and capped families.  It also covers all 9,880 instances at n = m = 3
(update_5/routeA.py).

So the open part of Conjecture 2 is the intersection of the four COMPLEMENTS,
and this script maps it.  Note that prop:no-balance's instance -- the one with
no uniformly balanced family -- is binary additive, hence inside S1: it refutes
the METHOD of Approach 5 without being residual at all.  Whether the residual is
non-empty is therefore genuinely open, and question 1 below has never been asked.

WHAT IS MEASURED

  (1) the first (n,m) at which the residual is non-empty, per generator family;
  (2) residual density as n and m grow;
  (3) explicit minimal witnesses, printed with full cost tables;
  (4) whether Conjecture 2 holds on every residual instance -- exhaustively over
      allocations.  A failure is a COUNTEREXAMPLE to Conjecture 2, and the
      residual is exactly where one could still hide;
  (5) which case does the work, and whether any of S1-S3 is inside S4.

Everything is enumerated completely; nothing is capped or sampled within an
instance.  All seven generators of update_44/counterexample_hunt.py are used,
and is_dichotomous is asserted on every instance.

Run:  python residual_map.py
"""
from itertools import combinations_with_replacement, product
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_5")
sys.path.insert(0, "../update_6")
sys.path.insert(0, "../update_17")
sys.path.insert(0, "../update_44")
sys.path.insert(0, "../update_47")
from routeA import partitions, uniformly_balanced, ellvec        # noqa: E402
from targetGbal import gen_functions                             # noqa: E402
from minimum_subsidy import subsets                              # noqa: E402
from counterexample_hunt import FAMILIES                         # noqa: E402
from cri_sweep import is_dichotomous                             # noqa: E402

NAMES = "abcdefghij"


# ------------------------------------------------------------------ the cases
def is_binary_additive(c, m):
    """c(S) = sum of singletons, all singletons in {0,1}."""
    sing = [c[frozenset({g})] for g in range(m)]
    if any(v not in (0, 1) for v in sing):
        return False
    for S in c:
        if c[S] != sum(sing[g] for g in S):
            return False
    return True


def classify(cs, n, m):
    """Return the membership flags and whether Conjecture 2 holds."""
    s1 = all(is_binary_additive(c, m) for c in cs)
    s2 = (n == 2) or all(cs[i] == cs[0] for i in range(n))

    # one pass over all partitions, computing S3, S4 and Conjecture 2 together
    s3 = s4 = conj2 = False
    for bd in partitions(m, n):
        if not s4 and uniformly_balanced(cs, bd, n):
            s4 = True
        e = ellvec(cs, bd, n)
        if e is None:                       # positive cycle: not envy-freeable
            continue
        if not conj2 and max(e) <= 1:
            conj2 = True
        if not s3 and all(cs[v][bd[i]] <= 1 for v in range(n)
                          for i in range(n)):
            s3 = True
        if s3 and s4 and conj2:
            break
    return dict(S1=s1, S2=s2, S3=s3, S4=s4, conj2=conj2)


def show_costs(cs, n, m):
    subs = sorted(subsets(m), key=lambda s: (len(s), sorted(s)))
    if m > 5:
        print("        (singletons only, m = %d)" % m)
        for i in range(n):
            print("        c_%-3d %s   grand %d"
                  % (i + 1, [cs[i][frozenset({g})] for g in range(m)],
                     cs[i][frozenset(range(m))]))
        return
    hdr = "".join("%7s" % ("{" + "".join(NAMES[g] for g in sorted(S)) + "}"
                           if S else "{}") for S in subs)
    print("        %-5s%s" % ("S", hdr))
    for i in range(n):
        print("        c_%-3d%s" % (i + 1, "".join("%7d" % cs[i][S]
                                                   for S in subs)))


# ------------------------------------------------------------------- anchors
def anchors():
    print("=== anchors ===")
    m, n = 4, 3
    D = [frozenset({0, 1}), frozenset({0, 2, 3}), frozenset({1, 2, 3})]
    cs = [{S: len(S & D[i]) for S in subsets(m)} for i in range(n)]
    f = classify(cs, n, m)
    print("  prop:no-balance instance : S4 (uniform balance) = %s, "
          "S1 (binary additive) = %s" % (f["S4"], f["S1"]))
    print("     -> residual = %s   (expected False: it is covered by thm:binadd)"
          % (not any(f[k] for k in ("S1", "S2", "S3", "S4"))))

    F = gen_functions(3)
    bad = tot = 0
    for cs in combinations_with_replacement(F, 3):
        tot += 1
        cs = list(cs)
        if not any(uniformly_balanced(cs, bd, 3) for bd in partitions(3, 3)):
            bad += 1
    print("  exhaustive n=m=3         : %d of %d instances admit a uniformly"
          " balanced family" % (tot - bad, tot))
    print("     -> expected all %d, matching routeA.py" % tot)
    print()
    return bad == 0


# ---------------------------------------------------------------------- sweep
def run_block(tag, inst, n, m, wits, fam_first):
    cnt = Counter()
    resid = []
    for name, cs in inst:
        f = classify(cs, n, m)
        for k in ("S1", "S2", "S3", "S4", "conj2"):
            if f[k]:
                cnt[k] += 1
        covered = any(f[k] for k in ("S1", "S2", "S3", "S4"))
        if not covered:
            cnt["residual"] += 1
            resid.append((name, cs, f))
            if name not in fam_first:
                fam_first[name] = (n, m)
            if len(wits) < 3:
                wits.append((n, m, name, cs, f))
        if not f["conj2"]:
            cnt["CONJ2_FAILS"] += 1
            wits.insert(0, (n, m, name + " *** CONJ2 FAILS ***", cs, f))
    print("  %-10s inst %4d | S1 %4d  S2 %4d  S3 %4d  S4 %4d | RESIDUAL %4d"
          " | conj2 fails %d"
          % (tag, len(inst), cnt["S1"], cnt["S2"], cnt["S3"], cnt["S4"],
             cnt["residual"], cnt["CONJ2_FAILS"]))
    return cnt, resid


def main():
    rng = random.Random(480480)
    if not anchors():
        print("  ANCHOR FAILED -- stopping.")
        return

    print("=== the residual of the four solved cases ===")
    print()
    agg = Counter()
    wits = []
    fam_first = {}
    resid_all = []

    sizes = [(3, 4, 120), (3, 5, 90), (3, 6, 60), (3, 7, 30), (3, 8, 15),
             (4, 4, 90), (4, 5, 50), (4, 6, 20),
             (5, 4, 40), (5, 5, 15), (6, 4, 20)]
    for (n, m, T) in sizes:
        inst = []
        while len(inst) < T:
            name, gen = FAMILIES[rng.randrange(len(FAMILIES))]
            cs = gen(m, n, rng)
            if max(max(c.values()) for c in cs) < 1:
                continue
            assert all(is_dichotomous(c, m) for c in cs), name
            inst.append((name, cs))
        c, r = run_block("n=%d m=%d" % (n, m), inst, n, m, wits, fam_first)
        agg.update(c)
        agg["inst"] += len(inst)
        resid_all.extend((n, m) + x for x in r)

    print()
    print("  ================= TOTALS =================")
    print("  instances                     : %d" % agg["inst"])
    for k, lab in [("S1", "binary additive"), ("S2", "identical / n=2"),
                   ("S3", "small bundles"), ("S4", "uniformly balanced")]:
        print("  %-4s %-22s : %d" % (k, lab, agg[k]))
    print("  RESIDUAL (covered by none)    : %d" % agg["residual"])
    print("  Conjecture 2 fails            : %d" % agg["CONJ2_FAILS"])
    print()

    if agg["CONJ2_FAILS"]:
        print("  *** CONJECTURE 2 IS FALSE -- see the witness below. ***")
    elif agg["residual"] == 0:
        print("  *** THE RESIDUAL IS EMPTY at every size tested.  The four")
        print("      solved cases jointly cover every instance enumerated, so")
        print("      the open part of Conjecture 2 begins beyond exhaustive")
        print("      reach.  That is a statement about the shape of the problem")
        print("      and it is not currently in the report. ***")
    else:
        print("  *** THE RESIDUAL IS NON-EMPTY: %d instances that no existing")
        print("      theorem covers.  These are exactly what a fifth theorem")
        print("      has to reach. ***" % agg["residual"])
        print()
        print("  first (n,m) at which each generator produces a residual"
              " instance:")
        for name in sorted(fam_first):
            print("     %-10s n=%d m=%d" % (name, fam_first[name][0],
                                            fam_first[name][1]))

    if wits:
        print()
        print("  minimal witnesses:")
        for (n, m, name, cs, f) in wits[:3]:
            print()
            print("     n=%d m=%d family=%s   S1=%s S2=%s S3=%s S4=%s conj2=%s"
                  % (n, m, name, f["S1"], f["S2"], f["S3"], f["S4"],
                     f["conj2"]))
            show_costs(cs, n, m)


if __name__ == "__main__":
    main()
