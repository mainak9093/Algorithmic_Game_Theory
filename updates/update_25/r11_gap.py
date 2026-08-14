"""R11's Proposition 3.1, and the exact inequality that fails for dichotomous.

R11 (Lu-Mackenzie-Suzuki, Reading_11.pdf) is entirely ADDITIVE -- Section 2 fixes
u_i(S) = sum_{j in S} u_i(j).  But its Proposition 3.1 proves the envy-path bound
by a TELESCOPING argument far simpler than BDNSV20's modified-valuation trick:
with F_t := max({0} u {u_k(g) : g in J^t}) for the terminal agent k of the path,
maximum-weight optimality gives w_t(P) <= F_t - F_{t+1}, and summing telescopes
to w(P) <= F_1 <= 1.

Additivity enters in exactly two places, both "sum over rounds":

  (A)  u_i(A_i)  = sum_t u_i(mu_i^t)          -- own bundle
  (B)  u_i(A_j)  = sum_t u_i(mu_j^t)          -- someone else's bundle

Our IMWPM (imwpm_raw.py) matches on MARGINALS, and that makes (A) survive for
free: writing A_i^t for i's bundle after round t,

    vt_i(A_i) = sum_t [ vt_i(A_i^t) - vt_i(A_i^{t-1}) ] = sum_t mu_i^t(own),

an exact telescoping identity requiring no additivity at all.  (B) has no such
identity, and it is the whole gap.  What the proof actually needs is only the
inequality in one direction,

    (B')  vt_i(A_j)  <=  sum_t [ vt_i(A_i^{t-1} u {mu_j^t}) - vt_i(A_i^{t-1}) ],

that is, i's value for j's whole bundle is at most the sum of the marginals of
j's round-t items measured against i's own bundle at that time.  For SUBMODULAR
valuations (B') is immediate.  Dichotomous functions need not be submodular, so
(B') is exactly where the additive proof breaks, and this script measures the
defect

    D_ij := sum_t [ marginals of j's items over A_i^{t-1} ]  -  vt_i(A_j).

(B') is the claim D_ij >= 0.  Reported: how often it fails, and by how much --
because a defect bounded by 1 would still yield a path bound of 2, which with the
compensation of prop:bdnsv-fails-dichotomous is all conj:imwpm-bound needs.

Run:  python r11_gap.py
"""
from itertools import combinations, permutations
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_6")
from targetGbal import size_shift, rand_dicho     # noqa: E402

DUM = 10 ** 6


def imwpm_rounds(v, items, n):
    """imwpm_raw.imwpm, but recording each round's assignment and the bundles
    held at the START of that round.  Logic mirrors imwpm_raw.py exactly."""
    m = len(items)
    T = -(-m // n)
    pad = T * n - m
    dummies = list(range(DUM, DUM + pad))
    bundles = [frozenset() for _ in range(n)]

    def val(i, S):
        return v[i][frozenset(x for x in S if x < DUM)]

    remaining = list(items) + dummies
    rounds = []
    for _ in range(T):
        best = None
        real_rem = [x for x in remaining if x < DUM]
        dum_rem = [x for x in remaining if x >= DUM]
        take = min(n, len(real_rem))
        for r in range(0, take + 1):
            if len(dum_rem) < n - r:
                continue
            for rc in combinations(real_rem, r):
                dc = tuple(dum_rem[:n - r])
                batch = list(rc) + list(dc)
                for perm in permutations(batch):
                    tot = sum(val(i, bundles[i] | {perm[i]}) - val(i, bundles[i])
                              for i in range(n))
                    if best is None or tot > best[0]:
                        best = (tot, perm, rc, dc)
        _, perm, rc, dc = best
        rounds.append((list(bundles), list(perm)))     # (bundles BEFORE, item per agent)
        for i in range(n):
            bundles[i] = bundles[i] | {perm[i]}
        for x in rc:
            remaining.remove(x)
        for x in dc:
            remaining.remove(x)
    final = [frozenset(x for x in b if x < DUM) for b in bundles]
    return final, rounds


def defects(v, A, rounds, n):
    """D_ij for every ordered pair, per (B')."""
    def val(i, S):
        return v[i][frozenset(x for x in S if x < DUM)]

    out = {}
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            s = 0
            for (pre, assigned) in rounds:
                g = assigned[j]
                s += val(i, pre[i] | {g}) - val(i, pre[i])
            out[(i, j)] = s - v[i][A[j]]
    return out


def check_own_telescoping(v, A, rounds, n):
    """(A) must be exact: sum of own marginals equals value of own bundle."""
    def val(i, S):
        return v[i][frozenset(x for x in S if x < DUM)]
    for i in range(n):
        s = sum(val(i, pre[i] | {a[i]}) - val(i, pre[i]) for pre, a in rounds)
        if s != v[i][A[i]]:
            return False
    return True


def main():
    rng = random.Random(31415926)
    hist = Counter()
    tele_fail = 0
    tot = 0
    worst = None
    print("=== (B'): is v_i(A_j) <= sum_t marginal of j's round-t item ? ===")
    print("   n   m   inst   pairs   (B') violations   worst defect")
    for (n, m, T) in [(3, 5, 250), (3, 6, 180), (3, 7, 100), (3, 9, 40),
                      (4, 6, 120), (4, 8, 50), (5, 7, 40), (5, 9, 20)]:
        viol = pairs = cnt = 0
        wd = 0
        for _ in range(T):
            cs = [rand_dicho(m, rng) for _ in range(n)]
            if max(max(c.values()) for c in cs) < 1:
                continue
            cnt += 1
            tot += 1
            v = [size_shift(c, m) for c in cs]
            A, rounds = imwpm_rounds(v, list(range(m)), n)
            if not check_own_telescoping(v, A, rounds, n):
                tele_fail += 1
            D = defects(v, A, rounds, n)
            for key, d in D.items():
                pairs += 1
                hist[d] += 1
                if d < 0:
                    viol += 1
                    if d < wd:
                        wd = d
                    if worst is None or d < worst[0]:
                        worst = (d, n, m)
        print("  %2d  %2d  %5d  %6d   %15d   %12d" % (n, m, cnt, pairs, viol, wd))
    print()
    print("  instances                                  : %d" % tot)
    print("  (A) own-bundle telescoping FAILED          : %d  (must be 0)" % tele_fail)
    print("  defect distribution D_ij                   : %s"
          % dict(sorted(hist.items())))
    neg = sum(c for d, c in hist.items() if d < 0)
    print("  (B') violations (D_ij < 0)                 : %d of %d pairs"
          % (neg, sum(hist.values())))
    if neg == 0:
        print()
        print("  *** (B') HOLDS on all tested instances.  Then R11's Proposition 3.1")
        print("      transplants verbatim to marginal-weighted IMWPM and gives")
        print("      path weight <= 1 -- which would PROVE conj:imwpm-bound. ***")
    else:
        mn = min(hist)
        print("  most negative defect                       : %d" % mn)
        if mn >= -1:
            print()
            print("  *** (B') fails by at most 1.  R11's telescoping then yields a path")
            print("      bound of 2 rather than 1 -- which is exactly what")
            print("      obs:imwpm-two reports and what conj:imwpm-bound needs. ***")
        else:
            print("  defect below -1, so the telescoping gives no bound of 2 either")
        if worst:
            print("  worst case at n=%d m=%d" % (worst[1], worst[2]))


if __name__ == "__main__":
    main()
