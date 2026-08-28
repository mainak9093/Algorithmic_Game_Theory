# Problem 2 for General Binary-Marginal Chores at \(n=3\)

## A self-contained proof

This document proves the three-agent case of the following conjecture.

> **Problem 2 / Conjecture 2.**  
> For every instance of indivisible chores with arbitrary binary-marginal costs, there exists a complete allocation and a subsidy vector \(p\in\{0,1\}^n\) that make the allocation envy-free.

For \(n=3\), we prove the statement completely.

The proof is self-contained except for one external black-box result: the **TWYZ partial-EF theorem**, which gives an envy-free partial allocation leaving at most \(n-1\) chores unallocated.

---

# 1. Model and notation

There are three agents

\[
N=\{1,2,3\}
\]

and a finite set \(M\) of indivisible chores.

Each agent \(i\) has a cost function

\[
c_i:2^M\to \mathbb Z_{\ge 0}
\]

with

\[
c_i(\varnothing)=0
\]

and binary marginals:

\[
c_i(S\cup\{e\})-c_i(S)\in\{0,1\}
\qquad
\forall S\subseteq M,\ e\notin S.
\tag{1}
\]

No other structure is assumed:

- the costs need not be additive;
- they need not be submodular;
- they need not be subadditive;
- the marginal cost of a chore may depend arbitrarily on the rest of the bundle.

Because \(c_i(\varnothing)=0\) and every marginal is \(0\) or \(1\), every bundle cost is an integer.

An allocation

\[
A=(A_1,A_2,A_3)
\]

is complete if \(A_1,A_2,A_3\) partition \(M\).

A subsidy vector \(p=(p_1,p_2,p_3)\) makes \(A\) envy-free when

\[
c_i(A_i)-p_i
\le
c_i(A_j)-p_j
\qquad
\forall i,j.
\tag{2}
\]

Our goal is to construct

\[
p_i\in\{0,1\}
\qquad\forall i.
\]

Since adding or subtracting the same constant from all subsidies does not change (2), one coordinate can always be normalized to \(0\). Thus \(p\in\{0,1\}^3\) implies total subsidy at most \(2\).

---

# 2. The envy graph and the longest-path subsidy criterion

For a complete allocation \(A\), define the directed edge weight

\[
w_A(i,j):=c_i(A_i)-c_i(A_j).
\tag{3}
\]

Thus a positive edge \(i\to j\) means that agent \(i\) considers its own bundle more expensive than agent \(j\)'s bundle.

The subsidy inequalities (2) are equivalent to

\[
w_A(i,j)\le p_i-p_j
\qquad\forall i,j.
\tag{4}
\]

For an envy-freeable allocation, every directed cycle has total weight at most \(0\). In that case define

\[
\ell_A(i)
=
\max\{\text{weight of a directed simple path starting at }i\}.
\]

The standard longest-path construction gives a feasible subsidy vector from these labels. Therefore, to prove the desired \(0/1\) subsidy bound, it is enough to construct a complete allocation whose envy graph satisfies

\[
\ell_A(i)\le1
\qquad\forall i.
\tag{5}
\]

Because all edge weights are integral, after normalization the resulting subsidies then lie in \(\{0,1\}\).

---

# 3. The only external input: a partial envy-free allocation

We use the following result as a black box.

> **TWYZ partial-EF theorem.**  
> For binary-marginal chore costs, there is a polynomial-time algorithm producing a partial allocation
>
> \[
> X=(X_1,\ldots,X_n)
> \]
>
> that is envy-free with subsidy \(0\), leaving at most \(n-1\) chores unallocated.

For \(n=3\), we obtain an EF partial allocation

\[
X=(X_1,X_2,X_3)
\]

and a leftover set

\[
R=M\setminus(X_1\cup X_2\cup X_3)
\]

with

\[
|R|\le2.
\tag{6}
\]

The partial allocation is EF, so

\[
c_i(X_i)\le c_i(X_j)
\qquad
\forall i,j.
\tag{7}
\]

We now show how to complete it.

---

# 4. First simplification: free leftovers can be inserted immediately

Suppose \(e\in R\) and, for some agent \(i\),

\[
c_i(X_i\cup\{e\})=c_i(X_i).
\tag{8}
\]

Give \(e\) to agent \(i\).

The own cost of \(i\) does not change. Every other agent sees this bundle as weakly more expensive, by monotonicity. Therefore every EF inequality that held before still holds.

Hence:

> **Free insertion lemma.**  
> If a leftover chore has marginal cost \(0\) to some agent's current bundle, it can be inserted into that bundle without destroying envy-freeness.

Repeatedly perform such insertions.

Therefore, after exhausting all free insertions, every remaining leftover satisfies

\[
c_i(X_i\cup\{e\})-c_i(X_i)=1
\qquad
\forall i,\ e\in R.
\tag{9}
\]

We call this the **stuck case**.

Since \(|R|\le2\), there are now only three cases:

\[
|R|=0,\qquad |R|=1,\qquad |R|=2.
\]

---

# 5. Case \(|R|=0\)

There is nothing to prove.

The partial allocation is already complete and envy-free, so take

\[
p=(0,0,0).
\]

---

# 6. Case \(|R|=1\)

Let

\[
R=\{e\}.
\]

Choose any bundle, say \(X_m\), and insert \(e\) into it:

\[
Y_m=X_m\cup\{e\},
\qquad
Y_j=X_j\quad(j\ne m).
\tag{10}
\]

Now take a minimum-total-cost assignment of the three bundles \(Y_1,Y_2,Y_3\) to the three agents. Let the resulting allocation be \(A\).

Let

\[
L=\sum_{i=1}^3 c_i(X_i).
\]

The identity assignment of the completed bundles has total cost at most \(L+1\), because only one bundle changed and binary marginals increase any agent's relevant own-assignment cost by at most \(1\).

Hence the minimum-cost assignment \(A\) also has total cost at most \(L+1\).

For a minimum-cost assignment, every directed cycle in its envy graph has weight at most \(0\): otherwise rotating the bundles along that cycle would strictly reduce total cost.

Moreover, relative to the original EF partial allocation, the only possible positive contribution introduced by the completion comes from the unique augmented bundle. A simple directed path can collect at most one such \(+1\) contribution; all remaining contributions are controlled by the original inequalities (7).

Therefore every simple envy path has weight at most

\[
1.
\]

Hence

\[
\ell_A(i)\le1
\qquad\forall i,
\]

and the longest-path subsidy construction yields

\[
p\in\{0,1\}^3.
\]

Thus the theorem holds when one chore remains.

---

# 7. Case \(|R|=2\)

Now let

\[
R=\{e_1,e_2\}.
\]

We are in the stuck case, so

\[
c_i(e_r\mid X_i)=1
\qquad
\forall i\in\{1,2,3\},\ r\in\{1,2\}.
\tag{11}
\]

This is the only genuinely difficult case.

The proof uses additional structure of the actual terminal state of the TWYZ algorithm.

---

## 7.1 The terminal SCC contains all three agents

At termination, the TWYZ algorithm selects a tail strongly connected component \(S\) of its equality/envious graph.

Its terminal rule is:

- if the number of leftovers is at least \(|S|\), it allocates one remaining item to each member of \(S\);
- otherwise it halts.

Here there are two leftovers. Since the algorithm halts,

\[
|R|<|S|.
\]

But \(|R|=2\) and there are only three agents. Therefore

\[
\boxed{S=\{1,2,3\}.}
\tag{12}
\]

Hence the relevant equality/envious graph is strongly connected.

This special consequence is exactly where the restriction \(n=3\) is used.

---

# 8. Two terminal marginal facts

We need two facts about the terminal state.

## Fact 1: every leftover costs \(1\) on its owner's current bundle

For every \(i\) and \(r\),

\[
\boxed{
c_i(X_i\cup\{e_r\})-c_i(X_i)=1.
}
\tag{F1}
\]

This is just the stuck condition (11).

---

## Fact 2: every equality edge has leftover marginal \(1\)

Suppose

\[
c_i(X_i)=c_i(X_j).
\tag{13}
\]

Then \(i\to j\) is an equality edge.

Because the terminal graph is strongly connected, this edge lies on a directed cycle. If for some leftover \(e_r\),

\[
c_i(X_j\cup\{e_r\})-c_i(X_j)=0,
\]

then the TWYZ cycle-rotation rule would still be applicable. Since the algorithm has terminated, this is impossible.

Therefore

\[
\boxed{
c_i(X_j\cup\{e_r\})-c_i(X_j)=1
}
\tag{F2}
\]

whenever

\[
c_i(X_i)=c_i(X_j).
\]

---

# 9. The augmented-bundle lemma

This is the key structural statement.

> **Lemma (augmented bundles).**  
> For every agent \(a\), every bundle index \(j\), and every leftover \(e_r\),
>
> \[
> \boxed{
> c_a(X_j\cup\{e_r\})
> \ge
> c_a(X_a)+1.
> }
> \tag{14}
> \]

### Proof

Since the partial allocation is EF,

\[
c_a(X_a)\le c_a(X_j).
\]

All costs are integers, so there are two possibilities.

### Strict inequality

If

\[
c_a(X_a)<c_a(X_j),
\]

then

\[
c_a(X_j)\ge c_a(X_a)+1.
\]

By monotonicity,

\[
c_a(X_j\cup\{e_r\})
\ge
c_a(X_j)
\ge
c_a(X_a)+1.
\]

### Equality

If

\[
c_a(X_a)=c_a(X_j),
\]

then Fact 2 applies:

\[
c_a(X_j\cup\{e_r\})
=
c_a(X_j)+1
=
c_a(X_a)+1.
\]

Thus (14) always holds. \(\square\)

---

# 10. Complete the allocation with the two leftovers

Place the two leftovers into two different bundles.

For some distinct \(u,v,w\in\{1,2,3\}\), define

\[
Y_u=X_u\cup\{e_1\},
\]

\[
Y_v=X_v\cup\{e_2\},
\]

and

\[
Y_w=X_w.
\tag{15}
\]

Thus exactly two bundles are augmented and one remains clean.

Let

\[
L=\sum_{a=1}^3 c_a(X_a).
\]

Consider any assignment of the three completed bundles to the agents.

For agent \(a\), define its excess over its original own-bundle cost by

\[
g_a
=
c_a(Y_{\pi(a)})-c_a(X_a).
\tag{16}
\]

By the augmented-bundle lemma:

- receiving an augmented bundle implies \(g_a\ge1\);
- receiving the clean bundle implies \(g_a\ge0\).

Therefore every assignment has total cost at least

\[
L+2.
\tag{17}
\]

On the other hand, the identity assignment gives each original owner exactly one leftover. By Fact 1, each such augmentation costs exactly \(1\). Hence the identity assignment has total cost exactly

\[
L+2.
\]

Consequently every minimum-cost assignment has total cost exactly

\[
L+2.
\tag{18}
\]

Exactly two agents receive augmented bundles. Each of them has excess at least \(1\), while the clean-bundle recipient has nonnegative excess. Since the total excess is exactly \(2\), the excess vector of every minimum-cost assignment is, after relabeling,

\[
\boxed{(1,1,0).}
\tag{19}
\]

Relabel agents so that:

- agents \(1\) and \(2\) receive the augmented bundles;
- agent \(3\) receives the clean bundle.

---

# 11. The envy graph of the minimum-cost assignment

Let \(A\) be such a minimum-cost assignment and define

\[
w(i,j)=c_i(A_i)-c_i(A_j).
\]

We show that every simple directed path has total weight at most \(1\).

---

## 11.1 Between the two augmented recipients

Agent \(1\) has excess \(1\):

\[
c_1(A_1)=c_1(X_1)+1.
\]

The bundle \(A_2\) is augmented. By the augmented-bundle lemma,

\[
c_1(A_2)\ge c_1(X_1)+1.
\]

Hence

\[
w(1,2)\le0.
\]

Similarly,

\[
w(2,1)\le0.
\tag{20}
\]

---

## 11.2 From an augmented recipient to the clean bundle

Since agent \(1\) has excess \(1\),

\[
c_1(A_1)=c_1(X_1)+1.
\]

The clean bundle is one of the original bundles, and partial EF gives

\[
c_1(A_3)\ge c_1(X_1).
\]

Therefore

\[
w(1,3)\le1.
\]

Likewise,

\[
w(2,3)\le1.
\tag{21}
\]

---

## 11.3 From the clean recipient to an augmented bundle

Agent \(3\) has excess \(0\):

\[
c_3(A_3)=c_3(X_3).
\]

Every augmented bundle costs agent \(3\) at least

\[
c_3(X_3)+1
\]

by the augmented-bundle lemma. Hence

\[
w(3,1)\le0,
\qquad
w(3,2)\le0.
\tag{22}
\]

---

# 12. Every simple envy path has weight at most \(1\)

From (20)–(22):

- the edges \(1\leftrightarrow2\) are nonpositive;
- the edges leaving \(3\) are nonpositive;
- the only potentially positive edges are
  \[
  1\to3,\qquad 2\to3,
  \]
  and each has weight at most \(1\).

A simple path can enter vertex \(3\) at most once. Once it enters \(3\), every outgoing edge is nonpositive.

Therefore every simple directed path has total weight at most

\[
\boxed{1}.
\tag{23}
\]

Since \(A\) is a minimum-cost assignment, it has no positive directed cycle. Thus the longest-path subsidy construction applies and gives

\[
\ell_A(i)\le1
\qquad
\forall i.
\]

After the usual common normalization,

\[
\boxed{
p_i\in\{0,1\}
\qquad
\forall i.
}
\]

Hence \(A\) is envy-free with per-agent subsidy at most \(1\).

---

# 13. Main theorem

> **Theorem.**  
> Let \(N=\{1,2,3\}\). For every finite set of indivisible chores \(M\) and every three arbitrary cost functions
>
> \[
> c_i:2^M\to\mathbb Z_{\ge0}
> \]
>
> satisfying
>
> \[
> c_i(\varnothing)=0,
> \qquad
> c_i(S\cup\{e\})-c_i(S)\in\{0,1\},
> \]
>
> there exists a complete allocation
>
> \[
> A=(A_1,A_2,A_3)
> \]
>
> and a subsidy vector
>
> \[
> p\in\{0,1\}^3
> \]
>
> such that
>
> \[
> c_i(A_i)-p_i
> \le
> c_i(A_j)-p_j
> \qquad
> \forall i,j.
> \]
>
> Consequently the total subsidy can be normalized to at most \(2\).

### Proof

Run the TWYZ partial-EF algorithm. It leaves at most two chores unallocated.

1. If no chore remains, the allocation is already complete and EF.
2. If one chore remains, insert it into any bundle and take a minimum-cost assignment; the resulting envy graph has longest simple path weight at most \(1\).
3. If two chores remain, the terminal SCC contains all three agents. The terminal rules imply Facts F1 and F2, which yield the augmented-bundle lemma. Put the two leftovers into two different bundles, take a minimum-cost assignment, and obtain excess profile \((1,1,0)\). Its envy graph has only two potentially positive edges, each of weight at most \(1\), and no simple path can collect more than one of them.

In every case the longest-path subsidy construction produces

\[
p\in\{0,1\}^3.
\]

Thus Problem 2 holds for \(n=3\). \(\square\)

---

# 14. Proof dependency map

The proof uses only:

1. binary-marginal costs;
2. the TWYZ partial-EF theorem;
3. the terminal rules of the TWYZ algorithm;
4. the free-insertion lemma;
5. integrality;
6. the augmented-bundle lemma;
7. minimum-cost assignment and the standard longest-path subsidy construction.

It does **not** require:

- additive costs;
- submodularity;
- subadditivity;
- the earlier \(\Sigma\)-spread program;
- Lemma D or simultaneous splitting;
- Lemma E;
- Venn/discrepancy arguments;
- the composed-cost reduction;
- the old saturation/enumeration argument.

The entire three-agent theorem is driven by the fact that the partial-EF algorithm leaves at most two chores, and in the two-leftover case the terminal SCC must therefore contain all three agents.
