# Approach 17 — (CANON) refuted, and a descent lemma that proves PS2 for $n=3$

*Target narrowed to $n = 3$, as PS1 was (approach 12 for $n=3$, approach 13 for
general $n$). This pass kills approach 16's §7 proposal, identifies a whole
family of criteria that cannot work and says why, and replaces them with a
local-search statement that survived the same attack that killed (CANON).*

---

## 0. Verdict

**(CANON) is false.** Approach 16 §7 proposed: inside the spread-$\le 2$ family,
take the welfare maximisers and break ties by leximin on the cost profile. It
survived 2,000 random instances and dies to a hill climb — 10 refutations from
200 climbs at $n{=}3, m{=}4$. Random sampling finds none of them.

**The damage is deeper than the tie-break.** In 5 of the 10 witnesses *no*
welfare maximiser of the family is valid. Welfare maximisation is the wrong
primary criterion.

**And deeper still — an entire family of criteria is dead.** There exist two
allocations of the *same instance* with the **same cost profile** $(0,0,0)$, one
valid and one not. Any criterion that scores an allocation by
$(v_i(A_i))_i$ alone therefore cannot separate them. That kills leximin, least
maximum cost, least sum of squares and least cost spread in one stroke — as
measured, all four do fail — and explains *why* rather than just *that*.

**What survives, and what replaces it.** (S2) is untouched: a valid
spread-$\le 2$ allocation existed in every witness, 14–23 of 54. The
replacement scores states by the thing itself rather than a proxy:

> **(DESCENT-1).** Let $\Psi(\pi)$ be the vector $(\ell(i))_i$ sorted
> downwards, **minimised over the assignments** of partition $\pi$'s bundles,
> and $+\infty$ if none is envy-freeable. If $\max \Psi(\pi) > 1$, then some
> partition differing from $\pi$ in the owner of **one item** has strictly
> smaller $\Psi$.

$\Psi$ takes finitely many values and strictly decreases, so iteration
terminates, and it can only stop where $\max_i \ell(i) \le 1$. **(DESCENT-1)
proves PS2 for $n=3$ outright** — not (S1), not (S2), the thing itself — and
constructively. Zero stuck states in ~2,500 tested, and 120 targeted climbs
failed to dent it.

---

## 1. How (CANON) died

`hunt_canon3.py` at $n{=}3, m{=}4$, general binary, spread $\le 2$. Two things
were changed from approach 16's test, and both mattered.

**Quantify over *every* leximin-optimal allocation.** Leximin itself ties — in
1,754 of 3,000 instances — so "the" leximin-optimal allocation is not well
defined, and approach 16 silently tested whichever representative the code saw
first. The honest statement is about all of them.

**Hill climb instead of sample.** Seed from instances whose leximin maximiser
is *tight* ($\max_i \ell = 1$, one step from failing) and mutate single
valuation entries, keeping any mutation that does not decrease the worst
longest path.

| | count |
|---|---|
| random instances | 3,000 |
| leximin itself ties | 1,754 |
| leximin maximiser tight ($\max \ell = 1$) | 872 |
| *some* leximin-optimal allocation invalid (breaks the ALL form) | 22 |
| **every** leximin-optimal allocation invalid — refutes (CANON) | **0 by sampling** |
| refutations found by hill climbing | **10 of 200 climbs** |

The gap between the last two rows is the lesson. Approach 16's evidence was
2,000 random instances at $m{=}3$ and 250 at $m{=}4$; this class hides its
counterexamples from uniform sampling, and any future claim here needs a climb
before it is written down.

## 2. How much the refutation kills

`diagnose_canon.py` runs three nested questions on each of the 10 witnesses.

| | question | answer |
|---|---|---|
| **Q1** | is *some* welfare maximiser of the family valid? | **5 / 10** |
| **Q2** | is *some* spread-$\le 2$ allocation valid? | **10 / 10** |
| **Q3** | is any allocation valid at all? | 10 / 10 |

Q1 is the important row: in half the witnesses the entire set of welfare
maximisers is invalid, so no tie-break whatsoever can repair (CANON).

Q2 says **(S2) stands** — approach 15 §18's table is not affected — and the
valid allocations are not scarce: 14 to 23 of the 54 allocations in the family.
Welfare maximisation is actively steering *away* from an abundant target.

Witness 7 shows the mechanism at its starkest:

| | bundles | cost profile | total | $\max_i \ell$ |
|---|---|---|---|---|
| leximin maximiser | $(5,2,8)$ | $(-2,-1,0)$ | $-3$ | **2** |
| a valid allocation | $(3,12,0)$ | $(0,0,0)$ | $0$ | 1 |

The valid allocation is **three units worse** in welfare and perfectly flat.

### This is the Pareto phenomenon again

That table is the same fact recorded in `PARETO_INVESTIGATION.md` and `PO.tex`,
seen from the other side. There, a subsidy capped at one unit per agent was
shown *incompatible* with Pareto optimality: efficiency wants to concentrate,
and concentration creates an envy gap the cap cannot fund. Here the same force
makes welfare maximisation a bad *search* criterion for a valid allocation.

The two findings should be quoted together. In hindsight the Pareto result
predicted this one, and had it been applied, (CANON) would not have been
proposed.

## 3. Why every profile-based criterion is dead

Flatness is the obvious repair, and it also fails (`flat_canon.py`, 4,000
instances, $n{=}3,m{=}4$, over the envy-freeable allocations of the family):

| criterion | valid | |
|---|---|---|
| FLAT least $\max c - \min c$, then least total | 3,994 / 4,000 | ✗ |
| LEX least cost profile sorted downwards | 3,991 / 4,000 | ✗ |
| MAXC least largest individual cost | 3,991 / 4,000 | ✗ |
| SQ least sum of squares | 3,971 / 4,000 | ✗ |

FLAT fails on a cost profile of $(-1,-1,0)$ — already flat. That is the clue,
and `descent.py` confirms the reason directly:

> **Obstruction (diagonal criteria).** There is an instance with two
> allocations of the same cost profile $(0,0,0)$, one valid and one not:
> $(5,10,0)$ invalid, $(9,2,4)$ valid. A second, with the spread bound
> dropped: $(15,0,0)$ valid, $(11,0,4)$ invalid.

The cost profile $(v_i(A_i))_i$ is the **diagonal** of the matrix $v_i(A_j)$,
while validity is a statement about the whole matrix — the envy arc
$w(i,j) = v_i(A_j) - v_i(A_i)$ reads off-diagonal entries. So **no criterion
that scores an allocation by its cost profile alone can decide validity**, and
the four rows above are not four separate failures but one.

This is worth keeping as a standing constraint: any canonical object for this
problem has to see off-diagonal data.

## 4. (DESCENT-1)

The way past the obstruction is to stop using a proxy. Score a state by the
quantity the theorem is about:

$$\Psi(\pi) \;=\; \min_{\sigma} \ \operatorname{sort}_{\downarrow}\bigl(\ell_{(\pi,\sigma)}(i)\bigr)_{i}, \qquad \Psi(\pi) = +\infty \text{ if no } \sigma \text{ is envy-freeable,}$$

compared lexicographically, with $\sigma$ ranging over assignments of $\pi$'s
bundles to the agents.

> **(DESCENT-1).** If $\max \Psi(\pi) > 1$, some partition differing from $\pi$
> in the owner of exactly one item has strictly smaller $\Psi$.

**Why this is not circular.** $\Psi$ is the thing being bounded, but the lemma
is a statement about *local moves*, and it does the work: $\Psi$ ranges over
finitely many values and each step strictly decreases it, so iteration
terminates; it cannot stop while $\max \Psi > 1$; hence it stops at
$\max_i \ell(i) \le 1$, which is PS2. The content is entirely in the move.

**The state space has to be partitions, not allocations.** This is approach 16
§1's reformulation — validity is a property of the bundle *multiset* — and
getting it wrong is what made two earlier versions fail:

| state space | potential | moves | stuck states |
|---|---|---|---|
| allocations | $\Psi$ of that allocation | 1 item + permutations | 3 |
| allocations | as above | **2** items, no permutations | 115 (all $\Psi = \infty$) |
| **partitions** | $\min$ over assignments | **1** item | **0** |

The 115 were all non-envy-freeable, given the same $+\infty$ and so
indistinguishable from each other, letting the descent jam among them.
Minimising over assignments removes that plateau: a partition whose bundles
admit *any* envy-freeable assignment never scores $\infty$.

### Measurements

`descent2.py`, testing **every** partition of every sampled instance, not only
reachable ones, which is the strong form a proof needs:

| | instances | partitions each | states with $\max \Psi > 1$ | stuck under 1-item moves |
|---|---|---|---|---|
| $n{=}3, m{=}3$ | 2,000 | 27 | 876 | **0** |
| $n{=}3, m{=}4$ | 500 | 81 | 837 | **0** |
| $n{=}3, m{=}5$ | 150 | 243 | 798 | **0** |

PS2 itself held in every one of those 2,650 instances.

### The refutation attempt

Since sampling is what let (CANON) through, `hunt_descent.py` climbs against
(DESCENT-1) directly. Its objective drives the *scarcest* bad state towards
zero improving neighbours, with more bad states as secondary pressure — the
analogue of the climb that killed (CANON) in 10 of 200 attempts.

| | |
|---|---|
| climbs | 120 × 300 steps, $n{=}3, m{=}4$ |
| refutations | **0** |
| tightest state reached | 60 bad states; the scarcest still had **2** improving one-item neighbours |

Never closer than 2. That is not proof, but it is the same attack at the same
strength, and (CANON) did not survive it.

---

## 5. What to prove, for $n = 3$

The target is now a single local statement. Let $\pi$ have $\max \Psi(\pi) \ge 2$
and fix an assignment attaining $\Psi$. At $n = 3$ the envy graph has three
vertices, so $\ell(i) \ge 2$ means either

- **a single arc** $w(i,j) = v_i(A_j) - v_i(A_i) \ge 2$, or
- **a two-arc path** $w(i,j) = w(j,k) = 1$ with $\set{i,j,k} = \set{1,2,3}$.

Two facts are free and should be used. Minimising over assignments means no
positive cycle, so closing either configuration into a cycle gives
$w(k,i) \le -2$ in the path case and $w(j,i) \le -2$ in the arc case: **the
agent at the far end finds the near bundle at least $2$ worse**. And general
binary gives $\abs{v_i(S) - v_i(T)} \le \abs{S \triangle T}$, so a gap of $2$
forces at least two items to separate the bundles.

The task is to turn a gap of $2$ plus at least two separating items into a
single item whose transfer strictly lowers $\Psi$. The measurements say such an
item always exists; at $n=3$ there are only the two configurations above, which
is exactly why $n=3$ is the right place to start.

Three things *not* to try, each already refuted: any criterion reading only the
cost profile (§3); welfare maximisation as the primary criterion (§2); and
descent over allocations rather than partitions (§4).

---

## 6. The proof so far, and the exact gap

**Status.** PS2 for $n=3$ is **not proved**. What is proved is the reduction
and the structure around the remaining step; the step itself, (PAIR) below, is
machine-verified but open. The chain is stated so the gap is unambiguous.

Throughout: $n = 3$, $v_i(\emptyset) = 0$, every marginal
$v_i(S \cup \set g) - v_i(S) \in \set{-1,0,1}$, no additivity or submodularity.
Write $w_A(i,j) = v_i(A_j) - v_i(A_i)$ and let $\ell_A(i)$ be the greatest
weight of a simple directed path leaving $i$, the empty path included.
*Valid* means envy-freeable with $\ell_A(i) \le 1$ for all $i$.

### Fact 1 — $\Phi$ is well defined and finite

For a partition $\pi$ put
$\Phi(\pi) = \min_{\sigma} \sum_i \ell_{(\pi,\sigma)}(i)$, over envy-freeable
assignments $\sigma$ of $\pi$'s bundles.

*Proof.* By Halpern–Shah an allocation is envy-freeable iff it maximises
welfare among reassignments of its own bundles. A welfare-maximal assignment
exists (finitely many), so at least one $\sigma$ qualifies and the minimum is
over a non-empty set. Each $\ell \ge 0$, so $\Phi(\pi)$ is a non-negative
integer. $\square$

This also disposes of the $+\infty$ branch in §4's definition: it is never
attained, and the two earlier jammed descents were artifacts of pretending
otherwise.

### Fact 2 — the reduction

> If (DESCENT) holds — every partition whose $\Phi$-optimal assignment has
> $\max_i \ell(i) \ge 2$ admits a one-item move strictly decreasing $\Phi$ —
> then every general binary instance with $n=3$ has a valid allocation.

*Proof.* Start at any partition. While $\max_i \ell(i) \ge 2$, apply (DESCENT).
$\Phi$ is a non-negative integer and strictly decreases, so the process halts
after at most $\Phi(\pi_0)$ steps. It cannot halt while $\max_i \ell \ge 2$, so
at the end $\max_i \ell(i) \le 1$ with an envy-freeable assignment; by
Halpern–Shah the minimal subsidy is $p^*_i = \ell(i) \in \set{0,1}$. $\square$

### Lemma 1 — the case split is exhaustive

Let $A$ be envy-freeable with $\ell_A(1) \ge 2$. Then either

- **(A)** some arc leaving $1$ has weight $\ge 2$; or
- **(B)** after relabelling $\set{2,3}$, $w(1,2) = w(2,3) = 1$ and every arc of
  the graph has weight $\le 1$.

*Proof.* With three vertices the simple paths leaving $1$ are the empty path,
$1 \to j$, and $1 \to j \to k$ with $\set{j,k} = \set{2,3}$. So
$\ell(1) = \max\bigl(0,\, w(1,2),\, w(1,3),\, w(1,2)+w(2,3),\, w(1,3)+w(3,2)\bigr)$.
If no single arc leaving $1$ reaches $2$, some two-arc path does, and since each
of its arcs is $\le 1$ both equal $1$. Finally any arc $w(a,b) \ge 2$ anywhere
is itself a path leaving $a$, giving $\ell(a) \ge 2$; relabelling $a$ as $1$
puts us in case (A). $\square$

Machine-confirmed: `case_split.py` classifies 480 of 480 states, none
unclassified (355 in case A, 125 in case B).

### Lemma 2 — an arc of weight $\le -2$ is forced

In case (A), $w(2,1) \le -2$. In case (B), $w(3,1) \le -2$.

*Proof.* Envy-freeability is exactly the absence of a positive-weight cycle.
The $2$-cycle $1 \to 2 \to 1$ gives $w(1,2) + w(2,1) \le 0$, so
$w(2,1) \le -w(1,2) \le -2$. The $3$-cycle $1 \to 2 \to 3 \to 1$ gives
$w(1,2) + w(2,3) + w(3,1) \le 0$, so $w(3,1) \le -(1+1) = -2$. $\square$

Machine-confirmed: `pair_lemma.py` finds such an arc in 387 of 387 states,
1.74 of them per state on average.

### Lemma 3 — a very negative arc forces two separating items

If $w(y,x) \le -2$ then $v_y(A_y) \ge v_y(A_x) + 2$ and
$\abs{A_x} + \abs{A_y} \ge 2$.

*Proof.* The first is the definition. For the second, transform $A_y$ into
$A_x$ by deleting the items of $A_y$ one at a time and then inserting those of
$A_x$; each step moves $v_y$ by at most $1$, so
$\abs{v_y(A_y) - v_y(A_x)} \le \abs{A_y \setminus A_x} + \abs{A_x \setminus A_y}$.
The bundles are disjoint, so that is $\abs{A_x} + \abs{A_y}$, which is
therefore at least $2$. $\square$

Lemma 3 matters because it makes the next step non-vacuous: the pair
$\set{A_x, A_y}$ always contains an item to move.

### The gap — (PAIR)

Everything above reduces PS2 for $n=3$ to a statement about **two** bundles,
the third agent entering only through Lemma 2's cycle condition.

> **(PAIR), open.** Let $A$ be envy-freeable with $\max_i \ell_A(i) \ge 2$. By
> Lemma 2 some arc has weight $\le -2$. Then for a *suitable* such arc
> $(y,x)$, moving one item between $A_x$ and $A_y$ strictly decreases $\Phi$.

Evidence and shape:

- **holds in 387 of 387** states at $n{=}3, m{=}4$ (`pair_lemma.py`);
- the word *suitable* is necessary — the "every such arc works" form fails,
  345 of 387, so a proof must choose the arc;
- $\Phi$ may be taken to be the plain **sum** $\sum_i \ell(i)$, not a sorted
  vector (`potentials.py`, zero stuck states at $n{=}2$ and $n{=}3$), which is
  the version to attack since it is a single integer;
- in case (A) the pair is $\set{A_1,A_2}$ with *both* agents preferring $A_2$
  to $A_1$ by at least $2$ — $w(1,2)\ge2$ and $w(2,1)\le-2$ — so the pair is
  lopsided in a way both agents agree on. That symmetry is the most promising
  handle and is where the next attempt should start.

**What is not yet ruled out.** (PAIR) has been checked but *not* attacked by a
hill climb of the kind that killed (CANON). Until it has been, §0's claim that
(DESCENT-1) survived a targeted hunt covers (DESCENT-1) only, and does not
transfer to (PAIR).

---

## 7. Reproducing

New scripts, in `updates_general_binary/update_1/`.

| Script | What it does |
|---|---|
| `hunt_canon3.py [m] [trials] [climbs] [steps]` | refutes (CANON); random sample and hill climb side by side, quantifying over every leximin-optimal allocation |
| `diagnose_canon.py` | the Q1/Q2/Q3 depth analysis on the 10 witnesses, which are embedded in the file |
| `flat_canon.py [m] [trials]` | the four flatness criteria of §3 |
| `descent.py [m] [trials] [K]` | the diagonal obstruction, and the first (allocation-level) descent |
| `descent2.py [m] [trials]` | (DESCENT-1) over partitions — the table of §4 |
| `stuck.py [m] [trials]` | prints jammed states with their envy matrices and which wider move clears them |
| `hunt_descent.py [m] [climbs] [steps]` | the targeted attempt to refute (DESCENT-1) |
| `potentials.py [n] [m] [trials]` | which potential admits the descent; the plain SUM suffices |
| `case_split.py [m] [trials]` | that Lemma 1's split is exhaustive, and which move settles each case |
| `pair_lemma.py [m] [trials]` | Lemma 2's forced arc, and (PAIR) in both strengths |

A note on method, earned the hard way this pass: in this class **a claim
supported only by uniform random sampling is not supported**. (CANON) passed
2,250 random instances and fell to the first serious climb. Every claim above
was either verified by construction or attacked by a climb, and where a climb
was run its strength is quoted.
