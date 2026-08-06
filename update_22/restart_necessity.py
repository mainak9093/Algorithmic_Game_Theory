"""What exactly would a proof of conj:algorithm-succeeds have to prove?

The construct-and-repair algorithm of Approach 6 has three steps: an IMWPM warm
start, a repair local search on (q-spread, -welfare) over balance-preserving
single-item moves, and RESTARTS from shuffled round-robin partitions when repair
stalls.  Its completeness (conj:algorithm-succeeds) is backed by 389,215
instances with no failure, but that evidence is over a finite sample and settles
nothing -- it says the conjecture may be true, which was already the position.

Before attempting a proof one must know which step carries the weight, because
the three demand very different arguments:

  (a) if repair alone always succeeds from the IMWPM warm start, completeness is
      a DESCENT statement about one starting point -- the same shape as
      conj:descent, and attackable;
  (b) if restarts are genuinely needed, completeness is a REACHABILITY statement
      over starting points, which presupposes that a good partition exists and
      then adds the claim that a shuffled round-robin start finds one.  That is
      strictly harder than Conjecture 2, not a route to it.

Measured here: over random instances, how often repair from the warm start
succeeds outright, and the distribution of the number of restarts consumed.

Run:  python restart_necessity.py
"""
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_6")
from targetGbal import size_shift, rand_dicho          # noqa: E402
from final_algorithm import solve, repair              # noqa: E402
from imwpm_raw import imwpm                            # noqa: E402


def main():
    rng = random.Random(20260806)
    hist = Counter()
    fail = 0
    tot = 0
    warmfail_examples = []
    print("=== restarts consumed by construct-and-repair ===")
    print("   n   m   inst   warm start alone   needed restarts   failed")
    for (n, m, T) in [(3, 5, 400), (3, 6, 300), (3, 7, 200), (3, 8, 120),
                      (4, 6, 200), (4, 7, 120), (4, 8, 60),
                      (5, 7, 60), (6, 8, 40), (8, 10, 25)]:
        warm = need = bad = cnt = 0
        for _ in range(T):
            cs = [rand_dicho(m, rng) for _ in range(n)]
            if max(max(c.values()) for c in cs) < 1:
                continue
            cnt += 1
            tot += 1
            v = [size_shift(c, m) for c in cs]
            ok, sp, r = solve(v, list(range(m)), n, rng)
            hist[r if ok else "FAIL"] += 1
            if not ok:
                bad += 1
                fail += 1
            elif r == 0:
                warm += 1
            else:
                need += 1
                if len(warmfail_examples) < 3:
                    warmfail_examples.append((n, m, r))
        print("  %2d  %2d  %5d   %16d   %15d   %6d" % (n, m, cnt, warm, need, bad))
    print()
    print("  instances                        : %d" % tot)
    print("  solved by warm start + repair    : %d" % hist[0])
    print("  needed at least one restart      : %d"
          % sum(v for k, v in hist.items() if k != "FAIL" and k != 0))
    print("  unsolved                         : %d" % fail)
    print("  restart-count histogram          : %s"
          % dict(sorted(hist.items(), key=lambda kv: (kv[0] == "FAIL", kv[0]))))
    print()
    if sum(v for k, v in hist.items() if k not in ("FAIL", 0)) == 0:
        print("  *** restarts NEVER used: completeness is a descent statement about")
        print("      the IMWPM warm start, which is a well-posed proof target. ***")
    else:
        print("  Restarts ARE used, so repair has genuine local optima and")
        print("  conj:algorithm-succeeds is a reachability claim over starting")
        print("  points -- it presupposes a good partition exists.  Proving it is")
        print("  therefore strictly harder than Conjecture 2, not a route to it.")
        print("  examples (n, m, restarts used): %s" % warmfail_examples)


if __name__ == "__main__":
    main()
