"""
Checking three claims in PS3_n3_current_state_from_scratch.md.

CLAIM 1 (sections 5, 6, 29, 33). "Spread" is defined there as VALUE spread,
spr_i(A) = max_j v_i(A_j) - min_j v_i(A_j), and (S2) is stated as: every
instance admits an allocation with spr_i <= 2 for every agent AND subsidy in
{0,1}^3. The table quoted as evidence comes from approach_15 section 18, where
(S2) is about BUNDLE-SIZE spread, max_i |A_i| - min_i |A_i|. Those are
different conditions, so the value-spread version is tested here directly.

Both are reported side by side:
    SIZE   exists an allocation with size spread <= 2 and subsidy in {0,1}^3
    VALUE  exists an allocation with value spread <= 2 for EVERY agent, and
           subsidy in {0,1}^3
    PS2    exists a valid allocation at all (no spread condition)

CLAIM 2 (section 7, P4). v_1(S) = -|S| and v_2 = v_3 = -|S cap {a,b}| + [c in S]
on three items: every BALANCED allocation needs subsidy 2, while
({a}, {b,c}, empty) is valid with p = (1,0,0).

CLAIM 3 (section 9, P5). v_1 = 0 and v_2 = v_3 = max(0, |S|-1) on three items:
every globally welfare-maximal allocation needs subsidy 2, while
({a},{b},{c}) needs none.
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


def valid(vals, c):
    if not is_envy_freeable(vals, c):
        return False
    return max(longest_paths(arc_weights(vals, c))) <= 1


def size_spread(c):
    s = [bin(x).count("1") for x in c]
    return max(s) - min(s)


def value_spread(vals, c):
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


def claim1(m, trials, rng):
    A = allocs(m)
    st = {"inst": 0, "ps2": 0, "size": 0, "value": 0}
    wit = None
    for _ in range(trials):
        vals = [random_gb(m, rng) for _ in range(N)]
        st["inst"] += 1
        ok = [c for c in A if valid(vals, c)]
        if ok:
            st["ps2"] += 1
        if any(size_spread(c) <= 2 for c in ok):
            st["size"] += 1
        if any(value_spread(vals, c) <= 2 for c in ok):
            st["value"] += 1
        elif wit is None and ok:
            wit = (vals, min(value_spread(vals, c) for c in ok))
    print("   m=%d, %d instances : PS2 %d | SIZE-spread<=2 %d | VALUE-spread<=2 %d%s"
          % (m, st["inst"], st["ps2"], st["size"], st["value"],
             "" if st["value"] == st["inst"] else "   <-- VALUE VERSION FAILS"))
    if wit:
        print("      e.g. an instance where every valid allocation has value "
              "spread >= %d" % wit[1])
    return wit


def show(m, x):
    return "{" + ",".join("abc"[k] for k in range(m) if x & (1 << k)) + "}"


def claim2():
    m = 3
    v1 = tuple(-bin(S).count("1") for S in range(1 << m))
    def v23(S):
        return -bin(S & 0b011).count("1") + (1 if S & 0b100 else 0)
    v2 = tuple(v23(S) for S in range(1 << m))
    vals = [v1, v2, v2]
    bal = [c for c in allocs(m) if size_spread(c) <= 1]
    badbal = [c for c in bal if not valid(vals, c)]
    target = (0b001, 0b110, 0)
    print("   balanced allocations: %d, of which NOT valid: %d%s"
          % (len(bal), len(badbal),
             "   <-- every balanced one needs subsidy 2" if len(badbal) == len(bal) else ""))
    print("   ({a},{b,c},{}) valid : %s" % valid(vals, target))
    if valid(vals, target):
        print("      its minimal subsidy: %s"
              % longest_paths(arc_weights(vals, target)))


def claim3():
    m = 3
    v1 = tuple(0 for _ in range(1 << m))
    v2 = tuple(max(0, bin(S).count("1") - 1) for S in range(1 << m))
    vals = [v1, v2, v2]
    A = allocs(m)
    best = max(sum(vals[i][c[i]] for i in range(N)) for c in A)
    wmax = [c for c in A if sum(vals[i][c[i]] for i in range(N)) == best]
    badw = [c for c in wmax if not valid(vals, c)]
    sep = (0b001, 0b010, 0b100)
    print("   welfare maximum %d, attained by %d allocations, of which NOT valid: %d%s"
          % (best, len(wmax), len(badw),
             "   <-- every welfare maximiser needs subsidy 2"
             if len(badw) == len(wmax) else ""))
    print("   ({a},{b},{c}) valid : %s  subsidy %s"
          % (valid(vals, sep), longest_paths(arc_weights(vals, sep))))


def main():
    rng = random.Random(20260911)
    print("CLAIM 1 -- value spread versus size spread")
    for m, t in ((3, 3000), (4, 800), (5, 200)):
        claim1(m, t, rng)
    print()
    print("CLAIM 2 -- section 7 / P4, balanced is insufficient")
    claim2()
    print()
    print("CLAIM 3 -- section 9 / P5, global welfare maximisation is insufficient")
    claim3()


if __name__ == "__main__":
    main()
