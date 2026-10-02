"""
Experiment 2: what goes wrong when the symmetric completion fails?

    python diagnose_ksym.py [n] [m] [trials] [seed] [family] [max_show]

Collects halting states where K-SYM is 'fail' or 'unmatchable' and prints,
for each: the instance in compact form, the halting allocation, its equality
graph and SCC structure, the leftovers with every agent's marginal on its own
bundle and on the bundles it is tied to, K-SYM's placement with the
Halpern-Shah subsidies, and a working placement found by brute force.
"""
import itertools
import random
import sys

import eqgraph_signed as eg


def name(e, cm):
    return ("c" if cm >> e & 1 else "g") + str(e)


def bundle(S, m, cm):
    return "{" + ",".join(name(b, cm) for b in range(m) if S >> b & 1) + "}"


def subsidies(v, A, n):
    NEG = -10 ** 9
    d = [[(v[i][A[j]] - v[i][A[i]]) if i != j else 0 for j in range(n)]
         for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] > d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    if any(d[i][i] > 0 for i in range(n)):
        return None
    return [max(d[i]) for i in range(n)]


def show(v, X, R, n, m, cmask, tag):
    cm = cmask[0]                                 # objective: one chore mask
    h = eg.halting_report(v, X, R, n, cmask)
    print("=" * 78)
    print(tag)
    print("X =", [bundle(S, m, cm) for S in X],
          "  own values", [v[i][X[i]] for i in range(n)])
    print("value matrix v_i(X_j):")
    for i in range(n):
        print("   agent", i, [v[i][X[j]] for j in range(n)])
    print("arcs", sorted(h["E"]), " SCCs", [sorted(c) for c in h["comps"]],
          " tails", [sorted(c) for c in h["tails"]],
          " sources", [sorted(c) for c in h["sources"]])
    for e in sorted(R):
        print("  leftover", name(e, cm), ": marginal of agent i on X_j ->")
        for i in range(n):
            print("     agent", i, [eg.marg(v, i, e, X[j]) for j in range(n)])
    st, A = eg.symmetric_completion(v, X, R, n, cmask)
    print("K-SYM:", st)
    if A is not None:
        print("   placement", [bundle(S, m, cm) for S in A],
              " subsidies", subsidies(v, A, n))
    items = sorted(R)
    for owners in itertools.product(range(n), repeat=len(items)):
        B = list(X)
        for e, o in zip(items, owners):
            B[o] |= 1 << e
        p = subsidies(v, B, n)
        if p is not None and max(p) <= 1:
            print("   a working placement:", [bundle(S, m, cm) for S in B],
                  " subsidies", p)
            break


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    m = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    trials = int(sys.argv[3]) if len(sys.argv) > 3 else 3000
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 16
    family = sys.argv[5] if len(sys.argv) > 5 else "additive"
    max_show = int(sys.argv[6]) if len(sys.argv) > 6 else 4
    rng = random.Random(seed)
    shown = 0
    for t in range(trials):
        v, cm = eg.random_instance(n, m, rng, "objective", family,
                                   p_chore=rng.choice([0.3, 0.5, 0.7]),
                                   p_one=rng.choice([0.3, 0.5, 0.7]))
        X, R, trace = eg.ef_phase(v, n, m, cm, eg.ORDERS["F-ROT-TAIL-SRC"], rng)
        if not R:
            continue
        st, _ = eg.symmetric_completion(v, X, R, n, cm)
        if st in ("fail", "unmatchable"):
            show(v, X, R, n, m, cm, "trial %d: K-SYM %s" % (t, st))
            shown += 1
            if shown >= max_show:
                break


if __name__ == "__main__":
    main()
