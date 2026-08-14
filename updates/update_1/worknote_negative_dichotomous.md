# Working note — negative dichotomous valuations (the chore analogue of R3)

**Status:** v1. Two theorems proved, one conjecture with exhaustive + randomized support,
one *negative* structural result that kills the obvious proof strategy.
Notation follows `glossary_fair_division_subsidies.md` (§0): allocation $A$, items $M$,
subsidy $p$, envy graph $G_A$ with $w_A(i,j) = v_i(A_j) - v_i(A_i)$.

---

## 0. Setting

Agents $[n]$, indivisible **chores** $M$, $|M| = m$. Each $v_i : 2^M \to \mathbb{Z}_{\le 0}$
is **negative dichotomous**:
$$v_i(\emptyset) = 0, \qquad v_i(S \cup \{g\}) - v_i(S) \in \{0, -1\}\ \ \forall S,\ g \notin S .$$
No additivity, submodularity or subadditivity assumed — exactly R3's level of generality,
sign-flipped.

**Cost form.** Put $c_i := -v_i$. Then $c_i$ is monotone non-decreasing, $c_i(\emptyset)=0$,
marginals in $\{0,1\}$ — i.e. **$c_i$ is literally an R3-dichotomous function, used as a
cost rather than a value.** Every statement below is in cost form.

$$w_A(i,j) \;=\; v_i(A_j) - v_i(A_i) \;=\; c_i(A_i) - c_i(A_j).$$

**What transfers for free.** The Halpern–Shah characterisation ([R1], [R2 Thm 2.1]) is
sign-agnostic — it never uses monotonicity or the sign of $v$. So verbatim:

> $A$ envy-freeable $\iff$ $A$ **minimises $\sum_i c_i(A_i)$ over all reassignments of its
> own bundles** $\iff$ $G_A$ has no positive-weight cycle; and then the minimum subsidy is
> $p^*_i = \ell_A(i)$, the max weight of a path leaving $i$.

So the target statement is purely graph-theoretic:

> **Target.** There is an allocation $A$ with no positive cycle in $G_A$ and
> $\ell_A(i) \le 1$ for every $i$ (integrality then forces $p \in \{0,1\}^n$).

**Lower bound (tight, same as R3).** $m = n-1$ chores, each costing $1$ to everyone,
additive. Any allocation leaves some agent empty, so $\ell_A(i) = |A_i|$; keeping every
$\ell_A(i) \le 1$ forces $|A_i| \le 1$ and hence total subsidy exactly $n-1$.

---

## 1. The sign flip, precisely (mirror of R3 Prop. 5–6)

Let $Z^x := (A_1,\dots,A_x \cup \{g\},\dots,A_n)$, and write marginals in **value** terms:
$\mu_x := v_x(A_x\cup g) - v_x(A_x)$ and $\mu_{i,x} := v_i(A_x \cup g) - v_i(A_x)$.
For *any* valuations:

| arc | new weight |
|---|---|
| $(i,j)$, $i,j \ne x$ | unchanged |
| $(x,j)$ — **out of** $x$ | $w_A(x,j) - \mu_x$ |
| $(i,x)$ — **into** $x$ | $w_A(i,x) + \mu_{i,x}$ |

Goods have $\mu \in \{0,1\}$; chores have $\mu \in \{-1,0\}$. Hence:

* **Goods (R3).** Give $g$ to an agent with $\mu_x = 1$: her out-arcs *drop*, only her
  *in*-arcs grow. Neutralised by requiring $x \in M(p)$ (most subsidised), since then every
  path into $x$ has weight $\le p_u - p_x \le 0$. Such an $x$ always exists — that is why
  R3's easy case is easy.
* **Chores.** Give $g$ to an agent with $\mu_x = 0$ (zero marginal *cost*): her out-arcs are
  *unchanged*, her in-arcs *drop*. If $\mu_x = -1$ her **out**-arcs grow by exactly 1, so
  the necessary condition is $p_x = 0$ (**least** subsidised) — the exact mirror.

This one table is the whole difference between the two problems, and §5 shows it is not a
cosmetic difference.

---

## 2. Theorem A (free insertion) — strictly simpler than R3's Lemma 7

> **Theorem A.** Let $A$ be envy-freeable and $g \notin \bigcup_i A_i$. If
> $c_x(A_x \cup \{g\}) = c_x(A_x)$ for some agent $x$, then $Z^x$ is envy-freeable and
> $\ell_{Z^x}(i) \le \ell_A(i)$ for every $i$.

*Proof.* Arcs $(i,j)$ with $i,j \ne x$ are unchanged. Arcs out of $x$:
$w_{Z^x}(x,j) = c_x(A_x\cup g) - c_x(A_j) = c_x(A_x) - c_x(A_j) = w_A(x,j)$.
Arcs into $x$: $w_{Z^x}(i,x) = c_i(A_i) - c_i(A_x \cup g) \le c_i(A_i) - c_i(A_x) = w_A(i,x)$
by monotonicity. So **every arc weakly decreases**; no positive cycle can appear and no path
weight can rise. $\square$

Note what is *absent*: no "most subsidised agent" hypothesis, no permutation, no
extendability machinery. R3 needs all of that for its easy case; the chore version needs
none. **Consequently the only hard case is a chore whose marginal cost is $1$ for every
agent on her own current bundle.**

---

## 3. Theorem B (cycle-closing bound) and its corollary

> **Theorem B.** For any envy-freeable $A$ and any $u$,
> $$\ell_A(u) \;\le\; \max\Big(0,\ \max_{v \ne u}\big[c_v(A_u) - c_v(A_v)\big]\Big).$$

*Proof.* A nonempty path $P$ from $u$ to $v$ closes into a cycle with the arc $(v,u)$, whose
weight is $\le 0$; hence $w_A(P) \le -w_A(v,u) = c_v(A_u) - c_v(A_v)$. $\square$

> **Corollary B1.** If $c_v(A_u) \le c_v(A_v) + 1$ for all $u,v$ — *no agent would suffer
> more than one extra unit by taking anybody else's bundle* — then $p \in \{0,1\}^n$.

This is the chore form of the trick R2 uses in its §4 ("a lower bound of $-1$ on each arc
weight suffices"). It is sufficient, far from necessary (an agent with $c_i \equiv 0$ can
absorb everything and the hypothesis fails while the subsidy is $0$), but it is the cheapest
handle available and it does all the work in Theorem C.

---

## 4. Two proved cases

### 4.1 Theorem C — binary additive chores, tight, polynomial time

Let $c_i(S) = |S \cap D_i|$, where $D_i \subseteq M$ is the set of chores agent $i$ dislikes.
Call $g$ **universally bad** if $g \in D_i$ for every $i$; let $U$ be the set of these,
$q = |U|$.

> **Algorithm.** Give every $g \notin U$ to some agent with $g \notin D_i$ (one exists, by
> definition). Split $U$ as evenly as possible: $u_i := |A_i \cap U| \in \{\lfloor q/n\rfloor, \lceil q/n\rceil\}$.
>
> **Theorem C.** The result is envy-freeable with $p \in \{0,1\}^n$ and total subsidy
> $\le n-1$. Tight.

*Proof.* By construction $c_i(A_i) = u_i$: every non-universal chore in $A_i$ is free for $i$.
For any $j$, $A_j \cap U \subseteq D_i$, so $c_i(A_j) = |A_j \cap D_i| \ge u_j$. Hence
$w_A(i,j) = u_i - c_i(A_j) \le u_i - u_j$. Summing along a path $(i_1,\dots,i_r)$ the bound
**telescopes**:
$$w_A(P) \;\le\; u_{i_1} - u_{i_r} \;\le\; 1 ,$$
and along a cycle it gives $\le 0$, so $A$ is envy-freeable. $\square$

(Verified on $2\times10^5$ random instances, $n\le5$, $m\le7$: maximum per-agent subsidy ever
observed $=1$.)

The shape of this proof — *dump every chore on somebody who finds it free, then balance
what nobody wants* — is the intuition the general case has to reproduce. The obstruction
in general dichotomous is that "free for $i$" is **context dependent**: $g$ may be free on
top of $A_j$ and cost $1$ on top of $A_i$.

### 4.2 Theorem D — identical costs, and $n = 2$

**Identical costs** $c_1 = \dots = c_n = c$. Every allocation is envy-freeable (all
reassignments have equal welfare), and path weights telescope exactly:
$w_A(P) = c(A_{i_1}) - c(A_{i_r})$, so $\ell_A(u) = c(A_u) - \min_j c(A_j)$.
Greedily adding each chore to a currently **cheapest** bundle keeps
$\max_i c(A_i) - \min_i c(A_i) \le 1$ (marginals are $1$-Lipschitz), so $p \in \{0,1\}^n$.

**$n = 2$: exact duality with R3.** Define $\hat v_i(S) := c_i(M) - c_i(M \setminus S)$. Its
marginals are $c_i(T) - c_i(T\setminus g)$ with $T = M\setminus S$, so $\hat v_i$ is a
*dichotomous goods* valuation. For $n=2$, $A_2 = M \setminus A_1$, so
$c_1(A_1) = c_1(M) - \hat v_1(A_2)$ and $c_1(A_2) = c_1(M) - \hat v_1(A_1)$, whence
$$w^{c}_A(1,2) \;=\; \hat v_1(A_1) - \hat v_1(A_2) \;=\; \hat w_{B}(1,2), \qquad B := A^{\mathrm{swap}} .$$
The two envy graphs coincide, so **R3 for $n=2$ gives the chore theorem for $n=2$**:
$p \in \{0,1\}^2$, total $\le 1$, tight. The argument dies at $n \ge 3$ because
$M \setminus A_i$ is no longer a bundle of the partition.

---

## 5. Theorem E (negative) — the R3 induction is *not* repairable

This is the main structural finding.

> **Theorem E.** There is a 3-agent instance with negative dichotomous valuations, an
> envy-freeable partial allocation $A$ with $p = \ell_A \in \{0,1\}^3$, and an unallocated
> chore $g$, such that **for every agent $x$**, $Z^x$ requires a subsidy of $2$ — even though
> the full instance admits a **zero-subsidy** allocation.

**Instance.** $M = \{a_1, a_2, g\}$,
$$c_1(S) = \max(0, |S| - 1), \qquad c_2(S) = c_3(S) = |S| .$$
($c_1$ is dichotomous and supermodular — legal, since R3's class is not restricted to
submodular.)

**State.** $A = (\{a_1,a_2\},\ \emptyset,\ \emptyset)$.
Envy matrix $\begin{psmallmatrix}0&1&1\\-2&0&0\\-2&0&0\end{psmallmatrix}$, no positive cycle,
$p = (1,0,0)$ — a legal state of the invariant.

**Not extendable.** The marginal cost of $g$ is $1$ for every agent on her own bundle, *and*
on every bundle she can receive under an envy-freeable reassignment (agent 1 must keep
$\{a_1,a_2\}$, since handing it to 2 or 3 costs $2$ instead of $1$).

**Every insertion fails.**

| receiver | resulting subsidies |
|---|---|
| agent 1 | $(2,0,0)$ |
| agent 2 | $(2,1,0)$ |
| agent 3 | $(2,0,1)$ |

**But the instance is trivial.** $(\{a_1\},\{a_2\},\{g\})$ gives an all-zero envy matrix and
$p = (0,0,0)$.

*(Machine-verified; see `deadend.py`.)*

### Why it happens, and what it rules out

By §1, in the hard case ($\mu_x = -1$ for all $x$) the receiving agent's **outgoing** arcs
all rise by exactly $1$. So $p_x = 0$ is necessary. It is not sufficient: a path
$u \rightsquigarrow i \to x \to y \rightsquigarrow$ of weight $1$ through $x$ becomes weight
$2$ whenever $\delta_{i,x} := c_i(A_x \cup g) - c_i(A_x) = 0$. In the instance above both
$x=2$ and $x=3$ are hit this way by $i=1$.

One consolation prize *is* provable, and it isolates exactly where the damage is:

> **Lemma E1.** In the hard case, if $(A,p)$ is not extendable then $Z^x$ is envy-freeable
> for **every** $x$.
>
> *Proof.* A cycle $C$ through $x$ with predecessor $i$ has
> $w_{Z^x}(C) = w_A(C) + 1 - \delta_{i,x}$. If $w_A(C) \le -1$ this is $\le 0$. If
> $w_A(C) = 0$, rotating along $C$ is an envy-freeable reassignment in which $i$ receives
> $A_x$, so non-extendability forces $\delta_{i,x} = 1$ and again $w_{Z^x}(C) \le 0$.
> $\square$

So **envy-freeability survives insertion; only the $\{0,1\}$ subsidy bound breaks.** R3's
FINDSINK cannot be mirrored either: its navigation rule jumps to an agent that needed
subsidy $\ge 2$, and in the goods world that agent is automatically in $M(p)$ (the set R3
wants); in the chore world the same agent automatically has $p_u = 1$, i.e. is exactly the
kind of agent we must *not* hand the chore to.

**Conclusion.** Any proof of the chore analogue must be allowed to **re-open already-allocated
bundles**. The "allocate one item at a time, never move an old item, reassign bundles only"
template of R3 is provably insufficient. This is a genuine asymmetry between R3 and its
mirror, not a gap in our ingenuity.

---

## 6. Theorem F (structure of a $\{0,1\}$ solution)

Writing $S := \{i : p_i = 1\}$, the pair $(A,p)$ with $p \in \{0,1\}^n$ is envy-free iff

* **(a)** $c_i(A_i) \le c_i(A_j)$ whenever $i,j$ are both in $S$ or both in $\bar S$;
* **(b)** $c_i(A_i) \le c_i(A_j) + 1$ for $i \in S$, $j \in \bar S$;
* **(c)** $c_i(A_i) + 1 \le c_i(A_j)$ for $i \in \bar S$, $j \in S$.

A **two-tier** structure: unpaid agents are exactly-EF among themselves and *strictly*
prefer their own bundle to every paid agent's bundle by at least one unit; paid agents are
exactly-EF among themselves and EF1 towards the unpaid. Useful as a certificate format and
as the object to construct directly (choose $S$ first, then allocate).

---

## 7. The size-shift transform — why this is *not* a corollary of R3

> **Theorem G.** Let $\tilde v_i(S) := |S| - c_i(S)$. Then each $\tilde v_i$ is a
> **dichotomous goods** valuation, and for every allocation $A$,
> $$w^{c}_A(i,j) \;=\; \tilde w_A(i,j) \;+\; |A_i| - |A_j| .$$
> Consequently **every cycle has the same weight in both graphs** (so $A$ is envy-freeable
> for the chores $c$ **iff** it is envy-freeable for the goods $\tilde v$), while for a path
> from $u$ to $v$, $\ \ w^c(P) = \tilde w(P) + |A_u| - |A_v|$, giving
> $$\ell^{c}_A(u) \;=\; \max_v\big[\tilde d_A(u,v) + |A_u| - |A_v|\big].$$

*Proof.* $\tilde v_i(S\cup g) - \tilde v_i(S) = 1 - (c_i(S\cup g) - c_i(S)) \in \{0,1\}$;
the identity is a one-line expansion; the telescoping of $|A_{i_t}| - |A_{i_{t+1}}|$ does the
rest. $\square$

**Reading.** The chore problem is *exactly* R3's goods problem **plus a cardinality-balancing
requirement**. A sufficient condition falls out: an R3 solution for $\tilde v$ in which
$|A_i| + p_i$ has spread $\le 1$ across agents gives $\ell^c \le 1$, since
$\tilde d_A(u,v) \le p_u - p_v$. R3 offers no control on bundle sizes — indeed its output need
not even be EF1 (their Appendix C) — so the chore theorem does **not** follow from R3 as a
black box, and Theorem E says the algorithm cannot simply be re-run either. This transform
is also the cleanest way to see that the chore problem is *at least as expressive* as R3's.

---

## 8. Conjecture and evidence

> **Conjecture 1.** For negative dichotomous valuations there is always an envy-free solution
> $(A,p)$ with $p \in \{0,1\}^n$, hence total subsidy $\le n-1$. Tight.
>
> **Conjecture 2 (stronger, and the one to attack).** Such an $A$ can be taken
> **utilitarian-optimal**, i.e. minimising $\sum_i c_i(A_i)$ over *all* allocations.

**Evidence.**

| experiment | result |
|---|---|
| exhaustive, $n=3$, $m=3$, all $9{,}880$ instances up to agent symmetry | worst-case minimum per-agent subsidy $= 1$ |
| randomised, $n\in\{3,4,5\}$, $m\in\{4,5,6\}$, $\approx 35{,}000$ instances | 0 counterexamples |
| does *some* utilitarian-optimal allocation attain $\le 1$? | yes in $100\%$ of $\approx 10{,}000$ instances |
| does *every* utilitarian-optimal allocation attain $\le 1$? | **no** (fails in $\approx 1\text{–}3\%$) |

So the utilitarian-optimal set always contains a witness but is not uniformly good — the
problem is reduced to a **selection rule inside that set**. Three natural rules were tested
and all fail: minimising $\Psi(A) = \sum_i\sum_j c_j(A_i)$; leximin on the perceived-load
vector $\big(\max_j c_j(A_i)\big)_i$; and single-chore-transfer local search on
$(\max_i \ell_A(i), \sum_i \ell_A(i))$ restricted to the utilitarian-optimal set (which has
bad local minima).

---

## 9. Where to push next

1. **Exploit utilitarian optimality.** It gives a strong exchange property: if $g \in A_i$ is
   *active* for $i$ (i.e. $c_i(A_i) - c_i(A_i \setminus g) = 1$) then
   $c_j(A_j \cup g) = c_j(A_j) + 1$ for **every** $j$ — nobody can absorb it for free.
   Combine with Theorem B: a path of weight $\ge 2$ from $u$ to $v$ forces
   $c_v(A_u) \ge c_v(A_v) + 2$, i.e. $A_u$ carries at least two units that are live for $v$.
   The goal is to transfer one of them along the path and show a potential drops.
2. **Richer moves than single transfers.** Local search with single transfers has bad local
   minima (§8). Use exchange *paths/cycles* (Yankee-Swap / matroid-union style, cf.
   `glossary` §7) so that the move set matches the utilitarian-optimal polytope's face
   structure.
3. **Milestone ladder.** binary additive **(done, Thm C)** $\to$ binary submodular
   (matroid-rank costs; expect matroid union to give the balancing directly) $\to$
   general dichotomous.
4. **Two-tier construction.** Build $S$ and $\bar S$ from Theorem F directly rather than
   allocating item-by-item. In Theorem C's proof, $S$ is exactly the set of agents holding a
   $\lceil q/n\rceil$-share of the universally-bad chores — worth seeing what plays that role
   in general.
5. **Literature check before investing.** Best current published bound covering this class is
   R9 (doubly monotone, from an EF1 allocation): $n-1$ per agent, $n(n-1)/2$ total. Our claim
   would be a factor-$n$ improvement on the dichotomous-chore subclass — the same factor R3
   gains over R2. Confirm nobody has done "dichotomous chores with subsidy" already.

---

## 10. Files

`gen.py` (enumerate dichotomous functions), `search.py` (exhaustive $n=3,m=3$),
`fast.py` (randomised counterexample hunt), `msw.py` (utilitarian-optimal test),
`tiebreak.py` (selection rules), `localsearch.py` (local minima), `deadend.py` (Theorem E),
`binadd.py` (Theorem C verification).
