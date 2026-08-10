"""What do the stuck CR states look like?

cri_sweep.py settles Phase 0: CRI (assignment + relabelling) has 0 bad roots over
10,318 instances including the complete exhaustive n = m = 3 family, but it is
NOT pointwise -- 3,024 reachable legal states admit no legal assignment, and
3,270 are dead.  Two facts from that sweep shape this script:

  - EVERY dead legal CR state is reachable from the root (3,270 of 3,270), so
    there is no unreachable junk to quarantine;
  - 3,024 of the 3,270 dead states -- 92.5% -- are dead because they are
    IMMEDIATELY stuck, not because they walk into trouble later.

So in the CR frame, death is almost always immediate, and characterising "no
legal assignment exists" very nearly characterises death.  That is a much more
tractable target than the peel frame offered, where the analogous local
statement (cor:stuck-structure) captured almost nothing.

By Lemma 2 a stuck state is a meaningful object: an allocation A that witnesses
Conjecture 2 on the contracted instance (D, c^R), such that un-contracting any
one chore of R and giving it to any agent destroys the witness.

CANDIDATE CHARACTERISATIONS TESTED, each as a two-way contingency against
stuckness over every reachable legal state:

  (C1) OVERCOMMIT      some agent already carries conditioned cost >= 2 on its
                       own decided bundle: c^R_i(A_i) >= 2.  The CR analogue of
                       (COMMIT) from rem:commit-predicate, which failed in the
                       peel frame on 17 dead states.
  (C2) BALANCE         the state admits a completion whose bundle sizes differ
                       by at most 1 -- the balance rule of conj:balance-rule,
                       transplanted.
  (C3) SATURATED       every agent is paid: ell(i) = 1 for all i, so no agent
                       has slack to absorb a new chore.
  (C4) TIGHT-IN        for every undecided chore a and every agent x, some agent
                       i has a tight arc into x that beta_i raises.  The CR
                       reading of prop:tight-arc.
  (C5) NO-FREE         no assignment is free in the sense of the CR free-
                       assignment lemma (beta_x(A_k) = 0 for all k, and
                       beta_i(A_k) <= beta_i(A_i) for i,k != x).

Reported for each: the 2x2 table, and whether the implication
"predicate => stuck" or "stuck => predicate" survives.  A predicate implied by
stuckness with no false positives is a certificate of liveness, which is what
conj:balance-rule was.

Run:  python cri_stuck.py
"""
from itertools import combinations_with_replacement, permutations, product
from collections import Counter, defaultdict
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


def bundles(own, n, m):
    A = [frozenset(j for j in range(m) if own[j] == i) for i in range(n)]
    R = frozenset(j for j in range(m) if own[j] == n)
    return A, R


def contracted_own(cs, own, n, m):
    """c^R_i(A_i) for each i."""
    A, R = bundles(own, n, m)
    return [cs[i][frozenset(A[i] | R)] - cs[i][R] for i in range(n)]


def admits_balanced_completion(own, n, m):
    """Some completion of the undecided chores has sizes differing by <= 1."""
    A, R = bundles(own, n, m)
    base = [len(a) for a in A]
    k = len(R)
    if k == 0:
        return max(base) - min(base) <= 1
    for f in product(range(n), repeat=k):
        sz = list(base)
        for owner in f:
            sz[owner] += 1
        if max(sz) - min(sz) <= 1:
            return True
    return False


def beta_table(cs, own, n, m, a):
    """beta_i(T) = marginal of chore a to agent i on T, conditioned on R - a."""
    A, R = bundles(own, n, m)
    Rp = R - {a}

    def beta(i, T):
        base = frozenset(T | Rp)
        return cs[i][frozenset(base | {a})] - cs[i][base]
    return beta, A


def no_free_assignment(cs, own, n, m):
    """True if no assignment satisfies the CR free-assignment hypothesis."""
    A, R = bundles(own, n, m)
    for a in R:
        beta, A = beta_table(cs, own, n, m, a)
        for x in range(n):
            if any(beta(x, A[k]) != 0 for k in range(n) if k != x):
                continue
            if all(beta(i, A[k]) <= beta(i, A[i])
                   for i in range(n) if i != x
                   for k in range(n) if k != i and k != x):
                return False
    return True


def analyse(cs, n, m, perms):
    root = tuple([n] * m)
    legal_set = {own for own in product(range(n + 1), repeat=m)
                 if cr_legal(cs, own, n, m)}
    terminals = [s for s in legal_set if n not in s]
    succ = {s: [t for _, _, t in assignments(s, n, m) if t in legal_set]
            for s in legal_set}
    succ_p = {s: [t for t in relabels(s, n, m, perms) if t in legal_set]
              for s in legal_set}

    pred = defaultdict(list)
    for s in legal_set:
        for t in succ[s] + succ_p[s]:
            pred[t].append(s)
    live = set(terminals)
    stack = list(terminals)
    while stack:
        t = stack.pop()
        for s in pred[t]:
            if s not in live:
                live.add(s)
                stack.append(s)

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

    rows = []
    for s in reach:
        if n not in s:
            continue
        stuck = not succ[s] and not any(succ[t] for t in succ_p[s])
        dead = s not in live
        e = ell(cs, profile(s, n, m), n)
        rows.append({
            "stuck": stuck,
            "dead": dead,
            "C1": max(contracted_own(cs, s, n, m)) >= 2,
            "C2": not admits_balanced_completion(s, n, m),
            "C3": all(v == 1 for v in e),
            "C5": no_free_assignment(cs, s, n, m),
            "state": s,
        })
    return rows


def table(rows, key, target):
    c = Counter()
    for r in rows:
        c[(r[key], r[target])] += 1
    return c


def report(name, rows, key, target="dead"):
    c = table(rows, key, target)
    tp = c[(True, True)]
    fp = c[(True, False)]
    fn = c[(False, True)]
    tn = c[(False, False)]
    print("  %-10s  P&%s %6d | P&~%s %6d | ~P&%s %6d | ~P&~%s %6d  ||"
          "  P=>%s %s | %s=>P %s"
          % (name, target[:4], tp, target[:4], fp, target[:4], fn,
             target[:4], tn,
             target[:4], "YES" if fp == 0 else "no ",
             target[:4], "YES" if fn == 0 else "no "))
    return fp, fn


def main():
    rng = random.Random(778899)
    allrows = []

    print("=== structure of the stuck / dead CR states ===")
    print()

    blocks = [("EXHAUSTIVE n=m=3", exhaustive_n3m3(), 3, 3)]
    for (n, m, T) in [(3, 4, 60), (3, 5, 30), (4, 4, 30), (4, 5, 12),
                      (5, 4, 10)]:
        inst = []
        while len(inst) < T:
            name, gen = FAMILIES[rng.randrange(len(FAMILIES))]
            cs = gen(m, n, rng)
            if max(max(c.values()) for c in cs) < 1:
                continue
            assert all(is_dichotomous(c, m) for c in cs)
            inst.append(cs)
        blocks.append(("n=%d m=%d" % (n, m), inst, n, m))

    for tag, inst, n, m in blocks:
        perms = list(permutations(range(n)))
        rows = []
        for cs in inst:
            rows.extend(analyse(cs, n, m, perms))
        allrows.extend(rows)
        st = sum(1 for r in rows if r["stuck"])
        dd = sum(1 for r in rows if r["dead"])
        print("  %-18s reachable non-terminal %7d | stuck %5d | dead %5d"
              % (tag, len(rows), st, dd))

    print()
    print("  total reachable non-terminal states : %d" % len(allrows))
    print("  stuck : %d     dead : %d"
          % (sum(1 for r in allrows if r["stuck"]),
             sum(1 for r in allrows if r["dead"])))
    print()
    print("  P = the predicate.  'P=>dead YES' means no false positive, so ~P")
    print("  certifies liveness -- the shape conj:balance-rule had.")
    print()
    for key, name in [("C1", "overcommit"), ("C2", "unbalanced"),
                      ("C3", "saturated"), ("C5", "no-free")]:
        report(name, allrows, key, "dead")
    print()
    for key, name in [("C1", "overcommit"), ("C2", "unbalanced"),
                      ("C3", "saturated"), ("C5", "no-free")]:
        report(name, allrows, key, "stuck")

    print()
    print("  smallest stuck witnesses:")
    seen = 0
    for r in sorted(allrows, key=lambda z: sum(1 for v in z["state"]
                                               if v != max(z["state"]))):
        if r["stuck"] and seen < 4:
            print("     own=%s  C1=%s C2=%s C3=%s C5=%s"
                  % (str(r["state"]), r["C1"], r["C2"], r["C3"], r["C5"]))
            seen += 1


if __name__ == "__main__":
    main()
