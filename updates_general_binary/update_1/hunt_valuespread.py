"""
Hunting the VALUE-spread reading of (S2).

PS3_n3_current_state_from_scratch.md sections 5, 6, 29 and 33 state (S2) with
spread meaning VALUE spread, spr_i(A) = max_j v_i(A_j) - min_j v_i(A_j) <= 2
for every agent, and the whole roadmap -- in particular the Extreme-Agent
Redistribution Lemma of section 29 -- is built on it. The table quoted as
evidence is from approach_15 section 18, which measured BUNDLE-SIZE spread, so
the value-spread version needs its own test.

Random sampling passes it. That is worth very little in this class: (CANON)
passed 2,250 random instances and died to a climb, and the SUM potential passed
random sampling and died to a climb. So this hill-climbs directly at it.

    OBJECTIVE  maximise  min { value spread of A : A valid }
    REFUTED    that minimum reaches 3 -- i.e. PS2 holds for the instance but
               EVERY valid allocation has some agent seeing a value spread of
               3 or more, so no allocation satisfies section 5's (S2)

Instances with no valid allocation at all are discarded rather than counted as
refutations: those would refute PS2 itself, which is reported separately.
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


def score(vals, A):
    """min value spread over valid allocations; None if PS2 fails."""
    best = None
    for c in A:
        if valid(vals, c):
            s = vspread(vals, c)
            if best is None or s < best:
                best = s
    return best


def main():
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    seeds = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    steps = int(sys.argv[3]) if len(sys.argv) > 3 else 300
    rng = random.Random(20260912)
    A = []
    for o in itertools.product(range(N), repeat=m):
        b = [0] * N
        for k, i in enumerate(o):
            b[i] |= 1 << k
        A.append(tuple(b))
    print("n=3, m=%d : %d allocations; %d climbs x %d steps"
          % (m, len(A), seeds, steps))

    refuted = ps2_fail = 0
    best_seen = 0
    for _ in range(seeds):
        cur = [list(random_gb(m, rng)) for _ in range(N)]
        s = score([tuple(v) for v in cur], A)
        cur_s = -1 if s is None else s
        for _ in range(steps):
            i = rng.randrange(N)
            S = rng.randrange(1, 1 << m)
            old = cur[i][S]
            cur[i][S] = old + rng.choice((-1, 1))
            if not legal(tuple(cur[i]), m):
                cur[i][S] = old
                continue
            vals = [tuple(v) for v in cur]
            s2 = score(vals, A)
            if s2 is None:
                ps2_fail += 1
                print("   PS2 ITSELF FAILS: vals=%s" % (vals,))
                cur[i][S] = old
                continue
            if s2 >= 3:
                refuted += 1
                print("   VALUE-SPREAD (S2) REFUTED: every valid allocation has "
                      "value spread >= %d" % s2)
                print("      vals=%s" % (vals,))
                break
            if s2 >= cur_s:
                cur_s = s2
                best_seen = max(best_seen, s2)
            else:
                cur[i][S] = old

    print()
    print("   climbs refuting the value-spread (S2) : %d / %d" % (refuted, seeds))
    print("   instances where PS2 itself failed     : %d" % ps2_fail)
    print("   largest 'min value spread' reached    : %d  (3 would refute)"
          % best_seen)


if __name__ == "__main__":
    main()
