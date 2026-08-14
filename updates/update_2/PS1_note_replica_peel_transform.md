# PS1 Working Note — The Replica Transform and the Peel Reformulation

**Version:** v1 (2026-08-02)
**Problem:** PS1 — envy-freeness with subsidies under *negative dichotomous* valuations (chores).
**Status:** four new results established (one machine-verified), one prior obstruction dissolved,
one new obstruction found and precisely characterised. Main conjecture still open.
**Attribution:** the replica construction of §2 is Mainak's. Everything downstream of it is
worked out jointly in the session of 2026-08-02.
**Predecessor:** the working note of 2026-07-31 (Theorems A–G, Theorem E obstruction). This note
does **not** restate that one; read it first. Cross-references below use its labels.
**Canonical files:** `glossary_fair_division_subsidies.md`, `paper_map_R1_to_R9.md`. Terminology
introduced here is flagged in §13 for promotion into the glossary; nothing here supersedes those files.

---

## 0. Purpose and how to use this note

This note records a change of coordinates for PS1. The chores problem is re-expressed as a *goods*
problem on a replicated item set, and then read dynamically as a process that removes chores from
agents one at a time. The payoff is that R3's proof orientation becomes correct again, and the
obstruction recorded as Theorem E stops being an obstruction. The cost is a new constraint —
coverage — which is now the sole remaining gap, and which is itself shown to be non-vacuous.

For LaTeX promotion: §§3–7 are theorem-proof material, ready to be sectioned. §§8–10 are
open-problem material and should be marked as such in any document shown to the professor.
Everything labelled **[Conjecture]** or **[Observation]** is *not* proved.

---

## 1. Setup (recap only — canonical definitions live in the glossary)

Instance $\langle [n], M, \{c_i\}_{i\in[n]}\rangle$ in **cost form**: $c_i := -v_i$, so each $c_i$
is monotone non-decreasing, $c_i(\emptyset)=0$, with all marginals in $\{0,1\}$. Envy-graph arc
weight and subsidy:

$$w_A(i,k) \;=\; v_i(A_k) - v_i(A_i) \;=\; c_i(A_i) - c_i(A_k), \qquad
p^*_i \;=\; \ell_A(i) \;=\; \max\{w_A(P) : P \text{ a directed path leaving } i\},$$

with the empty path counted, so $\ell_A(i) \ge 0$. Halpern–Shah transfers verbatim (its proof never
uses the sign of $v$): $A$ is envy-freeable $\iff$ $A$ minimises $\sum_i c_i(A_i)$ over reassignments
of its own bundles $\iff$ $G_A$ has no positive-weight cycle.

> **Target (unchanged).** Exhibit, for every instance, an allocation $A$ with no positive cycle in
> $G_A$ and $\ell_A(i) \le 1$ for all $i$. Integrality then forces $p \in \{0,1\}^n$ and total
> $\le n-1$.

**Invariant.** Throughout this note, a state is *invariant-respecting* (or "legal") if its graph has
no positive cycle and $\ell(i) \le 1$ for every $i$.

---

## 2. The idea

Fix the chore set $M = \{a_1,\dots,a_m\}$. Build a **replica instance** $\hat I$ with item set

$$\hat M \;=\; \{\, b_j^{(1)},\dots,b_j^{(n-1)} \;:\; j \in M \,\},$$

i.e. $n-1$ copies of a good $b_j$ for every chore $a_j$. For $S \subseteq \hat M$ let
$\tau(S) \subseteq M$ be the set of **types** occurring in $S$, and define

$$\boxed{\;\hat v_i(S) \;:=\; c_i(M) \;-\; c_i\big(M \setminus \tau(S)\big).\;}$$

The reading: *handing agent $i$ a copy of $b_j$ means relieving $i$ of chore $a_j$.* Since each chore
ends up with exactly one owner, exactly $n-1$ agents must be relieved of it — hence $n-1$ copies —
and no agent may be relieved of the same chore twice, hence at most one copy of each type per agent.
That last clause is the "catch" in the original idea and it is load-bearing: it is exactly what makes
$\hat v_i$ well-defined as a dual, since a second copy of a type has marginal $0$ and never $+1$ again.

**A warning about the naive reading.** If one instead declares that a copy of $b_j$ is worth $+1$ to
*every* recipient, the transform is false. An agent indifferent to $a_j$ would gain from $b_j$, every
$\hat v_i$ would collapse to $|\tau(S)|$, and the induced envy graph would be
$w(i,k) = |A_i| - |A_k|$ — the pure size term already isolated in **Theorem G**, carrying none of the
cost information. The correct reading is *marginal*: a copy of $b_j$ is worth to agent $i$ exactly
$i$'s marginal cost of $a_j$ on what remains of $i$'s workload, which for the agent being relieved is
$1$ precisely in the situation described in the original idea. All results below use the marginal
reading.

**Relation to prior work in this project.** This completes **Theorem D**. There the dual
$\hat v_i(S) = c_i(M) - c_i(M\setminus S)$ settled $n=2$ and was recorded as breaking at $n \ge 3$
"because $M \setminus A_i$ stops being a bundle of the partition." Replication is exactly the repair:
with $n-1$ copies of every type, the $n$ complements $M\setminus A_1,\dots,M\setminus A_n$ are
*simultaneously* realisable as disjoint bundles.

---

## 3. Theorem H (replica transform) — **established**

Call an allocation $B = (B_1,\dots,B_n)$ of *all* of $\hat M$ a **coverage allocation** if no $B_i$
contains two copies of the same type.

> **Theorem H.** Let $c_1,\dots,c_n$ be monotone with $c_i(\emptyset)=0$ and marginals in $\{0,1\}$.
> Then:
> **(i)** each $\hat v_i$ is a dichotomous valuation on $\hat M$ in the sense of R3;
> **(ii)** $\Phi$ below is a bijection between partitions of $M$ and coverage allocations of $\hat M$
> (up to relabelling copies of the same type);
> **(iii)** for corresponding $A$ and $B$, the envy graphs coincide arc for arc:
> $\hat w_B(i,k) = w_A(i,k)$ for all $i,k$.

### Proof

**(i) $\hat v_i$ is dichotomous.**

*Normalisation.* $\hat v_i(\emptyset) = c_i(M) - c_i(M\setminus\emptyset) = 0$.

*Monotonicity.* $S \subseteq S' \Rightarrow \tau(S)\subseteq\tau(S') \Rightarrow
M\setminus\tau(S) \supseteq M\setminus\tau(S')$, and $c_i$ is monotone, so
$c_i(M\setminus\tau(S)) \ge c_i(M\setminus\tau(S'))$, giving $\hat v_i(S) \le \hat v_i(S')$.

*Marginals in $\{0,1\}$.* Take $S \subseteq \hat M$ and a copy $b$ of type $j$ with $b \notin S$.
If $j \in \tau(S)$ then $\tau(S\cup\{b\}) = \tau(S)$ and the marginal is $0$. Otherwise
$M\setminus\tau(S\cup\{b\}) = \big(M\setminus\tau(S)\big)\setminus\{j\}$, so writing
$T := M\setminus\tau(S)$,

$$\hat v_i(S\cup\{b\}) - \hat v_i(S) \;=\; c_i(T) - c_i(T\setminus\{j\}) \;\in\;\{0,1\}$$

because $c_i$ has marginals in $\{0,1\}$ and $j \in T$. $\;\square$

**Consequence worth stating separately:** *the dual of a dichotomous cost function is a dichotomous
value function.* The class is closed under this duality, so R3's hypotheses apply to $\hat I$
verbatim — no additivity, submodularity or subadditivity is needed or assumed anywhere.

**(ii) The bijection.**

*Forward.* Given a partition $A = (A_1,\dots,A_n)$ of $M$, let $\Phi(A) = B$ where $B_i$ receives one
copy of each type in $M\setminus A_i$. Type $j$ is absent from exactly one bundle of $A$ (its owner's),
so exactly $n-1$ agents require a copy of $b_j$; the $n-1$ available copies suffice and are routed
injectively. Which physical copy goes to which agent is immaterial, since $\hat v_i$ depends on $S$
only through $\tau(S)$. By construction no $B_i$ holds a duplicate, so $B$ is a coverage allocation,
and $\bigcup_i B_i = \hat M$.

*Backward.* Given a coverage allocation $B$, the $n-1$ copies of type $j$ lie in $n-1$ *distinct*
bundles, so exactly one agent's bundle contains no copy of $j$. Define $\Psi(B) = A$ with
$A_i := M \setminus \tau(B_i)$. Then $j \in A_i$ for exactly one $i$, so $A$ is a partition of $M$.

*Inverse.* $\Psi(\Phi(A))_i = M \setminus (M\setminus A_i) = A_i$, and $\Phi(\Psi(B))$ agrees with $B$
up to which copy of a type sits where. $\;\square$

**(iii) Identical envy graphs.** For corresponding $A,B$ we have $\tau(B_k) = M\setminus A_k$, hence
$\hat v_i(B_k) = c_i(M) - c_i(A_k)$ and

$$\hat w_B(i,k) \;=\; \hat v_i(B_k) - \hat v_i(B_i) \;=\; \big(c_i(M)-c_i(A_k)\big) - \big(c_i(M)-c_i(A_i)\big)
\;=\; c_i(A_i) - c_i(A_k) \;=\; w_A(i,k). \;\square$$

Since the graphs are equal, envy-freeability, every $\ell(i)$, the whole set of feasible subsidy
vectors, and the invariant all transfer in both directions with no loss.

### Corollary H.1 (the exact gap) — **established**

> PS1's Conjecture 1 holds $\iff$ every replica instance $\hat I$ admits a **coverage** allocation
> $B$ with $\ell_{\hat B}(i) \le 1$ for all $i$.

R3 applied as a black box to $\hat I$ is legal by H(i) and returns some $B$ with
$\hat p \in \{0,1\}^n$ and total $\le n-1$. But R3 is free to place two copies of one type in one
bundle. If it does, that type is absent from $\ge 2$ bundles, i.e. the chore has $\ge 2$ owners, and
$\Psi(B)$ is not a partition. **The coverage constraint is the entire residual difficulty and the only
one.**

### Lemma H.2 (duplicate extraction is envy-neutral) — **established**

> Removing a duplicate copy from $B_x$ (a copy whose type occurs at least twice in $B_x$) leaves
> $\tau(B_x)$ unchanged, hence leaves every $\hat v_k(B_x)$ unchanged, hence leaves the entire envy
> graph unchanged.

*Proof.* Immediate from $\hat v_k(S)$ depending on $S$ only via $\tau(S)$. $\;\square$

So any R3 output may be stripped to a duplicate-free partial allocation for free. The difficulty is
never in removing duplicates; it is in **re-inserting** the stripped copies into agents that do not yet
hold that type.

---

## 4. The peel process

Read a coverage allocation as being built one copy at a time and translate back to chores. Giving
agent $x$ a copy of $b_j$ means *relieving $x$ of chore $j$*.

> **Definition (peel process).** A **state** is a workload profile $W = (W_1,\dots,W_n)$, $W_i \subseteq M$,
> such that $S_j := \{i : j \in W_i\} \ne \emptyset$ for every $j \in M$. Read $W_i$ as "agent $i$ is
> still on the hook for $W_i$" and $S_j$ as the **owner-candidate set** of chore $j$.
>
> - **Root:** $W_i = M$ for all $i$ — everyone on the hook for everything.
> - **Peel $\mathrm{peel}(x,j)$:** legal iff $j \in W_x$ and $|S_j| \ge 2$; sets $W_x \leftarrow W_x\setminus\{j\}$.
> - **Permutation:** replace $W$ by $W_\sigma := (W_{\sigma(1)},\dots,W_{\sigma(n)})$ for a permutation $\sigma$.
> - **Terminal:** $|S_j| = 1$ for every $j$. The unique element of $S_j$ is the **survivor**, i.e. the
>   owner of chore $j$; the induced allocation is $A_i = \{j : S_j = \{i\}\}$.
> - **Graph:** $w_W(i,k) = c_i(W_i) - c_i(W_k)$; the root graph is identically zero.

By Theorem H, a peel state is exactly a duplicate-free partial allocation of $\hat M$, a peel is
exactly R3's insertion of one good into one bundle, a permutation is exactly R3's bundle
reassignment, and terminal states are exactly coverage allocations. Nothing is lost or added in the
translation.

### Lemma P (peel dynamics) — **established**

> $\mathrm{peel}(x,j)$ changes only the arcs incident to $x$, and with these signs, where
> $\mu_k := c_k(W_x) - c_k(W_x\setminus\{j\})$ is $k$'s marginal cost of $j$ on $x$'s residual workload:
>
> $$\Delta w(k,x) \;=\; +\mu_k \;\in\;\{0,1\} \quad (k \ne x), \qquad
> \Delta w(x,k) \;=\; -\mu_x \;\in\;\{-1,0\} \quad (k \ne x).$$

*Proof.* Only $W_x$ changes. For $k \ne x$: $w(k,x) = c_k(W_k) - c_k(W_x)$, and $c_k(W_x)$ drops by
$\mu_k$, so $w(k,x)$ rises by $\mu_k$. For arcs out of $x$: $w(x,k) = c_x(W_x) - c_x(W_k)$, and
$c_x(W_x)$ drops by $\mu_x$. Arcs between two agents $\ne x$ involve neither $W_x$ nor $c_x$. $\;\square$

### The orientation reversal — why this is the point

| frame | move | receiver's **incoming** arcs | receiver's **outgoing** arcs | who should receive |
|---|---|---|---|---|
| R3, goods | insert good into $B_x$ | rise by $\mu$ | fall | a **most**-subsidised agent, $x \in M(p)$ |
| PS1, insertion frame (prior note) | insert chore into $A_x$ | fall | **rise** by $1$ | an agent with $p_x = 0$ — the *least* subsidised |
| PS1, **peel frame** (this note) | relieve $x$ of chore $j$ | **rise** by $\mu_k$ | fall | a **most**-subsidised agent |

The prior note's Theorem E obstruction was precisely this sign clash: R3's `FINDSINK` navigates to an
agent whose tentative subsidy was $\ge 2$, which in the goods world is automatically in $M(p)$ — the
set the algorithm wants — but in the chore-insertion world is automatically an agent with $p_u = 1$,
i.e. exactly the agent who must **not** receive the chore. In the peel frame the quantity handed out
is *relief*, relief correctly flows to the most-envious agents, and R3's orientation points the right
way again. `EXTEND`'s requirement $\kappa \in M(q)$ and `FINDSINK`'s walk inside $M(p)$ both become
meaningful rather than self-defeating.

---

## 5. What transfers from R3, and what does not

**Transfers, mechanically, by Theorem H.** R3's Lemma 3 (permuted allocations with permuted
subsidies), Lemma 8 (`EXTEND` decides extendability correctly), Lemma 9 (`FINDSINK`'s candidates lie
in $M(p)$; each tentative allocation is envy-freeable), Lemma 10 (the walk visits each agent at most
once, via the path argument in $G_A$), Lemma 11 (the returned agent keeps $p \in \{0,1\}^n$),
Propositions 5 and 6. None of these proofs uses anything about goods beyond dichotomous marginals, and
all of their objects are graph-level, so Theorem H(iii) carries them over unchanged. Permutations
remain legal in our frame: permuting whole workloads relabels each $S_j$ without changing $|S_j|$, so
coverage feasibility is preserved.

**Does not transfer: Theorem A.** In the insertion frame, adding a chore that is free *for the
receiver* was unconditionally safe (every arc weakly decreased). Lemma P shows the peel-frame safe
move is the one that is free *for everyone else*:

> **Lemma P.1 (spectator-free peel) — established.** If $\mu_k = 0$ for all $k \ne x$, then
> $\mathrm{peel}(x,j)$ weakly decreases every arc weight, hence $\ell$ pointwise, and preserves
> envy-freeability — whatever $\mu_x$ is.

*Proof.* By Lemma P, incoming arcs at $x$ are unchanged and outgoing arcs at $x$ change by
$-\mu_x \le 0$; all other arcs are untouched. Path and cycle weights are sums of arc weights. $\square$

The safety condition migrates from the recipient's marginal to the spectators' marginals — which is
precisely R3's goods-side safety structure, as the identification predicts. **The hard case is now a
chore $j$ and an agent $x$ such that some other agent $k$ has $\mu_k = 1$.**

**Does not transfer: the coverage constraint has no R3 analogue.** R3 may put any good in any bundle.
A peel demands $x \in S_j$, and a type is peelable only while $|S_j|\ge 2$. Everything that goes wrong
below goes wrong here.

---

## 6. The Theorem E witness dissolves — **machine-verified**

Recall the witness from the prior note: $M = \{a_1,a_2,g\}$, $c_1(S) = \max(0,|S|-1)$ (dichotomous
and supermodular — legal, the class is not restricted to submodular), $c_2 = c_3 = |S|$. In the
insertion frame, the state $A = (\{a_1,a_2\},\emptyset,\emptyset)$ with $g$ pending is a legal state of
the invariant from which *every* insertion of $g$ breaks the $\{0,1\}$ bound, although the instance has
a zero-subsidy solution. Two things happen in the peel frame.

### 6.1 The trap state is refused before it can form

Its peel-frame counterpart is $W = (\{a_1,a_2,g\},\{g\},\{g\})$, and

$$w_W(1,2) \;=\; c_1(\{a_1,a_2,g\}) - c_1(\{g\}) \;=\; 2 - 0 \;=\; 2 \;\Longrightarrow\; \ell(1) = 2.$$

The invariant is already violated, so no invariant-respecting peel schedule passes through this state.

**Why the two frames disagree — the conditioned-remainder principle.** At a stage where the finished
types form a partial assignment $A^{(t)}$ and the untouched types form $R$, the peel-frame arc is

$$c_i\big(A^{(t)}_i \cup R\big) - c_i\big(A^{(t)}_k \cup R\big), \qquad\text{not}\qquad c_i\big(A^{(t)}_i\big) - c_i\big(A^{(t)}_k\big).$$

Every comparison is made *conditioned on the common unfinished remainder*. For additive costs the
$R$-terms cancel and the frames coincide — consistent with the additive case already being closed by
Theorem C. For non-additive costs they differ, and on the witness it is exactly the supermodularity of
$c_1$ that the conditioning catches: with $g$ still pending, loading agent 1 with both $a$'s already
costs $2$, and the peel invariant sees it. **The insertion invariant was blind to pending load; the
peel invariant has hindsight built in.** This is, in my judgement, the substantive content of the
change of coordinates, and the sentence to keep if the note has to be compressed.

### 6.2 An invariant-respecting schedule reaches the zero-subsidy allocation

Six peels, every one of them the hard case ($\mu_k = 1$ for all $k$ — this instance never offers a
free move), invariant holding throughout. Verified by `peel.py`.

| step | move | resulting $W$ | $\ell$ | $\sum\ell$ |
|---|---|---|---|---|
| 0 | root | $(\{a_1a_2g\},\{a_1a_2g\},\{a_1a_2g\})$ | $(0,0,0)$ | 0 |
| 1 | relieve 1 of $g$ | $(\{a_1a_2\},\{a_1a_2g\},\{a_1a_2g\})$ | $(0,1,1)$ | 2 |
| 2 | relieve 2 of $g$ — owner$(g)=3$ | $(\{a_1a_2\},\{a_1a_2\},\{a_1a_2g\})$ | $(0,0,1)$ | 1 |
| 3 | relieve 3 of $a_1$ | $(\{a_1a_2\},\{a_1a_2\},\{a_2g\})$ | $(0,0,0)$ | 0 |
| 4 | relieve 1 of $a_2$ | $(\{a_1\},\{a_1a_2\},\{a_2g\})$ | $(0,1,1)$ | 2 |
| 5 | relieve 2 of $a_1$ — owner$(a_1)=1$ | $(\{a_1\},\{a_2\},\{a_2g\})$ | $(0,0,1)$ | 1 |
| 6 | relieve 3 of $a_2$ — owner$(a_2)=2$ | $(\{a_1\},\{a_2\},\{g\})$ | $(0,0,0)$ | 0 |

Terminal allocation $(\{a_1\},\{a_2\},\{g\})$, the known zero-subsidy solution.

**What this does and does not establish.** It establishes that the peel template is **not killed by
the existing obstruction**: the instance that defeats every insertion order is handled by peeling with
the full invariant intact. It does not establish that the template always works — see §7. Note also
that it satisfies the prior note's post-mortem requirement ("any correct proof must be allowed to
re-open already-allocated bundles") in the cleanest available way: **peeling never commits a chore's
owner until the last peel of that type, so ownership is a deferred decision and there is nothing to
re-open.**

---

## 7. The new obstruction: peel dead ends — **machine-verified**

The natural conjecture is local: *from every legal non-terminal state some legal move exists*. It is
**false**, and the same witness refutes it.

> **Refuted.** There exist invariant-respecting, non-terminal peel states from which **no** sequence of
> peels and permutations reaches a terminal state without violating the invariant.

Complete backward fixed-point computation over the witness's entire state space (`peel3.py`; all
$7^3 = 343$ states, both move types, no heuristics):

| quantity | value |
|---|---|
| states total | 343 |
| invariant-respecting states | 175 |
| terminal (partition) states that are invariant-respecting | 6 of 27 |
| states from which a terminal is reachable within the invariant | 166 |
| **invariant-respecting dead ends** | **9** |
| root is good | **yes** |

Smallest dead end: $W = (\{a_1,a_2\},\{g\},\{g\})$. It is legal ($\ell = (1,0,0)$), the only peelable
type is $g$, and both continuations fail: relieving 2 or 3 of $g$ creates a weight-2 path out of
agent 1. Permutations do not help (checked exhaustively; the profile $(\{g\},\{a_1a_2\},\{g\})$ is
legal but its two continuations fail identically).

### 7.1 What the dead ends are, in R3 terms

This is the sharpest statement in the note. At $W = (\{a_1,a_2\},\{g\},\{g\})$, the remaining
unallocated copy is a copy of $b_g$. Its three possible recipients:

- agent 2 or 3 — a genuine peel; **violates the invariant**;
- agent 1 — who *already holds* a copy of $b_g$. This is a **duplicate**, it is perfectly legal in
  $\hat I$, and by Lemma H.2 it changes nothing at all in the graph, so R3 accepts it.

So **R3's algorithm never gets stuck on $\hat I$. It gets stuck only in the sense that its only legal
move is to spend a copy on a duplicate — and spending a copy on a duplicate is exactly the loss of
coverage.** If agent 1 takes the second $b_g$, chore $g$ ends with owner-candidate set $\{2,3\}$: two
owners, not a partition. Corollary H.1 is therefore not merely a formal restatement; the gap it names
is realised.

### 7.2 Structure of the dead ends — the balance signal

All nine dead ends of the witness have the same shape: **one agent is already committed to a
two-element terminal bundle.** They are exactly the $3$ choices of which pair $\times$ $3$ choices of
which agent. Correspondingly, all six reachable terminals are the six perfect matchings, and in this
instance the only invariant-respecting partitions are the matchings.

This is the same signal as **Theorem G** (chores $=$ goods $+$ cardinality balancing) and as R2's
balancedness guarantee, arriving from a third direction. It suggests the missing ingredient in the
peel rule is a **balance discipline**, not a subsidy-based one. Consistent with this, restricting
recipients to $\arg\max_i \ell(i)$ — the direct mirror of R3's $M(p)$ — shrinks the reachable state
space but does **not** avoid the dead ends. A subsidy-based rule alone is not enough. **[Observation,
single instance — do not generalise without more data.]**

---

## 8. The reduced open problem

> **Conjecture H1 (local extendability).** From every legal non-terminal state, some legal move exists.
> **— REFUTED**, §7.

> **Conjecture H1′ (reachability).** From the **root**, some sequence of peels and permutations reaches
> a terminal state with the invariant holding at every intermediate state. **— OPEN.** True on the
> witness; this is the statement that implies PS1's Conjecture 1.

*Why H1′ suffices.* The root graph is identically zero, so the invariant holds there. If a legal
schedule reaches a terminal state $W^{\mathrm{end}}$, the induced allocation $A$ has $G_A = G_{W^{\mathrm{end}}}$
with no positive cycle and $\ell_A(i)\le 1$ for all $i$. Integrality of the $c_i$ forces
$p = \ell_A \in \{0,1\}^n$, and the endpoint of a maximum-weight path has $\ell = 0$, giving total
$\le n-1$. This is the Target of §1, unchanged.

*Why H1′ is not automatic.* H1′ is a reachability statement about a state space with genuine dead
ends. A proof must supply a **rule** — a way of choosing the next peel — that provably never enters
the bad region, or a potential/exchange argument that avoids the state space altogether. The two
resources R3 never had:

1. **Scheduling freedom.** Many types are unfinished at once; we need only one of them to admit a
   legal peel, not a specific one.
2. **$|S_j| \ge 2$.** A peelable type always has at least two candidate recipients, so the forbidden
   recipient set is never all of $[n]$.

*What a proof must rule out.* A **deadlock** is a legal non-terminal state at which, for every
unfinished type $j$ and every permutation, no recipient in $S_j$ preserves the invariant. §7 shows
deadlocks exist; H1′ asks only that the *root* avoid them. So the target theorem has the shape:
*there is a peel rule under which no deadlock is ever entered.* The balance signal of §7.2 is the
first candidate for what that rule must enforce.

---

## 9. A subclass that may fall first — **[Conjecture-level]**

On type space, the dual of a **supermodular** dichotomous cost is submodular with binary marginals,
i.e. a **matroid rank function**; lifting through $\tau$ to the copies is parallel extension of that
matroid, still an MRF. Additive costs dualise to partition-matroid ranks. Hence:

> **[Observation]** Supermodular dichotomous chores are exactly MRF-goods coverage problems, and the
> Theorem E witness lands entirely inside this class ($c_1$ dualises to the rank of $U_{2,3}$, parallel
> extended).

MRF is where the corpus's machinery is strongest (exchange properties in R5, R8; matroid-rank results
cited in R3's related work). So:

> **Intermediate target.** PS1 restricted to supermodular dichotomous costs, attacked via basis
> exchange in the parallel-copy matroid, sitting between Theorem C (binary additive, closed) and the
> full conjecture.

Not established. The reduction direction (supermodular $\to$ MRF) should be written out carefully
before being relied on; the parallel-extension step in particular deserves a full proof.

---

## 10. Status ledger

**Established (proof in this note):**
- **Theorem H** — replica transform; dichotomous costs dualise to dichotomous values; bijection with
  coverage allocations; envy graphs identical arc for arc. Completes Theorem D to all $n$.
- **Corollary H.1** — PS1's Conjecture 1 $\iff$ every replica instance has a *coverage* allocation
  with $\ell \le 1$. Coverage is the sole gap.
- **Lemma H.2** — duplicate extraction is envy-neutral.
- **Lemma P** — peel dynamics: incoming arcs at the relieved agent rise, outgoing fall. Orientation
  reversal relative to the insertion frame.
- **Lemma P.1** — spectator-free peels are unconditionally safe (the peel-frame replacement for
  Theorem A; the safety condition moves from recipient to spectators).

**Machine-verified (`peel.py`, `peel3.py`):**
- The Theorem E trap state violates the peel invariant; the witness admits a 6-step legal schedule to
  its zero-subsidy allocation.
- The witness's full state space: 175 legal states, 166 good, **9 dead ends**, root good, all
  reachable terminals are perfect matchings.

**Refuted:** Conjecture H1 (local extendability).

**Open:** Conjecture H1′ (reachability from the root) — the statement that implies PS1's Conjecture 1.
Also open: the balance rule of §7.2, and the MRF subclass of §9.

**Superseded framing:** the "insert chores one at a time" template remains dead (prior note,
Theorem E). It is not revived here; it is *replaced*.

---

## 11. Next steps, in priority order

1. **Extend the exhaustive search to the peel frame.** Reuse the `gen.py`/`search.py` harness over the
   full $n=3, m=3$ dichotomous family (9,880 instances up to agent symmetry). For each instance
   compute: is the root good? how many dead ends? Any instance with a *bad root* is a counterexample to
   H1′ and, via §8, to Conjecture 1 itself. **This is the single highest-value experiment available
   right now** — it tests the main conjecture directly, not a proxy.
2. **Characterise dead ends.** Across that family, test the §7.2 hypothesis: is every dead end a state
   committed to an unbalanced terminal? If yes, formulate the balance rule precisely and test whether
   greedy-under-that-rule reaches a terminal without backtracking.
3. **Candidate rules to test**, in order: (a) balance-first — peel so that a balanced terminal remains
   reachable; (b) spectator-free peels first (Lemma P.1), ties broken by balance; (c)
   $\arg\max_i \ell(i)$ with a balance tie-break — noting (c) alone already fails on the witness.
4. **Port R3's Lemmas 9 and 10 with the $S_j$ constraint attached**, and attempt a Hall-type counting
   argument across types: at a legal state, count (peelable types) $\times$ (candidate recipients)
   against (forbidden pairs) to show a legal peel exists whenever the state is reachable from the root.
5. **Randomised search** $n \in \{3,4,5\}$, $m \in \{4,5,6\}$ via `fast.py`, root-goodness only.
6. **MRF subclass** (§9): write the supermodular $\to$ matroid reduction properly, then attempt basis
   exchange.
7. **Literature check before investing further.** Confirm that "dichotomous chores with subsidy" is not
   already published. Best current published bound covering this class is R9 (doubly monotone, from an
   EF1 allocation): $n-1$ per agent, $n(n-1)/2$ total. Our claim would be a factor-$n$ improvement on
   this subclass — the same factor R3 gains over R2.

All of the above is CPU-scale; nothing here needs a GPU.

---

## 12. Terms to promote into the canonical files

For `glossary_fair_division_subsidies.md` (append, do not restate here):
**replica instance** $\hat I$; **type map** $\tau$; **dual valuation** $\hat v_i(S) = c_i(M)-c_i(M\setminus\tau(S))$;
**coverage allocation**; **duplicate copy**; **peel process**, **peel**, **workload profile** $W$;
**owner-candidate set** $S_j$; **survivor**; **spectator-free peel**; **conditioned-remainder
principle**; **peel dead end / deadlock**.

For `paper_map_R1_to_R9.md`: no change required. R3's entry may gain one line noting that its
dichotomous class is closed under the cost-dual of Theorem H, which is why R3 applies to $\hat I$
without additional hypotheses.

---

## 13. Files

- `peel.py` — verifies the 6-step schedule, the trap-state refusal, and runs a DFS peel search on the
  Theorem E witness.
- `peel3.py` — clean backward fixed-point over the witness's entire 343-state space with both move
  types; produces the table in §7.
- Prior session: `gen.py`, `search.py`, `fast.py`, `msw.py`, `tiebreak.py`, `localsearch.py`,
  `deadend.py`, `binadd.py`.

---

## 14. Changelog

- **v1 (2026-08-02)** — First version. Introduces the replica transform (Theorem H), the peel
  reformulation, Lemmas H.2, P, P.1; dissolves the Theorem E obstruction; refutes Conjecture H1 and
  isolates Conjecture H1′. Replica construction due to Mainak.
