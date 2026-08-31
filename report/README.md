# `report/` — the LaTeX write-up

**Two independent investigations share this directory.** The negative-binary
(chores-only) result below is closed. A second, open investigation — general
binary valuations, goods and chores together — lives in
[`working_general_binary/`](working_general_binary/) and does not touch
anything described here; see that directory's own `README.md`.

Paper: *Achieving Envy-Freeness with Limited Subsidies under Negative
Dichotomous Valuations*. **Proved for every $n$** — see §3 of `main.pdf`.

## Two documents, one preamble

| Build | Produces | Contains |
|---|---|---|
| `latexmk -pdf main.tex` | `main.pdf` (15 pp.) | **The report.** Introduction, notation and preliminaries, and the main theorem for every $n$. |
| `latexmk -pdf working.tex` | `working.pdf` (133 pp.) | **The full draft.** The report's sections, then the complete 14-approach trail — everything tried, proved, and refuted along the way. |

Both share `preamble.tex` and `references.bib`, so notation and citations can
never drift apart. `working.tex` includes the report's own sections first, so
every `\ref` in the parked material resolves and it stays readable in context.
Section and theorem numbers therefore differ between the two PDFs — they are
different documents, not two builds of one.

Nothing is deleted. Everything parked is under [`working/`](working/) and is
still compiled, cross-referenced and verified; see
[`working/README.md`](working/README.md) for the inventory and for how to
promote a section back into the report. **This trail is closed** — the main
theorem is proved, so nothing further gets promoted into `main.tex` for this
topic absent the user explicitly reopening it.

Without latexmk: `pdflatex main && bibtex main && pdflatex main && pdflatex main`.

## Layout

| Path | Holds |
|---|---|
| `main.tex` | The report. Title block and `\input` lines; parked/out-of-scope inputs present but commented out, with a note on why each is excluded. |
| `working.tex` | The full-draft driver: the report's sections, then all 14 parked approaches. |
| `preamble.tex` | Packages, theorem environments, notation macros, the `\ifdraft` and `\ifworking` switches. Shared with `working_general_binary/`. |
| `references.bib` | Bibliography. Header comment records which entries are verified against a PDF and which came from `../docs/map.md`. |
| `sections/abstract.tex` | Abstract. States the general-$n$ result. |
| `sections/introduction.tex` | §1 — the goods line, the chores turn, the lower bound, the target statement, related work. |
| `sections/preliminaries.tex` | §2 — notation, negative dichotomous valuations, envy graph, Halpern–Shah (sign-agnostic — reusable for the general-binary extension without re-derivation). |
| `sections/main_result.tex` | §3 of `main.tex` only — **the main theorem**, for every $n$: the terminal state of the partial-allocation algorithm, the completion, envy-freeness, and the theorem itself. |
| `sections/n3.tex` | An earlier, $n=3$-only argument. Correct, superseded by `main_result.tex`; `\input` by neither document (would restate the result twice in `main.tex`; `working.tex` gets the same content via `working/approach_13.tex`, its original, unpolished form). |
| `sections/structure.tex` | `\input` by `working.tex` only (arc-update lemma, two-tier characterisation, size-shift transform — proved, correct, not used by the final proof). Commented out of `main.tex`. |
| `sections/obstructions.tex`, `replica.tex`, `results.tex` | Proved/refuted material, `\input` by neither document currently; re-enable if useful. |
| `working/` | Parked material: the full 14-approach trail and the ideas log. Closed, not part of the report. |
| `working_general_binary/` | **A different, open investigation.** Not part of this paper. See its own `README.md`. |
| `figures/` | Figures, referenced by filename alone (`\graphicspath` is set). |

## Adding new thinking

For the closed chores topic: don't — see above. For the general-binary
extension: [`working_general_binary/ideas.tex`](working_general_binary/ideas.tex),
one dated `\subsection*` per idea, newest at the bottom, in the three-part
shape *what the idea is / why it might work / what would kill it*.

## Conventions

- **Notation** is fixed by `../docs/glossary_fair_division_subsidies.md`.
  Macros in `preamble.tex` implement it. If a symbol is missing, add it to
  the glossary first, then add the macro — do not introduce a competing
  symbol here. This file is shared by both investigations.
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
  grep -rn '\\todo{\|\\verify{' sections/ working/ working_general_binary/ main.tex working.tex
  ```
- **Style** deliberately mirrors Reading_3: Palatino body text, bold
  unpunctuated `Proof` heads, `alpha` citation labels, coloured links.
