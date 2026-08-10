"""How much foresight does CRI need?

cri_where.py found the sharpest structural fact so far: over 254,020 reachable
non-terminal CR states, every stuck state has |R| <= 2, and NO state with
|R| >= 3 is stuck.  Stuckness is not the right measure though -- a state can have
a legal move and still be doomed -- so this script redoes the histogram for DEAD
states, and then asks the question the histogram poses:

    if death only ever happens in the last K rungs, a rule may play ARBITRARILY
    while |R| > K and need only solve a bounded problem at the end.

Tested: play any legal assignment while |R| > K, then search exhaustively over
the last K chores.  The minimal K that never fails is the amount of foresight
CRI actually needs, and K bounded independently of m would be a genuine
structural theorem -- it turns an unbounded reachability question into a finite
one.

K = 0 is plain greedy.  If the minimal K is small and constant, the target
becomes: "from a legal CR state with |R| = K, a completion exists", which is a
statement about allocations, not about a search space.

Run:  python cri_lookahead.py
"""
from itertools import permutations, product
from collections import Counter, defaultdict
import random
import sys

sys.path.insert(0, "../update_6")
sys.path.insert(0, "../update_32")
sys.path.insert(0, "../update_44")
sys.path.insert(0, "../update_17")
from counterexample_hunt import FAMILIES                        # noqa: E402
from cri_sweep import (cr_legal, assignments, relabels,          # noqa: E402
                       is_dichotomous, exhaustive_n3m3)


def build(cs, n, m, perms):
    """legal set, successor maps, reachable set, live set."""
    root = tuple([n] * m)
    legal_set = {own for own in product(range(n + 1), repeat=m)
                 if cr_legal(cs, own, n, m)}
    succ = {s: [t for _, _, t in assignments(s, n, m) if t in legal_set]
            for s in legal_set}
    succ_p = {s: [t for t in relabels(s, n, m, perms) if t in legal_set]
              for s in legal_set}
    pred = defaultdict(list)
    for s in legal_set:
        for t in succ[s] + succ_p[s]:
            pred[t].append(s)
    live = {s for s in legal_set if n not in s}
    stack = list(live)
    while stack:
        t = stack.pop()
        for s in pred[t]:
            if s not in live:
                live.add(s)
                stack.append(s)
    reach = set()
    if root in legal_set:
        reach.add(root)
        st = [root]
        while st:
            s = st.pop()
            for t in succ[s] + succ_p[s]:
                if t not in reach:
                    reach.add(t)
                    st.append(t)
    return legal_set, succ, succ_p, live, reach


def lookahead_ok(cs, n, m, perms, K, rng):
    """Play a RANDOM legal assignment while |R| > K, then search the last K.

    Random rather than first-found, so the result is not an artefact of the
    enumeration order: a K that survives random play is genuinely a statement
    about the state, not about the tie-break.
    """
    own = tuple([n] * m)
    while True:
        r = sum(1 for v in own if v == n)
        if r == 0:
            return True
        if r <= K:
            return search(cs, own, n, m, perms, set())
        opts = [t for _, _, t in assignments(own, n, m)
                if cr_legal(cs, t, n, m)]
        if not opts:
            for t in relabels(own, n, m, perms):
                if not cr_legal(cs, t, n, m):
                    continue
                o2 = [u for _, _, u in assignments(t, n, m)
                      if cr_legal(cs, u, n, m)]
                if o2:
                    opts = o2
                    break
            if not opts:
                return False
        own = opts[rng.randrange(len(opts))]


def search(cs, own, n, m, perms, seen):
    """Exhaustive completion search from `own`."""
    if n not in own:
        return True
    if own in seen:
        return False
    seen.add(own)
    for _, _, t in assignments(own, n, m):
        if cr_legal(cs, t, n, m) and search(cs, t, n, m, perms, seen):
            return True
    for t in relabels(own, n, m, perms):
        if t != own and cr_legal(cs, t, n, m) and t not in seen:
            for _, _, u in assignments(t, n, m):
                if cr_legal(cs, u, n, m) and search(cs, u, n, m, perms, seen):
                    return True
            seen.add(t)
    return False


def main():
    rng = random.Random(24680)
    print("=== how much foresight does CRI need? ===")
    print()

    blocks = [("EXHAUSTIVE n=m=3", exhaustive_n3m3(), 3, 3)]
    for (n, m, T) in [(3, 4, 60), (3, 5, 30), (3, 6, 12), (3, 7, 6),
                      (4, 4, 30), (4, 5, 12), (4, 6, 5), (5, 4, 10)]:
        inst = []
        while len(inst) < T:
            name, gen = FAMILIES[rng.randrange(len(FAMILIES))]
            cs = gen(m, n, rng)
            if max(max(c.values()) for c in cs) < 1:
                continue
            assert all(is_dichotomous(c, m) for c in cs)
            inst.append(cs)
        blocks.append(("n=%d m=%d" % (n, m), inst, n, m))

    HD = Counter()      # |R| -> dead reachable states
    HA = Counter()      # |R| -> all reachable non-terminal states
    KS = [0, 1, 2, 3]
    fails = Counter()
    ninst = 0
    print("  %-18s  lookahead failures by K" % "block")
    for tag, inst, n, m in blocks:
        perms = list(permutations(range(n)))
        loc = Counter()
        for cs in inst:
            ninst += 1
            legal_set, succ, succ_p, live, reach = build(cs, n, m, perms)
            for s in reach:
                r = sum(1 for v in s if v == n)
                if r == 0:
                    continue
                HA[r] += 1
                if s not in live:
                    HD[r] += 1
            for K in KS:
                if not lookahead_ok(cs, n, m, perms, K, rng):
                    loc[K] += 1
                    fails[K] += 1
        print("  %-18s  %s" % (tag, dict(loc) if loc else "none"))

    print()
    print("  |R| at a DEAD reachable state:")
    print("       |R|    dead   all reachable    dead share")
    for r in sorted(HA):
        print("      %4d %7d %15d   %9.4f%%"
              % (r, HD[r], HA[r], 100.0 * HD[r] / max(HA[r], 1)))
    print("       tot %7d %15d" % (sum(HD.values()), sum(HA.values())))

    deep = [r for r in HD if HD[r] and r >= 3]
    print()
    if not deep:
        print("  *** NO reachable CR state with |R| >= 3 is dead, over %d"
              % sum(HA[r] for r in HA if r >= 3))
        print("      such states.  Death is confined to the last two rungs. ***")
    else:
        print("  dead states occur at |R| = %s, so death is not confined to the"
              % sorted(deep))
        print("  last two rungs.")

    print()
    print("  lookahead failures over %d instances: %s"
          % (ninst, {K: fails[K] for K in KS}))
    good = [K for K in KS if fails[K] == 0]
    if good:
        K = min(good)
        print()
        print("  *** K = %d suffices: play ANY legal assignment while |R| > %d,"
              % (K, K))
        print("      then solve the last %d chores.  CRI would follow from the"
              % K)
        print("      bounded statement -- every reachable legal CR state with")
        print("      |R| = %d admits a completion -- with no rule needed"
              % K)
        print("      anywhere else in the induction. ***")


if __name__ == "__main__":
    main()
