"""
Extract the incompatibility witnesses: instances in which NO allocation
meeting the paper's guarantee is Pareto optimal.

This is a stronger statement than "our algorithm fails PO". It says the
theorem's conclusion and Pareto optimality cannot be had together at all, so no
repair of the algorithm -- no tie-breaking rule, no different completion --
could recover PO while keeping p in {0,1}^n.

Exhaustive over n = 2, m = 3, where all 38^2 = 1444 ordered instances fit.
"""
import itertools

from algo1 import (masks_by_popcount, algorithm1, min_subsidy,
                   all_allocations, is_valid_cost)
from exhaustive_n3m3 import enumerate_costs, is_additive


def main():
    n, m = 2, 3
    pool = enumerate_costs(m)
    allocs = list(all_allocations(n, m))
    names = "abc"

    def bundle(x):
        return "{" + ",".join(names[k] for k in range(m) if x & (1 << k)) + "}"

    def profile(cs, A):
        return tuple(cs[i][A[i]] for i in range(n))

    def po_flags(cs):
        profs = [profile(cs, A) for A in allocs]
        po = []
        for a, pa in enumerate(profs):
            dom = any(a != b
                      and all(pb[i] <= pa[i] for i in range(n))
                      and any(pb[i] < pa[i] for i in range(n))
                      for b, pb in enumerate(profs))
            po.append(not dom)
        return po

    found = []
    for cs in itertools.product(pool, repeat=n):
        po = po_flags(cs)
        valid = []
        for k, B in enumerate(allocs):
            q = min_subsidy(cs, B, n)
            if q is not None and max(q) <= 1:
                valid.append((k, B, q))
        if valid and not any(po[k] for (k, _, _) in valid):
            found.append((cs, valid, po))

    print("instances where NO valid allocation is Pareto optimal: %d"
          % len(found))
    print()

    for idx, (cs, valid, po) in enumerate(found):
        print("=== witness %d ===" % (idx + 1))
        for i in range(n):
            print("   agent %d cost table %s   additive=%s"
                  % (i + 1, str(cs[i]), is_additive(cs[i], m)))
        print()
        print("   every allocation:")
        for k, A in enumerate(allocs):
            q = min_subsidy(cs, A, n)
            ok = q is not None and max(q) <= 1
            print("      %-8s %-8s costs=%s  minimal p=%-10s  valid=%-5s PO=%s"
                  % (bundle(A[0]), bundle(A[1]), profile(cs, A),
                     "none" if q is None else str(q), ok, po[k]))
        print()
        A, p, info = algorithm1(cs, n, m)
        print("   Algorithm 1 returns A = %s %s with p = %s"
              % (bundle(A[0]), bundle(A[1]), p))
        print()
        print("   valid allocations : %d, of which Pareto optimal : 0"
              % len(valid))
        print("   => on this instance the {0,1}-subsidy guarantee and Pareto")
        print("      optimality are mutually exclusive.")
        print()


if __name__ == "__main__":
    main()
