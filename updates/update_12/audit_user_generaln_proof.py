"""
AUDIT of conjecture2_general_n_full_proof.md (user's general-n proof).

That proof differs from the min-cost/potential route: it uses the IDENTITY
assignment (no bundle reassignment) and an explicitly constructed subsidy set

    P = T  union  {backward equality closure of T through agents OUTSIDE S}

with p = indicator(P). It never invokes Halpern-Shah.

This script implements exactly that construction on real terminal states of
TWYZ Algorithm 3 and checks:
  (1) the EF inequalities directly, for every ordered pair;
  (2) p in {0,1}^n and |P| <= n-1;
  (3) the two terminal lemmas (Lemma 1, Lemma 2) independently;
  (4) that the claim holds for EVERY choice of recipient set T inside S and
      EVERY bijection of leftovers to T (the proof says "choose any").
"""
import itertools
import random
import sys

from probe_n4 import random_dichotomous, algorithm3, envy_graph, marg


def backward_closure(costs, X, N, S, T):
    """P = T, then repeatedly add i not in S having an equality edge i->j, j in P."""
    E = envy_graph(costs, X, N)
    P = set(T)
    changed = True
    while changed:
        changed = False
        for i in range(N):
            if i in P or i in S:
                continue
            if any((i, j) in E for j in P):
                P.add(i)
                changed = True
    return P


def check_instance(costs, X, R, S, N, verbose=False):
    """Returns list of problem strings (empty = all good)."""
    problems = []
    Rl = sorted(R)
    r = len(Rl)
    if r == 0:
        return problems

    # (3) terminal lemmas, checked independently
    for i in range(N):
        for e in Rl:
            if marg(costs[i], e, X[i]) != 1:
                problems.append(f"Lemma1 fails: c_{i}(e{e}|X_{i}) != 1")
    E = envy_graph(costs, X, N)
    for (i, j) in E:
        if i in S and j in S:
            for e in Rl:
                if marg(costs[i], e, X[j]) != 1:
                    problems.append(f"Lemma2 fails: edge({i},{j}) in S, c_{i}(e{e}|X_{j}) != 1")
    # tail property: no edge leaving S
    for (i, j) in E:
        if i in S and j not in S:
            problems.append(f"S not a tail: edge ({i},{j}) leaves S")
    if not (r < len(S)):
        problems.append(f"r={r} not < |S|={len(S)}")

    # (4) every recipient set T inside S, every bijection
    for T_tuple in itertools.permutations(sorted(S), r):
        A = [set(b) for b in X]
        for e, t in zip(Rl, T_tuple):
            A[t].add(e)
        A = [frozenset(b) for b in A]
        P = backward_closure(costs, X, N, S, set(T_tuple))
        p = [1 if i in P else 0 for i in range(N)]

        # (2) budget
        if len(P) > N - 1:
            problems.append(f"|P|={len(P)} > n-1  (T={T_tuple})")
        if any(v not in (0, 1) for v in p):
            problems.append(f"p not binary: {p}")

        # (1) EF, checked directly
        for i in range(N):
            for j in range(N):
                if costs[i][A[i]] - p[i] > costs[i][A[j]] - p[j]:
                    problems.append(
                        f"EF VIOLATED i={i} j={j} T={T_tuple} P={sorted(P)} "
                        f"c_i(A_i)={costs[i][A[i]]} p_i={p[i]} "
                        f"c_i(A_j)={costs[i][A[j]]} p_j={p[j]}")
    return problems


def biased_dichotomous(m, rng, pbias):
    c = {frozenset(): 0}
    for r in range(1, m+1):
        for Ss in itertools.combinations(range(m), r):
            Ss = frozenset(Ss)
            lo = max(c[Ss-{b}] for b in Ss); hi = min(c[Ss-{b}]+1 for b in Ss)
            c[Ss] = hi if (lo != hi and rng.random() < pbias) else lo
    return c


def main(N, m, trials, seed, pbias=None):
    rng = random.Random(seed)
    stats = {}
    total_problems = 0
    for t in range(trials):
        if pbias is None:
            costs = [random_dichotomous(m, rng) for _ in range(N)]
        else:
            costs = [biased_dichotomous(m, rng, pbias) for _ in range(N)]
        X, R, S = algorithm3(costs, m, N)
        stats[len(R)] = stats.get(len(R), 0) + 1
        if not R:
            continue
        probs = check_instance(costs, X, R, S, N)
        if probs:
            total_problems += len(probs)
            print(f"  trial {t}: {len(probs)} problem(s); first 3:")
            for q in probs[:3]:
                print("     ", q)
            print(f"     X={[sorted(b) for b in X]} R={sorted(R)} S={sorted(S)}")
    print(f"n={N} m={m} trials={trials} seed={seed} bias={pbias}")
    print(f"  residue sizes: {dict(sorted(stats.items()))}")
    print(f"  TOTAL PROBLEMS: {total_problems}")
    return total_problems


if __name__ == "__main__":
    N = int(sys.argv[1]); m = int(sys.argv[2])
    tr = int(sys.argv[3]); sd = int(sys.argv[4])
    pb = float(sys.argv[5]) if len(sys.argv) > 5 else None
    sys.exit(1 if main(N, m, tr, sd, pb) else 0)
