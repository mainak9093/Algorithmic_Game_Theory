"""(F5) tested where it actually bites: instances of minimum spread 2.

    (F5)  every instance admits a family of spread <= 2 whose maximum-weight
          matching has ell <= 1.

thm:balanced-class is the spread <= 1 case, so the only new content of (F5) is
spread exactly 2.  spread_conjecture.py ran 1,792 random instances and found
minimum spread 0 or 1 on every single one -- not one spread-2 instance -- so
that test said nothing about (F5) at all.  It merely re-confirmed that S4 covers
almost everything.  All existing evidence is the 92 constructed residual
instances, which is a biased sample selected precisely for having no spread-1
family.  That is the LEXB failure mode waiting to happen (rem:n3-rules-fail:
227 instances, then 368).

So this script GENERATES spread-2 instances instead of hoping for them, and
splits (F5) into the two claims it bundles:

    (A) is the minimum spread over families always <= 2?
    (B) on a minimum-spread family, is the maximum-weight matching good?

(A) is the one that could fail silently.  If some instance has minimum spread 3
then (F5) is false as stated and the right constant is not 2 -- which matters,
because thm:smallbundle's argument gives ell <= spread and so degrades one for
one.  A spread-3 instance is therefore the single most valuable thing this
script can find, and it is looked for deliberately.

GENERATORS, all inside the composed family c_i(S) = f_i(|S & D_i|), which is
where the residual lives:

  hardcore   D_i a random subset of size >= 2, f_i random {0,1} increments
  skeleton   D_i = M minus a small set -- the shape of prop:no-balance, where
             near-covering sets force the discrepancy obstruction
  additive   f_i = identity: binary additive, the rigid case for balance
  capped     f_i = identity then flat: keeps the balance constraint, kills
             additivity -- the construction that produced the first residual
             instances

For (B), two strengths are separated, because a constructive theorem needs the
stronger one:
  (B-some)  SOME min-spread family has SOME optimal matching that is good
  (B-all)   SOME min-spread family has EVERY optimal matching good

Run:  python spread_hardcore.py
"""
from itertools import combinations, permutations, product
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_5")
sys.path.insert(0, "../update_17")
sys.path.insert(0, "../update_47")
from routeA import partitions, ellvec                            # noqa: E402
from minimum_subsidy import subsets                              # noqa: E402
from cri_sweep import is_dichotomous                             # noqa: E402
from residual_map import show_costs, classify                    # noqa: E402
from residual_attack import spread, matching_good                # noqa: E402

NAMES = "abcdefghij"


def composed(D, f, m):
    return {S: f[len(S & D)] for S in subsets(m)}


def rand_f(k, rng, mode):
    if mode == "additive":
        return list(range(k + 1))
    if mode == "capped":
        cap = rng.randrange(1, max(2, k))
        return [min(t, cap) for t in range(k + 1)]
    f = [0]
    for _ in range(k):
        f.append(f[-1] + rng.randrange(2))
    return f


def gen_hardcore(m, n, rng, mode="free", skeleton=False):
    cs = []
    for _ in range(n):
        if skeleton:
            drop = rng.randrange(0, max(1, m // 2))
            D = frozenset(rng.sample(range(m), m - drop))
        else:
            k = rng.randrange(2, m + 1)
            D = frozenset(rng.sample(range(m), k))
        cs.append(composed(D, rand_f(len(D), rng, mode), m))
    return cs


GENS = [
    ("hardcore", lambda m, n, r: gen_hardcore(m, n, r, "free")),
    ("skeleton", lambda m, n, r: gen_hardcore(m, n, r, "free", True)),
    ("additive", lambda m, n, r: gen_hardcore(m, n, r, "additive", True)),
    ("capped", lambda m, n, r: gen_hardcore(m, n, r, "capped", True)),
]


def min_spread_families(cs, n, m):
    best = None
    fams = []
    for bd in partitions(m, n):
        s = spread(cs, bd, n)
        if best is None or s < best:
            best, fams = s, [bd]
        elif s == best:
            fams.append(bd)
    return best, fams


def good_exists(cs, n, m):
    for bd in partitions(m, n):
        e = ellvec(cs, bd, n)
        if e is not None and max(e) <= 1:
            return True
    return False


def main():
    rng = random.Random(20260810)
    print("=== (F5) on instances of minimum spread 2 ===")
    print()
    SP = Counter()
    n_sp2 = bsome = ball = 0
    hi = []          # min spread >= 3
    bfail = []       # (B) failures
    c2fail = 0
    tot = 0

    print("  %-10s %-6s %6s   %-26s %7s %7s"
          % ("gen", "n,m", "inst", "min-spread distribution",
             "sprd>=3", "(B) bad"))
    for (n, m, T) in [(3, 4, 500), (3, 5, 400), (3, 6, 250), (3, 7, 90),
                      (4, 4, 400), (4, 5, 250), (4, 6, 90),
                      (5, 4, 250), (5, 5, 90), (6, 4, 90)]:
        for name, gen in GENS:
            loc = Counter()
            lh = lb = cnt = 0
            for _ in range(T):
                cs = gen(m, n, rng)
                if max(max(c.values()) for c in cs) < 1:
                    continue
                assert all(is_dichotomous(c, m) for c in cs), name
                cnt += 1
                tot += 1
                s, fams = min_spread_families(cs, n, m)
                loc[s] += 1
                SP[s] += 1
                if s >= 3:
                    lh += 1
                    if len(hi) < 3:
                        hi.append((n, m, name, cs, s))
                if s == 2:
                    n_sp2 += 1
                    ok_s = ok_a = False
                    for bd in fams:
                        a, b = matching_good(cs, bd, n)
                        ok_s = ok_s or a
                        ok_a = ok_a or b
                    bsome += ok_s
                    ball += ok_a
                    if not ok_s:
                        lb += 1
                        if len(bfail) < 3:
                            bfail.append((n, m, name, cs, s))
                    if not good_exists(cs, n, m):
                        c2fail += 1
                        print("  *** CONJECTURE 2 FAILS n=%d m=%d %s"
                              % (n, m, name))
                        show_costs(cs, n, m)
            if cnt:
                print("  %-10s %-6s %6d   %-26s %7d %7d"
                      % (name, "%d,%d" % (n, m), cnt,
                         str(dict(sorted(loc.items()))), lh, lb))

    print()
    print("  instances                        : %d" % tot)
    print("  minimum-spread distribution      : %s" % dict(sorted(SP.items())))
    print("  instances of minimum spread 2    : %d" % n_sp2)
    print()
    print("  (A) minimum spread >= 3          : %d" % sum(SP[s] for s in SP
                                                          if s >= 3))
    print("  (B-some) good on a min-spread family : %d / %d"
          % (bsome, n_sp2))
    print("  (B-all)  EVERY optimal matching good : %d / %d"
          % (ball, n_sp2))
    print("  Conjecture 2 failures (control)  : %d" % c2fail)
    print()

    if hi:
        n, m, name, cs, s = hi[0]
        print("  *** (A) FAILS -- minimum spread %d.  (F5) is FALSE as stated;"
              % s)
        print("      the constant is not 2.  n=%d m=%d gen=%s" % (n, m, name))
        show_costs(cs, n, m)
    elif n_sp2 == 0:
        print("  *** STILL VACUOUS: no spread-2 instance was generated, so")
        print("      (F5) remains untested.  The generators need more bite. ***")
    elif bsome == n_sp2:
        print("  *** (F5) SURVIVES on %d instances of minimum spread 2 --" % n_sp2)
        print("      the case that is not already thm:balanced-class.  Minimum")
        print("      spread never exceeded 2 over %d instances." % tot)
        if ball < n_sp2:
            print("      Note (B-all) fails %d times, so the theorem must pick"
                  % (n_sp2 - ball))
            print("      the matching, not merely any optimal one.")
    else:
        n, m, name, cs, s = bfail[0]
        print("  *** (B) FAILS: a min-spread family whose maximum-weight")
        print("      matching is never good.  n=%d m=%d gen=%s" % (n, m, name))
        show_costs(cs, n, m)
        print("      Conjecture 2 itself: %s" % good_exists(cs, n, m))


if __name__ == "__main__":
    main()
