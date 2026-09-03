"""
Towards a proof of (L): sign constancy, and how far the least balanced cut moves.

Two structural facts, the first PROVED here, reduce (L) to a single question.

FACT 1 (sign constancy, proved). Along the walk on an ordered set S, write
d_t = v(P_t) - v(Q_t). Steps satisfy |d_{t+1} - d_t| <= 2, so d cannot change
sign without first entering [-1,1]: to go from d >= 2 to d <= -2 needs a jump
of 4. Hence before the FIRST balanced cut t*, all d_t have one sign, and:

    v(S) >= 2   =>  d_{t*} is 0 or 1, so v(P) >= v(Q) and beta(S) = v(Q_{t*})
    v(S) <= -2  =>  d_{t*} is -1 or 0, so beta(S) = v(P_{t*})
    |v(S)| <= 1 =>  t* = 0 and beta(S) = min(0, v(S))

So in the main case the level is just the SUFFIX value at the least balanced
cut. Writing S' = S minus its first element, the cuts correspond with
Q_{j+1}(S) = Q'_j(S'), so beta(S) = y_{t*(S) - 1} in the notation of S'.

FACT 2 (the remaining question). beta(S') = y_{t*(S')}, and consecutive y
values differ by at most 1 -- the suffix loses one item. So

    |beta(S) - beta(S')| <= | (t*(S) - 1) - t*(S') |,

and (L) follows at once IF the least balanced cut moves by at most one under
deletion of the first element. That is the claim measured here:

    (SHIFT)  | t*(S) - 1 - t*(S') | <= 1.

If (SHIFT) holds, (L) is proved in the main case and only the small |v(S)| <= 1
cases remain.
"""
import itertools
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


def tstar(v, items):
    """items is an ordered list of bit positions; returns (t*, level, dsign)."""
    k = len(items)
    pre = 0
    full = 0
    for g in items:
        full |= 1 << g
    for t in range(k + 1):
        suf = full & ~pre
        if abs(v[pre] - v[suf]) <= 1:
            return t, min(v[pre], v[suf]), v[pre] - v[suf]
        if t < k:
            pre |= 1 << items[t]
    return None


def main():
    print("PART 1 -- exhaustive: sign constancy and (SHIFT)")
    for m in (3, 4):
        pool = list(enumerate_general_binary(m))
        n = 0
        sign_ok = shift_ok = lip_ok = 0
        worst_shift = 0
        bad = None
        for v in pool:
            for a in range(m - 1):          # suffixes of length >= 2
                items = list(range(a, m))
                items2 = list(range(a + 1, m))
                r1 = tstar(v, items)
                r2 = tstar(v, items2)
                if r1 is None or r2 is None:
                    continue
                t1, b1, d1 = r1
                t2, b2, d2 = r2
                n += 1
                full = 0
                for g in items:
                    full |= 1 << g
                vS = v[full]
                # FACT 1: the level is the suffix value when v(S) >= 2
                pre = 0
                for g in items[:t1]:
                    pre |= 1 << g
                suf = full & ~pre
                if vS >= 2:
                    sign_ok += 1 if (0 <= d1 <= 1 and b1 == v[suf]) else 0
                elif vS <= -2:
                    sign_ok += 1 if (-1 <= d1 <= 0 and b1 == v[pre]) else 0
                else:
                    sign_ok += 1 if t1 == 0 else 0
                s = abs((t1 - 1) - t2)
                worst_shift = max(worst_shift, s)
                if s <= 1:
                    shift_ok += 1
                elif bad is None:
                    bad = (v, a, t1, t2)
                if abs(b1 - b2) <= 1:
                    lip_ok += 1
        print("   m=%d : %d (suffix, shorter suffix) pairs" % (m, n))
        print("      FACT 1 sign constancy / level identity : %d / %d%s"
              % (sign_ok, n, "   <-- ALWAYS" if sign_ok == n else "   <-- FAILS"))
        print("      (SHIFT) |t*(S)-1 - t*(S')| <= 1        : %d / %d%s"
              "   (largest %d)"
              % (shift_ok, n,
                 "   <-- ALWAYS" if shift_ok == n else "   <-- FAILS",
                 worst_shift))
        print("      (L) |beta(S) - beta(S')| <= 1          : %d / %d%s"
              % (lip_ok, n, "   <-- ALWAYS" if lip_ok == n else "   <-- FAILS"))
        if bad:
            print("      a (SHIFT) failure: v=%s suffix from %d, t*=%d t*'=%d"
                  % bad)

    print()
    print("PART 2 -- sampling at larger m")
    rng = random.Random(20260928)
    for m, trials in ((6, 1500), (8, 400)):
        n = sign_ok = shift_ok = lip_ok = 0
        worst_shift = 0
        for _ in range(trials):
            v = random_gb(m, rng)
            for a in range(m - 1):
                r1 = tstar(v, list(range(a, m)))
                r2 = tstar(v, list(range(a + 1, m)))
                if r1 is None or r2 is None:
                    continue
                t1, b1, d1 = r1
                t2, b2, d2 = r2
                n += 1
                s = abs((t1 - 1) - t2)
                worst_shift = max(worst_shift, s)
                shift_ok += 1 if s <= 1 else 0
                lip_ok += 1 if abs(b1 - b2) <= 1 else 0
        print("   m=%d : %d pairs | (SHIFT) %d%s (largest %d) | (L) %d%s"
              % (m, n, shift_ok,
                 "" if shift_ok == n else "   <-- FAILS", worst_shift,
                 lip_ok, "" if lip_ok == n else "   <-- FAILS"))


if __name__ == "__main__":
    main()
