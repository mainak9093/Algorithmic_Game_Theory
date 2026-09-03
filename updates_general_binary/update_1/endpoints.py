"""
Does (W) follow from the intermediate-value argument alone?

D is 2-Lipschitz along the path (given (L)), and cannot step over the window
{0,1}: a move from D <= -1 to D >= 2 would need a jump of 3. So if the two
endpoints lie on OPPOSITE sides of the window, D must land in it and (INTERVAL)
is proved. The endpoints are

    D(0) = -mu(0)        block 1 empty
    D(m) = v(M)          blocks 2 and 3 empty, so mu(m) = 0.

The question is whether both endpoints can sit on the SAME side. If that never
happens, (W) is a corollary of the IVT and the proof closes. If it does happen,
D must be entering the window for some other reason, and the argument needs a
further ingredient -- so this distinguishes "proof complete modulo (L)" from
"proof still missing a step".

Cases counted:
    STRADDLE   one endpoint <= -1 and the other >= 2, or an endpoint already
               in the window
    SAME-LOW   both endpoints <= -1
    SAME-HIGH  both endpoints >= 2
and for the SAME cases, whether D nevertheless reaches the window.
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


def blocks(a, b, m):
    B1 = (1 << a) - 1
    B2 = ((1 << b) - 1) & ~B1
    B3 = ((1 << m) - 1) & ~((1 << b) - 1)
    return B1, B2, B3


def Dpath(v, m):
    Ds = []
    for a in range(m + 1):
        cand = [b for b in range(a, m + 1)
                if abs(v[blocks(a, b, m)[1]] - v[blocks(a, b, m)[2]]) <= 1]
        b = cand[0]
        B = blocks(a, b, m)
        Ds.append(v[B[0]] - min(v[B[1]], v[B[2]]))
    return Ds


def classify(Ds):
    d0, dm = Ds[0], Ds[-1]
    inwin = any(d in (0, 1) for d in Ds)
    if d0 in (0, 1) or dm in (0, 1):
        return "ENDPOINT-IN", inwin
    if (d0 <= -1 and dm >= 2) or (d0 >= 2 and dm <= -1):
        return "STRADDLE", inwin
    if d0 <= -1 and dm <= -1:
        return "SAME-LOW", inwin
    return "SAME-HIGH", inwin


def main():
    for m in (3, 4):
        pool = list(enumerate_general_binary(m))
        cnt, saved = {}, {}
        for v in pool:
            k, w = classify(Dpath(v, m))
            cnt[k] = cnt.get(k, 0) + 1
            if k.startswith("SAME"):
                saved[k] = saved.get(k, 0) + (1 if w else 0)
        print("m=%d, all %d valuations" % (m, len(pool)))
        for k in sorted(cnt):
            extra = ""
            if k.startswith("SAME"):
                extra = ("   of which D still reaches the window: %d / %d"
                         % (saved.get(k, 0), cnt[k]))
            print("   %-12s : %6d%s" % (k, cnt[k], extra))
        covered = cnt.get("ENDPOINT-IN", 0) + cnt.get("STRADDLE", 0)
        print("   IVT alone settles : %d / %d%s"
              % (covered, len(pool),
                 "   <-- PROOF CLOSES" if covered == len(pool)
                 else "   <-- a further ingredient is needed"))
        print()

    rng = random.Random(20260926)
    for m, trials in ((5, 3000), (6, 800), (7, 250)):
        cnt, saved = {}, {}
        for _ in range(trials):
            k, w = classify(Dpath(random_gb(m, rng), m))
            cnt[k] = cnt.get(k, 0) + 1
            if k.startswith("SAME"):
                saved[k] = saved.get(k, 0) + (1 if w else 0)
        covered = cnt.get("ENDPOINT-IN", 0) + cnt.get("STRADDLE", 0)
        same = {k: (cnt[k], saved.get(k, 0)) for k in cnt if k.startswith("SAME")}
        print("m=%d (%d): IVT alone settles %d | same-side cases %s"
              % (m, trials, covered, same if same else "none"))


if __name__ == "__main__":
    main()
