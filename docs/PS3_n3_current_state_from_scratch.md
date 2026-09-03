# PS3 for Three Agents — Research State and Proof Roadmap

## 0. Purpose of this file

This document records the current mathematical understanding of **PS3 for three agents** from scratch.

It is intended to be given to a fresh Claude/LLM session with little or no prior context. The goal is not to pretend that the conjecture has been proved. Instead, this file carefully separates:

- the exact conjecture;
- facts that are proved;
- facts that are only computationally verified;
- approaches that have been disproved by explicit counterexamples;
- the strongest route currently being investigated;
- the precise remaining lemma that should be attacked next.

The central problem is a fair-division problem for arbitrary, non-additive, non-monotone valuations with integer marginals in `{-1,0,1}`.

---

# 1. The PS3 problem

There are **three agents**

\[
N=\{1,2,3\}
\]

and a finite set of indivisible items \(M\).

Each agent \(i\) has a valuation

\[
v_i:2^M\to\mathbb Z
\]

with

\[
v_i(\emptyset)=0.
\]

The only structural assumption is the **general binary marginal condition**

\[
v_i(S\cup\{g\})-v_i(S)\in\{-1,0,1\}
\]

for every \(i\), every \(S\subseteq M\), and every \(g\notin S\).

This is deliberately much more general than additive valuations.

An item can:

- be good for one agent and bad for another;
- be good for an agent in one bundle context and bad for the same agent in another context.

For example, a single valuation can have

\[
v(g\mid\emptyset)=+1
\]

but

\[
v(g\mid\{a,b\})=-1.
\]

Thus "good item" and "chore item" are not intrinsic properties of an item or even of an agent-item pair. They are properties of the triple

\[
(i,g,S).
\]

---

# 2. Target statement PS3(3)

We seek a **complete allocation**

\[
A=(A_1,A_2,A_3)
\]

where the \(A_i\)'s partition \(M\), together with subsidies

\[
p\in\{0,1\}^3
\]

such that

\[
v_i(A_i)+p_i
\ge
v_i(A_j)+p_j
\qquad
\forall i,j.
\]

In words:

> Every agent can be made envy-free using a subsidy of at most one unit per agent.

The central conjecture is therefore:

\[
\boxed{\text{PS3(3): every general-binary instance with three agents has such an allocation.}}
\]

This is the mixed-sign extension of the known pure goods / pure chores results.

---

# 3. Why this is genuinely harder than pure goods or pure chores

There are two important special cases.

### Dichotomous goods

All marginals lie in

\[
\{0,1\}.
\]

Known results establish very strong envy-free guarantees in this class.

### Negative dichotomous chores

All marginals lie in

\[
\{0,-1\}.
\]

The corresponding subsidy-1-per-agent theorem is also established in the project.

### General binary / mixed signs

Here

\[
\Delta v\in\{-1,0,1\}.
\]

The difficulty is that an item can behave differently depending on the current bundle.

If an item \(g\) is inserted into bundle \(A_x\), then for another agent \(i\), the envy edge into \(A_x\) changes by

\[
v_i(g\mid A_x)\in\{-1,0,1\},
\]

while the outgoing edges from \(x\) change according to

\[
-v_x(g\mid A_x).
\]

Consequently a path can change by as much as **2** in the mixed-sign case.

That is the precise place where the pure goods/chores insertion arguments stop working.

---

# 4. Envy graph formulation

For an allocation \(A\), define

\[
w(i,j)=v_i(A_j)-v_i(A_i).
\]

This is the envy graph: edge \(i\to j\) has weight \(w(i,j)\).

An allocation is envy-freeable iff its envy graph has no positive directed cycle.

The minimum subsidy vector is given by the longest-path potentials.

For three agents, if the required subsidy is greater than 1, then the obstruction can be reduced to two basic forms.

## Type I: direct envy 2

There is an edge

\[
w(i,j)\ge2.
\]

## Type II: two consecutive envy-1 edges

There is a directed path

\[
i\to j\to k
\]

with

\[
w(i,j)=1,\qquad w(j,k)=1,
\]

while the closing edge must be sufficiently negative to avoid a positive cycle.

In particular, after relabelling, the canonical Type-II pattern can be written

\[
w_{12}=1,\qquad
w_{23}=1,\qquad
w_{31}=-2.
\]

The spread bound discussed below implies that these are the only relevant magnitudes.

---

# 5. A useful structural strengthening: spread 2

Define the value-spread of an allocation for agent \(i\) by

\[
\operatorname{spr}_i(A)
=
\max_j v_i(A_j)-\min_j v_i(A_j).
\]

The project formulated the following stronger statement.

## Spread-2 conjecture (S2)

Every general-binary instance with three agents admits a complete allocation \(A\) such that

\[
\operatorname{spr}_i(A)\le2
\qquad\forall i
\]

and whose minimum subsidy vector is in

\[
\{0,1\}^3.
\]

So the conjecture asks simultaneously for:

1. bundle-value spread at most 2 for every agent;
2. subsidy at most 1 per agent.

The spread-2 statement is useful because if

\[
\operatorname{spr}_i(A)\le2,
\]

then every envy edge satisfies

\[
w(i,j)\le2.
\]

Hence subsidy 2 cannot come from an edge larger than 2.

---

# 6. Status of spread 2

This has been **extensively computationally verified**, but is NOT proved.

For \(n=3,m=3\), the full general-binary valuation space was exhaustively checked:

\[
20,337,240
\]

instances.

No instance failed to have a spread-\(\le2\) valid allocation.

Larger sampled experiments also found no failure:

| \(n,m\) | Coverage | General spread 2 failures |
|---|---:|---:|
| 3,3 | exhaustive, 20,337,240 | 0 |
| 3,4 | 15,000 | 0 |
| 4,4 | 6,000 | 0 |
| 3,5 | 4,000 | 0 |
| 5,5 | 1,200 | 0 |
| 3,6 | 1,500 | 0 |
| 6,6 | 400 | 0 |

The constant 2 appears to be tight.

This is evidence only; it is not a proof of S2.

---

# 7. Why spread 1 / balanced allocations are insufficient

A balanced allocation means

\[
\max_i |A_i|-\min_i|A_i|\le1.
\]

For mixed valuations, balance alone cannot guarantee subsidy 1.

Take three items \(a,b,c\).

For agent 1,

\[
v_1(S)=-|S|.
\]

For agents 2 and 3,

\[
v_i(S)
=
-|S\cap\{a,b\}|
+
[c\in S].
\]

Thus \(a,b\) are chores for everyone, while \(c\) is a chore for agent 1 and a good for agents 2 and 3.

Every marginal is in \(\{-1,0,1\}\).

If the allocation is balanced with three items and three agents, every agent receives exactly one item.

The agent among 2 and 3 who does not receive \(c\) values her own bundle at \(-1\), while she values the bundle containing \(c\) at \(+1\).

Therefore she has envy

\[
1-(-1)=2.
\]

So every balanced allocation requires subsidy 2 for some agent.

Nevertheless the unbalanced allocation

\[
A=(\{a\},\{b,c\},\emptyset)
\]

has a valid subsidy vector

\[
(1,0,0).
\]

Thus spread 2 is genuinely necessary in general.

---

# 8. A proved lemma: welfare maximization inside a permutation-closed family

Let \(\mathcal F\) be any family of allocations closed under permuting the bundles among the agents.

If \(A\in\mathcal F\) maximizes

\[
W(A)=\sum_i v_i(A_i),
\]

then \(A\) is envy-freeable.

### Proof

Every permutation \(A_\sigma\) of the bundles remains in \(\mathcal F\).

Therefore

\[
W(A)\ge W(A_\sigma)
\]

for every permutation \(\sigma\).

This is exactly the permutation characterization of envy-freeability.

Hence \(A\) is envy-freeable.

### Application

The family of allocations with bundle-size spread at most \(K\) is closed under bundle permutation.

Therefore:

> A welfare maximizer among spread-\(\le2\) allocations is automatically envy-freeable.

This removes the issue of whether such an allocation has a positive envy cycle.

The remaining problem is only whether its minimum subsidy is at most 1.

---

# 9. Why welfare maximization over ALL allocations fails

It is tempting to choose a globally welfare-maximizing allocation.

This is false.

Consider three items and:

\[
v_1(S)=0
\]

for every \(S\), while agents 2 and 3 have

\[
v(S)=\max(0,|S|-1).
\]

All marginals are in \(\{0,1\}\).

The welfare maximum concentrates all three items on one of agents 2 or 3.

Suppose agent 2 gets all three.

Then

\[
v_3(\{a,b,c\})-v_3(\emptyset)=2.
\]

So agent 3 requires subsidy 2.

Yet

\[
(\{a\},\{b\},\{c\})
\]

gives every agent value 0 and needs no subsidy.

Thus ordinary welfare maximization is not the right canonical rule.

---

# 10. Why welfare maximization INSIDE spread 2 is more promising

The previous failure disappears if we restrict to spread \(\le2\).

Computational experiments found that welfare maximization within the spread-2 family never failed to find a useful allocation in the tested cases, although ties matter.

This is the current canonical route:

1. restrict to \(\mathcal F_2\);
2. choose a welfare maximizer;
3. exploit the structure forced by welfare maximality;
4. prove its longest envy path is at most 1.

The last step is not yet proved.

---

# 11. The path-increment lemma

Suppose \(Z\) is obtained from \(Y\) by adding item \(g\) to bundle \(Y_x\).

Then:

- arcs \((i,j)\) with \(i,j\ne x\) do not change;
- arc \((i,x)\) changes by
  \[
  +v_i(g\mid Y_x);
  \]
- arc \((x,j)\) changes by
  \[
  -v_x(g\mid Y_x).
  \]

Thus, for any directed path:

- in pure goods, its weight changes by at most 1;
- in pure chores, its weight changes by at most 1;
- in general binary, it can change by as much as 2.

The value 2 occurs precisely when another agent sees \(g\) as \(+1\) while the recipient sees \(g\) as \(-1\).

This is the exact obstruction to directly importing the pure-goods/pure-chores insertion proofs.

---

# 12. Failed route: local welfare improvement

One might try to prove PS3 by taking an allocation that requires subsidy 2 and transferring one item to improve welfare/subsidy.

This is false.

There are explicit general-binary \(n=3,m=3\) allocations that are locally welfare-maximal under every single-item transfer but still require subsidy 2.

Therefore no proof based solely on

> "a bad allocation always admits a beneficial one-item transfer"

can work.

---

# 13. Failed route: local transfer + swap

A stronger local strategy allows:

- moving one item between bundles;
- swapping one item from one bundle with one item from another.

This also fails.

The basic reason is already visible in the pure-chores valuation

\[
v_i(S)=-|S|.
\]

Take

\[
A=(\{a,b,c\},\emptyset,\emptyset).
\]

This allocation requires subsidy 2.

No single-item transfer or one-item swap necessarily captures the global improvement needed to reach a balanced allocation.

The good allocation is obtained by a global redistribution of several items.

Therefore the eventual proof must permit **global redistribution**, not just bounded-size local moves.

---

# 14. Failed route: balanced bundle sizes

As shown above, balanced allocations can fail even though PS3 is true.

Thus we cannot insist on

\[
\max_i|A_i|-\min_i|A_i|\le1.
\]

The correct computational target appears to be spread 2.

---

# 15. Failed route: simultaneous value-spread ≤ 1

Another overly strong target is to demand that for every agent,

\[
\max_jv_i(A_j)-\min_jv_i(A_j)\le1.
\]

This is not always achievable in the mixed-sign class.

Hence spread 2 is not merely a technical convenience; it appears to be the correct constant.

---

# 16. Failed route: total spread ≤ 3

It is also tempting to control

\[
\sum_i
\left(
\max_jv_i(A_j)-\min_jv_i(A_j)
\right).
\]

A theorem saying this total spread is at most 3 is false.

An explicit three-item instance has every allocation with total spread at least 4, yet an EF allocation exists.

Therefore the relevant structure is **per-agent spread**, not total spread.

---

# 17. Failed route: unique-demand / Tucker-style labeling

For a partition \(B=(B_1,B_2,B_3)\), define

\[
E_i(B)
=
\{j:
v_i(B_j)\ge
\max_kv_i(B_k)-1
\}.
\]

If there is a matching choosing distinct acceptable bundles for all agents, then the allocation is immediately subsidy-1 feasible.

So one might try a Hall/Tucker/Sperner argument.

For three agents, Hall failure has a rigid form, but the labeling is not stable under moving an item:

an item's addition can change two relevant bundle values, and because signs may differ, an envy difference can change by 2.

Thus a straightforward combinatorial labeling argument does not currently work.

---

# 18. Failed route: naive induction by inserting an item

Suppose a valid allocation exists for \(m-1\) items.

It does NOT follow that one can insert the new item into one of the three existing bundles and remain valid.

There are explicit witnesses where:

- a partial allocation is valid;
- the remaining item cannot simply be inserted into any bundle while preserving the subsidy bound.

Sometimes already allocated items must be taken back and redistributed.

Therefore ordinary one-item induction is insufficient.

---

# 19. Important computational fact: valid states are reachable, but bad states exist

A partial state is called valid if it is envy-freeable with subsidy vector in \(\{0,1\}^3\).

A state is dead if no completion by the remaining items can produce a valid complete allocation.

Computational experiments found dead states, including in pure chores.

But from the empty allocation, exhaustive reachability tests found a complete valid state in all tested cases.

For example, for \(n=3,m=3\) and \(n=3,m=4\), the corrected state graph always had a reachable complete valid state.

Thus:

> Bad partial states exist, but they appear avoidable.

This suggests that the proof needs a **steering rule**, rather than a claim that every valid partial state can be safely extended.

---

# 20. Search-verified safety criterion

Extensive experiments found:

> If a valid partial allocation is balanced, OR if some unallocated item has a \(+1\) marginal for some agent at some current bundle, then the state is safe.

This had zero counterexamples in more than 1.5 million tested valid states.

This is computational evidence only.

It suggests that dangerous states have two simultaneous properties:

1. they are unbalanced;
2. there is no available \(+1\) insertion.

The second condition is particularly important because when no \(+1\) marginal is available, the local structure begins to resemble the pure-chores case.

---

# 21. Bounded excursions from balance

Another computational observation:

Starting from balanced valid states, if balance cannot be maintained in the mixed-sign class, then the necessary excursions appeared very small.

For tested instances:

- spread never exceeded 2;
- balance was regained within 2 insertions, or the allocation completed successfully while unbalanced;
- no excursion hit a dead end.

This motivated the stronger **bounded-excursion conjecture**:

> There exists an algorithm that starts from the empty allocation, keeps every intermediate state valid, never lets bundle-size spread exceed 2, and restores balance within two insertions whenever it leaves balance.

This would imply PS3.

However, this remains unproved.

---

# 22. Signed-binary decomposition

There is a useful exact decomposition of every general-binary valuation.

Given

\[
\Delta v_i\in\{-1,0,1\},
\]

define

\[
h(S)=\frac{|S|-v(S)}2,
\]

\[
c(S)=\lfloor h(S)\rfloor,
\]

and

\[
u(S)=v(S)+c(S).
\]

Then:

\[
v=u-c.
\]

Moreover, both \(u\) and \(c\) have nonnegative binary marginals:

\[
\Delta u,\Delta c\in\{0,1\}.
\]

So every signed-binary valuation decomposes into:

- a dichotomous-goods valuation \(u\);
- a dichotomous-cost valuation \(c\).

This is an exact algebraic decomposition.

---

# 23. Why the decomposition does NOT solve PS3

Suppose one could find an allocation satisfying:

\[
u_i(A_i)+q_i\ge u_i(A_j)+q_j
\]

with

\[
q_i\in\{0,1\},
\]

and simultaneously

\[
c_i(A_i)-r_i
\le
c_i(A_j)-r_j
\]

with

\[
r_i\in\{0,1\}.
\]

Then adding the inequalities gives

\[
v_i(A_i)-v_i(A_j)
\ge
(q_j+r_j)-(q_i+r_i).
\]

So

\[
p_i=q_i+r_i
\]

would be a valid subsidy vector.

But the problem is that \(q_i+r_i\) can equal 2.

Worse, the two component valuations may not be envy-freeable on the same allocation at all.

Thus the decomposition is exact but the certificate bridge is lossy.

This route has been computationally refuted as a general proof strategy.

---

# 24. The current Type-II structure

Now consider the most important bad case inside spread 2.

Suppose

\[
w_{12}=1,\qquad
w_{23}=1,\qquad
w_{31}=-2.
\]

Equivalently,

\[
v_1(A_2)=v_1(A_1)+1,
\]

\[
v_2(A_3)=v_2(A_2)+1,
\]

\[
v_3(A_1)=v_3(A_3)-2.
\]

The last equality is especially rigid.

Agent 3's three bundle values lie in an interval of length exactly 2, and \(A_1\) and \(A_3\) occupy the two extremes.

This is the configuration we want to destroy.

---

# 25. Welfare maximality gives additional inequalities

Suppose \(A\) is welfare-maximal among spread-\(\le2\) allocations.

Since swapping any two bundles remains inside the spread-2 family,

\[
w_{12}+w_{21}\le0,
\]

\[
w_{23}+w_{32}\le0,
\]

\[
w_{13}+w_{31}\le0.
\]

Under the Type-II assumption,

\[
w_{12}=1,\qquad w_{23}=1,\qquad w_{31}=-2,
\]

we get

\[
w_{21}\le-1,
\]

\[
w_{32}\le-1,
\]

and

\[
w_{13}\le2.
\]

There is also a particularly useful fact.

Consider the cyclic bundle permutation

\[
A'=(A_2,A_3,A_1).
\]

Its welfare difference is

\[
w_{12}+w_{23}+w_{31}
=
1+1-2=0.
\]

Therefore

\[
W(A')=W(A).
\]

So the Type-II cycle makes the forward cyclic permutation another welfare maximizer.

This is an exact structural equality.

---

# 26. But bundle permutations alone do not solve the problem

The cyclic permutation may simply transform the Type-II obstruction into a direct envy edge of weight 2.

Thus:

> The proof cannot rely solely on permuting the existing bundles.

We need to use the actual item decomposition inside the bundles.

This is an important distinction:

- bundle-value matrix information is insufficient;
- item-level marginal structure must be exploited.

---

# 27. Why a global redistribution is necessary

The local-exchange counterexamples show that a bad allocation can be locally trapped.

Therefore the next proof target is not:

> "Find a one-item improvement."

It is:

> "Given an extreme agent in a spread-2 allocation, use the item-level marginal structure to perform a possibly large redistribution that decreases the obstruction."

This is the **global redistribution route**.

---

# 28. Current candidate potential

For \(A\in\mathcal F_2\), define

\[
R_i(A)
=
\max_jv_i(A_j)-v_i(A_i).
\]

Because of spread 2,

\[
R_i(A)\in\{0,1,2\}.
\]

Define the number of extreme agents

\[
E(A)
=
|\{i:R_i(A)=2\}|.
\]

A valid PS3 allocation has

\[
E(A)=0.
\]

The proposed global potential is lexicographic, beginning with

\[
E(A).
\]

One could then use secondary criteria such as:

- number of Type-II paths;
- welfare;
- an appropriate bundle-dispersion quantity.

The desired lemma would say:

> If \(A\in\mathcal F_2\) has \(E(A)>0\), then there is another \(A'\in\mathcal F_2\) with strictly smaller potential.

Because the allocation space is finite, repeated improvement would terminate.

This is only a proposed framework, not yet a theorem.

---

# 29. The precise remaining lemma

The most promising concrete formulation is the following.

## Extreme-agent redistribution lemma — TARGET

Let \(A\) be a spread-\(\le2\) allocation of three agents.

Suppose agent 3 is extreme in the subsidy sense:

\[
v_3(A_1)-v_3(A_3)=2.
\]

Equivalently,

\[
v_3(A_3)-v_3(A_1)=2.
\]

Prove that there exists a **global redistribution**

\[
(A_1,A_2,A_3)
\longrightarrow
(B_1,B_2,B_3)
\]

of all items such that:

1. \(B\) still has value-spread at most 2 for every agent;
2. agent 3 is no longer subsidy-extreme:
   \[
   v_3(B_3)\ge\max_jv_3(B_j)-1;
   \]
3. no previously non-extreme agent becomes extreme;
4. or, more generally, some lexicographically defined global obstruction strictly decreases.

The redistribution may move arbitrarily many items.

This is the exact point where the current proof attempt stands.

---

# 30. Why the extreme-agent lemma might be possible

The relation

\[
v_3(A_3)-v_3(A_1)=2
\]

uses the entire allowed spread.

Since every item has marginal magnitude at most 1, moving items between \(A_1\) and \(A_3\) changes the relevant values in tightly controlled increments.

For example:

- adding one item to \(A_1\) changes \(v_3(A_1)\) by at most 1;
- removing one item from \(A_3\) changes \(v_3(A_3)\) by at most 1.

Therefore the extreme gap cannot be arbitrarily stable under suitable redistribution.

The difficulty is that the same redistribution simultaneously affects agents 1 and 2, whose marginal signs may be opposite.

Hence a successful argument probably needs a three-agent alternating redistribution rather than a one-pair exchange.

---

# 31. Important warning for the next session

Do NOT assume any of the following without proving it:

1. Every valid partial allocation can be completed.
2. Every bad allocation has a local improving move.
3. Every spread-2 allocation with subsidy 2 can be repaired by a single transfer.
4. Every spread-2 allocation with subsidy 2 can be repaired by a single swap.
5. Welfare maximization alone gives subsidy 1.
6. Balanced allocations always suffice.
7. The signed valuation can simply be solved by independently solving its positive and negative components.
8. An item's good/chore status is fixed independently of the current bundle.
9. The spread-2 conjecture itself is proved.

Several of these have already been explicitly refuted.

---

# 32. What IS proved versus computational evidence

## Proved

### P1. Envy graph characterization

An allocation is envy-freeable iff its envy graph has no positive directed cycle, and minimum subsidies are longest-path potentials.

### P2. Permutation-closed welfare lemma

A welfare maximizer over a family closed under bundle permutations is envy-freeable.

### P3. Signed decomposition

Every valuation with marginals in \(\{-1,0,1\}\) can be written exactly as

\[
v=u-c
\]

where both \(u\) and \(c\) have binary nonnegative marginals.

### P4. Balanced allocation is insufficient

There is an explicit three-item mixed-sign example requiring subsidy 2 for every balanced allocation.

### P5. Global welfare maximization is insufficient

There is an explicit pure-goods example where every welfare-maximal allocation requires subsidy 2 although subsidy 0 is achievable.

### P6. Local transfer/swap approaches are insufficient

Explicit counterexamples show that a subsidy-2 allocation can be locally trapped.

---

## Computationally verified, NOT proved

### C1. Spread-2 existence

No counterexample to S2 was found in the exhaustive \(n=3,m=3\) sweep or larger sampled cases.

### C2. Safety criterion

Balanced valid states and states with an available \(+1\) insertion were never dead in extensive experiments.

### C3. Bounded excursions

Observed excursions from balance never exceeded spread 2 and generally returned within two insertions.

### C4. Complete valid states are reachable

All tested corrected state graphs had a reachable complete valid state.

These are evidence for the conjecture, not mathematical proofs.

---

# 33. The overall proof architecture we currently want

The ideal chain would be:

\[
\boxed{\text{General binary}}
\]

\[
\Downarrow
\]

\[
\boxed{\text{Find spread-}\le2\text{ allocation}}
\]

\[
\Downarrow
\]

\[
\boxed{\text{Choose a suitable canonical spread-2 allocation}}
\]

\[
\Downarrow
\]

\[
\boxed{\text{Rule out subsidy-2 Type I/II obstruction}}
\]

\[
\Downarrow
\]

\[
\boxed{\text{Minimum subsidy}\le1}
\]

\[
\Downarrow
\]

\[
\boxed{\text{PS3(3)}}
\]

The spread-2 existence step is currently only computationally supported.

The canonical-choice step is unresolved.

The current most promising mechanism for the final step is global redistribution around an extreme agent.

---

# 34. The next task for a fresh Claude session

Do NOT restart all previously rejected approaches.

Start from the following precise question:

> **Given a three-agent spread-\(\le2\) allocation with subsidy 2, can the Type-I or Type-II obstruction always be eliminated by a global redistribution of the items while staying inside the spread-\(\le2\) family?**

First analyze the Type-II canonical configuration

\[
w_{12}=1,\qquad
w_{23}=1,\qquad
w_{31}=-2.
\]

Then exploit:

\[
w_{21}\le-1,
\qquad
w_{32}\le-1,
\]

from welfare maximality if using a welfare-maximal spread-2 allocation.

Also exploit the exact equality

\[
w_{12}+w_{23}+w_{31}=0,
\]

which means the cyclic bundle permutation has the same welfare.

But do not assume that a bundle permutation fixes the problem.

The real target is an item-level redistribution argument.

---

# 35. Final status

As of this document:

\[
\boxed{\text{PS3(3) is NOT proved.}}
\]

However, the problem has been reduced substantially.

The strongest current evidence says:

\[
\boxed{
\text{spread 2 is the correct structural bound}
}
\]

and the main remaining difficulty is:

\[
\boxed{
\text{turn spread-2 existence into subsidy-1 existence}
}
\]

without relying on local exchanges or naive induction.

The most promising immediate lemma is the **Extreme-Agent Redistribution Lemma** described in Section 29.

Any future proof should either:

1. prove that lemma (or a suitable stronger/weaker variant), or
2. produce a counterexample to it and use that counterexample to identify a better global invariant.

