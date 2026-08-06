"""What does the IMWPM warm start actually guarantee?  Attacking conj:warmstart.

conj:warmstart says repair from the IMWPM warm start reaches q-spread <= 1 with
no restarts.  Unlike conj:descent it does not quantify over all partitions, so
the proof may use properties of the starting point -- but only if the starting
point HAS properties.  Three things are measured.

(1) THE STARTING SPREAD.  What is q-spread of IMWPM's raw output, before any
    repair?  This is the crux for provability.  If it is always small, say <= 2,
    then repair has at most one rung to descend and conj:warmstart reduces to
      "every balanced partition with q-spread exactly 2 has an improving move",
    a far smaller claim than a general descent lemma.  If it is unbounded, the
    proof must control an arbitrarily long descent.

(2) THE TRAPS.  Bad local optima exist -- 14 were found at n=3, m=5 from
    round-robin starts.  How many instances HAVE such a trap, and in how many
    does IMWPM's trajectory enter one?  A large gap between the two is the
    content of conj:warmstart and says what the warm start is buying.

(3) EXHAUSTIVE CHECK, restarts disabled, on the families where exhaustive
    enumeration is possible: the full n=m=3 family (9,880 instances) and the
    structured non-additive pools of targetGbal_stress.  Previous evidence for
    the algorithm allowed restarts; this isolates the warm start.

Run:  python warmstart.py
"""
from itertools import combinations, combinations_with_replacement, product
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_6")
from targetGbal import subsets, size_shift, gen_functions, rand_dicho  # noqa: E402
from targetGbal_local import score, round_robin_partition             # noqa: E402
from imwpm_raw import imwpm                                           # noqa: E402
from final_algorithm import repair                                    # noqa: E402


def spread_of(v, groups, n):
    key, _ = score(v, groups, n)
    return key[0]


def has_improving_move(v, groups, n):
    key, _ = score(v, groups, n)
    for a in range(n):
        for b in range(n):
            if a == b:
                continue
            for x in groups[a]:
                trial = list(groups)
                trial[a] = groups[a] - {x}
                trial[b] = groups[b] | {x}
                sz = [len(g) for g in trial]
                if max(sz) - min(sz) > 1:
                    continue
                if score(v, trial, n)[0] < key:
                    return True
    return False


def traps_exist(v, m, n):
    """Is there ANY balanced partition that is a bad local optimum?"""
    for assign in product(range(n), repeat=m):
        groups = [frozenset(g for g in range(m) if assign[g] == i)
                  for i in range(n)]
        sz = [len(g) for g in groups]
        if max(sz) - min(sz) > 1:
            continue
        if spread_of(v, groups, n) <= 1:
            continue
        if not has_improving_move(v, groups, n):
            return True
    return False


def run(v, m, n, stats, deep=False):
    A = list(imwpm(v, list(range(m)), n))
    stats["start_spread"][spread_of(v, A, n)] += 1
    ok, sp = repair(v, A, n)
    if ok:
        stats["warm_ok"] += 1
    else:
        stats["warm_fail"] += 1
        stats["fail_spread"][sp] += 1
    if deep:
        t = traps_exist(v, m, n)
        if t:
            stats["has_trap"] += 1
            if not ok:
                stats["fell_in"] += 1
    return ok


def main():
    rng = random.Random(11223344)
    stats = Counter()
    stats["start_spread"] = Counter()
    stats["fail_spread"] = Counter()

    print("=== (3) exhaustive n = m = 3, restarts DISABLED ===")
    F = gen_functions(3)
    cnt = 0
    for cs in combinations_with_replacement(F, 3):
        v = [size_shift(c, 3) for c in cs]
        run(v, 3, 3, stats, deep=True)
        cnt += 1
    print("  instances %d ; warm-start failures %d ; instances with a trap %d ;"
          " trajectories entering a trap %d"
          % (cnt, stats["warm_fail"], stats["has_trap"], stats["fell_in"]))

    print()
    print("=== (3) structured non-additive pools, exhaustive triples ===")
    from targetGbal_stress import structured_pool
    for m in (3, 4, 5):
        s2 = Counter()
        s2["start_spread"] = Counter()
        s2["fail_spread"] = Counter()
        pool = structured_pool(m)
        c = 0
        for cs in combinations(pool, 3):
            v = [size_shift(x, m) for x in cs]
            run(v, m, 3, s2, deep=(m <= 5))
            c += 1
        print("  m=%d : %d instances ; warm-start failures %d ; with a trap %d ;"
              " entered a trap %d"
              % (m, c, s2["warm_fail"], s2["has_trap"], s2["fell_in"]))
        for k, val in s2["start_spread"].items():
            stats["start_spread"][k] += val
        stats["warm_fail2"] += s2["warm_fail"]

    print()
    print("=== (3) randomised, larger, restarts DISABLED ===")
    for (n, m, T) in [(3, 6, 250), (3, 7, 150), (4, 6, 150), (4, 7, 80),
                      (5, 7, 50), (6, 8, 30)]:
        f = 0
        for _ in range(T):
            cs = [rand_dicho(m, rng) for _ in range(n)]
            if max(max(c.values()) for c in cs) < 1:
                continue
            v = [size_shift(c, m) for c in cs]
            if not run(v, m, n, stats):
                f += 1
        print("  n=%d m=%d : %d instances, warm-start failures %d" % (n, m, T, f))

    print()
    print("=== (1) q-spread of the IMWPM output, BEFORE repair ===")
    tot = sum(stats["start_spread"].values())
    for k in sorted(stats["start_spread"]):
        print("   spread %2d : %6d  (%.2f%%)"
              % (k, stats["start_spread"][k],
                 100.0 * stats["start_spread"][k] / tot))
    mx = max(stats["start_spread"])
    print()
    print("  maximum starting q-spread observed : %d" % mx)
    if mx <= 2:
        print("  *** IMWPM always starts at spread <= 2, so conj:warmstart reduces")
        print("      to: every balanced partition with q-spread 2 reachable as an")
        print("      IMWPM output has an improving move.  One rung, not a descent. ***")
    else:
        print("  IMWPM's output spread is not bounded by 2, so repair may have to")
        print("  descend several rungs and the proof must control the whole path.")
    print()
    print("  total warm-start failures across everything : %d"
          % (stats["warm_fail"] + stats["warm_fail2"]))


if __name__ == "__main__":
    main()
