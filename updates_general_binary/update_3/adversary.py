"""
Experiment 6: a hill-climbing adversary against the halting-state claims.

Random instances are mostly easy (about 9 in 10 finish with no subsidy at all),
so they are weak evidence. This searches for instances that break, at a state
where no envy-free extension is left (eqgraph_maximal.maximal_phase):

  MIXED      leftover goods-type items AND leftover chores-for-everyone
  UNMATCH    leftover goods-type items admit no injective assignment to
             agents each valuing its item at +1 on its own bundle
  STRUCT     the structured completion fails
  DEAD       no completion at all keeps the subsidy at most 1

Score (larger is worse for the conjectures): leftovers at the halt, plus large
bonuses for each violation; the worst of several runs of the randomised phase.
Mutations: redraw one agent's base function u_i, or flip one item's sign (for
one agent in doubly monotone mode, for everyone in objective mode).

    python adversary.py [n] [m] [restarts] [climb] [seed] [mode]
"""
import random
import sys

import eqgraph_signed as eg
import eqgraph_maximal as em


def build(us, cmask, m):
    return [eg.signed_from_u(us[i], m, cmask[i]) for i in range(len(us))]


def evaluate(us, cmask, n, m, runs, seed):
    v = build(us, cmask, m)
    worst, info = -1, None
    for r in range(runs):
        rng = random.Random(seed * 1000 + r)
        X, R, _ = em.maximal_phase(v, n, m, cmask, rng)
        if not R:
            score, flags = 0, ()
        else:
            h = eg.halting_report(v, X, R, n, cmask)
            flags = []
            if h["chores"] and h["goods"]:
                flags.append("MIXED")
            if h["goods"] and eg.sdr(h["goods"], list(range(n)),
                                     lambda g, t: eg.marg(v, t, g, X[t]) == 1) is None:
                flags.append("UNMATCH")
            if not em.struct_completion(v, X, R, n, cmask):
                flags.append("STRUCT")
                if not eg.exists_unit_completion(v, X, R, n, permute=True):
                    flags.append("DEAD")
            score = len(R) + 100 * len(flags) + (10000 if "DEAD" in flags else 0)
        if score > worst:
            worst, info = score, (X, sorted(R), tuple(flags))
    return worst, info


def mutate(us, cmask, n, m, mode, rng, p_one):
    us = [list(u) for u in us]
    cmask = list(cmask)
    if rng.random() < 0.5:
        i = rng.randrange(n)
        gen = rng.choice([eg.random_binary_monotone, eg.additive_binary])
        us[i] = gen(m, rng, p_one)
    else:
        b = rng.randrange(m)
        if mode == "objective":
            cmask = [c ^ (1 << b) for c in cmask]
        else:
            i = rng.randrange(n)
            cmask[i] ^= 1 << b
    return us, cmask


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    m = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    restarts = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    climb = int(sys.argv[4]) if len(sys.argv) > 4 else 300
    seed = int(sys.argv[5]) if len(sys.argv) > 5 else 1
    mode = sys.argv[6] if len(sys.argv) > 6 else "objective"
    rng = random.Random(seed)
    best_overall = (-1, None)
    flag_hits = {}
    for rs in range(restarts):
        p_one = rng.choice([0.3, 0.5, 0.7])
        v0, cmask = eg.random_instance(n, m, rng, mode, "random", 0.5, p_one)
        us = [[v0[i][S] + bin(S & cmask[i]).count("1") for S in range(1 << m)]
              for i in range(n)]
        cur, info = evaluate(us, cmask, n, m, 3, rs)
        for _ in range(climb):
            us2, cm2 = mutate(us, cmask, n, m, mode, rng, p_one)
            sc, inf2 = evaluate(us2, cm2, n, m, 3, rs)
            if sc >= cur:
                us, cmask, cur, info = us2, cm2, sc, inf2
                for f in info[2]:
                    flag_hits[f] = flag_hits.get(f, 0) + 1
        if cur > best_overall[0]:
            best_overall = (cur, (us, cmask, info))
        print("restart %2d  score %5d  flags %s  leftovers %s"
              % (rs, cur, info[2] if info else (), info[1] if info else []), flush=True)
    print()
    print("n=%d m=%d mode=%s  best score %d" % (n, m, mode, best_overall[0]))
    print("flag hits along the climbs:", flag_hits)
    if best_overall[1] is not None:
        us, cmask, info = best_overall[1]
        print("worst instance: chore masks", [bin(c) for c in cmask])
        print("  halting X", [bin(S) for S in info[0]], " leftovers", info[1], " flags", info[2])
        print("  u tables:", [tuple(u) for u in us])


if __name__ == "__main__":
    main()
