"""Stress conj:cri-depth where it is weakest: larger m, and the hard families.

conj:cri-depth says every reachable legal CR state with |R| >= 3 is live.  It
rests on 34,543 states at m <= 7 with only SIX states at |R| = 7, and CRI.md
flags it as a hypothesis rather than a result.  This is the rem:n3-rules-fail
lesson: LEXB survived 227 instances and died on 368.

Two things have been learned since that sweep, and both say where to look.

  - THRESHOLD is the tightest family.  With the generators repaired, of the 29
    instances that come within one unit of refuting Conjecture 2, 17 are
    threshold against 4 nested and 3 capped.
  - The COMPOSED family c_i(S) = f_i(|S & D_i|) is where the residual of the
    solved cases lives (residual_hunt.py).  Those are the instances no existing
    theorem reaches, so they are the ones a new conjecture must survive.

This script re-runs the depth measurement on both, at m up to 9, and reports the
|R| histogram of DEAD reachable states.  A single dead state with |R| >= 3
refutes conj:cri-depth.

Run:  python depth_stress.py
"""
from itertools import combinations, permutations, product
from collections import Counter, defaultdict
import random
import sys

sys.path.insert(0, "../update_6")
sys.path.insert(0, "../update_17")
sys.path.insert(0, "../update_32")
sys.path.insert(0, "../update_44")
sys.path.insert(0, "../update_47")
from minimum_subsidy import subsets                              # noqa: E402
from counterexample_hunt import f_threshold, f_capped, f_nested   # noqa: E402
from cri_sweep import (is_dichotomous, cr_legal, assignments,     # noqa: E402
                       relabels)
from residual_hunt import cost_family                             # noqa: E402


def build(cs, n, m, perms):
    legal_set = {own for own in product(range(n + 1), repeat=m)
                 if cr_legal(cs, own, n, m)}
    succ = {s: [t for _, _, t in assignments(s, n, m) if t in legal_set]
            for s in legal_set}
    succ_p = {s: [t for t in relabels(s, n, m, perms) if t in legal_set]
              for s in legal_set}
    pred = defaultdict(list)
    for s in legal_set:
        for t in succ[s] + succ_p[s]:
            pred[t].append(s)
    live = {s for s in legal_set if n not in s}
    stack = list(live)
    while stack:
        t = stack.pop()
        for s in pred[t]:
            if s not in live:
                live.add(s)
                stack.append(s)
    root = tuple([n] * m)
    reach = set()
    if root in legal_set:
        reach.add(root)
        st = [root]
        while st:
            s = st.pop()
            for t in succ[s] + succ_p[s]:
                if t not in reach:
                    reach.add(t)
                    st.append(t)
    return live, reach, root


def f_composed(m, n, rng):
    fam = cost_family(m)
    return [fam[rng.randrange(len(fam))][1] for _ in range(n)]


def f_thresh(m, n, rng):
    return f_threshold(m, n, rng)


GENS = [("threshold", f_thresh), ("composed", f_composed),
        ("capped", f_capped), ("nested", f_nested)]


def main():
    rng = random.Random(909090)
    print("=== conj:cri-depth under stress: larger m, threshold and composed ===")
    print()
    HD = Counter()
    HA = Counter()
    badroot = 0
    ninst = 0
    viol = []
    print("  %-12s %-8s %8s %8s %10s" % ("family", "n,m", "inst", "reach",
                                         "dead |R|>=3"))
    for (n, m, T) in [(3, 6, 40), (3, 7, 25), (3, 8, 12), (3, 9, 5),
                      (4, 5, 30), (4, 6, 12), (4, 7, 5),
                      (5, 5, 10), (5, 6, 4)]:
        perms = list(permutations(range(n)))
        for name, gen in GENS:
            loc_deep = 0
            loc_reach = 0
            cnt = 0
            for _ in range(T):
                cs = gen(m, n, rng)
                if max(max(c.values()) for c in cs) < 1:
                    continue
                assert all(is_dichotomous(c, m) for c in cs), name
                cnt += 1
                ninst += 1
                live, reach, root = build(cs, n, m, perms)
                if root not in live:
                    badroot += 1
                for s in reach:
                    r = sum(1 for v in s if v == n)
                    if r == 0:
                        continue
                    HA[r] += 1
                    loc_reach += 1
                    if s not in live:
                        HD[r] += 1
                        if r >= 3:
                            loc_deep += 1
                            if len(viol) < 3:
                                viol.append((n, m, name, cs, s))
            print("  %-12s %-8s %8d %8d %10d"
                  % (name, "%d,%d" % (n, m), cnt, loc_reach, loc_deep))

    print()
    print("  instances                       : %d" % ninst)
    print("  bad roots (refute CRI)          : %d" % badroot)
    print()
    print("  |R| at a DEAD reachable state:")
    print("       |R|      dead    reachable   dead share")
    for r in sorted(HA):
        print("      %4d %9d %12d   %8.4f%%"
              % (r, HD[r], HA[r], 100.0 * HD[r] / max(HA[r], 1)))
    deep = sum(HD[r] for r in HD if r >= 3)
    deepall = sum(HA[r] for r in HA if r >= 3)
    print("       tot %9d %12d" % (sum(HD.values()), sum(HA.values())))
    print()
    print("  states with |R| >= 3 : %d   of them dead : %d" % (deepall, deep))
    if deep == 0:
        print()
        print("  *** conj:cri-depth SURVIVES.  No reachable legal CR state with")
        print("      |R| >= 3 is dead, now over %d such states at m up to 9 and"
              % deepall)
        print("      on the two families that matter -- threshold, the tightest")
        print("      for Conjecture 2, and composed, where the residual of the")
        print("      solved cases lives. ***")
    else:
        print()
        print("  *** conj:cri-depth IS REFUTED: %d dead states with |R| >= 3."
              % deep)
        n, m, name, cs, s = viol[0]
        print("      first witness n=%d m=%d family=%s state=%s"
              % (n, m, name, s))
        for i in range(n):
            print("        c_%d singletons %s grand %d"
                  % (i + 1, [cs[i][frozenset({g})] for g in range(m)],
                     cs[i][frozenset(range(m))]))


if __name__ == "__main__":
    main()
