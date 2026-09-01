"""
Exhaustive settlement at the smallest interesting size, plus two sharper
questions the random sweeps raised.

At m = 3 there are only 38 cost functions with c(empty) = 0 and every marginal
in {0,1}, so all 38^3 = 54,872 ordered three-agent instances can be enumerated.
That turns "the algorithm sometimes fails PO" into an exact count, and settles:

  (a) exactly how many instances the algorithm fails PO on;
  (b) whether NO valid allocation is PO on any of them (Q2), exactly;
  (c) whether every failing instance is non-additive -- the random sweeps saw
      zero failures in the binary additive class across 15,200 runs, and the
      hand-built witness has exactly one non-additivity, so the conjecture is
      that additivity rules the failure out;
  (d) whether n = 2 can fail at all, which fixes the minimal agent count.

For (c) the PO DENSITY is also reported: if almost every allocation were PO in
the additive class, zero failures there would be uninformative rather than
meaningful.
"""
import itertools
import sys

from algo1 import (masks_by_popcount, is_valid_cost, algorithm1, min_subsidy,
                   all_allocations)


def enumerate_costs(m):
    """Every cost on m chores with c(empty)=0 and all marginals in {0,1}."""
    order = [s for s in masks_by_popcount(m) if s != 0]
    vals = [0] * (1 << m)

    def rec(idx):
        if idx == len(order):
            yield tuple(vals)
            return
        S = order[idx]
        bits = [1 << b for b in range(m) if S & (1 << b)]
        lo = max(vals[S ^ b] for b in bits)
        hi = min(vals[S ^ b] for b in bits) + 1
        for v in range(lo, hi + 1):
            vals[S] = v
            yield from rec(idx + 1)
        vals[S] = 0

    return list(rec(0))


def is_additive(c, m):
    singles = [c[1 << k] for k in range(m)]
    return all(c[S] == sum(singles[k] for k in range(m) if S & (1 << k))
               for S in range(1 << m))


def po_flags(cs, allocs, n):
    profs = [tuple(cs[i][A[i]] for i in range(n)) for A in allocs]
    L = len(profs)
    po = [True] * L
    for a in range(L):
        pa = profs[a]
        for b in range(L):
            if b != a:
                pb = profs[b]
                if all(pb[i] <= pa[i] for i in range(n)) and \
                   any(pb[i] < pa[i] for i in range(n)):
                    po[a] = False
                    break
    return po


def run(n, m, exhaustive_costs):
    allocs = list(all_allocations(n, m))
    index = {A: k for k, A in enumerate(allocs)}
    pool = exhaustive_costs

    total = notpo = incompat = 0
    notpo_additive = 0
    additive_instances = 0
    po_density_add = [0, 0]
    po_density_gen = [0, 0]
    smallest = None

    for cs in itertools.product(pool, repeat=n):
        A, p, info = algorithm1(cs, n, m)
        if A is None:
            continue
        total += 1
        po = po_flags(cs, allocs, n)
        all_add = all(is_additive(c, m) for c in cs)
        if all_add:
            additive_instances += 1
            po_density_add[0] += sum(po)
            po_density_add[1] += len(po)
        else:
            po_density_gen[0] += sum(po)
            po_density_gen[1] += len(po)

        if not po[index[A]]:
            notpo += 1
            if all_add:
                notpo_additive += 1
            if smallest is None:
                smallest = (cs, A, p, info)

        nv = nvpo = 0
        for k, B in enumerate(allocs):
            q = min_subsidy(cs, B, n)
            if q is not None and max(q) <= 1:
                nv += 1
                nvpo += po[k]
        if nv > 0 and nvpo == 0:
            incompat += 1

    print("  n=%d m=%d : %d instances (all %d^%d ordered tuples)"
          % (n, m, total, len(pool), n))
    print("     algorithm output NOT Pareto optimal : %d  (%.2f%%)"
          % (notpo, 100.0 * notpo / max(total, 1)))
    print("     ...of which fully additive          : %d" % notpo_additive)
    print("     NO valid allocation is PO (Q2)      : %d" % incompat)
    print("     fully additive instances            : %d" % additive_instances)
    if po_density_add[1]:
        print("     PO density, additive instances      : %.1f%%"
              % (100.0 * po_density_add[0] / po_density_add[1]))
    if po_density_gen[1]:
        print("     PO density, non-additive instances  : %.1f%%"
              % (100.0 * po_density_gen[0] / po_density_gen[1]))
    return notpo, incompat, notpo_additive


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "n3"

    if which == "n2":
        pool = enumerate_costs(3)
        print("Exhaustive n = 2, m = 3 (does two agents ever fail?)")
        print("  cost functions on 3 chores: %d" % len(pool))
        run(2, 3, pool)
        pool4 = enumerate_costs(4)
        print("  cost functions on 4 chores: %d" % len(pool4))
        run(2, 4, pool4)
        return

    pool = enumerate_costs(3)
    assert all(is_valid_cost(c, 3) for c in pool)
    print("Exhaustive n = 3, m = 3")
    print("  cost functions on 3 chores: %d" % len(pool))
    run(3, 3, pool)


if __name__ == "__main__":
    main()
