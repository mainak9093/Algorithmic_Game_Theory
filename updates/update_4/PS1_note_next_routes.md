# PS1 working note — routes after the encoding approaches closed

**Version** v1, 2026-08-03.
**Status** Conjecture D (double refinement) is **new and open**, supported by ~1600 random
instances with zero failures. Proposition IMM is **refuted** with counterexamples.
Everything else is a labelled proposal, not a result.
**Reproduce** `rules.py`.

---

## 0. What is closed and what that leaves

Two whole families are now shut:

* **Valuation-level encoding of coverage** (penalties, item weights) — no dichotomous
  reweighting of the replica instance can force coverage (`PS1_note_weighted_penalty_no_go.md`).
* **Algorithm-level weight forcing inside R3** — `FINDSINK` runs precisely where every
  candidate's marginal is $0$, so no weight can move the recipient's subsidy
  (`PS1_note_type_order_and_findsink.md`, Theorem F2).

Both failures share one cause: **they try to steer a procedure that is blind at exactly
the moment it must choose.** The routes below therefore split into (i) *choose the
allocation by a global criterion, with no procedure at all*, and (ii) *change the procedure
so it is never blind*.

---

## 1. Route D — global selection by double refinement  ⭐ strongest lead

Halpern–Shah force any envy-freeable allocation to be reassignment-stable, so restricting
to **utilitarian-optimal** allocations is free. The known problem is that utilitarian
optimality alone is necessary but not sufficient: previous sessions found *some* optimal
allocation is always good, but no rule that picks one.

The three independent balance signals — the size-shift theorem (chores $=$ goods $+$
cardinality balancing), R2's balancedness guarantee, and the balance remark in
`approach_3.tex` (all reachable terminals on the witness are the six perfect matchings) —
say the missing ingredient is **balance**. Adding it as a lexicographic refinement:

**Conjecture D.** Let $\mathcal U$ be the set of utilitarian-optimal partitions (minimising
$\sum_i \cost_i(\bundle{i})$). Refine to those minimising, lexicographically,
$$\text{(i) } \big(|\bundle{1}|,\dots,|\bundle{n}|\big)^{\downarrow}
\quad\text{then}\quad
\text{(ii) } \big(\cost_1(\bundle{1}),\dots,\cost_n(\bundle{n})\big)^{\downarrow}.$$
Then **every** allocation surviving both refinements has $\pathw{}(i) \le 1$ for all $i$.

**Evidence.** `rules.py`, exhaustive over all $n^m$ partitions per instance, checking the
*entire* selected set (not one arbitrary representative):

| $n,m$ | trials | selected set contains **no** good allocation | selected set contains a **bad** one |
|---|---|---|---|
| 3,3 | 400 | 0 | 0 |
| 3,4 | 250 | 0 | 0 |
| 3,5 | 120 | 0 | 0 |
| 3,6 | 40 | 0 | 0 |
| 4,3 | 200 | 0 | 0 |
| 4,4 | 80 | 0 | 0 |

Neither refinement alone suffices: over a further 800 instances, cardinality-balance alone
admitted a bad allocation once and cost-leximin alone three times. **Both orderings of the
pair survive** (balance-then-leximin and leximin-then-balance), which is a hint that the
two are cutting at the same structure. On the obstruction witness the selected set is
exactly the six perfect matchings, with $\pathw{} = 0$ — reproducing the balance remark
from a fourth direction.

**Why this is the right shape of target.** It is a *closed-form* criterion: no schedule, no
insertion order, no coverage constraint, hence none of the dead ends. It sidesteps the
whole replica/peel apparatus rather than repairing it.

**Proof obligation.** Show that any partition with $\pathw{}(i) \ge 2$ for some $i$ admits a
modification that strictly improves the lexicographic key $(\text{welfare}, \text{balance},
\text{leximin})$. Concretely: a heaviest path $i \to k \to \dots$ of weight $\ge 2$ should
certify a chore transfer or bundle exchange that either raises welfare (contradicting
optimality), or preserves welfare while flattening the cardinality vector, or preserves both
while flattening the cost vector. The first case is Halpern–Shah; the other two are new and
are where the work is. Worth attempting for $n=3$ first, where the path has length $\le 2$.

**Next experiments.** (a) push to $n=3, m=7\text{–}8$ and $n=5$; (b) test whether the
refinement is *necessary* — i.e. how large the good set is relative to the selected set;
(c) test structured adversarial families (supermodular $\cost_1$, unit-demand others)
rather than uniform random.

---

## 2. Route M — iterated matching, and why the additive proof does not lift

`Reading_11` (Lu, Mackenzie, Suzuki, *Optimal Subsidy Bounds for Goods and Chores: One
Dollar Each Suffices*, arXiv 2607.10089, Jul 2026) proves **one dollar per agent for mixed
manna with additive utilities in $[-1,1]$**, and its §3 develops the objective-chores
analogue of R2's iterated maximum-weight matching (IMWPM) with telescoping envy-path
bounds. That subsumes our binary-additive chores theorem and is the closest existing result
to PS1.

**Proposition IMM (refuted).** The obvious lift — iterated minimum-*marginal* perfect
matching, i.e. each round assign every agent one remaining chore minimising
$\sum_i [\cost_i(\bundle{i}\cup\{g_i\}) - \cost_i(\bundle{i})]$, padding with zero-cost
dummies — does **not** give $\pathw{} \le 1$ for non-additive dichotomous costs.
Failures: 13/250 at $n{=}3,m{=}4$ and 10/120 at $n{=}3,m{=}5$ (`rules.py`).

This is diagnostic rather than discouraging. Reading_11 itself flags the obstacle: their
telescoping argument needs additivity, because with additive costs the round-$t$ chore's
cost is independent of what came before, whereas a dichotomous marginal depends on the
bundle already held. The repair to attempt is a **round-invariant** replacing the additive
domination $\cost_i(\bundle{i}^t) \le \cost_i(\bundle{j}^{t+1})$ — for instance requiring
that each round's matching be minimum-cost *conditioned on the current bundles* and that
the marginals be non-increasing across rounds (a "peel the free chores first" discipline).

**Action item.** Readings 10 and 11 are in the Project but absent from
`paper_map_R1_to_R9.md`. Both need entries; Reading_11 in particular changes the frontier
table, and Reading_10 (Bhaskar, Sricharan, Vaish, *On Approximate Envy-Freeness for
Indivisible Chores and Mixed Resources*) supplies the **NP-completeness of deciding EF
existence for binary additive chores**, which is a hardness datum this project should be
citing.

---

## 3. Route N — non-redundancy instead of coverage

Theorem F2 says the failing placements are exactly the zero-marginal ones. The literature
already has a name for forbidding those: **non-wastefulness / non-redundancy** (R6
Def. 2.3 — no item sits with an agent who gains nothing from it while another agent would
gain). A duplicate copy is redundant for its holder by construction.

So instead of asking for coverage directly, ask R3's algorithm — or General Yankee Swap,
which is built to maintain non-redundancy — for a **non-redundant** allocation of the
replica set, and ask how far non-redundancy falls short of coverage. It is not equivalent:
a duplicate can be redundant for *everyone* when all other agents either already hold the
type or have zero marginal for it. But that residual gap is much narrower than coverage
itself, and it is exactly characterisable. Worth one session: enumerate non-redundant
non-coverage replica allocations on small instances and see whether any of them is good.

---

## 4. Route A — induction on agents rather than on items

Every approach so far inducts on *items* (insert a chore, peel a chore, hand out a copy).
`Reading_11` §4.3.1 does something different: it maintains a set of **active agents** and
adds agents one at a time, restoring invariants (I1) compensated utility $\ge \lambda$ with
$\lambda \le p_i \le 1$, and (I2) every active agent has an equality path to the set of
minimum compensated utility. Chores are then redistributed to the newcomer.

For chores this template is attractive because a new agent starts with an empty bundle,
i.e. zero cost, which is the *best* bundle — so the newcomer is the natural sink and the
orientation problem of Approach 1 does not arise. The invariant to carry is the equality
graph, not a subsidy scalar, which is precisely the extra information Theorem F2 says a
recipient rule needs.

---

## 5. Route X — matroid exchange on the parallel-copy matroid

Already flagged in `approach_3.tex` §MRF and still unattempted. Supermodular dichotomous
costs dualise to matroid rank functions; lifting through $\tau$ is the parallel extension.
The witness of the insertion obstruction lies inside this class. Basis exchange in the
parallel-copy matroid is the strongest machinery available in the surrounding literature
(R5's and Babaioff–Ezra–Feige's arguments), and it sits between the closed binary-additive
theorem and the full conjecture. The parallel-extension step needs a full proof before
anything is built on it.

---

## 6. Ranking

1. **Route D** — best evidence, cleanest statement, no scheduling. Attempt the $n=3$ proof.
2. **Route M** — closest published result; read Reading_11 §3 properly and map the paper.
3. **Route A** — genuinely new induction axis, and Reading_11 supplies a worked template.
4. **Route N** — cheap to test, narrows the coverage gap even if it does not close it.
5. **Route X** — highest ceiling, highest cost; the intermediate target, not the first move.

Conjecture H1″ (type-ordered peel, previous note) stays live as a fallback but is now
second to Route D, because D needs no schedule at all.
