"""
Rule 3: rotate, then insert freely -- and what survives all three rules.

rule_coverage.py leaves a quarter of the states uncovered, and their shape is
always the same: the chore is free for SOME agent on a minimum-size bundle,
just not for the agent currently holding it. The repair is Tao-Wu-Yu-Zhou's
rule (R2) in the language of demand graphs -- reassign the bundles so that the
agent for whom the chore is free ends up holding B_x, then Rule 1 applies.

    RULE 3 (rotate then insert). Suppose there is a minimum-size position x and
    an agent y with c_y(g | B_x) = 0, such that SOME valid assignment of the
    same bundles puts y on x. Reassign to it -- the bundle multiset is
    unchanged, so validity is preserved by construction -- and then Rule 1
    inserts g for free.

The point of the script is the last column: after all three rules, is anything
left? If not, (BAL-STEP) is proved modulo showing Rule 3's reassignment always
exists, which is a statement about rotations in the demand graph alone.
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
        k = int(sys.argv[4]) if len(sys.argv) > 4 else 300
        rng = random.Random(20260903)
        tuples = [tuple(rng.choice(pool) for _ in range(n)) for _ in range(k)]
    print("chores class m=%d: %d valuations; tuples: %d"
          % (m, len(pool), len(tuples)))

    c = {"pairs": 0, "r1": 0, "r2": 0, "r3": 0, "r3_bad": 0,
         "left": 0, "left_ok": 0, "left_fail": 0,
         "r3_nofree": 0, "r3_norot": 0}
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

                if any(d[x][x] == 0 for x in L):
                    c["r1"] += 1
                    continue
                if any(p[x] == 0 and all(t == 1 for t in d[x]) for x in L):
                    c["r2"] += 1
                    continue

                # RULE 3: some agent finds g free on a min bundle, and some
                # valid reassignment of the SAME bundles puts that agent there.
                any_free = False
                done = False
                for x in L:
                    free_agents = [y for y in range(n) if d[x][y] == 0]
                    if free_agents:
                        any_free = True
                    for y in free_agents:
                        for perm in itertools.permutations(range(n)):
                            # perm[i] = position held by agent i
                            if perm[y] != x:
                                continue
                            cand = tuple(b[perm[i]] for i in range(n))
                            if not valid(vals, cand):
                                continue
                            nb = list(cand)
                            nb[y] |= bit
                            c["r3"] += 1
                            if not valid(vals, tuple(nb)):
                                c["r3_bad"] += 1
                            done = True
                            break
                        if done:
                            break
                    if done:
                        break
                if done:
                    continue

                c["left"] += 1
                c["r3_nofree" if not any_free else "r3_norot"] += 1
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
                    leftovers.append((b, g, list(L), list(p),
                                      {x: d[x] for x in L}, ok))

    print()
    print("(valid balanced state, unallocated chore) pairs : %d" % c["pairs"])
    print("   RULE 1  free for the holder                  : %d" % c["r1"])
    print("   RULE 2  unsubsidised, chore costs everyone    : %d" % c["r2"])
    print("   RULE 3  rotate so a free agent holds it       : %-8d violations: %d"
          % (c["r3"], c["r3_bad"]))
    print("   left after all three rules                    : %d" % c["left"])
    if c["left"]:
        print("      no agent finds g free on any min bundle    : %d"
              % c["r3_nofree"])
        print("      free agent exists but no valid rotation    : %d"
              % c["r3_norot"])
        print("      of the leftovers, some move still works    : %d"
              % c["left_ok"])
        print("      of the leftovers, NOTHING works            : %d"
              % c["left_fail"])
        print()
        for w in leftovers:
            print("   bundles=%s g=%d L=%s p=%s d=%s solvable=%s" % w)


if __name__ == "__main__":
    main()
