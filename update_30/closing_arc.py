"""Attack A: the closing arc of a heaviest path.

If P is a heaviest path from a ending at b, then P + (b,a) is a cycle, so
no-positive-cycle gives

    ell(a)  <=  -w(b,a)  =  c_b(A_a) - c_b(A_b).                    (CL)

(CL) never splits P, which is what rem:cancellation demands: every two-term
decomposition of ell has both parts unbounded.  And it is strictly weaker than the
uniform balance refuted in Approach 5, which asks w(v,u) >= -1 for ALL pairs; (CL)
needs it only for the single pair (b,a) where b ends a's heaviest path.

WHAT THIS SCRIPT CAN AND CANNOT SHOW.  "Closing arc >= -1" is EQUIVALENT to
ell(a) <= 1, since ell(a) >= 2 forces -w(b,a) >= 2 by (CL).  So testing it as a
hypothesis merely reproduces the ell distribution and is not independent evidence
-- the same trap as the (NPC) test in update_24.  Its value is as a PROOF TARGET,
being a claim about one pair rather than a path.  The useful measurement is
therefore what DISTINGUISHES the endpoint agents b, since that is what a proof
would have to exploit.

Measured, at the IMWPM allocation:
  - the distribution of the closing arc w(b,a) over (source, endpoint) pairs,
    against its distribution over ALL ordered pairs -- if endpoints are
    systematically better, that gap is the structure to prove;
  - the SLACK -w(b,a) - ell(a): if (CL) is tight, bounding the closing arc is the
    same problem as bounding ell and nothing is gained; if slack is large, the
    route is actively worse than what it replaces;
  - candidate characterisations of b: minimum own cost, extremal bundle size,
    never paid a round, etc.

Run:  python closing_arc.py
"""
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_6")
sys.path.insert(0, "../update_25")
sys.path.insert(0, "../update_26")
from targetGbal import subsets, size_shift, rand_dicho    # noqa: E402
from r11_gap import imwpm_rounds, DUM                     # noqa: E402
from q_formula import chores_d                            # noqa: E402


def disjoint_interest(m, n, rng):
    blocks = [[] for _ in range(n)]
    for g in range(m):
        blocks[rng.randrange(n)].append(g)
    return [{S: len(S & frozenset(blocks[i])) for S in subsets(m)}
            for i in range(n)]


def nested_interest(m, n, rng):
    cuts = sorted(rng.randrange(1, m + 1) for _ in range(n))
    return [{S: len(S & frozenset(range(cuts[i]))) for S in subsets(m)}
            for i in range(n)]


def main():
    rng = random.Random(30303030)
    close_h = Counter()
    all_h = Counter()
    slack_h = Counter()
    charac = Counter()
    npairs = 0
    tot = 0
    print("=== Attack A: closing arcs of heaviest paths at the IMWPM allocation ===")
    for (n, m, T) in [(3, 6, 120), (3, 8, 80), (3, 10, 40), (3, 12, 15),
                      (4, 7, 80), (4, 9, 40), (4, 11, 15),
                      (5, 8, 40), (5, 10, 15), (6, 10, 12)]:
        fams = [lambda m, n, r: [rand_dicho(m, r) for _ in range(n)],
                disjoint_interest, nested_interest]
        for _ in range(T):
            cs = fams[rng.randrange(len(fams))](m, n, rng)
            if max(max(c.values()) for c in cs) < 1:
                continue
            v = [size_shift(c, m) for c in cs]
            A, _ = imwpm_rounds(v, list(range(m)), n)
            A = [frozenset(x for x in b if x < DUM) for b in A]
            d = chores_d(cs, A, n)
            if d is None:
                continue
            tot += 1
            W = [[cs[i][A[i]] - cs[i][A[j]] for j in range(n)] for i in range(n)]
            kap = [cs[i][A[i]] for i in range(n)]
            size = [len(A[i]) for i in range(n)]
            for i in range(n):
                for j in range(n):
                    if i != j:
                        all_h[W[i][j]] += 1
            for a in range(n):
                ell = max(d[a][j] for j in range(n))
                if ell <= 0:
                    continue
                # endpoint of a heaviest path out of a
                b = max(range(n), key=lambda j: d[a][j])
                if b == a:
                    continue
                npairs += 1
                close_h[W[b][a]] += 1
                slack_h[(-W[b][a]) - ell] += 1
                if kap[b] == min(kap):
                    charac["b has min own cost"] += 1
                if kap[b] == 0:
                    charac["b never paid"] += 1
                if size[b] == max(size):
                    charac["b has max bundle"] += 1
                if size[b] == min(size):
                    charac["b has min bundle"] += 1
                if max(d[b][j] for j in range(n)) == 0:
                    charac["ell(b) = 0"] += 1
    print("  instances %d ; (source,endpoint) pairs with ell>=1 : %d" % (tot, npairs))
    print()
    print("  closing arc w(b,a) over ENDPOINT pairs : %s" % dict(sorted(close_h.items())))
    print("  arc weight over ALL ordered pairs      : %s" % dict(sorted(all_h.items())))
    print()
    print("  slack  -w(b,a) - ell(a)                : %s" % dict(sorted(slack_h.items())))
    print()
    print("  characterisations of the endpoint b (out of %d):" % npairs)
    for k in sorted(charac, key=lambda x: -charac[x]):
        print("     %-22s %6d  (%.1f%%)" % (k, charac[k], 100.0 * charac[k] / npairs))
    print()
    if close_h and min(close_h) >= -1:
        print("  closing arcs never below -1, so (CL) gives ell <= 1 throughout.")
    elif close_h:
        print("  closing arcs reach %d." % min(close_h))
    if slack_h and max(slack_h) == 0:
        print("  (CL) is TIGHT everywhere: bounding the closing arc IS bounding ell,")
        print("  so Attack A is a restatement, not a reduction.")
    elif slack_h:
        print("  (CL) has slack up to %d, so the closing arc is a STRICTLY HARDER"
              % max(slack_h))
        print("  target than ell itself -- Attack A is worse than what it replaces.")


if __name__ == "__main__":
    main()
