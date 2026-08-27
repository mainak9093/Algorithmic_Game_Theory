"""
Approach 15: the exhaustive n=3, m=3 general binary sweep, specialised for
speed. Same question as hunt_counterexample.py --

    is there an instance where EVERY complete allocation needs subsidy >= 2
    for some agent?

-- but at n=3, m=3 there are C(497,3) = 20,338,440 multisets of valuations,
which the readable implementation would grind through for over an hour. This
version precomputes, for each valuation and each of the 3^3 = 27 allocations,
the triple of bundle values that agent would see, so the inner loop is pure
indexing with no set arithmetic and no function calls.

CROSS-VALIDATION. The specialisation is only trustworthy if it agrees with the
readable implementation, so `python hunt_n3m3.py check` reruns both on the two
boundary classes at n=3, m=3 (9880 multisets each) and compares instance
counts and maxima. Run that before trusting `python hunt_n3m3.py run`.

Progress is flushed to stdout as it goes, so a killed run still leaves a
usable partial record rather than an empty log.
"""
import itertools
import sys
import time

from gb_valuations import (
    enumerate_general_binary,
    enumerate_class,
    best_over_allocations,
    bundles_from_assignment,
)

N, M = 3, 3

# The 27 complete allocations, as triples of bundle masks.
ALLOCS = [bundles_from_assignment(a, N, M)
          for a in itertools.product(range(N), repeat=M)]

PERMS = list(itertools.permutations(range(N)))


def build_table(pool):
    """table[v][k] = (v(B_0), v(B_1), v(B_2)) for allocation k."""
    return [[(v[b[0]], v[b[1]], v[b[2]]) for b in ALLOCS] for v in pool]


def worst_subsidy_fast(r0, r1, r2):
    """
    max_i p*_i for one allocation, given each agent's row of the three bundle
    values, or None if the allocation is not envy-freeable.

    r_i[j] is agent i's value for bundle j, so the envy-graph arc weight is
    w[i][j] = r_i[j] - r_i[i]. Envy-freeability is Halpern-Shah (ii): no
    reassignment of the bundles beats the identity in utilitarian welfare.
    l(i) is then the heaviest simple path out of i; at n=3 the paths out of i
    are i->j, i->k, i->j->k and i->k->j, so the maximum is written out in full.
    """
    base = r0[0] + r1[1] + r2[2]
    rows = (r0, r1, r2)
    for p in PERMS:
        if rows[0][p[0]] + rows[1][p[1]] + rows[2][p[2]] > base:
            return None

    w01 = r0[1] - r0[0]
    w02 = r0[2] - r0[0]
    w10 = r1[0] - r1[1]
    w12 = r1[2] - r1[1]
    w20 = r2[0] - r2[2]
    w21 = r2[1] - r2[2]

    l0 = max(0, w01, w02, w01 + w12, w02 + w21)
    l1 = max(0, w10, w12, w10 + w02, w12 + w20)
    l2 = max(0, w20, w21, w20 + w01, w21 + w10)
    return max(l0, l1, l2)


def sweep(pool, label, progress_every=0):
    table = build_table(pool)
    npool = len(pool)
    worst, worst_key = -1, None
    counterexamples = []
    total = 0
    t0 = time.time()

    for a in range(npool):
        ta = table[a]
        for b in range(a, npool):
            tb = table[b]
            for c in range(b, npool):
                tc = table[c]
                total += 1
                best = None
                for k in range(27):
                    val = worst_subsidy_fast(ta[k], tb[k], tc[k])
                    if val is None:
                        continue
                    if best is None or val < best:
                        best = val
                        if best == 0:
                            break
                if best is None:
                    print("  !! no envy-freeable allocation:", (a, b, c))
                    continue
                if best > worst:
                    worst, worst_key = best, (a, b, c)
                if best >= 2:
                    counterexamples.append(((a, b, c), best))
                    if len(counterexamples) <= 3:
                        print("  COUNTEREXAMPLE %s value=%d"
                              % (str((a, b, c)), best), flush=True)
                        for idx in (a, b, c):
                            print("      ", pool[idx], flush=True)
        if progress_every and (a + 1) % progress_every == 0:
            print("  ... %d/%d outer, %d instances, max=%d, %.0fs"
                  % (a + 1, npool, total, worst, time.time() - t0), flush=True)

    dt = time.time() - t0
    print("  %-22s n=3 m=3 : %d instances, max = %d, counterexamples = %d "
          "(%.1fs)" % (label, total, worst, len(counterexamples), dt),
          flush=True)
    if worst_key is not None:
        print("       witness attaining %d:" % worst)
        for idx in worst_key:
            print("      ", pool[idx], flush=True)
    return total, worst, counterexamples


def check():
    """Fast path must agree with the readable implementation."""
    ok = True
    for label, allowed in (("goods {0,1}", {0, 1}),
                           ("chores {-1,0}", {-1, 0})):
        pool = enumerate_class(M, allowed)
        print("cross-check on %s (%d valuations)" % (label, len(pool)))

        total_f, worst_f, ce_f = sweep(pool, "fast " + label)

        worst_s, total_s = -1, 0
        for vals in itertools.combinations_with_replacement(pool, N):
            total_s += 1
            value, _ = best_over_allocations(vals, N, M)
            if value is not None and value > worst_s:
                worst_s = value
        print("  slow  %-16s : %d instances, max = %d"
              % (label, total_s, worst_s))

        agree = (total_f == total_s and worst_f == worst_s and not ce_f)
        print("  agreement: %s" % ("OK" if agree else "MISMATCH"))
        ok = ok and agree
        print()
    print("cross-validation %s" % ("PASSED" if ok else "FAILED"))
    return ok


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "check"
    if mode == "check":
        check()
    elif mode == "run":
        pool = list(enumerate_general_binary(M))
        n = len(pool)
        print("EXHAUSTIVE n=3 m=3, general binary: %d valuations, "
              "%d multisets" % (n, n * (n + 1) * (n + 2) // 6), flush=True)
        sweep(pool, "general {-1,0,1}", progress_every=25)
    else:
        print("usage: hunt_n3m3.py [check|run]")


if __name__ == "__main__":
    main()
