"""
Experiment 7: machine check of main_findings_scc_migration.md (2026-10-03).

Pipeline, exactly as in the objective proof: chores first (Tao's rules F/ROT/
TAIL to a halt, then our completion: residual chores to the first members of
the halting tail SCC S*, payments = recipients + backward closure outside S*),
then the FIRST good g inserted with BKNS: EXTEND if possible, else FINDSINK
started at a recipient s0 in T, exploring EVERY choice of the next selected
agent (any agent whose minimal subsidy would reach 2).

Claims tested (p = pointwise-minimal subsidy of the chore allocation A):
  S2   g extendable (some tight reassignment hands a max-subsidy package to an
       agent valuing g at +1 on it)  <=>  some (i,j) with j in M(p) and
       Delta_i^g(A_j) = 1 has i = j, or (i,j) tight in H_p and on a tight cycle
  S3   T is contained in S* and in M(p)
  S4   each FINDSINK selection s_{t+1} reaches s_t by a tight path in H_p
  S5   s1 (the first selection) is not in S*
  S6   no re-entry: once a selection is outside S*, no later one is inside

    python scc_migration_check.py [n] [m] [instances] [seed]
"""
import itertools
import random
import sys

import eqgraph_signed as eg
from ins_eligible import minimal_subsidy


def chores_phase(v, n, cmask, chores, rng):
    """Tao's rules on the chores only, to a halt."""
    X, R = [0] * n, set(chores)
    for _ in range(200):
        if not R:
            break
        E = eg.eq_graph(v, X, n)
        comps = eg.sccs(E, n)
        cand = (list(eg.moves_F(v, X, R, E, n)) or list(eg.moves_ROT(v, X, R, E, n))
                or list(eg.moves_TAIL(v, X, R, E, n, cmask, comps)))
        if not cand:
            break
        X, R = eg.apply_move(v, X, R, rng.choice(cand), n)
    return X, R


def completion(v, X, R, n, cmask):
    E = eg.eq_graph(v, X, n)
    S = sorted(sorted(eg.tail_sccs(E, eg.sccs(E, n)), key=lambda c: (len(c), min(c)))[0])
    Rl = sorted(R)
    T = S[:len(Rl)]
    A = list(X)
    for c, t in zip(Rl, T):
        A[t] |= 1 << c
    return A, set(S), set(T)


def tight_graph(v, A, p, n):
    return {(i, j) for i in range(n) for j in range(n)
            if i != j and v[i][A[i]] + p[i] == v[i][A[j]] + p[j]}


def reach(E, n, a):
    seen, st = {a}, [a]
    while st:
        u = st.pop()
        for (x, y) in E:
            if x == u and y not in seen:
                seen.add(y)
                st.append(y)
    return seen


def extendable_bruteforce(v, A, p, n, g):
    mx = max(p)
    for perm in itertools.permutations(range(n)):
        if all(v[i][A[perm[i]]] + p[perm[i]] == v[i][A[i]] + p[i] for i in range(n)):
            for k in range(n):
                if p[perm[k]] == mx and eg.marg(v, k, g, A[perm[k]]) == 1:
                    return True
    return False


def extendable_graph(v, A, p, n, g, H):
    mx = max(p)
    for j in range(n):
        if p[j] != mx:
            continue
        for i in range(n):
            if eg.marg(v, i, g, A[j]) != 1:
                continue
            if i == j or ((i, j) in H and i in reach(H, n, j)):
                return True
    return False


def do_extend(v, A, p, n, g):
    """Apply EXTEND: a tight reassignment, then the max-subsidy holder valuing
    g at +1 takes it and drops its subsidy if it had one; return the new
    allocation with its pointwise-minimal subsidy."""
    mx = max(p)
    for perm in itertools.permutations(range(n)):
        if all(v[i][A[perm[i]]] + p[perm[i]] == v[i][A[i]] + p[i] for i in range(n)):
            for k in range(n):
                if p[perm[k]] == mx and eg.marg(v, k, g, A[perm[k]]) == 1:
                    B = [A[perm[i]] for i in range(n)]
                    B[k] |= 1 << g
                    q = minimal_subsidy(v, B, n)
                    assert eg.max_min_subsidy(v, B, n) is not None and max(q) <= 1
                    return B, q
    raise AssertionError("not extendable")


def do_findsink(v, A, p, n, g):
    """FINDSINK from the first max-subsidy agent, first choice each time."""
    s = min(i for i in range(n) if p[i] == max(p))
    seen = set()
    while s not in seen:
        seen.add(s)
        B = list(A)
        B[s] |= 1 << g
        if eg.max_min_subsidy(v, B, n) is None:
            return None, None
        f = minimal_subsidy(v, B, n)
        nxt = [a for a in range(n) if f[a] >= 2]
        if not nxt:
            return B, f
        s = nxt[0]
    return None, None


def findsink_tree(v, A, p, n, g, s0, H, Sstar, stats, max_depth=12, ctx=""):
    """Explore every FINDSINK branch from s0; record the claims."""
    def phi(s):
        B = list(A)
        B[s] |= 1 << g
        if eg.max_min_subsidy(v, B, n) is None:
            return None
        return minimal_subsidy(v, B, n)

    def walk(seq):
        s = seq[-1]
        f = phi(s)
        if f is None:
            stats["not envy-freeable (BKNS says impossible)"] += 1
            return
        nxt = [a for a in range(n) if f[a] >= 2]
        if not nxt:
            stats["branches terminating"] += 1
            return
        if len(seq) > max_depth:
            stats["depth cap"] += 1
            return
        for a in nxt:
            stats["selections"] += 1
            if p[a] != max(p):
                stats["selection outside M(p) (BKNS says impossible)"] += 1
            if s not in reach(H, n, a):
                stats["S4 fails: no tight path s_{t+1} -> s_t"] += 1
            if len(seq) == 1 and a in Sstar:
                stats["S5 fails: s1 in S*"] += 1
                Sconn = all(y in reach(H, n, x) for x in Sstar for y in Sstar)
                print("   S5 case: %s; S* strongly connected in H_p: %s; s0=%d s1=%d S*=%s p=%s"
                      % (ctx, Sconn, s, a, sorted(Sstar), p))
            outside_seen = any(x not in Sstar for x in seq[1:])
            if outside_seen and a in Sstar:
                stats["S6 fails: re-entry into S*"] += 1
                if stats["S6 fails: re-entry into S*"] <= 2:
                    print("   re-entry: selections", seq + [a], " S*", sorted(Sstar),
                          " p", p)
            if a in seq:
                stats["repeat selection (BKNS says impossible)"] += 1
                continue
            walk(seq + [a])

    walk([s0])


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    m = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    instances = int(sys.argv[3]) if len(sys.argv) > 3 else 3000
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    rng = random.Random(seed)
    stats = {}

    class D(dict):
        def __missing__(self, k):
            return 0
    stats = D()
    for _ in range(instances):
        v, cmask = eg.random_instance(n, m, rng, "objective",
                                      rng.choice(["random", "additive"]),
                                      p_chore=rng.choice([0.5, 0.7]),
                                      p_one=rng.choice([0.3, 0.5, 0.7]))
        chores = [e for e in range(m) if cmask[0] >> e & 1]
        goods = [e for e in range(m) if not cmask[0] >> e & 1]
        if not chores or not goods:
            continue
        X, R = chores_phase(v, n, cmask, chores, rng)
        if not R:
            continue
        A, Sstar, T = completion(v, X, R, n, cmask)
        p = minimal_subsidy(v, A, n)
        if max(p) > 1:
            stats["chore completion over 1 (our theorem says impossible)"] += 1
            continue
        stats["instances with residual chores"] += 1
        if not (T <= Sstar and all(p[t] == max(p) for t in T)):
            stats["S3 fails"] += 1
        for idx, g in enumerate(goods):           # every good, in sequence
            H = tight_graph(v, A, p, n)
            bf = extendable_bruteforce(v, A, p, n, g)
            gr = extendable_graph(v, A, p, n, g, H)
            stats["S2 agree"] += bf == gr
            stats["S2 DISAGREE"] += bf != gr
            if bf:
                stats["extendable"] += 1
                A, p = do_extend(v, A, p, n, g)
                continue
            stats["non-extendable -> FINDSINK"] += 1
            starts = sorted(s for s in range(n) if p[s] == max(p) and s in Sstar)
            for s0 in starts:
                findsink_tree(v, A, p, n, g, s0, H, Sstar, stats,
                              ctx="good #%d inserted, s0 %s T" % (idx + 1, "in" if s0 in T else "NOT in"))
            A, p = do_findsink(v, A, p, n, g)
            if A is None:
                stats["FINDSINK found no terminal state"] += 1
                break
    print()
    print("n=%d m=%d instances=%d seed=%d" % (n, m, instances, seed))
    for k in sorted(stats):
        print("  %-55s %d" % (k, stats[k]))


if __name__ == "__main__":
    main()
