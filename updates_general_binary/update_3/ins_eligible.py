"""
Experiment 3: the one-item insertion step for a DOUBLY MONOTONE item.

The objective proof inserts goods one at a time (BKNS Extend/FindSink,
Lemma 4.1 of the AAMAS paper). Approach 15 tested that step (INS-G) only for a
UNIVERSAL good. In a doubly monotone instance an item e can be a good for the
agents in Elig(e) (marginals in {0,1} on every bundle) and a chore for the rest
(marginals in {-1,0}). Path-increment lemma: if e lands with an ELIGIBLE
holder, arcs out of the holder do not rise and arcs into it rise by at most 1,
exactly as for a universal good, because ineligible onlookers can only lose.
So the natural statement to test is

  (INS-E)  Let (A,p) be an envy-free solution of the other items whose minimal
           subsidy lies in {0,1}^n, and e a doubly monotone item with
           Elig(e) nonempty. Then e can be added to some bundle, under some
           reassignment of the bundles, so that the minimal subsidy stays in
           {0,1}^n -- and (INS-E-elig) with the holder of e eligible.

If (INS-E-elig) holds, doubly monotone dichotomous valuations follow from the
existing architecture: chores-for-everyone first (Tao + our completion), then
every other item one at a time. Every state with all other items allocated is
enumerated, for random instances.

    python ins_eligible.py [n] [m] [instances] [seed]
"""
import itertools
import random
import sys

import eqgraph_signed as eg


def instance(n, m, rng):
    """Doubly monotone on all items; the last item is MIXED: a good for a
    nonempty proper subset of agents, a chore for the others."""
    while True:
        cmask = [sum(1 << b for b in range(m - 1) if rng.random() < 0.5)
                 for _ in range(n)]
        elig = [i for i in range(n) if rng.random() < 0.5]
        if 0 < len(elig) < n:
            break
    e = m - 1
    for i in range(n):
        if i not in elig:
            cmask[i] |= 1 << e
    gen = rng.choice([eg.random_binary_monotone, eg.additive_binary])
    p_one = rng.choice([0.3, 0.5, 0.7])
    v = [eg.signed_from_u(gen(m, rng, p_one), m, cmask[i]) for i in range(n)]
    for i in range(n):
        assert eg.is_signed_dichotomous(v[i], m, cmask[i])
    return v, cmask, set(elig)


def envy_freeable_perms(v, B, n):
    """All agent->bundle permutations that maximise welfare (these are exactly
    the envy-freeable assignments of the bundle multiset B)."""
    best, out = None, []
    for perm in itertools.permutations(range(n)):
        w = sum(v[i][B[perm[i]]] for i in range(n))
        if best is None or w > best:
            best, out = w, [perm]
        elif w == best:
            out.append(perm)
    return out


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    m = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    instances = int(sys.argv[3]) if len(sys.argv) > 3 else 400
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    rng = random.Random(seed)
    e = m - 1
    states = fail_any = fail_elig = 0
    hard = hard_ok = hard_unpaid_holder = 0   # max p = 1, every paid agent ineligible
    noperm_ok = 0                             # a solution with no reassignment
    shown = 0
    for _ in range(instances):
        v, cmask, elig = instance(n, m, rng)
        for owners in itertools.product(range(n), repeat=m - 1):
            A = [0] * n
            for b, o in enumerate(owners):
                A[o] |= 1 << b
            s = eg.max_min_subsidy(v, A, n)
            if s is None or s > 1:
                continue                      # not a valid state
            states += 1
            p = minimal_subsidy(v, A, n)
            paid = {i for i in range(n) if p[i] == 1}
            is_hard = bool(paid) and not (paid & elig)
            ok_any = ok_elig = ok_noperm = False
            unpaid_holder = False
            for k in range(n):                # e joins bundle k
                B = list(A)
                B[k] |= 1 << e
                for perm in envy_freeable_perms(v, B, n):
                    Af = [B[perm[i]] for i in range(n)]
                    sub = eg.max_min_subsidy(v, Af, n)
                    if sub is None or sub > 1:
                        continue
                    ok_any = True
                    holder = next(i for i in range(n) if perm[i] == k)
                    if holder in elig:
                        ok_elig = True
                        if all(perm[i] == i for i in range(n)):
                            ok_noperm = True
                        if p[holder] == 0:
                            unpaid_holder = True
            fail_any += not ok_any
            fail_elig += not ok_elig
            noperm_ok += ok_noperm
            if is_hard:
                hard += 1
                hard_ok += ok_elig
                hard_unpaid_holder += unpaid_holder
            if not ok_elig and shown < 3:
                shown += 1
                print("--- (INS-E-elig) fails%s" % ("" if ok_any else ", and so does (INS-E)"))
                print("  eligible for e:", sorted(elig), "  chore masks", [bin(c) for c in cmask])
                print("  state", [bin(S) for S in A], " values matrix",
                      [[v[i][A[j]] for j in range(n)] for i in range(n)])
    print()
    print("n=%d m=%d instances=%d seed=%d" % (n, m, instances, seed))
    print("valid states tested       : %d" % states)
    print("(INS-E)      failures     : %d" % fail_any)
    print("(INS-E-elig) failures     : %d" % fail_elig)
    print("solvable with no reassignment (eligible holder): %d" % noperm_ok)
    print("hard states (someone paid, every paid agent ineligible): %d" % hard)
    print("   of which solvable (eligible holder)        : %d" % hard_ok)
    print("   of which solvable with an UNPAID eligible holder: %d" % hard_unpaid_holder)


def minimal_subsidy(v, A, n):
    """Pointwise-minimal subsidy vector (longest paths, Floyd-Warshall)."""
    d = [[(v[i][A[j]] - v[i][A[i]]) if i != j else 0 for j in range(n)]
         for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] > d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return [max(row) for row in d]


if __name__ == "__main__":
    main()
