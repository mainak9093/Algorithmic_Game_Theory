# Fair allocation WITHOUT money for mixed goods and chores under binary / bivalued / ternary valuations (building blocks for subsidy results)

Conventions used in these notes: **[PR]** = peer-reviewed venue (verified from the paper itself or from a reference list in another paper); **[PP]** = arXiv preprint with no venue verified. "Subjective signs" = an item may be a good for some agents and a chore for others. "Objective signs" = every item is a good for all agents or a chore for all agents (Livanos et al. call this "separable"; Hosseini–Sethia call it "objective"). "Doubly monotone" (Bhaskar–Sricharan–Vaish) = each agent splits the items into her own goods (marginal ≥ 0 with respect to every set) and her own chores (marginal ≤ 0 with respect to every set); the split may differ across agents, so signs may be subjective. "{−1,0,1} marginals" = v_i(S∪{g}) − v_i(S) ∈ {−1,0,1}. Do not confuse this with Bhaskar–Kumar–Pandit–Rakshitha's "trilean" (bundle VALUES in {0,a,b}) or with Bérczi et al.'s "Boolean" (bundle values in {0,1}). arXiv 2609.14465, the requester's own paper, came up in searches. It was deliberately left out as prior work.

---

## 1. EF1 for mixed manna: additive, doubly monotone, and non-doubly-monotone (including {−1,0,1} marginals)

### Takeaway
EF1 is solved, with polynomial-time algorithms, in two cases: additive mixed manna with subjective signs (double round-robin) and doubly monotone non-additive valuations (two-phase envy-cycle elimination with top-trading cycles). Arbitrary non-monotone valuations include every non-doubly-monotone {−1,0,1}-marginal valuation. For these, EF1 is known only for n = 2 (polynomial time) and for a few isolated subclasses (Boolean, negative-Boolean, identical trilean, separable single-peaked). For n ≥ 3 it is open even when all agents have identical valuations, and preprints from August–September 2026 still list it as open.

### Cited Findings

#### Map of EF1 existence results
| Valuation class | Signs | Result (theorem) | Existence / poly-time | Source |
|---|---|---|---|---|
| Additive | subjective | EF1 by double round-robin (Thm 1), O(max{m log m, mn}) | poly | [Aziz, Caragiannis, Igarashi, Walsh, JAAMAS 2022 [PR]](https://arxiv.org/abs/1807.10684) |
| Additive | subjective | EF1^3 = EF1 overall, among goods and among bads, by modified DRR (Thm 1) | poly | [Aleksandrov & Walsh, KI 2020 [PR]](https://arxiv.org/abs/2007.04129) |
| Additive, unequal entitlements | subjective | complete WEF1 (Thm 3.1) | poly | [Teh 2026 [PP]](https://arxiv.org/abs/2609.01580) |
| Monotone non-increasing (non-additive chores) | objective | EF1 by top-trading envy-cycle elimination (Thm 3) | poly | [Bhaskar, Sricharan, Vaish, APPROX 2021 [PR]](https://arxiv.org/abs/2012.06788) |
| Doubly monotone (non-additive) | subjective | EF1 (Thm 4, Algorithm 3) | poly (Lemma 10) | [Bhaskar et al. 2021 [PR]](https://arxiv.org/abs/2012.06788) |
| Arbitrary (non-monotone, non-additive), n = 2 | any | EF1 (Thm 1) | poly | [Bérczi et al., TCS 2024 [PR]](https://arxiv.org/abs/2006.04428) |
| Boolean (bundle values in {0,1}), normalized | n/a | EFX^0_− (Thm 5), so EF1 | existence | [Bérczi et al. [PR]](https://arxiv.org/abs/2006.04428) |
| Negative Boolean ({0,−1}), non-identical | n/a | EF1 (Thm 3) | poly | [Bhaskar, Kumar, Pandit, Rakshitha, AAMAS 2025 [PR]](https://arxiv.org/abs/2411.19881) |
| Boolean with arbitrary v_i(∅) (unnormalized) | n/a | EF1 (Thm 1) | existence | [Shah & Verma 2026 [PP]](https://arxiv.org/abs/2608.29497) |
| Identical trilean (bundle values in {0,a,b}) | n/a | EF1 (Thms 4, 13; reduction Prop 1) | existence (may need exponentially many queries) | [Bhaskar et al. AAMAS 2025 [PR]](https://arxiv.org/abs/2411.19881) |
| Separable single-peaked (SSP) | items switch from good to chore at a threshold | EF1 with common per-type thresholds (Thm 14); EF1 for 3 agents with arbitrary thresholds | existence | [Bhaskar et al. AAMAS 2025 [PR]](https://arxiv.org/abs/2411.19881) |
| {−1,0,c}-order-neutral submodular | items can flip sign | leximin is not always EF1 (Ex 6.5); for the additive {−1,0,c} case leximin is EF1 (Prop 6.6) | n/a | [Cousins, Viswanathan, Zick, WINE 2023 [PR]](https://arxiv.org/abs/2307.12516) |
| Non-negative or non-positive set functions | n/a | EF1^c_g (Thms 3.5, 4.3); EF1 itself open | existence | [Bilò, Loebl, Vinci, AAAI 2026 [PR]](https://arxiv.org/abs/2503.05695) |
| Non-negative; globally non-negative σ-subadditive | n/a | EFE3 (Thms 12, 11) | existence (not poly) | [Barman & Verma 2025 [PP]](https://arxiv.org/abs/2501.14609) |
| Arbitrary, n = 3 | any | balanced EF1^c_g (Thm 1); balanced EF1 can fail (Thm 2) | existence | [Dupré la Tour 2026 [PP]](https://arxiv.org/abs/2608.09437) |

#### Details and precise statements
- Aziz et al. allow subjective signs explicitly: "an item can be a good for one agent i (u_i(o) > 0) but a chore for another agent j (u_j(o) < 0)". Their Proposition 3 shows that plain round-robin can violate EF1 (2 agents with identical values 2, −3, −3, −3). In Theorem 1 (DRR), chores are picked first in the order 1..n; these are the items with u_i(o) ≤ 0 for all i, padded with k dummy chores so their number is a multiple of n. Items that someone values positively are then picked in the order n..1, and an agent with no positive item left takes a dummy. — [Aziz et al.](https://arxiv.org/abs/1807.10684)
- The JAAMAS version acknowledges an error in the IJCAI-2019 version, pointed out by Bérczi et al. and Bhaskar et al. It names "the existence of an EF1 allocation under arbitrary non-monotonic utilities" as the most intriguing open question. — [Aziz et al.](https://arxiv.org/abs/1807.10684)
- Bérczi et al. define EF1 for arbitrary utilities as: i's envy disappears after deleting one item from A_i ∪ A_j. Section 3.1 gives a 3-item, 2-agent example with identical non-monotone non-additive utilities on which the generalized envy-graph algorithm of the IJCAI version fails EF1. Question 12 asks whether EF1 exists for non-monotone non-additive identical utilities. The proof of Theorem 1 shows that for any ordering of the items, some prefix/suffix split, with the two bundles possibly swapped, is EF1. — [Bérczi et al.](https://arxiv.org/abs/2006.04428); published in TCS 1002:114596 (2024) per the reference list of [Dupré la Tour](https://arxiv.org/abs/2608.09437)
- Bhaskar et al. define doubly monotone instances as follows: "each agent i can partition the items as M = G_i ⊎ C_i ... an item may be a good for one agent and a chore for another." Example 1 shows that naive envy-cycle elimination (give a chore to a sink, resolve arbitrary cycles) fails EF1 even for additive chores. Lemma 6: if the envy graph has no sink, the top-trading envy graph has a cycle. In the goods phase of Algorithm 3, each item that is a good for some agent goes to a source of the envy graph restricted to the agents who see it as a good. In the chores phase, items that are chores for every agent go to a sink, after top-trading cycles are resolved. — [Bhaskar et al.](https://arxiv.org/abs/2012.06788)
- Bhaskar et al., Theorem 2: deciding whether an envy-free allocation exists is strongly NP-complete even for binary additive chores, v_ij ∈ {−1, 0}. — [Bhaskar et al.](https://arxiv.org/abs/2012.06788)
- Bhaskar–Kumar–Pandit–Rakshitha:
  - Definitions: valuations are "trilean if ... v_i(S) ∈ {0, a, b}". The authors stress: "It is important to distinguish the valuations we study from the case where any item has 0 or 1 marginal value."
  - Theorem 3 (non-identical negative Boolean): EF1 in poly time. The algorithm repeatedly assigns an inclusion-minimal set that every unallocated agent values at −1.
  - Theorem 4 (identical negative trilean {0,−1,1}): EF1. The algorithm "may need to make an exponential number of queries".
  - SSP: values are additive across item types and single-peaked in the count of each type, with thresholds θ_ij. Theorem 14 (common thresholds) holds because the doubly-monotone two-phase algorithm still works. EF1 also holds for 3 agents with arbitrary thresholds.
  - Theorem 18: EFX^+_− may not exist (2 identical agents, 3 items).
  - Open problems they state: non-identical trilean valuations; and "It remains open if an EF1 allocation exists for arbitrary valuations, even, e.g., for the case of 3 identical agents."
  — [Bhaskar et al. (AAMAS 2025 / arXiv 2411.19881)](https://arxiv.org/abs/2411.19881)
- Shah–Verma (August 2026), Table 2, still lists "Arbitrary valuations: EF1^+_− Open" and "Nonnegative (nonmonotone) valuations: Open". Their Theorem 1 combines Bérczi et al.'s Theorem 7 with Bhaskar et al.'s Theorem 3 to get EF1 for any Boolean profile. — [Shah & Verma](https://arxiv.org/abs/2608.29497)
- Dupré la Tour (August 2026) writes: "For three or more agents, the existence of this EF1 notion for general nonmonotone valuations is open even without a balance constraint". The paper also cites Dupré la Tour & Igarashi (2026) for EF1^c_g under arbitrary valuations when n is a prime power (secondary citation; I did not read that paper). — [Dupré la Tour](https://arxiv.org/abs/2608.09437)
- The mixed fair division survey's Open Question 1 is EF1 for three or more agents with arbitrary utilities over mixed goods and chores, "open even if agents have identical utility functions". — [Liu, Lu, Suzuki, Walsh, JAIR 2024 [PR]](https://arxiv.org/abs/2306.09564)
- On {−1,0,c}-submodular valuations, Cousins et al. write: "there is no clear demarcation between goods and chores; an item may provide positive marginal value when added to an empty bundle but provide negative marginal value when added to a non-empty bundle." — [Cousins et al.](https://arxiv.org/abs/2307.12516)
- Bilò et al. define EF1^c_g as removing at most one chore from one's own bundle and at most one good from the other bundle, simultaneously. Their Table 1 marks EF1 as open ("?") for general, non-negative and non-positive valuations, and as polynomial-time for objective valuations. — [Bilò et al.](https://arxiv.org/abs/2503.05695)
- Barman–Verma define EFEk as: envy is removed by moving at most k items into or out of A_i and A_j combined, so EF1 implies EFE1. EFE3 existence goes through a contiguous envy-free cake division, which is PPAD-complete to find, so the algorithm is not claimed to be polynomial. — [Barman & Verma, "Fair Division Beyond Monotone Valuations"](https://arxiv.org/abs/2501.14609)
- Weighted mixed manna: Garg–Sharma (arXiv 2410.12966) obtained WEF1T (a weaker notion) for any n and WEF1+fPO for two agents, and left complete WEF1 open even for three agents. Teh's Theorem 3.1 resolves this. — [Teh](https://arxiv.org/abs/2609.01580)
- Temporal mixed manna:
  - With at most k item types, an online cyclic rule is EF⌈k/2⌉ after every arrival (Thm 3.1), so at most 2 types gives TEF1.
  - For two agents, TEF1 for arbitrary mixed manna can be found in poly time (attributed by the authors to the full version of Elkind et al. AAMAS 2025).
  — [Choi, Li, Teh 2026 [PP]](https://arxiv.org/abs/2608.20033)

### Inferences
- **Doubly monotone {−1,0,1} marginals are solved.** These are valuations where, for each agent, every item is consistently a good (marginals in {0,1}) or consistently a chore (marginals in {−1,0}), with signs that may differ across agents. EF1 exists and is computable in polynomial time by Bhaskar et al.'s Theorem 4, given value oracles and the goods/chores split. This covers the requester's objective signed dichotomous setting and the subjective doubly monotone setting. The open territory is therefore {−1,0,1} marginals where the same agent's marginal for an item flips between +1 and −1 depending on the bundle.
- **Non-doubly-monotone {−1,0,1} marginals are only partly covered.** EF1 is known for n = 2 (Bérczi et al., Thm 1, any valuations). It is also known for SSP instances whose per-type step sizes are in {−1,0,1}: such SSP valuations have {−1,0,1} marginals and turn items from goods into chores past the threshold, and Bhaskar et al. give EF1 for common thresholds (any n) or n = 3. Order-neutral submodular valuations with c = 1 also have {−1,0,1} marginals, but no EF1 guarantee is known for them, because their leximin allocation can fail EF1.
- **Per-edge envy bounds that matter for subsidies.** With {−1,0,1} marginals, deleting one item changes a bundle's value by at most 1. So EF1 implies every envy edge has weight ≤ 1, EF1^c_g implies ≤ 2, and EFE3 implies ≤ 3. A path-weight subsidy argument would start from these per-edge bounds.
- **Available algorithmic templates:**
  - double round-robin (additive);
  - two-phase source / top-trading envy-cycle elimination (doubly monotone);
  - prefix/suffix scanning (n = 2, arbitrary);
  - inclusion-minimal set peeling (negative Boolean);
  - equality-edge envy graphs (Tao et al. for binary chores; Bu–Song–Yu for binary goods, see Q3/Q4).

### Gaps
- No source settles EF1 for n ≥ 3 with non-doubly-monotone {−1,0,1} marginals, either way. Arbitrary-valuation EF1 is open even for identical agents.
- I found no counterexample to EF1, or even to EFX, built specifically with {−1,0,1} marginals. The known non-monotone counterexamples (Bérczi Thm 2; Bhaskar et al. Thm 18; Dupré la Tour Thm 2) all use marginals of magnitude 2 or more.
- I did not verify whether the SSP (n = 3) and identical-trilean EF1 algorithms of Bhaskar et al. run in polynomial time.
- I did not read the prime-power EF1^c_g result of Dupré la Tour & Igarashi (2026) directly.

---

## 2. EF1 + PO for mixed manna (general, and binary / bivalued / ternary), plus EQ1/EQX, MNW, leximin, and envy-freeability hooks

### Takeaway
For general additive mixed manna, EF1+PO is OPEN for n ≥ 3 as of September 2026; it is known only for n = 2. Weaker or neighbouring guarantees with PO do exist: EFR-(n−1)+PO, IEF1+PO, IEF1+fPO and PROP1+PO. EF1+fPO is outright false (3 agents, 4 items, objective signs). For chores alone, EF1+PO was resolved by Mahara (SODA 2026).

For additive ternary valuations the picture is essentially complete and polynomial:
- {−α,0,β} gives EF1+PO and EFX+PO.
- {−α_i,0,α_i} gives leximin + GEF1 + PO.
- {−c_i,0,c_i} gives online EF1+PO.
- Additive {−1,0,1} is a special case of Livanos et al.'s "binary mixed goods + identical bads" class, which gets EFX0 + PO + maximum utilitarian welfare.

### Cited Findings

#### General additive mixed manna (subjective signs)
- **Two agents.** "For two agents with additive utilities, a Pareto-optimal and EF1 allocation always exists and can be computed in O(m²) time" (Thm 2, generalized adjusted winner). Items that one agent sees as a good and the other as a chore are pre-assigned to the agent who likes them. The paper asks whether EF1+PO exists for n ≥ 3. — [Aziz et al.](https://arxiv.org/abs/1807.10684)
- **Status of n ≥ 3:**
  - Survey Open Question 2: does EF1+PO exist for three or more agents with additive mixed utilities? — [Liu et al.](https://arxiv.org/abs/2306.09564)
  - "For mixed manna, the existence of EF1 and PO allocations remains open even among three agents with additive valuations" — [Barman, HV, Sethia, Suzuki, WINE 2025 [PR]](https://arxiv.org/abs/2507.03946)
  - "The existence of an EF1 and PO allocation remains open even for unweighted mixed manna" (September 2026) — [Teh](https://arxiv.org/abs/2609.01580)
- **EFR-k (Barman, HV, Sethia, Suzuki).** An allocation is EFR-k if some set R of at most k items exists such that, for each agent i, reassigning items within R makes the allocation envy-free for i.
  - Thm 3.1: EFR-(n−1) + PO always exists (KKM theorem plus perturbed weighted welfare maximization), and each per-agent envy-free reassignment A^i is itself PO.
  - Thm 4.1: computable in m^{poly(n)} time, i.e. polynomial for fixed n.
  - Thm 5.1: EFR-(n−1) + EF1 in polynomial time.
  - Thm 5.2: there are chores-only instances with no EFR-(n−2) allocation.
  - Thm A.1: deciding EFR-k is NP-hard.
  - Thms 5.4–5.5: goods admit EFR-⌊n/2⌋, and this is tight.
  - Proceedings: WINE 2025, LNCS 16266, pp. 467–483 (per the reference list of [He & Tao](https://arxiv.org/abs/2606.08872)). — [Barman et al.](https://arxiv.org/abs/2507.03946)
- **IEF1 (Barman–Verma).** IEF1 means each agent can remove its envy by adding one good to, or removing one chore from, its own bundle.
  - Thm 1: IEF1 + PO exists for additive mixed manna.
  - Thm 18: IEF1 + fPO exists.
  - Thm 28: XEF1 + PO exists.
  - Thm 20: gives a new proof of EF + fPO for divisible mixed manna.
  - IEF1 coincides with EF1 for chores, and IEF1 implies PROP1 and EFR-(n−1). The results are existence only; the authors list pseudo-polynomial algorithms as future work.
  — [Barman & Verma [PP]](https://arxiv.org/abs/2509.18673)
- **Chores only (Mahara).** Thm 1.1: EF1+PO exists for additive chores. Thm 1.2: EF1+fPO exists. Thm 1.3: polynomial time for constant n. Thm 1.4: weighted versions. The paper explicitly lists mixed manna as open. — [Mahara, SODA 2026 [PR]](https://arxiv.org/abs/2507.09544)
- **EF1 + fPO is impossible for mixed manna.** Theorem 4.3 gives a "three-agent, four-item additive mixed-manna profile" (one good valued positively by all, three chores valued negatively by all, so objective signs) with no allocation that is both EF1 and fPO, robustly in a neighbourhood. In the same neighbourhood a fixed allocation is EF1+PO. — [Mackenzie & Suzuki 2026 [PP]](https://arxiv.org/abs/2607.17811)
- **PROP1 + PO** can be computed in polynomial time for additive goods and chores (Aziz, Moulin, Sandomirskiy, ORL 2020), as restated in Theorem 4.4 of [Liu et al.](https://arxiv.org/abs/2306.09564).
- **Category constraints.** Igarashi & Meunier show PO with envy-freeness after reallocating at most n(n−1) items, under category constraints with mixed manna, using KKM. — reported by [Barman et al.](https://arxiv.org/abs/2507.03946) and [Mahara](https://arxiv.org/abs/2507.09544)
- **Welfare functions.** "There does not exist a welfare function (analogous to Nash social welfare) that guarantees EF1 for chores" (Eckart, Psomas, Verma, EC 2024). — reported by [Barman et al.](https://arxiv.org/abs/2507.03946)
- **Best of both worlds.** A randomized allocation can be envy-free in expectation with every realized allocation EF1, for mixed manna (Aziz, Bu, Lu, Mackenzie, Suzuki, Tao, Walsh 2026, arXiv 2607.10232). — reported by [Choi, Li, Teh](https://arxiv.org/abs/2608.20033)

#### Ternary / binary additive mixed manna (map)
| Class (additive) | Signs | Guarantee (theorem) | Poly | Source |
|---|---|---|---|---|
| {−α, 0, β}, common α, β > 0 | subjective | EF1^3 + PO (Thm 4); EFX + PO (Thm 5; EFX ignoring zero-valued items) | yes | [Aleksandrov & Walsh [PR]](https://arxiv.org/abs/2007.04129) |
| {−α, 0, α} | subjective | EFX^3 + PO (Thm 6) | yes | [Aleksandrov & Walsh](https://arxiv.org/abs/2007.04129) |
| absolute identical (each item has the same magnitude for all agents, signs may differ) | subjective | EFX + PO (Thm 3), O(max{m log m, mn}); EF1^3 + PO (Thm 2) | yes | [Aleksandrov & Walsh](https://arxiv.org/abs/2007.04129) |
| identical | n/a | EFX + PO (Cor 1); EFX and GEF1 by egal-sequential (Lemma 1, Thm 1) | yes | [Aleksandrov & Walsh](https://arxiv.org/abs/2007.04129); [Aziz & Rey, IJCAI 2020 [PR]](https://arxiv.org/abs/1907.09279) |
| ternary symmetric {−α_i, 0, α_i}, agent-specific α_i | subjective | Ternary Flow algorithm: leximin-optimal for normalized utilities (Lemma 5), leximin implies GEF1 (Lemma 6), so GEF1 (Thm 2), which implies EF1; PO | yes | [Aziz & Rey](https://arxiv.org/abs/1907.09279) |
| restricted mixed goods (each item someone likes has one common positive value v_j for all who like it; others arbitrary ≤ 0) + identical pure bads | subjective | EFX + PropMX + PO + max-USW (Thm 2) | yes | [Livanos, Mehta, Murhekar, AAMAS 2022 [PR, ext. abstract]](https://arxiv.org/abs/2202.02672) |
| binary mixed goods (all liked items share one positive value) + identical pure bads | subjective | EFX0 + PropMX0 + PO + max-USW (Thm 3) | yes | [Livanos et al.](https://arxiv.org/abs/2202.02672) |
| scaled ternary {−c_i, 0, c_i} | subjective | online rule that is EF1 + PO after every arrival and maximizes Σ_i v_i(A_i)/c_i (Cor 4.3) | yes (online) | [Choi, Li, Teh [PP]](https://arxiv.org/abs/2608.20033) |
| {−1, 0, c} (c a positive integer) | subjective | leximin computable in poly time (Thm 5.8); leximin is EF1 (Prop 6.6) and MMS (Prop 6.16) | yes | [Cousins et al. [PR]](https://arxiv.org/abs/2307.12516) |
| {−a_i, 0, a_i}, unequal entitlements | subjective | WMMS exists, poly, and can be fPO (Thm 4.2); every WEF1 allocation gets ≥ WMMS_i − a_i(1 − w_i/w_max) (Thm 4.4), so under equal entitlements every EF1 allocation is MMS | yes | [Teh [PP]](https://arxiv.org/abs/2609.01580) |

- **Aleksandrov–Walsh, Algorithm 2.** Items are processed in non-increasing order of the maximum absolute utility any agent has for them. A mixed item or good goes to an agent of minimum current utility among those who like it. A pure bad goes to an agent of maximum current utility. An item nobody likes but someone values at 0 goes to such an agent.
  - Prop 1: EFX^3 may not exist (2 agents, identical ternary values 2, −1, −1).
  - Prop 2: their EFX0, which also counts zero-valued items in one's own bundle, may not exist (one good and one dummy).
  - Both algorithms give every item to an agent who values it most, so the result maximizes utilitarian welfare (proof of Thm 4).
  — [Aleksandrov & Walsh](https://arxiv.org/abs/2007.04129)
- Aleksandrov–Walsh also report that the Ternary Flow algorithm can violate EFX^3 when α = β = 1, and EFX when α = 2, β = 1. — [Aleksandrov & Walsh](https://arxiv.org/abs/2007.04129)
- **Aziz–Rey, Lemma 3:** for ternary symmetric utilities, an allocation is PO if and only if every item goes to an agent with maximum normalized utility for it (positive, zero, or negative). Lemma 4 / Corollary 1: for binary goods, leximin-optimal allocations are exactly the minimum-cost flows of Darmann–Schauer's Nash-flow network, so they maximize Nash welfare. — [Aziz & Rey](https://arxiv.org/abs/1907.09279)
- **Livanos et al., class definitions and limits.** M+ are items some agent values positively; M0 are items nobody values positively and someone values at 0; M− are items everyone values negatively. "Identical bads" means every pure bad has the same value for all agents. Appendix A.2: PropMX0+PO, and hence EFX0+PO, can fail for restricted goods. Their EFX0 counts zero-valued items in the envied bundle only. — [Livanos et al.](https://arxiv.org/abs/2202.02672)
- **Equity-flavoured implication.** Garg & Sharma (AAMAS 2026) imply that, with equal entitlements, EF1 implies MMS for additive values in {−1,0,1}. — reported by [Teh](https://arxiv.org/abs/2609.01580)

#### Bivalued
- Bivalued chores admit EF1+PO in polynomial time (Ebadian–Peters–Shah, AAMAS 2022; Garg–Murhekar–Qin, AAAI 2022). EF1+PO for chores was also known for three agents and for two or three types. — reported by [Mahara](https://arxiv.org/abs/2507.09544) and [He & Tao](https://arxiv.org/abs/2606.08872)
- Chores with costs in {1, 2} admit EFX+fPO (Lin, Wu, Zhou, IJCAI 2025). — reported by [Lin, Liu, Tao, Zhou](https://arxiv.org/abs/2608.10572)
- I found no paper on EF1+PO for bivalued **mixed** manna, i.e. values {−α, β} with subjective signs and no zero value.

#### Non-additive binary marginals: EF1+PO, MNW, leximin, Lorenz domination
- **Binary supermodular costs (chores with marginal cost in {0,1}, increasing marginals),** all in polynomial time with a value oracle:
  - EF1 + PO, via a social-cost-minimizing allocation (Thm 6);
  - MMS + PO (Thm 9);
  - a Lorenz-dominating allocation (Thm 10).
  - Thm 11: these notions are incomparable, and in one instance no Lorenz-dominating allocation is EF1 or MMS.
  — [Barman, Narayan, Verma, AAMAS 2023 [PR, ext. abstract]](https://arxiv.org/abs/2302.11530)
- **Binary goods:**
  - Binary additive goods: "maximum Nash welfare with a fixed tie-breaking rule is simultaneously weakly group-strategyproof, EF1, and Pareto optimal" (Halpern et al., WINE 2020).
  - Matroid-rank goods: Babaioff–Ezra–Feige's truthful mechanism "returns a Lorenz-dominating allocation, which is in particular EFX and of maximum Nash welfare".
  — both reported by [Shah & Verma](https://arxiv.org/abs/2608.29497)
- Bérczi et al. summarize Benabbou et al. (SAGT 2020) as: "utilitarian socially optimal (hence Pareto optimal), leximin, and maximum Nash welfare allocations are all EF1 if in addition the utility functions have binary marginal gain". This is quoted verbatim; I did not check the "all utilitarian-optimal allocations" part against Benabbou et al. directly. — [Bérczi et al.](https://arxiv.org/abs/2006.04428)
- **Cousins et al. on {−1,0,c}-ONSUB** (submodular, marginals in {−1,0,c}, order-neutral):
  - Thm 5.8: a leximin allocation can be computed efficiently, and Algorithm 1 outputs a maximum-utilitarian-welfare allocation (corollary after Thm 5.8).
  - Prop 6.3: leximin is PROP1. Prop 6.17: leximin is Lorenz dominating.
  - Ex 6.5: leximin is not EF1. Ex 6.7: leximin gives no approximate MMS.
  - Thm 7.1: computing leximin is NP-hard for additive {−p, q} with p, q coprime and p ≥ 3.
  - "the Nash welfare of an allocation ... loses its meaning in settings where agent utilities can be negative." Thm 6.18 says that when all agents can simultaneously get positive utility, Lorenz dominance yields optimal non-negative welfare objectives (such as Nash welfare); otherwise the negative part is Lorenz-dominant.
  — [Cousins et al.](https://arxiv.org/abs/2307.12516)
- **Submodular goods.** EF1+PO can fail for two agents with eight goods and monotone submodular valuations (Thm 1.1). For common-weight matroid-rank valuations, EF1+PO exists (Cor 4.5), but EF1+fPO can fail (Thm 4.2). — [Mackenzie & Suzuki](https://arxiv.org/abs/2607.17811)

#### Equitability: EQ1 / EQX
- **Hosseini–Sethia** (additive mixed manna):
  - Ex 3.1: EQ1 can fail with {−1, 1} subjective values (2 agents, 2 items). Thm 3.2: deciding whether an EQ1 allocation exists is NP-complete.
  - Prop 3.3: for objective additive valuations, EQ1 exists and is polynomial.
  - Thm 4.4: for normalized {−1, 0, 1} valuations, EQ1 is polynomial. EQX exists and is computable for normalized {−1, 1} subjective valuations, any n.
  - Ex 5.1: EQ1+PO can fail even for type-normalized {−1, 1}. Thm 5.2: deciding EQ1+PO is strongly NP-hard.
  - Thm 5.3: for normalized {−1, 0, 1}, a polynomial algorithm finds an EQ1+PO allocation whenever one exists.
  - Prop 5.5: identical valuations admit EQ1+PO. Thm 5.6: two agents with type-normalized {−1, 0, 1} admit EQ1+PO.
  — [Hosseini & Sethia [PP; venue not verified]](https://arxiv.org/abs/2501.06799)
- **Hosseini–HV–Sethia–Yadav** (general, possibly non-monotone valuations, assuming all agents agree on the sign of the grand bundle):
  - Thm 3.1: two agents, EQ1 in poly time.
  - Thms 4.4 / 4.5: submodular or doubly monotone valuations with a non-negatively valued grand bundle, EQ1 in poly time.
  - Thm 5.1: non-negative valuations, EQ1 exists.
  - Thm 3.2: supermodular valuations with n ≥ 3, EQ1 can fail and deciding it is NP-complete.
  - Thm 6.1 / Cor 6.2: identical subadditive valuations, EQ1 exists, hence EF1.
  — [Hosseini, HV, Sethia, Yadav [PP]](https://arxiv.org/abs/2511.07395)
- **Bilò et al.:**
  - EQX^c_g exists for objective valuations (Thm E.1, pseudo-polynomial; Thm E.3, greedy when additive).
  - EQ1 for non-additive objective valuations (Thm E.2).
  - They report Barman–Bhaskar–Pandit–Pyne (AAAI 2024): EQX exists for monotone non-decreasing valuations, and without monotonicity EQX may fail even for two agents with additive valuations.
  — [Bilò et al.](https://arxiv.org/abs/2503.05695)

#### Envy-freeability hooks (for layering subsidies on top of the allocations above)
- **Halpern–Shah characterization.** For an allocation A, these are equivalent: (a) A is envy-freeable; (b) A maximizes utilitarian welfare over all reassignments of its bundles; (c) the envy graph has no positive-weight directed cycle. The minimum subsidies are the maximum weights of paths starting at each agent. Lu, Mackenzie and Suzuki note that the characterization "also works for the setting with mixed goods and chores" (their Thm 2.2). — [Lu, Mackenzie, Suzuki 2026 [PP]](https://arxiv.org/abs/2607.10089); original: [Halpern & Shah, SAGT 2019 [PR]](https://www.cs.toronto.edu/~nisarg/papers/subsidy.pdf)
- **One dollar each for mixed manna.** Thm 1.1: for additive utilities in [−1, 1] with subjective signs, an envy-free outcome with every p_i ∈ [0, 1] exists and can be computed in polynomial time, so total subsidy is at most n − 1.
  - The construction deliberately does not maintain EF1: "requiring the allocation to remain EF1 is too restrictive and is incompatible with the operations used later in the proof".
  - Prop 3.1 (subjective goods only, iterated maximum-weight matching) and Prop 3.2 (objective chores only, iterated maximum-weight perfect matching) each give per-agent subsidy at most 1.
  — [Lu, Mackenzie, Suzuki](https://arxiv.org/abs/2607.10089)
- **EF1 together with envy-freeability.** "Every instance of indivisible mixed manna admits an allocation that is both EF1 and envy-freeable" (Aziz, Lu, Mackenzie, Suzuki, EC 2026, arXiv 2511.04891). However, "even in goods-only instances, an allocation may be both EF1 and envy-freeable while its heaviest envy path has weight n − 1". — reported by [Lu, Mackenzie, Suzuki](https://arxiv.org/abs/2607.10089)

### Inferences
- **Additive {−1,0,1} with subjective signs is essentially fully solved without money.** It fits Livanos et al.'s "binary mixed goods + identical pure bads" class: every liked item is liked at value 1, items everyone values at −1 are identical bads, and the rest are dummy bads. So their Thm 3 gives EFX0 (goods-side) + PO + max-USW in polynomial time. In addition:
  - Aleksandrov–Walsh Thm 5 gives EFX + PO;
  - Aziz–Rey Thm 2 gives leximin + GEF1 + PO;
  - Cousins et al. Prop 6.6 (c = 1) shows leximin is EF1;
  - Teh / Garg–Sharma give EF1 ⇒ MMS.
- **For additive {−1,0,1}, PO = max-USW, so every PO allocation is envy-freeable.** By Aziz–Rey Lemma 3 with α_i = 1, PO holds exactly when every item goes to an agent who values it most, which is the same as maximizing utilitarian welfare. Halpern–Shah (b) then makes every PO allocation envy-freeable. Adding EF1 bounds each envy edge by 1. No source bounds the full envy-path weights for these allocations by 1, which is what p ∈ {0,1}^n would require.
- **Which algorithms land in max-USW.** The Aleksandrov–Walsh, Livanos et al., Cousins et al. (Algorithm 1), Tao et al. (binary additive chores, minimum social cost) and Barman–Narayan–Verma (minimum social cost) outputs are all utilitarian-optimal, hence envy-freeable. The KKM / weighted-welfare constructions (Mahara; Barman–Verma; Barman et al.) output weighted-welfare maximizers (fPO). Those are not utilitarian-optimal in general, so envy-freeability does not follow automatically.
- **EF1+PO for mixed manna cannot go through fPO.** By Mackenzie–Suzuki Thm 4.3, any existence proof of EF1+PO for mixed manna cannot work by finding an fPO / weighted-welfare-maximizing EF1 allocation. This is consistent with Barman–Verma getting IEF1+fPO, since IEF1 is weaker than EF1 for mixed manna.
- **Agent-specific magnitudes break the PO = max-USW link.** With {−α_i, 0, α_i}, PO in normalized utilities need not maximize utilitarian welfare in the original utilities, so envy-freeability in original units is not automatic.

### Gaps
- EF1+PO for additive mixed manna with n ≥ 3 is open.
- I found no EF1+PO result for non-additive doubly monotone {−1,0,1}-marginal mixed valuations (goods side matroid-rank, chores side matroid-nullity, or general binary marginals).
- I found no EF1+PO result for bivalued mixed manna with subjective signs.
- None of the ternary algorithms come with a bound on envy-path weights.
- Venues not verified: Barman–Verma (IEF1) and Hosseini–Sethia.
- I did not read Aziz–Lu–Mackenzie–Suzuki (EC 2026) directly.

---

## 3. EFX for mixed binary/ternary valuations, and binary goods / binary chores as building blocks

### Takeaway
EFX for mixed manna fails in general, even for additive valuations. Additive tri-valued chores with n ≥ 4 give a counterexample (June 2026), and so do objective goods and chores with lexicographic preferences. EFX does hold together with PO for additive ternary, absolute-identical and identical mixed instances. On the non-additive side:
- Binary-marginal goods always admit EFX in polynomial time.
- Binary chores admit EFX when costs are additive (together with PO) or cancelable.
- EFX can fail for binary XOS and binary supermodular chores (August 2026). So the requester's negative-dichotomous chore class does **not** guarantee EFX.
- Binary submodular chores remain open.

### Cited Findings

#### Map
| Class | Result (theorem) | Source |
|---|---|---|
| Additive chores, tri-valued, n ≥ 4 | no EFX (Thm 1); uses 3 chore types and 2 agent types, both tight | [He & Tao 2026 [PP]](https://arxiv.org/abs/2606.08872) |
| Bivalued chores {1, r}, n ≥ 4, r > ⌈n/2⌉+1 | every EFX allocation fails PO (Thm 2); for n = 4, EFX exists (Thm 3) | [He & Tao](https://arxiv.org/abs/2606.08872) |
| Objective goods + chores, lexicographic preferences | EFX may fail (Hosseini, Sikdar, Vaish, Xia, AAMAS 2023) | reported by [Liu et al.](https://arxiv.org/abs/2306.09564) and [He & Tao](https://arxiv.org/abs/2606.08872) |
| Separable lexicographic | EFX + PO in poly time (Hosseini, Mammadov, Wąs, IJCAI 2023) | reported by [Liu et al.](https://arxiv.org/abs/2306.09564) |
| Additive {−α, 0, β} | EFX + PO, poly (Thm 5) | [Aleksandrov & Walsh](https://arxiv.org/abs/2007.04129) |
| Additive {−1, 0, 1} ("tertiary") | EF1 implies EFX, so double round-robin gives EFX | [Bérczi et al.](https://arxiv.org/abs/2006.04428) |
| Identical additive mixed | EFX by egal-sequential (Lemma 1) | [Aziz & Rey](https://arxiv.org/abs/1907.09279) |
| Two agents, additive mixed | EFX via identical-valuation EFX plus Plaut–Roughgarden cut-and-choose (as stated in Bérczi et al.'s introduction) | [Bérczi et al.](https://arxiv.org/abs/2006.04428) |
| Binary mixed goods + identical bads | EFX0 + PO, poly (Thm 3) | [Livanos et al.](https://arxiv.org/abs/2202.02672) |
| Monotone goods with binary marginals (not necessarily submodular) | EFX (any-item version), poly (Thm 3.1) | [Bu, Song, Yu, IJTCS-FAW 2023 [PR]](https://arxiv.org/abs/2308.05503) |
| Binary submodular (matroid-rank) goods | EFX + MNW (Lorenz-dominating mechanism of Babaioff et al.) | reported by [Shah & Verma](https://arxiv.org/abs/2608.29497) |
| Binary additive chores | EFX + PO, poly (Thm 3.1) | [Tao, Wu, Yu, Zhou, TCS 1042:115248 (2025) [PR]](https://arxiv.org/abs/2308.12177) |
| Binary additive chores, unequal entitlements | WEFX + fPO, poly (Thm 3.5); lottery that is ex-ante EF + fPO with every realization EFX + fPO (Thm 4.8) | [Lin, Wu, Zhou 2026 [PP]](https://arxiv.org/abs/2609.13970) |
| Binary cancelable chores | EFX, poly (Thm 4.1); EFX incompatible with PO for every n ≥ 2 (Thm 4.8) | [Tao et al.](https://arxiv.org/abs/2308.12177) |
| Binary submodular chores | 2-EFX, poly (Thm D.1 / Cor D.2); exact EFX open | [Tao et al.](https://arxiv.org/abs/2308.12177); [Lin, Liu, Tao, Zhou](https://arxiv.org/abs/2608.10572) |
| Binary XOS chores (max of two binary additive functions) | no EFX (Thm 1; 18 agents, 53 chores) | [Lin, Liu, Tao, Zhou 2026 [PP]](https://arxiv.org/abs/2608.10572) |
| Binary supermodular chores (nullity of a rank-2 partition matroid) | no EFX (Thm 2; same gadget) | [Lin, Liu, Tao, Zhou](https://arxiv.org/abs/2608.10572) |
| Binary supermodular chores | PO + β-EFkX impossible for every β ∈ (0,1] and k ≥ 1, even with identical costs (Thm 12); identical binary-marginal costs admit EFX in poly time (Thm 13, Add-and-Fix) | [Barman, Narayan, Verma](https://arxiv.org/abs/2302.11530) |
| Non-monotone, non-additive, identical, n = 2 | EFX^+_− may fail (Thm 2) | [Bérczi et al.](https://arxiv.org/abs/2006.04428) |
| Identical negative trilean, or identical SSP, n = 2 | EFX^+_− may fail (Thm 18) | [Bhaskar et al. 2024](https://arxiv.org/abs/2411.19881) |
| Boolean (normalized) | EFX^0_− exists (Thm 5); identical negative Boolean: EFX^+_0 in poly time (Thm 6) | [Bérczi et al.](https://arxiv.org/abs/2006.04428) |
| Negative Boolean, non-identical | EFX^+_0 exists, poly in the value-oracle model (Thm 3); resolves Bérczi Question 16 | [Shah & Verma](https://arxiv.org/abs/2608.29497) |
| Ternary identical, 2 agents | EFX^3 and the Aleksandrov–Walsh EFX0 may fail (Props 1–2) | [Aleksandrov & Walsh](https://arxiv.org/abs/2007.04129) |

#### Details
- **EFX definitions for mixed manna differ across papers.**
  - Aziz et al.: i's envy toward j must vanish after removing any good from j's bundle that i values positively, or any chore from i's own bundle. They posed EFX existence for mixed manna as open. — [Aziz et al.](https://arxiv.org/abs/1807.10684)
  - Bérczi et al. define four variants (EFX^0_0, EFX^0_−, EFX^+_0, EFX^+_−) depending on whether zero-marginal items are tested on each side. EFX^+_− and EFX^0_− match the usual EFX and EFX0 for monotone additive goods. — [Bérczi et al.](https://arxiv.org/abs/2006.04428)
  - Aleksandrov–Walsh's EFX ignores zero-valued items, and their EFX0 counts zero-valued items on both sides. Livanos et al.'s EFX0 counts zero-valued items in the envied bundle only. — [Aleksandrov & Walsh](https://arxiv.org/abs/2007.04129); [Livanos et al.](https://arxiv.org/abs/2202.02672)
- **Bu–Song–Yu technique.** They build on Chaudhury et al.'s charity envy-graph. The new ingredients are "pre-envy" edges, meaning v_j(A_j) = v_j(A_i), which they note equal the "equality edge" of Bei et al.; "safe bundles"; and "maximal envy edges". They also give an example where every maximum-Nash-welfare allocation fails EFX for binary non-submodular valuations. — [Bu, Song, Yu](https://arxiv.org/abs/2308.05503)
- **Lin–Liu–Tao–Zhou.**
  - The two cost constructions are c_i(S) = max{z_i(S), o_i(S)} (binary XOS) and c_i(S) = |S| − r_i(S), with r_i the rank of a two-block partition matroid (binary supermodular).
  - The proof uses a projection-matching property of 53 binary words of length 18, and is verified in Lean 4. The word construction was produced with an AI model.
  - Their Fig. 1 frontier, all for binary marginals: additive EFX (yes), cancelable EFX (yes), submodular (open), XOS (no), subadditive (no, via XOS), supermodular (no).
  — [Lin et al.](https://arxiv.org/abs/2608.10572)
- **Other chore EFX results** (reported by Lin et al.; I did not read the originals):
  - EFX exists for two types of chores, leveled preferences, lexicographic preferences, identical ordering, m ≤ 2n (Garg–Murhekar–Qin, STOC 2025; Kobayashi–Mahara–Sakamoto, TCS 2025), and restricted additive costs (Lin–Wu–Zhou, WWW 2026).
  - 2-EFX exists for additive chores (Garg–Murhekar, AAAI 2026).
  - EFX can fail for superadditive chores with 3 agents and 6 chores (Christoforidis–Santorinaios, IJCAI 2024).
  — [Lin, Liu, Tao, Zhou](https://arxiv.org/abs/2608.10572)
- **Goods.** EFX for additive goods remains open for n ≥ 4. Counterexamples now exist for submodular goods (Akrami et al. 2026; Mackenzie–Suzuki 2026). — reported by [He & Tao](https://arxiv.org/abs/2606.08872)

### Inferences
- **EFX is not a universal target for the requester's base class.** Lin et al.'s supermodular and XOS counterexamples have marginals in {−1,0} on the valuation side, so EFX can fail for negative dichotomous non-additive chores. EF1 is therefore the right "before payments" fairness target. EFX survives only for additive, cancelable and possibly submodular dichotomous chores.
- **Non-existence is inherited upwards.** Any mixed class that contains binary XOS or binary supermodular chores, or additive tri-valued chores, also loses EFX. Additive {−1,0,1} mixed manna is an island where EFX+PO (and even goods-side EFX0+PO) exists in polynomial time.
- **A shared device.** Both binary-marginal EFX/EF constructions, Bu–Song–Yu for goods and Tao et al. for chores, rely on "equality / pre-envy" edges (agent i values bundle j exactly as much as its own). That is the natural primitive for {−1,0,1} marginals, where envy jumps in unit steps.

### Gaps
- Open: EFX for binary submodular chores; EFX for 3 agents with additive chores; EFX for bivalued chores with n ≥ 5.
- I found no counterexample to EFX (any variant) for two agents with non-doubly-monotone {−1,0,1}-marginal valuations. The known two-agent non-monotone counterexamples have marginals of magnitude 2.
- Hosseini–Sikdar–Vaish–Xia and Hosseini–Mammadov–Wąs are cited only through the survey and through He–Tao.

---

## 4. Envy-free partial allocations / "charity" for chores and mixed items

### Takeaway
For chores, the only exact envy-free partial-allocation result I found is Tao et al.'s: general monotone binary-marginal costs, at most n − 1 chores left unallocated, polynomial time. The n − 1 bound is tight. For goods, EFX with charity (at most n − 1 goods unallocated and nobody envies the pool) is a classical result. For mixed manna I found **no** partial-allocation analogue. The closest relatives are "reallocation" relaxations (EFR-(n−1), tight for chores; IEF1) and fractional sharing of at most n − 1 items.

### Cited Findings
- **Tao, Wu, Yu, Zhou, Theorem 5.1:** "For cost functions with binary marginals, there exists a partial allocation that is envy-free and leaves at most n − 1 items unallocated. Moreover, such an allocation can be computed in polynomial time."
  - Definition 5.2 (equality graph): an edge (i, j) exists exactly when i's cost for its own bundle equals i's cost for j's bundle, i.e. i is "about to envy" j. The algorithm starts from empty bundles, where the equality graph is complete, and applies three update rules.
    1. Give an unallocated item with zero marginal cost to an agent who has that zero marginal.
    2. If an edge (i, j) lies on a cycle C and adding item e to X_j costs i nothing, rotate the bundles along C and give e to i.
    3. Otherwise, take a tail strongly connected component S (one with no outgoing edges) and give each agent in S an arbitrary item. If fewer than |S| items remain, stop.
  - Why envy-freeness is preserved: for i in S and k outside S, c_i(X_i) ≤ c_i(X_k) − 1, so one more unit of cost creates no envy. Inside S, rules 1–2 failing means c_i(e | X_i) = c_i(e | X_j) = 1, so both sides go up by 1.
  - The same algorithm yields a complete 2-EFX allocation for binary submodular costs (Thm D.1). The authors write: "we do not know if complete EFX allocations always exist, even for the more special case with submodular binary cost functions."
  — [Tao et al.](https://arxiv.org/abs/2308.12177)
- **Goods with charity:**
  - Chaudhury, Kavitha, Mehlhorn, Sgouritsa (SICOMP 2021): "a pseudo-polynomial-time algorithm that computes a partial EFX allocation such that the number of the unallocated items is at most n − 1 and no one envies the unallocated bundle".
  - Caragiannis, Gravin, Huang (EC 2019): a partial EFX allocation achieving a 0.5 approximation to optimal Nash welfare.
  - Berger, Cohen, Feldman, Fiat (AAAI 2022): for four agents, partial EFX with at most one unallocated good.
  - Bu–Song–Yu show that with binary marginals the leftover items can always be allocated, giving complete EFX.
  — reported by [Bu, Song, Yu](https://arxiv.org/abs/2308.05503)
- **Mixed-manna relatives (reassignment or fractional sharing, not unallocated items):**
  - EFR-(n−1) + PO exists (Thm 3.1). EFR-(n−1) + EF1 is polynomial (Thm 5.1). It is tight for chores: some chores-only instances admit no EFR-(n−2) (Thm 5.2). — [Barman et al.](https://arxiv.org/abs/2507.03946)
  - Sandomirskiy & Segal-Halevi (OR 2022) prove envy-free and PO allocations of divisible mixed manna in which at most n − 1 items are shared fractionally. Barman et al.'s Appendix B shows that one cannot always round n − 1 fractionally assigned chores into an EFR-(n−1) integral allocation. — [Barman et al.](https://arxiv.org/abs/2507.03946)
  - IEF1 + PO implies EFR-(n−1) + PO (footnote 3). — [Barman & Verma](https://arxiv.org/abs/2509.18673)
  - Igarashi & Meunier: envy-freeness after reassigning at most n² − n items, together with PO, under category constraints with mixed manna. — reported by [Barman et al.](https://arxiv.org/abs/2507.03946)
- **Lotteries.** For binary cancelable chores, a polynomial-time lottery is ex-ante EF with every realization EFX (Thm 4.9). For weighted binary additive chores, WEFX + fPO is achievable (Thm 3.5), but WEFX can fail for weighted cancelable binary costs (Ex 3.6). — [Lin, Wu, Zhou](https://arxiv.org/abs/2609.13970)

### Inferences
- **Tao et al.'s n − 1 is tight.** Take n agents and n − 1 chores, each costing 1 to every agent (additive binary). Envy-freeness with identical costs forces equal bundle costs, so any envy-free partial allocation must leave all n − 1 chores unallocated. This matches the tightness of EFR-(n−1) for chores (Barman et al. Thm 5.2) and the n − 1 total-subsidy benchmark.
- **The tail-component argument needs monotone costs.** It uses the fact that every remaining item adds 0 or +1 to any bundle's cost, so the inequality c_i(X_i) ≤ c_i(X_k) − 1 survives one more unit. With non-doubly-monotone {−1,0,1} marginals, adding an item can lower an agent's value for her own bundle, or move another agent's bundle up or down by 1 in her eyes, so rule 3's invariant breaks. A mixed analogue would plausibly need a goods-side step: allocating to sources, as in Bhaskar et al.'s goods phase, or "safe bundles" as in Bu–Song–Yu. That two-phase structure is only justified for doubly monotone valuations. This is my speculation, not a cited result.
- **"Charity" means different things for goods and chores.** Leaving a good unallocated is donation; leaving a chore unallocated means the task is not done. For a mixed analogue, the "≤ n − 1 unallocated items" would sensibly be chores-for-everyone (as in Tao et al.), while any item that is a good for someone could always be given away. This is again an inference.

### Gaps
- I found no envy-free partial allocation with at most n − 1 unallocated items for mixed signs, subjective or objective.
- I found no EFX-with-charity result for chores beyond the binary case.
- I found nothing that combines Tao et al.'s chores rule with a goods phase for doubly monotone {−1,0,1} valuations.
- I did not read Chaudhury et al., Caragiannis–Gravin–Huang, Berger et al. or Sandomirskiy–Segal-Halevi directly.

---

## 5. Matroidal / M♮-type structure for binary marginals, and analogues for {−1,0,1} marginals

### Takeaway
Monotone binary-marginal valuations have clean matroid structure on both sides:
- binary submodular goods are exactly matroid-rank functions;
- binary supermodular costs are matroid nullities, |S| − rank(S).

This structure drives the known leximin, MNW, Lorenz-domination and EF1+PO results. For {−1,0,1} marginals, the only structured class that has been studied is Cousins–Viswanathan–Zick's order-neutral submodular {−1,0,c} valuations; leximin is computable in polynomial time via a three-level decomposition into binary-submodular "clean" allocations. I found **no** fair-division work on M♮-concave or valuated-matroid valuations with {−1,0,1} marginals, nor on "matroid rank minus matroid nullity" mixed valuations.

### Cited Findings
- **Binary submodular = matroid rank (goods).** Shah–Verma describe "submodular valuations with binary marginals, also known as matroid-rank valuations" and Babaioff–Ezra–Feige's Lorenz-dominating, EFX, MNW mechanism, with ex-ante envy-freeness via random priorities. Tao et al. write that "binary submodular (or matroid-rank) valuations ... EFX and PO allocations always exist" and mention Viswanathan–Zick's Yankee Swap as a faster algorithm. — [Shah & Verma](https://arxiv.org/abs/2608.29497); [Tao et al.](https://arxiv.org/abs/2308.12177)
- **Binary supermodular costs = matroid nullity (chores).** Barman–Narayan–Verma present "a useful connection between binary supermodular cost functions and the well-known matroid rank valuation functions (Lemma 2)", with r_i(S) = |S| − c_i(S) a rank function. Minimax shares are τ_i = ⌈(m − r_{i×n}([m]))/n⌉ via the n-fold matroid union (Lemma 7), and the matroid union theorem gives Σ_i τ_i ≥ minimum social cost (Lemma 8). — [Barman, Narayan, Verma](https://arxiv.org/abs/2302.11530)
- **The EFX counterexample sits inside this structure.** Lin et al. note "c_i(S) = |S| − r_i(S) ... our impossibility holds even for partition-matroid nullity functions". — [Lin et al.](https://arxiv.org/abs/2608.10572)
- **Inclusions among binary-marginal cost classes.** Binary additive ⊊ binary cancelable ⊊ binary submodular (Thms 2.1–2.2; the second inclusion is specific to binary marginals). Prop 2.4 gives structural facts for binary submodular costs, e.g. if c(S) = 1 with |S| ≥ 2, then some e ∈ S has c(S − e) = 1. — [Tao et al.](https://arxiv.org/abs/2308.12177)
- **Cousins–Viswanathan–Zick's {−1,0,c}-ONSUB:**
  - Definitions: A-SUB is submodular with every marginal in A. Order-neutral means the sorted vector of telescoping marginals of any bundle does not depend on the order in which items are added.
  - Not every {−1,0,1}-submodular function is order-neutral. Their example: v({o1}) = 0, v({o2}) = 1, v({o1,o2}) = 0, whose marginals all lie in {−1,0,1}.
  - Prop 8.1: every two-valued A-SUB function is order-neutral, so {0,1}-SUB, {−1,0}-SUB and {−1,1}-SUB are.
  - Lemma 4.1: any allocation decomposes into X^c, X^0 and X^{−1} (items contributing c, 0, −1) via decompositions with respect to binary submodular functions β^0 and β^c ("clean" allocations).
  - Leximin is computed by weighted path augmentation on exchange graphs (Thms 4.4, 4.5, 5.8). The same Algorithm 1 also computes leximin for {−1,0}-SUB and {0,1}-SUB.
  - Prop 8.5: {0,1}-OXS ⊊ {0,1}-SUB. The authors conjecture, without proof, that Rado and gross-substitutes valuations strictly contain ONSUB.
  - Open: leximin for {−c,0,1}-ONSUB and {−2,0,c}-ONSUB.
  — [Cousins et al.](https://arxiv.org/abs/2307.12516)
- **Mackenzie–Suzuki on matroid-type goods.** Gross substitutes include OXS and weighted matroid-rank valuations. For common-weight matroid rank, EF1+PO exists with a leximin-optimal choice (Cor 4.5, via a "common-envelope" condition), but EF1+fPO fails (Thm 4.2). They conjecture EF1+PO for all weighted matroid-rank valuations (Conjecture 4.1). For general submodular goods, EF1+PO fails (Thm 1.1). — [Mackenzie & Suzuki](https://arxiv.org/abs/2607.17811)
- **Matroid constraints with Boolean valuations.** Shah–Verma characterize which matroids guarantee a feasible EF1 allocation for two agents with Boolean valuations (Thm 7, linked to the White/Gabow reconfiguration conjectures). Under a partition matroid, EF1 and PO can be incompatible (Prop 8). — [Shah & Verma](https://arxiv.org/abs/2608.29497)

### Inferences
- **A natural doubly monotone "matroidal" {−1,0,1} class.** Let v_i(S) = r_i(S ∩ G_i) − (#(S ∩ C_i) − ρ_i(S ∩ C_i)), where r_i is a matroid rank on agent i's goods and ρ_i a matroid rank on her chores; this is matroid rank minus matroid nullity, separable across the two parts. EF1 follows from Bhaskar et al.'s Thm 4. Leximin, PO, MNW or Lorenz-type results would require combining the goods-side machinery (Babaioff et al.; Viswanathan–Zick) with the chores-side machinery (Barman–Narayan–Verma). I found no source that does this.
- **Order-neutrality is the operative property.** Cousins et al.'s ONSUB with c = 1 is a submodular {−1,0,1} class that is **not** doubly monotone. Because non-order-neutral {−1,0,1}-SUB functions exist, the property that makes path augmentation and decomposition work is order-neutrality, not just having {−1,0,1} marginals.
- **What ONSUB gives the requester, and what it doesn't.** For a subjective-sign, non-doubly-monotone target, the ONSUB decomposition is the closest existing matroid-like tool, and it yields utilitarian-optimal (hence envy-freeable) leximin allocations. Its leximin output can fail EF1, so it is a PO/USW building block, not an EF1 one.

### Gaps
- I found no fair-division paper on M♮-concave or valuated-matroid valuations with marginals in {−1,0,1}, or on "matroid rank minus matroid rank" valuations.
- The equivalence of gross substitutes and M♮-concave functions (Fujishige–Yang) is background knowledge I did not re-verify here.
- Whether ONSUB is contained in gross substitutes or Rado valuations is open (Cousins et al.).
- The complexity of leximin, and the existence of EF1, for general (non-order-neutral) {−1,0,1}-SUB valuations are unknown.
- The specific Viswanathan–Zick binary-supermodular-chores paper cited by Cousins et al. ("Viswanathan and Zick 2023c") was not located or read.
