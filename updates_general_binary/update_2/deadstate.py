"""
Where does the mirror actually break on this instance?

bkns_mirror.py finds no state with one chore left that cannot absorb it, and
288 of 729 complete allocations are valid, so the instance is nowhere near a
counterexample to the theorem. Three sharper questions:

  Q1  Are there DEAD states -- valid partial allocations no completion of which
      is valid? Those would break the inductive architecture outright.

  Q2  What does BKNS's rule literally do? Its Case I requires the recipient to
      be in M(q), the set of MOST-subsidised agents, and its Lemma 9 shows
      FINDSINK only ever considers agents in M(p). Mirroring the sign but
      keeping "most subsidised" should fail immediately, since handing a chore
      to the most-subsidised agent is exactly the wrong move.

  Q3  What about the PROPERLY mirrored rule, which gives the chore to a LEAST
      subsidised agent for whom it is free? That is the version worth
      exhibiting a failure for, since the naive one is a straw man.

Each is answered by direct computation on the instance of the handwritten note.
"""
import itertools

N, MITEMS = 3, 6
A1, A2, A3, C, B1, B2 = 0, 1, 2, 3, 4, 5
NAMES = ["a1", "a2", "a3", "c", "b1", "b2"]
UNIT = {A1, A2, A3, C}
BS = {B1, B2}


def cost(i, S):
    u = sum(1 for k in UNIT if S & (1 << k))
    if i == 2 and all(S & (1 << k) for k in BS):
        return u + 1
    return u


def show(S):
    return "{" + ",".join(NAMES[k] for k in range(MITEMS) if S & (1 << k)) + "}"


def subsidy(X):
    base = sum(-cost(i, X[i]) for i in range(N))
    for p in itertools.permutations(range(N)):
        if sum(-cost(i, X[p[i]]) for i in range(N)) > base:
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


def best_assign(bundles):
    """Valid assignment of these bundles, or None."""
    for p in itertools.permutations(range(N)):
        X = tuple(bundles[p[i]] for i in range(N))
        if valid(X):
            return X
    return None


def completions(X, left):
    if not left:
        yield X
        return
    g, rest = left[0], left[1:]
    for s in range(N):
        nb = list(X)
        nb[s] |= 1 << g
        yield from completions(tuple(nb), rest)


def main():
    print("Q1 -- dead states (valid, but no valid completion)")
    dead = 0
    ex = []
    for o in itertools.product(list(range(N)) + [None], repeat=MITEMS):
        b = [0] * N
        left = []
        for k, i in enumerate(o):
            if i is None:
                left.append(k)
            else:
                b[i] |= 1 << k
        X = tuple(b)
        if not left or not valid(X):
            continue
        if not any(valid(Z) for Z in completions(X, tuple(left))):
            dead += 1
            if len(ex) < 3:
                ex.append((X, left))
    print("   dead states found : %d" % dead)
    for X, left in ex:
        print("      %s  left=%s" % ([show(x) for x in X],
                                     [NAMES[g] for g in left]))
    if dead == 0:
        print("   -> every valid partial state of this instance can be completed,")
        print("      so the instance does NOT break the inductive architecture.")

    print()
    print("Q2 -- BKNS's rule mirrored literally (recipient in M(p), most subsidised)")
    X = (1 << A1, 0, 0)
    p = subsidy(X)
    print("   state %s   subsidy %s   M(p) = %s"
          % ([show(x) for x in X], p, [i + 1 for i in range(N)
                                       if p[i] == max(p)]))
    print("   next chore a2. Options:")
    for s in range(N):
        nb = list(X)
        nb[s] |= 1 << A2
        q = subsidy(tuple(nb))
        print("      to agent %d -> %s  subsidy %s%s"
              % (s + 1, [show(x) for x in nb], q,
                 "   <- the only agent in M(p)" if p[s] == max(p) else ""))
    print("   -> the sole most-subsidised agent forces subsidy 2, while both")
    print("      least-subsidised agents work. The 'most subsidised' half of")
    print("      BKNS's rule inverts under the sign flip.")

    print()
    print("Q3 -- the properly mirrored rule: free chore to a LEAST subsidised agent")
    order = [A1, A2, B1, B2, A3, C]
    X = (0, 0, 0)
    ok = True
    for g in order:
        p = subsidy(X)
        lo = [i for i in range(N) if p[i] == min(p)]
        pick = None
        for s in lo:                       # prefer a least-subsidised agent
            if cost(s, X[s] | (1 << g)) - cost(s, X[s]) == 0:
                pick = s
                break
        if pick is None:                   # else any least-subsidised agent
            cand = [s for s in lo
                    if (lambda q: q is not None and max(q) <= 1)(
                        subsidy(tuple(X[i] | ((1 << g) if i == s else 0)
                                      for i in range(N))))]
            pick = cand[0] if cand else None
        if pick is None:
            print("   STUCK at chore %s from state %s (subsidy %s)"
                  % (NAMES[g], [show(x) for x in X], p))
            ok = False
            break
        X = tuple(X[i] | ((1 << g) if i == pick else 0) for i in range(N))
        print("   %-3s -> agent %d   state %s   subsidy %s"
              % (NAMES[g], pick + 1, [show(x) for x in X], subsidy(X)))
    if ok:
        print("   -> the properly mirrored rule COMPLETES on this instance.")


if __name__ == "__main__":
    main()
