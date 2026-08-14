# `report/` — the LaTeX write-up

Working paper: *Achieving Envy-Freeness with Limited Subsidies under Negative
Dichotomous Valuations*.

## Two documents, one preamble

| Build | Produces | Contains |
|---|---|---|
| `latexmk -pdf main.tex` | `main.pdf` (11 pp.) | **The report.** Introduction, notation and preliminaries, structure of the problem. Deliberately stops there. |
| `latexmk -pdf working.tex` | `working.pdf` (22 pp.) | **The full draft.** The report's sections, then everything proved so far but not yet report-worthy. |

Both share `preamble.tex` and `references.bib`, so notation and citations can
never drift apart. `working.tex` includes the report's own sections first, so
every `\ref` in the parked material resolves and it stays readable in context.
Section and theorem numbers therefore differ between the two PDFs — they are
different documents, not two builds of one.

Nothing is deleted. Everything parked is under [`working/`](working/) and is
still compiled, cross-referenced and verified; see
[`working/README.md`](working/README.md) for the inventory and for how to
promote a section back into the report.

Without latexmk: `pdflatex main && bibtex main && pdflatex main && pdflatex main`.

## Layout

| Path | Holds |
|---|---|
| `main.tex` | The report. Structure only — title block and `\input` lines, with the parked inputs present but commented out in their intended order. |
| `working.tex` | The full-draft driver. |
| `preamble.tex` | Packages, theorem environments, notation macros, the `\ifdraft` and `\ifworking` switches. |
| `references.bib` | Bibliography. Header comment records which entries are verified against a PDF and which came from `../docs/map.md`. |
| `sections/abstract.tex` | Abstract. Scoped to what the report currently carries. |
| `sections/introduction.tex` | §1 — the goods line, the chores turn, the lower bound, **Conjecture 2** (the target), scope, related work. |
| `sections/preliminaries.tex` | §2 — notation, negative dichotomous valuations, envy graph, Halpern–Shah. |
| `sections/structure.tex` | §3 — arc-update lemma, two-tier characterisation, size-shift transform. |
| `working/` | Parked material and the ideas log. Not part of the report. |
| `figures/` | Figures, referenced by filename alone (`\graphicspath` is set). |

## Adding new thinking

New ideas go in [`working/ideas.tex`](working/ideas.tex) — one dated
`\subsection*` per idea, newest at the bottom, in the three-part shape *what the
idea is / why it might work / what would kill it*. A template sits at the end of
that file. Ideas graduate to their own file under `working/` once proved, and
from there into `sections/` once worth reporting.

## Conventions

- **Notation** is fixed by `../glossary_fair_division_subsidies.md`. Macros in
  `preamble.tex` implement it. If a symbol is missing, add it to the glossary
  first, then add the macro — do not introduce a competing symbol here.
- **Theorem numbering** runs a single counter across
  Definition/Theorem/Lemma/Proposition/Observation, as in R3. `claim` has its
  own counter.
- **`\Cref` is unsafe for theorem-like environments** — they share one counter,
  so cleveref calls every one of them "Theorem". Write `Example~\ref{...}`,
  `Remark~\ref{...}` and so on explicitly, which is also what R3 does. `\Cref`
  is fine for sections.
- **`\ifworking`** guards report sentences that point at parked material, so
  they appear in `working.pdf` and vanish from `main.pdf`. Never put a `\label`
  inside such a guard.
- **Draft notes.** `\todo{...}` and `\verify{...}` render in orange. Set
  `\draftfalse` in `preamble.tex` for a clean copy. Grep for the outstanding
  work:
  ```bash
  grep -rn '\\todo{\|\\verify{' sections/ working/ main.tex working.tex
  ```
- **Style** deliberately mirrors Reading_3: Palatino body text, bold
  unpunctuated `Proof` heads, `alpha` citation labels, coloured links.
