# Lemma D — Two-Way Balance for Two Arbitrary Dichotomous Agents

## Status

**PROVED.**

Let U be a finite set and let c_1,c_2 be arbitrary dichotomous costs. Then there exists S⊆U such that

|c_1(S)-c_1(U\\S)|≤1 and |c_2(S)-c_2(U\\S)|≤1.

The proof below is self-contained. A previous project status file marked Lemma D as open because an earlier proof attempt had not yet been certified. The argument below was checked line-by-line; the key adjacent-transposition argument is valid. Exhaustive verification for all pairs of normalized dichotomous costs on |U|≤4 also found no counterexample.

## 1. Statement and discrepancy functions

For i∈{1,2}, define

 d_i(S)=c_i(S)-c_i(U\\S).

Then the desired conclusion is |d_i(S)|≤1 for both agents.

Complementation gives

 d_i(U\\S)=-d_i(S).  (1)

## 2. Edge increments

If x∉S,

 d_i(S∪{x})-d_i(S)
 = [c_i(S∪{x})-c_i(S)]
   +[c_i(U\\S)-c_i(U\\(S∪{x}))].

Each bracketed term lies in {0,1}. Hence

 d_i(S∪{x})-d_i(S)∈{0,1,2}.  (2)

Thus d_i is nondecreasing along every inclusion chain and every edge changes it by at most 2.

## 3. Every maximal chain balances each individual agent

Fix an ordering σ=(x_1,…,x_m) and prefixes S_t={x_1,…,x_t}.

For each i,

 d_i(S_0)=-c_i(U)≤0,
 d_i(S_m)=c_i(U)≥0.

Because d_i is nondecreasing and each step is at most 2, it cannot jump directly from a value ≤−2 to a value ≥2. Hence some prefix satisfies

 d_i(S_t)∈{-1,0,1}.

So each agent has at least one balanced prefix on every ordering.

## 4. Balanced intervals

For each i define

 L_i=min{t:d_i(S_t)≥−1},
 R_i=max{t:d_i(S_t)≤1}.

Monotonicity gives

 |d_i(S_t)|≤1  iff  L_i≤t≤R_i.  (3)

Hence the balanced prefixes for agent i form a nonempty interval I_i=[L_i,R_i].

If I_1∩I_2 is nonempty, the corresponding prefix proves the lemma.

Assume for contradiction that no common balanced subset exists. Then, for every ordering,

 I_1∩I_2=∅.  (4)

Exactly one interval lies strictly before the other. Call agent 1 the winner when R_1<L_2, and agent 2 the winner when R_2<L_1.

## 5. Adjacent transpositions preserve the winner

Consider orderings

 σ=(…,x,y,…),
 σ'=(…,y,x,…).

Let S be their common prefix immediately before x,y, and put

 A=S∪{x},  B=S∪{y},  T=S∪{x,y}.

The chains coincide except at A versus B.

Suppose the winner changes; relabel agents so σ is won by 1 and σ' by 2.

The common vertices S and T cannot be balanced for either agent, because then the corresponding agent would win on both chains. Therefore

 d_1(S)≤−2,   d_2(S)≤−2.  (5)

Since 1 wins σ, A is balanced for 1 but not for 2:

 |d_1(A)|≤1,   d_2(A)≤−2.  (6)

Since 2 wins σ', B is balanced for 2 but not for 1:

 |d_2(B)|≤1,   d_1(B)≤−2.  (7)

Now compare the common successor T with A. By (2),

 d_2(T)−d_2(A)≤2,

so d_2(T)≤0. By monotonicity,

 d_2(T)≥d_2(B)≥−1.

Thus |d_2(T)|≤1.  (8)

Symmetrically, comparing T with B gives

 d_1(T)≤0,
 d_1(T)≥d_1(A)≥−1,

hence |d_1(T)|≤1.  (9)

Therefore T is balanced for both agents, contradicting (4). Hence adjacent transpositions cannot change the winner.

## 6. Reversal flips the winner

Let σ=(x_1,…,x_m) and σ^rev=(x_m,…,x_1). The reversed prefix satisfies

 S_t^rev=U\\S_{m−t}.

By (1),

 d_i(S_t^rev)=−d_i(S_{m−t}).

Thus the balanced interval transforms as

 I_i^rev=[m−R_i,m−L_i].  (10)

If σ is won by agent 1, R_1<L_2, so

 m−R_2 < m−L_2 < m−R_1 ≤ m−L_1.

Thus I_2^rev lies strictly before I_1^rev, so σ^rev is won by agent 2. Similarly, if σ is won by 2, the reverse is won by 1.

Therefore reversal always flips the winner.  (11)

## 7. Final contradiction

Every permutation can be transformed into its reverse by adjacent transpositions. Section 5 says the winner is invariant under every adjacent transposition, so σ and σ^rev must have the same winner.

Section 6 says σ^rev has the opposite winner.

Contradiction.

Therefore the assumption (4) was false. Some ordering has I_1∩I_2≠∅, and its corresponding prefix S satisfies

 |c_1(S)-c_1(U\\S)|≤1,
 |c_2(S)-c_2(U\\S)|≤1.

Hence Lemma D is proved. □

## 8. What the proof uses

Only the following properties are needed:

1. complement antisymmetry of d_i;
2. monotonicity of d_i along inclusion chains;
3. edge increments in {0,1,2}.

No additivity, submodularity, matroid structure, or representation c(S)=f(|S∩D|) is used.

## 9. Independent finite verification

Exhaustive enumeration of normalized dichotomous costs gives:

| |U| | # costs | unordered pairs checked | counterexamples |
|---:|---:|---:|---:|---:|
| 1 | 2 | 3 | 0 |
| 2 | 6 | 21 | 0 |
| 3 | 38 | 741 | 0 |
| 4 | 990 | 490,545 | 0 |

These checks are only sanity verification; the proof above is general.

## 10. Consequence for the project

Lemma D is now available as a proved two-agent theorem. It does not by itself close the remaining three-agent Lemma E, which still asks for a 3-partition with total spread at most 3 for three arbitrary dichotomous costs.
