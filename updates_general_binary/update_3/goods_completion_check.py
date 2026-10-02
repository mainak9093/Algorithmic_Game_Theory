"""
Machine check of the GOODS COMPLETION LEMMA (approach 21), with the explicit
payment the proof constructs -- not Halpern-Shah's optimum.

LEMMA. Let X be an envy-free partial allocation (signed dichotomous,
objective or doubly monotone) whose unallocated items R are all goods-type,
and let tau : R -> N be injective with v_{tau(g)}(g | X_{tau(g)}) = 1 for
every g (each recipient values its item at exactly +1 on its own bundle).
Put A_t = X_t + tau^{-1}(t), T = tau(R), and let Q be the smallest set with
  (Q1) every k not in T tied to some t in T (v_k(X_k) = v_k(X_t)) with
       v_k(g | X_t) = 1 for the item g of t, is in Q;
  (Q2) every k not in T tied to some member of Q is in Q.
Then (A, 1[Q]) is envy-free, and sum p = |Q| <= n - |T| <= n - 1.

The check: random envy-free partial allocations whose leftovers are
goods-type, EVERY admissible tau, the explicit payment above.

    python goods_completion_check.py [n] [m] [instances] [seed] [mode]
"""
import itertools
import random
import sys

import eqgraph_signed as eg


def closure_payment(v, X, n, tau):
    T = set(tau.values())
    gift = {t: g for g, t in tau.items()}
    tied = {(k, j) for k in range(n) for j in range(n)
            if k != j and v[k][X[k]] == v[k][X[j]]}
    Q = {k for k in range(n) if k not in T
         and any((k, t) in tied and eg.marg(v, k, gift[t], X[t]) == 1 for t in T)}
    frontier = list(Q)
    while frontier:
        q = frontier.pop()
        for k in range(n):
            if k not in T and k not in Q and (k, q) in tied:
                Q.add(k)
                frontier.append(k)
    return [1 if i in Q else 0 for i in range(n)], T


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    m = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    instances = int(sys.argv[3]) if len(sys.argv) > 3 else 2000
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    mode = sys.argv[5] if len(sys.argv) > 5 else "objective"
    rng = random.Random(seed)
    states = taus = bad_ef = bad_budget = 0
    for _ in range(instances):
        v, cmask = eg.random_instance(n, m, rng, mode,
                                      rng.choice(["random", "additive"]),
                                      p_chore=rng.choice([0.3, 0.5, 0.7]),
                                      p_one=rng.choice([0.3, 0.5, 0.7]))
        goods = [e for e in range(m) if not all(cmask[i] >> e & 1 for i in range(n))]
        for _ in range(30):                       # random states per instance
            left = [g for g in goods if rng.random() < 0.5][:n]
            X = [0] * n
            for e in range(m):
                if e not in left:
                    X[rng.randrange(n)] |= 1 << e
            if not left or not eg.is_ef(v, X, n):
                continue
            states += 1
            for TG in itertools.permutations(range(n), len(left)):
                if any(eg.marg(v, t, g, X[t]) != 1 for g, t in zip(left, TG)):
                    continue
                taus += 1
                tau = dict(zip(left, TG))
                p, T = closure_payment(v, X, n, tau)
                A = list(X)
                for g, t in tau.items():
                    A[t] |= 1 << g
                ok = all(v[i][A[i]] + p[i] >= v[i][A[j]] + p[j]
                         for i in range(n) for j in range(n))
                bad_ef += not ok
                bad_budget += sum(p) > n - len(T)
                if not ok and bad_ef <= 2:
                    print("COUNTEREXAMPLE", [bin(S) for S in X], tau, p)
    print("n=%d m=%d instances=%d seed=%d mode=%s" % (n, m, instances, seed, mode))
    print("envy-free states with goods-type leftovers : %d" % states)
    print("admissible tau tested                      : %d" % taus)
    print("explicit payment NOT envy-free              : %d   (must be 0)" % bad_ef)
    print("explicit payment over n - |T|               : %d   (must be 0)" % bad_budget)


if __name__ == "__main__":
    main()
