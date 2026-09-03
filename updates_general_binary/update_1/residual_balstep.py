"""
(BAL-STEP), residual case: what is left after the free-insertion lemma.

Section 33 of approach_15.md proves the free-insertion fragment. In the chores
class its hypothesis reduces to "the chore is free for its recipient",
v_x(g | A_x) = 0, which is Tao-Wu-Yu-Zhou's rule (R1). This script measures
what happens on the states that rule does NOT cover:

    FREE   some minimum-size bundle A_x has v_x(g | A_x) = 0
    HARD   every minimum-size bundle A_x has v_x(g | A_x) = -1

and, on the HARD states, which repair is actually needed:

    ID     inserting into some minimum-size bundle works with the agents left
           where they are (only the subsidy vector is recomputed)
    PERM   no minimum-size bundle works under the identity, but some bundle
           plus a genuine reassignment does
    FAIL   nothing works -- would refute (BAL-STEP)

The point is to find out whether a proof has to carry a reassignment argument
at all, or whether the identity always suffices once the recipient is chosen.
Chores are the class run here; by the duality of section 23 the goods half is
the same statement.
"""
import itertools
import random
import sys

from gb_valuations import (
    enumerate_class,
    arc_weights,
    is_envy_freeable,
    longest_paths,
)


def valid(vals, b):
    if not is_envy_freeable(vals, b):
        return False
    return all(q <= 1 for q in longest_paths(arc_weights(vals, b)))


def sizes(b):
    return [bin(x).count("1") for x in b]


def balanced(b):
    s = sizes(b)
    return max(s) - min(s) <= 1


def analyse(vals, n, m):
    """Returns counters over every (valid balanced state, unallocated g)."""
    stat = {"states": 0, "free": 0, "hard": 0,
            "hard_id": 0, "hard_perm": 0, "hard_fail": 0}
    witnesses = []

    for assign in itertools.product(list(range(n)) + [None], repeat=m):
        b = [0] * n
        for k, owner in enumerate(assign):
            if owner is not None:
                b[owner] |= 1 << k
        b = tuple(b)
        if not balanced(b) or not valid(vals, b):
            continue
        unalloc = [k for k in range(m) if assign[k] is None]
        if not unalloc:
            continue
        s = sizes(b)
        lo = min(s)
        L = [i for i in range(n) if s[i] == lo]

        for g in unalloc:
            stat["states"] += 1
            bit = 1 << g

            # FREE: the chore is free for the owner of some minimum bundle
            if any(vals[x][b[x] | bit] - vals[x][b[x]] == 0 for x in L):
                stat["free"] += 1
                continue
            stat["hard"] += 1

            # identity insertion into some minimum-size bundle
            id_ok = False
            for x in L:
                nb = list(b)
                nb[x] |= bit
                if valid(vals, tuple(nb)):
                    id_ok = True
                    break
            if id_ok:
                stat["hard_id"] += 1
                continue

            # any minimum-size bundle, any reassignment of the new bundles
            perm_ok = False
            for x in L:
                nb = list(b)
                nb[x] |= bit
                for perm in itertools.permutations(range(n)):
                    cand = tuple(nb[perm[i]] for i in range(n))
                    if balanced(cand) and valid(vals, cand):
                        perm_ok = True
                        break
                if perm_ok:
                    break
            if perm_ok:
                stat["hard_perm"] += 1
                if len(witnesses) < 3:
                    witnesses.append((vals, b, g, list(L)))
            else:
                stat["hard_fail"] += 1
                witnesses.append(("FAIL", vals, b, g, list(L)))
    return stat, witnesses


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "exhaustive"
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    m = int(sys.argv[3]) if len(sys.argv) > 3 else 3

    pool = enumerate_class(m, {-1, 0})
    print("chores valuations on m=%d: %d" % (m, len(pool)))

    if mode == "exhaustive":
        tuples = itertools.product(pool, repeat=n)
        total = len(pool) ** n
    else:
        k = int(sys.argv[4]) if len(sys.argv) > 4 else 3000
        rng = random.Random(20260903)
        tuples = (tuple(rng.choice(pool) for _ in range(n)) for _ in range(k))
        total = k
    print("valuation tuples: %d  (n=%d, m=%d)" % (total, n, m))

    agg = {"states": 0, "free": 0, "hard": 0,
           "hard_id": 0, "hard_perm": 0, "hard_fail": 0}
    all_wit = []
    for vals in tuples:
        st, wit = analyse(list(vals), n, m)
        for k2 in agg:
            agg[k2] += st[k2]
        for w in wit:
            if w[0] == "FAIL":
                all_wit.append(w)

    print()
    print("(state, unallocated chore) pairs on valid balanced states : %d"
          % agg["states"])
    print("   FREE  (rule R1 applies, free-insertion lemma covers it)  : %d"
          % agg["free"])
    print("   HARD  (chore costs every minimum-bundle owner)           : %d"
          % agg["hard"])
    if agg["hard"]:
        print("      of the HARD ones:")
        print("         identity insertion suffices  : %d" % agg["hard_id"])
        print("         reassignment REQUIRED        : %d" % agg["hard_perm"])
        print("         no move at all (refutes)     : %d" % agg["hard_fail"])
    if all_wit:
        print()
        print("REFUTING WITNESSES: %d" % len(all_wit))
        for w in all_wit[:3]:
            print("   vals=%s bundles=%s g=%d minbundles=%s"
                  % (w[1], w[2], w[3], w[4]))


if __name__ == "__main__":
    main()
