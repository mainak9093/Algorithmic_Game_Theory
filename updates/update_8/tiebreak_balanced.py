"""Does a deterministic tie-break inside the cost-minimising BALANCED set always
select a good allocation?

balanced_msw.py showed: some cost-min balanced allocation is always good, but
not every one.  If a simple tie-break always picks a good one, the rule becomes
a single deterministic optimisation and the proof obligation becomes an exchange
argument.  If every natural tie-break fails, that is itself informative -- it is
the Route D failure mode reappearing inside the balanced set.

Tie-breaks tested, applied only among cost-minimising balanced allocations:
  (a) leximin on the descending-sorted own-cost vector (c_i(A_i))
  (b) minimise Psi = sum_i sum_j c_j(A_i)          (total perceived load)
  (c) leximin on the descending-sorted perceived-load vector (max_j c_j(A_i))
  (d) minimise the number of (i,j) pairs with c_i(A_i) > c_i(A_j)  (envy count)

Run:  python tiebreak_balanced.py
"""
from itertools import combinations, combinations_with_replacement, product
import random

from balanced_msw import (subsets, gen_functions, rand_dicho, ellvec, balanced,
                          as_dict)


def winners(cs, m, n):
    best = None
    wins = []
    for assign in product(range(n), repeat=m):
        bd = [frozenset(g for g in range(m) if assign[g] == i) for i in range(n)]
        if not balanced(bd, m, n):
            continue
        tot = sum(cs[i][bd[i]] for i in range(n))
        if best is None or tot < best:
            best = tot; wins = [bd]
        elif tot == best:
            wins.append(bd)
    return wins


def good(cs, bd, n):
    e = ellvec(cs, bd, n)
    return e is not None and max(e) <= 1


def keys(cs, bd, n):
    own = tuple(sorted((cs[i][bd[i]] for i in range(n)), reverse=True))
    psi = sum(cs[j][bd[i]] for i in range(n) for j in range(n))
    perc = tuple(sorted((max(cs[j][bd[i]] for j in range(n)) for i in range(n)),
                        reverse=True))
    envy = sum(1 for i in range(n) for j in range(n)
               if i != j and cs[i][bd[i]] > cs[i][bd[j]])
    return {"a_leximin_own": own, "b_min_psi": psi,
            "c_leximin_perceived": perc, "d_min_envy_count": envy}


NAMES = ["a_leximin_own", "b_min_psi", "c_leximin_perceived", "d_min_envy_count"]


def test(cs, m, n):
    """Returns dict name -> True if EVERY allocation selected by that tie-break
    is good (i.e. the deterministic rule is safe on this instance)."""
    ws = winners(cs, m, n)
    if not ws:
        return None
    ks = [keys(cs, bd, n) for bd in ws]
    out = {}
    for nm in NAMES:
        best = min(k[nm] for k in ks)
        sel = [bd for bd, k in zip(ws, ks) if k[nm] == best]
        out[nm] = all(good(cs, bd, n) for bd in sel)
    return out


def main():
    print("=== EXHAUSTIVE n=3, m=3 ===")
    F = gen_functions(3)
    fail = {nm: 0 for nm in NAMES}
    tot = 0
    for cs in combinations_with_replacement(F, 3):
        r = test(list(cs), 3, 3)
        tot += 1
        for nm in NAMES:
            if not r[nm]:
                fail[nm] += 1
    for nm in NAMES:
        print("  %-22s: %d failures / %d" % (nm, fail[nm], tot))

    print("\n=== adversarial / randomised ===")
    rng = random.Random(31415)
    for (n, m, T) in [(3, 4, 2500), (3, 5, 900), (3, 6, 300), (4, 4, 700)]:
        fail = {nm: 0 for nm in NAMES}
        for _ in range(T):
            cs = [rand_dicho(m, rng, rng.choice([0.0, 0.1, 0.5, 0.9, 1.0]))
                  for _ in range(n)]
            r = test(cs, m, n)
            if r is None:
                continue
            for nm in NAMES:
                if not r[nm]:
                    fail[nm] += 1
        print("  n=%d m=%d T=%4d : %s" % (n, m, T,
              "  ".join("%s=%d" % (nm.split('_')[0], fail[nm]) for nm in NAMES)))

    print("\n=== named hard instances ===")
    D = [frozenset({0, 1}), frozenset({0, 2, 3}), frozenset({1, 2, 3})]
    disc = [as_dict(4, lambda S, Ds=Ds: len(S & Ds)) for Ds in D]
    wit = [as_dict(3, lambda S: max(0, len(S) - 1)),
           as_dict(3, lambda S: len(S)), as_dict(3, lambda S: len(S))]
    for tag, cs, m in (("discrepancy cex", disc, 4), ("insertion witness", wit, 3)):
        r = test(cs, m, 3)
        print("  %-20s %s" % (tag, {nm.split('_')[0]: r[nm] for nm in NAMES}))


if __name__ == "__main__":
    main()
