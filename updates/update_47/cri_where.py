"""WHERE in the induction does CRI get stuck, and does a rule avoid it?

cri_stuck.py established two things.  Death in the CR frame is essentially
IMMEDIATE -- over the complete exhaustive n=m=3 family the stuck and the dead
states coincide exactly (912 = 912) -- and the free-assignment hypothesis is
SOUND: over 235,349 reachable non-terminal states, every one of the 1,285 stuck
states had no free assignment, with 0 exceptions.

Two questions remain, and they decide what a proof has to do.

  (Q1) WHERE.  What is |R| at a stuck state?  If the stuck states sit at small
       |R|, the whole difficulty is the end of the induction, and CRI reduces to
       a LAST-RUNG lemma: given a legal state with one chore left, some agent can
       take it.  That would be a one-step statement about allocations rather than
       a reachability statement about a search space.

  (Q2) A RULE.  Does free-first -- take a free assignment whenever one exists,
       otherwise any legal one -- reach a terminal?  This is the CR counterpart
       of the peel frame's free-first strategy, which reached a terminal on every
       instance tested there.  Also tested: the two naive rules, min-marginal
       (the rule prop-first-chore forces at the root) and max-marginal.

Run:  python cri_where.py
"""
from itertools import permutations, product
from collections import Counter, defaultdict
import random
import sys

sys.path.insert(0, "../update_6")
sys.path.insert(0, "../update_32")
sys.path.insert(0, "../update_44")
sys.path.insert(0, "../update_17")
from peel_general import ell                                    # noqa: E402
from counterexample_hunt import FAMILIES                        # noqa: E402
from cri_sweep import (profile, cr_legal, assignments, relabels,  # noqa: E402
                       is_dichotomous, exhaustive_n3m3)
from cri_stuck import bundles, no_free_assignment, beta_table    # noqa: E402


def free_assignments(cs, own, n, m):
    """All (a,x) meeting the CR free-assignment hypothesis."""
    A, R = bundles(own, n, m)
    out = []
    for a in sorted(R):
        beta, A = beta_table(cs, own, n, m, a)
        for x in range(n):
            if any(beta(x, A[k]) != 0 for k in range(n) if k != x):
                continue
            if all(beta(i, A[k]) <= beta(i, A[i])
                   for i in range(n) if i != x
                   for k in range(n) if k != i and k != x):
                out.append((a, x))
    return out


def where(cs, n, m, perms):
    """|R| histogram at stuck states, over reachable legal states."""
    root = tuple([n] * m)
    legal_set = {own for own in product(range(n + 1), repeat=m)
                 if cr_legal(cs, own, n, m)}
    succ = {s: [t for _, _, t in assignments(s, n, m) if t in legal_set]
            for s in legal_set}
    succ_p = {s: [t for t in relabels(s, n, m, perms) if t in legal_set]
              for s in legal_set}
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
    hist_stuck = Counter()
    hist_all = Counter()
    for s in reach:
        r = sum(1 for v in s if v == n)
        if r == 0:
            continue
        hist_all[r] += 1
        if not succ[s] and not any(succ[t] for t in succ_p[s]):
            hist_stuck[r] += 1
    return hist_stuck, hist_all


def greedy(cs, n, m, perms, mode):
    """Follow a rule from the root; 'ok' / 'stuck'."""
    own = tuple([n] * m)
    for _ in range(m + 1):
        if n not in own:
            return "ok"
        opts = [(a, x, t) for a, x, t in assignments(own, n, m)
                if cr_legal(cs, t, n, m)]
        if not opts:
            moved = False
            for t in relabels(own, n, m, perms):
                if not cr_legal(cs, t, n, m):
                    continue
                o2 = [(a, x, u) for a, x, u in assignments(t, n, m)
                      if cr_legal(cs, u, n, m)]
                if o2:
                    own, opts, moved = t, o2, True
                    break
            if not moved:
                return "stuck"
        if mode == "free-first":
            fr = set(free_assignments(cs, own, n, m))
            pref = [o for o in opts if (o[0], o[1]) in fr]
            opts = pref or opts
        elif mode in ("min-marg", "max-marg"):
            A, R = bundles(own, n, m)
            Rf = frozenset(R)

            def marg(a, x):
                base = frozenset(A[x] | (Rf - {a}))
                return cs[x][frozenset(base | {a})] - cs[x][base]
            key = min if mode == "min-marg" else max
            best = key(marg(a, x) for a, x, _ in opts)
            opts = [o for o in opts if marg(o[0], o[1]) == best]
        own = opts[0][2]
    return "cap"


def main():
    rng = random.Random(31337)
    print("=== where CRI gets stuck, and whether a rule avoids it ===")
    print()

    blocks = [("EXHAUSTIVE n=m=3", exhaustive_n3m3(), 3, 3)]
    for (n, m, T) in [(3, 4, 60), (3, 5, 30), (3, 6, 12),
                      (4, 4, 30), (4, 5, 12), (5, 4, 10)]:
        inst = []
        while len(inst) < T:
            name, gen = FAMILIES[rng.randrange(len(FAMILIES))]
            cs = gen(m, n, rng)
            if max(max(c.values()) for c in cs) < 1:
                continue
            assert all(is_dichotomous(c, m) for c in cs)
            inst.append(cs)
        blocks.append(("n=%d m=%d" % (n, m), inst, n, m))

    HS = Counter()
    HA = Counter()
    rules = ["free-first", "min-marg", "max-marg", "any"]
    fails = Counter()
    ninst = 0
    print("  %-18s %s" % ("block", "rule failures (instances not reaching a terminal)"))
    for tag, inst, n, m in blocks:
        perms = list(permutations(range(n)))
        loc = Counter()
        for cs in inst:
            ninst += 1
            hs, ha = where(cs, n, m, perms)
            HS.update(hs)
            HA.update(ha)
            for r in rules:
                if greedy(cs, n, m, perms, r) != "ok":
                    loc[r] += 1
                    fails[r] += 1
        print("  %-18s %s" % (tag, dict(loc) if loc else "none"))

    print()
    print("  (Q1) |R| at a stuck state, against all reachable non-terminal states:")
    print("       |R|   stuck   all reachable   stuck share")
    for r in sorted(HA):
        print("      %4d %7d %15d   %8.4f%%"
              % (r, HS[r], HA[r], 100.0 * HS[r] / max(HA[r], 1)))
    tot_s = sum(HS.values())
    print("       tot %7d %15d" % (tot_s, sum(HA.values())))
    if tot_s and HS[1] == tot_s:
        print()
        print("  *** EVERY stuck state has |R| = 1.  CRI is therefore equivalent")
        print("      to a LAST-RUNG lemma: from a legal state with one chore")
        print("      undecided, some agent can take it.  The induction has no")
        print("      difficulty anywhere else. ***")
    elif tot_s:
        print()
        print("  stuck states occur at |R| in %s, so the difficulty is not"
              % sorted(r for r in HS if HS[r]))
        print("  confined to the last rung.")

    print()
    print("  (Q2) rule failures over %d instances: %s"
          % (ninst, {r: fails[r] for r in rules}))
    ok = [r for r in rules if fails[r] == 0]
    if ok:
        print("       rules that always reached a terminal: %s" % ", ".join(ok))


if __name__ == "__main__":
    main()
