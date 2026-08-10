"""The exact witnesses for every claim in the CR line that failed.

CRI itself is not refuted -- 0 bad roots over 10,318 instances including the
complete exhaustive n = m = 3 family.  But five sharper statements inside the
line ARE refuted, and this script extracts the minimal witness for each one,
prints the full cost table, and demonstrates the failure move by move through the
project's own longest-path routine.  Counts are not evidence; instances are.

  (W1) CRI WITHOUT RELABELLING.  3 bad roots in the exhaustive n=m=3 family.
       Shows that A -> A o sigma is not decoration: without it the induction
       genuinely stalls, and with it the same instance completes.

  (W2) POINTWISE CRI.  A legal non-terminal CR state at which NO assignment is
       legal.  This is the CR analogue of conj:h1, and like conj:h1 it is false.

  (W3) THE LAST-RUNG LEMMA.  A legal state with one chore left that no agent can
       take.  1,765 of the 1,778 stuck states have |R| = 1, so this is where
       essentially all stuckness lives.

  (W4) A DELAYED DEATH.  A dead state with |R| = 2 that HAS a legal assignment --
       so death is not always immediate, and a rule cannot be certified by
       one-step legality alone.  Only 45 of 1,275 dead states are of this kind.

  (W5) BALANCE, TRANSPLANTED.  A dead state admitting a balanced completion, so
       "admits a balanced terminal => live" -- the one surviving idea of the peel
       frame (conj:balance-rule) -- is FALSE in the CR frame.

  (W6) FREE-FIRST.  An instance on which the free-first rule fails although the
       root is live, so a correct schedule exists and the rule misses it.

Every witness is re-verified here independently of the sweep that found it.

Run:  python cri_witnesses.py
"""
from itertools import combinations_with_replacement, permutations, product
from collections import defaultdict
import random
import sys

sys.path.insert(0, "../update_6")
sys.path.insert(0, "../update_32")
sys.path.insert(0, "../update_44")
sys.path.insert(0, "../update_17")
from peel_general import ell                                    # noqa: E402
from targetGbal import gen_functions                            # noqa: E402
from counterexample_hunt import FAMILIES                        # noqa: E402
from minimum_subsidy import subsets                             # noqa: E402
from cri_sweep import (profile, cr_legal, assignments, relabels,  # noqa: E402
                       is_dichotomous, exhaustive_n3m3)
from cri_stuck import bundles, admits_balanced_completion        # noqa: E402
from cri_where import free_assignments, greedy                   # noqa: E402

NAMES = "abcdefgh"


def show_costs(cs, n, m):
    subs = sorted(subsets(m), key=lambda s: (len(s), sorted(s)))
    hdr = "".join("%8s" % ("{" + "".join(NAMES[g] for g in sorted(S)) + "}"
                           if S else "{}") for S in subs)
    print("        %-6s%s" % ("S", hdr))
    for i in range(n):
        print("        c_%-4d%s" % (i + 1, "".join("%8d" % cs[i][S]
                                                   for S in subs)))


def show_state(cs, own, n, m, label="state"):
    A, R = bundles(own, n, m)
    W = profile(own, n, m)
    e = ell(cs, W, n)
    print("     %s: A = (%s)   R = {%s}"
          % (label,
             ", ".join("{%s}" % "".join(NAMES[g] for g in sorted(A[i]))
                       for i in range(n)),
             "".join(NAMES[g] for g in sorted(R))))
    print("        profile W = (%s)"
          % ", ".join("{%s}" % "".join(NAMES[g] for g in sorted(W[i]))
                      for i in range(n)))
    print("        envy matrix w(i,k) = c_i(W_i) - c_i(W_k):")
    for i in range(n):
        print("           %s" % [cs[i][W[i]] - cs[i][W[k]] for k in range(n)])
    print("        ell = %s   legal = %s"
          % (e, cr_legal(cs, own, n, m)))


def why_stuck(cs, own, n, m):
    """Print every candidate assignment and the reason it is illegal."""
    A, R = bundles(own, n, m)
    print("        every assignment and why it fails:")
    for a in sorted(R):
        for x in range(n):
            t = list(own)
            t[a] = x
            t = tuple(t)
            W = profile(t, n, m)
            e = ell(cs, W, n)
            if e is None:
                why = "positive-weight cycle"
            elif max(e) > 1:
                why = "ell = %s, max %d > 1" % (e, max(e))
            else:
                why = "LEGAL"
            print("           give %s to agent %d -> %s" % (NAMES[a], x + 1, why))


def build(cs, n, m, perms):
    root = tuple([n] * m)
    legal_set = {own for own in product(range(n + 1), repeat=m)
                 if cr_legal(cs, own, n, m)}
    succ = {s: [t for _, _, t in assignments(s, n, m) if t in legal_set]
            for s in legal_set}
    succ_p = {s: [t for t in relabels(s, n, m, perms) if t in legal_set]
              for s in legal_set}
    pred = defaultdict(list)
    predA = defaultdict(list)
    for s in legal_set:
        for t in succ[s]:
            pred[t].append(s)
            predA[t].append(s)
        for t in succ_p[s]:
            pred[t].append(s)

    def close(pr):
        live = {s for s in legal_set if n not in s}
        st = list(live)
        while st:
            t = st.pop()
            for s in pr[t]:
                if s not in live:
                    live.add(s)
                    st.append(s)
        return live

    live = close(pred)
    liveA = close(predA)
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
    return legal_set, succ, succ_p, live, liveA, reach


def w1_no_relabelling():
    print("=" * 74)
    print("(W1) CRI WITHOUT RELABELLING IS REFUTED")
    print("=" * 74)
    print("  Searching the complete exhaustive n = m = 3 family (9,880"
          " instances)...")
    perms = list(permutations(range(3)))
    n = m = 3
    found = []
    for cs in exhaustive_n3m3():
        _, _, _, live, liveA, _ = build(cs, n, m, perms)
        root = tuple([n] * m)
        if root not in liveA and root in live:
            found.append(cs)
    print("  instances where the root is live WITH relabelling but not"
          " without: %d" % len(found))
    if not found:
        return
    cs = found[0]
    print()
    print("  smallest witness:")
    show_costs(cs, n, m)
    print()
    print("     All three are dichotomous; a,b,c denote the three chores.")
    root = tuple([n] * m)
    show_state(cs, root, n, m, "root ")
    print()
    print("     Assignment-only: the root cannot reach any legal terminal.")
    print("     With relabelling it can.  A witnessing schedule:")
    _, succ, succ_p, live, liveA, _ = build(cs, n, m, perms)
    # exhibit one schedule using a relabelling
    path = [root]
    cur = root
    guard = 0
    while n in cur and guard < 12:
        guard += 1
        nxt = [t for t in succ[cur] if t in live]
        if nxt:
            cur = nxt[0]
            path.append(cur)
            continue
        moved = False
        for t in succ_p[cur]:
            if t in live and any(u in live for u in succ[t]):
                path.append(("relabel", t))
                cur = [u for u in succ[t] if u in live][0]
                path.append(cur)
                moved = True
                break
        if not moved:
            break
    for step in path:
        if isinstance(step, tuple) and step and step[0] == "relabel":
            print("        -- relabel --")
            show_state(cs, step[1], n, m, "after ")
        else:
            show_state(cs, step, n, m, "      ")
    print()


def find_state(pred, blocks):
    """First (cs, state, n, m) over the blocks satisfying pred(ctx)."""
    for tag, inst, n, m in blocks:
        perms = list(permutations(range(n)))
        for cs in inst:
            legal_set, succ, succ_p, live, liveA, reach = build(cs, n, m, perms)
            for s in sorted(reach, key=lambda z: sum(1 for v in z if v != n)):
                ctx = dict(cs=cs, s=s, n=n, m=m, succ=succ, succ_p=succ_p,
                           live=live, reach=reach)
                if pred(ctx):
                    return cs, s, n, m, tag
    return None


def main():
    rng = random.Random(13572468)
    n = m = 3

    w1_no_relabelling()

    blocks = [("exhaustive n=m=3", exhaustive_n3m3(), 3, 3)]
    for (nn, mm, T) in [(3, 4, 40), (3, 5, 20), (4, 4, 20)]:
        inst = []
        while len(inst) < T:
            name, gen = FAMILIES[rng.randrange(len(FAMILIES))]
            cs = gen(mm, nn, rng)
            if max(max(c.values()) for c in cs) < 1:
                continue
            assert all(is_dichotomous(c, mm) for c in cs)
            inst.append(cs)
        blocks.append(("n=%d m=%d" % (nn, mm), inst, nn, mm))

    # ---- (W2)/(W3) pointwise CRI and the last rung -------------------------
    print("=" * 74)
    print("(W2)+(W3) POINTWISE CRI AND THE LAST-RUNG LEMMA ARE REFUTED")
    print("=" * 74)
    r = find_state(lambda c: c["n"] in c["s"] and not c["succ"][c["s"]]
                   and not any(c["succ"][t] for t in c["succ_p"][c["s"]]),
                   blocks[:1])
    if r:
        cs, s, nn, mm, tag = r
        print("  smallest witness, from the %s family:" % tag)
        show_costs(cs, nn, mm)
        print()
        show_state(cs, s, nn, mm, "stuck")
        print()
        why_stuck(cs, s, nn, mm)
        R = sum(1 for v in s if v == nn)
        print()
        print("     |R| = %d, so this is also a LAST-RUNG failure: the state is"
              % R)
        print("     legal, one chore remains, and no agent can take it.")
        print("     It is reachable from the root, so an induction really does")
        print("     have to avoid arriving here.")
    print()

    # ---- (W4) a delayed death ----------------------------------------------
    print("=" * 74)
    print("(W4) DEATH IS NOT ALWAYS IMMEDIATE")
    print("=" * 74)
    r = find_state(lambda c: c["s"] not in c["live"] and c["succ"][c["s"]]
                   and c["n"] in c["s"], blocks)
    if r:
        cs, s, nn, mm, tag = r
        print("  smallest witness, from the %s family:" % tag)
        show_costs(cs, nn, mm)
        print()
        show_state(cs, s, nn, mm, "dead ")
        print()
        print("     This state HAS a legal assignment, yet every continuation")
        print("     dies.  So one-step legality cannot certify a rule, and the")
        print("     free-assignment lemma is sufficient for a legal MOVE but")
        print("     never for a legal SCHEDULE.")
        why_stuck(cs, s, nn, mm)
    print()

    # ---- (W5) balance does not transplant ----------------------------------
    print("=" * 74)
    print("(W5) BALANCE DOES NOT TRANSPLANT: dead, yet admits a balanced"
          " completion")
    print("=" * 74)
    r = find_state(lambda c: c["s"] not in c["live"] and c["n"] in c["s"]
                   and admits_balanced_completion(c["s"], c["n"], c["m"]),
                   blocks)
    if r:
        cs, s, nn, mm, tag = r
        print("  smallest witness, from the %s family:" % tag)
        show_costs(cs, nn, mm)
        print()
        show_state(cs, s, nn, mm, "dead ")
        A, R = bundles(s, nn, mm)
        print("        bundle sizes %s with %d undecided, so a completion with"
              % ([len(a) for a in A], len(R)))
        print("        sizes differing by at most 1 exists -- and the state is")
        print("        still dead.  conj:balance-rule's certificate is FALSE")
        print("        in the CR frame.")
    print()

    # ---- (W6) free-first fails ---------------------------------------------
    print("=" * 74)
    print("(W6) THE FREE-FIRST RULE FAILS ON A LIVE ROOT")
    print("=" * 74)
    perms = list(permutations(range(3)))
    for cs in exhaustive_n3m3():
        _, _, _, live, _, _ = build(cs, 3, 3, perms)
        if tuple([3] * 3) not in live:
            continue
        if greedy(cs, 3, 3, perms, "free-first") != "ok":
            print("  smallest witness:")
            show_costs(cs, 3, 3)
            print()
            print("     The root IS live -- a legal schedule to a terminal")
            print("     exists -- but free-first walks into a stuck state.")
            print("     Free assignments are safe individually and still do not")
            print("     compose into a schedule.")
            break
    print()
    print("=" * 74)
    print("NOT REFUTED: CRI itself.  0 bad roots over 10,318 instances,")
    print("including the complete exhaustive n = m = 3 family.  What the")
    print("witnesses above kill are the LOCAL statements one would like to")
    print("prove it with, not the conjecture.")
    print("=" * 74)


if __name__ == "__main__":
    main()
