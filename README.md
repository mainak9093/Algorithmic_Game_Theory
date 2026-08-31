# Algorithmic Game Theory

Research notes and working material on **fair division of indivisible items with
subsidies**, built around one problem statement: envy-free allocation of **chores**
under negative dichotomous valuations.

## Problem Statement : Fair Envy Free Allocations with subsidy for Negative Dichotomous Valuations

Envy-freeness fails for indivisible items — the standard one-item, two-agent instance
already has no envy-free allocation. One repair keeps envy-freeness **exact** and buys
off the residual envy with money: each agent $i$ receives, alongside her bundle, a
subsidy $p_i \ge 0$ from a third party. The question is how much money this takes.

R3 (Barman et al.) settles this for **dichotomous** valuations, where every marginal
$v(S \cup \{g\}) - v(S) \in \{0, 1\}$ — every item is a *good*. There, a subsidy of
$0$ or $1$ per agent always suffices.

This project asks the mirrored question: **negative dichotomous** valuations, where

$$v(S) - v(S \cup \{g\}) \in \{0, 1\},$$

so every item is a **chore** — taking on one more costs an agent either nothing or
exactly one unit. No further structure is assumed: valuations need not be additive,
submodular, or subadditive.

**The objective.** Either prove the analogue of R3's guarantee in the chores setting —
subsidy in $\{0,1\}$ per agent, $n-1$ in total, in polynomial time — or exhibit an
instance showing the transfer fails.

Two facts fixed the target before any work began, both argued in
[`report/sections/introduction.tex`](report/sections/introduction.tex):

- **A bounded subsidy already existed.** Negative dichotomous valuations are doubly
  monotone under the two-sided normalisation, so R9's EF1 ⇒ EF-with-subsidy reduction
  applies off the shelf and gives $n-1$ per agent, $n(n-1)/2$ total. That was the
  baseline to beat, not the goal.
- **The $n-1$ lower bound transfers.** With $n$ agents and $n-1$ unit chores, every
  complete allocation forces a total subsidy of $n-1$ — so the target bound, once
  proved, is tight.

The gap between the two was a factor of $n$ in the total. In the report this problem
statement is formalised as **Conjecture 2**.

## Notation

$N = [n]$ agents; $M$ items with $|M| = m$; valuation $v_i : 2^M \to \mathbb{R}$ with
$v_i(\emptyset) = 0$; allocation $A = (A_1,\dots,A_n)$; subsidy vector
$p \in \mathbb{R}^n_+$; entitlement weights $w_i > 0$; value matrix $V^A_{ij} = v_i(A_j)$;
$V$ = max item value; $W = \sum_i w_i$.

It is often cleaner to work in **cost form**, $c_i := -v_i$, so that $c_i$ is
non-decreasing with marginals in $\{0,1\}$ and an envy-free solution reads
$c_i(A_i) - p_i \le c_i(A_j) - p_j$.

Source papers use their own letters — divergences are flagged in the glossary §10.

## Status

**The problem statement is solved, for every number of agents $n$.** For every instance
with negative dichotomous valuations there is an envy-free solution with a subsidy of
$0$ or $1$ per agent — hence at most $n-1$ in total — computable in polynomial time in
the value-oracle model, under no assumption on the cost functions beyond binary
marginals, and with no bound on the number of chores. The allocation is moreover
EF1. The bound is tight.

| Result | Where |
|---|---|
| **The proof, general $n$** | [`report/sections/main_result.tex`](report/sections/main_result.tex) → §3 of `main.pdf` |
| Earlier $n = 3$ only argument | [`report/sections/n3.tex`](report/sections/n3.tex) — correct, superseded, not built into `main.pdf` |
| Full draft incl. all 14 approaches | [`report/working/`](report/working/) → `working.pdf` |
| Full research log, every route tried | [`docs/RESIDUAL.md`](docs/RESIDUAL.md) §7.16 |

The proof completes an envy-free **partial** allocation — taken from R12 (Tao et al.) —
by placing the residual chores and then reassigning which agent receives which bundle.
Two independent routes reach the general-$n$ result: a minimum-cost-within-$S$ argument
with a telescoping potential, and a simpler one using the identity assignment plus a
backward equality closure that never invokes Halpern–Shah.

**One dependency worth stating plainly:** the argument uses the *halting state* of R12's
Algorithm 3 — its internal stopping rule — not merely the statement of its Theorem 5.1.
That is legitimate but is the first thing a referee should check. It is flagged in the
write-up itself.

This fills the remaining corner of the square:

| | goods | chores |
|---|---|---|
| additive | R2 | R11 |
| dichotomous | R3 | **this project** |

each of the four giving one dollar per agent and $n-1$ in total.

## What's next

A second, independent investigation is starting: **general binary**
valuations, every marginal in $\{-1,0,1\}$ — goods and chores together,
rather than chores only. Problem statement:
[`docs/PS2_general_binary.md`](docs/PS2_general_binary.md). It has its own
scratch area, [`report/working_general_binary/`](report/working_general_binary/),
its own research log, [`docs/RESIDUAL_GENERAL_BINARY.md`](docs/RESIDUAL_GENERAL_BINARY.md),
and its own scripts folder, `updates_general_binary/` — kept separate from
everything above on purpose, so the closed result and the open question can
never be confused for each other. Nothing above this section is affected.

## Contents

| Path | What it is |
|---|---|
| [`report/`](report/) | The LaTeX write-up of the closed result. Two documents: `main.tex` → the report (the general-$n$ proof), `working.tex` → the full draft, including every parked approach that came before it. See [`report/README.md`](report/README.md). |
| [`report/working_general_binary/`](report/working_general_binary/) | Scratch area for the new, open investigation — independent of `report/`'s two documents above. |
| [`docs/`](docs/) | All project notes. [`RESIDUAL.md`](docs/RESIDUAL.md) is the closed chores-only research log; [`RESIDUAL_GENERAL_BINARY.md`](docs/RESIDUAL_GENERAL_BINARY.md) is the new one. Also `CRI.md`, `BALANCE_RULE.md`, `approach_14.md`, `PS2_general_binary.md`, and the standalone proof/audit notes. |
| [`updates/`](updates/) | `update_1/` … `update_49/`, one folder per work session on the closed result. Every claim in `report/working/` is machine-checked by scripts here. |
| `updates_general_binary/` | The same convention, for the new investigation. Created on first use. |
| [`References/`](References/) | Source papers, `Reading_1.pdf` … `Reading_12.pdf`. |
| [`graphify-out/`](graphify-out/) | Knowledge graph of the repository — see [Knowledge graph](#knowledge-graph) below. |
| [`docs/map.md`](docs/map.md) | Paper map: one entry per reading (R1–R12) — what it does, what it improves on, what it leaves open — plus the dependency DAG and the bound tables. Shared by both investigations. |
| [`docs/glossary_fair_division_subsidies.md`](docs/glossary_fair_division_subsidies.md) | Project glossary — every definition restated in a single fixed notation, with provenance tags back to the source readings. Shared by both investigations. |
| [`Problem Statement 1.txt`](Problem%20Statement%201.txt) | The original (closed) problem statement, as first written. |

## The corpus

The readings are **not** a chronology — they form a small DAG with one trunk, several
branches, and papers answering adjacent questions. Publication order:

| Reading | Year | Short name | Setting |
|---|---|---|---|
| R1 | 2019 (SAGT) | Halpern–Shah | unweighted, additive, money |
| R2 | 2019/20 (EC) | Brustle et al. | unweighted, additive + monotone, money |
| R10 | 2021 (APPROX) | Bhaskar–Sricharan–Vaish | chores + mixed resources, *no money* |
| R3 | 2022 | Barman et al. | unweighted, dichotomous, money |
| R5 | 2023 (FAW) | Bu–Song–Yu | unweighted, binary, *no money* |
| R12 | 2023 | Tao–Wu–Yu–Zhou | **binary chores**, *no money* (EFX + PO) |
| R9 | 2023 (AAAI'24) | Kawase et al. | unweighted, doubly monotone, money |
| R8 | 2024 (AAAI) / 2025 (SCW) | Montanari et al. | weighted, submodular, *no money* |
| R7 | 2024 | Dai et al. | weighted, house allocation, money |
| R4 | 2024 | Klein Elmalem et al. | weighted, additive, money |
| R6 | 2025 | Klein Elmalem, Aziz et al. | weighted, monotone + subclasses, money |
| R11 | 2026 | Lu–Mackenzie–Suzuki | additive **goods and chores**, money |

The corpus splits on the repair to envy-freeness:

- **(A) Add money** — keep EF exact, buy off the envy with an outside subsidy $p$, and
  ask how much. → R1, R2, R3, R9, R11 (equal entitlements); R4, R6, R7 (unequal).
- **(B) Weaken the notion** — no money; relax EF to EF1 / EFX / WEF$(x,1-x)$ / TWEF /
  WMEF and ask what still exists. → R5, R8, R10, R12.

See [`docs/map.md`](docs/map.md) §0 for the full structure and the dependency DAG.

### The three papers that matter most here

- **R3 — Barman, Krishna, Narahari, Sadhukhan** (2022). The goods-side result this
  project mirrors: dichotomous valuations admit a subsidy of $0$ or $1$ per agent.
- **R12 — Tao, Wu, Yu, Zhou** (2023). **The paper the proof is built on.** Its
  Theorem 5.1 gives a polynomial-time envy-free *partial* allocation leaving at most
  $n-1$ chores unassigned, with no subsidy at all. Completing that partial allocation
  is the whole of our argument.
- **R11 — Lu, Mackenzie, Suzuki** (2026). The additive goods-and-chores analogue of R2.
  It subsumes this project's binary-additive special case but **not** the dichotomous
  class — additive and dichotomous are incomparable — which is why the main question
  survived it.

R10 (Bhaskar–Sricharan–Vaish, 2021) is the other late addition: it establishes that
money is genuinely needed, since exact EF for chores is NP-complete already for binary
additive costs, and it supplies the EF1 algorithm that R9's reduction consumes.

## Knowledge graph

The repository is indexed with [graphify](https://pypi.org/project/graphifyy/):
`graphify-out/` holds `graph.json`, a browsable `graph.html`, and
`GRAPH_REPORT.md` (1686 nodes, 3006 edges, 101 communities). Query it instead of
grepping:

```bash
graphify query "how is Conjecture 2 proved for n=3"
graphify explain "excess"
graphify path "approach_12.tex" "prove_r1.py"
graphify update .        # rebuild after code changes (AST-only, free)
```

The current graph is an AST-only build, which covers the scripts; a semantic pass over
the `.md` notes and PDFs can be added with `/graphify --update`.

## Building

```bash
cd report
latexmk -pdf main.tex       # the report: the closed result, proved for every n
latexmk -pdf working.tex    # the full draft: same, plus the full 14-approach trail

cd working_general_binary
latexmk -pdf working_general_binary.tex   # the new, open investigation
```

## A note on the PDFs

`References/` holds the source papers for convenience while working. Copyright rests
with the respective authors and publishers; consult the originals for citation.
