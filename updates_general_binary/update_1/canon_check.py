"""
Is the tie-break doing real work, and does it hold at m=4?

canon_target.py says the leximin-optimal welfare maximiser of spread 2 is
always valid in the general binary class. Two things have to be checked before
that is worth writing down.

FIRST, the tie-break must not be vacuous. Section 24 records that not every
spread-2 welfare maximiser is valid -- an explicit witness has 4 of 10
maximisers invalid -- so the ALL column below should fall short of `inst`
while LEX does not. If ALL equalled LEX the tie-break would be doing nothing
and the statement would be weaker than it looks.

SECOND, m=3 is small enough that costs never exceed 3, so the sizes where
longer envy paths become possible have to be reached before the statement is
credible.
"""
import itertools
import random
import sys

from gb_valuations import (
    enumerate_general_binary,
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


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    m = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    k = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
    K = int(sys.argv[4]) if len(sys.argv) > 4 else 2

    pool = list(enumerate_general_binary(m))
    rng = random.Random(20260903)
    fam = family(n, m, K)
    print("general binary m=%d: %d valuations; n=%d, spread<=%d, %d instances"
          % (m, len(pool), n, K, k))

    st = {"inst": 0, "lex": 0, "all": 0, "any": 0, "ties": 0, "maxbucket": 0}
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
        st["maxbucket"] = max(st["maxbucket"], len(bucket))
        if len(bucket) > 1:
            st["ties"] += 1
        oks = [valid(vals, b) for b, _ in bucket]
        if all(oks):
            st["all"] += 1
        if any(oks):
            st["any"] += 1
        lex = min(bucket, key=lambda t: sorted(t[1], reverse=True))[0]
        if valid(vals, lex):
            st["lex"] += 1

    print()
    print("   instances                                  : %d" % st["inst"])
    print("   welfare maximisers tie (bucket > 1)        : %d  (largest bucket %d)"
          % (st["ties"], st["maxbucket"]))
    print("   ALL maximisers valid                       : %d%s"
          % (st["all"], "" if st["all"] == st["inst"] else "   <-- tie-break is NOT vacuous"))
    print("   SOME maximiser valid                       : %d" % st["any"])
    print("   the LEXIMIN maximiser valid                : %d%s"
          % (st["lex"], "   <-- NEVER FAILED" if st["lex"] == st["inst"] else ""))


if __name__ == "__main__":
    main()
