# Paper Map — Readings 1–9

**Companion to `glossary_fair_division_subsidies.md`.** One entry per paper: what it
does, what it improves on, and what it leaves open. Notation is the Project's (see
glossary §0); bounds are restated in it, so they may not match the source's letters.

**Read this first.** The file numbering `Reading_1 … Reading_9` is *not* a chronology and
*not* a linear improvement chain. The corpus is a small DAG with one trunk, three
branches, and one paper that answers a different question entirely. §0 gives the shape;
§§1–9 give the papers; §10 gives the bound tables.

---

## 0. The actual structure

Publication order, which is what the improvement relation follows:

| Reading | Year | Short name | Setting |
|---|---|---|---|
| R1 | 2019 (SAGT) | Halpern–Shah | unweighted, additive, **money** |
| R2 | 2019/20 (EC) | Brustle et al. | unweighted, additive + monotone, **money** |
| R3 | 2022 | Barman et al. | unweighted, **dichotomous**, money |
| R5 | 2023 (FAW) | Bu–Song–Yu | unweighted, **binary**, *no money* |
| R9 | 2023 (AAAI'24) | Kawase et al. | unweighted, **doubly monotone**, money |
| R8 | 2024 (AAAI) / 2025 (SCW) | Montanari et al. | **weighted**, submodular, *no money* |
| R7 | 2024 | Dai et al. | **weighted**, house allocation, money |
| R4 | 2024 | Klein Elmalem et al. | **weighted**, additive, money |
| R6 | 2025 | Klein Elmalem, Aziz et al. | **weighted**, monotone + subclasses, money |

Envy-freeness fails for indivisible goods. There are exactly two repairs in this corpus,
and the split is the main organizing fact:

- **(A) Add money.** Keep EF exact; buy off the envy with an outside subsidy $p$. Ask
  how much. → R1, R2, R3, R9 (equal entitlements); R4, R6, R7 (unequal).
- **(B) Weaken the notion.** No money; relax EF to EF1 / EFX / WEF$(x,1-x)$ / TWEF /
  WMEF and ask what still exists. → R5 (unweighted, EFX); R8 (weighted, submodular).

The dependency graph:

```
                        R1 (characterization + conjectures)
                         │
                         ▼
                        R2 (proves both conjectures; opens monotone case)
                    ┌────┼─────────────┐
                    ▼    ▼             ▼
                   R3   R9        [weights break everything]
             (dichotomous) (doubly monotone,                │
                            better constants)         ┌─────┴─────┐
                                                      ▼           ▼
                                                     R4 ───► R6   R7
                                                  (additive) (general) (house alloc.)

    separate branch, no money:      R5 (EFX, binary)      R8 (WEF relaxations, submodular)
```

Three relationships worth naming up front, because they are where the corpus is doing
real work rather than accumulating:

1. **R2 answers R1's conjectures.** This is the one clean "paper $k+1$ closes paper $k$"
   link in the set.
2. **R9 does not beat R2 by finding a better algorithm — it changes the input.** R2
   builds a special allocation and subsidizes it. R9 takes *any* EF1 allocation as given
   and shows the subsidy needed is small. That decoupling is why the bound halves and
   why the result simultaneously covers chores.
3. **R4/R6/R7 are not "R2 with weights."** R1's characterization theorem — the engine
   everything unweighted runs on — is *false* under entitlements. The weighted papers
   had to rebuild the foundation, and one of them (R7) found that under a cardinality
   constraint the foundation cannot be rebuilt at all.

---

## 1. R1 — Halpern & Shah, *Fair Division with Subsidy* (SAGT 2019)

**The founding paper of the subsidy line.** Setting: $n$ agents, additive valuations,
$v_i(g) \in [0,1]$, subsidy $p \ge 0$ from a third party, quasi-linear utilities.

**What it does.**

- **The characterization (the paper's lasting contribution).** $A$ is envy-freeable
  $\iff$ $A$ is reassignment-stable (no permutation of $A$'s own bundles among the same
  agents raises $\sum_i v_i(A_i)$) $\iff$ the envy graph $G_A$ has no positive-weight
  directed cycle. Envy-freeability is therefore a property of the allocation alone, and
  it is fundamentally an *efficiency* condition, not a fairness one.
- **Minimum subsidy.** $p^*_i$ = the max-weight directed path out of $i$ in $G_A$;
  strongly polynomial to compute (Floyd–Warshall) once no positive cycle exists.
- **Given allocation.** Worst-case minimum subsidy is $\Theta(nm)$ — precisely
  $(n-1)mV$ — and tight even for binary and for identical valuations.
- **Chosen allocation.** Lower bound $n-1$. Matched by efficient algorithms for
  **binary** and **identical** valuations, and for **$n = 2$**.
- **Experiments** on synthetic and Spliddit data: real instances need far less than
  worst case.

**Improves on.** Maskin (1987) and the rent-division literature, which handled only
unit demand with $m = n$. R1 is the first to ask for asymptotic subsidy bounds in the
multi-demand model where $m \ne n$ and an agent may hold many items.

**Leaves open.** Two conjectures: (1.1) $n-1$ total suffices for general additive;
(1.2) some allocation is simultaneously envy-freeable *and* EF1.

---

## 2. R2 — Brustle, Dippel, Narayan, Suzuki, Vetta, *One Dollar Each Eliminates Envy* (2019/EC 2020)

**Directly answers R1.** Two results.

- **Additive:** subsidy $\le \mathbf{1}$ **per agent**, hence $\le n-1$ total. Proves
  R1's Conjecture 1.1 — and in a strictly stronger per-agent form, which R1 did not ask
  for. The allocation produced is also **EF1** (settling Conjecture 1.2) and
  **balanced** (bundle sizes differ by $\le 1$), and is computed in polynomial time.
  Algorithm: **iterated maximum matching** — repeatedly match agents to remaining items
  and hand out one round at a time.
- **General monotone:** subsidy $\le 2(n-1)$ per agent, $2(n-1)^2$ total. Poly-time with
  a value oracle.

**Why the monotone result is the conceptually bigger one.** R1's given-allocation bound
was $(n-1)mV$ — it grows with the number of items. R2 shows that once you may *choose*
the allocation, the total subsidy is $O(n^2)$, **independent of $m$**. Envy caused by a
thousand items is no more expensive to buy off than envy caused by ten. This is the
result every later paper is measured against.

**Improves on.** R1 on every axis: closes both conjectures, converts a total bound into
a per-agent bound, adds EF1 + balancedness for free, and extends from additive to
monotone.

**Leaves open.** Is $2(n-1)^2$ tight for monotone? The only known lower bound is $n-1$.
This gap becomes Open Question 9 in the Liu–Lu–Suzuki–Walsh survey, and is what R9
attacks.

---

## 3. R3 — Barman, Krishna, Narahari, Sadhukhan, *Achieving Envy-Freeness with Limited Subsidies under Dichotomous Valuations* (2022)

**Trades generality of the valuation class for a factor of $n$.**

Setting: **dichotomous** valuations — every marginal $v_i(S\cup\{g\}) - v_i(S) \in \{0,1\}$
— with *no* additivity, submodularity, or even subadditivity assumed.

**Result.** There is an allocation and a subsidy with **$p_i \in \{0,1\}$ for every
agent**, hence total $\le n-1$. Computable in polynomial time in the value-oracle model.
Tight: $n$ agents, one valuable good forces $n-1$ agents to be paid 1 each.

**Improves on.**

- **R2's monotone bound**, by a factor of $n$: $O(n^2) \to O(n)$ total, on the
  dichotomous subclass.
- **R1's binary-additive result** and **Goko et al.'s binary-submodular result**, by
  dropping both additivity and submodularity. Binary additive $\subsetneq$ matroid-rank
  $\subsetneq$ dichotomous, and R3 covers the outermost class.

**The point to carry forward.** The per-agent subsidy is not merely bounded by 1, it is
*integral* — every agent is paid exactly 0 or exactly 1. That is a structural statement
about the envy graph under dichotomous valuations, not just an inequality.

---

## 4. R5 — Bu, Song, Yu, *EFX Allocations Exist for Binary Valuations* (FAW 2023)

**Branch (B): no money at all.** Same valuation class as R3, opposite repair strategy.
Included in the Project as the natural companion: under binary valuations, *either*
you pay 0-or-1 per agent and get exact EF (R3), *or* you pay nothing and get EFX (R5).

**Result.** EFX allocations always exist for **general binary** valuations (marginals in
$\{0,1\}$, not necessarily submodular), and can be computed in polynomial time.

**Improves on.** Babaioff–Ezra–Feige (2021), who proved EFX existence for binary
**submodular** (matroid-rank) valuations via a Nash-welfare-maximizing mechanism.
R5 shows that approach *cannot* be pushed further, with an explicit counterexample:
$n$ agents, $m > n$ items, agent 1 valuing only bundles of size $\ge m-n+1$, everyone
else additive. Every MNW allocation there gives agent 1 the huge bundle and everyone
else one item — and fails EFX when $m \gg n$. So the welfare-maximization route is dead
outside submodularity, and R5 needs different machinery.

**Method.** Builds on Chaudhury et al.'s (2021) envy-graph procedure, which gives a
*partial* EFX allocation with $\le n-1$ items left over and nobody envying the leftover
pool, in *pseudo-polynomial* time. R5's contribution: binary valuations admit extra
update steps that place those remaining items while preserving EFX, yielding a
**complete** allocation, and in **polynomial** time.

**Note for the Project.** Verify EFX$_0$ vs. EFX$_+$ directly from the PDF — the
distinction is real under binary valuations and my copy of this file is OCR only.

---

## 5. R9 — Kawase, Makino, Sumita, Tamura, Yokoo, *Towards Optimal Subsidy Bounds for Envy-freeable Allocations* (2023 / AAAI 2024)

**The strongest unweighted result in the corpus, and a genuine change of method.**

Setting is *wider* than R2: **doubly monotone** valuations (each item is a good or a
chore for each agent), normalized two-sided, $|v_i(S\cup\{e\}) - v_i(S)| \le 1$.

**Results.**

- **Theorem 1.** *Given any EF1 allocation*, compute in polynomial time an envy-free
  allocation with subsidy $\le n-1$ per agent and $\le n(n-1)/2$ total.
- **Generalization.** From an EF$k$ allocation: $k(n-1)$ per agent, $k \cdot n(n-1)/2$
  total.
- **Tightness and its evasion.** These bounds cannot be improved if you insist on
  starting from an *arbitrary* EF1 allocation (Example 1). R9 escapes by perturbing the
  bundles slightly: for **monotone** valuations with $n \ge 3$, $n - 1.5$ per agent and
  $(n^2-n-1)/2$ total (Theorem 2).
- For $n = 2$ the bounds are best possible — a subsidy of 1 is unavoidable.

**Improves on R2.** Per-agent $2(n-1) \to n-1$; total $2(n-1)^2 \to n(n-1)/2$, i.e.
roughly a factor 2 and a factor 4 — *and in a strictly larger model*, since monotone
$\subsetneq$ doubly monotone. Answers Open Question 9 of the survey.

**The structural move that makes it work.** R2 constructs one specific allocation
(iterated maximum matching) and shows *that* allocation is cheap to subsidize. R9
separates the two jobs: someone else finds an EF1 allocation (envy-cycle elimination,
Lipton et al.), and R9 supplies a general reduction *EF1 $\Rightarrow$ EF-with-subsidy*
with a bound depending only on $n$ and $k$. Because EF1 is known to exist for doubly
monotone valuations, the wider class comes along for free. This is why R9 gets a better
constant on a bigger class simultaneously, which usually does not happen.

**Machinery.** LP duality on the assignment problem: $p$ and $q_i = \max_j(v_i(A_j)+p_j)$
are dual variables to the max-weight matching, and complementary slackness converts the
EF1 hypothesis into a bound on the longest path in the envy graph.

---

## 6. R8 — Montanari, Schmidt-Kraepelin, Suksompong, Teh, *Weighted Envy-Freeness for Submodular Valuations* (AAAI 2024 / Soc. Choice Welf. 2025)

**Branch (B) in the weighted setting. No subsidies anywhere in this paper** — it is in
the corpus because it maps what fairness notions are even *available* once you have
both weights and non-additivity, which is exactly the terrain R4/R6 must subsidize.

**The obstruction it starts from** (Chakraborty et al. 2021a, Example 1.1): $n=2$,
$w_1=1, w_2=2$, $m \ge 6$; agent 1 additive with value 1 per good, agent 2 valuing any
nonempty bundle at 1. No complete WEF1 allocation exists. The impossibility survives
weakening to WWEF1, to WWEF$c$ for any constant $c$, and to multiplicative $r$-WEF1.
So the entire additive weighted toolkit collapses at matroid-rank valuations — the
*simplest* non-additive class.

**Contributions.**

- **Two new notion families.** **TWEF$(x,1-x)$**, based on *transferability*: $i$'s
  complaint counts only if she would actually gain from absorbing $j$'s whole bundle.
  **WMEF$(x,1-x)$**, the weighted extension of Caragiannis et al.'s MEF1: $i$ compares
  against her *marginal* value of $j$'s bundle. TWEF $\Rightarrow$ WMEF, strictly. Both
  collapse to WEF$(x,1-x)$ under additivity, hence to EF1 at equal weights — so nothing
  is lost in the base case.
- **Division of labour between them:** TWEF is the right notion for matroid-rank;
  WMEF is achievable for **general submodular**.
- **Picking sequences** adapted to submodular valuations (pick the highest *marginal*
  gain each turn) satisfy WMEF$(x,1-x)$ for every $x$. Corollary: plain round-robin
  gives MEF1 for unweighted submodular valuations.
- **MWNW** satisfies WWMEF1 (the remove-or-copy relaxation), extending Chakraborty et
  al. and Caragiannis et al.
- **Transfer algorithm** (Benabbou et al.) extended to weights: returns a *clean*
  TWEF$(x,1-x)$ allocation maximizing **unweighted** utilitarian welfare. Termination
  generalizes easily; *polynomial-time* termination needed a new argument.
- **Harmonic welfare — the headline surprise.** Define $\mathrm{MWHW}_x$ maximizing
  $\sum_i w_i H_{v_i(A_i),x}$ with shifted harmonic numbers. Under matroid-rank
  valuations a clean maximum weighted harmonic welfare allocation satisfies
  TWEF$(x,1-x)$ — hence WEF$(x,1-x)$ for binary additive. MWNW provably cannot do this
  for *any* $x$. A welfare rule nobody was using dominates the canonical one on
  fairness. Plus a characterization of the harmonic rules within a natural class
  (Thm 6.7), and: in unweighted additive instances with integer values, max harmonic
  welfare $\Rightarrow$ EF1.

**Improves on.** Chakraborty et al. (2021a, 2024) — answers their explicitly stated open
direction of finding envy-based notions that survive non-additivity under weights. Also
directly answers the limitation Viswanathan–Zick flagged in their own weighted
matroid-rank work: their method cannot deliver envy-based properties.

---

## 7. R7 — Dai, Chen, Wu, Xu, Zhang, *Weighted Envy-Freeness in House Allocation* (2024)

**Weights plus a cardinality constraint.** $m \ge n$ houses, each agent gets **exactly
one**. So a "bundle" is a single house and an allocation is an $N$-saturating matching.

**Results.**

1. **Polynomial-time algorithm** deciding whether a WEF allocation exists and computing
   one. Method: preprocess utilities by weights, then iteratively ban agent–house pairs,
   proving each ban preserves the existence question, and run matching on what remains.
   (Unweighted analogue: Gan, Suksompong, Voudouris.)
2. **Characterization of WEF-able allocations** — and the paper's real contribution,
   a **non-existence result**: WEF-able allocations *may not exist*. No amount of money,
   however large, can make some instances weighted-envy-free.
3. **Special cases** where existence is restored, with polynomial algorithms: identical
   utilities, two types of agents, bi-valued utilities.

**Why (2) matters more than it looks.** In the unweighted setting, R1 guarantees every
house-allocation instance is EF-able. In *unconstrained* weighted fair division (all
items allocated, no cap per agent), WEF-able allocations always exist — R7 notes this
explicitly. Non-existence here is produced **jointly** by the weights and the
one-house-per-agent constraint; neither alone does it. That is a clean, quotable
statement about where the theory actually breaks, and it is the sharpest negative
result in the corpus.

**Improves on.** Halpern–Shah applied to house allocation (which gives EF-ability for
free, unweighted) and Gan et al.'s unweighted existence algorithm — by adding
entitlements to both, and finding that one of the two guarantees does not survive.

---

## 8. R4 — Klein Elmalem, Gonen, Segal-Halevi, *Weighted Envy Freeness With Limited Subsidies* (2024)

**Opens branch (A) under entitlements.** First paper to study WEF with subsidies.

**The two demolitions it leads with** — both worth memorizing, since they are the reason
this branch exists:

- **Example 1.1 (kills R1).** $n=2$, $w=(1,10)$, items $o_1,o_2$, $v_1=(5,7)$,
  $v_2=(10,8)$. Halpern–Shah says *some permutation of any given family of bundles* is
  envy-freeable. Here **neither** permutation is WEF-able: each yields two contradictory
  linear inequalities in $(p_1,p_2)$.
- **Corollary (kills R2).** Since iterated maximum matching outputs a balanced
  allocation, and balancedness is exactly wrong under unequal entitlements, IMM gives no
  WEF guarantee.

**Results** (additive valuations, weights sorted $w_1 \le \dots \le w_n$, $W = \sum_i w_i$):

| Setting | Guarantee |
|---|---|
| Allocation **given** | necessary + sufficient condition for WEF-ability (no positive-cost cycle in the *weighted* envy graph); total subsidy $\le (\tfrac{W}{w_1}-1)mV$, **tight** |
| Allocation **chosen**, general additive, integer weights | WEF-able with total $\le (W-w_1)V$ |
| Identical additive | $\le V$ per agent, $\le (n-1)V$ total, **tight** — and *independent of the weights* |
| Binary additive | modified General Yankee Swap: $\le w_i/w_1$ for agent $i$, total $\le \tfrac{W}{w_1}-1$ |

Every bound collapses to the known unweighted bound at equal weights, which is the
correctness check the paper leans on.

**The identical-additive row is the interesting one.** Everywhere else the subsidy
scales with the weight *ratio* $W/w_{\min}$, which is unbounded. Under identical
valuations the weights drop out entirely and you recover $(n-1)V$. Worth understanding
why before assuming the ratio dependence is intrinsic.

---

## 9. R6 — Klein Elmalem, Aziz, Gonen, Huang, Kimura, Saha, Segal-Halevi, Sun, Suzuki, Yokoo, *Whoever Said Money Won't Solve All Your Problems?* (2025)

**The merged, superseding version of R4.** Explicitly combines Aziz et al. (2024) with
Elmalem et al. (2024) = R4; ten authors, both AAMAS extended abstracts folded in. Same
Example 1.1, now joined by:

- **Example 1.2 (kills the efficiency route too).** $w=(1,3)$, two identical items,
  unit-demand agents valuing any nonempty bundle at 30 and 90. The
  welfare-maximizing allocation — also the only non-wasteful one — is **not** WEF-able.
  So under weights, "maximize welfare, then subsidize" fails as well.

**Results, by valuation class** (see §10 for the table):

- **General monotone:** total $(\tfrac{W}{w_{\min}}-1)mV$, **tight**.
- **Supermodular / superadditive:** WEF *and* welfare-maximization *and* truthfulness
  simultaneously, via VCG with a large upfront subsidy. The only truthfulness result in
  the weighted branch.
- **Additive, integer weights:** $\tfrac{W-w_{\min}}{\gcd(w)}V$ — **independent of $m$**,
  the weighted analogue of R2's headline. This strengthens R4's $(W-w_1)V$ by the
  $\gcd$ factor.
- **Relaxations:** WEF-ability is **incompatible** with WWEF1, and with WEF$(x,y)$
  whenever $x+y<2$. For two agents, WEF-able + WEF$(1,1)$ is achievable. (Read this
  against R8: R8 relaxes the notion and keeps existence; R6 shows you cannot have the
  relaxation *and* subsidizability at once.)
- **Identical additive:** WEF-able + WEF$(0,1)$, total $\le (n-1)V$, tight.
- **Binary additive:** General Yankee Swap → WEF-able + WEF$(0,1)$, total
  $\le \tfrac{W}{w_{\min}}-1$.
- **Matroidal:** lower bound linear in $m$ — so no $m$-independent bound exists here.
  Marks the boundary of the additive-style results.
- **Identical items:** near-tight
  $V\sum_{2\le i\le n}\big(w_i \sum_{1 \le j \le i} 1/w_j\big)$, agents sorted by
  descending single-item value. **The striking corollary:** with weights that are nearly
  equal but not exactly equal, the required subsidy can be $\Omega(n^2 V)$, against
  $O(nV)$ for exactly equal weights. The bound is *discontinuous* at equal entitlements.
  Also: polynomial-time exact minimum subsidy for this case — unlike binary additive and
  identical additive, where it is NP-hard.
- **Limited budget** (§9): when the subsidy budget is too small for WEF, compute a fair
  allocation of items *and* money anyway. **New even in the unweighted setting.**
- Experiments comparing the algorithms against the theoretical bounds.

**Improves on R4.** Strictly. Monotone $\supsetneq$ additive; the $\gcd$ refinement; the
VCG/truthfulness result; the relaxation impossibilities; the identical-items analysis;
the limited-budget algorithm. Cite R6 over R4 by default.

---

## 10. Bound tables

**Unweighted, total subsidy, choosing the allocation.** ($V=1$ normalization.)

| Valuation class | Bound | Source | Superseded by |
|---|---|---|---|
| additive (given allocation) | $(n-1)mV$, tight | R1 | — (still the right answer for *given* allocations) |
| additive | $1$/agent, $n-1$ total, tight | R2 | — |
| dichotomous | $p_i \in \{0,1\}$, $n-1$ total, tight | R3 | — |
| monotone | $2(n-1)$/agent, $2(n-1)^2$ total | R2 | **R9** |
| doubly monotone (from EF1) | $n-1$/agent, $n(n-1)/2$ total | R9 | — |
| monotone, $n\ge3$ | $n-1.5$/agent, $(n^2-n-1)/2$ total | R9 | — |
| EF$k$ start | $k(n-1)$/agent, $k\,n(n-1)/2$ total | R9 | — |

Lower bound throughout: $n-1$ total. The monotone gap ($n-1$ vs. $(n^2-n-1)/2$) is the
main open quantitative question on this trunk.

**Weighted, total subsidy** (R6 Table 1; $w_2$ = second-smallest weight):

| Valuation class | Lower bound | Upper bound |
|---|---|---|
| general / superadditive / supermodular | $(\tfrac{W}{w_{\min}}-1)mV$ | $(\tfrac{W}{w_{\min}}-1)mV$ |
| additive | $(\tfrac{W}{w_{\min}}-1)V$ | $\tfrac{W-w_{\min}}{\gcd(w)}V$ |
| identical additive | $(n-1)V$ | $(n-1)V$ |
| binary additive | $\tfrac{W}{w_2}-1$ | $\tfrac{W}{w_{\min}}-1$ |
| matroidal | $\tfrac{m}{n}(\tfrac{W}{w_{\min}}-n)$ | $(\tfrac{W}{w_{\min}}-1)m$ |
| additive, identical items | $\sum_{2\le i\le n}\big(Vw_i\sum_{1\le j<i}\tfrac1{w_j}\big)$ | $\sum_{2\le i\le n}\big(Vw_i\sum_{1\le j\le i}\tfrac1{w_j}\big)$ |

Note that every weighted bound except identical-additive carries a $W/w_{\min}$ factor,
which is unbounded in the weight ratio — the qualitative price of entitlements. Whether
that factor is necessary or an artifact of current techniques is, as far as this corpus
goes, open.

---

## 11. Where the corpus is thin

Candidates for what to read or attack next, stated as gaps rather than suggestions:

- **The monotone constant.** R9 gives $(n^2-n-1)/2$; the lower bound is $n-1$. Nothing
  in the corpus closes this.
- **Weighted × doubly monotone.** R9's EF1 $\Rightarrow$ EF-with-subsidy reduction is
  unweighted. R6 is monotone-only. Nobody has run R9's argument against a weighted
  envy graph — and the reason is visible in the glossary (§5): weighted
  reassignment-stability is not a maximization statement, so the LP-duality step has no
  obvious analogue. That is either a real obstruction or an open problem.
- **Is $W/w_{\min}$ necessary?** R6's identical-additive row proves it is not intrinsic
  to weighted settings. No characterization of when it can be dropped.
- **R7's non-existence, generalized.** R7 shows constraint + weights $\Rightarrow$
  possible non-existence of WEF-able allocations, for one specific constraint. There is
  no general theory of which constraints do this.
- **R8 × subsidies.** R8 designs notions that exist without money; R6 shows WEF-ability
  is incompatible with WWEF1 and WEF$(x,y)$ for $x+y<2$. Nobody has asked what subsidy
  buys you TWEF or WMEF, or whether R6's impossibility extends to them.

---

*v1. Update alongside the glossary as papers are added.*
