"""Does round dominance accumulate along a path?  Search for a POTENTIAL.

The obstruction to turning obs:arc-one (every arc <= 1) into a path bound is that
k arcs of weight 1 give a path of weight k.  The standard remedy is a potential:
if some phi on agents satisfies

    (P)   w(i,j) <= phi_j - phi_i     for every arc,

then any path from a to b has weight at most phi_b - phi_a <= spread(phi), so
max ell <= spread(phi) and, by lem:q-formula, conj:imwpm-bound follows as soon as
spread(phi) <= 2.

Taking phi = -ell satisfies (P) trivially and is circular.  What is needed is a
phi read off the ALGORITHM's round structure.  Candidates, with
kappa_i := c_i(A_i) (which by the chores telescoping equals the number of rounds
in which agent i's own chore had marginal 1), and delta_i the dummies received:

    phi = -kappa      (P) becomes  c_j(A_j) <= c_i(A_j) for all i,j, i.e.
                      every bundle is cheapest for its own owner
    phi = kappa
    phi = |A_i|       bundle size
    phi = -|A_i|
    phi = |A_i|-kappa free rounds carrying a real chore
    phi = kappa-|A_i|
    phi = -firstpay   first round in which i pays (T+1 if never)
    phi = firstpay
    phi = -lastpay    last round in which i pays (0 if never)

For each: does (P) hold on every arc, and what is spread(phi)?  A phi that
satisfies (P) with spread <= 2 would PROVE conj:imwpm-bound.

Also tested directly, since it is the (P) condition for phi = -kappa and is of
independent interest:

    (OWN)  c_j(A_j) <= c_i(A_j)   for all i, j.

Run:  python potential_search.py
"""
from collections import Counter
import random
import sys

sys.path.insert(0, "../update_6")
sys.path.insert(0, "../update_25")
sys.path.insert(0, "../update_26")
from targetGbal import size_shift, rand_dicho     # noqa: E402
from r11_gap import imwpm_rounds, DUM             # noqa: E402
from q_formula import chores_d                    # noqa: E402

NAMES = ["-kappa", "kappa", "|A|", "-|A|", "|A|-kappa", "kappa-|A|",
         "-firstpay", "firstpay", "-lastpay"]


def phis(cs, A, rounds, n, T):
    kappa = [cs[i][A[i]] for i in range(n)]
    size = [len(A[i]) for i in range(n)]
    first = [T + 1] * n
    last = [0] * n
    for ti, (pre, asg) in enumerate(rounds, start=1):
        for i in range(n):
            base = frozenset(x for x in pre[i] if x < DUM)
            new = frozenset(x for x in (pre[i] | {asg[i]}) if x < DUM)
            if cs[i][new] - cs[i][base] == 1:
                first[i] = min(first[i], ti)
                last[i] = max(last[i], ti)
    return {"-kappa": [-k for k in kappa],
            "kappa": kappa,
            "|A|": size,
            "-|A|": [-s for s in size],
            "|A|-kappa": [size[i] - kappa[i] for i in range(n)],
            "kappa-|A|": [kappa[i] - size[i] for i in range(n)],
            "-firstpay": [-f for f in first],
            "firstpay": first,
            "-lastpay": [-l for l in last]}


def main():
    rng = random.Random(16180339)
    holds = Counter()
    spreadmax = Counter()
    tot = 0
    own_bad = 0
    own_checks = 0
    ellmax = 0
    print("=== searching for a potential phi with w(i,j) <= phi_j - phi_i ===")
    for (n, m, T) in [(3, 5, 200), (3, 7, 150), (3, 9, 60),
                      (4, 6, 130), (4, 8, 60), (5, 7, 50), (5, 9, 25),
                      (6, 9, 20)]:
        for _ in range(T):
            cs = [rand_dicho(m, rng) for _ in range(n)]
            if max(max(c.values()) for c in cs) < 1:
                continue
            v = [size_shift(c, m) for c in cs]
            A, rounds = imwpm_rounds(v, list(range(m)), n)
            A = [frozenset(x for x in b if x < DUM) for b in A]
            d = chores_d(cs, A, n)
            if d is None:
                continue
            tot += 1
            Tr = -(-m // n)
            P = phis(cs, A, rounds, n, Tr)
            W = [[cs[i][A[i]] - cs[i][A[j]] for j in range(n)] for i in range(n)]
            ellmax = max(ellmax, max(max(d[i][j] for j in range(n))
                                     for i in range(n)))
            # (OWN)
            for i in range(n):
                for j in range(n):
                    own_checks += 1
                    if cs[j][A[j]] > cs[i][A[j]]:
                        own_bad += 1
            for name in NAMES:
                p = P[name]
                ok = all(W[i][j] <= p[j] - p[i]
                         for i in range(n) for j in range(n) if i != j)
                if ok:
                    holds[name] += 1
                    sp = max(p) - min(p)
                    spreadmax[name] = max(spreadmax[name], sp)
    print("  instances : %d ;  max ell observed : %d" % (tot, ellmax))
    print()
    print("  (OWN) c_j(A_j) <= c_i(A_j) : %d violations of %d checks"
          % (own_bad, own_checks))
    print()
    print("  potential      holds on all arcs      max spread where it holds")
    for name in NAMES:
        print("  %-11s   %6d / %-6d            %s"
              % (name, holds[name], tot,
                 spreadmax[name] if holds[name] else "-"))
    print()
    winners = [n_ for n_ in NAMES if holds[n_] == tot]
    if winners:
        for w in winners:
            print("  *** %s satisfies (P) on every instance, max spread %d ***"
                  % (w, spreadmax[w]))
            if spreadmax[w] <= 2:
                print("      spread <= 2 throughout: this would PROVE conj:imwpm-bound")
    else:
        print("  no candidate potential satisfies (P) on every instance")


if __name__ == "__main__":
    main()
