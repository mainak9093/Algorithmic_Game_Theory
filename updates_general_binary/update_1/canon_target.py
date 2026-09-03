"""
The same canonical-object idea, aimed at PS2 itself.

The (S1) experiments say a minimum-cost BALANCED allocation is valid once ties
are broken, and that four different tie-breaks all work. If the same holds for
general binary at spread 2, it is not a warm-up any more -- it is (S2), which
implies PS2 outright.

Section 24 already rules out the un-tie-broken version: not every welfare
maximiser of spread 2 is valid, and an explicit witness is on record with 4 of
10 maximisers invalid. So the question is exactly whether a tie-break repairs
it, and which one:

    LEX     leximin -- sort the cost profile descending, take the least
    MAX     least largest individual cost
    SQ      least sum of squared costs
    SPREAD  least (max cost - min cost)

The primary objective is welfare maximisation WITHIN the spread-bounded family,
not globally -- global welfare maximisation is refuted in section 19. The
control row is the spread bound itself: `any` reports whether some allocation
in the family is valid at all, so a tie-break failing while `any` succeeds is a
tie-break problem, and both failing together would be a failure of (S2).
"""
import itertools
import random
import sys

from gb_valuations import (
    enumerate_general_binary,
    enumerate_class,
    arc_weights,
    is_envy_freeable,
    longest_paths,
)


def valid(vals, b):
    if not is_envy_freeable(vals, b):
        return False
    return all(t <= 1 for t in longest_paths(arc_weights(vals, b)))


def family(n, m, K):
    out = []
    for assign in itertools.product(range(n), repeat=m):
        b = [0] * n
        for k, owner in enumerate(assign):
            b[owner] |= 1 << k
        s = [bin(x).count("1") for x in b]
        if max(s) - min(s) <= K:
            out.append(tuple(b))
    return out


def run(n, m, k, K, pool, label):
    rng = random.Random(20260903)
    fam = family(n, m, K)
    st = {"inst": 0, "lex": 0, "mx": 0, "sq": 0, "spread": 0, "any": 0}
    bad = []
    for _ in range(k):
        vals = [rng.choice(pool) for _ in range(n)]
        st["inst"] += 1
        best, bucket = None, []
        for b in fam:
            costs = tuple(-vals[i][b[i]] for i in range(n))
            tot = sum(costs)
            if best is None or tot < best:
                best, bucket = tot, [(b, costs)]
            elif tot == best:
                bucket.append((b, costs))

        def pick(key):
            return min(bucket, key=lambda t: key(t[1]))[0]

        cand = {
            "lex": pick(lambda c: sorted(c, reverse=True)),
            "mx": pick(lambda c: (max(c), sorted(c, reverse=True))),
            "sq": pick(lambda c: sum(t * t for t in c)),
            "spread": pick(lambda c: (max(c) - min(c), max(c))),
        }
        for key, b in cand.items():
            if valid(vals, b):
                st[key] += 1
        if any(valid(vals, b) for b in fam):
            st["any"] += 1
        elif len(bad) < 2:
            bad.append((vals, best))
    print("   %-28s inst %-5d | LEX %-5d MAX %-5d SQ %-5d SPREAD %-5d | any %-5d"
          % (label, st["inst"], st["lex"], st["mx"], st["sq"],
             st["spread"], st["any"]))
    for w in bad:
        print("      (S2) ITSELF FAILS: vals=%s" % (w[0],))


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    m = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    k = int(sys.argv[3]) if len(sys.argv) > 3 else 2000
    print("general binary, welfare-maximal inside the spread-bounded family")
    print("(a tie-break column equal to `inst` means it never failed)")
    print()
    gb = list(enumerate_general_binary(m))
    print("   general binary class on m=%d: %d valuations" % (m, len(gb)))
    for K in (1, 2):
        run(n, m, k, K, gb, "n=%d m=%d general K=%d" % (n, m, K))
    ch = enumerate_class(m, {-1, 0})
    run(n, m, k, 1, ch, "n=%d m=%d chores  K=1" % (n, m))


if __name__ == "__main__":
    main()
