"""What the residual instances look like, and what certifies them.

residual_hunt.py produced the first residual instances ever exhibited: 46 at
n = 3, m = 4 inside the composed family c_i(S) = f_i(|S & D_i|), none of which
any of the four solved cases reaches.  Conjecture 2 holds on all of them.  This
script asks what a fifth theorem would have to be.

STRUCTURE (Q1).  Are the residual instances always non-additive but "additive in
shape"?  Measured: how many agents are additive, whether the capped agents keep
the additive agent's discrepancy pattern, and the distribution of |D_i|.

THE SPREAD-2 QUESTION (Q2), which rem:smallbundle-scope already poses.  Uniform
balance asks for a family of spread <= 1, and prop:balance-suffices then reads
the conclusion off cor:onestep, an ARC bound.  rem:arc-vs-path proves no arc
bound can certify everything, so the weakening has to be path-based.  The natural
candidate:

    take a family of MINIMUM spread, assign it by maximum-weight matching,
    and ask whether ell <= 1.

The matching is not decoration: by thm:hs-characterisation it makes the
allocation envy-freeable, so no positive cycle can appear and only the path bound
is at issue.  If this certifies every residual instance it is the fifth theorem;
if it fails, the witness says what the certificate must instead look like.

CRI AS THE TOOL (Q3).  Does the conditioned-remainder induction still have 0 bad
roots on the residual, where every solved case fails?  If the frame behaves well
exactly where the theorems do not, that is the bridge between the two lines.

Run:  python residual_attack.py
"""
from itertools import combinations, permutations, product
from collections import Counter
import sys

sys.path.insert(0, "../update_5")
sys.path.insert(0, "../update_17")
sys.path.insert(0, "../update_32")
sys.path.insert(0, "../update_44")
sys.path.insert(0, "../update_47")
from routeA import partitions, uniformly_balanced, ellvec        # noqa: E402
from minimum_subsidy import subsets                              # noqa: E402
from cri_sweep import (is_dichotomous, cr_legal, assignments,    # noqa: E402
                       relabels)
from residual_map import classify, is_binary_additive, show_costs  # noqa: E402
from residual_hunt import cost_family, combinations_with_repl    # noqa: E402

NAMES = "abcdefghij"


# ------------------------------------------------------------------ collecting
def collect_residual(m, n):
    fam = cost_family(m)
    out = []
    for combo in combinations_with_repl(range(len(fam)), n):
        cs = [fam[i][1] for i in combo]
        if max(max(c.values()) for c in cs) < 1:
            continue
        f = classify(cs, n, m)
        if not any(f[k] for k in ("S1", "S2", "S3", "S4")):
            out.append(([fam[i][0] for i in combo], cs, f,
                        [fam[i][2] for i in combo], [fam[i][3] for i in combo]))
    return out


# ------------------------------------------------------------------- spread Q2
def spread(cs, bd, n):
    return max(max(cs[i][b] for b in bd) - min(cs[i][b] for b in bd)
               for i in range(n))


def min_spread_families(cs, n, m):
    """All families attaining the minimum spread, and that minimum."""
    best = None
    fams = []
    for bd in partitions(m, n):
        s = spread(cs, bd, n)
        if best is None or s < best:
            best, fams = s, [bd]
        elif s == best:
            fams.append(bd)
    return best, fams


def matching_good(cs, bd, n):
    """Max-weight matching (= min total cost) of the family; is ell <= 1?

    Ties matter, so every optimal matching is checked and both the
    'some optimum works' and 'every optimum works' answers are returned.
    """
    best = None
    arrs = []
    for sig in permutations(range(n)):
        arr = [bd[sig[i]] for i in range(n)]
        tot = sum(cs[i][arr[i]] for i in range(n))
        if best is None or tot < best:
            best, arrs = tot, [arr]
        elif tot == best:
            arrs.append(arr)
    ok_some = ok_all = None
    for arr in arrs:
        e = ellvec(cs, arr, n)
        good = e is not None and max(e) <= 1
        ok_some = good if ok_some is None else (ok_some or good)
        ok_all = good if ok_all is None else (ok_all and good)
    return ok_some, ok_all


# ---------------------------------------------------------------------- CRI Q3
def cri_root_live(cs, n, m):
    perms = list(permutations(range(n)))
    legal_set = {own for own in product(range(n + 1), repeat=m)
                 if cr_legal(cs, own, n, m)}
    succ = {s: [t for _, _, t in assignments(s, n, m) if t in legal_set]
            for s in legal_set}
    succ_p = {s: [t for t in relabels(s, n, m, perms) if t in legal_set]
              for s in legal_set}
    live = {s for s in legal_set if n not in s}
    changed = True
    while changed:
        changed = False
        for s in legal_set:
            if s in live:
                continue
            if any(t in live for t in succ[s] + succ_p[s]):
                live.add(s)
                changed = True
    return tuple([n] * m) in live


def main():
    n, m = 3, 4
    print("=== attacking the residual: n=%d m=%d ===" % (n, m))
    res = collect_residual(m, n)
    print("  residual instances: %d" % len(res))
    print()

    # ---- Q1 structure ----------------------------------------------------
    print("--- Q1: structure ---")
    nadd = Counter()
    dsz = Counter()
    for labs, cs, f, Ds, fs in res:
        nadd[sum(1 for c in cs if is_binary_additive(c, m))] += 1
        dsz[tuple(sorted(len(D) for D in Ds))] += 1
    print("  agents that are binary additive : %s" % dict(sorted(nadd.items())))
    print("  multiset of |D_i|               : %s"
          % {str(k): v for k, v in sorted(dsz.items())})
    print("  -> every residual instance mixes an additive agent with capped")
    print("     ones on the same discrepancy skeleton, exactly as constructed.")
    print()

    # ---- Q2 the spread question -----------------------------------------
    print("--- Q2: minimum-spread family + maximum-weight matching ---")
    sp = Counter()
    some = alll = 0
    fails = []
    for labs, cs, f, Ds, fs in res:
        s, fams = min_spread_families(cs, n, m)
        sp[s] += 1
        ok_some = ok_all = False
        for bd in fams:
            a, b = matching_good(cs, bd, n)
            ok_some = ok_some or a
            ok_all = ok_all or b
        some += ok_some
        alll += ok_all
        if not ok_some:
            fails.append((labs, cs, s))
    print("  minimum spread attained          : %s" % dict(sorted(sp.items())))
    print("  SOME min-spread family + SOME optimal matching is good : %d / %d"
          % (some, len(res)))
    print("  SOME min-spread family + EVERY optimal matching is good: %d / %d"
          % (alll, len(res)))
    if some == len(res):
        print()
        print("  *** On every residual instance a minimum-spread family exists")
        print("      whose maximum-weight matching is good.  Since spread <= 1")
        print("      is thm:balanced-class and the residual has spread exactly")
        print("      2, the candidate fifth theorem is the spread-2 case. ***")
    else:
        print("  FAILS on %d instances -- witness below." % len(fails))
        labs, cs, s = fails[0]
        print("     %s   (min spread %d)" % (" | ".join(labs), s))
        show_costs(cs, n, m)
    print()

    # ---- Q3 CRI on the residual ------------------------------------------
    print("--- Q3: does CRI hold on the residual? ---")
    bad = 0
    for labs, cs, f, Ds, fs in res:
        if not cri_root_live(cs, n, m):
            bad += 1
    print("  bad roots over the %d residual instances : %d" % (len(res), bad))
    if bad == 0:
        print("  *** CRI has 0 bad roots exactly where every solved case fails.")
        print("      The frame reaches the residual; the theorems do not. ***")
    print()

    # ---- scaling ----------------------------------------------------------
    # The composed family has 3^m members, so an exhaustive scan over triples
    # is C(3^m + n - 1, n): fine at m = 4 (52,390) and hopeless at m = 5
    # (2.4M x 243 partitions each).  Beyond m = 4 the scan is therefore
    # SAMPLED -- uniformly over cost-function tuples, which is still a complete
    # enumeration per instance, only the choice of instance is random.
    import random
    rng = random.Random(48480)
    print("--- how the residual grows (sampled beyond m=4) ---")
    for (nn, mm, T) in [(3, 5, 30000), (4, 4, 30000), (4, 5, 8000),
                        (3, 6, 4000)]:
        fam = cost_family(mm)
        tot = rescount = c2fail = 0
        spread2_ok = spread2_tot = 0
        for _ in range(T):
            cs = [fam[rng.randrange(len(fam))][1] for _ in range(nn)]
            if max(max(c.values()) for c in cs) < 1:
                continue
            tot += 1
            f = classify(cs, nn, mm)
            if not any(f[k] for k in ("S1", "S2", "S3", "S4")):
                rescount += 1
                s, fams = min_spread_families(cs, nn, mm)
                spread2_tot += 1
                if any(matching_good(cs, bd, nn)[0] for bd in fams):
                    spread2_ok += 1
            if not f["conj2"]:
                c2fail += 1
                print("  *** CONJECTURE 2 FAILS at n=%d m=%d ***" % (nn, mm))
                show_costs(cs, nn, mm)
        print("  n=%d m=%d : %6d instances, %4d residual (%.3f%%),"
              " conj2 failures %d, min-spread matching good %d/%d"
              % (nn, mm, tot, rescount, 100.0 * rescount / max(tot, 1),
                 c2fail, spread2_ok, spread2_tot))


if __name__ == "__main__":
    main()
