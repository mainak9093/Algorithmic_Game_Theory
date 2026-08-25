# `working/` — the closed chores-only trail

**This directory is closed.** The theorem it was working toward is proved —
`report/main.tex` §3 (`report/sections/main_result.tex`) — for every $n$.
Nothing here is stale or wrong; every result below is proved and
machine-checked exactly as claimed. It stays exactly as it is: a complete
record of how the proof was actually found, including the 11 routes that
didn't close it before the 12th–13th did.

**Starting new work?** This is the wrong directory. A second, independent
investigation — general binary valuations (goods and chores together) — has
its own scratch area at [`../working_general_binary/`](../working_general_binary/),
its own research log (`docs/RESIDUAL_GENERAL_BINARY.md`), and its own
`updates_general_binary/` scripts folder, precisely so it never gets mixed
into this one.

## Two documents

| Build | Contains | Pages |
|---|---|---|
| `latexmk -pdf ../main.tex` | **The report.** Introduction, notation and preliminaries, the main theorem for every $n$. | 14 |
| `latexmk -pdf ../working.tex` | **The full draft.** The report's sections (via `structure.tex`, not `main_result.tex` — see below), then everything parked here. | 132 |

`working.tex` does **not** currently share `sections/main_result.tex` with
`main.tex`; it shares `sections/structure.tex` instead and carries the same
result via `approach_13.tex` below, in its original unpolished form. Section
and theorem numbers differ between the two PDFs — they are different
documents, not two builds of one.

## What is parked

Every file, in the order the investigation actually happened, with its own
final status. "Superseded" means the theorem itself is now proved by a later,
different route (`approach_12`/`13`) — it does not mean the file's own
internal claims were wrong; they stand as proved on their own terms.

| File | Contents | Status |
|---|---|---|
| `results.tex` | Overview; a utilitarian-optimal strengthening | **Refuted** |
| `solved_cases.tex` | Binary additive costs; identical costs; $n=2$ | Proved, tight |
| `approach_1.tex` | Item-by-item insertion: free-insertion theorem, cycle-closing bound, **and the obstruction killing the template** | **Refuted** (the template), rest proved |
| `approach_2.tex` | Utilitarian-optimal selection | **Refuted**; failed tie-break rules |
| `approach_3.tex` | Replica transform, coverage reduction, the peel process, dead ends | **Superseded** |
| `approach_4.tex` | Encoding coverage into the numbers, at valuation and algorithm level | **Refuted**, both levels; proved + machine-verified |
| `approach_5.tex` | Agent induction and the balance invariant | **Refuted** (the invariant); technique itself not otherwise pursued |
| `approach_6.tex` | Pure goods reformulation (size-shift), construct-and-repair | **Superseded** — proved for $n=2$, was the best lead before approach 11 |
| `approach_7.tex` | Descent on a lexicographic potential | **Superseded** — the reduction is proved, its key input never closed |
| `approach_8.tex` | The global route (leximax, tie-break chains, the balance lemma) | **Superseded** — several refuted, the balance lemma left open |
| `approach_9.tex` | The conditioned-remainder induction | **Superseded** — one sub-conjecture refuted, the rest left open |
| `approach_10.tex` | Minimum-spread families | **Superseded** — was "the best lead" before approach 11 arrived |
| `approach_11.tex` | Partial allocation + permuted extension — the **first** route to $n=3$ | **Superseded** — its saturation lemma was later found false; see `approach_12.tex` |
| `approach_12.tex` | A complete, self-contained proof of the theorem at $n=3$ | **Proved** — superseded only in scope by `approach_13.tex` |
| `approach_13.tex` | **Unit subsidies for an arbitrary number of agents — the main result** | **Proved.** Promoted to `sections/main_result.tex` |
| `approach_14.tex` | Almost-balanced size-shift, a proposed alternative route | **Closed, negative** — the reduction is correct, the specific proof program is refuted |
| `experiments.tex` | Evidence table, sampler-bias analysis, reproduction | Historical |
| `ideas.tex` | Status register of every thread this investigation raised | Closed, complete record |
| `conclusion.tex` | Open directions ranked | Superseded by the closure |

The two negative results worth not re-deriving if this topic is ever revisited:

- **The insertion template is dead.** A three-agent instance where every
  choice of receiving agent forces a subsidy of 2, though the full instance
  solves with 0. Any correct proof must re-open already-allocated bundles.
  (`approach_1.tex`, verified by `updates/update_1/deadend.py`.)
- **Utilitarian optimality is the wrong restriction**, and no refinement of it
  can work either — on the witness instance the utilitarian-optimal set is a
  *singleton*. (`approach_2.tex`, verified by `updates/update_1/mswcex.py`,
  `updates/update_4/checkD.py`.)

## What actually closed it

`approach_12.tex` and `approach_13.tex`, via a route external to everything
above: Tao–Wu–Yu–Zhou's polynomial-time envy-free *partial* allocation
(leaving at most $n-1$ items unassigned, no subsidy needed at all), completed
by placing the residual items and reassigning which agent receives which
bundle. Full derivation: `docs/RESIDUAL.md` §7.16.32–39.

## The `\ifworking` switch

A few sentences in `sections/structure.tex` point at parked material. They are
wrapped in `\ifworking ... \fi`, so they appear in `working.pdf`, where their
targets exist, and vanish from `main.pdf`, where they would dangle. `main.tex`
leaves the default `\workingfalse`; `working.tex` sets `\workingtrue`.

Never put a `\label` inside such a guard — it would exist in one document and
not the other. If you add a report sentence that references parked material,
guard it the same way, and give the `\else` branch a version that stands alone.
