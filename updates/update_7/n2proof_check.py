"""Machine verification of the n=2 completeness THEOREM and its constructive
walk, before either goes in the report.

THEOREM (n=2 completeness of Target G-bal).  Every 2-agent dichotomous goods
instance admits a cardinality-balanced split with q-spread <= 1.

Proof objects being verified here, per instance:
  (E) existence: some balanced split has a valid (envy-freeable) orientation
      with q-spread <= 1  [the theorem itself];
  (W) the O(m) constructive walk finds one:
      - even m: walk from any split toward its complement by single swaps;
        h = u(A) - u(B), u = v1+v2, changes by <= 4 per swap and flips sign,
        so it must enter the window |h| <= 3, where the split is good;
      - odd m: if h(A) >= 4, the jump B := (M \\ A) u {x} has h(B) <= -1;
        if h(A) <= -2, the same jump has h(B) >= 2; either the jump lands in
        the window [-1, 3] or the swap path A -> B crosses it.
  Both are checked SEMANTICALLY: goodness = actual q-spread <= 1 computed via
  valid orientations, not via the window reasoning being tested.

Run:  python n2proof_check.py
"""
from itertools import combinations, combinations_with_replacement
import random


# ---------------------------------------------------------------- generator
def subsets(m):
    return [frozenset(s) for k in range(m + 1) for s in combinations(range(m), k)]


def gen_functions(m):
    subs = sorted(subsets(m), key=lambda s: (len(s), sorted(s)))
    res, val = [], {}

    def rec(i):
        if i == len(subs):
            res.append(dict(val)); return
        S = subs[i]
        if len(S) == 0:
            val[S] = 0; rec(i + 1); del val[S]; return
        lo, hi = 0, 10 ** 9
        for g in S:
            T = S - {g}
            lo = max(lo, val[T]); hi = min(hi, val[T] + 1)
        for x in range(lo, hi + 1):
            val[S] = x; rec(i + 1)
        del val[S]

    rec(0)
    return res


def rand_dicho(m, rng, hi_prob=None):
    subs = sorted(subsets(m), key=lambda s: (len(s), sorted(s)))
    val = {frozenset(): 0}
    for S in subs:
        if not S:
            continue
        lo, hi = 0, 10 ** 9
        for g in S:
            T = S - {g}
            lo = max(lo, val[T]); hi = min(hi, val[T] + 1)
        pr = rng.random() if hi_prob is None else hi_prob
        val[S] = hi if (lo != hi and rng.random() < pr) else lo
    return val


# ------------------------------------------------------------- semantics
def split_spread(v1, v2, A, B):
    """Best q-spread over VALID (envy-freeable) orientations of the split
    (A, B); None if neither orientation is envy-freeable (cannot happen)."""
    best = None
    for (X, Y) in ((A, B), (B, A)):          # agent 1 gets X, agent 2 gets Y
        e1 = v1[Y] - v1[X]                    # envy of agent 1
        e2 = v2[X] - v2[Y]
        if e1 + e2 > 0:                       # positive 2-cycle: not EF-able
            continue
        p1, p2 = max(0, e1), max(0, e2)
        q1, q2 = p1 + len(X), p2 + len(Y)
        sp = abs(q1 - q2)
        if best is None or sp < best:
            best = sp
    return best


def is_good(v1, v2, A, B):
    sp = split_spread(v1, v2, A, B)
    return sp is not None and sp <= 1


# ------------------------------------------------------------- the walk
def h_of(u, A, B):
    return u[A] - u[B]


def swap_path(A, B, M):
    """Yield the splits along the standard swap path from A to B (both the
    same size), exchanging one element of A\\B for one of B\\A at a time."""
    A = set(A)
    Bset = set(B)
    while A != Bset:
        a = next(iter(A - Bset))
        b = next(iter(Bset - A))
        A.remove(a); A.add(b)
        yield frozenset(A), frozenset(M - A)


def constructive_walk(v1, v2, m):
    """Return (good split found, number of splits evaluated)."""
    M = frozenset(range(m))
    u = {S: v1[S] + v2[S] for S in v1}
    k_big = -(-m // 2)
    A = frozenset(range(k_big))
    B = M - A
    evals = 1
    if is_good(v1, v2, A, B):
        return (A, B), evals

    if m % 2 == 0:
        # walk toward the complement
        for (A2, B2) in swap_path(A, B, M):
            evals += 1
            if is_good(v1, v2, A2, B2):
                return (A2, B2), evals
        return None, evals
    else:
        # the jump: B2 = (M \ A) + one element of A, another (k+1)-set
        x = next(iter(A))
        A2 = (M - A) | {x}
        B2 = M - A2
        evals += 1
        if is_good(v1, v2, A2, B2):
            return (A2, B2), evals
        # walk between the two (k+1)-sets, crossing the window
        for (A3, B3) in swap_path(A, A2, M):
            evals += 1
            if is_good(v1, v2, A3, B3):
                return (A3, B3), evals
        return None, evals


# ------------------------------------------------------------- existence
def existence(v1, v2, m):
    M = frozenset(range(m))
    k_big = -(-m // 2)
    for combo in combinations(range(m), k_big):
        A = frozenset(combo)
        if is_good(v1, v2, A, M - A):
            return True
    return False


# ------------------------------------------------------------------ main
def run_family(name, pairs, m):
    ex_fail = walk_fail = 0
    max_evals = 0
    total = 0
    for v1, v2 in pairs:
        total += 1
        if not existence(v1, v2, m):
            ex_fail += 1
            continue
        found, evals = constructive_walk(v1, v2, m)
        max_evals = max(max_evals, evals)
        if found is None:
            walk_fail += 1
    print("  %-28s: %7d instances | existence failures: %d | walk failures: %d"
          " | max splits evaluated by walk: %d (bound m+2 = %d)"
          % (name, total, ex_fail, walk_fail, max_evals, m + 2))
    return ex_fail + walk_fail


def main():
    bad = 0
    for m in (1, 2, 3, 4):
        F = gen_functions(m)
        pairs = combinations_with_replacement(F, 2)
        bad += run_family("exhaustive m=%d (%d fns)" % (m, len(F)), pairs, m)

    rng = random.Random(7)
    for m, T in ((5, 20000), (6, 8000), (7, 2000)):
        pairs = ((rand_dicho(m, rng, rng.choice([0.0, 0.1, 0.5, 0.9, 1.0])),
                  rand_dicho(m, rng, rng.choice([0.0, 0.1, 0.5, 0.9, 1.0])))
                 for _ in range(T))
        bad += run_family("random m=%d" % m, pairs, m)

    print("\nTOTAL failures (existence or walk): %d" % bad)
    if bad == 0:
        print("=> the n=2 theorem and its constructive O(m) walk verify cleanly.")


if __name__ == "__main__":
    main()
