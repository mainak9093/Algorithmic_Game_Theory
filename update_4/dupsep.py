"""
dupsep.py  --  verification for PS1_note_weighted_penalty_no_go.md  (v1, 2026-08-03)

Question.  After the replica transform (approach_3.tex), can the coverage constraint
"no bundle holds two copies of one type" be enforced by RE-WEIGHTING the replica items,
so that R3 [Barman-Krishna-Narahari-Sadhukhan 2022] can be applied as a black box?

A candidate reweighting is u = (u_1,...,u_n) on the replica item set Mhat with
  (D) each u_i dichotomous:  u_i(empty)=0, monotone, all marginals in {0,1}
  (F) faithful:              u_i(S) = vhat_i(S) for every duplicate-free S
u SEPARATES if every non-coverage allocation B has max_i l^u_B(i) >= 2.
If some faithful u separates, Conjecture 2 follows for that instance (Observation W0).

Result: no such u exists, already for n=3, m=2, c_i = |.|  -- and not even if (F) is
dropped.  Runs in a few seconds, exhaustive, no heuristics.

Usage:  python3 dupsep.py           main verification (Theorems W3, W4, W4')
        python3 dupsep.py pfamily   the separable P-family sweeps
"""
import itertools
import sys

INF = float('inf')


# --------------------------------------------------------------------------- #
#  instance / replica                                                          #
# --------------------------------------------------------------------------- #
class Inst:
    """negative dichotomous chore instance + its replica (n-1 copies per chore)"""

    def __init__(self, n, m, cost, name=''):
        self.n, self.m, self.cost, self.name = n, m, cost, name
        self.copies = [(j, r) for j in range(m) for r in range(n - 1)]
        self.K = len(self.copies)
        self.full = frozenset(range(m))
        self.cM = [cost[i](self.full) for i in range(n)]
        self.check_cost()

    def check_cost(self):
        for i in range(self.n):
            c = self.cost[i]
            assert c(frozenset()) == 0, 'cost not normalised'
            for r in range(self.m + 1):
                for S in itertools.combinations(range(self.m), r):
                    S = frozenset(S)
                    for j in set(range(self.m)) - S:
                        assert c(S | {j}) - c(S) in (0, 1), 'marginal not in {0,1}'

    def tau(self, S):
        return frozenset(self.copies[b][0] for b in range(self.K) if S >> b & 1)

    def vhat(self, i, S):
        return self.cM[i] - self.cost[i](self.full - self.tau(S))

    def dupfree(self, S):
        seen = set()
        for b in range(self.K):
            if S >> b & 1:
                j = self.copies[b][0]
                if j in seen:
                    return False
                seen.add(j)
        return True

    def d(self, S):
        return bin(S).count('1') - len(self.tau(S))

    def allocations(self):
        for a in itertools.product(range(self.n), repeat=self.K):
            B = [0] * self.n
            for b, ag in enumerate(a):
                B[ag] |= 1 << b
            yield B

    def coverage(self, B):
        return all(self.dupfree(S) for S in B)

    def show(self, B):
        return [('{' + ','.join(f'b{self.copies[b][0]+1}^{self.copies[b][1]+1}'
                                for b in range(self.K) if S >> b & 1) + '}') for S in B]


def unit(n, m):
    return Inst(n, m, [lambda S: len(S)] * n, f'unit n={n} m={m}')


def witness():
    return Inst(3, 3, [lambda S: max(0, len(S) - 1), lambda S: len(S), lambda S: len(S)],
                'obstruction witness n=3 m=3')


# --------------------------------------------------------------------------- #
#  envy graph                                                                  #
# --------------------------------------------------------------------------- #
def path_weights(W, n):
    """longest-path weight out of each vertex; [INF]*n if a positive cycle exists"""
    p = [0] * n
    for _ in range(n):
        q = p[:]
        for i in range(n):
            for k in range(n):
                if i != k and W[i][k] + p[k] > q[i]:
                    q[i] = W[i][k] + p[k]
        p = q
    p2 = p[:]
    for i in range(n):
        for k in range(n):
            if i != k and W[i][k] + p[k] > p2[i]:
                p2[i] = W[i][k] + p[k]
    return [INF] * n if p2 != p else p


def graph(us, B, n):
    return [[us[i][B[k]] - us[i][B[i]] for k in range(n)] for i in range(n)]


def excluded(us, B, n):
    return max(path_weights(graph(us, B, n), n)) >= 2


def separates(inst, us, noncov):
    for B in noncov:
        if not excluded(us, B, inst.n):
            return False, B
    return True, None


# --------------------------------------------------------------------------- #
#  reweighting families                                                        #
# --------------------------------------------------------------------------- #
def enumerate_dichotomous(inst, i=None, faithful=True):
    """all dichotomous u on Mhat; if faithful, pinned to vhat_i on duplicate-free sets"""
    K = inst.K
    order = sorted(range(1 << K), key=lambda S: bin(S).count('1'))
    vh = [inst.vhat(i, S) for S in range(1 << K)] if faithful else None
    out, u = [], {}

    def rec(t):
        if t == len(order):
            out.append([u[S] for S in range(1 << K)])
            return
        S = order[t]
        if S == 0:
            cands = [0]
        elif faithful and inst.dupfree(S):
            cands = [vh[S]]
        else:
            lo = max(u[S ^ (1 << b)] for b in range(K) if S >> b & 1)
            hi = min(u[S ^ (1 << b)] + 1 for b in range(K) if S >> b & 1)
            cands = range(lo, hi + 1)
        for v in cands:
            if all(v - u[S ^ (1 << b)] in (0, 1) for b in range(K) if S >> b & 1):
                u[S] = v
                rec(t + 1)
                del u[S]

    rec(0)
    return out


def P_family(inst, i, P):
    """u_i = vhat_i + (number of duplicate copies whose type lies in P)"""
    u = []
    for S in range(1 << inst.K):
        cnt = {}
        for b in range(inst.K):
            if S >> b & 1:
                cnt[inst.copies[b][0]] = cnt.get(inst.copies[b][0], 0) + 1
        u.append(inst.vhat(i, S) + sum(max(0, c - 1) for j, c in cnt.items() if j in P))
    return u


# --------------------------------------------------------------------------- #
#  the checks                                                                  #
# --------------------------------------------------------------------------- #
def theorem_W3():
    print('--- Theorem W3(3): the uniform maximal penalty u = vhat + d is blind ---')
    inst = unit(3, 3)
    us = [P_family(inst, i, set(range(inst.m))) for i in range(3)]
    B = [0, 0, 0]
    for j in range(3):                       # agent j gets both copies of type j
        for r in range(2):
            B[j] |= 1 << inst.copies.index((j, r))
    W = graph(us, B, 3)
    print('   B =', inst.show(B))
    print('   coverage?', inst.coverage(B), '   arcs', W, '  l =', path_weights(W, 3))
    assert not inst.coverage(B) and max(path_weights(W, 3)) == 0
    print('   => non-coverage yet zero subsidy under the strongest uniform penalty.\n')


def theorem_W4_table():
    print('--- Theorem W4: on n=3,m=2 unit costs the whole freedom is delta in {0,1}^3 ---')
    inst = unit(3, 2)
    D = sum(1 << inst.copies.index((0, r)) for r in range(2))
    s = [1 << inst.copies.index((1, r)) for r in range(2)]
    for delta in itertools.product([0, 1], repeat=3):
        res = []
        for x in range(3):
            y, z = [k for k in range(3) if k != x]
            B = [0, 0, 0]
            B[x], B[y], B[z] = D, s[0], s[1]
            us = [[0] * (1 << inst.K) for _ in range(3)]
            for i in range(3):
                us[i][D] = 1 + delta[i]
                us[i][s[0]] = us[i][s[1]] = 1
            res.append('excl' if excluded(us, B, 3) else 'SURVIVES')
        print(f'   delta={delta}  B^(1),B^(2),B^(3): {res}')
        assert 'SURVIVES' in res, 'a delta separated the family!'
    print('   => every delta leaves some B^(x) alive.  No faithful u separates.\n')


def theorem_W4_prime():
    print("--- Theorem W4': exhaustive, faithfulness DROPPED ---")
    inst = unit(3, 2)
    allU = enumerate_dichotomous(inst, faithful=False)
    allocs = list(inst.allocations())
    noncov = [B for B in allocs if not inst.coverage(B)]
    crit = [B for B in noncov if sorted(bin(S).count('1') for S in B) == [1, 1, 2]]
    print(f'   dichotomous valuations on the {inst.K} copies: {len(allU)}'
          f'   ({len(allU)}^3 = {len(allU)**3} triples)')
    print(f'   non-coverage allocations: {len(noncov)};  critical family: {len(crit)}')

    sig = {}
    for U in allU:
        k = tuple(tuple(U[B[kk]] - U[B[i]] for kk in range(3)) for B in crit for i in range(3))
        sig.setdefault(k, 0)
        sig[k] += 1
    G = list(sig)
    print(f'   behaviour classes on the critical family: {len(G)}')

    surv = 0
    for a in range(len(G)):
        for b in range(len(G)):
            for c in range(len(G)):
                if all(max(path_weights([G[a][3 * t], G[b][3 * t + 1], G[c][3 * t + 2]], 3)) >= 2
                       for t in range(len(crit))):
                    surv += 1
    print(f'   class-triples surviving the critical filter: {surv}')
    assert surv == 0
    print('   => NO dichotomous reweighting separates, faithful or not.\n')


def conjecture_still_holds():
    print('--- sanity: the instance is not a counterexample to Conjecture 2 ---')
    inst = unit(3, 2)
    base = [[inst.vhat(i, S) for S in range(1 << inst.K)] for i in range(3)]
    best = None
    for B in inst.allocations():
        if not inst.coverage(B):
            continue
        p = path_weights(graph(base, B, 3), 3)
        if max(p) <= 1 and (best is None or sum(p) < sum(best[1])):
            best = (B, p)
    print('   best coverage allocation', inst.show(best[0]), ' l =', best[1],
          ' total =', sum(best[1]), '= n-1\n')


def pfamily():
    print('--- the separable P-family (for n=3 this is every separable penalty) ---')
    for inst in (unit(3, 2), unit(3, 3), witness()):
        allocs = list(inst.allocations())
        noncov = [B for B in allocs if not inst.coverage(B)]
        subsets = [frozenset(s) for r in range(inst.m + 1)
                   for s in itertools.combinations(range(inst.m), r)]
        hit = None
        for Ps in itertools.product(subsets, repeat=inst.n):
            us = [P_family(inst, i, Ps[i]) for i in range(inst.n)]
            ok, _ = separates(inst, us, noncov)
            if ok:
                hit = Ps
                break
        print(f'   {inst.name:28s}  {len(subsets)**inst.n:5d} triples  '
              f'separating: {hit if hit else "NONE"}')
    print()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'pfamily':
        pfamily()
    else:
        theorem_W3()
        theorem_W4_table()
        theorem_W4_prime()
        conjecture_still_holds()
        print('all assertions passed.')
