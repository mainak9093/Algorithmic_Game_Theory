"""
typeorder.py -- two independent checks on the 'type-ordered + weight-inflated FINDSINK' idea.

CHECK A (peel frame).  The proposal fixes an order of chores and finishes all n-1 copies
of b_j before starting b_{j+1}.  In the peel frame that is exactly: decide the owner of
a_1 first, then a_2, etc.  Coverage is automatic there, so the ONLY question is whether
the invariant (no positive cycle, l(i) <= 1) can be kept along such a schedule.
We search exhaustively over chore orders, over which n-1 agents get relieved in each
round, and over the order within each round.

CHECK B (replica frame).  Simulate R3's ALG (EXTEND then FINDSINK) on the replica
instance under the type-ordered good order and see whether FINDSINK produces duplicates.
"""
import itertools

INF = float('inf')


# ---------------- envy graph ----------------
def path_weights(W, n):
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


# ---------------- peel frame ----------------
class Chores:
    def __init__(self, n, m, cost, name=''):
        self.n, self.m, self.cost, self.name = n, m, cost, name

    def arcs(self, W):
        return [[self.cost[i](W[i]) - self.cost[i](W[k]) for k in range(self.n)]
                for i in range(self.n)]

    def ell(self, W):
        return path_weights(self.arcs(W), self.n)

    def legal(self, W):
        p = self.ell(W)
        return max(p) <= 1


def type_ordered_search(inst, restrict_argmax=False):
    """exists a legal schedule that finishes chore j_1, then j_2, ...?"""
    n, m = inst.n, inst.m
    root = tuple(frozenset(range(m)) for _ in range(n))
    for order in itertools.permutations(range(m)):
        stack = [(root, 0)]                      # (state, how many chores decided)
        seen = set()
        found = _round(inst, root, order, 0, restrict_argmax, seen)
        if found is not None:
            return order, found
    return None, None


def _round(inst, W, order, r, restrict_argmax, seen):
    n = inst.n
    if r == len(order):
        return []
    j = order[r]
    # relieve n-1 of the n agents of chore j, in some order
    for owner in range(n):                       # the agent NOT relieved
        others = [i for i in range(n) if i != owner]
        for seq in itertools.permutations(others):
            cur, moves, ok = W, [], True
            for x in seq:
                if restrict_argmax:
                    p = inst.ell(cur)
                    if p[x] < max(p):
                        ok = False
                        break
                nxt = list(cur)
                nxt[x] = nxt[x] - {j}
                cur = tuple(nxt)
                if not inst.legal(cur):
                    ok = False
                    break
                moves.append((x, j))
            if ok:
                key = (cur, r + 1)
                if key in seen:
                    continue
                rest = _round(inst, cur, order, r + 1, restrict_argmax, seen)
                if rest is not None:
                    return moves + rest
                seen.add(key)
    return None


def free_search(inst):
    """exists ANY legal peel schedule (no ordering constraint)?  BFS over states."""
    n, m = inst.n, inst.m
    root = tuple(frozenset(range(m)) for _ in range(n))
    from collections import deque
    seen, dq = {root}, deque([root])
    while dq:
        W = dq.popleft()
        if all(sum(1 for i in range(n) if j in W[i]) == 1 for j in range(m)):
            return W
        for x in range(n):
            for j in W[x]:
                if sum(1 for i in range(n) if j in W[i]) >= 2:
                    nxt = list(W)
                    nxt[x] = nxt[x] - {j}
                    nxt = tuple(nxt)
                    if nxt not in seen and inst.legal(nxt):
                        seen.add(nxt)
                        dq.append(nxt)
    return None


# ---------------- instances ----------------
def witness():
    return Chores(3, 3, [lambda S: max(0, len(S) - 1), lambda S: len(S), lambda S: len(S)],
                  'obstruction witness  c1=max(0,|S|-1), c2=c3=|S|')


def additive(n, m, T):
    """c_i(S) = |S ∩ T_i|  (binary additive chores)"""
    return Chores(n, m, [(lambda t: (lambda S: len(S & t)))(frozenset(T[i])) for i in range(n)],
                  'additive T=' + str([sorted(t) for t in T]))


if __name__ == '__main__':
    print('=== CHECK A: is a TYPE-ORDERED legal peel schedule available? ===\n')
    insts = [witness(),
             additive(3, 3, [{0, 1, 2}, {0, 1, 2}, {0, 1, 2}]),
             additive(3, 3, [{0}, {1}, {2}]),
             additive(3, 3, [{0, 1}, {1, 2}, {0, 2}])]
    for inst in insts:
        free = free_search(inst)
        order, sched = type_ordered_search(inst)
        oa, sa = type_ordered_search(inst, restrict_argmax=True)
        print(f'  {inst.name}')
        print(f'     some legal schedule exists (unordered): {free is not None}')
        print(f'     type-ordered legal schedule           : '
              f'{"YES order=" + str(order) if order else "NO"}')
        print(f'     type-ordered + argmax-recipient rule  : '
              f'{"YES order=" + str(oa) if oa else "NO"}')
        print()
