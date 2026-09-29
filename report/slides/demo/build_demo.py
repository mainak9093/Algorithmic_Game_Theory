# -*- coding: utf-8 -*-
"""
Build the algorithm walkthrough frames and splice them into ../talk.tex.

    python build_demo.py

The instance below was found by search_demo.py (seed 3). Nothing is drawn by
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
     sum p <= n - 1, and A is EF1.

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

INSTANCE = {
    "n": 6, "m": 15, "K": [5, 6, 6, 4, 6, 6],
    "grp": [[4, 3, 1, 0, 3, 0, 3, 2, 2, 4, 2, -1, 1, -1, 1],
            [4, 0, 4, 2, 4, 3, 4, 1, 2, 4, 5, 2, 3, 5, 0],
            [2, 4, 0, 0, 5, 5, 3, -1, 4, 5, 0, 4, 0, 0, 4],
            [2, 3, 2, 2, 3, 1, 3, 1, 1, 1, 3, 2, 0, 0, 1],
            [3, 5, 5, 0, 1, 1, 0, 1, 2, 1, 3, -1, 4, 0, 1],
            [0, 3, 5, 2, -1, 4, -1, -1, 0, 3, 4, -1, 2, 3, 2]],
    "a": [1, 1, 0, 0, 0, 0],
    "b": [2, 2, 3, 2, 2, None],
}

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

    return dict(n=n, m=m, ev=ev, snaps=snaps, X=tuple(X), R=sorted(R),
                S=sorted(S), T=list(T), P=sorted(P), rounds=rounds,
                E=frozenset(E), A=tuple(A), p=list(p))


# ==========================================================================
# Overlays: what each page of the animation shows
# ==========================================================================

def agents(xs):
    return ",".join(str(a + 1) for a in sorted(xs))


def ch(e):
    return "e_{%d}" % (e + 1)


def overlay(snap, caption, phase, **kw):
    ov = dict(X=snap["X"], R=snap["R"], E=snap["E"], caption=caption,
              phase=phase, node={}, arc={}, chore={}, bundle={}, chip={},
              badge=None, pvec=None)
    ov.update(kw)
    return ov


def storyboard(run):
    n, ev, snaps = run["n"], run["ev"], run["snaps"]
    ovs = [overlay(snaps[0],
                   r"Start: every bundle is empty, so everyone is indifferent "
                   r"to everything --- the equality graph is complete.",
                   "tao")]
    k = 0
    while k < len(ev):
        x = ev[k]
        if x[0] == "R1":
            j = k
            while j < len(ev) and ev[j][0] == "R1" and j - k < R1_CHUNK:
                j += 1
            batch = ev[k:j]
            moves = ", ".join(r"$%s\!\to\!%d$" % (ch(b[1]), b[2] + 1) for b in batch)
            ovs.append(overlay(
                snaps[j], r"\textbf{(R1)} free chores placed: " + moves + ".", "tao",
                node={b[2]: "R1" for b in batch},
                chore={b[1]: "R1" for b in batch}, badge="R1"))
            k = j
            continue
        if x[0] == "R2":
            _, e, i, jj, cyc = x
            loop = [i] + list(cyc[:-1])            # i -> j -> ... -> back to i
            arcs = {(loop[t], loop[(t + 1) % len(loop)]): "R2" for t in range(len(loop))}
            path = r"\!\to\!".join(str(a + 1) for a in loop + [i])
            ovs.append(overlay(
                snaps[k],
                r"\textbf{(R2)} no free chore left, but the arc $%d\!\to\!%d$ lies "
                r"on the cycle $%s$." % (i + 1, jj + 1, path), "tao",
                node={a: "R2" for a in cyc}, arc=arcs, chip={e: "R2"}, badge="R2"))
            ovs.append(overlay(
                snaps[k + 1],
                r"\textbf{(R2)} each agent on the cycle takes the bundle its arc "
                r"points to; then agent %d takes $%s$." % (i + 1, ch(e)), "tao",
                node={a: "R2" for a in cyc}, bundle={a: "R2" for a in cyc},
                chore={e: "R2"}, badge="R2"))
            k += 1
            continue
        if x[0] == "R3":
            _, tail, gave, _ = x
            inner = {(a, b): "R3" for (a, b) in snaps[k]["E"] if a in tail and b in tail}
            ovs.append(overlay(
                snaps[k],
                r"\textbf{(R3)} no free chore and no rotation: the tail SCC is "
                r"$\{%s\}$, and $|R| = %d \ge %d$." % (agents(tail), len(snaps[k]["R"]),
                                                        len(tail)),
                "tao", node={a: "R3" for a in tail}, arc=inner,
                chip={e: "R3" for e, _ in gave}, badge="R3"))
            moves = ", ".join(r"$%s\!\to\!%d$" % (ch(e), a + 1) for e, a in gave)
            ovs.append(overlay(
                snaps[k + 1],
                r"\textbf{(R3)} one leftover chore to each member: " + moves + ".",
                "tao", node={a: "R3" for a in tail},
                chore={e: "R3" for e, _ in gave}, badge="R3"))
            k += 1
            continue
        # HALT
        _, tail, _ = x
        inner = {(a, b): "S" for (a, b) in snaps[k]["E"] if a in tail and b in tail}
        ovs.append(overlay(
            snaps[k],
            r"\textbf{Halt.} The tail SCC $S=\{%s\}$ has %d agents, but only "
            r"$r=%d$ chore%s left." % (agents(tail), len(tail), len(snaps[k]["R"]),
                                       "" if len(snaps[k]["R"]) == 1 else "s"),
            "tao", node={a: "S" for a in tail}, arc=inner, chip={e: "S" for e in snaps[k]["R"]},
            badge="S"))
        k += 1

    # ---- our completion ---------------------------------------------------
    S, T, R, rounds, E = run["S"], run["T"], run["R"], run["rounds"], run["E"]
    done = dict(X=run["A"], R=frozenset(), E=E)
    sn = {a: "S" for a in S}
    sarcs = {(a, b): "S" for (a, b) in E if a in S and b in S}

    nodes = dict(sn)
    for t in T:
        nodes[t] = "T"
    moves = ", ".join(r"$%s\!\to\!%d$" % (ch(R[q]), T[q] + 1) for q in range(len(T)))
    ovs.append(overlay(
        done,
        r"\textbf{Our completion.} The leftover chore%s go%s to distinct agents "
        r"$T=\{%s\}\subseteq S$: " % ("" if len(R) == 1 else "s",
                                       "es" if len(R) == 1 else "", agents(T)) + moves + ".",
        "ours", node=dict(nodes), arc=dict(sarcs), chore={e: "T" for e in R}, badge="T"))

    paid = set(T)
    arcs = dict(sarcs)
    for rd in rounds:
        pull = [(a, b) for (a, b) in E if a in rd and b in paid]
        for a in rd:
            nodes[a] = "PT"
        for pr in pull:
            arcs[pr] = "PT"
        via = ", ".join(r"$%d\!\to\!%d$" % (a + 1, b + 1) for (a, b) in sorted(pull))
        first = rd is rounds[0]
        ovs.append(overlay(
            done,
            (r"\textbf{Subsidy set $P$:} " if first else r"\textbf{$P$ grows again:} ")
            + r"agent%s $%s$, outside $S$, %s an equality arc into $P$ (%s), so %s paid."
            % ("" if len(rd) == 1 else "s", agents(rd), "has" if len(rd) == 1 else "have",
               via, "it is" if len(rd) == 1 else "they are"),
            "ours", node=dict(nodes), arc=dict(arcs), badge="PT"))
        paid |= set(rd)

    p = run["p"]
    unpaid_S = [a for a in S if a not in T]
    outsiders = [a for a in range(run["n"]) if a not in S and p[a] == 0]
    tail = r"Unpaid: $S\setminus T=\{%s\}$" % agents(unpaid_S)
    if outsiders:
        tail += r" and agent%s $%s$" % ("" if len(outsiders) == 1 else "s", agents(outsiders))
    ovs.append(overlay(
        done,
        r"\textbf{Result.} One unit to each agent of $P$: envy-free, total "
        r"$%d \le n-1 = %d$. " % (sum(p), run["n"] - 1) + tail + ".",
        "ours", node=dict(nodes), arc=dict(arcs), badge="p", pvec=p))
    return ovs


# ==========================================================================
# TikZ
# ==========================================================================

W, H = 13.8, 6.8                    # fixed canvas: no jitter between overlays
CX, CY, RAD = 4.6, 3.2, 1.8         # the agent polygon
PANEL = 9.3                         # left edge of the right-hand panel
CHIPS_PER_ROW = 4

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
BADGE_TEXT = {"R1": "(R1)", "R2": "(R2)", "R3": "(R3)", "S": "halt",
              "T": r"$T$", "PT": r"$P$", "p": r"$p$"}


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
             r"chip/.style={rounded corners=1.5pt, minimum width=9.4mm, minimum height=4.8mm, "
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
    for q, e in enumerate(sorted(ov["R"])):
        cx = PANEL + 0.5 + 1.05 * (q % CHIPS_PER_ROW)
        cy = 4.72 - 0.6 * (q // CHIPS_PER_ROW)
        c = ov["chip"].get(e)
        sty = ("draw=%s, line width=1.2pt, fill=%s!30" % (KEY[c], KEY[c])) if c \
            else "draw=gray!60, fill=gray!8"
        L.append(r"\node[chip, %s] at (%.2f,%.2f) {$%s$};" % (sty, cx, cy, ch(e)))
    if not ov["R"]:
        L.append(r"\node[anchor=west, font=\footnotesize, text=Muted] at (%.2f,4.72) "
                 r"{none --- every chore is placed};" % PANEL)

    if ov["badge"]:
        b = ov["badge"]
        col = KEY.get(b, "Slate")
        L.append(r"\node[anchor=west, rounded corners=2pt, draw=%s, line width=1pt, "
                 r"fill=%s!15, font=\small\bfseries, inner sep=3pt] at (%.2f,2.15) {%s};"
                 % (col, col, PANEL, BADGE_TEXT[b]))
    if ov["pvec"] is not None:
        L.append(r"\node[anchor=west, font=\small] at (%.2f,1.45) {$p=(%s)$};"
                 % (PANEL, ",".join(str(q) for q in ov["pvec"])))
        L.append(r"\node[anchor=west, font=\small] at (%.2f,0.95) "
                 r"{$\textstyle\sum_i p_i=%d\le n-1=%d$};" % (PANEL, sum(ov["pvec"]), n - 1))

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
    splice(frames(run, ovs))
    print("overlays: %d  ->  spliced into %s" % (len(ovs), TALK))
