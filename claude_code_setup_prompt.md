# Claude Code Setup Prompt — Algorithmic Game Theory Project

Copy everything below the line into Claude Code (VS Code, Opus Max) as your first message
in the project root (`D:\Desktop\Coding\Projects\Algorithmic_Game_Theory`).

---

## PROJECT CONTEXT

You are setting up long-term bookkeeping for a research project in algorithmic game theory,
specifically **fair division of indivisible goods with subsidies**. This is ongoing work
toward a paper for professor review, built on a corpus of 9 reference papers (R1–R9) that
have already been read and distilled into two canonical reference documents.

**Field background:** In fair division, an *envy-free* allocation of indivisible goods may
not exist (trivial counterexample: two agents, one good). One remedy is to add *subsidies*
— a divisible good (money) supplied by an external party — so that each agent's bundle
value plus subsidy is at least her value for anyone else's bundle plus their subsidy. The
corpus studies how much subsidy is needed under various valuation classes (additive,
submodular, matroidal, dichotomous, weighted/entitlement settings, etc.), and the trade-offs
between total subsidy, per-agent subsidy, and computational tractability in the value-oracle
model.

**Current problem statement (Problem Statement 1):** Reading_3 (R3, Barman–Krishna–Narahari–
Sadhukhan, "Achieving Envy-Freeness with Limited Subsidies under Dichotomous Valuations")
proves that under *dichotomous valuations* (marginal value of any good is always 0 or 1),
there is an envy-free allocation with per-agent subsidy in {0,1}, computable in poly time.
We are now extending this to **negative dichotomous valuations** — i.e., every item is a
*chore* instead of a good, with marginal value $v(S) - v(S \cup \{g\}) \in \{0,1\}$ (note the
sign flip relative to R3). The objective is to prove an analogous result for this chores
setting, or find a counterexample showing the R3-style guarantee does not carry over.

**Canonical reference documents (do not restate their contents in chat — read them
directly and keep them updated):**
- `glossary_fair_division_subsidies.md` — all notation conventions, term definitions,
  cross-paper symbol conflicts (e.g., R9 uses $w$ for a weight matrix, others for
  entitlements — project convention is fixed here).
- `paper_map_R1_to_R9.md` — per-paper summaries, the lineage/subsumption relationships
  between papers (e.g., R4 is subsumed by R6), bound tables, and open-gap analysis.

These two files are the single source of truth for terminology and prior results. New
terms and new paper summaries should be appended to them, not duplicated elsewhere.

---

## WHAT I NEED YOU TO DO

### 1. Set up the folder structure

I already have `References\` with the source PDFs (R1–R9). Build out the rest of the
project directory like this:

```
Algorithmic_Game_Theory\
├── References\                    (existing — PDFs R1-R9, do not touch)
├── Glossary\
│   └── glossary_fair_division_subsidies.md
├── Paper_Map\
│   └── paper_map_R1_to_R9.md
├── Problem_Statements\
│   └── PS1_negative_dichotomous_valuations.md
├── Notes_and_Findings\
│   ├── YYYY-MM-DD_<short-topic>.md      (one file per work session/idea)
│   └── open_questions.md                 (running list, updated not rewritten)
├── Proofs_and_Derivations\
│   └── (scratch work, lemma attempts, counterexample constructions — markdown or .tex)
├── Code\
│   ├── experiments\                      (verification scripts, small instance search, etc.)
│   └── README.md                         (what each script does and how to run it)
├── LaTeX\
│   ├── main.tex
│   ├── sections\
│   ├── references.bib
│   └── figures\
├── CLAUDE.md                             (persistent project instructions — see below)
└── .gitignore
```

Move/copy the glossary and paper map content I'll paste in (or that already exists in
this chat's project knowledge) into the `Glossary\` and `Paper_Map\` files respectively,
and the problem statement into `Problem_Statements\`.

### 2. Create a `CLAUDE.md` at the project root

This is the persistent memory file Claude Code reads at the start of every session. It
should contain:
- A condensed version of the project context above (2–3 paragraphs).
- The rule: **glossary and paper map are canonical — always check them before introducing
  new notation or re-summarizing a paper; append to them, don't fork new copies.**
- The current active problem statement, with a pointer to its file, and a note to update
  `Problem_Statements\` (not overwrite) if the problem evolves.
- Folder-purpose table (one line per folder, matching the structure above).
- Git conventions (see below).
- Notation conventions pulled from the glossary's "Project notation" section, so they're
  visible without opening a second file.

### 3. Git bookkeeping

Initialize git if not already done. For every commit:
- **Never add "Claude" or "Opus" (or any AI) as a co-author or in the commit trailer.**
  Do not include `Co-authored-by` lines referencing Claude/Anthropic in any commit.
- Use plain, descriptive commit messages (what changed and why), no attribution footers.
- Commit the folder scaffold first, then each subsequent piece of work as its own commit.

### 4. LaTeX skeleton for professor review

Set up `LaTeX\main.tex` with a standard research-note structure: title, abstract, notation
section (pulling from the glossary conventions), problem statement section (current: PS1),
related work section (summarizing R1–R9 lineage from the paper map, citing appropriately),
a results section with theorem/lemma/proof environments left as placeholders, and a
references.bib stub with entries for R1–R9 (use the actual paper titles/authors from the
References folder — extract them from the PDFs if bibliographic info isn't already in the
paper map). Use a clean, standard math article class (amsart or similar) with amsthm.

### 5. Ongoing workflow going forward

Once the scaffold exists, my typical use going forward will be:
- I'll describe an idea, a lemma attempt, or a partial proof in chat.
- You append it to the right dated file in `Notes_and_Findings\` (or
  `Proofs_and_Derivations\` if it's a formal attempt), rather than creating a new file
  each time unless it's a genuinely new topic.
- When something is solid enough for the writeup, you migrate it into the appropriate
  `LaTeX\sections\` file and note in `Notes_and_Findings\` that it's been promoted.
- If a new paper (R10, R11, ...) gets added to References, extend the paper map and
  glossary rather than starting new documents.
- Any code (e.g., small-instance search for counterexamples, verifying a bound
  computationally) goes in `Code\experiments\` with a short README note. Any actual
  machine learning / deep learning model training should be assumed to run on GPU, not
  on my local CPU — flag it if a task would need that so I can move it to a GPU
  environment rather than running it locally.

Please start by creating the full folder structure and `CLAUDE.md`, then show me the
`CLAUDE.md` content for review before committing.
