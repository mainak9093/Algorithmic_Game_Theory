# Target T: The Three-Set `(1,1,2)` Discrepancy Theorem

**Project frontier:** Conjecture 2 / fair division with dichotomous
costs\
**Primary scope:** the unresolved `n = 3` case, especially the residual
composed-cost family\
**Status:** Target T is **open**. It has survived the computational
stress tests described in the current project state, but no proof is
currently certified.

------------------------------------------------------------------------

## 0. Executive summary for an AI agent

The current proof program for Conjecture 2 at `n = 3` has been reduced
to a small three-set discrepancy problem.

The key target is:

> **Target T.** For any three sets `D1, D2, D3`, there exists a
> 3-colouring of the ground set such that, after relabelling the sets if
> necessary,
>
> -   `D1` has count-spread at most `1`,
> -   `D2` has count-spread at most `1`,
> -   `D3` has count-spread at most `2`.

Here the count-spread of `D` under a partition `(B1,B2,B3)` is \> \>
`max_t |B_t ∩ D| - min_t |B_t ∩ D|`.

This target is deliberately weaker than simultaneous uniform balance
`(1,1,1)`. Uniform balance is known to fail for three sets: the `K4`
example forces three pairwise rainbow constraints that cannot be
satisfied with three colours. Nevertheless, the same example has total
spread only `2`, so relaxing one set from `1` to `2` is plausible and
exactly matches what the remaining `n=3` argument needs.

### Why Target T matters

For the residual **composed** family

`cost_i(S) = f_i(|S ∩ D_i|)`

with monotone `0/1` increments:

1.  the known residual instances have at least one `D_i` with
    `3 | |D_i|`;
2.  equal splitting of that `D_i` gives its composed cost spread exactly
    `0`;
3.  Target T can make two sets count-balanced within `1` and the third
    within `2`;
4.  assign the divisible set to one of the two tight slots;
5.  the resulting cost-spread sum is at most `0 + 1 + 2 = 3`;
6.  the established `n=3` Lemma A says every minimum-cost assignment on
    any family with total spread at most `3` is good;
7.  therefore the residual instance satisfies the required `F5*`
    certificate and hence Conjecture 2 at `n=3`.

The important logical chain is therefore:

``` text
Target T
   ↓
residual composed instance has Σ ≤ 3
   ↓
Lemma A: every minimum-cost assignment is good
   ↓
F5* at n = 3
   ↓
Conjecture 2 at n = 3
```

**Do not silently promote Target T to a theorem.** It is the current
proof target.

------------------------------------------------------------------------

# 1. Definitions and notation

We work with a finite ground set `M` and three subsets

`D1, D2, D3 ⊆ M`.

A 3-colouring is a map

`χ : M → {1,2,3}`,

equivalently a partition

`B1 ⊔ B2 ⊔ B3 = M`.

For a set `D_i`, define its colour-count vector

`a_i(χ) = (|D_i ∩ B1|, |D_i ∩ B2|, |D_i ∩ B3|)`.

Define

`sp_i(χ) = max_t a_{i,t} - min_t a_{i,t}`.

Thus `sp_i ≤ 1` means that the elements of `D_i` are distributed as
evenly as possible among the three bundles.

The total spread is

`Σ(χ) = sp_1(χ) + sp_2(χ) + sp_3(χ)`.

For composed costs

`cost_i(S) = f_i(|S ∩ D_i|)`

where `f_i` is monotone with increments in `{0,1}`, the compression
lemma gives

`sp_cost_i(χ) ≤ sp_count(D_i,χ)`.

Therefore a count-colouring with spread bounds `(1,1,2)` gives the
same-or-better cost-spread bounds `(1,1,2)`.

------------------------------------------------------------------------

# 2. The established `n=3` machinery

The following results are already established and should be treated as
inputs, not rediscovered.

## 2.1 Normalised minimum-cost assignment

For a partition `B=(B1,B2,B3)`, define

`v_i(t) = cost_i(B_t) - min_s cost_i(B_s)`.

Then:

-   `v_i ≥ 0`;
-   at least one coordinate of `v_i` is zero;
-   `sp_i(B) = max_t v_i(t)`;
-   a minimum-cost assignment minimises `F(σ) = Σ_i v_i(σ(i))`.

This converts the assignment problem into a small weighted matching
problem.

## 2.2 Goodness criterion at `n=3`

Let

`x_i = v_i(σ(i))`.

A minimum-cost assignment is good exactly when:

1.  every `x_i ≤ 1`; and
2.  there is no weight-2 directed two-path.

Equivalently, the dangerous structure is an arc of weight at least `2`,
or two consecutive weight-1 arcs.

## 2.3 Lemma A

For `n=3`:

> If a minimum-cost assignment has an arc of weight at least `2`, then
> the total spread satisfies `Σ ≥ 4`.

> If all arcs have weight at most `1` but there is a weight-2 two-path,
> then `Σ ≥ 5`.

Therefore:

`Σ ≤ 3  ⇒  every minimum-cost assignment is good`.

This is a particularly strong fact because it does **not** require
family minimality, uniform balance, or an exchange argument.

## 2.4 Consequence

The remaining existence problem can be phrased as:

> **Lemma E.** Every three-agent dichotomous instance admits a partition
> with total spread at most `3`.

If Lemma E holds, Lemma A immediately gives the desired good
minimum-cost assignment.

------------------------------------------------------------------------

# 3. Why the current obstruction is so specific

Suppose a partition is minimum-total-spread and `Σ = 4`.

The established matching-optimality analysis rules out every other
failure mode below this threshold.

The unique remaining `Σ=4` pattern is, after relabelling agents and
bundles,

`v_i = v_k = (2,2,0),   v_j = (0,0,0)`.

Interpretation:

-   agents `i` and `k` see two bundles as equally heavy and one bundle
    as light;
-   agent `j` is indifferent among the three bundles;
-   every minimum-cost assignment strands one of `i,k` on a heavy
    bundle.

Thus the remaining proof task is not a generic fair-division problem. It
is a **three-bundle exchange / discrepancy problem involving two
correlated problematic agents**.

The previous one-item/common-pivot approach is insufficient:
dichotomousness does not force one item to have the desired marginal
signature for both problematic agents simultaneously.

Therefore the correct next object is the global three-set structure.

------------------------------------------------------------------------

# 4. Why two sets are already solved

A major established theorem is:

> **Two-set balance theorem.** For any two subsets `D1,D2 ⊆ M` and any
> number `k` of bundles, there exists a `k`-colouring splitting both
> sets within one.

For `k=3`, this says:

`sp(D1) ≤ 1` and `sp(D2) ≤ 1`

simultaneously.

The proof uses the three Venn regions

`P1 = D1 \ D2`, `P12 = D1 ∩ D2`, `P2 = D2 \ D1`.

Each region is split as evenly as possible. The shared region is fixed
first; the two private regions can then be chosen independently so that
each resulting sum has spread at most one.

This establishes an important structural fact:

> **Two-set interaction is not the obstruction. The obstruction requires
> all three sets.**

------------------------------------------------------------------------

# 5. The exact new target

## Target T

For arbitrary `D1,D2,D3 ⊆ M`, prove that there is a 3-colouring
satisfying

`sp(D1) ≤ 1`, `sp(D2) ≤ 1`, `sp(D3) ≤ 2`.

The names of the sets may be permuted.

Equivalently, there is a partition `B1 ⊔ B2 ⊔ B3 = M` such that two
agents have perfectly balanced integer discrepancy and the third has
discrepancy at most two.

The target is intentionally asymmetric only in the bound. Because the
original problem is symmetric in agents, the proof may freely choose
which set is the relaxed one.

------------------------------------------------------------------------

# 6. Why Target T is exactly strong enough

There are two cases according to how many underlying sets have
cardinality divisible by `3`.

## Case A: at least two `|D_i|` are divisible by 3

The established two-set theorem implies that two such sets can
simultaneously be split within one.

For an additive count cost, if `3 | |D_i|`, spread cannot equal `1`: the
three integer counts sum to a multiple of `3`, and a three-vector with
spread exactly `1` has sum congruent to `1` or `2` modulo `3`.

Therefore:

`sp_i ≤ 1  ⇒  sp_i = 0`.

For composed costs, the same conclusion follows once the underlying
count vector is equalised.

So the two divisible sets can be made exactly balanced:

`(sp_1,sp_2,sp_3) = (0,0,≤2)`,

and hence

`Σ ≤ 2`.

This is even stronger than needed.

## Case B: exactly one `|D_i|` is divisible by 3

Say

`3 | |D_3|`.

Apply Target T with `D3` occupying one of the two tight slots:

`sp(D3) ≤ 1`, `sp(D1) ≤ 1`, `sp(D2) ≤ 2`.

Because `3 | |D3|`, the first inequality forces

`sp(D3)=0`.

Thus:

`Σ ≤ 0 + 1 + 2 = 3`.

This is exactly the threshold required by Lemma A.

## Case C: no `|D_i|` is divisible by 3

For arbitrary additive sets, this case is connected to the already
isolated additive discrepancy question. For the **residual composed
family**, the current structural reduction says this case does not occur
unless one has a counterexample to the additive shadow problem `(Q)`.

Therefore Target T only needs to be applied to the residual instances
that actually survive S1--S4.

------------------------------------------------------------------------

# 7. Why composed costs are the correct residual setting

A composed dichotomous cost has the form

`cost_i(S) = f_i(|S ∩ D_i|)`

where `f_i` is monotone and every marginal increment is `0` or `1`.

The compression lemma says:

`sp_cost_i(B) ≤ sp_count(D_i,B)`.

Hence a count discrepancy bound is automatically a cost discrepancy
bound.

This is important because the residual search found its first genuine
residual examples in this composed family.

At `n=3,m=4`, exhaustive enumeration produced 46 residual composed
instances. Their set-size multisets were always

`(2,3,3)` or `(3,3,3)`.

Thus every residual instance contains at least one underlying set whose
size is divisible by `3`.

That is exactly the condition required to turn a `(1,1,2)` count
certificate into a total cost spread at most `3`.

------------------------------------------------------------------------

# 8. The Venn-region reduction

For three sets, the seven nonempty Venn regions are

``` text
R1   = D1 \ (D2 ∪ D3)
R2   = D2 \ (D1 ∪ D3)
R3   = D3 \ (D1 ∪ D2)

R12  = D1 ∩ D2 \ D3
R13  = D1 ∩ D3 \ D2
R23  = D2 ∩ D3 \ D1

R123 = D1 ∩ D2 ∩ D3.
```

Write

`|R| = 3q_R + b_R`

with

`b_R ∈ {0,1,2}`.

The `3q_R` elements can be distributed one per colour in complete
triples and therefore contribute equally to every set.

Only the residues `b_R` matter.

This reduces the discrepancy problem to at most seven residue variables.

------------------------------------------------------------------------

# 9. Signed residue formulation

For each active region:

-   if `b_R = 0`, there is no residual choice;
-   if `b_R = 1`, choose one colour to receive the extra element;
-   if `b_R = 2`, equivalently choose one colour to *omit*.

Thus each active region can be represented as

`σ_R e_{c_R}`,

where

`σ_R = +1` if `b_R=1`, `σ_R = -1` if `b_R=2`.

For each set `D_i`, the residual count vector is therefore

`F_i = Σ_{R ⊆ D_i} σ_R e_{c_R}`.

Adding or subtracting a constant all-ones vector does not affect spread,
so:

`sp(D_i) = spread(F_i)`.

This is the central finite combinatorial formulation.

------------------------------------------------------------------------

# 10. Constraint taxonomy

For each set `D_i`, let

`p_i = number of active +1 regions inside D_i`,
`q_i = number of active -1 regions inside D_i`.

Then

`s_i = p_i - q_i`

controls the sum of the residual vector modulo `3`.

The rigidity condition `3 ∤ |D_i|` translates to

`s_i ≠ 0 (mod 3)`.

The possible local constraints have already been classified.

### One active region

No colour constraint is required.

### Two active regions

The mixed-sign case `(1,1)` is forbidden by the non-divisibility
hypothesis.

The surviving cases impose a **disequality**:

`c_a ≠ c_b`.

### Three active regions

The surviving `(2,1)` or `(1,2)` cases impose a **membership
constraint**:

`c_minor ∈ {c_major1,c_major2}`.

If a private region is active, it can often serve as a local "knob" that
satisfies the constraint without affecting other sets.

### Four active regions

This is the genuinely difficult case.

The `(2,2)` sign pattern is forbidden by the rigidity hypothesis.

The remaining cases impose a **diversity-type constraint**: roughly, the
four chosen colours must exhibit enough diversity, with an additional
special condition in the `(3,1)` / `(1,3)` cases.

This is where the additive shadow problem remains nontrivial.

------------------------------------------------------------------------

# 11. Known obstructions and what they teach us

## The `K4` obstruction

Consider

`D1={1,2,3}`, `D2={1,2,4}`, `D3={1,3,4}`.

All three sets have size `3`.

Uniform balance would require each set to have counts `(1,1,1)`, so
every pair of elements inside each `D_i` must receive different colours.

The union of these pairwise constraints is all of `E(K4)`, which is not
3-colourable.

Therefore uniform balance fails.

But the partition

`{1}, {2,4}, {3}`

gives counts

`D1 : (1,1,1)` `D2 : (1,2,0)` `D3 : (1,1,1)`,

hence spreads

`(0,2,0)`,

so

`Σ=2`.

This example is crucial:

> Failure of `(1,1,1)` does **not** imply failure of `(1,1,2)`.

It demonstrates why Target T is plausible.

------------------------------------------------------------------------

# 12. Why the obvious independent-greedy proof is insufficient

There is a useful greedy levelling lemma:

> Given integer weights `0 ≤ w_j ≤ k`, one can choose binary vectors of
> those weights so that their sum has spread at most one.

This proves one-set balance and, through the Venn decomposition,
explains the two-set theorem.

But three sets share multiple Venn regions.

For two sets, the shared region is essentially one common commitment.

For three sets, the shared regions are

`R12, R13, R23, R123`.

In particular, `R123` influences all three constraints.

A greedy choice made to satisfy one set can consume exactly the residue
freedom another set needs.

Therefore:

> **Do not attempt to prove Target T by independently levelling each
> set.**

The proof must coordinate the shared regions globally.

------------------------------------------------------------------------

# 13. A second useful structural lemma: in-region placement

Suppose a two-set colouring has already made a region `R` internally
balanced.

If `D3` occupies `d_R` elements of `R`, those elements can be placed
among the three colours with discrepancy at most one subject to the
existing capacities.

Thus, locally, the third set can also be balanced.

The failure of uniform balance must therefore come from **capacity
interactions between regions**, not from an individual Venn region.

This yields the established structural diagnostic:

> In a residual composed instance, for every choice of two sets as the
> initially balanced pair, some Venn region must have a capacity
> obstruction: its size is not divisible by `3`, while `D3` nearly fills
> it in a way that leaves insufficient residue freedom.

This is a useful clue for any proof of Target T.

------------------------------------------------------------------------

# 14. The most promising proof architecture

The next proof attempt should not start from the original envy graph.

It should proceed in this order.

## Step 1 --- Remove multiples of three

For every Venn region `R`, write

`|R|=3q_R+b_R`.

Distribute the `3q_R` elements cyclically/equally.

Only `b_R ∈ {0,1,2}` remains.

## Step 2 --- Choose the relaxed set

Because Target T is symmetric, choose which of `D1,D2,D3` receives the
spread-2 allowance.

For the residual composed application, choose a set with

`3 | |D_i|`

as one of the tight sets.

## Step 3 --- Solve the two-set subsystem

Use the established two-set balance theorem to guarantee spread `≤1` for
the two tight sets.

Do not rebuild this theorem.

## Step 4 --- Characterise the remaining freedom

Instead of fixing one particular two-set colouring, describe the set of
all legal residue assignments satisfying the two tight constraints.

This is the key missing move.

The legal assignments form a structured family because each Venn region
has only `0`, `1`, or `2` residual elements.

## Step 5 --- Prove the third set cannot exceed spread 2

Assume for contradiction that every legal extension gives the third set
spread at least `3`.

Translate this into forbidden colour patterns among the seven residue
variables.

Then use the rigidity/non-divisibility conditions to show that such a
forbidden pattern forces either:

1.  a uniform `(1,1,1)` solution after all, contradicting the assumption
    that the instance is residual; or
2.  a forbidden `s_i ≡ 0 mod 3` pattern; or
3.  a previously solved two-set obstruction, which cannot exist.

This is the most promising route to an actual proof.

------------------------------------------------------------------------

# 15. Alternative proof architecture: finite constraint classification

Because there are only seven Venn regions, another viable strategy is a
complete structural case analysis.

Classify each `D_i` by

`d_i = number of active Venn regions`.

Known cases:

-   `d_i ≤ 2`: already controlled by disequality constraints;
-   `d_i = 3`: membership constraints, with private-region freedom in
    important cases;
-   `d_i = 4`: diversity constraints; only remaining difficult regime.

Thus a proof can potentially reduce Target T to configurations
containing at least one `d_i=4` set.

Then classify the interaction of the `d_i=4` set with the other two
sets.

Because there are only three agents and seven regions, this is finite.

**Important:** a finite case analysis must be fully written and
verified. Do not infer a theorem merely because computational
enumeration found no counterexample.

------------------------------------------------------------------------

# 16. Computational protocol for testing candidate lemmas

Any new lemma should be stress-tested before being added to the theorem
chain.

Minimum test families:

1.  arbitrary dichotomous costs;
2.  binary additive costs;
3.  capped costs `min(|S∩D|,k)`;
4.  threshold costs;
5.  arbitrary monotone `0/1` marginal functions `f`.

For Target T specifically, test the underlying set formulation
independently of the cost functions.

For each `m`:

1.  enumerate all triples `(D1,D2,D3)`;
2.  enumerate all `3^m` colourings;
3.  compute `(sp1,sp2,sp3)`;
4.  test whether some permutation satisfies `(≤1,≤1,≤2)`;
5.  record the smallest counterexample if one exists.

A failure must be stored explicitly as:

``` text
m
D1, D2, D3
all colourings or certificate of infeasibility
minimum achievable sorted spread profile
```

Do not report "no failure" without recording the search space.

------------------------------------------------------------------------

# 17. What NOT to retry

The following routes have already been falsified or superseded.

## 17.1 "Any spread-2 family works"

False.

Only about `85.8%` of tested spread-2 families had good maximum-weight
matchings.

## 17.2 Minimum spread alone

Not enough as a selector for the original argument.

Even when every tested family had minimum total spread, additional
structure was needed.

## 17.3 Balanced bundle sizes

False as a selector.

Hundreds of counterexamples were found.

## 17.4 Nonempty bundles

Also insufficient.

## 17.5 CRI-depth

The earlier conjectured depth property was refuted by dead states with
remainder size at least `3`.

## 17.6 Common pivotal item

Not enough.

The two problematic agents can have simultaneous gaps without one item
necessarily providing the required marginal improvement for both.

## 17.7 Merging two bundles and leaving the third fixed

Insufficient.

Balancing `B1∪B2` controls only the internal two-way discrepancy. It
says nothing about the comparison with `B3`.

The capped example

`c(S)=min(|S|,2)`

with

`B1={1,2}, B2={3,4}, B3=∅`

already demonstrates the failure: the merged two-way split can be
perfectly balanced while the three-way profile remains `(2,2,0)`.

------------------------------------------------------------------------

# 18. Relationship to the original exchange target

The original exchange formulation asks to show that a family with

`v_i=v_k=(2,2,0)`

cannot be exchange-minimal.

For the two problematic agents, an elementary item transfer has
signature

`τ(x;a→b)=(τ_i,τ_k) ∈ {-1,0,1}²`.

The desired global exchange proof would show that the six directed
bundle transfers cannot all avoid a sequence that decreases total
spread.

Target T is essentially a **set-level/global version of the same idea**.

Instead of proving that one of six elementary transfers works, it
constructs a whole repartition whose count-discrepancy certificate
prevents the `(2,2,0)` obstruction.

This is preferable because dichotomous costs support set-level exchange
via the intermediate-value lemma even when single-item exchange is
unavailable.

------------------------------------------------------------------------

# 19. Exact logical dependency graph

Keep the dependency graph explicit.

``` text
                         Target T
                            │
                            ▼
             residual composed instance
                  admits Σ ≤ 3
                            │
                            ▼
                    Lemma A
             Σ ≤ 3 ⇒ every min-cost
                  assignment good
                            │
                            ▼
                         F5*
                        n = 3
                            │
                            ▼
                    Conjecture 2
                        n = 3
```

More specifically:

``` text
Target T
+
3 | |D_r| for some residual set D_r
+
compression lemma
+
equal split of D_r
        │
        ▼
cost-spread profile ≤ (0,1,2)
        │
        ▼
Σ ≤ 3
        │
        ▼
Lemma A
        │
        ▼
good minimum-cost assignment
        │
        ▼
F5*
```

Do not skip the residual-instance qualification.

Target T by itself is a set-discrepancy statement. The bridge to
Conjecture 2 uses the structural facts specific to the residual composed
family.

------------------------------------------------------------------------

# 20. What a successful proof of Target T would look like

A proof should ideally have the following form.

### Lemma T1 --- Residue reduction

Multiples of three in every Venn region can be discarded without
changing any spread.

### Lemma T2 --- Two-set normal form

There exists a colouring satisfying the two chosen tight-set
constraints, and the remaining legal colour assignments can be
represented by a finite residue-state system.

### Lemma T3 --- Extension lemma

Every legal state for the two tight sets has an extension in which the
third set has spread at most two.

### Theorem T

Combine T1--T3.

The proof should avoid introducing fair-division machinery that is
irrelevant to the residue problem.

------------------------------------------------------------------------

# 21. The critical contradiction to aim for

Suppose Target T fails.

Then, after choosing the best two sets as the tight pair, every
colouring satisfying

`sp(D1)≤1`, `sp(D2)≤1`

must satisfy

`sp(D3)≥3`.

Because the two-set theorem guarantees the existence of the first two
inequalities, this means the obstruction is entirely in the extension
from two-set balance to three-set balance.

The proof should then derive a structural contradiction.

The strongest desired contradiction would be:

``` text
T fails
  ⇒ residue constraints force a rigid equality/diversity pattern
  ⇒ some Di has residual sum ≡ 0 mod 3
  ⇒ Di is not rigid
  ⇒ the supposed residual obstruction is impossible.
```

This would explain *why* the theorem is true rather than merely
verifying it computationally.

------------------------------------------------------------------------

# 22. Current evidence

The existing project evidence is unusually strong but must be
interpreted correctly.

The residual search found:

-   46 residual composed instances at `n=3,m=4`;
-   all had a set-size divisible by `3`;
-   all 46 admitted a total-spread-3 certificate;
-   all 46 had zero bad roots in the CRI attack.

The broader F5\* stress test also found zero failures on a corpus of
2,574 instances with `n≤6,m≤8`, and the stronger statement that
**every** minimum-total-spread family tested had a good maximum-weight
matching.

These are computational observations, not proofs.

The current project explicitly records F5\* as unproved.

------------------------------------------------------------------------

# 23. AI-agent continuation protocol

When another AI agent continues this work, it should begin here.

## First

Load this file and the latest residual analysis.

## Then treat these as established

-   Normalisation of costs.
-   `n=3` goodness criterion.
-   Lemma A.
-   Unique `Σ=4` obstruction.
-   Individual spread-1 lemma.
-   Compression lemma.
-   Two-set balance theorem.
-   Equal-split consequence for `3 | |D_i|`.
-   Residue/sign formulation.
-   Constraint taxonomy through `d_i=4`.

## Do not restart

Do not redo:

-   CRI-depth;
-   broad spread-2 selector searches;
-   balanced-size selectors;
-   nonempty-bundle selectors;
-   common-pivotal-item arguments;
-   the discarded merged-two-bundle argument.

## Main task

Attack:

``` text
Target T:
three sets
→ two spread ≤ 1
→ third spread ≤ 2.
```

## Preferred representation

Use the seven Venn regions and their residues modulo `3`.

Do not immediately return to the envy graph.

## Verification requirement

Every claimed new lemma must be tested against:

-   additive;
-   capped;
-   threshold;
-   arbitrary monotone `0/1`-marginal composed costs.

A computational pattern is evidence only. A theorem requires a
mathematical proof.

------------------------------------------------------------------------

# 24. Final status table

  -----------------------------------------------------------------------
  Statement                           Status
  ----------------------------------- -----------------------------------
  Normalised matching formulation     **proved**

  `n=3` goodness criterion            **proved**

  Lemma A: `Σ≤3 ⇒ good`               **proved**

  Unique `Σ=4` obstruction            **proved**

  Individual spread ≤1                **proved**

  Two-set balance theorem             **proved**

  Compression for composed costs      **proved**

  Equal split when `3 | |D_i|`        **proved**

  Residual composed instances contain **observed/computational**
  a divisible set in tested corpus    

  Residual reduction to `Σ≤3`         **proved conditionally on Target
                                      T**

  Target T `(1,1,2)`                  **OPEN**

  Lemma E                             **OPEN**

  F5\* for `n=3`                      **OPEN**

  Conjecture 2 for `n=3`              **OPEN**
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 25. One-line research objective

The entire next phase should be understood as:

> **Prove that three arbitrary sets can be 3-coloured so that two have
> discrepancy at most one and the third has discrepancy at most two;
> then use the divisible-set structure and compression of the residual
> composed family to obtain `Σ≤3`, invoke Lemma A, and close Conjecture
> 2 for `n=3`.**

This is the current cleanest mathematical target.
