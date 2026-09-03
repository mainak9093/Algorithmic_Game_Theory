"""
Two provable insertion rules, and how much of (BAL-STEP) they cover.

Read the subsidy as a PRICE on the bundle (demand_form.py verifies this is the
same thing): a state is valid exactly when every agent holds a bundle
maximising v_i(B) + q_B for prices q in {0,1}. Insert g into B_x and write
d_i = c_i(g | B_x) in {0,1} for the marginal cost of g to agent i at B_x.

RULE 1 (free insertion, section 33). If the agent holding B_x has d = 0, no
arc weight rises, so the state stays valid with the SAME assignment and SAME
prices. In the chores class this is Tao-Wu-Yu-Zhou's rule (R1).

RULE 2 (uniform cost -- new here). Suppose q_x = 0 and d_i = 1 for EVERY agent
i. Raise the price of position x to 1. The score of x for agent i changes by
-d_i + 1 = 0, and every other score is untouched, so every agent's demand set
is EXACTLY as before and the old matching still works. The state is valid.

Rule 2 is what covers the case Rule 1 cannot: the chore is not free for its
holder. The two hypotheses are complementary in d, so the question this script
answers is how much of the residual is left once BOTH are applied, and what
the leftover looks like.
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


def subsidy(vals, b):
    """Minimal subsidy vector, or None if the state is not valid."""
    if not is_envy_freeable(vals, b):
        return None
    l = longest_paths(arc_weights(vals, b))
    return l if all(q <= 1 for q in l) else None


def valid(vals, b):
    return subsidy(vals, b) is not None


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "exhaustive"
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    m = int(sys.argv[3]) if len(sys.argv) > 3 else 3

    pool = enumerate_class(m, {-1, 0})
    if mode == "exhaustive":
        tuples = list(itertools.product(pool, repeat=n))
    else:
        k = int(sys.argv[4]) if len(sys.argv) > 4 else 400
        rng = random.Random(20260903)
        tuples = [tuple(rng.choice(pool) for _ in range(n)) for _ in range(k)]
    print("chores class m=%d: %d valuations; tuples: %d"
          % (m, len(pool), len(tuples)))

    c = {"pairs": 0, "r1": 0, "r2": 0, "left": 0,
         "r1_bad": 0, "r2_bad": 0, "left_ok": 0, "left_fail": 0}
    leftovers = []

    for vals in tuples:
        vals = list(vals)
        for assign in itertools.product(list(range(n)) + [None], repeat=m):
            b = [0] * n
            for k2, owner in enumerate(assign):
                if owner is not None:
                    b[owner] |= 1 << k2
            b = tuple(b)
            s = [bin(x).count("1") for x in b]
            if max(s) - min(s) > 1:
                continue
            p = subsidy(vals, b)
            if p is None:
                continue
            unalloc = [k2 for k2 in range(m) if assign[k2] is None]
            lo = min(s)
            L = [i for i in range(n) if s[i] == lo]

            for g in unalloc:
                c["pairs"] += 1
                bit = 1 << g
                d = {x: [vals[i][b[x]] - vals[i][b[x] | bit] for i in range(n)]
                     for x in L}

                # RULE 1: free for the holder of some minimum bundle
                r1 = [x for x in L if d[x][x] == 0]
                if r1:
                    c["r1"] += 1
                    x = r1[0]
                    nb = list(b)
                    nb[x] |= bit
                    if not valid(vals, tuple(nb)):
                        c["r1_bad"] += 1
                    continue

                # RULE 2: unsubsidised holder, chore costs everybody
                r2 = [x for x in L if p[x] == 0 and all(t == 1 for t in d[x])]
                if r2:
                    c["r2"] += 1
                    x = r2[0]
                    nb = list(b)
                    nb[x] |= bit
                    if not valid(vals, tuple(nb)):
                        c["r2_bad"] += 1
                    continue

                c["left"] += 1
                ok = False
                for x in L:
                    nb = list(b)
                    nb[x] |= bit
                    for perm in itertools.permutations(range(n)):
                        if valid(vals, tuple(nb[perm[i]] for i in range(n))):
                            ok = True
                            break
                    if ok:
                        break
                c["left_ok" if ok else "left_fail"] += 1
                if len(leftovers) < 6:
                    leftovers.append((list(vals), b, g, list(L), list(p),
                                      {x: d[x] for x in L}))

    print()
    print("(valid balanced state, unallocated chore) pairs : %d" % c["pairs"])
    print("   RULE 1 applies (free for a min-bundle holder): %-8d  violations: %d"
          % (c["r1"], c["r1_bad"]))
    print("   RULE 2 applies (unsubsidised, costs everyone): %-8d  violations: %d"
          % (c["r2"], c["r2_bad"]))
    print("   NEITHER rule applies                         : %-8d" % c["left"])
    if c["left"]:
        print("      of those, some move still works           : %d" % c["left_ok"])
        print("      of those, NOTHING works (refutes BAL-STEP) : %d" % c["left_fail"])
        print()
        print("LEFTOVER SHAPES (what a third rule must handle):")
        for w in leftovers:
            print("   bundles=%s g=%d L=%s p=%s d=%s"
                  % (w[1], w[2], w[3], w[4], w[5]))


if __name__ == "__main__":
    main()
