import itertools, random
from guidedR3 import extend_options, M_of_p, compute_p

def random_dichotomous(m, rng):
    c = {frozenset(): 0}
    for r in range(1, m + 1):
        for S in itertools.combinations(range(m), r):
            S = frozenset(S)
            lo = max(c[S - {b}] for b in S)
            hi = min(c[S - {b}] + 1 for b in S)
            c[S] = rng.randint(lo, hi)
    return c

n, m = 3, 5
rng = random.Random(1)
for t in range(400):
    v = [random_dichotomous(m, rng) for _ in range(n)]
    items = list(range(m)); rng.shuffle(items)
    A = [frozenset() for _ in range(n)]; p = [0]*n
    for step, g in enumerate(items[:-1]):
        opts = extend_options(v, A, p, g, n)
        if not opts: break
        sizes = [len(b) for b in A]; min_size = min(sizes)
        opts_to_min = [(rho,kk) for (rho,kk) in opts if len(A[rho[kk]])==min_size]
        if not opts_to_min and any(len(b)!=sizes[0] for b in A) and t==1 and step==2:
            print("FOUND trial 1 step 2")
            print("v (item -> marginal contribution table, per agent):")
            for i in range(n):
                print(f"  agent {i}:")
                for S in sorted(v[i], key=lambda x:(len(x),sorted(x))):
                    print(f"    v_{i}({sorted(S)}) = {v[i][S]}")
            print("A (bundles before this step):", [sorted(b) for b in A])
            print("p (before):", p)
            print("item being inserted g =", g, " remaining order:", items)
            print("all EXTEND options (rho,k):")
            for rho,kk in opts:
                print(f"   agent {kk} grows bundle currently={sorted(A[rho[kk]])} (size {len(A[rho[kk]])}); rho={rho}")
            raise SystemExit
        rho,kk = rng.choice(opts)
        A = [A[rho[i]] for i in range(n)]; A[kk]=A[kk]|{g}; p=compute_p(v,A,n)
