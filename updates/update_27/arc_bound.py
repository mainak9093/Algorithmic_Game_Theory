"""Localising conj:imwpm-bound: from paths to arcs.

lem:q-formula gives q_i = max_j [d(i,j) + |A_j|].  If j* attains q_i then
q_{i'} >= d(i',j*) + |A_{j*}|, so

    q_i - q_{i'}  <=  d(i,j*) - d(i',j*),

and therefore

    (R)   q-spread <= 2   <==>   d(i,j) - d(i',j) <= 2  for all i,i',j.

Since d(i,j) >= w(i,i') + d(i',j) whenever i != i' (no positive cycles, so the
heaviest walk is a heaviest simple path and concatenation is legitimate), (R)
FORCES every arc weight w(i,i') <= 2.  So a necessary condition for
conj:imwpm-bound is the purely local statement

    (ARC)  every chores envy arc at the IMWPM allocation has weight <= 2,

which is exactly the sort of pairwise claim the one-round exchange property of
lem:imwpm-chores could plausibly deliver -- unlike the path statements that
defeated every "sum the rounds" argument in sec:approach6-r11-audit.

Measured here at the IMWPM allocation:
  - the distribution of arc weights w(i,j) = c_i(A_i) - c_i(A_j);
  - the distribution of max_{i,i',j} [d(i,j) - d(i',j)], i.e. the left side of (R);
  - whether (ARC) with the observed bound would already give the path bound, by
    comparing max arc against max path.

Also checked: kappa_i := c_i(A_i) equals the number of rounds in which agent i's
own chore had marginal 1 -- the chores form of lem:own-telescoping, which is exact.

Run:  python arc_bound.py
"""
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_6")
sys.path.insert(0, "../update_25")
sys.path.insert(0, "../update_26")
from targetGbal import size_shift, rand_dicho      # noqa: E402
from imwpm_raw import q_spread                     # noqa: E402
from r11_gap import imwpm_rounds, DUM              # noqa: E402
from q_formula import chores_d                     # noqa: E402


def main():
    rng = random.Random(1618033)
    arch = Counter()
    diffh = Counter()
    qh = Counter()
    kappa_bad = 0
    tot = 0
    worst_arc = None
    print("=== arc weights and path-difference at the IMWPM allocation ===")
    print("   n   m   inst   max arc   max d(i,j)-d(i',j)   max q-spread")
    for (n, m, T) in [(3, 5, 200), (3, 6, 150), (3, 7, 120), (3, 9, 50),
                      (4, 6, 120), (4, 8, 60), (5, 7, 50), (5, 9, 25),
                      (6, 9, 20)]:
        ma = md = mq = 0
        cnt = 0
        for _ in range(T):
            cs = [rand_dicho(m, rng) for _ in range(n)]
            if max(max(c.values()) for c in cs) < 1:
                continue
            v = [size_shift(c, m) for c in cs]
            A, rounds = imwpm_rounds(v, list(range(m)), n)
            A = [frozenset(x for x in b if x < DUM) for b in A]
            d = chores_d(cs, A, n)
            if d is None:
                continue
            sp, _, _ = q_spread(v, A, n)
            if sp is None:
                continue
            cnt += 1
            tot += 1
            # kappa check: own cost equals count of marginal-1 rounds
            for i in range(n):
                k = sum(1 for pre, asg in rounds
                        if cs[i][frozenset(x for x in (pre[i] | {asg[i]})
                                           if x < DUM)]
                        - cs[i][frozenset(x for x in pre[i] if x < DUM)] == 1)
                if k != cs[i][A[i]]:
                    kappa_bad += 1
            for i in range(n):
                for j in range(n):
                    if i == j:
                        continue
                    w = cs[i][A[i]] - cs[i][A[j]]
                    arch[w] += 1
                    if w > ma:
                        ma = w
                    if worst_arc is None or w > worst_arc[0]:
                        worst_arc = (w, n, m)
            best = 0
            for j in range(n):
                col = [d[i][j] for i in range(n)]
                if max(col) - min(col) > best:
                    best = max(col) - min(col)
            diffh[best] += 1
            md = max(md, best)
            qh[sp] += 1
            mq = max(mq, sp)
        print("  %2d  %2d  %5d   %7d   %18d   %12d" % (n, m, cnt, ma, md, mq))
    print()
    print("  instances                          : %d" % tot)
    print("  kappa identity failures (must be 0): %d" % kappa_bad)
    print("  arc-weight distribution            : %s" % dict(sorted(arch.items())))
    print("  max arc weight observed            : %d" % max(arch))
    print("  max_j spread of d(.,j) distribution: %s" % dict(sorted(diffh.items())))
    print("  q-spread distribution              : %s" % dict(sorted(qh.items())))
    print()
    if max(arch) <= 2:
        print("  *** (ARC) holds: every arc <= %d at the IMWPM allocation." % max(arch))
        print("      This is a PAIRWISE claim, so the one-round exchange property")
        print("      of lem:imwpm-chores is the right tool -- no round summation. ***")
    else:
        print("  (ARC) fails: an arc of weight %d occurs (n=%d, m=%d), so the"
              % (worst_arc[0], worst_arc[1], worst_arc[2]))
        print("  necessary condition for q-spread <= 2 is violated somewhere;")
        print("  check whether those instances still have q-spread <= 2.")


if __name__ == "__main__":
    main()
