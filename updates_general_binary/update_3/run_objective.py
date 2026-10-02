"""
Experiment 1: run the equality-graph rules on random OBJECTIVE signed
dichotomous instances and examine the halting states.

    python run_objective.py [n] [m] [trials] [seed] [order] [family]

For each instance the rules run to a halt (random tie-breaking among moves of
the highest-priority applicable rule), and the halting state is classified:

  complete      every item placed by the rules alone: envy-free, no subsidy
  K-SYM ok      the symmetric one-shot completion has max subsidy <= 1
  unmatchable   the leftover goods cannot be given to distinct agents who
                each value theirs at +1
  K-SYM fail    matchable, but the completion needs a subsidy of 2
  overflow      leftover chores >= the halting tail SCC (should never happen)

and, whenever K-SYM does not succeed, a brute force asks whether ANY
placement of the leftovers works, with and without a reassignment of the
bundles. Counterexamples are printed in full.
"""
import random
import sys
from collections import Counter

import eqgraph_signed as eg


def fmt_bundle(S, m, cm):
    return "{" + ",".join(("c" if cm >> b & 1 else "g") + str(b)
                          for b in range(m) if S >> b & 1) + "}"


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    m = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    trials = int(sys.argv[3]) if len(sys.argv) > 3 else 500
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    order = eg.ORDERS[sys.argv[5]] if len(sys.argv) > 5 else eg.ORDERS["F-ROT-TAIL-SRC"]
    family = sys.argv[6] if len(sys.argv) > 6 else "random"
    rng = random.Random(seed)

    tally = Counter()
    leftover_goods = Counter()
    rule_use = Counter()
    shown = 0
    for t in range(trials):
        v, cmask = eg.random_instance(n, m, rng, "objective", family,
                                      p_chore=rng.choice([0.3, 0.5, 0.7]),
                                      p_one=rng.choice([0.3, 0.5, 0.7]))
        X, R, trace = eg.ef_phase(v, n, m, cmask, order, rng)
        for mv in trace:
            rule_use[mv[0]] += 1
        if not R:
            tally["complete"] += 1
            continue
        h = eg.halting_report(v, X, R, n, cmask)
        leftover_goods[len(h["goods"])] += 1
        status, A = eg.symmetric_completion(v, X, R, n, cmask)
        key = "K-SYM " + status
        if status != "ok":
            noperm = eg.exists_unit_completion(v, X, R, n, permute=False)
            perm = noperm or eg.exists_unit_completion(v, X, R, n, permute=True)
            key += " | any-placement=%s, with-reassignment=%s" % (noperm, perm)
            if shown < 3 and not perm:
                shown += 1
                print("=== uncompletable halting state, trial", t)
                print("chore mask", bin(cmask[0]), "  X =",
                      [fmt_bundle(S, m, cmask[0]) for S in X],
                      "  leftover", sorted(R))
                print("trace", trace)
        tally[key] += 1

    print()
    print("n=%d m=%d trials=%d seed=%d order=%s family=%s"
          % (n, m, trials, seed, "-".join(order), family))
    for k, c in sorted(tally.items(), key=lambda kv: -kv[1]):
        print("  %6d  %s" % (c, k))
    print("  leftover goods at halt:", dict(sorted(leftover_goods.items())))
    print("  rule use:", dict(rule_use))


if __name__ == "__main__":
    main()
