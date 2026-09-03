# Approach 16 — A canonical object for PS2, and the residual of (BAL-STEP)

*Continues approach 15. That pass reduced (S1) to a single-step lemma
(BAL-STEP) and proved a fragment of it (§33). This pass finishes the anatomy of
the residual, adds two new lemmas and a selection rule that between them leave
nothing uncovered in the chores class, and then finds a **canonical object for
PS2 itself** which makes the incremental route optional rather than necessary.*

---

## 0. Verdict

Two things came out, one tactical and one strategic.

**Tactical.** (BAL-STEP) in the chores class is now covered by three rules plus
a selection rule, all machine-verified with zero violations:

| | what it needs | share of states | status |
|---|---|---|---|
| **Rule 1** free insertion (§33) | chore free for the holder | 61.7% | proved in §33 |
| **Rule 2** price headroom | recipient unsubsidised, chore costs *everyone* | 12.9% | **proved below, new** |
| **Rule 3** rotate then insert | some agent finds the chore free there | 13.3% | verified |
| residual | rotation only available *after* the insertion | 12.2% | open |

and the recipient is not free to choose: growing a **subsidised** smallest
bundle genuinely fails (12 failures at $n{=}3,m{=}4$), growing an
**unsubsidised** one never did, and an unsubsidised smallest bundle always
exists in the chores class.

**Strategic, and the more important half.** The whole incremental apparatus can
be bypassed. Inside the spread-$\le 2$ family, take the welfare-maximising
allocations and break ties by **leximin on the cost profile**. That allocation
was valid in every instance tested, in the *general binary* class — which is
(S2), and (S2) implies PS2. The tie-break is doing real work: 14 of 1,500
instances at $m{=}3$ have a welfare maximiser that is *not* valid, so the
un-tie-broken statement is false and §24's correction is confirmed, but the
leximin one never failed.

This replaces "run an algorithm and prove every step is safe" with "write down
one allocation and prove it works", which is a much smaller target.

---

## 1. Validity is a Hall condition

Everything below is easier in one reformulation, which is just Halpern–Shah
with the subsidy read as a price on the **bundle** rather than on the agent.

$(A,\subsidy)$ is envy-free exactly when
$v_i(A_i) + \subsidy_i \ge v_i(A_j) + \subsidy_j$ for all $i,j$. Attach
$q_j := \subsidy_j$ to the *position* $j$ instead. Then the condition says
precisely that every agent holds a bundle maximising $v_i(B_j) + q_j$.

> **Reformulation.** A multiset of bundles $\mathcal B = \set{B_1,\dots,B_n}$
> admits a valid assignment **iff** there is a set $Q$ of positions such that
> the *demand graph* — agent $i$ joined to every position maximising
> $v_i(B_j) + q_j$, with $q_j = 1$ iff $j \in Q$ — has a perfect matching.

Envy graphs, longest paths and the assignment all disappear; what is left is a
Hall condition on $2^n$ candidate price vectors. Two consequences are used
throughout:

- **validity is a property of the bundle multiset**, not of the assignment, so
  (BAL-STEP) is a statement about multisets;
- the effect of an insertion can be tracked one *score* at a time.

Checked in `demand_form.py` against the envy-graph implementation on every
balanced multiset at $n{=}3,m{=}3$: **1,865,648 multisets, zero mismatches.**

---

## 2. What the free-insertion lemma leaves

§33's free-insertion lemma covers the case where nothing can rise; in the
chores class its hypothesis collapses to "the chore is free for its recipient",
which is Tao–Wu–Yu–Zhou's rule (R1). Measuring the rest
(`residual_balstep.py`, exhaustive at $n{=}3,m{=}3$, 1,225,464
(state, unallocated chore) pairs):

| | count | share |
|---|---|---|
| **FREE** — some smallest bundle has the chore free for its holder | 755,553 | 61.7% |
| **HARD** — the chore costs the holder of *every* smallest bundle | 469,911 | 38.3% |
| &nbsp;&nbsp;of HARD: identity insertion still works | 307,533 | |
| &nbsp;&nbsp;of HARD: **reassignment genuinely required** | 162,378 | 13.3% |
| &nbsp;&nbsp;of HARD: nothing works | **0** | |

The middle row is the one that matters for a proof: in 162,378 states no
insertion into any smallest bundle is valid *unless the bundles are also
reassigned*. **No identity-only argument can prove (BAL-STEP).** A reassignment
step is unavoidable, exactly as §33 predicted.

---

## 3. Rule 2 — price headroom (new)

Insert $g$ into $B_x$ and write $d_i := \cost_i(g \mid B_x) \in \set{0,1}$.
Only two price updates are available at position $x$, and their failure modes
are exactly opposite:

| update | score of $x$ moves by | who is disturbed |
|---|---|---|
| **keep** $q'_x = q_x$ | $-d_i$ | agents with $d_i = 1$ may *lose* $x$ |
| **raise** $q'_x = 1$ (needs $q_x = 0$) | $1 - d_i$ | agents with $d_i = 0$ that already demanded $x$ *collapse* onto it |

That gives a clean new lemma covering precisely the case Rule 1 cannot.

> **Lemma (price headroom).** Let $(q,\sigma)$ be a valid witness, let $q_x = 0$,
> and suppose $\cost_i(g \mid B_x) = 1$ for **every** agent $i$. Insert $g$ into
> $B_x$ and set $q'_x = 1$. Then the state is valid, with the same assignment.

*Proof.* Since $q_x = 0$, agent $i$'s score at position $x$ is $v_i(B_x)$, and
after the move it is $v_i(B_x) - d_i + 1 = v_i(B_x)$, because $d_i = 1$. Every
other score is untouched. So every agent's demand set is **exactly** what it
was, and the old matching is still perfect. $\square$

The hypothesis $q_x = 0$ is not decoration: a position already at price $1$ has
no headroom left, and §5 below exhibits the failures that result. Verified with
zero violations on the 158,475 states where it applies (12.9%).

---

## 4. Rule 3 — and why the rotation must come *after* the insertion

The states left over after Rules 1 and 2 have one shape, without exception: the
chore is free for *some* agent on a smallest bundle, just not for the agent
holding it. The repair is TWYZ's rule (R2) — put the bundle in the hands of the
agent for whom the chore is free — and it works whenever that reassignment is
available (162,378 states, zero violations).

But it is **not** always available beforehand. After all three rules, 149,058
states (12.2%) remain, and in **every one of them** a free agent exists while
**no valid reassignment of the un-grown bundles puts that agent on that
bundle**. All 149,058 are nevertheless solvable.

The reading is that the move is genuinely "insert, *then* reassign": the
intermediate allocation need not be valid, and requiring it to be is what
blocks the argument. This is the same trap recorded once before in this project
(the reachability move model), and it is worth stating as a standing rule:

> A step is *insert + reassign*. Only the **result** has to be valid.

---

## 5. The selection rule — grow an unsubsidised smallest bundle

At $n{=}3,m{=}4$ the recipient starts to matter: of 544,000 pairs, every
smallest bundle works in 543,808, and in 192 the choice is real
(`select_rule.py`). Inspecting those 192, the failing bundle is the
**subsidised** one every single time. That suggests two claims, tested directly
in `unsub_rule.py`:

- **(U1)** some smallest bundle is unsubsidised;
- **(U2)** growing **any** unsubsidised smallest bundle keeps the multiset good.

| class | pairs | (U1) fails | (U2) fails | subsidised bundles grown | of which fail |
|---|---|---|---|---|---|
| chores $n{=}3,m{=}4$ | 34,000 | **0** | **0** | 468 | **12** |
| chores $n{=}4,m{=}4$ | 35,040 | **0** | **0** | 0 | 0 |
| goods $n{=}3,m{=}4$ | 34,000 | 10,365 | **0** | 15,378 | 0 |
| goods $n{=}4,m{=}4$ | 35,040 | 18,528 | **0** | 37,752 | 0 |

In the chores class (U1) and (U2) together give (BAL-STEP) **with no search and
no tie-breaking**: the algorithm may take the chores in any order and grow any
unsubsidised smallest bundle. The price reading says why it should be true —
an unsubsidised position has one unit of headroom with which to pay for the
damage the new chore does, and a position at price $1$ has none.

The 12 failures in the chores row are the evidence that the restriction to
unsubsidised bundles is necessary, not merely convenient.

**One caveat, recorded because it cost time.** The fully explicit version — fix
every other price and use only *keep* or *raise* at $x$ — is **not** enough:
it fails in 31,410 of 544,000 pairs (`explicit_step.py`). Some states need a
different price vector entirely, so a proof of (U2) cannot be a two-case
argument on the price of $x$ alone.

## 6. The two pure classes are not interchangeable step by step

(U1) holds in chores and **fails** in goods, while growing a subsidised bundle
is harmless in goods and sometimes fatal in chores. This looks like it should
contradict §23, which proves (S1)-goods and (S1)-chores equivalent — and it
does not, for an instructive reason.

§23's size-shift is an isometry of the envy graph **only on equal-cardinality
allocations**; on a balanced allocation with sizes in $\set{k,k+1}$ the arc
weights pick up the correction $\abs{B_j} - \abs{B_i} \in \set{-1,0,1}$. So the
*existence* statements are dual, while the *step-by-step processes* are not.
Any proof that runs an induction over insertions has to be carried out in one
named class; it does not transfer for free.

---

## 7. A canonical object — the strategic result

The incremental route can be bypassed altogether. Instead of building an
allocation chore by chore, write one down and prove it works.

> **(CANON).** Inside the family of allocations of spread $\le K$, take those
> maximising welfare, and among them the **leximin-optimal** one — sort each
> cost profile in decreasing order and take the lexicographically least. That
> allocation is valid.

At $K = 1$ this is (S1); at $K = 2$ in the general binary class it is (S2),
which implies PS2. Measured in `canon_target.py` and `canon_check.py`:

| class | spread | instances | LEX | MAX | SQ | SPREAD | some maximiser valid |
|---|---|---|---|---|---|---|---|
| general binary $m{=}3$ | $K{=}1$ | 2,000 | 1,995 | 1,995 | 1,995 | 1,995 | 1,995 |
| **general binary $m{=}3$** | $K{=}2$ | 2,000 | **2,000** | 2,000 | 2,000 | 2,000 | 2,000 |
| **general binary $m{=}4$** | $K{=}2$ | 250 | **250** | — | — | — | 250 |
| chores $m{=}3$ | $K{=}1$ | 2,000 | **2,000** | 2,000 | 2,000 | 2,000 | 2,000 |

Three readings.

**The $K=1$ row is a control, not a failure.** 5 of 2,000 general binary
instances admit no valid allocation of spread $\le 1$ at all — this is §18's
finding that $K=1$ is genuinely insufficient for general binary. What matters
is that the tie-break columns *exactly* match the "some maximiser valid"
column: whenever the family contains a valid allocation, leximin finds it.

**The tie-break is not vacuous.** At $m{=}3$, $K{=}2$: welfare maximisers tie in
1,020 of 1,500 instances (largest tie 15 allocations), and **ALL maximisers are
valid in only 1,486** — so 14 instances contain a maximiser that is not valid.
This confirms §24's correction, and shows the leximin choice is doing the work
rather than being carried by an already-true statement.

**Four different tie-breaks all worked** (leximin, least maximum cost, least sum
of squares, least cost spread), which is weak evidence that the mechanism is
flattening the cost profile rather than anything specific to leximin.

### Why a canonical object is the better target

A minimum-cost allocation is automatically envy-freeable: no reassignment of
its own bundles can beat it, so no positive cycle exists. Cost minimisation
therefore disposes of **cycles for free**, and the entire remaining content of
(CANON) is:

> the leximin-optimal welfare maximiser of spread $\le 2$ has no envy **path**
> of weight $2$.

A path is not a permutation, which is exactly why minimising the sum cannot see
it and why a *secondary* criterion is needed. That is a single self-contained
statement about one explicitly described allocation, with no algorithm, no
reachability, no insertion order and no excursions in it — the smallest target
this problem has had.

---

## 8. What to prove next, in order

1. **(CANON) at $K = 2$**, general binary. Suppose the leximin-optimal
   spread-$2$ maximiser has a path $i \to j \to k$ of weight $2$. No positive
   cycle exists, so closing the path into a cycle gives
   $\cost_k(A_i) \ge \cost_k(A_k) + 2$: the terminal agent finds the initial
   bundle at least $2$ dearer. The task is to turn that, plus a single item
   swap between $A_i$ and $A_k$ (which preserves both sizes, hence the spread
   bound), into either a cheaper allocation or a leximin-smaller one at equal
   cost. Both contradict the choice of $A$.
2. **(U1) for chores** — some smallest bundle is unsubsidised. Small, clean,
   and it is what makes the selection rule well defined.
3. **(U2)** — growing an unsubsidised smallest bundle preserves goodness. Note
   §5's caveat: it cannot be proved by a case split on the price of $x$ alone.
4. Only if 1 fails: return to the incremental route, where the open piece is
   §4's residual — the rotation that is available only after the insertion.

---

## 9. Reproducing

All scripts in `updates_general_binary/update_1/`, runnable from that folder.

| Script | What it does |
|---|---|
| `demand_form.py [n] [m]` | checks the demand-graph reformulation of §1 against the envy-graph implementation |
| `residual_balstep.py exhaustive [n] [m]` | the FREE / HARD / reassignment-required split of §2 |
| `rule_coverage.py exhaustive [n] [m]` | Rules 1 and 2 with their violation counts, and the leftover shapes |
| `rule3_rotate.py exhaustive [n] [m]` | adds Rule 3 and isolates the residual of §4 |
| `select_rule.py [n] [m] [k]` | four candidate selection rules against brute-force truth |
| `explicit_step.py [n] [m] [k]` | whether recipient *and* prices can be written down explicitly; the 31,410 counterexamples of §5 |
| `unsub_rule.py [n] [m] [k]` | (U1) and (U2) in both pure classes — the table of §5 |
| `mincost_balanced.py [n] [m] [k]` | is a minimum-cost balanced allocation valid; ALL versus SOME |
| `tiebreak.py [n] [m] [k]` | the four tie-breaks among minimum-cost balanced allocations |
| `canon_target.py [n] [m] [k]` | (CANON) at $K=1$ and $K=2$, general binary, with the chores control |
| `canon_check.py [n] [m] [k] [K]` | that the tie-break is not vacuous, and $m=4$ |

Every rule claimed above is checked by *applying* it and then testing the
resulting state with the independent envy-graph routines, so a rule that looked
right for the wrong reason would still register as a violation.
