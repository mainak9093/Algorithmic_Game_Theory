"""
How large does the value spread of a VALID allocation actually have to be?

hunt_valuespread.py could not push
    minimum over valid allocations of the value spread
above 1 in 12,500 evaluations. If that quantity is always <= 1 then two things
in PS3_n3_current_state_from_scratch.md need revising: section 15, which lists
"simultaneous value-spread <= 1" as a FAILED route, and section 5, whose
constant 2 would then be slack rather than tight.

This measures the distribution directly, and climbs at several sizes to try to
force it up. There is a reason to expect a small answer: if A is valid with
subsidy p in {0,1}^3 then for every i and j,

    v_i(A_j) - v_i(A_i) = w(i,j) <= p_i - p_j <= 1,

so v_i(A_i) is within 1 of the MAXIMUM. The spread is only large if some
bundle is far BELOW agent i's own -- which costs nothing in subsidy terms. So
the interesting question is whether an instance can force every valid
allocation to contain such a far-below bundle.
"""
import itertools
import random
import sys

from gb_valuations import (
    masks_by_popcount, arc_weights, is_envy_freeable, longest_paths)

N = 3


def random_gb(m, rng):
    v = [0] * (1 << m)
    for S in masks_by_popcount(m):
        if S == 0:
            continue
        bits = [1 << b for b in range(m) if S & (1 << b)]
        v[S] = rng.randint(max(v[S ^ b] for b in bits) - 1,
                           min(v[S ^ b] for b in bits) + 1)
    return tuple(v)


def legal(v, m):
    for S in range(1 << m):
        for b in range(m):
            if not S & (1 << b) and v[S | (1 << b)] - v[S] not in (-1, 0, 1):
                return False
    return v[0] == 0


def valid(vals, c):
    if not is_envy_freeable(vals, c):
        return False
    return max(longest_paths(arc_weights(vals, c))) <= 1


def vspread(vals, c):
    return max(max(vals[i][c[j]] for j in range(N))
               - min(vals[i][c[j]] for j in range(N)) for i in range(N))


def allocs(m):
    out = []
    for o in itertools.product(range(N), repeat=m):
        b = [0] * N
        for k, i in enumerate(o):
            b[i] |= 1 << k
        out.append(tuple(b))
    return out


def best(vals, A):
    s = None
    for c in A:
        if valid(vals, c):
            t = vspread(vals, c)
            if s is None or t < s:
                s = t
    return s


def main():
    rng = random.Random(20260913)
    for m, trials in ((3, 4000), (4, 1200), (5, 300), (6, 60)):
        A = allocs(m)
        hist = {}
        for _ in range(trials):
            vals = [random_gb(m, rng) for _ in range(N)]
            s = best(vals, A)
            hist[s] = hist.get(s, 0) + 1
        print("   m=%d (%d instances): min value spread over valid allocations = %s"
              % (m, trials, dict(sorted(hist.items(),
                                        key=lambda t: (t[0] is None, t[0])))))

    print()
    print("climbing to force it up (m=4 and m=3, 60 climbs x 300 steps each):")
    for m in (3, 4):
        A = allocs(m)
        top = 0
        for _ in range(60):
            cur = [list(random_gb(m, rng)) for _ in range(N)]
            s = best([tuple(v) for v in cur], A)
            cs = -1 if s is None else s
            for _ in range(300):
                i = rng.randrange(N)
                S = rng.randrange(1, 1 << m)
                old = cur[i][S]
                cur[i][S] = old + rng.choice((-1, 1))
                if not legal(tuple(cur[i]), m):
                    cur[i][S] = old
                    continue
                s2 = best([tuple(v) for v in cur], A)
                if s2 is not None and s2 >= cs:
                    cs = s2
                    top = max(top, s2)
                else:
                    cur[i][S] = old
        print("   m=%d : largest forced minimum value spread = %d" % (m, top))


if __name__ == "__main__":
    main()
