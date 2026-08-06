"""What q really is: an explicit formula in the CHORES envy graph.

The compensation of prop:bdnsv-fails-dichotomous -- subsidy 2 with sizes (3,3,1)
giving q = (3,3,3) -- is not a coincidence, and this script checks the identity
behind it.

DERIVATION.  Size-shift gives vt_i(S) = |S| - c_i(S), so the GOODS arc weight is
    wt(i,j) = vt_i(A_j) - vt_i(A_i) = [c_i(A_i) - c_i(A_j)] + |A_j| - |A_i|
            = w(i,j) + |A_j| - |A_i|,
where w is the CHORES arc weight.  Along a path i -> ... -> j the size terms
telescope, leaving
    dt(i,j) = d(i,j) + |A_j| - |A_i|,
with d the heaviest i->j path in the chores envy graph (d(i,i) = 0).  Hence
    pt_i = max_j dt(i,j) = max_j [ d(i,j) + |A_j| ] - |A_i|,
and therefore

    q_i  =  pt_i + |A_i|  =  max_j [ d(i,j) + |A_j| ].            (Q)

So q needs no goods picture at all: q_i is the largest bundle SIZE reachable from
agent i, inflated by the envy accumulated on the way.  The compensation is then
automatic -- an agent holding a small bundle can still have large q by envying its
way to a big one, and vice versa, so neither term is controlled alone.

COROLLARY FOR IMWPM.  IMWPM runs T = ceil(m/n) rounds giving every agent exactly
one object per round, so |A_j| = T - delta_j with delta_j the number of dummies
agent j received.  Substituting into (Q),

    q_i = T + max_j [ d(i,j) - delta_j ],                          (Q')

so the q-spread does not depend on T.  In particular when n divides m every
delta_j = 0 and q_i = T + ell(i), so on such instances conj:imwpm-bound says
exactly max_i ell(i) <= 2, and Target G says max_i ell(i) <= 1, which IS
Conjecture 2 at that allocation.

Both identities are checked here against direct computation.

Run:  python q_formula.py
"""
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_6")
from targetGbal import size_shift, rand_dicho            # noqa: E402
from imwpm_raw import imwpm, q_spread, compute_p         # noqa: E402


def chores_d(cs, A, n):
    """All-pairs heaviest path in the CHORES envy graph; None if positive cycle."""
    W = [[cs[i][A[i]] - cs[i][A[j]] for j in range(n)] for i in range(n)]
    d = [[(0 if i == j else W[i][j]) for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] > d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    for i in range(n):
        if d[i][i] > 0:
            return None
    return d


def main():
    rng = random.Random(2718281)
    ok_q = bad_q = 0
    ok_qp = bad_qp = 0
    tot = 0
    spreadhist = Counter()
    ndivm = Counter()
    print("=== checking (Q) and (Q') at the IMWPM allocation ===")
    for (n, m, T) in [(3, 5, 200), (3, 6, 150), (3, 7, 120), (3, 9, 60),
                      (4, 6, 120), (4, 8, 60), (5, 7, 50), (5, 10, 25)]:
        for _ in range(T):
            cs = [rand_dicho(m, rng) for _ in range(n)]
            if max(max(c.values()) for c in cs) < 1:
                continue
            v = [size_shift(c, m) for c in cs]
            A = list(imwpm(v, list(range(m)), n))
            sp, p, q = q_spread(v, A, n)
            if sp is None:
                continue
            d = chores_d(cs, A, n)
            if d is None:
                continue
            tot += 1
            # (Q)
            qform = [max(d[i][j] + len(A[j]) for j in range(n)) for i in range(n)]
            if qform == list(q):
                ok_q += 1
            else:
                bad_q += 1
                if bad_q == 1:
                    print("  !! (Q) mismatch: q=%s formula=%s" % (list(q), qform))
            # (Q')
            Trounds = -(-m // n)
            delta = [Trounds - len(A[j]) for j in range(n)]
            qp = [Trounds + max(d[i][j] - delta[j] for j in range(n))
                  for i in range(n)]
            if qp == list(q):
                ok_qp += 1
            else:
                bad_qp += 1
            spreadhist[sp] += 1
            if m % n == 0:
                ell = max(max(d[i][j] for j in range(n)) for i in range(n))
                ndivm[(sp, ell)] += 1
    print()
    print("  instances checked            : %d" % tot)
    print("  (Q)  q_i = max_j [d(i,j)+|A_j|]  : %d ok, %d mismatched" % (ok_q, bad_q))
    print("  (Q') q_i = T + max_j [d(i,j)-delta_j] : %d ok, %d mismatched"
          % (ok_qp, bad_qp))
    print("  q-spread histogram           : %s" % dict(sorted(spreadhist.items())))
    if ndivm:
        print()
        print("  when n divides m, (q-spread, max ell) pairs : %s"
              % dict(sorted(ndivm.items())))
        bad = [k for k in ndivm if k[0] != k[1]]
        print("  q-spread == max ell on those instances : %s"
              % ("yes" if not bad else "NO, exceptions %s" % bad))
    print()
    if bad_q == 0 and bad_qp == 0:
        print("  *** both identities hold exactly.  Target G and conj:imwpm-bound")
        print("      are now statements about the CHORES envy graph alone. ***")


if __name__ == "__main__":
    main()
