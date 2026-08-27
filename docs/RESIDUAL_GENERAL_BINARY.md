# General binary valuations (goods and chores) — running research log

*Started 2026-08-24. Sibling log to `RESIDUAL.md`, which is now closed — see
its banner. This file follows the same conventions: one running document,
numbered subsections, a status table maintained at the end as sections are
added. Nothing here is deleted, only superseded, exactly as in `RESIDUAL.md`.*

---

## 0. Context

The negative-binary (chores) problem is closed: for every $n$, every instance
with marginals in $\set{0,-1}$ admits an envy-free allocation with subsidy
$\subsidy \in \set{0,1}^n$, $\sum_i \subsidy_i \le n-1$, in polynomial time.
Proof: `report/main.tex` §3 (`report/sections/main_result.tex`); full
derivation trail: `RESIDUAL.md` §7.16.35–39 (`report/working/approach_13.tex`).

This log tracks the natural generalization: **general binary** valuations,
where every marginal lies in $\set{-1,0,1}$ rather than only $\set{0,-1}$ —
each item may be a good for some agents and a chore for others (a *mixed
manna* dichotomous model). See `docs/PS2_general_binary.md` for the problem
statement.

## 1. What transfers from the closed result without re-proof

- **Halpern–Shah** (`sections/preliminaries.tex`, Theorem `thm:hs-characterisation`
  / `thm:hs-minsubsidy`): envy-freeability $\iff$ no positive-weight cycle in
  the envy graph, and the minimal subsidy is the longest outgoing path. The
  proof of both facts uses only arc weights and permutations of bundles —
  nothing about the sign or structure of the valuations — so it applies
  verbatim here. **Do not re-derive.**
- **Integrality** (`obs:integrality`): every arc weight is an integer whenever
  every marginal is an integer, which holds here too ($\set{-1,0,1} \subset
  \Z$). The minimal subsidy is therefore still integral, so "$\subsidy \le 1$"
  is again the same statement as "$\subsidy \in \set{0,1}^n$."
- **The chores-only result itself** is a special case (every marginal
  restricted to $\set{0,-1}$) and is available as a known, proved lemma —
  useful wherever an argument can localize to the chore-only part of an
  instance.
- **Some agent is unpaid** (`prop:zero-coordinate`): the minimal subsidy of an
  envy-freeable allocation has at least one zero coordinate, because the
  shifted vector $\subsidy - (\min_i \subsidy_i)\mathbf{1}$ is again
  envy-free and pointwise no larger. The argument reads only arc weights, so
  it is sign-agnostic and holds here. Consequence: per-agent $\le 1$ still
  implies total $\le n-1$, so the two forms of the conjecture coincide.
- **Both known theorems are boundary cases.** Restricting every marginal to
  $\set{0,1}$ recovers [R3, Theorem 4] (Barman–Krishna–Narahari–Sadhukhan);
  restricting to $\set{0,-1}$ recovers the closed result. The conjecture is
  exactly their common generalization, and the $n-1$ lower bound is inherited
  from *either* boundary case, so if it holds it is tight.

## 2. What does *not* transfer, and must be re-derived

- The completion argument of `sections/main_result.tex` (Tao–Wu–Yu–Zhou's
  partial-allocation algorithm and its terminal-state lemma) is stated for
  chores specifically (dichotomous *cost* functions, marginals in
  $\set{0,1}$ after negation). Whether an analogous partial-allocation
  algorithm exists for mixed marginals is open and is the first thing to
  check against the literature (`docs/map.md`) before assuming it.
- **[R9]'s $n-1$-per-agent baseline does not transfer off the shelf.** In the
  chores case, negative dichotomous valuations are doubly monotone, so
  Kawase et al.'s EF1-to-EF reduction applied directly and supplied a bounded
  starting point. General binary is **not** contained in the doubly monotone
  class: with $M = \set{a,b,g}$, $v(S) = \abs{S}$ for $\abs{S} \le 2$ and
  $v(M) = 1$, every marginal lies in $\set{-1,0,1}$, yet $g$ has marginal
  $+1$ on $\emptyset$ and $-1$ on $\set{a,b}$ — the same item is a good and
  a chore for the *same* agent. Both boundary classes are doubly monotone;
  their union is not. So this investigation starts without a bounded baseline,
  unlike the chores one. Proof: `report/working_general_binary/framing.tex`,
  Lemma 10.
- The literature corpus (`docs/map.md`) already contains one goods-and-chores
  result — R11 (Lu–Mackenzie–Suzuki, 2026) — but for the *additive* class, not
  dichotomous. Dichotomous and additive are incomparable classes (this is
  exactly why R3 was not a corollary of R2, and why the chores result was not
  a corollary of R11); R11 does not settle this question, and its machinery
  (iterated matchings, telescoping over rounds) is additivity-specific.

## 3. Status table

| Claim | Status | Where |
|---|---|---|
| Envy-free solution with $\subsidy \in \set{0,1}^n$ for every general binary instance, in polynomial time | **open** — the target | `framing.tex` Conjecture 3 |
| Integrality: marginals in $\set{-1,0,1}$ give integral arc weights and integral minimal subsidy | **proved** | `framing.tex` Observation 5 |
| Halpern–Shah characterisation and minimal-subsidy formula apply verbatim (sign-agnostic) | **proved** (cited, [R1]) | `framing.tex` Theorems 6, 7 |
| Minimal subsidy has a zero coordinate, so per-agent $\le 1 \Rightarrow$ total $\le n-1$ | **proved** | `framing.tex` Proposition 8 |
| $n-1$ is tight if the conjecture holds (inherited from either boundary case) | **proved** | `framing.tex` Example 9 |
| General binary $\not\subseteq$ doubly monotone, so [R9]'s bound does not apply | **proved** (explicit witness) | `framing.tex` Lemma 10 |
| Path-increment lemma: one insertion moves a path by $v_i(g\mid Y_x) - v_x(g\mid Y_x)$, so $\le 1$ in either pure class and $\le 2$ only when two agents disagree in sign about the same set | **proved** | `approach_15.md` §3 |
| BKNS's positive insertion step survives the signed model; a recipient with marginal $+1$ preserves envy-freeability and every path bound whatever other agents think of the item | **proved**, and search-confirmed (0 failures in 2,994,329 exhaustive states) | `approach_15.md` §4, §7 |
| The insertion lemma is **false** for chore insertion: a state with minimal $p\in\set{0,1}^3$ admits no recipient and no reassignment absorbing one more chore | **refuted** (witness verified independently) | `approach_15.md` §8 |
| Signed-binary decomposition $v = u - c$ into two positive dichotomous parts | **proved** (Mainak), verified on all 495 valuations at $m=3$ | `approach_15.md` §6 |
| The certificate bridge built on that decomposition ($q_i + r_i \le 1$) | **refuted** — lossy; $u$ and $c$ disagree about which allocations are envy-freeable | `approach_15.md` §6, §9 |
| Conjecture survives exhaustive search: all 20,337,240 instances at $n=3$, $m=3$ | **search-verified** (max subsidy exactly 1) | `approach_15.md` §9 |
| Residual Completion Problem: complete from a state whose residual items have no $+1$ recipient, keeping $p\in\set{0,1}^n$ | **refuted** — dead states exist, already inside the pure chores class | `approach_15.md` §12 |
| The incremental architecture: is a complete valid allocation always reachable from the empty one? | **not refuted** — reachable in every instance tested; stuck states exist but are avoidable | `approach_15.md` §13 |
| Safety criterion: balanced ($\mathrm{spread}\le 1$) **or** a $+1$ move available $\Rightarrow$ safe | **search-verified**, 0 counterexamples in $>1.5$M valid states | `approach_15.md` §14 |
| Balance is maintainable in goods (0 failures) and chores (0 failures) but **not** in general binary (81/34226) | **proved by separation** — why both known proofs work and neither extends | `approach_15.md` §15 |
| Forced departures from balance: depth $\le 2$, spread never exceeds 2, never dead-end | **search-verified** | `approach_15.md` §15 |
| Bounded-excursion conjecture — valid throughout, spread $\le 2$, balance restored within 2 insertions | superseded by (S2) below, which drops the algorithmic half | `approach_15.md` §16 |
| **(S2)** every general binary instance admits a valid allocation of bundle-size spread $\le 2$; implies the main conjecture | **open — the current target**; verified exhaustively at $n=3,m=3$ (20,337,240 instances) and never violated up to $n,m\le 6$ | `approach_15.md` §18 |
| **(S1)** every dichotomous-goods and every negative-dichotomous instance admits a valid **balanced** allocation | **open**; never violated. Does not follow from [R3] (silent on bundle sizes) nor from [R2] (additive only) — needs a literature check | `approach_15.md` §18 |
| The constant 2 in (S2) is tight — no balanced allocation works on an explicit $n=3,m=3$ instance | **proved** (hand-checkable witness) | `approach_15.md` §19 |
| A welfare-maximiser over any permutation-closed family of allocations is envy-freeable | **proved** (two lines) — removes the envy-freeability half of (S2) | `approach_15.md` §19 |
| Global welfare maximisation fails: a **dichotomous goods** instance where every welfare-maximal allocation needs subsidy 2, though 0 is achievable | **proved** (explicit witness) | `approach_15.md` §19 |
| (S1)-goods $\iff$ (S1)-chores, via the size-shift being an envy-graph isometry on equal-cardinality allocations plus dummy padding | **proved** | `approach_15.md` §23 |
| Welfare-maximality *inside* the spread-2 family is not a selection rule — some maximisers there still need subsidy 2 | **refuted** (witness: 4 of 10 maximisers invalid); corrects the gap as first stated | `approach_15.md` §24 |
| Literature: nothing found covering (S1); PS2 open on [R11]'s own account (their §6) | **searched** against primary sources 2026-08-27 | `approach_15.md` §22, `map.md` §13 |
| First-excursion repair: every spread-2 state reached from balance in one insertion can be closed next step | **refuted** (Mainak) — a valid *balanced* state reaches the §8 dead state in one valid insertion; kills "spread $\le 2$", "unique max bundle" and "one step from balance" as invariants | `approach_15.md` §26 |
| Any invariant that is a property of the current state alone | **refuted** — the missing object is a *choice*, not a state property | `approach_15.md` §26 |
| Subsidy-pattern table: for valid $A$ with minimal $\subsidy\in\set{0,1}^n$, $w(i,j)\le \subsidy_i-\subsidy_j$; every positive arc runs paid $\to$ unpaid with weight exactly 1 | **proved** (Mainak); characterises valid states but does *not* separate safe from dead | `approach_15.md` §28 |
| **(SR-forced)** every maximal run of the steering rule "never leave balance without cause" ends complete | 0 dead ends in 22,200 instances, non-vacuous (86 forced departures) | `approach_15.md` §27 |
| At a forced state, is every valid successor safe? | **refuted** — 1,319 forced states have a dead successor; but the ones growing a **minimum-size bundle** never do | `approach_15.md` §30 |
| **(SR+)** = balanced move, else minimum-size-bundle move, else anything | 0 dead ends everywhere; in **both pure classes steps 2 and 3 never fire** | `approach_15.md` §30 |
| A single insertion preserves balance iff it grows a minimum-size bundle | **proved** (one line) | `approach_15.md` §31 |
| **(BAL-STEP)** from a valid balanced allocation, every unallocated item can be inserted into some minimum-size bundle, with a reassignment, landing valid | **open — the current target.** Holds in the strong EVERY-ITEM form in both pure classes (0 failures, ~71,000 balanced states each); with §23 it is **equivalent to all of (S1)** | `approach_15.md` §32 |
| **Free-insertion lemma**: $v_x(g\mid A_x)\ge 0$ and $v_i(g\mid A_x)\le 0$ for all $i$ $\Rightarrow$ no path weight rises, so $\subsidy$ cannot rise | **proved**; on chores it is exactly [R12]'s rule (R1). First version was wrong and the machine check caught it | `approach_15.md` §33 |

## 4. Formal statement of record

The framing above is written up, with proofs and citations, in
`report/working_general_binary/framing.tex` (compiled into
`working_general_binary.pdf` via that directory's driver). That file — not
this log — is the statement of record for the model, the conjecture, and the
transferred facts; approach sections should cite its numbered results rather
than re-derive them. This log records the trail.

## 5. Approach 15 — establishing the facts (2026-08-27)

First substantive pass, recorded in full in `approach_15.md`; scripts in
`updates_general_binary/update_1/`. Summary of what changed:

- The conjecture survived every search, including an **exhaustive** sweep of
  all 20,337,240 instances at $n=3$, $m=3$ over the whole class.
- The **positive** half of BKNS's mechanism transfers to the signed model
  intact; the **negative** half is impossible as a single-item step, so no
  algorithm that places items one at a time and never disturbs earlier
  placements can work. Our chores theorem being one-shot is therefore forced,
  not incidental.
- The frontier is now the **residual completion problem** (`approach_15.md`
  §10): complete an envy-free solution whose unallocated items have no $+1$
  recipient, in one shot, with the freedom to rebuild bundles.

**Second half of the pass — the residual completion problem, attacked and
refuted.** Dead states exist: valid partial allocations from which no
completion keeps $\subsidy \in \set{0,1}^n$, already inside the pure chores
class, so the problem is not about mixing signs. But the architecture it was
meant to serve survives, because those states are avoidable — a complete valid
allocation was reachable from the empty one in every instance tested.

That turns the question into a search for the steering rule, and the data
names one: **every dead state is unbalanced and has no $+1$ move**, so
balanced-or-$+1$ implies safe, with no counterexample in over 1.5 million
valid states. Balance is maintainable in both pure classes and not in the
mixed one, which is a precise account of why BKNS's proof and ours each work
and neither extends.

Open: the **bounded-excursion conjecture** (`approach_15.md` §16), and whether
Tao-Wu-Yu-Zhou's Algorithm 3 can close an excursion, despite the
local-to-global sign-flip gap.

---

*Scripts for this investigation go in `updates_general_binary/`, one
session folder per entry above, mirroring `updates/update_N/`'s relationship
to `RESIDUAL.md`.*
