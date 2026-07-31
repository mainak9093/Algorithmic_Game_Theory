# `report/` — the LaTeX write-up

Working paper: *Achieving Envy-Freeness with Limited Subsidies under Negative
Dichotomous Valuations*.

## Build

```bash
latexmk -pdf main.tex          # preferred
latexmk -c                     # clean aux files, keep the PDF
```

or, without latexmk:

```bash
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

Two BibTeX passes are needed because the bibliography is `alpha`-styled and the
cross-references are resolved by `cleveref`.

## Layout

| Path | Holds |
|---|---|
| `main.tex` | Structure only — title block and `\input` lines. No prose, no packages. |
| `preamble.tex` | Packages, theorem environments, notation macros. |
| `references.bib` | Bibliography. Header comment records which entries are verified against a PDF and which came from `paper_map_R1_to_R9.md`. |
| `sections/abstract.tex` | Abstract. |
| `sections/introduction.tex` | §1 — setting, the goods line, the chores turn, the lower bound, related work. |
| `sections/preliminaries.tex` | §2 — notation, negative dichotomous valuations, envy graph, Halpern–Shah. |
| `sections/results.tex` | §3 — **intentionally empty** until an approach produces a theorem. |
| `sections/approach_1.tex` | §4 — template for an approach. |
| `sections/conclusion.tex` | Closing section, stub. |
| `figures/` | Figures, referenced by filename alone (`\graphicspath` is set). |

## Adding an approach

One approach = one file = one section.

1. `cp sections/approach_1.tex sections/approach_2.tex`
2. Add `\input{sections/approach_2}` to `main.tex` (a commented line is already
   waiting there).
3. State the results in `sections/results.tex`; keep the proofs in the approach
   section that produced them. This is R3's split — its Theorem 4 is stated in
   §3 and proved in §4.

A failed approach stays in the paper. Record where it breaks rather than
deleting the file; a located obstruction is a result.

## Conventions

- **Notation** is fixed by `../glossary_fair_division_subsidies.md`. Macros in
  `preamble.tex` implement it. If a symbol is missing, add it to the glossary
  first, then add the macro — do not introduce a competing symbol here.
- **Theorem numbering** runs a single counter across
  Definition/Theorem/Lemma/Proposition/Observation, as in R3. `claim` has its
  own counter.
- **Draft notes.** `\todo{...}` and `\verify{...}` render in orange. Set
  `\draftfalse` in `preamble.tex` to compile a clean copy — nothing else
  changes. Every open question in the current draft is marked with one of these,
  so grepping for them lists the outstanding work:
  ```bash
  grep -rn '\\todo{\|\\verify{' sections/ main.tex
  ```
- **Style** deliberately mirrors Reading_3: Palatino body text, bold
  unpunctuated `Proof` heads, `alpha` citation labels, coloured links.
