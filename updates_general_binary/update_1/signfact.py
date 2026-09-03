"""
Sign constancy, with the direction corrected.

shift.py tested the wrong orientation. The walk on an ordered set S has
d_t = v(P_t) - v(Q_t) with P_0 EMPTY, so

    d_0 = -v(S)   and   d_k = +v(S),

the opposite of what was assumed there. Redone:

    FACT 1.  Steps satisfy |d_{t+1} - d_t| <= 2, so d cannot cross from <= -2
    to >= 2 without entering [-1,1]. Hence before the least balanced cut t* all
    d_t share one sign, and

        v(S) >= 2   =>  d starts at <= -2, so d_{t*} is -1 or 0, giving
                        v(P) <= v(Q) and  beta(S) = v(P_{t*})   -- the PREFIX
        v(S) <= -2  =>  d starts at >= 2, so d_{t*} is 0 or 1, giving
                        beta(S) = v(Q_{t*})   -- the SUFFIX
        |v(S)| <= 1 =>  d_0 is already in [-1,1], so t* = 0 and
                        beta(S) = min(0, v(S))

The prefix case is the useful one, because prefixes of S and of
S' = S minus its first element differ by exactly one item:
P_{j+1}(S) = P'_j(S') + s_1, so their values are within 1. If the least
balanced cut shifted by one, (L) would follow immediately -- but shift.py
refutes that, with shifts up to 4. This script confirms FACT 1 in the corrected
form and measures how far apart the two levels can be given the shift, which is
what a proof still has to bridge.
"""
import random
import sys

from gb_valuations import masks_by_popcount, enumerate_general_binary


def random_gb(m, rng):
    v = [0] * (1 << m)
    for S in masks_by_popcount(m):
        if S == 0:
            continue
        bits = [1 << b for b in range(m) if S & (1 << b)]
        v[S] = rng.randint(max(v[S ^ b] for b in bits) - 1,
                           min(v[S ^ b] for b in bits) + 1)
    return tuple(v)


def walk(v, items):
    """Returns (t*, prefix mask, suffix mask, d at t*)."""
    full = 0
    for g in items:
        full |= 1 << g
    pre = 0
    for t in range(len(items) + 1):
        suf = full & ~pre
        d = v[pre] - v[suf]
        if abs(d) <= 1:
            return t, pre, suf, d
        if t < len(items):
            pre |= 1 << items[t]
    return None


def main():
    for m in (3, 4):
        pool = list(enumerate_general_binary(m))
        n = ok = 0
        step_ok = 0
        gapmax = 0
        for v in pool:
            for a in range(m):
                items = list(range(a, m))
                if len(items) < 1:
                    continue
                r = walk(v, items)
                if r is None:
                    print("   two-bundle lemma failed -- impossible")
                    return
                t, pre, suf, d = r
                full = 0
                for g in items:
                    full |= 1 << g
                vS = v[full]
                n += 1
                if vS >= 2:
                    good = (d in (-1, 0)) and min(v[pre], v[suf]) == v[pre]
                elif vS <= -2:
                    good = (d in (0, 1)) and min(v[pre], v[suf]) == v[suf]
                else:
                    good = (t == 0)
                ok += 1 if good else 0
                # step bound along this walk
                p2 = 0
                prev = v[0] - v[full]
                bad = False
                for g in items:
                    p2 |= 1 << g
                    cur = v[p2] - v[full & ~p2]
                    if abs(cur - prev) > 2:
                        bad = True
                    prev = cur
                step_ok += 0 if bad else 1
                if len(items) >= 2:
                    r2 = walk(v, items[1:])
                    gapmax = max(gapmax,
                                 abs(min(v[pre], v[suf])
                                     - min(v[r2[1]], v[r2[2]])))
        print("m=%d : %d ordered suffixes" % (m, n))
        print("   step bound |d_{t+1}-d_t| <= 2        : %d / %d%s"
              % (step_ok, n, "   <-- ALWAYS" if step_ok == n else ""))
        print("   FACT 1 corrected (sign + which side) : %d / %d%s"
              % (ok, n, "   <-- ALWAYS" if ok == n else "   <-- FAILS"))
        print("   largest |beta(S) - beta(S')| seen    : %d   (L) says <= 1"
              % gapmax)
        print()


if __name__ == "__main__":
    main()
