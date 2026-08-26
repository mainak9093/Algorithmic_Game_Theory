# Glossary — Fair Division of Indivisible Goods with Subsidies

**Project reference, v1.** Every definition below is written in the Project notation
(fixed in the setup chat), *not* in the source paper's own symbols. Where a paper uses
different letters, that is flagged in §10.

**Project notation.** $N = [n]$ agents; $M$ items, $|M| = m$; valuation
$v_i : 2^M \to \mathbb{R}$ with $v_i(\emptyset) = 0$; allocation $A = (A_1,\dots,A_n)$;
subsidy vector $p \in \mathbb{R}^n_+$; entitlement weights $w_i > 0$; value matrix
$V^A_{ij} = v_i(A_j)$; $V$ = max item value; $W = \sum_i w_i$.

**Provenance tags.** `[R9 §2]` = Reading_9, Section 2. `[R1]`, `[R5]` are OCR-derived
(no text layer in those files), so section numbers there are approximate and exact
symbol forms should be checked against the PDF before being quoted in writing.

---

## 1. The model

**Indivisible good / item.** An object that cannot be split. The whole difficulty of
the field: with indivisibilities, exact envy-freeness can fail to exist for trivial
reasons (one item, two agents who both want it).

**Divisible good / money / subsidy.** A continuously divisible side-payment used to
patch up the indivisibility. In this literature money is supplied by an outside party
(a government, a court, an employer), *not* transferred between agents — so the
budget is not balanced, and "how much money is needed" becomes the object of study.

**Bundle.** A subset $A_i \subseteq M$ assigned to one agent.

**Allocation.** An *ordered* tuple $A = (A_1,\dots,A_n)$ of pairwise disjoint bundles.
The ordering matters enormously: much of the subsidy theory is about permuting a fixed
family of bundles among agents to make envy patchable. [R9 §2]

**Complete vs. partial allocation.** Complete: $\bigcup_i A_i = M$. Partial: some items
go unallocated. Several results (especially for matroid-rank valuations) only hold for
partial allocations. [R3 §2], [R8 §2]

**Balanced allocation.** All bundle cardinalities differ by at most one. A secondary
guarantee delivered by the Iterated Maximum Matching algorithm. [R2 §1]

**Instance.** The tuple $\langle N, M, (v_i)_{i\in N}\rangle$, or
$\langle N, M, (w_i)_{i\in N}, (v_i)_{i\in N}\rangle$ in the weighted setting.

**Value oracle model.** Valuations are not given as an explicit table (which would be
$2^m$ numbers); instead an algorithm may query $v_i(S)$ for any $S$ it constructs.
"Polynomial time" then means polynomial in $n, m$ and the number of oracle calls. [R9 §2]

**Unit demand.** An agent who values any nonempty bundle at the same amount as her best
single item — i.e., extra items are worthless. Used to construct counterexamples in the
weighted setting. [R6, Example 1.2]

**Rent division.** The classical special case $m = n$ with unit demand: assign rooms to
housemates and split a fixed rent. Historically the origin of the "envy-freeness with
money" question. [R9 §1]

**Quasi-linear utility.** Agent $i$'s utility is $v_i(A_i) + p_i$ — value plus money,
with money entering linearly and at the same exchange rate for everyone. Assumed
throughout the corpus. [R6 §1]

---

## 2. Valuation classes

Ordered roughly from most general to most restrictive. Which class you are in
determines almost every result in this corpus.

| Class | Definition | Note |
|---|---|---|
| **General** | Any $v_i : 2^M \to \mathbb{R}$ | EF1 may fail for $n \ge 3$ |
| **Monotone** | $v_i(S) \le v_i(T)$ whenever $S \subseteq T$ | equivalently, every item is a *good* for everyone |
| **Doubly monotone** | every item is either a good or a chore *for each agent* | strictly wider than monotone; the setting of [R9] |
| **Subadditive / superadditive** | $v_i(S\cup T) \le$ (resp. $\ge$) $v_i(S)+v_i(T)$ for disjoint $S,T$ | superadditivity is the hypothesis of the VCG result in [R6 §4] |
| **Submodular** | $v_i(S\cup\{g\}) - v_i(S) \ge v_i(T\cup\{g\}) - v_i(T)$ for $S \subseteq T$, $g \notin T$ | diminishing marginal returns |
| **Supermodular** | reverse inequality | increasing returns; [R6 §4] |
| **Additive** | $v_i(S) = \sum_{g\in S} v_i(g)$ | the workhorse assumption of [R1], [R2], [R4] |
| **Dichotomous** | every marginal is $0$ or $1$: $v_i(S\cup\{g\}) - v_i(S) \in \{0,1\}$ | *no* additivity, submodularity, or even subadditivity assumed — this is the point of [R3] and [R5] |
| **General binary** | every marginal is $-1$, $0$, or $1$: $v_i(S\cup\{g\}) - v_i(S) \in \{-1,0,1\}$ | goods and chores together: an item may be a good for one agent and a chore for another, and a single agent's marginal for an item may change sign with $S$. Strictly wider than **Dichotomous** and than its negative mirror ($\{0,-1\}$, the setting of the closed result); **not** contained in **Doubly monotone**, so [R9]'s bound does not apply to it. The setting of `PS2_general_binary.md`. |
| **Matroid-rank / binary submodular** | dichotomous **and** submodular | equivalently $v_i$ is the rank function of a matroid on $M$; the setting of [R8] |
| **Binary additive** | additive with $v_i(g) \in \{0,1\}$ | strictly inside matroid-rank |
| **Bi-valued** | $v_i(g)$ takes one of two values | a tractable special case in house allocation [R7 §5] |
| **Identical** | $v_1 = \dots = v_n$ | |
| **Identical items** | all items interchangeable (apportionment) | [R6 §8] |

**Good / chore (for agent $i$).** Item $e$ is a *good* for $i$ if
$v_i(S\cup\{e\}) \ge v_i(S)$ for all $S$; a *chore* if $v_i(S\cup\{e\}) \le v_i(S)$ for
all $S$ with at least one strict. An item can be a good for one agent and a chore for
another. [R9 §2]

**Marginal gain / marginal loss.** $\Delta^+_i(S,g) := v_i(S\cup\{g\}) - v_i(S)$ for
$g \notin S$; $\Delta^-_i(S,g) := v_i(S) - v_i(S\setminus\{g\})$ for $g \in S$. These are
distinct objects for non-additive $v_i$ and both appear in the [R8] fairness notions. [R8 §2]

**Normalization / scaling.** Every absolute subsidy bound needs one, or you can inflate
the required subsidy by rescaling. Two versions appear in this corpus:
- $v_i(g) \le 1$ for every agent and every item (additive setting): [R1], [R2], [R3]
- $|v_i(S\cup\{e\}) - v_i(S)| \le 1$ for all $i, e, S$ — two-sided, so it also caps chore
  disutility: [R9 §2]

These are **not** the same hypothesis. Check which one a bound is stated under before
comparing bounds across papers.

---

## 3. Fairness notions — unweighted

**Envy-freeness (EF).** $v_i(A_i) \ge v_i(A_j)$ for all $i,j$. Due to Foley (1967).
Fails to exist for indivisible goods. [R1 Def. 1], [R3 Def. 1]

**EF1 (envy-freeness up to one good).** Two inequivalent forms in this corpus:

- *Goods-only form* [R1]: for all $i,j$, either $v_i(A_i) \ge v_i(A_j)$ or there
  is $g \in A_j$ with $v_i(A_i) \ge v_i(A_j \setminus \{g\})$. Remove one item from the
  **envied** bundle.
- *Two-sided form* [R9 §1]: for all $i,j$ there is $X \subseteq A_i \cup A_j$ with
  $|X| \le 1$ and $v_i(A_i\setminus X) \ge v_i(A_j \setminus X)$. Remove one item from
  **either** bundle.

They coincide when all items are goods. With chores present they do not — the two-sided
form is the right one, and is what makes EF1 existence hold for doubly monotone
valuations. Do not silently swap them.

**EFk.** The two-sided EF1 condition with $|X| \le k$. [R9 §2]

**EFX (envy-freeness up to any good).** For all $i,j$ and **every** $g \in A_j$,
$v_i(A_i) \ge v_i(A_j\setminus\{g\})$. Strictly stronger than EF1 ("any" vs. "some").
General existence is a major open problem; known for $n=2$, for $n=3$ under restricted
valuations, and for matroid-rank valuations. [R5] extends existence to dichotomous goods
(binary marginals, not necessarily submodular) valuations. [R5 §1]

> Caution: the literature distinguishes **EFX$_0$** (remove *any* good, including
> zero-marginal ones) from **EFX$_+$** (remove only positively-valued goods). These
> genuinely differ under binary valuations. Verify which convention [R5] uses directly
> from the PDF — my copy is OCR only.

**MEF1 (marginal EF1).** Caragiannis et al. (2019). Replaces "$i$'s value for $j$'s
bundle" with "$i$'s *marginal* value for $j$'s bundle on top of her own", i.e.
$v_i(A_i \cup A_j) - v_i(A_i)$. The natural repair for non-additive valuations, where
$v_i(A_j)$ overstates what $i$ would actually gain. The unweighted ancestor of WMEF.
[R8 §1.1]

**Proportionality.** $v_i(A_i) \ge \frac{1}{n} v_i(M)$. A *threshold* notion, not a
comparative one — weaker than EF. [R8 §1.2]

**Maximin share (MMS).** Relaxation of proportionality: $i$'s MMS is the best she could
guarantee herself by partitioning $M$ into $n$ bundles and taking the worst. Also weaker
than EF. Mentioned but not used in this corpus. [R8 §1.2]

**Equitability.** All agents get equal utility. Studied jointly with EF-plus-subsidy by
Aziz; cited but not developed here. [R9 §1], [R6 §1.2]

---

## 4. Fairness notions — weighted (unequal entitlements)

**Weight / entitlement $w_i > 0$.** A publicly recognized claim to a larger share:
shares in a partnership, family size in housing, seats in an apportionment. All notions
below reduce to their unweighted counterparts when all $w_i$ are equal.

**WEF (weighted envy-freeness).**
$$\frac{v_i(A_i)}{w_i} \;\ge\; \frac{v_i(A_j)}{w_j} \qquad \forall i,j \in N.$$
Read $v_i(A_i)/w_i$ as *value per unit entitlement*. With subsidies, the outcome $(A,p)$
is WEF if
$$\frac{v_i(A_i) + p_i}{w_i} \;\ge\; \frac{v_i(A_j) + p_j}{w_j} \qquad \forall i,j.$$
[R6 Def. 2.1], [R4 §1], [R7 Def. 2.1]

**WEF-able (weighted envy-freeable).** There exists $p \ge 0$ making $(A,p)$ WEF.
[R6 Def. 2.1], [R7 §4]

**WEF1.** Weighted EF1 (Chakraborty et al. 2021a): after removing some good from $j$'s
bundle, $i$'s per-entitlement value is at least $j$'s. Equal to WEF$(1,0)$ below. [R8 §1]

**WEF$(x,y)$**, Chakraborty et al. For $x,y \in [0,1]$: for each $i,j$ there exists
$B \subseteq A_j$ with $|B|\le 1$ such that
$$\frac{v_i(A_i) + y\,v_i(B)}{w_i} \;\ge\; \frac{v_i(A_j) - x\,v_i(B)}{w_j}.$$
So $i$ may both *discount* $x$ times a good in $j$'s bundle and *credit herself*
$y$ times that good. Attention is almost always restricted to $y = 1-x$.
$x=1$ gives WEF1; larger $x$ favours **lower**-weight agents. Unlike the unweighted case
there is no single canonical relaxation — $x$ parameterizes a genuine trade-off between
satisfying small- and large-entitlement agents. [R6 Def. 5.11], [R8 §1, Ex. 1.2]

**WWEF1 (weak WEF1).** For each $i,j$ with $A_j \ne \emptyset$ there is $o \in A_j$ such
that **either** $\frac{v_i(A_i)}{w_i} \ge \frac{v_i(A_j\setminus\{o\})}{w_j}$ **or**
$\frac{v_i(A_i)+v_i(o)}{w_i} \ge \frac{v_i(A_j)}{w_j}$. Either *remove* the good from
$j$'s bundle or *copy* it into $i$'s. Weaker than WEF$(x,1-x)$ for every $x$.
[R6 Def. 5.12], [R8 §1]

**TWEF$(x,y)$ (transferable WEF).** For each $i,j$: **either** $v_i(A_i) = v_i(A_i\cup A_j)$
(so $i$ gains nothing even from absorbing $j$'s entire bundle — she has no legitimate
complaint) **or** there is $g \in A_j$ with
$$\frac{v_i(A_i) + y\,\Delta^+_i(A_i,g)}{w_i} \;\ge\; \frac{v_i(A_j) - x\,\Delta^-_i(A_j,g)}{w_j}.$$
Reduces to WEF$(x,y)$ under additive valuations. Designed for matroid-rank valuations.
[R8 Def. 2.2]

**WMEF$(x,y)$ (weighted marginal EF).** For each $i,j$: either $A_j = \emptyset$ or there
is $g \in A_j$ with
$$\frac{v_i(A_i) + y\,\Delta^+_i(A_i,g)}{w_i} \;\ge\; \frac{v_i(A_i\cup A_j) - v_i(A_i) - x\,\Delta^-_i(A_i\cup A_j, g)}{w_j}.$$
The right-hand numerator is $i$'s *marginal* value for $j$'s bundle. Reduces to
WEF$(x,y)$ under additive valuations; achievable for **general submodular** valuations,
unlike TWEF. Note the asymmetry: WMEF$(x,1-x)$ reduces to MEF1 in the unweighted case
**only** when $x=1$. [R8 Def. 2.3]

**Relationship.** TWEF$(x,1-x) \Rightarrow$ WMEF$(x,1-x)$; the converse fails. [R8 Prop. 2.4]

**WWMEF1 (weak weighted marginal EF1).** The "remove-or-copy" weakening of WMEF, in the
same spirit as WWEF1. What MWNW can be guaranteed to satisfy. [R8 Def. 4.2]

**MWEF (monetarily weighted EF).** An outcome $(A,p)$ where $p_j = 0$ for every agent $j$
toward whom somebody has weighted envy. I.e., money is never wasted on an agent who is
already envied. Deliberately says nothing about whether $A$ itself is fair. [R6 Def. 9.1]

---

## 5. Subsidy machinery

This is the technical core shared by [R1], [R2], [R9] and generalized by [R6], [R7].

**Envy-free solution $(A,p)$.** An allocation together with a subsidy vector such that
$v_i(A_i) + p_i \ge v_i(A_j) + p_j$ for all $i,j$. [R3 Def. 2], [R9 §2]

**Envy-freeable (EF-able).** $A$ is envy-freeable if some $p \ge 0$ makes $(A,p)$
envy-free. A property of the **allocation alone**. [R2 §2.1], [R9 §2.1]

**Envy-eliminating subsidy.** Any such $p$. [R9 §2.1]

**Envy graph $G_A$.** Complete directed graph on vertex set $N$, with arc $(i,j)$
weighted by $i$'s envy of $j$: $v_i(A_j) - v_i(A_i)$. [R2 §2.1]

**Weighted envy graph $G_{A,w}$.** Same vertex set, arc cost
$\text{cost}_A(i,j) = \frac{v_i(A_j)}{w_j} - \frac{v_i(A_i)}{w_i}$.
Costs may be negative. [R6 Def. 3.2]

**Reassignment-stable.** $\sum_i v_i(A_i) \ge \sum_i v_i(A_{\sigma(i)})$ for every
permutation $\sigma$ — no relabelling of the *same* bundles among the *same* agents raises
utilitarian welfare. Weighted version:
$\sum_i \frac{v_i(A_i)}{w_i} \ge \sum_i \frac{v_i(A_{\sigma(i)})}{w_{\sigma(i)}}$. [R6 Def. 3.1]

> Sharp point worth remembering: with equal weights, reassignment-stability says $A$
> maximizes a sum of utilities. With unequal weights it does **not** imply $A$ maximizes
> anything — the objective changes as the permutation changes, because the denominator
> travels with the agent. This is exactly why the unweighted theory does not port over.
> [R6 §3]

**Halpern–Shah characterization.** For an allocation $A$, the following are equivalent:
(a) $A$ is envy-freeable; (b) $A$ is reassignment-stable; (c) $G_A$ has no
positive-weight directed cycle. [R1], restated as [R2 Thm. 2.1], weighted analogue at
[R6 Thm. 3.3], house-allocation analogue at [R7 §4].

**Maximum-weight permutation.** A $\sigma$ maximizing $\sum_i V^A_{i\sigma(i)}$, i.e. a
max-weight perfect matching in the bipartite agent–bundle graph. Reassigning bundles
according to $\sigma$ turns any allocation into an envy-freeable one **in the unweighted
setting only** — [R4 Ex. 1.1] shows this fails under weights. [R9 §2.1]

**Minimum subsidy vector $p^*$.** The componentwise-least envy-eliminating subsidy; it
exists and is unique because the feasible polyhedron is closed under componentwise min.
**Characterization:** $p^*_i$ equals the maximum-weight directed path in the envy graph
starting at $i$ — well defined precisely because no positive cycle exists. Computable by
Floyd–Warshall. [R1 Thm. 2], [R2 Obs. 1], [R9 Lem. 1]

**LP-duality view.** $p$ and the auxiliary vector $q_i = \max_j (v_i(A_j)+p_j)$ are the
dual variables of the assignment LP whose primal is the max-weight matching above.
Complementary slackness ties them together. Useful when you want a bound rather than an
algorithm. [R9 §2.1]

**Maximum vs. total subsidy.** $\|p\|_\infty = \max_i p_i$ (per agent) and
$\|p\|_1 = \sum_i p_i$ (total). Papers bound one, the other, or both; a per-agent bound
of $c$ only gives a total bound of $nc$, which is usually far from tight. Always record
which one a theorem gives.

---

## 6. Efficiency and welfare

**Pareto domination / Pareto optimality (PO, Pareto efficiency).** $A'$ dominates $A$ if
$v_i(A'_i) \ge v_i(A_i)$ for all $i$ with at least one strict inequality. $A$ is PO if
nothing dominates it. [R6 Def. 2.2], [R8 §2]

**Utilitarian social welfare.** $\mathrm{SW}(A) = \sum_i v_i(A_i)$; restricted to a
subset $S$, $\mathrm{SW}_S(A) = \sum_{i\in S} v_i(A_i)$. **MSW** = an allocation
maximizing it. Every MSW allocation is PO; not conversely. [R6 Def. 2.4]

> Note the terminology trap in [R8]: "**unweighted** utilitarian welfare" means
> $\sum_i v_i(A_i)$ *even in the weighted setting* — the weights are deliberately not
> used in the objective.

**Nash social welfare (NSW).** $\prod_i v_i(A_i)$. **MNW** maximizes it. **MWNW**
(maximum weighted Nash welfare) maximizes $\prod_i v_i(A_i)^{w_i}$, with the standard
tie-breaking rule: first maximize the number of agents with positive utility, then
maximize the product over those agents. [R8 Def. 4.1]

**Weighted harmonic welfare (MWHW$_x$).** [R8]'s own construction:
$\sum_i w_i H_{v_i(A_i),x}$ where $H_{k,x} = \frac{1}{1-x} + \frac{1}{2-x} + \dots + \frac{1}{k-x}$
is a shifted harmonic number ($H_{k,0}$ is the ordinary harmonic number). Under
matroid-rank valuations this gives *stronger* fairness guarantees than MWNW — the
paper's headline surprise. [R8 §6]

**Clean / non-redundant allocation.** Every item an agent holds strictly contributes:
$\Delta^-_i(A_i,g) > 0$ for all $i$ and $g \in A_i$. Under matroid-rank valuations this
is equivalent to $v_i(A_i) = |A_i|$ for all $i$. Cleanness is a *hypothesis* in most
matroid-rank theorems, and clean allocations may be incomplete. [R8 Def. 2.1],
[R6 Def. 7.3]

**Non-wasteful.** No item can be moved from its holder (who does not need it) to someone
who would gain from it. Weaker than PO. [R6 Def. 2.3]

**Non-zero social welfare property.** $\mathrm{SW}(A) = 0$ only if *every* allocation has
zero welfare. A deliberately weak efficiency axiom introduced because WEF-ability and
non-wastefulness turn out to be incompatible. [R6 Def. 2.5]

---

## 7. Algorithms and mechanisms

**Envy-cycle elimination** (Lipton–Markakis–Mossel–Saberi 2004). Allocate items one at a
time to an unenvied agent; when everyone is envied, the envy graph has a cycle, so
rotate bundles along it. Yields EF1 for monotone valuations in polynomial time. The
standard starting point for "take an EF1 allocation, then subsidize". [R9 §4]

**Iterated maximum matching** [R2]. Repeatedly compute a maximum-weight matching between
agents and remaining items and hand out one round of items. Produces an allocation that
is simultaneously envy-freeable, EF1, and balanced, with $\le 1$ per agent for additive
valuations. Explicitly **fails** to give WEF once entitlements differ. [R2 Thm. 1.3],
[R4 Ex. 1.1], [R6 Ex. 1.1]

**Picking sequence.** A prescribed order of turns in which agents pick their favourite
remaining item (highest marginal gain, in the submodular version). **Round-robin** is
the sequence $1,2,\dots,n,1,2,\dots$. The weighted versions realize WEF$(x,1-x)$ /
WMEF$(x,1-x)$. [R8 §3]

**Transfer algorithm.** Start from a clean utilitarian-welfare-maximizing allocation;
while some TWEF$(x,1-x)$ condition is violated, transfer one good from the envied agent
to the envious one. Terminates in polynomial time (nontrivially, in the weighted case).
[R8 §5, Alg. 1]

**Yankee Swap / General Yankee Swap (GYS).** Viswanathan–Zick's framework for
matroid-rank valuations: agents take turns, and a turn may trigger a chain of item
transfers. Produces non-redundant allocations. Adapted to unequal entitlements by
[R4 §5] / [R6 §7]. [R6 §7]

**Envy-graph procedure** (Chaudhury et al. 2021). Pseudo-polynomial algorithm returning a
*partial* EFX allocation with at most $n-1$ items unallocated and nobody envying the
unallocated pool. [R5] shows binary valuations admit extra update steps that place the
leftovers while preserving EFX, and make the whole thing polynomial. [R5 §1.1]

**VCG mechanism.** Choose a welfare-maximizing allocation and charge each agent her
externality: $\mathrm{SW}_{N\setminus\{i\}}(A') - \mathrm{SW}_{N\setminus\{i\}}(A)$ where
$A'$ is optimal without $i$. Truthful. Used in [R6 §4] with a large upfront subsidy to
get WEF under superadditive valuations. [R6 Def. 4.2]

**Strategy-proofness / truthfulness.** No agent can gain by misreporting $v_i$. Mostly
peripheral here, but the *subsidized egalitarian mechanism* (Goko et al.) achieves it
with $\le 1$ per agent, $\le n-1$ total, for binary submodular valuations. [R9 §1],
[R4 §1.1]

**Prioritized egalitarian mechanism** (Babaioff–Ezra–Feige). For matroid-rank valuations:
maximizes Nash welfare, is EFX, and is utilitarian-optimal. [R9 §1], [R5 §1]

**Complexity vocabulary.** *Strongly polynomial* — running time independent of the
numeric magnitudes ([R1]'s minimum-subsidy algorithm). *Pseudo-polynomial* — polynomial
in the numeric values, not their encoding length ([R5]'s cited EFX partial-allocation
result). *FPTAS* — $(1+\epsilon)$-approximation in time polynomial in input and
$1/\epsilon$; Caragiannis–Ioannidis give one for minimum subsidy with constantly many
agents. [R3 §1]

---

## 8. House allocation ([R7] only)

**House allocation problem.** $m \ge n$ houses, each agent receives **exactly one**.
So $A_i \in H$ is a single house, not a bundle, and an allocation is an
$N$-saturating matching in the agent–house bipartite graph. [R7 §2]

**Why this is not a special case of the general model.** The cardinality constraint is
binding. [R7]'s central negative result is that weighted envy-freeable allocations may
**fail to exist** under this constraint — even though in unconstrained fair division,
where all items must be allocated with no cap per agent, they always do. The
non-existence is produced jointly by the weights and the constraint, not by either
alone. [R7 Result 2]

**Two types of agents / bi-valued utilities.** Restrictions under which [R7] recovers
existence plus polynomial-time computation. [R7 §5]

---

## 9. Standing conjectures and settled questions named in the corpus

- **Halpern–Shah Conjecture 1.1** (subsidy $\le n-1$ total for additive valuations with
  $v_i(g)\le 1$): **proved** by [R2 Thm. 1.3], in the stronger per-agent form $\le 1$ each.
- **Halpern–Shah Conjecture 1.2** (an allocation exists that is simultaneously
  envy-freeable and EF1): **proved** by [R2], which also gets balancedness.
- **Open Question 9** of the Liu–Lu–Suzuki–Walsh survey (can the $2(n-1)^2$ total-subsidy
  bound for monotone valuations be improved?): addressed by [R9], which gives
  $n(n-1)/2$ in the doubly monotone model and $(n^2-n-1)/2$ for monotone with $n\ge 3$.
- **Chakraborty et al.'s open direction** (find envy-based notions that survive
  non-additive valuations in the weighted setting): answered by [R8] with TWEF and WMEF.
- **Existence of EFX in general**: still open. [R5] settles the dichotomous goods
  (binary-marginal, goods-only) case.
- **Minimum-subsidy computation**: NP-hard in general, and even in the binary additive
  case under non-wastefulness [R1 Cor. 1]; hard to approximate for super-constant $n$
  (Caragiannis–Ioannidis). [R6 §1.2] gives a poly-time exact minimum for the
  identical-items case only.

---

## 10. Cross-paper conflicts to watch

These are real; each has bitten someone.

1. **$w$ means two different things.** [R9 §2.1] uses $w_{i,j} = v_i(A_j)$ as a *weight
   matrix* for the max-weight-permutation argument. [R4], [R6], [R7], [R8] use $w_i$ for
   an agent's *entitlement*. Project convention: $w_i$ = entitlement only; the value
   matrix is $V^A$.

2. **Subsidy symbol.** $p$ in [R1], [R3], [R6], [R9]; $s$ in [R4]; "payment vector $p$"
   in [R2]. Project convention: $p$.

3. **Allocation symbol.** $A$ in [R1], [R2], [R3], [R8], [R9]; $X$ in [R6]. Project
   convention: $A$.

4. **Item-set symbol.** $M$ in [R6], [R9]; $G$ in [R8]; $[m]$ in [R3]; $H$ (houses) in
   [R7]. Project convention: $M$.

5. **EF1 has two inequivalent definitions** across [R1] and [R9] — see §3. Only the
   two-sided version supports the doubly monotone results.

6. **Normalization differs** — one-sided $v_i(g)\le1$ vs. two-sided $|{\Delta_i}|\le1$ —
   see §2. Bounds are not comparable across this line without saying which.

7. **"Clean" = "non-redundant".** [R8] says clean; [R6], following Viswanathan–Zick, says
   non-redundant. Same property.

8. **$w_1$ vs. $w_{\min}$.** [R4] sorts weights increasingly and writes $w_1$ for the
   smallest; [R6] writes $w_{\min}$. Same quantity, and the bounds
   $(W/w_1 - 1)$ and $(W/w_{\min} - 1)$ are the same bound.

9. **[R4] is subsumed by [R6].** [R6] is the merged journal-length version combining
   Elmalem et al. (2024) = [R4] with Aziz et al. (2024). Cite [R6] unless you
   specifically need [R4]'s phrasing; every [R4] bound reappears in [R6], usually
   strengthened.

---

*End of v1. Add new terms here rather than in chat, so the Project has one canonical
reference.*
