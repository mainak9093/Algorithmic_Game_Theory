## Project state — two independent investigations

**1. CLOSED — negative binary valuations (chores).** Proved for every $n$: an
envy-free allocation with subsidy $p \in \{0,1\}^n$, $\sum_i p_i \le n-1$,
polynomial time, no assumption beyond binary marginals.

- Report: `report/main.tex` → `main.pdf` (14 pp.), §3 = the theorem
  (`report/sections/main_result.tex`).
- Full trail: `report/working.tex` → `working.pdf` (132 pp.), 14 approaches.
- Research log: `docs/RESIDUAL.md` (frozen — see its banner).
- Do not edit `report/sections/`, `report/main.tex`, `report/working.tex`,
  `report/working/*.tex`, or append to `docs/RESIDUAL.md` for this topic
  unless the user explicitly asks to revisit the closed result.

**2. OPEN — general binary valuations (goods and chores).** Just starting.
Every marginal in $\{-1,0,1\}$, not just $\{0,-1\}$.

- Problem statement: `docs/PS2_general_binary.md`.
- Scratch draft: `report/working_general_binary/` → its own PDF, independent
  of `main.tex`/`working.tex`.
- Research log: `docs/RESIDUAL_GENERAL_BINARY.md`.
- Scripts: `updates_general_binary/` (mirrors `updates/update_N/`'s
  per-session convention; created on first use).

**Shared and reusable by both** (topic-agnostic; extend in place, don't fork):
`docs/glossary_fair_division_subsidies.md`, `docs/map.md` (paper corpus, R1–R12),
`report/preamble.tex`, and `report/sections/preliminaries.tex`'s
Halpern–Shah characterisation, which assumes nothing about the sign of the
valuations and so transfers to topic 2 without re-derivation.

`updates/update_1/` … `update_49/` and `report/working/approach_1.tex` …
`approach_14.tex` belong to topic 1 only.

**When in doubt which investigation a request belongs to, ask rather than
guess.**

---

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
