"""BDNSV20's modified-valuation trick, transplanted to the MATRIX level.

WHERE ADDITIVITY IS USED in BDNSV20 (Reading_2.pdf, Section 4).  Five places:
Lemma 3.1, Lemma 3.2, eq (1) and eq (7) all decompose v_i(A_k) = sum_t v_i(mu_k^t);
Claim 4.4 eq (9) invokes it by name.  The fatal one is the ENGINE of Section 4:
the modified profile vbar_i is DEFINED by assigning item values,

    vbar_i(mu_k^t) = max( v_i(mu_k^t), v_i(mu_i^{t+1}) ),

and extending additively.  A non-additive dichotomous function has no such
extension, so the construction has no direct analogue.

WHAT SURVIVES.  Lemma 4.1 -- "envy-freeable, plus every arc weight >= -1, implies
subsidy at most 1 per agent" -- is proved by closing the maximum-weight path into
a cycle and using cycle weight <= 0.  It is pure envy-graph combinatorics and uses
no additivity whatever.  And vbar enters the argument ONLY through the n^2 numbers
vbar_i(A_k).  So the trick can be attempted directly on the matrix, with no
valuation function to construct:

    a_ik   := v_i(A_k)                      (the true value matrix)
    abar_ik := max( a_ik, a_ii - 1 )        (raise every entry to the -1 floor)

Then, immediately from the definition:
    (1) abar_ii = a_ii, so the modified arc weights are abar_ik - a_ii >= -1;
    (2) abar_ik >= a_ik, so every modified arc is at least the true arc, hence
        every modified path is at least the true path, hence ellbar >= ell.
So IF the modified envy graph has no positive cycle, Lemma 4.1 gives ellbar <= 1
and therefore ell <= 1 -- subsidy at most one per agent, with no additivity used
anywhere.  Combined with cardinality balance that is exactly conj:imwpm-bound.

The whole burden is thus a single testable condition:

    (NPC)  the modified matrix abar of the IMWPM allocation has no positive cycle.

This is the maximal modification, which makes the -1 floor automatic but makes
(NPC) as hard as possible -- BDNSV20 chose a smaller modification precisely to
keep envy-freeability.  If (NPC) fails, the fallback is a minimal modification:
raise entries only as far as needed, floor at a_ii - 1 only where a_ik < a_ii - 1.

Run:  python matrix_modification.py
"""
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_6")
from targetGbal import size_shift, rand_dicho, subsets   # noqa: E402
from imwpm_raw import imwpm                              # noqa: E402


def ell_vec(W, n):
    """Longest-path weights; None if a positive cycle exists."""
    e = [0] * n
    for _ in range(n + 1):
        ch = False
        new = list(e)
        for i in range(n):
            for j in range(n):
                if i != j and W[i][j] + e[j] > new[i]:
                    new[i] = W[i][j] + e[j]
                    ch = True
        e = new
        if not ch:
            return e
    return None


def analyse(v, A, n):
    """Return (ell true, ell modified, sizes) for the given bundles."""
    a = [[v[i][A[k]] for k in range(n)] for i in range(n)]
    W = [[a[i][k] - a[i][i] for k in range(n)] for i in range(n)]
    abar = [[max(a[i][k], a[i][i] - 1) for k in range(n)] for i in range(n)]
    Wbar = [[abar[i][k] - abar[i][i] for k in range(n)] for i in range(n)]
    return ell_vec(W, n), ell_vec(Wbar, n), [len(A[k]) for k in range(n)]


def main():
    rng = random.Random(777333)
    stats = Counter()
    ellhist = Counter()
    firstfail = None
    print("=== (NPC): does the modified matrix stay free of positive cycles? ===")
    print("   n   m   inst   true ell>1   MODIFIED has positive cycle")
    for (n, m, T) in [(3, 5, 400), (3, 6, 300), (3, 7, 200), (3, 9, 100),
                      (4, 6, 250), (4, 8, 100), (5, 7, 80), (5, 9, 40),
                      (6, 9, 30), (7, 10, 20)]:
        bad_true = bad_mod = cnt = 0
        for _ in range(T):
            cs = [rand_dicho(m, rng) for _ in range(n)]
            if max(max(c.values()) for c in cs) < 1:
                continue
            cnt += 1
            v = [size_shift(c, m) for c in cs]
            A = list(imwpm(v, list(range(m)), n))
            e, ebar, sizes = analyse(v, A, n)
            if e is None:
                stats["true_cycle"] += 1
                continue
            ellhist[max(e)] += 1
            if max(e) > 1:
                bad_true += 1
                stats["true_ell_big"] += 1
            if ebar is None:
                bad_mod += 1
                stats["mod_cycle"] += 1
                if firstfail is None:
                    firstfail = (n, m, [sorted(x) for x in A], e)
            else:
                stats["mod_ok"] += 1
                if max(ebar) > 1:
                    stats["mod_ell_big"] += 1
            stats["tot"] += 1
        print("  %2d  %2d  %5d   %10d   %26d" % (n, m, cnt, bad_true, bad_mod))
    print()
    print("  instances analysed                        : %d" % stats["tot"])
    print("  IMWPM allocation not envy-freeable as given : %d" % stats["true_cycle"])
    print("  true max ell histogram                    : %s" % dict(sorted(ellhist.items())))
    print("  MODIFIED matrix has a positive cycle      : %d" % stats["mod_cycle"])
    print("  modified ell exceeded 1 (impossible if Lemma 4.1 applies) : %d"
          % stats["mod_ell_big"])
    print()
    if stats["mod_cycle"] == 0 and stats["mod_ell_big"] == 0:
        print("  *** (NPC) HOLDS.  Then Lemma 4.1 applies to abar with no additivity,")
        print("      giving ell <= 1 per agent at the IMWPM allocation -- which with")
        print("      cardinality balance is conj:imwpm-bound. ***")
    else:
        print("  (NPC) fails on some instances: the MAXIMAL modification is too")
        print("  coarse, exactly as BDNSV20 anticipated by choosing a smaller one.")
        if firstfail:
            print("  first failure: n=%d m=%d bundles=%s true ell=%s" % firstfail)


if __name__ == "__main__":
    main()
