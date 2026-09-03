"""
A sharper sufficient condition: confine the 2-entries to one row.

hard_residue.py shows the whole difficulty of (AVOID) lives in the ~1% of
instances where no allocation has every value spread <= 1, and that the clean
allocations found there put their 2-entries in a single ROW.

That is not a coincidence. Every one of the three obstructions needs 2-entries
in at least TWO rows:

    C  needs a whole COLUMN at >= 2, so all three rows;
    A  needs two rows each carrying two entries >= 2;
    B  needs two rows each carrying an entry >= 2 in a common column.

So if every 2-entry lies in one row, no obstruction can be dominated. Part 1
verifies this against all 30 obstruction patterns rather than trusting the
reading. Note a row can hold at most TWO twos, since every row contains a zero.

    LEMMA (one row).  If all entries ghat_i(j) = 2 lie in a single row, the
                      allocation is valid.

    (AVOID-1ROW)      every instance admits such an allocation -- equivalently,
                      an allocation in which AT MOST ONE agent sees a value
                      spread of 2 and no agent sees more.

Part 2 tests (AVOID-1ROW) by sampling and Part 3 climbs at it, since two claims
in this line have already died to climbs after passing random sampling.
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


BASE = [((0, 0, 2), (0, 0, 2), (0, 0, 2)),
        ((0, 0, 0), (0, 2, 2), (0, 2, 2)),
        ((0, 0, 1), (0, 1, 2), (0, 1, 2))]
OBS = set()
for p in BASE:
    for rp in itertools.permutations(range(N)):
        for cp in itertools.permutations(range(N)):
            OBS.add(tuple(tuple(p[rp[i]][cp[j]] for j in range(N))
                          for i in range(N)))


def one_row(G):
    rows = {i for i in range(N) for j in range(N) if G[i][j] == 2}
    return len(rows) <= 1


def allocs_for(m):
    out = []
    for o in itertools.product(range(N), repeat=m):
        b = [0] * N
        for k, i in enumerate(o):
            b[i] |= 1 << k
        out.append(tuple(b))
    return out


def main():
    print("PART 1 -- every obstruction needs 2-entries in at least two rows")
    worst = 9
    for o in OBS:
        rows = {i for i in range(N) for j in range(N) if o[i][j] == 2}
        worst = min(worst, len(rows))
    print("   fewest rows carrying a 2, over all %d obstructions : %d%s"
          % (len(OBS), worst,
             "   <-- LEMMA HOLDS" if worst >= 2 else "   <-- LEMMA FALSE"))

    print()
    print("PART 2 -- does an allocation with all 2s in one row always exist?")
    rng = random.Random(20260919)
    for m, trials in ((3, 3000), (4, 800), (5, 200)):
        A = allocs_for(m)
        ok = sound = 0
        for _ in range(trials):
            vals = [random_gb(m, rng) for _ in range(N)]
            cand = [c for c in A if one_row(ghat(vals, c))]
            if cand:
                ok += 1
                if all(good_multiset(vals, c) for c in cand):
                    sound += 1
            else:
                sound += 1
        print("   m=%d (%d instances): exists %d%s | all such really valid %d"
              % (m, trials, ok,
                 "" if ok == trials else "   <-- FAILS", sound))

    print()
    print("PART 3 -- climbing at (AVOID-1ROW)")
    for m, seeds, steps in ((4, 60, 300), (5, 25, 200)):
        A = allocs_for(m)
        refuted = 0
        fewest = 10 ** 9
        for _ in range(seeds):
            cur = [list(random_gb(m, rng)) for _ in range(N)]
            cnt = sum(1 for c in A if one_row(ghat([tuple(v) for v in cur], c)))
            for _ in range(steps):
                i = rng.randrange(N)
                S = rng.randrange(1, 1 << m)
                old = cur[i][S]
                cur[i][S] = old + rng.choice((-1, 1))
                if not legal(tuple(cur[i]), m):
                    cur[i][S] = old
                    continue
                vals = [tuple(v) for v in cur]
                c2 = sum(1 for c in A if one_row(ghat(vals, c)))
                if c2 == 0:
                    refuted += 1
                    print("   (AVOID-1ROW) REFUTED at m=%d: vals=%s" % (m, vals))
                    break
                if c2 <= cnt:
                    cnt = c2
                    fewest = min(fewest, c2)
                else:
                    cur[i][S] = old
        print("   m=%d : %d climbs, refutations %d, fewest one-row "
              "allocations reached %d  (0 would refute)"
              % (m, seeds, refuted, fewest))


if __name__ == "__main__":
    main()
