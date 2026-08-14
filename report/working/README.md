# `working/` — parked material

**Nothing here is deleted, stale, or unverified.** Every result in this
directory is proved and machine-checked against the scripts in
[`../../updates/update_1/`](../../updates/update_1/). It is parked only because the report is
deliberately short right now: it sets up the problem and stops.

## Two documents

| Build | Contains | Pages |
|---|---|---|
| `latexmk -pdf ../main.tex` | **The report.** Introduction, notation and preliminaries, structure of the problem. | 11 |
| `latexmk -pdf ../working.tex` | **The full draft.** The report's sections, then everything below. | 21 |

`working.tex` includes the report's own sections first, so every `\ref`
resolves and the parked material stays readable in context. Section and theorem
numbers differ between the two PDFs — they are different documents, not two
builds of one.

## What is parked

| File | Contents | Status |
|---|---|---|
| `results.tex` | Overview; Conjecture 2 (utilitarian-optimal strengthening) | Conjecture 2 **refuted** |
| `solved_cases.tex` | Binary additive costs; identical costs; $n=2$ | Proved, tight |
| `approach_1.tex` | Item-by-item insertion: free-insertion theorem, cycle-closing bound, **and the obstruction killing the template** | Proved |
| `approach_2.tex` | Utilitarian-optimal selection, **refuted**; failed tie-break rules | Proved |
| `approach_3.tex` | Replica transform, coverage reduction, the peel process, dead ends, the type-ordered restriction | **Open — the live approach.** Less polished than the rest. |
| `approach_4.tex` | Encoding coverage into the numbers, at valuation and algorithm level | **Both closed.** Proved + machine-verified. |
| `experiments.tex` | Evidence table, the sampler-bias analysis, the peel-frame search plan, reproduction | Current |
| `ideas.tex` | **Running log of new thinking.** Newest entry last. | Inbox |
| `conclusion.tex` | Open directions ranked | Current |

The two results worth not re-deriving:

- **The insertion template is dead.** A three-agent instance where every choice
  of receiving agent forces a subsidy of 2, though the full instance solves with
  0. Any correct proof must re-open already-allocated bundles.
  (`approach_1.tex`, verified by `updates/update_1/deadend.py`.)
- **Utilitarian optimality is the wrong restriction.** A three-agent, four-chore
  instance whose *unique* cost-minimising allocation needs subsidy 2 while a
  costlier one needs 0. A correct algorithm must be free to give up total cost.
  (`approach_2.tex`, verified by `updates/update_1/mswcex.py`.)

- **No refinement of the utilitarian-optimal set can work.** The point above is
  not just about tie-breaking: on that instance the optimal set is a *singleton*,
  so any rule selecting inside it returns the bad allocation. This kills the
  cardinality-balance-then-cost-leximin refinement despite ~1050 clean random
  trials. (`approach_2.tex`, verified by `updates/update_4/checkD.py`.)
- **Coverage cannot be encoded into the numbers.** No dichotomous reweighting of
  the replica instance separates coverage from non-coverage — exhaustive over all
  $990^3$ triples — and no weight inflation can steer R3's algorithm, because its
  repair subroutine runs exactly where every candidate's marginal is 0 and a
  duplicate moves no arc. (`approach_4.tex`, verified by `updates/update_4/dupsep.py`.)

All four negative results share one shape: **a rule fixed ex ante against a
quantity determined ex post.** What survives is procedures that decide late.

And the one worth building on:

- **The replica transform.** A chore instance is a goods instance on $n-1$ copies
  of each chore, with an *identical* envy graph, so the whole conjecture reduces
  to one constraint: no agent may be relieved of the same chore twice. Read
  dynamically this defers every ownership decision to the last move touching a
  chore, which is exactly what the two negative results demand. Not known to
  work — the state space has dead ends, and the reduction is sufficient but not
  known to be complete. (`approach_3.tex`, verified by `updates/update_2/peel3.py`.)

**Pending:** the terms introduced in `approach_3.tex` — replica instance, type
map, coverage allocation, peel process, workload profile, owner-candidate set,
survivor, spectator-free peel, conditioned-remainder principle, deadlock — are
flagged for promotion into `../../docs/glossary_fair_division_subsidies.md`, which has
not been updated. Do that before this notation leaves `working/`.

## Adding a new idea

Append a dated `\subsection*` to `ideas.tex`, newest at the bottom. Keep the
three-part shape: what the idea is, why it might work, what would kill it. A
template is at the end of that file. Ideas graduate to their own file under
`working/` once they are proved.

## Promoting a section into the report

1. `git mv working/<file>.tex sections/<file>.tex`
2. Uncomment its `\input` line in `main.tex` (the lines are already there,
   commented, in the intended order).
3. Delete the corresponding `\input` from `working.tex` — it will now come in
   with the report's own sections.
4. Update the abstract to lead with the result, and the *Scope of this report*
   paragraph in `sections/introduction.tex`.

## The `\ifworking` switch

A few sentences in `sections/structure.tex` point at parked material. They are
wrapped in `\ifworking ... \fi`, so they appear in `working.pdf`, where their
targets exist, and vanish from `main.pdf`, where they would dangle. `main.tex`
leaves the default `\workingfalse`; `working.tex` sets `\workingtrue`.

Never put a `\label` inside such a guard — it would exist in one document and
not the other. If you add a report sentence that references parked material,
guard it the same way, and give the `\else` branch a version that stands alone.
