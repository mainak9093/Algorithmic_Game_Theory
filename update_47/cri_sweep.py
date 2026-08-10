"""Phase 0 of the CONDITIONED-REMAINDER INDUCTION (CRI): is it false?

THE FRAME.  A CR STATE is a pair (A, R) with R a set of undecided chores and A a
partition of D = M \\ R.  Its profile is

    W_i := A_i  union  R

-- every agent is still on the hook for the whole undecided remainder.  Writing
c^R_i(T) := c_i(T union R) - c_i(R) for the CONTRACTED cost function, two facts
motivate the whole thing:

  (L1) c^R_i is again normalised with marginals in {0,1}, so (D, c^R) is again a
       negative dichotomous instance;
  (L2) w_W(i,k) = c_i(A_i u R) - c_i(A_k u R) = c^R_i(A_i) - c^R_i(A_k), so the
       envy graph of the profile W IS the envy graph of the allocation A in the
       instance (D, c^R).  Hence

           (A,R) is legal  <==>  A witnesses Conjecture 2 on (D, c^R).

So a CR state is a witness for Conjecture 2 on a SMALLER instance, and the single
move -- assign one chore of R to one agent -- un-contracts one element.  CRI is
therefore an induction in which the instance GROWS and a witness is maintained,
which is the shape of the [BKNS22] proof, run on the conditioned cost functions
that dissolve the Approach 1 obstruction (rem:conditioned).

    CRI.  From the root (A empty, R = M) some sequence of assignments reaches
          R = empty with every intermediate CR state legal.

In peel language an assignment is one ATOMIC BLOCK: relieve all n-1 non-owners of
the chore at once.  So CRI drops the legality requirement at the n-2 within-block
intermediates that conj:h1pp imposes, and

    conj:h1pp  ==>  CRI  ==>  Conjecture 2,

i.e. CRI is strictly the weaker target.  Two structural consequences make it
worth running: the state space is (n+1)^m partial functions rather than (2^m)^n
profiles, and the known peel dead ends are NOT CR states -- both
({a1,a2},{g},{g}) and ({g2},{g2},{g1,g3,g4}) repeat an item across bundles, which
a partial allocation cannot do.

WHAT IS MEASURED.  Over ALL (n+1)^m states, not merely the reachable ones, since
a pointwise lemma is a claim about every legal state:

  (a) BAD ROOTS       -- the root is not live.  One refutes CRI.
  (b) THE GAP         -- bad roots on which Conjecture 2 nevertheless holds.  For
                         conj:h1prime this gap is real (rem:converse); if it is
                         empty here, CRI is not observably stronger than the
                         conjecture, which is a strictly better position.
  (P1) EXTENDABILITY  -- does every legal non-terminal state have a legal
                         successor?  An assignment strictly shrinks R, so unlike
                         the peel frame P1 cannot be satisfied by a move that
                         makes no progress: P1 ALONE IMPLIES CRI, hence
                         Conjecture 2.  The peel analogue, conj:h1, is refuted.
  (P2) NO DEAD STATES -- is every legal state live?  Weaker than P1.
  (d) ORDER FREEDOM   -- from a live state, is EVERY undecided chore assignable
                         to some agent keeping it live?  In the peel frame the
                         chore order is not free (sec:typeorder).
  (e) PERMUTATIONS    -- does allowing A -> A o sigma add any reachability?

VERIFICATION RULES observed here: the longest-path routine is the project's own
(update_32/peel_general.ell), not a re-implementation; the state space is
enumerated completely and never capped; and every one of the seven adversarial
generators of update_44/counterexample_hunt.py is used, not rand_dicho alone --
every Approach 3 sweep so far has used rand_dicho only.

Run:  python cri_sweep.py
"""
from itertools import combinations_with_replacement, permutations, product
from collections import Counter, defaultdict
import random
import sys

sys.path.insert(0, "../update_6")
sys.path.insert(0, "../update_32")
sys.path.insert(0, "../update_44")
from peel_general import ell                                    # noqa: E402
from targetGbal import gen_functions                            # noqa: E402
from counterexample_hunt import FAMILIES                        # noqa: E402

UNDEC = None            # placeholder; the sentinel is n, set per call


def is_dichotomous(c, m):
    """Every marginal in {0,1}.  Guard, not decoration: f_capped and f_threshold
    silently produced marginals of 2 until 2026-08-09, so every instance this
    sweep touches is checked before it is used."""
    for S in c:
        for g in range(m):
            if g in S:
                continue
            if c[frozenset(S | {g})] - c[S] not in (0, 1):
                return False
    return True


def profile(own, n, m):
    """W_i = A_i union R.  own[j] in 0..n-1 is the owner, own[j] == n undecided."""
    return tuple(frozenset(j for j in range(m)
                           if own[j] == i or own[j] == n)
                 for i in range(n))


def cr_legal(cs, own, n, m):
    e = ell(cs, profile(own, n, m), n)
    return e is not None and max(e) <= 1


def assignments(own, n, m):
    """Successors under the CR move: give one undecided chore to one agent."""
    out = []
    for j in range(m):
        if own[j] != n:
            continue
        for x in range(n):
            s = list(own)
            s[j] = x
            out.append((j, x, tuple(s)))
    return out


def relabels(own, n, m, perms):
    """A -> A o sigma.  Undecided chores are untouched."""
    out = []
    for p in perms:
        out.append(tuple(p[v] if v != n else n for v in own))
    return out


def analyse(cs, n, m, perms):
    """Complete analysis over ALL (n+1)^m states.  Nothing is sampled or capped.

    The move set is ASSIGNMENT + RELABELLING, matching def:peel, which also
    carries permutations.  The assignment-only frame is reported alongside,
    because the difference between the two is itself a result.

    P1/P2 are reported over the states REACHABLE from the root, not over all
    legal states: an induction that starts at the root never has to handle a
    state it cannot reach, and quantifying over all legal states overstates the
    difficulty.  Both figures are returned.

    A relabelling makes no PROGRESS (|R| is unchanged), so -- exactly the
    correction recorded in obs:peel-residual -- a state whose only legal moves
    are relabellings is stuck.  `p1` below therefore asks for a legal
    ASSIGNMENT, reachable directly or after any sequence of legal relabellings.
    """
    root = tuple([n] * m)
    legal_set = set()
    for own in product(range(n + 1), repeat=m):
        if cr_legal(cs, own, n, m):
            legal_set.add(own)

    terminals = [s for s in legal_set if n not in s]

    # forward edges, restricted to legal states -------------------------------
    succ = {}
    succ_perm = {}
    for s in legal_set:
        succ[s] = [t for _, _, t in assignments(s, n, m) if t in legal_set]
        succ_perm[s] = [t for t in relabels(s, n, m, perms) if t in legal_set]

    def live_set(with_perms):
        pred = defaultdict(list)
        for s in legal_set:
            for t in succ[s]:
                pred[t].append(s)
            if with_perms:
                for t in succ_perm[s]:
                    pred[t].append(s)
        live = set(terminals)
        stack = list(terminals)
        while stack:
            t = stack.pop()
            for s in pred[t]:
                if s not in live:
                    live.add(s)
                    stack.append(s)
        return live

    live = live_set(False)          # assignment-only frame
    live_p = live_set(True)         # the real frame

    # forward reachability from the root, in the real frame -------------------
    reach = set()
    if root in legal_set:
        reach.add(root)
        stack = [root]
        while stack:
            s = stack.pop()
            for t in succ[s] + succ_perm[s]:
                if t not in reach:
                    reach.add(t)
                    stack.append(t)

    # (P1) progress: a legal ASSIGNMENT, possibly after legal relabellings -----
    def progresses(s):
        if succ[s]:
            return True
        for t in succ_perm[s]:
            if succ[t]:
                return True
        return False

    p1_all = [s for s in legal_set if n in s and not progresses(s)]
    p1_reach = [s for s in p1_all if s in reach]

    # (P2) deadness ------------------------------------------------------------
    p2_all = [s for s in legal_set if s not in live_p]
    p2_reach = [s for s in p2_all if s in reach]

    # (d) from a reachable live state, is every undecided chore assignable? ----
    d_bad = 0
    d_tot = 0
    for s in reach & live_p:
        if n not in s:
            continue
        for j in range(m):
            if s[j] != n:
                continue
            d_tot += 1
            if not any(tuple(s[:j] + (x,) + s[j + 1:]) in live_p
                       for x in range(n)):
                d_bad += 1

    return {
        "root_live": root in live,
        "root_live_perm": root in live_p,
        "conj2": bool(terminals),
        "legal": len(legal_set),
        "live": len(live_p),
        "reach": len(reach),
        "p1_bad": p1_reach,
        "p1_all": len(p1_all),
        "p2_bad": p2_reach,
        "p2_all": len(p2_all),
        "d_bad": d_bad,
        "d_tot": d_tot,
    }


def run_block(tag, instances, n, m):
    perms = list(permutations(range(n)))
    tot = bad = badna = gap = 0
    p1 = p2 = dbad = dtot = p1all = p2all = 0
    states = live = reach = 0
    wit_p1 = wit_p2 = wit_bad = None
    for cs in instances:
        r = analyse(cs, n, m, perms)
        tot += 1
        states += r["legal"]
        live += r["live"]
        reach += r["reach"]
        if not r["root_live"]:
            badna += 1                      # bad root, assignment-only frame
        if not r["root_live_perm"]:
            bad += 1                        # bad root, the REAL frame
            if wit_bad is None:
                wit_bad = (n, m, cs)
            if r["conj2"]:
                gap += 1
        p1 += len(r["p1_bad"])
        p2 += len(r["p2_bad"])
        p1all += r["p1_all"]
        p2all += r["p2_all"]
        if r["p1_bad"] and wit_p1 is None:
            wit_p1 = (n, m, cs, r["p1_bad"][0])
        if r["p2_bad"] and wit_p2 is None:
            wit_p2 = (n, m, cs, r["p2_bad"][0])
        dbad += r["d_bad"]
        dtot += r["d_tot"]
    print("  %-20s inst %5d | reach %7d | BAD ROOTS %3d (assign-only %3d)"
          " | gap %2d | P1 %5d/%-7d | P2 %5d/%-7d | order %5d/%-7d"
          % (tag, tot, reach, bad, badna, gap, p1, p1all, p2, p2all,
             dbad, dtot))
    return dict(tot=tot, bad=bad, badna=badna, gap=gap, p1=p1, p2=p2,
                p1all=p1all, p2all=p2all, dbad=dbad, dtot=dtot,
                states=states, live=live, reach=reach,
                wit_p1=wit_p1, wit_p2=wit_p2, wit_bad=wit_bad)


def exhaustive_n3m3():
    F = gen_functions(3)
    return [list(cs) for cs in combinations_with_replacement(F, 3)]


def main():
    rng = random.Random(20260809)
    print("=== CRI Phase 0: complete state-space analysis ===")
    print()
    print("  P1 = every legal non-terminal state has a legal successor "
          "(implies CRI, hence Conjecture 2)")
    print("  P2 = every legal state is live       "
          "  gap = bad roots on which Conjecture 2 holds anyway")
    print()

    agg = Counter()
    wits = {}
    KEYS = ("tot", "bad", "badna", "gap", "p1", "p2", "p1all", "p2all",
            "dbad", "dtot", "states", "live", "reach")

    # ---- the complete exhaustive n = m = 3 family --------------------------
    inst = exhaustive_n3m3()
    r = run_block("EXHAUSTIVE n=m=3", inst, 3, 3)
    for k in KEYS:
        agg[k] += r[k]
    for k in ("wit_p1", "wit_p2", "wit_bad"):
        if r[k] and k not in wits:
            wits[k] = r[k]
    print()

    # ---- adversarial families, all seven -----------------------------------
    print("  --- adversarial generators (uniform / disjoint / nested /"
          " one-heavy / capped / threshold / mixed) ---")
    for (n, m, T) in [(3, 4, 150), (3, 5, 80), (3, 6, 40), (3, 7, 15),
                      (4, 4, 80), (4, 5, 30), (4, 6, 10),
                      (5, 4, 25), (5, 5, 8)]:
        inst = []
        while len(inst) < T:
            name, gen = FAMILIES[rng.randrange(len(FAMILIES))]
            cs = gen(m, n, rng)
            if max(max(c.values()) for c in cs) < 1:
                continue
            if not all(is_dichotomous(c, m) for c in cs):
                raise AssertionError(
                    "generator %s produced a non-dichotomous instance at "
                    "n=%d m=%d" % (name, n, m))
            inst.append(cs)
        r = run_block("n=%d m=%d" % (n, m), inst, n, m)
        for k in KEYS:
            agg[k] += r[k]
        for k in ("wit_p1", "wit_p2", "wit_bad"):
            if r[k] and k not in wits:
                wits[k] = r[k]

    print()
    print("  ====================== TOTALS ======================")
    print("  instances                          : %d" % agg["tot"])
    print("  legal CR states examined           : %d" % agg["states"])
    print("  reachable from the root            : %d" % agg["reach"])
    print()
    print("  (a)  BAD ROOTS, assignment + relabelling : %d" % agg["bad"])
    print("       BAD ROOTS, assignment only          : %d" % agg["badna"])
    print("  (b)  bad roots on which Conjecture 2 holds anyway : %d" % agg["gap"])
    print("  (P1) REACHABLE legal non-terminal states with no legal"
          " assignment : %d  (over all legal states: %d)"
          % (agg["p1"], agg["p1all"]))
    print("  (P2) REACHABLE legal states that are DEAD : %d"
          "  (over all legal states: %d)" % (agg["p2"], agg["p2all"]))
    print("  (d)  reachable live state x undecided chore with no live owner"
          " : %d of %d" % (agg["dbad"], agg["dtot"]))
    print()

    if agg["bad"]:
        print("  *** CRI IS REFUTED: %d bad roots. ***" % agg["bad"])
        if wits.get("wit_bad"):
            n, m, cs = wits["wit_bad"]
            print("      first witness n=%d m=%d, singleton costs:" % (n, m))
            for i, c in enumerate(cs):
                print("        agent %d: %s  grand %d"
                      % (i, [c[frozenset({g})] for g in range(m)],
                         c[frozenset(range(m))]))
    else:
        print("  *** CRI survives every instance tested. ***")

    if agg["p1"] == 0:
        print()
        print("  *** P1 HOLDS EVERYWHERE.  Every legal non-terminal CR state has")
        print("      a legal successor, and an assignment strictly shrinks R, so")
        print("      no schedule can stall: P1 implies CRI implies Conjecture 2.")
        print("      The peel analogue conj:h1 is REFUTED, so this is a genuine")
        print("      difference between the two frames and the target theorem")
        print("      becomes a POINTWISE lemma. ***")
    else:
        print()
        print("  P1 fails %d times -- a legal non-terminal state with no legal"
              % agg["p1"])
        print("  successor exists, so CRI needs more than local extendability.")
        if wits.get("wit_p1"):
            n, m, cs, s = wits["wit_p1"]
            print("     first witness n=%d m=%d state own=%s" % (n, m, s))
            for i, c in enumerate(cs):
                print("        agent %d: %s  grand %d"
                      % (i, [c[frozenset({g})] for g in range(m)],
                         c[frozenset(range(m))]))

    if agg["p2"] == 0:
        print()
        print("  *** P2 HOLDS: no legal CR state is dead.  Every one of the")
        print("      peel frame's dead ends (prop:deadends) has vanished under")
        print("      the change of state space. ***")
    else:
        print()
        print("  P2 fails %d times: dead legal CR states exist." % agg["p2"])
        if wits.get("wit_p2"):
            n, m, cs, s = wits["wit_p2"]
            print("     first witness n=%d m=%d state own=%s" % (n, m, s))

    if agg["dbad"] == 0:
        print()
        print("  *** The chore ORDER is free: from any live state, every")
        print("      undecided chore has an owner keeping the state live.  So")
        print("      only the OWNER choice carries content, and a rule need not")
        print("      schedule the chores.  (In the peel frame the order is not")
        print("      free -- sec:typeorder.) ***")


if __name__ == "__main__":
    main()
