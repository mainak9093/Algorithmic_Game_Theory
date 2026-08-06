"""Does the n=2 window lemma generalise?  The route to proving the algorithm works.

thm:n2-complete proves completeness at n = 2 in two pieces:
    WINDOW  |h| <= 3 implies the split is good, where h = u(A) - u(B) and
            u = sum_i v_i is the TOTAL welfare function;
    IVT     walking from (A,B) to the complementary split (B,A) flips the sign
            of h, and each swap moves h by at most 4, so some intermediate split
            lands in the window.

The natural generalisation replaces the scalar h by the spread of u across the
bundles.  For a partition B_1,...,B_n put

    uspread(B) := max_j u(B_j) - min_j u(B_j),      u := sum_i c_i .

At n = 2 this is |h| exactly, so the conjecture below is a genuine
generalisation, not an analogy:

    WINDOW(K)   every balanced partition with uspread <= K is good
    EXISTS(K)   every instance has a balanced partition with uspread <= K

WINDOW(K) and EXISTS(K) together give the balance lemma and Conjecture 2.  The
division of labour is favourable: EXISTS(K) concerns ONE function u, not n of
them, so it is a balancing/discrepancy statement of a standard kind, attackable
by an exchange argument -- whereas everything that has failed so far had to
control n cost functions at once.

Measured here, over all balanced partitions of each instance:
  - the largest K for which WINDOW(K) held (i.e. smallest uspread of a BAD
    balanced partition, minus one);
  - the smallest uspread achievable, per instance, for EXISTS(K).

Run:  python window_general.py
"""
from itertools import product, permutations
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_17")
sys.path.insert(0, "../update_18")
from minimum_subsidy import rand_dicho, matrix_realising  # noqa: E402
from localsearch_lemma import ell_vec  # noqa: E402


def canon_good(cs, bundles, n, perms):
    best = None
    for perm in perms:
        t = sum(cs[i][bundles[perm[i]]] for i in range(n))
        if best is None or t < best[0]:
            best = (t, perm)
    _, perm = best
    a = [[cs[i][bundles[perm[j]]] for j in range(n)] for i in range(n)]
    e = ell_vec(a, n)
    return e is not None and max(e) <= 1


def scan(cs, m, n, perms):
    """(min uspread of a BAD balanced partition, min uspread overall, min uspread of a GOOD one)."""
    u = lambda S: sum(cs[i][S] for i in range(n))
    bad_min = None
    any_min = None
    good_min = None
    for assign in product(range(n), repeat=m):
        bundles = tuple(frozenset(g for g in range(m) if assign[g] == i)
                        for i in range(n))
        sz = [len(b) for b in bundles]
        if max(sz) - min(sz) > 1:
            continue
        vals = [u(b) for b in bundles]
        sp = max(vals) - min(vals)
        if any_min is None or sp < any_min:
            any_min = sp
        if canon_good(cs, bundles, n, perms):
            if good_min is None or sp < good_min:
                good_min = sp
        else:
            if bad_min is None or sp < bad_min:
                bad_min = sp
    return bad_min, any_min, good_min


def main():
    rng = random.Random(24682468)
    print("=== window lemma: is a small u-spread enough to force goodness? ===")
    print("   n   m   inst   min u-spread of a BAD balanced partition (histogram)")
    worstK = None
    exists_hist = Counter()
    for (n, m, T) in [(2, 5, 200), (2, 6, 150),
                      (3, 5, 200), (3, 6, 150), (3, 7, 80),
                      (4, 6, 90), (4, 7, 30), (5, 5, 40)]:
        perms = list(permutations(range(n)))
        hist = Counter()
        cnt = 0
        for _ in range(T):
            cs = (matrix_realising(m, n, rng, 3) if rng.random() < 0.5
                  else [rand_dicho(m, rng, rng.choice([0.0, 0.2, 0.5, 0.8, 1.0]))
                        for _ in range(n)])
            if max(max(x.values()) for x in cs) < 2:
                continue
            cnt += 1
            bad_min, any_min, good_min = scan(cs, m, n, perms)
            hist[bad_min if bad_min is not None else "none"] += 1
            exists_hist[any_min] += 1
            if bad_min is not None:
                if worstK is None or bad_min < worstK:
                    worstK = bad_min
        print("  %2d  %2d  %5d   %s" % (n, m, cnt, dict(sorted(
            hist.items(), key=lambda kv: (kv[0] == "none", kv[0])))))
    print()
    print("  smallest u-spread ever seen on a BAD balanced partition : %s" % worstK)
    if worstK is not None:
        print("  => WINDOW(K) can hold only for K <= %d" % (worstK - 1))
        if worstK - 1 >= 1:
            print("     WINDOW(%d) is consistent with all data above." % (worstK - 1))
        else:
            print("     *** WINDOW fails even at K = 0: a balanced partition with")
            print("         PERFECTLY equal u can still be bad, so u-spread alone")
            print("         does not control goodness and the n=2 route does not")
            print("         generalise in this form. ***")
    print()
    print("=== EXISTS(K): smallest achievable u-spread per instance ===")
    for k in sorted(exists_hist):
        print("   min u-spread = %s : %d instances" % (k, exists_hist[k]))


if __name__ == "__main__":
    main()
