"""Two further results, and where the residual really sits.

(A) THE mu_x = 0 CASE IS EXACT.  By lem:new-paidsets, mu_x = 0 forces
    P(W') subset P(W); and for S in P(W) conditions (i),(iii) of the peel
    criterion are automatic.  Hence

        mu_x = 0  ==>  peel(x,j) legal  iff  some S in P(W) satisfies
                       w(i,x) + mu_i <= lambda_S(i,x) for all i != x.

    An exact criterion, decidable by scanning P(W).  So all remaining difficulty
    is in the mu_x = 1 case, which is exactly where new paid sets can appear.

(B) THE TWO CONSTRUCTIONS COMBINE.  lem:paid-peel takes S containing x and
    deletes x; lem:slack-transfer takes S avoiding x and adds the blockers T.
    Doing both -- S' := (S \ {x}) union T for S containing x, T outside S --
    is strictly more general.  Moving x OUT raises every in-arc lambda(i,x) by at
    least one:
        i in S \ {x} :  0 -> +1        i in T : -1 -> +1        i outside : -1 -> 0
    so condition (ii) is free, whatever the marginals.  What must be paid is (iii),
    the out-arcs, and (i), the cost of moving T in:

        (1) w(k,i) <= lambda_S(k,i) - 1   for i in T, k outside T, k != i
        (2) w(x,k) <= mu_x - 1            for k in (S \ {x}) union T
        (3) w(x,k) <= mu_x                for k outside S union T

    With T empty and mu_x = 1 this degenerates to lem:paid-peel.

Checked: (A) as an exact criterion, (B) for soundness, the coverage (B) adds over
the three existing lemmas, and a breakdown of the residual by mu_x.

Run:  python combined.py
"""
from itertools import permutations, combinations
from collections import Counter, deque
import random
import sys

sys.path.insert(0, "../update_6")
sys.path.insert(0, "../update_32")
sys.path.insert(0, "../update_34")
sys.path.insert(0, "../update_36")
sys.path.insert(0, "../update_37")
from targetGbal import rand_dicho                              # noqa: E402
from peel_general import legal, terminal, peels, make          # noqa: E402
from reachable_stuck import ok                                 # noqa: E402
from potential_set import admissible, arcs                     # noqa: E402
from slack_transfer import lam, marginals, slack_transfer_certifies  # noqa: E402


def mu0_exact(cs, W, x, j, n, A, mu, PW):
    """(A): for mu_x = 0, legality iff some S in P(W) absorbs the in-arcs."""
    return any(all(A[i][x] + mu[i] <= lam(S, i, x)
                   for i in range(n) if i != x)
               for S in PW)


def combined_certifies(cs, W, x, j, n, A, mu, PW):
    """(B): S' = (S \\ {x}) u T for some S containing x and some T outside S."""
    others = [i for i in range(n) if i != x]
    for S in PW:
        if x not in S:
            continue
        outside = [i for i in others if i not in S]
        for r in range(len(outside) + 1):
            for T in combinations(outside, r):
                T = frozenset(T)
                ok1 = all(A[k][i] <= lam(S, k, i) - 1
                          for i in T for k in range(n)
                          if k != i and k not in T)
                if not ok1:
                    continue
                ok2 = all(A[x][k] <= mu[x] - 1
                          for k in (set(S) - {x}) | T)
                if not ok2:
                    continue
                ok3 = all(A[x][k] <= mu[x]
                          for k in others if k not in S and k not in T)
                if ok3:
                    return True
    return False


def main():
    rng = random.Random(38383838)
    bad_A = n_A = bad_B = n_B = 0
    cov = Counter()
    resid_mu = Counter()
    tot = 0
    print("=== (A) mu_x=0 exact criterion, (B) combined construction ===")
    for (n, m, T) in [(3, 4, 40), (3, 5, 18), (3, 6, 6),
                      (4, 3, 30), (4, 4, 12), (5, 3, 12)]:
        perms = list(permutations(range(n)))
        for _ in range(T):
            cs = [rand_dicho(m, rng) for _ in range(n)]
            if max(max(c.values()) for c in cs) < 1:
                continue
            root = tuple([make(m)] * n)
            seen = {root}; q = deque([root])
            while q and len(seen) < 3000:
                W = q.popleft()
                if not terminal(W, n, m):
                    tot += 1
                    PW = admissible(cs, W, n)
                    A = arcs(cs, W, n)
                    old = new = False
                    residual_mus = []
                    for mv, s in peels(W, n, m):
                        x, j = mv
                        mu = marginals(cs, W, x, j, n)
                        lg = legal(cs, s, n)
                        # (A)
                        if mu[x] == 0:
                            n_A += 1
                            if mu0_exact(cs, W, x, j, n, A, mu, PW) != lg:
                                bad_A += 1
                        # (B) soundness
                        cB = combined_certifies(cs, W, x, j, n, A, mu, PW)
                        if cB:
                            n_B += 1
                            if not lg:
                                bad_B += 1
                        if not ok(cs, s, n, m):
                            continue
                        free = all(mu[k] == 0 for k in range(n) if k != x)
                        paid = mu[x] == 1 and any(x in S for S in PW)
                        st = slack_transfer_certifies(cs, W, x, j, n)[0]
                        if free or paid or st:
                            old = True
                        if cB:
                            new = True
                        if not (free or paid or st or cB):
                            residual_mus.append(mu[x])
                    cov[(old, new)] += 1
                    if not old and not new and residual_mus:
                        resid_mu[max(residual_mus)] += 1
                for s in ([s for _, s in peels(W, n, m)]
                          + [tuple(W[p[i]] for i in range(n)) for p in perms]):
                    if s not in seen and ok(cs, s, n, m):
                        seen.add(s); q.append(s)
    print("  (A) mu_x=0 exact criterion : %d peels, %d mismatches" % (n_A, bad_A))
    print("  (B) combined soundness     : %d fired, %d ILLEGAL" % (n_B, bad_B))
    print()
    print("  states                     : %d" % tot)
    print("  (old3, combined) coverage  : %s" % dict(cov))
    a = cov[(True, True)] + cov[(True, False)]
    b = cov[(False, True)]
    print("  three existing lemmas cover: %d  (%.1f%%)" % (a, 100.0 * a / tot))
    print("  combined ADDS              : %d  (%.1f%%)" % (b, 100.0 * b / tot))
    print("  still uncovered            : %d  (%.1f%%)"
          % (cov[(False, False)], 100.0 * cov[(False, False)] / tot))
    print()
    print("  residual by max mu_x over its peels: %s" % dict(sorted(resid_mu.items())))


if __name__ == "__main__":
    main()
