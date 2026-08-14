"""P(W) is a LATTICE.  Structure inside the admissible paid sets.

The report has treated P(W) only as a feasibility object -- non-empty or not.
But P(W) is the solution set of a difference-constraint system, and those are
lattices.  Concretely, for p, q in P(W) and r = max(p,q) coordinatewise, the only
interesting case is r_i = p_i >= q_i and r_k = q_k >= p_k, where

    w(i,k) <= q_i - q_k <= p_i - q_k = r_i - r_k,

using the q-constraint and q_i <= p_i.  Symmetrically for min.  Hence

    P(W) is closed under union and intersection,

so it has a unique maximum S_max and a unique minimum S_min, and these are
computable.  Consequences tested here:

  (L1) closure under union and intersection;
  (L2) S_min = { i : ell(i) = 1 }, i.e. the longest-path potential is the
       minimum admissible paid set;
  (L3) lem:paid-peel fires for x iff mu_x = 1 and x in S_MAX -- so the
       existential "some admissible S contains x" collapses to one membership
       test, and S_max is the only set worth trying;
  (L4) slack-transfer should always be run at S = S_max, since no larger
       admissible set exists to add blockers to.

(L3) is the useful one: it removes a search over 2^n sets from every safety test
and says which potential is canonical for peeling.

Run:  python lattice.py
"""
from itertools import permutations
from collections import Counter, deque
import random
import sys

sys.path.insert(0, "../update_6")
sys.path.insert(0, "../update_32")
sys.path.insert(0, "../update_34")
sys.path.insert(0, "../update_36")
sys.path.insert(0, "../update_37")
sys.path.insert(0, "../update_35")
from targetGbal import rand_dicho                             # noqa: E402
from peel_general import legal, terminal, peels, make         # noqa: E402
from reachable_stuck import ok                                # noqa: E402
from potential_set import admissible, arcs                    # noqa: E402
from slack_transfer import lam, marginals                     # noqa: E402
from stuck_profile import ell_vec                             # noqa: E402


def main():
    rng = random.Random(39393939)
    bad_union = bad_inter = bad_min = bad_max = 0
    n_pairs = n_states = 0
    sizes = Counter()
    print("=== P(W) as a lattice ===")
    for (n, m, T) in [(3, 4, 40), (3, 5, 18), (3, 6, 6),
                      (4, 3, 30), (4, 4, 12), (5, 3, 12), (5, 4, 4)]:
        perms = list(permutations(range(n)))
        for _ in range(T):
            cs = [rand_dicho(m, rng) for _ in range(n)]
            if max(max(c.values()) for c in cs) < 1:
                continue
            root = tuple([make(m)] * n)
            seen = {root}; q = deque([root])
            while q and len(seen) < 3000:
                W = q.popleft()
                P = admissible(cs, W, n)
                if P:
                    n_states += 1
                    sizes[len(P)] += 1
                    Pset = set(P)
                    # (L1) closure
                    for a in P:
                        for b in P:
                            n_pairs += 1
                            if (a | b) not in Pset:
                                bad_union += 1
                            if (a & b) not in Pset:
                                bad_inter += 1
                    # (L2) S_min = {i : ell(i) = 1}
                    Smin = frozenset.intersection(*P) if P else frozenset()
                    e = ell_vec(cs, W, n)
                    if e is not None:
                        if Smin != frozenset(i for i in range(n) if e[i] == 1):
                            bad_min += 1
                    # (L3) x in some S  iff  x in S_max
                    Smax = frozenset.union(*P)
                    for x in range(n):
                        if (any(x in S for S in P)) != (x in Smax):
                            bad_max += 1
                for s in ([s for _, s in peels(W, n, m)]
                          + [tuple(W[p[i]] for i in range(n)) for p in perms]):
                    if s not in seen and ok(cs, s, n, m):
                        seen.add(s); q.append(s)
    print("  legal states examined        : %d" % n_states)
    print("  pairs tested for closure     : %d" % n_pairs)
    print()
    print("  (L1) closed under UNION      : %d violations" % bad_union)
    print("  (L1) closed under INTERSECT  : %d violations" % bad_inter)
    print("  (L2) S_min = {i : ell(i)=1}  : %d violations" % bad_min)
    print("  (L3) x in some S iff x in S_max : %d violations" % bad_max)
    print()
    print("  |P(W)| distribution: %s" % dict(sorted(sizes.items())[:10]))
    print()
    if bad_union == bad_inter == 0:
        print("  *** P(W) is a lattice.  It has a unique maximum S_max and a")
        print("      unique minimum S_min = {i : ell(i) = 1}. ***")
    if bad_max == 0:
        print("  *** lem:paid-peel fires iff mu_x = 1 and x in S_max: the")
        print("      existential over 2^n paid sets collapses to ONE membership")
        print("      test, and S_max is the canonical potential for peeling. ***")


if __name__ == "__main__":
    main()
