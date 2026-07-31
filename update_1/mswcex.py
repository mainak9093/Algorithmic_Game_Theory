"""Isolate and check the instance found by `msw.py 4 3 3000 11` (trial 2460),
on which NO utilitarian-welfare-optimal allocation admits a subsidy of <= 1.

Question: does this refute Conjecture 1 (no allocation at all works) or only
Conjecture 2 (some allocation works, but none of the MSW-optimal ones)?

Run:  python mswcex.py
"""
from itertools import combinations, product

M = 4
N = 3

# Transcribed from the msw.py stdout for trial 2460.
RAW = [
    {(): 0, (0,): 1, (1,): 1, (2,): 1, (3,): 1,
     (0, 1): 2, (0, 2): 1, (0, 3): 2, (1, 2): 1, (1, 3): 2, (2, 3): 2,
     (0, 1, 2): 2, (0, 1, 3): 3, (0, 2, 3): 2, (1, 2, 3): 2, (0, 1, 2, 3): 3},
    {(): 0, (0,): 1, (1,): 1, (2,): 1, (3,): 1,
     (0, 1): 2, (0, 2): 2, (0, 3): 2, (1, 2): 2, (1, 3): 2, (2, 3): 1,
     (0, 1, 2): 3, (0, 1, 3): 2, (0, 2, 3): 2, (1, 2, 3): 2, (0, 1, 2, 3): 3},
    {(): 0, (0,): 1, (1,): 1, (2,): 0, (3,): 1,
     (0, 1): 2, (0, 2): 1, (0, 3): 2, (1, 2): 1, (1, 3): 2, (2, 3): 1,
     (0, 1, 2): 2, (0, 1, 3): 2, (0, 2, 3): 2, (1, 2, 3): 2, (0, 1, 2, 3): 3},
]
CS = [{frozenset(k): v for k, v in d.items()} for d in RAW]

SUBSETS = [frozenset(s) for k in range(M + 1) for s in combinations(range(M), k)]


def is_dichotomous(c):
    """c(empty)=0, monotone, every marginal in {0,1}."""
    if c[frozenset()] != 0:
        return False, "c(empty) != 0"
    for S in SUBSETS:
        for g in range(M):
            if g in S:
                continue
            d = c[S | {g}] - c[S]
            if d not in (0, 1):
                return False, "marginal %d at S=%s g=%d" % (d, sorted(S), g)
    return True, "ok"


def ellvec(cs, bd, n):
    """Longest-path subsidies; None iff a positive-weight cycle exists."""
    W = [[cs[i][bd[i]] - cs[i][bd[j]] for j in range(n)] for i in range(n)]
    e = [0] * n
    for _ in range(n + 1):
        ch = False
        new = list(e)
        for i in range(n):
            for j in range(n):
                if i != j and W[i][j] + e[j] > new[i]:
                    new[i] = W[i][j] + e[j]
                    ch = True
        e = new
        if not ch:
            return e
    return None


def main():
    for i, c in enumerate(CS):
        good, why = is_dichotomous(c)
        print("agent %d: negative dichotomous? %s (%s)" % (i, good, why))
    print()

    rows = []
    for assign in product(range(N), repeat=M):
        bd = [frozenset(g for g in range(M) if assign[g] == i) for i in range(N)]
        welfare = sum(CS[i][bd[i]] for i in range(N))
        e = ellvec(CS, bd, N)
        rows.append((bd, welfare, e))

    msw = min(w for _, w, _ in rows)
    print("minimum total cost (utilitarian optimum) = %d" % msw)

    def summarise(sel, label):
        feasible = [(bd, w, e) for bd, w, e in sel if e is not None]
        if not feasible:
            print("%s: no envy-freeable allocation at all" % label)
            return None
        best = min(max(e) for _, _, e in feasible)
        wit = [(bd, w, e) for bd, w, e in feasible if max(e) == best]
        print("%s: %d allocations, %d envy-freeable, min over them of "
              "max-subsidy = %d" % (label, len(sel), len(feasible), best))
        for bd, w, e in wit[:3]:
            print("    witness %s  cost=%d  p=%s"
                  % ([sorted(b) for b in bd], w, e))
        return best

    opt = [r for r in rows if r[1] == msw]
    b_opt = summarise(opt, "MSW-optimal allocations")
    b_all = summarise(rows, "ALL allocations")

    print()
    if b_all is not None and b_all <= 1 and b_opt is not None and b_opt >= 2:
        print("VERDICT: Conjecture 2 is FALSE -- a subsidy of <= 1 is achievable,")
        print("         but every utilitarian-optimal allocation needs >= 2.")
        print("         Conjecture 1 survives on this instance.")
    elif b_all is not None and b_all >= 2:
        print("VERDICT: Conjecture 1 is FALSE on this instance.")
    else:
        print("VERDICT: no separation here.")


if __name__ == "__main__":
    main()
