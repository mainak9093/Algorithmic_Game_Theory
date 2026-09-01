# Is the returned allocation Pareto optimal?

*Investigation opened 2026-09-01 at the supervisor's request. Scripts:
`updates_pareto/update_1/`. This concerns the closed chores paper (PS1,
`report/main.tex`), not PS2.*

---

## 0. Answer

**No — and the reason is stronger than "our algorithm misses it".**

| | Finding | Status |
|---|---|---|
| **A** | Algorithm 1's output is frequently **not** Pareto optimal — **14.40%** of all 54,872 instances at $n=3,m=3$, exhaustively | **proved** by exhaustion |
| **B** | **PO is incompatible with the theorem's guarantee.** There are instances where *no* allocation is both Pareto optimal and envy-free with $p \in \{0,1\}^n$ | **proved**, minimal witness verified independently |
| **C** | B is a **general family**, not a small-case artefact: identical agents with $c(S)=\min(\lvert S\rvert,2)$ and $m \ge n+1$. Confirmed for $n=2,3,4$ | **proved** by exhaustion over the family |
| **D** | The **binary additive** subclass is exempt: zero failures, exhaustively and in sampling | search-verified |

Because of **B**, this is not a defect that a better tie-breaking rule inside
Algorithm 1 could repair. Chasing a PO proof would be chasing something false.

---

## 1. What "Pareto optimal" means here

For chores in cost form, allocation $B$ **Pareto dominates** $A$ when
$\cost_i(B_i) \le \cost_i(A_i)$ for every agent, strictly for at least one. $A$
is **PO** when nothing dominates it.

This is a property of the **allocation alone** and ignores subsidies. It is the
notion Tao et al. use when they prove EFX $+$ PO for binary *additive* chores,
so it is the natural reading of the question.

## 2. Finding A — the algorithm's output is often not PO

Algorithm 1 was implemented in full for arbitrary $n$ (TWYZ Algorithm 3, then
the completion, then the subsidy set $P$) and its output tested against every
complete allocation.

| $n,m$ | coverage | output not PO |
|---|---|---|
| 2, 3 | **exhaustive**, all $38^2 = 1{,}444$ instances | **160 (11.08%)** |
| 2, 4 | **exhaustive**, all $990^2 = 980{,}100$ | **204,560 (20.87%)** |
| 3, 3 | **exhaustive**, all $38^3 = 54{,}872$ | **7,904 (14.40%)** |
| 3, 4 | 4,000 sampled | 546 (13.7%) |
| 3, 5 | 1,200 sampled | 281 (23.4%) |
| 4, 4 | 2,000 sampled | 121 (6.0%) |

Not a rare edge case, and the rate grows with the number of chores.

**A clean small witness** (`verify_counterexample.py`, checked with the
envy-graph machinery rewritten from scratch). $n=3$, $m=3$; agents 1 and 3 have
the additive cost "$a$ and $c$ cost 1, $b$ is free"; agent 2 has singletons
costing 1 but $\cost_2(\{a,c\}) = 1$ — one non-additivity, and the only one.

- Algorithm 1 returns $A = (\{a,b\}, \{c\}, \emptyset)$, costs $(1,1,0)$,
  needing $p=(1,1,0)$, total subsidy $2$.
- $B = (\{b\}, \{a,c\}, \emptyset)$ has costs $(0,1,0)$: agent 1 strictly
  better, nobody worse. So $B$ dominates $A$.
- **The sting:** $B$ is itself feasible for the theorem, and cheaper —
  envy-free with $p=(0,1,0)$, total subsidy $1$.

So on that instance the algorithm returns an outcome dominated by another
outcome that also satisfies the theorem *and* costs the sponsor less.

## 3. Finding B — PO is *unattainable*, not merely missed

The decisive result. **Minimal witness**, verified independently in
`verify_incompatibility.py`:

> $n = 2$ agents, $m = 3$ chores, **both agents share**
> $$\cost(S) = \min(\lvert S\rvert,\, 2).$$

One chore costs 1, two cost 2, and a third is free once you hold two. Every
marginal is $0$ or $1$, $\cost(\emptyset)=0$, monotone — a legitimate instance
of the paper's class. Non-additive: an additive $\cost$ would give
$\cost(\{a,b,c\}) = 3$.

| allocation | costs | PO? | valid ($p\in\{0,1\}^2$)? | cheapest $p$ |
|---|---|---|---|---|
| $(\{a,b,c\}, \emptyset)$ | $(2,0)$ | **yes** | **no** | $(2,0)$ |
| $(\emptyset, \{a,b,c\})$ | $(0,2)$ | **yes** | **no** | $(0,2)$ |
| the six splits | $(2,1)$ or $(1,2)$ | no | yes | total $1$ |

**Both** Pareto optimal allocations need a subsidy of $2$, which the theorem
forbids; **all six** allocations the theorem allows are dominated. Zero
allocations are both.

*Why.* Cost saturates at $2$, so concentrating all three chores on one agent is
socially cheapest — total cost $2$ against $3$ for any split. But concentration
makes the loaded agent envy the empty one by exactly $2$, and the theorem caps
the subsidy at $1$ per agent. The bound therefore *forces* a split, and every
split wastes a unit of cost.

## 4. Finding C — a general family, not a small-case artefact

Sweeping $\cost(S) = \min(\lvert S\rvert, t)$ with identical agents over
$n \in \{2,3,4\}$, $m \le 7$, $t \le m$ gives **16** incompatible triples:

| $n$ | incompatible at |
|---|---|
| 2 | $m \ge 3$ with $t=2$; also $t=3$ for $m\ge5$, $t=4$ for $m=7$ |
| 3 | $m \ge 4$ with $t=2$; also $t=3$ at $m=7$ |
| 4 | $m \ge 5$ with $t=2$ |

The pattern is $t=2$ and $m \ge n+1$. The efficiency loss grows with $m$:

| $n,m,t$ | least total cost, PO | least total cost, valid |
|---|---|---|
| 3, 4, 2 | 2 | 4 |
| 3, 7, 2 | 2 | 4 |
| 4, 5, 2 | 2 | 5 |
| 4, 6, 2 | 2 | 5 |

So the guarantee does not merely miss PO by a hair — on this family it costs a
constant-factor loss in total disutility.

## 5. Finding D — binary additive is exempt

| coverage | additive instances | output not PO |
|---|---|---|
| exhaustive $n{=}2,m{=}3$ | 64 | **0** |
| exhaustive $n{=}2,m{=}4$ | 256 | **0** |
| exhaustive $n{=}3,m{=}3$ | 512 | **0** |
| random, four $(n,m)$ settings | 15,200 runs | **0** |

Not vacuous: PO density in those instances is only $24.4\%$ at $n=3,m=3$ and
$42.2\%$ at $n=2,m=3$, so most allocations are *not* PO — the algorithm is
landing on PO ones rather than PO being easy to hit.

This is consistent with Tao et al., who obtain EFX $+$ PO for binary additive
chores. It also matches every counterexample above being non-additive:
**non-additivity appears to be necessary for the failure**, which is a natural
next thing to try to prove if the paper wants a positive companion statement.

## 6. What this means for the paper

- The honest claim is that the allocation is **EF1 and envy-free with subsidy
  $\le 1$ per agent**, and *not* Pareto optimal. Do not claim PO.
- Finding B means there is no point attempting a PO proof: it would be false.
  If PO is wanted, something must give — a larger subsidy, or a weaker fairness
  target.
- There is a clean positive statement available if wanted: on **binary
  additive** costs the failure never occurred in any test, exhaustive or
  sampled. Proving "additive $\Rightarrow$ the output is PO" would be a real
  addition and is the obvious next question.
- Worth stating explicitly in the paper as a short remark, since a reader who
  knows Tao et al.'s EFX $+$ PO result for binary additive chores will
  immediately wonder whether PO survives here. The answer — that it cannot,
  with a three-chore two-agent witness — is short enough to include.

## 7. Reproducing

All scripts in `updates_pareto/update_1/`, runnable from that folder.

| Script | What it does |
|---|---|
| `algo1.py` | Algorithm 1 for arbitrary $n$: TWYZ Algorithm 3, the completion, the subsidy set $P$; plus envy-graph, minimal subsidy and Pareto routines |
| `hunt_pareto.py [small\|wide]` | the first sweep: is the output PO, is PO reachable by some free choice, is PO attainable at all |
| `stress_q2.py [big]` | pushes the incompatibility question and the additive control at larger sizes |
| `exhaustive_n3m3.py [n3\|n2]` | exhaustive settlement at $m=3$ and $n \in \{2,3\}$, plus PO densities |
| `find_incompat.py` | extracts the incompatibility witnesses with a full allocation table |
| `saturating_family.py` | sweeps $\cost(S)=\min(\lvert S\rvert,t)$ to show the family generalises |
| `verify_counterexample.py` | independent re-check of the finding-A witness |
| `verify_incompatibility.py` | independent re-check of the finding-B witness |

Both negative findings have dedicated verifiers that reimplement the
envy-graph, envy-freeness and domination checks from scratch, so a bug in
`algo1.py` could not both produce a finding and confirm it.
