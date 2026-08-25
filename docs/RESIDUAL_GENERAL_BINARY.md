# General binary valuations (goods and chores) — running research log

*Started 2026-08-24. Sibling log to `RESIDUAL.md`, which is now closed — see
its banner. This file follows the same conventions: one running document,
numbered subsections, a status table maintained at the end as sections are
added. Nothing here is deleted, only superseded, exactly as in `RESIDUAL.md`.*

---

## 0. Context

The negative-binary (chores) problem is closed: for every $n$, every instance
with marginals in $\set{0,-1}$ admits an envy-free allocation with subsidy
$\subsidy \in \set{0,1}^n$, $\sum_i \subsidy_i \le n-1$, in polynomial time.
Proof: `report/main.tex` §3 (`report/sections/main_result.tex`); full
derivation trail: `RESIDUAL.md` §7.16.35–39 (`report/working/approach_13.tex`).

This log tracks the natural generalization: **general binary** valuations,
where every marginal lies in $\set{-1,0,1}$ rather than only $\set{0,-1}$ —
each item may be a good for some agents and a chore for others (a *mixed
manna* dichotomous model). See `docs/PS2_general_binary.md` for the problem
statement.

## 1. What transfers from the closed result without re-proof

- **Halpern–Shah** (`sections/preliminaries.tex`, Theorem `thm:hs-characterisation`
  / `thm:hs-minsubsidy`): envy-freeability $\iff$ no positive-weight cycle in
  the envy graph, and the minimal subsidy is the longest outgoing path. The
  proof of both facts uses only arc weights and permutations of bundles —
  nothing about the sign or structure of the valuations — so it applies
  verbatim here. **Do not re-derive.**
- **Integrality** (`obs:integrality`): every arc weight is an integer whenever
  every marginal is an integer, which holds here too ($\set{-1,0,1} \subset
  \Z$). The minimal subsidy is therefore still integral, so "$\subsidy \le 1$"
  is again the same statement as "$\subsidy \in \set{0,1}^n$."
- **The chores-only result itself** is a special case (every marginal
  restricted to $\set{0,-1}$) and is available as a known, proved lemma —
  useful wherever an argument can localize to the chore-only part of an
  instance.

## 2. What does *not* transfer, and must be re-derived

- The completion argument of `sections/main_result.tex` (Tao–Wu–Yu–Zhou's
  partial-allocation algorithm and its terminal-state lemma) is stated for
  chores specifically (dichotomous *cost* functions, marginals in
  $\set{0,1}$ after negation). Whether an analogous partial-allocation
  algorithm exists for mixed marginals is open and is the first thing to
  check against the literature (`docs/map.md`) before assuming it.
- The literature corpus (`docs/map.md`) already contains one goods-and-chores
  result — R11 (Lu–Mackenzie–Suzuki, 2026) — but for the *additive* class, not
  dichotomous. Dichotomous and additive are incomparable classes (this is
  exactly why R3 was not a corollary of R2, and why the chores result was not
  a corollary of R11); R11 does not settle this question, and its machinery
  (iterated matchings, telescoping over rounds) is additivity-specific.

## 3. Status table

| Claim | Status |
|---|---|
| — | *(empty — first entry goes here)* |

---

*Scripts for this investigation go in `updates_general_binary/`, one
session folder per entry above, mirroring `updates/update_N/`'s relationship
to `RESIDUAL.md`.*
