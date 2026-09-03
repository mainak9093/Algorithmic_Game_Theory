"""
Splitting (AVOID) into a free case and a narrow hard case.

Every obstruction pattern contains an entry equal to 2. So an allocation whose
gap matrix has all entries <= 1 -- equivalently, every agent's value spread is
at most 1 -- dominates no obstruction and is therefore VALID, with no further
argument. That disposes of every instance admitting such an allocation.

    STEP 1  if some allocation has value spread <= 1 for every agent, done.
    STEP 2  otherwise every allocation forces some agent to a spread of 2,
            and the 2-entries must be arranged to avoid C, A and B.

vspread_dist.py says step 2 is rare -- about 1.5% at m=3 and 0.3% at m=4 -- so
the whole difficulty of (AVOID) is concentrated there. This script isolates
those instances and asks what they look like:

  - do they still admit an obstruction-free allocation, and how many?
  - among their spread-2 allocations, WHERE do the 2-entries sit -- how many
    are there, and in what shape?
  - which of the three obstructions is the binding one, i.e. which rules out
    the most allocations?

The point is to see whether the hard case has a rigid enough form to attack
directly, since it is now the only case left.
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


def ghat(vals, c):
    G = []
    for i in range(N):
        best = max(vals[i][c[j]] for j in range(N))
        G.append(tuple(min(best - vals[i][c[j]], 2) for j in range(N)))
    return tuple(G)


def valid(vals, c):
    if not is_envy_freeable(vals, c):
        return False
    return max(longest_paths(arc_weights(vals, c))) <= 1


def good_multiset(vals, b):
    return any(valid(vals, tuple(b[p[i]] for i in range(N)))
               for p in itertools.permutations(range(N)))


BASE = {"C": ((0, 0, 2), (0, 0, 2), (0, 0, 2)),
        "A": ((0, 0, 0), (0, 2, 2), (0, 2, 2)),
        "B": ((0, 0, 1), (0, 1, 2), (0, 1, 2))}
ORB = {}
for k, p in BASE.items():
    s = set()
    for rp in itertools.permutations(range(N)):
        for cp in itertools.permutations(range(N)):
            s.add(tuple(tuple(p[rp[i]][cp[j]] for j in range(N))
                        for i in range(N)))
    ORB[k] = s


def hits(G):
    """Which obstruction classes this pattern dominates."""
    out = set()
    for k, s in ORB.items():
        for o in s:
            if all(G[i][j] >= o[i][j] for i in range(N) for j in range(N)):
                out.add(k)
                break
    return out


def main():
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 6000
    rng = random.Random(20260918)
    allocs = []
    for o in itertools.product(range(N), repeat=m):
        b = [0] * N
        for k, i in enumerate(o):
            b[i] |= 1 << k
        allocs.append(tuple(b))

    st = {"inst": 0, "step1": 0, "step2": 0, "step2_clean": 0,
          "step2_noclean": 0}
    binding = {"C": 0, "A": 0, "B": 0}
    twocount = {}
    examples = []
    for _ in range(trials):
        vals = [random_gb(m, rng) for _ in range(N)]
        st["inst"] += 1
        Gs = [(c, ghat(vals, c)) for c in allocs]
        flat = [(c, G) for (c, G) in Gs
                if max(G[i][j] for i in range(N) for j in range(N)) <= 1]
        if flat:
            st["step1"] += 1
            continue
        st["step2"] += 1
        cl = [(c, G) for (c, G) in Gs if not hits(G)]
        if cl:
            st["step2_clean"] += 1
            for c, G in cl[:1]:
                n2 = sum(1 for i in range(N) for j in range(N) if G[i][j] == 2)
                twocount[n2] = twocount.get(n2, 0) + 1
                if len(examples) < 4:
                    examples.append((G, n2))
        else:
            st["step2_noclean"] += 1
        for c, G in Gs:
            for k in hits(G):
                binding[k] += 1

    print("n=3, m=%d, %d instances" % (m, trials))
    print("   STEP 1  some allocation has value spread <= 1 (free)   : %d"
          % st["step1"])
    print("   STEP 2  every allocation forces a spread of 2 (hard)   : %d"
          % st["step2"])
    if st["step2"]:
        print("      of those, an obstruction-free allocation exists     : %d%s"
              % (st["step2_clean"],
                 "   <-- always" if st["step2_clean"] == st["step2"] else ""))
        print("      of those, NONE exists (would refute AVOID)          : %d"
              % st["step2_noclean"])
        print("      2-entries in the clean allocation found: %s"
              % dict(sorted(twocount.items())))
        print("      obstruction hits across all allocations: %s" % binding)
        print()
        print("      example clean gap matrices from the hard case:")
        for G, n2 in examples:
            print("         %s   (%d twos)" % (list(G), n2))


if __name__ == "__main__":
    main()
