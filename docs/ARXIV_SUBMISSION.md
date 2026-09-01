# arXiv submission — bundle, metadata, and handoff

*Prepared 2026-09-01 against the revision memo
`pre_arxiv_revision_comments.pdf`. Covers memo items 11 and 12, and records
items 7, 9 and 10, which are the guide's to do by hand.*

---

## 1. The upload bundle

`report/arxiv/` is the clean source directory. It contains exactly what
`main.tex` needs and nothing else:

```
main.tex          preamble.tex      references.bib    main.bbl
sections/abstract.tex     sections/introduction.tex
sections/preliminaries.tex  sections/main_result.tex
```

Excluded on purpose: `sections/n3.tex`, `obstructions.tex`, `replica.tex`,
`structure.tex` (parked, in no build), everything under `report/working/`, and
all build artefacts. `main.bbl` is included because arXiv does not run BibTeX.

**To regenerate** after editing `report/`:

```
cd report && rm -rf arxiv && mkdir -p arxiv/sections
cp main.tex preamble.tex references.bib main.bbl arxiv/
cp sections/{abstract,introduction,preliminaries,main_result}.tex arxiv/sections/
cd arxiv && latexmk -pdf main.tex
```

## 2. Preflight results (memo item 11)

Compiled from the clean directory on 2026-09-01:

| Check | Result |
|---|---|
| builds from clean | yes, `latexmk -pdf main.tex`, exit 0 |
| pages | **16** |
| PDF identical to `report/main.pdf` | **yes**, 249,061 bytes both |
| undefined references | **none** |
| unresolved citations | **none** |
| overfull boxes | **0** |
| floats breaking definitions | none — Definition 16 is whole on p. 11, Algorithm 1 entirely on p. 12 |
| `\todo` / `\draftnote` uses in shipped sections | none (macros defined, never used) |

**One optional tidy, deliberately not done.** The shipped sources still carry
`\ifworking … \fi` blocks — the terminology remark and the complementation
remark in `preliminaries.tex`, and the conjecture/theorem switch in
`introduction.tex`. They are suppressed in the compiled paper, since
`\workingfalse` is the default, so the PDF arXiv renders is unaffected. They
are ordinary mathematics, nothing private. Stripping them would make the public
source exactly the paper; leaving them costs nothing but tidiness. Note that
one of them refers to `\Cref{sec:approach13}`, a label that exists only in the
working draft, so anyone flipping the switch would see one undefined reference.

## 3. arXiv metadata (memo item 12)

**Primary category:** `cs.GT` (Computer Science and Game Theory).
**Suggested cross-list:** `cs.DS`.

**Title.** Achieving Envy-Freeness with Limited Subsidies under Negative
Dichotomous Valuations

**Abstract for the submission form** — shorter than the manuscript abstract,
and naming all five points the memo asks for (domain, $\{0,1\}$ per agent,
tight $n-1$ total, polynomial time, EF1):

> We study envy-free allocation of indivisible chores with subsidies. An
> instance is negative dichotomous if every agent's marginal disutility for a
> chore is either zero or one, with no further assumption: not additivity, not
> submodularity, and no relation between different agents' cost functions. This
> is the exact mirror of the dichotomous goods model of Barman, Krishna,
> Narahari and Sadhukhan, who show that a subsidy of 0 or 1 per agent always
> suffices there.
>
> We prove the same guarantee for chores, for every number of agents: every
> negative dichotomous instance admits a complete allocation together with a
> subsidy vector p in {0,1}^n, hence a total subsidy of at most n-1, under which
> no agent envies any other. The bound is tight. The allocation is computable in
> polynomial time in the value-oracle model and is moreover EF1 before any
> subsidy is paid, so the money is precisely what upgrades EF1 to exact
> envy-freeness. The proof completes an envy-free partial allocation produced by
> the algorithm of Tao, Wu, Yu and Zhou, assigning the residual chores to
> distinct agents inside the strongly connected component at which that
> algorithm halts.

---

## 4. Items 7 and 9 — now done (2026-09-01)

### Item 9 — title-page contact

Filled with the address the user supplied:

```latex
\author[1]{Mainak Sarkar\footnote{Contact: mainaks23@iitk.ac.in}}
```

Same institutional affiliation as Soumyarup (`\affil[1]{Indian Institute of
Technology Kanpur}`, already shared). Verified in the rendered PDF, page 1.

### Item 7 — bibliographic entries

Applied to `report/references.bib`. All four are additions/replacements of
metadata only — no key was renamed, so every `\cite{...}` in the manuscript
still resolves without any other edit.

| Key | Was | Now |
|---|---|---|
| `TWYZ23` | `@misc`, arXiv 2308.12177, with a note | `@article`, *Theoretical Computer Science* **1042**, article 115248, 2025; arXiv id kept as a note |
| `KMSTY24` | `@inproceedings`, AAAI 2024 | `@article`, *Artificial Intelligence* **348**, article 104406, 2025; AAAI + arXiv kept as a note |
| `BKNS22` | `@misc`, arXiv 2201.07419 | `@inproceedings`, IJCAI 2022, pages **60–66**; arXiv id kept as a note |
| `BSY23` | `@inproceedings`, FAW 2023, no volume | IJTCS-FAW 2023, *LNCS* **13933**, pages 252–262, Springer |
| `LMS26` | arXiv 2607.10089 | unchanged, already correct |

The TWYZ, BKNS and BSY details were read off the reference lists of
arXiv 2607.10089 and arXiv 2608.10572; the Kawase figures are the memo's.

**One side effect worth knowing about, not an error.** The `alpha` bibliography
style derives its bracketed label from the entry's actual year, so updating the
year field changed the *visible* citation label even though the BibTeX key
(hence every `\cite{TWYZ23}` etc. in the source) did not change:
`[TWYZ23]` → **`[TWYZ25]`**, `[KMS+24]` → **`[KMS+25]`**. This is correct
behaviour — the label now reflects the true publication year — and was checked
against the full reference list for collisions: none found, all labels
distinct.

Rebuilt and verified: `main.pdf` 16 pp., `working.pdf` 133 pp., both clean, no
undefined references or citations, zero overfull boxes. The `report/arxiv/`
bundle was regenerated to match (§1–2 above); its own `main.pdf` is now kept in
the repo rather than deleted by the preflight cleanup, so it doesn't disappear
again.

## 5. Item 10 — upload-day literature sweep

Run on the day of upload, not before. What was already cleared on 2026-09-01:

- **arXiv 2607.10089** (Lu, Mackenzie, Suzuki) — one dollar each for mixed
  goods and chores, **additive** only; their §6 poses the non-additive case as
  open. Does not overlap.
- **arXiv 2608.10572** (Lin, Liu, Tao, Zhou) — EFX non-existence for binary XOS
  and binary supermodular chores. Now cited (memo item 6).
- **arXiv 2608.06325** (Cookson, Shah, Verma) — balanced EF1 + fPO, additive
  goods, **no money**. Adjacent, not overlapping.

Search terms that surfaced these: *subsidy dichotomous chores envy-free*,
*binary marginals chores EFX*, *one dollar each goods and chores*. The thing to
watch for is any new paper claiming a per-agent subsidy bound for
**non-additive** chores with binary marginals.

---

## 6. Memo items — status

All twelve items are now closed.

| Item | Where |
|---|---|
| 1 formal EF1 definition | `preliminaries.tex`, `def:ef1chores` (Definition 6) |
| 2 EF1 to abstract / headline theorem / Our contribution; abstract typo | `abstract.tex`, `introduction.tex` |
| 3 `r = 0` branch covers EF1 | `main_result.tex`, the guide's own sentence |
| 4 corrected lower bound kept | `introduction.tex`, Example 1 |
| 5 Algorithm 1 no longer splits Definition 16 | `float` package, `[H]` |
| 6 Lin et al. in Related Work | `introduction.tex`, `LLTZ26` |
| 7 bibliographic entries updated | §4 above, 2026-09-01 |
| 8 Algorithm 3 supplies the terminal state | `main_result.tex`, proof of Theorem 20 |
| 9 title-page contact filled | §4 above, 2026-09-01 |
| 10 upload-day literature sweep | §5 above — **run again on the actual upload day**, this is not a substitute |
| 11 preflight | §2 above |
| 12 metadata | §3 above |
