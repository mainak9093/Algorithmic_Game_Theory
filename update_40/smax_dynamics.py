"""Dynamics of S_max, and the canonical-support conjecture.

Two questions, both suggested by thm:paidsets-lattice giving a canonical element.

(A) HOW DOES S_max EVOLVE?  Put F(W) := S_max(W), the unique maximum admissible
    paid set.  A peel raises the in-arcs at x and lowers the out-arcs, so there is
    no a-priori reason for F to move in either direction.  Tested:
        F(W') subset F(W)?          F(W) subset F(W')?
        F(W') subset F(W) u {x}?    |F(W) symmetric-difference F(W')| distribution
    A containment or a bounded jump would make F a usable monovariant; a one-step
    flip would make peels moves in the lattice.

(B) CANONICAL-SUPPORT CONJECTURE.  Every reachable legal balance-admitting state
    admits a balanced terminal f with

        f(j) in S_max   whenever   S_j n S_max is non-empty.

    If true, every chore whose candidate set meets S_max can be given to a PAID
    owner, so paid-agent peels (which by cor:smax-canonical need exactly
    x in S_max) are always schedulable -- and it is the first statement linking
    the transportation side to the potential side.  Also recorded: the
    distribution of |S_j n S_max| over chores, since the mixed case is where the
    conjecture has content.

Run:  python smax_dynamics.py
"""
from itertools import permutations, product
from collections import Counter, deque
import random
import sys

sys.path.insert(0, "../update_6")
sys.path.insert(0, "../update_32")
sys.path.insert(0, "../update_34")
sys.path.insert(0, "../update_36")
from targetGbal import rand_dicho                             # noqa: E402
from peel_general import legal, cand, terminal, peels, make   # noqa: E402
from reachable_stuck import ok                                # noqa: E402
from potential_set import admissible                          # noqa: E402


def smax(cs, W, n):
    P = admissible(cs, W, n)
    return frozenset.union(*P) if P else None


def canonical_support(W, n, m, Smax):
    """Is there a balanced terminal f with f(j) in Smax whenever S_j meets Smax?"""
    S = cand(W, n, m)
    choices = []
    for j in range(m):
        inter = S[j] & Smax
        choices.append(sorted(inter) if inter else sorted(S[j]))
    for f in product(*choices):
        sz = [0] * n
        for o in f:
            sz[o] += 1
        if max(sz) - min(sz) <= 1:
            return True
    return False


def any_balanced(W, n, m):
    S = cand(W, n, m)
    for f in product(*[sorted(s) for s in S]):
        sz = [0] * n
        for o in f:
            sz[o] += 1
        if max(sz) - min(sz) <= 1:
            return True
    return False


def main():
    rng = random.Random(40404040)
    rel = Counter(); sym = Counter(); plusx = 0; npeel = 0
    cs_ok = cs_bad = 0
    inter_hist = Counter()
    print("=== (A) dynamics of S_max, (B) canonical-support conjecture ===")
    for (n, m, T) in [(3, 4, 40), (3, 5, 18), (3, 6, 6),
                      (4, 3, 30), (4, 4, 12), (5, 3, 12)]:
        perms = list(permutations(range(n)))
        for _ in range(T):
            cs = [rand_dicho(m, rng) for _ in range(n)]
            if max(max(c.values()) for c in cs) < 1:
                continue
            root = tuple([make(m)] * n)
            seen = {root}; q = deque([root])
            while q and len(seen) < 2500:
                W = q.popleft()
                A = smax(cs, W, n)
                if A is not None and not terminal(W, n, m):
                    # (A)
                    for mv, s in peels(W, n, m):
                        x, _ = mv
                        B = smax(cs, s, n)
                        if B is None:
                            continue
                        npeel += 1
                        if B <= A and A <= B:
                            rel["equal"] += 1
                        elif B <= A:
                            rel["shrinks"] += 1
                        elif A <= B:
                            rel["grows"] += 1
                        else:
                            rel["incomparable"] += 1
                        sym[len(A ^ B)] += 1
                        if B <= (A | {x}):
                            plusx += 1
                    # (B)
                    if any_balanced(W, n, m):
                        for j in range(m):
                            inter_hist[len(cand(W, n, m)[j] & A)] += 1
                        if canonical_support(W, n, m, A):
                            cs_ok += 1
                        else:
                            cs_bad += 1
                for s in ([s for _, s in peels(W, n, m)]
                          + [tuple(W[p[i]] for i in range(n)) for p in perms]):
                    if s not in seen and ok(cs, s, n, m):
                        seen.add(s); q.append(s)
    print("  peels examined                     : %d" % npeel)
    print("  S_max(W') vs S_max(W)              : %s" % dict(rel))
    print("  |symmetric difference| distribution: %s" % dict(sorted(sym.items())))
    print("  S_max(W') subset S_max(W) u {x}    : %d / %d  (%.1f%%)"
          % (plusx, npeel, 100.0 * plusx / max(npeel, 1)))
    print()
    print("  (B) balance-admitting states tested: %d" % (cs_ok + cs_bad))
    print("      canonical support HOLDS        : %d" % cs_ok)
    print("      canonical support FAILS        : %d" % cs_bad)
    print("      |S_j n S_max| distribution     : %s" % dict(sorted(inter_hist.items())))
    print()
    if cs_bad == 0:
        print("  *** CANONICAL-SUPPORT CONJECTURE survives.  Every chore whose")
        print("      candidate set meets S_max can be given to a PAID owner in")
        print("      some balanced terminal -- the first bridge between the")
        print("      transportation side and the potential side. ***")
    else:
        print("  *** canonical support FAILS on %d states. ***" % cs_bad)


if __name__ == "__main__":
    main()
