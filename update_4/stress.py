"""random stress test: is a legal TYPE-ORDERED peel schedule always available?"""
import itertools, random, sys
from typeorder import Chores, type_ordered_search, free_search


def random_dichotomous(m, rng):
    """random monotone c with c(empty)=0 and all marginals in {0,1}"""
    c = {frozenset(): 0}
    for r in range(1, m + 1):
        for S in itertools.combinations(range(m), r):
            S = frozenset(S)
            lo = max(c[S - {b}] for b in S)
            hi = min(c[S - {b}] + 1 for b in S)
            c[S] = rng.randint(lo, hi)
    return lambda S: c[frozenset(S)]


def run(n, m, trials, seed=0):
    rng = random.Random(seed)
    bad_free = bad_ord = bad_arg = 0
    for _ in range(trials):
        cost = [random_dichotomous(m, rng) for _ in range(n)]
        inst = Chores(n, m, cost, f'random n={n} m={m}')
        f = free_search(inst)
        o, _ = type_ordered_search(inst)
        a, _ = type_ordered_search(inst, restrict_argmax=True)
        if f is None:
            bad_free += 1
        if o is None:
            bad_ord += 1
        if a is None:
            bad_arg += 1
    print(f'  n={n} m={m}  trials={trials}:  '
          f'no legal schedule at all: {bad_free};  '
          f'no TYPE-ORDERED schedule: {bad_ord};  '
          f'no type-ordered+argmax: {bad_arg}')


if __name__ == '__main__':
    print('=== randomised stress test, type-ordered peel schedules ===')
    run(3, 2, 300, 1)
    run(3, 3, 300, 2)
    run(3, 4, 150, 3)
    run(4, 3, 100, 4)
    run(4, 4, 40, 5)
