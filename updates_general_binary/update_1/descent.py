"""
Two things: why every profile-based criterion failed, and a descent that works.

PART 1 -- why they all failed. FLAT, LEX, MAXC and SQ all score an allocation
by its COST PROFILE (v_i(A_i))_i, which is the DIAGONAL of the matrix
v_i(A_j). Validity is a statement about the whole matrix: the envy arc
w(i,j) = v_i(A_j) - v_i(A_i) reads off-diagonal entries. So if two allocations
share a cost profile while one is valid and the other is not, NO criterion that
looks only at the profile can separate them, and the entire family of such
criteria is dead at once. Part 1 looks for such a pair.

PART 2 -- the extremal setup that avoids the trap. Instead of scoring
allocations by a proxy, score them by the thing itself:

    PSI(A) = the vector (l_A(i))_i sorted downwards, compared
             lexicographically, and +infinity when A is not envy-freeable

and ask for a DESCENT LEMMA: every allocation of the family with max_i l > 1
admits a single local move -- transfer one item, swap two items, or reassign
the bundles -- that stays in the family and strictly decreases PSI. Since PSI
takes finitely many values and decreases strictly, iterating it must terminate,
and it can only stop at max_i l <= 1. That is a constructive proof of (S2),
and it is not circular: the content is entirely in the local move.
"""
import itertools
import random
import sys

from gb_valuations import (
    masks_by_popcount,
    arc_weights,
    is_envy_freeable,
    longest_paths,
)

N = 3
INF = (99,) * N


def random_gb(m, rng):
    v = [0] * (1 << m)
    for S in masks_by_popcount(m):
        if S == 0:
            continue
        bits = [1 << b for b in range(m) if S & (1 << b)]
        lo = max(v[S ^ b] for b in bits) - 1
        hi = min(v[S ^ b] for b in bits) + 1
        v[S] = rng.randint(lo, hi)
    return tuple(v)


def sizes(b):
    return [bin(x).count("1") for x in b]


def in_family(b, K):
    s = sizes(b)
    return max(s) - min(s) <= K


def psi(vals, b):
    if not is_envy_freeable(vals, b):
        return INF
    return tuple(sorted(longest_paths(arc_weights(vals, b)), reverse=True))


def moves(b, m, K):
    """Transfers, swaps and reassignments that stay inside the family."""
    out = []
    for perm in itertools.permutations(range(N)):
        cand = tuple(b[perm[i]] for i in range(N))
        if cand != b:
            out.append(cand)
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            for g in range(m):
                bit = 1 << g
                if not b[i] & bit:
                    continue
                nb = list(b)
                nb[i] &= ~bit
                nb[j] |= bit
                if in_family(tuple(nb), K):
                    out.append(tuple(nb))
                for h in range(m):
                    hb = 1 << h
                    if not b[j] & hb:
                        continue
                    sw = list(b)
                    sw[i] = (sw[i] & ~bit) | hb
                    sw[j] = (sw[j] & ~hb) | bit
                    if in_family(tuple(sw), K):
                        out.append(tuple(sw))
    return out


def family(m, K):
    out = []
    for assign in itertools.product(range(N), repeat=m):
        b = [0] * N
        for k, o in enumerate(assign):
            b[o] |= 1 << k
        if in_family(tuple(b), K):
            out.append(tuple(b))
    return out


def main():
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 1500
    K = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    rng = random.Random(20260903)
    fam = family(m, K)
    print("n=3, m=%d, spread<=%d family: %d allocations, %d instances"
          % (m, K, len(fam), trials))

    prof_pair = None
    st = {"inst": 0, "states": 0, "bad": 0, "stuck": 0, "any": 0}
    stuck_ex = []

    for _ in range(trials):
        vals = [random_gb(m, rng) for _ in range(N)]
        st["inst"] += 1
        by_profile = {}
        anyvalid = False
        for b in fam:
            st["states"] += 1
            p = psi(vals, b)
            costs = tuple(-vals[i][b[i]] for i in range(N))
            ok = p != INF and p[0] <= 1
            anyvalid = anyvalid or ok
            if prof_pair is None:
                if costs in by_profile and by_profile[costs][1] != ok:
                    prof_pair = (vals, by_profile[costs], (b, ok))
                by_profile.setdefault(costs, (b, ok))
            if p == INF or p[0] <= 1:
                continue
            st["bad"] += 1
            if not any(psi(vals, c) < p for c in moves(b, m, K)):
                st["stuck"] += 1
                if len(stuck_ex) < 3:
                    stuck_ex.append((vals, b, p))
        if anyvalid:
            st["any"] += 1

    print()
    print("PART 1 -- can the cost profile decide validity?")
    if prof_pair:
        vals, (b1, ok1), (b2, ok2) = prof_pair
        print("   NO. Two allocations, same cost profile %s, different validity:"
              % (tuple(-vals[i][b1[i]] for i in range(N)),))
        print("      %s valid=%s   vs   %s valid=%s" % (b1, ok1, b2, ok2))
        print("   So every criterion scoring only (v_i(A_i))_i is dead.")
    else:
        print("   no such pair found")

    print()
    print("PART 2 -- the descent lemma")
    print("   instances                                : %d" % st["inst"])
    print("   (S2) holds                               : %d" % st["any"])
    print("   states examined                          : %d" % st["states"])
    print("   states with max l > 1 (or not EF-able)   : %d" % st["bad"])
    print("   ... of those, NO improving move (STUCK)  : %d%s"
          % (st["stuck"], "   <-- DESCENT LEMMA HOLDS" if not st["stuck"] else ""))
    for vals, b, p in stuck_ex:
        print("      stuck: bundles=%s psi=%s" % (b, p))


if __name__ == "__main__":
    main()
