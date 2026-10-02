# Approach 21 — the two-sided equality graph, and a route to doubly monotone

*2026-10-03. Question (Mainak): can the objective signed dichotomous case be
solved the way the chores case was — an envy-free partial allocation and its
equality graph, chores to **tail** SCCs (Tao–Wu–Yu–Zhou), goods to **source**
SCCs, then a one-shot completion with unit subsidies — and does that say
anything about doubly monotone valuations? Scripts:
`updates_general_binary/update_3/`; every number below is in `update_3/logs/`.*

---

## 0. Verdict

| | Status |
|---|---|
| The literal mirror (goods to a source SCC, one each, every member valuing its good at $+1$) | **does not mirror**: halts with up to $n+1$ leftover goods; one-shot completion fails 16 times in 2,040 non-trivial halts (§2) |
| Why: a chore's harm falls on its holder uniformly; a good's harm falls on onlookers by agent-dependent amounts | explained (§3) |
| **Goods completion lemma**: any envy-free partial allocation whose leftover goods go to distinct agents each valuing theirs at $+1$ completes with unit subsidies, by backward closure, no SCC needed | **proved** (§4), machine-checked on 27,934 assignments |
| Maximal version: extend while any envy-free extension exists, then complete | **0 failures** in 824 non-trivial halts (8,100 instances), and a hill-climbing adversary found none (§5) |
| **Reduction**: (C1) leftovers at a maximal state are single-signed, and (C2) leftover goods are matchable $\Rightarrow$ unit subsidies for **doubly monotone** dichotomous valuations | **proved**, conditional on (C1), (C2) (§6) |
| **Eligible insertion** (INS-E): a doubly monotone item can always be inserted with an eligible holder, keeping $\subsidy\in\set{0,1}^n$ | **0 failures in 426,827 states**; BKNS's proof covers part of it, data for the rest (§7) |
| Mainak's SCC-migration notes | §2–§5 confirmed (one correction), §6 has a gap (§8) |

Both (C1)+(C2) and (INS-E) would each settle doubly monotone dichotomous
valuations. Neither is proved yet.

---

## 1. The rules, and why they keep envy-freeness

State: an envy-free partial allocation $X$ (no subsidy), equality arcs
$k\to j$ iff $v_k(X_k)=v_k(X_j)$.

- **F (free insertion).** Item $e$ to agent $i$ when $v_i(e\mid X_i)\ge 0$
  and every $k$ with $k\to i$ has $v_k(e\mid X_i)\le 0$. *Keeps EF:* $i$ does
  not drop; tied onlookers do not rise; untied onlookers have slack $\ge 1$
  and rise by $\le 1$.
- **ROT (free after rotation).** Some $k\to j$ on a cycle of $E$: rotate so
  $k$ holds $X_j$ (no value changes), then F with holder $k$; the agents tied
  to $X_j$ afterwards are $j$ and its old in-neighbours.
- **TAIL.** Tao's R3, unchanged.
- **SRC.** A source SCC $S$; each member a distinct leftover good worth
  exactly $+1$ to it. *Keeps EF:* members rise by 1 and see others rise by
  $\le 1$; outsiders are untied to $S$ (source) so have slack.

F and ROT are **sign-agnostic**: for a chore they are Tao's R1 and R2, for a
good "nobody tied to the holder gains". Only TAIL and SRC look at signs.

## 2. The literal mirror (Experiment 1, `run_objective.py`)

14,000 objective instances ($n=3,4$; $m=5$–$7$; random and additive):
11,960 finish with **every item placed and no subsidy**; 2,040 halt with
leftovers. The symmetric completion (chores to distinct members of the halting
tail SCC, goods to distinct agents valuing them at $+1$) works in 2,024 and
fails in 16 — 7 "unmatchable", 9 needing a subsidy of 2. **No halting state
was dead**: every one had some unit completion, never needing a reassignment.

The failures (`diagnose_ksym.py`) have two causes:

1. *SRC is too strict.* Trial 497 ($n=3$): agent 1 values no leftover good,
   so no source-SCC handout exists, and **4 goods are left with $n=3$**. Giving
   goods only to agents 0 and 2 — the only ones who gain — keeps EF.
2. *Goods and chores cancel.* Trials 1845, 2010: the leftover good and the
   leftover chore on **one** agent leave every value unchanged, and the
   allocation is EF with **zero** subsidy; splitting them forced a 2.

## 3. Why goods do not mirror chores

Adding $e$ to $X_j$ moves arc weights by $+v_i(e\mid X_j)$ into $j$ and by
$-v_j(e\mid X_j)$ out of $j$ (approach 15, §3).

- A **chore** harms its *holder*, and uniformly: every comparison the holder
  makes worsens by the same $-v_j(c\mid X_j)$. Once R1 fails that amount is
  exactly 1 for everyone, so TAIL can always hand one chore to each member of
  a tail SCC when $\abs R\ge\abs S$: the halting bound $r<\abs S$ is automatic.
- A **good** harms its *onlookers*, by agent-dependent amounts
  $v_i(g\mid X_j)$. Its uniform part is the holder's own gain, and nothing in
  the halting conditions forces that to be 1. So the mirror handout needs a
  matching condition, and when the matching fails the leftover goods are not
  bounded by $\abs S - 1$.

## 4. The goods completion lemma (proved)

**Lemma.** Let $X$ be envy-free, every leftover item a goods-type item, and
$\tau$ inject the leftovers into agents with
$v_{\tau(g)}(g\mid X_{\tau(g)})=1$. Put $A_t=X_t\cup\tau^{-1}(t)$,
$T=\tau(R)$, and let $Q$ be the smallest set with
(Q1) every $k\notin T$ tied to some $t\in T$ that gains from $t$'s item on
$X_t$ is in $Q$; (Q2) every $k\notin T$ tied to a member of $Q$ is in $Q$.
Then $(\alloc,\mathbf 1[Q])$ is envy-free and $\sum\subsidy=\abs Q\le n-\abs T\le n-1$.

*Proof.* Net own values: $v_i(X_i)+1$ for $i\in T\cup Q$, $v_i(X_i)$ otherwise.
Views: $v_i(X_j)+1$ of $j\in Q$; $v_i(X_j\cup g_j)\le v_i(X_j)+1$ of $j\in T$;
$v_i(X_j)$ otherwise. An agent of $T\cup Q$ sees every package at most
$v_i(X_j)+1\le v_i(X_i)+1$. An agent $i\notin T\cup Q$ is untied to $Q$
(else Q2), and towards $t\in T$ it is untied or does not gain (else Q1); in
each case its view is $\le v_i(X_i)$ by envy-freeness and integrality. $\square$

Onlookers who see an item as a chore only lose, so the lemma holds verbatim
for **doubly monotone** items. Machine check with the explicit payment
(`goods_completion_check.py`): 27,242 states, 27,934 admissible $\tau$,
$n\le5$, objective and doubly monotone — **0 violations**.

## 5. Halting only at maximality (Experiment 4, `eqgraph_maximal.py`)

The phase applies any envy-free extension, in this order: one item; one item
after an envy-free reassignment; TAIL; any two items (to one agent or two,
with or without reassignment — covers the good–chore pair); goods to $\ge3$
agents. 8,100 instances (objective and doubly monotone, $n=3,4$, $m=6,7$):

- 7,276 finish with every item placed and **no subsidy**;
- 824 halt, and the structured completion (chores to distinct members of a
  tail SCC, goods to distinct agents valuing them at $+1$) works in **all 824**;
- at every halt the leftovers are **only chores or only goods**, never both,
  and number at most $n-1$.

`adversary.py` (hill-climbing over instances to force mixed leftovers,
unmatchable goods, a failed or dead completion; 66 restarts, ~9,000
mutations, both modes): **nothing**; the most leftovers it reached was $n-1$.

## 6. The reduction to two combinatorial conjectures (proved)

Call an envy-free partial allocation **maximal** if no nonempty set of
leftover items can be added — after any reassignment that leaves every
agent's value unchanged — keeping envy-freeness. (Maximal states exist: start
from the empty allocation and extend.)

- **(C1)** At a maximal state the leftovers are all chores-for-everyone or all
  goods-type.
- **(C2)** If they are goods-type, they inject into agents each valuing its
  item at $+1$ on its own bundle.

**Theorem (conditional).** (C1) and (C2) imply that every doubly monotone
dichotomous instance has a complete allocation with $\subsidy\in\set{0,1}^n$,
$\sum_i\subsidy_i\le n-1$.

*Proof.* Take a maximal state. If only chores-for-everyone are left: single
insertion and rotation fail, which is exactly Tao's halting condition (R1,
R2), and TAIL fails, so $r<\abs S$; the completion theorem of the paper
applies verbatim — its proof uses only those facts and that adding a
chore-for-everyone never raises anyone's view of a bundle. If only goods-type
items are left: (C2) and §4. (C1) excludes the mixed case. $\square$

Nothing here uses objective signs: that is the doubly monotone insight.

## 7. Doubly monotone through the existing architecture (Experiments 3, 5)

Treat a doubly monotone item $e$ as a good that only its **eligible** agents
$\mathrm{Elig}(e)$ (those for whom it is a good) may hold.

**(INS-E).** Envy-free solution $(A,\subsidy)$, minimal $\subsidy\in\set{0,1}^n$,
item $e$ with $\mathrm{Elig}(e)\neq\emptyset$: $e$ can be added, under some
reassignment, with an eligible holder and minimal subsidy still in $\set{0,1}^n$.

If true, doubly monotone follows: chores-for-everyone first (the paper's
theorem), then every other item one at a time.

- **Evidence** (`ins_eligible.py`): every valid state with all other items
  placed, random instances, $n\le5$, $m\le7$: **426,827 states, 0 failures**;
  over 99% need no reassignment.
- **What BKNS's proof gives.** Claims 1–2 and the extendable case survive: a
  $+1$ recipient is automatically eligible, and ineligible onlookers only lose.
  FindSink transfers verbatim when every maximally subsidised agent is
  eligible. It can break when some is not.
- **The hard case** (someone paid, every paid agent ineligible): 59,994 of the
  states above, all solvable, always with an unpaid eligible holder. In a
  separate run of 34,645 hard states (`hard_case.py`), 36% are BKNS-extendable
  through a package swap (bundles and subsidies move together along tight
  arcs). Of the remaining 22,278, a closure rule — pay the tied eligible
  gainers, close backwards over unpaid agents — works in all but one. That one needs a **new move**: the eligible agent takes a paid bundle
  *plus* $e$ and keeps the payment, because $e$ supplies the one unit by which
  it fell short of indifference (the mirror of EXTEND).

## 8. Mainak's SCC-migration notes (`scc_migration_findings_2026-10-03.md`)

Checked by `scc_migration_check.py` (chores algorithm, then BKNS on the goods,
FindSink explored over every choice):

- **§2** (extendable $\iff$ a cyclic-tight marginal-1 edge enters $M(\subsidy)$):
  **correct in the boxed form**; the "same SCC" formulation must require the
  edge itself to be tight, and a self-loop (own marginal 1 at an agent of
  $M(\subsidy)$) counts. Matches brute force in ~15,500 distinct checks.
- **§3, §4**: correct; §4 is BKNS's (S8) plus telescoping.
- **§5**: correct for the first good after the chore completion (it also
  follows directly from non-extendability). It does not persist: in 5 cases,
  all at goods #3–#6, $S^\star$ had lost strong connectivity in $H_\subsidy$
  and FindSink chose $s_1\in S^\star$.
- **§6 (no re-entry): proof gap.** Tight edges can leave $S^\star$: an unpaid
  $u\in S^\star\setminus T$ that prefers its bundle by exactly 1 to a *paid*
  outsider's is tight towards it (the payment closes the slack), and a
  recipient $u\in T$ similarly when its slack was 1 before its chore. Also a
  zero-weight tight path need not have zero-weight edges. So
  "$w_A(u,v)<0$" fails as stated. Empirically untested: FindSink made only 23
  selections in ~3,900 non-extendable insertions.

## 9. Next

1. Prove (C1) and (C2) — statements purely about envy-free partial
   allocations; start with $n=2,3$ and pure goods (C2 for pure goods would be
   a new, graph-theoretic proof of BKNS).
2. Or prove (INS-E): extend FindSink with the closure rule and the
   "short-by-one" swap of §7.
3. Either way, find polynomial rule sets: maximality as tested is exponential
   (reassignments, pairs, handouts).
4. Push the adversary harder (finer mutations, $n=5$).

## 10. Reproducing

```
cd updates_general_binary/update_3
python run_objective.py 3 6 3000 11 F-ROT-TAIL-SRC random   # §2
python diagnose_ksym.py 3 5 3000 16 additive 4               # §2 failures
python eqgraph_maximal.py 4 6 400 44 random objective        # §5
python adversary.py 4 6 10 150 73 objective                  # §5
python goods_completion_check.py 4 6 2000 62 objective       # §4
python ins_eligible.py 4 6 400 21                            # §7
python hard_case.py 3 6 1500 51                              # §7
python scc_migration_check.py 4 7 8000 95                    # §8
```
