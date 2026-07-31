# Algorithmic Game Theory — Fair Division with Subsidies

Research notes and working material on **fair division of indivisible items with
subsidies**, and an open problem on **negative dichotomous valuations** (chores).

## Contents

| File | What it is |
|---|---|
| [`glossary_fair_division_subsidies.md`](glossary_fair_division_subsidies.md) | Project glossary, v1 — every definition restated in a single fixed notation, with provenance tags back to the source readings. |
| [`paper_map_R1_to_R9.md`](paper_map_R1_to_R9.md) | One entry per paper (R1–R9): what it does, what it improves on, what it leaves open. Includes the dependency DAG and the bound tables. |
| [`Problem Statement 1.txt`](Problem%20Statement%201.txt) | The open problem being worked on. |
| [`References/`](References/) | Source papers, `Reading_1.pdf` … `Reading_9.pdf`. |

## The corpus

The readings are **not** a chronology — they form a small DAG with one trunk, three
branches, and one paper answering a different question. Publication order:

| Reading | Year | Short name | Setting |
|---|---|---|---|
| R1 | 2019 (SAGT) | Halpern–Shah | unweighted, additive, money |
| R2 | 2019/20 (EC) | Brustle et al. | unweighted, additive + monotone, money |
| R3 | 2022 | Barman et al. | unweighted, dichotomous, money |
| R5 | 2023 (FAW) | Bu–Song–Yu | unweighted, binary, *no money* |
| R9 | 2023 (AAAI'24) | Kawase et al. | unweighted, doubly monotone, money |
| R8 | 2024 (AAAI) / 2025 (SCW) | Montanari et al. | weighted, submodular, *no money* |
| R7 | 2024 | Dai et al. | weighted, house allocation, money |
| R4 | 2024 | Klein Elmalem et al. | weighted, additive, money |
| R6 | 2025 | Klein Elmalem, Aziz et al. | weighted, monotone + subclasses, money |

Envy-freeness fails for indivisible goods, and the corpus splits on the repair:

- **(A) Add money** — keep EF exact, buy off the envy with an outside subsidy $p$, and
  ask how much. → R1, R2, R3, R9 (equal entitlements); R4, R6, R7 (unequal).
- **(B) Weaken the notion** — no money; relax EF to EF1 / EFX / WEF$(x,1-x)$ / TWEF /
  WMEF and ask what still exists. → R5, R8.

See [`paper_map_R1_to_R9.md`](paper_map_R1_to_R9.md) §0 for the full structure.

## Problem Statement 1 — negative dichotomous valuations

R3 (Barman et al.) treats **dichotomous** valuations, where every marginal
$v(S \cup \{g\}) - v(S) \in \{0, 1\}$ — every item is a *good*.

This project asks the mirrored question: **negative dichotomous** valuations, where
$v(S) - v(S \cup \{g\}) \in \{0, 1\}$, so every item is a **chore**.

**Objective.** Either prove the analogues of R3's results in the chores setting, or
find a counter-example showing the transfer fails.

## Notation

$N = [n]$ agents; $M$ items with $|M| = m$; valuation $v_i : 2^M \to \mathbb{R}$ with
$v_i(\emptyset) = 0$; allocation $A = (A_1,\dots,A_n)$; subsidy vector
$p \in \mathbb{R}^n_+$; entitlement weights $w_i > 0$; value matrix $V^A_{ij} = v_i(A_j)$;
$V$ = max item value; $W = \sum_i w_i$.

Source papers use their own letters — divergences are flagged in the glossary §10.

## A note on the PDFs

`References/` holds the source papers for convenience while working. Copyright rests
with the respective authors and publishers; consult the originals for citation.
