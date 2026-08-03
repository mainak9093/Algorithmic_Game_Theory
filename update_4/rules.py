"""
rules.py -- candidate constructions for PS1, tested exhaustively on small instances.

For each random dichotomous chore instance we enumerate every partition of M into n
bundles, compute l(i) = longest path in the envy graph w(i,k) = c_i(A_i) - c_i(A_k),
and ask whether each candidate rule lands on an allocation with max_i l(i) <= 1.

Rules tested
  U            : some utilitarian-optimal allocation is good (sanity, known TRUE so far)
  U+bal        : utilitarian-optimal, tie-break lexicographically smallest sorted |A_i|
  U+leximin    : utilitarian-optimal, tie-break lexicographically smallest sorted c_i(A_i)
  U+bal+leximin: both, balance first
  IMM          : iterated minimum-marginal perfect matching (chore analogue of IMWPM)
  IMM-good?    : whether the IMM output is good
"""
import itertools, random
from typeorder import path_weights


def ell(cost, A, n):
    W = [[cost[i](A[i]) - cost[i](A[k]) for k in range(n)] for i in range(n)]
    return path_weights(W, n)


def random_dichotomous(m, rng):
    c = {frozenset(): 0}
    for r in range(1, m + 1):
        for S in itertools.combinations(range(m), r):
            S = frozenset(S)
            lo = max(c[S - {b}] for b in S)
            hi = min(c[S - {b}] + 1 for b in S)
            c[S] = rng.randint(lo, hi)
    return lambda S: c[frozenset(S)]


def partitions(n, m):
    for a in itertools.product(range(n), repeat=m):
        A = [set() for _ in range(n)]
        for g, i in enumerate(a):
            A[i].add(g)
        yield [frozenset(S) for S in A]


def imm(cost, n, m):
    """iterated minimum-marginal perfect matching; pad with zero-cost dummy chores"""
    rem = list(range(m))
    A = [set() for _ in range(n)]
    while rem:
        pool = rem + [None] * max(0, n - len(rem))       # None = dummy chore
        best, bestc = None, None
        for pick in itertools.permutations(range(len(pool)), n):
            tot, ok = 0, True
            for i in range(n):
                g = pool[pick[i]]
                if g is None:
                    continue
                tot += cost[i](frozenset(A[i] | {g})) - cost[i](frozenset(A[i]))
            if bestc is None or tot < bestc:
                bestc, best = tot, pick
        used = []
        for i in range(n):
            g = pool[best[i]]
            if g is not None:
                A[i].add(g)
                used.append(g)
        rem = [g for g in rem if g not in used]
    return [frozenset(S) for S in A]


def run(n, m, trials, seed):
    rng = random.Random(seed)
    fail = {k: 0 for k in ['U', 'U+bal', 'U+leximin', 'U+bal+leximin', 'IMM']}
    ex = {}
    for _ in range(trials):
        cost = [random_dichotomous(m, rng) for _ in range(n)]
        best_of = {}
        good_exists_U = False
        allparts = list(partitions(n, m))
        tot = [sum(cost[i](A[i]) for i in range(n)) for A in allparts]
        opt = min(tot)
        U = [A for A, t in zip(allparts, tot) if t == opt]
        for A in U:
            if max(ell(cost, A, n)) <= 1:
                good_exists_U = True
                break
        if not good_exists_U:
            fail['U'] += 1
            ex.setdefault('U', cost)

        def pick(key):
            return min(U, key=key)

        cands = {
            'U+bal': pick(lambda A: sorted((len(S) for S in A), reverse=True)),
            'U+leximin': pick(lambda A: sorted((cost[i](A[i]) for i in range(n)), reverse=True)),
            'U+bal+leximin': pick(lambda A: (sorted((len(S) for S in A), reverse=True),
                                             sorted((cost[i](A[i]) for i in range(n)),
                                                    reverse=True))),
        }
        for k, A in cands.items():
            if max(ell(cost, A, n)) > 1:
                fail[k] += 1
                ex.setdefault(k, cost)
        A = imm(cost, n, m)
        if max(ell(cost, A, n)) > 1:
            fail['IMM'] += 1
            ex.setdefault('IMM', (cost, A))
    print(f'  n={n} m={m} trials={trials}: ' +
          '  '.join(f'{k}:{v}' for k, v in fail.items()))
    return ex


if __name__ == '__main__':
    print('=== failures out of trials (0 = rule survived every instance) ===')
    for (n, m, t, s) in [(3, 3, 400, 21), (3, 4, 250, 22), (3, 5, 120, 23),
                         (4, 3, 200, 24), (4, 4, 80, 25)]:
        run(n, m, t, s)
