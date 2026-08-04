"""Is monotonicity of c_i enough for the replica dual v-hat to be dichotomous?

Answer: NO.  Monotonicity of c_i buys monotonicity of v-hat and nothing else.
The marginals of v-hat are DOWNWARD marginals of c_i,

    v-hat(S + b) - v-hat(S) = c(T) - c(T - {j}),   T = M \\ tau(S),

so they lie in {0,1} exactly when c_i's own marginals do.  Monotonicity alone
gives only ">= 0".

Also checks the redundancy: marginals in {0,1} already IMPLIES monotone, so the
three-part hypothesis is really two.

Run:  python monotone_check.py
"""
from itertools import combinations, product


def subsets(m):
    return [frozenset(s) for k in range(m + 1) for s in combinations(range(m), k)]


def is_monotone(m, c):
    for S in subsets(m):
        for g in range(m):
            if g not in S and c[S | {g}] < c[S]:
                return False
    return True


def marginals_in_01(m, c):
    for S in subsets(m):
        for g in range(m):
            if g not in S and c[S | {g}] - c[S] not in (0, 1):
                return False
    return True


def vhat(m, c):
    """The replica dual, as a function of the TYPE SET tau(S)."""
    univ = frozenset(range(m))
    return {T: c[univ] - c[univ - T] for T in subsets(m)}


def report(name, m, c):
    mono = is_monotone(m, c)
    dich = mono and c[frozenset()] == 0 and marginals_in_01(m, c)
    V = vhat(m, c)
    vmono = all(V[T] <= V[T | {g}] for T in subsets(m) for g in range(m) if g not in T)
    vmarg = all(V[T | {g}] - V[T] in (0, 1)
                for T in subsets(m) for g in range(m) if g not in T)
    bad = [(sorted(T), g, V[T | {g}] - V[T])
           for T in subsets(m) for g in range(m)
           if g not in T and V[T | {g}] - V[T] not in (0, 1)]
    print("  %-28s c monotone=%-5s c dichotomous=%-5s ||  vhat monotone=%-5s "
          "vhat marginals in {0,1}=%s" % (name, mono, dich, vmono, vmarg))
    if bad:
        T, g, d = bad[0]
        print("        offending vhat marginal: tau=%s, add type %d  ->  %+d"
              % (T, g, d))


def main():
    m = 2
    U = frozenset(range(m))

    print("=== monotone but NOT dichotomous (one marginal equal to 2) ===")
    c = {frozenset(): 0, frozenset({0}): 0, frozenset({1}): 0, U: 2}
    report("c(ab)=2, c(a)=c(b)=0", m, c)

    print("\n=== monotone, marginals in {0,1}, but c(empty) != 0 ===")
    c2 = {frozenset(): 1, frozenset({0}): 1, frozenset({1}): 1, U: 2}
    report("c(empty)=1", m, c2)

    print("\n=== genuinely dichotomous, for contrast ===")
    for name, f in [("c(S)=|S|", lambda S: len(S)),
                    ("c(S)=max(0,|S|-1)", lambda S: max(0, len(S) - 1)),
                    ("c(S)=min(|S|,1)", lambda S: min(len(S), 1))]:
        report(name, m, {S: f(S) for S in subsets(m)})

    print("\n=== redundancy: does 'marginals in {0,1}' already imply monotone? ===")
    # exhaustive over all integer functions on 2^[3] with marginals in {0,1}
    m = 3
    subs = subsets(m)
    cnt = viol = 0
    for vals in product(range(0, 4), repeat=len(subs)):
        c = dict(zip(subs, vals))
        if c[frozenset()] != 0:
            continue
        if not marginals_in_01(m, c):
            continue
        cnt += 1
        if not is_monotone(m, c):
            viol += 1
    print("  functions on 2^[3] with c(empty)=0 and all marginals in {0,1} : %d" % cnt)
    print("  of those, NOT monotone                                        : %d" % viol)
    print("  => 'monotone' is implied, so the hypothesis has two real parts,")
    print("     not three.")


if __name__ == "__main__":
    main()
