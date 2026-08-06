"""Correcting prop:inarcs-only, and a third safety criterion.

THE ERROR.  prop:inarcs-only was stated as a biconditional for ANY S:

    S in P(W')  iff  S satisfies the non-x constraints of W
                     and w(i,x) + mu_i <= lambda_S(i,x) for all i.

That omits the OUT-ARC condition w(x,k) - mu_x <= lambda_S(x,k), which is
automatic only when S is already in P(W) -- the arcs out of x drop by mu_x, so a
bound that held before still holds.  For an S not in P(W) it has to be checked.
Corrected:

    S in P(W')  iff   (i)   w(i,k)        <= lambda_S(i,k)   for i,k != x
                      (ii)  w(i,x) + mu_i <= lambda_S(i,x)   for i != x
                      (iii) w(x,k) - mu_x <= lambda_S(x,k)   for k != x

and if S is in P(W) then (i) and (iii) are free, leaving only (ii).

WHAT THE CORRECTION BUYS.  Suppose S' is in P(W') but not in P(W).  By (ii),
w(i,x) <= lambda - mu_i <= lambda, so its in-arcs already held at W; by (i) its
non-x arcs held.  So S' can only have violated an OUT-arc of x, and by at most
mu_x.  Hence:

    (NEW)  P(W') \ P(W) is empty unless mu_x = 1, and its members are exactly
           the S violating some out-arc of x by exactly 1 and nothing else.

That says where a third criterion must live, and suggests one.  Adding an agent
i to the paid set raises lambda(i,k) by 1 for every k -- buying slack on the
in-arc (i,x) -- at the cost of lowering lambda(k,i) by 1.  So:

    SLACK-TRANSFER PEEL.  Let S in P(W) with x not in S, and let
        T := { i != x : arc (i,x) is tight for S and mu_i = 1 }
    be the blockers.  If
        (1) every arc into each i in T from outside T has slack >= 1, and
        (2) w(x,k) - mu_x <= -1 for every k in T,
    then S union T certifies peel(x,j), so the peel is legal.

Checked here: the corrected proposition, claim (NEW), soundness of the
slack-transfer lemma, and how much coverage it adds over free + paid.

Run:  python slack_transfer.py
"""
from itertools import permutations
from collections import Counter, deque
import random
import sys

sys.path.insert(0, "../update_6")
sys.path.insert(0, "../update_32")
sys.path.insert(0, "../update_34")
sys.path.insert(0, "../update_36")
from targetGbal import rand_dicho                              # noqa: E402
from peel_general import legal, cand, terminal, peels, make    # noqa: E402
from reachable_stuck import ok                                 # noqa: E402
from potential_set import admissible, arcs                     # noqa: E402


def lam(S, i, k):
    if (i in S) == (k in S):
        return 0
    return 1 if i in S else -1


def in_P(A, S, n):
    return all(A[i][k] <= lam(S, i, k)
               for i in range(n) for k in range(n) if i != k)


def marginals(cs, W, x, j, n):
    return [cs[k][W[x]] - cs[k][W[x] - {j}] for k in range(n)]


def slack_transfer_certifies(cs, W, x, j, n):
    """Does the slack-transfer construction certify peel(x,j)?"""
    A = arcs(cs, W, n)
    mu = marginals(cs, W, x, j, n)
    for S in admissible(cs, W, n):
        if x in S:
            continue
        T = frozenset(i for i in range(n)
                      if i != x and A[i][x] == lam(S, i, x) and mu[i] == 1)
        if not T:
            continue
        # (1) arcs into each i in T from outside T have slack >= 1
        if not all(A[k][i] <= lam(S, k, i) - 1
                   for i in T for k in range(n) if k != i and k not in T):
            continue
        # (2) out-arcs from x into T survive
        if not all(A[x][k] - mu[x] <= -1 for k in T):
            continue
        return True, S, T
    return False, None, None


def main():
    rng = random.Range if False else random.Random(37373737)
    bad_prop = bad_new = bad_slack = 0
    n_prop = n_new = n_slack = 0
    cov = Counter()
    tot = 0
    print("=== corrected prop:inarcs-only, claim (NEW), slack-transfer lemma ===")
    for (nn, m, T) in [(3, 4, 40), (3, 5, 18), (3, 6, 6),
                       (4, 3, 30), (4, 4, 12), (5, 3, 12)]:
        perms = list(permutations(range(nn)))
        for _ in range(T):
            cs = [rand_dicho(m, rng) for _ in range(nn)]
            if max(max(c.values()) for c in cs) < 1:
                continue
            root = tuple([make(m)] * nn)
            seen = {root}
            q = deque([root])
            while q and len(seen) < 4000:
                W = q.popleft()
                if not terminal(W, nn, m):
                    tot += 1
                    PW = set(admissible(cs, W, nn))
                    hasF = hasP = hasS = False
                    for mv, s in peels(W, nn, m):
                        x, j = mv
                        mu = marginals(cs, W, x, j, nn)
                        A = arcs(cs, W, nn); A2 = arcs(cs, s, nn)
                        PW2 = set(admissible(cs, s, nn))
                        # corrected biconditional
                        for bits in range(1 << nn):
                            S = frozenset(i for i in range(nn) if bits >> i & 1)
                            lhs = S in PW2
                            c1 = all(A[i][k] <= lam(S, i, k) for i in range(nn)
                                     for k in range(nn) if i != k and i != x and k != x)
                            c2 = all(A[i][x] + mu[i] <= lam(S, i, x)
                                     for i in range(nn) if i != x)
                            c3 = all(A[x][k] - mu[x] <= lam(S, x, k)
                                     for k in range(nn) if k != x)
                            n_prop += 1
                            if lhs != (c1 and c2 and c3):
                                bad_prop += 1
                        # (NEW)
                        newsets = PW2 - PW
                        if newsets:
                            n_new += 1
                            if mu[x] != 1:
                                bad_new += 1
                        # criteria
                        if not ok(cs, s, nn, m):
                            continue
                        if all(mu[k] == 0 for k in range(nn) if k != x):
                            hasF = True
                        if mu[x] == 1 and any(x in S for S in PW):
                            hasP = True
                        good, S0, T0 = slack_transfer_certifies(cs, W, x, j, nn)
                        if good:
                            n_slack += 1
                            if not legal(cs, s, nn):
                                bad_slack += 1
                            hasS = True
                    cov[(hasF or hasP, hasS)] += 1
                for s in ([s for _, s in peels(W, nn, m)]
                          + [tuple(W[p[i]] for i in range(nn)) for p in perms]):
                    if s not in seen and ok(cs, s, nn, m):
                        seen.add(s); q.append(s)
    print("  corrected prop:inarcs-only : %d checks, %d violations" % (n_prop, bad_prop))
    print("  (NEW) new sets need mu_x=1 : %d cases,  %d violations" % (n_new, bad_new))
    print("  slack-transfer soundness   : %d fired,  %d ILLEGAL" % (n_slack, bad_slack))
    print()
    print("  states: %d" % tot)
    print("  (free|paid, slack) coverage: %s" % dict(cov))
    a = cov[(True, True)] + cov[(True, False)]
    b = cov[(False, True)]
    print("  free|paid covers      : %d  (%.1f%%)" % (a, 100.0 * a / tot))
    print("  slack-transfer ADDS   : %d  (%.1f%%)" % (b, 100.0 * b / tot))
    print("  still uncovered       : %d" % cov[(False, False)])


if __name__ == "__main__":
    main()
