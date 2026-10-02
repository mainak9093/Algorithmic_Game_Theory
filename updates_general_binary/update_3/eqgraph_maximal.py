"""
Experiment 4: halt only when no envy-free extension is left, then test a
structured one-shot completion.

Experiment 2 showed two ways the literal mirror stops early: the goods handout
demanded a good for EVERY member of the source SCC, and goods and chores were
never placed together. Both are envy-free extensions the rules missed. Here the
phase applies any envy-free extension it can find, in this priority:

  E1   one item, bundles where they are
  E2   one item, after an envy-free reassignment of the bundles
       (each agent moves along an equality arc, so no value changes)
  TAIL Tao's handout: one chore-for-everyone to each member of a tail SCC
  E3   any two items, to one agent or two, with or without a reassignment
       (covers a good and a chore on the same agent, which cancel)
  E4   goods to any set of three or more agents, one each, each worth +1
       to its recipient, with or without a reassignment

so that at a halt the state is envy-free MAXIMAL for moves of these shapes.

Completion tested at the halt ("STRUCT"): some tail SCC S, distinct members of
S each take one leftover chore, and the leftover goods go to distinct agents
each valuing its good at +1 on the bundle it lands in; Halpern-Shah decides.
STRUCT is what a proof would construct, so its failures are what matter.

    python eqgraph_maximal.py [n] [m] [trials] [seed] [family] [mode]
"""
import itertools
import random
import sys
from collections import Counter

import eqgraph_signed as eg


def ef_perms(v, X, n):
    """Envy-free reassignments: every agent keeps its own value."""
    ident = tuple(range(n))
    out = [ident]
    for perm in itertools.permutations(range(n)):
        if perm != ident and all(v[i][X[perm[i]]] == v[i][X[i]] for i in range(n)):
            out.append(perm)
    return out


def try_add(v, Y, adds, n):
    Z = list(Y)
    for e, a in adds:
        Z[a] |= 1 << e
    return Z if eg.is_ef(v, Z, n) else None


def find_extension(v, X, R, n, cmask, rng):
    """The first rule class with an envy-free extension, and one such move."""
    items = sorted(R)
    perms = ef_perms(v, X, n)
    ident, others = perms[0], perms[1:]

    def single(plist):
        cand = []
        for perm in plist:
            Y = [X[perm[i]] for i in range(n)]
            for e in items:
                for a in range(n):
                    if try_add(v, Y, [(e, a)], n) is not None:
                        cand.append((perm, ((e, a),)))
        return cand

    cand = single([ident]) or single(others)
    if cand:
        return "E1/E2", rng.choice(cand)

    E = eg.eq_graph(v, X, n)
    comps = eg.sccs(E, n)
    tail = list(eg.moves_TAIL(v, X, R, E, n, cmask, comps))
    if tail:
        return "TAIL", (ident, tail[0][2])

    for plist in ([ident], others):
        cand = []
        for perm in plist:
            Y = [X[perm[i]] for i in range(n)]
            for e1, e2 in itertools.combinations(items, 2):
                for a1 in range(n):
                    for a2 in range(n):
                        if try_add(v, Y, [(e1, a1), (e2, a2)], n) is not None:
                            cand.append((perm, ((e1, a1), (e2, a2))))
        if cand:
            return "E3", rng.choice(cand)

    goods = [e for e in items if not all(cmask[i] >> e & 1 for i in range(n))]
    for plist in ([ident], others):
        for perm in plist:
            Y = [X[perm[i]] for i in range(n)]
            for size in range(3, n + 1):
                for T in itertools.combinations(range(n), size):
                    for gs in itertools.permutations(goods, size):
                        if all(eg.marg(v, t, g, Y[t]) == 1 for t, g in zip(T, gs)):
                            adds = list(zip(gs, T))
                            if try_add(v, Y, adds, n) is not None:
                                return "E4", (perm, tuple(adds))
    return None, None


def maximal_phase(v, n, m, cmask, rng, cap=400):
    X, R = [0] * n, set(range(m))
    used = Counter()
    for _ in range(cap):
        if not R:
            break
        rule, mv = find_extension(v, X, R, n, cmask, rng)
        if rule is None:
            break
        perm, adds = mv
        X = [X[perm[i]] for i in range(n)]
        for e, a in adds:
            X[a] |= 1 << e
            R.discard(e)
        assert eg.is_ef(v, X, n)
        used[rule] += 1
    return X, R, used


def struct_completion(v, X, R, n, cmask):
    """Does STRUCT succeed for some tail SCC and some choice of recipients?"""
    h = eg.halting_report(v, X, R, n, cmask)
    chores, goods = h["chores"], h["goods"]
    for S in h["tails"]:
        if len(chores) >= len(S) and chores:
            continue
        for TC in itertools.permutations(sorted(S), len(chores)):
            B = list(X)
            for c, t in zip(chores, TC):
                B[t] |= 1 << c
            for TG in itertools.permutations(range(n), len(goods)):
                if any(eg.marg(v, t, g, B[t]) != 1 for g, t in zip(goods, TG)):
                    continue
                A = list(B)
                for g, t in zip(goods, TG):
                    A[t] |= 1 << g
                s = eg.max_min_subsidy(v, A, n)
                if s is not None and s <= 1:
                    return True
    return False


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    m = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    trials = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    family = sys.argv[5] if len(sys.argv) > 5 else "random"
    mode = sys.argv[6] if len(sys.argv) > 6 else "objective"
    rng = random.Random(seed)
    tally, left, rules = Counter(), Counter(), Counter()
    shown = 0
    for t in range(trials):
        v, cmask = eg.random_instance(n, m, rng, mode, family,
                                      p_chore=rng.choice([0.3, 0.5, 0.7]),
                                      p_one=rng.choice([0.3, 0.5, 0.7]))
        X, R, used = maximal_phase(v, n, m, cmask, rng)
        rules.update(used)
        if not R:
            tally["complete, no subsidy"] += 1
            continue
        h = eg.halting_report(v, X, R, n, cmask)
        left[(len(h["chores"]), len(h["goods"]))] += 1
        if struct_completion(v, X, R, n, cmask):
            tally["STRUCT ok"] += 1
            continue
        anyp = eg.exists_unit_completion(v, X, R, n, permute=True)
        tally["STRUCT fails | some completion exists=%s" % anyp] += 1
        if shown < 3:
            shown += 1
            print("--- STRUCT fails (trial %d); some completion exists: %s" % (t, anyp))
            print("   chore masks", [bin(c) for c in cmask], " X", [bin(S) for S in X],
                  " leftover chores", h["chores"], " goods", h["goods"])
            print("   values v_i(X_j):", [[v[i][X[j]] for j in range(n)] for i in range(n)])
            print("   tails", [sorted(c) for c in h["tails"]],
                  " sources", [sorted(c) for c in h["sources"]])
    print()
    print("n=%d m=%d trials=%d seed=%d family=%s mode=%s" % (n, m, trials, seed, family, mode))
    for k, c in sorted(tally.items(), key=lambda kv: -kv[1]):
        print("  %6d  %s" % (c, k))
    print("  (leftover chores, leftover goods) at halt:", dict(sorted(left.items())))
    print("  rule use:", dict(rules))


if __name__ == "__main__":
    main()
