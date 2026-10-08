# Envy-freeness with subsidies for mixed / {−1,0,1}-marginal valuations: lower bounds, impossibility results, hardness, and stated open problems (as of 2 Oct 2026)

Scope note: "PR" = peer-reviewed venue; "PP" = arXiv preprint (not refereed as far as I could tell). The requester's own paper (arXiv 2609.14465, "Envy-Free Chore Allocation with Unit Subsidies under Negative Dichotomous Valuations") showed up in searches. It is deliberately **not** used as prior work anywhere below. Several 2026 preprints declare heavy AI assistance in their proofs: 2608.09437 says most proofs were obtained with GPT-5.6, 2608.10572 says its gadget was built by GPT-5.6 and checked in Lean 4, and 2608.29497 discloses significant GPT-5.6-Sol assistance. Treat those results as unrefereed. Where I read an arXiv version that predates the journal version, I say so, because open-problem numbering can differ between versions.

## Where the target question stands: unit subsidies p ∈ {0,1}^n, total ≤ n−1, for marginals in {−1,0,1}

### Takeaway
The general question (non-additive set functions with marginals in {−1,0,1}, mixed and possibly agent-specific signs, n ≥ 3) is **not settled by any external source I found**. Several neighbouring cases are already settled:
- **Additive** {−1,0,1} instances with subjective signs follow from Lu–Mackenzie–Suzuki (July 2026, PP) plus integrality.
- **n = 2** with arbitrary valuations follows from Kawase et al. combined with Bérczi et al.
- **Dichotomous goods** ({0,1} marginals) are covered by Barman et al. (IJCAI 2022).
- **Matroid-rank goods** are covered by Goko et al.
- **Boolean-valued** valuations are trivial.

Outside these cases, the best known bounds are polynomial in n and not unit:
- n−1 per agent and n(n−1)/2 total for doubly monotone valuations.
- O(n^{3/2}√log n) total, existential only, either for prime-power n with arbitrary signs, or for any n when every bundle value has the same sign.

### Cited Findings
- **Lu–Mackenzie–Suzuki (PP, 11 Jul 2026), Theorem 1.1, verbatim:** "For every instance with additive utilities u_i : M → [−1, 1], where each item may be a good for some agents and a chore for others, there exists an envy-free outcome (A, p) such that 0 ≤ p_i ≤ 1 for all i ∈ N. Furthermore, such an allocation can be computed in polynomial time." — [Lu, Mackenzie, Suzuki, arXiv 2607.10089](https://arxiv.org/abs/2607.10089)
- **LMS on scope:** "Our techniques rely heavily on additivity both to define meta-goods and to obtain telescoping envy-path bounds from iterated matchings. This approach does not directly extend to richer valuation classes." — [arXiv 2607.10089](https://arxiv.org/abs/2607.10089)
- **LMS on tightness:** the per-agent bound of 1 is optimal because "even in the goods-only setting, some instances require a subsidy of 1 for at least one agent [Brustle et al., 2020]". — [arXiv 2607.10089](https://arxiv.org/abs/2607.10089)
- **Halpern–Shah, Theorem 2.** For an envy-freeable allocation A, p*_i(A) = ℓ(i) (the maximum weight of any path starting at i in the envy graph) is envy-eliminating and componentwise minimal ("for every p ∈ P(A) and i ∈ N, p*_i(A) ≤ p_i"). It is computable in O(nm + n³) for additive valuations. — [Halpern & Shah, SAGT 2019 (PR), author PDF](https://www.cs.toronto.edu/~nisarg/papers/subsidy.pdf)
- **Goko et al., Theorem 2.3 (combining Halpern–Shah Theorems 1–2).** "A is envy-freeable with a subsidy of at most q for each agent" if and only if "G_A has neither a positive-weight cycle nor a path with a weight larger than q." — [Goko et al., arXiv 2105.01801 (AAMAS 2022; GEB 144:49–70, 2024; PR)](https://arxiv.org/abs/2105.01801)
- **Kawase et al.** consider non-monotone valuations with |v_i(X∪{e}) − v_i(X)| ≤ 1. Their Theorem 1, verbatim: "If the valuations are doubly monotone or n = 2, there exists an envy-free allocation with a subsidy (A, p) such that max p_i ≤ n − 1 and Σ p_i ≤ n(n − 1)/2. Moreover, such an envy-free allocation with a subsidy can be computed in polynomial time." The n = 2 case relies on the two-agent EF1 algorithm of Bérczi et al. — [Kawase et al., arXiv 2308.11230 (AAAI 2024; AIJ 348:104406, 2025; PR)](https://arxiv.org/abs/2308.11230)
- **Bérczi et al., Theorem 1:** "There always exists an EF1 allocation for two agents with arbitrary (not necessarily monotone or additive) utility functions. Such an allocation can be computed in polynomial time." — [Bérczi et al., arXiv 2006.04428 (TCS 1002:114596, 2024; PR)](https://arxiv.org/abs/2006.04428)
- **Kawase et al. on EFk:** "even when the valuations are general and we only have an EFk allocation, we can still derive an envy-free allocation with a subsidy of at most k(n − 1) per agent and k · n(n − 1)/2 in total." — [arXiv 2308.11230](https://arxiv.org/abs/2308.11230)
- **Barman–Krishna–Narahari–Sadhukhan, Theorem 4.** For dichotomous valuations (v_i(S∪{g}) − v_i(S) ∈ {0,1}; monotone, not necessarily submodular), "there exists an envy-free solution (A, p) such that p ∈ {0, 1}^n", computable in polynomial time in the value-oracle model. — [Barman et al., arXiv 2201.07419 (IJCAI 2022; PR)](https://arxiv.org/abs/2201.07419)
- **Goko et al., Theorem 3.1:** "For matroidal valuations, there is a polynomial-time implementable mechanism that is truthful, utilitarian optimal, and envy-free with each agent receiving subsidy 0 or 1, and the the total subsidy being at most n − 1." — [arXiv 2105.01801](https://arxiv.org/abs/2105.01801)
- **Halpern–Shah, Theorem 5 (binary additive goods):** "an allocation produced by the maximum Nash welfare algorithm is envy-freeable and requires at most n − 1 subsidy." The proof shows that every path in G_A has weight at most 1. — [Halpern & Shah (PR)](https://www.cs.toronto.edu/~nisarg/papers/subsidy.pdf)
- **Dupré la Tour–Fujii, Lemma 5.** Bundles from an n-coloring are assigned by welfare-maximizing matching, and p_i ≤ |v_j(A_i) − v_j(A_j)|, where j is the endpoint of i's heaviest path (no positive cycles). Hence p_i ≤ disc(V, n).
- **Dupré la Tour–Fujii, Corollary 2:** "For arbitrary valuations with marginals in the interval [−1, 1], if the number of agents n = p^ν is a power of a prime, there exists an envy-free allocation requiring a total subsidy of O(n√(n log n))." — [Dupré la Tour & Fujii, arXiv 2509.16802 (PP, Sep 2025)](https://arxiv.org/abs/2509.16802)
- **Dupré la Tour–Suzuki, Theorem 1 (PP, 8 Sep 2026).** Assume v_i(∅) = 0, single-item marginals in [−1,1] (per the abstract), and either v_i(S) ≥ 0 for every i and S, or v_i(S) ≤ 0 for every i and S. Then an EF outcome exists with Σp_i ≤ 5√2 (n−1)^{3/2} √log(4n), and "The guarantee is existential". Neither class requires monotonicity. — [Dupré la Tour & Suzuki, arXiv 2609.08272](https://arxiv.org/abs/2609.08272)
- **Dai et al., Lemma 3.2 (house allocation, binary utilities):** "each agent requires a subsidy of at most 1 in any EFable allocation". The proof closes the heaviest path with a back-edge of weight ≥ −1. — [Dai, Li, Wu, Zhang, arXiv 2608.22216 (PP, Aug 2026)](https://arxiv.org/abs/2608.22216)
- **Dupré la Tour (PP, Aug 2026), Theorem 1:** "Every instance with three agents and arbitrary valuations admits a balanced EF1^c_g allocation." Here EF1^c_g means envy-free up to one good and one chore. The proof is existential. — [Dupré la Tour, arXiv 2608.09437](https://arxiv.org/abs/2608.09437)
- **Dupré la Tour–Fujii, Table 1 (state of the art as of Sep 2025), marginals in [−1,1]:**
  - Monotone additive: n−1 [Brustle et al.]
  - Monotone: 2(n−1)² [Brustle et al.], improved to (n²−n−1)/2 [Kawase et al.]
  - Monotone dichotomous: n−1 [Barman et al.]
  - Doubly monotone: n(n−1)/2 [Kawase et al.]
  - Arbitrary valuations with n a prime power: O(n√(n log n)) [Dupré la Tour–Fujii]
  
  — [arXiv 2509.16802](https://arxiv.org/abs/2509.16802)

### Inferences
- **Integrality reduces "unit subsidies" to "per-agent ≤ 1".** If v_i(∅) = 0 and every marginal lies in {−1,0,1}, every bundle value is an integer. So every envy-graph weight and every longest-path value ℓ(i) is an integer. By Halpern–Shah Theorem 2, any EF outcome (A, p) with p ≤ 1 gives p*(A) ≤ p with p*(A) integral, hence p*(A) ∈ {0,1}^n. Since some p*_i = 0, the total is ≤ n−1.
- **Additive {−1,0,1} case is already solved externally.** Combining LMS Theorem 1.1 with the integrality argument settles the additive case of the target question in polynomial time, with arbitrary subjective signs and no double monotonicity needed (additive items are automatically doubly monotone per agent). This is my inference from LMS plus Halpern–Shah. LMS is an unrefereed July 2026 preprint with an intricate case analysis and should be checked.
- **n = 2 is already solved externally.** For any valuations with marginals in [−1,1], Kawase Theorem 1 gives max p_i ≤ 1 and Σp_i ≤ 1 in polynomial time (via Bérczi's EF1 for two agents). With integer marginals this yields p ∈ {0,1}². The target question is therefore open only for n ≥ 3.
- **Boolean-valued valuations are trivial.** Valuations v_i: 2^M → {0,1} with v_i(∅) = 0 have marginals in {−1,0,1}. By the back-edge argument used in Dupré la Tour–Fujii Lemma 5 and Dai et al. Lemma 3.2, every envy-freeable allocation (for example, any partition with bundles reassigned by maximum-weight matching) has p*_i ≤ max_j (v_j(A_j) − v_j(A_i)) ≤ 1. More generally, the target is trivial whenever each agent's values on the bundles of the chosen partition span a range ≤ 1. Hard instances must have bundle-value ranges ≥ 2.
- **n = 3 has a constant bound, but not a unit one.** Dupré la Tour's EF1^c_g allocation (remove one item c from your own bundle and one item g from the other's) is EFk with k = 2 in Kawase's sense (take X = {c, g}). Kawase's EFk remark then gives per-agent ≤ 4 and total ≤ 6 for n = 3 with arbitrary valuations. This is existential, not unit, and not polynomial-time.
- **The real open frontier** is non-additive valuations, n ≥ 3, with mixed signs. It splits into two subcases:
  - Doubly monotone (agent-specific but consistent sign per item): best known is n−1 per agent and n(n−1)/2 total (Kawase).
  - Non-doubly-monotone: even EF1 existence is open (next section), and for non-prime-power n with mixed-sign bundle values I found no m-independent subsidy bound at all.

### Gaps
- I found no external paper that studies unit or {0,1} subsidies for non-additive mixed-sign valuations with {−1,0,1} marginals. Every paper on that exact class that I found is the requester's own.
- I found no source giving an m-independent total-subsidy bound for arbitrary-sign valuations when n is not a prime power. Dupré la Tour–Suzuki say extending to mixed signs for every n "calls for an alternative way to equalize expected prices" ([arXiv 2609.08272](https://arxiv.org/abs/2609.08272)).
- I found no source that asks whether utilitarian optimality or PO together with unit subsidies holds for general (non-submodular) dichotomous goods. Goko et al. cover only matroid-rank goods.

## Lower bounds: instances forcing large subsidy, and allocation/technique-level lower bounds

### Takeaway
When the allocation can be chosen, the only instance-level lower bound known in any class with marginals in [−1,1] is **n−1 total (1 per agent)**: one item valued 1 by everyone. It is already tight for binary and identical valuations, and every 2023–2026 source repeats that nothing larger is known. The large lower bounds in the literature are all **conditional**: a *given* allocation, an *arbitrary* EF1 allocation, an extra efficiency or truthfulness requirement, a specific technique (discrepancy), or a restricted feasibility model (orientations, house allocation).

### Cited Findings
- **Halpern–Shah, Theorem 4, verbatim:** "When the allocation can be chosen, the minimum subsidy required is at least n − 1 in the worst case, even in the special cases of binary valuations and identical valuations." Instance: each agent values one special good at 1 and the rest at 0. — [Halpern & Shah (PR)](https://www.cs.toronto.edu/~nisarg/papers/subsidy.pdf)
- **Halpern–Shah, Theorem 3, verbatim:** "When an envy-freeable allocation is given, the minimum subsidy required is (n − 1)m in the worst case." The lower-bound instance has v_i(g) = 1 for all i and g, with all goods given to one agent. So even identical binary valuations can force per-agent subsidy m for a badly chosen envy-freeable allocation. — [Halpern & Shah](https://www.cs.toronto.edu/~nisarg/papers/subsidy.pdf)
- **Liu–Lu–Suzuki–Walsh survey:** "As there are no lower bounds known beyond the aforementioned n − 1 bound, this leads to a natural question." (This leads into Open Question 9.) — [Liu et al., arXiv 2306.09564 (JAIR 80:1373–1406, 2024; PR)](https://arxiv.org/abs/2306.09564)
- **Kawase et al.:** "the only known lower bound on the total subsidy is n − 1 (which can be obtained using the case with n agents and one item ...)" — [arXiv 2308.11230](https://arxiv.org/abs/2308.11230)
- **Li–Sun–Suzuki–Xing:** "the tight bound for monotone valuations is still unknown [LLSW24], where the lower bound is n − 1." — [Li et al., arXiv 2502.13671 (PP, 2025)](https://arxiv.org/abs/2502.13671)
- **Dupré la Tour–Suzuki (Sep 2026):** "The single-good example gives a lower bound of n − 1, leaving a gap between this linear lower bound and our upper bound of O(n^{3/2}√log n)." — [arXiv 2609.08272](https://arxiv.org/abs/2609.08272)
- **Barrier for arbitrary EF1 allocations (Kawase et al.).** "our upper bounds of n−1 per agent and n(n−1)/2 in total cannot be improved when considering an arbitrary EF1 allocation (Example 1)." Example 1 is additive monotone with values n/(n+1) and 1, an envy-freeable EF1 allocation, and minimum subsidy vector (0, 1, …, n−1). By modifying bundles they reach n−1.5 per agent and (n²−n−1)/2 total for monotone valuations with n ≥ 3 (Theorem 2). For n = 2, "This bound cannot be improved even when there is one item with a value of 1 for each agent." — [arXiv 2308.11230](https://arxiv.org/abs/2308.11230)
- **LMS barriers:**
  - "Even in goods-only instances, an allocation may be both EF1 and envy-freeable while its heaviest envy path has weight n − 1."
  - Bundles must be kept at value ≤ 1: "Without it, even a two-agent instance containing a single meta-good may require a subsidy strictly greater than one."
  
  — [arXiv 2607.10089](https://arxiv.org/abs/2607.10089)
- **Brustle et al., Claim 3.3:** "Let A be both envy-freeable and EF1. Then the minimum total subsidy required is at most (n − 1)²". This is the natural EF1-route bound that their matching analysis then beats. — [Brustle et al., arXiv 1912.02797 (EC 2020; PR)](https://arxiv.org/abs/1912.02797)
- **Halpern–Shah on simple algorithms.** For binary valuations, round-robin with an arbitrary ordering gives only O(n²), "This is the best we can do using the round-robin method with an arbitrary agent ordering". MNW does not minimize per-instance subsidy: there are instances "where envy-free allocations exist but the MNW algorithm produces an allocation which requires as much as n − 2 subsidy". — [Halpern & Shah](https://www.cs.toronto.edu/~nisarg/papers/subsidy.pdf)
- **Efficiency-constrained lower bound (Goko et al., Theorem 4.2), verbatim:** "For any ε > 0, if a mechanism is envy-free and utilitarian optimal, it requires a subsidy of m − ε for each agent, even when there are only two agents with additive valuations such that the value of each item is at most 1." Instance: v_1(X) = |X| and v_2(X) = (1 − ε/m)|X|, which is not binary. — [arXiv 2105.01801](https://arxiv.org/abs/2105.01801)
- **Truthfulness-constrained lower bound (Goko et al., Theorem 3.19), verbatim:** "If a truthful mechanism is envy-free, and returns a complete Lorenz dominating allocation, it requires a subsidy of Ω(m), even when there are two agents with binary additive valuations." — [arXiv 2105.01801](https://arxiv.org/abs/2105.01801)
- **Goko et al., Theorem 5.2.** Completeness plus EF can force per-agent subsidy m, but only with unnormalized marginals. Footnote 14: "we do not know whether a similar example exists under the assumption that the maximum marginal contribution of each item is 1". — [arXiv 2105.01801](https://arxiv.org/abs/2105.01801)
- **Truthful approximation (Caragiannis–Ioannidis).** By Myerson's characterization, for truthful algorithms "no approximation guarantee better than n − 1 is possible". The instance is a single item with one agent valuing it 1 and the rest 0; truthfulness forces subsidies n − 1 although an EF allocation exists. — [Caragiannis & Ioannidis, arXiv 2002.02789 (WINE 2021; PR)](https://arxiv.org/abs/2002.02789)
- **Technique lower bound (discrepancy).** Dupré la Tour–Fujii, Proposition 1: "For every k ≥ 2, there exists a collection of n (additive) valuation functions with k-color transfer-discrepancy at least Ω(√n)" (via Manurangsi–Meka). — [arXiv 2509.16802](https://arxiv.org/abs/2509.16802)
- **Restricted model, graph orientations (goods):**
  - Additive: subsidy n/2 is "necessary and sufficient" (Example 10, Theorem 11).
  - Simple graph, monotone: lower bound n − 2 (Example 20, Boolean-type valuations) with a matching upper bound (Theorem 21).
  - Multigraph, monotone: n − 1 upper bound (Theorem 9).
  
  — [arXiv 2502.13671](https://arxiv.org/abs/2502.13671)
- **Restricted model, house allocation with binary utilities:** "a total subsidy of at most (n − 1) suffices to guarantee envy-freeness in house allocation, and this bound is tight." — [arXiv 2608.22216](https://arxiv.org/abs/2608.22216)
- **Tightness of Barman et al.'s bound** comes from the same single good: "(n − 1) agents would each require a subsidy of 1." — [arXiv 2201.07419](https://arxiv.org/abs/2201.07419)

### Inferences
- **A counterexample would be significant on its own.** Suppose some {−1,0,1}-marginal instance (n ≥ 3) forced total > n−1, or forced some agent's subsidy > 1 in every envy-freeable allocation. That would be, as far as these sources show, the first instance in any class with marginals in [−1,1] beating the single-good lower bound. A negative answer to the target question would therefore be a notable result, not a routine one.
- **Routes that are ruled out.** Any unit-subsidy proof for the target class must avoid:
  - Arbitrary EF1 allocations, which can need n−1 per agent (Kawase Ex. 1; LMS).
  - Insisting on utilitarian optimality, which can force m−ε per agent (Goko Thm 4.2). That instance is non-binary, so this barrier may not apply to {−1,0,1}.
  - Requiring truthfulness, completeness and Lorenz dominance together (Goko Thm 3.19 holds even for binary additive goods).
  - Pure discrepancy rounding, which loses Ω(√n) per agent in general.
- **Allocation choice matters for the guarantee, not the input class.** Halpern–Shah Theorem 3 shows binary identical valuations already force (n−1)m for a bad envy-freeable allocation.

### Gaps
- I found no source exhibiting an instance (allocation chosen optimally, marginals in [−1,1], any sign pattern) where every envy-freeable allocation needs some agent's subsidy > 1. LMS state that a constant per-agent bound "is open even in the goods-only setting" for submodular/XOS ([arXiv 2607.10089](https://arxiv.org/abs/2607.10089)). So per-agent lower bounds beyond 1 are simply unknown, not refuted.
- Weighted envy-freeness with subsidy (e.g., Aziz et al., arXiv 2408.08711; Elmalem et al. 2025), which reportedly has "important differences from the unweighted case", was not examined. It is a different fairness notion.

## Impossibility and non-existence: EF1/EFX for non-monotone and mixed valuations, EF1 + envy-freeability, subsidies vs PO / utilitarian optimality / truthfulness

### Takeaway
- **EF1:** existence for **n ≥ 3 agents with arbitrary (non-doubly-monotone) valuations is still open as of Aug 2026**, even for identical valuations. *Balanced* EF1 can fail for three agents with identical non-monotone valuations.
- **EFX:** fails in many mixed and chore settings: two-agent non-monotone identical valuations; objective goods and chores under lexicographic additive utilities; binary XOS and binary supermodular chores (Lin–Liu–Tao–Zhou 2026). Binary submodular chores remain open.
- **EF1 together with envy-freeability:** known for additive mixed manna. Open for doubly monotone valuations, even for goods.
- **Subsidies versus efficiency and incentives:** EF with utilitarian optimality can cost m−ε per agent (additive, non-binary). Truthful, envy-free and utilitarian optimal mechanisms are impossible for monotone submodular valuations. For binary goods, PO or utilitarian optimality *is* compatible with unit subsidies.

### Cited Findings
- **Liu et al., Open Question 1, verbatim:** "For three (or more) agents with arbitrary utility functions over mixed indivisible goods and chores, does there always exist an EF1 allocation? This question remains open even if agents have identical utility functions." — [arXiv 2306.09564](https://arxiv.org/abs/2306.09564)
- **Bérczi et al. found a flaw in an earlier EF1 claim.** The generalized envy-graph algorithm of Aziz et al. is not EF1 even for identical utilities; counterexample u(1) = 1, u(2) = u(3) = −1, all pairs = 1, u(123) = 1. "thus the existence of an EF1 allocation in the non-monotone, non-additive setting is still open even for identical utility functions." — [arXiv 2006.04428](https://arxiv.org/abs/2006.04428)
- **Shah–Verma, Table 2 (30 Aug 2026):** "Arbitrary valuations EF1+− Open" and "Nonnegative (nonmonotone) valuations EF1+− Open".
- **Shah–Verma, Theorem 1:** "Every instance with arbitrary valuations v_i : 2^M → {0, 1} admits a complete EF1 allocation." They also resolve Bérczi et al.'s "Question 16" (TCS numbering): EFX^+_0 exists for non-identical negative-Boolean valuations. Their Theorem 4 counterexample has two agents, three items and the identical valuation v(S) = 1 iff |S| ≤ 1 (so v(∅) = 1); it admits no EFX^0_− allocation. — [Shah & Verma, arXiv 2608.29497 (PP)](https://arxiv.org/abs/2608.29497)
- **Dupré la Tour (Aug 2026):** "For three or more agents, the existence of this EF1 notion for general nonmonotone valuations is open even without a balance constraint (Bérczi et al., 2024; Bhaskar et al., 2021, 2025; Bilò et al., 2026)."
  - Theorem 2, verbatim: "There exists an instance with three agents and an identical valuation over nine items that admits no balanced EF1 allocation."
  - Positive side: "Bilò et al. (2026) prove the existence of EF1^c_g under arbitrary nonnegative or arbitrary nonpositive valuations. For arbitrary valuations and a prime-power number of agents, Dupré la Tour and Igarashi (2026) obtain EF1^c_g".
  
  — [arXiv 2608.09437](https://arxiv.org/abs/2608.09437)
- **EF1 for doubly monotone valuations (Bhaskar–Sricharan–Vaish).** A modified top-trading envy-cycle elimination gives EF1 for doubly monotone instances (Theorem 4). Naive envy-cycle elimination "could fail to find an EF1 allocation even when agents have additive valuations" for chores (Example 1). — [Bhaskar et al., arXiv 2012.06788 (APPROX/RANDOM 2021; PR)](https://arxiv.org/abs/2012.06788)
- **EFX non-existence for mixed items (Bérczi et al., Theorem 2):** "There need not exist an EFX+− allocation for two agents with non-monotone, non-additive, identical utility functions." Counterexample: u(∅) = 0, u(1) = 1, u(2) = 2, u(3) = 0, u(12) = 3, u(13) = 0, u(23) = 3, u(123) = 4. — [arXiv 2006.04428](https://arxiv.org/abs/2006.04428)
- **EFX for additive tertiary utilities (Bérczi et al.):** "A utility function is tertiary if u(s) ∈ {−1, 0, +1} ... for tertiary utilities EF1 implies EFX, thus the Double Round Robin Algorithm ... provides such a solution". Aleksandrov–Walsh additionally give PO. — [arXiv 2006.04428](https://arxiv.org/abs/2006.04428)
- **EFX for objective mixed items (Liu et al. survey):**
  - "With additive utilities, EFX allocations do not always exist. This can be seen from an instance with a mixture of objective goods and chores and lexicographic preferences [Hosseini et al., 2023b]."
  - On the positive side, "ternary utilities of the form {α, 0, −β}" and "absolute identical utilities" admit polynomial-time EFX+PO.
  - "Cousins et al. [2023] ... restricting the possible marginal values to −1, 0, and c ... a leximin allocation can be computed efficiently; such an allocation, however, may not be EF1 even with two agents."
  
  — [arXiv 2306.09564](https://arxiv.org/abs/2306.09564)
- **Lin–Liu–Tao–Zhou (PP, 11 Aug 2026), binary-marginal chores.**
  - Theorem 1: "There is an instance with 18 agents and 53 chores in which every cost function is an XOS monotone function with binary marginals, but no complete EFX allocation exists. In addition, every cost function is the maximum of two binary additive functions in this instance."
  - Theorem 2: the same holds for "a supermodular monotone function with binary marginals ... the nullity function of a rank-two partition matroid".
  - Binary submodular costs are "the only unresolved class".
  
  — [Lin, Liu, Tao, Zhou, arXiv 2608.10572](https://arxiv.org/abs/2608.10572)
- **Context cited by Lin et al.** (secondary; I did not read the originals):
  - Tao et al. (TCS 2025): EFX+PO for binary additive chores; EFX for binary cancelable costs; 2-EFX for binary submodular costs; "an envy-free partial allocation with at most n − 1 unallocated chores for general binary-marginal costs".
  - Barman–Narayan–Verma (AAMAS 2023), binary supermodular costs: "allocations satisfying PO can fail every constant-factor EFX guarantee".
  - Goods side: Bu–Song–Yu (2023) prove EFX exists for all monotone valuations with binary marginals.
  - Christoforidis–Santorinaios (IJCAI 2024): a three-agent, six-chore superadditive instance with no EFX.
  - He–Tao (arXiv 2606.08872): no EFX for tri-valued additive chores.
  
  — [arXiv 2608.10572](https://arxiv.org/abs/2608.10572)
- **EF1 + envy-freeability for additive mixed manna (Aziz–Lu–Mackenzie–Suzuki), Theorem 4.2:** "With indivisible goods and chores, an EF1 and envy-freeable allocation always exists" (additive). Their example: two agents with identical u(g) = +1, u(c) = −1, where "The only way to achieve both EF1 and envy-freeability is to bundle the two items together". — [Aziz, Lu, Mackenzie, Suzuki, arXiv 2511.04891 (EC 2026, forthcoming per LMS; PR)](https://arxiv.org/abs/2511.04891)
- **The same question is open for doubly monotone valuations (ALMS Discussion):** "Is EF1 compatible with envy-freeability for doubly monotone instances? Note that the question is still open in the setting with only indivisible goods." — [arXiv 2511.04891](https://arxiv.org/abs/2511.04891)
- **LMS drop EF1 on purpose:** "In the mixed setting, especially after goods have been bundled with chores, requiring the allocation to remain EF1 is too restrictive and is incompatible with the operations used later in the proof. We therefore do not maintain EF1". This describes their technique; it is not an impossibility theorem. — [arXiv 2607.10089](https://arxiv.org/abs/2607.10089)
- **Barman et al. (dichotomous goods) output need not be EF1:** "we can, in fact, construct an instance wherein a specific execution of the developed algorithm returns an allocation that is not EF1". The instance in their Appendix C is binary submodular; the authors remark that Goko et al.'s algorithm would give EF1 there. — [arXiv 2201.07419](https://arxiv.org/abs/2201.07419)
- **EF1 + PO for mixed manna (Liu et al., Open Question 2):** "With mixed indivisible goods and chores, for three (or more) agents and additive utilities, does an EF1 and PO allocation always exist?" — [arXiv 2306.09564](https://arxiv.org/abs/2306.09564)
- **Barman–Prakash HV–Sethia–Suzuki:** for mixed manna "this problem is, in fact, open for three agents". They prove EFR-(n−1)+PO exists, and EFR-(n−2) can fail for chores while goods admit EFR-⌊n/2⌋ ("an interesting dichotomy between goods and chores"). — [Barman et al., arXiv 2507.03946 (WINE 2025; PR)](https://arxiv.org/abs/2507.03946)
- **Subsidies versus truthfulness and efficiency (Goko et al.):**
  - Theorem 5.1 (Feldman–Lai): "No mechanism satisfies truthfulness, envy-freeness, and utilitarian optimality, even when all agents have monotone submodular valuations."
  - Example 3.2 (two agents, one item, binary): truthful, envy-free and utilitarian-optimal mechanisms must subsidize "agents who want nothing".
  - Theorem 4.2 (EF + utilitarian optimality ⇒ m−ε per agent).
  
  — [arXiv 2105.01801](https://arxiv.org/abs/2105.01801)
- **Halpern–Shah on PO and binary goods:**
  - "Meertens et al. [22] ... show that envy-freeness and Pareto optimality may be incompatible regardless of the amount of money available. In contrast, in our setting with quasi-linear preferences, allocations that are both envy-free and Pareto optimal exist given a sufficient amount of money".
  - For binary goods: "non-wasteful is equivalent to Pareto efficiency. For binary valuations, it is easy to see that every non-wasteful allocation is envy-freeable".
  
  — [Halpern & Shah](https://www.cs.toronto.edu/~nisarg/papers/subsidy.pdf)
- **House allocation, binary utilities (Dai et al., Lemma 3.4):** a minimum-subsidy outcome with positive subsidy is a maximum-cardinality matching, "and A* is Pareto optimal". — [arXiv 2608.22216](https://arxiv.org/abs/2608.22216)

### Inferences
- **EF1 cannot be a stepping stone in the target class.** EF1 existence is open for n ≥ 3 non-doubly-monotone valuations, so a unit-subsidy proof for the general {−1,0,1} class cannot first obtain EF1 (the Kawase/Brustle route). Conversely, a unit-subsidy theorem need not yield EF1: LMS's output is not EF1, and Barman et al.'s dichotomous algorithm can output non-EF1.
- **The known non-monotone counterexamples lie outside {−1,0,1}.**
  - Bérczi's EFX counterexample has a marginal of +2 (u(2) = 2).
  - Their envy-graph counterexample has a marginal of +2 (u(12) − u(2) = 2).
  - Dupré la Tour's balanced-EF1 counterexample has a marginal of −2 (v drops from 2 to 0 between 3 and 4 items).
  
  So none of these directly constrains the {−1,0,1}-marginal class. Lin et al.'s instance *does* lie in the negative-binary class (costs with {0,1} marginals), but it concerns EFX without money.
- **Goods-versus-chores asymmetries under binary marginals:**
  - EFX: exists for goods (Bu et al.) but fails for binary XOS/supermodular chores (Lin et al.).
  - PO with unit subsidies: holds for binary additive goods (Halpern–Shah MNW) and matroid-rank goods (Goko: utilitarian optimal).
  
  The requester's claim that unit subsidies are incompatible with PO for identical binary submodular costs, if correct, is a genuine goods/chores separation. The closest external negative result is Barman–Narayan–Verma's PO-versus-approximate-EFX conflict for binary supermodular costs.
- **"Goods algorithms fail for chores" has precedents.** The requester's finding that Barman et al.'s incremental extension fails for chores matches documented precedents: Bhaskar et al.'s envy-cycle elimination failure for chores, the round-robin failure for mixed items (Liu et al. Example 4.1), and the EFR goods/chores dichotomy (Barman et al. 2025).

### Gaps
- I found no external paper on subsidies combined with PO for chores or for mixed manna (binary or not).
- No source states whether **EF1 + per-agent subsidy ≤ 1** is achievable for additive mixed manna. ALMS give EF1 + envy-freeable; LMS give subsidy ≤ 1 without EF1.
- No source states whether **utilitarian optimality (or PO) + unit subsidies** holds for general dichotomous (non-submodular) goods.
- I did not read Bhaskar–Kumar–Pandit–Rakshitha (AAMAS 2025) or Bilò–Loebl–Vinci (AAAI 2026) directly. Their results are known here only via Shah–Verma and Dupré la Tour.

## Hardness: computing the minimum subsidy (given allocation vs chosen allocation; binary and mixed classes)

### Takeaway
- **Given allocation:** minimum subsidy is polynomial-time (longest paths, Floyd–Warshall) for any valuation class with value-oracle access.
- **Chosen allocation:** minimizing subsidy (SMEF) is NP-hard because deciding whether zero subsidy suffices is deciding EF existence. This is already NP-complete for binary additive goods and **strongly NP-complete for binary additive chores {−1,0}**. Hence no multiplicative approximation is possible. Additive approximation within 3·10⁻⁴·Σv is NP-hard; constant-n instances admit an FPTAS-style algorithm.
- **Restricted models:** orientations are NP-hard for {1,2}-valued additive valuations but polynomial for {0,1}. House allocation with binary utilities is NP-complete and conditionally Ω(n^{1/4})-inapproximable.

### Cited Findings
- **Fixed allocation (Halpern–Shah):**
  - Proposition 1: envy-freeability can be checked "in O(mn + n³) time".
  - Theorem 2: p*(A) computable in O(nm + n³) via Floyd–Warshall on negated weights.
  
  — [Halpern & Shah](https://www.cs.toronto.edu/~nisarg/papers/subsidy.pdf)
- **Fixed allocation, general valuations (Kawase et al.):** "The maximum weight permutation can be computed in polynomial time via a maximum-weight bipartite perfect matching algorithm. The minimum subsidy vector for w can be computed in polynomial time via the Floyd–Warshall algorithm". The minimum subsidy vector does not depend on which maximum-weight permutation is used (Lemma 2). — [arXiv 2308.11230](https://arxiv.org/abs/2308.11230)
- **Chosen allocation (Halpern–Shah):**
  - "When we are allowed to choose the allocation, computing the minimum subsidy required is NP-hard. This is because checking whether zero subsidy is required is equivalent to checking whether an envy-free allocation exists, which is NP-hard even for identical valuations [9]."
  - Proposition 2: "For binary valuations, the problems of computing the minimum subsidy required and checking the existence of an envy-free allocation are Turing-equivalent."
  - Corollary 1: "For binary valuations, it is NP-hard to compute the minimum subsidy required to achieve envy-freeness using a non-wasteful allocation."
  - Proposition 3: for identical valuations, minimizing subsidy is NP-hard (multiprocessor scheduling).
  - At the time they wrote: "it is an open question whether existence of an envy-free allocation can be checked efficiently for binary valuations."
  
  — [Halpern & Shah](https://www.cs.toronto.edu/~nisarg/papers/subsidy.pdf)
- **Binary chores (Bhaskar–Sricharan–Vaish):** "determining whether an envy-free allocation of chores exists is strongly NP-complete, even in the highly restricted setting when agents have binary additive valuations, i.e., when for all agents i ∈ [n] and items j ∈ [m], v_{i,j} ∈ {−1, 0} (Theorem 2). The analogous problem for indivisible goods with binary valuations is already known to be NP-complete [13, 49]." [13, 49] are Aziz–Gaspers–Mackenzie–Walsh (AIJ 2015) and Hosseini et al. (AAAI 2020). The reduction is from Set Splitting. — [arXiv 2012.06788](https://arxiv.org/abs/2012.06788)
- **Caragiannis–Ioannidis:**
  - "SMEF is NP-hard; this follows by the NP-hardness of deciding whether a given allocation problem has an envy-free allocation or not." Folklore: two identical agents encode Partition.
  - "it is NP-hard to decide whether the minimum amount of subsidies is zero or not". Hence multiplicative approximation is hopeless.
  - Theorem 6: "Approximating SMEF within an additive term of 3 · 10^{−4} sum v is NP-hard." The reduction is from bounded MAX-3DM, with item values in {0, χ, 3χ, χK} (not binary).
  - Theorem 5 (constant n): time O((m/ε)^{n²+2}) with subsidy ≤ χ + ε·max v.
  - Footnote 2: "our positive result can be extended to work without this assumption, in the model of Aziz et al. [2019] where items can be goods or chores."
  
  — [arXiv 2002.02789](https://arxiv.org/abs/2002.02789)
- **Liu et al. survey summary:** "This problem is NP-hard since deciding whether an envy-free allocation exists for a given fair division instance is NP-hard. The same argument shows that it is NP-hard to approximate the minimum subsidy to any multiplicative factor." — [arXiv 2306.09564](https://arxiv.org/abs/2306.09564)
- **Amanatidis et al. AIJ survey:** "finding the envy-freeable allocation with overall minimum total subsidy is an NP-hard problem; this follows since deciding the existence of an envy-free allocation without any subsidy is ... NP-hard [Bouveret and Lang, 2008]." — [Amanatidis et al., arXiv 2208.08782 (AIJ 322:103965, 2023; PR)](https://arxiv.org/abs/2208.08782)
- **Orientations (Li–Sun–Suzuki–Xing):**
  - Theorem 2: "Computing an orientation with the minimum subsidy is the NP-hard, even when the graph is simple and the valuations are additive and v_i(e) ∈ {1, 2}" ("it is NP-hard to differentiate between zero subsidy and a positive subsidy").
  - Theorem 4: binary additive {0,1} is polynomial; the minimum subsidy equals the number of components failing properties (P1)–(P4).
  
  — [arXiv 2502.13671](https://arxiv.org/abs/2502.13671)
- **House allocation (Dai–Li–Wu–Zhang).** Theorem 3.5: deciding whether Σp_i ≤ γ is achievable "is NP-complete even when all agents have binary utilities". This is a reduction from Minimum k-Union. It yields Ω(n^{1/4})-approximation hardness under the "Dense versus Random" conjecture, and FPT in the number of agent types. — [arXiv 2608.22216](https://arxiv.org/abs/2608.22216)
- **Recent existence results are non-constructive:**
  - Dupré la Tour–Suzuki: the "KKM argument establishes the existence of an equalizing point x* but does not provide a polynomial-time procedure for finding it."
  - Dupré la Tour (three agents): "Dold's theorem does not provide an efficient method ... We therefore leave open whether the guaranteed allocations can be found in polynomial time".
  
  — [arXiv 2609.08272](https://arxiv.org/abs/2609.08272); [arXiv 2608.09437](https://arxiv.org/abs/2608.09437)
- **Barman et al. (WINE 2025):** "deciding whether a given allocation is EFR-k is NP-hard" (tangential). — [arXiv 2507.03946](https://arxiv.org/abs/2507.03946)

### Inferences
- **The polynomial-time goal must be the worst-case bound.** The target class contains binary additive chores ({−1,0}) and binary additive goods ({0,1}). Deciding whether the minimum subsidy is 0 is therefore NP-hard (strongly NP-hard on the chore side) within the class. "Polynomial time" can only mean achieving the worst-case unit/(n−1) bound, not the instance-optimal subsidy, and the optimum cannot be approximated multiplicatively unless P = NP.
- **Hardness needs n as part of the input (additive case).** For constant n and additive integer-valued instances, including mixed signs per CI's footnote, run Caragiannis–Ioannidis's dynamic program with ε < 1/max v (e.g., ε = 1/(2m)). It returns subsidy < χ + 1, and since subsidies are integral here, it returns exactly χ in time O((2m²)^{n²+2}). This is my derivation, not stated by the authors.
- **Binary utilities do not uniformly make minimum-subsidy computation easy.** They help in orientations ({0,1} is polynomial) but not in house allocation (NP-hard, conditionally Ω(n^{1/4})-inapproximable).

### Gaps
- No source addresses the complexity of the minimum subsidy, or of computing any unit-subsidy allocation, for **non-additive** {−1,0,1}-marginal valuations in the value-oracle model (beyond Barman et al.'s polynomial algorithm for {0,1} goods).
- I did not obtain the Aziz–Gaspers–Mackenzie–Walsh (2015) or Hosseini et al. (2020) proofs directly; the binary-goods EF-existence NP-completeness is taken from Bhaskar et al.'s citation.

## Explicitly stated open problems (verbatim, with source and number)

### Takeaway
- The canonical subsidy open problem is **Liu et al. JAIR Open Question 9** (subquadratic total subsidy for monotone utilities). As of Sep 2026 it is answered existentially, in preprints only:
  - Dupré la Tour–Fujii, for prime-power n with arbitrary signs.
  - Dupré la Tour–Suzuki, for all n when every bundle value is nonnegative, or every bundle value is nonpositive.
- Remaining stated questions:
  - A linear bound, and polynomial-time computation.
  - Mixed-sign valuations for every n.
  - Constant per-agent subsidy for submodular/XOS valuations (open even for goods).
  - EF1 + envy-freeability for doubly monotone valuations.
  - EF1 existence for n ≥ 3 with arbitrary valuations.
- No surveyed survey poses an open question specifically about subsidies with chores, mixed items, or binary valuations. The JAIR survey's subsidy section is goods-only. The AIJ survey has no numbered subsidy problem.

### Cited Findings
- **Liu–Lu–Suzuki–Walsh, JAIR 2024 (arXiv v4).** The subsidy section is titled "6 Indivisible Goods with Subsidy" and is goods-only.
  - **Open Question 9:** "For monotonic utilities, does there exist an envy-free allocation whose total subsidy is O(n^{2−ε}) for some ε > 0?"
  - Context sentence: "As there are no lower bounds known beyond the aforementioned n − 1 bound, this leads to a natural question."
  - Footnote 16: "Kawase et al. [2024a]'s result works for doubly-monotonic utilities."
  - Closing questions of Section 6: "Can subsidy payments be used to find fair allocations for problems with externalities?"; "Exploring other fairness notions (e.g., MMS and AnyPrice share ...) using subsidy payments is an intriguing direction for future research."
  - **Open Question 1:** "For three (or more) agents with arbitrary utility functions over mixed indivisible goods and chores, does there always exist an EF1 allocation? This question remains open even if agents have identical utility functions."
  - **Open Question 2:** "With mixed indivisible goods and chores, for three (or more) agents and additive utilities, does an EF1 and PO allocation always exist? Recall that this question remains open even in the indivisible-chores setting."
  - **Open Question 3:** "Are there other natural subclasses of additive utilities over mixed indivisible goods and chores that always admit an EFX allocation? Or even an EFX and PO allocation?"
  
  — [arXiv 2306.09564](https://arxiv.org/abs/2306.09564)
- **Note on Open Question 7 of Liu et al.** (EFM existence for indivisible chores plus cake) is reported resolved by Aziz–Lu–Mackenzie–Suzuki: "The problem has again been highlighted in the survey paper by Liu et al. [40, Open Question 7]". — [arXiv 2511.04891](https://arxiv.org/abs/2511.04891)
- **Lu–Mackenzie–Suzuki 2026, §6 Discussion:** "This raises the following questions: for mixed goods and chores with bounded marginal values, does a constant per-agent subsidy bound still hold for submodular or XOS valuations? Note that this question is open even in the goods-only setting." — [arXiv 2607.10089](https://arxiv.org/abs/2607.10089)
- **Dupré la Tour–Fujii 2025.** They restate the survey question as their own "Open Question 1 ([Liu+24]). Given n monotone valuations with marginals in [−1, 1], is there an envy-free allocation with sub-quadratic total subsidy?" This is their paraphrase, citing the AAAI 2024 version of the survey. Conclusion, verbatim: "A natural question is whether our bound can be extended to all values of k, beyond prime powers. Additionally, there remains a small √log(nk) gap between the upper and lower bounds. Can this gap be closed? Even in the case k = 2, it is unclear whether the extra √log n factor is inherent". On necklace splitting beyond prime powers: "it remains open even without the extra requirement that each bundle contain at most n pieces." — [arXiv 2509.16802](https://arxiv.org/abs/2509.16802)
- **Dupré la Tour–Suzuki 2026, §6 Discussion:**
  - "Beyond the sign assumption. ... Extending our approach to mixed-sign valuations for every number of agents therefore calls for an alternative way to equalize expected prices."
  - "Closing the gap. ... Can a different rounding argument remove this factor? More broadly, does a linear total-subsidy bound hold for general monotone valuations?"
  - "Efficient computation. A further question is whether our total-subsidy bound of O(n^{3/2}√log n) can be achieved by a polynomial-time algorithm."
  - They also state that a careful accounting gives (n−1)√((2n+3) log n), and (n−1)√(((n+5)/2) log n) for monotone goods or chores.
  
  — [arXiv 2609.08272](https://arxiv.org/abs/2609.08272)
- **Kawase et al. (AAAI 2024; read arXiv v1).** There is no separate open-problems section. The introduction says: "it remains an open question whether we can improve on the total subsidy bound of 2(n − 1)² for monotone valuations, as mentioned in a recent survey paper [18, Open Question 9]." — [arXiv 2308.11230](https://arxiv.org/abs/2308.11230)
- **Barman–Krishna–Narahari–Sadhukhan (IJCAI 2022), §5:** "extending the current work to additionally obtain the EF1 guarantee is a relevant direction of future work. Another interesting direction would be to obtain tight subsidy bounds for general monotone valuations." — [arXiv 2201.07419](https://arxiv.org/abs/2201.07419)
- **Goko et al. (GEB 2024; read arXiv v1), §6:**
  - "An obvious direction would be to study whether the amount of m is necessary to achieve a truthful, envy-free, and complete mechanism when agents have additive valuations, assuming that the maximum value of each item is 1."
  - "for general monotone valuations beyond matroidal and additive valuations, it remains an open question as to what is the asymptotically minimal amount of subsidies required to make some allocation envy-free. Brustle et al. [8] showed ... 2(n − 1) for each agent ...; however, it is unclear whether this bound is tight."
  
  — [arXiv 2105.01801](https://arxiv.org/abs/2105.01801)
- **Halpern–Shah (SAGT 2019), §4.2 and §6:**
  - "Conjecture 1. There always exists an envy-freeable allocation that is envy-free up to one good."
  - "Conjecture 2. There always exists an envy-freeable allocation which requires at most n − 1 subsidy."
  - "In fact, it may be possible that a subsidy of at most n − 1 can always be achieved through an envy-freeable EF1 allocation."
  - Discussion: "Perhaps the most immediate question is to settle our two conjectures ... Settling the complexity of checking the existence of an envy-free allocation for binary valuations is also an important open question. Finally, it would be interesting to extend this framework to non-additive valuations."
  - Also: "It would be interesting to study other natural objective functions (e.g., minimizing the number of agents that have a non-zero payment) in such models."
  - Status: both conjectures were proved for additive goods by Brustle et al., and binary EF existence is NP-complete per Bhaskar et al.'s citations.
  
  — [Halpern & Shah](https://www.cs.toronto.edu/~nisarg/papers/subsidy.pdf); [Brustle et al.](https://arxiv.org/abs/1912.02797); [Bhaskar et al.](https://arxiv.org/abs/2012.06788)
- **Brustle et al. (EC 2020; read arXiv v1).** There is no conclusion or open-problems section. They restate Halpern–Shah's conjectures as "Conjecture 1.1. [11] For additive valuations, there is an envy-freeable allocation that requires a total subsidy of at most n − 1 dollars." and "Conjecture 1.2. [11] For additive valuations, there is an envy-freeable allocation that is EF1." Both are settled for additive goods (Theorem 1.3). — [arXiv 1912.02797](https://arxiv.org/abs/1912.02797)
- **Caragiannis–Ioannidis (WINE 2021), §5:**
  - "The challenging open problem that deserves investigation is to close the gap between the trivial approximation guarantee of n − 1 in Section 2 and our negative result for super-constant numbers of agents in Section 4."
  - "What is the best possible approximation guarantee that can be obtained for SMEF by truthful algorithms?" They answer this with an n−1 lower bound.
  
  — [arXiv 2002.02789](https://arxiv.org/abs/2002.02789)
- **Amanatidis et al. AIJ 2023.** §8.7 "Subsidies" contains no numbered open problem. §8.9: "It is an intriguing future research direction to study the fair allocation problem under other non-monotonic valuations." — [arXiv 2208.08782](https://arxiv.org/abs/2208.08782)
- **Aziz–Lu–Mackenzie–Suzuki (EC 2026), §5:** "Does an EFM allocation always exist for agents with doubly monotone valuations over indivisible items? Is EF1 compatible with envy-freeability for doubly monotone instances? Note that the question is still open in the setting with only indivisible goods." — [arXiv 2511.04891](https://arxiv.org/abs/2511.04891)
- **Bérczi et al. (arXiv v1 numbering; the TCS version renumbers, e.g., a "Question 16" cited by Shah–Verma):**
  - "Question 12. Does there always exist an EF1 allocation for non-monotone, non-additive, identical utility functions?"
  - "Question 13. Does there always exist an EFX+− allocation for monotone, additive, non-identical utility functions?"
  
  — [arXiv 2006.04428](https://arxiv.org/abs/2006.04428)
- **Lin–Liu–Tao–Zhou 2026, §4:** "For the future direction, it would be interesting to explore the existence of EFX allocations for binary submodular cost functions." — [arXiv 2608.10572](https://arxiv.org/abs/2608.10572)
- **Li–Sun–Suzuki–Xing 2025, §7:** "we have been focusing on the allocation of goods and the mirror problem of chores/mixed manna has not been studied yet. Finally, the optimal bound of subsidy in the unrestricted setting ... when agents have arbitrary monotone valuations ... remains unknown." — [arXiv 2502.13671](https://arxiv.org/abs/2502.13671)
- **Dupré la Tour 2026 (three agents), §7:** "We therefore leave open whether the guaranteed allocations can be found in polynomial time, for example in the value-oracle model. Extending the balanced result beyond three agents appears to require new ideas." — [arXiv 2608.09437](https://arxiv.org/abs/2608.09437)
- **Dai–Li–Wu–Zhang 2026, §6:** "One natural direction is to extend our results to general utilities with more than two agent types. ... Other interesting directions include considering additional fairness notions with subsidies, such as proportionality or maximin share guarantees." — [arXiv 2608.22216](https://arxiv.org/abs/2608.22216)

### Inferences
- **The target question is not on any published open-problem list.** The question "unit subsidies for {−1,0,1} marginals with mixed signs" sits in the intersection of:
  - Liu OQ9 (goods-only; now subquadratic existentially),
  - LMS's §6 question (constant per-agent subsidy beyond additive, open even for goods), and
  - the ALMS doubly-monotone question.
  
  The requester can therefore frame it as a binary-marginal special case of the LMS question that is *beyond* additivity yet *within* reach. Barman et al. (dichotomous goods) is the goods-side precedent.
- **Unit subsidies in the target class would answer DlT–Suzuki's linear-bound question for that class.** A unit-subsidy result for general {−1,0,1} marginals would give a linear (n−1) total bound there, answering DlT–Suzuki's "does a linear total-subsidy bound hold" restricted to binary marginals and extending it to mixed signs. That is the case they flag as needing a new idea.

### Gaps
- I read arXiv versions of Kawase (v1, 2023), Goko (v1, 2021), Brustle (v1, 2019) and Bérczi (v1, 2020). The journal versions (AIJ 2025, GEB 2024, EC 2020, TCS 2024) may contain different or additional open problems; I could not verify them.
- The AAAI 2024 conference version of the Liu et al. survey uses different question numbering. Dupré la Tour–Fujii's "Open Question 1" refers to it, while the JAIR version numbers the same topic OQ9.

## Separations between objective (common sign per item) and subjective (agent-specific sign) mixed instances

### Takeaway
I found **no theorem separating objective from subjective mixed instances in the subsidy literature**. For additive utilities the optimal per-agent bound is 1 in both cases (LMS), and proportional-subsidy bounds also coincide with goods-only. Differences exist only in **what is known** for non-additive valuations:
- doubly monotone (subjective but item-wise consistent) versus non-doubly-monotone;
- sign-uniform bundle values (DlT–Suzuki) versus mixed signs.

In proof structure, LMS treat "subjective goods only" and "objective chores only" directly by iterated matchings, and need bundling for the general mix. In other fairness questions, objective mixing already breaks EFX (lexicographic, additive). The documented separations are **goods versus chores**, not objective versus subjective.

### Cited Findings
- **LMS definitions:** "An item j ∈ M is a subjective good if u_i(j) ≥ 0 for some i ∈ N. An item j ∈ M is an objective good (resp., objective chore) if u_i(j) ≥ 0 (resp., u_i(j) < 0) for all agents i ∈ N."
- **LMS on why mixing is hard:** "Existing arguments for goods exploit that every item is weakly beneficial, while analyses for chores rely on all items being weakly harmful; both assumptions fail when an item can be a good for one agent and a chore for another."
- **LMS proof structure:**
  - Proposition 3.1: subjective-goods-only instances (utilities in (−∞,1]) are handled by IMWM with p_i ≤ 1.
  - Proposition 3.2: objective-chores-only instances are handled by IMWPM.
  - The general case branches on |Z_rem| = 0, 0 < |Z_rem| < |G|, |Z_rem| ≥ |G| (meta-goods versus remaining objective chores).
  - Theorem 1.1 gives the same bound of 1 in all cases.
  
  — [arXiv 2607.10089](https://arxiv.org/abs/2607.10089)
- **Proportionality with subsidy (LMS's summary of Wu–Xue–Zhou 2025b):** in the fully mixed setting, total subsidy n/4 (n even) and (n²−1)/(4n) (n odd) suffice for proportionality, and "both bounds are tight [Wu et al., 2023]". These are the same bounds as for goods or chores. — [arXiv 2607.10089](https://arxiv.org/abs/2607.10089)
- **Liu et al. survey definitions and EFX:** "agents have subjective opinions on whether the item is a good or a chore. An item is said to be an objective good (resp., objective chore) if the item is a good (resp., chore) for all agents." EFX can fail with "a mixture of objective goods and chores and lexicographic preferences [Hosseini et al., 2023b]". — [arXiv 2306.09564](https://arxiv.org/abs/2306.09564)
- **ALMS on the same EFX result:** EFX may not exist "even with objective goods and chores and under lexicographic preferences—a subclass of additive utilities". — [arXiv 2511.04891](https://arxiv.org/abs/2511.04891)
- **Doubly monotone instances (Bhaskar et al.):** "each agent i can partition the items as M = G_i ⊎ C_i ... Note that an item may be a good for one agent and a chore for another." EF1 exists for this class (agent-specific signs allowed). — [arXiv 2012.06788](https://arxiv.org/abs/2012.06788)
- **Kawase et al.'s quadratic subsidy bound** covers exactly this doubly monotone (subjective, item-wise consistent) class. Beyond it, only n = 2 is covered. — [arXiv 2308.11230](https://arxiv.org/abs/2308.11230)
- **Dupré la Tour–Suzuki's sign condition** is global over agents and bundles: "either v_i(S) ≥ 0 for every i, S, or v_i(S) ≤ 0 for every i, S". The sign assumption "enters our proof only through the empty-bundle boundary condition". — [arXiv 2609.08272](https://arxiv.org/abs/2609.08272)
- **Goods-versus-chores dichotomies documented elsewhere:**
  - EFR: goods admit EFR-⌊n/2⌋, chores need n−1 ("an interesting dichotomy between goods and chores"). — [arXiv 2507.03946](https://arxiv.org/abs/2507.03946)
  - EFX under binary marginals: exists for goods (Bu et al.), fails for binary XOS/supermodular chores. — [arXiv 2608.10572](https://arxiv.org/abs/2608.10572)

### Inferences
- **Any objective/subjective separation in the target class would have to come from non-additivity.** For additive {−1,0,1} instances there is no subsidy separation (LMS gives 1 per agent either way).
- **The requester's case split mirrors LMS's additive one.** "Objective signed dichotomous" sits inside the doubly monotone class (each item has a common sign, so it is a good or a chore for every agent). The next natural steps are:
  1. subjective but doubly monotone {−1,0,1}-marginal valuations, where Kawase's n(n−1)/2 is the best known bound;
  2. then non-doubly-monotone valuations, where EF1 itself is open.

### Gaps
- No paper found that proves a lower bound (subsidy or otherwise) holding for subjective-sign instances but failing for objective-sign instances with the same valuation class, or vice versa.
- I did not examine the "Best-of-Both-Worlds Fairness for Mixed Goods and Chores" preprint (arXiv 2607.10232) or "Tight Subsidy Bounds for Weighted Proportional Allocation of Mixed Manna" (arXiv 2609.15208). They appeared in searches and might contain objective/subjective case distinctions.
