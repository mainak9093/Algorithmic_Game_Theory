"""Stress the two claims that would give cor:constant-bound, before proving them.

obs:kappa-parts rests on n <= 6, m <= 9, and its part (i) -- spread(kappa) <= 2 --
was attained on only 3 of 657 instances.  That is thin evidence for a claim about
to absorb a proof attempt.  kappa_i is the number of ROUNDS in which agent i's own
chore had marginal 1, so more rounds is exactly the regime where the spread could
grow; the earlier sweep barely left T = 3.

Stressed here at larger m (hence larger T = ceil(m/n)) and on adversarial shapes:

  (i)   spread(kappa) <= 2,           kappa_i = c_i(A_i)
  (iii) sum_{(i,j) in P} E_ij >= -1 for every simple path P,
        E_ij = c_i(A_j) - c_j(A_j)

Adversarial families included alongside the uniform sampler:
  - disjoint-interest: each agent cares only about its own block of chores, so
    agents disagree maximally about which chores are costly;
  - nested-interest: agent i cares about the first b_i chores, a chain of
    inclusions, which maximises asymmetry between agents' cost functions;
  - one-heavy: a single agent finds everything costly, the rest almost nothing.

Run:  python stress_kappa.py
"""
from collections import Counter
from itertools import permutations
import random
import sys

sys.path.insert(0, "../update_6")
sys.path.insert(0, "../update_25")
sys.path.insert(0, "../update_26")
from targetGbal import subsets, size_shift, rand_dicho   # noqa: E402
from r11_gap import imwpm_rounds, DUM                    # noqa: E402
from q_formula import chores_d                           # noqa: E402


def disjoint_interest(m, n, rng):
    blocks = [[] for _ in range(n)]
    for g in range(m):
        blocks[rng.randrange(n)].append(g)
    return [{S: len(S & frozenset(blocks[i])) for S in subsets(m)}
            for i in range(n)]


def nested_interest(m, n, rng):
    cuts = sorted(rng.randrange(1, m + 1) for _ in range(n))
    return [{S: len(S & frozenset(range(cuts[i]))) for S in subsets(m)}
            for i in range(n)]


def one_heavy(m, n, rng):
    out = [{S: len(S) for S in subsets(m)}]
    for _ in range(n - 1):
        k = rng.randrange(0, 2)
        out.append({S: min(len(S), k) for S in subsets(m)})
    return out


def analyse(cs, m, n):
    v = [size_shift(c, m) for c in cs]
    A, rounds = imwpm_rounds(v, list(range(m)), n)
    A = [frozenset(x for x in b if x < DUM) for b in A]
    d = chores_d(cs, A, n)
    if d is None:
        return None
    kap = [cs[i][A[i]] for i in range(n)]
    E = [[cs[i][A[j]] - cs[j][A[j]] for j in range(n)] for i in range(n)]
    mn = 0
    for k in range(2, n + 1):
        for p in permutations(range(n), k):
            s = sum(E[p[t]][p[t + 1]] for t in range(len(p) - 1))
            if s < mn:
                mn = s
    ell = max(max(d[i][j] for j in range(n)) for i in range(n))
    return max(kap) - min(kap), mn, ell


def main():
    rng = random.Random(9090909)
    ksp = Counter()
    dsp = Counter()
    ellh = Counter()
    worst_k = None
    worst_d = None
    print("=== (i) spread(kappa) and (iii) path defect, larger m ===")
    print("   n   m   T   inst   max spread(kappa)   min path defect   max ell")
    fams = [("uniform", lambda m, n, r: [rand_dicho(m, r) for _ in range(n)]),
            ("disjoint", disjoint_interest),
            ("nested", nested_interest),
            ("one-heavy", one_heavy)]
    for (n, m, T) in [(3, 9, 60), (3, 11, 30), (3, 12, 20),
                      (4, 10, 30), (4, 12, 12), (5, 11, 10), (6, 12, 8)]:
        mk = 0
        md = 0
        me = 0
        cnt = 0
        for _ in range(T):
            name, gen = fams[rng.randrange(len(fams))]
            cs = gen(m, n, rng)
            if max(max(c.values()) for c in cs) < 1:
                continue
            r = analyse(cs, m, n)
            if r is None:
                continue
            k, dd, ell = r
            cnt += 1
            ksp[k] += 1
            dsp[dd] += 1
            ellh[ell] += 1
            mk = max(mk, k)
            md = min(md, dd)
            me = max(me, ell)
            if worst_k is None or k > worst_k[0]:
                worst_k = (k, n, m, name)
            if worst_d is None or dd < worst_d[0]:
                worst_d = (dd, n, m, name)
        print("  %2d  %2d  %2d  %5d   %17d   %15d   %7d"
              % (n, m, -(-m // n), cnt, mk, md, me))
    print()
    print("  spread(kappa) distribution : %s" % dict(sorted(ksp.items())))
    print("  path-defect distribution   : %s" % dict(sorted(dsp.items())))
    print("  max ell distribution       : %s" % dict(sorted(ellh.items())))
    print()
    print("  worst spread(kappa) : %s" % (worst_k,))
    print("  worst path defect   : %s" % (worst_d,))
    print()
    if max(ksp) <= 2 and min(dsp) >= -1:
        print("  *** (i) and (iii) both survive: max ell <= spread + 1 <= 3. ***")
    else:
        print("  *** one of the two claims FAILS at these sizes:")
        if max(ksp) > 2:
            print("      spread(kappa) reached %d, so cor:constant-bound's (i) is false"
                  % max(ksp))
        if min(dsp) < -1:
            print("      path defect reached %d, so (iii) is false" % min(dsp))
        print("      resulting bound would be spread + |defect| = %d"
              % (max(ksp) + (-min(dsp))))


if __name__ == "__main__":
    main()
