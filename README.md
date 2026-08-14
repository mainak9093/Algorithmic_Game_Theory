# Algorithmic Game Theory — Fair Division with Subsidies

Research notes and working material on **fair division of indivisible items with
subsidies**, and the problem this project set out to settle: **negative
dichotomous valuations** (chores).

## Status — solved

**Conjecture 2 is proved, for every number of agents $n$.** For every instance
with negative dichotomous valuations there is an envy-free solution with a
subsidy of $0$ or $1$ per agent — hence at most $n-1$ in total — computable in
polynomial time in the value-oracle model, under no assumption on the cost
functions beyond binary marginals (not additivity, not submodularity, and no
bound on the number of chores). The bound is tight.

| Result | Where |
|---|---|
| $n = 3$, self-contained proof | [`report/sections/n3.tex`](report/sections/n3.tex) → §3 of `main.pdf` |
| **General $n$** | [`report/working/approach_13.tex`](report/working/approach_13.tex) → `working.pdf` |
| Full research log, every route tried | [`docs/RESIDUAL.md`](docs/RESIDUAL.md) §7.16 |

The proof completes an envy-free **partial** allocation — taken from R12 (Tao
et al.) — by placing the residual chores and then reassigning which agent
receives which bundle. Two independent routes reach the general-$n$ result: a
minimum-cost-within-$S$ argument with a telescoping potential, and a simpler
one using the identity assignment plus a backward equality closure that never
invokes Halpern–Shah.

**One dependency worth stating plainly:** the argument uses the *halting state*
of R12's Algorithm 3 — its internal stopping rule — not merely the statement of
its Theorem 5.1. That is legitimate but is the first thing a referee should
check. It is flagged in the write-up itself.

## Contents

| Path | What it is |
|---|---|
| [`report/`](report/) | The LaTeX write-up. Two documents: `main.tex` → the report (scoped to the $n=3$ proof), `working.tex` → the full draft, including the general-$n$ proof and every parked approach. See [`report/README.md`](report/README.md). |
| [`docs/`](docs/) | All project notes. [`RESIDUAL.md`](docs/RESIDUAL.md) is the running research log and the authoritative status record; also `CRI.md`, `BALANCE_RULE.md`, `approach_14.md`, and the standalone proof/audit notes. |
| [`updates/`](updates/) | `update_1/` … `update_49/`, one folder per work session. Every claim in `report/working/` is machine-checked by scripts here. |
| [`References/`](References/) | Source papers, `Reading_1.pdf` … `Reading_12.pdf`. |
| [`graphify-out/`](graphify-out/) | Knowledge graph of the repository — see [Knowledge graph](#knowledge-graph) below. |
| [`docs/glossary_fair_division_subsidies.md`](docs/glossary_fair_division_subsidies.md) | Project glossary — every definition restated in a single fixed notation, with provenance tags back to the source readings. |
| [`docs/paper_map_R1_to_R9.md`](docs/paper_map_R1_to_R9.md) | One entry per paper (R1–R9): what it does, what it improves on, what it leaves open. Includes the dependency DAG and the bound tables. R10–R12 arrived later and are covered in the report's introduction and bibliography rather than here. |
| [`Problem Statement 1.txt`](Problem%20Statement%201.txt) | The original problem statement. |

## The corpus

The readings are **not** a chronology — they form a small DAG with one trunk,
several branches, and papers answering adjacent questions. Publication order:

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

Envy-freeness fails for indivisible goods, and the corpus splits on the repair:

- **(A) Add money** — keep EF exact, buy off the envy with an outside subsidy $p$, and
  ask how much. → R1, R2, R3, R9, R11 (equal entitlements); R4, R6, R7 (unequal).
- **(B) Weaken the notion** — no money; relax EF to EF1 / EFX / WEF$(x,1-x)$ / TWEF /
  WMEF and ask what still exists. → R5, R8, R10, R12.

See [`docs/paper_map_R1_to_R9.md`](docs/paper_map_R1_to_R9.md) §0 for the full
structure of R1–R9.

### The three later additions

- **R10 — Bhaskar, Sricharan, Vaish**, *On Approximate Envy-Freeness for
  Indivisible Chores and Mixed Resources* (APPROX/RANDOM 2021). Establishes that
  money is genuinely needed here: deciding whether an exactly envy-free
  allocation of chores exists is NP-complete already for binary additive costs.
  Also gives polynomial-time EF1 for chores and for doubly monotone instances,
  which is what supplies the input to R9's reduction.
- **R11 — Lu, Mackenzie, Suzuki**, *Optimal Subsidy Bounds for Goods and Chores:
  One Dollar Each Suffices* (2026). The additive goods-and-chores analogue of
  R2, and it subsumes this project's binary-additive special case. It does
  **not** cover the dichotomous (non-additive) class, which is why the main
  question survived it — additive and dichotomous are incomparable classes.
- **R12 — Tao, Wu, Yu, Zhou**, *On the Existence of EFX (and Pareto-Optimal)
  Allocations for Binary Chores* (2023). The direct chores analogue of R5, and
  **the paper this project's proof is built on**: its Theorem 5.1 gives a
  polynomial-time envy-free *partial* allocation leaving at most $n-1$ chores
  unassigned, with no subsidy at all. Completing that partial allocation is the
  whole of our argument.

## Problem Statement 1 — negative dichotomous valuations

R3 (Barman et al.) treats **dichotomous** valuations, where every marginal
$v(S \cup \{g\}) - v(S) \in \{0, 1\}$ — every item is a *good*.

This project asked the mirrored question: **negative dichotomous** valuations,
where $v(S) - v(S \cup \{g\}) \in \{0, 1\}$, so every item is a **chore**.

Two things fixed the target, both argued in
[`report/sections/introduction.tex`](report/sections/introduction.tex):

- **A bounded subsidy already existed.** Negative dichotomous valuations are
  doubly monotone under the two-sided normalisation, so R9's EF1 ⇒
  EF-with-subsidy reduction applies off the shelf and gives $n-1$ per agent,
  $n(n-1)/2$ total. That was the baseline to beat, not the goal.
- **The $n-1$ lower bound transfers.** With $n$ agents and $n-1$ unit chores,
  every complete allocation forces a total subsidy of $n-1$ — so the target
  bound, once proved, is tight.

The open question was exactly R3's guarantee — subsidy in $\{0,1\}$ per agent,
$n-1$ total, in polynomial time — a factor of $n$ below the R9 baseline. **That
is now proved.** It fills the remaining corner of the square:

| | goods | chores |
|---|---|---|
| additive | R2 | R11 |
| dichotomous | R3 | **this project** |

each of the four giving one dollar per agent and $n-1$ in total.

## Notation

$N = [n]$ agents; $M$ items with $|M| = m$; valuation $v_i : 2^M \to \mathbb{R}$ with
$v_i(\emptyset) = 0$; allocation $A = (A_1,\dots,A_n)$; subsidy vector
$p \in \mathbb{R}^n_+$; entitlement weights $w_i > 0$; value matrix $V^A_{ij} = v_i(A_j)$;
$V$ = max item value; $W = \sum_i w_i$.

Source papers use their own letters — divergences are flagged in the glossary §10.

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

The current graph is an AST-only build, which covers the scripts; a semantic
pass over the `.md` notes and PDFs can be added with `/graphify --update`.

## Building the report

```bash
cd report
latexmk -pdf main.tex       # the report: setup + the n = 3 proof
latexmk -pdf working.tex    # the full draft: everything, incl. general n
```

## A note on the PDFs

`References/` holds the source papers for convenience while working. Copyright rests
with the respective authors and publishers; consult the originals for citation.
