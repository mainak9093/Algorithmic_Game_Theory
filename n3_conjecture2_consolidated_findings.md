# n=3 Conjecture 2 — Consolidated Findings Before the General-Dichotomous Attack

## Executive status

This document consolidates the mathematically meaningful results obtained so far.

The main goal is **Conjecture 2 for negative dichotomous costs**, with special focus on `n = 3`.

The central state of the project is now:

- The assignment/matching side of the `n=3` problem is essentially understood.
- The remaining `n=3` existence question is a total-spread statement, called **Lemma E / Lemma E′** in the project.
- The previously difficult **set/Venn/composed-cost branch has now been closed by Target T**.
- The stronger conjecture “all three arbitrary dichotomous costs can simultaneously have spread at most 1” is **false**.
- The remaining frontier is therefore the genuinely **arbitrary-dichotomous** case, where costs need not be functions of a single underlying set cardinality.

This document deliberately distinguishes:
1. formally established mathematics,
2. exhaustive finite/computer-assisted results,
3. open statements.

Do not upgrade computational evidence into a symbolic theorem without a separate proof.

---

# 1. Core model

Let `M` be a finite set of indivisible chores/items and let there be three agents.

A cost function `c_i: 2^M -> Z_{\ge 0}` is **negative dichotomous** if

\[
c_i(\varnothing)=0
\]

and for every `S ⊆ M` and `g ∉ S`,

\[
c_i(S)\le c_i(S\cup\{g\})\le c_i(S)+1.
\]

Thus every marginal cost is in `{0,1}`.

For a partition

\[
B=(B_1,B_2,B_3),
\]

define agent `i`'s spread

\[
\operatorname{sp}_i(B)
=
\max_t c_i(B_t)-\min_t c_i(B_t),
\]

and total spread

\[
\Sigma(B)=\sum_{i=1}^3\operatorname{sp}_i(B).
\]

---

# 2. Conjecture 2 at n=3

The project's main conjecture asks for an envy-free allocation with subsidy vector in `{0,1}^n`.

At `n=3`, the established route is:

\[
\boxed{
\text{find a partition }B\text{ with }\Sigma(B)\le3
}
\]

then choose a minimum-cost assignment of the three bundles to agents.

This is because of the `n=3` goodness lemma described below.

The project file explicitly identifies the existence statement

\[
\boxed{
\text{Lemma E: every three-agent dichotomous instance admits }\Sigma\le3
}
\]

as the remaining combinatorial core.

---

# 3. Normalization and the minimum-cost matching formulation

For a fixed partition `B`, define

\[
v_i(t)=c_i(B_t)-\min_s c_i(B_s).
\]

Then:

- `v_i(t) >= 0`;
- at least one coordinate of each `v_i` is zero;
- 
\[
\operatorname{sp}_i(B)=\max_t v_i(t).
\]

If `σ` is an assignment of bundles to agents, then

\[
\sum_i c_i(B_{\sigma(i)})
=
\sum_i v_i(\sigma(i))+\text{constant}.
\]

Thus a minimum-cost assignment minimizes

\[
F(\sigma)=\sum_i v_i(\sigma(i)).
\]

Write

\[
x_i=v_i(\sigma(i)).
\]

The project records exactly this normalization and matching reduction.

---

# 4. The n=3 goodness criterion

For the minimum-cost assignment, the normalized envy graph is controlled entirely by the `v_i`.

The project establishes:

> A minimum-cost assignment is good iff
>
> 1. every directed envy-arc has weight at most `1`, and
> 2. there is no directed two-path of weight `2`.

Using the normalized assignment values `x_i`, this becomes:

\[
x_i\le1
\]

for every `i`, together with the explicit forbidden two-path pattern.

This is important because it reduces the subsidy question to a tiny `3×3` combinatorial problem.

---

# 5. Lemma A — the decisive matching-side implication

The project proves:

> **Lemma A.** For `n=3`, if a partition admits a minimum-cost assignment with:
>
> - an arc of weight at least `2`, then
>   \[
>   \Sigma(B)\ge4;
>   \]
> - all arcs at most `1` but a two-path of weight `2`, then
>   \[
>   \Sigma(B)\ge5.
>   \]
>
> Therefore
> \[
> \boxed{\Sigma(B)\le3\implies\text{every minimum-cost assignment is good}.}
> \]

The proof uses only minimum-matching optimality; it does not require family minimality, uniform balance, or exchange lemmas.

This is one of the strongest finished parts of the project.

---

# 6. Consequence: Lemma E is the correct n=3 existence target

Because of Lemma A:

\[
\boxed{
\text{Lemma E}
\Longrightarrow
\text{good minimum-cost assignment}
\Longrightarrow
\text{Conjecture 2 at }n=3.
}
\]

Conversely, failure of Lemma E means that every partition has

\[
\Sigma\ge4.
\]

So the entire existence problem is now concentrated in finding a low-total-spread partition.

---

# 7. Complete classification of the Sigma=4 matching obstruction

At `Σ=4`, the matching analysis is extremely restrictive.

The project proves that the only possible bad normalized pattern is, after relabelling,

\[
\boxed{
v_i=(2,2,0),\qquad
v_j=(0,0,0),\qquad
v_k=(2,2,0).
}
\]

Interpretation:

- agents `i` and `k` both see two bundles as heavy and one as light;
- agent `j` is indifferent;
- every minimum-cost assignment leaves one of the two problematic agents on a heavy bundle.

The project explicitly states that removing this pattern requires a **repartitioning of the heavy bundles**, not another matching argument.

This observation became important because many later attacks incorrectly tried to extract the missing theorem from the matching layer.

---

# 8. What we conclusively ruled out

Several proof mechanisms were attacked and should now be considered closed unless new information appears.

## 8.1 Fixed-third-bundle split

Keeping `C` fixed and splitting `A∪B` is insufficient.

Even additive costs can have

\[
c_1=c_2=|\cdot|,
\qquad
A,B\text{ of size }2,
\qquad
C=\varnothing,
\]

giving `(2,2,0)`.

A purely two-way rebalance of `A∪B` cannot by itself repair the gap to `C`.

## 8.2 Single pivotal item

There need not be one item whose marginal signature simultaneously improves both problematic agents.

So a common-pivot proof does not work in general.

## 8.3 Minimal threshold witness transfer

A minimal threshold witness controls the **receiving** context but need not control the **donor** context.

A set `W` can satisfy

\[
c(C\cup W)-c(C)=1
\]

while

\[
c(A)-c(A\setminus W)=2.
\]

So “find a minimal witness and move it” is false as a general proof mechanism.

## 8.4 Type-II / Type-II exclusion

The proposed claim that two problematic agents cannot both have the “donor-catastrophic witness” structure is false.

Explicit dichotomous examples realize it.

## 8.5 Nested threshold / critical-edge route

The nested witness and critical-edge constructions do not control the third agent.

Two agents can have perfectly synchronized critical edges while the third cost has an independent threshold boundary on the refined partition.

Hence critical-edge compatibility is insufficient.

## 8.6 Matching transpositions and 3-cycles

The full six-permutation matching layer can be completely optimal while a much better **repartition of the items** exists.

Therefore permutation/cycle optimality cannot prove Lemma E.

This is a fundamental level distinction:

\[
\text{assignment of existing bundles}
\neq
\text{repartitioning of items into new bundles}.
\]

## 8.7 “Good matching implies small spread”

False.

A minimum-cost assignment can be good even when the individual bundle spreads are arbitrarily large.

The project’s Lemma A is only the one-way implication

\[
\Sigma\le3\Rightarrow\text{good},
\]

not the converse.

---

# 9. Individual balancing is completely solved

For any single dichotomous cost, the project proves:

\[
\boxed{
\exists\text{ partition with }\operatorname{sp}\le1.
}
\]

The proof greedily places each item into a currently minimum-cost bundle and maintains the invariant that bundle costs differ by at most one.

This is a robust theorem and re-proves the corresponding individual-balance result.

The remaining problem is therefore **simultaneous** balancing.

---

# 10. Two-set set-balancing theorem

For ordinary underlying sets `D_1,D_2`, the project proves a strong theorem:

> **Theorem S.** For any two sets and any number of bundles, one can colour the items so that both sets have count-spread at most `1`.

The proof uses the three Venn regions

\[
D_1\setminus D_2,
\quad
D_1\cap D_2,
\quad
D_2\setminus D_1
\]

and a disjoint-or-covering support choice.

This is a genuine and reusable theorem.

It immediately implies the corresponding two-agent balancing result for **composed costs**.

It does **not** currently prove the analogous theorem for arbitrary dichotomous cost functions.

---

# 11. Composed costs and the compression theorem

A composed cost has the form

\[
c_i(S)=f_i(|S\cap D_i|)
\]

where `f_i` is monotone with increments in `{0,1}`.

Such `f_i` is 1-Lipschitz, so

\[
\boxed{
\operatorname{sp}_{c_i}(B)
\le
\operatorname{sp}_{|\,\cdot\cap D_i|}(B).
}
\]

This is the **compression theorem**.

Therefore ordinary set-count discrepancy certificates immediately transfer to composed costs.

This is the key bridge that makes the set/Venn attack relevant to the residual composed family.

---

# 12. Target T — now proved

The important set theorem is:

> **Target T.**
>
> For arbitrary
> \[
> D_1,D_2,D_3\subseteq M,
> \]
> there exists a 3-colouring such that, after relabelling,
> \[
> \boxed{
> \operatorname{sp}(D_1)\le1,\quad
> \operatorname{sp}(D_2)\le1,\quad
> \operatorname{sp}(D_3)\le2.
> }
> \]

This is now **closed by an exact finite residue certificate**.

---

# 13. Proof of Target T: exact residue reduction

Split the seven Venn regions

\[
R_1,R_2,R_3,R_{12},R_{13},R_{23},R_{123}
\]

according to

\[
|R|=3q_R+r_R,
\qquad
r_R\in\{0,1,2\}.
\]

The `3q_R` elements can be coloured in complete rainbow triples. Those triples add equal amounts to every colour count for every set containing the region, hence change no spread.

Therefore every instance is exactly equivalent, for discrepancy purposes, to one of

\[
3^7=2187
\]

residue patterns.

For a residue:

- `0`: only `(0,0,0)`;
- `1`: one of `(1,0,0),(0,1,0),(0,0,1)`;
- `2`: one of `(1,1,0),(1,0,1),(0,1,1)`.

There are therefore

\[
7^7=823543
\]

legal residual colourings across the whole residue universe.

The corrected exhaustive verifier checks all of them.

Result:

\[
\boxed{\text{0 counterexamples to Target T}.}
\]

The complete witness-profile histogram is:

| sorted profile | residue patterns |
|---|---:|
| `(0,0,0)` | 21 |
| `(0,0,1)` | 128 |
| `(0,0,2)` | 92 |
| `(0,1,1)` | 226 |
| `(0,1,2)` | 514 |
| `(1,1,1)` | 268 |
| `(1,1,2)` | 938 |
| **total** | **2187** |

Because the residue reduction covers arbitrary Venn-region sizes exactly, this is a finite proof for arbitrary finite ground sets.

### Verifier

[Download the corrected Target-T verifier](sandbox:/mnt/data/verify_target_T_corrected.py)

---

# 14. Consequence for residual composed costs

For residual composed instances, the project identifies a set `D_r` whose cardinality is divisible by `3`.

Target T gives that set count-spread at most `1`.

For a set of size divisible by `3`, spread `1` is arithmetically impossible; the spread is therefore `0`.

So after compression, the composed cost-spread profile is bounded by

\[
(0,1,2)
\]

up to permutation, and hence

\[
\boxed{\Sigma\le3}.
\]

Lemma A then supplies a good minimum-cost assignment.

Therefore:

\[
\boxed{
\text{The residual composed }n=3\text{ branch is closed.}
}
\]

Together with the project's already-solved S1–S4 cases, this closes the **composed-cost `n=3` programme**.

The source explicitly records the residual reduction to this two-agent-with-one-equal-split problem and the role of Target T. 

---

# 15. Simultaneous spread-1 balancing is false

We also investigated the stronger statement

\[
\exists B:
\operatorname{sp}_1,\operatorname{sp}_2,\operatorname{sp}_3\le1.
\]

This is false.

A four-item counterexample was constructed by explicit dichotomous cost tables.

Every 3-partition has at least one agent with spread `2`.

Yet the same instance has partitions with

\[
\Sigma=2.
\]

Thus:

\[
\boxed{
\text{uniform spread-1 balancing is strictly stronger than Lemma E and false.}
}
\]

This is an important negative result: the general theorem must allow a sacrificial spread-2 agent.

---

# 16. Why the K4 set obstruction does not hurt Lemma E

The standard three-set `K_4` example has no uniform spread-1 colouring, because its rainbow constraints amount to a proper 3-colouring of `K_4`.

Nevertheless a colouring exists with profile

\[
(0,2,0)
\]

and total spread

\[
2.
\]

So failure of uniform balance is not evidence against Lemma E.

This example is actually a model for the correct phenomenon:

> **one agent may absorb the discrepancy while the other two become exactly balanced.**

The residual arbitrary-dichotomous theorem must permit this type of compensation.

---

# 17. The important correction about “spread-zero must occur”

An earlier line of reasoning incorrectly concluded that every `Σ≤3` solution outside uniform balance must have a spread-zero agent.

That is false.

A partition can have

\[
(1,1,1)
\]

with total spread `3`.

So the actual Lemma E target is simply

\[
\boxed{
\Sigma\le3,
}
\]

not necessarily a profile containing zero.

This correction is important for future proof work.

---

# 18. Small-universe evidence against the remaining arbitrary-cost obstruction

The project and subsequent attacks tested the unique `Σ=4` and two-path obstruction structures for small ground sets.

The six-item obstruction searches did not produce a general dichotomous counterexample.

However, **these computational eliminations do not constitute a general theorem**.

The current evidence supports Lemma E rather than refuting it, but it does not close the arbitrary-cost case.

---

# 19. The actual remaining theorem

The next target is now completely clear:

> ### General Lemma E′
>
> Every `n=3` instance outside S1–S4 admits a partition
> \[
> B_1\sqcup B_2\sqcup B_3=M
> \]
> with
> \[
> \boxed{
> \sum_i\operatorname{sp}_i(B)\le3.
> }
> \]

This is the precise statement needed for Conjecture 2 at `n=3`.

The source explicitly warns that the additive shadow `(Q)` is not sufficient for this final step, because the actual residual instances contain non-additive costs; the primary target is the arbitrary-dichotomous residual statement. fileciteturn123file1L144-L165

---

# 20. The conceptual gap we have finally isolated

The solved composed branch has a **membership-set representation**:

\[
c_i(S)=f_i(|S\cap D_i|).
\]

That creates a finite Venn-region description.

The arbitrary-dichotomous cost can instead distinguish subsets having the same underlying membership counts.

Therefore the remaining obstacle is:

\[
\boxed{
\text{replace Venn-region structure by a general structural representation of
arbitrary dichotomous costs.}
}
\]

The previous witness/threshold/critical-edge paths were attempts to do exactly that, but all were shown insufficient.

---

# 21. Final status table

| Result | Status |
|---|---|
| Individual spread-1 balance | **PROVED** |
| `n=3` normalized matching formulation | **PROVED** |
| Goodness criterion | **PROVED** |
| Lemma A: `Σ≤3 ⇒ good` | **PROVED** |
| Unique `Σ=4` matching obstruction | **PROVED** |
| Two-set Venn balance | **PROVED** |
| Compression for composed costs | **PROVED** |
| Target T `(1,1,2)` for three sets | **PROVED by finite certificate** |
| Residual composed `n=3` branch | **CLOSED** |
| Simultaneous spread-1 for arbitrary dichotomous costs | **REFUTED** |
| General arbitrary-dichotomous Lemma E′ | **OPEN** |
| Conjecture 2 for arbitrary dichotomous `n=3` | **OPEN** |
| Conjecture 2 for arbitrary `n` | **OPEN** |

---

# 22. Bottom line before the next phase

We have now genuinely **finished the set/Venn route**.

The entire chain

\[
\boxed{
\text{seven-region discrepancy}
\rightarrow
\text{Target T}
\rightarrow
\text{residual composed }\Sigma\le3
\rightarrow
\text{Lemma A}
}
\]

is complete.

What remains is not another refinement of Target T.

It is a different problem:

\[
\boxed{
\textbf{How do we extract a finite structural representation from an arbitrary
dichotomous cost function, strong enough to replace the Venn-region argument?}
}
\]

That is the correct place to begin the **general-dichotomous attack**.
