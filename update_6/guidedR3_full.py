"""Full backtracking search over ALL legal executions of R3's ALG (all item
orders, all EXTEND choices, all FINDSINK starting points) on the smallest
instance where the GREEDY heuristic failed, to separate two possibilities:

  (a) greedy is just a weak heuristic -- SOME execution reaches spread <= 1;
  (b) R3's algorithmic template cannot reach a good outcome here AT ALL, no
      matter how it is guided -- a genuine reachability obstruction, in the
      same family as the peel dead ends of Approach 3.

Run:  python guidedR3_full.py
"""
from itertools import permutations

from guidedR3 import (size_shift, extend_options, apply_extend,
                      findsink_run, apply_findsink, compute_p, M_of_p, q_spread)


def full_search(v, items, n, cutoff=None):
    """DFS over all legal (order, EXTEND choice, FINDSINK-s0 choice)
    combinations.  Returns the best (min) final q-spread found, and a
    witnessing execution trace."""
    best = [None, None]   # [spread, trace]
    seen = 0

    def rec(remaining, A, p, trace):
        nonlocal seen
        seen += 1
        if not remaining:
            sp, _, q = q_spread(v, A, n)
            if best[0] is None or sp < best[0]:
                best[0] = sp
                best[1] = (list(trace), [set(b) for b in A], q)
            return
        if cutoff is not None and seen > cutoff:
            return
        g = remaining[0]
        rest = remaining[1:]
        opts = extend_options(v, A, p, g, n)
        if opts:
            for (rho, k) in opts:
                B = apply_extend(A, rho, k, g, n)
                pB = compute_p(v, B, n)
                rec(rest, B, pB, trace + [("E", k, tuple(sorted(rho.items())))])
        else:
            for s0 in M_of_p(p, n):
                s = findsink_run(v, A, p, g, n, s0)
                B = apply_findsink(A, s, g)
                pB = compute_p(v, B, n)
                rec(rest, B, pB, trace + [("F", s0, s)])

    for order in permutations(items):
        A0 = [frozenset() for _ in range(n)]
        p0 = [0] * n
        rec(list(order), A0, p0, [])

    return best[0], best[1], seen


def main():
    m, n = 3, 3
    c = [
        {frozenset(): 0, frozenset({0}): 0, frozenset({1}): 0, frozenset({2}): 0,
         frozenset({0, 1}): 0, frozenset({0, 2}): 0, frozenset({1, 2}): 0,
         frozenset({0, 1, 2}): 0},
        {frozenset(): 0, frozenset({0}): 0, frozenset({1}): 0, frozenset({2}): 0,
         frozenset({0, 1}): 1, frozenset({0, 2}): 1, frozenset({1, 2}): 1,
         frozenset({0, 1, 2}): 1},
        {frozenset(): 0, frozenset({0}): 1, frozenset({1}): 1, frozenset({2}): 1,
         frozenset({0, 1}): 2, frozenset({0, 2}): 2, frozenset({1, 2}): 2,
         frozenset({0, 1, 2}): 2},
    ]
    v = [size_shift(ci, m) for ci in c]

    print("instance (the smallest greedy failure): costs")
    for i, ci in enumerate(c):
        print("  agent", i, {tuple(sorted(k)): val for k, val in
                             sorted(ci.items(), key=lambda kv: (len(kv[0]), sorted(kv[0])))})

    sp, trace, seen = full_search(v, list(range(m)), n)
    print("\nnodes explored in full search: %d" % seen)
    print("best q-spread over ALL legal R3 executions: %d" % sp)
    if trace:
        exec_trace, bundles, q = trace
        print("witnessing execution: %s" % exec_trace)
        print("final bundles: %s   q = %s" % ([sorted(b) for b in bundles], q))

    if sp <= 1:
        print("\n=> (a) GREEDY WAS JUST WEAK: some R3 execution reaches spread <= 1.")
    else:
        print("\n=> (b) REACHABILITY OBSTRUCTION: no legal R3 execution reaches")
        print("   spread <= 1, although Target G holds for this instance (some")
        print("   allocation not reachable by ANY R3 execution achieves it).")


if __name__ == "__main__":
    main()
