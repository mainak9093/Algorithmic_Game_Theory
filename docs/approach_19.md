# Approach 19 — the marginal condition as *continuity*, and a proved balancing lemma

*Follows approach 18, which reduced PS2 at $n=3$ to (AVOID-1ROW): a partition
that two of the three agents each see as equal to within one. This pass
decomposes that statement, characterises the hard instances exactly, and
**proves** its two-bundle base case by a discrete intermediate-value argument —
the first time in this project the marginal condition is used as a continuity
property rather than a counting one.*

---

## 0. What is new

**Proved.**

> **Lemma (two bundles).** Every general binary valuation $v$ admits a
> partition $M = B_1 \sqcup B_2$ with $\abs{v(B_1) - v(B_2)} \le 1$.

**Exhaustively verified**, over the entire valuation class, not a sample:

> **(BAL-1).** Every general binary valuation admits a partition into **three**
> bundles with $\max_j v(B_j) - \min_j v(B_j) \le 1$.
>
> All **495** valuations at $m=3$; all **197,547** at $m=4$.

**Characterised.** The instances where PS2 at $n=3$ is not free — where no
partition gives all three agents spread $\le1$ — are exactly those where **some
agent holds both a $+1$ and a $-1$ singleton**: 45 of 45 at $m=3$, 3 of 3 at
$m=4$. Such an agent cannot use the one-item-each partition, and that is the
whole source of difficulty.

**Refuted.** The clean two-valuation statement — *every* pair of agents can be
simultaneously balanced — is **false**, 28 counterexamples at $m=3$. Only the
*some pair* version survives, and that is exactly what (AVOID-1ROW) needs.

---

## 1. The proof

Fix an order on the items and walk from $(M, \emptyset)$ to $(\emptyset, M)$,
moving one item at a time from $B_1$ to $B_2$. Write $d = v(B_1) - v(B_2)$.

Moving $g$ changes $v(B_1)$ by $-v(g \mid B_1 \setminus g)$ and $v(B_2)$ by
$+v(g \mid B_2)$, and both marginals lie in $\set{-1,0,1}$. Hence

$$\abs{d_{t+1} - d_t} \;\le\; 2 \qquad \text{at every step.}$$

The walk begins at $d = v(M)$ and ends at $d = -v(M)$.

- If $\abs{v(M)} \le 1$, the starting partition already works.
- Otherwise $d$ travels from $\ge 2$ to $\le -2$ (or the reverse). To avoid the
  interval $[-1,1]$ entirely, a single step would have to carry $d$ from
  $\ge 2$ to $\le -2$ — a change of at least $4$, contradicting the bound of
  $2$.

So some partition along the walk has $\abs{d} \le 1$. $\square$

Checked exhaustively: the step bound holds for all 495 valuations at $m=3$ and
all 197,547 at $m=4$, with the largest step exactly $2$ — so the bound is tight
and the argument has no slack to spare.

**Why this is a different kind of argument.** Every previous use of
"marginals in $\set{-1,0,1}$" in this project has been a counting bound —
$\abs{v(S) - v(T)} \le \abs{S \mathbin{\triangle} T}$, used to force items to
separate bundles. Here it is used to say that a walk through partition space
*cannot jump*, which is an intermediate-value argument. That is the toolkit of
consensus splitting and discrepancy, and it is the first thing in approaches
15–19 that actually proves an existence statement rather than reducing one.

## 2. How (AVOID-1ROW) decomposes

Approach 18 §6 leaves (AVOID-1ROW): a partition that two agents each see as
equal to within one, the third within two. It splits cleanly:

| | statement | status |
|---|---|---|
| **(BAL-1)** | one valuation, three bundles, spread $\le1$ | exhaustive at $m=3,4$; two-bundle case **proved** |
| **(TWO-BALANCE)** | *some pair* of agents balanced to spread $\le1$ simultaneously | 4,000 / 4,000, 1,000 / 1,000, 250 / 250 |
| **(THIRD)** | on such a partition the third agent is within 2 | never failed — 0 instances where every two-balanced partition left the third above 2 |

with (BAL-1) $\le$ (TWO-BALANCE) $\le$ (AVOID-1ROW) $\Rightarrow$ (AVOID)
$\Rightarrow$ PS2 at $n=3$.

**A negative result worth recording.** The tempting clean form — *every* pair
of agents can be simultaneously balanced, which would remove the three-agent
structure altogether — is **false**: 3,972 of 4,000 at $m=3$, so 28
counterexamples. It holds at $m=4,5,6$ and under climbs there, so it is a
statement that fails only when there are too few items to balance with. The
*some pair* form is what survives, and fortunately it is all (AVOID-1ROW) needs.

## 3. The hard instances, exactly

Every obstruction contains a $2$, so an instance admitting a partition with all
three spreads $\le 1$ is valid outright (approach 18 §6). The rest are the hard
case, and they have a complete description:

| | $m=3$ | $m=4$ | $m=5$ |
|---|---|---|---|
| instances | 4,000 | 1,000 | 250 |
| all three at spread $\le1$ — free | 3,955 | 997 | 250 |
| **hard** | **45** | **3** | 0 |
| of the hard, some agent holds both a $+1$ and a $-1$ singleton | **45** | **3** | — |

Every single one. The reason is immediate: if agent $i$ has $v_i(\set g) = +1$
and $v_i(\set h) = -1$, then the one-item-each partition hands her bundles she
values $+1$ and $-1$, a spread of $2$ before anything else happens. She must be
given a bundle that mixes the two signs, and that is what couples the three
agents together.

The hard fraction also **shrinks** with $m$ — 1.1%, 0.3%, 0% — which is the
opposite of the usual pattern and says the difficulty is a small-instance
effect, not a growing one.

## 4. Where the proof stands

$$\underbrace{\text{two bundles}}_{\textbf{proved, §1}} \;\longrightarrow\;
\underbrace{\text{(BAL-1)}}_{\text{exhaustive } m\le4} \;\longrightarrow\;
\underbrace{\text{(TWO-BALANCE)}}_{\text{open}} \;\longrightarrow\;
\underbrace{\text{(AVOID-1ROW)}}_{\text{open}} \;\longrightarrow\;
\underbrace{\text{PS2}(n{=}3)}_{\text{approach 18}}$$

The first arrow is the live question: **does the intermediate-value argument
reach three bundles?**

What is known about it. A one-dimensional walk does not suffice — the path from
$(M,\emptyset,\emptyset)$ to $(\emptyset,M,\emptyset)$ starts and ends at the
same spread, so there is nothing to cross. Three bundles need a
two-parameter family, which is the standard setting for a Sperner- or
Tucker-type argument rather than a plain IVT. Note also that the obvious
reduction fails: splitting $M$ into $C \sqcup D$ balanced, then splitting $D$
balanced, controls $\abs{v(D_1)-v(D_2)}$ but says nothing relating either to
$v(C)$, because $v$ is not additive and $v(D)$ does not determine $v(D_1)$ and
$v(D_2)$.

## 5. Next

1. **Extend §1 to three bundles.** Sperner / Tucker on the space of
   3-partitions, with the step bound of §1 as the "no jump" hypothesis. This is
   the single most valuable open step: it would turn (BAL-1) from exhaustive
   evidence into a theorem.
2. **(TWO-BALANCE) from (BAL-1).** Given (BAL-1) for each agent separately,
   what forces a *common* partition for some pair? The $m=3$ counterexamples to
   the every-pair form are the data to work from.
3. Exhaustive (BAL-1) at $m=5$ is out of reach by enumeration, but a climb at
   it has already found nothing.

### Scripts

`two_balance.py` (the decomposition and the hard-instance characterisation),
`balance_lemma.py` ((BAL-1), (BAL-2) in both strengths, and climbs at each),
`ivt.py` (the step bound, the walk, and exhaustive (BAL-1) at $m=3,4$).
