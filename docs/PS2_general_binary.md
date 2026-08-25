# Problem Statement 2 — General Binary Valuations (Goods and Chores)

*[To be refined. This is a faithful transcription of the framing given
verbally on 2026-08-24, in the style of `Problem Statement 1.txt`, not yet a
worked-out formal statement.]*

## Where this sits

PS1 (`Problem Statement 1.txt`) asked the chores mirror of R3 (Barman et al.):
**negative dichotomous** valuations, $v(S) - v(S \cup \set g) \in \set{0,1}$ —
every item a chore for every agent. That question is now **closed**: proved
for every $n$, written up at `report/main.tex`.

PS2 generalizes the valuation class one step further: from *negative*
dichotomous (chores only) to **general binary** — every marginal in
$\set{-1,0,1}$, so each item may be a good for some agents and a chore for
others, rather than every item being a good for everyone (R3's setting) or a
chore for everyone (PS1's setting).

## The model

$n$ agents, $m$ indivisible items. Each agent $i$ has a valuation
$v_i : 2^M \to \mathbb{R}$ with $v_i(\emptyset) = 0$ and

$$v_i(S \cup \set g) - v_i(S) \in \set{-1,0,1} \qquad \text{for every } S \subseteq M,\ g \in M \setminus S.$$

This subsumes R3's dichotomous goods ($\set{0,1}$ only) and PS1's negative
dichotomous chores ($\set{0,-1}$ only) as the two boundary cases; the general
case allows a single item to be a good for one agent and a chore for another,
and an agent's own relationship to an item to depend arbitrarily on the rest
of her bundle (no additivity is assumed, matching R3 and PS1).

## Objective

Either prove the analogue of R3's guarantee — an envy-free allocation with
subsidy $\subsidy \in \set{0,1}^n$, hence $\le n-1$ total, in polynomial
time — for this general class, or exhibit an instance showing the guarantee
fails.

## Relationship to the existing corpus

Not the same question as R11 (Lu–Mackenzie–Suzuki, 2026), which settles
goods-and-chores for **additive** valuations. Dichotomous and additive are
incomparable classes (§1 of `docs/RESIDUAL_GENERAL_BINARY.md` says why this
matters). See `docs/map.md` for the full corpus and `docs/RESIDUAL_GENERAL_BINARY.md`
for the running log on this question.
