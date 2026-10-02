"""
Experiment 5: the sub-case of eligible insertion that BKNS's proof does not
reach, and a candidate proof for it.

HARD CASE. (A,p) envy-free, p in {0,1}^n pointwise-minimal, somebody paid,
and every paid agent sees the new item e as a chore (Elig(e) lies inside the
unpaid set U). Arc weights w(i,j) = v_i(A_j) - v_i(A_i) satisfy
w(i,j) <= p_i - p_j; "tight" means equality.

CANDIDATE RULE. Give e to an eligible x in U. Only eligible onlookers can gain,
and they are unpaid, so the new envy comes from
    G_x = { k in Elig(e) : (k,x) tight, v_k(e | A_x) = 1 }.
Raise G_x to 1 and close backwards over U: an unpaid l tight towards a raised
agent is raised too -- except x itself when v_x(e|A_x) = 1 (its own gain pays
for it). The rule FAILS if the closure Q_x contains x (then x's onlookers would
see +2), or contains an agent with a tight arc from a paid agent (weight 1
into it), who would then need a subsidy of 2.

Measured on every hard state: whether some eligible x has a non-failing
closure, with the bundles where they are and after envy-free reassignments;
and, as a check, that the closure payment really is envy-free.

    python hard_case.py [n] [m] [instances] [seed]
"""
import itertools
import random
import sys

import eqgraph_signed as eg
from ins_eligible import instance, minimal_subsidy


def closure_rule(v, A, p, n, e, x, elig):
    """Payments from the candidate rule, or None if it fails."""
    U = [i for i in range(n) if p[i] == 0]
    w = [[v[i][A[j]] - v[i][A[i]] for j in range(n)] for i in range(n)]
    tight = {(i, j) for i in range(n) for j in range(n)
             if i != j and w[i][j] == p[i] - p[j]}
    own_gain = eg.marg(v, x, e, A[x]) == 1
    Q = {k for k in elig if k != x and (k, x) in tight
         and eg.marg(v, k, e, A[x]) == 1}
    frontier = list(Q)
    while frontier:
        q = frontier.pop()
        for l in U:
            if l not in Q and (l, q) in tight and not (l == x and own_gain):
                Q.add(l)
                frontier.append(l)
    if x in Q:
        return None
    if any((l, q) in tight and p[l] == 1 for q in Q for l in range(n)):
        return None
    return [1 if (i in Q or p[i] == 1) else 0 for i in range(n)]


def ef_with(v, A, p, n):
    return all(v[i][A[i]] + p[i] >= v[i][A[j]] + p[j]
               for i in range(n) for j in range(n))


def package_perms(v, A, p, n):
    """Reassignments of (bundle, subsidy) packages that leave every agent's
    subsidised value unchanged; identity first."""
    ident = tuple(range(n))
    out = [ident]
    for perm in itertools.permutations(range(n)):
        if perm != ident and all(v[i][A[perm[i]]] + p[perm[i]] == v[i][A[i]] + p[i]
                                 for i in range(n)):
            out.append(perm)
    return out


def extend_case(v, A, p, n, e, elig):
    """BKNS Case 1 under package-preserving reassignments: some eligible agent
    ends up holding a PAID package and values e at +1 on it; it takes e and
    gives up the payment. Returns True if some reassignment allows it."""
    for perm in package_perms(v, A, p, n):
        B = [A[perm[i]] for i in range(n)]
        q = [p[perm[i]] for i in range(n)]
        for x in sorted(elig):
            if q[x] == 1 and eg.marg(v, x, e, B[x]) == 1:
                Bf = list(B)
                Bf[x] |= 1 << e
                q2 = list(q)
                q2[x] = 0
                assert ef_with(v, Bf, q2, n), "Extend step not envy-free"
                return True
    return False


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    m = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    instances = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    rng = random.Random(seed)
    e = m - 1
    hard = rule_ok_noperm = rule_ok_perm = free_noperm = extendable = 0
    rule_payment_not_ef = 0
    shown = 0
    for _ in range(instances):
        v, cmask, elig = instance(n, m, rng)
        for owners in itertools.product(range(n), repeat=m - 1):
            A = [0] * n
            for b, o in enumerate(owners):
                A[o] |= 1 << b
            s = eg.max_min_subsidy(v, A, n)
            if s is None or s > 1:
                continue
            p = minimal_subsidy(v, A, n)
            paid = {i for i in range(n) if p[i] == 1}
            if not paid or paid & elig:
                continue
            hard += 1
            if extend_case(v, A, p, n, e, elig):
                extendable += 1
                continue
            ok0 = free0 = False
            for x in sorted(elig):
                pay = closure_rule(v, A, p, n, e, x, elig)
                if pay is None:
                    continue
                Af = list(A)
                Af[x] |= 1 << e
                if not ef_with(v, Af, pay, n):
                    rule_payment_not_ef += 1
                    continue
                ok0 = True
                free0 = free0 or pay == p
            rule_ok_noperm += ok0
            free_noperm += free0
            okp = ok0
            if not okp:
                # envy-free reassignments of the bundles, paying p along
                for perm in itertools.permutations(range(n)):
                    if all(v[i][A[perm[i]]] + p[perm[i]] == v[i][A[i]] + p[i]
                           for i in range(n)):
                        B = [A[perm[i]] for i in range(n)]
                        q = [p[perm[i]] for i in range(n)]
                        if q != minimal_subsidy(v, B, n):
                            continue
                        for x in sorted(elig):
                            pay = closure_rule(v, B, q, n, e, x, elig)
                            if pay is not None:
                                Bf = list(B)
                                Bf[x] |= 1 << e
                                if ef_with(v, Bf, pay, n):
                                    okp = True
                                    break
                        if okp:
                            break
            rule_ok_perm += okp
            if not okp and shown < 3:
                shown += 1
                print("--- closure rule fails: elig", sorted(elig), " p", p,
                      " w-matrix", [[v[i][A[j]] - v[i][A[i]] for j in range(n)] for i in range(n)],
                      " gains of e on X_j", [[eg.marg(v, i, e, A[j]) for j in range(n)] for i in range(n)])
                print("    bundles", [bin(S) for S in A], " chore masks", [bin(c) for c in cmask])
                for k in range(n):                       # what DOES work?
                    B = list(A)
                    B[k] |= 1 << e
                    for perm in itertools.permutations(range(n)):
                        Af = [B[perm[i]] for i in range(n)]
                        sub = eg.max_min_subsidy(v, Af, n)
                        holder = perm.index(k)
                        if sub is not None and sub <= 1 and holder in elig:
                            print("    works: e into bundle of agent", k, "; agent i takes old bundle of",
                                  list(perm), "; holder", holder,
                                  "; new minimal subsidy", minimal_subsidy(v, Af, n),
                                  "; new values", [[v[i][Af[j]] for j in range(n)] for i in range(n)])
    print()
    print("n=%d m=%d instances=%d seed=%d" % (n, m, instances, seed))
    print("hard states                                   : %d" % hard)
    print("  extendable (BKNS Case 1 via package swaps)  : %d" % extendable)
    print("  non-extendable                              : %d" % (hard - extendable))
    print("non-extendable: closure rule works, as is     : %d" % rule_ok_noperm)
    print("   ... and it is free insertion (no new payment): %d" % free_noperm)
    print("non-extendable: closure rule works, w/ reassign: %d" % rule_ok_perm)
    print("closure payment computed but NOT envy-free    : %d   (must be 0)" % rule_payment_not_ef)


if __name__ == "__main__":
    main()
