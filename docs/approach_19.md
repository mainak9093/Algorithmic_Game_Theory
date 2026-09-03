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

## 5. The three bundles can be taken to be INTERVALS

The two-bundle proof of §1 is really a statement about an *ordered* ground set:
the walk moves items one at a time, so its partitions are prefix/suffix splits.
Read that way, §1 says every order admits a prefix cut with the two sides within
1. The natural three-bundle analogue is to allow **two** cuts — which is exactly
the discrete shape of necklace splitting, one measure and three parts.

> **(INTERVAL).** For any general binary $v$ and **any** linear order
> $g_1,\dots,g_m$, there are cuts $0 \le a \le b \le m$ such that the three
> consecutive blocks
> $$\set{g_1..g_a},\quad \set{g_{a+1}..g_b},\quad \set{g_{b+1}..g_m}$$
> have $\max_j v(B_j) - \min_j v(B_j) \le 1$.

**Exhaustively true, and order-free** — not "for some order", for *every* order:

| | valuations | every order has a good cut |
|---|---|---|
| $m=3$ | all **495** | **495** |
| $m=4$ | all **197,547** | **197,547** |

and robust beyond enumeration range:

| | sampled | climbs | refutations | cuts vs partitions |
|---|---|---|---|---|
| $m=5$ | 4,000 / 4,000 | 60 × 300 | **0** | 21 vs 243 |
| $m=6$ | 1,200 / 1,200 | 30 × 250 | **0** | 28 vs 729 |
| $m=7$ | 300 / 300 | — | — | **36 vs 2,187** |

This is a large structural gain independently of any proof: the search collapses
from $3^m$ partitions to $\binom{m+2}{2}$ cuts, and the cuts carry a
**two-parameter lattice structure** — the triangle $\set{(a,b) : 0\le a\le b\le m}$
— in which moving one cut by one step transfers a single item between adjacent
blocks. That is precisely the "no jump" hypothesis a Sperner or Tucker argument
needs, and it is why (INTERVAL) is a better target than (BAL-1) even though it
is formally stronger.

### The Sperner attempt, and exactly where it breaks

Label each cut by an index attaining the **maximum** block value. The triangle's
corners are the cuts where one block is everything:
$P_1 = (m,m)$, $P_2 = (0,m)$, $P_3 = (0,0)$.

**The corner condition holds** — always. At $P_j$ block $j$ is $M$ and the other
two are empty, so when $v(M) > 0$ the maximum is at $j$ and the corner gets
label $j$: 148 of 148 at $m=3$, 54,413 of 54,413 at $m=4$.

**The boundary condition fails.** Sperner also needs that on the edge where
block $j$ is empty, the maximum is attained outside $j$. It is not: 133 of 148
at $m=3$, 48,439 of 54,413 at $m=4$. The smallest witness is

$$v = (0,\,-1,-1,-1,\,0,0,0,\,+1) \quad\text{by bundle size } 0,1,2,3,$$

singletons worth $-1$, pairs worth $0$, the whole set worth $+1$. On an edge
where one block is empty, the other two can both be singletons worth $-1$ — so
the **empty** block, worth $0$, is the strict maximum, and the label points
inward. Sperner does not apply.

That is a real obstruction, not a bookkeeping slip: a valuation can be negative
on every small block while positive on the whole set, so "empty" is genuinely
the best block on part of the boundary. Any labelling used here has to survive
that.

## 6. Next

1. **Prove (INTERVAL)**, not (BAL-1) — §5 makes it the sharper target, with a
   two-parameter lattice and a one-item step bound already in place. The
   labelling must cope with the failure in §5: an *empty* block can be the
   strict maximum, because a valuation may be negative on every small block and
   positive on the whole set. Two ways round it are untried — a labelling by
   argmin with a Tucker-type lemma (the corners then carry the dual condition,
   label $
e j$ at $P_j$), or restricting the triangle to cuts with all three
   blocks non-empty and handling the degenerate edges by the proved two-bundle
   lemma, which already settles any edge on which one block is empty.
2. **(TWO-BALANCE) from (BAL-1).** Given (BAL-1) for each agent separately,
   what forces a *common* partition for some pair? The $m=3$ counterexamples to
   the every-pair form are the data to work from. (INTERVAL) helps here too:
   both agents' good cuts live in the same $inom{m+2}{2}$-point triangle, so
   the question becomes whether two subsets of a small triangle must meet.
3. Exhaustive (BAL-1) at $m=5$ is out of reach by enumeration, but climbs at
   both (BAL-1) and (INTERVAL) have found nothing.

### Scripts

`two_balance.py` (the decomposition and the hard-instance characterisation),
`balance_lemma.py` ((BAL-1), (BAL-2) in both strengths, and climbs at each),
`ivt.py` (the step bound, the walk, and exhaustive (BAL-1) at $m=3,4$),
`interval.py` ((INTERVAL), exhaustive and order-free at $m=3,4$),
`interval_hunt.py` (climbs at (INTERVAL), and the Sperner corner and boundary
conditions).
