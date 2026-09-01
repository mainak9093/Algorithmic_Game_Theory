"""
The two questions the first sweep left open, tested harder and faster.

  (Q2) Is there an instance in which NO allocation meeting the paper's
       guarantee -- envy-free with p in {0,1}^n -- is Pareto optimal? If such
       an instance exists, PO is outright incompatible with the theorem and no
       repair of the algorithm could recover it. The first sweep found none at
       small sizes; this pushes further.

  (CTRL) Binary ADDITIVE costs, where Tao et al. prove EFX + PO by a different
       route. The first sweep saw zero non-PO outputs there across 5300 runs.
       Is that robust, or an artefact of small instances?

Speed. Cost profiles for all n^m allocations are computed once per instance and
reused for both the PO test and the domination search, and the minimal-subsidy
routine is only invoked on allocations that survive the cheap checks.
"""
import itertools
import random
import sys

from algo1 import (random_cost, additive_cost, is_valid_cost, algorithm1,
                   min_subsidy, all_allocations)


def profiles(cs, allocs, n):
    return [tuple(cs[i][A[i]] for i in range(n)) for A in allocs]


def po_flags(profs, n):
    """po[k] is True when no other profile Pareto dominates profs[k]."""
    L = len(profs)
    po = [True] * L
    for a in range(L):
        pa = profs[a]
        for b in range(L):
            if b == a:
                continue
            pb = profs[b]
            if all(pb[i] <= pa[i] for i in range(n)) and \
               any(pb[i] < pa[i] for i in range(n)):
                po[a] = False
                break
    return po


def analyse(cs, n, m, allocs):
    """Returns (algo_output_is_po, n_valid, n_valid_and_po)."""
    profs = profiles(cs, allocs, n)
    po = po_flags(profs, n)
    index = {A: k for k, A in enumerate(allocs)}

    A, p, info = algorithm1(cs, n, m)
    algo_po = None
    if A is not None:
        algo_po = po[index[A]]

    n_valid = n_valid_po = 0
    for k, B in enumerate(allocs):
        q = min_subsidy(cs, B, n)
        if q is None or max(q) > 1:
            continue
        n_valid += 1
        if po[k]:
            n_valid_po += 1
    return algo_po, n_valid, n_valid_po


def sweep(label, sampler, n, m, trials, seed):
    rng = random.Random(seed)
    allocs = list(all_allocations(n, m))
    runs = notpo = incompat = novalid = 0
    witness = None

    for _ in range(trials):
        cs = tuple(sampler(m, rng) for _ in range(n))
        if not all(is_valid_cost(c, m) for c in cs):
            continue
        algo_po, nv, nvpo = analyse(cs, n, m, allocs)
        if algo_po is None:
            continue
        runs += 1
        if not algo_po:
            notpo += 1
        if nv == 0:
            novalid += 1
        elif nvpo == 0:
            incompat += 1
            if witness is None:
                witness = cs

    print("  %-24s n=%d m=%d : %d runs" % (label, n, m, runs))
    print("     algorithm output not PO            : %d  (%.1f%%)"
          % (notpo, 100.0 * notpo / max(runs, 1)))
    print("     NO valid allocation is PO  (Q2)    : %d" % incompat)
    if novalid:
        print("     instances with no valid allocation : %d  (cannot happen"
              " -- investigate)" % novalid)
    if witness is not None:
        print("     Q2 witness:")
        for i, c in enumerate(witness):
            print("        agent %d %s" % (i + 1, str(c)))
    return notpo, incompat


def main():
    print("Q2 (is PO incompatible with the guarantee?) and the additive control")
    print()

    def general(m, rng):
        return random_cost(m, rng)

    def additive(m, rng):
        return additive_cost(m, [rng.randint(0, 1) for _ in range(m)])

    plan = [(3, 3, 8000), (3, 4, 4000), (4, 4, 2000), (3, 5, 1200)]
    if len(sys.argv) > 1 and sys.argv[1] == "big":
        plan = [(4, 5, 300), (5, 5, 120)]

    tot_inc = 0
    for (n, m, trials) in plan:
        _, inc = sweep("general binary", general, n, m, trials,
                       seed=3000 + 10 * n + m)
        tot_inc += inc
        sweep("control: additive", additive, n, m, trials,
              seed=4000 + 10 * n + m)
        print()
    print("total Q2 incompatibility witnesses: %d" % tot_inc)


if __name__ == "__main__":
    main()
