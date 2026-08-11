# Conjecture 2 for n = 3 — Verification Dossier
## Status, exact dependency chain, and proof audit

**Purpose.** This document is a self-contained research record for an AI agent continuing the negative-dichotomous fair-division project. It isolates exactly what is proved, what is conditional, and what must still be verified before Conjecture 2 for `n = 3` can be declared a theorem.

**Important status warning.** The current project source files do **not** contain a certified proof of the Target Theorem. They explicitly still mark the Target Theorem and Lemma E as open. Therefore this dossier does **not** falsely promote the previous conversational claim into a theorem. Instead it records the complete proof chain that would close Conjecture 2 for `n = 3` *if Target T is supplied with a rigorous proof*, and it identifies every place that must be checked.

---

# 1. Problem statement

We work with a finite set of indivisible chores/items

\[
M,\qquad |M|=m,
\]

and three agents

\[
N=\{1,2,3\}.
\]

Agent `i` has a **negative dichotomous valuation/cost**

\[
c_i:2^M\to\mathbb Z_{\ge 0},
\]

normalized by

\[
c_i(\varnothing)=0,
\]

and satisfying

\[
c_i(S)-c_i(S\cup\{g\})\in\{0,1\}
\]

for every `S` and every `g\notin S`.

Equivalently, adding one chore changes the cost by either `0` or `1`.

For an allocation

\[
A=(A_1,A_2,A_3)
\]

define the cost matrix

\[
C^A_{ij}=c_i(A_j).
\]

The goal is an allocation for which every agent has subsidy at most `1` in an envy-free solution.

For `n=3`, the project has already reduced this to the following existence statement:

> **F5\*(n=3).** There exists a partition `B=(B_1,B_2,B_3)` with total cost-spread
>
> \[
> \Sigma(B):=\sum_{i=1}^3
> \left(
> \max_t c_i(B_t)-\min_t c_i(B_t)
> \right)
> \le 3.
> \]

The established minimum-assignment lemma then turns such a partition into a good minimum-cost assignment.

---

# 2. Conjecture 2

The project's main conjecture is:

> **Conjecture 2.** For every negative-dichotomous instance there exists an envy-free allocation with subsidy vector
>
> \[
> p\in\{0,1\}^n,
> \]
>
> and hence total subsidy at most `n-1`, with a polynomial-time algorithm producing it.

For `n=3`, the existence part is equivalent to finding an allocation whose longest-path envy labels are at most `1`.

The project records the reduction

\[
\text{Conjecture 2}
\Longleftarrow
\texttt{h1prime}
\Longleftarrow
\texttt{balance-rule},
\]

but this is the broader all-`n` program. The present dossier concerns the separate `n=3` route through F5*.

---

# 3. Normalized costs for a fixed partition

Fix a partition

\[
B=(B_1,B_2,B_3).
\]

For each agent `i`, define

\[
v_i(t)
=
c_i(B_t)-\min_{s\in\{1,2,3\}}c_i(B_s).
\]

Then:

1. `v_i(t) >= 0`;
2. at least one `v_i(t)` is zero;
3. the spread of agent `i` is

\[
\operatorname{sp}_i(B)
=
\max_t v_i(t);
\]

4. hence

\[
\Sigma(B)
=
\sum_i\max_t v_i(t).
\]

Now let `σ` be a minimum-cost assignment of bundles to agents. Then

\[
\sum_i c_i(B_{\sigma(i)})
=
\sum_i v_i(\sigma(i))
+
\text{constant}.
\]

Therefore `σ` minimizes

\[
F(\sigma)
=
\sum_i v_i(\sigma(i)).
\]

This is the assignment problem used throughout the `n=3` proof.

---

# 4. The established bridge: total spread <= 3 implies goodness

For a fixed partition and a minimum-cost assignment `σ`, define

\[
x_i=v_i(\sigma(i)).
\]

The project establishes the following `n=3` criterion.

> **Lemma A / goodness lemma.**
>
> If
>
> \[
> \Sigma(B)\le3,
> \]
>
> then every minimum-cost assignment is good: its envy graph has longest directed path weight at most `1`.

The proof works through the normalized matrix `v_i(t)` and the minimum assignment objective `F(σ)`.

The critical fact is that for `n=3` a bad assignment would require a normalized cost pattern whose total spread exceeds `3`; hence `Σ<=3` rules out all bad cases.

This lemma is treated as established in the project and should be reused rather than reproved.

---

# 5. Therefore the real n=3 existence target is Lemma E

Define

\[
\Sigma(B)=\sum_i\operatorname{sp}_i(B).
\]

Then:

> **Lemma E.**
>
> Every three-agent negative-dichotomous instance has a partition `B` with
>
> \[
> \Sigma(B)\le3.
> \]

Together with Lemma A:

\[
\boxed{
\text{Lemma E}
\Longrightarrow
\text{F5* at }n=3
\Longrightarrow
\text{Conjecture 2 at }n=3.
}
\]

The current project files explicitly record Lemma E as open.

---

# 6. Structural reduction to the residual family

The project has already isolated several families that do not require the difficult residual argument.

The important solved classes include:

- binary-additive cases;
- identical/two-agent cases where applicable;
- small-bundle cases;
- uniformly balanced cases.

Thus the difficult branch is the **residual family**.

For the residual instances actually arising in the current `n=3` development, the important structural family is the composed family

\[
c_i(S)=f_i(|S\cap D_i|),
\]

where

\[
f_i:\mathbb Z_{\ge0}\to\mathbb Z_{\ge0}
\]

is monotone and has increments in `{0,1}`.

---

# 7. Compression lemma for composed costs

For

\[
c(S)=f(|S\cap D|)
\]

with monotone `0/1` increments, `f` is monotone and 1-Lipschitz.

For any partition `B`, let

\[
a_t=|B_t\cap D|.
\]

Then

\[
\operatorname{sp}_c(B)
=
f(\max_t a_t)-f(\min_t a_t)
\le
\max_t a_t-\min_t a_t.
\]

Therefore:

> **Compression Lemma.**
>
> \[
> \boxed{
> \operatorname{sp}_{c}(B)
> \le
> \operatorname{sp}_{D}(B)
> }
> \]

where the right-hand side is the ordinary count discrepancy of `D`.

Consequently a set-count discrepancy certificate automatically yields a cost-spread certificate.

---

# 8. Divisible-set lemma

Suppose

\[
3\mid |D|.
\]

Choose a partition satisfying

\[
|D\cap B_1|
=
|D\cap B_2|
=
|D\cap B_3|
=
|D|/3.
\]

Then for a composed cost

\[
c(S)=f(|S\cap D|)
\]

we have

\[
c(B_1)=c(B_2)=c(B_3).
\]

Hence

\[
\boxed{\operatorname{sp}_c(B)=0.}
\]

This holds for every monotone `0/1` increment function `f`; no linearity is needed.

This is one of the main reasons divisibility by `3` is so useful in the residual case.

---

# 9. Three-set representation

For three underlying sets

\[
D_1,D_2,D_3\subseteq M,
\]

partition `M` into the seven nonempty Venn regions:

\[
R_1,\ R_2,\ R_3,\ R_{12},\ R_{13},\ R_{23},\ R_{123}.
\]

For every region,

\[
|R|=3q_R+b_R,
\qquad
b_R\in\{0,1,2\}.
\]

The `3q_R` elements can be distributed cyclically:

\[
1,2,3,\;1,2,3,\ldots
\]

so that every set containing that region receives exactly the same number in each bundle.

Therefore only the residue

\[
b_R\in\{0,1,2\}
\]

affects discrepancy.

This reduces the underlying set problem to a finite seven-region residue problem.

---

# 10. Residual colouring variables

For a region with residue `0` there is no residual choice.

For residue `1`, one residual element is assigned to one colour:

\[
e_1,\ e_2,\ e_3.
\]

For residue `2`, equivalently choose the omitted colour:

\[
e_1+e_2,\quad
e_1+e_3,\quad
e_2+e_3.
\]

Thus every active region has only seven possible residual colour patterns.

The residual problem is therefore finite after quotienting out complete triples.

---

# 11. Theorem S: the established two-set precursor

The project has an established theorem for **two underlying sets**:

> **Theorem S.**
>
> For any two sets `D,E`, there is a 3-colouring such that both sets have count spread at most `1`.

This is the key predecessor to Target T.

For a set whose total cardinality is divisible by `3`, spread `<=1` forces spread `0`, because a count vector of total divisible by `3` cannot have spread exactly `1`.

Thus:

> If
>
> \[
> 3\mid |D|,
> \]
>
> Theorem S can make `D` exactly balanced while simultaneously keeping the second set within `1`.

---

# 12. Target Theorem T

The desired set-level theorem is:

> **Target T.**
>
> For any three sets
>
> \[
> D_1,D_2,D_3,
> \]
>
> there exists a 3-colouring such that, after relabelling the sets,
>
> \[
> \boxed{
> \operatorname{sp}(D_1)\le1,\qquad
> \operatorname{sp}(D_2)\le1,\qquad
> \operatorname{sp}(D_3)\le2.
> }
> \]

The stronger computational claim previously discussed was that the total set spread can in fact be at most `2` in the unrestricted three-set problem. **That stronger claim must not be used in a formal proof unless its exhaustive certificate and correctness have been independently verified.**

For the Conjecture-2 `n=3` bridge, only Target T is required.

---

# 13. Exact logical bridge from Target T to the residual composed case

Assume Target T is rigorously proved.

Take a residual composed instance

\[
c_i(S)=f_i(|S\cap D_i|).
\]

The residual structural analysis supplies a set `D_r` with

\[
3\mid |D_r|.
\]

Apply Target T to the three underlying sets.

Arrange the labels so that the divisible set occupies one of the two spread-`<=1` positions.

Then

\[
\operatorname{sp}_{D_r}\le1.
\]

But since

\[
3\mid |D_r|,
\]

we actually have

\[
\operatorname{sp}_{D_r}=0.
\]

For the other two sets Target T gives

\[
\operatorname{sp}_{D_j}\le1,
\qquad
\operatorname{sp}_{D_k}\le2.
\]

By compression,

\[
\operatorname{sp}_{c_r}\le0,
\]

\[
\operatorname{sp}_{c_j}\le1,
\]

\[
\operatorname{sp}_{c_k}\le2.
\]

Therefore

\[
\boxed{
\Sigma(B)
\le0+1+2
=3.
}
\]

This is exactly Lemma E for the residual composed instance.

---

# 14. Completion of the n=3 proof, conditional on Target T

We now have:

1. Target T gives the set-spread profile

\[
(1,1,2).
\]

2. The residual structural theorem supplies a divisible underlying set.

3. Divisibility upgrades its spread `<=1` to spread `0`.

4. Compression transfers set discrepancy to composed dichotomous costs.

Therefore:

\[
\boxed{\Sigma(B)\le3.}
\]

Then Lemma A applies.

Choose a minimum-cost assignment `σ` of the three bundles.

Its envy graph is good:

\[
\max_i\ell_A(i)\le1.
\]

Set

\[
p_i=\ell_A(i).
\]

Then

\[
p_i\in\{0,1\}.
\]

The envy-free condition follows from the standard shortest/longest-path subsidy construction used in the project.

Since the normalized envy graph has at least one zero label,

\[
\min_i p_i=0,
\]

so

\[
\sum_i p_i\le2.
\]

Hence the `n=3` Conjecture-2 existence claim follows.

---

# 15. The exact theorem chain

The complete conditional proof can be written compactly as:

\[
\boxed{
\begin{array}{c}
\text{Target T}\\
\Downarrow\\
\text{residual composed instance admits}\\
(\operatorname{sp}_1,\operatorname{sp}_2,\operatorname{sp}_3)
\le(0,1,2)\\
\Downarrow\\
\Sigma\le3\\
\Downarrow\\
\text{Lemma A}\\
\Downarrow\\
\text{minimum-cost assignment is good}\\
\Downarrow\\
\exists\,p\in\{0,1\}^3\\
\Downarrow\\
\text{Conjecture 2 for }n=3.
\end{array}}
\]

The non-residual families are handled separately by their already-established lemmas.

---

# 16. What is NOT part of this proof

The following statements must not be silently substituted into the proof:

### 16.1 Arbitrary dichotomous Lemma D

The statement

> every two arbitrary dichotomous costs admit a bipartition simultaneously giving spread `<=1`

is **not certified**.

There is a proof attempt in `lemma_D_full_proof.md`, but the project explicitly warns not to treat it as proved.

### 16.2 Uniform balance of three arbitrary sets

False in general.

The standard `K_4` obstruction is:

\[
D_1=\{1,2,3\},\quad
D_2=\{1,2,4\},\quad
D_3=\{1,3,4\}.
\]

Each set has size `3`, so exact balance would require each of the three vertices of every triangle to receive different colours.

The three triangles force all six edges of `K_4` to be bichromatic, which would require a proper 3-colouring of `K_4`, impossible.

Thus one cannot replace Target T by uniform balance.

### 16.3 “Any spread-2 partition works”

False.

The project has explicit computational counterexamples showing that merely having small total spread is insufficient for the original assignment-selection argument.

### 16.4 Balanced bundle sizes

Not a valid selector.

### 16.5 Nonempty bundles

Not a valid selector.

### 16.6 The all-n theorem

Target T does not by itself prove Conjecture 2 for arbitrary `n`.

The present dossier closes only the `n=3` route, conditional on a certified Target-T proof.

---

# 17. Verification checklist for an AI agent

Before marking the theorem `PROVED`, verify the following in order.

## A. Cost-model verification

- [ ] Negative dichotomous means every marginal cost increment is `0` or `1`.
- [ ] Costs are normalized consistently.
- [ ] The envy/subsidy convention matches the project definitions.

## B. Assignment lemma

- [ ] The normalized-cost representation is correct.
- [ ] Minimum-cost bundle assignment minimizes `F(σ)`.
- [ ] Lemma A really proves `Σ<=3 => good` for `n=3`.

## C. Residual reduction

- [ ] Every non-residual case is already covered.
- [ ] The residual family is indeed of composed form where Target T is being applied.
- [ ] The existence of a divisible underlying set is a theorem, not merely a computational observation.

## D. Compression

- [ ] Each `f_i` is monotone.
- [ ] Every increment is in `{0,1}`.
- [ ] Therefore `f_i` is 1-Lipschitz.
- [ ] Hence cost spread is bounded by count spread.

## E. Target T

This is the critical item:

- [ ] For every three sets, construct a colouring with profile `<= (1,1,2)`.
- [ ] If using the seven-region residue reduction, prove that the reduction preserves spread exactly.
- [ ] If using exhaustive enumeration, provide the complete state space and a machine-checkable certificate.
- [ ] If using a structural proof, verify every residue configuration/case.
- [ ] Do not replace a proof with “no counterexample was found”.

## F. Final conversion

- [ ] Divisible set gets spread `0`, not merely `1`.
- [ ] Total cost spread is at most `3`.
- [ ] Apply Lemma A.
- [ ] Construct subsidies from the good envy graph.
- [ ] Verify every subsidy is `0` or `1`.

Only after all boxes are checked should the status be changed to:

\[
\boxed{\text{CONJECTURE 2 PROVED FOR }n=3.}
\]

---

# 18. Current project status — authoritative audit

The source research files currently say:

- Theorem S: **proved**.
- Lemma X: **proved**.
- Corollary Y: **proved**.
- Theorem Z: **proved**.
- Target T: **open**.
- Lemma E: **open**.
- Lemma D for arbitrary dichotomous costs: **open**.
- F5* at `n=3`: **not closed**.

Therefore, as of the source state used to construct this document, the rigorous mathematical status is:

\[
\boxed{
\text{Conjecture 2 for }n=3
\text{ is CONDITIONAL on Target T.}
}
\]

The conversational claim that Target T has already been solved must therefore be treated as a **candidate result requiring verification**, not as a certified theorem.

---

# 19. What would constitute a genuine final proof

A future AI agent should not simply repeat the chain above.

It should produce one of the following:

### Option 1 — Human-readable proof of Target T

A finite structural proof that covers every possible seven-region residue pattern, with no omitted cases.

Then the chain in Sections 13–15 becomes a formal proof.

### Option 2 — Certified finite proof

Provide:

1. a precise finite state space;
2. an exact enumeration algorithm;
3. a proof that the enumeration represents every arbitrary finite three-set instance;
4. a complete certificate/checksum or independently reproducible verifier;
5. the result that every state admits the required colouring.

Then Target T is a computer-assisted theorem.

### Option 3 — Stronger theorem

Prove a stronger statement such as

\[
\min_B
\sum_i\operatorname{sp}_{D_i}(B)\le2
\]

for all triples of sets.

If rigorously proved, this immediately implies Target T.

---

# 20. AI-agent continuation instruction

A new AI agent reading this file should **not** restart the entire negative-dichotomous project.

It should begin with exactly one question:

> **Is Target T actually proved?**

If yes, inspect the proof line-by-line and verify Sections 13–15.

If no, the next mathematical task is:

\[
\boxed{
\textbf{Prove or refute Target T rigorously.}
}
\]

Do not attack arbitrary dichotomous Lemma D first.

Do not restart the Barman positive-cost peel algorithm.

Do not restart the already refuted CRI-depth, balanced-size, nonempty-bundle, or arbitrary spread-2 selector routes.

The entire `n=3` project has now been reduced to this sharply defined bottleneck.

---

# 21. Final dependency graph

```text
                    TARGET T
             (three-set discrepancy)
                       |
                       v
        residual composed n=3 instance
                       |
          divisible underlying D_r
                       |
             compression lemma
                       |
                       v
              cost spreads <= (0,1,2)
                       |
                       v
                   Sigma <= 3
                       |
                       v
                   Lemma A
                       |
                       v
             good minimum-cost
                 assignment
                       |
                       v
             subsidy labels <= 1
                       |
                       v
          CONJECTURE 2, n = 3
```

And the logical status is:

```text
Theorem S        PROVED
Lemma X          PROVED
Corollary Y      PROVED
Compression      PROVED
Divisible-set    PROVED
Lemma A          PROVED
Target T         OPEN in current certified files
Lemma E          OPEN
F5* n=3          OPEN
Conjecture 2 n=3 CONDITIONAL ON TARGET T
Conjecture 2 all n OPEN
```

This distinction is essential for future proof integrity.
