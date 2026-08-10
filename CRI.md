# The conditioned-remainder induction — frame, machinery, and what remains

*Approach 3, reformulated. Status as of 2026-08-09.*

> **⚠ SUPERSEDED IN PART, 2026-08-10.** The depth theorem of §7 —
> `conj:cri-depth` — is **REFUTED**: 657 dead states with $\lvert R\rvert \ge 3$
> on the composed and capped families at $m = 6,7,8$
> (`update_48/depth_stress.py`). The caveat in §7 was correct and the corpus it
> warned about was the one that broke it. **§7 below is retained as the record
> of a refuted conjecture; do not read it as open.**
>
> **The replacement route is §11**, the witness-carrying invariant, with a bridge
> making `RESIDUAL.md` §7.3's Lemma A the soundness clause of this induction. Its
> one open clause is at least as strong as Lemma E (`RESIDUAL.md` §7.5), so
> **that is the target to settle first**.
>
> Everything else stands: the CR frame, Lemmas 1–3, the first-chore proposition,
> and CRI itself, which still has 0 bad roots — including on all 46 residual
> instances, where every one of the four solved cases fails
> (`RESIDUAL.md` §3).

This document is self-contained: it states the frame, gives every proved lemma
with its proof, reports the evidence, and delimits what is left. It is the
working reference for the CR line of attack, and stands alongside
`BALANCE_RULE.md`, which records the earlier peel-frame line.

---

## 1. Why a new frame

`BALANCE_RULE.md` §8 records that the peel-frame attack is out of candidates.
Three whole families of invariant are dead — local conditions on the peel
(96.1% per step, still only 48/191 schedules), predicates on (state, move)
(nothing separates good moves from bad at the 171 predecessors), and
$(\textsc{commit})$ (17 dead states satisfy it) — and seven greedy rules are
refuted outright. The route is also *provably strictly stronger* than
Conjecture 2 (`rem:converse`), so success would prove more than needed and
failure would prove nothing.

The diagnosis is that a workload profile $W$ is the wrong object. It is an
arbitrary tuple of subsets, there are $(2^m)^n$ of them, and they mean nothing
individually.

---

## 2. The CR frame

**Definition (CR state).** A pair $(A, R)$ with $R \subseteq M$ and
$A = (A_1,\dots,A_n)$ a partition of $D := M \setminus R$. Its **profile** is

$$W_i := A_i \cup R$$

— every agent is still on the hook for the whole undecided remainder. Its
**contracted cost functions** are

$$c^R_i(T) \;:=\; c_i(T \cup R) - c_i(R), \qquad T \subseteq D .$$

**Move.** *Assign* $a \in R$ to $x$: $A'_x = A_x \cup \{a\}$, $A'_k = A_k$ for
$k \ne x$, $R' = R \setminus \{a\}$. *Relabel*: $A \mapsto A \circ \sigma$.
**Root**: $A$ all empty, $R = M$. **Terminal**: $R = \emptyset$.
**Legal**: no positive-weight cycle and $\ell_W(i) \le 1$ for all $i$ — the same
invariant as `def:peel`.

In peel language an assignment is one **atomic block**: relieve all $n-1$
non-owners of $a$ at once. So a CR state is a peel state, a CR move is $n-1$
consecutive peels, and CRI drops the legality requirement at the $n-2$
within-block intermediates that `conj:h1pp` imposes.

**Conjecture (CRI).** From the root, some sequence of assignments and
relabellings reaches $R = \emptyset$ with every intermediate CR state legal.

$$\texttt{h1pp} \;\Longrightarrow\; \texttt{CRI} \;\Longrightarrow\; \text{Conjecture 2}$$

so CRI is strictly the weaker target. It implies Conjecture 2 because a terminal
CR state *is* an allocation, and its legality is exactly $\max_i \ell_A(i) \le 1$.

---

## 3. Why the frame is different, not a rebranding

**(i) The space is small and its states mean something.** CR states are partial
functions $M \to N$: $(n+1)^m$ of them against $(2^m)^n$ profiles. At $n=3,m=6$
that is 4,096 against 262,144, so reachability is decidable exhaustively well
past every sweep in `BALANCE_RULE.md`.

**(ii) The known peel dead ends are not CR states.** A profile $W$ is a CR state
iff the sets $W_i \setminus \bigcap_k W_k$ are pairwise disjoint and cover
$M \setminus \bigcap_k W_k$. Both recorded witnesses repeat an item across
bundles — $(\{a_1,a_2\},\{g\},\{g\})$ and $(\{g_2\},\{g_2\},\{g_1,g_3,g_4\})$ —
so neither is a CR state. *(Verified, `cri_anchor.py` A2.)*

**(iii) It restores the induction.** By Lemmas 1–2 below, CRI is an induction in
which the **instance grows** by un-contracting one chore while a witness is
maintained. That is the shape of the [BKNS22] proof, run on the conditioned cost
functions that dissolve the Approach 1 obstruction (`rem:conditioned`).
Approach 1 grew the instance with the *unconditioned* costs and died on
`thm:obstruction`; the peel frame got the conditioning right and then abandoned
the induction for a state-space search. This is the synthesis of the two.

---

## 4. The machinery (all proved)

### 4.1 The contraction

**Lemma 1 (contraction stays in the class).** $c^R_i$ is normalised with all
marginals in $\{0,1\}$, so $(D, c^R)$ is again a negative dichotomous instance.

> *Proof.* $c^R_i(\emptyset) = c_i(R) - c_i(R) = 0$. For $g \notin T \subseteq D$,
> $c^R_i(T \cup \{g\}) - c^R_i(T) = c_i((T\cup R)\cup\{g\}) - c_i(T \cup R) \in
> \{0,1\}$, since $c_i$ is dichotomous. $\square$

**Lemma 2 (a CR state is a witness on a smaller instance).**
$w_W(i,k) = c^R_i(A_i) - c^R_i(A_k)$. Hence

> $(A,R)$ is legal $\iff$ $A$ witnesses Conjecture 2 on $(D, c^R)$.

> *Proof.* $w_W(i,k) = c_i(A_i \cup R) - c_i(A_k \cup R)
> = [c^R_i(A_i) + c_i(R)] - [c^R_i(A_k) + c_i(R)]$; the $c_i(R)$ cancel. The
> envy graphs are equal arc for arc, so the two legality conditions coincide.
> $\square$
>
> *(Verified on 400 random states across all seven generators, 0 mismatches.)*

**This is the load-bearing lemma.** A CR state is not a bookkeeping device; it is
a solved instance of the problem on a contracted ground set, and a move
un-contracts one element.

### 4.2 The arc update

**Contraction identity.** For $T \subseteq D$,
$c^R_i(T) = c^{R'}_i(T \cup \{a\}) - c^{R'}_i(\{a\})$.

> *Proof.* $c^{R'}_i(T\cup\{a\}) - c^{R'}_i(\{a\})
> = [c_i(T\cup\{a\}\cup R') - c_i(R')] - [c_i(\{a\}\cup R') - c_i(R')]
> = c_i(T \cup R) - c_i(R) = c^R_i(T)$. $\square$

**Lemma 3 (CR arc update).** Write $\beta_i(T) := c^{R'}_i(T \cup \{a\}) -
c^{R'}_i(T) \in \{0,1\}$ for the marginal of $a$ to agent $i$ on $T$, conditioned
on $R'$. Then for $i \ne k$,

$$w'(i,k) - w(i,k) \;=\; \beta_i(A_k)\,[k \ne x] \;-\; \beta_i(A_i)\,[i \ne x].$$

So arcs **into** $x$ fall by $\beta_i(A_i)$, arcs **out of** $x$ rise by
$\beta_x(A_k)$, and third-party arcs move by
$\beta_i(A_k) - \beta_i(A_i) \in \{-1,0,1\}$.

> *Proof.* By the contraction identity the $c^{R'}_i(\{a\})$ terms cancel in
> $w$, giving $w(i,k) = c^{R'}_i(A_i\cup\{a\}) - c^{R'}_i(A_k\cup\{a\})
> = [c^{R'}_i(A_i) + \beta_i(A_i)] - [c^{R'}_i(A_k) + \beta_i(A_k)]$, while
> $w'(i,k) = c^{R'}_i(A'_i) - c^{R'}_i(A'_k)$ with $A'_x = A_x \cup \{a\}$ and
> $A'_k = A_k$ otherwise. Subtracting in each of the three cases
> ($i,k \ne x$; $k = x$; $i = x$) gives the stated formula. $\square$
>
> *(Verified on every arc of 248 random assignments, 0 mismatches.)*

**Corollary (the additive collapse).** If the $c_i$ are additive then $\beta_i$ is
constant, third-party arcs do not move, and only the arcs at $x$ change.

> **So the entire difficulty is the variation of $\beta_i$ across bundles.** This
> is consistent with `thm:binadd` already closing the additive case, and it is a
> much sharper localisation than the peel frame offered. *(Verified: 198 additive
> instances, 0 third-party arc moves.)*

### 4.3 The root, exactly

**Proposition (the first chore).** From the root, assigning $a$ to $x$ is legal
**iff** $\beta_x \le \beta_k$ for every $k$, where $\beta_i = c_i(M) - c_i(M \setminus \{a\})$
— give the chore to an agent of **minimal** marginal.

> *Proof.* At the root all $A_i = \emptyset$, so after the assignment
> $W_x = M$ and $W_i = M \setminus \{a\}$ for $i \ne x$. Hence $w(i,k) = 0$ for
> $i,k \ne x$, $w(i,x) = -\beta_i$, and $w(x,k) = \beta_x$. For $n \ge 3$ the
> first group forces $p_i = c$ for all $i \ne x$; the rest give
> $c + \beta_x \le p_x \le c + \min_{i \ne x}\beta_i$. That interval contains a
> point of $\{0,1\}$ iff $\beta_x \le \min_{i\ne x}\beta_i$: if $\beta_x = 0$ take
> $c = p_x = 0$, and if $\beta_x = 1$ then $\min\beta_i = 1$ and $c=0, p_x=1$
> works; conversely $\beta_x = 1 > 0 = \min\beta_i$ leaves the interval empty. For
> $n = 2$ the first group is vacuous and the same two constraints give the same
> criterion. $\square$
>
> *(Verified: 6,480 root assignments at $n \in \{3,4,5\}$ and 4,264 at $n = 2$,
> 0 mismatches.)*

This is the exact **mirror** of `prop:first-peel`, which takes a chore from an
agent of *maximal* marginal. Such an $x$ always exists, so the base case never
blocks.

### 4.4 Free assignments

**Lemma (free assignment).** If $\beta_x(A_k) = 0$ for all $k \ne x$, and
$\beta_i(A_k) \le \beta_i(A_i)$ for all $i,k \ne x$, then every arc weakly
decreases, so legality is preserved.

> *Proof.* Immediate from Lemma 3: arcs into $x$ fall, arcs out of $x$ rise by
> $\beta_x(A_k) = 0$, third-party arcs move by
> $\beta_i(A_k) - \beta_i(A_i) \le 0$. Path and cycle weights are sums of arc
> weights. $\square$

**Soundness, measured.** Over 235,349 reachable non-terminal states, all 1,285
stuck states had **no** free assignment — 0 exceptions. But the condition is far
from necessary: 112,540 non-stuck states also have none, so free assignments
cover only about 52% of states.

---

## 5. Evidence

All sweeps enumerate the state space **completely** — no caps — and use all seven
generators of `update_44/counterexample_hunt.py`, not `rand_dicho` alone as every
peel-frame sweep did.

| claim | scope | result |
|---|---|---|
| **CRI: no bad root** | **complete exhaustive $n=m=3$ family, 9,880 instances** | **0 bad roots** |
| CRI: no bad root | $n=3\ (m\le7)$, $n=4\ (m\le6)$, $n=5\ (m\le5)$, 438 adversarial instances | 0 bad roots |
| CRI without relabelling | same 10,318 instances | **3 bad roots** — relabelling is necessary |
| Lemma 2 | 400 random states | 0 mismatches |
| Lemma 3 | every arc of 248 assignments | 0 mismatches |
| additive collapse | 198 additive instances | 0 third-party arc moves |
| first-chore proposition | 10,744 root assignments, $n \in \{2,3,4,5\}$ | 0 mismatches |
| free assignment is sound | 1,285 stuck states | 0 had a free assignment |
| **no dead state at $\lvert R\rvert \ge 3$** | **34,543 reachable states with $\lvert R\rvert\ge3$** | **0 dead** |
| $K=3$ look-ahead | 10,045 instances, random play above $K$ | 0 failures |

**Where death lives** — over 312,436 reachable non-terminal states:

| $\lvert R\rvert$ | dead | all reachable | dead share |
|---|---|---|---|
| 1 | 1,230 | 183,984 | 0.669% |
| 2 | 45 | 93,909 | 0.048% |
| $\ge 3$ | **0** | 34,543 | **0%** |

---

## 6. What is refuted, with the exact witness (do not retry)

**CRI itself is not among these.** Every entry below is a *local* statement one
would like to prove CRI with; the conjecture survives all of them. Counts are not
evidence, so each is given with its minimal instance, extracted and re-verified
by `update_47/cri_witnesses.py`. Chores are $a,b,c,\dots$; every cost function
shown is dichotomous.

### 6.1 The central witness — pointwise CRI, and the last rung

$n = m = 3$, from the complete exhaustive family:

| $S$ | $\emptyset$ | $a$ | $b$ | $c$ | $ab$ | $ac$ | $bc$ | $abc$ |
|---|---|---|---|---|---|---|---|---|
| $c_1$ | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 |
| $c_2$ | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 |
| $c_3$ | 0 | 1 | 1 | 1 | 1 | 1 | 2 | 2 |

At the state $A = (\emptyset, \{b\}, \{a\})$, $R = \{c\}$ the profile is
$W = (\{c\}, \{bc\}, \{ac\})$ with envy matrix and path weights

$$\big(w(i,k)\big) = \begin{pmatrix} 0 & -1 & -1 \\ 0 & 0 & 0 \\ 0 & -1 & 0\end{pmatrix},
\qquad \ell = (0,0,0).$$

All three continuations create a **positive-weight cycle**, so none is even
envy-*freeable*, let alone within budget:

| move | result |
|---|---|
| $c \to$ agent 1 | positive cycle ($2 \to 3 \to 2$ has weight $1$) |
| $c \to$ agent 2 | positive cycle ($3 \to 1 \to 3$ has weight $1$) |
| $c \to$ agent 3 | positive cycle ($2 \to 1 \to 2$ has weight $1$) |

This one instance refutes three things at once, and the third is the important
one:

- **pointwise CRI** — 3,024 reachable counterexamples in all;
- **the last-rung lemma** — $\lvert R\rvert = 1$, and 1,765 of the 1,778 stuck
  states are of this shape, so this is where essentially all stuckness lives;
- **⚠ any invariant that scores the current state.** The state has
  $\ell = (0,0,0)$: it is *exactly envy-free, needing no subsidy at all* — the
  best a CR state can possibly be — and it is a dead end. Conjecture 2 holds on
  this instance (some allocation achieves $\max_i \ell = 0$), so the failure is
  purely one of scheduling. **No potential function measuring the quality of the
  current state can serve as $\Phi$**, because the doomed state is optimal. This
  eliminates the same class of candidate that `BALANCE_RULE.md` §8 was reduced to
  hunting in, and eliminates it for a structural reason rather than by a count.

### 6.2 Balance does not transplant

The **same instance and the same state** also refutes the one idea that survived
the peel frame. Bundle sizes are $[0,1,1]$ with one chore undecided, so the
completion $(1,1,1)$ is perfectly balanced and
`admits a balanced completion` holds — yet the state is dead. Over the corpus,
**132 dead states admit a balanced completion**. `conj:balance-rule`'s
certificate is false here.

### 6.3 Death is not always immediate

$n=3, m=5$. At $A = (\emptyset, \{ce\}, \emptyset)$, $R = \{abd\}$ with
$\ell = (0,1,0)$, two assignments are legal ($b \to 2$ and $d \to 2$) and **every
continuation still dies**. So one-step legality cannot certify a rule: the
free-assignment lemma is sound for a legal *move* and worthless for a legal
*schedule*. 45 of the 1,275 dead states are of this delayed kind.

### 6.4 Relabelling is load-bearing

$n=m=3$, with $c_1 = c_2$ charging $1$ only for the grand bundle and
$c_3(S) = \min(\lvert S\rvert, 2)$:

| $S$ | $\emptyset$ | $a$ | $b$ | $c$ | $ab$ | $ac$ | $bc$ | $abc$ |
|---|---|---|---|---|---|---|---|---|
| $c_1, c_2$ | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| $c_3$ | 0 | 1 | 1 | 1 | 2 | 2 | 2 | 2 |

Assignments alone cannot reach a legal terminal from the root. With one
relabelling they can: $\emptyset \to a{\to}3 \to b{\to}3 \to$ **relabel** $\to
c{\to}1$, ending at $(\{c\},\{ab\},\emptyset)$ with $\ell = (0,0,0)$. 3 such
instances exist in the exhaustive family.

### 6.5 The rest

| claim | why it died |
|---|---|
| $(\textsc{commit})$, transplanted ($c^R_i(A_i) \ge 2 \Rightarrow$ dead) | exactly backwards: 1,210 overcommitted states, **0** of them dead |
| "saturated" ($\ell \equiv 1$) as a stuckness predicate | vacuous — no state has $\ell \equiv 1$, since the endpoint of a heaviest path always has $\ell = 0$ |
| free-first as a rule | 31 failures / 10,034; smallest witness $n=m=3$ with $c_1(S)$ = $\lvert S\rvert$ capped at 2 shifted, root live yet the rule walks into a stuck state |
| min-marginal as a rule | 46 failures — it is *forced* at the root by §4.3, but not after |
| max-marginal as a rule | 70 failures |
| any-legal greedy | 39 failures |

---

## 7. What remains to prove

**One statement.**

> **Depth theorem (open).** Every reachable legal CR state with
> $\lvert R \rvert \ge 3$ is live.

It would reduce CRI — hence Conjecture 2 — to a **bounded** problem: play any
legal assignment while more than three chores remain, then complete the last
three. No rule is needed anywhere else in the induction.

This is a different shape of target from `conj:balance-rule`. That asked for a
global invariant on an unbounded search. This asks for a statement with a
constant in it, and the constant is small.

**Why it is plausible.** Death requires the committed bundles to be locked into a
bad configuration, and with three or more chores still free every agent still
carries them all, so the arcs retain slack. The measured numbers are consistent:
the dead share falls by an order of magnitude from $\lvert R\rvert = 1$ to
$\lvert R\rvert = 2$ and then to zero.

**What §6.1 forces the proof to look like.** Since the doomed state there is
*optimal* — $\ell = (0,0,0)$, no subsidy at all — a proof of the depth theorem
cannot proceed by showing the state stays good. It must be an argument about
what is still *available*: with $\lvert R\rvert \ge 3$ every agent still carries
all of $R$, so for each pair $i,k$ the arc $w(i,k) = c^R_i(A_i) - c^R_i(A_k)$ is
computed against a common load of at least three chores, and the claim is that
this common load leaves enough freedom to finish. That is a statement about the
contracted instance $(D, c^R)$ of §4.1, not about $A$.

**⚠ Caveat, and it is the LEXB lesson.** The depth theorem rests on 34,543 states
across sizes with $m \le 7$. LEXB survived 227 instances and died on 368. Before
any proof effort is spent, this must be re-run at larger $m$, where
$\lvert R\rvert \ge 3$ states are far more numerous — the current corpus has only
6 states at $\lvert R\rvert = 7$. **The claim is a hypothesis, not a result.**

---

## 8. Status

**What is genuinely new.** Lemmas 1–3 and §4.3 are the first statement of
Approach 3 as an *induction on the instance* rather than a search over profiles,
and the additive collapse localises the whole difficulty in the variation of
$\beta_i$ across bundles. These stand whatever happens to the depth theorem.

**What is not close.** CRI is not pointwise, dead ends survive the change of
frame, and no rule tested reaches a terminal on every instance. The frame removes
the *known* peel dead ends but grows its own.

**Do not represent this as close to a proof of Conjecture 2.** There is still no
proof of any $n \ge 3$ case in any approach; the unconditional results remain
$n = 2$ (all $m$) and $m \le n$.

---

## 9. A corpus bug found on the way — affects earlier work

`f_capped` and `f_threshold` in `update_44/counterexample_hunt.py` had the
`rng.randrange(...)` **inside** the dict comprehension, so the cap / threshold was
redrawn for every subset $S$. The result was neither a capping nor a threshold
function, and had marginals of 2 and more — i.e. **outside the dichotomous class
this project studies**. `f_mixed` draws from both, so it was affected too.

Measured before the fix, at $m=5, n=4$ over 20 draws: capped 1,081 and threshold
1,462 non-dichotomous marginals, mixed 500; uniform, disjoint, nested and
one-heavy were clean. After the fix all seven are clean at $m \in \{4,5,6\}$.

Fixed in place (old lines commented, not deleted). **Results that used these
generators should be re-read:**

| file | what it computed | effect |
|---|---|---|
| `update_44/counterexample_hunt.py` | the adversarial counterexample hunt | searched a **larger** class than intended, so "no counterexample" still stands, but genuine capped/threshold coverage was much thinner than reported |
| `update_44/n3_cases.py` | the $n=3$ residual map, paid/unpaid characterisation | statistics partly over non-dichotomous instances — **should be re-run** |
| `update_45/n3_rules.py` | the LEXB refutation | the refutation stands (a counterexample is a counterexample only if it is in the class — **needs re-checking**) |
| `update_46/cyclebound_check.py` | the cycle-closing bound | **unaffected**: `thm:cyclebound` assumes only envy-freeability, not dichotomous costs, so running it on a wider class is stronger evidence, not weaker |

`update_47/cri_sweep.py` now asserts `is_dichotomous` on every generated
instance, so this class of error cannot recur silently.

**The fix is not only hygiene — it revealed which family is adversarial.**
Re-running the hunt with genuine generators: 0 counterexamples over 263
exhaustively searched instances, but of the 29 instances that are *one step away*
(minimum over allocations of $\max_i \ell$ equal to 1), **17 are threshold**,
against 4 nested, 3 capped and 5 mixed — and 0 uniform, disjoint or one-heavy.
Threshold costs $c(S) = \max(0, \lvert S\rvert - t)$ are where Conjecture 2 is
tightest, and before the fix that family was not being generated at all. Any
future stress test should be weighted towards it.

---

## 10. Scripts

| file | what it establishes |
|---|---|
| `update_47/cri_anchor.py` | Lemmas 1–3, the additive collapse, the first-chore proposition, and that the peel dead ends are not CR states |
| `update_47/cri_sweep.py` | the complete state-space analysis: 0 bad roots, 3 without relabelling, and the P1/P2 refutations |
| `update_47/cri_stuck.py` | the contingency tables: balance does not transplant, $(\textsc{commit})$ is backwards, free assignment is sound |
| `update_47/cri_where.py` | stuckness is confined to $\lvert R\rvert \le 2$; the four rules and their failures |
| `update_47/cri_lookahead.py` | no dead state at $\lvert R\rvert \ge 3$; $K = 3$ look-ahead suffices |
| `update_47/cri_witnesses.py` | the minimal instance for every refuted claim in §6, each re-verified |
| `update_47/diag_first.py` | the diagnostic that surfaced the generator bug |

---

## 11. The witness-carrying invariant, and the bridge to the spread line

*Added 2026-08-10, after `conj:cri-depth` fell. Written up in full in
`report/working/approach_9.tex`, §"Carrying a witness".*

Every invariant tried in this project has been a **predicate on the state**, and
every one has died. `ex:cri-deadend` explains why and kills the whole family at
once: the state to be avoided has $\ell = (0,0,0)$ — **optimal** — so no measure
of the current state's quality can separate it from a live one. The standard
response is a stronger induction hypothesis: carry a witness.

**Definition.** A *completion* of $(A,R)$ is a full allocation $A^\star$ with
$A_i \subseteq A^\star_i$; it is *good* if $\ell_{A^\star} \le 1$. Put
$\Phi(A,R) :\iff$ "$(A,R)$ legal and some completion is good".

- **Root**: $\Phi$ holds iff Conjecture 2 holds for the instance. **Terminal**:
  $\Phi$ holds iff the state is good. **Soundness**: by definition. So progress
  is the whole content.
- **$\Phi$ survives `ex:cri-deadend`.** All three placements of the last chore
  there create positive cycles, so that state has no good completion and $\Phi$
  excludes it. Every predicate eliminated in `BALANCE_RULE.md` §8 and in §6 above
  was satisfied by some dead state. **This is the first candidate invariant the
  standing counterexample does not dispose of.**
- **Pure witness-following is refuted.** Such a rule would give an
  assignment-only schedule by induction on $|R|$, contradicting the **3
  assignment-only bad roots** in the exhaustive $n{=}m{=}3$ family. So
  relabelling is unavoidable and the carried target must be allowed to move.

### The bridge

Lemma 2 says a CR state is a witness on the contracted instance; Lemma 1 says
that instance is again dichotomous; and in the CR frame **relabelling *is* the
choice of assignment**, so a minimum-cost labelling may always be selected. With
$\Sigma^R(A) := \sum_i \big[\max_t c^R_i(A_t) - \min_t c^R_i(A_t)\big]$:

> **Bridge Theorem.** At $n = 3$, if $\Sigma^R(A) \le 3$ then every labelling of
> $A$ minimising $\sum_i c^R_i(A_{\sigma(i)})$ is legal.

*Proof.* Apply Lemma A of `RESIDUAL.md` §7.3 to the contracted instance
$(D, c^R)$, legitimate by Lemmas 1 and 2. $\square$

**This is the first point at which the two lines meet** — the spread line's
theorem becomes the soundness clause of the CR induction.

**Base case, and it agrees with what was already proved.** From the root,
assigning any $a$ gives values $(\beta_i,0,0)$ with
$\beta_i = c_i(M) - c_i(M\setminus a)$, so $\Sigma^{R'} = \sum_i \beta_i \le 3$
*always*; and the minimum-cost labelling hands $\{a\}$ to an agent of minimal
$\beta$ — exactly the first-chore proposition of §4.3.

### What is left, and what it costs

Candidate invariant $\Phi_\Sigma(A,R) :\iff \Sigma^R(A) \le 3$. Root free
($\Sigma = 0$), soundness by the Bridge Theorem, terminal gives a good allocation
— i.e. **Conjecture 2 at $n=3$**. One clause remains:

> **Progress (open).** If $\Sigma^R(A) \le 3$ and $R \ne \emptyset$, then some
> legal labelling of $A$, some $a \in R$ and some bundle give a family with
> $\Sigma^{R'} \le 3$ whose induced labelling is legal.

⚠ **The labelling is not a detail.** Every state *visited* must be legal, so one
may not assign and then relabel — the un-relabelled state is visited, and a
relabelling is a single move between two states both of which must be legal, so
it cannot be used to escape an illegal one. Hence the quantification over
labellings.

⚠ **This route is not independent of the spread line.** At $|R| = 1$ Progress
yields a terminal family with $\Sigma \le 3$, so **Progress implies Lemma E**
(`RESIDUAL.md` §7.5). Two consequences, and they are the practical content:
Lemma E is the weaker target and should be settled first, since refuting it
refutes Progress with no further work; and if Lemma E falls, $\Phi_\Sigma$ dies
and CRI needs a different invariant — with $\Phi$ above the candidate still
standing.
