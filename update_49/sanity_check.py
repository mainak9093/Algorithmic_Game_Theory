import itertools
from test_permuted_extension import find_ef_partial, permuted_extension_works, full_ef_exists

# ground set: a=0,b=1,c=2,e=3
def mk_cost(trigger):
    c = {}
    for r in range(5):
        for S in itertools.combinations(range(4), r):
            S = frozenset(S)
            c[S] = 1 if trigger <= S else 0
    return c

c1 = mk_cost(frozenset({0,3}))  # {a,e}
c2 = mk_cost(frozenset({1,3}))  # {b,e}
c3 = mk_cost(frozenset({2,3}))  # {c,e}
costs = [c1,c2,c3]

X, R = find_ef_partial(costs, 4, max_leftover=2)
print("partial:", X, "leftover:", R)
works, Yf, perm, p = permuted_extension_works(costs, X, R, 4)
print("permuted extension works:", works, Yf, perm, p)

gt, Xg, pg = full_ef_exists(costs, 4)
print("ground truth:", gt, Xg, pg)
