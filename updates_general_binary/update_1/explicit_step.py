"""
Can the (BAL-STEP) move be written down explicitly -- recipient AND prices?

Insert g into B_x and keep every other price. Only two updates are available
for position x itself, and their failure modes are exactly complementary.
Write d_i = c_i(g | B_x) in {0,1}.

  KEEP  (q'_x = q_x). The score of x falls by d_i. Agents with d_i = 0 are
        untouched; an agent with d_i = 1 who demanded x may now drop it. The
        risk is that x becomes too UNattractive and someone is left stranded.

  RAISE (q'_x = 1, only available when q_x = 0). The score of x moves by
        1 - d_i. Agents with d_i = 1 are untouched; an agent with d_i = 0 who
        already demanded x collapses to demanding ONLY x. The risk is that x
        becomes too attractive and two agents collide on it.

So the two updates fail in opposite directions, which is why a proof should be
able to pick one. This script asks whether that is enough: is there always a
minimum-size position x and one of these two updates that lands on a valid
state, with no search over the remaining prices at all?

It also isolates the pairs where the choice of recipient genuinely matters,
since those are the only ones a proof has to think about.
"""
import itertools
import random
import sys

from gb_valuations import enumerate_class


def perfect_matching(adj, n):
    match = [-1] * n
    def go(i, seen):
        for j in adj[i]:
            if not seen[j]:
                seen[j] = True
                if match[j] == -1 or go(match[j], seen):
                    match[j] = i
                    return True
        return False
    return sum(1 for i in range(n) if go(i, [False] * n)) == n


def demand(vals, bundles, q, n):
    adj = []
    for i in range(n):
        sc = [vals[i][bundles[j]] + q[j] for j in range(n)]
        top = max(sc)
        adj.append([j for j in range(n) if sc[j] == top])
    return adj


def matchable(vals, bundles, q, n):
    return perfect_matching(demand(vals, bundles, q, n), n)


def good(vals, bundles, n):
    for mask in sorted(range(1 << n), key=lambda t: bin(t).count("1")):
        q = [(mask >> j) & 1 for j in range(n)]
        if matchable(vals, bundles, q, n):
            return True
    return False


def witness(vals, bundles, n):
    """Fewest subsidised positions first -- a canonical witness."""
    for mask in sorted(range(1 << n), key=lambda t: (bin(t).count("1"), t)):
        q = [(mask >> j) & 1 for j in range(n)]
        if matchable(vals, bundles, q, n):
            return q
    return None


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    m = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    k = int(sys.argv[3]) if len(sys.argv) > 3 else 4000

    pool = enumerate_class(m, {-1, 0})
    rng = random.Random(20260903)
    print("chores class m=%d: %d valuations; sampled tuples: %d (n=%d)"
          % (m, len(pool), k, n))

    st = {"pairs": 0, "explicit": 0, "keep": 0, "raise": 0,
          "no_explicit": 0, "unsub_min": 0, "choice_matters": 0,
          "rC": 0, "rD": 0}
    hard = []

    for _ in range(k):
        vals = [rng.choice(pool) for _ in range(n)]
        for assign in itertools.product(list(range(n)) + [None], repeat=m):
            b = [0] * n
            for idx, owner in enumerate(assign):
                if owner is not None:
                    b[owner] |= 1 << idx
            b = tuple(b)
            s = [bin(x).count("1") for x in b]
            if max(s) - min(s) > 1:
                continue
            q = witness(vals, b, n)
            if q is None:
                continue
            unalloc = [idx for idx in range(m) if assign[idx] is None]
            lo = min(s)
            L = [i for i in range(n) if s[i] == lo]

            for g in unalloc:
                st["pairs"] += 1
                bit = 1 << g
                if any(q[x] == 0 for x in L):
                    st["unsub_min"] += 1

                works, expl = {}, {}
                for x in L:
                    nb = list(b)
                    nb[x] |= bit
                    nb = tuple(nb)
                    works[x] = good(vals, nb, n)
                    qk = list(q)
                    ok_keep = matchable(vals, nb, qk, n)
                    qr = list(q)
                    qr[x] = 1
                    ok_raise = matchable(vals, nb, qr, n)
                    expl[x] = (ok_keep, ok_raise)

                if not all(works.values()):
                    st["choice_matters"] += 1
                    d = {x: [vals[i][b[x]] - vals[i][b[x] | bit]
                             for i in range(n)] for x in L}
                    if len(hard) < 8:
                        hard.append((b, g, list(L), list(q), d, dict(works),
                                     dict(expl)))

                anyk = any(expl[x][0] for x in L)
                anyr = any(expl[x][1] for x in L)
                if anyk or anyr:
                    st["explicit"] += 1
                    st["keep"] += 1 if anyk else 0
                    st["raise"] += 1 if anyr else 0
                else:
                    st["no_explicit"] += 1

                clash = {x: sum(1 for i in range(n)
                                if (vals[i][b[x]] - vals[i][b[x] | bit]) == 0
                                and x in demand(vals, b, q, n)[i])
                         for x in L}
                xc = min(L, key=lambda x: (q[x], clash[x]))
                xd = min(L, key=lambda x: (clash[x], q[x]))
                st["rC"] += 1 if works[xc] else 0
                st["rD"] += 1 if works[xd] else 0

    p = st["pairs"]
    print()
    print("(valid balanced state, unallocated chore) pairs : %d" % p)
    print("   some minimum bundle is unsubsidised          : %d / %d%s"
          % (st["unsub_min"], p, "   <-- ALWAYS" if st["unsub_min"] == p else ""))
    print("   recipient choice actually matters            : %d" % st["choice_matters"])
    print()
    print("   an EXPLICIT move exists (keep or raise)      : %d / %d%s"
          % (st["explicit"], p, "   <-- ALWAYS" if st["explicit"] == p else ""))
    print("      KEEP  q'_x = q_x  suffices somewhere      : %d" % st["keep"])
    print("      RAISE q'_x = 1    suffices somewhere      : %d" % st["raise"])
    print("      neither, needs a different price vector   : %d" % st["no_explicit"])
    print()
    print("   rule C (unsubsidised, then fewest clashes)   : %d / %d%s"
          % (st["rC"], p, "   <-- ALWAYS" if st["rC"] == p else ""))
    print("   rule D (fewest clashes, then unsubsidised)   : %d / %d%s"
          % (st["rD"], p, "   <-- ALWAYS" if st["rD"] == p else ""))
    if hard:
        print()
        print("PAIRS WHERE THE RECIPIENT CHOICE MATTERS:")
        for w in hard:
            print("   bundles=%s g=%d L=%s q=%s" % (w[0], w[1], w[2], w[3]))
            print("      d=%s works=%s (keep,raise)=%s" % (w[4], w[5], w[6]))


if __name__ == "__main__":
    main()
