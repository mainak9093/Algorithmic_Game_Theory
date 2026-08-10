"""Anchors for the CRI machinery, run through the REAL functions of cri_sweep.py.

Nothing here is a hand-written re-derivation: every quantity is produced by the
same `profile`, `cr_legal` and `analyse` that the sweep calls, so a divergence
between anchor and sweep is impossible.

Checked:

  (A1) The witness of thm:obstruction -- M = {a1,a2,g},
       c_1(S) = max(0,|S|-1), c_2 = c_3 = |S| -- is CRI-schedulable along
       a1->1, a2->2, g->3, with ell = (0,0,0), (1,0,0), (1,1,0), (0,0,0).
       This instance is exactly the one on which item-by-item insertion fails
       (thm:obstruction) and on which the peel frame has its 9 dead ends
       (prop:deadends).

  (A2) The two known peel dead ends are NOT CR states.  A profile W is a CR
       state iff the sets W_i minus the common intersection are pairwise
       disjoint and cover the rest; both witnesses repeat an item.

  (A3) Lemma 2 numerically: the envy graph of the profile W_i = A_i u R equals
       the envy graph of the allocation A under the contracted costs
       c^R_i(T) = c_i(T u R) - c_i(R).

  (A4) Lemma 3, the CR arc-update formula
           w'(i,k) - w(i,k) = beta_i(A_k)[k != x] - beta_i(A_i)[i != x],
       checked exhaustively against directly recomputed arcs.

Run:  python cri_anchor.py
"""
from itertools import product, combinations
import random
import sys

sys.path.insert(0, "../update_6")
sys.path.insert(0, "../update_32")
sys.path.insert(0, "../update_44")
sys.path.insert(0, "../update_17")
from peel_general import ell                                    # noqa: E402
from minimum_subsidy import subsets                             # noqa: E402
from counterexample_hunt import FAMILIES                        # noqa: E402
from cri_sweep import profile, cr_legal, analyse                # noqa: E402


def witness():
    """thm:obstruction: M = {a1,a2,g} = {0,1,2}."""
    c1 = {S: max(0, len(S) - 1) for S in subsets(3)}
    c2 = {S: len(S) for S in subsets(3)}
    return [c1, c2, dict(c2)]


def arcs(cs, W, n):
    return [[cs[i][W[i]] - cs[i][W[k]] for k in range(n)] for i in range(n)]


def contracted(c, R, m):
    """c^R(T) = c(T u R) - c(R) for T inside M \\ R."""
    return {T: c[frozenset(T | R)] - c[R]
            for T in subsets(m) if not (T & R)}


def a1_schedule():
    cs = witness()
    n, m = 3, 3
    print("(A1) thm:obstruction witness, schedule a1->1, a2->2, g->3")
    sched = [(3, 3, 3), (0, 3, 3), (0, 1, 3), (0, 1, 2)]
    okall = True
    for own in sched:
        W = profile(own, n, m)
        e = ell(cs, W, n)
        ok = cr_legal(cs, own, n, m)
        okall &= ok
        print("     own=%-12s W=%-34s ell=%-10s legal=%s"
              % (str(own), str([sorted(x) for x in W]), str(e), ok))
    print("     -> every state legal: %s" % okall)
    return okall


def a2_deadends():
    print("(A2) the peel dead ends are not CR states")
    cases = [("({a1,a2},{g},{g})", [{0, 1}, {2}, {2}]),
             ("({g2},{g2},{g1,g3,g4})", [{1}, {1}, {0, 2, 3}])]
    allgood = True
    for name, W in cases:
        inter = set.intersection(*[set(x) for x in W])
        rest = [set(x) - inter for x in W]
        disjoint = all(not (rest[i] & rest[k])
                       for i in range(len(W)) for k in range(i + 1, len(W)))
        print("     %-24s common=%s  residues=%s  pairwise disjoint=%s"
              % (name, sorted(inter), [sorted(r) for r in rest], disjoint))
        allgood &= not disjoint
    print("     -> neither is a CR state: %s" % allgood)
    return allgood


def a3_lemma2(trials=400):
    """envy graph of W_i = A_i u R  ==  envy graph of A under c^R."""
    rng = random.Random(4711)
    bad = 0
    tot = 0
    for _ in range(trials):
        n = rng.choice([3, 4])
        m = rng.choice([3, 4])
        name, gen = FAMILIES[rng.randrange(len(FAMILIES))]
        cs = gen(m, n, rng)
        own = tuple(rng.randrange(n + 1) for _ in range(m))
        R = frozenset(j for j in range(m) if own[j] == n)
        A = [frozenset(j for j in range(m) if own[j] == i) for i in range(n)]
        W = profile(own, n, m)
        direct = arcs(cs, W, n)
        cR = [contracted(c, R, m) for c in cs]
        viaC = [[cR[i][A[i]] - cR[i][A[k]] for k in range(n)] for i in range(n)]
        tot += 1
        if direct != viaC:
            bad += 1
    print("(A3) Lemma 2 (CR state == witness on the contracted instance)")
    print("     random states checked: %d   mismatches: %d" % (tot, bad))
    return bad == 0


def a4_lemma3(trials=400):
    """w'(i,k) - w(i,k) = beta_i(A_k)[k!=x] - beta_i(A_i)[i!=x]."""
    rng = random.Random(881)
    bad = 0
    tot = 0
    for _ in range(trials):
        n = rng.choice([3, 4])
        m = rng.choice([3, 4, 5])
        name, gen = FAMILIES[rng.randrange(len(FAMILIES))]
        cs = gen(m, n, rng)
        own = tuple(rng.randrange(n + 1) for _ in range(m))
        und = [j for j in range(m) if own[j] == n]
        if not und:
            continue
        a = rng.choice(und)
        x = rng.randrange(n)
        nxt = list(own)
        nxt[a] = x
        nxt = tuple(nxt)

        R = frozenset(j for j in range(m) if own[j] == n)
        Rp = R - {a}
        A = [frozenset(j for j in range(m) if own[j] == i) for i in range(n)]
        cRp = [contracted(c, Rp, m) for c in cs]

        def beta(i, T):
            return cRp[i][frozenset(T | {a})] - cRp[i][frozenset(T)]

        w = arcs(cs, profile(own, n, m), n)
        w2 = arcs(cs, profile(nxt, n, m), n)
        tot += 1
        for i in range(n):
            for k in range(n):
                if i == k:
                    continue
                pred = (beta(i, A[k]) if k != x else 0) \
                     - (beta(i, A[i]) if i != x else 0)
                if w2[i][k] - w[i][k] != pred:
                    bad += 1
    print("(A4) Lemma 3 (CR arc update)")
    print("     random assignments checked: %d   arc mismatches: %d"
          % (tot, bad))
    return bad == 0


def a5_additive(trials=300):
    """Additive costs: third-party arcs must not move (the additive collapse)."""
    rng = random.Random(90210)
    bad = 0
    tot = 0
    for _ in range(trials):
        n = rng.choice([3, 4])
        m = rng.choice([3, 4, 5])
        val = [[rng.randrange(2) for _ in range(m)] for _ in range(n)]
        cs = [{S: sum(val[i][g] for g in S) for S in subsets(m)}
              for i in range(n)]
        own = tuple(rng.randrange(n + 1) for _ in range(m))
        und = [j for j in range(m) if own[j] == n]
        if not und:
            continue
        a = rng.choice(und)
        x = rng.randrange(n)
        nxt = list(own)
        nxt[a] = x
        nxt = tuple(nxt)
        w = arcs(cs, profile(own, n, m), n)
        w2 = arcs(cs, profile(nxt, n, m), n)
        tot += 1
        for i in range(n):
            for k in range(n):
                if i == k or i == x or k == x:
                    continue
                if w[i][k] != w2[i][k]:
                    bad += 1
    print("(A5) the additive collapse: only arcs at x move")
    print("     additive instances checked: %d   third-party arc moves: %d"
          % (tot, bad))
    return bad == 0


def a6_first_chore(trials=400):
    """From the root, assign a to x is legal iff beta_x(empty) <= beta_k(empty)."""
    rng = random.Random(1357)
    bad = 0
    tot = 0
    for _ in range(trials):
        n = rng.choice([3, 4, 5])
        m = rng.choice([3, 4, 5])
        name, gen = FAMILIES[rng.randrange(len(FAMILIES))]
        cs = gen(m, n, rng)
        root = tuple([n] * m)
        for a in range(m):
            full = frozenset(range(m))
            b = [cs[i][full] - cs[i][full - {a}] for i in range(n)]
            for x in range(n):
                s = list(root)
                s[a] = x
                tot += 1
                pred = (b[x] <= min(b))
                if cr_legal(cs, tuple(s), n, m) != pred:
                    bad += 1
    print("(A6) the first chore: legal iff the owner has MINIMAL marginal")
    print("     root assignments checked: %d   mismatches: %d" % (tot, bad))
    return bad == 0


def main():
    print("=== CRI anchors ===")
    print()
    res = [a1_schedule(), a2_deadends(), a3_lemma2(), a4_lemma3(),
           a5_additive(), a6_first_chore()]
    print()
    print("  all anchors pass: %s" % all(res))


if __name__ == "__main__":
    main()
