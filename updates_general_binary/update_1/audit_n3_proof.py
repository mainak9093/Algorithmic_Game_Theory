"""
Audit of docs/PS2_general_binary_n3_full_proof (2).md.

WHAT THE DOCUMENT ACTUALLY PROVES. Its section 1 fixes cost functions
c_i : 2^M -> Z_{>=0} with c_i(empty) = 0 and every marginal in {0,1}. That is
the NEGATIVE DICHOTOMOUS (chores) class, i.e. PS1, not PS2. PS2 allows
marginals in {-1,0,1} with goods and chores mixed. The audit below is therefore
an audit of an n=3 proof of PS1.

The script implements Tao-Wu-Yu-Zhou's Algorithm 3 exactly as recorded in
report/sections/main_result.tex, runs it on random chores instances, and checks
every claim the document makes, in order:

  T(a)-(d)  the terminal-state facts  (document sections 7.1 and 8)
  F1        every leftover has marginal 1 on its owner's bundle
  F2        every equality arc has leftover marginal 1
  AUG       the augmented-bundle lemma, c_a(X_j + e) >= c_a(X_a) + 1
  R1CASE    the |R| = 1 construction, including the excess bound the document
            asserts without proof
  R2CASE    the |R| = 2 construction: total cost L+2, excess profile (1,1,0),
            the six edge bounds of section 11, and the final subsidy

One documented gap is checked separately. Section 9's equality case cites
Fact 2, which is stated for an equality ARC i -> j and so needs i != j; when
a = j the needed statement is Fact 1 instead. The script records how often the
a = j branch is actually taken, to show the gap is reached and not vacuous.
"""
import itertools
import random
import sys

from gb_valuations import enumerate_class


N = 3


def cost_from_valuation(v, m):
    """A chores valuation v (marginals in {-1,0}) as a cost c = -v."""
    return tuple(-v[S] for S in range(1 << m))


def marginals_ok(c, m):
    for S in range(1 << m):
        for k in range(m):
            bit = 1 << k
            if not S & bit and c[S | bit] - c[S] not in (0, 1):
                return False
    return c[0] == 0


def equality_graph(cs, X):
    """(i,j) with i != j and c_i(X_i) = c_i(X_j)."""
    return {(i, j) for i in range(N) for j in range(N)
            if i != j and cs[i][X[i]] == cs[i][X[j]]}


def is_ef(cs, X):
    return all(cs[i][X[i]] <= cs[i][X[j]]
               for i in range(N) for j in range(N))


def sccs(edges):
    """Strongly connected components of the equality graph, by brute force."""
    reach = {i: {i} for i in range(N)}
    changed = True
    while changed:
        changed = False
        for (i, j) in edges:
            if not reach[i] >= reach[j]:
                reach[i] |= reach[j]
                changed = True
    comps = []
    seen = set()
    for i in range(N):
        if i in seen:
            continue
        comp = frozenset(k for k in range(N)
                         if k in reach[i] and i in reach[k])
        comps.append(comp)
        seen |= comp
    return comps, reach


def find_cycle_through(edges, i, j):
    """A directed cycle of the equality graph containing the arc (i,j)."""
    if (i, j) not in edges:
        return None
    # any simple path j -> ... -> i, then the arc (i,j)
    stack = [(j, [j])]
    while stack:
        cur, path = stack.pop()
        if cur == i:
            return path
        for k in range(N):
            if (cur, k) in edges and k not in path:
                stack.append((k, path + [k]))
    return None


def twyz(cs, m, cap=200):
    """
    Algorithm 3 of Tao-Wu-Yu-Zhou, as restated in main_result.tex:
      (R1) a residual chore free for some agent goes to that agent;
      (R2) a residual chore free for i on X_j, for an equality arc (i,j) on a
           cycle, triggers a rotation along that cycle and then the assignment;
      (R3) otherwise take a tail SCC S; if |R| >= |S| give one chore to each
           member, else halt.
    Returns (X, R, S_at_halt) with S_at_halt None unless (R3) halted.
    """
    X = [0] * N
    R = set(range(m))
    for _ in range(cap):
        if not R:
            return tuple(X), R, None

        # (R1)
        done = False
        for e in sorted(R):
            for i in range(N):
                if cs[i][X[i] | (1 << e)] - cs[i][X[i]] == 0:
                    X[i] |= 1 << e
                    R.discard(e)
                    done = True
                    break
            if done:
                break
        if done:
            continue

        edges = equality_graph(cs, X)

        # (R2)
        for e in sorted(R):
            for (i, j) in sorted(edges):
                if cs[i][X[j] | (1 << e)] - cs[i][X[j]] != 0:
                    continue
                cyc = find_cycle_through(edges, i, j)
                if cyc is None:
                    continue
                # rotate: each agent on the cycle takes its successor's bundle
                old = list(X)
                order = cyc                    # j = cyc[0], ..., i = cyc[-1]
                for t, a in enumerate(order):
                    X[a] = old[order[(t + 1) % len(order)]]
                X[i] |= 1 << e
                R.discard(e)
                done = True
                break
            if done:
                break
        if done:
            continue

        # (R3): a tail SCC, i.e. one with no equality arc leaving it
        comps, _ = sccs(edges)
        tail = None
        for comp in comps:
            if not any(i in comp and j not in comp for (i, j) in edges):
                tail = comp
                break
        if tail is None:
            tail = comps[0]
        if len(R) >= len(tail):
            for a in sorted(tail):
                e = min(R)
                X[a] |= 1 << e
                R.discard(e)
            continue
        return tuple(X), R, tail
    return tuple(X), R, "CAP"


def subsidy(cs, A):
    """Minimal subsidy in cost form; None if a positive cycle exists."""
    def w(i, j):
        return cs[i][A[i]] - cs[i][A[j]]
    # no positive cycle: check the two 3-cycles and the three 2-cycles
    for cyc in ((0, 1, 2), (0, 2, 1)):
        if sum(w(cyc[t], cyc[(t + 1) % 3]) for t in range(3)) > 0:
            return None
    for i, j in itertools.combinations(range(N), 2):
        if w(i, j) + w(j, i) > 0:
            return None
    out = []
    for i in range(N):
        others = [j for j in range(N) if j != i]
        best = 0
        for j in others:
            best = max(best, w(i, j))
            for k in others:
                if k != j:
                    best = max(best, w(i, j) + w(j, k))
        out.append(best)
    return out


def min_cost_assignment(cs, bundles):
    """Assignment of the three bundles to the three agents minimising cost."""
    best, arg = None, None
    for perm in itertools.permutations(range(N)):
        A = tuple(bundles[perm[i]] for i in range(N))
        tot = sum(cs[i][A[i]] for i in range(N))
        if best is None or tot < best:
            best, arg = tot, A
    return arg, best


def main():
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
    rng = random.Random(20260828)

    pool = [cost_from_valuation(v, m) for v in enumerate_class(m, {-1, 0})]
    pool = [c for c in pool if marginals_ok(c, m)]
    print("chores cost functions on m=%d items: %d" % (m, len(pool)))

    stat = {k: 0 for k in
            ("runs", "cap", "r0", "r1", "r2", "notEF", "S_not_all",
             "F1_bad", "F2_bad", "AUG_bad", "AUG_diag_used",
             "r1_excess_bad", "r1_path_bad", "r1_sub_bad",
             "r2_total_bad", "r2_profile_bad", "r2_edge_bad", "r2_sub_bad",
             "AUG_bad_r1")}

    for _ in range(trials):
        cs = tuple(rng.choice(pool) for _ in range(N))
        X, R, S = twyz(cs, m)
        stat["runs"] += 1
        if S == "CAP":
            stat["cap"] += 1
            continue
        if not is_ef(cs, X):
            stat["notEF"] += 1
            continue
        r = len(R)
        stat["r%d" % min(r, 2)] += 1

        if r == 0:
            continue

        # F1
        for i in range(N):
            for e in R:
                if cs[i][X[i] | (1 << e)] - cs[i][X[i]] != 1:
                    stat["F1_bad"] += 1

        if r == 2:
            if S is None or set(S) != {0, 1, 2}:
                stat["S_not_all"] += 1
            edges = equality_graph(cs, X)
            for (i, j) in edges:
                for e in R:
                    if cs[i][X[j] | (1 << e)] - cs[i][X[j]] != 1:
                        stat["F2_bad"] += 1

        # AUG: c_a(X_j + e) >= c_a(X_a) + 1.
        # The document states this inside its |R| = 2 case (sections 7-10),
        # where Fact 2 is available because the terminal SCC is all of N.
        # Checked separately for r = 1, where Fact 2 is NOT available.
        for a in (range(N) if r == 2 else []):
            for j in range(N):
                for e in R:
                    if cs[a][X[j] | (1 << e)] < cs[a][X[a]] + 1:
                        stat["AUG_bad"] += 1
                    if a == j and cs[a][X[a]] == cs[a][X[j]]:
                        stat["AUG_diag_used"] += 1

        if r == 1:
            for a in range(N):
                for j in range(N):
                    for e in R:
                        if cs[a][X[j] | (1 << e)] < cs[a][X[a]] + 1:
                            stat["AUG_bad_r1"] += 1

        L = sum(cs[i][X[i]] for i in range(N))

        if r == 1:
            e = next(iter(R))
            for mbundle in range(N):
                Y = tuple(X[i] | (1 << e) if i == mbundle else X[i]
                          for i in range(N))
                A, tot = min_cost_assignment(cs, Y)
                if tot > L + 1:
                    stat["r1_excess_bad"] += 1
                p = subsidy(cs, A)
                if p is None or max(p) > 1:
                    stat["r1_sub_bad"] += 1
                excess = sum(cs[i][A[i]] for i in range(N)) - L
                if excess > 1:
                    stat["r1_path_bad"] += 1

        if r == 2:
            e1, e2 = sorted(R)
            for u, v in itertools.permutations(range(N), 2):
                Y = list(X)
                Y[u] |= 1 << e1
                Y[v] |= 1 << e2
                A, tot = min_cost_assignment(cs, tuple(Y))
                if tot != L + 2:
                    stat["r2_total_bad"] += 1
                g = sorted(cs[i][A[i]] - cs[i][X[i]] for i in range(N))
                if g != [0, 1, 1]:
                    stat["r2_profile_bad"] += 1
                aug = [i for i in range(N)
                       if A[i] in (Y[u], Y[v]) and A[i] != X[i] or
                       (A[i] == Y[u] or A[i] == Y[v])]
                # identify recipients by excess instead, which is exact
                hi = [i for i in range(N) if cs[i][A[i]] - cs[i][X[i]] == 1]
                lo = [i for i in range(N) if cs[i][A[i]] - cs[i][X[i]] == 0]
                if len(hi) == 2 and len(lo) == 1:
                    a, b = hi
                    c = lo[0]

                    def w(i, j):
                        return cs[i][A[i]] - cs[i][A[j]]
                    if not (w(a, b) <= 0 and w(b, a) <= 0
                            and w(a, c) <= 1 and w(b, c) <= 1
                            and w(c, a) <= 0 and w(c, b) <= 0):
                        stat["r2_edge_bad"] += 1
                p = subsidy(cs, A)
                if p is None or max(p) > 1:
                    stat["r2_sub_bad"] += 1

    print()
    for k in ("runs", "cap", "notEF", "r0", "r1", "r2"):
        print("  %-16s %d" % (k, stat[k]))
    print()
    print("  claim violations (all should be 0):")
    for k in ("S_not_all", "F1_bad", "F2_bad", "AUG_bad",
              "r1_excess_bad", "r1_path_bad", "r1_sub_bad",
              "r2_total_bad", "r2_profile_bad", "r2_edge_bad", "r2_sub_bad"):
        print("  %-16s %d" % (k, stat[k]))
    print()
    print("  AUG checked in the |R|=1 case, where Fact 2 is unavailable:")
    print("  %-16s %d   (the document does NOT claim it there)"
          % ("AUG_bad_r1", stat["AUG_bad_r1"]))
    print()
    print("  section 9 equality case reached with a = j (needs Fact 1,")
    print("  not Fact 2) : %d times" % stat["AUG_diag_used"])


if __name__ == "__main__":
    main()
