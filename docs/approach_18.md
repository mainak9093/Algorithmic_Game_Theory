# Approach 18 — PS2 at $n=3$ is a finite problem about a $3\times3$ matrix

*A reduction that removes envy graphs, longest paths, prices and potential
functions from the statement entirely, replacing them with three explicit
forbidden patterns. Machine-verified end to end.*

---

## 0. The result

> **Reduction.** For $n = 3$, whether a multiset of bundles admits a valid
> assignment depends **only** on the $3\times3$ matrix
> $$\hat g_i(j) \;=\; \min\Bigl(\max_k v_i(B_k) - v_i(B_j),\ 2\Bigr),$$
> each of whose rows contains a zero. There are $19^3 = 6{,}859$ such patterns;
> exactly **624 are forbidden**.

Verified against the envy-graph implementation on **102,060 allocations at
$m = 3,4,5$: zero mismatches.**

> **Obstructions.** Every forbidden pattern dominates, entrywise, one of **three**
> canonical patterns — up to relabelling agents and bundles, an orbit of 30:
>
> | | pattern | meaning |
> |---|---|---|
> | **C** | $\begin{smallmatrix}0&0&2\\0&0&2\\0&0&2\end{smallmatrix}$ | **all three** agents rank one bundle $\ge 2$ below their best — nobody can be handed it |
> | **A** | $\begin{smallmatrix}0&0&0\\0&2&2\\0&2&2\end{smallmatrix}$ | **two** agents rank one bundle $\ge 2$ above both others — both must have it |
> | **B** | $\begin{smallmatrix}0&0&1\\0&1&2\\0&1&2\end{smallmatrix}$ | the mixed case |

Domination is **necessary** for a pattern to be forbidden, and not sufficient —
90 valid patterns also dominate one. That asymmetry is the useful direction:

> **Soundness (a theorem, not a measurement).** An allocation whose gap matrix
> dominates none of C, A, B is **valid**.

leaving one existence statement:

> **(AVOID), open.** Every general binary instance with $n=3$ admits an
> allocation whose gap matrix dominates none of the three obstructions.

**(AVOID) + soundness $\Rightarrow$ PS2 for $n=3$.** And (AVOID) is a statement
about bundle values only — no envy graph, no longest path, no price vector, no
potential, no descent.

---

## 1. Why validity collapses to a ternary matrix

Start from the verified reformulation of approach 16 §1: an allocation is valid
iff for some $q \in \set{0,1}^3$ every agent holds a bundle maximising
$v_i(B_j) + q_j$. Writing $g_i(j) = \max_k v_i(B_k) - v_i(B_j) \ge 0$,

$$v_i(B_j) + q_j \;=\; \Bigl(\max_k v_i(B_k)\Bigr) - g_i(j) + q_j,$$

so agent $i$ demands whichever $j$ maximises $q_j - g_i(j)$. Every row of $g$
has a zero, so that maximum is always at least $0$, and it is at most $1$.
Hence exactly two branches:

- **if some $j$ has $g_i(j) = 0$ and $q_j = 1$:** the maximum is $1$ and
  $D_i = \set{j : g_i(j)=0,\ q_j=1}$;
- **otherwise:** the maximum is $0$ and
  $D_i = \set{j : g_i(j)=0} \cup \set{j : g_i(j)=1,\ q_j=1}$.

In both branches the only thing ever consulted is whether $g_i(j)$ is $0$, $1$,
or **at least** $2$. Everything above $2$ is invisible. $\square$

Rows are vectors over $\set{0,1,2}$ containing a zero: $27 - 8 = 19$ of them,
hence $6{,}859$ patterns. Validity of each is decided by trying all $8$ price
vectors and running Hall — a finite computation, done once.

## 2. A warning: more indifference can *hurt*

The natural guess is that lowering a gap makes matching easier, so that the
forbidden set is upward closed. **It is not** — 54 patterns become forbidden
when a single entry is lowered. Verified by hand as well as by machine:

$$\begin{pmatrix}0&1&1\\0&1&2\\0&1&2\end{pmatrix} \text{ is valid,} \qquad
\begin{pmatrix}0&\mathbf{0}&1\\0&1&2\\0&1&2\end{pmatrix} \text{ is forbidden.}$$

The mechanism is the first branch above. When agent $i$ has a *second* top
bundle and that bundle carries a price, her demand **shrinks** to
$Z_i \cap Q$ — she is forced onto the priced bundle and loses the flexibility
she had when it was merely second-best. In the valid pattern, pricing
$\set{1,2}$ leaves agent 1 demanding all three bundles and a matching exists;
in the forbidden one it pins her to bundle 1, and every price vector then fails.

**Consequence for proofs.** No argument of the form "make the agents more
indifferent" is available, and the forbidden set cannot be described by its
minimal elements alone. This is why domination is necessary but not sufficient.

## 3. Soundness, and what the obstructions say about the items

Soundness is immediate from §0: every forbidden pattern dominates an
obstruction (checked, 624 of 624), so a pattern dominating none is not
forbidden, hence valid. What makes it usable is that each `2` has content.
By the marginal bound $\abs{v_i(S) - v_i(T)} \le \abs{S \mathbin{\triangle} T}$
(approach 17, Lemma 3), an entry $\hat g_i(j) = 2$ forces at least **two items**
to separate $B_j$ from agent $i$'s best bundle. So the obstructions read:

- **avoid C** — *every bundle is within 1 of somebody's best.* No bundle is
  universally bad by two.
- **avoid A** — *no bundle is the strict favourite, by a margin of two, of two
  different agents.* No bundle is doubly coveted by two.
- **avoid B** — the mixed case, one agent tied at the top and two agents in a
  common $0/1/2$ ladder.

## 4. Measurements

`avoid_three.py`, over random instances:

| | $m=3$ | $m=4$ | $m=5$ |
|---|---|---|---|
| instances | 2,000 | 600 | 150 |
| admits an obstruction-free allocation | **2,000** | **600** | **150** |
| every obstruction-free allocation really is valid | 2,000 | 600 | 150 |
| PS2 holds | 2,000 | 600 | 150 |

The middle row is soundness, confirmed empirically as well as derived.

`hunt_avoid.py` then climbs directly at (AVOID) — objective: drive the number
of obstruction-free allocations to zero, the same machinery that killed (CANON)
in 10 of 200 climbs:

| | |
|---|---|
| climbs, $n{=}3, m{=}4$ | 70 × 300 |
| refutations | **0** |
| fewest obstruction-free allocations reached | **33 of 81** |

**33 of 81, not 1 of 81.** For comparison, the climb pushes (PAIR) down to a
single surviving option and killed (CANON) outright. (AVOID) has an enormous
margin — the first statement in this line that adversarial search does not even
approach.

## 5. Where this sits against approaches 15–17

It replaces the search for a potential, not the descent results.

| | status |
|---|---|
| (CANON) — leximin welfare maximiser | refuted (approach 17 §1) |
| any criterion reading only $(v_i(A_i))_i$ | refuted — the diagonal obstruction |
| (DESCENT-SUM) | refuted (approach 17 §7) |
| (DESCENT-1), (PAIR) | open; survived climbs, (PAIR) tight at 1 |
| **(AVOID)** | **open; climb margin 33 of 81** |

The earlier line needs a *potential* and a *move*, and its remaining gap (PAIR)
is a statement about how $\Psi$ responds to shifting one item. (AVOID) needs
neither: it asks only that some partition of the items avoids three explicit
value patterns. The two are independent routes to the same theorem, and (AVOID)
is now the better-supported one.

It also explains the earlier failures rather than merely avoiding them.
Obstruction **A** is exactly the Pareto phenomenon of `PO.tex` in pattern form:
a bundle two better than the alternatives for two agents at once is what
efficiency drives you toward and what the one-unit cap cannot fund.

## 6. Next

1. **Prove (AVOID).** The margin suggests it is not delicate. A natural first
   target is avoiding **C** alone — *every bundle is within 1 of some agent's
   best* — which is already a non-trivial statement about partitions and may
   have a direct argument.
2. **Climb harder at (AVOID)** — $m = 5, 6$ and longer runs — before trusting
   the margin. Two claims have died to climbs in this line already.
3. Check whether an explicit rule (rather than mere existence) always produces
   an obstruction-free allocation; that would make the proof constructive.

### Scripts

`gap_matrix.py` (the reduction and its cross-check), `gap_minimal.py`
(monotonicity, the minimal patterns, the three classes), `avoid_three.py`
(soundness and existence), `hunt_avoid.py` (the climb).

*A note on method. Two runs in this document reported nonsense before the bug
was found, both from the same confusion: the gap matrix and the pattern test
are functions of the bundle **multiset** and say whether **some** assignment is
valid, so comparing them against one fixed assignment is meaningless. The
cross-check is what caught it both times, which is the argument for always
having one.*
