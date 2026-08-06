"""The peel reachability sweep: the decisive experiment Approach 3 never ran.

conj:h1prime (Reachability) says: from the root, some sequence of peels and
permutations reaches a TERMINAL state with the legality invariant holding at
every intermediate state.  It implies Conjecture 2, since a terminal state's
graph is the induced allocation's envy graph.

The state space is small enough to settle exhaustively at n = m = 3.  A state is
a workload profile W = (W_1,...,W_n) with W_i a subset of the items and every
owner-candidate set S_j = {i : j in W_i} nonempty, so there are at most
(2^m)^n = 512 profiles.  Per def:peel:

    root       W_i = all items for every i          (graph identically zero)
    peel(x,j)  legal iff j in W_x and |S_j| >= 2;  removes j from W_x
    permute    relabel the profile by any sigma
    terminal   |S_j| = 1 for every j
    legal      no positive cycle, and ell_W(i) <= 1 for all i,
               where w_W(i,k) = c_i(W_i) - c_i(W_k)

The sweep does a full reachability search over LEGAL states only, from the root,
and asks whether any legal terminal state is reachable.  An instance where none
is -- a "bad root" -- refutes conj:h1prime and kills Approach 3.  Per
rem:converse it would NOT refute Conjecture 2, which asserts only that a good
terminal EXISTS, not that it is reachable through legal states; so both are
recorded separately here, and the gap between them is the interesting number.

Run over the full exhaustive n = m = 3 dichotomous family (9,880 instances).

Run:  python peel_sweep.py
"""
from itertools import combinations_with_replacement, permutations, product
from collections import Counter, deque
import sys

sys.path.insert(0, "../update_6")
from targetGbal import gen_functions                      # noqa: E402

M = 3
FULL = frozenset(range(M))


def ell(cs, W, n):
    """Longest-path vector for the state graph; None if a positive cycle."""
    a = [[cs[i][W[k]] for k in range(n)] for i in range(n)]
    Wt = [[a[i][i] - a[i][k] for k in range(n)] for i in range(n)]
    e = [0] * n
    for _ in range(n + 1):
        ch = False
        new = list(e)
        for i in range(n):
            for k in range(n):
                if i != k and Wt[i][k] + e[k] > new[i]:
                    new[i] = Wt[i][k] + e[k]; ch = True
        e = new
        if not ch:
            return e
    return None


def legal(cs, W, n):
    e = ell(cs, W, n)
    return e is not None and max(e) <= 1


def cand(W, n):
    return [frozenset(i for i in range(n) if j in W[i]) for j in range(M)]


def terminal(W, n):
    return all(len(s) == 1 for s in cand(W, n))


def reachable_terminal(cs, n):
    """BFS over legal states from the root; True if a legal terminal is reached."""
    root = tuple([FULL] * n)
    if not legal(cs, root, n):
        return False, 0
    seen = {root}
    q = deque([root])
    perms = list(permutations(range(n)))
    while q:
        W = q.popleft()
        if terminal(W, n):
            return True, len(seen)
        S = cand(W, n)
        nxt = []
        for x in range(n):
            for j in W[x]:
                if len(S[j]) >= 2:
                    nw = list(W)
                    nw[x] = W[x] - {j}
                    nxt.append(tuple(nw))
        for p in perms:
            nxt.append(tuple(W[p[i]] for i in range(n)))
        for s in nxt:
            if s not in seen and legal(cs, s, n):
                seen.add(s)
                q.append(s)
    return False, len(seen)


def conj2_holds(cs, n):
    """Does a good allocation exist at all (Conjecture 2 for this instance)?"""
    for assign in product(range(n), repeat=M):
        bd = tuple(frozenset(g for g in range(M) if assign[g] == i)
                   for i in range(n))
        e = ell(cs, bd, n)
        if e is not None and max(e) <= 1:
            return True
    return False


def main():
    n = 3
    F = gen_functions(M)
    tot = badroot = noconj2 = 0
    seen_hist = Counter()
    gap = []
    print("=== peel reachability sweep, full n = m = 3 family ===")
    for cs in combinations_with_replacement(F, n):
        tot += 1
        ok, nstates = reachable_terminal(list(cs), n)
        seen_hist[nstates // 25 * 25] += 1
        if not ok:
            badroot += 1
            c2 = conj2_holds(list(cs), n)
            if not c2:
                noconj2 += 1
            else:
                gap.append(cs)
    print("  instances                                   : %d" % tot)
    print("  BAD ROOTS (no legal schedule to a terminal) : %d" % badroot)
    print("  of those, Conjecture 2 also fails           : %d" % noconj2)
    print("  of those, Conjecture 2 HOLDS (the gap)      : %d" % len(gap))
    print()
    if badroot == 0:
        print("  *** conj:h1prime SURVIVES the full n=m=3 family.  Approach 3 is")
        print("      not refuted, and the peel frame reaches a good allocation")
        print("      from the root through legal states on every instance. ***")
    else:
        print("  *** conj:h1prime is REFUTED: %d bad roots. ***" % badroot)
        if gap:
            print("      On %d of them a good allocation EXISTS but is unreachable"
                  % len(gap))
            print("      through legal states -- rem:converse's gap is real, and")
            print("      Approach 3 is strictly weaker than Conjecture 2.")
            cs = gap[0]
            print()
            print("      first witness, singleton costs c_i({g}):")
            for i, c in enumerate(cs):
                print("        agent %d: %s   (grand bundle %d)"
                      % (i, [c[frozenset({g})] for g in range(M)], c[FULL]))
        if noconj2:
            print("      %d bad roots are instances where Conjecture 2 itself fails"
                  % noconj2)
            print("      -- which would be a COUNTEREXAMPLE and must be checked.")


if __name__ == "__main__":
    main()
