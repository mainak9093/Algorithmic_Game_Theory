# -*- coding: utf-8 -*-
"""
Search for a running example for the algorithm walkthrough in talk.tex.

We want ONE negative dichotomous instance whose run shows every case of
Algorithm 1: Tao et al.'s rules (R1), (R2) and (R3), a halt with chores left
over, and our completion with a subsidy set P that genuinely propagates.
Random instances almost never do this, so we search.

Cost family (never shown on the slides, so it only has to be dichotomous):
agent i splits the chores into "windows" and pays one unit per window her
bundle touches, after a free allowance a_i and up to a cap b_i:

    c_i(S) = min( max(0, #windows of i touched by S  -  a_i),  b_i ).

Window counting has marginals in {0,1}; the map x -> min(max(0, x - a), b) is
non-decreasing with unit steps, so every marginal of c_i stays in {0,1} and
c_i(empty) = 0. It covers the paper's own examples: min(|S|, 2) and
max(0, |S| - 1) are singleton windows with a cap, resp. an allowance.

Tie-breaking is taken from updates_pareto/update_1/algo1.py by calling its
own sccs_and_tail and find_cycle_through, so a run here is the run twyz()
performs on the same costs. build_demo.py re-checks that on full cost tables.
"""
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ALGO = os.path.normpath(os.path.join(HERE, "..", "..", "..", "updates_pareto", "update_1"))
sys.path.insert(0, ALGO)
from algo1 import sccs_and_tail, find_cycle_through  # noqa: E402


# --------------------------------------------------------------------------
# Instances
# --------------------------------------------------------------------------

class Inst:
    def __init__(self, n, m, K, grp, a, b):
        self.n, self.m, self.K = n, m, list(K)
        self.grp = [list(g) for g in grp]      # grp[i][e] in {-1, 0..K_i-1}
        self.a, self.b = list(a), list(b)      # allowance, cap (None = no cap)
        self.rebuild()

    def rebuild(self):
        self.gm = []
        for i in range(self.n):
            masks = [0] * self.K[i]
            for e in range(self.m):
                if self.grp[i][e] >= 0:
                    masks[self.grp[i][e]] |= 1 << e
            self.gm.append(masks)

    def cost(self, i, S):
        f = 0
        for mk in self.gm[i]:
            if S & mk:
                f += 1
        c = f - self.a[i]
        if c < 0:
            c = 0
        if self.b[i] is not None and c > self.b[i]:
            c = self.b[i]
        return c

    def copy(self):
        return Inst(self.n, self.m, self.K, self.grp, self.a, self.b)

    def as_dict(self):
        return {"n": self.n, "m": self.m, "K": self.K, "grp": self.grp,
                "a": self.a, "b": self.b}


def random_inst(rng, n, m):
    K = [rng.randint(3, 6) for _ in range(n)]
    grp = [[(-1 if rng.random() < 0.10 else rng.randrange(K[i])) for _ in range(m)]
           for i in range(n)]
    a = [rng.choice([0, 0, 0, 1]) for _ in range(n)]
    b = [rng.choice([None, None, 2, 3]) for _ in range(n)]
    return Inst(n, m, K, grp, a, b)


# --------------------------------------------------------------------------
# The run, mirroring algo1.twyz() and algo1.algorithm1()
# --------------------------------------------------------------------------

def eq_graph(I, X):
    n = I.n
    own = [I.cost(i, X[i]) for i in range(n)]
    return {(i, j) for i in range(n) for j in range(n)
            if i != j and own[i] == I.cost(i, X[j])}


def tails_of(E, n):
    """All tail SCCs (to check uniqueness); the one used is algo1's choice."""
    comps, _ = sccs_and_tail(E, n)
    return [c for c in comps if not any(i in c and j not in c for (i, j) in E)]


def run(I, cap=300):
    n, m = I.n, I.m
    X = [0] * n
    R = set(range(m))
    scan = list(range(m))
    ev = []
    for _ in range(cap):
        if not R:
            return X, R, None, ev
        done = False
        for e in [x for x in scan if x in R]:                          # (R1)
            for i in range(n):
                if I.cost(i, X[i] | (1 << e)) - I.cost(i, X[i]) == 0:
                    X[i] |= 1 << e
                    R.discard(e)
                    ev.append(("R1", e, i))
                    done = True
                    break
            if done:
                break
        if done:
            continue
        E = eq_graph(I, X)
        for e in [x for x in scan if x in R]:                          # (R2)
            for (i, j) in sorted(E):
                if I.cost(i, X[j] | (1 << e)) - I.cost(i, X[j]) != 0:
                    continue
                cyc = find_cycle_through(E, i, j, n)
                if cyc is None:
                    continue
                old = list(X)
                for t, x in enumerate(cyc):
                    X[x] = old[cyc[(t + 1) % len(cyc)]]
                X[i] |= 1 << e
                R.discard(e)
                ev.append(("R2", e, i, j, tuple(cyc)))
                done = True
                break
            if done:
                break
        if done:
            continue
        _, tail = sccs_and_tail(E, n)                                  # (R3)
        ntails = len(tails_of(E, n))
        if len(R) >= len(tail):
            gave = []
            for x in sorted(tail):
                e = min(R)
                X[x] |= 1 << e
                R.discard(e)
                gave.append((e, x))
            ev.append(("R3", tuple(sorted(tail)), tuple(gave), ntails))
            continue
        ev.append(("HALT", tuple(sorted(tail)), ntails))
        return X, R, tail, ev
    return X, R, "CAP", ev


def complete(I, X, R, S):
    n = I.n
    Rl = sorted(R)
    r = len(Rl)
    T = sorted(S)[:r]
    A = list(X)
    for k, t in enumerate(T):
        A[t] = X[t] | (1 << Rl[k])
    E = eq_graph(I, X)
    P = set(T)
    rounds = []
    while True:
        new = {i for i in range(n) if i not in P and i not in S
               and any((i, j) in E for j in P)}
        if not new:
            break
        rounds.append(sorted(new))
        P |= new
    p = [1 if i in P else 0 for i in range(n)]
    return A, p, T, P, rounds, E


def overlays(ev, rounds):
    """Overlay count after batching consecutive R1 steps."""
    cnt, prev = 1, None
    for x in ev:
        if x[0] == "R1":
            if prev != "R1":
                cnt += 1
        elif x[0] in ("R2", "R3"):
            cnt += 2
        else:
            cnt += 1
        prev = x[0]
    return cnt + 1 + 1 + len(rounds) + 1        # S, T, P rounds, payments


# --------------------------------------------------------------------------
# Scoring
# --------------------------------------------------------------------------

def evaluate(I):
    X, R, S, ev = run(I)
    if S is None or S == "CAP" or len(R) < 1:
        return None
    kinds = [x[0] for x in ev]
    A, p, T, P, rounds, E = complete(I, X, R, S)
    n = I.n
    hard = {
        "|S|>=3": len(S) >= 3,
        "R1": kinds.count("R1") >= 1,
        "R2": kinds.count("R2") >= 1,
        "proper R3 handout": any(x[0] == "R3" and len(x[1]) < n for x in ev),
        "unique tail at every R3": all(x[-1] == 1 for x in ev if x[0] in ("R3", "HALT")),
        "P beyond T": len(P) > len(T),
        "unpaid outsider": any(i not in S and i not in P for i in range(n)),
    }
    nice = {
        "two R3 handouts": kinds.count("R3") >= 2,
        "P chain of 2": len(rounds) >= 2,
        "sparse final graph": len(E) <= 12,
        "short": overlays(ev, rounds) <= 18,
        # a handout to a genuine multi-agent tail SCC shows (R3) far better
        # than one to a singleton
        "multi-agent R3 handout": any(x[0] == "R3" and 2 <= len(x[1]) < n for x in ev),
        # a rotation around 3+ agents shows (R2) better than a 2-cycle swap
        "R2 cycle of 3+": any(x[0] == "R2" and len(x[4]) >= 3 for x in ev),
        "few R1 steps": kinds.count("R1") <= 6,
    }
    score = 10 * sum(hard.values()) + sum(nice.values())
    return score, hard, nice, dict(X=X, R=R, S=S, ev=ev, A=A, p=p, T=T, P=P,
                                   rounds=rounds, E=E)


def mutate(I, rng):
    J = I.copy()
    roll = rng.random()
    i = rng.randrange(J.n)
    if roll < 0.80:
        e = rng.randrange(J.m)
        J.grp[i][e] = rng.randrange(-1, J.K[i])
    elif roll < 0.90:
        J.a[i] = rng.choice([0, 0, 1, 2])
    else:
        J.b[i] = rng.choice([None, 1, 2, 3, 4])
    J.rebuild()
    return J


def search(seed, budget_restarts=60, climb=900):
    rng = random.Random(seed)
    best = None
    for restart in range(budget_restarts):
        n = rng.choice([6, 7])
        m = rng.randint(11, 15)
        # rejection-sample a starting point that already halts with leftovers
        for _ in range(4000):
            I = random_inst(rng, n, m)
            got = evaluate(I)
            if got is not None:
                break
        else:
            continue
        cur, cur_score = I, got[0]
        for _ in range(climb):
            J = mutate(cur, rng)
            g = evaluate(J)
            if g is None:
                continue                      # keep "halts with leftovers" hard
            if g[0] >= cur_score:
                cur, cur_score = J, g[0]
        g = evaluate(cur)
        key = (g[0], -len(g[3]["E"]))
        if best is None or key > best[0]:
            best = (key, cur, g)
            print("restart %2d  n=%d m=%d  score=%d  hard=%d/7  nice=%d/7  |E|=%d"
                  % (restart, n, m, g[0], sum(g[1].values()), sum(g[2].values()),
                     len(g[3]["E"])), flush=True)
        if g[0] == 77:
            break
    return best


if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    best = search(seed)
    key, I, g = best
    print()
    print("hard:", g[1])
    print("nice:", g[2])
    st = g[3]
    print("events:", [x[0] for x in st["ev"]])
    print("S =", sorted(st["S"]), " R =", sorted(st["R"]), " T =", st["T"],
          " P =", sorted(st["P"]), " rounds =", st["rounds"])
    print("INSTANCE =", I.as_dict())
