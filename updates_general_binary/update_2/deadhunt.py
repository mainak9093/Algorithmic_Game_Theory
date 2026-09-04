"""
Hunting a genuine DEAD STATE in the negative dichotomous class.

deadstate.py shows the handcrafted instance has none: every valid partial
allocation of it can be completed, so it does not break BKNS's inductive
architecture. What WOULD break that architecture, independently of which agent
any mirrored rule picks, is a state witnessing the failure of

    INV  every envy-freeable partial allocation with subsidies in {0,1}^n can
         absorb one more chore -- into some bundle, after any reassignment of
         the bundles -- and still have subsidies in {0,1}^n.

For goods INV is a theorem (BKNS Case I plus Lemma 11), and it is the engine of
the whole proof. A negative dichotomous instance in which INV fails therefore
shows the mirror cannot work, whatever rule is used.

Two strengths are searched for, since they say different things:

    STUCK  a valid partial state and a chore g such that inserting g into any
           bundle, under any reassignment, leaves subsidies above 1 -- the
           direct failure of INV;
    DEAD   a valid partial state with NO valid completion at all -- strictly
           worse, since no ordering of the remaining chores rescues it.

Reassignment is allowed throughout, exactly as BKNS's Case I allows it; leaving
it out is what made the first version of this test report a false failure.
"""
import itertools
import random
import sys

from gb_valuations import enumerate_class

N = 3
PERM = list(itertools.permutations(range(N)))


def subsidy(cs, X):
    base = sum(cs[i][X[i]] for i in range(N))       # cs are valuations (<=0)
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


def good_multiset(cs, b):
    return any(valid(cs, tuple(b[p[i]] for i in range(N))) for p in PERM)


def completions(X, left):
    if not left:
        yield X
        return
    g, rest = left[0], left[1:]
    for s in range(N):
        nb = list(X)
        nb[s] |= 1 << g
        yield from completions(tuple(nb), rest)


def analyse(cs, m):
    stuck, dead = None, None
    for o in itertools.product(list(range(N)) + [None], repeat=m):
        b = [0] * N
        left = []
        for k, i in enumerate(o):
            if i is None:
                left.append(k)
            else:
                b[i] |= 1 << k
        X = tuple(b)
        if not left or not valid(cs, X):
            continue
        if stuck is None:
            for g in left:
                if not any(good_multiset(cs, [X[t] | ((1 << g) if t == s else 0)
                                              for t in range(N)])
                           for s in range(N)):
                    stuck = (X, g)
                    break
        if dead is None:
            if not any(good_multiset(cs, list(Z))
                       for Z in completions(X, tuple(left))):
                dead = (X, tuple(left))
        if stuck and dead:
            break
    return stuck, dead


def show(m, S):
    return "{" + ",".join("abcdef"[k] for k in range(m) if S & (1 << k)) + "}"


def main():
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
    rng = random.Random(20260929)
    pool = enumerate_class(m, {-1, 0})
    print("negative dichotomous valuations on m=%d: %d ; sampling %d triples"
          % (m, len(pool), trials))

    nstuck = ndead = 0
    first_stuck = first_dead = None
    for _ in range(trials):
        cs = [rng.choice(pool) for _ in range(N)]
        st, dd = analyse(cs, m)
        if st:
            nstuck += 1
            if first_stuck is None:
                first_stuck = (cs, st)
        if dd:
            ndead += 1
            if first_dead is None:
                first_dead = (cs, dd)

    print()
    print("instances with a STUCK state (INV fails)     : %d / %d" % (nstuck, trials))
    print("instances with a DEAD state (no completion)  : %d / %d" % (ndead, trials))
    for tag, item in (("STUCK", first_stuck), ("DEAD", first_dead)):
        if item is None:
            continue
        cs, w = item
        print()
        print("  first %s witness" % tag)
        for i in range(N):
            print("     agent %d costs by subset: %s"
                  % (i + 1, [-cs[i][S] for S in range(1 << m)]))
        if tag == "STUCK":
            X, g = w
            print("     state %s   chore %s unallocated   subsidy %s"
                  % ([show(m, x) for x in X], "abcdef"[g], subsidy(cs, X)))
        else:
            X, left = w
            print("     state %s   left %s   subsidy %s"
                  % ([show(m, x) for x in X],
                     [ "abcdef"[g] for g in left], subsidy(cs, X)))


if __name__ == "__main__":
    main()
