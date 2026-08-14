import itertools
from test_permuted_extension import permuted_extension_works, full_ef_exists

def mk_cost(trigger):
    c = {}
    for r in range(5):
        for S in itertools.combinations(range(4), r):
            S = frozenset(S)
            c[S] = 1 if trigger <= S else 0
    return c

c1 = mk_cost(frozenset({0,3}))
c2 = mk_cost(frozenset({1,3}))
c3 = mk_cost(frozenset({2,3}))
costs = [c1,c2,c3]

X = [frozenset({0}), frozenset({1}), frozenset({2})]
R = frozenset({3})
works, Yf, perm, p = permuted_extension_works(costs, X, R, 4)
print("permuted extension works on THIS specific X,R:", works, Yf, perm, p)
