"""
Approach 15: welfare maximisation is NOT the right canonical rule.

A welfare-maximal allocation is always envy-freeable, so it is the first thing
one would reach for: pick the allocation maximising sum_i v_i(A_i) and read off
its minimal subsidy. This script shows that rule fails, and fails in the
easiest possible setting -- the pure DICHOTOMOUS GOODS class, where BKNS's
Theorem 4 guarantees some allocation achieves subsidy at most 1 per agent.

What is exhibited is the strong form: an instance in which EVERY globally
welfare-maximal allocation leaves some agent needing subsidy 2. So no
tie-breaking among welfare maximisers can rescue the rule.

The contrast with the spread-bounded rule is the point. Restricting to
allocations of spread <= 2 and maximising welfare inside that smaller family
never failed in any experiment, while maximising over everything does. The
constraint costs welfare and buys short envy paths.

Everything is recomputed from scratch here rather than imported, since this is
a negative claim.
"""
import itertools
import sys

from gb_valuations import enumerate_class, enumerate_general_binary


def popcount(x):
    return bin(x).count("1")


def welfare(vals, bundles, n):
    return sum(vals[i][bundles[i]] for i in range(n))


def envy_freeable(vals, bundles, n):
    base = welfare(vals, bundles, n)
    for perm in itertools.permutations(range(n)):
        if sum(vals[i][bundles[perm[i]]] for i in range(n)) > base:
            return False
    return True


def subsidy(vals, bundles, n):
    """Minimal subsidy by explicit enumeration of simple paths."""
    if not envy_freeable(vals, bundles, n):
        return None

    def w(i, j):
        return vals[i][bundles[j]] - vals[i][bundles[i]]

    out = []
    for i in range(n):
        best = 0
        others = [j for j in range(n) if j != i]
        for r in range(1, n):
            for path in itertools.permutations(others, r):
                tot, cur = 0, i
                for nxt in path:
                    tot += w(cur, nxt)
                    cur = nxt
                best = max(best, tot)
        out.append(best)
    return out


def allocations(n, m):
    for assign in itertools.product(range(n), repeat=m):
        b = [0] * n
        for k, owner in enumerate(assign):
            b[owner] |= 1 << k
        yield tuple(b)


def spread(bundles):
    z = [popcount(b) for b in bundles]
    return max(z) - min(z)


def analyse(vals, n, m):
    allocs = list(allocations(n, m))
    best = max(welfare(vals, b, n) for b in allocs)
    gwm = [b for b in allocs if welfare(vals, b, n) == best]

    gwm_min = None
    for b in gwm:
        p = subsidy(vals, b, n)
        if p is None:
            continue
        gwm_min = max(p) if gwm_min is None else min(gwm_min, max(p))

    # the spread-bounded rule, for contrast
    fam = [b for b in allocs if spread(b) <= 2]
    fbest = max(welfare(vals, b, n) for b in fam)
    twm = [b for b in fam if welfare(vals, b, n) == fbest]
    twm_min = None
    for b in twm:
        p = subsidy(vals, b, n)
        if p is None:
            continue
        twm_min = max(p) if twm_min is None else min(twm_min, max(p))

    overall = None
    for b in allocs:
        p = subsidy(vals, b, n)
        if p is not None:
            overall = max(p) if overall is None else min(overall, max(p))
    return gwm, gwm_min, twm, twm_min, overall


def show(mask, m):
    return "{" + ",".join("abcdefg"[k] for k in range(m)
                          if mask & (1 << k)) + "}"


def search(n, m, allowed, label):
    pool = (enumerate_class(m, allowed) if allowed != {-1, 0, 1}
            else list(enumerate_general_binary(m)))
    print("searching %s at n=%d m=%d (%d valuations)"
          % (label, n, m, len(pool)))
    for vals in itertools.combinations_with_replacement(pool, n):
        gwm, gwm_min, twm, twm_min, overall = analyse(vals, n, m)
        if gwm_min is not None and gwm_min >= 2 and overall is not None \
                and overall <= 1:
            return vals, gwm, gwm_min, twm, twm_min, overall
    return None


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "goods"
    n, m = 3, 3
    allowed, label = ({0, 1}, "dichotomous goods") if which == "goods" \
        else ({-1, 0, 1}, "general binary")

    found = search(n, m, allowed, label)
    if found is None:
        print("no instance found in this class at n=%d m=%d" % (n, m))
        return

    vals, gwm, gwm_min, twm, twm_min, overall = found
    print()
    print("WITNESS -- %s, n=%d, m=%d" % (label, n, m))
    for i, v in enumerate(vals):
        print("   agent %d  %s" % (i + 1, str(v)))
    print()
    print("   best achievable max-subsidy over ALL allocations : %d" % overall)
    print("   best among GLOBAL welfare maximisers             : %d"
          % gwm_min)
    print("   best among welfare maximisers of spread <= 2     : %d"
          % twm_min)
    print()
    print("   the %d global welfare maximisers, all of them bad:" % len(gwm))
    for b in gwm:
        print("      %s  welfare=%d spread=%d subsidy=%s"
              % (" ".join(show(x, m) for x in b), welfare(vals, b, n),
                 spread(b), subsidy(vals, b, n)))
    print()
    print("   a spread-bounded welfare maximiser that works:")
    for b in twm:
        p = subsidy(vals, b, n)
        if p is not None and max(p) <= 1:
            print("      %s  welfare=%d spread=%d subsidy=%s"
                  % (" ".join(show(x, m) for x in b), welfare(vals, b, n),
                     spread(b), p))
            break
    print()
    print("CONFIRMED: every global welfare maximiser needs subsidy %d, while"
          % gwm_min)
    print("subsidy %d is achievable -- welfare maximisation is not the rule."
          % overall)


if __name__ == "__main__":
    main()
