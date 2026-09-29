# -*- coding: utf-8 -*-
"""
Build the algorithm walkthrough frames and splice them into ../talk.tex.

    python build_demo.py

The instance below was found by search_demo.py (seed 21). Nothing is drawn by
hand: the script replays the run, checks it, and only then emits TikZ.

Checks, all of which must pass before anything is written:
  1. the costs are dichotomous (algo1.is_valid_cost on full cost tables);
  2. the run in search_demo.py and algo1.twyz() reach the same terminal state,
     and our completion matches algo1.algorithm1() exactly;
  3. every step is re-verified on the cost tables: its rule really applied,
     the earlier rules really did not, and the tail SCC was the only one;
  4. the partial allocation stays envy-free after every step (Tao's
     invariant);
  5. the final (A, p) is complete and envy-free, with p in {0,1}^n,
     sum p <= n - 1, and A is EF1;
  6. every marginal, cost and envy claim in a step's "why" box is recomputed
     from the cost tables and asserted where the sentence is written.

The frames go into talk.tex between the markers "% BEGIN DEMO" and
"% END DEMO", placed right after the "The algorithm" frame, so talk.tex
stays one self-contained file.
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ALGO = os.path.normpath(os.path.join(HERE, "..", "..", "..", "updates_pareto", "update_1"))
sys.path.insert(0, HERE)
sys.path.insert(0, ALGO)
import algo1  # noqa: E402
import search_demo as sd  # noqa: E402

TALK = os.path.normpath(os.path.join(HERE, "..", "talk.tex"))

# Seed 21: every hard and nice criterion of search_demo.evaluate, including a
# subsidy closure whose first round is needed -- the leftover chore is free for
# agent 1 on the recipient's bundle, so paying T alone leaves 1 envious.
INSTANCE = {
    "n": 6, "m": 14, "K": [5, 5, 5, 5, 5, 6],
    "grp": [[-1, 0, 1, 0, 4, 1, 0, 1, 0, -1, 0, 0, 2, 0],
            [3, 4, 3, 4, 4, 4, 2, 0, 1, -1, 1, 2, 0, 3],
            [2, 3, 1, 2, 0, 4, 4, 2, 2, 2, -1, 4, 4, 2],
            [3, 4, 4, 1, 2, 4, 0, 3, 3, 2, -1, 1, 1, 3],
            [2, 2, 3, 2, 0, 2, 4, 1, 0, 4, 2, 0, 0, 3],
            [5, 2, 5, 2, 1, 5, 4, 3, 3, 4, 5, 3, 4, 0]],
    "a": [0, 0, 0, 0, 0, 1],
    "b": [3, 2, 4, 3, 4, 3],
}
# The first example (seed 3 of the earlier search). Same shape of run, but its
# closure paid agents that would not have envied anyone: paying T alone was
# already envy-free there, which undersells why P has to propagate.
# INSTANCE = {
#     "n": 6, "m": 15, "K": [5, 6, 6, 4, 6, 6],
#     "grp": [[4, 3, 1, 0, 3, 0, 3, 2, 2, 4, 2, -1, 1, -1, 1],
#             [4, 0, 4, 2, 4, 3, 4, 1, 2, 4, 5, 2, 3, 5, 0],
#             [2, 4, 0, 0, 5, 5, 3, -1, 4, 5, 0, 4, 0, 0, 4],
#             [2, 3, 2, 2, 3, 1, 3, 1, 1, 1, 3, 2, 0, 0, 1],
#             [3, 5, 5, 0, 1, 1, 0, 1, 2, 1, 3, -1, 4, 0, 1],
#             [0, 3, 5, 2, -1, 4, -1, -1, 0, 3, 4, -1, 2, 3, 2]],
#     "a": [1, 1, 0, 0, 0, 0],
#     "b": [2, 2, 3, 2, 2, None],
# }

R1_CHUNK = 5          # consecutive (R1) steps shown per overlay


# ==========================================================================
# 1-5. Replay and verify
# ==========================================================================

def marg(cs, i, e, S):
    return cs[i][S | (1 << e)] - cs[i][S]


def reaches(E, n, src):
    seen, stack = {src}, [src]
    while stack:
        u = stack.pop()
        for (a, b) in E:
            if a == u and b not in seen:
                seen.add(b)
                stack.append(b)
    return seen


def on_cycle(E, a, b, n):
    return (a, b) in E and a in reaches(E, n, b)


def tail_sccs(E, n):
    comps, _ = algo1.sccs_and_tail(E, n)
    return [c for c in comps if not any(i in c and j not in c for (i, j) in E)]


def r1_applicable(cs, X, R, n):
    return any(marg(cs, i, e, X[i]) == 0 for e in R for i in range(n))


def r2_applicable(cs, X, R, E, n):
    return any(marg(cs, a, e, X[b]) == 0 and on_cycle(E, a, b, n)
               for e in R for (a, b) in E)


def replay(cs, n, m, ev):
    X = [0] * n
    R = set(range(m))
    E = frozenset(algo1.equality_graph(cs, X, n))
    snaps = [dict(X=tuple(X), R=frozenset(R), E=E)]
    for x in ev:
        E = algo1.equality_graph(cs, X, n)
        if x[0] == "R1":
            _, e, i = x
            assert e in R and marg(cs, i, e, X[i]) == 0, x
            X[i] |= 1 << e
            R.discard(e)
        elif x[0] == "R2":
            _, e, i, j, cyc = x
            assert not r1_applicable(cs, X, R, n), x
            assert e in R and (i, j) in E, x
            assert cyc[0] == j and cyc[-1] == i and len(set(cyc)) == len(cyc), x
            assert all((cyc[t], cyc[t + 1]) in E for t in range(len(cyc) - 1)), x
            assert marg(cs, i, e, X[j]) == 0, x
            old = list(X)
            for t, a in enumerate(cyc):
                X[a] = old[cyc[(t + 1) % len(cyc)]]
                assert cs[a][X[a]] == cs[a][old[a]], "rotation changed a cost"
            X[i] |= 1 << e
            R.discard(e)
        elif x[0] == "R3":
            _, tail, gave, _ = x
            assert not r1_applicable(cs, X, R, n), x
            assert not r2_applicable(cs, X, R, E, n), x
            tails = tail_sccs(E, n)
            assert len(tails) == 1 and set(tails[0]) == set(tail), x
            assert len(R) >= len(tail), x
            assert sorted(a for _, a in gave) == sorted(tail), x
            assert len({e for e, _ in gave}) == len(gave), x
            for e, a in gave:
                assert e in R
                X[a] |= 1 << e
                R.discard(e)
        else:
            _, tail, _ = x
            assert not r1_applicable(cs, X, R, n), x
            assert not r2_applicable(cs, X, R, E, n), x
            tails = tail_sccs(E, n)
            assert len(tails) == 1 and set(tails[0]) == set(tail), x
            assert 1 <= len(R) < len(tail), x
        assert algo1.is_ef(cs, X, n), "partial allocation lost envy-freeness"
        snaps.append(dict(X=tuple(X), R=frozenset(R),
                          E=frozenset(algo1.equality_graph(cs, X, n))))
    return snaps


def verify_final(cs, n, m, A, p):
    everything = 0
    for i in range(n):
        assert everything & A[i] == 0, "bundles overlap"
        everything |= A[i]
    assert everything == (1 << m) - 1, "allocation is not complete"
    assert all(q in (0, 1) for q in p) and sum(p) <= n - 1, "subsidy bound"
    for i in range(n):
        for j in range(n):
            assert cs[i][A[i]] - p[i] <= cs[i][A[j]] - p[j], "envy with subsidy"
    for i in range(n):                                   # EF1, chore form
        for j in range(n):
            if cs[i][A[i]] <= cs[i][A[j]]:
                continue
            assert any(cs[i][A[i] & ~(1 << e)] <= cs[i][A[j]]
                       for e in range(m) if A[i] >> e & 1), "not EF1"


def build_and_verify():
    I = sd.Inst(INSTANCE["n"], INSTANCE["m"], INSTANCE["K"], INSTANCE["grp"],
                INSTANCE["a"], INSTANCE["b"])
    n, m = I.n, I.m
    cs = [tuple(I.cost(i, S) for S in range(1 << m)) for i in range(n)]
    for i in range(n):
        assert algo1.is_valid_cost(cs[i], m), "cost %d is not dichotomous" % i

    X, R, S, ev = sd.run(I)
    Xr, Rr, Sr = algo1.twyz(cs, n, m)
    assert tuple(X) == Xr and set(R) == set(Rr) and set(S) == set(Sr), \
        "search_demo.run disagrees with algo1.twyz"

    A, p, T, P, rounds, E = sd.complete(I, X, R, S)
    A1, p1, info = algo1.algorithm1(cs, n, m)
    assert tuple(A) == A1 and list(p) == list(p1), "completion disagrees with algo1"
    assert list(T) == list(info["T"]) and sorted(P) == list(info["P"])

    snaps = replay(cs, n, m, ev)
    assert snaps[-1]["X"] == tuple(X) and snaps[-1]["R"] == frozenset(R)
    verify_final(cs, n, m, A, p)

    return dict(n=n, m=m, cs=cs, ev=ev, snaps=snaps, X=tuple(X), R=sorted(R),
                S=sorted(S), T=list(T), P=sorted(P), rounds=rounds,
                E=frozenset(E), A=tuple(A), p=list(p))


# ==========================================================================
# Overlays: what each page of the animation shows
# ==========================================================================

def agents(xs):
    return ",".join(str(a + 1) for a in sorted(xs))


def listing(xs):
    """1 / 1 and 2 / 1, 2 and 3 (agents are 1-indexed on the slides)."""
    xs = [str(a + 1) for a in sorted(xs)]
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def none_envious(xs):
    xs = [str(a + 1) for a in sorted(xs)]
    if len(xs) == 1:
        return "does not make %s envious" % xs[0]
    if len(xs) == 2:
        return "makes neither %s nor %s envious" % tuple(xs)
    return "makes none of %s envious" % ", ".join(xs)


def ch(e):
    return "e_{%d}" % (e + 1)


def bset(S, m):
    items = [e for e in range(m) if S >> e & 1]
    if not items:
        return r"\emptyset"
    return r"\{" + ",".join(ch(e) for e in items) + r"\}"


def mtab(cells, cols=2):
    """Short formulas in a borderless table, `cols` to a row."""
    rows = [" & ".join(cells[q:q + cols]) for q in range(0, len(cells), cols)]
    spec = r"@{\hspace{1em}}".join(["l"] * cols)
    return (r"\begin{tabular}{@{}%s@{}}" % spec) + r" \\ ".join(rows) + r"\end{tabular}"


def overlay(snap, caption, phase, **kw):
    ov = dict(X=snap["X"], R=snap["R"], E=snap["E"], caption=caption,
              phase=phase, node={}, arc={}, chore={}, bundle={}, chip={},
              badge=None, title="", why=[])
    ov.update(kw)
    return ov


def storyboard(run):
    n, m, ev, snaps, cs = run["n"], run["m"], run["ev"], run["snaps"], run["cs"]

    # Each "why" sentence is written next to the assertion that makes it true.
    def r1_fails(snap):
        X, R = snap["X"], snap["R"]
        assert all(marg(cs, i, e, X[i]) == 1 for e in R for i in range(n))
        return r"(R1) fails: each leftover chore costs every agent $+1$ on her own bundle."

    def r2_fails(snap):
        X, R, E = snap["X"], snap["R"], snap["E"]
        assert all(marg(cs, a, e, X[b]) == 1 for e in R for (a, b) in E
                   if on_cycle(E, a, b, n))
        return (r"(R2) fails: $c_i(e\mid X_j)=1$ for each leftover $e$ and each "
                r"arc $i\to j$ on a cycle.")

    s0 = snaps[0]
    assert all(cs[i][0] == 0 for i in range(n)) and len(s0["E"]) == n * (n - 1)
    ovs = [overlay(
        s0, r"Start: every bundle is empty, so everyone is indifferent to "
            r"everything --- the equality graph is complete.", "tao",
        title="Reading the graph",
        why=[r"An arc $i\to j$ means $c_i(X_i)=c_i(X_j)$: agent $i$ is indifferent "
             r"between her bundle and $j$'s.",
             r"Every bundle is empty and $c_i(\emptyset)=0$, so all %d arcs are "
             r"present." % (n * (n - 1)),
             r"Every step keeps $X$ envy-free: $c_i(X_i)\le c_i(X_j)$ for all $i,j$."])]
    k = 0
    while k < len(ev):
        x = ev[k]
        if x[0] == "R1":
            j = k
            while j < len(ev) and ev[j][0] == "R1" and j - k < R1_CHUNK:
                j += 1
            batch = ev[k:j]
            moves = ", ".join(r"$%s\!\to\!%d$" % (ch(b[1]), b[2] + 1) for b in batch)
            cells = []
            for q in range(k, j):
                _, e, i = ev[q]
                Xi = snaps[q]["X"][i]                  # her bundle just before
                assert marg(cs, i, e, Xi) == 0
                cells.append(r"$c_{%d}(%s\mid %s)=0$" % (i + 1, ch(e), bset(Xi, m)))
            why = [mtab(cells)]                        # the title says "(R1)"
            if k and ev[k - 1][0] == "R3" and j - k == 1:
                # (R1) again right after (R3): say what made the chore free
                _, e, i = x
                got = [g for g, a in ev[k - 1][2] if a == i]
                if got:
                    before = snaps[k - 1]["X"][i]
                    assert marg(cs, i, e, before) == 1
                    why.append(r"Free only since (R3) gave her $%s$: before, "
                               r"$c_{%d}(%s\mid %s)=1$."
                               % (ch(got[0]), i + 1, ch(e), bset(before, m)))
            if j == len(ev) or ev[j][0] != "R1":
                assert not r1_applicable(cs, snaps[j]["X"], snaps[j]["R"], n)
                why.append(r"Now no leftover chore is free for anyone.")
            if k == 0:
                why.append(r"Dashed arcs were just lost: the bundle they point to "
                           r"grew, and now costs more.")
            ovs.append(overlay(
                snaps[j], r"\textbf{(R1)} free chore%s placed: "
                % ("" if len(batch) == 1 else "s") + moves + ".", "tao",
                node={b[2]: "R1" for b in batch},
                chore={b[1]: "R1" for b in batch}, badge="R1",
                title="Why (R1) applies", why=why))
            k = j
            continue
        if x[0] == "R2":
            _, e, i, jj, cyc = x
            s, s1 = snaps[k], snaps[k + 1]
            X, X1 = s["X"], s1["X"]
            loop = [i] + list(cyc[:-1])            # i -> j -> ... -> back to i
            arcs = {(loop[t], loop[(t + 1) % len(loop)]): "R2" for t in range(len(loop))}
            path = r"\!\to\!".join(str(a + 1) for a in loop + [i])
            assert marg(cs, i, e, X[jj]) == 0
            ovs.append(overlay(
                s,
                r"\textbf{(R2)} no free chore left, but the arc $%d\!\to\!%d$ lies "
                r"on the cycle $%s$." % (i + 1, jj + 1, path), "tao",
                node={a: "R2" for a in cyc}, arc=arcs, chip={e: "R2"}, badge="R2",
                title="Why (R2) applies",
                why=[r1_fails(s),
                     r"But $c_{%d}(%s\mid X_{%d})=0$: $%s$ is free for %d on top of "
                     r"%d's bundle," % (i + 1, ch(e), jj + 1, ch(e), i + 1, jj + 1),
                     r"and $%d\to%d$ lies on a cycle, so a rotation can hand %d's "
                     r"bundle to %d." % (i + 1, jj + 1, jj + 1, i + 1)]))
            cells = []
            for t in range(len(loop)):
                a, b = loop[t], loop[(t + 1) % len(loop)]
                assert cs[a][X[b]] == cs[a][X[a]] == cs[a][X1[a]]
                cells.append(r"$c_{%d}(X_{%d})=c_{%d}(X_{%d})=%d$"
                             % (a + 1, b + 1, a + 1, a + 1, cs[a][X[a]]))
            assert X1[i] == X[jj] | (1 << e) and cs[i][X1[i]] == cs[i][X[jj]]
            ovs.append(overlay(
                s1,
                r"\textbf{(R2)} each agent on the cycle takes the bundle her arc "
                r"points to; then agent %d takes $%s$." % (i + 1, ch(e)), "tao",
                node={a: "R2" for a in cyc}, bundle={a: "R2" for a in cyc},
                chore={e: "R2"}, badge="R2",
                title="Why no cost changes",
                why=[r"Each arc of the cycle is an equality ($X$ = the bundles "
                     r"before the move):", mtab(cells),
                     r"so no cost on the cycle changes, and then "
                     r"$c_{%d}(X_{%d}\cup\{%s\})=c_{%d}(X_{%d})$."
                     % (i + 1, jj + 1, ch(e), i + 1, jj + 1)]))
            k += 1
            continue
        if x[0] == "R3":
            _, tail, gave, _ = x
            s, s1 = snaps[k], snaps[k + 1]
            X, X1 = s["X"], s1["X"]
            out = [j for j in range(n) if j not in tail]
            assert all(cs[a][X[a]] < cs[a][X[j]] for a in tail for j in out)
            own = {cs[a][X[a]] for a in tail}
            low = min(cs[a][X[j]] for a in tail for j in out)
            if len(own) == 1 and len(tail) == 1:
                a, v = tail[0], min(own)
                tl = (r"No arc leaves $\{%d\}$: $c_{%d}(X_{%d})=%d$, and every other "
                      r"bundle costs her $\ge %d$." % (a + 1, a + 1, a + 1, v, low))
            elif len(own) == 1:
                tl = (r"No arc leaves $\{%s\}$: each member has cost %d, and every "
                      r"outside bundle costs each of them $\ge %d$."
                      % (agents(tail), min(own), low))
            else:
                tl = (r"No arc leaves $\{%s\}$: every outside bundle costs each member "
                      r"strictly more than her own." % agents(tail))
            inner = {(a, b): "R3" for (a, b) in s["E"] if a in tail and b in tail}
            ovs.append(overlay(
                s,
                r"\textbf{(R3)} no free chore and no rotation: the tail SCC is "
                r"$\{%s\}$, and $|R| = %d \ge %d$." % (agents(tail), len(s["R"]),
                                                        len(tail)),
                "tao", node={a: "R3" for a in tail}, arc=inner,
                chip={e: "R3" for e, _ in gave}, badge="R3",
                title="Why (R3) applies", why=[r1_fails(s), r2_fails(s), tl]))
            cells = []
            for e, a in gave:
                assert marg(cs, a, e, X[a]) == 1
                cells.append(r"$c_{%d}(%s\mid %s)=1$" % (a + 1, ch(e), bset(X[a], m)))
            if len(tail) == 1:
                why = [r"Her cost rises by exactly one:", mtab(cells, 1),
                       r"No envy: every other bundle was strictly dearer to her."]
            else:
                why = [r"Each member's cost rises by exactly one:", mtab(cells),
                       r"Outside bundles were already dearer, and (R2) fails "
                       r"inside the tail."]
            added = sorted((a, b) for (a, b) in s1["E"] - s["E"]
                           if a in tail and b not in tail)
            for (a, b) in added:
                assert X1[b] == X[b] and cs[a][X1[a]] == cs[a][X[a]] + 1 == cs[a][X[b]]
            if added and len(tail) == 1:
                a = tail[0]
                why.append(r"New arcs %s: her cost rose to $%d=%s$."
                           % (", ".join(r"$%d\to%d$" % (a + 1, b + 1) for _, b in added),
                              cs[a][X1[a]],
                              "=".join(r"c_{%d}(X_{%d})" % (a + 1, b + 1) for _, b in added)))
            elif added:
                a, b = added[0]
                why.append(r"Bold arcs are new ties, e.g.\ $c_{%d}(X_{%d})=c_{%d}(X_{%d})$."
                           % (a + 1, a + 1, a + 1, b + 1))
            moves = ", ".join(r"$%s\!\to\!%d$" % (ch(e), a + 1) for e, a in gave)
            ovs.append(overlay(
                s1,
                r"\textbf{(R3)} one leftover chore to each member: " + moves + ".",
                "tao", node={a: "R3" for a in tail},
                chore={e: "R3" for e, _ in gave}, badge="R3",
                title="Why no envy arises", why=why))
            k += 1
            continue
        # HALT
        _, tail, _ = x
        s = snaps[k]
        r = len(s["R"])
        left = ",".join(ch(e) for e in sorted(s["R"]))
        r1_fails(s)
        r2_fails(s)
        inner = {(a, b): "S" for (a, b) in s["E"] if a in tail and b in tail}
        ovs.append(overlay(
            s,
            r"\textbf{Halt.} The tail SCC $S=\{%s\}$ has %d agents, but only "
            r"$r=%d$ chore%s left." % (agents(tail), len(tail), r, "" if r == 1 else "s"),
            "tao", node={a: "S" for a in tail}, arc=inner, chip={e: "S" for e in s["R"]},
            badge="S", title="Why the algorithm halts",
            why=[(r"(R1), (R2) fail: $%s$ costs everyone $+1$, on her own bundle "
                  r"and on every cycle arc." % left) if r == 1 else
                 (r"(R1), (R2) fail: each of $%s$ costs everyone $+1$, on her own "
                  r"bundle and on every cycle arc." % left),
                 r"(R3) needs one chore per agent of the tail $S=\{%s\}$: %d chores, "
                 r"but only $r=%d$." % (agents(tail), len(tail), r),
                 r"Tao et al.\ stop here: $X$ is envy-free, but $%s$ %s unassigned."
                 % (left, "is" if r == 1 else "are")]))
        k += 1

    # ---- our completion ---------------------------------------------------
    S, T, R, rounds, E = run["S"], run["T"], run["R"], run["rounds"], run["E"]
    X, A, p = run["X"], run["A"], run["p"]
    done = dict(X=A, R=frozenset(), E=E)
    sn = {a: "S" for a in S}
    sarcs = {(a, b): "S" for (a, b) in E if a in S and b in S}

    nodes = dict(sn)
    for t in T:
        nodes[t] = "T"
    moves = ", ".join(r"$%s\!\to\!%d$" % (ch(R[q]), T[q] + 1) for q in range(len(T)))
    why = []
    for q, t in enumerate(T):
        e = R[q]
        assert A[t] == X[t] | (1 << e) and marg(cs, t, e, X[t]) == 1
        j = min((j for j in range(n) if j != t), key=lambda j: (cs[t][A[j]], j))
        assert cs[t][A[t]] > cs[t][A[j]] and p[t] == 1
        why.append(r"$c_{%d}(%s\mid X_{%d})=1$ by lemma (i), so $c_{%d}(A_{%d})=%d>%d="
                   r"c_{%d}(A_{%d})$: unpaid, %d would envy %d."
                   % (t + 1, ch(e), t + 1, t + 1, t + 1, cs[t][A[t]], cs[t][A[j]],
                      t + 1, j + 1, t + 1, j + 1))
        nb = [s for s in S if s not in T and (s, t) in E]
        for s in nb:
            assert marg(cs, s, e, X[t]) == 1 and p[s] == 0
            assert cs[s][A[s]] <= cs[s][A[t]] - p[t]
        if nb:
            why.append(r"Inside $S$, by lemma (ii): $%s=1$, so a unit to %d %s."
                       % ("=".join(r"c_{%d}(%s\mid X_{%d})" % (s + 1, ch(e), t + 1)
                                   for s in nb), t + 1, none_envious(nb)))
    ovs.append(overlay(
        done,
        r"\textbf{Our completion.} The leftover chore%s go%s to distinct agents "
        r"$T=\{%s\}\subseteq S$: " % ("" if len(R) == 1 else "s",
                                       "es" if len(R) == 1 else "", agents(T)) + moves + ".",
        "ours", node=dict(nodes), arc=dict(sarcs), chore={e: "T" for e in R}, badge="T",
        title=("Why agent %d must be paid" % (T[0] + 1)) if len(T) == 1
        else "Why the recipients must be paid", why=why))

    paid = set(T)
    arcs = dict(sarcs)
    for q, rd in enumerate(rounds):
        pull = [(a, b) for (a, b) in E if a in rd and b in paid]
        for a in rd:
            nodes[a] = "PT"
        for pr in pull:
            arcs[pr] = "PT"
        via = ", ".join(r"$%d\!\to\!%d$" % (a + 1, b + 1) for (a, b) in sorted(pull))
        why = []
        for a in rd:
            b = min(b for (x, b) in pull if x == a)
            v = cs[a][X[a]]
            assert a not in S and cs[a][X[b]] == v and p[a] == 1 and p[b] == 1
            head = r"Arc $%d\to%d$: $c_{%d}(X_{%d})=c_{%d}(X_{%d})=%d$" % (
                a + 1, b + 1, a + 1, a + 1, a + 1, b + 1, v)
            if b in T:
                e = R[T.index(b)]
                if cs[a][A[b]] == cs[a][X[b]]:
                    why.append(head + r", and $%s$ is free for %d on $X_{%d}$." % (
                        ch(e), a + 1, b + 1))
                else:
                    why.append(head + r". (P2) pays %d even though $%s$ costs her "
                               r"$+1$ on $X_{%d}$." % (a + 1, ch(e), b + 1))
            else:
                assert A[b] == X[b]
                why.append(head + r", and $A_{%d}=X_{%d}$." % (b + 1, b + 1))
            if cs[a][A[b]] - p[b] < cs[a][A[a]]:
                why.append(r"Once %d is paid, $c_{%d}(A_{%d})-p_{%d}=%d<%d=c_{%d}(A_{%d})$:"
                           r" unpaid, %d would envy %d."
                           % (b + 1, a + 1, b + 1, b + 1, cs[a][A[b]] - p[b], cs[a][A[a]],
                              a + 1, a + 1, a + 1, b + 1))
        paid |= set(rd)
        if q == len(rounds) - 1:
            assert not any((a, b) in E for a in range(n) if a not in S and a not in paid
                           for b in paid)
            why.append(r"No other agent outside $S$ has an arc into $P$: the closure stops.")
        first = q == 0
        ovs.append(overlay(
            done,
            (r"\textbf{Subsidy set $P$:} " if first else r"\textbf{$P$ grows again:} ")
            + r"agent%s $%s$, outside $S$, %s an equality arc into $P$ (%s), so %s paid."
            % ("" if len(rd) == 1 else "s", agents(rd), "has" if len(rd) == 1 else "have",
               via, "she is" if len(rd) == 1 else "they are"),
            "ours", node=dict(nodes), arc=dict(arcs), badge="PT",
            title="Why agent%s %s %s paid" % ("" if len(rd) == 1 else "s", listing(rd),
                                              "is" if len(rd) == 1 else "are"),
            why=why))

    P = run["P"]
    unpaid_S = [a for a in S if a not in T]
    outsiders = [a for a in range(n) if a not in S and p[a] == 0]
    why = [r"$p=(%s)$, and $\sum_i p_i=%d\le n-1=%d$."
           % (",".join(str(q) for q in p), sum(p), n - 1)]
    for o in outsiders:
        assert not any((o, j) in E for j in P)
        assert all(cs[o][A[o]] <= cs[o][A[j]] - 1 for j in P)
        why.append(r"Agent %d: no arc into $P$, so $c_{%d}(A_{%d})=%d\le c_{%d}(A_j)-1$ "
                   r"for every $j\in P$." % (o + 1, o + 1, o + 1, cs[o][A[o]], o + 1))
    if unpaid_S:
        for s in unpaid_S:
            for t, e in zip(T, R):                  # lemma (ii) towards T
                assert (marg(cs, s, e, X[t]) == 1 if (s, t) in E
                        else cs[s][X[s]] < cs[s][X[t]])
            # lemma (iii) towards P \ T
            assert all(cs[s][X[s]] < cs[s][X[j]] for j in P if j not in S)
        why.append(r"Agent%s %s in $S\setminus T$: lemma (ii) towards $T$, lemma (iii) "
                   r"towards $P\setminus T$." % ("" if len(unpaid_S) == 1 else "s",
                                                  listing(unpaid_S)))
    why.append(r"Checked: $c_i(A_i)-p_i\le c_i(A_j)-p_j$ for all $i,j$.")
    tail = r"Unpaid: $S\setminus T=\{%s\}$" % agents(unpaid_S)
    if outsiders:
        tail += r" and agent%s $%s$" % ("" if len(outsiders) == 1 else "s", agents(outsiders))
    ovs.append(overlay(
        done,
        r"\textbf{Result.} One unit to each agent of $P$: envy-free, total "
        r"$%d \le n-1 = %d$. " % (sum(p), n - 1) + tail + ".",
        "ours", node=dict(nodes), arc=dict(arcs), badge="p",
        title="Why this is envy-free", why=why))
    return ovs


# ==========================================================================
# TikZ
# ==========================================================================

W, H = 13.8, 6.8                    # fixed canvas: no jitter between overlays
CX, CY, RAD = 3.62, 3.2, 1.8        # the agent polygon (CX was 4.6 before the why box)
PANEL = 7.55                        # left edge of the right-hand panel (was 9.3)
CHIPS_PER_ROW = 8                   # was 4
CHIP_DX, CHIP_DY = 0.76, 0.54       # chip pitch
BOX_TOP, BOX_BOT = 3.76, 0.45       # the "why" box

COLOURS = [  # Okabe-Ito, colour-blind safe; one fixed meaning each
    ("OIgreen", "0,158,115"), ("OIpurple", "204,121,167"),
    ("OIorange", "230,159,0"), ("OIblue", "0,114,178"),
    ("OIverm", "213,94,0"), ("OIsky", "86,180,233"),
]
KEY = {"R1": "OIgreen", "R2": "OIpurple", "R3": "OIorange",
       "S": "OIblue", "T": "OIverm", "PT": "OIsky"}

NODE_STYLE = {
    None: r"draw=Slate, line width=0.8pt, fill=white",
    "R1": r"draw=OIgreen, line width=1.5pt, fill=OIgreen!28",
    "R2": r"draw=OIpurple, line width=1.5pt, fill=OIpurple!30",
    "R3": r"draw=OIorange, line width=1.5pt, fill=OIorange!35",
    "S":  r"draw=OIblue, line width=2pt, fill=OIblue!18",
    "T":  r"draw=OIverm, double, double distance=0.9pt, line width=0.9pt, fill=OIverm!32",
    "PT": r"draw=OIsky!75!black, dashed, line width=1.5pt, fill=OIsky!35",
}
# The rule badge is now the coloured title of the "why" box.
# BADGE_TEXT = {"R1": "(R1)", "R2": "(R2)", "R3": "(R3)", "S": "halt",
#               "T": r"$T$", "PT": r"$P$", "p": r"$p$"}


def pos(k, n):
    import math
    th = math.radians(90 - 360.0 * k / n)
    return th


def xy(k, n, rad):
    import math
    th = pos(k, n)
    return CX + rad * math.cos(th), CY + rad * math.sin(th)


def bundle_label(ov, i, m):
    items = [e for e in range(m) if ov["X"][i] >> e & 1]
    if not items:
        body = r"\emptyset"
    else:
        parts = []
        for e in items:
            c = ov["chore"].get(e)
            parts.append(r"\textcolor{%s}{\mathbf{%s}}" % (KEY[c], ch(e)) if c else ch(e))
        body = r"\{" + ",".join(parts) + r"\}"
    if i in ov["bundle"]:
        return r"{\color{%s}$%s$}" % (KEY[ov["bundle"][i]], body)
    return "$%s$" % body


def arc_draws(ov, prevE, n):
    """One entry per unordered pair: a double-headed line when both directions
    look identical, otherwise one (bent) arrow per direction."""
    E = ov["E"]
    out = []
    for a in range(n):
        for b in range(a + 1, n):
            st = {}
            for (u, v) in ((a, b), (b, a)):
                if (u, v) in E:
                    kind = "added" if (u, v) not in prevE else "present"
                elif (u, v) in prevE:
                    kind = "removed"
                else:
                    continue
                st[(u, v)] = (kind, ov["arc"].get((u, v)))
            if not st:
                continue
            if len(st) == 2 and st[(a, b)] == st[(b, a)]:
                out.append((a, b, "<->", st[(a, b)], None))
            else:
                bend = "bend left=11" if len(st) == 2 else None
                for (u, v), s in st.items():
                    out.append((u, v, "->", s, bend))
    return out


def arc_style(kind, colour):
    # Removed arcs must read as "gone": faint and finely dashed, clearly
    # lighter than the arcs that remain.
    if kind == "removed":
        return "gray!30, dash pattern=on 1.6pt off 1.6pt, line width=0.55pt"
    if colour:
        return "%s, line width=1.6pt" % KEY[colour]
    if kind == "added":
        return "black!80, line width=1.4pt"
    return "Slate!55, line width=0.75pt"


def render(ov, prevE, n, m):
    L = []
    L.append(r"\begin{tikzpicture}[>={Stealth[length=1.9mm,width=1.6mm]}, "
             r"agent/.style={circle, minimum size=7.6mm, inner sep=0pt, font=\normalsize\bfseries}, "
             r"chip/.style={rounded corners=1.5pt, minimum width=6.8mm, minimum height=4.5mm, "
             r"inner sep=0pt, font=\footnotesize}]")
    L.append(r"\useasboundingbox (0,0) rectangle (%.2f,%.2f);" % (W, H))
    L.append(r"\node[anchor=north west, text width=%.2fcm, font=\small, inner sep=0pt] "
             r"at (0,%.2f) {%s};" % (W, H, ov["caption"]))

    for k in range(n):                                               # agents
        x, y = xy(k, n, RAD)
        L.append(r"\node[agent, %s] (a%d) at (%.3f,%.3f) {%d};"
                 % (NODE_STYLE[ov["node"].get(k)], k, x, y, k + 1))
    for (u, v, tip, (kind, colour), bend) in arc_draws(ov, prevE, n):  # arcs
        path = "to[%s]" % bend if bend else "--"
        L.append(r"\draw[%s, %s] (a%d) %s (a%d);"
                 % (tip, arc_style(kind, colour), u, path, v))
    import math
    for k in range(n):                                               # bundles
        # Anchor on a side, never a diagonal: a wide label anchored at a
        # diagonal point extends back toward its own node.
        th = math.radians(90 - 360.0 * k / n)
        c, s = math.cos(th), math.sin(th)
        if abs(c) < 0.3:
            anchor = "south" if s > 0 else "north"
        else:
            anchor = "west" if c > 0 else "east"
        x, y = xy(k, n, RAD + 0.46)
        L.append(r"\node[anchor=%s, font=\footnotesize, inner sep=1pt] at (%.3f,%.3f) {%s};"
                 % (anchor, x, y, bundle_label(ov, k, m)))

    phase = r"Tao et al.'s rules" if ov["phase"] == "tao" else r"Our completion"
    L.append(r"\node[anchor=west, font=\small\bfseries, text=Slate] at (%.2f,5.75) {%s};"
             % (PANEL, phase))
    L.append(r"\node[anchor=west, font=\footnotesize, text=Muted] at (%.2f,5.25) "
             r"{Leftover chores, $|R|=%d$};" % (PANEL, len(ov["R"])))
    assert m <= 2 * CHIPS_PER_ROW, "chips would run into the why box"
    for q, e in enumerate(sorted(ov["R"])):
        cx = PANEL + 0.34 + CHIP_DX * (q % CHIPS_PER_ROW)
        cy = 4.74 - CHIP_DY * (q // CHIPS_PER_ROW)
        c = ov["chip"].get(e)
        sty = ("draw=%s, line width=1.2pt, fill=%s!30" % (KEY[c], KEY[c])) if c \
            else "draw=gray!60, fill=gray!8"
        L.append(r"\node[chip, %s] at (%.2f,%.2f) {$%s$};" % (sty, cx, cy, ch(e)))
    if not ov["R"]:
        L.append(r"\node[anchor=west, font=\footnotesize, text=Muted] at (%.2f,4.74) "
                 r"{none --- every chore is placed};" % PANEL)

    # The "why" box: the marginals and costs behind this step. storyboard()
    # computes every number in it from the cost tables and asserts it.
    col = KEY.get(ov["badge"], "Slate")
    L.append(r"\draw[%s, line width=0.8pt, rounded corners=3pt, fill=%s!6] "
             r"(%.2f,%.2f) rectangle (%.2f,%.2f);"
             % (col, col, PANEL, BOX_BOT, W - 0.02, BOX_TOP))
    # Ragged right, and no line breaks inside a formula or a word: justified
    # text stretched the spacing around = and < on a 6 cm measure. A formula
    # that does not fit moves whole to the next line; the fil stretch lets
    # the short line it leaves behind stand without an underfull warning.
    body = (r"\raggedright\rightskip=0pt plus 1fil\relpenalty=10000 \binoppenalty=10000 "
            r"\hyphenpenalty=10000 \exhyphenpenalty=10000 ")
    body += r"{\footnotesize\bfseries\color{%s!80!black}%s}" % (col, ov["title"])
    body += "".join(r"\par\vspace{2.5pt}" + w for w in ov["why"])
    body += r"\par"             # break the last paragraph under these settings too
    L.append(r"\node[anchor=north west, text width=%.2fcm, font=\scriptsize, "
             r"inner sep=0pt] at (%.2f,%.2f) {%s};"
             % (W - PANEL - 0.36, PANEL + 0.17, BOX_TOP - 0.14, body))
    # (was: a coloured rule badge at (PANEL, 2.15), and on the last overlay the
    #  vector p at (PANEL, 1.45) and its sum at (PANEL, 0.95); both now live in
    #  the why box)

    # Legend: each entry chained off the previous one, so spacing is even
    # whatever the label widths.
    legend = [("R1", "(R1) free chore"), ("R2", "(R2) rotation"), ("R3", "(R3) tail SCC"),
              ("S", "final $S$"), ("T", "$T$"), ("PT", r"$P\setminus T$")]
    for q, (k, text) in enumerate(legend):
        sty = (NODE_STYLE[k].replace("line width=2pt", "line width=1.2pt")
               .replace("line width=1.5pt", "line width=1.1pt"))
        where = "at (0.18,0.2)" if q == 0 else "at ([xshift=0.42cm]lt%d.east)" % (q - 1)
        anchor = "" if q == 0 else "anchor=west, "
        L.append(r"\node[circle, minimum size=3mm, inner sep=0pt, %s%s] (ls%d) %s {};"
                 % (anchor, sty, q, where))
        L.append(r"\node[anchor=west, font=\scriptsize, inner sep=2pt] (lt%d) at (ls%d.east) {%s};"
                 % (q, q, text))
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


def frames(run, ovs):
    n, m = run["n"], run["m"]
    out = [r"% BEGIN DEMO --- generated by report/slides/demo/build_demo.py.",
           r"% Do not edit by hand: change the script and re-run it.",
           r"% --------------------------------------------------------------------------"]
    for name, rgb in COLOURS:
        out.append(r"\definecolor{%s}{RGB}{%s}" % (name, rgb))
    out.append(r"\begin{frame}{The algorithm, run on an example}")
    out.append(r"  \transdissolve<2->[duration=0.25]")
    out.append(r"  \centering")
    prevE = ovs[0]["E"]
    for q, ov in enumerate(ovs, start=1):
        out.append(r"  \only<%d>{%%" % q)
        out.append(render(ov, prevE, n, m))
        out.append(r"  }%")
        prevE = ov["E"]
    out.append(r"\end{frame}")
    out.append(r"% END DEMO")
    return "\n".join(out) + "\n"


def splice(block):
    t = io.open(TALK, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in t else "\n"
    s = t.replace(nl, "\n")
    begin, end = "% BEGIN DEMO", "% END DEMO"
    if begin in s:
        i = s.index(begin)
        j = s.index(end, i) + len(end)
        while j < len(s) and s[j] == "\n":
            j += 1
        s = s[:i] + block + "\n" + s[j:]
    else:
        anchor = r"\begin{frame}{The algorithm}"
        i = s.index(anchor)
        j = s.index(r"\end{frame}", i) + len(r"\end{frame}")
        s = s[:j] + "\n\n" + block + s[j:]
    io.open(TALK, "w", encoding="utf-8", newline="").write(s.replace("\n", nl))


if __name__ == "__main__":
    run = build_and_verify()
    print("verified: costs dichotomous; run == algo1.twyz; completion == "
          "algo1.algorithm1; every step's rule re-checked; envy-free throughout; "
          "final (A,p) envy-free, p in {0,1}^n, sum p = %d <= %d, EF1"
          % (sum(run["p"]), run["n"] - 1))
    ovs = storyboard(run)
    print("why boxes: every stated marginal, cost and envy claim asserted")
    splice(frames(run, ovs))
    print("overlays: %d  ->  spliced into %s" % (len(ovs), TALK))
