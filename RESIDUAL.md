# The residual of the solved cases, and the spread-2 line

*Status as of 2026-08-10. Companion to `BALANCE_RULE.md` (the peel frame) and
`CRI.md` (the conditioned-remainder induction).*

> **What changed.** `conj:cri-depth` is **refuted**. In its place the open
> statement is now (F5\*) of §5 — a *constructive* rule, which is a better shape
> of target than anything this project has had, and which is **not yet stressed
> enough to believe**.

---

## 1. Four solved cases, never intersected

| case | label | covers |
|---|---|---|
| S1 binary additive | `thm:binadd` | $\cost_i(S) = \lvert S \cap D_i\rvert$ |
| S2 identical costs, $n=2$ | `thm:identical` | $\cost_1 = \dots = \cost_n$ |
| S3 small bundles | `thm:smallbundle`, `cor:m-le-n` | every bundle costs $\le 1$ to everyone |
| **S4 uniformly balanced family** | `thm:balanced-class` | a partition every agent values within 1 unit |

**S4 is far stronger than the report claims.** It subsumes every *symmetric*
instance $\cost_i(S) = f_i(\lvert S\rvert)$ — a balanced partition shows agent
$i$ only $f_i(q)$ and $f_i(q+1)$, which differ by one marginal — hence the whole
threshold and capped families. Any "new theorem for symmetric costs" is already
done.

**The open part of Conjecture 2 is the intersection of the four complements**,
and nobody had mapped it. Note `prop:no-balance`'s instance, the only known one
with no uniformly balanced family, is *binary additive* and so sits inside S1: it
refutes the method of Approach 5 without being residual at all.

## 2. The residual is empty under random generation

Over **550 random instances** across all seven generators, $n \le 6$, $m \le 8$:
S1 covered 177, S2 38, S3 292 — and **S4 covered 550 of 550**. Residual: **0**.
No sampler this project has ever used produces a residual instance
(`update_48/residual_map.py`).

## 3. Why — and how to construct one anyway

For an **additive** cost the total over any partition is fixed,
$\sum_t \cost_i(B_t) = \cost_i(\items)$, so "every bundle within one unit" pins
each bundle to $\cost_i(\items)/n$ exactly: a rigid discrepancy constraint with
no slack. For a non-additive cost the total *varies* with the partition —
supermodular costs get cheaper when split, submodular ones dearer — so there is
always slack.

> **Additivity is exactly what makes uniform balance hard.** That is why the one
> known witness is additive, and why it is already solved.

So a residual instance needs a cost that keeps additivity's rigid balance
constraint while not being additive. **Capping does it**: over three bundles both
$\lvert S \cap D\rvert$ and $\min(\lvert S\cap D\rvert, 2)$ force the pattern
$(1,1,1)$, but the second has a zero marginal.

**The construction works.** With $\items=\{a,b,c,d\}$, $D_1=\{a,b\}$,
$D_2=\{a,c,d\}$, $D_3=\{b,c,d\}$ and $\cost_3 = \min(\lvert S\cap D_3\rvert,2)$:
S1–S4 all fail. **The first residual instance ever exhibited.**

Exhaustively over the *composed* family $\cost_i(S) = f_i(\lvert S\cap D_i\rvert)$
at $n{=}3, m{=}4$: 52,390 instances, **46 residual**, Conjecture 2 holding on all
(`update_48/residual_hunt.py`). Density elsewhere: 0.023% at $n{=}3,m{=}5$,
0.487% at $n{=}4,m{=}5$, 0 at $n{=}4,m{=}4$ and $n{=}3,m{=}6$.

**Structure** — of the 46: 18 have one binary-additive agent, 24 have two, and
**4 have none**, so the residual is not merely "additive plus capping". The
multiset of $\lvert D_i\rvert$ is always $(2,3,3)$ or $(3,3,3)$: the
`prop:no-balance` discrepancy skeleton.

**CRI reaches it.** 0 bad roots on all 46 — the frame works exactly where the
four theorems fail (`update_48/residual_attack.py`).

## 4. `conj:cri-depth` is refuted

CRI.md §7 conjectured that every reachable legal CR state with
$\lvert R\rvert \ge 3$ is live, flagged as resting on only 6 states at
$\lvert R\rvert = 7$. It is false. Dead states with $\lvert R\rvert \ge 3$:

| family | $m{=}6$ | $m{=}7$ | $m{=}8$ |
|---|---|---|---|
| composed | 7 | 243 | 137 |
| capped | 60 | 210 | 0 |
| threshold | 0 | 0 | 0 |
| nested | 0 | 0 | 0 |

All failures are on **composed** and **capped** — and capped had never been
correctly generated before the 2026-08-09 generator fix. `CRI.md` §7 and
`report/working/approach_9.tex` still present this as open and **are stale on
that point** (`update_48/depth_stress.py`; the $n\ge4$ blocks did not finish).

## 5. The spread-2 line

`thm:balanced-class` is the spread-$\le 1$ case: uniform balance gives every arc
$\ge -1$, and `cor:onestep` reads $\pathw{} \le 1$ off it. `rem:smallbundle-scope`
asks what happens at spread 2, where `thm:cyclebound` gives only
$\pathw{} \le 2$ and the argument stops. `rem:arc-vs-path` proves any correct
certificate must be **path-based**. So the natural next statement is

> **(F5)** every instance admits a family of spread $\le 2$ whose
> maximum-weight matching has $\pathw{} \le 1$.

### What holds

- **(A) minimum spread $\le 2$**, over 9,640 hard-core instances and a further
  558 in the $m \gg n$ regime up to $m/n = 4.3$ — the regime where a random
  partition would deviate by $\sqrt{\lvert D_i\rvert/n} > 2$ and where nothing
  had ever been tested. **0 failures.**
- **(B)** on the 91 instances of minimum spread exactly 2, a minimum-spread
  family's maximum-weight matching is good — **91/91**, plus 92/92 on the
  residual instances of §3.

### What fails — and it reshapes the statement

**(F5) is *not* `thm:balanced-class` with 1 replaced by 2.** On instances of
minimum spread 2, only **85.8%** of spread-$\le2$ families have a good matching
(36,648 of 42,711), and only 3 of 60 instances have *every* such family work.
Since those instances have minimum spread 2, every family examined already **is**
a minimum-spread family, so **minimality is not the selector either**. Bare (F5)
is an existence claim with no construction.

### The rule that does select

Over 42,711 families, tested as sufficient conditions (no false positives):

| predicate | good | bad | sufficient | exists on |
|---|---|---|---|---|
| nonempty bundles | 25,308 | 1,080 | no | 70/70 |
| **balanced sizes** | 24,276 | **792** | **no** | 70/70 |
| $\le 1$ agent at spread 2 | 5,802 | **0** | yes | 66/70 |
| **min. agents at spread 2** | 6,666 | **0** | **yes** | **70/70** |
| **min. total spread** | 4,770 | **0** | **yes** | **70/70** |

Balance is **not** sufficient — 792 counterexamples — so the `rem:balance` signal
that three routes pointed at does not survive here either. What does:

> **(F5\*)** Let $B$ minimise
> $\sum_i \big[\max_t \cost_i(B_t) - \min_t \cost_i(B_t)\big]$ over all families.
> Assign $B$ by a maximum-weight matching. Then $\pathw{} \le 1$.

A minimiser exists by definition, so this **always applies** and is
**constructive** — the first target in this project with both properties. It also
explains `thm:balanced-class`, a uniformly balanced family having small total
spread.

### It survived the test designed to kill it

The sample that *produced* (F5\*) was doubly selected — only minimum-spread-2
instances, only $n \le 4$, $m \le 6$ — which is the exact profile of two rules
this project has already lost. LEXB was perfect on 227 residual instances and
died on 368 (`rem:n3-rules-fail`); `conj:balance-rule` survived 305 instances
from one uniform sampler and its certificate then failed outright in the CR
frame, and fails here too (§5, 792 counterexamples).

So (F5\*) was re-run on a corpus **not selected for it**:

> **2,574 instances, $n$ up to 6, $m$ up to 8, all 11 generators —
> 0 failures, in the STRONG form: *every* minimiser of the total spread has a
> good maximum-weight matching, not merely some.**
> Control: 0 Conjecture 2 failures. (`update_48/minsum_stress.py`)

The sibling rule (minimise the number of agents attaining the maximum spread)
also has 0 failures. Together with the 4,770 families of the selected sample,
(F5\*) has not failed once.

**(F5\*) implies Conjecture 2**, immediately: the allocation it produces has
$\pathw{} \le 1$, and `obs:integrality` upgrades that to
$\optsubsidy \in \set{0,1}^n$ with total at most $n-1$. It is the first target in
this project that is simultaneously *constructive*, *always applicable*, and
*unrefuted*.

### ⚠ What is still missing

- **It is unproved.** No argument is offered here, only evidence.
- The *computational* clause of Conjecture 2 does **not** follow: finding a
  minimum-total-spread family is itself a search over partitions. (F5\*) would
  settle existence, not polynomial time.
- $n \le 6$ and $m \le 8$. The $m \gg n$ regime is tested only for (A), up to
  $m/n = 4.3$.
- A subtlety not yet examined: minimising the *sum* can buy a low total by
  giving one agent spread 3 while others sit at 0, and there
  `thm:cyclebound` yields only $\pathw{} \le 3$. It still worked every time, and
  why is not understood.

## 6. What is refuted — do not retry

| claim | why it died |
|---|---|
| `conj:cri-depth` | 657 dead states with $\lvert R\rvert \ge 3$ on composed and capped |
| a new theorem for symmetric costs | already inside `thm:balanced-class` |
| the residual is empty | 46 instances at $n{=}3,m{=}4$ by construction |
| (F5) as "any spread-2 family works" | 6,063 of 42,711 families fail |
| minimality of spread as the selector | every family tested was already minimum-spread |
| **balanced sizes as the selector** | 792 counterexamples |
| nonempty bundles as the selector | 1,080 counterexamples |

## 7. Towards a proof at $n = 3$

Mathematics only — nothing in this section rests on a sweep. Throughout, $n=3$,
the family is $B = (B_1,B_2,B_3)$ and $\sigma$ is a minimum-cost assignment.

### 7.1 Normalisation

Put $v_i(t) := \cost_i(B_t) - \min_s \cost_i(B_s)$, so each $v_i \ge 0$ attains
the value $0$. Then

- $\mathrm{sp}_i(B) = \max_t v_i(t)$, hence $\Sigma(B) = \sum_i \max_t v_i$;
- $\edgew{}(i,k) = v_i(\sigma(i)) - v_i(\sigma(k))$, so the envy graph depends
  only on the $v_i$;
- $\sum_i \cost_i(B_{\sigma(i)}) = \sum_i v_i(\sigma(i)) + \text{const}$, so a
  minimum-cost $\sigma$ **minimises $\sum_i v_i(\sigma(i))$**.

Write $x_i := v_i(\sigma(i))$ — what agent $i$ pays, normalised — and
$F(\sigma) = \sum_i x_i$.

### 7.2 A criterion for goodness

> **Observation 1.** The heaviest arc out of $i$ equals $x_i$ when $x_i \ge 1$,
> and is $\le 0$ when $x_i = 0$.

*Proof.* $\max_{k \ne i}\edgew{}(i,k) = x_i - \min_{k\ne i} v_i(\sigma(k))$. If
$x_i \ge 1$ then $v_i$'s zero is not at $\sigma(i)$, so the inner minimum is $0$.
If $x_i = 0$ then $\edgew{}(i,k) = -v_i(\sigma(k)) \le 0$. $\square$

Minimum-cost matching makes $\alloc$ envy-freeable
(`thm:hs-characterisation`), so `prop:n3` applies and goodness is: every arc
$\le 1$, and every two-path $\le 1$. With Observation 1:

> **Proposition 2 ($n=3$ criterion).** $\alloc$ is good if and only if
> **(a)** $x_i \le 1$ for every $i$, and **(b)** there are no distinct $i,j,k$
> with $x_i = x_j = 1$, $v_i(\sigma(j)) = 0$ and $v_j(\sigma(k)) = 0$.

*Proof.* (a) is "every arc $\le 1$" by Observation 1. Given (a), a two-path
$i \to j \to k$ has weight $2$ iff both arcs weigh $1$, i.e.
$x_i - v_i(\sigma(j)) = 1$ and $x_j - v_j(\sigma(k)) = 1$, which under (a) is
exactly (b). $\square$

### 7.3 Lemma A — $\Sigma \le 3$ needs no family minimality

> **Lemma A.** At $n = 3$, for any minimum-cost assignment:
> **(i)** an arc of weight $\ge 2$ forces $\Sigma(B) \ge 4$;
> **(ii)** all arcs $\le 1$ but a two-path of weight 2 forces $\Sigma(B) \ge 5$.
> In particular $\Sigma(B) \le 3$ implies **every** minimum-cost assignment of
> $B$ is good.

*Proof.* **(i)** Say $x_i \ge 2$. Since $x_i > 0$, $v_i$'s zero sits on
$\sigma(k)$ for some $k \ne i$. Transposing $i$ and $k$ changes $F$ by
$\big[v_i(\sigma(k)) + v_k(\sigma(i))\big] - \big[x_i + x_k\big]
= v_k(\sigma(i)) - x_i - x_k \ge 0$, so $v_k(\sigma(i)) \ge x_i + x_k \ge 2$ and
$\mathrm{sp}_k \ge 2$. With $\mathrm{sp}_i \ge x_i \ge 2$, $\Sigma \ge 4$.

**(ii)** Here $x_i = x_j = 1$, $v_i(\sigma(j)) = 0$, $v_j(\sigma(k)) = 0$, and
$F = 2 + x_k$. Transposing $i,j$ costs $v_j(\sigma(i)) + x_k$, so
$v_j(\sigma(i)) \ge 2$ and $\mathrm{sp}_j \ge 2$. The **three-cycle**
$i \mapsto \sigma(j),\ j \mapsto \sigma(k),\ k \mapsto \sigma(i)$ costs
$v_i(\sigma(j)) + v_j(\sigma(k)) + v_k(\sigma(i)) = v_k(\sigma(i))$, so
$v_k(\sigma(i)) \ge 2 + x_k \ge 2$ and $\mathrm{sp}_k \ge 2$. With
$\mathrm{sp}_i \ge 1$, $\Sigma \ge 1+2+2 = 5$. $\square$

*(The three-cycle in (ii) is what pushes the two-path mode from $\ge 4$ to
$\ge 5$; the transposition alone gives only $\mathrm{sp}_k \ge 1$. This is why
the $\Sigma = 4$ obstruction of §7.6 is unique.)*

Note what this does **not** use: no family minimality, no balance, no exchange.
It is pure matching optimality, so it sidesteps all three closures of §5.

### 7.4 Lemma A already re-proves `thm:balanced-class`

If a uniformly balanced family exists then every $\mathrm{sp}_i \le 1$, so
$\Sigma \le 3$ and Lemma A applies. So Lemma A **contains** `thm:balanced-class`
and is strictly wider: it also covers spread profiles such as $(2,1,0)$ and
$(3,0,0)$, which are not uniformly balanced. This is the specialisation check of
the plan's Step 8, discharged.

### 7.5 The reduction

> **Corollary 3.** (F5\*) holds at $n=3$ for every instance admitting a family
> with $\Sigma \le 3$.

*Proof.* The $\Sigma$-minimal family then has $\Sigma \le 3$; apply Lemma A.
$\square$

So the whole of (F5\*) at $n=3$ reduces to the purely combinatorial

> **Lemma E (open).** Every three-agent dichotomous instance admits a partition
> into three bundles with $\sum_i \mathrm{sp}_i \le 3$.

### 7.6 If Lemma E fails: the one bad pattern at $\Sigma = 4$

By Lemma A(ii) a two-path failure needs $\Sigma \ge 5$, so at $\Sigma = 4$ the
only failure is an arc of weight 2. Running the optimality conditions to
equality — against $i\!\leftrightarrow\!k$, $i\!\leftrightarrow\!j$ and the
three-cycle $i\mapsto\sigma(k),\,j\mapsto\sigma(i),\,k\mapsto\sigma(j)$ — forces,
in coordinates $(\sigma(i),\sigma(j),\sigma(k))$,

$$v_i = v_k = (2,2,0), \qquad v_j = (0,0,0).$$

Agents $i$ and $k$ have **identical** normalised vectors: both see two heavy
bundles and one light one, and $j$ is indifferent. Every minimum-cost $\sigma$
then strands one of $i,k$ on a heavy bundle. Ruling this out requires
re-partitioning the two heavy bundles so as to balance $i$ and $k$ together —
which is Lemma D below.

### 7.7 The exchange lemmas

> **Lemma B (intermediate value).** For dichotomous $\cost$ and
> $Y \subseteq \items$, every integer $0 \le k \le \cost(Y)$ equals $\cost(Z)$
> for some $Z \subseteq Y$.

*Proof.* Along a maximal chain $\emptyset = Z_0 \subset \dots \subset Z_r = Y$
consecutive costs differ by $0$ or $1$, so the values sweep $[0,\cost(Y)]$.
$\square$

This supplies **set** exchange where single-item exchange is provably
unavailable (§5, closure 3).

> **Lemma C (two-way balance, one agent).** Every $U$ splits as
> $U = Z \sqcup (U \setminus Z)$ with
> $\lvert \cost(Z) - \cost(U\setminus Z)\rvert \le 1$.

*Proof.* On a maximal chain from $\emptyset$ to $U$ put
$f(t) = \cost(Z_t) - \cost(U \setminus Z_t)$. Then $f(0) = -\cost(U) \le 0$ and
$f(r) = \cost(U) \ge 0$; each step raises the first term by $0$ or $1$ and the
second by $0$ or $-1$, so $f$ increases by $0$, $1$ or $2$. A step of $2$ cannot
carry $f$ from $\le -2$ to $\ge 2$, so some $f(t) \in \{-1,0,1\}$. $\square$

> **Lemma D (two-way balance, two agents) — open.** Every $U$ splits into two
> parts on which **both** of two given dichotomous agents have spread $\le 1$.

`prop:no-balance` obstructs the *three*-agent analogue, not this one, so no
barrier is known. Lemma D is what §7.6 needs.

**Reduction of Lemma D to a monotone lattice walk.** For $Z \subseteq U$ put
$g(Z) := \big(\cost_1(Z) - \cost_1(U\setminus Z),\ \cost_2(Z) - \cost_2(U\setminus Z)\big)$.
Lemma D asks for $g(Z) \in \{-1,0,1\}^2$. Note $g(U \setminus Z) = -g(Z)$, so the
image is symmetric about the origin. Along any maximal chain
$\emptyset = Z_0 \subset \dots \subset Z_r = U$, adding one element raises
$\cost_i(Z)$ by $0$ or $1$ and lowers $\cost_i(U\setminus Z)$ by $0$ or $1$, so

> each coordinate of $g$ is **non-decreasing** along the chain, with steps in
> $\{0,1,2\}$, running from $(-\cost_1(U), -\cost_2(U))$ to
> $(\cost_1(U), \cost_2(U))$.

Lemma C is the one-coordinate case: a step of $2$ cannot carry a coordinate from
$\le -2$ to $\ge 2$, so it must land in $\{-1,0,1\}$. The two-coordinate
statement does **not** follow, because the two coordinates cross the band at
different times: at the first $t$ with $g_2(t) \ge -1$ one gets
$g_2(t) \in \{-1,0\}$, but $g_1(t)$ may already be large. **The content of
Lemma D is exactly that the chain can be chosen to synchronise the two
crossings** — and the order of the chain is free, which is the whole of the
available freedom. Note the classical necklace-splitting theorem gives this for
*additive* measures with two cuts; dichotomous costs are not additive, so it does
not transfer.

### 7.8 Is Lemma E true? A concrete reason to doubt it

On a residual instance no family has all three spreads $\le 1$, so
$\Sigma \le 3$ must be attained as $(2,1,0)$, $(2,0,0)$ or $(3,0,0)$ — **each of
which requires some agent to have spread exactly $0$**, i.e. to value all three
bundles equally.

For a binary additive agent $\cost_i(S) = \lvert S \cap D_i \rvert$, spread $0$
means the three bundles hold equally many elements of $D_i$, which is impossible
unless $3 \mid \lvert D_i \rvert$. Hence:

> **Test for refuting Lemma E.** An instance with three binary additive agents,
> no $\lvert D_i \rvert$ divisible by $3$, and no uniformly balanced family, has
> $\Sigma \ge 4$ for every partition — refuting Lemma E.

`prop:no-balance`'s own instance does *not* qualify: its sizes are $2,3,3$, and
the family $\{a,c\},\{b\},\{d\}$ gives spreads $(1,2,0)$ with $\Sigma = 3$,
agent 3 reaching spread $0$ because $\lvert D_3 \rvert = 3$ splits $(1,1,1)$.

**And the test may be unfireable — which is evidence *for* Lemma E.** The two
conditions pull against each other. Write $\lvert D_i\rvert = 3q_i + r_i$.
Uniform balance requires the counts of $D_i$ across the bundles to be
$(q_i{+}1,q_i,q_i)$ up to order when $r_i = 1$, and $(q_i{+}1,q_i{+}1,q_i)$ when
$r_i = 2$ — in both cases a *free choice of which bundle is heavy*, three
options. Only when $3 \mid \lvert D_i\rvert$ is the count vector $(q_i,q_i,q_i)$
completely rigid, and it is exactly that rigidity which `prop:no-balance`
exploits: its two size-$3$ sets are forced rainbow, and the size-$2$ set then
contradicts them. Requiring no size divisible by $3$ removes the rigidity that
makes uniform balance fail, while being precisely what is needed to block spread
$0$. So the refutation test asks for rigidity and non-rigidity at once.

This is only a heuristic, and only about binary additive agents — a general
dichotomous agent can reach spread $0$ with no divisibility condition at all
(e.g. $\cost(S) = \min(\lvert S\rvert,1)$ has spread $0$ on any partition into
non-empty bundles). But it is the reason to expect Lemma E to be true, and it
turns the question into a pure hypergraph-discrepancy problem in the sense of
`rem:discrepancy`.

**If Lemma E fails**, Corollary 3 dies but Lemma A survives, and the proof must
instead rule out the §7.6 pattern via Lemma D. **If Lemma E holds**, (F5\*) at
$n=3$ is closed outright.

### 7.9 Status

| statement | status |
|---|---|
| Observation 1, Proposition 2 | **proved** |
| **Lemma A** ($\Sigma\le3 \Rightarrow$ good) | **proved** |
| Corollary 3 (the reduction) | **proved** |
| Lemma A contains `thm:balanced-class` | **proved** |
| the $\Sigma=4$ pattern $v_i=v_k=(2,2,0)$, $v_j=0$ | **proved** |
| Lemma B, Lemma C | **proved** |
| **Lemma E** ($\min \Sigma \le 3$) | **open** — §7.8 gives the refutation test |
| **Lemma D** (two-agent balance) | **open** |

(F5\*) at $n = 3$ is **not** closed. It is reduced to Lemma E, or failing that to
Lemma D. Everything above is unconditional.

## 8. Scripts

| file | what it establishes |
|---|---|
| `update_48/residual_map.py` | the residual is empty under random generation; S4 covers 550/550 |
| `update_48/residual_hunt.py` | the capping construction; the first 46 residual instances |
| `update_48/residual_attack.py` | their structure; spread 2; CRI reaches them |
| `update_48/depth_stress.py` | `conj:cri-depth` refuted |
| `update_48/spread_conjecture.py` | ⚠ its broad test is **vacuous** — min spread was 0 or 1 on all 1,792 instances, so spread-2 was never exercised |
| `update_48/spread_hardcore.py` | (F5) on 91 generated spread-2 instances |
| `update_48/spread_scale.py` | (A) survives $m \gg n$ up to $m/n = 4.3$ |
| `update_48/spread_which.py` | not every spread-2 family works |
| `update_48/spread_rule.py` | the sufficient predicates; balance is not one |
| `update_48/minsum_stress.py` | the broad stress test of (F5\*) |
