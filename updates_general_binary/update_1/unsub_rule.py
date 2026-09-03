"""
The candidate theorem: grow an UNSUBSIDISED minimum-size bundle.

Every pair in explicit_step.py where the choice of recipient mattered had the
same shape -- the minimum-size bundles that FAILED were the subsidised ones,
and the unsubsidised ones all worked. That suggests (BAL-STEP) holds in a form
with no search and no tie-breaking in it at all:

    (U1)  some minimum-size position is unsubsidised;
    (U2)  growing ANY unsubsidised minimum-size position by g keeps the
          multiset good.

(U2) is the order-free strength: the algorithm may take the chores in any
order and grow any unsubsidised smallest bundle. The price reading says why it
should be true -- an unsubsidised position has one unit of headroom, so the
damage done by the new chore can always be paid for by raising its price to 1,
whereas a position already at price 1 has nothing left to give.

Both halves are checked here against goodness computed by brute force, at
several sizes, with the goods class run as a control (by the duality of
section 23 the two should behave identically).
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


MASKS = {}
def masks(n):
    if n not in MASKS:
        MASKS[n] = sorted(range(1 << n), key=lambda t: (bin(t).count("1"), t))
    return MASKS[n]


def good(vals, bundles, n):
    for mask in masks(n):
        if matchable(vals, bundles, [(mask >> j) & 1 for j in range(n)], n):
            return True
    return False


def witness(vals, bundles, n):
    for mask in masks(n):
        q = [(mask >> j) & 1 for j in range(n)]
        if matchable(vals, bundles, q, n):
            return q
    return None


def run(n, m, k, allowed, label):
    pool = enumerate_class(m, allowed)
    rng = random.Random(20260903)
    st = {"pairs": 0, "u1_fail": 0, "u2_fail": 0, "sub_fail": 0,
          "unsub_tested": 0, "sub_tested": 0, "balstep_fail": 0}
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
            lo = min(s)
            L = [i for i in range(n) if s[i] == lo]
            for g in [idx for idx in range(m) if assign[idx] is None]:
                st["pairs"] += 1
                bit = 1 << g
                if not any(q[x] == 0 for x in L):
                    st["u1_fail"] += 1
                any_ok = False
                for x in L:
                    nb = list(b)
                    nb[x] |= bit
                    ok = good(vals, tuple(nb), n)
                    any_ok = any_ok or ok
                    if q[x] == 0:
                        st["unsub_tested"] += 1
                        if not ok:
                            st["u2_fail"] += 1
                    else:
                        st["sub_tested"] += 1
                        if not ok:
                            st["sub_fail"] += 1
                if not any_ok:
                    st["balstep_fail"] += 1
    print("   %-26s pairs %-8d U1 fail %-4d U2 fail %-4d "
          "| subsidised tested %-7d of which fail %-5d | BAL-STEP fail %d"
          % (label, st["pairs"], st["u1_fail"], st["u2_fail"],
             st["sub_tested"], st["sub_fail"], st["balstep_fail"]))
    return st


def main():
    print("U1: some minimum-size position is unsubsidised")
    print("U2: growing ANY unsubsidised minimum-size position keeps goodness")
    print()
    jobs = [(3, 3, 400), (3, 4, 400), (4, 4, 200), (3, 5, 60), (4, 5, 40),
            (5, 5, 25)]
    if len(sys.argv) > 1:
        jobs = [(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))]
    for (n, m, k) in jobs:
        for allowed, name in (({-1, 0}, "chores"), ({0, 1}, "goods")):
            run(n, m, k, allowed, "n=%d m=%d %s" % (n, m, name))


if __name__ == "__main__":
    main()
