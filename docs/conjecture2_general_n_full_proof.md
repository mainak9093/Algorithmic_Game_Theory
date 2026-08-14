# Conjecture 2 for Arbitrary n — Full Audited Proof

## Status

**Theorem:** Conjecture 2 holds for every number `n` of agents for the full class of dichotomous / binary-marginal chore costs.

The proof has one external input: the Tao–Wu–Yu–Zhou (TWYZ) theorem and the terminal behavior of their Algorithm 3. Everything after the TWYZ terminal partial allocation is proved here.

The TWYZ paper proves that, for general cost functions with binary marginals, a polynomial-time algorithm produces an envy-free partial allocation with at most `n-1` unallocated chores. Its Algorithm 3 uses an equality graph and, when the first two update rules are unavailable, chooses a tail strongly connected component; if fewer than `|S|` chores remain, the algorithm terminates. citeturn898728search0turn898728search1

The completion argument below is a new deduction from that terminal structure; it is not being attributed to TWYZ.

---

# 1. Definitions

There are `n` agents, indexed by `[n]`, and a finite set `M` of indivisible chores.

Agent `i` has a cost function

\[
c_i:2^M\to \mathbb Z_{\ge 0}
\]

satisfying

\[
c_i(\varnothing)=0
\]

and, for every `S ⊆ M` and `e ∉ S`,

\[
c_i(S\cup\{e\})-c_i(S)\in\{0,1\}.
\tag{D}
\]

An allocation is `A=(A_1,...,A_n)` with the bundles partitioning `M`.

A subsidy vector is

\[
p=(p_1,\ldots,p_n)\in\{0,1\}^n.
\]

The allocation is envy-free with subsidies `p` if

\[
c_i(A_i)-p_i\le c_i(A_j)-p_j
\qquad\forall i,j.
\tag{EF}
\]

This is the statement of Conjecture 2.

---

# 2. Elementary facts about dichotomous costs

Because all marginals lie in `{0,1}`, every cost function is monotone:

\[
S\subseteq T\implies c_i(S)\le c_i(T).
\tag{M}
\]

Also every cost is an integer. For `S={e_1,...,e_k}`, telescope along a chain from `∅` to `S`; the increments are all `0` or `1`. Hence

\[
c_i(S)\in\mathbb Z_{\ge0}.
\tag{I}
\]

Therefore whenever

\[
c_i(S)<c_i(T),
\]

we automatically have

\[
c_i(S)\le c_i(T)-1.
\tag{I1}
\]

---

# 3. External starting theorem: TWYZ partial EF

We use the following published result.

> **TWYZ partial-EF theorem.** For any number `n` of agents and arbitrary binary-marginal cost functions, Algorithm 3 computes in polynomial time a partial allocation
> `X=(X_1,...,X_n)` that is envy-free with zero subsidy and leaves at most `n-1` chores unallocated.

The equality graph has an edge `i -> j` exactly when

\[
c_i(X_i)=c_i(X_j).
\tag{E}
\]

The algorithm maintains partial EF and uses three update rules:

1. If an unallocated chore has marginal cost `0` on some agent's own bundle, allocate it.
2. If an equality edge lies on a directed cycle and some unallocated chore has marginal `0` to the target bundle from the source agent's perspective, perform the cycle rotation that allocates it.
3. Otherwise choose a tail SCC `S` of the equality graph. If at least `|S|` chores remain, allocate one arbitrary remaining chore to each agent in `S`. If fewer than `|S|` remain, terminate.

These statements are contained in the description/proof of Algorithm 3 and Theorem 5.1 in the published work. citeturn898728search0turn898728search1

Run this algorithm and let

\[
X=(X_1,\ldots,X_n)
\]

be its terminal partial allocation.

Let

\[
R=M\setminus\bigcup_i X_i,
\qquad r=|R|.
\]

Then

\[
0\le r\le n-1.
\tag{3.1}
\]

If `r=0`, the allocation is already complete and EF with `p=0`. Hence assume `r≥1`.

At termination, the chosen tail SCC `S` satisfies

\[
r<|S|.
\tag{3.2}
\]

This strict inequality is the central counting fact.

---

# 4. Terminal marginal facts

## Lemma 1 — every leftover has marginal 1 on every own bundle

For every agent `i` and every leftover `e∈R`,

\[
\boxed{c_i(e\mid X_i)=1.}
\tag{4.1}
\]

### Proof

If `c_i(e|X_i)=0`, update rule 1 of Algorithm 3 would still apply. Since the algorithm has terminated, this is impossible. Binary marginality leaves only `1`. ∎

---

## Lemma 2 — equality edges inside the terminal SCC have leftover marginal 1

Suppose `i,j∈S` and

\[
c_i(X_i)=c_i(X_j).
\tag{4.2}
\]

Then for every leftover `e∈R`,

\[
\boxed{c_i(e\mid X_j)=1.}
\tag{4.3}
\]

### Proof

Equation (4.2) is the equality-graph edge `i -> j`. Since `S` is strongly connected, that edge lies on a directed cycle. If some leftover `e` had `c_i(e|X_j)=0`, update rule 2 would apply on that cycle. The algorithm has terminated, so this cannot happen. Hence the binary marginal is `1`. ∎

---

# 5. Choose where the leftover chores go

Because

\[
r<|S|,
\]

choose `r` distinct agents inside `S`:

\[
T=\{t_1,\ldots,t_r\}\subset S.
\]

Choose any bijection

\[
e_k\longmapsto t_k
\]

from the leftover set `R={e_1,...,e_r}` to `T`.

Define the completed bundles

\[
A_i=
\begin{cases}
X_i\cup\{e_k\},&i=t_k,\\
X_i,&i\notin T.
\end{cases}
\tag{5.1}
\]

Thus each recipient in `T` receives exactly one leftover, and everyone else receives none.

---

# 6. Which agents receive subsidy 1?

Giving subsidy `1` to each recipient compensates its one-unit own cost increase. For `n>3`, however, an additional issue appears: an agent outside the terminal SCC can have an equality edge into a subsidized recipient. That agent also needs subsidy `1`.

Define the subsidy set `P` as the following backward equality closure:

1. Initially put every recipient in `T` into `P`.
2. If `i∉S` and there exists `j∈P` such that
   \[
   c_i(X_i)=c_i(X_j),
   \tag{6.1}
   \]
   then add `i` to `P`.
3. Repeat until no new agent can be added.

Equivalently, `P` consists of `T` together with all agents outside `S` that can reach some member of `T` through a directed path of equality edges whose vertices outside `S` are processed backward from the target.

Set

\[
\boxed{
 p_i=
 \begin{cases}
 1,&i\in P,\\
 0,&i\notin P.
 \end{cases}}
\tag{6.2}
\]

---

# 7. Subsidy budget

The set `P` contains:

- exactly `r` chosen recipients from `S`, and
- at most `n-|S|` agents outside `S`.

Therefore

\[
|P|\le r+(n-|S|).
\]

Using `r<|S|`,

\[
|P|<n.
\]

Since `|P|` is integral,

\[
\boxed{|P|\le n-1.}
\tag{7.1}
\]

Hence

\[
p\in\{0,1\}^n,
\qquad
\sum_i p_i\le n-1.
\]

The subsidy budget is therefore exactly of the form required by Conjecture 2.

---

# 8. The key one-unit-gap observation

Fix an agent `i` and a bundle index `j`.

Because the partial allocation is EF,

\[
c_i(X_i)\le c_i(X_j).
\tag{8.1}
\]

If the inequality is strict, integrality gives

\[
\boxed{c_i(X_i)\le c_i(X_j)-1.}
\tag{8.2}
\]

If equality holds,

\[
c_i(X_i)=c_i(X_j),
\tag{8.3}
\]

then `i -> j` is an equality edge.

There are two important cases for equality:

- if `i,j∈S`, Lemma 2 says every leftover has marginal `1` on `X_j` from agent `i`'s perspective;
- if `j∈P` and `i∉S`, the backward-closure definition forces `i∈P`, contradiction.

This dichotomy is what prevents an unsubsidized agent from being exactly tied with a subsidized bundle.

---

# 9. Prove envy-freeness

We prove

\[
c_i(A_i)-p_i
\le
c_i(A_j)-p_j
\qquad\forall i,j.
\tag{9.1}
\]

There are four structurally relevant cases.

---

## Case 1: `i` is a recipient (`i∈T`)

Then `p_i=1`, and by Lemma 1,

\[
c_i(A_i)=c_i(X_i)+1.
\]

Thus

\[
c_i(A_i)-p_i=c_i(X_i).
\tag{9.2}
\]

### 1a. `j∉T`

Then `A_j=X_j`.

If `j∈P`, then `p_j=1`, so

\[
c_i(A_j)-p_j=c_i(X_j)-1.
\]

Since `i∈S` and `j∈P\setminus T` cannot be outside `S` with equality into `j` (the terminal SCC is a tail), the only potentially dangerous case is equality inside `S`; there `j∈S` and both subsidies are equal. In all cases the original EF inequality plus integrality gives the needed bound.

More explicitly:

- if `c_i(X_i)<c_i(X_j)`, then
  \[
  c_i(X_i)\le c_i(X_j)-1;
  \]
- if equality holds and `j∈S`, then `i->j` is an equality edge inside `S`, so Lemma 2 gives the necessary unit marginal whenever `j` is augmented; if `j` is not a recipient then both completed bundles are unchanged and equal old costs with equal subsidy.

Thus (9.1) holds.

### 1b. `j∈T`

Both agents receive one leftover and both subsidies are `1`.

If

\[
c_i(X_i)<c_i(X_j),
\]

integrality gives a one-unit gap and the claim follows.

If

\[
c_i(X_i)=c_i(X_j),
\]

then `i->j` is an equality edge inside `S`; Lemma 2 gives

\[
c_i(A_j)=c_i(X_j)+1=c_i(X_i)+1.
\]

Therefore

\[
c_i(A_j)-1=c_i(X_i)=c_i(A_i)-1.
\]

So there is no envy.

---

## Case 2: `i∈P\setminus T`

Then `A_i=X_i` and `p_i=1`.

Hence

\[
c_i(A_i)-p_i=c_i(X_i)-1.
\]

Because the original partial allocation is EF and every completed bundle satisfies

\[
c_i(A_j)\ge c_i(X_j),
\]

we have

\[
c_i(A_i)-p_i
=c_i(X_i)-1
\le c_i(X_j)-1
\le c_i(A_j)-p_j.
\]

Thus `i` does not envy anyone.

---

## Case 3: `i∉P` and `j∉P`

Since every recipient belongs to `P`, agent `i` receives no leftover, so

\[
A_i=X_i,
\qquad p_i=0.
\]

Similarly, `j` receives no leftover and `p_j=0`.

By original partial EF and monotonicity,

\[
c_i(A_i)=c_i(X_i)
\le c_i(X_j)
\le c_i(A_j).
\]

Hence (9.1) holds.

---

## Case 4: `i∉P` and `j∈P`

Now `p_i=0`, `p_j=1`.

There are two subcases.

### 4a. `j∈T`

Then `j` receives a leftover.

If `i∈S` and

\[
c_i(X_i)=c_i(X_j),
\]

then `i->j` is an equality edge inside `S`; Lemma 2 gives marginal `1` on the recipient bundle, so

\[
c_i(A_j)=c_i(X_j)+1=c_i(X_i)+1.
\]

Thus

\[
c_i(A_i)=c_i(X_i)=c_i(A_j)-1.
\]

If equality does not hold, integrality gives

\[
c_i(X_i)c_i(X_j)-1,
\]

and monotonicity gives

\[
c_i(A_i)
=c_i(X_i)
\le c_i(X_j)-1
\le c_i(A_j)-1.
\]

If `i∉S`, equality would make `i` an equality-edge predecessor of recipient `j`, which would put `i` in `P` by definition. Since `i∉P`, equality is impossible; therefore the one-unit-gap argument applies.

Hence

\[
c_i(A_i)-p_i
\le
c_i(A_j)-p_j.
\]

### 4b. `j∈P\setminus T`

Then `A_j=X_j` and `p_j=1`.

If `i∉S` and equality held, the backward closure would force `i∈P`, contradiction. Therefore

\[
c_i(X_i)<c_i(X_j),
\]

and hence

\[
c_i(A_i)=c_i(X_i)
\le c_i(X_j)-1
=c_i(A_j)-p_j.
\]

If `i∈S`, then an equality edge `i->j` cannot leave the tail SCC `S` because `S` has no outgoing equality edges. Hence equality is impossible here as well, and again the one-unit-gap argument gives the result.

Thus (9.1) holds.

---

# 10. Completion theorem

We have proved:

> **Terminal Completion Theorem.**
> Let `X` be a terminal partial-EF allocation produced by TWYZ Algorithm 3, let `R` be its leftover set with `r=|R|`, and let `S` be the terminal tail SCC. Choose `r` recipients inside `S`, assign one leftover to each, and define `P` as the backward equality closure of the recipients through agents outside `S`. Then the resulting complete allocation is envy-free with subsidies
> 
> \[
> p_i=1_{i\in P},
> \]
> 
> and
> \[
> |P|\le n-1.
> \]

The proof uses only binary marginality, integrality, partial EF, the terminal SCC condition, and the two terminal consequences of Algorithm 3.

---

# 11. Polynomial-time construction

The algorithm is constructive.

1. Run TWYZ Algorithm 3.
2. Read the leftover set `R` and terminal tail SCC `S`.
3. Choose any `r=|R|` distinct agents from `S`.
4. Assign the `r` leftovers injectively to those agents.
5. Build the equality graph using the already-computed partial bundles.
6. Compute backward reachability from the chosen recipients, restricted to agents outside `S`.
7. Give subsidy `1` to the resulting set `P` and `0` to everyone else.

The additional work after TWYZ is a constant number of graph operations and an injection of at most `n-1` items. Therefore the entire procedure is polynomial-time.

---

# 12. Main theorem — Conjecture 2 for arbitrary n

> **Theorem.** For every finite binary-marginal / dichotomous chore instance with any number `n` of agents, there exists a complete allocation `A` and a subsidy vector
> \[
> p\in\{0,1\}^n
> \]
> satisfying
> \[
> c_i(A_i)-p_i\le c_i(A_j)-p_j
> \qquad\forall i,j.
> \]
> Moreover, such an outcome can be computed in polynomial time and uses total subsidy at most `n-1`.

### Proof

Run TWYZ Algorithm 3.

- If no chores remain unallocated, the output is already a complete EF allocation with `p=0`.
- Otherwise, let `R` and `S` be the terminal leftover set and tail SCC. Since `|R|<|S|`, choose `|R|` distinct recipients inside `S`.
- Assign one leftover chore to each recipient.
- Form the backward equality closure `P` outside `S`.
- Subsidize precisely the agents in `P` by `1`.

By the Terminal Completion Theorem, the resulting complete allocation is EF. By the counting argument,

\[
|P|\le n-1.
\]

TWYZ is polynomial-time, and the completion is polynomial-time.

Therefore Conjecture 2 holds for arbitrary `n`. \(\square\)

---

# 13. Why the n=3 proof was the special case

For `n=3`, if two chores remain then

\[
|R|=2<|S|\le3,
\]

so necessarily

\[
|S|=3.
\]

Thus the terminal SCC contains every agent, and the backward-closure construction reduces to the simpler `n=3` proof.

For general `n`, `S` may be a proper subset of the agents. The new ingredient is precisely the backward equality closure outside `S`.

The counting inequality

\[
|P|\le |R|+(n-|S|)<n
\]

replaces the `n=3` fact that the terminal SCC equals the whole agent set.

---

# 14. What this does NOT prove

This proof does **not** establish the stronger spread statement

\[
\exists (B_1,\\ldots,B_3):
\sum_i
\left[
\max_t c_i(B_t)-\min_t c_i(B_t)
\right]
\le3.
\]

That is the project's Lemma E / spread route and is logically separate.

Likewise, this proof does not use the old `Saturation` lemma or any finite bounded-cost enumeration.

---

# 15. Attribution boundary

TWYZ establish the starting partial-EF theorem and Algorithm 3. The following are the new deductions in this proof record:

1. choose the leftover recipients inside the terminal tail SCC;
2. define the backward equality closure outside the SCC;
3. prove the subsidy bound
   \[
   |P|\le r+n-|S|<n;
   \]
4. prove that the resulting completed allocation is EF.

The full conjecture follows by combining those deductions with the published TWYZ starting theorem. citeturn898728search0turn898728search1

---

# Final status

\[
\boxed{
\textbf{CONJECTURE 2 IS PROVED FOR ALL }n.
}
\]

The essential new mechanism is:

\[
\boxed{
\text{leftover recipients in terminal SCC}
\;+
\text{backward equality closure}
\;+
(r+n-|S|<n)
\;\Longrightarrow\;
\text{complete EF with }p\in\{0,1\}^n.
}
\]
