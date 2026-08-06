"""Track 1, work item 2: does an explicit rule solve the n = 3 residual?

obs:n3-residual leaves a well-posed target: prove Conjecture 2 at n = 3, knowing
that at a minimal witness the paid agent attains max_i c_i(A_i) when |S| = 1 and
the unpaid one attains min_i c_i(A_i) when |S| = 2.

Approach 8 tested global objectives at general n and found none whose optima are
ALL good.  But it never tested them on the n = 3 RESIDUAL -- the 6.2% of instances
with no exactly envy-free allocation, which is the only place the question has
content, and where the paid agent is now pinned.  A rule that is good on every
residual instance at n = 3 is a proof target; one that is not saves the effort.

Rules, each a lexicographic minimisation over ALL allocations:
    E     (max own cost)
    ET    (max own cost, total cost)
    EN    (max own cost, #agents at that max)
    ENT   (max own cost, #at max, total cost)
    LEX   (own-cost vector sorted descending)
    LEXB  (own-cost vector sorted descending, then sum |A_i|^2)
    EB    (max own cost, then sum |A_i|^2)

For each rule and each residual instance: is EVERY optimum good, is SOME optimum
good, or is none?  "Every" is what a proof can use, since then the rule may return
any optimum.

Run:  python n3_rules.py
"""
from itertools import product
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_17")
sys.path.insert(0, "../update_44")
from minimum_subsidy import total_subsidy                       # noqa: E402
from counterexample_hunt import (f_nested, f_mixed, f_capped,   # noqa: E402
                                 f_threshold, f_disjoint, f_uniform)

N = 3
RULES = ["E", "ET", "EN", "ENT", "LEX", "LEXB", "EB"]


def key(rule, own, tot, sizes):
    srt = tuple(sorted(own, reverse=True))
    mx = max(own)
    nm = sum(1 for o in own if o == mx)
    sq = sum(s * s for s in sizes)
    return {"E": (mx,), "ET": (mx, tot), "EN": (mx, nm), "ENT": (mx, nm, tot),
            "LEX": srt, "LEXB": srt + (sq,), "EB": (mx, sq)}[rule]


def scan(cs, m):
    """Return (has_ef, per-rule (all_good, some_good))."""
    recs = []
    has_ef = False
    for assign in product(range(N), repeat=m):
        bd = [frozenset(g for g in range(m) if assign[g] == i) for i in range(N)]
        a = [[cs[i][bd[j]] for j in range(N)] for i in range(N)]
        own = [a[i][i] for i in range(N)]
        if all(a[i][i] <= a[i][j] for i in range(N) for j in range(N)):
            has_ef = True
        t, e = total_subsidy(a, N)
        good = (t is not None and max(e) <= 1)
        recs.append((own, sum(own), [len(b) for b in bd], good))
    out = {}
    for r in RULES:
        best = min(key(r, o, t, s) for o, t, s, _ in recs)
        opt = [g for o, t, s, g in recs if key(r, o, t, s) == best]
        out[r] = (all(opt), any(opt))
    return has_ef, out


def main():
    rng = random.Random(45454545)
    gens = [f_uniform, f_nested, f_mixed, f_capped, f_threshold, f_disjoint]
    allbad = Counter()
    somebad = Counter()
    resid = 0
    tot = 0
    print("=== explicit rules on the n = 3 residual (EF-free instances only) ===")
    for (m, T) in [(4, 1500), (5, 900), (6, 400), (7, 150), (8, 60)]:
        for _ in range(T):
            cs = gens[rng.randrange(len(gens))](m, N, rng)
            if max(max(c.values()) for c in cs) < 1:
                continue
            tot += 1
            has_ef, res = scan(cs, m)
            if has_ef:
                continue
            resid += 1
            for r in RULES:
                a, s = res[r]
                if not a:
                    allbad[r] += 1
                if not s:
                    somebad[r] += 1
    print("  instances scanned : %d" % tot)
    print("  EF-free residual  : %d" % resid)
    print()
    print("  rule    every optimum good      some optimum good")
    for r in RULES:
        print("  %-6s  %5d fail of %-5d    %5d fail of %d"
              % (r, allbad[r], resid, somebad[r], resid))
    print()
    win = [r for r in RULES if allbad[r] == 0]
    if win:
        for r in win:
            print("  *** %s : EVERY optimum is good on the whole residual --"
                  " a proof target ***" % r)
    else:
        w2 = [r for r in RULES if somebad[r] == 0]
        if w2:
            print("  no rule has all optima good; these have SOME good optimum"
                  " throughout: %s" % ", ".join(w2))
            print("  (a tie-break would be needed, and Approach 8 found none)")
        else:
            print("  every rule fails outright on the residual")


if __name__ == "__main__":
    main()
