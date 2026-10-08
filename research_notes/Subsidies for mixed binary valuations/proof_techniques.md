# Proof techniques behind unit- and linear-subsidy envy-freeness guarantees, and whether they extend to {−1,0,1} marginals with subjective signs

Conventions (mine, used in every section; status as of 2 Oct 2026). **T** is the target class: v_i : 2^M → ℤ, v_i(∅)=0, every marginal δ_i(g|S) := v_i(S∪{g}) − v_i(S) ∈ {−1,0,1}. Signs may differ across agents and, for one agent, across bundles (T need not be doubly monotone). "Unit subsidy" means p ∈ {0,1}^n, so Σp ≤ n−1. M(p) is the set of most-subsidized agents. Lemma and theorem numbers refer to the linked arXiv/PDF versions. Conference and journal versions may renumber. The requester's own results (arXiv 2609.14465) appear only as context labelled "(a)–(c)". They are not treated as prior work. Every bullet under "Inferences" is my own assessment, labelled [Assessment], unless it only restates a cited finding.

## 1. BKNS22 (Extend/FindSink): which lemmas rely on the inserted item's marginal being in {0,1}, what happens with an item that is +1 for some agents and −1 for others, and is there a published mixed variant?

### Takeaway
BKNS assumes monotonicity in only two places, and both concern the inserted item at the tentative recipient's own bundle: Prop. 6 (outgoing arcs) and the base case of Lemma 9. "Dichotomous" is otherwise used as "every marginal ≤ 1" and "subsidies are integers". In T, the Extend branch (Def. 3, Lemmas 7–8) therefore survives unchanged. FindSink (Lemmas 9–11) survives whenever the item has nonnegative own-bundle marginal for every most-subsidized agent. It breaks when some agent in M(p) has own-bundle marginal −1, and a subjective item can trigger this even if it is +1 for everyone else. I found no published Extend/FindSink variant for chores or mixed items.

### Cited Findings
- BKNS study monotone valuations with every marginal in {0,1} ("dichotomous"). Theorem 4 gives an envy-free (A,p) with p ∈ {0,1}^n, computable in polynomial time with value oracles. The result needs neither additivity, submodularity nor subadditivity. — [BKNS22](https://arxiv.org/abs/2201.07419)
- ALG (Algorithm 1) inserts one unallocated good per iteration and maintains an envy-free (A^t,p^t) with p^t ∈ {0,1}^n. If (A^t,p^t) is "extendable" with g, it permutes the bundles and gives g to κ (Lines 4–6). Otherwise it calls FINDSINK and gives g to the returned agent s (Lines 8–9). Subsidies are recomputed by HS longest paths (Line 11). — [BKNS22](https://arxiv.org/abs/2201.07419)
- The preliminaries restate HS as Theorem 1 (envy-freeable ⟺ welfare-maximal over bundle permutations ⟺ no positive-weight cycle) and Theorem 2 (p*_i = ℓ_A(i) is coordinatewise minimal). Lemma 3 says that if A_σ is envy-freeable then (A_σ, p_σ) is envy-free; it is proved "for general valuations" (footnote 4). — [BKNS22](https://arxiv.org/abs/2201.07419)
- **Proposition 5.** If Y is envy-freeable and v_x(Y_x∪{g}) − v_x(Y_x) = 1, then Y with g added to x is envy-freeable. The proof bounds SW(Ẑ) ≤ SW(Y)+1 for every permutation Ẑ (ineq. (11)) using only that every agent's marginal for g is at most 1. — [BKNS22](https://arxiv.org/abs/2201.07419)
- **Proposition 6.** After g is added to x:
  - Arcs not incident to x are unchanged.
  - Outgoing arcs (x,j) do not increase: "the last inequality follows from the fact that the valuation v_x is monotonic".
  - Incoming arcs (i,x) increase by at most 1: "we use the fact that v_i is dichotomous".
  - Hence every path weight rises by at most 1. — [BKNS22](https://arxiv.org/abs/2201.07419)
- **Definition 3 and Lemma 7.** (A,p) is extendable with g if two conditions hold: some permutation σ keeps (A_σ,p_σ) envy-free, and some κ ∈ M(p_σ) has v_κ(B_κ∪g) − v_κ(B_κ) = 1. Lemma 7 then keeps subsidies in {0,1}:
  - If q_κ = 0, by Prop. 6.
  - If q_κ = 1, by setting κ's subsidy to 0. This uses v_κ(B_κ∪g) = v_κ(B_κ)+1 and, for every other i, v_i(B_κ∪g) − 1 ≤ v_i(B_κ) ("follows from the fact that v_i is dichotomous"). — [BKNS22](https://arxiv.org/abs/2201.07419)
- **Algorithm 2 (EXTEND) and Lemma 8.** EXTEND tries every pair k ∈ [n], ℓ ∈ M(p) with v_k(A_ℓ∪g) − v_k(A_ℓ) = 1. It fixes ρ(k)=ℓ, completes ρ by a max-weight matching from [n]∖{k} to [n]∖{ℓ} with weights v_i(A_j), and accepts if Σv_i(A_ρ(i)) ≥ Σv_i(A_i). Lemma 8 (proof in App. B.1) shows this decides extendability exactly, using only Theorem 1 and Lemma 3. — [BKNS22](https://arxiv.org/abs/2201.07419)
- **Algorithm 3 (FINDSINK).** Start at an arbitrary s ∈ M(p) and tentatively give g to s. While some agent j would need a subsidy ≥ 2, move g to j. — [BKNS22](https://arxiv.org/abs/2201.07419)
- **Lemma 9 (App. B.2).** For non-extendable inputs, every visited s lies in M(p) and every tentative allocation is envy-freeable.
  - Base case: "the social welfare of X^0 is at least the social welfare of A; the agents' valuations are monotonic". A welfare-improving permutation would then yield an agent k with v_k(B_k∪g) − v_k(B_k) = 1 (by the upper bound 1 and integrality), contradicting non-extendability.
  - Induction step: uses Prop. 6. — [BKNS22](https://arxiv.org/abs/2201.07419)
- **Lemma 10.** FINDSINK visits each agent at most once.
  - Claim 1: each subpath P^τ from s_τ to s_{τ−1} has w_A(P^τ) ≥ 0, by Prop. 6 and p ∈ {0,1}^n.
  - The concatenated closed walk decomposes into cycles, which must all have weight 0 by Theorem 1.
  - Claim 2: by Prop. 6, the weight increase of Q^1 comes only from its last arc (k,s_0), so v_k(A_{s_0}∪g) − v_k(A_{s_0}) = 1.
  - Claim 3: rotating bundles along that zero-weight cycle keeps welfare, so the input was extendable, a contradiction. — [BKNS22](https://arxiv.org/abs/2201.07419)
- **Lemma 11.** At termination the required subsidies are < 2, and "Since the subsidies are nonnegative integers (for dichotomous valuations), they are either 0 or 1." — [BKNS22](https://arxiv.org/abs/2201.07419)
- **Limits stated by BKNS.** Their algorithm "resolves positive-weight cycles", unlike envy-cycle elimination, which resolves top-trading cycles. Appendix C gives a 3-agent, 5-good run whose output is not EF1. Section 5 lists adding EF1, and tight bounds for general monotone valuations, as future work. — [BKNS22](https://arxiv.org/abs/2201.07419)
- LMS26 state the general obstacle: "Existing arguments for goods exploit that every item is weakly beneficial, while analyses for chores rely on all items being weakly harmful; both assumptions fail when an item can be a good for one agent and a chore for another." — [LMS26](https://arxiv.org/abs/2607.10089)
- **Closest published relative of FINDSINK: Goko et al.'s SEC Step 2(b).** It moves a leftover item to the initial agent of any positive-weight path ending at the tentative recipient.
  - Its termination proof (Lemma 3.23) uses the same decomposition into zero-weight cycles.
  - It handles only leftovers with zero marginal for the recipient, under monotone binary valuations. Lemma 3.22 uses v_i(A_i∪{e}) = v_i(A_i) and v_j(A_i∪{e}) ∈ {v_j(A_i), v_j(A_i)+1}. — [Goko et al.](https://arxiv.org/abs/2105.01801)
- **Obstacle for non-doubly-monotone valuations.** An item can be "a chore for agent 1 given A_1 and ... a good for agent 1 given A_2 ... There is no obvious way to assign item x while maintaining the EF1 property. This situation does not arise with doubly-monotone valuations." — [Bhaskar, Kumar, Pandit, Rakshitha 2024](https://arxiv.org/abs/2411.19881)

### Inferences
- [Assessment] **Where signs are used.** In T, every marginal is ≤ 1 and all values are integers. So the following hold unchanged whenever the recipient has δ = +1 where required: Prop. 5, the incoming-arc half of Prop. 6, both cases of Lemma 7, Lemma 8, and Lemma 11.
  - Only two steps are sensitive to sign. The outgoing-arc half of Prop. 6 needs δ_x(g|Y_x) ≥ 0 for the recipient x. The base case of Lemma 9 needs δ_{s_0}(g|A_{s_0}) ≥ 0.
  - Every later use (Lemma 9's induction, Lemma 10 Claims 1–2) goes through Prop. 6 applied to a tentative recipient s_τ ∈ M(p).
  - Monotonicity with respect to items allocated earlier is never used. This matches the requester's (c).
- [Assessment] **Sufficient condition in T.** Take an envy-free (A,p) with p ∈ {0,1}^n and an item g. The BKNS step for g goes through in T if either of the following holds:
  - (A,p) is extendable with g. Lemma 7 does not depend on signs.
  - δ_s(g|A_s) ≥ 0 for every s ∈ M(p). Lemmas 9–11 then go through line by line, because every tentative recipient lies in M(p) by Lemma 9's induction. If δ_s = 0, Lemma 9's base case still yields SW(X^0_σ) ≥ SW(A)+1, which forces a +1 marginal and a contradiction.
  - EXTEND already evaluates δ_k(g|A_ℓ) at other agents' bundles. So it natively uses the non-doubly-monotone situation "a chore at my bundle, a good at yours" whenever a welfare-preserving permutation exists.
- [Assessment] **Item that is +1 for some agents and −1 for others.** Suppose g is −1 at A_s for some s ∈ M(p) and (A,p) is not extendable. FINDSINK may then start at, or move to, such an s. Three things break:
  - Every outgoing arc of s increases by 1, so a path through s can gain 2 instead of 1 (Prop. 6 fails).
  - Lemma 9's base case only yields "some agent k has δ_k(g|B_k) ≥ 0", which does not contradict Definition 3.
  - Lemma 10's Claims 1–2 lose the step "a single incoming arc accounts for the whole increase".
  
  This is the same failure as for a chore (the requester's (b)). A subjective item triggers it as soon as one most-subsidized agent dislikes the item at her own bundle, even if everyone else values it +1.
- [Assessment] **Scheduling.** In objective-sign doubly-monotone instances, after all objective chores are placed, every remaining item has δ ≥ 0 for every agent at every bundle. The sufficient condition then holds at every step, which is why "chores first, then goods" works ((c)). In T no fixed order can guarantee the condition, for three reasons:
  - M(p) changes over time.
  - Own-bundle signs change as bundles grow.
  - For non-doubly-monotone agents, an item's sign depends on the bundle.
  
  A dynamic rule ("insert any item that is extendable or weakly good for all of M(p)") gets stuck exactly when every remaining item is non-extendable and is a strict chore for some most-subsidized agent. Those items would need a separate chore-type phase (Q7), and interleaving the two phases is where new ideas are needed.
- [Assessment] **EF1.** Unit subsidies give pairwise envy ≤ 1. That implies EF1 for additive ternary valuations, but not for non-additive ones: BKNS App. C already fails EF1 for monotone dichotomous goods. EF1 in T would therefore need its own invariant on top of BKNS-type bookkeeping.

### Gaps
- I found no published variant of Extend/FindSink for chores or mixed items. Searches covered subsidy with chores, mixed manna and dichotomous valuations. The follow-ups found (LMS26, ALMS25, DlT–F25, DlT–S26, Goko) all use different techniques.
- I did not check whether the IJCAI 2022 proceedings renumber the lemmas; the numbering above is arXiv v1.
- I did not build or verify an explicit counterexample for the "+1 for some agents, −1 for a most-subsidized agent" case. The failure above is an obstruction in the proof, not a proven impossibility.

## 2. Lu, Mackenzie, Suzuki 2026 (arXiv 2607.10089): algorithm and proof structure, and where additivity is used essentially

### Takeaway
LMS26 prove unit subsidy for additive mixed manna (u_i(g) ∈ [−1,1], subjective signs) in polynomial time. The proof uses neither EF1 nor a potential function. It has three parts:
- A bundling step turns the instance into "meta-goods" of value ≤ 1 with pairwise-disjoint interest sets, plus residual objective chores.
- Iterated maximum-weight matchings (perfect matchings for chores) make each envy path's weight telescope across rounds.
- A three-way case split: no residual chores; fewer chores than meta-goods (incremental equality-graph plus payment-reduction construction); at least as many (pairing, thresholding and a flow argument).

Every component uses additivity essentially, and the authors say the approach does not extend beyond additive utilities. For the additive slice of T it already delivers p ∈ {0,1}^n. By my own argument it also delivers EF1 there.

### Cited Findings
- **Theorem 1.1.** For additive u_i : M → [−1,1], where items may be goods for some agents and chores for others, an envy-free outcome with 0 ≤ p_i ≤ 1 exists and is computable in polynomial time. The bound is tight already for goods. — [LMS26](https://arxiv.org/abs/2607.10089)
- The proof is "guided by the envy-freeability characterization of Halpern and Shah": it suffices to build an allocation in which every envy path has weight ≤ 1. — [LMS26](https://arxiv.org/abs/2607.10089)
- **EF1 plus envy-freeability is not enough.** "Even in goods-only instances, an allocation may be both EF1 and envy-freeable while its heaviest envy path has weight n − 1." — [LMS26](https://arxiv.org/abs/2607.10089)
- **Two design choices.**
  - Meta-goods (adopted from Aziz et al.) must have value ≤ 1: "Without it, even a two-agent instance containing a single meta-good may require a subsidy strictly greater than one."
  - EF1 is dropped: "requiring the allocation to remain EF1 is too restrictive and is incompatible with the operations used later in the proof". — [LMS26](https://arxiv.org/abs/2607.10089)
- **Definitions 2.3–2.7.**
  - Goods-style graph: maximum-weight matchings with ties broken toward maximum cardinality. Such a matching never uses a negative edge, so IMWM "never assigns an object to an agent who values it negatively".
  - Chores-style graph: maximum-weight perfect matchings (IMWPM), padded with value-0 dummies to a multiple of n.
  - Meta-good (Def. 2.6): some agent values it ≥ 0. Chore-maximality: Def. 2.7. — [LMS26](https://arxiv.org/abs/2607.10089)
- **Proposition 3.1** covers subjective goods only (u ≤ 1, every item valued ≥ 0 by someone). IMWM's output has every envy path ≤ 1.
  - The bound telescopes: w^t(P) ≤ F^t − F^{t+1}, where F^t := max({0} ∪ {u_k(g) : g ∈ J^t}) for the path's terminal agent k. Summing gives w_A(P) ≤ F^1 ≤ 1.
  - The authors present this as a much simpler proof of Brustle et al.'s result. — [LMS26](https://arxiv.org/abs/2607.10089)
- **Proposition 3.2** covers objective chores (u ≥ −1). IMWPM gives envy-path weight ≤ −u_k(μ^T_1) ≤ 1 (App. A.1). — [LMS26](https://arxiv.org/abs/2607.10089)
- **Algorithm 3 (Conditional Pairwise Merging).**
  - Phase 1 merges an objective chore into a (meta-)good whenever some agent still values the union ≥ 0.
  - Phase 2 runs while objective chores remain. It merges two meta-goods that a common agent values ≥ 0, absorbing a chore when the union would otherwise not be chore-maximal. — [LMS26](https://arxiv.org/abs/2607.10089)
- **Lemma 4.2.**
  - (P1) If residual chores remain, the interest sets T_j = {i : u_i(M_j) ≥ 0} are pairwise disjoint.
  - (P2) 0 ≤ u_i(M_j) ≤ 1 for i ∈ T_j.
  - (P3) u_i(M_j ∪ {c}) = u_i(M_j) + u_i(c) < 0 for every agent i and residual chore c. — [LMS26](https://arxiv.org/abs/2607.10089)
- **Case I (|Z_rem| = 0).** Run IMWM on the meta-goods, which is valid by Prop. 3.1. A meta-good's value is "well-defined by additivity". — [LMS26](https://arxiv.org/abs/2607.10089)
- **Case II (0 < |Z_rem| = k < |G| = ℓ).**
  - Relabel meta-goods by v_j = max_{i∈T_j} u_i(M_j); the maximizers are distinct by (P1).
  - Stage 1 allocates the top-k meta-goods and all k residual chores among the active agents. It runs IMWPM on the chores and shifts payments uniformly so that u_i(A_i)+p_i ≥ λ. It then adds the remaining agents one at a time using the equality graph and a payment-reduction procedure (Proposition 4.6).
  - Stage 2 (Theorem 4.7) gives M_j to agent j for j > k and lowers p_j by v_j. This creates no envy because u_i(M_j) ≤ v_j for every i. — [LMS26](https://arxiv.org/abs/2607.10089)
- **Case III (k ≥ ℓ).**
  - Pair every meta-good with a distinct residual chore through an injective map φ, and choose φ* to lexicographically maximize the IMWPM round values.
  - Use thresholded utilities û (Observation 4.11). Lemma 4.10 shows every assigned item has u ≥ −1.
  - Conclude by Prop. 3.2 (Lemma 4.12). Section 5 gives a flow-based polynomial implementation (Prop. 5.2). — [LMS26](https://arxiv.org/abs/2607.10089)
- **Authors' discussion of additivity.** "Our techniques rely heavily on additivity both to define meta-goods and to obtain telescoping envy-path bounds from iterated matchings. This approach does not directly extend to richer valuation classes." They pose a constant per-agent subsidy for submodular or XOS mixed valuations as open, and note this "is open even in the goods-only setting". — [LMS26](https://arxiv.org/abs/2607.10089)
- **ALMS25 (Aziz, Lu, Mackenzie, Suzuki).**
  - Theorem 4.2: "With indivisible goods and chores, an EF1 and envy-freeable allocation always exists" (additive utilities). It is proved by "Iterative Item Merging" (Algorithm 1; Lemma 4.5 gives chore-maximal meta-goods with disjoint interest sets) followed by IMWM/IMWPM.
  - A two-item example (identical agents, one item +1 and one −1) shows bundling is necessary.
  - Section 5: "Our iterative matching techniques can no longer extend beyond additive valuations". EF1 together with envy-freeability for doubly monotone instances is open, "still open in the setting with only indivisible goods". — [ALMS25](https://arxiv.org/abs/2511.04891)

### Inferences
- [Assessment] **Additivity is used essentially in at least five places.**
  1. A meta-good's value is the sum of its items' values, so it can be treated as one item.
  2. Phase 1 and (P3) use u_i(g ∪ c) = u_i(g) + u_i(c).
  3. The IMWM/IMWPM path bound needs u_i(A_j) = Σ_t u_i(μ^t_j), i.e. a per-round decomposition.
  4. Theorem 4.7's completion uses u_i(A_j ∪ M_j) = u_i(A_j) + u_i(M_j).
  5. Case III compares u and û item by item.
  
  None of these is available for non-additive T. A meta-good's value then depends on the rest of the recipient's bundle, interest sets and chore-maximality are not stable under union, and round-by-round telescoping has no meaning.
- [Assessment] **The additive slice of T is closed, including EF1.** For u_i(g) ∈ {−1,0,1}, the HS-minimal subsidies are integers and at most LMS26's ≤ 1 payments, so they lie in {0,1}. Then every envy is ≤ p_i − p_j ≤ 1. With additive ternary utilities, envy ≤ 1 implies EF1: if v_i(A_j) > v_i(A_i), either A_j contains an item i values +1 or A_i contains one i values −1, and removing that item removes the envy. This derivation is mine; LMS26 do not claim EF1.
- [Assessment] **What might transfer to non-additive T.**
  - The interest-graph separation of "who can like what".
  - The case split on the number of objective chores versus good-like objects.
  - Case II's incremental addition of agents via equality paths and payment reduction. This is a structural cousin of the requester's backward-closure payments along equality arcs.
  
  The matching-and-telescoping core does not transfer.

### Gaps
- I did not extract Case II's full invariant list (the "(I1)/(I2)" invariants), the exact definition of λ, or the payment-reduction rules of Prop. 4.6. The text only shows u_i(M_i) ≥ λ for the initial active agents and λ ≥ v_j for j > k. The description above comes from the overview and partial proof pages.
- Whether LMS26's allocation is EF1 for general [−1,1] additive values is not addressed; the authors deliberately drop EF1.

## 3. Brustle, Dippel, Narayan, Suzuki, Vetta (EC 2020): the matching-round algorithm for additive goods, the 2(n−1)-per-agent argument for monotone goods, and chore/mixed adaptations

### Takeaway
**Additive goods.** Round-by-round maximum-weight matchings (Algorithm 1) give an envy-freeable, EF1 allocation. The unit bound comes from a modified valuation v̄ under which every arc is ≥ −1; Lemma 4.1 then forces every path to weigh ≤ 1. That proof uses additivity (per-round decomposition, Claim 4.4) and nonnegativity (Claim 4.3, and the convention that every agent is matched every round).

**Monotone goods.** The 2(n−1)-per-agent argument (Lemma 5.2) needs no assumption on valuations once some allocation with all pairwise envies ≤ 1 is available. Monotonicity enters only through the envy-cycle EF1 algorithm (Lemma 5.1).

**Chores and mixed items.** Adaptations exist only for additive utilities: IMWPM for chores, LMS26, and ALMS25.

### Cited Findings
- **Main results.**
  - Theorem 1.3 (additive): an envy-freeable allocation with subsidy ≤ 1 per agent; the allocation is also EF1, balanced, and polynomial-time.
  - Theorem 1.4 (monotone): subsidy ≤ 2(n−1) per agent, polynomial time with a valuation oracle.
  - Valuations are monotone with v(∅)=0 and every marginal ≤ 1. — [Brustle et al.](https://arxiv.org/abs/1912.02797)
- **Algorithm 1 (Bounded-Subsidy).** In round t, compute a maximum-weight matching between agents and the remaining items. They assume every agent receives an item each round, "evident because agent i can be assigned a item for which it has zero value", and pad the last round with zero-value dummies. — [Brustle et al.](https://arxiv.org/abs/1912.02797)
- **Lemmas 3.1, 3.2 and Claim 3.3.**
  - Lemma 3.1 (envy-freeable): a cycle's weight decomposes as Σ_t Σ_{(i,k)∈C}[v_i(μ^t_k) − v_i(μ^t_i)]. Each round's sum is ≤ 0 by max-weight optimality.
  - Lemma 3.2 (EF1): v_i(μ^t_i) ≥ v_i(j) for every j ∈ J^{t+1}, so v_i(A_i) ≥ v_i(A_k∖{μ^1_k}).
  - Claim 3.3: EF1 plus envy-freeable gives total subsidy ≤ (n−1)². — [Brustle et al.](https://arxiv.org/abs/1912.02797)
- **Lemma 4.1.** If A is envy-freeable and every arc has weight ≥ −1, every agent's subsidy is ≤ 1. Closing the maximum-weight path with its back-arc gives a cycle of weight ≤ 0. — [Brustle et al.](https://arxiv.org/abs/1912.02797)
- **Section 4.1: the modified valuation and Claims 4.2–4.4.**
  - Definition: v̄_i(μ^t_k) = max(v_i(μ^t_k), v_i(μ^{t+1}_i)) for k ≠ i and t < T; all other values are unchanged.
  - Claim 4.2: A stays envy-freeable under v̄, via a blue/red-arc decomposition of a cycle.
  - Claim 4.3: every v̄-arc is ≥ Σ_{t<T}(v_i(μ^{t+1}_i) − v_i(μ^t_i)) = v_i(μ^T_i) − v_i(μ^1_i) ≥ −v_i(μ^1_i) ≥ −1.
  - Claim 4.4: "by additivity", v̄-arcs dominate v-arcs, so subsidies under v are at most those under v̄. — [Brustle et al.](https://arxiv.org/abs/1912.02797)
- **Lemmas 5.1–5.2.** Lemma 5.1 is Lipton et al.'s envy-cycle algorithm, giving EF1 for monotone valuations. Lemma 5.2: if A is EF1 and B is the max-weight reassignment of A's bundles, every path in G_B has weight ≤ 2(n−1). The proof splits the path weight into two terms, each at most n−1:
  - First term: v_i(B_{i+1}) − v_i(A_i) ≤ 1 for each step, by EF1.
  - Second term, Σ(v_i(A_i) − v_i(B_i)): bounded by an R/S split. Agents worse off in B lose at most what the ≤ n−1 better-off agents gain, and each gain is ≤ 1 by EF1. — [Brustle et al.](https://arxiv.org/abs/1912.02797)
- **Later adaptations.** LMS26's Prop. 3.1 re-proves the additive bound by F^t-telescoping. Prop. 3.2 is the IMWPM (perfect-matching) analogue for objective chores. — [LMS26](https://arxiv.org/abs/2607.10089)
- **ALMS25.** Proposition 2.8: IMWPM on chores gives an EF1 and envy-freeable allocation. Theorem 4.2 extends EF1 plus envy-freeability to additive mixed manna by bundling. The authors add: "Our iterative matching techniques can no longer extend beyond additive valuations." — [ALMS25](https://arxiv.org/abs/2511.04891)
- **Kawase et al. improvement.** They improve the per-agent bound from 2(n−1) to n−1, starting from any EF1 allocation (see Q4). — [Kawase et al.](https://arxiv.org/abs/2308.11230)

### Inferences
- [Assessment] **Where signs and additivity are used in the additive argument.** Nonnegativity is used in two places:
  - Letting every agent be matched every round. With chores, a maximum-weight matching leaves negative items unmatched, which is why LMS26 use IMWPM for objective chores and IMWM only for subjective goods.
  - The step v_i(μ^T_i) ≥ 0 in Claim 4.3.
  
  Additivity is used in the per-round decompositions of Lemmas 3.1–3.2 and in Claim 4.4.
- [Assessment] **Lemma 5.2 needs only two things:** the bundles are reassigned by a maximum-weight permutation, and every pairwise envy in A is ≤ 1. Under |δ| ≤ 1, two-sided EF1 (remove one item from either bundle) gives envy ≤ 1. So Lemma 5.2 holds verbatim in T whenever an EF1 (or merely envy-≤1) allocation exists. This gives 2(n−1) per agent for doubly monotone T and for n = 2, but Kawase's n−1 dominates it.
- [Assessment] **Unit subsidies for non-additive T.** The matching-round technique is unavailable because there is no per-round decomposition. Lemma 4.1 itself holds for any valuations. It could be reused if one could build, in T, an envy-freeable allocation whose arcs are all ≥ −1 under some dominating modified valuation. Brustle's construction of that valuation (Claims 4.2–4.4), however, is additive.

### Gaps
- I did not check whether the EC 2020 version renumbers the lemmas (arXiv v1 was used).
- I found no non-additive chore or mixed adaptation of the matching-round algorithm.

## 4. Kawase, Makino, Sumita, Tamura, Yokoo (AAAI 2024): converting an EF1 allocation into an envy-freeable one with bounded path weights, and where double monotonicity is used

### Takeaway
The conversion is a statement about weight matrices alone. For any allocation, permute the bundles by a maximum-weight permutation and pay HS-minimal subsidies. Then the r-th largest subsidy is ≤ Σ_{ℓ ≤ n−r} β_ℓ, where β_i is agent i's maximum envy in the original allocation (Lemma 3, via the ŵ re-weighting of Lemma 4 and a forest argument on path lengths).

Double monotonicity is used only to guarantee that an EF1 allocation exists, which makes every β ≤ 1. So in T the bounds n−1 per agent and n(n−1)/2 in total hold whenever an EF1 (or envy-≤1) allocation exists. That is known for doubly monotone instances and for n = 2, but open for non-doubly-monotone T with n ≥ 3. The bound is tight for arbitrary EF1 inputs, so this route cannot by itself give unit subsidies.

### Cited Findings
- **Model.**
  - Valuations v_i : 2^M → ℝ are arbitrary, with |v_i(X∪{e}) − v_i(X)| ≤ 1.
  - An item is a good for i if all its marginals are ≥ 0, and a chore if all are ≤ 0. An instance is doubly monotone if every item is a good or a chore for each agent.
  - EF1 allows removing one item from either bundle. — [Kawase et al.](https://arxiv.org/abs/2308.11230)
- **Lemma 3.** Take any weight matrix w, and let β_1 ≥ … ≥ β_n be the sorted values of max_j(w_{i,j} − w_{i,i}). Then the r-th largest entry of the minimum subsidy vector p* is ≤ Σ_{ℓ=1}^{n−r} β_ℓ. The authors remark that "the identical permutation id may not be a maximum weight permutation", so G_{w,id} may contain positive cycles. — [Kawase et al.](https://arxiv.org/abs/2308.11230)
- **Lemma 4 and the proof of Lemma 3.**
  - Set q_i := max_j(v_i(A_j) + p*_j), r_i := q_i − (v_i(A_i) + p*_i) ≥ 0, and ŵ_{i,i} := v_i(A_i) + r_i, leaving off-diagonal entries unchanged.
  - Then the identity is a maximum-weight permutation for ŵ, and the minimum subsidy vectors of w and ŵ coincide.
  - Envy arcs under ŵ are ≤ those under w, so path weights are bounded by sums of β's.
  - The longest paths form a forest, so |P_i| ≤ n − i after relabelling. — [Kawase et al.](https://arxiv.org/abs/2308.11230)
- **Theorem 1.** "If the valuations are doubly monotone or n = 2", there is an envy-free (A,p) with max p ≤ n−1 and Σp ≤ n(n−1)/2, computable in polynomial time.
  - The proof combines Lemma 3 with β_i ≤ 1 for EF1 and the existence and computability of EF1 "if the valuations are doubly monotone [8] or n = 2 [11]". Here [8] is Bhaskar–Sricharan–Vaish (APPROX 2021) and [11] is Bérczi et al.
  - From an EFk allocation one gets k(n−1) per agent and k·n(n−1)/2 in total, "even when the valuations are general".
  - For n = 2 the bound is best possible. — [Kawase et al.](https://arxiv.org/abs/2308.11230)
- **Example 1.** An additive monotone EF1, envy-freeable allocation has minimal subsidies (0,1,…,n−1). The bound is therefore tight for arbitrary EF1 inputs. — [Kawase et al.](https://arxiv.org/abs/2308.11230)
- **Theorem 2 (n ≥ 3, monotone).** Max subsidy ≤ n − 1.5 and total ≤ (n² − n − 1)/2.
  - Construction: among bundle permutations that keep EF1, pick a welfare-maximal one, then move one item e* ∈ A_1 to A_n (Lemmas 5–8).
  - The case analysis uses monotonicity (e.g. A'_i ⊇ A_i in Lemma 7) and goods-type EF1 (min_{e∈A_1} v_1(A_1∖{e}) in Lemma 6). — [Kawase et al.](https://arxiv.org/abs/2308.11230)
- **Bérczi et al.** Theorem 1: EF1 exists, and is polynomial-time computable, for two agents with arbitrary (non-monotone, non-additive) utilities. The earlier general EF1 algorithm of Aziz et al. has a flawed proof. Question 12 asks whether EF1 exists for non-monotone, non-additive identical utilities. — [Bérczi et al.](https://arxiv.org/abs/2006.04428)
- **Bhaskar, Kumar, Pandit, Rakshitha (2024).**
  - Known EF1 existence: two agents (arbitrary), doubly monotone, Boolean, and identical negative Boolean valuations.
  - "It remains open if an EF1 allocation exists for arbitrary valuations, even, e.g., for the case of 3 identical agents."
  - New results: EF1 for identical "trilean" valuations (bundle values in {0,a,b}), for non-identical {0,−1}-valued valuations, and for separable single-peaked valuations with three agents. — [BKPR24](https://arxiv.org/abs/2411.19881)

### Inferences
- [Assessment] **What the conversion needs.** Lemmas 3–4 assume nothing about signs, monotonicity or additivity. In T, any allocation with all pairwise envies ≤ 1 yields ≤ n−1 per agent; double monotonicity enters only through EF1 existence. Two consequences:
  - Doubly monotone T: n−1 per agent and n(n−1)/2 in total, in polynomial time.
  - T with n = 2: unit subsidy (total ≤ 1), using Bérczi's EF1.
  
  The final allocation is a permutation of the EF1 allocation, so in non-additive T it need not itself be EF1.
- [Assessment] **Non-doubly-monotone T with n ≥ 3.** This route is blocked by the open EF1-existence question. Separable single-peaked valuations with unit slopes ("too much of a good thing") lie in T and are exactly the non-doubly-monotone examples BKPR24 study. Even the weaker statement "an allocation with envy ≤ k, k independent of m, exists" is not established in the sources I read.
- [Assessment] **Not a route to unit subsidies.** Kawase-type conversion cannot by itself give unit subsidies (Example 1). A unit result must control the structure of paths, not just the weight of individual arcs.

### Gaps
- I did not read the journal version (Artificial Intelligence 348:104406, 2025, as cited by LMS26). It may contain additional results or a different numbering.

## 5. Halpern & Shah (SAGT 2019): the envy-graph characterization and Theorem 5 (maximum Nash welfare for binary additive goods); validity for arbitrary valuations and a mixed-manna analogue

### Takeaway
Theorem 1 (the characterization) and Theorem 2 (minimal subsidies are longest paths) use only sums of bundle values over permutations and nonnegativity of payments. They therefore hold verbatim for non-monotone, mixed-sign, non-additive valuations, and later papers use them that way.

Theorem 5's maximum Nash welfare (MNW) argument (every path ≤ 1 for binary additive goods) uses four ingredients:
- non-wastefulness;
- v_i(A_i) = |A_i|;
- integrality;
- a Pigou–Dalton transfer along a subpath with no negative arcs.

The identity v_i(A_i) = |A_i| and the item-passing step are specific to goods and to additivity. I found no welfarist (MNW/leximin-style) analogue for mixed manna. LMS26 supersedes Theorem 5 on the additive ternary slice, and the non-additive goods analogue is Goko et al. (matroidal valuations).

### Cited Findings
- **Model.** Additive valuations, v_i : 2^M → ℝ≥0, item values in [0,1]. — [HS19](https://www.cs.toronto.edu/~nisarg/papers/subsidy.pdf)
- **Theorem 1.** (a) A is envy-freeable ⟺ (b) A is welfare-maximal over bundle permutations ⟺ (c) G_A has no positive-weight cycle. The proof: (a)⇒(b) sums the EF constraints along σ; (b)⇒(c) rotates bundles along the cycle; (c)⇒(a) sets p_i = ℓ(i). Proposition 1 tests this in O(mn + n³). — [HS19](https://www.cs.toronto.edu/~nisarg/papers/subsidy.pdf)
- **Theorem 2.** p*_i = ℓ(i) is coordinatewise minimal; the proof uses only p ≥ 0. It is computable in O(nm + n³). — [HS19](https://www.cs.toronto.edu/~nisarg/papers/subsidy.pdf)
- **Bounds for a fixed or a chosen allocation.**
  - Lemma 1 and Theorem 3: for a given envy-freeable allocation, every path weighs ≤ m and the worst-case subsidy is (n−1)m. The proof uses w(i_t, i_{t+1}) ≤ |A_{i_{t+1}}|.
  - Theorem 4: a lower bound of n−1 for a chosen allocation, even with binary or identical valuations.
  - Lemma 2: envy-freeable plus EF1 gives path weight ≤ min(n−1, m). — [HS19](https://www.cs.toronto.edu/~nisarg/papers/subsidy.pdf)
- **Theorem 5.** "For binary valuations, an allocation produced by the maximum Nash welfare algorithm is envy-freeable and requires at most n − 1 subsidy." The proof:
  - MNW is non-wasteful, hence envy-freeable.
  - v_i(A_i) = |A_i| and v_i(A_j) ≤ |A_j| give w(i,j) ≤ |A_j| − |A_i|.
  - By integrality, a path of weight ≥ 2 contains a subpath P with no negative arcs and weight ≥ 2 (Claim, App. C).
  - Along P, (a) |A_{i_k}| ≥ |A_{i_1}| + 2, and (b) each i_t likes some good in A_{i_{t+1}}.
  - Passing one such good backward along P lowers i_k's utility by 1, raises i_1's by 1 and leaves everyone else unchanged, contradicting MNW. — [HS19](https://www.cs.toronto.edu/~nisarg/papers/subsidy.pdf)
- **Only the transfer property is used.** Besides non-wastefulness, "the only property of the MNW algorithm that we used" is this transfer property. It is implied by the Pigou–Dalton principle, so leximin also works. — [HS19](https://www.cs.toronto.edu/~nisarg/papers/subsidy.pdf)
- **Other results.**
  - Proposition 2 (binary valuations): computing the minimum subsidy is Turing-equivalent to deciding EF existence; the proof uses integral edge weights and integral subsidies.
  - Propositions 3–4 (identical valuations): every allocation is envy-freeable, p*_i = max_j v(A_j) − v(A_i), and any EF1 allocation needs ≤ n−1.
  - Theorem 6: n = 2 via round robin.
  - Conjecture 1: an EF1 and envy-freeable allocation exists. Conjecture 2: n−1 suffices. — [HS19](https://www.cs.toronto.edu/~nisarg/papers/subsidy.pdf)
- **The characterization is reused beyond nonnegative additive valuations.**
  - BKNS prove Lemma 3 "for general valuations". — [BKNS22](https://arxiv.org/abs/2201.07419)
  - Kawase et al. allow arbitrary v_i : 2^M → ℝ. — [Kawase et al.](https://arxiv.org/abs/2308.11230)
  - Dupré la Tour–Suzuki give "a self-contained derivation for mandatory assignment and possibly negative bundle values" (Lemma 4). — [DlT–S26](https://arxiv.org/abs/2609.08272)
  - LMS26 apply it to mixed additive valuations. — [LMS26](https://arxiv.org/abs/2607.10089)

### Inferences
- [Assessment] **Validity in T.** Theorems 1 and 2 hold in T unchanged: no step uses additivity, monotonicity or sign, and Theorem 2 uses only p ≥ 0. In T all arc weights and minimal subsidies are integers, so unit subsidy ⟺ some envy-freeable allocation has every simple path of weight ≤ 1.
- [Assessment] **Theorem 5's ingredients, checked against T.**
  - Non-wastefulness can be replaced by utilitarian optimality: a USW-optimal allocation is envy-freeable for any valuations, by Theorem 1(b).
  - v_i(A_i) = |A_i| fails as soon as an owner holds a chore or a zero-marginal item, and also for non-additive valuations.
  - Backward item-passing needs an exchange property: each move changes exactly the two endpoint utilities, by ±1. This holds for additive binary goods and, via matroid augmentation, for matroid-rank goods (Goko/Babaioff), but not in general T.
  - MNW is undefined with negative utilities. Leximin/Lorenz criteria are still defined, and HS note the argument needs only the Pigou–Dalton transfer property.
- [Assessment] **What a mixed-manna analogue would need.** For a positive path of weight ≥ 2, a sequence of single-item moves along it whose net effect is a Pigou–Dalton transfer: −1 to the richer endpoint, +1 to the poorer one, 0 elsewhere, while keeping USW optimality. With chores, a move could also push a chore forward (i_t hands one of her chores to i_{t+1}). I found no paper doing this in the subsidy context. For additive ternary utilities the question is moot because of LMS26.
- [Assessment] **Identical valuations in T (a cheap sanity check).** HS's identical-valuation argument holds for arbitrary set functions: every allocation is envy-freeable and p*_i = max_j v(A_j) − v(A_i). So unit subsidy for identical T is equivalent to a partition whose bundle values all lie within 1 of each other.
  - For n = 2 this follows from a prefix/suffix intermediate-value argument: moving one item changes v(F) − v(L) by at most 2, and the sign flips between the endpoints. This mirrors Bérczi et al.'s Theorem 1 and is my derivation.
  - For n ≥ 3 I found no result.

### Gaps
- I did not read the appendix examples in HS (App. B.3).

## 6. Goko et al. (GEB 2024): matroidal goods, truthful, utilitarian-optimal, ≤ 1 per agent; which matroid/M♮-concavity properties are used, and whether there is an analogue for binary marginals with both signs

### Takeaway
Goko et al.'s unit subsidy (together with truthfulness and utilitarian optimality) for matroidal goods rests on three pillars:
- Clean allocations, with v_i(A_i) = |A_i|, and free disposal.
- Matroid augmentation/exchange (Lemma 3.3): an augmenting path in the exchange graph of a matroid intersection.
- M-convexity of the size vectors of clean (utilitarian-optimal) allocations (Lemma 3.4), plus Frank–Murota's theorem that the Lorenz-dominating elements of an M-convex set form a matroidal M-convex set (Lemma 3.5). Proposition 3.6 follows: each agent's value varies by ≤ 1 across clean Lorenz-dominating (cLD) allocations.

Envy-freeness (Lemma 3.12) is a three-case argument using augmentation, Lorenz dominance and M-convex exchange. Completion without free disposal (SEC, Theorem 3.20) is a FindSink-like loop, and it works because leftover items have zero marginal for every recipient. All of this is specific to goods. I found no analogue for M♮-concave valuations with {−1,0,1} marginals.

### Cited Findings
- **Theorem 3.1.** Matroidal valuations are submodular with dichotomous marginals. For them there is a polynomial-time, truthful, utilitarian-optimal, envy-free mechanism with subsidies in {0,1} and total ≤ n−1. The model assumes v_i : 2^M → ℝ+ monotone. — [Goko et al.](https://arxiv.org/abs/2105.01801)
- **The SE mechanism.** Choose any A ∈ cLD, and give 1 to agent i iff |A_i| = min_{B∈cLD}|B_i| and |A_i| < max_j |A_j|. Example 3.2 shows that truthfulness forces subsidizing agents who want nothing. — [Goko et al.](https://arxiv.org/abs/2105.01801)
- **Structure of cLD allocations.**
  - Lemma 3.3 (from Babaioff–Ezra–Feige, Lemma 17): between clean allocations A and B with |A_i| > |B_i| there is a transfer sequence built from matroid augmentation, "interpreted as an augmenting path in the exchange graph of a matroid intersection".
  - Lemma 3.4: the size vectors of clean allocations (with A_0 the unallocated set), and of clean utilitarian-optimal allocations, are M-convex.
  - Lemma 3.5 (via Frank–Murota, Thm 5.7): the size vectors of cLD allocations form a matroidal M-convex set, and a minimum-weight cLD allocation is computable in polynomial time.
  - Proposition 3.6: max_{B∈cLD}|B_i| − min_{C∈cLD}|C_i| ∈ {0,1}.
  - Proposition 3.7: utilities do not depend on which cLD allocation is chosen. — [Goko et al.](https://arxiv.org/abs/2105.01801)
- **Lemma 3.12 (envy-freeness).** Suppose i still envies j after subsidies. Two cases:
  - v_i(A_i) < v_i(A_j): augmentation gives e ∈ A_j with v_i(A_i∪e) = v_i(A_i)+1, and moving e produces another cLD allocation. Proposition 3.6 then gives p_i = 1 and p_j = 0, so the envy disappears.
  - v_i(A_i) = v_i(A_j): handled by M-convex exchange within cLD. — [Goko et al.](https://arxiv.org/abs/2105.01801)
- **Completion: Theorems 3.19–3.20, Lemmas 3.22–3.23, Corollary 3.24.**
  - Theorem 3.19: no truthful, envy-free mechanism returning complete Lorenz-dominating allocations has o(m) subsidy, even for two agents with binary additive valuations.
  - Theorem 3.20: the SEC algorithm is complete, utilitarian-optimal and envy-free with subsidies in {0,1}, but not truthful. Example 3.21 shows naive completion can force a subsidy of 2.
  - SEC Step 2(b): if adding e to i creates a positive-weight path ending at i, move e to that path's initial agent.
  - Lemma 3.22 maintains the invariants "USW-optimal" and "no path > 1, no positive cycle". It uses v_i(A_i∪{e}) = v_i(A_i), from utilitarian optimality, and v_j(A_i∪{e}) ∈ {v_j(A_i), v_j(A_i)+1}.
  - Lemma 3.23: each agent is visited at most once (closed walk → zero-weight cycles → welfare-improving rotation).
  - Corollary 3.24 / Proposition A.1: the SEC output is EFX. — [Goko et al.](https://arxiv.org/abs/2105.01801)
- **Beyond matroidal valuations.** For superadditive valuations (Section 4), VCG with an upfront subsidy of m is truthful, envy-free and utilitarian-optimal, and m is necessary even for additive valuations. For general monotone submodular valuations (Section 5), no mechanism is simultaneously truthful, envy-free and utilitarian-optimal, whatever the subsidy. — [Goko et al.](https://arxiv.org/abs/2105.01801)
- **Chore-side binary class.** For binary supermodular costs, EF1 and PO allocations exist, while EFX and PO are incompatible (Barman, Narayan, Verma 2023, as reported by TWYZ). — [TWYZ](https://arxiv.org/abs/2308.12177)

### Inferences
- [Assessment] **Each property used, and its status in T.**
  - Cleanliness and free disposal: chores cannot be discarded, and "value = size of the clean bundle" has no analogue once an owner holds chores.
  - Augmentation: valuated-matroid / M♮-concave exchange does exist for gross-substitutes functions. It covers {−1,0,1} examples such as v(S) = r(S ∩ G) − |S ∩ C|, and v(S) = r(S) − |S|, which is minus the binary supermodular "nullity" cost. But Goko's arguments use the unit-increment form (the receiver gains exactly 1, the giver loses exactly 1), which fails when the exchanged item is a chore for one side.
  - M-convexity of utility vectors: for matroidal goods, utility vectors are size vectors of clean bundles. I know of no result that the utility vectors of USW-optimal allocations under {−1,0,1} M♮-concave valuations form an M-convex set. Without that, Frank–Murota's Lorenz machinery (Prop. 3.6) is unavailable.
- [Assessment] **Most promising piece to reuse.** SEC's completion loop and the cycle argument of Lemma 3.23. This is the same skeleton as BKNS's FINDSINK and the requester's completion. Its correctness needs the recipient's own-bundle marginal for the leftover item to be ≥ 0 (here exactly 0), the same condition isolated in Q1.
- [Assessment] **Natural first test class for an analogue:** "matroid goods minus additive chores", v_i(S) = r_i(S ∩ G_i) − |S ∩ C_i|. It is doubly monotone and M♮-concave, with marginals in {−1,0,1}.

### Gaps
- I found no paper on subsidies, or on Lorenz-dominating allocations, for M♮-concave or valuated-matroid valuations with negative marginals.
- The GEB 2024 version may renumber lemmas; arXiv v1 was used.

## 7. Tao, Wu, Yu, Zhou (binary chores): which steps of the partial-allocation algorithm use chores only (cost marginals in {0,1}), and is a mixed-sign version plausible?

### Takeaway
TWYZ's Theorem 5.1 gives an envy-free partial allocation leaving ≤ n−1 chores unallocated, for arbitrary cost functions with marginals in {0,1}. Every rule relies on "chores only": rules R1–R3 preserve envy-freeness because adding an item to a bundle never makes that bundle look better to an observer (costs are monotone). R3 additionally uses integrality and marginal ≤ 1. With subjective goods, R1–R3 can create envy along tight (equality) arcs. A mixed version would need a "source-SCC" rule for goods and a "tail-SCC" rule for chores, and these conflict when an item's sign varies across observers. I found no mixed version.

### Cited Findings
- **Setting and results.** Costs have binary marginals, c_i(e|S) ∈ {0,1}, and "any binary marginal cost function is also monotone".
  - Theorem 3.1 (additive binary costs): EFX and PO, in polynomial time.
  - Theorem 4.1 (cancelable costs): EFX. Theorem 4.8: for cancelable costs, EFX and PO are incompatible.
  - Theorem 5.1 (general binary-marginal costs): an envy-free partial allocation with ≤ n−1 unallocated items, in polynomial time.
  - Theorem D.1 / Corollary D.2 (submodular binary costs): a complete 2-EFX allocation. — [TWYZ](https://arxiv.org/abs/2308.12177)
- **Definition 5.2 (the graph).** There is an arc (i,j) iff agent i's cost for her own bundle equals her cost for j's bundle: "an edge in our envy graph represents equality, or, 'about to envy'." — [TWYZ](https://arxiv.org/abs/2308.12177)
- **Algorithm 3 (three rules).**
  - R1: give an unallocated item e to an agent i with c_i(e|X_i) = 0.
  - R2: if (i,j) lies on a directed cycle C and c_i(e|X_j) = 0, rotate the bundles along C and add e to i's new bundle.
  - R3: otherwise, pick a tail SCC S (no outgoing arcs) and give each agent of S one unallocated item. Stop if fewer than |S| items remain. — [TWYZ](https://arxiv.org/abs/2308.12177)
- **Why envy-freeness is preserved.** R1 and R2 are called "straightforward". For R3:
  - "Agent k does not envy agent i as agent i's cost can only be increased from k's perspective."
  - S is a tail SCC, so (i,k) ∉ E for k outside S, which gives c_i(X_i) ≤ c_i(X_k) − 1.
  - i's cost rises by at most 1 (by exactly 1, since R1 does not apply).
  - For an arc (i,j) ∈ E inside S, the arc lies on a cycle. Since R1–R2 do not apply, c_i(e|X_i) = c_i(e|X_j) = 1, so both costs rise by 1.
  - At termination fewer than |S| ≤ n−1 items remain. — [TWYZ](https://arxiv.org/abs/2308.12177)
- **Goods versus chores.** TWYZ note: "In the setting of chores division, the cycle-elimination process will sometimes break the EFX property, which will not happen in the world of goods division." — [TWYZ](https://arxiv.org/abs/2308.12177)

### Inferences
- [Assessment] **Exact uses of "chores only".**
  - R1 and R2 need c_k(X ∪ e) ≥ c_k(X) for every observer k, so that nobody starts envying the recipient.
  - R3 needs the same property for observers k ∉ S, and for pairs i,j ∈ S without an arc between them.
  - R3's step inside the SCC needs c_i(e|X_j) = 1 on in-SCC arcs. That follows from binary costs plus the other rules being exhausted. It is sign-specific: a cost of −1 (a good) relative to X_j would create envy.
  - Integrality and marginal ≤ 1 give R3's slack c_i(X_i) ≤ c_i(X_k) − 1.
- [Assessment] **A mixed version.** In utility terms, a mixed item in T can be a good (+1) for some observers relative to the recipient's bundle.
  - Giving it to i breaks envy-freeness for any k with a tight arc (k,i) who sees it as a good.
  - The goods counterpart of R3 would hand goods to a source SCC (no tight arcs entering from outside), the mirror image of a tail SCC. An item that is a chore for some members and a good for some observers needs both conditions at once.
  - The "≤ n−1 leftovers" accounting would also need a two-sided version. Leftover goods create envy towards their recipient, while leftover chores create envy from their recipient.
  
  So the requester's completion (leftovers to distinct tail-SCC agents plus backward-closure payments) would need a goods mirror. This looks plausible only in restricted cases, such as objective signs, where the requester's (c) already applies.
- [Assessment] **Most reusable piece.** The equality-graph view (tight arc = "about to envy") does not depend on signs, and LMS26's Case II equality paths share it.

### Gaps
- I did not check the venue or version of TWYZ (arXiv v1 was used).
- I found no published goods or mixed analogue of Theorem 5.1.
- I did not read arXiv 2608.10572 ("Non-Existence of EFX Chore Allocations for Monotone Cost Functions with Binary Marginals", 2026), which surfaced in search and may be relevant background.

## 8. Topological and discrepancy methods (Dupré la Tour & Fujii 2025; Dupré la Tour & Suzuki 2026): where exactly does the sign assumption enter?

### Takeaway
**DlT–F (2025)** gives O(√(n log n)) per agent and O(n^{3/2}√log n) in total for arbitrary valuations with marginals in [−1,1], but only when n is a prime power. Their topological input (Jojić–Panina–Živaljević constrained necklace splitting, a Borsuk–Ulam-type argument) needs only continuity and no sign condition; the restriction is number-theoretic.

**DlT–S (2026)** removes the prime-power restriction for all-nonnegative or all-nonpositive valuations, using KKM. The sign assumption enters only through the empty-bundle boundary condition (Lemma 6): an empty slot's canonical price is the minimum price (nonnegative case) or the maximum price (nonpositive case). Mixed-sign T breaks that boundary, and the authors say an alternative equalization is needed.

Both results are existential and far from unit subsidies.

### Cited Findings
- **DlT–F Theorem 1 and Corollary 2.** For k a prime power and n valuations with marginals in [−1,1] (monotonicity not assumed), there is a k-partition with |v_i(S_ℓ) − v_i(S_ℓ')| = O(√(n log nk)). Corollary 2: "For arbitrary valuations with marginals in the interval [−1, 1], if the number of agents n = p^ν is a power of a prime, there exists an envy-free allocation requiring a total subsidy of O(n√(n log n))." This is the first subquadratic bound. — [DlT–F25](https://arxiv.org/abs/2509.16802)
- **DlT–F proof.** It uses multilinear extensions and Theorem 3 (Jojić–Panina–Živaljević): for prime-power k, continuous set functions on unions of intervals admit a partition into k equal-valued bundles with few pieces.
  - "Additivity is never used in the proof—the argument relies solely on continuity to invoke a Borsuk–Ulam-type theorem".
  - It finishes with randomized rounding and McDiarmid's inequality.
  - For composite k, "the standard proof … uses a recursive cutting procedure that crucially depends on additivity". — [DlT–F25](https://arxiv.org/abs/2509.16802)
- **DlT–F Lemma 5.** Reassign the discrepancy partition's bundles to maximize welfare. Then p_i ≤ |v_j(A_i) − v_j(A_j)| ≤ disc(V,n), via the back-arc (j,i) that closes the maximum path; the total is ≤ (n−1)·disc. Their Table 1 lists earlier bounds: additive n−1, dichotomous n−1, monotone (n²−n−1)/2, doubly monotone n(n−1)/2. — [DlT–F25](https://arxiv.org/abs/2509.16802)
- **DlT–S Theorem 1.** Assume v_i(∅)=0, single-item marginals in [−1,1], and either v_i(S) ≥ 0 for all i and S, or v_i(S) ≤ 0 for all i and S. Monotonicity is not required, and the paper gives a non-monotone nonnegative example. Then an envy-free outcome exists with Σp ≤ 5√2(n−1)^{3/2}√log(4n) (per agent ≤ 5√(2(n−1)log(4n))). The result is existential. — [DlT–S26](https://arxiv.org/abs/2609.08272)
- **DlT–S mechanism.**
  - Lemma 4: canonical prices are the coordinatewise least nonnegative supporting prices, equal to the maximum walk weight ending at each slot. Their minimum is 0, and subsidies are p_i = q_max − q_σ(i).
  - Lemma 5: duplicate-bundle identity q_k = W⁺_k − W, the mandatory-assignment counterpart of Gul–Stacchetti.
  - Lemma 7: moving one item changes every price by ≤ 5.
  - Random interval cuts leave ≤ n−1 fractional items.
  - Lemma 8 (KKM equalization): continuous functions F_k ≥ 0 with F_k = 0 whenever x_k = 0 can be equalized.
  - Proposition 9: take F_k = Q_k in the nonnegative case and F_k = max_j Q_j − Q_k in the nonpositive case.
  - Finish with McDiarmid's inequality and a union bound. — [DlT–S26](https://arxiv.org/abs/2609.08272)
- **DlT–S Lemma 6 and the authors' discussion.** "We first record the only step in the proof that uses the sign of the valuations." If B_k = ∅:
  - Nonnegative case: q_k = 0, because arcs leaving the empty slot have weight v_{a_k}(B_j) ≥ 0.
  - Nonpositive case: q_k = max_j q_j, because arcs entering it have weight −v_{a_j}(B_j) ≥ 0.
  
  Discussion: "All other ingredients—the matching identity, one-item stability, and concentration—apply to arbitrary valuations with bounded single-item marginals. Extending our approach to mixed-sign valuations for every number of agents therefore calls for an alternative way to equalize expected prices." — [DlT–S26](https://arxiv.org/abs/2609.08272)
- **Analogy and open questions (DlT–S).** They compare their boundary condition with Su's "hungry"/"lazy" condition in cake cutting. They cite Avvakumov–Karasev (2021): without such assumptions, envy-free cake division "is still guaranteed when the number of agents is a prime power, but may fail otherwise". Open questions: removing the √log n factor, a linear total bound for general monotone valuations, and efficient computation. — [DlT–S26](https://arxiv.org/abs/2609.08272)

### Inferences
- [Assessment] **Status in T.**
  - DlT–F applies directly when n is a prime power, giving O(√(n log n)) per agent, which is far from unit.
  - DlT–S applies only to the subclass where every agent values every bundle ≥ 0 (or every bundle ≤ 0). In genuinely mixed T an agent can value some bundles positively and others negatively, so neither boundary case of Lemma 6 holds.
  - Precisely: the nonnegative case needs only the agent matched to the empty slot to value every bundle ≥ 0. The nonpositive case needs every agent's own bundle to be ≤ 0. Both fail generically when agents' signs differ.
- [Assessment] **The obstruction is a known one.** It matches the obstruction in envy-free cake cutting without a boundary condition (Avvakumov–Karasev): topological existence is available for prime-power n but may fail otherwise. A topological route to mixed-sign subsidy results for all n would therefore need new equivariant arguments or a non-topological equalization.
- [Assessment] **Not a route to unit subsidies, but useful vocabulary.** These methods lose constants and logs (union bound, McDiarmid) and are existential, so they cannot deliver p ∈ {0,1}^n. Their reusable components are combinatorial:
  - Lemmas 4 and 5 (canonical prices) and Lemma 7 (one-item stability) hold for arbitrary valuations.
  - For a fixed partition with a welfare-maximizing assignment, the largest HS-minimal subsidy equals the longest path weight, which is q_max. So unit subsidy ⟺ some partition has q_max ≤ 1. This is a convenient way to measure how far a partition is from unit subsidies.

### Gaps
- I did not read Avvakumov–Karasev or Jojić–Panina–Živaljević directly.
- In the text extraction of DlT–S, the marginal assumption in eqs. (1) and (3) appears one-sided (≤ 1). The abstract and introduction state two-sided marginals in [−1,1], and Lemma 7 needs a two-sided bound.

## 9. Cross-cutting: which ingredients survive in T, which break, and what is the best known bound for each slice of T?

### Takeaway
In T the bookkeeping layer of subsidy theory survives intact. This includes:
- the HS characterization and minimal subsidies, plus integrality (unit ⟺ every path ≤ 1);
- BKNS Lemma 3;
- Brustle's Lemma 4.1;
- Kawase's Lemmas 3–4;
- DlT–F's back-arc lemma and DlT–S's price lemmas;
- the BKNS/Goko rotation argument on zero-weight cycles.

What breaks is every step that adds an item to a bundle and needs the resulting change in arc weights to have one sign:
- BKNS Prop. 6 and Lemma 9 (the recipient must not dislike the item);
- TWYZ R1–R3 (observers must not like it);
- Goko's unit exchanges;
- matching-round telescoping, which needs additivity;
- DlT–S's empty-bundle boundary.

Slices of T with known results:
- additive: unit (LMS26);
- monotone: unit (BKNS);
- matroidal: unit and truthful (Goko);
- n = 2: unit (Kawase + Bérczi);
- doubly monotone: n−1 per agent (Kawase);
- prime-power n: O(√(n log n)) per agent (DlT–F);
- all-nonnegative or all-nonpositive: the same order (DlT–S).

I found no bound independent of m for non-doubly-monotone, mixed-sign T with n ≥ 3 not a prime power, and EF1 existence there is open.

### Cited Findings
- **Integrality of subsidies.**
  - HS's proof of Proposition 2: with binary valuations, "edges in G_A have integral weight. Hence … sub(A) is integral", and minimal subsidies are integral. — [HS19](https://www.cs.toronto.edu/~nisarg/papers/subsidy.pdf)
  - BKNS Lemma 11 uses the same fact. — [BKNS22](https://arxiv.org/abs/2201.07419)
- **Additive {−1,0,1} ("tertiary") utilities.** EF1 implies EFX, and the double round-robin algorithm gives such allocations. Aleksandrov–Walsh give EF1 plus PO in that setting (as reported). — [Bérczi et al.](https://arxiv.org/abs/2006.04428)
- **Non-monotone EF1 and the obstacle quote.** EF1 is open for arbitrary valuations even for three identical agents. The paper records the non-doubly-monotone obstacle "Item x is a chore for agent 1 given A_1 and is a good for agent 1 given A_2". It also states: "we know of no other properties (other than EF1) that hold in such general valuation classes" beyond doubly monotone. — [BKPR24](https://arxiv.org/abs/2411.19881)
- **EF1 plus envy-freeability for doubly monotone instances** is open, "still open in the setting with only indivisible goods". — [ALMS25](https://arxiv.org/abs/2511.04891)
- **Open questions beyond additive valuations.**
  - LMS26 pose constant per-agent subsidy for submodular or XOS mixed valuations. — [LMS26](https://arxiv.org/abs/2607.10089)
  - DlT–S say mixed signs need "an alternative way to equalize expected prices", and ask whether a linear total bound holds for general monotone valuations. — [DlT–S26](https://arxiv.org/abs/2609.08272)
- **Graph-orientation instances (goods only).** Li, Sun, Suzuki, Xing (2025) give an n−1 bound for general monotone valuations in graphical instances (as described by DlT–S). — [DlT–S26](https://arxiv.org/abs/2609.08272)
- **Other mixed-manna subsidy work targets proportionality, not envy-freeness.** LMS26 cite Wu et al. (2025b): total subsidy n/4 suffices for proportionality in mixed manna (n even). — [LMS26](https://arxiv.org/abs/2607.10089). A 2026 paper on weighted proportionality for mixed manna also appeared in the search (abstract only). — [arXiv 2609.15208](https://www.alphaxiv.org/abs/2609.15208)

### Inferences
- [Assessment] Summary of each technique against T:

| Technique | Property it really uses | Survives in T? | Where it breaks in T |
|---|---|---|---|
| HS Thm 1–2 (characterization, minimal subsidies) | sums over permutations; p ≥ 0 | Yes, verbatim | — |
| HS Thm 5 (MNW, binary additive goods) | owner values own items at +1; unit Pigou–Dalton transfer; MNW positivity | No (additive ternary slice covered by LMS26) | owner may hold chores; non-additive exchanges not unit |
| Brustle IMWM + v̄ (Thm 1.3) | additivity; nonnegativity | Only additive slice (via LMS26/IMWPM) | no per-round decomposition |
| Brustle Lemma 5.2 / Kawase Lemmas 3–4 | an allocation with all envies ≤ 1 | Yes, if EF1 exists | EF1 existence open for non-doubly-monotone T, n ≥ 3; at best n−1 per agent |
| BKNS EXTEND (Def. 3, Lemmas 7–8) | HS; marginals ≤ 1; recipient marginal = +1 | Yes | — |
| BKNS FINDSINK (Lemmas 9–11) | tentative recipients' own-bundle marginal ≥ 0 | Only if item is weakly good for all of M(p) | item is a chore for some most-subsidized agent |
| Goko SE/SEC | matroid augmentation; M-convexity; clean bundles; free disposal | No | chores cannot be disposed; no M-convexity known |
| TWYZ R1–R3 | observers' costs monotone; integrality | Chores-only slice | goods create envy along tight arcs |
| LMS26 | additivity (meta-goods, telescoping, completion) | Additive slice only | non-additive |
| DlT–F | continuity; prime-power n | Yes for prime-power n (O(√(n log n)) per agent) | composite n |
| DlT–S | empty-bundle boundary (sign) | Only all-nonnegative or all-nonpositive | mixed signs |

- [Assessment] **Conditions for a unit-subsidy proof in T.** Combining Q1 and Q7, an incremental proof would have to handle three kinds of item:
  1. Items weakly good for every most-subsidized agent at her own bundle, or extendable: these are covered by BKNS-in-T.
  2. Items that are strict chores for some most-subsidized agent: these need a TWYZ/requester-style chore mechanism.
  3. Non-doubly-monotone agents, for whom the class of an item changes as bundles evolve.
  
  The bookkeeping available is HS + integrality + rotation along zero-weight cycles. The missing piece is an invariant that survives a −1 own-bundle marginal for a most-subsidized agent. Two places where that invariant is likely to come from:
  - an equality-graph closure argument (as in the requester's (a) and LMS26 Case II);
  - a two-sided (source and tail SCC) version of TWYZ.
- [Assessment] **EF1 inside the target.** Asking for EF1 together with unit subsidy in T is at least as hard as two open problems that are special cases of the target:
  - EF1 plus envy-freeability for dichotomous monotone goods. BKNS list it as future work and ALMS25 say the general monotone case is open.
  - EF1 existence for non-doubly-monotone valuations (BKPR24).
  
  Since T includes non-doubly-monotone instances with n ≥ 3 (e.g. unit-slope single-peaked valuations), the EF1 part of the target contains an open EF1-existence question.

### Gaps
- None of the sources I read gives a bound independent of m for general T (mixed signs, non-doubly-monotone, n ≥ 3 not a prime power). I cannot rule out unpublished or very recent work; discovery used alphaXiv search and web search, not exhaustive "cited-by" crawls on Google Scholar or Semantic Scholar.
- I found no paper treating M♮-concave or valuated-matroid valuations with negative marginals in the subsidy model.
- The sufficient condition in Q1 (own-bundle marginal ≥ 0 for all of M(p)) is my proof-reading, not a published lemma. Whether it can be met by a cleverer dynamic schedule in subclasses of T, such as doubly monotone with subjective signs, is untested.
