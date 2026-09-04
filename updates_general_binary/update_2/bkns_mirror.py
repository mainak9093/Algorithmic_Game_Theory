"""
Checking the handcrafted instance against what BKNS's algorithm actually does.

BKNS (arXiv:2201.07419) Algorithm 1 maintains an envy-free solution (A,p) with
p in {0,1}^n and inserts one good per iteration, so its whole proof rests on
the invariant

    INV  every envy-freeable partial allocation with subsidies in {0,1}^n can
         absorb one more item -- into some bundle, after some reassignment of
         the bundles -- and still have subsidies in {0,1}^n.

For goods that invariant is a theorem: Case I handles extendable states and
Lemma 11 handles the rest. A negative dichotomous instance in which INV FAILS
therefore breaks the architecture regardless of which agent the mirrored rule
would pick, which is stronger and cleaner than tracking a particular run.

The instance under test, from the handwritten note. Six chores
a1,a2,a3,c and b1,b2, three agents:

    agents 1 and 2 :  c_i(S) = |S n {a1,a2,a3,c}|          (b's always free)
    agent 3        :  c_3(S) = |S n {a1,a2,a3,c}| + [ |S n {b1,b2}| = 2 ]

so the a's and c are unit chores for everyone, a single b is free for everyone,
and only the PAIR of b's costs anything, and only to agent 3.

Reported: legality of the instance, the cost table, whether a valid complete
allocation exists, and -- the point -- every valid partial state with one chore
left from which no insertion plus reassignment stays valid.
"""
import itertools

N, MITEMS = 3, 6
A1, A2, A3, C, B1, B2 = 0, 1, 2, 3, 4, 5
NAMES = ["a1", "a2", "a3", "c", "b1", "b2"]
UNIT = {A1, A2, A3, C}
BS = {B1, B2}


def cost(i, S):
    units = sum(1 for k in UNIT if S & (1 << k))
    if i == 2:
        both = 1 if all(S & (1 << k) for k in BS) else 0
        return units + both
    return units


def legal():
    for i in range(N):
        if cost(i, 0) != 0:
            return False, "c_%d(empty) != 0" % i
        for S in range(1 << MITEMS):
            for k in range(MITEMS):
                if not S & (1 << k):
                    d = cost(i, S | (1 << k)) - cost(i, S)
                    if d not in (0, 1):
                        return False, "marginal %d for agent %d" % (d, i)
    return True, "all marginals in {0,1}, c_i(empty)=0"


def show(S):
    return "{" + ",".join(NAMES[k] for k in range(MITEMS) if S & (1 << k)) + "}"


def envy_freeable(X):
    base = sum(-cost(i, X[i]) for i in range(N))
    for p in itertools.permutations(range(N)):
        if sum(-cost(i, X[p[i]]) for i in range(N)) > base:
            return False
    return True


def subsidy(X):
    """Minimum subsidy vector, or None if not envy-freeable."""
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


def good_multiset(bundles):
    """Some assignment of these bundles to agents is valid."""
    return any(valid(tuple(bundles[p[i]] for i in range(N)))
               for p in itertools.permutations(range(N)))


def main():
    ok, why = legal()
    print("INSTANCE LEGAL: %s  (%s)" % (ok, why))
    print()
    print("cost table for the bundles named in the note:")
    hdr = [("{a1,a3}", (1 << A1) | (1 << A3)),
           ("{a2}", 1 << A2),
           ("{b1,b2}", (1 << B1) | (1 << B2)),
           ("{b1,b2,c}", (1 << B1) | (1 << B2) | (1 << C))]
    print("   agent | " + " | ".join("%-9s" % h[0] for h in hdr))
    for i in range(N):
        print("     %d    | " % (i + 1)
              + " | ".join("%-9d" % cost(i, h[1]) for h in hdr))

    # does a valid COMPLETE allocation exist?
    full = (1 << MITEMS) - 1
    comp = []
    for o in itertools.product(range(N), repeat=MITEMS):
        b = [0] * N
        for k, i in enumerate(o):
            b[i] |= 1 << k
        comp.append(tuple(b))
    good = [X for X in comp if valid(X)]
    print()
    print("valid COMPLETE allocations: %d of %d" % (len(good), len(comp)))
    if good:
        X = good[0]
        print("   e.g. %s   subsidy %s"
              % ([show(x) for x in X], subsidy(X)))

    # dead ends: valid partial state, one chore left, no insertion works
    print()
    print("DEAD ENDS -- valid partial states with ONE chore unallocated from")
    print("which no insertion into any bundle, under any reassignment, stays valid:")
    found = 0
    for o in itertools.product(list(range(N)) + [None], repeat=MITEMS):
        if sum(1 for x in o if x is None) != 1:
            continue
        b = [0] * N
        g = None
        for k, i in enumerate(o):
            if i is None:
                g = k
            else:
                b[i] |= 1 << k
        X = tuple(b)
        if not valid(X):
            continue
        rescue = False
        for s in range(N):
            nb = list(X)
            nb[s] |= 1 << g
            if good_multiset(nb):
                rescue = True
                break
        if not rescue:
            found += 1
            if found <= 4:
                print("   state %s  unallocated %s  subsidy %s"
                      % ([show(x) for x in X], NAMES[g], subsidy(X)))
    print("   total dead ends of this shape: %d" % found)


if __name__ == "__main__":
    main()
