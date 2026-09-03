"""
Characterising the 624 forbidden gap patterns.

gap_matrix.py reduces validity to a 3x3 matrix over {0,1,2} with a zero in
every row: 6,859 patterns, 624 of them forbidden, verified against the envy
graph on 102,060 allocations with no mismatch.

624 is still a list, not a theorem. Two things would turn it into one.

MONOTONICITY. Lowering a gap entry can only enlarge demand sets -- bundle j
becomes acceptable to agent i at more prices -- so it should only make matching
easier. If so the GOOD set is downward closed, the FORBIDDEN set is upward
closed, and the whole classification is determined by the MINIMAL forbidden
patterns. That is the difference between a lookup table and a characterisation.

MINIMAL ELEMENTS. Those minimal patterns are the real obstructions, and each
one says something concrete about the valuations -- an entry of 2 in row i at
column j means v_i(B_i-best) - v_i(B_j) >= 2, which by the marginal bound
forces at least two items to separate the bundles.

Symmetry is quotiented out as well: relabelling agents permutes rows and
relabelling bundles permutes columns, and validity is invariant under both, so
the minimal patterns are reported up to that action.
"""
import itertools

N = 3


def perfect_matching(adj):
    match = [-1] * N
    def go(i, seen):
        for j in adj[i]:
            if not seen[j]:
                seen[j] = True
                if match[j] == -1 or go(match[j], seen):
                    match[j] = i
                    return True
        return False
    return sum(1 for i in range(N) if go(i, [False] * N)) == N


def pattern_valid(G):
    for mask in range(1 << N):
        q = [(mask >> j) & 1 for j in range(N)]
        adj = []
        for i in range(N):
            hit = [j for j in range(N) if G[i][j] == 0 and q[j] == 1]
            if hit:
                adj.append(hit)
            else:
                adj.append([j for j in range(N)
                            if G[i][j] == 0 or (G[i][j] == 1 and q[j] == 1)])
        if perfect_matching(adj):
            return True
    return False


def main():
    rows = [r for r in itertools.product((0, 1, 2), repeat=N) if 0 in r]
    pats = list(itertools.product(rows, repeat=N))
    good = {p for p in pats if pattern_valid(p)}
    forb = [p for p in pats if p not in good]
    print("patterns %d, forbidden %d" % (len(pats), len(forb)))

    # --- monotonicity: does lowering an entry ever turn good into forbidden?
    bad = 0
    ex = None
    for p in pats:
        for i in range(N):
            for j in range(N):
                if p[i][j] == 0:
                    continue
                q = [list(r) for r in p]
                q[i][j] -= 1
                q = tuple(tuple(r) for r in q)
                if p in good and q not in good:
                    bad += 1
                    if ex is None:
                        ex = (p, q, i, j)
    print()
    print("MONOTONICITY: lowering one entry turns a valid pattern invalid : %d%s"
          % (bad, "   <-- forbidden set is UPWARD CLOSED" if not bad else ""))
    if ex:
        print("   counterexample %s -> %s at (%d,%d)" % ex)

    # --- minimal forbidden patterns
    forbset = set(forb)
    minimal = []
    for p in forb:
        lower_ok = True
        for i in range(N):
            for j in range(N):
                if p[i][j] == 0:
                    continue
                q = [list(r) for r in p]
                q[i][j] -= 1
                q = tuple(tuple(r) for r in q)
                if q in forbset:
                    lower_ok = False
                    break
            if not lower_ok:
                break
        if lower_ok:
            minimal.append(p)
    print("   minimal forbidden patterns : %d" % len(minimal))

    # --- quotient by row and column permutations
    def canon(p):
        best = None
        for rp in itertools.permutations(range(N)):
            for cp in itertools.permutations(range(N)):
                q = tuple(tuple(p[rp[i]][cp[j]] for j in range(N))
                          for i in range(N))
                if best is None or q < best:
                    best = q
        return best

    classes = {}
    for p in minimal:
        classes.setdefault(canon(p), []).append(p)
    print("   ... up to relabelling agents and bundles : %d classes"
          % len(classes))
    print()
    for c in sorted(classes):
        print("      %s        (orbit size %d)" % (list(c), len(classes[c])))

    # sanity: is every forbidden pattern above some minimal one?
    def above(p, q):
        return all(p[i][j] >= q[i][j] for i in range(N) for j in range(N))
    cover = sum(1 for p in forb if any(above(p, mq) for mq in minimal))
    print()
    print("   forbidden patterns lying above a minimal one : %d of %d%s"
          % (cover, len(forb), "   <-- generated" if cover == len(forb) else ""))


if __name__ == "__main__":
    main()
