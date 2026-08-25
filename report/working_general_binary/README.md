# `working_general_binary/` — scratch area for the general-binary extension

**This is a second, independent investigation, not a continuation of the
closed chores-only proof.** See `docs/PS2_general_binary.md` for the problem
statement and `docs/RESIDUAL_GENERAL_BINARY.md` for the running research log.

## What is closed, and what this is not

`report/main.tex` proves the negative-binary (chores-only) result for every
$n$; `report/working/` holds its full 14-approach trail, compiled by
`report/working.tex`. That work is **done**. Nothing under `report/working/`,
`report/sections/`, `report/main.tex`, or `report/working.tex` is edited from
this line of work — not to fix a stale comment, not to add a cross-reference,
nothing — without the user explicitly asking to revisit the closed result.

This directory is where the **general binary** extension (every marginal in
$\set{-1,0,1}$: each item may be a good for some agents and a chore for
others) lives while it is being worked out.

## Build

```bash
cd report/working_general_binary
latexmk -pdf working_general_binary.tex
```

Shares `../preamble.tex` with the closed paper (packages, theorem
environments, notation macros), so notation never drifts between the two
investigations. Otherwise fully independent: no `\input` from `../sections/`
or `../working/`, and nothing here is `\input` by `main.tex` or
`working.tex`.

## Layout

| File | Contents |
|---|---|
| `working_general_binary.tex` | The driver. `\input`s whatever accumulates below. |
| `ideas.tex` | Dated inbox, newest at the bottom — what the idea is / why it might work / what would kill it. |

As results firm up, give each its own file here (mirroring
`report/working/approach_N.tex`'s convention) and `\input` it from
`working_general_binary.tex`.

## Reusable machinery from the closed paper

Nothing under `report/working/` is off-limits to *read* — only to edit. In
particular, `report/sections/preliminaries.tex`'s Halpern–Shah
characterisation (envy-freeability $\iff$ no positive-weight cycle in the
envy graph; the minimal subsidy is the longest outgoing path) assumes nothing
about the sign of the valuations, so it transfers verbatim to general binary
marginals and does not need to be re-derived.

## Promoting a result

Once a real result exists, decide then — not before — whether it becomes a
new section of the existing paper or a separate report:

1. If it extends `report/main.tex`: follow the same promotion path as
   `report/working/README.md` describes (move the file to `sections/`,
   wire it into `main.tex`), after checking with the user.
2. If it becomes its own paper: a full skeleton (own `main.tex`, abstract,
   `references.bib`) is scaffolded at that point, not before.

## Adding a new idea

Append a dated `\subsection*` to `ideas.tex`, newest at the bottom. A template
sits at the end of that file.
