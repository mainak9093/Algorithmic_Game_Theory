"""
The smallest and most readable witness that the incremental invariant fails.

deadhunt.py shows STUCK states are common at m=4. For the paper a witness must
be small and interpretable, so this searches exhaustively at m=3 -- the whole
negative dichotomous class, 38 valuations, 54,872 triples -- and ranks the
witnesses by how simple their cost functions are.

The invariant at stake, which is what BKNS's proof runs on:

    INV  every envy-freeable partial allocation with subsidies in {0,1}^n can
         absorb one more chore, into some bundle and under some reassignment
         of the bundles, and still have subsidies in {0,1}^n.

A STUCK state is a valid partial allocation X and an unallocated chore g such
that for every agent s, the multiset obtained by adding g to X_s admits no
valid assignment. Since reassignment is quantified over, the failure does not
depend on any tie-breaking rule.

Simplicity score: prefer cost functions that are symmetric in the items and
take few distinct values, so the example can be stated in words.
"""
import itertools

from gb_valuations import enumerate_class

N, M = 3, 3
PERM = list(itertools.permutations(range(N)))


def subsidy(cs, X):
    base = sum(cs[i][X[i]] for i in range(N))
    for p in PERM:
        if sum(cs[i][X[p[i]]] for i in range(N)) > base:
            return None
    w = [[cs[i][X[j]] - cs[i][X[i]] for j in range(N)] for i in range(N)]
    best = [0] * N
    def walk(s, cur, seen, tot):
        best[s] = max(best[s], tot)
        for j in range(N):
            if j != cur and not seen & (1 << j):
                walk(s, j, seen | (1 << j), tot + w[cur][j])
    for i in range(N):
        walk(i, i, 1 << i, 0)
    return best


def valid(cs, X):
    p = subsidy(cs, X)
    return p is not None and max(p) <= 1


def good(cs, b):
    return any(valid(cs, tuple(b[p[i]] for i in range(N))) for p in PERM)


def sym(v):
    """True if the cost depends only on |S| -- the most readable shape."""
    by = {}
    for S in range(1 << M):
        k = bin(S).count("1")
        if k in by and by[k] != -v[S]:
            return False
        by[k] = -v[S]
    return True


def show(S):
    return "{" + ",".join("abc"[k] for k in range(M) if S & (1 << k)) + "}"


def main():
    pool = enumerate_class(M, {-1, 0})
    print("chores valuations on m=3: %d ; triples: %d" % (len(pool), len(pool) ** N))
    hits = []
    for cs in itertools.product(pool, repeat=N):
        cs = list(cs)
        for o in itertools.product(list(range(N)) + [None], repeat=M):
            b = [0] * N
            left = []
            for k, i in enumerate(o):
                if i is None:
                    left.append(k)
                else:
                    b[i] |= 1 << k
            X = tuple(b)
            if len(left) != 1 or not valid(cs, X):
                continue
            g = left[0]
            if any(good(cs, [X[t] | ((1 << g) if t == s else 0)
                             for t in range(N)]) for s in range(N)):
                continue
            score = (-sum(1 for v in cs if sym(v)),
                     len({tuple(v) for v in cs}),
                     sum(len({-v[S] for S in range(1 << M)}) for v in cs))
            hits.append((score, cs, X, g))
            break
    hits.sort(key=lambda t: t[0])
    print("instances with a STUCK state at m=3 : %d" % len(hits))
    print()
    seen = set()
    shown = 0
    for score, cs, X, g in hits:
        key = tuple(tuple(v) for v in cs)
        if key in seen:
            continue
        seen.add(key)
        print("WITNESS %d  (symmetric agents: %d)" % (shown + 1, -score[0]))
        for i in range(N):
            costs = [-cs[i][S] for S in range(1 << M)]
            if sym(cs[i]):
                by = [costs[(1 << k) - 1] for k in range(M + 1)]
                print("   agent %d : cost depends only on size -- %s" % (i + 1, by))
            else:
                print("   agent %d : costs %s" % (i + 1, costs))
        print("   state %s  chore %s left  subsidy %s"
              % ([show(x) for x in X], "abc"[g], subsidy(cs, X)))
        for s in range(N):
            nb = [X[t] | ((1 << g) if t == s else 0) for t in range(N)]
            print("      add %s to bundle %d -> %s : valid under any "
                  "reassignment? %s"
                  % ("abc"[g], s + 1, [show(x) for x in nb], good(cs, nb)))
        print()
        shown += 1
        if shown >= 3:
            break


if __name__ == "__main__":
    main()
