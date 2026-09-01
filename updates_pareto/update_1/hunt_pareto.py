"""
Does Algorithm 1 return a Pareto optimal allocation?

Two questions, deliberately separated, because they have very different
consequences for the paper.

  (Q1) WEAK -- does the algorithm, as specified, ever output a non-PO
       allocation? A single instance settles this. It says the algorithm does
       not GUARANTEE PO; it leaves open whether a smarter tie-breaking rule
       inside the same construction would.

  (Q2) STRONG -- is there an instance in which NO allocation admitting an
       envy-free solution with p in {0,1}^n is Pareto optimal? That would say
       the paper's guarantee and PO are outright incompatible, so no repair of
       the algorithm could recover PO, and the answer to the supervisor is
       final rather than provisional.

A third measurement is reported because it bears on how to phrase any claim:

  (Q3) among the instances where the algorithm's output is not PO, how often
       does SOME choice of the algorithm's free parameters -- the chore scan
       order, and which agents of the tail component receive the residue --
       yield a PO allocation? If that is usually possible, the defect is
       tie-breaking; if it is usually impossible, it is structural.

Controls. Binary ADDITIVE costs are run separately, since Tao et al. prove
EFX + PO there; a counterexample inside the additive class would be the
sharpest possible form of the answer.
"""
import itertools
import random
import sys

from algo1 import (random_cost, additive_cost, is_valid_cost, algorithm1,
                   is_po, pareto_dominator, cost_profile, min_subsidy,
                   all_allocations)


def valid_allocations(cs, n, m):
    """Complete allocations admitting an envy-free solution with p in {0,1}^n."""
    out = []
    for A in all_allocations(n, m):
        p = min_subsidy(cs, A, n)
        if p is not None and max(p) <= 1:
            out.append((A, p))
    return out


def q2_incompatible(cs, n, m):
    """
    True when no allocation meeting the paper's guarantee is PO. Returns
    (incompatible, n_valid, n_valid_po).
    """
    vs = valid_allocations(cs, n, m)
    po = [A for (A, _) in vs if is_po(cs, A, n, m)]
    return (len(vs) > 0 and len(po) == 0), len(vs), len(po)


def some_choice_is_po(cs, n, m, tries=24, rng=None):
    """
    (Q3): does SOME execution of Algorithm 1 -- varying the chore scan order
    and the recipient set -- produce a PO allocation?
    """
    rng = rng or random.Random(0)
    orders = [list(range(m))]
    for _ in range(tries):
        o = list(range(m))
        rng.shuffle(o)
        orders.append(o)
    for order in orders:
        A, p, info = algorithm1(cs, n, m, order=order)
        if A is None:
            continue
        S = info.get("S")
        r = len(info.get("R", ()))
        if not S or r == 0:
            if A is not None and is_po(cs, A, n, m):
                return True
            continue
        for T in itertools.permutations(S, r):
            A2, p2, _ = algorithm1(cs, n, m, order=order, recipients=T)
            if A2 is not None and is_po(cs, A2, n, m):
                return True
    return False


def sweep(label, sampler, n, m, trials, seed, show=2):
    rng = random.Random(seed)
    stat = {"runs": 0, "cap": 0, "r0": 0, "notPO": 0, "incompat": 0,
            "notPO_fixable": 0, "notPO_unfixable": 0}
    shown = 0
    witnesses = []

    for _ in range(trials):
        cs = tuple(sampler(m, rng) for _ in range(n))
        if not all(is_valid_cost(c, m) for c in cs):
            continue
        A, p, info = algorithm1(cs, n, m)
        if A is None:
            stat["cap"] += 1
            continue
        stat["runs"] += 1
        if info["status"] == "r0":
            stat["r0"] += 1

        if not is_po(cs, A, n, m):
            stat["notPO"] += 1
            fixable = some_choice_is_po(cs, n, m, rng=rng)
            stat["notPO_fixable" if fixable else "notPO_unfixable"] += 1
            if shown < show:
                shown += 1
                witnesses.append((cs, A, p, info, fixable))

        inc, nv, npo = q2_incompatible(cs, n, m)
        if inc:
            stat["incompat"] += 1
            witnesses.append((cs, A, p, dict(info, INCOMPAT=(nv, npo)), None))

    print("  %-26s n=%d m=%d : %d runs (%d with empty residue, %d capped)"
          % (label, n, m, stat["runs"], stat["r0"], stat["cap"]))
    print("     (Q1) output NOT Pareto optimal      : %d" % stat["notPO"])
    print("          ...but some free choice is PO  : %d" % stat["notPO_fixable"])
    print("          ...no free choice is PO        : %d" % stat["notPO_unfixable"])
    print("     (Q2) NO valid allocation is PO      : %d" % stat["incompat"])
    return stat, witnesses


def show_witness(cs, A, p, info, fixable, n, m):
    names = "abcdefgh"[:m]

    def bundle(x):
        return "{" + ",".join(names[k] for k in range(m) if x & (1 << k)) + "}"

    print("     ---- witness ----")
    for i in range(n):
        print("        agent %d cost table %s" % (i + 1, str(cs[i])))
    print("        X = %s   R = %s   S = %s   T = %s   P = %s"
          % (" ".join(bundle(x) for x in info.get("X", ())),
             info.get("R"), info.get("S"), info.get("T"), info.get("P")))
    print("        A = %s   p = %s   costs = %s"
          % (" ".join(bundle(x) for x in A), p, cost_profile(cs, A, n)))
    D = pareto_dominator(cs, A, n, m)
    if D is not None:
        print("        dominated by %s costs = %s"
              % (" ".join(bundle(x) for x in D), cost_profile(cs, D, n)))
    if fixable is not None:
        print("        some free choice PO? %s" % fixable)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "small"

    print("Is the allocation returned by Algorithm 1 Pareto optimal?")
    print()

    def general(m, rng):
        return random_cost(m, rng)

    def additive(m, rng):
        return additive_cost(m, [rng.randint(0, 1) for _ in range(m)])

    if mode == "small":
        plan = ((3, 3, 3000), (3, 4, 1500), (4, 4, 800))
    else:
        plan = ((3, 5, 600), (4, 5, 300), (5, 5, 150))

    for (n, m, trials) in plan:
        st, ws = sweep("general binary marginals", general, n, m, trials,
                       seed=1000 + 10 * n + m)
        for w in ws[:2]:
            show_witness(w[0], w[1], w[2], w[3], w[4], n, m)
        st2, ws2 = sweep("control: binary additive", additive, n, m, trials,
                         seed=2000 + 10 * n + m)
        for w in ws2[:2]:
            show_witness(w[0], w[1], w[2], w[3], w[4], n, m)
        print()


if __name__ == "__main__":
    main()
