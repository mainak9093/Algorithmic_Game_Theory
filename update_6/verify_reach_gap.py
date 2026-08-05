"""Independent, algorithm-free verification of the reachability gap found by
guidedR3_full.py: does the instance really admit SOME allocation with q-spread
<= 1 (confirming Target G holds), even though no execution of guided-R3 can
reach one?

Run:  python verify_reach_gap.py
"""
from itertools import product
from guidedR3 import size_shift, compute_p, q_spread


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

    best = None
    all_results = []
    for assign in product(range(n), repeat=m):
        A = [frozenset(g for g in range(m) if assign[g] == i) for i in range(n)]
        p = compute_p(v, A, n)
        if p is None:
            continue
        q = [p[i] + len(A[i]) for i in range(n)]
        sp = max(q) - min(q)
        all_results.append((sp, [sorted(b) for b in A], p, q))
        if best is None or sp < best[0]:
            best = (sp, [sorted(b) for b in A], p, q)

    print("all envy-freeable allocations, sorted by q-spread:")
    for sp, bd, p, q in sorted(all_results, key=lambda r: r[0])[:6]:
        print("   spread=%d  bundles=%s  p=%s  q=%s" % (sp, bd, p, q))

    print("\nBEST achievable q-spread (unrestricted search): %d" % best[0])
    print("BEST reachable by any guided-R3 execution        : 2   (from guidedR3_full.py)")
    if best[0] < 2:
        print("\n=> CONFIRMED: Target G holds on this instance (spread=%d achievable)," % best[0])
        print("   but no R3-style insertion algorithm can reach a witness of it.")
        print("   This is a genuine reachability obstruction to Approach 6's")
        print("   'run R3 on the transformed goods instance' strategy.")


if __name__ == "__main__":
    main()
