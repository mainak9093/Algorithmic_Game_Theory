# Approach 14 — Almost-Balanced Positive Dichotomous Allocations

Full record of the proposal in `approach_14_proposal.pdf`, its audit, and its status.

Cross-reference: `RESIDUAL.md` §7.16.40. Scripts: `update_14/`, `update_6/`.

---

## 0. Verdict

| Component | Status |
|---|---|
| Proposition 1 (RQ1 ⟹ Conjecture 2), the size-shift reduction | **CORRECT** — verified line by line |
| Research Question 1 (RQ1) itself | **Open**; no counterexample found. **Not new** — equals Approach 6's *Target G-bal* |
| Proposed proof program, Steps 1–3 (modify BKNS to maintain (I1)–(I3)) | **BLOCKED** — explicit reachability obstruction, re-verified |
| Step 4 (fall back to the path condition (6)) | **BLOCKED** — fails for a *different* reason than Steps 1–3 |
| Effect on Conjecture 2 | **None.** Conjecture 2 is proved unconditionally for all `n` by Approach 13 |

The proposal is a correct and reusable *reduction* whose *target* is an
already-open project conjecture and whose *proposed route* is closed.

---

## 1. The proposal, restated

### 1.1 Setting

Agents `N = [n]`, chores `M`, `|M| = m`. Each `c_i : 2^M → Z_{≥0}` has
`c_i(∅) = 0` and marginals in `{0,1}` (negative dichotomous). Conjecture 2 asks
for a complete allocation `A` and `p ∈ {0,1}^n` with

```
c_i(A_i) − p_i ≤ c_i(A_j) − p_j        for all i, j.
```

### 1.2 The size-shift transformation

```
ṽ_i(S) := |S| − c_i(S)
```

has marginals `1 − (c_i(S∪{g}) − c_i(S)) ∈ {0,1}`, so `ṽ_i` is a *positive*
dichotomous valuation. The map is an involution of the dichotomous class
(already recorded in Approach 6).

Writing `w^c_B(i,j) := c_i(B_i) − c_i(B_j)` and
`w̃_B(i,j) := ṽ_i(B_j) − ṽ_i(B_i)`:

```
w̃_B(i,j) = (|B_j| − c_i(B_j)) − (|B_i| − c_i(B_i))
         = w^c_B(i,j) − (|B_i| − |B_j|)
```

so

```
w^c_B(i,j) = w̃_B(i,j) + |B_i| − |B_j|.                                  (1)
```

If `(B,q)` is envy-free for the positive instance then `w̃_B(i,j) ≤ q_i − q_j`
(2), and combining,

```
w^c_B(i,j) ≤ (q_i + |B_i|) − (q_j + |B_j|).                              (3)
```

### 1.3 Research Question 1

Write `m = kn + r`, `0 ≤ r < n`. An allocation is *almost balanced* if
`|B_i| ∈ {k, k+1}` for all `i`; then `L := {i : |B_i| = k}` and
`H := {i : |B_i| = k+1}`, `|H| = r`.

> **RQ1.** For every positive dichotomous instance, is there a complete
> allocation `B` and `q ∈ {0,1}^n` with
> **(i)** `(B,q)` envy-free for the positive instance;
> **(ii)** `||B_i| − |B_j|| ≤ 1`;
> **(iii)** `|B_i| > |B_j| ⟹ q_i ≤ q_j` (equivalently `q_h ≤ q_ℓ` for
> `h ∈ H, ℓ ∈ L`)?

### 1.4 The exact weaker condition, and the IISc-style invariants

With `d̃_B(i,j)` the heaviest positive-graph path `i → j`, cardinalities
telescope, giving `d^c_B(i,j) = d̃_B(i,j) + |B_i| − |B_j|` (5). Only the case
`i = h ∈ H, j = ℓ ∈ L` can push the correction to `+1`, so conditional on the
positive `{0,1}` subsidy property the exact requirement is

```
d̃_B(h, ℓ) ≤ 0     for all h ∈ H, ℓ ∈ L.                                 (6)
```

*No positive-weight path from a large-bundle agent to a small-bundle agent.*
Condition (iii) is a sufficient condition for (6).

With `M(q)` the maximally subsidised agents, `L ⊆ M(q)` (7) is a sufficient
condition for (iii). The proposed algorithmic target is to maintain

- **(I1)** `B` envy-freeable with minimum subsidy `q ∈ {0,1}^n`;
- **(I2)** `max_i |B_i| − min_i |B_i| ≤ 1`;
- **(I3)** `{i : |B_i| = min_j |B_j|} ⊆ M(q)`

throughout the BKNS incremental construction, via
**Step 1** (restrict Extend to a minimum-cardinality bundle when unbalanced),
**Step 2** (choose the bundle permutation to keep the receiver, and afterwards
the minimum-cardinality agents, in `M(q)`),
**Step 3** (redo the non-extendable / FindSink case under the same
restriction), and
**Step 4** (if (I3) fails, weaken it to (6)).

---

## 2. Audit (a) — Proposition 1 is correct

Assume RQ1 gives `(B,q)`. Put `d_i := |B_i| − k ∈ {0,1}` and `r_i := q_i + d_i`.

| `|B_i|` | `q_i` | `r_i` |
|---|---|---|
| `k` | 0 | 0 |
| `k` | 1 | 1 |
| `k+1` | 0 | 1 |
| `k+1` | 1 | 2 |

`r_i = 0` forces `i ∈ L, q_i = 0`; `r_i = 2` forces `i ∈ H, q_i = 1`. Both
occurring would give `ℓ ∈ L, h ∈ H` with `q_ℓ = 0 < 1 = q_h`, contradicting
(iii). Hence `max_i r_i − min_i r_i ≤ 1`. With `α := min_i r_i` and
`p_i := r_i − α`, we get `p ∈ {0,1}^n`, and since a common shift cancels,

```
p_i − p_j = (q_i − q_j) + (|B_i| − |B_j|),
```

so by (3), `w^c_B(i,j) ≤ p_i − p_j`, i.e. `c_i(B_i) − p_i ≤ c_i(B_j) − p_j`. ∎

**Checked and correct.** The reduction is constructive and uses only value
queries plus arithmetic.

*Note.* Running the implication backwards, `q_i = p_i − d_i + α`, the binding
requirement is `q ∈ {0,1}^n`, i.e. that `p_i − d_i` has spread `≤ 1`. In chore
terms RQ1 says: **every chore instance admits an almost-balanced allocation
with `p ∈ {0,1}^n` and `p_h ≥ p_ℓ` for all `h ∈ H, ℓ ∈ L`** — larger chore
bundles are subsidised at least as much as smaller ones.

---

## 3. Audit (b) — RQ1 is Approach 6's Target G-bal

Approach 6 (`report/working/approach_6.tex`) already defines:

- **Target G** (`conj:targetG`): every dichotomous goods instance admits an
  allocation whose vector `q_i = p̃_i + |B_i|` has spread `≤ 1`; and
  `prop:targetG-implies` shows Target G ⟹ Conjecture 2.
- **Target G-bal** (`def:targetGbal`): the same, restricted to partitions whose
  group sizes **differ by at most 1**.

Since `q_i − k = q^{goods}_i + d_i = r_i`, RQ1's (i)+(ii)+(iii) is exactly
`r`-spread `≤ 1`. So

```
RQ1  ⟹  Target G-bal  ⟹  Target G  ⟹  Conjecture 2,
```

all already on record. In particular the proposal's **Remark 1 ("no dummy
chores needed") does not distinguish the two**: Target G-bal was already stated
for sizes differing by `≤ 1`, not for exact balance.

**What the proposal genuinely adds** (worth keeping):

1. the explicit two-tier compatibility condition (iii), which is easier to
   carry algorithmically than "spread `≤ 1`";
2. the exact path condition (6), which isolates precisely what must be
   controlled — no positive-weight path `H → L`;
3. the sufficient condition `L ⊆ M(q)` (7), phrased in BKNS's own vocabulary.

---

## 4. Audit (c) — RQ1 survives search

`update_14/rq1_search.py` generates positive dichotomous instances, enumerates
**every** almost-balanced allocation and **every** `q ∈ {0,1}^n`, and tests
(i)–(iii).

| n | m | generator | trials | RQ1 failures |
|---|---|---|---|---|
| 3 | 4 | uniform | 200 | 0 |
| 3 | 5 | uniform | 150 | 0 |
| 3 | 6 | biased 0.3 | 60 | 0 |
| 3 | 6 | biased 0.7 | 60 | 0 |
| 4 | 5 | biased 0.3 | 60 | 0 |
| 4 | 5 | biased 0.7 | 60 | 0 |
| 4 | 6 | biased 0.5 | 25 | 0 |

Consistent with Approach 6's `0 / 389,215` for Target G. **RQ1 appears true.**

---

## 5. Audit (d) — Steps 1–4 are blocked

All four steps modify the BKNS/R3 incremental algorithm. Approach 6 §"Item-by-item
insertion is the wrong template here too" already refutes this; both scripts
were re-run and independently confirmed.

### 5.1 The obstruction instance

`n = m = 3`, chore costs:

| `|S|` | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| `c_0(S)` | 0 | 0 | 0 | 0 |
| `c_1(S)` | 0 | 0 | 1 | 1 |
| `c_2(S)` | 0 | 1 | 2 | 2 |

(each `c_i` depends only on `|S|` here, and all marginals lie in `{0,1}`)

Size-shifted (`ṽ_i(S) = |S| − c_i(S)`):

```
ṽ_0(S) = |S|                      (values every item)
ṽ_1: ∅→0, singleton→1, pair→1, triple→2
ṽ_2: ∅→0, singleton→0, pair→0, triple→1      ← all-or-nothing
```

### 5.2 The three verifications

| Script | Result |
|---|---|
| `update_6/guidedR3_full.py` | Full backtracking over **every** legal R3 execution — every item order, every Extend choice, every FindSink start; **474 nodes**. Best reachable `q`-spread = **2**. Witness: bundles `[[1,2],[0],[]]`, `q = [2,1,0]` |
| `update_6/verify_reach_gap.py` | Algorithm-free enumeration on the same instance: `q`-spread **0** achievable, via `[0],[1],[2]` with goods subsidy `(0,0,0)`. **So RQ1 holds on this instance** |
| `update_14/reach_sizes.py` | **New, sharper.** The *only* final size profile any legal execution can reach is **`(0,1,2)`**. The almost-balanced profile `(1,1,1)` is **unreachable** |

### 5.3 Root cause

After size-shifting, agent 2 is **all-or-nothing**: `ṽ_2(S) = 0` for every
proper subset and `1` only on the full set. Its marginal for any single item on
the empty bundle is `0`, so an insertion algorithm that hands an item to an
agent only when the marginal is `1` never gives agent 2 a first item, and its
bundle stays empty. Bundle sizes are therefore driven to `(0,1,2)` and cannot
be evened out later — insertion fixes which items share a bundle the moment
they are grouped, and no permutation splits a bundle back apart.

### 5.4 Why each step dies

- **Step 1** restricts Extend to a minimum-cardinality bundle. A restriction
  only **shrinks** the reachable set, and **(I2) is already unreachable** here.
  The restriction is simply infeasible on this instance.
- **Step 2** restricts which bundle permutation is chosen — same argument.
- **Step 3** restricts FindSink — same argument.
- **Step 4** was the designed fallback, and it fails for a *different* reason:
  it weakens **(I3)** to the path condition (6), but the failure on this
  instance is **(I2)**, not (I3). Weakening (I3) does not enlarge the set of
  reachable **allocations**.

The obstruction is on **reachability of the allocation**, not on which
invariant is tracked. That is what makes it fatal to the whole program rather
than to one step of it.

---

## 6. What remains

- **RQ1 / Target G-bal is still open** for `n ≥ 3`, with no counterexample
  known and substantial supporting evidence.
- The live non-insertion route is Approach 6's **construct-and-repair**
  (IMWPM warm start + repair + restart): proved sound, terminating, and
  complete at `n = 2`; completeness open for `n ≥ 3`.
- Any future attempt must be able to **move an item out of a bundle it is
  already in**. Insertion-only templates are excluded by §5.

---

## 7. Reproducing

```bash
cd update_14
python rq1_search.py 3 4 200 1        # RQ1 search, uniform
python -c "import rq1_search as R; R.main_biased(4,5,60,13,0.3)"
python reach_sizes.py                 # reachable size profiles (needs ../update_6)

cd ../update_6
python guidedR3_full.py               # all legal R3 executions, 474 nodes
python verify_reach_gap.py            # algorithm-free: spread 0 achievable
```

---

## 8. Relationship to Conjecture 2

None of the above affects Conjecture 2, which is **proved unconditionally for
every `n`** by Approach 13 (`report/working/approach_13.tex`, `RESIDUAL.md`
§7.16.39): run the Tao–Wu–Yu–Zhou partial-EF algorithm, place the residue into
distinct bundles indexed by the terminal tail SCC, and subsidise the backward
equality closure of the recipients. Approach 14 was explored as an independent
alternative route while Approach 13 is being checked by hand.
