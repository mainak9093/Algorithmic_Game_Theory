# Upper bounds and algorithms for envy-freeness with subsidies when items are goods for some agents and chores for others (mixed manna), focusing on binary marginals

*Scope and conventions. Literature status as of 2026-10-02. arXiv 2609.14465 is the requester's own paper and is NOT treated as prior work anywhere below. "Per-agent" means max_i p_i and "total" means Σ_i p_i. Subsidies are always p ≥ 0, and (A,p) is envy-free (EF) iff v_i(A_i)+p_i ≥ v_i(A_j)+p_j for all i,j. Unless a row says otherwise, marginals are normalized to |v_i(S∪{g})−v_i(S)| ≤ 1. Every paper is tagged PEER-REVIEWED or PREPRINT. When a result is cited only through another paper, it is marked "(secondary)".*

---

## Q1. What exactly do Lu, Mackenzie and Suzuki prove in "Optimal Subsidy Bounds for Goods and Chores: One Dollar Each Suffices" (arXiv 2607.10089, 2026)?

### Takeaway
- **Setting:** additive utilities, each item value in [−1,1], and subjective signs, meaning an item can be a good for some agents and a chore for others.
- **Bound:** at most $1 per agent always suffices, so the total is at most n−1. The bound is tight, and the allocation is computable in polynomial time.
- **Status:** PREPRINT. Only v1 exists (11 Jul 2026), with no comments field and no journal-ref.
- **Limits:** the paper is additive-only. It says its technique does not extend beyond additivity, and it poses submodular/XOS as an open question. It has no result specific to binary or dichotomous valuations, and it deliberately gives up EF1.

### Cited Findings
- **Status.** arXiv:2607.10089 [cs.GT] by Xinhang Lu (Kyushu), Simon Mackenzie (UNSW) and Mashbat Suzuki (UNSW). The only version is v1, 11 Jul 2026, with no Comments or Journal-ref field. This makes it a PREPRINT. — [arXiv abs](https://arxiv.org/abs/2607.10089)
- **Model.** Utilities are additive: u_i(S)=Σ_{j∈S} u_i(j), with "the standard normalization that u_i(j) ∈ [−1, 1] ∀ i ∈ N, ∀ j ∈ M".
  - An item j is a **subjective good** if u_i(j) ≥ 0 for some i.
  - It is an **objective good** (resp. **objective chore**) if u_i(j) ≥ 0 (resp. u_i(j) < 0) for all agents.
  - For computational claims, item values are rationals encoded in binary.
  - [Lu–Mackenzie–Suzuki](https://arxiv.org/abs/2607.10089)
- **Theorem 1.1 (verbatim):** "For every instance with additive utilities u_i : M → [−1, 1], where each item may be a good for some agents and a chore for others, there exists an envy-free outcome (A, p) such that 0 ≤ p_i ≤ 1 for all i ∈ N. Furthermore, such an allocation can be computed in polynomial time." — [Lu–Mackenzie–Suzuki](https://arxiv.org/abs/2607.10089)
- **Tightness and total bound.**
  - Tightness: "The per-agent bound in Theorem 1.1 is optimal: even in the goods-only setting, some instances require a subsidy of 1 for at least one agent [Brustle et al., 2020]."
  - Total: "we can uniformly decrease agents' payments until one agent's payment reaches 0 … a total subsidy of at most n − 1 dollars suffices."
  - [Lu–Mackenzie–Suzuki](https://arxiv.org/abs/2607.10089)
- **Envy-freeability criterion.** The Halpern–Shah characterization is restated as Theorem 2.2: an allocation is envy-freeable ⇔ it is welfare-maximal over all permutations of its bundles ⇔ its envy graph has no positive-weight cycle. The authors note that it "also works for the setting with mixed goods and chores". Minimal payments are given by longest paths, so it suffices to build an allocation in which every envy path has weight ≤ 1. — [Lu–Mackenzie–Suzuki](https://arxiv.org/abs/2607.10089)
- **Building blocks for special cases (Section 3).**
  - Iterated maximum-weight matching (IMWM) and iterated maximum-weight perfect matching (IMWPM) give path bounds "not only for objective goods (recovering the result of Brustle et al. [2020] with a much simpler proof), but also for subjective-goods and objective-chores instances".
  - **Proposition 3.2 (verbatim):** "Suppose that every item g ∈ M is an objective chore and that, for every agent i ∈ N, the utility satisfies u_i(g) ≥ −1. Then, IMWPM produces an envy-free allocation (A, p) such that 0 ≤ p_i ≤ 1 for all i ∈ N."
  - [Lu–Mackenzie–Suzuki](https://arxiv.org/abs/2607.10089)
- **Proof structure (Section 4).**
  - Items are first bundled into objective chores Z_rem and subjective meta-goods G. Each meta-good is required to have value at most one: "Without it, even a two-agent instance containing a single meta-good may require a subsidy strictly greater than one."
  - **Case I**, |Z_rem| = 0: IMWM is applied directly.
  - **Case II**, 0 < |Z_rem| < |G|: an incremental active-set construction using an equality graph and payment reduction. Theorem 4.7: "Under Case II, there exists a polynomial-time algorithm that computes an envy-free allocation with subsidies, where each agent receives at most one dollar."
  - **Case III**, |Z_rem| ≥ |G|: the instance is reduced to objective chores and solved with IMWPM. Lemma 4.12 gives 0 ≤ p*_i ≤ 1.
  - Polynomial time: Section 5 / Proposition 5.2 use a flow computation with integral optimum, plus a longest-path computation.
  - [Lu–Mackenzie–Suzuki](https://arxiv.org/abs/2607.10089)
- **EF1 is deliberately dropped.**
  - They start from Aziz et al. (EC 2026), who show that "every instance of indivisible mixed manna admits an allocation that is both EF1 and envy-freeable".
  - They then note that this "do[es] not imply a tight subsidy bound. Even in goods-only instances, an allocation may be both EF1 and envy-freeable while its heaviest envy path has weight n − 1."
  - Their resolution: "requiring the allocation to remain EF1 is too restrictive and is incompatible with the operations used later in the proof. We therefore do not maintain EF1 and instead control the weights of envy paths directly."
  - [Lu–Mackenzie–Suzuki](https://arxiv.org/abs/2607.10089)
- **Extensions and open problems (Section 6, verbatim):** "Our techniques rely heavily on additivity both to define meta-goods and to obtain telescoping envy-path bounds from iterated matchings. This approach does not directly extend to richer valuation classes. This raises the following questions: for mixed goods and chores with bounded marginal values, does a constant per-agent subsidy bound still hold for submodular or XOS valuations? Note that this question is open even in the goods-only setting." There are no binary- or dichotomous-specific results. In related work, Barman et al. 2022, Goko et al. 2024 and Li et al. 2025 appear only as goods-side refinements. — [Lu–Mackenzie–Suzuki](https://arxiv.org/abs/2607.10089)
- **Related-work claims in the paper.**
  - Wu, Xue and Zhou (IJCAI 2025) "also concerned the same setting" (mixed manna) and showed that a total subsidy of n/4 (n even) or (n²−1)/(4n) (n odd) suffices for proportionality, and that these bounds are tight.
  - Most of the earlier subsidy literature "focuses on instances consisting entirely of goods or entirely of chores".
  - [Lu–Mackenzie–Suzuki](https://arxiv.org/abs/2607.10089)

### Inferences
- **Integral valuations give unit subsidies.** By Halpern–Shah, the minimal envy-eliminating vector for an envy-freeable allocation A is p*_i = ℓ_A(i), the heaviest path starting at i. This vector is coordinate-wise dominated by every envy-eliminating vector ([Barman et al., Thm 2 restating HS19](https://arxiv.org/abs/2201.07419)).
  - For additive u_i(j) ∈ {−1,0,1}, all envy-graph weights are integers, so p*_i ∈ ℤ_{≥0}.
  - Combined with Theorem 1.1's 0 ≤ p_i ≤ 1, this gives p* ∈ {0,1}^n. By minimality, min_i p*_i = 0, so Σp* ≤ n−1.
  - Computing p* takes polynomial time (Floyd–Warshall on the negated envy graph).
  - **Consequence:** the additive special case of the requester's target class (u_i(g) ∈ {−1,0,1}, subjective signs) already has a polynomial-time unit-subsidy guarantee. It comes from Lu–Mackenzie–Suzuki, but without EF1 before payments.
- **Additive special cases of the requester's own results are covered externally.** The additive versions of the requester's two proved results (negative dichotomous; objective-sign signed dichotomous) are special cases of Theorem 1.1 and Proposition 3.2. The requester's contribution beyond Lu et al. is therefore (a) non-additivity and (b) EF1 before payments.
- **Bundling does not transfer directly.** The meta-good bundling step uses additivity: a bundle's value is the sum of its items' values, and each meta-good is capped at value ≤ 1. Under non-additive {−1,0,1} marginals, a bundle's value is context-dependent, so the step cannot be imported as is.

### Gaps
- I found no peer-reviewed version or venue (v1 only). The proofs were not checked independently.
- The verbatim statement of Proposition 3.1 (subjective-goods-only instances, IMWM) was not extracted. Only the intro sentence describing it was seen.
- The paper does not address whether EF1-before-payments and ≤ $1 per agent can hold together for additive mixed instances. I found no source answering it.

---

## Q2. What exactly do Kawase, Makino, Sumita, Tamura and Yokoo prove in "Towards optimal subsidy bounds for envy-freeable allocations" (AAAI 2024; AIJ 2025)?

### Takeaway
- **Setting:** value-oracle valuations with |marginal| ≤ 1.
- **Theorem 1:** if valuations are doubly monotone (agent-specific good/chore classification allowed, no additivity) or n = 2 (arbitrary valuations), then per-agent ≤ n−1 and total ≤ n(n−1)/2, in polynomial time. The route is "EF1 allocation + Lemma 3".
- **EFk remark:** for general valuations, an EFk allocation gives per-agent k(n−1) and total k·n(n−1)/2.
- **Theorem 2:** for monotone goods with n ≥ 3, per-agent ≤ n−1.5 and total ≤ (n²−n−1)/2, in polynomial time.
- **Not covered:** nothing specific to binary marginals; no improvement for chores or mixed beyond Theorem 1.
- **Status:** PEER-REVIEWED (AAAI 2024; Artificial Intelligence 348:104406, 2025).

### Cited Findings
- **Venues.** AAAI 2024, Proceedings 38(9):9824–9831 ([AAAI OJS](https://ojs.aaai.org/index.php/AAAI/article/view/28842)). Journal version: *Artificial Intelligence* 348:104406 (2025) ([reference list in Lu–Mackenzie–Suzuki](https://arxiv.org/abs/2607.10089); also [Garg–Sharma–Wu refs](https://arxiv.org/abs/2609.15208)). The arXiv v1 is 2308.11230 (22 Aug 2023) — [arXiv](https://arxiv.org/abs/2308.11230)
- **Normalization and model (verbatim):** "we assume that the maximum marginal contribution of each item is at most one, i.e., |v_i(X ∪ {e}) − v_i(X)| ≤ 1 for any i ∈ N, e ∈ M, and X ⊆ M \ {e}". Valuations are given as value oracles. — [Kawase et al.](https://arxiv.org/abs/2308.11230)
- **Definitions (verbatim).**
  - "We define an item e ∈ M as a good for agent i ∈ N if v_i(X ∪ {e}) ≥ v_i(X) for every X ⊆ M \ {e}."
  - "an item e ∈ M as a chore for agent i ∈ N if v_i(X ∪{e}) ≤ v_i(X) for every X ⊆ M \{e}, with at least one of these inequalities being strict."
  - "An instance is said to be monotone if every e ∈ M is a good for any agent i ∈ N. An instance is said to be doubly monotone if every item e ∈ M is either a good or a chore for any agent i ∈ N."
  - The classification is per (agent, item) pair, so subjective signs are allowed.
  - [Kawase et al.](https://arxiv.org/abs/2308.11230)
- **Lemma 3 (key lemma, verbatim):** "Let w ∈ R^{[n]×[n]} be a weight matrix. We denote the sequence of numbers in descending order of (max_{j∈[n]}(w_{i,j} − w_{i,i}))_{i∈[n]} as (β_1, …, β_n) … Let p* be the minimum subsidy vector for w. Then, the rth largest value among p*_1, …, p*_n is at most Σ_{ℓ=1}^{n−r} β_ℓ for r = 1, 2, …, n." For an EF1 allocation, every β_i ∈ [0,1], "because v_i(A_i) ≥ v_i(A_j) − 1". — [Kawase et al.](https://arxiv.org/abs/2308.11230)
- **Theorem 1 (verbatim):** "If the valuations are doubly monotone or n = 2, there exists an envy-free allocation with a subsidy (A, p) such that max_i p_i ≤ n − 1 and Σ_i p_i ≤ Σ_{ℓ=1}^{n}(n − ℓ) = n(n − 1)/2. Moreover, such an envy-free allocation with a subsidy can be computed in polynomial time."
  - It relies on polynomial-time EF1 for doubly monotone valuations (Bhaskar–Sricharan–Vaish, APPROX 2021) or for n = 2 (Bérczi et al.).
  - The algorithm takes an EF1 allocation, finds a maximum-weight permutation of its bundles, and computes minimum subsidies (Floyd–Warshall).
  - [Kawase et al.](https://arxiv.org/abs/2308.11230)
- **General valuations via EFk (verbatim):** "Lemma 3 also implies that, even when the valuations are general and we only have an EFk allocation, we can still derive an envy-free allocation with a subsidy of at most k(n − 1) per agent and k · n(n − 1)/2 in total." — [Kawase et al.](https://arxiv.org/abs/2308.11230)
- **Example 1: tight for arbitrary EF1 allocations.** The instance is additive and monotone, with values n/(n+1), 1 and 0. Its EF1 allocation has minimum subsidy vector (0,1,…,n−1), so "max p_i = n − 1 and Σ p_i = n(n − 1)/2". The authors conclude that the bounds "cannot be improved when considering an arbitrary EF1 allocation". — [Kawase et al.](https://arxiv.org/abs/2308.11230)
- **Theorem 2 (verbatim):** "If n ≥ 3 and the valuations are monotone, there exists an envy-free allocation with a subsidy (A, p) such that max_{i∈[n]} p_i ≤ n − 1.5 and Σ_{i∈[n]} p_i ≤ (n² − n − 1)/2. Moreover, such an envy envy-free allocation with a subsidy can be computed in polynomial time." This holds for monotone (goods) valuations only. — [Kawase et al.](https://arxiv.org/abs/2308.11230)
- **Two agents.** "if n = 2, Theorem 1 implies that there exists an envy-free allocation with a subsidy where only one agent receives a subsidy of at most 1. This bound cannot be improved even when there is one item with a value of 1 for each agent." — [Kawase et al.](https://arxiv.org/abs/2308.11230)
- **Binary classes in Kawase's related work.** Binary additive [Halpern–Shah], matroidal [Goko et al.] and dichotomous [Barman et al.] each get "a subsidy of the amount at most 1 per agent and n − 1 in total". — [Kawase et al.](https://arxiv.org/abs/2308.11230)
- **How later work positions it.**
  - The JAIR survey (footnote 16): "Kawase et al. [2024a]'s result works for doubly-monotonic utilities." — [Liu–Lu–Suzuki–Walsh](https://arxiv.org/abs/2306.09564)
  - Dupré la Tour–Fujii (Table 1): "Doubly monotone: n(n − 1)/2 [Kaw+24]". — [DLT–Fujii](https://arxiv.org/abs/2509.16802)
  - Dupré la Tour–Suzuki: "it covers monotone chores". — [DLT–Suzuki](https://arxiv.org/abs/2609.08272)

### Inferences
- **Best constructive bound for non-additive mixed binary.** For doubly monotone binary instances with subjective signs (for each pair (i,g), all marginals of g are in {0,1} or all are in {−1,0}), Theorem 1 is the best constructive, peer-reviewed bound for non-additive mixed instances: integral p_i ∈ {0,…,n−1} and total ≤ n(n−1)/2. Integrality follows as in Q1.
- **n = 2 is settled even without double monotonicity.** For n = 2, Theorem 1 + Bérczi et al.'s two-agent EF1 cover arbitrary valuations. With {−1,0,1} marginals this gives p ∈ {0,1}², total ≤ 1 = n−1, in polynomial time. So the requester's general target problem (including bundle-dependent signs) is open only for n ≥ 3.
- **The output is not claimed to be EF1.** Theorem 1 outputs a maximum-weight permutation of an EF1 allocation, and permuting bundles can break EF1. The paper makes no EF1 claim about its output, so Kawase does not give "EF1 before payments".
- **No binary-specific sharpening.** Nothing in Kawase uses binary marginals beyond β ≤ 1, so the quadratic bound is not improved for {−1,0,1} instances.

### Gaps
- I inspected only arXiv v1. I did not check whether the AIJ 2025 journal version adds results, for example a chores or doubly-monotone analogue of Theorem 2's n−1.5 refinement.

---

## Q3. What do Dupré la Tour & Fujii (arXiv 2509.16802, 2025) and Dupré la Tour & Suzuki (arXiv 2609.08272, 2026) prove, and does either cover mixed-sign or non-monotone valuations for every n?

### Takeaway
- **Dupré la Tour–Fujii (PREPRINT, 2025):**
  - Covers arbitrary valuations: non-monotone, mixed sign, marginals in [−1,1].
  - Requires n to be a prime power.
  - Total O(n·√(n log n)) = O(n^{3/2}√log n); per-agent ≤ disc = O(√(n log n)).
  - Existential only (necklace splitting + randomized rounding).
- **Dupré la Tour–Suzuki (PREPRINT, Sep 2026):**
  - Works for every n, with v_i(∅)=0 and marginals in [−1,1].
  - Requires that all agents' bundle values be ≥ 0, or that all be ≤ 0. Non-monotone valuations are allowed inside each sign class.
  - Total ≤ 5√2(n−1)^{3/2}√ln(4n); per-agent ≤ 5√(2(n−1) ln(4n)).
  - Existential only (KKM + McDiarmid).
- **Neither covers mixed-sign valuations for every n.** Dupré la Tour–Suzuki explicitly say this needs a new idea.

### Cited Findings
- **Dupré la Tour–Fujii status.** arXiv:2509.16802, v1 only (20 Sep 2025), no Journal-ref or comments, so a PREPRINT. — [arXiv abs](https://arxiv.org/abs/2509.16802)
- **Dupré la Tour–Fujii Theorem 1 (verbatim):** "Let k = p^ν be a power of a prime, let M be a set of m items and let v_1, …, v_n : 2^M → R be n valuation functions with marginals in [−1, 1]. There exists a partition of the items in k subsets M = S_1 ∪ ··· ∪ S_k such that for all ℓ, ℓ′ ∈ [k] and for all i ∈ [n]: |v_i(S_ℓ) − v_i(S_ℓ′)| = O(√(n log nk))." Also: "Note that the bound does not depend on the number of items, and that we do not assume monotonicity of the valuations." — [DLT–Fujii](https://arxiv.org/abs/2509.16802)
- **Dupré la Tour–Fujii Lemma 5 (verbatim):** "There exists an allocation A = (A_1, …, A_n) and a payment vector p = (p_1, …, p_n) such that the pair (A, p) is envy-free and, for all i ∈ N, it holds that p_i ≤ disc(V, n). In particular, the total payment satisfies: Σ p_i ≤ (n − 1) disc(V, n)."
  - The proof takes the welfare-maximizing reassignment of a low-discrepancy n-partition.
  - It then shows p_i ≤ |v_j(A_i) − v_j(A_j)| for the endpoint j of the heaviest path.
  - It uses only the absence of positive cycles, not monotonicity.
  - [DLT–Fujii](https://arxiv.org/abs/2509.16802)
- **Dupré la Tour–Fujii Corollary 2 (verbatim):** "For arbitrary valuations with marginals in the interval [−1, 1], if the number of agents n = p^ν is a power of a prime, there exists an envy-free allocation requiring a total subsidy of O(n√(n log n))." The paper calls this "the first known subquadratic guarantee in this setting". Dupré la Tour–Suzuki describe it as "O(n^{3/2}√log n) for arbitrary valuations, but only when the number of agents is a prime power". — [DLT–Fujii](https://arxiv.org/abs/2509.16802); [DLT–Suzuki](https://arxiv.org/abs/2609.08272)
- **Dupré la Tour–Fujii Table 1 (their summary of known upper bounds, all marginals in [−1,1]):**

  | Valuation class | Total subsidy | Source |
  |---|---|---|
  | Monotone + additive | m(n−1) | HS19 |
  | Monotone + additive | n−1 | Bru+20 |
  | Monotone | 2(n−1)² | Bru+20 |
  | Monotone + dichotomous | n−1 | Bar+22 |
  | Monotone | (n²−n−1)/2 | Kaw+24 |
  | Doubly monotone | n(n−1)/2 | Kaw+24 |
  | Arbitrary (n prime power) | O(n√(n log n)) | Corollary 2 |

  — [DLT–Fujii](https://arxiv.org/abs/2509.16802)
- **Why the prime-power restriction.** Dupré la Tour–Fujii: "For composite k, the standard proof for necklace splitting uses a recursive cutting procedure that crucially depends on additivity; dropping that assumption breaks the recursion and no alternative argument is known." Their stated open question: "whether our bound can be extended to all values of k, beyond prime powers". — [DLT–Fujii](https://arxiv.org/abs/2509.16802)
- **Concurrent work by Hollender, Manurangsi, Meka and Suksompong.** "Discrepancy Beyond Additive Functions with Applications to Fair Division", PEER-REVIEWED at ITCS 2026 (LIPIcs vol. 362, paper 77).
  - It proves disc < √(2n(k−1)(1+ln(nk))) for 1-Lipschitz families and prime k.
  - It contains no subsidy result.
  - It notes that Dupré la Tour–Fujii's sharper O(√(n log nk)) bound is what subsidy applications with k = n need.
  - [Hollender et al. arXiv](https://arxiv.org/abs/2509.09252); [ITCS 2026 page](https://drops.dagstuhl.de/storage/00lipics/lipics-vol362-itcs2026/html/LIPIcs.ITCS.2026.77/LIPIcs.ITCS.2026.77.html)
- **Dupré la Tour–Suzuki status.** arXiv:2609.08272, v1 only (8 Sep 2026), so a PREPRINT. It already cites Lu–Mackenzie–Suzuki 2026. — [arXiv abs](https://arxiv.org/abs/2609.08272)
- **Dupré la Tour–Suzuki Theorem 1 (verbatim, with the absolute value restored from the abstract's "every single-item marginal value lies in [−1, 1]"):** "Let N = [n] be a set of agents and let M be a finite set of indivisible items. Suppose that each valuation v_i : 2^M → R satisfies v_i(∅) = 0 and |v_i(S ∪ {g}) − v_i(S)| ≤ 1 … Assume that either v_i(S) ≥ 0 for every i, S, or v_i(S) ≤ 0 for every i, S. Then there exist an allocation A = (A_1, …, A_n) and nonnegative subsidies (p_1, …, p_n) that are envy-free and satisfy Σ_{i∈N} p_i ≤ 5√2 (n − 1)^{3/2} √log(4n)."
  - Per-agent: "The proof also bounds each agent's subsidy by 5√(2(n − 1) log(4n))."
  - Existential: "The guarantee is existential: the argument identifies a suitable partition through a topological existence theorem, rather than a polynomial-time algorithm."
  - The log is natural, from the McDiarmid tail 2·exp(−2t²/(25h)).
  - [DLT–Suzuki](https://arxiv.org/abs/2609.08272)
- **Which valuations the class includes.**
  - "These classes include monotone goods and monotone chores, respectively, but do not require monotonicity."
  - Their example of a non-monotone member: "with two items a, b, the valuation v(∅) = v({a, b}) = 0 and v({a}) = v({b}) = 1 is nonnegative and has marginals in [−1, 1], but is not monotone."
  - [DLT–Suzuki](https://arxiv.org/abs/2609.08272)
- **Refined constants (Section 6).** "A more careful accounting in our proof yields a total-subsidy bound of (n − 1)√((2n + 3) log n) when valuations are either all nonnegative or all nonpositive. For monotone goods or monotone chores, this bound improves to (n − 1)√((n+5)/2 · log n)." — [DLT–Suzuki](https://arxiv.org/abs/2609.08272)
- **Where the sign assumption enters, and the mixed-sign limitation.**
  - Lemma 6: if B_k = ∅, then for nonnegative valuations q_k(B) = 0 (the empty slot has the minimum price), and for nonpositive valuations q_k(B) = max_j q_j(B).
  - Discussion: "The sign assumption enters our proof only through the empty-bundle boundary condition … All other ingredients—the matching identity, one-item stability, and concentration—apply to arbitrary valuations with bounded single-item marginals. Extending our approach to mixed-sign valuations for every number of agents therefore calls for an alternative way to equalize expected prices."
  - [DLT–Suzuki](https://arxiv.org/abs/2609.08272)
- **Open questions they state.**
  - Gap to the lower bound: "The single-good example gives a lower bound of n − 1 … does a linear total-subsidy bound hold for general monotone valuations?"
  - Computation: whether the bound "can be achieved by a polynomial-time algorithm … Our KKM argument establishes the existence of an equalizing point x* but does not provide a polynomial-time procedure for finding it."
  - [DLT–Suzuki](https://arxiv.org/abs/2609.08272)

### Inferences
- **Dupré la Tour–Fujii on the target class.** It applies to every {−1,0,1}-marginal instance, including bundle-dependent signs, but only when n is a prime power. The bound is existential, O(n^{3/2}√log n) in total and O(√(n log n)) per agent, with unspecified constants. That per-agent bound is far from unit subsidies.
- **Dupré la Tour–Suzuki on the target class.** It applies only to {−1,0,1} instances in which every agent values every bundle ≥ 0, or every agent values every bundle ≤ 0. Their own example v(a)=v(b)=1, v(ab)=0 is a non-doubly-monotone binary valuation in the nonnegative class. Negative dichotomous valuations ({−1,0} marginals, possibly non-additive) are in the nonpositive class. Genuinely mixed instances with subjective signs, where some agent values some bundle > 0 and some bundle < 0, are outside it.
- **Per-agent constant shifts do not help.** EF is invariant under adding a constant to each agent's valuation, but Dupré la Tour–Suzuki need the empty bundle to be every agent's minimum (or maximum) bundle, and a shift does not create that. (My reasoning from their Lemma 6.)
- **When the existential bound beats Kawase (my arithmetic, natural log).** This comparison applies only on the overlap with Kawase, i.e. monotone goods and chores.
  - The refined bound (n−1)√((2n+3)ln n) drops below Kawase's n(n−1)/2 at about n ≥ 29.
  - The headline bound 5√2(n−1)^{3/2}√ln(4n) drops below n(n−1)/2 only at about n ≳ 1,750.

### Gaps
- I found no peer-reviewed venue for either paper.
- Neither paper offers polynomial-time algorithms.
- Neither paper gives a mixed-sign result for non-prime-power n.

---

## Q4. Is there any work on subsidies for binary, dichotomous, bivalued or ternary ({−1,0,1}) valuations with mixed or subjective signs, including chore or mixed extensions of Barman et al. 2022 and Goko et al. 2024?

### Takeaway
- **No external paper targets binary/ternary valuations with mixed or subjective signs.** The binary-marginal subsidy literature is goods-only:
  - Halpern–Shah: binary additive.
  - Goko et al.: matroidal.
  - Barman et al.: dichotomous, non-additive.
  - Li et al.: binary additive graph orientations.
  - Elmalem et al.: weighted, binary additive.
  - Dai et al.: binary house allocation.
  - Kulkarni et al.: online, binary.
- **Ternary additive mixed** is covered only implicitly, as a special case of Lu–Mackenzie–Suzuki's general additive mixed result (Q1).
- **Additive chores** were already handled by Wu–Zhang–Zhou (WINE 2023): EF1 before payments, ≤ $1 each, total ≤ n−1, polynomial time. This covers additive {0,−1} chores.
- **Non-additive binary chores and mixed binary:** apart from the requester's own paper (excluded), I found no subsidy work. The one binary-chores paper (Barman–Narayan–Verma, binary supermodular costs) has no subsidy results.

### Cited Findings
- **Barman, Krishna, Narahari, Sadhukhan (IJCAI 2022; PEER-REVIEWED; arXiv 2201.07419).**
  - **Class:** dichotomous means "v_i(S ∪ {g}) − v_i(S) ∈ {0, 1}", with v_i(∅) = 0. "Note that a dichotomous valuation v_i is monotone". The result does "not require the (dichotomous) valuations to be additive, submodular, or even subadditive."
  - **Theorem 4 (verbatim):** "For any discrete fair division instance ⟨[n], [m], {v_i}⟩ with dichotomous valuations, there exists an envy-free solution (A, p) such that p ∈ {0, 1}^n. Furthermore, given value oracle access to the v_i s, such an envy-free solution, (A, p), can be computed in polynomial time."
  - **Total and tightness:** "the total required subsidy is at most (n − 1)", tight because of a single good valued 1 by all.
  - [Barman et al.](https://arxiv.org/abs/2201.07419) ([IJCAI proceedings](https://www.ijcai.org/proceedings/2022/9))
- **Barman et al.'s algorithm** (the "one-good extension").
  - ALG inserts goods one at a time while keeping a partial allocation envy-freeable with {0,1} subsidies.
  - EXTEND (Lemma 8) tests whether there is a bundle permutation and a most-subsidized agent κ with marginal 1 for g.
  - Otherwise FINDSINK (Lemmas 9–11) finds an agent s such that adding g keeps subsidies in {0,1}.
  - Proposition 5: "Let Y be an envy-freeable (partial) allocation. Also, assume that, for an agent x and an unallocated good g, we have v_x(Y_x ∪ {g}) − v_x(Y_x) = 1. Then, the allocation (Y_1, …, Y_x ∪ {g}, …, Y_n) is envy-freeable as well."
  - Integrality: footnote 5 says "under dichotomous valuations the edge weights in the envy graph are integers", and in Lemma 11 "the subsidies are nonnegative integers … they are either 0 or 1".
  - [Barman et al.](https://arxiv.org/abs/2201.07419)
- **Barman et al.: no EF1, and open directions (verbatim).** "We can, in fact, construct an instance wherein a specific execution of the developed algorithm returns an allocation that is not EF1; see Appendix C. Hence, extending the current work to additionally obtain the EF1 guarantee is a relevant direction of future work. Another interesting direction would be to obtain tight subsidy bounds for general monotone valuations." The paper does not discuss chores or negative marginals. — [Barman et al.](https://arxiv.org/abs/2201.07419)
- **Goko, Igarashi, Kawase, Makino, Sumita, Tamura, Yokoi, Yokoo (AAMAS 2022; GEB 144:49–70, 2024; PEER-REVIEWED).**
  - **Class:** matroidal valuations (monotone submodular with dichotomous marginals), goods only (v_i: 2^M → R_+, v_i(∅)=0).
  - **Theorem 3.1:** "For matroidal valuations, there is a polynomial-time implementable mechanism that is truthful, utilitarian optimal, and envy-free with each agent receiving subsidy 0 or 1, and the total subsidy being at most n − 1." This is the subsidized-egalitarian mechanism, which may leave items unallocated.
  - **Theorem 3.20:** the "complete, utilitarian optimal, and envy-free" variant, with subsidies 0/1 and total ≤ n−1, in polynomial time, but not truthful.
  - **Proposition A.1:** the complete-allocation algorithm's output is EFX.
  - **Impossibility:** "even when agents have binary additive valuations, no truthful and envy-free mechanism allocates all items and returns a Lorenz dominating allocation with each agent being subsidized by at most 1."
  - [Goko et al.](https://arxiv.org/abs/2105.01801); GEB citation in [DLT–Suzuki refs](https://arxiv.org/abs/2609.08272)
- **Halpern & Shah (SAGT 2019; PEER-REVIEWED; secondary).**
  - For binary additive goods, a maximum-Nash-welfare allocation "can be made envy-free with a subsidy of at most 1 for each agent" ([Goko et al.](https://arxiv.org/abs/2105.01801)), with total n−1 ([Barman et al.](https://arxiv.org/abs/2201.07419)).
  - For general additive goods with values ≤ 1, total m(n−1) ([Wu–Zhang–Zhou](https://arxiv.org/abs/2307.04411); [Li et al.](https://arxiv.org/abs/2502.13671)).
- **Wu, Zhang, Zhou, "One Quarter Each (on Average) Ensures Proportionality" (WINE 2023, LNCS 14413:582–599; PEER-REVIEWED; arXiv 2307.04411) — EF for additive chores.**
  - **Result 1:** "For the allocation of chores, we can compute in polynomial time an EF1 allocation X and subsidies s such that (X, s) is EF, where the total subsidy ‖s‖_1 ≤ n − 1. Moreover, there exists an instance for which every EF allocation requires a total subsidy of at least n − 1."
  - **Theorem A.3:** "the allocation without subsidy is EF1, the subsidy to each agent is at most 1 and the total subsidy is at most n − 1".
  - **Normalization:** additive costs with c_i(e) ≤ 1.
  - **Algorithm:** "Modified Bounded-Subsidy Algorithm", i.e. iterated minimum-weight perfect matching.
  - **Lower bound (Lemma A.6):** "an instance with n − 1 items having cost 1 to n identical agents … ‖s‖_1 ≥ Σ c_i(X_i) = n − 1."
  - The authors wrote: "As far as we know, the problem of computing EF or PROP allocations with subsidy has not been considered for the allocation of chores", and suggested extending "to the setting of mixed items (goods and chores)".
  - [Wu–Zhang–Zhou](https://arxiv.org/abs/2307.04411)
  - Garg–Sharma–Wu likewise describe it: "An analogous result was also shown for chores by [WZZ23], under the assumption that every chore has disutility at most 1 to every agent." — [Garg–Sharma–Wu](https://arxiv.org/abs/2609.15208)
- **Barman, Narayan, Verma, "Fair Chore Division under Binary Supermodular Costs" (arXiv 2302.11530; per Kawase's reference list, AAMAS 2023 is unverified).**
  - Costs have binary marginals, c_i(S+a) − c_i(S) ∈ {0,1}, and are supermodular.
  - Results: EF1+PO, MMS+PO and Lorenz-dominating allocations, in polynomial time.
  - Lemma 2: f is binary supermodular iff g(S) = |S| − f(S) is a matroid rank function.
  - My query against the paper text found no subsidy or monetary-transfer result.
  - [Barman–Narayan–Verma](https://arxiv.org/abs/2302.11530)
- **Ternary (additive {−1,0,1}) without subsidies.** Bérczi et al.: "A utility function is tertiary if u(s) ∈ {−1, 0, +1} for every s ∈ S. It is not difficult to see that for tertiary utilities EF1 implies EFX, thus the Double Round Robin Algorithm of [Aziz et al. 2022] provides such a solution." Envy-freeability or subsidies are not considered there. — [Bérczi et al.](https://arxiv.org/abs/2006.04428)
- **EF1 before payments for mixed additive (no bound).** Aziz, Lu, Mackenzie, Suzuki, "Fair Division with Indivisible Goods, Chores, and Cake" (EC 2026 per [Lu–Mackenzie–Suzuki refs](https://arxiv.org/abs/2607.10089); arXiv 2511.04891).
  - Main Result 2 / Theorem 4.2: "With indivisible goods and chores, an EF1 and envy-freeable allocation always exists" (additive utilities, subjective signs).
  - No subsidy bound is stated.
  - Their open question: "Is EF1 compatible with envy-freeability for doubly monotone instances? Note that the question is still open in the setting with only indivisible goods."
  - [Aziz et al.](https://arxiv.org/abs/2511.04891)
- **Bivalued / k-valued.**
  - Li et al.: computing a minimum-subsidy EF orientation is NP-hard "even when the graph is simple and the agents have bi-valued additive valuations" (goods). — [Li et al.](https://arxiv.org/abs/2502.13671)
  - Kulkarni et al.: online subsidy for k-valued goods (Theorem 4.3) is independent of m. — [Kulkarni et al.](https://arxiv.org/abs/2510.13633)
  - No bivalued mixed or chores subsidy result was found.
- **Binary goods variants.** These are described under Q5 and in the master catalogue (Q6):
  - binary additive graph orientations ([Li et al.](https://arxiv.org/abs/2502.13671));
  - weighted binary additive ([Elmalem et al.](https://arxiv.org/abs/2502.09006));
  - binary house allocation ([Dai et al.](https://arxiv.org/abs/2608.22216));
  - online binary submodular, supermodular and additive ([Kulkarni et al.](https://arxiv.org/abs/2510.13633)).

### Inferences
- **External tightness of the requester's chores bound.** Wu–Zhang–Zhou's Lemma A.6 instance (n−1 unit chores, n identical agents) is an additive negative-dichotomous instance. So total n−1 is necessary even for {0,−1} additive chores, and the requester's Σp ≤ n−1 is tight by an external lower bound.
- **Prior art for the requester's own classes (context only).**
  - *Additive* negative dichotomous: Wu–Zhang–Zhou 2023 already gives EF1 + p_i ≤ 1, hence p ∈ {0,1}^n by integrality, in polynomial time.
  - *Non-additive* negative dichotomous: the best external bounds were Kawase et al. (n−1 per agent, n(n−1)/2 total, constructive; these valuations are doubly monotone) and Dupré la Tour–Suzuki (O(n^{3/2}√log n) total, existential; these valuations are nonpositive).
  - Objective-sign signed dichotomous (non-additive): the best external bound was Kawase's n(n−1)/2, plus Dupré la Tour–Fujii (existential) for prime-power n.
- **Integrality is a free conversion in binary settings.** Any proof of per-agent subsidy < 2 for {−1,0,1} valuations automatically yields p ∈ {0,1}^n. This is the same argument Barman et al. (Lemma 11) and Goko et al. use.
- **The one-good extension may not survive bundle-dependent signs.** Barman et al.'s argument uses monotonicity in places; Proposition 5 needs "marginal 1 for the receiver". The weight-only parts survive marginals in {−1,0,1}: integrality, and the fact that a +1 marginal raises identity-permutation welfare by exactly 1 while any permutation's welfare rises by at most 1. Whether Lemma 9 (envy-freeability of FINDSINK candidates) survives items with −1 marginals for some agents was not checked.

### Gaps
- My DBLP title sweep was blocked by an anti-bot page, so coverage relies on alphaXiv discovery, citation chasing and web search. Workshop-only or non-arXiv papers could be missed.
- I found no paper on subsidies for bivalued, ternary or dichotomous valuations with subjective signs beyond what is listed here.
- I did not verify the published (journal) version of Bérczi et al.

---

## Q5. What related variants exist with mixed items, and what does the Liu–Lu–Suzuki–Walsh survey record about subsidies?

### Takeaway
- **Covered for mixed manna:** proportionality with subsidy. Unweighted tight τ(n) is due to Wu–Xue–Zhou (IJCAI 2025). Weighted tight τ(n) is due to Garg–Sharma–Wu (preprint, Sep 2026). Here τ(n) = n/4 for even n and (n²−1)/(4n) for odd n.
- **Goods only (sometimes with chores remarks), never mixed:**
  - weighted envy-freeness with subsidy (Elmalem et al.);
  - graph orientations (Li et al.; they say "chores/mixed manna … has not been studied yet");
  - online item arrival (Kulkarni et al.; chores mentioned informally);
  - online and offline house allocation (Teh et al.; Dai et al.).
- **The JAIR survey's subsidy section** is titled "Indivisible Goods with Subsidy". It records Brustle, Kawase (with a footnote that Kawase works for doubly-monotonic utilities), Goko, Barman and Wu et al. Its Open Question 9 asks for subquadratic total subsidy for monotone utilities. It poses no mixed-manna subsidy question in the extracted text.

### Cited Findings
- **The survey: Liu, Lu, Suzuki, Walsh, "Mixed Fair Division: A Survey" (JAIR 80:1373–1406, 2024; PEER-REVIEWED).**
  - Section 6 is "Indivisible Goods with Subsidy".
  - Theorem 6.3 restates Brustle et al.: "For additive utilities, there exists a polynomial-time algorithm which outputs an envy-free allocation with subsidy (O, p) such that: (i) Subsidy to each agent is at most one, i.e., p_i ≤ 1. (ii) Allocation O is EF1 and balanced."
  - Monotone: "Brustle et al. [2020] showed that for monotone valuations, a total subsidy of 2(n − 1)² suffices … Kawase et al. [2024a] improved this bound to (n²−n−1)/2" (footnote 16: "Kawase et al. [2024a]'s result works for doubly-monotonic utilities").
  - Open Question 9: "For monotonic utilities, does there exist an envy-free allocation whose total subsidy is O(n^{2−ε}) for some ε > 0?"
  - Goko et al. (matroid rank: n−1, truthful) and Barman et al. (binary marginals: n−1) are noted.
  - Proportionality with subsidy (Wu et al. 2023: n/4; footnote 17: "mainly focused on chores") and transfers (Narayan–Suzuki–Vetta; Aziz 2021) are also covered.
  - Its general model (Section 2.2) allows positive, zero and negative values and defines doubly-monotonic utilities.
  - [Survey arXiv v4](https://arxiv.org/abs/2306.09564); [JAIR](https://jair.org/index.php/jair/article/view/15800)
- **Brustle et al. (EC 2020; PEER-REVIEWED; secondary).**
  - Additive goods [0,1]: ≤ 1 per agent, EF1 and balanced, polynomial time ([survey Thm 6.3](https://arxiv.org/abs/2306.09564)).
  - Monotone goods: "a maximum subsidy of 2(n − 1) and a total subsidy of 2(n − 1)²" ([Kawase et al.](https://arxiv.org/abs/2308.11230)).
- **Extensions of Brustle's iterated-matching method.**
  - To additive chores: Wu–Zhang–Zhou 2023, iterated minimum-weight perfect matching; EF1, ≤1, n−1 ([Wu–Zhang–Zhou](https://arxiv.org/abs/2307.04411)).
  - To subjective goods and objective chores (Propositions 3.1/3.2) and to full mixed additive via bundling ([Lu–Mackenzie–Suzuki](https://arxiv.org/abs/2607.10089)).
  - To EF1 + envy-freeable for mixed additive, with no bound ([Aziz et al.](https://arxiv.org/abs/2511.04891)).
- **Proportionality, mixed, unweighted.** Wu, Xue, Zhou, "Revisiting Proportional Allocation with Subsidy" (IJCAI 2025, pp. 4082–4090; PEER-REVIEWED; secondary): mixed manna, additive, total τ(n), "tight for all n". — [Garg–Sharma–Wu](https://arxiv.org/abs/2609.15208); [Lu–Mackenzie–Suzuki](https://arxiv.org/abs/2607.10089)
- **Proportionality, mixed, weighted.** Garg, Sharma, Wu, "Tight Subsidy Bounds for Weighted Proportional Allocation of Mixed Manna" (arXiv 2609.15208, 14 Sep 2026; PREPRINT).
  - Theorem 4.20: "For any mixed manna instance I with n agents with additive valuation functions and general weights, there always exists a WPROP1 allocation that can be made WPROP with total subsidy at most τ(n) · range(I)."
  - Existential via KKM; polynomial-time only for a fixed number of agents (Result 2).
  - Earlier weighted bounds were goods-only or chores-only: (n−1)/2 [Wu–Zhang–Zhou 2023] and n/3 − 1/6 [Wu–Zhou, WINE 2024].
  - [Garg–Sharma–Wu](https://arxiv.org/abs/2609.15208)
- **Weighted envy-freeness with subsidy (goods only).** Klein Elmalem, Aziz, Gonen, Huang, Kimura, Saha, Segal-Halevi, Sun, Suzuki, Yokoo, "Whoever said money won't solve all your problems?" (arXiv 2502.09006).
  - It merges two AAMAS 2025 extended abstracts; it is cited as SAGT 2025 by [Dai et al.](https://arxiv.org/abs/2608.22216), a venue I did not verify.
  - Valuations: monotone, v_i ≥ 0, V = max per-item value.
  - General monotone: (W/w_min − 1)mV, tight.
  - Additive with integer weights: (W − w_min)V/gcd(w).
  - Identical additive: (n−1)V.
  - **Binary additive (Theorem 7.12):** "subsidy to each agent i ∈ N is at most w_i/w_min in polynomial-time. Moreover, the total subsidy is bounded by W/w_min − 1."
  - **Matroidal lower bound (Theorem 7.14):** (m/n)(W/w_min − n), which grows with m.
  - No chores.
  - [Elmalem et al.](https://arxiv.org/abs/2502.09006)
- **Graph orientations (goods only).** Li, Sun, Suzuki, Xing, "On the Subsidy of Envy-Free Orientations in Graphs" (arXiv 2502.13671; PREPRINT; abstract at [AAAC 2025](https://conference.cs.cityu.edu.hk/aaac2025/abstract/AAAC_2025_paper_26.pdf)). Valuations are monotone, v_i: 2^M → R_+, with "max_{e,S} v_i(S∪{e}) − v_i(S) = 1".
  - **Theorem 9:** "For multigraphs with monotone agent valuations, there always exists an EF orientation with a total subsidy of at most n − 1, and it can be computed in polynomial time using value queries." Lemma 8 bounds the heaviest path by 1, so p_i ≤ 1.
  - **Theorem 11:** multigraph + additive gives n/2 (tight), in polynomial time.
  - **Theorem 21:** simple graph + monotone gives n−2 (tight), in polynomial time.
  - **Theorem 4:** binary additive minimum subsidy is computable in polynomial time.
  - Bi-valued additive minimum subsidy is NP-hard.
  - Conclusion: "we have been focusing on the allocation of goods and the mirror problem of chores/mixed manna has not been studied yet."
  - [Li et al.](https://arxiv.org/abs/2502.13671)
- **Online item arrival (goods; chores informal).** Kulkarni, Mehta, Narayan, Ponitka (arXiv 2510.13633, Oct 2025; PREPRINT).
  - Envy-freeability "cannot always be preserved online when the valuations are submodular or supermodular, even with binary marginals".
  - Additive: m(n−1), tight online (Theorem 4.1).
  - "the minimum subsidy is Θ(n²) even for … binary additive valuations and rank-one valuations".
  - Identical monotone: n−1 (Theorem 4.6).
  - Section 5: "most of our results extend to the fair division of chores via similar analyses"; nothing on mixed manna.
  - [Kulkarni et al.](https://arxiv.org/abs/2510.13633)
- **House allocation (unit demand, goods).**
  - Online (Teh, Cohen, Celine, Yu, Wooldridge, arXiv 2609.29691; PREPRINT): utilities in [0,1]. Lemma 4.1: any complete envy-freeable house allocation has sub ≤ n−1. No bounded competitive ratio is possible for minimum subsidy (Theorem 4.3). — [Teh et al.](https://arxiv.org/abs/2609.29691)
  - Offline binary (Dai, Li, Wu, Zhang, arXiv 2608.22216; PREPRINT): "For binary instances … a total subsidy of at most (n − 1) suffices … and this bound is tight". Minimum subsidy is NP-hard even for binary utilities. — [Dai et al.](https://arxiv.org/abs/2608.22216)

### Inferences
- **Proportionality does not give envy-freeness.** The mixed-manna proportionality bounds are strictly weaker targets (EF ⇒ PROP), so they give no EF bound for the target class.
- **Mixed-sign envy-freeness work is sparse.** The only EF-with-subsidy results that explicitly handle subjective-sign items are Lu–Mackenzie–Suzuki (additive, unit), Aziz et al. (additive, EF1 + envy-freeable, no bound), Kawase (doubly monotone, quadratic) and Dupré la Tour–Fujii (arbitrary, prime-power n, existential).
- **Binary-marginal positive results are fragile under model changes.** Weighted matroidal subsidies must grow with m, and online binary submodular/supermodular instances cannot even stay envy-freeable. Unit subsidies for binary classes in the standard offline unweighted model should therefore not be presumed to transfer automatically.

### Gaps
- I did not read Wu–Xue–Zhou (IJCAI 2025) or Wu–Zhou (WINE 2024) directly; their statements come from two citing papers.
- I did not read the published JAIR text, only arXiv v4. The survey's Section 4 (goods and chores) was not fully extracted for subsidy mentions.
- No online subsidy work handles mixed manna.

---

## Q6. For the target class (general {−1,0,1} marginals, subjective signs, possibly not doubly monotone, arbitrary n), what is the best known total and per-agent bound, from which paper, and is it constructive?

### Takeaway
Excluding the requester's own paper, there is no single bound for the whole class. The best known results are piecewise:
- **(a) Additive {−1,0,1}, subjective signs:** ≤ 1 per agent and ≤ n−1 total, constructive in polynomial time — Lu–Mackenzie–Suzuki 2026 (PREPRINT). By integrality this is p ∈ {0,1}^n, but with no EF1.
- **(b) Non-additive but doubly monotone, subjective signs:**
  - Constructive: ≤ n−1 per agent and ≤ n(n−1)/2 total — Kawase et al. (PEER-REVIEWED).
  - Existential, prime-power n only: O(√(n log n)) per agent and O(n^{3/2}√log n) total — Dupré la Tour–Fujii (PREPRINT).
- **(c) Not doubly monotone (signs depend on the bundle):**
  - n = 2: total ≤ 1 (unit), polynomial time — Kawase Theorem 1 with Bérczi et al.'s two-agent EF1.
  - n a prime power: existential O(n^{3/2}√log n) — Dupré la Tour–Fujii.
  - Sign-restricted subclass (every agent's bundle values all ≥ 0, or all ≤ 0): existential 5√2(n−1)^{3/2}√ln(4n) for every n — Dupré la Tour–Suzuki (PREPRINT).
  - Otherwise, for n ≥ 3 not a prime power with mixed-sign bundle values: **I found no bound independent of m.** Kawase's EF1/EFk route is blocked because EF1 existence for non-monotone non-additive valuations with n ≥ 3 is open. Only a trivial (n−1)·m bound applies.
- **Lower bounds:** the only ones known are n−1 total and 1 per agent.
- **Unit subsidies (p ∈ {0,1}^n, total ≤ n−1) for the general binary subjective class** are therefore neither proved nor refuted in the external literature.

### Cited Findings
- **Additive.** Theorem 1.1 of [Lu–Mackenzie–Suzuki](https://arxiv.org/abs/2607.10089): u_i: M → [−1,1], subjective signs, 0 ≤ p_i ≤ 1, polynomial time, tight. It does not maintain EF1.
- **Doubly monotone.** Theorem 1 of [Kawase et al.](https://arxiv.org/abs/2308.11230): max p_i ≤ n−1, Σp_i ≤ n(n−1)/2, polynomial time. EF1 for doubly monotone valuations is computed in polynomial time [Bhaskar–Sricharan–Vaish 2021, secondary via [Kawase et al.](https://arxiv.org/abs/2308.11230) and [Aziz et al.](https://arxiv.org/abs/2511.04891): "An EF1 allocation of mixed indivisible goods and chores always exists and can be computed efficiently for agents with additive or even doubly monotone utilities"].
- **Two agents, arbitrary valuations.** Bérczi et al. Theorem 1: "There always exists an EF1 allocation for two agents with arbitrary (not necessarily monotone or additive) utility functions. Such an allocation can be computed in polynomial time." Kawase et al. use it for the n = 2 case of Theorem 1. — [Bérczi et al.](https://arxiv.org/abs/2006.04428); [Kawase et al.](https://arxiv.org/abs/2308.11230)
- **EF1 for non-monotone valuations with n ≥ 3 is open.** Bérczi et al.: "the existence of an EF1 allocation for non-monotone, non-additive utility functions is still open even for identical utilities". Their Question 12 asks exactly this. They also show that the earlier claimed EF1 algorithm for arbitrary utilities (Aziz et al. 2022's Generalized Envy Graph Algorithm) is flawed. — [Bérczi et al. (arXiv 2006.04428, 2020)](https://arxiv.org/abs/2006.04428)
- **EFk route.** Kawase et al. show that an EFk allocation yields k(n−1) per agent and k·n(n−1)/2 total. — [Kawase et al.](https://arxiv.org/abs/2308.11230)
- **Prime-power n.** Corollary 2 of [DLT–Fujii](https://arxiv.org/abs/2509.16802): arbitrary valuations with marginals in [−1,1]; Lemma 5 gives per-agent ≤ disc(V,n) = O(√(n log n)). Existential.
- **Sign-restricted, every n.** Theorem 1 of [DLT–Suzuki](https://arxiv.org/abs/2609.08272). Existential. The authors say that mixed-sign for every n "calls for an alternative way to equalize expected prices".
- **Lower bounds.**
  - n−1 total, from one item valued 1 by all; this holds within binary additive goods ([Barman et al.](https://arxiv.org/abs/2201.07419)).
  - n−1 total for unit chores ([Wu–Zhang–Zhou Lemma A.6](https://arxiv.org/abs/2307.04411)).
  - For general monotone valuations, "The single-good example gives a lower bound of n − 1" and no better lower bound is stated ([DLT–Suzuki](https://arxiv.org/abs/2609.08272)).

#### Master catalogue: upper bounds and algorithms for EF with subsidy, especially with chores or mixed items

| # | Paper (status) | Valuation class | Signs | Normalization | Per-agent | Total | Constructive? | Source |
|---|---|---|---|---|---|---|---|---|
| 1 | Halpern–Shah, SAGT 2019 (peer-reviewed) | additive; binary additive | goods | item value ≤ 1 | binary: ≤ 1 (MNW allocation) | additive m(n−1); binary n−1 | binary: via MNW | secondary: [Goko](https://arxiv.org/abs/2105.01801), [Barman](https://arxiv.org/abs/2201.07419), [WZZ23](https://arxiv.org/abs/2307.04411) |
| 2 | Brustle et al., EC 2020 (peer-reviewed) | additive; monotone | goods | values in [0,1]; marginal ≤ 1 | additive ≤ 1 (EF1, balanced); monotone 2(n−1) | n−1; 2(n−1)² | poly | secondary: [survey](https://arxiv.org/abs/2306.09564), [Kawase](https://arxiv.org/abs/2308.11230) |
| 3 | Barman–Krishna–Narahari–Sadhukhan, IJCAI 2022 (peer-reviewed) | dichotomous, non-additive (monotone) | goods | marginals ∈ {0,1}, v(∅)=0 | p ∈ {0,1}^n | ≤ n−1 (tight) | poly, value oracle; not necessarily EF1 | [arXiv](https://arxiv.org/abs/2201.07419) |
| 4 | Goko et al., AAMAS 2022 / GEB 2024 (peer-reviewed) | matroidal (submodular binary) | goods | marginals ∈ {0,1} | 0 or 1 | ≤ n−1 | poly; truthful version (may leave items unallocated); complete version is EFX | [arXiv](https://arxiv.org/abs/2105.01801) |
| 5 | Wu–Zhang–Zhou, WINE 2023 (peer-reviewed) | additive | objective chores | c_i(e) ≤ 1 | ≤ 1, EF1 before payments | ≤ n−1 (tight) | poly (iterated min-weight perfect matching) | [arXiv](https://arxiv.org/abs/2307.04411) |
| 6 | Kawase et al., AAAI 2024 / AIJ 2025 (peer-reviewed) | doubly monotone (non-additive), or n = 2 arbitrary | subjective signs allowed | \|marginal\| ≤ 1 | ≤ n−1 | ≤ n(n−1)/2 | poly (from an EF1 allocation) | [arXiv](https://arxiv.org/abs/2308.11230) |
| 6′ | same | general valuations given an EFk allocation | any | \|marginal\| ≤ 1 | k(n−1) | k·n(n−1)/2 | poly given the EFk allocation | [arXiv](https://arxiv.org/abs/2308.11230) |
| 6″ | same, Theorem 2 | monotone, n ≥ 3 | goods | \|marginal\| ≤ 1 | n−1.5 | (n²−n−1)/2 | poly | [arXiv](https://arxiv.org/abs/2308.11230) |
| 7 | Li–Sun–Suzuki–Xing 2025 (preprint) | graph orientations: monotone multigraph / additive multigraph / monotone simple graph | goods | max marginal 1 | ≤ 1 (multigraph monotone) | n−1 / n/2 (tight) / n−2 (tight) | poly, value queries | [arXiv](https://arxiv.org/abs/2502.13671) |
| 8 | Dupré la Tour–Fujii 2025 (preprint) | arbitrary (non-monotone, non-additive), n a prime power | arbitrary, incl. mixed | marginals in [−1,1] | O(√(n log n)) | O(n√(n log n)) | existential only | [arXiv](https://arxiv.org/abs/2509.16802) |
| 9 | Aziz–Lu–Mackenzie–Suzuki, EC 2026 (accepted; arXiv 2511.04891) | additive | subjective signs | — | no bound stated (EF1 + envy-freeable exists) | — | existence stated | [arXiv](https://arxiv.org/abs/2511.04891) |
| 10 | Lu–Mackenzie–Suzuki 2026 (preprint) | additive | subjective signs (mixed manna) | u_i(g) ∈ [−1,1] | ≤ 1 (tight) | ≤ n−1 | poly; EF1 not maintained | [arXiv](https://arxiv.org/abs/2607.10089) |
| 11 | Dupré la Tour–Suzuki 2026 (preprint) | non-monotone allowed; all v_i(S) ≥ 0, or all ≤ 0 | single sign of bundle values across all agents | v(∅)=0, marginals in [−1,1] | ≤ 5√(2(n−1)ln(4n)) | ≤ 5√2(n−1)^{3/2}√ln(4n); refined (n−1)√((2n+3)ln n); monotone goods/chores (n−1)√((n+5)/2·ln n) | existential only | [arXiv](https://arxiv.org/abs/2609.08272) |
| 12 | Klein Elmalem et al. 2025 (weighted EF) | binary additive / additive / monotone | goods | V = max item value | binary: w_i/w_min | binary: W/w_min − 1 | poly | [arXiv](https://arxiv.org/abs/2502.09006) |
| 13 | Kulkarni–Mehta–Narayan–Ponitka 2025 (preprint, online) | identical monotone / additive / k-valued etc. | goods (chores informal) | marginal ≤ 1 | — | identical n−1; additive m(n−1) (tight online); binary additive Θ(n²) | online algorithms | [arXiv](https://arxiv.org/abs/2510.13633) |
| 14 | Dai–Li–Wu–Zhang 2026 (preprint, house allocation) | binary unit-demand | goods | utilities ∈ {0,1} | ≤ 1 | ≤ n−1 (tight) | min-subsidy NP-hard; poly for bounded agent types | [arXiv](https://arxiv.org/abs/2608.22216) |
| 15 | Wu–Xue–Zhou, IJCAI 2025 (peer-reviewed; PROP, not EF) | additive | mixed manna | values in [−1,1] | — | τ(n) (tight) | poly (secondary) | secondary: [GSW26](https://arxiv.org/abs/2609.15208), [LMS26](https://arxiv.org/abs/2607.10089) |
| 16 | Garg–Sharma–Wu 2026 (preprint; weighted PROP) | additive, weighted | mixed manna | range(I) ≤ 1 | — | τ(n) (tight) | existential; poly for fixed n | [arXiv](https://arxiv.org/abs/2609.15208) |

### Inferences
- **Where the requester's target sits.**
  - It strictly contains row 10 (additive, unit, polynomial time).
  - Its doubly-monotone part is covered by row 6 (quadratic, constructive) and row 8 (subquadratic, prime-power n, existential).
  - Its non-doubly-monotone part is covered only by row 6 at n = 2 (unit), row 8 (prime-power n), row 11 (sign-restricted subclass), and the EFk-conditional row 6′.
  - So, excluding the requester's own paper, the best general guarantee for the full class at arbitrary n ≥ 3 is unknown (non-prime-power) or existential O(n^{3/2}√log n) (prime-power). Even within doubly monotone subjective-sign binary instances, the best constructive bound is quadratic: n(n−1)/2 total and n−1 per agent.
- **What a positive answer would add.** A polynomial-time unit-subsidy result (p ∈ {0,1}^n, Σ ≤ n−1) for general subjective {−1,0,1} marginals would be new on several fronts:
  - it would generalize Barman et al. (goods, dichotomous) and Lu–Mackenzie–Suzuki (additive mixed) simultaneously;
  - it would improve Kawase's n(n−1)/2 to the optimal n−1 on binary doubly-monotone instances;
  - for non-doubly-monotone instances with n ≥ 3, it would be the first m-independent bound for arbitrary n.
  - The matching lower bound n−1 already exists (rows 3 and 5).
- **The trivial m-dependent bound.** For arbitrary valuations with v(∅)=0 and marginals in [−1,1], combining Dupré la Tour–Fujii's Lemma 5 argument with |v(S)−v(T)| ≤ |S|+|T| ≤ m (disjoint S, T) bounds every minimal payment by m, so the total is ≤ (n−1)·m for any welfare-maximizing reassignment of any partition. Kulkarni et al.'s Lemma 2.5 gives the analogous m(n−1) for monotone goods ([Kulkarni et al.](https://arxiv.org/abs/2510.13633)). This is the only bound I can certify for the fully general class at non-prime-power n ≥ 3. It is my derivation, not a published statement.
- **EF1 before payments.**
  - Known for: additive chores with unit subsidies (row 5); additive goods with unit subsidies (row 2); matroidal goods, with EFX (row 4); additive mixed but without a good bound (row 9).
  - Not established for: dichotomous goods (Barman et al. list it as future work) or additive mixed with unit subsidies (Lu et al. drop EF1). An "EF1 + unit subsidy" result for general binary mixed instances would therefore also be new on the EF1 side.
- **No known obstruction.** No negative result was found showing that unit subsidies fail for any binary class in the standard unweighted offline model. The known separations involve different models: online, weighted, or orientation constraints.

### Gaps
- **Status of EF1 for non-monotone valuations, n ≥ 3.** I confirmed it as open only as of Bérczi et al. 2020 (arXiv v1). I did not find a later resolution, but did not search exhaustively for one. If EF1 (or EFk) were proven for {−1,0,1} non-monotone valuations, Kawase's route would immediately give n−1 per agent and n(n−1)/2 total.
- **Possible missing m-independent bounds.** I could not verify whether any work gives an m-independent bound for arbitrary (mixed-sign, non-doubly-monotone) valuations at non-prime-power n. The only evidence of absence is Dupré la Tour–Suzuki's framing and my own search.
- **Unverified additions.** I did not check the journal or proceedings versions of Kawase et al. (AIJ 2025), Aziz et al. (EC 2026) or Goko et al. (GEB 2024) for results absent from the arXiv versions read.
- **Out of scope.** The requester's own arXiv 2609.14465 was deliberately excluded and not analyzed.
