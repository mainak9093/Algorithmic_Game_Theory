"""
Independent verification of the minimal witness, from the definitions.

Three agents, three chores a, b, c. Cost depends only on bundle size:

    agents 1 and 2 :  c(S) = min(|S|, 2)        -- 0, 1, 2, 2 by size
    agent 3        :  c(S) = max(0, |S| - 1)    -- 0, 0, 1, 2 by size

so for agents 1 and 2 the first two chores hurt and the third is absorbed, and
for agent 3 the first chore is absorbed and every later one hurts.

Everything below is recomputed from the definitions rather than reused from the
search: envy-freeability is checked as welfare-maximality over reassignments
(Halpern-Shah condition (ii)) and the minimum subsidy as the longest path.

Checked here:
  1  the instance is negative dichotomous;
  2  the state X = (empty, empty, {a,b}) is valid, with minimum subsidy (0,0,1);
  3  X is REACHABLE by inserting a then b, each step valid;
  4  no way of adding c -- any bundle, any reassignment -- is valid;
  5  the instance nevertheless HAS a valid complete allocation, so the theorem
     is untouched and only the incremental invariant fails.
"""
import itertools

N, M = 3, 3
NAMES = "abc"
PERM = list(itertools.permutations(range(N)))


def cost(i, S):
    k = bin(S).count("1")
    return min(k, 2) if i in (0, 1) else max(0, k - 1)


def show(S):
    return "{" + ",".join(NAMES[k] for k in range(M) if S & (1 << k)) + "}"


def envy_freeable(X):
    base = sum(-cost(i, X[i]) for i in range(N))
    return all(sum(-cost(i, X[p[i]]) for i in range(N)) <= base for p in PERM)


def subsidy(X):
    if not envy_freeable(X):
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


def valid(X):
    p = subsidy(X)
    return p is not None and max(p) <= 1


def good(b):
    for p in PERM:
        X = tuple(b[p[i]] for i in range(N))
        if valid(X):
            return X
    return None


def main():
    print("1  negative dichotomous?")
    ok = True
    for i in range(N):
        if cost(i, 0) != 0:
            ok = False
        for S in range(1 << M):
            for k in range(M):
                if not S & (1 << k) and cost(i, S | (1 << k)) - cost(i, S) not in (0, 1):
                    ok = False
    print("   c_i(empty)=0 and every marginal in {0,1} : %s" % ok)
    print("   cost by bundle size: agent1 %s  agent2 %s  agent3 %s"
          % ([cost(0, (1 << k) - 1) for k in range(M + 1)],
             [cost(1, (1 << k) - 1) for k in range(M + 1)],
             [cost(2, (1 << k) - 1) for k in range(M + 1)]))

    X = (0, 0, 0b011)
    print()
    print("2  the state X = %s" % [show(x) for x in X])
    print("   envy-freeable : %s   minimum subsidy : %s"
          % (envy_freeable(X), subsidy(X)))
    print("   arc weights w(i,j) = c_i(X_i) - c_i(X_j):")
    for i in range(N):
        print("      agent %d : %s"
              % (i + 1, [cost(i, X[i]) - cost(i, X[j]) for j in range(N)]))

    print()
    print("3  reachability -- insert a, then b")
    S = (0, 0, 0)
    for g, who in ((0, 2), (1, 2)):
        S = tuple(S[t] | ((1 << g) if t == who else 0) for t in range(N))
        print("   %s -> agent %d : %s   subsidy %s   valid %s"
              % (NAMES[g], who + 1, [show(x) for x in S], subsidy(S), valid(S)))
    print("   reaches X : %s" % (S == X))

    print()
    print("4  can chore c be added anywhere?")
    for s in range(N):
        nb = [X[t] | ((1 << 2) if t == s else 0) for t in range(N)]
        g = good(nb)
        print("   into bundle %d -> %s : %s"
              % (s + 1, [show(x) for x in nb],
                 "valid as %s" % ([show(x) for x in g],) if g
                 else "NO valid assignment"))
        if not g:
            for p in PERM:
                Y = tuple(nb[p[i]] for i in range(N))
                sp = subsidy(Y)
                print("        assignment %s : %s"
                      % ([show(x) for x in Y],
                         "not envy-freeable" if sp is None
                         else "subsidy %s" % sp))

    print()
    print("5  does a valid COMPLETE allocation exist?")
    allc = []
    for o in itertools.product(range(N), repeat=M):
        b = [0] * N
        for k, i in enumerate(o):
            b[i] |= 1 << k
        allc.append(tuple(b))
    ok = [Y for Y in allc if valid(Y)]
    print("   valid complete allocations : %d of %d" % (len(ok), len(allc)))
    for Y in ok[:3]:
        print("      %s   subsidy %s" % ([show(x) for x in Y], subsidy(Y)))


if __name__ == "__main__":
    main()
