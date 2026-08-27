# Approach 15 — Establishing the Facts for General Binary

*Started 2026-08-27. First substantive pass on PS2 (`docs/PS2_general_binary.md`):
marginals in $\{-1,0,1\}$, goods and chores together, target an envy-free
solution with $p \in \{0,1\}^n$. Framing of record:
`report/working_general_binary/framing.tex`. Scripts:
`updates_general_binary/update_1/`.*

*No LaTeX was written this pass, and no proof of the conjecture is claimed.*

---

## 0. Verdict

The conjecture **survives every search run here**, including an exhaustive
sweep of all 20,337,240 instances at $n=3$, $m=3$ over the full valuation
class: the minimum over allocations of the largest required subsidy never
exceeded 1.

Nine structural facts now delimit how it could be proved, and the pass ends
with the target sharpened to a single bounded quantity (§20).

| | Finding | Status |
|---|---|---|
| **A** | The **positive** insertion step of Barman–Krishna–Narahari–Sadhukhan survives the signed model intact — a recipient with marginal $+1$ keeps every path bound, no matter what other agents think of the item | proved §4, search-confirmed §7 (0 failures in 2,994,329 states) |
| **B** | The **negative** insertion step is impossible, not merely unproven. There is a state, verified exhaustively, where no recipient and no reassignment can absorb one more chore | proved §8, witness verified independently |
| **C** | The signed-binary **decomposition** $v = u - c$ into two positive dichotomous parts is correct, but the certificate bridge built on it is **lossy** — and it fails on envy-freeability, not on budget | §6, verified §9 |
| **D** | An item's good/chore role is not a property of the item, nor even of an (agent, item) pair | proved, `framing.tex` Lemma 10 |
| **E** | The Residual Completion Problem of §10 is **false**; but the incremental architecture it was meant to rescue is **not** refuted — a complete valid allocation was reachable in every instance tested | §12, §13 |
| **F** | **Balanced or a +1 move available $\Rightarrow$ safe.** Every dead end is unbalanced *and* has no $+1$ move. Zero counterexamples in over 1.5 million valid states | §14 |
| **G** | Balance is maintainable in **both** pure classes and **not** in the mixed one. This is why both known proofs work and neither extends | §15 |
| **H** | **(S2)** Every general binary instance admits a valid allocation of bundle-size spread $\le 2$ — verified **exhaustively** at $n{=}3,m{=}3$ and never violated up to $n,m \le 6$. The constant is **tight** and does not grow with $m$ | §18; tightness **proved** §19 |
| **I** | **Welfare maximisation is not the rule** — there is a *dichotomous goods* instance where every globally welfare-maximal allocation needs subsidy 2 while subsidy 0 is achievable | **proved**, §19 |

**H is where the pass lands.** B rules out any algorithm that places items one
at a time and can never revisit a bad state, and retroactively explains why our
own chores theorem had to be one-shot — but it does *not* kill the incremental
architecture, because the states it exhibits are avoidable (E). What B really
shows is that a correct algorithm needs a **steering rule**. F supplies a
candidate (balance), G explains why neither known proof can supply it, and H
turns the whole thing into an existence statement with no algorithm in it:
**spread at most 2**. Combined with the lemma of §19 — a welfare-maximiser
inside any permutation-closed family is envy-freeable for free — the remaining
gap is a single bounded quantity, stated in §20.

Sections 10 and 16 record the two earlier formulations of the target and are
superseded by §18; both are kept because the refutations are themselves
findings.

---

## 1. The two questions this pass was asked

> **Q1.** Can we allocate all chores first and then all goods, or the reverse,
> and still reach the per-agent-1 bound?

**Not as stated, and the two orders are not symmetric.** Three separate
reasons, in increasing order of severity.

1. *The question is not well-posed on the full class.* "The set of chores" is
   not a well-formed object (§2). It becomes well-posed only inside the
   objective sub-model, where every item is a good for everyone or a chore for
   everyone.
2. *The two phases cannot be run in parallel and added.* Subsidies do not
   compose: the envy graph of $A^C \cup A^G$ is not determined by the envy
   graphs of the two phases, because $v_i$ is not additive across the split.
   The correct shape is **incremental** — phase 1 produces an envy-free
   solution, phase 2 inserts into it one item at a time (§4).
3. *Chores-first is viable; goods-first is not.* Our chores theorem yields a
   complete allocation with $p \in \{0,1\}^n$ in one shot, and goods can then
   be inserted into it one at a time — fact **A**, confirmed by 2,994,329
   exhaustive states (§7). The reverse has no counterpart: our chores proof is
   not incremental and cannot absorb one chore at a time (fact **B**, §8), and
   its monotonicity hypothesis fails outright on mixed bundles (§5).

> **Q2.** Can an item be a good at some point and a chore at another?

**Yes — and worse than the question supposes.** Not only can an item be a good
for one agent and a chore for another; a *single* agent's marginal for one item
can change sign with the rest of her bundle. Witness (`framing.tex` Lemma 10):
$M = \{a,b,g\}$, $v(S) = |S|$ for $|S| \le 2$, $v(M) = 1$. Every marginal lies
in $\{-1,0,1\}$, yet $v(g \mid \emptyset) = +1$ and $v(g \mid \{a,b\}) = -1$.

So "good" and "chore" are properties of a *triple* (agent, item, current
bundle), never of an item or of an (agent, item) pair.

---

## 2. The sub-model hierarchy

Q1 only becomes well-posed inside a restriction, so the three levels are worth
naming once.

| Model | Definition | Is "allocate the chores first" meaningful? |
|---|---|---|
| **Objective** | a global split $M = G \sqcup C$; every item is a good for all agents or a chore for all | yes |
| **Doubly monotone** | a per-agent split; each item is a good for $i$ or a chore for $i$, but agents may disagree | no — an item that is a good for $i$ and a chore for $j$ belongs to neither phase |
| **General binary** | marginals in $\{-1,0,1\}$, nothing else | no — signs move with the bundle (§1, Q2) |

Only the first two are contained in the doubly monotone class of Kawase et
al., so only there does their $n-1$-per-agent reduction supply a baseline. On
the full class there is **no bounded baseline in the literature at all**
(`framing.tex` Remark 11).

---

## 3. The path-increment lemma

The single computation everything else is measured against.

**Lemma.** Let $Z$ be $Y$ with item $g$ added to bundle $Y_x$. Then

| arc | new weight |
|---|---|
| $(i,j)$, both $\ne x$ | unchanged |
| $(i,x)$ | $w_Y(i,x) + v_i(g \mid Y_x)$ |
| $(x,j)$ | $w_Y(x,j) - v_x(g \mid Y_x)$ |

*Proof.* $w(i,j) = v_i(Z_j) - v_i(Z_i)$ and only bundle $x$ changed. $\square$

A directed path visits distinct vertices, so it meets $x$ at most once, and its
weight changes by $v_i(g \mid Y_x) - v_x(g \mid Y_x)$ when $x$ is internal, or
by one of the two terms alone when $x$ is an endpoint. Hence

| class | bound on the change |
|---|---|
| goods, marginals $\subseteq \{0,1\}$ | $\le 1 - 0 = 1$ |
| chores, marginals $\subseteq \{-1,0\}$ | $\le 0 - (-1) = 1$ |
| general binary | $\le 1 - (-1) = \mathbf{2}$ |

and the value 2 is attained **exactly** when $v_i(g \mid Y_x) = +1$ while
$v_x(g \mid Y_x) = -1$: two agents disagreeing in sign about the *same* set
$Y_x$. That single configuration is the entire gap between the two known
theorems and the conjecture.

**Corollary (the safe-recipient rule).** Any recipient $x$ with
$v_x(g \mid Y_x) \ge 0$ keeps the change at $\le 1$, whatever the other agents
think of $g$. In particular every insertion is safe in the objective
sub-model, where all agents agree on each item's sign.

---

## 4. Fact A — the positive insertion step survives the signed model

BKNS prove Theorem 4 by induction on the number of allocated goods, and
reading their proof (`References/Reading_3.pdf`, p. 11) the **empty allocation
is used only to seed $t=0$**; Cases I and II read nothing but the current
$(\mathcal A^t, p^t)$ and the new good. Their theorem is therefore a black-box
insertion statement, not a statement about their own algorithm's history.

Auditing the chain Prop 5 $\to$ Prop 6 $\to$ Lemma 7 $\to$ Lemmas 9/10/11
$\to$ Theorem 4 against $\{-1,0,1\}$ marginals:

- **Proposition 5 survives.** With $Z$ = $Y$ plus $g$ in $Y_x$, welfare under a
  permutation $\sigma$ is $W_Z(\sigma) = W_Y(\sigma) + v_y(g \mid Y_x)$ where
  $y = \sigma^{-1}(x)$. If $v_x(g \mid Y_x) = +1$ then
  $W_Z(\mathrm{id}) = W_Y(\mathrm{id}) + 1 \ge W_Y(\sigma) + 1 \ge W_Z(\sigma)$,
  using only that every marginal is $\le 1$. Envy-freeability is preserved
  **even when other agents see $g$ as a chore**.
- **Lemma 7 and Lemma 11 survive**, using only marginal $\le 1$ and
  integrality (`framing.tex` Observation 5).
- **Proposition 6 is the one genuine break.** Its second clause,
  $w_Z(x,j) \le w_Y(x,j)$, is exactly $-v_x(g \mid Y_x) \le 0$ — false when
  $g$ is a chore for the recipient. Its corollary $w_Z(P) \le w_Y(P) + 1$ is
  what Lemma 10's Claim 2 runs on.

By §3 that clause is restored the moment the recipient has
$v_x(g \mid Y_x) \ge 0$; when the recipient's marginal is $+1$ the outgoing arcs
strictly *decrease*, so an internal $x$ contributes $\le 0$ and the $+1$ can
only arise at a path endpoint. **The repair surface is one clause, and it is
governed entirely by the recipient's own marginal.**

*This fact was reached independently twice — by audit of the BKNS proof chain,
and by Mainak's marginal analysis of the same step — and is confirmed
empirically in §7.*

---

## 5. Fact — our chores proof does not port

`report/sections/main_result.tex`, Observation `obs:m-gap`, carries a
monotonicity clause: $\cost_i(S) \le \cost_i(T)$ whenever $S \subseteq T$. It
is used essentially in Lemma `lem:m-expensive` and in Theorem
`thm:m-completion`. General binary valuations are monotone in neither
direction, so the completion argument does not transfer as written.

Independently: the proof is **one-shot**, not incremental. It runs
Tao–Wu–Yu–Zhou's partial-allocation algorithm to a terminal state and then
completes it in a single step. There is no "insert one chore" black box inside
it to reuse — and by fact **B** (§8) there could not be.

---

## 6. Fact C — the signed-binary decomposition, and why the bridge is lossy

**The lemma (Mainak).** For $v$ with $v(\emptyset) = 0$ and every marginal in
$\{-1,0,1\}$, put

$$h(S) = \tfrac{1}{2}\bigl(|S| - v(S)\bigr), \qquad c(S) = \lfloor h(S) \rfloor,
\qquad u(S) = v(S) + c(S).$$

Since $h(S \cup \{g\}) - h(S) = \tfrac{1}{2}(1 - \Delta_v)$, the increments of
$h$ lie in $\{0, \tfrac12, 1\}$, and

| $\Delta_v$ | $\Delta_h$ | $\Delta_c$ | $\Delta_u = \Delta_v + \Delta_c$ |
|---|---|---|---|
| $+1$ | $0$ | $0$ | $1$ |
| $0$ | $\tfrac12$ | $0$ or $1$ | $0$ or $1$ |
| $-1$ | $1$ | $1$ | $0$ |

so $c$ and $u$ are both **positive dichotomous** and $v = u - c$ exactly. Our
own theorem applies to $c$ (a dichotomous cost function) and BKNS's applies to
$u$.

**Verified.** Exhaustively on all 495 valuations at $m=3$ and on 20,000 sampled
at $m=4$: zero violations of $\Delta_c \in \{0,1\}$, $\Delta_u \in \{0,1\}$,
$v = u - c$, or $u(\emptyset) = c(\emptyset) = 0$
(`test_decomposition.py`).

**One correction to the closed forms.** $c(S) = \lfloor (|S| - v(S))/2 \rfloor$
is the definition, but the companion is a **floor, not a ceiling**: since
$v(S) \in \Z$,

$$u(S) = v(S) + \Bigl\lfloor \tfrac{|S|-v(S)}{2} \Bigr\rfloor
       = \Bigl\lfloor \tfrac{|S|+v(S)}{2} \Bigr\rfloor .$$

The two disagree exactly when $|S| + v(S)$ is odd — e.g. $|S| = 3$, $v(S) = 0$
gives $u = 1$ but $\lceil 3/2 \rceil = 2$. Measured: the ceiling form is wrong
for 457 of the 495 valuations at $m=3$ and 19,903 of 20,000 at $m=4$.

**The bridge.** If one allocation $A$ carries $q, r \in \{0,1\}^n$ with

$$u_i(A_i) + q_i \ge u_i(A_j) + q_j \tag{G}$$
$$c_i(A_i) - r_i \le c_i(A_j) - r_j \tag{C}$$

then adding the two gives $v_i(A_i) - v_i(A_j) \ge (q_j + r_j) - (q_i + r_i)$,
so $p = q + r$ is a valid subsidy for $v$. **This is correct.** It is useful
only if some allocation achieves $q_i + r_i \le 1$ for every $i$, since
naively $q_i + r_i \in \{0,1,2\}$.

**That coupled target is not achievable in general.** The test is exact rather
than heuristic: by Halpern–Shah the minimal certificates $q^\*, r^\*$ are
pointwise below every valid pair, so a good $(q,r)$ exists iff the minimal ones
work. Sweeping every complete allocation:

| $n, m$ | instances | conjecture holds directly | bridge reaches it | bridge loses |
|---|---|---|---|---|
| 2, 2 | 190 (exhaustive) | 190 | 190 | 0 |
| 2, 3 | 20,000 sampled | 20,000 | 19,997 | **3** |
| 3, 3 | 8,000 sampled | 8,000 | 7,999 | **1** |

**And it fails for a different reason than the budget.** The witness, verified
independently in `verify_bridge_loss.py`:

$$v_1 = (0,-1,-1,-1,-1,-1,-1,-2), \qquad v_2 = (0,0,0,0,0,0,0,-1)$$

Of the 8 complete allocations, $v$ is envy-freeable at **7**, $u$ at **4**,
$-c$ at **5**, and both components at only **1** — where $q^\* + r^\* = (0,2)$.
The obstruction is not that the two budgets add to 2; it is that **$u$ and $c$
disagree about which allocations are envy-freeable at all**, so at the
allocation you want, one of the two certificates does not exist. That is
structural: Halpern–Shah envy-freeability is welfare-maximality, and
maximising $\sum u_i - \sum c_i$ does not maximise either sum.

The bridge covers about 99.98% of instances. It is a good analytical tool. It
cannot be a proof.

---

## 7. Fact A, confirmed — inserting a good into chore-laden bundles

The route that survives Q1 needs a statement strictly weaker than a general
insertion lemma:

> **(INS-G)** Let $(A,p)$ be an envy-free solution with minimal subsidy in
> $\{0,1\}^n$ over bundles that may contain anything, and let $g$ be an
> unallocated item that is a good for every agent at every set. Is there a
> recipient and a reassignment keeping the minimal subsidy in $\{0,1\}^n$?

Phase 2 inserts only goods, so this is all it needs, and §3 predicts it should
hold because the recipient's marginal is $\ge 0$.

Exhaustive, over states in which every non-good item is already allocated
(`test_mixed_insertion.py`):

| $n, m$ | control: fully dichotomous | mixed: chores in the bundles |
|---|---|---|
| 2, 3 | 2,226 states, **0** failures | 38,756 states, **0** failures |
| 3, 3 | 45,384 states, **0** failures | 2,994,329 states, **0** failures |

The control must show zero (BKNS prove it), and does. The mixed column is the
new information: **chores in the bundles do not break the goods insertion
step.**

One caveat for algorithm design. Choosing a safe recipient and not permuting
is *not* enough by itself: that alone failed in 47,716 of the $n=3$ states.
Reassignment, as in BKNS's EXTEND and FINDSINK, is still doing real work.

---

## 8. Fact B — the negative insertion step is impossible

The general insertion lemma — same statement with an arbitrary item instead of
a good — is **false**, and it fails already inside the pure chores class.

| $n, m$ | goods (control) | chores | general |
|---|---|---|---|
| 2, 2 | 108 states, 0 | 108, 0 | 900, 0 |
| 2, 3 | 15,627, 0 | 15,627, 0 | 2,333,304, 0 |
| 3, 2 | 340, 0 | 340, 0 | 6,986, 0 |
| 3, 3 | 11,366, 0 | 11,534, **7 failures** | 9,276, 0 |

It first breaks at $n = 3$, $m = 3$. Since chores $\subset$ general binary, it
fails for general binary too; the general row shows 0 only because sampling
400 of 495 valuations rarely draws an all-chores triple.

**The witness**, re-verified in `verify_ins_failure.py` with the envy-graph
routines reimplemented from scratch. Three agents, three chores,
$v_1 = v_2 = -|S|$, and

$$v_3: \ \emptyset \mapsto 0,\ a \mapsto -1,\ b \mapsto 0,\ ab \mapsto -1,\
c \mapsto -1,\ ac \mapsto -1,\ bc \mapsto -1,\ abc \mapsto -2 .$$

State: agent 3 holds $\{a,c\}$, agents 1 and 2 hold nothing, chore $b$
unallocated. That state is an envy-free solution with **minimal** subsidy
$(0,0,1) \in \{0,1\}^3$ — exactly the kind of state an induction would hand
itself. Inserting $b$:

- **all 3 recipients $\times$ 6 reassignments = 18 options**;
- 6 are not envy-freeable, the other 12 all require subsidy **2**;
- **zero** keep the subsidy within $\{0,1\}^3$.

**But the conjecture is untouched on this instance.** The complete allocation
$A_1 = \{a\}$, $A_2 = \{c\}$, $A_3 = \{b\}$ needs subsidy **0**. What fails is
the incremental route, not the theorem.

Two consequences worth stating plainly.

1. **Any correct algorithm must be able to move already-allocated items.** The
   good allocation here requires taking $a$ and $c$ back off agent 3.
   Reassigning whole bundles by a permutation is not enough — the bundles
   themselves have to be rebuilt.
2. **The stuck state is unbalanced and the good one is balanced** (one chore
   each). That is the rebalancing theme already recorded in
   `docs/BALANCE_RULE.md`, arriving from a new direction.

This also explains retroactively why our chores theorem had to be proved in one
shot: no item-by-item induction could have worked.

---

## 9. The counterexample hunt

An instance is a counterexample iff for **every** complete allocation, either
the allocation is not envy-freeable or some agent needs subsidy $\ge 2$. The
sweeps report the minimum over allocations of the largest required subsidy —
the conjecture says it never reaches 2.

| $n, m$ | coverage | instances | max | counterexamples |
|---|---|---|---|---|
| 2, 2 | exhaustive | 190 | 1 | 0 |
| 2, 3 | exhaustive | 122,760 | 1 | 0 |
| 3, 2 | exhaustive | 1,330 | 1 | 0 |
| **3, 3** | **exhaustive** | **20,337,240** | **1** | **0** |
| 3, 4 | 400,000 sampled | — | 0 | 0 |
| 4, 4 | 200,000 sampled | — | 1 | 0 |

Class sizes: 3 valuations at $m=1$, 19 at $m=2$ (hand-checked), 495 at $m=3$,
197,547 at $m=4$.

**Controls.** Every sweep was repeated on the goods-only and chores-only
classes, where the answer is known to be $\le 1$. All returned max exactly 1
with zero counterexamples — they have to attain 1, since both classes contain
the tight lower-bound instance, and a harness that only ever printed 0 would be
silently broken.

The $n=3$, $m=3$ row is the strongest single piece of evidence: the entire
class, no sampling. The specialised implementation that made it feasible was
cross-validated against the readable one on both boundary classes before use
(`hunt_n3m3.py check`).

Uniform random sampling is weak here — the $n=3$, $m=4$ row reports max 0,
meaning it never even found an instance needing any subsidy, so it is evidence
of nothing. `hunt_targeted.py` addresses that with a hill climb seeded at the
known tight instances.

---

## 10. The first proposed frontier (SUPERSEDED by sections 12-16)

> **Superseded.** This section proposed the Residual Completion Problem
> as the next target. Section 12 refutes it. Kept as written, since the
> refutation is the finding; section 16 states what replaces it.

The frontier is no longer "combine the goods and chores mechanisms". Facts A
and B narrow it to one question.

Phase 2 can insert every item that has a $+1$ recipient (fact A, §7). What
remains is the **residual**: a state $(A,p)$ with $p \in \{0,1\}^n$ in which no
unallocated item has marginal $+1$ for any agent at any current bundle. On the
residual, every marginal in sight lies in $\{-1,0\}$ — locally chore-like.

> **Residual completion problem.** Given an envy-free solution $(A,p)$ with
> $p \in \{0,1\}^n$ and a set $R$ of unallocated items, none of which has a
> $+1$ marginal at any current bundle, complete the allocation keeping
> $p \in \{0,1\}^n$.

Three things are already known about it.

- It **cannot** be solved one item at a time (fact B). It has to be a one-shot
  argument in the shape of `sections/main_result.tex` — a partial-allocation
  algorithm run to a terminal state, then a completion — and it must be free to
  rebuild bundles, not just permute them.
- Tao–Wu–Yu–Zhou's Algorithm 3 (rules R1/R2/R3, the equality graph, the tail
  SCC) is the natural engine, since the residual is locally negative
  dichotomous. The open point is that "locally" is not "globally": a marginal
  that is $-1$ at the current bundles may become $+1$ at a bundle the algorithm
  creates, which is precisely the sign-flip of §1 Q2.
- The decomposition of §6 is available as an analytical tool but **not** as a
  proof strategy, since the certificate bridge is lossy.

**A note on the literature.** A claim that recent (2025/26) discrepancy-theory
work gives subquadratic total subsidy for arbitrary bounded-marginal valuations
has not been checked against a source in this repository. It is **not** recorded
in `docs/map.md` and must be located and cited before it enters any write-up,
per the project's citation rule. Lu–Mackenzie–Suzuki (R11) is the closest
recorded result and covers the *additive* mixed case only, which is
incomparable to this class.

---

## 12. The Residual Completion Problem is false

§10 proposed it as the frontier. Attacking it directly refutes it.

Formalised, RCP says: from a valid state whose unallocated items have no $+1$
recipient, distribute those items among the existing bundles (reassigning
bundles to agents freely) and keep $p \in \{0,1\}^n$. Call a valid state
**dead** when no such completion exists.

**Dead states exist.** The §8 witness is one: $A = (\emptyset, \emptyset,
\{a,c\})$ with $p = (0,0,1)$, chore $b$ unallocated, no $+1$ marginal anywhere,
and all 18 completions failing. Systematically:

| class | $n=3, m=3$ | $n=3, m=4$ |
|---|---|---|
| goods (control) | **0** dead states | **0** dead states |
| chores | 45 dead states / 3,000 instances | 196 / 600 instances |
| general binary | 1 / 3,000 | 0 / 600 |

The goods column must be zero — BKNS's Theorem 4 forbids dead states there —
and is. That is the harness's correctness control.

So RCP is refuted, and the refutation is *not* about mixing signs: it already
fails inside the pure chores class. Dead states need $n \ge 3$ **and**
$m \ge 3$, exactly where the insertion lemma first failed in §8.

## 13. But the incremental architecture survives

A dead state is only fatal if it cannot be avoided. Define

- **valid state** — a partial allocation, envy-freeable, minimal subsidy
  $p_i \le 1$ for all $i$;
- **move** — add one unallocated item to one bundle *and* reassign the bundles
  to the agents, with only the result required to be valid;
- **safe** — some complete valid state is reachable.

> **Question.** From the empty allocation, is a complete valid state always
> reachable?

Answered by exhaustive reachability on the state graph:

| class | $n{=}2,m{=}3$ | $n{=}3,m{=}2$ | $n{=}3,m{=}3$ | $n{=}3,m{=}4$ |
|---|---|---|---|---|
| complete state reachable | always | always | always | always |
| architecture refuted by | 0 | 0 | 0 | 0 |

**Never refuted.** Stuck states are real but always avoidable, so the problem
reduces to finding the rule that avoids them.

*One caveat recorded because it changed the numbers.* The first version of this
experiment required the intermediate allocation — item inserted but bundles not
yet reassigned — to be valid too. That is wrong: from $(\{a\},\{c\})$ inserting
$b$, the allocation $(\{c\},\{a,b\})$ can be valid while $(\{a,b\},\{c\})$ is
not, and only the former is the move actually taken. The too-strict model
reported 488 stuck states for general binary at $n=2$, $m=3$; with the correct
move set there are **none**. All figures here are from the corrected model, and
the goods control passing is what exposed the error.

## 14. Fact F — the safety criterion

Every dead state found, in every class and size, is **unbalanced** — writing
$\mathrm{spread}(A) = \max_i |A_i| - \min_i |A_i|$, every dead state has
$\mathrm{spread} \ge 2$ — **and** has no unallocated item with a $+1$ marginal
at any current bundle. Contrapositive:

> **Safety criterion (search-verified).** If a valid partial allocation is
> balanced ($\mathrm{spread} \le 1$) **or** some unallocated item has a $+1$
> marginal for some agent at some current bundle, then it is safe.

Zero counterexamples over more than 1.5 million valid states, across all three
classes and $(n,m) \in \{(2,3),(3,2),(3,3),(3,4)\}$. In particular **not one
balanced valid state was dead**.

Other plausible invariants do not survive. Requiring every paid agent to hold a
maximum-size bundle fails: 38 dead states in the chores class satisfy it. So
the criterion is not an artefact of testing something vacuous.

**This is a strengthening of the conjecture, not a lemma toward it.** The empty
allocation is balanced, so "balanced $\Rightarrow$ safe" already yields a
complete valid allocation and hence the conjecture itself. That is exactly why
it is worth having: the bare statement resists induction, and strengthening the
hypothesis is the standard way to get one through.

## 15. Fact G — balance is what separates the two known theorems from the mixed problem

Balance is *sufficient* for safety in all three classes. Is it *maintainable* —
from a valid balanced state with an unallocated item, is there a move to a
valid balanced state?

| class | balanced states tested | cannot stay balanced |
|---|---|---|
| goods (control) | 45,087 | **0** |
| chores (control) | 45,087 | **0** |
| general binary | 35,104 | **81** |

At $n=3$, $m=3$. Repeating the measurement as forced excursions at $m=3$ and
$m=4$: goods **0**, chores **0**, general binary 83 and 4.

**Both known theorems admit a balanced algorithm; the mixed problem does not.**
That is a precise statement of why BKNS's proof and ours each work and neither
extends — and it arrives at the same place as `docs/BALANCE_RULE.md` from a new
direction.

The excursions are nonetheless tightly controlled. Measuring how far an
algorithm must leave balance:

- $\mathrm{spread}$ **never exceeded 2** anywhere;
- balance was regained within **2 insertions**, or the allocation completed
  successfully while unbalanced;
- **no excursion ever hit a dead end.**

## 16. The target, restated

RCP is dead. What replaces it is sharper and is not refuted by anything above:

> **Bounded-excursion conjecture.** There is an algorithm which, starting from
> the empty allocation, keeps every intermediate allocation valid, never lets
> $\mathrm{spread}$ exceed 2, and restores $\mathrm{spread} \le 1$ within two
> insertions of any departure from it.

By §14 this implies the main conjecture. Three things support it and one thing
must be supplied.

- Supported: balanced states are never dead (§14); excursions are shallow,
  narrow, and never dead-end (§15); and every $+1$ insertion is safe by fact A,
  which covers the case where balance cannot be kept for the usual reason.
- Missing: a *proof* that an excursion can always be closed. This is where
  Tao–Wu–Yu–Zhou's Algorithm 3 should enter, since a state with no $+1$ move is
  locally negative dichotomous — and it is the natural engine for the one-shot
  rebalancing step that fact B (§8) shows is unavoidable.

**Not attempted this pass:** any proof of the conjecture, any LaTeX, any change
under `report/`.

---

## 18. The target sharpened — a spread-bounded existence statement

§16's bounded-excursion conjecture mixed an existence claim with an
algorithmic one. Separating them leaves a statement with no algorithm in it at
all, and that statement is what all the evidence actually supports:

> **(S2) Spread-2 conjecture.** Every general binary instance admits an
> envy-freeable allocation whose minimal subsidy lies in $\{0,1\}^n$ and whose
> bundle-size spread $\max_i |A_i| - \min_i |A_i|$ is at most $2$.

> **(S1) Balanced pure conjecture.** Every dichotomous goods instance, and
> every negative dichotomous instance, admits such an allocation that is
> **balanced** — spread at most $1$.

(S2) implies the main conjecture and is strictly more structured, which is what
makes it the better induction target. Testing both, with $K$ the spread bound
and the entry counting instances admitting **no** valid allocation at that
bound:

| $n,m$ | coverage | goods $K{=}1$ | chores $K{=}1$ | general $K{=}1$ | general $K{=}2$ |
|---|---|---|---|---|---|
| 3, 3 | **exhaustive** (20,337,240; 9,880 per pure class) | 0 | 0 | 98,931 | **0** |
| 3, 4 | 15,000 sampled | 0 | 0 | 0 | **0** |
| 4, 4 | 6,000 | 0 | 0 | 11 | **0** |
| 3, 5 | 4,000 | 0 | 0 | 0 | **0** |
| 5, 5 | 1,200 | 0 | 0 | 52 | **0** |
| 3, 6 | 1,500 | 0 | 0 | 0 | **0** |
| 6, 6 | 400 | 0 | 0 | 12 | **0** |

**(S2) never failed once**, and the constant does not grow with $m$ — spread 2
still sufficed at $m=6$. **(S1) never failed either**: in both pure classes a
balanced allocation always exists, at every size tested.

Two further readings of the table. First, the $K=1$ failures for general binary
cluster at $n = m$ — 98,931 at $(3,3)$, 11 at $(4,4)$, 52 at $(5,5)$, 12 at
$(6,6)$, and none at $(3,4)$, $(3,5)$, $(3,6)$ — which is where balance is most
rigid, since every agent must hold exactly one item. Second, (S1) restricted to
goods does **not** follow from what is on record: BKNS's Theorem 4 says nothing
about bundle sizes, and their concluding section notes their allocation need not
even be EF1; Brustle et al.'s balanced guarantee is for *additive* valuations,
an incomparable class. A literature check is needed before claiming it is new,
but it is not a corollary of either.

## 19. What is proved, not merely verified

Three results in this pass are proofs rather than search outcomes.

**Lemma (permutation-closed families).** Let $\mathcal F$ be any family of
allocations closed under permuting the bundles among the agents, and let
$A \in \mathcal F$ maximise $\sum_i v_i(A_i)$ over $\mathcal F$. Then $A$ is
envy-freeable.

*Proof.* Every permutation $A_\sigma$ lies in $\mathcal F$, so
$\sum_i v_i(A_i) \ge \sum_i v_i(A_{\sigma(i)})$ for all $\sigma$, which is
Halpern–Shah condition (ii). $\square$

Permuting bundles leaves the multiset of bundle sizes unchanged, so
"allocations of spread at most $K$" is such a family for every $K$. **This
removes half of (S2)**: the envy-freeability is automatic, and only the subsidy
bound remains to be proved.

**Proposition (the constant 2 is tight).** There is a general binary instance
in which no balanced allocation admits a subsidy of at most 1 per agent.

*Proof.* Take $n=3$, $m=3$, with $a,b$ unit chores for everyone and $c$ a unit
chore for agent 1 but a unit good for agents 2 and 3:
$v_1(S) = -|S|$ and $v_i(S) = -|S \cap \{a,b\}| + [c \in S]$ for $i \in
\{2,3\}$. All marginals lie in $\{-1,0,1\}$. A balanced allocation gives each
agent exactly one item, so exactly one agent holds $c$ and at least one of
agents 2, 3 does not; call her $i$. She values her own bundle at $-1$ and the
bundle holding $c$ at $+1$, so the arc from $i$ to that holder has weight
$1-(-1) = 2$ and $\optsubsidy_i \ge 2$. This is independent of who holds $c$,
so all six balanced allocations fail. Meanwhile $A = (\{a\},\{b,c\},\emptyset)$
has spread 2 and minimal subsidy $(1,0,0)$. $\square$

Checked against all 27 allocations in `verify_spread2_tight.py`: eight are
valid, and every one of them has spread 2 or 3.

**Proposition (welfare maximisation is not the rule).** There is a
*dichotomous goods* instance in which every globally welfare-maximal allocation
leaves some agent needing subsidy 2, although subsidy 0 is achievable.

*Proof.* $n=3$, $m=3$; agent 1 values every bundle at 0; agents 2 and 3 have
$v(S) = \max(0, |S|-1)$, whose marginals are all in $\{0,1\}$. The unique
welfare optimum, value 2, is to give all three items to agent 2 or to agent 3.
Say agent 2 holds them; then $w(3,2) = v_3(\{a,b,c\}) - v_3(\emptyset) = 2$, so
the path $1 \to 3 \to 2$ has weight 2 and $\optsubsidy_1 = 2$. Yet
$(\{a\},\{b\},\{c\})$ gives every agent value 0 and subsidy $(0,0,0)$.
$\square$

This is worth stating because it kills the most natural canonical rule, and it
does so **inside the pure goods class**, where BKNS's theorem holds. It also
explains why the spread bound helps rather than hurts: maximising welfare
concentrates items on one agent and manufactures a length-2 envy path, whereas
the spread constraint forces the items apart. Maximising welfare *inside* the
spread-2 family never failed in any experiment — 100% across every class and
size in `canonical_allocation.py` — though it needs a tie-break, since not every
maximiser in that family is valid.

## 20. Where this leaves the problem

The remaining gap is a single bounded quantity. By §19's lemma, a
welfare-maximiser over the spread-$\le 2$ allocations is envy-freeable for
free, so (S2) reduces to:

> show that its longest envy path has weight at most 1

with the path-increment lemma (§3) as the tool and the two pure cases (§18,
(S1)) as the boundary conditions the argument must reproduce. The constant 2
cannot be improved (§19) and does not grow with $m$ (§18), so the statement is
sharp as posed.

---

## 21. Reproducing

All scripts in `updates_general_binary/update_1/`, runnable from that folder.

| Script | What it does |
|---|---|
| `gb_valuations.py` | enumerates the valuation class and the Halpern–Shah routines; prints class sizes, checks the $m=2$ hand count of 19 |
| `hunt_counterexample.py [small\|big\|wide]` | the counterexample sweeps with the goods and chores controls |
| `hunt_n3m3.py [check\|run]` | the exhaustive $n=3$, $m=3$ sweep; `check` cross-validates it against the readable implementation |
| `hunt_targeted.py` | hill climb on the hardest instances, seeded at the tight lower-bound structures |
| `test_insertion.py` | the general insertion lemma (INS) and the greedy routing rule — produces fact **B** |
| `verify_ins_failure.py` | independent re-check of the (INS) witness, routines rewritten from scratch |
| `test_mixed_insertion.py` | (INS-G): inserting a universal good into chore-laden bundles — produces fact **A** |
| `test_decomposition.py` | audits the decomposition lemma and tests the coupled target — produces fact **C** |
| `verify_bridge_loss.py` | independent re-check of the bridge-loss witness |
| `reachability.py [small\|wide]` | is a complete valid state always reachable from the empty one — produces facts **E** and the dead-state counts of §12–13 |
| `analyse_safe.py [small\|wide]` | computes the safe/dead split exactly and characterises the dead states — produces fact **F** |
| `test_balance_invariant.py` | can balance always be maintained — produces fact **G** |
| `invariant_battery.py` | measures safe-sufficiency and maintainability for five candidate invariants side by side |
| `excursion_depth.py` | how deep and how wide the forced departures from balance are (§15) |
| `bounded_excursion.py [small\|wide]` | both halves of the bounded-excursion conjecture: existence and reachability within a spread bound |
| `canonical_allocation.py [small\|wide]` | welfare-maximal allocations inside spread-bounded families; refutes global welfare maximisation |
| `gwm_refutation.py [goods\|general]` | finds and verifies the welfare-maximisation failure of §19 |
| `existence_spread.py exhaustive` | the exhaustive $n=3,m=3$ test of (S1) and (S2) |
| `existence_spread.py sampled <n> <m> <k>` | the same at larger sizes, one size per invocation |
| `verify_spread2_tight.py` | independent re-check that the constant 2 cannot be lowered to 1 |

Every negative claim in this document (facts **B** and **C**) has a dedicated
independent verifier that reimplements the envy-graph machinery, so that a bug
in the shared module could not both generate a finding and confirm it.
