"""
Which minimum-size bundle should receive the chore?

(BAL-STEP) says SOME minimum-size bundle works. Section 32 shows not every one
does -- EVERY-MIN already fails at n=3, m=4 -- so a proof needs a rule for
choosing the recipient. This script hunts for one that is both correct and
local enough to prove.

The theory says where to look. Reading the subsidy as a price on the bundle,
insert g into B_x and raise the price of x from 0 to 1. Agent i's score for
position x moves by 1 - d_i, where d_i = c_i(g | B_x) in {0,1}; every other
score is untouched. So:

  d_i = 1  ->  the score is unchanged and so is i's demand set;
  d_i = 0  ->  the score rises by one, and if i already demanded x its demand
               set COLLAPSES to {x}.

Two agents collapsing onto x is the only way Hall's condition can break. That
makes one quantity the natural candidate for the rule:

    clash(x) = #{ i : c_i(g | B_x) = 0 and i demands position x }

and the conjecture is that some minimum-size bundle has clash(x) <= 1, and that
choosing such a bundle always works. Four rules are measured against the truth
computed by brute force.
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


def good(vals, bundles, n):
    """Some price vector in {0,1}^n makes the demand graph matchable."""
    for mask in range(1 << n):
        q = [(mask >> j) & 1 for j in range(n)]
        if perfect_matching(demand(vals, bundles, q, n), n):
            return True
    return False


def witness(vals, bundles, n):
    """A price vector and matching certifying goodness, or None."""
    for mask in range(1 << n):
        q = [(mask >> j) & 1 for j in range(n)]
        adj = demand(vals, bundles, q, n)
        if perfect_matching(adj, n):
            return q, adj
    return None


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    m = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    k = int(sys.argv[3]) if len(sys.argv) > 3 else 4000

    pool = enumerate_class(m, {-1, 0})
    rng = random.Random(20260903)
    print("chores class m=%d: %d valuations; sampled tuples: %d (n=%d)"
          % (m, len(pool), k, n))

    st = {"pairs": 0, "everymin": 0, "some_only": 0, "none": 0,
          "clash_exists": 0, "clash_bad": 0,
          "rA": 0, "rB": 0, "rC": 0, "rD": 0}

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
            wit = witness(vals, b, n)
            if wit is None:
                continue
            q, adj = wit
            unalloc = [idx for idx in range(m) if assign[idx] is None]
            lo = min(s)
            L = [i for i in range(n) if s[i] == lo]

            for g in unalloc:
                st["pairs"] += 1
                bit = 1 << g
                works = {}
                for x in L:
                    nb = list(b)
                    nb[x] |= bit
                    works[x] = good(vals, tuple(nb), n)
                if all(works.values()):
                    st["everymin"] += 1
                elif any(works.values()):
                    st["some_only"] += 1
                else:
                    st["none"] += 1

                d = {x: [vals[i][b[x]] - vals[i][b[x] | bit] for i in range(n)]
                     for x in L}
                clash = {x: sum(1 for i in range(n)
                                if d[x][i] == 0 and x in adj[i]) for x in L}

                # is there always a minimum bundle with clash <= 1?
                cand = [x for x in L if clash[x] <= 1]
                if cand:
                    st["clash_exists"] += 1
                    if not any(works[x] for x in cand):
                        st["clash_bad"] += 1

                # rule A: fewest agents for whom the chore is free
                xa = min(L, key=lambda x: sum(1 for t in d[x] if t == 0))
                st["rA"] += 1 if works[xa] else 0
                # rule B: fewest clashes
                xb = min(L, key=lambda x: clash[x])
                st["rB"] += 1 if works[xb] else 0
                # rule C: unsubsidised bundle first, then fewest clashes
                xc = min(L, key=lambda x: (q[x], clash[x]))
                st["rC"] += 1 if works[xc] else 0
                # rule D: fewest clashes, then unsubsidised
                xd = min(L, key=lambda x: (clash[x], q[x]))
                st["rD"] += 1 if works[xd] else 0

    p = st["pairs"]
    print()
    print("(valid balanced state, unallocated chore) pairs : %d" % p)
    print("   every minimum bundle works                   : %d" % st["everymin"])
    print("   only some minimum bundles work               : %d" % st["some_only"])
    print("   NO minimum bundle works (refutes BAL-STEP)   : %d" % st["none"])
    print()
    print("   a minimum bundle with clash <= 1 exists      : %d / %d"
          % (st["clash_exists"], p))
    print("   ... but no such bundle works                 : %d" % st["clash_bad"])
    print()
    for name, key in (("A  fewest free agents", "rA"),
                      ("B  fewest clashes", "rB"),
                      ("C  unsubsidised, then fewest clashes", "rC"),
                      ("D  fewest clashes, then unsubsidised", "rD")):
        print("   rule %-38s succeeds %d / %d%s"
              % (name, st[key], p, "   <-- ALWAYS" if st[key] == p else ""))


if __name__ == "__main__":
    main()
