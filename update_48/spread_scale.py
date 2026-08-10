"""Does (A) survive m >> n?  The regime where minimum spread could exceed 2.

spread_hardcore.py found minimum spread never above 2 over 9,640 instances, but
every one had m <= 7 and n >= 3, i.e. m about n.  That is the EASY regime and
the test was close to rigged: with m/n small each bundle holds one or two items,
so |D_i & B_t| is 0 or 1 and spread <= 1 is nearly forced.

The honest regime is m >> n.  For a random partition, |D_i & B_t| concentrates
around |D_i|/n with deviation about sqrt(|D_i|/n), so a spread above 2 needs
|D_i| of order 4n, i.e. m of order 4n at least.  For n = 3 that means m >= 12,
which no sweep in this project has ever reached.  Optimal partitions do far
better than random -- that is exactly what discrepancy theory is about -- but the
question is whether the optimum stays at 2, and nothing so far tests it.

Note also which failure would matter.  Balance is RIGID exactly for binary
additive costs, since then sum_t c_i(B_t) = c_i(M) is fixed; that is why
prop:no-balance is additive.  So (A) is likeliest to fail there -- but binary
additive is already closed by thm:binadd, so such a failure would refute (F5) as
stated while leaving Conjecture 2 untouched.  Both are therefore tracked:

    (A)   minimum spread <= 2 over ALL instances
    (A')  minimum spread <= 2 over instances NOT covered by S1-S3
          -- the only version that (F5) needs in order to close Conjecture 2

METHOD.  Searching for a spread-<=2 partition exits as soon as one is found,
which is the common case and cheap.  Only when none exists is the full n^m
enumeration paid for -- and that is precisely the interesting instance, so the
cost lands where it should.  Nothing is capped: a reported failure means the
whole space was searched.

Run:  python spread_scale.py
"""
from itertools import product
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_5")
sys.path.insert(0, "../update_17")
sys.path.insert(0, "../update_47")
from routeA import ellvec                                        # noqa: E402
from minimum_subsidy import subsets                              # noqa: E402
from cri_sweep import is_dichotomous                             # noqa: E402
from residual_map import show_costs, is_binary_additive          # noqa: E402
from residual_attack import matching_good                        # noqa: E402
from spread_hardcore import composed, rand_f                     # noqa: E402


def spread_of(cs, bd, n):
    return max(max(cs[i][b] for b in bd) - min(cs[i][b] for b in bd)
               for i in range(n))


def find_spread_le(cs, n, m, k):
    """First partition of spread <= k, or None after exhausting all n^m."""
    for assign in product(range(n), repeat=m):
        bd = [frozenset(g for g in range(m) if assign[g] == i)
              for i in range(n)]
        if spread_of(cs, bd, n) <= k:
            return bd
    return None


def min_spread_exhaustive(cs, n, m):
    best = None
    for assign in product(range(n), repeat=m):
        bd = [frozenset(g for g in range(m) if assign[g] == i)
              for i in range(n)]
        s = spread_of(cs, bd, n)
        if best is None or s < best:
            best = s
            if best == 0:
                break
    return best


def gen(m, n, rng, mode):
    """Large-|D| composed costs: the regime where balance can actually fail."""
    cs = []
    for _ in range(n):
        k = rng.randrange(max(2, m // 2), m + 1)      # big sets
        D = frozenset(rng.sample(range(m), k))
        cs.append(composed(D, rand_f(k, rng, mode), m))
    return cs


def main():
    rng = random.Random(8102026)
    print("=== (A): is the minimum spread still <= 2 when m >> n? ===")
    print()
    print("  %-10s %-7s %6s %7s  %-22s %s"
          % ("mode", "n,m", "m/n", "inst", "spread>2 (all)", "spread>2 (residual)"))
    bad = []
    badres = []
    tot = 0
    SP = Counter()
    for (n, m, T) in [(3, 9, 60), (3, 10, 40), (3, 11, 25), (3, 12, 12),
                      (3, 13, 6), (4, 9, 25), (4, 10, 12), (5, 10, 6)]:
        for mode in ("additive", "capped", "free"):
            cnt = lb = lr = 0
            for _ in range(T):
                cs = gen(m, n, rng, mode)
                if max(max(c.values()) for c in cs) < 1:
                    continue
                assert all(is_dichotomous(c, m) for c in cs)
                cnt += 1
                tot += 1
                bd = find_spread_le(cs, n, m, 2)
                if bd is not None:
                    SP["<=2"] += 1
                    continue
                # no spread-2 family: pay for the exact minimum
                s = min_spread_exhaustive(cs, n, m)
                SP[s] += 1
                lb += 1
                if len(bad) < 3:
                    bad.append((n, m, mode, cs, s))
                if not all(is_binary_additive(c, m) for c in cs):
                    lr += 1
                    if len(badres) < 3:
                        badres.append((n, m, mode, cs, s))
            if cnt:
                print("  %-10s %-7s %6.1f %7d  %-22d %d"
                      % (mode, "%d,%d" % (n, m), m / n, cnt, lb, lr))

    print()
    print("  instances                              : %d" % tot)
    print("  spread distribution                    : %s"
          % dict(sorted(SP.items(), key=lambda z: str(z[0]))))
    print("  (A)  minimum spread > 2, any instance  : %d"
          % sum(v for k, v in SP.items() if k != "<=2"))
    print("  (A') minimum spread > 2, NOT binary additive : %d" % len(badres))
    print()

    if not bad:
        print("  *** (A) SURVIVES into the m >> n regime, up to m/n = 4.3."
              "  The")
        print("      minimum spread stayed at most 2 on every instance, so")
        print("      (F5) is still standing where it was most likely to fall.")
        print("      ***")
        return

    n, m, mode, cs, s = bad[0]
    print("  *** (A) FAILS.  An instance whose minimum spread is %d, so no" % s)
    print("      family of spread <= 2 exists at all and (F5) is FALSE as")
    print("      stated.  n=%d m=%d mode=%s  (searched all %d partitions)"
          % (n, m, mode, n ** m))
    show_costs(cs, n, m)
    print("      binary additive: %s"
          % all(is_binary_additive(c, m) for c in cs))
    print()
    if badres:
        n, m, mode, cs, s = badres[0]
        print("  *** AND IT FAILS OUTSIDE THE SOLVED CASES: minimum spread %d"
              % s)
        print("      on a NON binary additive instance, so (F5) cannot close")
        print("      Conjecture 2 either.  n=%d m=%d mode=%s" % (n, m, mode))
        show_costs(cs, n, m)
    else:
        print("  But every failure is binary additive, which thm:binadd already")
        print("  closes.  So (F5) is false as stated while (F5') -- the same")
        print("  claim restricted to instances outside the solved cases -- is")
        print("  still standing, and that is the version Conjecture 2 needs.")


if __name__ == "__main__":
    main()
