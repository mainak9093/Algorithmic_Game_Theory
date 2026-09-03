# PS2 for three agents — merged state

*Response to `PS3_n3_current_state_from_scratch.md`. That document and the
repo's approach 15–17 line were written independently; this merges them, says
what checked out, corrects two things, and states the one correction that
changes the roadmap.*

**Naming.** Your "PS3" is the repo's **PS2** — general binary, marginals in
$\set{-1,0,1}$. Same problem, different label. `PS2` is used below.

---

## 0. The headline

Your §27 concludes that a proof "must permit **global** redistribution, not
just bounded-size local moves", and §29 accordingly targets an
Extreme-Agent Redistribution Lemma that may move arbitrarily many items.

**That conclusion does not follow from the evidence given for it.** Your §12
and §13 counterexamples refute hill-climbing on *welfare*; they say nothing
about local moves under a different potential. Measured directly:

| state | one-item moves improving **welfare** | one-item moves decreasing $\Psi$ |
|---|---|---|
| §13's $(\set{a,b,c},\emptyset,\emptyset)$, $v_i(S)=-\abs S$ | **0** — locally welfare-maximal | **6**, $\Psi: (3,0,0) \to (2,1,0)$ |
| §12's class — 170 states found that are locally welfare-maximal and need subsidy $\ge 2$ | 0 by construction | **170 of 170** |

where

$$\Psi(\pi) \;=\; \min_{\sigma}\ \operatorname{sort}_{\downarrow}\bigl(\ell_{(\pi,\sigma)}(i)\bigr)_i,$$

the longest-path vector sorted downwards, **minimised over the assignments** of
the partition's bundles, ordered lexicographically.

So a one-item move suffices at exactly the states you cite as showing it does
not. What fails is *welfare* as the thing to improve — which is the same fact
your own §9 records, and the same one the repo hit from the other side (§4
below). **The live target is much smaller than §29's lemma**, and §31's warning
2 ("every bad allocation has a local improving move") should be narrowed: it is
false for welfare, and so far true for $\Psi$.

---

## 1. What checked out exactly as you state it

- **§7 / P4** — $v_1(S)=-\abs S$, $v_2=v_3=-\abs{S\cap\set{a,b}}+[c\in S]$.
  All **6** balanced allocations are invalid; $(\set a,\set{b,c},\emptyset)$ is
  valid with minimal subsidy exactly $(1,0,0)$. ✓
- **§9 / P5** — $v_1\equiv0$, $v_2=v_3=\max(0,\abs S-1)$. Welfare maximum $2$,
  attained by **2** allocations, **both** invalid; $(\set a,\set b,\set c)$ is
  valid with subsidy $\mathbf 0$. ✓
- **§8 / P2**, the permutation-closed welfare lemma, and **§11**, the
  path-increment lemma, agree with the repo (approach 15 §19 and §3).
- **§22 / P3**, the signed decomposition $v = u - c$, and **§23**, that the
  certificate bridge is lossy — matches approach 15 §6, which reached the same
  conclusion with an independent verifier.

## 2. One transcription to fix — value spread versus size spread

§5 defines spread as **value** spread,
$\mathrm{spr}_i(A)=\max_j v_i(A_j)-\min_j v_i(A_j)$. The table in §6 (the
20,337,240-instance sweep) is from approach 15 §18, where (S2) is stated for
**bundle-size** spread, $\max_i\abs{A_i}-\min_i\abs{A_i}$. Different
conditions; the table is not evidence for the value-spread version.

**But the value-spread version independently holds**, so §5 stands once the
citation is corrected:

| | m=3 | m=4 | m=5 | m=6 |
|---|---|---|---|---|
| instances | 4,000 | 1,200 | 300 | 60 |
| min value spread over valid allocations $=0$ | 380 | 299 | 84 | 32 |
| $=1$ | 3,561 | 897 | 216 | 28 |
| $=2$ | **59** | **4** | 0 | 0 |
| $\ge 3$ | **0** | **0** | **0** | **0** |

Two readings, both supporting you. **§15 is right** — value spread $1$ is *not*
always achievable, forced to $2$ in about 1.5% of $m{=}3$ instances. And the
constant $2$ is **tight and sufficient**: never forced to $3$, in sampling or
under a hill climb that tried to force it (50 climbs × 250 steps at $m{=}5$,
best reached $2$).

## 3. Warning: this class defeats random sampling

Twice this session a statement passed thousands of random instances and then
died to a hill climb:

- **(CANON)** — "the leximin welfare maximiser of the spread-$\le2$ family is
  valid" — survived 2,250 random instances, refuted by 10 of 200 climbs. Worse,
  in 5 of 10 witnesses *no* welfare maximiser is valid, so no tie-break repairs
  it. This is the sharpened form of your §10, and it kills that route.
- **(DESCENT-SUM)** — the same descent with $\Psi$ replaced by
  $\sum_i \ell(i)$ — survived random sampling, refuted by a climb.

Anything added to your §32 "computationally verified" list should say whether
it has been *climbed at*, not just sampled. Several entries there (C1–C4) are
sampling only.

## 4. Your §9 and the repo's Pareto result are the same fact

§9 shows global welfare maximisation fails. The repo has the sharper statement,
in `PARETO_INVESTIGATION.md` and `docs/PO.tex`: a subsidy capped at one unit per
agent is **incompatible with Pareto optimality** — there are instances where no
allocation is both. Efficiency wants to concentrate; concentration creates an
envy gap the cap cannot fund.

That is why welfare is the wrong objective at *every* scale — globally (your
§9), inside the spread-2 family ((CANON), §3 above), and locally (your §12).
The three are one phenomenon. Worth stating once in your §9 rather than three
times as separate failures.

## 5. A second structural obstruction, which rules out a family of criteria

Beyond welfare: **no criterion that scores an allocation by the profile
$(v_i(A_i))_i$ alone can work.** There are two allocations of one instance with
the *same* profile $(0,0,0)$, one valid and one not — $(5,10,0)$ invalid versus
$(9,2,4)$ valid, in bitmask form at $m{=}4$.

The profile is the **diagonal** of the matrix $v_i(A_j)$, while validity reads
off-diagonal entries through $w(i,j)=v_i(A_j)-v_i(A_i)$. So leximin, least
maximum, least sum of squares and least spread all fail — and as one
obstruction, not four coincidences. Any canonical object must see off-diagonal
data. $\Psi$ does.

---

## 6. The live route, and what is actually proved

### Proved

- **Fact 1.** $\Psi$ is finite: by Halpern–Shah a welfare-maximal assignment of
  any partition's bundles is envy-freeable, so the minimum is over a non-empty
  set, and each $\ell\ge0$.
- **Fact 2 (the reduction).** If every partition with $\max_i\ell(i)\ge2$
  admits a one-item move strictly decreasing $\Psi$, then PS2 for $n=3$ holds
  *constructively*: $\Psi$ takes finitely many values and strictly decreases,
  so the process halts, and it cannot halt while $\max_i\ell\ge2$.
- **Lemma 1 (your §4, sharpened).** The Type I / Type II split is exhaustive —
  three vertices admit only the empty path, one arc, two arcs. Machine-checked:
  480 of 480 states classified, none left over.
- **Lemma 2.** In Type I the 2-cycle forces $w(2,1)\le-2$; in Type II the
  3-cycle forces $w(3,1)\le-2$. So an arc of weight $\le-2$ always exists
  (387 of 387 states, 1.74 per state).
- **Lemma 3.** $w(y,x)\le-2$ plus marginals in $\set{-1,0,1}$ gives
  $\abs{v_y(S)-v_y(T)}\le\abs{S\mathbin{\triangle}T}$, hence
  $\abs{A_x}+\abs{A_y}\ge2$ — the pair always contains an item to move, so the
  next step is not vacuous.

### Open — this is the whole remaining gap

> **(PAIR).** Let $A$ be envy-freeable with $\max_i\ell_A(i)\ge2$. Then for a
> *suitable* arc $(y,x)$ of weight $\le-2$, moving **one item** between $A_x$
> and $A_y$ strictly decreases $\Psi$.

Verified 387 of 387; survived 90 climbs at $m{=}4$ and 30 at $m{=}5$. Its
weakest point reached is a state with only **1** suitable arc, against 2 for the
plainer (DESCENT-1), so it is the likelier of the two to fall.

"Suitable" is not removable: the *every*-arc form fails, 345 of 387.

### One route to (PAIR) already closed

The natural proof shrinks the offending arc. Moving $g$ from $A_2$ to $A_1$
changes the gap by $-[v(g\mid A_2-g)+v(g\mid A_1)]$, and $h$ the other way by
$+[v(h\mid A_2)+v(h\mid A_1-h)]$, so the gap drops when one bracket has the
right sign. That is a statement about **one** valuation and two disjoint sets,
so it is exhaustively decidable — and it is false at exactly the gap Lemma 2
delivers:

| hypothesis | $m=3$ | $m=4$ |
|---|---|---|
| gap $\ge1$ | 24 violations | 44,496 |
| **gap $\ge2$** — what Lemma 2 gives | 0 | **48** |
| gap $\ge3$ | 0 | 0 |

The witness is a saturating valuation, $0,0,-1,-2,-2$ by bundle size, with
$A_1$ everything and $A_2$ empty: moving any one item leaves a triple worth
$-2$ against a singleton worth $0$, so **the gap stays at 2**; only two items
close it.

Yet building 3,000 instances *around* that obstruction gives 1,824 bad states,
1,722 carrying an arc of weight exactly $-2$, and **zero** failures of (PAIR).
So the descent works through the **aggregate** — rebalancing the other agents'
longest paths — not through the offending arc. Any proof must handle the whole
vector at once, which is §5's diagonal obstruction wearing a different hat.

---

## 7. Suggested next steps, in order

1. **Attack (PAIR)**, not §29's global lemma. It is a two-bundle statement with
   the third agent entering only through Lemma 2's cycle condition, and Facts 1
   and 2 already convert it into PS2 for $n=3$.
2. **Climb at (PAIR) harder first** — at $m{=}5,6$ and with more steps. It
   reaches 1 where (DESCENT-1) reaches 2, and two claims have already died this
   way. If it falls, the witness identifies the right invariant, exactly as
   §35(2) recommends.
3. **Do not re-propose**: any welfare-based canonical object (§4 above), any
   criterion reading only $(v_i(A_i))_i$ (§5), the sum potential, or
   arc-shrinking as the mechanism for (PAIR) (§6).
4. **Only if (PAIR) falls**, return to §29's global redistribution — but note
   that the local route has not been refuted, only left unproved, and §12/§13
   are not evidence against it.

### Scripts

All in `updates_general_binary/update_1/`. Relevant to this document:
`check_user_doc.py` (your P4, P5 and the spread readings), `vspread_dist.py`
(the value-spread table), `hunt_valuespread.py` (the climb at it),
`reconcile_local.py` (§0's table), `pair_lemma.py`, `hunt_pair.py`,
`transfer2.py`, `probe_gap2.py`, `verify_stuck.py`. Full index in
`approach_17.md` §8.
