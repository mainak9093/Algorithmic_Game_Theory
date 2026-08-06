# The Balance Rule — conjecture, machinery, and what remains

*Approach 3 of the dichotomous-chores subsidy project. Status as of 2026-08-08.*

This document is self-contained: it states the target, defines the peel frame,
gives every proved lemma with its proof, and delimits exactly what is left. It is
the working reference for the balance-rule line of attack.

---

## 1. The target

**Conjecture 2 (the project's goal).** For every instance with negative
dichotomous valuations there is an envy-free solution $(A, p)$ with
$p \in \{0,1\}^n$, hence total subsidy at most $n-1$, computable in polynomial
time.

By `prop:zero-coordinate` the total-subsidy clause is free, so Conjecture 2 is the
single statement

$$\exists A : \quad \max_{i} \ell_A(i) \le 1 .$$

**The reduction chain.** Both arrows are *proved*:

$$\text{Conjecture 2} \;\Longleftarrow\; \texttt{h1prime} \;\Longleftarrow\; \texttt{balance-rule}$$

So exactly one statement is open.

---

## 2. The peel frame

Derived from the replica transform (`thm:replica`) and `cor:coverage`, which
reduce Conjecture 2 to: *the replica instance admits an allocation in which no
agent holds two copies of one type.*

**State.** A *workload profile* $W = (W_1,\dots,W_n)$ with $W_i \subseteq M$,
such that the *owner-candidate set*

$$S_j := \{\, i : j \in W_i \,\}$$

is non-empty for every chore $j$. Read $W_i$ as "agent $i$ is still on the hook
for $W_i$".

**Moves.**

| move | definition | legality |
|---|---|---|
| root | $W_i = M$ for all $i$ | — |
| $\mathrm{peel}(x,j)$ | $W_x \leftarrow W_x \setminus \{j\}$ | requires $j \in W_x$ and $\lvert S_j\rvert \ge 2$ |
| permutation | relabel $W$ by any $\sigma$ | — |
| terminal | $\lvert S_j \rvert = 1$ for all $j$ | induced allocation $A_i = \{j : S_j = \{i\}\}$ |

**Envy graph.** $w_W(i,k) := c_i(W_i) - c_i(W_k)$. The root graph is identically
zero.

**Legal state.** No positive-weight cycle, and $\ell_W(i) \le 1$ for all $i$.

A peel state is exactly a duplicate-free partial allocation of the replica, a peel
is exactly one insertion, a permutation is a bundle reassignment, and terminal
states are exactly the coverage allocations. Nothing is lost in the translation.

**Lemma (peel dynamics) — `lem:peel`.** Write
$\mu_k := c_k(W_x) - c_k(W_x \setminus \{j\}) \in \{0,1\}$. Then
$\mathrm{peel}(x,j)$ changes only the arcs incident to $x$:

$$\Delta w(k,x) = +\mu_k \in \{0,1\}, \qquad \Delta w(x,k) = -\mu_x \in \{-1,0\}.$$

*Peeling raises the arcs into $x$ and lowers the arcs out of it.*

---

## 3. The conjectures

**`h1prime` (Reachability).** From the root, some sequence of peels and
permutations reaches a terminal state with the invariant holding at every
intermediate state.

> Implies Conjecture 2: the root graph is zero (so legal); a terminal's graph is
> the induced allocation's envy graph; legality there gives $\ell_A \le 1$, and
> `obs:integrality` upgrades this to $p \in \{0,1\}^n$.

**`balance-rule`.** Say $W$ *admits a balanced terminal* if some choice of owner
$f(j) \in S_j$ induces bundle sizes differing by at most 1. Then:

> Restricting the state graph to states that are both **legal** and
> **balance-admitting**, a terminal is reachable from the root.

**Proposition — `prop:balance-rule-implies`.** `balance-rule` $\Rightarrow$
`h1prime` $\Rightarrow$ Conjecture 2, and yields a polynomial algorithm, each step
choosing a peel by one max-flow feasibility test.

*Balance-admissibility is a transportation feasibility question: with $m = qn+r$,
assign each chore to an agent of $S_j$ with $r$ agents at $q{+}1$ and $n-r$ at
$q$. One max-flow.*

---

## 4. The machinery (all proved)

### 4.1 Potentials

**Lemma — `lem:potential-form`.** $W$ is legal **iff** there is
$p \in \{0,1\}^n$ with $w(i,k) \le p_i - p_k$ for all $i \ne k$.

> *Proof.* ($\Leftarrow$) Summing along a path telescopes to
> $w(P) \le p_{i_0} - p_{i_r} \le 1$, and around a cycle to $\le 0$.
> ($\Rightarrow$) Take $p = \ell$, which lies in $\{0,1\}^n$ by legality and
> integrality; $\ell(i) \ge w(i,k) + \ell(k)$ is the inequality. $\square$

Identify $p$ with the **paid set** $S = \{i : p_i = 1\}$ and put

$$\lambda_S(i,k) := \begin{cases} 0 & i,k \text{ same side of } S \\ +1 & i \in S,\ k \notin S \\ -1 & i \notin S,\ k \in S \end{cases} \qquad \mathcal P(W) := \{\, S : w(i,k) \le \lambda_S(i,k)\ \forall i\ne k \,\}$$

So **$W$ is legal iff $\mathcal P(W) \ne \emptyset$**. This is the two-tier data
of `prop:twotier` carried along the peel process.

**Observation — `obs:paidsets-root`.** At the root every arc is $0$, so the $-1$
constraint fails for every pair with $i \notin S, k \in S$. Hence

$$\mathcal P(\text{root}) = \{\emptyset,\ N\}$$

— only the two constant potentials. *(Verified on 169 instances.)*

### 4.2 When is a peel legal?

**Proposition (peel criterion) — `prop:inarcs-only`.** For any $S \subseteq N$,
$S \in \mathcal P(W')$ **iff**

$$\text{(i) } w(i,k) \le \lambda_S(i,k)\ (i,k \ne x); \quad \text{(ii) } w(i,x) + \mu_i \le \lambda_S(i,x); \quad \text{(iii) } w(x,k) - \mu_x \le \lambda_S(x,k).$$

**If moreover $S \in \mathcal P(W)$, then (i) and (iii) are automatic and only the
in-arc condition (ii) remains** — the out-arcs drop by $\mu_x$, so a bound that
held still holds.

> ⚠ **Earlier this was stated with (iii) omitted for arbitrary $S$. That is
> false.** (iii) is automatic only for $S$ already admissible at $W$, and the
> whole point of $\mathcal P$ is that new sets appear. Corrected form checked on
> 21,451,744 instances of the criterion, 0 violations.

**Lemma (new paid sets require a costly chore) — `lem:new-paidsets`.** If
$\mu_x = 0$ then $\mathcal P(W') \subseteq \mathcal P(W)$. If $\mu_x = 1$, every
$S \in \mathcal P(W')\setminus\mathcal P(W)$ violates at $W$ exactly one kind of
constraint — an out-arc of $x$, by exactly one unit.

> *Proof.* By (ii), $w(i,x) \le \lambda_S(i,x) - \mu_i \le \lambda_S(i,x)$, so the
> in-arcs already held at $W$; by (i) so did the arcs off $x$. The only
> constraint left is an out-arc of $x$, and (iii) bounds its violation by
> $\mu_x$. $\square$
>
> *(Verified: 418,662 peels where a new paid set appears, $\mu_x = 1$ in all.)*

**Proposition — `prop:tight-arc`.** Specialising to $S = \{i : \ell(i) = 1\}$:
call an arc $(k,x)$ *tight* if $w(k,x) = p_k - p_x$. Then $p$ certifies
$\mathrm{peel}(x,j)$ **iff** $\mu_k = 0$ for every $k \ne x$ with $(k,x)$ tight.

> *Proof.* Slack $p_k - p_x - w(k,x)$ is a non-negative integer and
> $\mu_k \in \{0,1\}$, so the constraint holds exactly when $\mu_k = 0$ or the
> slack is $\ge 1$. $\square$

### 4.2b Structure: $\mathcal P(W)$ is a lattice

**Theorem — `thm:paidsets-lattice`.** $\mathcal P(W)$ is closed under union and
intersection. When non-empty it therefore has a unique maximum $S_{\max}$ and a
unique minimum $S_{\min}$.

> *Proof.* Let $p,q \in \mathcal P(W)$, $r = \max(p,q)$. If $r$ agrees with $p$ at
> both $i,k$ (or with $q$ at both) the constraint is a hypothesis. Otherwise say
> $r_i = p_i \ge q_i$ and $r_k = q_k \ge p_k$; then
> $w(i,k) \le q_i - q_k \le p_i - q_k = r_i - r_k$, using the $q$-constraint and
> $q_i \le p_i$. The mixed case for $\min$ is symmetric. $\square$

**Corollary — `cor:smin-is-ell`.** $S_{\min} = \{i : \ell(i) = 1\}$: the
longest-path potential is the **smallest** admissible paid set.

**Corollary (canonical potential) — `cor:smax-canonical`.** Some admissible paid
set contains $x$ **iff** $x \in S_{\max}$. So `lem:paid-peel` fires exactly when
$\mu_x = 1$ and $x \in S_{\max}$, and `lem:slack-transfer` need only be run at
$S = S_{\max}$.

> *(Verified: 140,785 legal states, 492,100 pairs; closure and both corollaries,
> 0 violations.)*

**This explains the earlier error.** Evaluating `lem:paid-peel` at $p = \ell$ is
evaluating it at $S_{\min}$ — the admissible set with the *fewest* paid agents,
the worst possible choice for a lemma whose hypothesis is $x \in S$. The right
representative is $S_{\max}$, and it is the only one that ever needs computing:
the existential over $2^n$ sets collapses to one membership test.

**Corollary ($\mu_x = 0$ is exact) — `cor:mu-zero-exact`.** If $\mu_x = 0$ then
$\mathcal P(W') \subseteq \mathcal P(W)$ by `lem:new-paidsets`, and (i),(iii) are
automatic, so

> peel$(x,j)$ is legal **iff** some $S \in \mathcal P(W)$ satisfies
> $w(i,x) + \mu_i \le \lambda_S(i,x)$ for all $i \ne x$.

*(Verified: 697,572 peels with $\mu_x = 0$, 0 mismatches.)* **All remaining
difficulty is the $\mu_x = 1$ case** — exactly where new paid sets can appear.

### 4.3 Two sufficient conditions

**Lemma (free peels are safe) — `lem:free-peel-safe`.** Call $\mathrm{peel}(x,j)$
*free* if $\mu_k = 0$ for every $k \ne x$. A free peel applied to a legal state
yields a legal state.

> *Proof.* By `lem:peel` every arc weakly decreases: $\Delta w(k,x) = 0$ and
> $\Delta w(x,k) = -\mu_x \le 0$. No positive cycle appears and no path weight
> rises. $\square$

**Lemma (paid-agent peel) — `lem:paid-peel`.** Let $S \in \mathcal P(W)$. If
$x \in S$ and $\mu_x = 1$, then $\mathrm{peel}(x,j)$ is legal — **whatever the
other marginals are**.

> *Proof.* Take $S' := S \setminus \{x\}$. Constraints off $x$ are unchanged.
> Into $x$: $\lambda$ rises by exactly 1 (from $0$ to $+1$ for $i \in S$, from
> $-1$ to $0$ for $i \notin S$), and $\mu_i \le 1$, so
> $w(i,x) + \mu_i \le \lambda_S(i,x) + 1 = \lambda_{S'}(i,x)$. Out of $x$:
> $\lambda$ drops by exactly 1, and $w(x,k) - \mu_x \le \lambda_S(x,k) - 1
> = \lambda_{S'}(x,k)$ using $\mu_x = 1$. $\square$

> ⚠ **$S$ is any admissible paid set, not necessarily $\ell$.** Testing with
> $S = \{i : \ell(i)=1\}$ alone badly understates the lemma — at the root
> $\ell \equiv 0$ and it appears never to fire, yet $N \in \mathcal P(\text{root})$
> makes every agent paid.

The two conditions are **complementary**: a free peel constrains the *other*
agents' marginals and says nothing about $x$; `lem:paid-peel` constrains only $x$
and leaves the others free.

**Lemma (balance-preservation is free) — `lem:balance-free`.** If $W$ admits a
balanced terminal $f$, then for every chore $j$ with $\lvert S_j\rvert \ge 2$ and
every $i \in S_j \setminus \{f(j)\}$, $\mathrm{peel}(i,j)$ still admits $f$.

> *Proof.* Peeling removes $i$ from $S_j$ only; $f(j) \ne i$ remains in $S_j$, so
> $f$ is still a legal choice function and the induced sizes are unchanged.
> $\square$

**So the balance half of the rule costs nothing — the entire content is
legality.**

**Lemma (slack-transfer peel) — `lem:slack-transfer`.** Let
$S \in \mathcal P(W)$ with $x \notin S$, and let

$$T := \{\, i \ne x : w(i,x) = \lambda_S(i,x) \text{ and } \mu_i = 1 \,\}$$

be the agents whose in-arc blocks the peel. If

1. $w(k,i) \le \lambda_S(k,i) - 1$ for every $i \in T$, $k \notin T\cup\{i\}$, and
2. $w(x,k) - \mu_x \le -1$ for every $k \in T$,

then $S \cup T$ certifies $\mathrm{peel}(x,j)$.

> *Proof.* Moving $i$ from outside $S$ to inside raises $\lambda(i,\cdot)$ by one
> and lowers $\lambda(\cdot,i)$ by one; pairs within $T$ and pairs avoiding $T$
> are unchanged. (1) supplies the slack for the lowered constraints, giving (i).
> For (ii): $i \in T$ has $\lambda$ raised by 1, absorbing $\mu_i = 1$; $i \notin
> T$ is either untight or has $\mu_i = 0$. For (iii): out-arcs into $T$ need
> $\lambda_{S'}(x,k) = -1$, which is (2). $\square$
>
> *(Verified: 46,723 certified peels, 0 illegal.)*

**Idea:** adding an agent to the paid set *buys* $+1$ of slack on its outgoing
arcs — in particular on its in-arc to $x$ — at the price of $-1$ on its incoming
arcs. Slack transfer pays that price where there is slack to spare.

### 4.4 The root, exactly

**Proposition — `prop:first-peel`.** From the root, $\mathrm{peel}(x,j)$ is legal
**iff** $\mu_x \ge \mu_k$ for every $k \ne x$: the chore must be taken from an
agent who finds it at least as costly as everybody else.

> *Proof.* After the peel, $w(k,x) = \mu_k$, $w(x,k) = -\mu_x$, and $0$ elsewhere.
> A potential must be constant $= c$ off $x$; the rest gives
> $c - \mu_x \le p'_x \le c - \max_k \mu_k$, which contains an integer iff
> $\mu_x \ge \max_k \mu_k$ (take $c=1$, $p'_x = 1 - \max_k\mu_k$). $\square$

*Consistency: if $\mu_x = 1$ then $\mu_x \ge \max_k \mu_k$ automatically, so
`lem:paid-peel` with $S = N$ recovers this; if all $\mu_k = 0$ the peel is free.*

**Corollary (structure of a stuck state) — `cor:stuck-structure`.** If $W$ is
stuck then for every peelable chore $j$ and admissible $x \in S_j$, either
$\ell(x) = 0$ or $\mu_x = 0$. *(Contrapositive of `lem:paid-peel` with
$S = \{i:\ell(i)=1\}$.)*

### 4.5 Dynamics of $S_{\max}$

Write $F(W) := S_{\max}(W)$.

**Proposition — `prop:smax-monotone-mu0`.** If $\mu_x = 0$ then
$F(W') \subseteq F(W)$.

> *Proof.* `lem:new-paidsets` gives $\mathcal P(W')\subseteq\mathcal P(W)$, and
> the maximum of a subfamily is contained in the maximum of the family. $\square$

**Proposition (what $S_{\max}$ is) — `prop:smax-closed-form`.** Let $\ell^*(k)$ be
the heaviest weight of a path **ending** at $k$ (empty path $=0$). Then

$$S_{\max}(W) = \{\, k : \ell^*(k) \le 0 \,\}$$

> *Proof.* $w(i,k) \le p_i - p_k$ reads $p_k \le p_i - w(i,k)$; iterating along a
> path ending at $k$ gives $p_k \le 1 - \ell^*(k)$, so $\ell^*(k)\ge1$ forces
> $p_k=0$. Conversely $p_k := [\ell^*(k)\le 0]$ is admissible. $\square$

Compare `cor:smin-is-ell`: **$S_{\min}$ is read off paths *leaving* an agent,
$S_{\max}$ off paths *entering* it.** That duality is what makes $\mu_x=1$
tractable.

**Lemma (monotonicity off the peeled agent) — `lem:smax-mono-mu1`.** If
$\mu_x = 1$ then $S_{\max}(W)\setminus\{x\} \subseteq S_{\max}(W')$.

> *Proof.* Fix $k \ne x$ with $\ell^*(k)\le0$ and let $P$ end at $k$ in $W'$. If
> $P$ avoids $x$, unchanged. If $P$ crosses $x$ it uses one arc in (risen by
> $\mu_i \le 1$) and one out (fallen by $\mu_x = 1$), net $\le 0$. If $P$ starts
> at $x$ it uses only a lowered arc. $\square$
>
> *(Verified: closed form on 93,819 states, monotonicity on 264,139 peels with
> $\mu_x=1$; 0 violations each.)*

With `prop:smax-monotone-mu0` this accounts for all observed behaviour but one
case: $\mu_x=1$ with $x$ *leaving* $S_{\max}$, where $S_{\max}(W')$ contains
$S_{\max}(W)\setminus\{x\}$ and could in principle also acquire a new element —
making the two incomparable. **That never happens**, and proving it doesn't is
what would close comparability.

**Theorem ($F$ never moves sideways) — `obs:smax-comparable`.** If $W$ and
$W' = \mathrm{peel}(x,j)$ are both legal, then $S_{\max}(W)$ and $S_{\max}(W')$
are **comparable** under inclusion. In the case $\mu_x = 1$ with
$x \in S_{\max}(W)$, $x \notin S_{\max}(W')$ one has
$S_{\max}(W') = S_{\max}(W)\setminus\{x\}$ exactly.

> *Proof.* $\mu_x = 0$ is `prop:smax-monotone-mu0`. For $\mu_x = 1$,
> `lem:smax-mono-mu1` gives $S_{\max}(W)\setminus\{x\}\subseteq S_{\max}(W')$;
> if $x \in S_{\max}(W')$ or $x \notin S_{\max}(W)$ that already reads
> $S_{\max}(W)\subseteq S_{\max}(W')$. In the remaining case suppose
> $k \notin S_{\max}(W)$ but $k \in S_{\max}(W')$, $k \ne x$. Take a simple $Q$
> ending at $k$ with $w_W(Q)\ge1$; then $w_{W'}(Q)\le0$, and $Q$ must meet $x$
> (once, being simple). Splitting $Q = Q_1\cdot Q_2$ at $x$,
> $w_{W'}(Q) = w_W(Q)+\mu_{i'}-\mu_x$ forces $\mu_{i'}=0$, $w_W(Q)=1$. As
> $x \in S_{\max}(W)$, $w_W(Q_1)\le0$, so $w_W(Q_2)\ge1$ and $w_{W'}(Q_2)\ge0$.
> As $x \notin S_{\max}(W')$ take $P$ ending at $x$ with $w_{W'}(P)\ge1$; then
> $P\cdot Q_2$ is a walk ending at $k$ of weight $\ge1$, and $W'$ having no
> positive cycle a heaviest walk may be taken simple — contradicting
> $k \in S_{\max}(W')$. $\square$
>
> *(Verified: 755,051 peels, 0 violations of the conclusion or of any step of
> the case split; the critical case arose 212,930 times, so it is not vacuous.)*

**Two cautions.** The jump is not bounded by one — symmetric difference reached
4, and $F(W')\subseteq F(W)\cup\{x\}$ held only 87.9% — so peels are **not**
single lattice flips.

Since the shrinking half is proved, **every growth event has $\mu_x = 1$**,
consistent with `lem:new-paidsets`.

> ⚠ **$F$ is *not* a monovariant** — it grows on roughly one peel in eight, so it
> gives no monotone progress. Termination was never the issue anyway: each peel
> deletes an element, so $\sum_i|W_i|$ already decreases. The problem is
> legality.

**Refuted — the canonical-support conjecture.** *"Every reachable legal
balance-admitting state admits a balanced terminal $f$ with $f(j) \in S_{\max}$
whenever $S_j \cap S_{\max} \ne \emptyset$."* **False**, and not marginally: over
117,141 balance-admitting states it fails on **59,623** (51%). The mixed case is
common enough for the statement to have content ($|S_j \cap S_{\max}| = 0$ on
only 14,082 chores), so this is not a vacuity. A bridge between balanced
terminals and admissible potentials, if one exists, does not take this form.

---

## 5. Evidence

| claim | scope | result |
|---|---|---|
| `h1prime`: no bad root | **complete exhaustive $n=m=3$ family, 9,880 instances** | 0 bad roots |
| `h1prime`: no bad root | $n=3\ (m\le6)$, $n=4\ (m\le4)$, $n=5\ (m=3)$ | 0 bad roots |
| balance $\Rightarrow$ live | 1,192,108 reachable legal states | 0 counterexamples |
| `balance-rule` | 305 instances | 0 failures |
| `lem:free-peel-safe` | 674,062 free peels | 0 illegal |
| `lem:paid-peel` | 693,276 paid-agent peels | 0 illegal |
| both lemmas, $S$ free | 1,558,435 certified peels | 0 illegal |
| `prop:inarcs-only` corrected form | 21,451,744 checks | 0 violations |
| `lem:new-paidsets` | 418,662 peels creating a new set | 0 with $\mu_x 
e 1$ |
| `lem:slack-transfer` | 46,723 certified peels | 0 illegal |

**Coverage by the three sufficient conditions** (each with $S$ ranging over all of
$\mathcal P(W)$), over 174,630 reachable non-terminal states:

| conditions | states covered |
|---|---|
| free + paid-agent | 165,613 (94.8%) |
| \+ slack-transfer | **166,480 (95.3%)** |
| residual | 8,150 (4.7%) |

---

## 6. What is refuted (do not retry)

| claim | why it died |
|---|---|
| pointwise balance-rule ("from *every* such state") | 5 states admit no legal balance-preserving move; smallest $n{=}3,m{=}4$, $W = (\{g_1g_2\},\{g_3g_4\},\{g_3g_4\})$ |
| greedy-safety (no backtracking) | 37 reachable states are progress-stuck |
| mechanism "balance $\Rightarrow$ legal *balanced* terminal" | fails on 21.8% of 349,188 states; live states often reach an **unbalanced** legal terminal |
| dominant-marginal peel as a lemma | 272,757 of 2,912,968 illegal (9.4%) |
| dominant-marginal as a rule | terminates on 10/191 |
| the three naive greedy rules | argmax-$\ell$ / biggest $S_j$ / most-burdened: 81, 64, 66 failures |
| $\lvert\mathcal P\rvert$-driven greedy as *explanation* | max- and min-$\lvert\mathcal P\rvert$ both terminate on 169/169 — no discriminating power |

**Death is over-commitment.** Every dead state has $\min_j \lvert S_j\rvert = 1$;
no state with $\min_j \lvert S_j \rvert \ge 2$ was ever dead. Typical witness:
$W = (\{g_2\},\{g_2\},\{g_1,g_3,g_4\})$ with own costs $(0,0,2)$ — three chores
already committed to agent 3, forcing $\ell \ge 2$ at every terminal below, and
that same over-commitment is what makes a balanced terminal impossible.

---

## 7. What remains to prove

**One statement.** `balance-rule` cannot be proved pointwise (5 counterexamples),
so it needs an **invariant** $\Phi$ on states with

1. **Initialisation** — $\Phi(\text{root})$;
2. **Progress** — $\Phi(W)$ and $W$ non-terminal $\Rightarrow$ some legal
   balance-preserving peel gives $W'$ with $\Phi(W')$;
3. **Soundness** — $\Phi(W) \Rightarrow W$ legal.

(3) is free if $\Phi$ includes legality; (1) is easy; **(2) is the whole
content.** By `prop:inarcs-only`, proving (2) means exhibiting $j$, $x \in S_j$
and $S$ with

$$w(i,x) + \mu_i \le \lambda_S(i,x) \quad \forall i \ne x$$

plus the non-$x$ constraints — *one row of the envy matrix, not the whole graph.*

**Constraints $\Phi$ must satisfy**, from the refutations:

- not "legal ∧ balance-admitting" — the 37 stuck states satisfy it;
- strictly stronger than the three safety lemmas — restricting to steps the
  first two certify (with $S$ free) reaches a terminal on only **48 of 191**
  instances, and the residual they leave is 4.7% of states;
- it must produce a maximal-marginal first peel, since `prop:first-peel` proves
  that is the only legal option at the root.

**Not required.** "balance $\Rightarrow$ live" (verified on 1.19M states) is
motivational, not load-bearing: the chain never invokes it.

**Caveat.** `balance-rule` and `h1prime` are both *strictly stronger* than
Conjecture 2 (`rem:converse`): a good allocation may exist while no legal
schedule reaches one. This route therefore proves more than needed — which buys
the polynomial algorithm, but means failure here would not refute Conjecture 2.

---

## 8. The next milestone

**Certify one complete schedule** — even at $n=m=3$. That is the smallest thing
that would show the lemma set can close, and it currently fails: the two lemmas
carry a full schedule on 48 of 191 instances, so a third safety criterion is
needed. `prop:inarcs-only` says where to look — the in-arcs at the peeled agent,
and specifically at sets $S' \notin \mathcal P(W)$, since
$\mathcal P(W') \not\subseteq \mathcal P(W)$ and new paid sets appear precisely
when an out-arc drops by $\mu_x$.

---

## 9. Scripts

| file | what it establishes |
|---|---|
| `update_32/peel_sweep.py` | the exhaustive $n=m=3$ sweep, 0 bad roots |
| `update_32/peel_general.py` | larger sizes; the three naive rules fail |
| `update_32/deadend_char.py` | balance $\Rightarrow$ live, 1.19M states |
| `update_32/balance_rule.py` | the rule reaches a terminal, 305 instances |
| `update_33/why_balance_works.py` | refutes the "legal balanced terminal" mechanism |
| `update_34/reachable_stuck.py` | the stuck-state count (note: its stuck test is too lenient — permutations make no progress) |
| `update_35/stuck_profile.py` | the stuck-state characterisation |
| `update_36/potential_set.py` | $\mathcal P(W)$, and $\mathcal P(\text{root}) = \{\emptyset,N\}$ |
