"""
The run: BKNS's algorithm, sign-flipped, on the 3-agent 3-chore instance.

BKNS Algorithm 1 has two branches. Its EXTEND branch requires the incoming item
to have MARGINAL +1 for the recipient; no chore has a positive marginal, so
that branch is vacuous under the sign flip and every step goes to FINDSINK.
FINDSINK selects an agent from M(p), the set of agents of MAXIMUM subsidy.

This prints the state, the subsidy, and M(p) at each step, and at the final
step every option for the last chore.
"""
import itertools

N, M = 3, 3
NAMES = "abc"
PERM = list(itertools.permutations(range(N)))


def cost(i, S):
    # agent 1 is the absorbing one: the first chore is free for her.
    k = bin(S).count("1")
    return max(0, k - 1) if i == 0 else min(k, 2)


def show(S):
    return "{" + ",".join(NAMES[k] for k in range(M) if S & (1 << k)) + "}"


def subsidy(X):
    base = sum(-cost(i, X[i]) for i in range(N))
    if any(sum(-cost(i, X[p[i]]) for i in range(N)) > base for p in PERM):
        return None
    w = [[cost(i, X[i]) - cost(i, X[j]) for j in range(N)] for i in range(N)]
    best = [0] * N
    def walk(s, cur, seen, tot):
        best[s] = max(best[s], tot)
        for j in range(N):
            if j != cur and not seen & (1 << j):
                walk(s, j, seen | (1 << j), tot + w[cur][j])
    for i in range(N):
        walk(i, i, 1 << i, 0)
    return best


def main():
    print("costs by bundle size:  agent1 : %s     agents 2,3 : %s"
          % ([cost(0, (1 << k) - 1) for k in range(M + 1)],
             [cost(1, (1 << k) - 1) for k in range(M + 1)]))
    print()
    X = (0, 0, 0)
    p = subsidy(X)
    print("start           %s   subsidy %s   M(p)=%s"
          % ([show(x) for x in X], p,
             [i + 1 for i in range(N) if p[i] == max(p)]))
    for g, who in ((0, 0), (1, 0)):
        X = tuple(X[t] | ((1 << g) if t == who else 0) for t in range(N))
        p = subsidy(X)
        print("give %s to agent %d  %s   subsidy %s   M(p)=%s"
              % (NAMES[g], who + 1, [show(x) for x in X], p,
                 [i + 1 for i in range(N) if p[i] == max(p)]))
    print()
    print("last chore c -- every option:")
    for s in range(N):
        nb = [X[t] | ((1 << 2) if t == s else 0) for t in range(N)]
        best = None
        for perm in PERM:
            Y = tuple(nb[perm[i]] for i in range(N))
            q = subsidy(Y)
            if q is not None and (best is None or max(q) < max(best[1])):
                best = (Y, q)
        print("   add c to bundle %d -> %-28s best over all reassignments: %s"
              % (s + 1, str([show(x) for x in nb]),
                 "subsidy %s (max %d)" % (best[1], max(best[1]))))
    print()
    print("a valid complete allocation does exist:")
    Y = (1, 2, 4)
    print("   %s   subsidy %s" % ([show(x) for x in Y], subsidy(Y)))


if __name__ == "__main__":
    main()
