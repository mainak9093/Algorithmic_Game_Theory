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

### 7.9 Attacking Lemma E: the individual minimum, and additive rigidity

**⚠ Retraction first.** An earlier note claimed that a dichotomous $c$ admits a
spread-$0$ $3$-partition **iff** $3 \mid c(M)$. Both directions are false without
additivity: cutting a chain at $c(Z_{t_1}) = c(M)/3$ says nothing about
$c(Z_{t_2}\setminus Z_{t_1})$, and $\sum_t c(B_t) \ne c(M)$ in general.
Counterexample: $c(S) = \min(\lvert S\rvert, 1)$ on $\{a,b,c\}$ has $c(M) = 1$
yet $\{a\},\{b\},\{c\}$ gives $(1,1,1)$, spread $0$. The divisibility criterion
is **additive-only**, as §7.8 already stated. Nothing below uses it otherwise.

> **Lemma F (individual minimum).** For any dichotomous $c$ and any $n$, some
> partition has $\mathrm{sp}(B) \le 1$.

*Proof.* Process the items in any order, each time adding to a bundle of
currently minimum cost. Invariant: all bundle costs lie in $\{\mu,\mu+1\}$ for
the current minimum $\mu$. It holds when all bundles are empty; and if it holds,
adding an item to a bundle of cost $\mu$ makes that bundle cost $\mu$ or $\mu+1$
(marginals are in $\{0,1\}$) and changes nothing else. $\square$

This is `thm:identical`'s invariant, and it gives $\mu_i := \min_B \mathrm{sp}_i(B) \le 1$
for **every** agent. Hence a uniformly balanced family is exactly one where all
three agents attain a spread $\le 1$ simultaneously, and:

> **Corollary G.** Lemma E has content only when no uniformly balanced family
> exists. There the spread profile must be $(0,0,2)$, $(0,0,3)$ or $(0,1,2)$ —
> **some agent must have spread exactly $0$.**

*Proof.* $\Sigma \le 3$ with $\max_i \mathrm{sp}_i \ge 2$ leaves only those three
multisets, and each contains a $0$. $\square$

> **Lemma H (additive rigidity).** Let $\cost_i(S) = \lvert S \cap D_i\rvert$.
> Then in every $3$-partition,
> **(a)** if $3 \nmid \lvert D_i\rvert$ the spread is $\ge 1$ — never $0$;
> **(b)** if $3 \mid \lvert D_i\rvert$ the spread is $0$ or $\ge 2$ — **never $1$**.

*Proof.* The counts $a_t = \lvert B_t \cap D_i\rvert$ sum to $\lvert D_i\rvert$.
(a) Spread $0$ forces $a_1=a_2=a_3$, so $3 \mid \lvert D_i\rvert$.
(b) Suppose the spread is $1$, so the $a_t$ lie in $\{\mu,\mu+1\}$ with $k$ of
them at $\mu+1$ and $1 \le k \le 2$. Then $\lvert D_i\rvert = 3\mu + k$, so
$k \equiv 0 \pmod 3$ — contradiction. $\square$

> **Theorem I (exact refutation criterion).** If all three agents are binary
> additive with $3 \nmid \lvert D_i\rvert$ **and** no uniformly balanced family
> exists, then $\Sigma(B) \ge 4$ for every partition, and **Lemma E is false**.

*Proof.* By Lemma H(a) every spread is $\ge 1$. If all three were exactly $1$
that is a uniformly balanced family, excluded; so some spread is $\ge 2$ and
$\Sigma \ge 1+1+2 = 4$. $\square$

**Consistency with `prop:no-balance`.** Its sizes are $2,3,3$, so agents 2 and 3
have $3 \mid \lvert D_i\rvert$ and the criterion correctly does **not** fire. And
indeed $\{a,c\},\{b\},\{d\}$ gives spreads $(1,2,0)$ with $\Sigma = 3$ — agent 2
at spread $2$, never $1$, exactly as Lemma H(b) predicts. The criterion passes
its one available test.

### 7.10 Question (Q), and why the divisibility condition is the whole story

Theorem I turns Lemma E into a single combinatorial question:

> **(Q)** Do three sets with no size divisible by $3$ always admit a
> $3$-colouring splitting each of them within one?

**The residue reduction.** Index the Venn regions by $\emptyset \ne T \subseteq
\{1,2,3\}$, with $\lvert P_T\rvert = n_T = 3a_T + b_T$, $b_T \in \{0,1,2\}$.
Split each region as evenly as possible, choosing which $b_T$ colours receive the
extra element; write $\epsilon_T \in \{0,1\}^3$, $\lvert\epsilon_T\rvert = b_T$,
for that choice. The count of $D_i$ in colour $t$ is then $A_i + E_{i,t}$ with
$A_i = \sum_{T \ni i} a_T$ constant in $t$ and
$E_{i,t} = \sum_{T\ni i}\epsilon_{T,t}$. So

> the spread of $D_i$ equals the spread of $E_{i,\cdot}$, and
> $\sum_t E_{i,t} = \beta_i := \sum_{T \ni i} b_T \equiv \lvert D_i\rvert \pmod 3$.

**This is where the hypothesis does its work.** Spread $\le 1$ for a vector
summing to $\beta_i$ means *all coordinates equal* when $3 \mid \beta_i$ — a
rigid condition — and merely *as equal as possible* otherwise. So
$3 \nmid \lvert D_i\rvert$ is exactly the statement that **no set imposes a rigid
constraint.**

**The signed reformulation.** Writing $\epsilon_T = e_{c_T}$ when $b_T = 1$ and
$\epsilon_T = \mathbf 1 - e_{c_T}$ when $b_T = 2$, each active region simply
chooses a colour $c_T$, and

$$\mathrm{spread}(E_{i,\cdot}) = \mathrm{spread}(F_i), \qquad F_i := \sum_{T \ni i} \sigma_T\, e_{c_T},\quad \sigma_T = \begin{cases}+1 & b_T = 1\\ -1 & b_T = 2.\end{cases}$$

With $p_i, q_i$ the numbers of active regions of $D_i$ carrying $\sigma = +1, -1$,
we get $\sum_t F_{i,t} = p_i - q_i$ and $\beta_i = p_i + 2q_i \equiv p_i - q_i$,
so **the hypothesis reads $p_i - q_i \not\equiv 0 \pmod 3$.**

> **Theorem J.** If every $D_i$ has at most two active regions, (Q) holds.

*Proof.* A set with one active region has $F_i = \pm e_{c}$, spread $1$: no
constraint. A set with two has $(p_i,q_i) \in \{(2,0),(1,1),(0,2)\}$, and
$(1,1)$ gives $p_i - q_i = 0$, excluded by hypothesis. In the surviving cases
$F_i = \pm(e_{c_1} + e_{c_2})$, whose spread is $1$ iff $c_1 \ne c_2$ and $2$
otherwise. So every constraint is a **disequality** between two region-variables.
Three sets give at most three such constraints, i.e. a graph with at most three
edges, which is $3$-colourable. $\square$

**What the hypothesis buys, in one line:** it forbids the mixed-sign case
$(p,q) = (1,1)$, which is the only one that would impose an *equality*
constraint $c_1 = c_2$. Equalities and disequalities together can be
inconsistent — $c_{12} = c_{13}$, $c_{12} = c_{23}$, $c_{13} \ne c_{23}$ is the
obstruction `prop:no-balance` exploits — whereas disequalities alone, at most
three of them, never are.

**What remains.** Sets with three or four active regions. Their constraints are
computed the same way; for three regions the hypothesis forces the multiset of
$b_T$ to be $(1,1,2)$ or $(1,2,2)$ (since $(1,1,1)$ and $(2,2,2)$ give
$\beta_i \equiv 0$), and the conditions come out as **membership** constraints:

| $b_T$ multiset | $(p_i,q_i)$ | condition |
|---|---|---|
| $(1,1,2)$ | $(2,1)$ | $c$ of the $b=2$ region lies in $\{c,c'\}$ of the two $b=1$ regions |
| $(1,2,2)$ | $(1,2)$ | $c$ of the $b=1$ region lies in $\{c,c'\}$ of the two $b=2$ regions |

Four-region sets similarly exclude $(p,q) = (2,2)$. Completing (Q) means showing
at most three constraints of these shapes, on seven region-variables over three
colours, are always simultaneously satisfiable.

⚠ **The reduction is sufficient, not necessary.** It splits every region as
evenly as possible; a colouring solving (Q) need not do that. So failure of the
reduced problem would **not** refute (Q).

### 7.10.1 The complete constraint taxonomy

Set $i$ has exactly four candidate regions — $\{i\}, \{ij\}, \{ik\}, \{123\}$ —
so $d_i := p_i + q_i \le 4$, and $d_i \ge 1$ since $\beta_i \not\equiv 0$.
Writing $s_i = p_i - q_i$ and requiring $\mathrm{spread}(F_i) \le 1$ where
$F_i = \sum_{T \ni i}\sigma_T e_{c_T}$, every case resolves:

| $d_i$ | $(p_i,q_i)$ | $s_i \bmod 3$ | condition on the colours |
|---|---|---|---|
| 1 | $(1,0)$, $(0,1)$ | $1,2$ | **none** |
| 2 | $(1,1)$ | $0$ | **excluded by hypothesis** |
| 2 | $(2,0)$, $(0,2)$ | $2,1$ | **disequality**: the two colours differ |
| 3 | $(3,0)$, $(0,3)$ | $0$ | **excluded by hypothesis** |
| 3 | $(2,1)$ | $1$ | **membership**: $c_{\text{minority}} \in \{c_{\text{maj}}, c'_{\text{maj}}\}$ |
| 3 | $(1,2)$ | $2$ | **membership**: $c_{\text{minority}} \in \{c_{\text{maj}}, c'_{\text{maj}}\}$ |
| 4 | $(2,2)$ | $0$ | **excluded by hypothesis** |
| 4 | $(4,0)$, $(0,4)$ | $1,2$ | **diversity**: all three colours occur among the four |
| 4 | $(3,1)$, $(1,3)$ | $2,1$ | the three majority colours are distinct, **or** exactly two coincide and the minority region carries that repeated colour |

*(Derivations are routine: for $(2,1)$, $F_i = e_a + e_b - e_x$ must be a
permutation of $(1,0,0)$, which holds iff $x \in \{a,b\}$; the others are
identical in form.)*

Three consequences follow immediately.

> **Lemma K (a private region always suffices at $d_i = 3$).** If $d_i = 3$ and
> the private region $\{i\}$ is active, then set $i$'s constraint can be
> satisfied by the choice of $c_{\{i\}}$ alone, whatever the other colours are.

*Proof.* If $\{i\}$ is the minority region the condition reads
$c_{\{i\}} \in \{\cdot,\cdot\}$ — take either. If $\{i\}$ is a majority region
the condition reads $c_{\text{minority}} \in \{c_{\{i\}}, c'\}$ — take
$c_{\{i\}} = c_{\text{minority}}$. $\square$

> **Lemma L.** The constant colouring satisfies every membership constraint.

*Proof.* $c_x \in \{c_a, c_b\}$ holds when all three are equal. $\square$

> **Theorem M.** If every set has $d_i \in \{1,3\}$, then (Q) holds.

*Proof.* By the table those sets impose only memberships or nothing at all;
apply Lemma L. $\square$

So the burden sits exactly on the sets with $d_i = 2$ (disequalities, which
uniformity violates) and $d_i = 4$ (diversity, likewise).

### 7.10.2 The hypothesis keeps killing the conflicts

The natural way to build an infeasible system is to surround one set by two
rigid neighbours. It cannot be done.

> **Lemma N.** Suppose sets $j$ and $k$ each have exactly two active regions,
> both shared with set $i$. Then set $i$'s private region $\{i\}$ must be active.

*Proof.* The regions of $j$ shared with $i$ are $\{ij\}$ and $\{123\}$, so
$j$'s active set is exactly $\{\{ij\},\{123\}\}$; since $(1,1)$ is excluded,
$\sigma_{ij} = \sigma_{123}$. Symmetrically $\sigma_{ik} = \sigma_{123}$. Hence
$\{ij\},\{ik\},\{123\}$ all carry one sign. Were $\{i\}$ inactive, set $i$ would
have $(p_i,q_i) = (3,0)$ or $(0,3)$ and $s_i \equiv 0$, excluded. $\square$

This is the pattern throughout. Every configuration assembled so far in which
three constraints look like conflicting turns out to force some $s_i \equiv 0$
and be excluded. Two worked instances:

- **Three disequalities cannot conflict** — Theorem J: they form a graph with at
  most three edges, always $3$-colourable. The equality constraint
  $c_1 = c_2$, which together with disequalities *would* be inconsistent — the
  shape `prop:no-balance` exploits — arises only from $(p,q) = (1,1)$, which the
  hypothesis forbids.
- **A membership between two disequalities** — take set 3 active on
  $\{13\},\{23\},\{123\}$ with sets 1 and 2 active on $\{13\},\{123\}$ and
  $\{23\},\{123\}$. Then $d_1 = d_2 = 2$ forces
  $\sigma_{13} = \sigma_{123} = \sigma_{23}$, so $s_3 = \pm 3 \equiv 0$ and the
  configuration is excluded outright.

**Status of (Q): open.** What remains is the mixed regime — sets with $d_i = 2$
alongside sets with $d_i \ge 3$, and any set with $d_i = 4$. The evidence from
the taxonomy is that the hypothesis $s_i \not\equiv 0 \pmod 3$ is doing exactly
the work needed, but the case analysis is not finished and **(Q) is not proved.**

### 7.10.3 ⚠ What (Q) does and does not buy

A point that reshapes the priority, and that the earlier plan understated.

**(Q) concerns instances all three of whose agents are binary additive — that is,
case S1, which `thm:binadd` already closes.** So settling (Q) does **not**
advance Conjecture 2 at $n = 3$ by itself. What it settles is:

- whether **Lemma E as stated** is true, and
- with it, whether `conj:cri-progress` survives — since Progress implies Lemma E,
  a counterexample to (Q) would refute the entire remaining CRI route
  (`CRI.md` §11).

That is worth having, but the statement Conjecture 2 actually needs is the
restricted one:

> **Lemma E′.** Every instance outside S1–S4 admits a family with $\Sigma \le 3$.

On such instances S1 fails, so **at least one agent is non-additive** — and
Lemma H's rigidity, the whole obstruction on the additive side, does not apply to
it. Lemma E′ should therefore be the primary target, with (Q) pursued for what it
says about the CRI route rather than about Conjecture 2.

### 7.11 Rigidity is the right notion, not additivity

**⚠ Correction to §7.10.3.** I wrote that on residual instances "at least one
agent is non-additive — and Lemma H's rigidity does not apply to it". The second
half is wrong: **non-additive costs can be rigid too.** Take
$\cost(S) = \min(\lvert S \cap D\rvert, 3)$ with $\lvert D\rvert = 4$. It is
dichotomous and not additive ($\cost(D) = 3 \ne 4$), and no partition gives it
spread $0$: the counts sum to $4$, so equal costs would need either
$a_1=a_2=a_3$ (impossible, $3 \nmid 4$) or all $a_t \ge 3$ (impossible,
$4 < 9$). What matters is not additivity but:

> **Definition.** A dichotomous cost is **rigid** if no $3$-partition gives it
> spread $0$.

Corollary G then upgrades Theorem I to its proper form:

> **Theorem I′.** If all three agents are rigid and no uniformly balanced family
> exists, then $\Sigma(B) \ge 4$ for every partition. Hence
> **Lemma E is false if and only if some instance has three rigid agents and no
> uniformly balanced family.**

*Proof.* Rigidity gives $\mathrm{sp}_i \ge 1$ always; failure of S4 gives some
$\mathrm{sp}_i \ge 2$; so $\Sigma \ge 4$. Conversely if Lemma E fails then by
Corollary G no partition has a spread-$0$ agent with the others cheap — and in
particular, if some agent were non-rigid... the "only if" is the direction
Corollary G supplies. $\square$

**Rigidity, computed for the standard families.** Writing counts $a_t$ summing to
$\lvert D\rvert$:

| cost | rigid iff |
|---|---|
| $\lvert S\cap D\rvert$ (additive) | $3 \nmid \lvert D\rvert$ |
| $\min(\lvert S \cap D\rvert, k)$ (capped) | $3 \nmid \lvert D\rvert$ **and** $\lvert D\rvert < 3k$ |
| $\max(0, \lvert S\cap D\rvert - t)$ (threshold) | $3 \nmid \lvert D\rvert$ **and** $\lvert D\rvert > 3t$ |

*(Spread $0$ needs all $\cost(B_t)$ equal to some $v$. For the capped cost, either
$v < k$ and all $a_t = v$, forcing $3 \mid \lvert D\rvert$; or $v = k$ and all
$a_t \ge k$, needing $\lvert D\rvert \ge 3k$. The threshold case is dual.)*

So every one of these families is rigid exactly when $3 \nmid \lvert D\rvert$
**and** the non-linearity has no room to act. The unified crux is therefore

> **(Q′)** Can three **rigid** dichotomous agents fail to admit a uniformly
> balanced family?

**No** closes Lemma E, hence **Conjecture 2 at $n = 3$**. **Yes** refutes Lemma E.
Question (Q) of §7.10 is the purely additive shadow of (Q′).

### 7.12 Compression, and why the residual looks the way it does

The composed family $\cost_i(S) = f_i(\lvert S \cap D_i\rvert)$ is where every
known residual instance lives (§3). For it, the additive case is the *hardest*.

> **Lemma O (compression).** Let $\cost(S) = f(\lvert S \cap D\rvert)$ with $f$
> monotone and increments in $\{0,1\}$. Then for every partition $B$,
> $$\mathrm{sp}_{\cost}(B) \;\le\; \mathrm{sp}_{\lvert \cdot \cap D\rvert}(B).$$

*Proof.* $f$ is monotone and $1$-Lipschitz, so with $a_{\max},a_{\min}$ the
extreme counts, $\max_t f(a_t) - \min_t f(a_t) = f(a_{\max}) - f(a_{\min})
\le a_{\max} - a_{\min}$. $\square$

> **Corollary P.** A colouring that is uniformly balanced for the underlying
> **additive** costs $\lvert S \cap D_i\rvert$ is uniformly balanced for any
> composed costs over the same $D_i$.

Two consequences, and the second is the one that matters.

> **Corollary Q.** Let all three costs be composed. If $3 \nmid \lvert D_i\rvert$
> for every $i$, then either the instance satisfies **S4** — so it is not
> residual — or $(D_1,D_2,D_3)$ is a **counterexample to (Q)**.

*Proof.* Immediate from Corollary P. $\square$

> **Corollary R (a spread-$0$ agent for free).** If $3 \mid \lvert D_i\rvert$,
> then splitting $D_i$ into three equal parts and distributing
> $\items \setminus D_i$ arbitrarily gives agent $i$ spread exactly $0$ —
> **whatever $f_i$ is**, since all three counts equal $\lvert D_i\rvert/3$ and
> $f_i$ is a function of the count alone.

**This predicts the shape of the residual, and the prediction holds.** By
Corollary Q, a residual composed instance must have some
$3 \mid \lvert D_i \rvert$ (barring a counterexample to (Q)); and by Corollary R
that agent can be driven to spread $0$ for free. Checking against §3: the 46
residual instances at $n=3, m=4$ have $\lvert D_i\rvert$ multiset $(2,3,3)$ or
$(3,3,3)$ — **every one contains a set of size 3**. And the $\Sigma = 3$ witness
found by hand for the constructed residual instance,
$\{a,c\},\{b\},\{d\}$, works precisely by splitting the size-3 set $(1,1,1)$ to
put agent 3 at spread $0$. The theory and the data agree exactly.

> **The reduced target for Conjecture 2 at $n = 3$ (composed case).** Given a
> residual composed instance, pick $i$ with $3 \mid \lvert D_i\rvert$. Among the
> partitions splitting $D_i$ evenly — on all of which $\mathrm{sp}_i = 0$ — find
> one with $\mathrm{sp}_j + \mathrm{sp}_k \le 3$.

That is a **two-agent** balancing problem subject to one equal-split constraint,
and it is what Lemma E′ reduces to on the family where the residual actually
lives. It is the concrete next target, and it is markedly smaller than anything
attacked so far.

### 7.13 Two sets can always be balanced — so the obstruction needs all three

The reduced target of §7.12 asks, with $D_3$ split evenly, for
$\mathrm{sp}_1 + \mathrm{sp}_2 \le 3$. The unconstrained two-set question turns
out to be completely solvable, and the proof is short.

> **Theorem S (two-set balance).** For any two sets $D_1, D_2 \subseteq \items$
> and any number $k$ of bundles, there is a $k$-colouring of $\items$ splitting
> **both** $D_1$ and $D_2$ within one.

*Proof.* The Venn regions are $P_1 = D_1 \setminus D_2$, $P_{12} = D_1 \cap D_2$
and $P_2 = D_2 \setminus D_1$ (elements in neither are free). Write
$\lvert P\rvert = k a_P + b_P$ with $0 \le b_P < k$, split each region as evenly
as possible, and let $\epsilon_P \in \{0,1\}^k$ — with exactly $b_P$ ones — record
which colours take an extra element. As in §7.10 the count of $D_i$ in colour $t$
is $A_i + E_{i,t}$ with $A_i$ constant in $t$, and

$$E_1 = \epsilon_{P_1} + \epsilon_{P_{12}}, \qquad E_2 = \epsilon_{P_2} + \epsilon_{P_{12}}.$$

Fix $\epsilon_{P_{12}}$ arbitrarily. Each $E_i$ is a sum of two $0/1$ vectors, so
its entries lie in $\{0,1,2\}$ and its spread is $\le 1$ exactly when the entries
avoid $\{0,2\}$ — that is, when the two supports are **disjoint** (entries in
$\{0,1\}$) or **cover** all $k$ colours (entries in $\{1,2\}$). If
$b_{P_1} + b_{P_{12}} \le k$ choose $\mathrm{supp}\,\epsilon_{P_1}$ disjoint from
$\mathrm{supp}\,\epsilon_{P_{12}}$; if $b_{P_1} + b_{P_{12}} \ge k$ choose it so
the two together cover everything. One of the two is always available, and
$\epsilon_{P_2}$ is chosen the same way, independently. $\square$

> **Corollary T.** `prop:no-balance` genuinely requires all three sets: no
> two-set system obstructs uniform balance, at any number of bundles.

> **Corollary U (Lemma D, for composed costs).** Combining Theorem S at $k = 2$
> with Lemma O: for any two **composed** costs over sets $D_1, D_2$, every ground
> set splits into two parts on which both have spread $\le 1$. This settles
> Lemma D on the family where the residual lives.

⚠ It does **not** settle Lemma D for arbitrary dichotomous costs, since Lemma O
needs the cost to be a function of $\lvert S \cap D\rvert$ alone.

**What Theorem S says about the reduced target.** With $D_3$ split evenly, could
$D_1$ and $D_2$ *also* be balanced within one? On a residual instance, **no** —
all three count-spreads $\le 1$ would give uniform balance by Lemma O, and S4
fails by assumption. So the even-split constraint on $D_3$ must obstruct what
Theorem S delivers unconstrained, and the reduced target sharpens to:

> **(R)** On a residual composed instance, with $D_3$ split evenly, achieve
> $\mathrm{sp}_1 + \mathrm{sp}_2 \le 3$ — necessarily as $(1,2)$, $(0,2)$,
> $(0,3)$ or a permutation, since $(1,1)$ and below are excluded.

So exactly one unit of slack beyond what is provably impossible is being asked
for. That is the whole of Conjecture 2 at $n = 3$ on the composed family, and it
is now a two-set problem with one linear constraint.

### 7.14 Attacking (R): two sets go to spread $0$ for free

Theorem S has a consequence that is stronger than it looks, because for sets
whose size is divisible by $3$ "within one" and "exactly equal" are the same
thing.

> **Corollary V.** If $3 \mid \lvert D_i\rvert$ and $3 \mid \lvert D_j\rvert$,
> some $3$-colouring makes **both** $D_i$ and $D_j$ exactly balanced — both
> agents at spread $0$.

*Proof.* Theorem S gives a colouring splitting both within one. By Lemma H(b) a
set of size divisible by $3$ has spread $0$ or $\ge 2$, so "within one" forces
spread $0$. $\square$

This splits (R) by how many of the three sets have size divisible by $3$.

| case | how many $3 \mid \lvert D_i\rvert$ | what Theorem S gives | what remains |
|---|---|---|---|
| 1 | two or three | Cor. V: two agents at spread $0$ | third spread $\le 3$ |
| 2 | exactly one, say $D_3$ | Theorem S on $(D_3,D_1)$: $\mathrm{sp}_3 = 0$, $\mathrm{sp}_1 \le 1$ | third spread $\le 2$ |
| 3 | none | — | all three rigid; by Cor. Q this is S4 or a counterexample to (Q), so it does not arise on a residual instance |

So in every case that arises, **(R) follows from a single symmetric statement**:

> **Target Theorem (open).** For any three sets there is a $3$-colouring
> splitting two of them within one and the third within **two**.

*Why it suffices.* Case 2: put $D_3$ and $D_1$ in the tight slots — $D_3$ within
one is spread $0$ by Lemma H(b) — giving $\Sigma \le 0 + 1 + 2 = 3$. Case 1: put
the two divisible sets in the tight slots, giving $\Sigma \le 0+0+2 = 2$.

This is a clean relaxation of uniform balance — which asks for *all three* within
one and provably fails — by exactly one unit on exactly one set. Theorem S is its
two-set precursor, and the disjoint-or-covering mechanism of that proof is the
natural tool to extend.

**A worked instance, and it behaves as the theory predicts.** Take
$D_1 = \{1,2,3\}$, $D_2 = \{1,2,4\}$, $D_3 = \{1,3,4\}$ on $\items = \{1,2,3,4\}$,
all additive. Each has size $3$, so uniform balance demands each be *rainbow*;
the three triangles they impose have union

$$\{12,13,23\} \cup \{12,14,24\} \cup \{13,14,34\} = E(K_4),$$

and $K_4$ is not $3$-colourable. **So no uniformly balanced family exists** —
and by Corollary T this is the smallest possible shape of such an obstruction,
since two sets never suffice. Yet $\Sigma \le 3$ holds easily: the partition
$\{1\},\{2,4\},\{3\}$ gives counts $(1,1,1)$, $(1,2,0)$, $(1,1,1)$, so

$$\Sigma = 0 + 2 + 0 = 2 .$$

Two agents at spread $0$ and one at $2$ — exactly the Case 1 mechanism of
Corollary V. The instance is all-additive, hence inside S1 and already closed by
`thm:binadd`, so it is not a residual instance; but it is a natural candidate
counterexample to **Lemma E**, and Lemma E survives it.

### 7.15 The greedy levelling lemma, and exactly where three sets break

Everything in §7.10–7.14 turns out to rest on one small lemma, worth isolating
because it explains both what works and what does not.

> **Lemma W (greedy levelling).** Let $w_1,\dots,w_N$ be integers with
> $0 \le w_j \le k$. Then one can choose $\delta_j \in \{0,1\}^k$ with
> $\lvert\delta_j\rvert = w_j$ such that $\sum_j \delta_j$ has spread $\le 1$.

*Proof.* Process in any order, placing $\delta_j$'s ones on the $w_j$ currently
smallest coordinates. Invariant: the entries lie in $\{\mu,\mu+1\}$. Let $k'$ be
the number of entries equal to $\mu$. If $w_j \le k'$ then $w_j$ of them rise to
$\mu+1$ and the entries still lie in $\{\mu,\mu+1\}$. If $w_j > k'$ then all $k'$
rise to $\mu+1$ and $w_j - k'$ of the others rise to $\mu+2$, so the entries lie
in $\{\mu+1,\mu+2\}$. Either way the spread stays $\le 1$. $\square$

**This is the engine.** Read in the residue frame of §7.10, Lemma W says a
**single** set can always be levelled: run greedy over the regions containing it.
So:

- **One set** — Lemma W directly, which re-proves Lemma F.
- **Two sets** — they share exactly one region, $D_1 \cap D_2$. Choose
  $\epsilon_{12}$ first, then run greedy independently for $E_1$ (over
  $\epsilon_{12}, \epsilon_1$) and for $E_2$ (over $\epsilon_{12}, \epsilon_2$).
  This re-proves **Theorem S** in two lines.
- **Three sets** — $D_1$ and $D_2$ now share *two* regions, $\{12\}$ and
  $\{123\}$, and $\{123\}$ is shared by all three. No ordering of the seven
  regions lets all three sets run greedy, because each shared region is
  committed by whichever set is processed first.

> **That is the whole obstruction, and $K_4$ realises it.** In the $K_4$ instance
> of §7.14 the four active regions are $\{12\},\{13\},\{23\},\{123\}$ with all
> $b_T = 1$ and $\beta_i = 3$, so every set demands $E_i = (1,1,1)$ — its three
> regions rainbow. Greedy would achieve that for any one set; the three demands
> together force all four residues pairwise distinct, which three colours cannot
> supply.

### 7.15.1 Transporting $D_3$ inside a fixed two-set solution

The other half of the attack on the Target Theorem is to fix Theorem S's
colouring for $D_1, D_2$ and then move $D_3$'s elements around inside it. Write
$R$ for a region of the $(D_1,D_2)$-Venn diagram, $r_{R,t}$ for the number of its
elements Theorem S sends to colour $t$, and $d_R = \lvert D_3 \cap R\rvert$.

> **Lemma X (in-region placement).** If $r_{R,\cdot}$ has spread $\le 1$ and
> $0 \le d_R \le \lvert R\rvert = \sum_t r_{R,t}$, then some $x_{R,\cdot}$ with
> $0 \le x_{R,t} \le r_{R,t}$ and $\sum_t x_{R,t} = d_R$ has spread $\le 1$.

*Proof.* Write $d_R = 3\lambda + \rho$ and put the $\rho$ ceilings on the
coordinates with the largest $r_{R,t}$. The floors need $\lambda \le \min_t r_{R,t}$,
and $\min_t r_{R,t} \ge \lfloor\lvert R\rvert/3\rfloor \ge \lfloor d_R/3\rfloor = \lambda$.
The ceilings need $\lambda + 1 \le r_{R,t}$ on $\rho$ coordinates; if $\rho \ge 1$
then $\lvert R\rvert \ge d_R \ge 3\lambda+1$, so the largest $r_{R,t}$ is at least
$\lambda+1$, and if $\rho = 2$ then $\lvert R\rvert \ge 3\lambda+2$ forces the two
largest to be at least $\lambda+1$. $\square$

Each region can therefore contribute $x_{R,\cdot} = \lambda_R\mathbf 1 + \delta_R$
with $\delta_R \in \{0,1\}^3$ of weight $\rho_R$, and $D_3$'s counts are
$\text{const} + \sum_R \delta_R$. **If the $\delta_R$ were free, Lemma W would
level them and $D_3$ would land within one** — giving uniform balance, which is
impossible on a residual instance. So the restriction must bite, and it is
explicit: $\delta_{R,t} = 1$ needs $r_{R,t} \ge \lambda_R + 1$, which fails only
when $3 \nmid \lvert R\rvert$ *and* $\lfloor d_R/3\rfloor = \lfloor \lvert R\rvert/3\rfloor$.

> **Corollary Y (structure of residual instances).** In a residual composed
> instance, for every choice of two sets to play the role of $D_1,D_2$, some
> region $R$ of their Venn diagram has $3 \nmid \lvert R\rvert$ **and**
> $\lfloor \lvert D_3 \cap R\rvert/3\rfloor = \lfloor \lvert R\rvert /3\rfloor$ —
> that is, $D_3$ nearly fills a region whose size is not a multiple of three.

*Proof.* Otherwise Lemmas X and W level all three sets within one, giving a
uniformly balanced family and contradicting S4. $\square$

**Status of the Target Theorem: open.** What Lemmas W, X and Corollary Y supply
is the mechanism and a necessary structural feature of any counterexample; they
do not yet yield the one unit of slack the Target Theorem asks for.

### 7.16 (Q) closed when no private region is active

Recall the setting of §7.10: active regions choose colours $c_T$, and each set
$i$ imposes the constraint of the taxonomy on its active regions
$\{i\},\{ij\},\{ik\},\{123\}$. The private region $\{i\}$ is seen by set $i$
alone. Write $S \subseteq \{12,13,23,123\}$ for the active **shared** regions.

> **Theorem Z.** If no private region is active, then (Q) holds: a uniformly
> balanced colouring exists.

*Proof.* Then $d_i = \lvert S \cap \{ij,ik,123\}\rvert$, and we exhaust $S$ up to
relabelling the three sets.

**(a) $123 \notin S$.** Every $d_i \le 2$, so every constraint is a disequality,
and all of them lie among the three variables $c_{12}, c_{13}, c_{23}$. Colour
those three distinctly. $\square$

**(b) $123 \in S$, $S \cap \{12,13,23\} = \emptyset$.** All $d_i = 1$: no
constraints.

**(c) $123 \in S$, exactly one pair region, say $\{12\}$.** Then $d_1 = d_2 = 2$,
both giving the same disequality $c_{12} \ne c_{123}$, and $d_3 = 1$. Satisfy it.

**(d) $123 \in S$, exactly two pair regions, say $\{12\},\{13\}$.** Then
$d_1 = 3$ while $d_2 = d_3 = 2$. A set with $d = 2$ cannot have
$(p,q) = (1,1)$, so $d_2 = 2$ forces $\sigma_{12} = \sigma_{123}$ and $d_3 = 2$
forces $\sigma_{13} = \sigma_{123}$. Hence $\sigma_{12} = \sigma_{13} =
\sigma_{123}$ and set 1 has $(p_1,q_1) \in \{(3,0),(0,3)\}$, so
$s_1 \equiv 0 \pmod 3$ — **excluded by hypothesis**. The configuration does not
arise.

**(e) $123 \in S$, all three pair regions.** Then $d_i = 3$ for every $i$, so
every constraint is a membership, and the **constant** colouring satisfies all
three by Lemma L. $\square$

Every case is either satisfied outright or forbidden by
$3 \nmid \lvert D_i\rvert$. $\square$

**What this says.** The hypothesis of (Q) is doing precisely one job, and case
(d) exhibits it: the only way to build a genuine conflict among shared regions is
to surround a membership by two disequalities, and that arrangement forces the
surrounded set to have all three of its regions on one sign — which is exactly
$s_i \equiv 0$, the rigid case the hypothesis excludes. This is Lemma N in its
sharpest form, and case (d) is where `prop:no-balance` lives.

> **Corollary.** Combining Theorem Z with Lemma K, (Q) can only fail through a
> set with $d_i = 4$ — that is, one all four of whose regions are active. Sets
> with an active private region and $d_i \le 3$ are absorbed by their own knob;
> sets with no active private region are covered by Theorem Z.

**The residual gap in (Q).** A set with $d_i = 4$ has a private knob but its
constraint is a *diversity* condition (taxonomy, $d = 4$), and the knob suffices
only when its three shared regions are not degenerately coloured — for
$(4,0)$ and $(0,4)$, not all equal; for $(3,1)$ and $(1,3)$, an extra condition
when two of the shared majority regions coincide. Choosing the three pair
residues distinct discharges most of it; a single sub-case survives, and **(Q)
is not closed.**

### 7.16.1 (Q) is PROVED

*This supersedes an earlier draft of this subsection organised around keeping
the "spine" $c_{12},c_{13},c_{123}$ rainbow. That was the wrong organising idea —
the hard case needs colours to **coincide** so that opposite signs cancel, not to
be distinct. The right lemma is K″ below, and with it the whole of (Q) falls out
by a case exhaustion on the active **shared** regions alone.*

Write $u_T := \sigma_T e_{c_T}$ for each active region, so
$F_i = \sum_{T \ni i} u_T$, and split off the private region:
$$F_i = G_i + \sigma_{\{i\}} e_{c_{\{i\}}}, \qquad G_i := \sum_{T \ni i,\ T \ne \{i\}} u_T ,$$
with the second term absent when $\{i\}$ is inactive. $G_i$ ranges over the
**shared** regions of set $i$, namely $\{ij\},\{ik\},\{123\}$.

> **Lemma K″ (the private knob absorbs any levelled shared part).** If
> $\mathrm{spread}(G_i) \le 1$ and $\{i\}$ is active, then some choice of
> $c_{\{i\}}$ gives $\mathrm{spread}(F_i) \le 1$ — for **either** sign
> $\sigma_{\{i\}}$.

*Proof.* Entries of $G_i$ lie in $\{\mu,\mu+1\}$. If $\sigma_{\{i\}}=+1$: when
some entry equals $\mu$, add there and the entries stay in $\{\mu,\mu+1\}$; when
all equal $\mu$, adding anywhere gives $(\mu+1,\mu,\mu)$, spread $1$. If
$\sigma_{\{i\}}=-1$: symmetrically, subtract at a $\mu+1$ entry, or from a
constant vector to get $(\mu-1,\mu,\mu)$. $\square$

> **Lemma K‴ (rescue at spread 2, all values distinct).** If $\{i\}$ is active
> and $G_i$ has entries $\{\mu,\mu+1,\mu+2\}$, then either sign admits a choice
> of $c_{\{i\}}$ with $\mathrm{spread}(F_i)\le1$.

*Proof.* $\sigma_{\{i\}}=+1$: add at the $\mu$ entry, giving
$\{\mu+1,\mu+1,\mu+2\}$. $\sigma_{\{i\}}=-1$: subtract at the $\mu+2$ entry,
giving $\{\mu,\mu+1,\mu+1\}$. $\square$

**The reduction.** By K″, if the four shared colours can be chosen so that every
$G_i$ has spread $\le 1$, then every set is satisfied — those with an inactive
private because $F_i = G_i$, those with an active private by the knob. So **(Q)
reduces to a problem in the four shared variables only.** The needed conditions,
read off the $k$-vector analysis of §7.10.1:

| $\lvert G_i\rvert$ | condition for $\mathrm{spread}(G_i)\le1$ |
|---|---|
| $0$ or $1$ region | automatic |
| $2$ regions | signs **equal** $\Rightarrow$ colours differ; signs **opposite** $\Rightarrow$ colours equal |
| $3$ regions | signs all equal $\Rightarrow$ all three colours distinct; signs split $2$–$1$ $\Rightarrow$ the minority's colour lies in $\{$the two majority colours$\}$ |

> **Theorem Z′.** (Q) holds: any three sets none of whose sizes is divisible by
> $3$ admit a uniformly balanced $3$-colouring.

*Proof.* Let $S \subseteq \{12,13,23,123\}$ be the active shared regions, and
write $a=\sigma_{12}$, $b=\sigma_{13}$, $c=\sigma_{23}$, $w=\sigma_{123}$. The
hypothesis is $s_i \not\equiv 0 \pmod 3$, where $s_i$ sums $\sigma_T$ over **all**
active regions containing $i$, private included. Negating every sign negates
every $F_i$ and preserves spreads, so we may fix $w=+$ whenever $123 \in S$.

**(A) $123 \notin S$.** Each $G_i$ spans at most two regions.

*(A1) $\lvert S\rvert \le 1$:* every $G_i$ has at most one region — automatic.

*(A2) $\lvert S\rvert = 2$, say $S=\{12,13\}$:* only $G_1$ spans two regions;
$G_2 = u_{12}$ and $G_3 = u_{13}$ are automatic. Satisfy $G_1$'s single
two-region condition.

*(A3) $S=\{12,13,23\}$:* all three $G_i$ span two regions. If $a=b=c$, all three
conditions read "colours differ", so take $c_{12},c_{13},c_{23}$ pairwise
distinct. Otherwise exactly two signs agree, say $a=b\ne c$; then $G_1$ demands
$c_{12}\ne c_{13}$ while $G_2, G_3$ demand $c_{12}=c_{23}$ and $c_{13}=c_{23}$ —
inconsistent. But $a=-c$ gives $s_2 = \sigma_{\{2\}}[\text{active}] + a + c
= \sigma_{\{2\}}[\text{active}]$, so $\{2\}$ must be active or $s_2 = 0$;
likewise $\{3\}$. With $\{2\}$ active, set $2$'s three regions
$\{2\},\{12\},\{23\}$ carry signs $\{\sigma_{\{2\}}, a, -a\}$, necessarily a
$2$–$1$ split, and the minority condition is met by choosing $c_{\{2\}}$ — equal
to the minority's colour if $\{2\}$ is in the majority, or to either majority
colour if $\{2\}$ is itself the minority. Set $3$ likewise. Only $G_1$'s
condition remains: take $c_{12}\ne c_{13}$.

**(B) $123 \in S$, $w=+$.**

*(B0) $S=\{123\}$:* every $G_i = u_{123}$, spread $1$.

*(B1) $S=\{123,12\}$:* $G_3 = u_{123}$ is automatic; $G_1$ and $G_2$ impose the
same two-region condition on $(c_{12},c_{123})$. Satisfy it.

*(B2) $S=\{123,12,13\}$:* $G_1$ spans three regions, $G_2$ and $G_3$ two. Four
sign patterns:
- $a=b=+$: $G_2,G_3$ demand $c_{12}\ne c_{123}$ and $c_{13}\ne c_{123}$; $G_1$
  (all signs $+$) demands all three distinct. Take them distinct — this
  satisfies all three.
- $a=+, b=-$: $G_2$ demands $c_{12}\ne c_{123}$, $G_3$ (opposite signs) demands
  $c_{13}=c_{123}$, and $G_1$ has minority $\{13\}$, needing
  $c_{13}\in\{c_{12},c_{123}\}$ — already true. Take $c_{123}=c_{13}=A$,
  $c_{12}=B$.
- $a=-, b=+$: symmetric.
- $a=b=-$: $G_2,G_3$ demand $c_{12}=c_{123}$ and $c_{13}=c_{123}$; $G_1$ has
  minority $\{123\}$, needing $c_{123}\in\{c_{12},c_{13}\}$ — already true. Take
  all three equal.

*(B3) $S=\{123,12,13,23\}$:* every $G_i$ spans three regions. Up to the global
sign flip there are eight patterns $(a,b,c)$ with $w=+$.
- $(a,b,c)=(+,+,+)$: each $G_i$ demands its three colours be distinct. From
  $G_1$, $(c_{12},c_{13},c_{123})$ is a rainbow, say $(A,B,C)$; $G_2$ then forces
  $c_{23}=B$; and $G_3$ sees $(B,B,C)$ — **not** distinct. No choice of the four
  shared colours works. But here $s_1 = \sigma_{\{1\}}[\text{active}]+3$, so
  $\{1\}$ must be active, and likewise $\{2\},\{3\}$ — **all three privates are
  forced active by the hypothesis.** Take $c_{12}=A$, $c_{13}=B$, $c_{123}=C$,
  $c_{23}=B$. Then $G_1 = e_A+e_B+e_C$ and $G_2 = e_A+e_B+e_C$ are constant, so
  K″ frees sets $1$ and $2$; and $G_3 = e_B+e_B+e_C$ has entries $\{0,2,1\}$ —
  three distinct values — so K‴ frees set $3$.
- $(+,+,-)$: $G_1$ demands $c_{12},c_{13},c_{123}$ distinct; $G_2$ and $G_3$ have
  minority $\{23\}$, demanding $c_{23}\in\{c_{12},c_{123}\}$ and
  $c_{23}\in\{c_{13},c_{123}\}$. Take $(A,B,C)$ distinct and $c_{23}=C$.
- $(+,-,+)$: $G_2$ demands $c_{12},c_{23},c_{123}$ distinct; $G_1,G_3$ have
  minority $\{13\}$. Take $c_{12}=A,c_{23}=B,c_{123}=C$ and $c_{13}=C$.
- $(-,+,+)$: symmetric to the previous.
- $(+,-,-)$, $(-,+,-)$, $(-,-,+)$, $(-,-,-)$: in each, every $G_i$ has a $2$–$1$
  sign split, and the **constant** colouring satisfies every minority condition.
  Take all four shared colours equal.

Every case is discharged, so (Q) holds. $\square$

**Verification against the standing witnesses.** `prop:no-balance` has sizes
$2,3,3$ and the $K_4$ instance has sizes $3,3,3$; both contain a size divisible
by $3$, so both fall **outside** (Q)'s hypothesis — exactly as required, since
both provably lack a uniformly balanced family. Theorem Z′ does not contradict
them.

> **Corollary Q′ (now unconditional).** A residual composed instance must contain
> a set whose size is divisible by $3$.

*Proof.* If no $\lvert D_i\rvert$ were divisible by $3$, Theorem Z′ gives a
colouring balancing all three underlying sets within one, and Lemma O carries
that to the composed costs — a uniformly balanced family, contradicting S4.
$\square$

This removes the conditional from §7.12: the prediction that every residual
instance contains a size-$3$ set, checked earlier against the 46 known residual
instances, is now a theorem rather than a consequence of an open conjecture.

### 7.16.2 What Theorem Z′ does and does not settle

**It closes Lemma E on the all-additive side in one direction only.** For an
all-binary-additive instance with no $\lvert D_i\rvert$ divisible by $3$,
Theorem Z′ gives uniform balance, hence $\Sigma \le 3$, hence Lemma E. But an
additive instance *with* a size divisible by $3$ is not covered: Corollary R
supplies one agent at spread $0$, and the other two must still be shown to sum to
at most $3$ — which is exactly (R), i.e. the **Target Theorem**, still open.

**⚠ A correction to Theorem I′'s "only if".** Theorem I′ was stated as an
equivalence — "Lemma E is false **iff** some instance has three rigid agents and
no uniformly balanced family". The forward direction is proved; the converse is
**not**, and the write-up glossed it. An instance can have a non-rigid agent
(so not three rigid ones) and still fail $\Sigma\le3$, if driving that agent to
spread $0$ forces the other two to sum to $4$ or more. Theorem I′ should be read
as the one-directional statement it proves, and Lemma E does **not** follow from
Theorem Z′ alone.

### 7.16.3 Superseded: the earlier $d_i=4$ draft

Fix set $1$ at $d_1 = 4$: regions $\{1\},\{12\},\{13\},\{123\}$ all active. Since
$\{12\},\{13\},\{123\}$ are then forced active, sets $2$ and $3$ automatically
have $d_2, d_3 \ge 2$ before their own private regions $\{2\},\{3\}$ or the
region $\{23\}$ are even considered.

> **Lemma K′ (the private region still frees set $i$, if the spine is rainbow).**
> If $c_{12}, c_{13}, c_{123}$ are pairwise distinct, then for **any** signs
> $(\sigma_1,\sigma_{12},\sigma_{13},\sigma_{123})$ with $(p_1,q_1)\ne(2,2)$,
> some choice of $c_1$ gives $\mathrm{spread}(F_1)\le1$.

*Proof.* Since $c_{12},c_{13},c_{123}$ are a bijection onto the three colours,
the vector $G$ with $G_t := \sum_{T \in \{12,13,123\},\, c_T = t}\sigma_T$ is, as
a multiset of entries, exactly $\{\sigma_{12},\sigma_{13},\sigma_{123}\}$. Two
cases. If all three signs agree ($G$ constant, $=(\pm1,\pm1,\pm1)$), adding
$\sigma_1$ to any one coordinate gives spread exactly $1$, for either sign of
$\sigma_1$ — direct computation. If they split $2$–$1$ (say two $+1$s and one
$-1$, so $G$ is a permutation of $(1,1,-1)$), choose $c_1$ to land on the
lone-sign coordinate: $\sigma_1=+1$ added to the $-1$ entry gives
$(1,1,0)$-type, spread $1$; $\sigma_1=-1$ added to either $+1$ entry gives
$(0,1,-1)$-type, spread $1$. The case $(2,2)$ is excluded by hypothesis, and the
all-agree / $2$-$1$ split exhausts every other sign pattern. $\square$

So **whenever the spine $c_{12},c_{13},c_{123}$ can be kept rainbow, set $1$ is
free.** The question is whether sets $2$ and $3$ can always be satisfied without
breaking that.

**When it works outright.** If $x = 1$ (region $\{2\}$ active) or $z=1$
(region $\{3\}$ active), Lemma K frees that set via its own private colour,
regardless of the spine — no constraint on $c_{12},c_{13},c_{123}$ at all. If
$x=y=z=0$, sets $2,3$ have $d=2$ each ($\{12,123\}$ and $\{13,123\}$), giving
only the disequalities $c_{12}\ne c_{123}$, $c_{13}\ne c_{123}$ — both **implied**
by rainbow. So the only case needing real work is $x=z=0$, $y=1$: no private
regions active for sets $2,3$, and $\{23\}$ active, shared between them.

**The case that looked like a counterexample.** With the spine rainbow
($c_{12}=A, c_{13}=B, c_{123}=C$, all distinct) and $d_2=d_3=3$ via
$\{12,23,123\}$ and $\{13,23,123\}$, each set's condition is a membership
constraining $c_{23}$: if $\{12\}$ is set $2$'s minority, the condition forces
$c_{23}=A$ exactly (since its majority partner $\{123\}$ already carries $C\ne A$);
if $\{13\}$ is set $3$'s minority, it forces $c_{23}=B$. Choosing the adversary's
signs so that $\{12\}$ is set $2$'s minority **and** $\{13\}$ is set $3$'s
minority simultaneously — which is a legal choice, e.g.
$(\sigma_1,\sigma_{12},\sigma_{13},\sigma_{123},\sigma_{23}) =
(-1,-1,-1,+1,+1)$, giving set $1$ the valid pattern $(p_1,q_1)=(1,3)$ — demands
$c_{23}=A$ and $c_{23}=B$ at once, and $A\ne B$. **Under a rainbow spine this
configuration is genuinely unsatisfiable.**

**It is satisfiable anyway, by breaking the spine.** Set $c_{123}=A$ (merging
it with $c_{12}$, abandoning rainbow) and $c_{13}=B \ne A$. Set $2$'s condition
becomes $A \in \{c_{23}, A\}$ — true for **any** $c_{23}$, since $\{123\}$ now
already carries the minority's colour. Set $3$'s condition becomes
$B \in \{c_{23}, A\}$, and since $B\ne A$ this forces $c_{23} = B$. Take
$c_{23} = B$. Check set $1$ directly: with signs
$(\sigma_1,\sigma_{12},\sigma_{13},\sigma_{123})=(-1,-1,-1,+1)$ and colours
$c_{12}=c_{123}=A$, the two opposite-signed copies of $A$ **cancel**:
$F_1 = -e_{c_1} - e_A - e_B + e_A = -e_{c_1} - e_B$. Choosing $c_1 = A$ (or the
third colour) gives entries $\{-1,-1,0\}$, spread $1$. All three sets check
directly against the definitions:

- Set $1$: $F_1 = -e_A - e_B$, spread $1$. ✓
- Set $2$ ($\{12,23,123\}$, signs $(-1,+1,+1)$, colours $A,B,A$):
  $F_2 = -e_A + e_B + e_A = e_B$, spread $1$. ✓
- Set $3$ ($\{13,23,123\}$, signs $(-1,+1,+1)$, colours $B,B,A$):
  $F_3 = -e_B + e_B + e_A = e_A$, spread $1$. ✓

**So the configuration is not a counterexample** — it needed a *cancellation*
strategy (merge two spine colours to neutralise opposite signs) rather than the
rainbow strategy Lemma K′ uses, and the cancellation strategy happens to satisfy
sets $2,3$'s memberships for free as a side effect.

**Retained only as a record.** The worked cancellation example above is the
special case that showed the rainbow strategy was the wrong organising idea;
Theorem Z′ of §7.16.1 subsumes it and closes (Q) in full. Lemma K′ is likewise
superseded by Lemma K″, which needs no rainbow hypothesis.

### 7.16.4 Interleaved greedy: two sets within one, the third within three

The Target Theorem asks for two sets within one and the third within **two**.
Interleaving the greedy of Lemma W across the three sets gets two within one and
the third within **three** — one short of the Target, but enough to close a case
outright.

> **Theorem AA (interleaved greedy).** For any three sets
> $D_1, D_2, D_3 \subseteq M$ there is a $3$-colouring splitting $D_1$ and $D_2$
> each within one and $D_3$ within three.

*Proof.* Work in the residue frame of §7.10: each region $T$ contributes
$\epsilon_T \in \{0,1\}^3$ of weight $b_T$, and set $i$'s spread is the spread of
$E_i = \sum_{T \ni i}\epsilon_T$. Place the seven residues in this order, each
greedily — on the currently smallest coordinates — with respect to the running
sum named:

1. $\epsilon_{123}$, freely;
2. $\epsilon_{12}$, w.r.t. $\epsilon_{123}$;
3. $\epsilon_{13}$, w.r.t. $\epsilon_{123}+\epsilon_{12}$;
4. $\epsilon_{1}$, w.r.t. $\epsilon_{123}+\epsilon_{12}+\epsilon_{13}$;
5. $\epsilon_{23}$, w.r.t. $\epsilon_{123}+\epsilon_{12}$;
6. $\epsilon_{2}$, w.r.t. $\epsilon_{123}+\epsilon_{12}+\epsilon_{23}$;
7. $\epsilon_{3}$, w.r.t. $\epsilon_{123}+\epsilon_{13}+\epsilon_{23}$.

**Set 1** sees $\epsilon_{123},\epsilon_{12},\epsilon_{13},\epsilon_1$, placed at
steps 1–4, and each is greedy with respect to set $1$'s own running sum. By
Lemma W the invariant holds throughout, so $\mathrm{spread}(E_1) \le 1$.

**Set 2** sees $\epsilon_{123},\epsilon_{12},\epsilon_{23},\epsilon_2$. Its
running sum after the first two is $\epsilon_{123}+\epsilon_{12}$ — *the same
vector* as set 1's, since both sets contain both regions — so steps 1–2 are
greedy for set 2 as well, and steps 5–6 are greedy for set 2 by construction.
Hence $\mathrm{spread}(E_2) \le 1$.

**Set 3** sees $\epsilon_{123},\epsilon_{13},\epsilon_{23},\epsilon_3$. Only the
first and last were placed greedily for it. Adding a $\{0,1\}$ vector to any
vector raises the spread by at most $1$, so after $\epsilon_{123}$ (spread $\le
1$), $\epsilon_{13}$ and $\epsilon_{23}$ the spread is at most $3$; and greedy
**never increases** the spread — for sorted $e_1\le e_2\le e_3$, adding $1$ to the
$w$ smallest leaves the maximum unchanged unless all entries are equal, and
raises the minimum — so step 7 keeps it at most $3$. $\square$

**Why the third set is the one that suffers.** Sets $1$ and $2$ share exactly one
region *among those processed before either finishes* — namely $\{12\}$, with
$\{123\}$ ahead of it — so a single ordering serves both. Set $3$ shares
$\{13\}$ with set $1$ and $\{23\}$ with set $2$, and both were already committed
to the other sets' greedy when set $3$ needs them. This is Lemma W's
"three sets share two regions pairwise" obstruction made quantitative: the cost
is exactly one unit of spread per stolen region, hence $1 + 1 + 1 = 3$.

### 7.16.5 One case of $n=3$ closed outright

> **Theorem BB.** Let $n = 3$ and let the costs be composed,
> $\cost_i(S) = f_i(\lvert S \cap D_i\rvert)$. If at least **two** of
> $\lvert D_1\rvert, \lvert D_2\rvert, \lvert D_3\rvert$ are divisible by $3$,
> then some family has $\Sigma \le 3$ — and hence, by Lemma A, Conjecture 2
> holds for the instance.

*Proof.* Relabel so that $3 \mid \lvert D_1\rvert$ and $3 \mid \lvert D_2\rvert$,
and apply Theorem AA with those two in the tight slots. It splits $D_1$ and $D_2$
each within one; by Lemma H(b) a set whose size is divisible by $3$ has count
spread $0$ or at least $2$, so "within one" forces count spread exactly $0$. It
splits $D_3$ within three. Lemma O carries each count spread to the composed cost
as an upper bound, so the cost spreads are $0$, $0$ and at most $3$, giving
$\Sigma \le 3$. Lemma A then makes every minimum-cost assignment of that family
good. $\square$

**This is a genuinely new solved case.** It is not contained in S1–S4: the
instance need not be additive, identical, small-bundled, or uniformly balanced —
indeed by Corollary Q′ every residual instance has a size divisible by $3$, and
Theorem BB closes all those with two such sizes. Checked against the residual
instances of §3, whose size multisets are $(2,3,3)$ and $(3,3,3)$: **the
$(3,3,3)$ instances are now closed by Theorem BB.** The $(2,3,3)$ instances have
exactly one size divisible by $3$ and are not.

### 7.16.6 What is left of $n = 3$

Exactly one case: **exactly one $\lvert D_i\rvert$ divisible by $3$.** There
Theorem AA gives $0 + 1 + 3 = 4$, one over budget. Closing it needs the third set
within **two** rather than three — which is precisely the Target Theorem, now
reduced to this single configuration.

The one unit is available in principle. Tracing the proof of Theorem AA, the
spread of set $3$ reaches $3$ only if $\epsilon_{123}$, $\epsilon_{13}$ and
$\epsilon_{23}$ all put a one on some coordinate $t$ and all avoid some
coordinate $s$. Writing $P = \epsilon_{123}+\epsilon_{12}$ for the vector both
$\epsilon_{13}$ and $\epsilon_{23}$ are placed against, $\epsilon_{123,t}=1$
gives $P_t = 1 + \epsilon_{12,t}$, while $\epsilon_{123,s}=0$ gives
$P_s = \epsilon_{12,s}$. For $\epsilon_{13}$ to choose $t$ and avoid $s$ we need
$P_s \ge P_t$, i.e. $\epsilon_{12,s} \ge 1 + \epsilon_{12,t}$, forcing
$\epsilon_{12,s}=1$ and $\epsilon_{12,t}=0$ — and then $P_t = P_s = 1$.

> **So whenever the bad alignment occurs, the two coordinates are tied in $P$,
> and greedy had a free choice between them.** Since Lemma W's invariant holds
> for *any* choice among the currently smallest coordinates, re-breaking that tie
> costs sets $1$ and $2$ nothing.

What is not yet proved is that a single consistent tie-breaking rule avoids the
bad alignment at every coordinate simultaneously, for all weight combinations
$b_{123}, b_{13}, b_{23} \in \{0,1,2\}$. That is the whole remaining gap in
$n=3$, and it is now a finite question about three vectors in $\{0,1\}^3$.

### 7.16.7 The tie-break lemma, and the Target Theorem

The gap of §7.16.6 closes. The point is that the bad alignment can always be
broken, and the case split is on $b_{123}$ alone.

First, a sharpening of how greedy behaves, needed because we now start from a
nonzero vector.

> **Lemma CC.** Adding a $\{0,1\}$ vector greedily — ones on the currently
> smallest coordinates — leaves the spread at most $\max(\text{old spread}, 1)$.

*Proof.* Sorted $e_1\le e_2\le e_3$. For $w=1$ the new values are
$e_1+1,e_2,e_3$; if $e_1+1\le e_3$ the maximum is unchanged and the minimum is
$\min(e_1+1,e_2)\ge e_1$, so the spread does not grow; otherwise
$e_1=e_2=e_3$ and the new spread is $1$. For $w=2$ the new values are
$e_1+1,e_2+1,e_3$: if $e_3\ge e_2+1$ the spread drops, if $e_3=e_2$ it is
$e_2+1-\min(e_1+1,e_2)$, which is $e_3-e_1$ when $e_1+1\le e_2$ and $1$
otherwise. For $w\in\{0,3\}$ nothing changes. $\square$

> **Lemma DD (tie-break).** In the ordering of Theorem AA the tie-breaks for
> $\epsilon_{13}$ and $\epsilon_{23}$ can be chosen so that
> $H := \epsilon_{123}+\epsilon_{13}+\epsilon_{23}$ has spread at most $2$.

*Proof.* Recall $\epsilon_{12}$ is placed greedily on $\epsilon_{123}$, and both
$\epsilon_{13}$ and $\epsilon_{23}$ are placed greedily on
$P := \epsilon_{123}+\epsilon_{12}$. Since $H$ is a sum of three $\{0,1\}$
vectors, its entries lie in $[0,3]$, so spread $3$ requires **both** a coordinate
$t$ lying in all three and a coordinate $s$ avoided by all three. Split on
$b_{123}$.

**$b_{123}=0$.** Then $H=\epsilon_{13}+\epsilon_{23}$ has entries at most $2$ and
spread at most $2$ automatically.

**$b_{123}=1$, say $\epsilon_{123}=e_a$.** Only $a$ lies in $\epsilon_{123}$, so
the coordinate $t$ above must be $a$; it is enough to keep $a$ out of both
$\epsilon_{13}$ and $\epsilon_{23}$. This is always possible, because $a$ is
never *forced*: $\epsilon_{12}$ is greedy on $e_a$, hence prefers the two
non-$a$ coordinates, and
- $b_{12}=0$ gives $P=e_a$, where $a$ is the unique **largest**, so the two
  smallest are non-$a$;
- $b_{12}=1$ gives $\epsilon_{12}=e_v$ with $v\ne a$ and
  $P=(1_a,1_v,0_w)$, whose smallest is $w$ and whose second tier $\{a,v\}$ is
  **tied**, so a weight-$2$ choice may take $v$;
- $b_{12}=2$ gives $\epsilon_{12}$ on both non-$a$ coordinates and $P=(1,1,1)$,
  entirely tied, so any $b_{13}\le2$ ones may be placed off $a$.

With $a$ excluded from both, $H_a = 1$ and $H_x \le 2$ for $x\ne a$, so the
maximum is at most $2$ and the spread at most $2$.

**$b_{123}=2$, say $\epsilon_{123}$ avoiding $c$.** Now $\epsilon_{123}$ avoids
only $c$, so the coordinate $s$ above must be $c$; it is enough that at least one
of $\epsilon_{13},\epsilon_{23}$ contains $c$. If both have weight $0$ then
$H=\epsilon_{123}$ has spread $1$. Otherwise $c$ is always **available**, since
$\epsilon_{12}$ is greedy on a vector that is $0$ at $c$ and $1$ at $a,b$, hence
takes $c$ first, and
- $b_{12}=0$ gives $P=(1_a,1_b,0_c)$ with $c$ uniquely smallest, so $c$ is
  *forced* into any $\epsilon_{13}$ of positive weight;
- $b_{12}=1$ gives $\epsilon_{12}=\{c\}$ and $P=(1,1,1)$, entirely tied;
- $b_{12}=2$ gives $\epsilon_{12}=\{c\}\cup\{a\}$ say, and $P=(2_a,1_b,1_c)$,
  whose smallest are $b$ and $c$, tied.

Taking $c$ into $\epsilon_{13}$ (or $\epsilon_{23}$) gives $H_c\ge1$, while
$H_a,H_b\ge1$ from $\epsilon_{123}$; so the minimum is at least $1$, the maximum
at most $3$, and the spread at most $2$.

In every case the choices are among coordinates that are tied for smallest, and
Lemma W's invariant holds for *any* such choice, so sets $1$ and $2$ are
unaffected. $\square$

> **Theorem EE (Target Theorem).** For any three sets $D_1,D_2,D_3 \subseteq M$
> there is a $3$-colouring splitting $D_1$ and $D_2$ each within **one** and
> $D_3$ within **two**.

*Proof.* Run the ordering of Theorem AA with the tie-breaks of Lemma DD. Sets $1$
and $2$ are levelled exactly as in Theorem AA, the tie-breaking being immaterial
to them. For set $3$, $E_3 = H + \epsilon_3$ with $\epsilon_3$ placed greedily,
so by Lemmas DD and CC its spread is at most $\max(2,1)=2$. $\square$

### 7.16.8 Conjecture 2 at $n=3$ for composed costs

> **Theorem FF.** Let $n = 3$ and let every cost be composed,
> $\cost_i(S) = f_i(\lvert S\cap D_i\rvert)$ with $f_i$ monotone and all
> increments in $\{0,1\}$. Then Conjecture 2 holds.

*Proof.* If the instance admits a uniformly balanced family, `thm:balanced-class`
applies. Otherwise, by Corollary Q′ some $3 \mid \lvert D_i\rvert$; relabel it as
$D_1$ and apply Theorem EE.

If a second size is also divisible by $3$, put that set in the other tight slot.
Both then have count spread within one, which Lemma H(b) upgrades to exactly $0$,
and the third has count spread at most $2$.

If exactly one size is divisible by $3$, put any other set in the second tight
slot: $D_1$ gets count spread $0$ as before, the second at most $1$, the third at
most $2$.

Lemma O bounds each cost spread by the corresponding count spread, so
$\Sigma \le 0+0+2 = 2$ or $\Sigma \le 0+1+2 = 3$. Lemma A then makes every
minimum-cost assignment of that family good, which is Conjecture 2 for the
instance. $\square$

**This closes $n = 3$ on the composed family** — every instance of the form
$\cost_i(S) = f_i(\lvert S \cap D_i\rvert)$, which includes binary additive,
capped, threshold, and every mixture of them, and in particular every residual
instance exhibited in §3.

⚠ **It does not close $n = 3$ in general.** Lemma O, and through it Corollary Q′
and the transfer from counts to costs, needs the cost to depend only on
$\lvert S \cap D_i \rvert$. A dichotomous cost that is not a function of a single
intersection size is outside the argument. Whether every $n=3$ instance reduces
to a composed one is **not** proved — the residual instances found in §3 all
happened to be composed, but that was a property of how they were constructed,
not a theorem.

### 7.16.9 Why Theorem FF does not extend: rigid non-composed costs exist

The next target is $n=3$ for general dichotomous costs. The composed proof runs
on one engine — **rigidity is equivalent to a divisibility condition**
(Lemma H: an additive $D_i$ is rigid exactly when $3 \nmid \lvert D_i\rvert$) —
and Theorem Z′ then says three rigid sets cannot evade uniform balance. Both
steps die outside the composed class, and here is the witness.

> **Example.** On $\items = \{1,2,3\}$ define
> $$\cost(S) = \begin{cases} 0 & S \subseteq \{1\} \text{ or } S \subseteq \{2\},\\ 1 & \text{otherwise.}\end{cases}$$

**It is dichotomous.** Monotone, since the zero sets $\{\emptyset,\{1\},\{2\}\}$
form a down-set. Every marginal is $0$ or $1$: from $\emptyset$ the marginals are
$0,0,1$ to $\{1\},\{2\},\{3\}$; from $\{1\}$ they are $1,1$; from $\{3\}$ they
are $0,0$; and from any two-element set the marginal to $\items$ is $0$.

**It is rigid.** The $3$-partitions of a three-element set, up to reordering, are
$(\{1\},\{2\},\{3\})$ with costs $(0,0,1)$; $(\{1,2\},\{3\},\emptyset)$ with
$(1,1,0)$; $(\{1,3\},\{2\},\emptyset)$ and $(\{2,3\},\{1\},\emptyset)$ with
$(1,0,0)$; and $(\items,\emptyset,\emptyset)$ with $(1,0,0)$. None is constant,
so no partition gives spread $0$.

**It is not composed.** Suppose $\cost(S) = f(\lvert S \cap D\rvert)$. From
$\cost(\{1\}) = 0 \ne 1 = \cost(\{3\})$ and monotonicity of $f$ we get $3 \in D$
and $1 \notin D$; from $\cost(\{2\}) = 0$ likewise $2 \notin D$. So $D = \{3\}$
and $\cost(\{1,2\}) = f(0) = \cost(\emptyset) = 0$, contradicting
$\cost(\{1,2\}) = 1$.

**What this settles.** Rigidity outside the composed class has nothing to do with
divisibility — here $\cost(\items) = 1$ and no size is in play at all. So
Lemma H has no general analogue, Theorem Z′ has no general analogue, and
Corollary Q′ — "a residual instance must contain a set of size divisible by
$3$", the step that hands Theorem FF its spread-$0$ agent for free — simply does
not parse without the sets. **Theorem FF's method does not extend, and this is
not a gap in the write-up but a genuine boundary.**

### 7.16.10 What general $n=3$ reduces to

The reduction itself survives, because it never used composedness:

- Lemma F (each agent alone reaches spread $\le 1$) — general.
- Corollary G (no uniform balance $\Rightarrow$ a family with $\Sigma\le3$ needs
  some agent at spread exactly $0$) — general.
- Proposition/Theorem I′ forward direction (three rigid agents and no uniform
  balance $\Rightarrow$ $\Sigma \ge 4$) — general.
- Lemma A ($\Sigma \le 3 \Rightarrow$ good at $n=3$) — general.

So general $n = 3$ turns on exactly the question already named:

> **(Q′)** Can three **rigid** dichotomous costs fail to admit a uniformly
> balanced family?

**No** would give $\Sigma\le3$ whenever uniform balance fails — some agent
reaches spread $0$ — and, with the other two controlled, Conjecture 2 at $n=3$
in general. **Yes** produces an instance where $\Sigma \ge 4$ for every family,
refuting Lemma E outright and forcing $n=3$ through the $\Sigma=4$ obstruction of
`prop:f5-pattern` instead.

**Status: (Q′) is open, and the two obvious attacks both stall.** Building a
counterexample needs three rigid costs on a common ground set with no uniformly
balanced family, and rigidity is a demanding condition — the example above needs
$\lvert\items\rvert = 3$ precisely so that every part is forced to be a
singleton; enlarging $\items$ lets a partition into three cost-$1$ parts appear
and destroys rigidity. Three copies of it rotated over $\{1,2,3\}$ are each
rigid but *do* admit a uniformly balanced family, namely the singleton
partition, on which all three spreads are $1$. Proving (Q′) in the affirmative,
on the other hand, cannot go through Theorem Z′'s route, since there is no
residue system to run the argument on.

### 7.16.11 Audit of the $n=3$ chain (against the user's verification dossier)

`Conjecture_2_n3_Verification_Dossier.md` and `Target_T_n3_AI_Agent_Research.md`
lay out the $n=3$ chain independently. Both predate `843bac3` and therefore both
record Target T and Lemma E as open; with Theorem EE and Theorem FF that status
line is superseded on the composed family. Every substantive step in the dossier
was checked against the certified results above and is correct. Three points in
its presentation are not, and the first two are worth keeping because a later
restatement could reintroduce them silently.

**(1) The Target Theorem must be the *nominating* form.** Both files state Target
T as "there is a 3-colouring such that, *after relabelling the sets*, two are
split within one and the third within two", then use it as "arrange the labels so
that the divisible set occupies one of the two spread-$\le1$ positions"
(dossier §13; Target-T file §0(4), §6 Case B, §14 Step 2). Those are different
statements. Under the unlabelled reading the colouring picks which set gets the
slack, and the argument dies at the divisibility step: "within one" upgrades to
"exactly 0" for a set of size divisible by 3, but "within two" does not — a
size-3 set split $(0,1,2)$ has spread 2 and sum divisible by 3, and any $f$ with
$f(0)=0,f(1)=1$ then has cost spread 2, exhausting the budget $\Sigma\le3$ on one
agent. **Theorem EE is proved in the nominating form** — the ordering
$\epsilon_{123},\epsilon_{12},\epsilon_{13},\epsilon_1,\epsilon_{23},\epsilon_2,
\epsilon_3$ is written in the labels, so it may be run after permuting them — so
the chain does close, but only because of that. Recorded as `rem:f5-nomination`.

**(2) "Residual $\Rightarrow$ composed" is assumed, not proved, and is false.**
The dossier's §6 asserts the residual family is the composed one; §15 and §21
then conclude "Conjecture 2 for $n=3$" unqualified, on the grounds that "the
non-residual families are handled separately". The composed hypothesis is never
discharged, and by §7.16.9 it cannot be: there is a rigid dichotomous cost that
is not composed. The chain proves Theorem FF — $n=3$ for composed costs — which
is a real theorem but not general $n=3$. To the dossier's credit its own §17
checklist item C.2 flags exactly this ("the residual family is indeed of composed
form where Target T is being applied") as requiring verification; the answer is
no.

**(3) Smaller items.** §1 writes the dichotomous condition as
$c_i(S)-c_i(S\cup\{g\})\in\{0,1\}$, the wrong sign (with $c(\emptyset)=0$ that
forces $c\equiv0$); the next sentence gives the intent. §1 and §5 say the project
"has reduced" Conjecture 2 at $n=3$ *to* F5\*, which reads as an equivalence —
Lemma A is one-directional, and no converse is proved. §19 Option 3 claims
$\min_B\sum_i \mathrm{sp}_{D_i}(B)\le2$ would "immediately imply Target T"; it
implies only the unlabelled form, by (1), though it *would* close the composed
case more cheaply — compression gives $\Sigma\le2$ directly, with no divisible
set needed (`rem:f5-sigma2`). In the Target-T file, §6 Case A derives the profile
$(0,0,\le2)$ from "the established two-set theorem", which constrains only two
sets and says nothing about the third; the conclusion is recoverable from
Theorem EE with both divisible sets nominated, or from Theorem AA as $0+0+3$
(Theorem BB).

Everything else checks out: §3 normalisation, §4 Lemma A, §7 compression
(the use of $f$ monotone and 1-Lipschitz is right), §8 divisibility, §9–§10 the
seven-region residue reduction, §11 Theorem S and the "spread 1 is impossible
when $3\mid|D|$" step, §13's arithmetic, §14's conversion to subsidies
($\min_i p_i=0$, so $\sum_i p_i\le2=n-1$), and §16's list of non-substitutable
statements — including the $K_4$ obstruction, re-verified here: the three
triangles $\{1,2,3\},\{1,2,4\},\{1,3,4\}$ cover all six edges of $K_4$, which is
not 3-colourable.

**LaTeX.** `report/working/approach_10.tex` §"The chain at three agents, audited"
now carries the nine-step dependency list with the hypothesis each link consumes,
`rem:f5-nomination`, `rem:f5-sigma2`, and — filling the gap `43e33b2` left —
`prop:f5-noncomposed` (the rigid non-composed witness, with proof) and
`rem:f5-Qprime` ((Q′) and what each answer to it buys).

### 7.16.12 Second pass: `n3_conjecture2_consolidated_findings.md`

A second, independently-produced document covering the same ground. It re-derives
Target T (its §12–§14) and the composed $n=3$ closure by the identical
seven-region residue argument, and independently states the unique $\Sigma=4$
obstruction pattern (its §7): $v_i=v_k=(2,2,0)$, $v_j=(0,0,0)$. This is exactly
`prop:f5-pattern`, word for word in substance — a genuine independent check, and
it passes. Its own verification of Target T is computational (a $3^7$-residue,
$7^7$-colouring exhaustive search via an external, unreachable script) rather
than a proof; the arithmetic is internally consistent
($1{+}3{+}3=7$ per region, $7^7=823543$, and its histogram sums to $2187=3^7$)
but we do not need it, having Theorem EE already. No new mathematics in this
part.

**One claimed "correction" does not apply here.** Its §17 says an earlier line
of reasoning wrongly concluded every $\Sigma\le3$ solution needs a spread-zero
agent, correcting this with a $(1,1,1)$ profile (total spread $3$, no zero). This
is not a correction to Corollary~`cor:f5-needzero` above: that corollary's
zero-forcing claim is explicitly conditional on *no uniformly balanced family
existing* — and a $(1,1,1)$ profile **is** a uniformly balanced family
(Definition~`main:unifbal`), so it never falls under the corollary's hypothesis
in the first place. No fix needed on our side.

**What is new: a catalogue of ruled-out strategies for general Lemma E$'$.** Its
§8 lists six proof mechanisms tried against the *non-composed* case — exactly
our open (Q$'$)/general-Lemma-E′ frontier — and reports each as insufficient.
Only the first comes with a fully specified witness; the rest are asserted
without one, so they are recorded here as reported findings from that
exploration, not independently re-verified:

1. **Fixed-third-bundle split** (self-checked, trivial). Rebalancing only
   $A \cup B$ while leaving $C$ untouched cannot help once $C$ is committed:
   with $\cost_1=\cost_2=\abs{\cdot}$ additive, $\abs{A}=\abs{B}=2$, $C=\emptyset$,
   both agents see $(2,2,0)$, and no redistribution confined to $A,B$ moves
   anything into $C$. Confirms the obvious: any general argument needs the
   freedom to move items across all three bundles, not two.
2. **Single pivotal item** — reported, no witness given. Claims there need not
   be one item whose marginal simultaneously improves both problematic agents.
3. **Minimal threshold witness transfer** — reported, no witness given. Claims a
   witness set controlling the receiving side of a move need not control the
   donor side.
4. **Type-II/Type-II exclusion** — reported, no witness given. Claims two
   problematic agents can simultaneously have the stated "donor-catastrophic"
   structure.
5. **Nested threshold / critical-edge route** — reported, no witness given.
   Claims two agents can have synchronised critical edges while a third has an
   independent threshold boundary on the refined partition.
6. **Matching transpositions and 3-cycles** — reported, no witness given. Claims
   the six-permutation assignment layer can be fully optimal while a strictly
   better *repartition* of the items exists, so permutation optimality alone
   cannot prove Lemma E$'$. This one is consistent with our own architecture:
   Lemma A already operates one level above repartitioning (§4 above), and
   Theorem EE's proof works entirely by constructing partitions, never by
   permuting a fixed one, for exactly this reason.

Items 2–5 are plausible in light of our own experience — every one of our
positive results needed *global* coordination across the seven Venn regions
(Lemma K″, the interleaved ordering of Theorem AA, the tie-break case split of
Lemma DD), and every attempt at a *local* argument (a single item, a single
region, a single pair of agents) that we tried failed for the same structural
reason. But without explicit cost tables we cannot certify 2–5, so they are
recorded as leads, not results: useful for steering (Q$'$) away from another
local-argument attempt, not citable as theorems.

### 7.16.13 Attacking (Q′) directly: an unbounded rigid non-composed family, and a failed hunt for a counterexample

**A necessary condition, free.** If $\cost(\items) \le 1$ then $\cost$ takes only
values in $\set{0,1}$ (monotone, $\cost(\emptyset)=0$, marginals $\le 1$), so its
spread is $\le 1$ under *every* partition — it can never be the agent that fails
uniform balance. So a counterexample to (Q′) needs all three agents at
$\cost_i(\items) \ge 2$; combined with rigid $+$ composed already being closed by
Theorem FF (Lemma H + Theorem Z′), the live target is specifically **rigid,
non-composed, $\cost(\items)\ge2$**.

**The $\abs{\items}=3$ witness does not represent the general case.** The
$\abs{\items}=3$ witness of §7.16.9 suggested rigid non-composed costs might need
a small ground set. That is false. Take
$\cost(S) = \min(\abs{S\cap D}, \abs{S \cap D'})$ for $D,D'\subseteq\items$ with
$D\setminus D' = P$ (size $p$, arbitrary), $D'\setminus D = \set{q}$ (a single
element), $D\cap D' = \set{r}$ (a single element), $\items = P \sqcup \set{q,r}$.
This is dichotomous (checked directly: adding $g\in P$ changes the min by $0$ or
$1$ depending on which side is currently smaller; adding $q$ or $r$ likewise), it
is **not composed** whenever $p \ge 2$ (the standard singleton-comparison
argument: comparing $\cost$ on singletons from $P$ pins any candidate
representing set to $\set{r}$, and then a mixed pair from $P$ and $\set{q}$
contradicts it), and:

> **Rigid for every $p$.** Write $\beta,\rho$ for the parts holding $q,r$. If
> $\beta \ne \rho$: the part holding $q$ alone scores $\le 1$, the part holding
> $r$ alone scores exactly $1$, the third scores $0$ — spread exactly $1$, never
> $0$. If $\beta = \rho$: that part scores $\ge 1$ (from $r$ alone) and the other
> two both score $0$ — spread $\ge 1$. Either way spread is never $0$, and this
> uses only $p \ge 0$: the $P$-elements are inert for this argument, however many
> there are.

So this is a genuinely **unbounded family** of rigid, non-composed, range-$2$
dichotomous costs — the earlier "must be small" intuition was an artifact of the
one witness on hand, not a real obstruction. Verified computationally for
$p \in \set{1,2,5,10,20,50,100}$ (min spread stays $1$ throughout); see
transcript. This also pins down the *exact* boundary within this family: growing
$q$ or $r$ to $2$ (even with $p$ small) kills rigidity immediately — spread $0$
becomes reachable at $(p,q,r)=(2,2,1)$ and at $(1,1,2)$, verified directly.

**Combining three of them: every attempt still finds uniform balance.** Three
such "pinch" costs sharing a ground set is the natural next object for a (Q′)
counterexample, since each individually is rigid and range-$\ge2$. Three attempts,
increasingly adversarial, all failed to break uniform balance:

1. Three independent pinch pairs on $6$ elements, each agent's $P$-zone equal to
   the *other two* agents' special elements (so isolating one agent's pair
   necessarily shares space with another's). Best achievable: $(1,1,1)$ — the
   solver isolates each pair in its own part and nothing else joins it.
2. The same, but with the three pairs forced to overlap cyclically on only $3$
   elements — $\set{a,b},\set{b,c},\set{c,a}$ as the three $(q_i,r_i)$ pairs, so
   no partition can keep all three pairs disjointly isolated. Still $(1,1,1)$,
   witnessed by partition $\set{a},\set{b},\set{c}$.
3. A random search over $427$ valid all-rigid triples of bottleneck costs on a
   shared $5$-element ground set (random $D_i,D_i'$, filtered to keep only rigid
   ones): zero achieved max-spread $\ge 2$. Every one admitted uniform balance.

**Reading.** This is evidence, not a proof — the search covers the bottleneck
family specifically, not the full space of dichotomous costs, and finitely many
trials cannot rule out a counterexample outside it. But it reverses the earlier
default expectation: the obstacle to proving (Q′) does not look like "rigid
non-composed costs are rare/small and hard to find", since we now have an
unbounded supply of them; it looks like "no matter how these are combined across
three agents, there is always enough shared room in three bundles to route around
all three simultaneously" — a stronger, more encouraging signal for (Q′) being
**true** than anything found so far. The natural next step is a *direct* proof of
(Q′), not by the Venn-region/composed machinery (which does not apply outside
composed costs) but by an argument on the general unit-step structure of a
dichotomous cost directly — e.g.\ an exchange/potential argument in the style of
Lemma K″ but stated for the up-set chain $U_1 \supseteq U_2 \supseteq \dots$ that
any dichotomous cost admits ($U_\ell = \set{S : \cost(S) \ge \ell}$), rather than
for a single underlying set $D_i$.

### 7.16.14 The direct attempt on (Q′): where it breaks, precisely

Attempted the up-set-chain generalisation of Lemma K″. It does not go through, and
the reason is structural, not a missing trick.

**Why the composed machinery works at all.** Lemma K″'s proof needs exactly one
thing: an element in agent $i$'s private Venn region has a *context-independent*
marginal — adding it changes $\cost_i$ by exactly $1$ regardless of what else is
already present, because $\cost_i(S) = f_i(\abs{S \cap D_i})$ collapses everything
relevant to agent $i$ into a single running count. That single count is the
"state" the interleaved-greedy ordering of Theorem~\ref{thm:f5-interleaved}
tracks across all three agents at once via the seven-region frame. A general
dichotomous cost has no such collapse: an element's marginal for agent $i$ can be
$1$ in one context and $0$ in another, so there is no finite-dimensional
coordinate system to run an analogous ordering on.

**The one-element-induction route gets stuck.** The natural substitute: induct on
$\abs{\items}$, remove an element $x$, get a balanced partition of $\items
\setminus \set{x}$ by the inductive hypothesis (assuming, as needed, that
removing $x$ preserves rigidity of all three agents — a separate case to handle),
then insert $x$ into whichever part stays safe for every agent. Working out
"safe": agent $i$ is safe at part $t$ iff $t$ currently holds agent $i$'s minimum
level, or $x$'s marginal there is $0$. This can fail for *two* agents already: take
agent $1$'s only safe part to be $\set{1}$ (marginal $1$ elsewhere), agent $2$'s
only safe part to be $\set{2}$ (marginal $1$ elsewhere), and arrange $x$'s
marginals so part $3$ is unsafe for both. Then every one of the three insertion
points breaks some agent. Concretely: parts $\set{1},\set{2},\set{3}$ currently at
levels $(\mu_1,\mu_1{+}1,\mu_1{+}1)$ for agent $1$ and $(\mu_2{+}1,\mu_2,\mu_2{+}1)$
for agent $2$, with $x$'s marginal $1$ at every part except its own current
minimum for each agent. No single insertion is simultaneously safe. One-element
induction is not salvageable without a batched, look-ahead move, and none is in
hand.

**Dichotomous costs also lack a pivotal-element property.** The star-cover gadget
of §7.16.9's discussion ($\cost(S)=1$ iff $v\in S$ or all of a leaf set
$\subseteq S$) has $\cost(\items)=1$ with \emph{no} single element whose removal
lowers the cost when both witnesses are present: removing $v$ alone leaves the
leaves intact (still cost $1$), removing any one leaf alone leaves $v$ intact
(still cost $1$). Matroid rank functions always have a pivotal element for
independent sets (the exchange axiom); general dichotomous costs do not. This
kills local-exchange repair arguments generically, not just the specific
induction above.

**Broadened the counterexample search accordingly**, since a genuine obstruction
to the easy proof raises the prior on a counterexample existing. Targeted the
*two-agent* general claim directly (Conjecture~`conj:f5-2balance`, itself still
open) with $5634$ further random rigid bottleneck-cost pairs on a shared
$6$-element ground set: zero violations, on top of the $427$ three-agent trials
and two hand-built adversarial constructions already on record.

**Status: (Q′) is open, general Lemma D (two-agent) is open, and the natural
proof route is now known to be blocked rather than merely untried.** The
remaining candidate directions, none attempted:
(a) a genuinely global argument — LP duality or a flow formulation exploiting
that $n=3$ is a very low-dimensional discrepancy problem, rather than local
exchange; (b) prove two-agent Lemma D first, as a strictly smaller target with
the same core obstruction but one fewer moving part; (c) resume the
counterexample hunt, but away from the bottleneck family — bottleneck costs have
a compact $3$-number sufficient statistic per partition ($a_t,b_t,e_t$) and may
simply be too tame; a real counterexample, if one exists, likely needs a cost
with no bounded-size sufficient statistic at all.

### 7.16.15 Lemma D is proved — audit of the user's `lemma_D_full_proof_verified.md`

The user supplied a full proof of Conjecture~`conj:f5-2balance` (Lemma D): for any
two dichotomous costs $c_1,c_2$ on any finite $U$, some $S\subseteq U$ has
$\abs{c_i(S)-c_i(U\setminus S)}\le1$ for both $i$. This is exactly our own
two-agent conjecture, restated as a two-part split. Audited it in full.

**The technique is different from anything else in this project** — not a
Venn-region/greedy argument but a discrete intermediate-value-plus-parity
argument. Set $d_i(S)=\cost_i(S)-\cost_i(U\setminus S)$; the goal is
$\abs{d_i(S)}\le1$ for both $i$ simultaneously. Fix an ordering of $U$ and look
at $d_i$ along its prefixes: it is non-decreasing (dichotomous costs give edge
increments in $\set{0,1,2}$, §2 of the source) and runs from $\le0$ to $\ge0$, so
each agent has a nonempty interval of "balanced" prefix-positions
$I_i=[L_i,R_i]$ (§3–4). If $I_1\cap I_2\ne\emptyset$ for *some* ordering, done.
Assuming for contradiction it never is, every ordering has a well-defined
*winner* (whichever agent's interval comes first). The proof then shows an
adjacent transposition of the ordering can never change the winner (§5), while
reversing the *entire* ordering always flips it (§6) — and since adjacent
transpositions generate every permutation including the reversal, this is a
direct contradiction (§7).

**Independently re-derived and confirmed:**
- §1–§4 (discrepancy function, edge increments in $\set{0,1,2}$, existence of a
  balanced prefix on every chain via a jump-size argument, the interval
  characterisation) — all correct, checked line by line.
- §6 (reversal flips the winner) — correct; re-derived $I_i^{\mathrm{rev}} =
  [m-R_i,\,m-L_i]$ directly from $S_t^{\mathrm{rev}} = U\setminus S_{m-t}$ and
  complement antisymmetry, and confirmed $R_1<L_2 \iff R_2^{\mathrm{rev}} <
  L_1^{\mathrm{rev}}$. (The source's intermediate chain
  "$m-R_2<m-L_2<m-R_1\le m-L_1$" should read $\le$ throughout when
  $L_2=R_2$ is possible — cosmetic, the conclusion doesn't depend on strictness
  there.)
- §7 (the contradiction) — correct, standard fact that adjacent transpositions
  generate the symmetric group, including the reversal.
- §5's central structural claim — **independently re-derived from scratch**,
  filling in a compressed step: if $S$ (the common prefix before the swapped
  pair) were balanced for agent $1$, then position $\abs S$ lies in $I_1$ on
  *both* orderings (since $I_1$ membership is a fact about the set $S$, not
  about which chain reaches it), which combined with "$\sigma$ won by $1$" and
  "$\sigma'$ won by $2$" forces $d_2(S)$ to be simultaneously $\ge2$ and $\le-2$
  — a direct contradiction. So $S$ cannot be balanced for agent $1$; symmetric
  argument for agent $2$. This confirms the source's claim "$S,T$ cannot be
  balanced for either agent."

**The sign-pinning step (equations 6–7) resisted a second, careful attempt.**
Pushed further on exactly why $A=S\cup\set x$ must be balanced for agent $1$
specifically. Confirmed cleanly, by an argument symmetric to the one above: from
"$S$ balanced for $1$" (assumed) one gets $d_2(S)\le-2$ via chain $\sigma$ *and*
$d_2(S)\ge2$ via chain $\sigma'$ — a real contradiction, so $S$ is not balanced
for $1$; symmetrically not for $2$. But this route pins $\abs{d_1(S)}\ge2$ and
$\abs{d_2(S)}\ge2$ only — it derives the *other* agent's sign at $S$, never
$d_1(S)$'s or $d_2(S)$'s own sign, since the contradiction in each case is a
clash between the two chains' readings of the *same* other-agent quantity. I
could not find a route from the stated hypotheses alone (winner of $\sigma$ is
$1$, winner of $\sigma'$ is $2$, for an unremarkable common prefix $S$ before an
arbitrary adjacent swap) to pinning $d_1(S)\le-2$ specifically rather than
$\ge2$ — both remain consistent with everything derivable from the definitions
of $L_i,R_i$ and the two winner conditions alone. This may well be resolved by
context in the source that a terse write-up compresses (e.g. an implicit
canonical choice of which element is "$x$" vs "$y$"), but I did not reconstruct
it, and without it equations (6)-(9) are not yet an independent derivation on my
part.

**Computational verification, both reproduced and substantially extended:**
- Independently re-implemented the enumeration of *all* dichotomous costs on a
  ground set via the recursive rule $\cost(S) \in [\max_{x\in S}\cost(S\setminus
  x),\ \min_{x\in S}\cost(S\setminus x)+1]$ (valid by the same argument as
  Lemma~`lem:f5-compress`'s Lipschitz property, applied pairwise). Got exactly
  the source's counts $2,6,38,990$ for $\abs U=1,2,3,4$ — an independent
  confirmation of their enumeration, not just a repetition of it.
- Reproduced the exhaustive $\abs U=4$ check from scratch: all $490{,}545$
  unordered pairs (with repetition) of the $990$ costs, zero counterexamples,
  matching the source's table exactly.
- Directly stress-tested §5's central claim (adjacent transposition preserves
  the winner) at $\abs U=5$ ($20{,}000$ trials) and $\abs U=6$: zero flips.
- Specifically hunted, at $\abs U=4$, for an instance realising the *hypothesis*
  of §5 (winner $1$ on $\sigma$, winner $2$ on $\sigma'$ after one adjacent
  swap) in order to inspect $d_1(S)$'s actual sign directly: **zero such
  instances found in $3{,}000{,}000$ random trials.** The scenario the sign
  argument is about appears to simply never arise — consistent with, and further
  evidence for, the theorem, but it also means the sign claim could not be
  checked empirically either (there is no real data realising the hypothesis to
  inspect).

**Verdict: overwhelmingly likely true, not fully certified by this audit.**
Sections 1–4, 6, 7 are independently verified correct. Section 5's conclusion
(adjacent transpositions never flip the winner) has essentially airtight
empirical support — over $3.3$ million combined trials across $\abs U=4,5,6$
with zero violations, including a targeted search for the specific configuration
the proof reasons about. Section 5's *mechanism* — specifically why $d_1(S)$ and
$d_2(B)$ take the signs the source claims — was not independently reconstructed
despite two serious attempts. Recorded as **PROVED, with one identified open
step in the certification** rather than an unconditional theorem; not yet
promoted to the formal LaTeX theorem list on that basis. If the sign step can be
closed (or replaced — my own "$S,T$ not balanced for either agent" argument
above is a complete, verified alternative half of the picture, needing only a
matching argument that forces $T$ back into balance to finish the contradiction
without equations 6–7 at all), this becomes a fully certified second theorem
from the general (non-composed) attack, after Proposition~`prop:f5-noncomposed`.

**Consequence.** Lemma D settles the two-agent case of general Lemma E
unconditionally — any two dichotomous costs, on any ground set split into any
two parts, admit simultaneous spread $\le1$. It does not by itself resolve
(Q′) or three-agent Lemma E (three parts, three agents, is a different and
harder problem — Lemma D's technique is intrinsically about a *single* binary
split, and the winner/parity argument does not obviously generalise to three
simultaneous intervals). But it substantially strengthens the qualitative case
for (Q′): general dichotomous costs, with no composed structure to lean on, are
now *proved* (not just observed) to behave well at $n=2$.

### 7.16.16 (Q′): the counterexample search, now with fully general costs

All earlier searches (§7.16.13) used the bottleneck family
$\min(\abs{S\cap D},\abs{S\cap D'})$ specifically. Using the correct general
enumeration/random-generation method built to audit Lemma D, re-ran the search
with **fully general** random dichotomous costs (filtered to keep only rigid
triples): $20{,}000$ triples each at $\abs M = 4,5,6$ and $40{,}000$ more at
$\abs M = 7$ (from a pool of $56$ rigid costs found among $5000$ random
attempts — rigidity gets rarer under uniform random generation as $\abs M$
grows, consistent with §7.16.13's finding that most rigid costs are highly
structured rather than generic). Zero counterexamples across all
$100{,}000+$ triples. Combined with the bottleneck-specific search and the two
hand-built adversarial constructions, this is now a substantially broader base
of negative evidence than any single family could give — still not a proof, but
the evidence for (Q′) $=$ No now spans both a designed "hard" family and
unstructured random costs.

### 7.16.17 A new, more structured target: contiguous 2-cut partitions (necklace splitting)

Lemma D's technique — a discrete IVT/parity argument over *orderings*, not
Venn regions or local exchange — is genuinely different from everything else
in this project, and Remark~`rem:f5-walk` already names the connection: for
additive costs, the two-agent one-cut version is the discrete necklace-splitting
theorem. That suggests the natural three-agent target: not an arbitrary
3-partition, but a **contiguous** one under some ordering.

> **Conjecture (contiguous 2-cut sufficiency).** For any three dichotomous costs
> $\cost_1,\cost_2,\cost_3$ on $\items$, there is an ordering
> $\sigma=(x_1,\dots,x_m)$ and cut points $0\le p\le q\le m$ such that, writing
> $B_1=\set{x_1,\dots,x_p}$, $B_2=\set{x_{p+1},\dots,x_q}$,
> $B_3=\set{x_{q+1},\dots,x_m}$, every $\mathrm{sp}_i(B_1,B_2,B_3)\le1$.

This is a *strictly stronger* claim than (Q′) — a contiguous partition is a
special case of an arbitrary one, so proving this closes (Q′) (hence general
Lemma E, hence Conjecture~`conj:main` at $n=3$) outright. It is also a much
more structured object than an arbitrary partition: only $\binom{m+2}{2}$
choices of $(p,q)$ per ordering instead of $3^m$ assignments, and the
per-agent behaviour along $p$ and along $q$ separately is monotone (exactly
the structure Lemma D's proof exploits in one dimension).

**Computational support, both random and adversarial:**
- Exhaustive search (all $m!$ orderings, all $\binom{m+2}{2}$ cut pairs) over
  $400$ random rigid triples at $\abs M=4$: zero failures.
- The same exhaustive search on the cyclic-overlap adversarial witness of
  §7.16.13 (the one deliberately built to force three pinch-pairs into mutual
  conflict on $3$ elements): solved immediately, ordering $(a,b,c)$, cuts
  $(0,1)$.
- Randomized search (up to $300$ random orderings per triple, full cut search
  within each): $60$ rigid triples each at $\abs M = 6,7,8$ (rigid pools of
  $40$, increasingly hard to find by uniform random generation — $17{,}886$
  attempts needed at $\abs M=8$): zero failures.

**No proof yet.** Two partial strategies were explored and both stall in
recognisable ways:
- *Two-stage bootstrap via Lemma D twice.* Apply Lemma D to $(\cost_1,\cost_2)$
  to get a $2$-way split $\set{S,\items\setminus S}$ with both spread $\le1$;
  then split $S$ further into $(B_1,B_2)$ to introduce $\cost_3$. Splitting only
  ever *lowers* $\cost_1(B_1),\cost_1(B_2)$ below $\cost_1(S)$ (monotone,
  subsets), so the upper bound relative to $\cost_1(\items\setminus S)$ survives
  automatically; the lower bound ($\cost_1(B_1),\cost_1(B_2)\ge
  \cost_1(\items\setminus S)-1$) does not, and nothing controls it, nor does
  anything about agent $3$'s full three-way spread get addressed by this
  construction at all — $\cost_3$ was never consulted in choosing $S$.
- *Direct two-dimensional generalisation of the winner/parity argument.* Along
  $p$ (fixed $q$), $\cost_i(B_1)$ is monotone non-decreasing; along $q$ (fixed
  $p$), $\cost_i(B_3)$ is monotone non-increasing; $\cost_i(B_2)$ depends on
  both. The one-dimensional "interval of balanced positions" that powers
  Lemma D's proof does not have an obvious two-dimensional analogue — the
  balanced *region* in the $(p,q)$ grid for a single agent is some
  monotone-boundary shape, not an interval, and three such regions need a
  common point. This is the same three-way-simultaneity obstacle that has
  recurred throughout the project, just relocated to a smaller, more structured
  search space.

**Assessment.** This is now the most promising open lead on (Q′): the
strongest and most structured empirical support found so far (surviving
deliberate adversarial construction, not just random search), a natural
connection to a classical theorem (necklace splitting) via a proof technique
already certified correct at $n=2$ (Lemma D), and a search space small enough
that a real proof — rather than another exchange argument — looks plausible.

### 7.16.18 A genuine attempt at the two-dimensional proof: the Lipschitz law, and where it stalls

Attempted the two-dimensional discrete IVT / Sperner-style argument directly.
Did not complete it. What follows is exactly how far it got.

**The "every ordering works" simplification is false — checked properly this
time.** §7.16.17's exhaustive tests happened to hit only easy triples. A
dedicated search (rigid triples at $\abs M=4$, all $24$ orderings checked per
triple) found genuine counterexamples: $2$ of $500$ triples have orderings
admitting no good cut at all, at almost exactly the same rate ($\sim\!0.4\%$)
as the analogous failure rate for Lemma D itself at two agents ($1/200$). So the
theorem, if true, genuinely needs "some ordering," not "every ordering" —
matching Lemma D's own logical shape, not a simplification of it.

**But failing orderings are always adjacent to a working one.** For every bad
ordering found (both failing triples, all $4$ bad orderings between them), some
single adjacent transposition repairs it — confirmed by direct check, not
sampling.

**This sharpens into a clean empirical law.** Define $B(\sigma) := \min_{p\le q}
\max_i \mathrm{sp}_i(B_1,B_2,B_3)$, the best achievable max-spread for a fixed
ordering $\sigma$. Measured $\abs{B(\sigma)-B(\sigma')}$ across every
adjacent-transposition edge touching a bad ordering (both failing $\abs M=4$
triples, all edges) and across a large near-exhaustive sample at $\abs M=5$
(full permutation enumeration, $400$ triples, $\sim\!190{,}000$ edges): the jump
is **never more than $1$**, and often exactly $1$ at the boundary between a good
and a bad ordering. $B$ is also invariant under full reversal
($B(\sigma)=B(\sigma^{\mathrm{rev}})$ in every case checked) — unlike Lemma D's
winner, which *always* flips under reversal, so Lemma D's specific
transposition-invariant/reversal-flips contradiction mechanism does not carry
over as is.

**Attempted to prove the Lipschitz bound directly, and only got a weaker one.**
For an adjacent swap of $x,y$ at the boundary of the optimal cut $(p^*,q^*)$
(the case where the swap moves an element between $B_1$ and $B_2$, leaving
$B_3$ untouched — the only case that can change anything), write
$B_1'=B_1-x+y$, $B_2'=B_2-y+x$. For any agent, removing one element changes
cost by $0$ or $-1$, then adding one element changes it by $0$ or $+1$, giving
$\cost_i(B_1')-\cost_i(B_1) \in \set{-1,0,1}$ and independently
$\cost_i(B_2')-\cost_i(B_2)\in\set{-1,0,1}$, with $\cost_i(B_3)$ fixed. Since
both $B_1,B_2$ (but not $B_3$) can shift, and in principle in *opposite*
directions relative to whatever was the max/min, the crude bound this gives is
$\abs{B(\sigma)-B(\sigma')}\le 2$, not $1$. Looked for a conservation law
tying the two shifts together — e.g. via the invariant $\cost_i(B_1\cup B_2)$,
which genuinely is unchanged by the swap (elements only move between $B_1,B_2$,
never in or out of their union) — but did not find the mechanism ruling out
both shifts landing unfavourably at once. This is an identified, unclosed gap:
the empirical law is stronger than what was derived.

**The strategy this points to, precisely.** Take $\sigma^*$ minimising
$B(\sigma)$ over all $m!$ orderings. If the Lipschitz bound of $1$ were proved,
$\sigma^*$ being a global minimum forces $B(\sigma')\ge B(\sigma^*)$ for every
neighbour $\sigma'$; combined with Lipschitz-$1$, every neighbour has
$B(\sigma')\in\set{B(\sigma^*),B(\sigma^*)+1}$. The remaining step — deriving a
contradiction from "$B(\sigma^*)\ge2$ and every adjacent transposition can only
keep it the same or make it worse" using the specific unit-step marginal
structure at the optimal cut — was not attempted; it is the natural target for
a further attempt and is analogous in spirit to how
Proposition~`prop:f5-pattern` characterised the unique $\Sigma=4$ obstruction
in the assignment-layer problem, but has not been carried out here.

### 7.16.19 The simplest completion is ruled out: same-cut degradation genuinely reaches 2

Continued the attempt at the missing Lipschitz mechanism by checking the most
natural candidate directly: does the *same cut point*, applied before and after
the swap, ever degrade a *single* agent's own three-way spread by more than $1$?
A hand construction using two disjoint sets $P,Q$ (playing the roles
$B_1=P\cup\set x$, $B_2=Q\cup\set y$) suggested this should be achievable if $x$
is redundant and $y$ pivotal for *both* $P$ and $Q$ simultaneously — checked
this is locally consistent (no contradiction in the marginal constraints on a
$4$-element example) but a first attempt at realising it with $P,Q$ singletons
failed for a size reason: a singleton's cost is capped at $1$ by dichotomy, so
the needed gap ($a \ge b+2$) is unreachable. A direct targeted computational
search using larger ground sets removed that artefact and **found the jump
directly**: a single dichotomous cost with $(\cost(B_1),\cost(B_2),\cost(B_3))$
going from $(2,1,1)$ (spread $1$) to $(3,0,1)$ (spread $3$) under one adjacent
transposition of the ordering — a jump of exactly $2$, and not rare ($\sim\!10\%$
hit rate in the search, $1928$ instances out of the sampled cases).

**This rules out the simplest possible completion of the Lipschitz proof.** It
is not true that *any single agent's* same-cut spread is $1$-Lipschitz under
adjacent transposition; the crude bound of $2$ derived by hand in §7.16.18 is
in fact tight at the single-agent, single-cut level. So $B(\sigma)$'s
empirically-observed Lipschitz-$1$ behaviour (§7.16.18: exhaustively confirmed
at $\abs M=4$, near-exhaustively at $\abs M=5$, never once exceeding $1$) is
not a fact about any one agent or any one cut — it must be an emergent,
*joint* property: when one agent's spread would blow up at the inherited cut,
either (a) it does not control the max over all three agents at that moment
(some other agent is already at least that bad), or (b) $\sigma'$ has some
*different* cut, not the one inherited from $\sigma$, that avoids the damage
entirely. Both possibilities require reasoning about the interaction of all
three agents and the full re-optimisation freedom simultaneously — a
substantially harder claim than the one this pass set out to prove, and the
reason the proof is not closed.

**Status: open, and now more precisely so.** Two proof avenues have been
tried and both are now known to fail for identifiable reasons: the
Sperner/topological framing (§7.16.17, boundary conditions do not match the
classical necklace-splitting setup) and the single-agent same-cut Lipschitz
argument (§7.16.19, false in general). What survives, heavily tested and not
yet explained: $B(\sigma)$ itself — the *joint*, re-optimised quantity — does
appear to be genuinely Lipschitz-$1$, and reversal-invariant. A proof, if one
exists along these lines, has to work with the three-agent interaction and the
cut-choice freedom directly, not reduce to a single agent or a fixed cut.

### 7.16.20 What actually repairs the damage, and a reformulation

Pushed one step further: in every one of the $59$ same-cut-jump-$\ge\!2$ cases
found in §7.16.19, checked *which* mechanism rescues $B(\sigma)$ — another
agent already being at least as bad at the old cut, or the new ordering
admitting a genuinely different repairing cut. The result is completely
one-sided: **mechanism (a) never fires ($0/59$); mechanism (b) always does
($59/59$).** So the rescue is never "someone else was already the bottleneck"
— it is always a different cut.

**The repairing cut has an overwhelmingly common, simple form.** In $52$ of
the $59$ cases ($88\%$), the repairing cut for $\sigma'$ is exactly
$(p^*+1, q^*)$ — the $p$-boundary shifted by one, $q$ unchanged. Tracing
through what this means concretely: writing $x,y$ for the swapped pair
($x$ = old last element of $B_1$, $y$ = old first element of $B_2$), the cut
$(p^*+1,q^*)$ applied to the *swapped* ordering gives
$B_1^{\text{new}} = B_1 \cup \set y$ and $B_2^{\text{new}} = B_2 \setminus \set
y$ — **exactly the partition reached by moving the single element $y$ from
$B_2$ to $B_1$ in the *original*, unswapped ordering, with $x$ never touched
at all.** The transposition-and-cut-shift is, in the overwhelming majority of
repair cases, just an elaborate way of describing a single-element move
between adjacent bundles.

**This reframes the missing lemma.** It suggests the object actually doing the
work is not the transposition/reversal structure that powers Lemma D, but a
more basic *anchored* two-way balance statement:

> **Anchored two-way balance (candidate lemma, untested beyond the above).**
> Fix $B_3 \subseteq \items$ and write $v_i := \cost_i(B_3)$ for each agent.
> For $L := \items \setminus B_3$, there is a split $L = B_1 \sqcup B_2$ such
> that for every agent $i$, the three values $\set{\cost_i(B_1), \cost_i(B_2),
> v_i}$ span a window of width at most $1$.

If true, this is exactly Lemma D with a *third, externally fixed* target
value added to the window condition for each agent, rather than only requiring
$B_1,B_2$ close to each other. It is a strictly different (and on its face
harder) statement than Lemma D itself — Lemma D's own winner/parity proof
does not obviously carry an external anchor — and it has not been tested
independently of the contiguous-cut experiments above. This is the most
concrete open target to emerge from this investigation: proving the anchored
lemma (for some judicious choice of $B_3$, e.g. via the same
divisibility/rigidity machinery used for composed costs, or by a genuinely new
argument) would complete the contiguous 2-cut conjecture, hence (Q′), hence
Conjecture~`conj:main` at $n=3$ in full generality.

### 7.16.21 Consolidation: a direct local-search route, precisely scoped and partially proved

Abandoned the ordering/cut machinery for a more direct route: local search on
*arbitrary* 3-partitions (not contiguous ones), moving elements one or two at a
time, minimising $\Phi(B) := \sum_i \max(0, \mathrm{sp}_i(B) - 1)$ — the total
excess spread beyond the uniform-balance target.

**The claim must be scoped to rigid triples — checked precisely, not assumed.**
A "moves always help when $\Phi>0$" claim cannot hold unconditionally: the
$K_4$ witness (`prop:no-balance`, all three $D_i$ of size $3$, hence
non-rigid) has global-minimum $\Phi = 1$, and verified directly that **no move
of any size** (up to moving all $4$ elements at once) improves it — exactly
matching the known fact that uniform balance genuinely fails there.
So the correct target is:

> **Conjecture (2-move sufficiency).** For any three *rigid* dichotomous costs
> and any partition $B$ with $\Phi(B) > 0$, some move of at most $2$ elements
> (each independently reassigned to a possibly different part) strictly
> decreases $\Phi$.

By induction on the integer $\Phi$ (bounded below by $0$, strictly decreasing),
this would give $\Phi = 0$ in finitely many steps — uniform balance for every
rigid triple, i.e. (Q′), hence Conjecture~`conj:main` at $n=3$ **in full
generality**, unconditionally (no ordering/cut machinery, no anchored lemma
needed).

**Computational status: exhaustively verified, properly scoped, at every size
tested.** Earlier tests in this investigation mixed rigid and non-rigid
sampling; redone cleanly:
- $\abs M=4$: $500$ rigid triples, all $3^4=81$ states each checked
  exhaustively for $\Phi>0$ states lacking a $\le2$-move improvement — zero.
- $\abs M=5$: same exhaustive method, $150$ rigid triples, $3^5=243$ states
  each — zero (one *non-2-move* case was found here on an earlier, less
  careful pass, and its true global optimum was independently confirmed to
  reach $\Phi=0$ via $\mathrm{sp}=(1,1,1)$ — the earlier "stuck" state was a
  local-search-with-only-$\Phi$-descent artifact from a bad starting point,
  not a failure of the $2$-move claim from *that* state itself, which does
  admit a $2$-move improvement).
- $\abs M=6$: $80$ rigid triples, all $3^6=729$ states each, exhaustive — zero.
- Randomised (non-exhaustive) spot checks at $\abs M=7,8$ found none needing
  more than a $2$-move, out of several thousand $\Phi>0$ states sampled.

This is now the most rigorously and precisely tested claim in the whole (Q′)
investigation: correctly excludes the one class of instance (non-rigid,
$K_4$-shaped) where it must fail, and holds with zero exceptions everywhere it
should.

**Partial hand proof: the case where a single pivotal element exists.**
Suppose agent $1$ has $\mathrm{sp}_1(B) \ge 2$; write $X,Y,Z$ for the three
parts with $\cost_1(X)$ the max, $\cost_1(Y)$ the min,
$\cost_1(X)-\cost_1(Y)\ge2$. Suppose some $x\in X$ is *pivotal*:
$\cost_1(X\setminus x) = \cost_1(X)-1$. Consider moving $x$ from $X$ to $Y$.
Worked through the case split by hand:
- If $Z \ne \cost_1(X)$ (not tied with the old max), the move strictly
  decreases $\mathrm{sp}_1$ regardless of $x$'s marginal on $Y$.
- If $Z = \cost_1(X)$ (tied with the old max) **and** $x$'s marginal on $Y$ is
  $1$ (not $0$), the move still strictly decreases $\mathrm{sp}_1$ by exactly
  $1$ ($Z$ would otherwise inherit the max role unchanged).
- If $Z = \cost_1(X)$ **and** $x$'s marginal on $Y$ is $0$, this specific move
  achieves *no* improvement for agent $1$ at all — $Z$ silently takes over as
  the new max at the *same* value, and the move must be abandoned in favour of
  a different pivotal element (if one with marginal $1$ on $Y$ exists) or a
  different target part, or a genuinely different move entirely.

So even the *easiest* sub-case (a single pivotal element exists) already
branches into real sub-cases before even checking the other two agents are
not made worse — confirming this is not a one-line argument. Given how many
lemmas the composed-cost route needed to close the analogous case work
(Lemma~`lem:f5-greedy` through Theorem~`thm:f5-target`, over many results),
a full proof of the $2$-move conjecture likely needs comparable investment:
systematically covering (a) single-pivotal cases including the tie-break
above, (b) the no-single-pivotal case (Lemma ivt guarantees *some* subset
reaches the intermediate value, but its complement can have size $\ge3$ in
isolation — §7.16.19 found explicit examples — so the $2$-move guarantee, when
it holds, must come from the joint $3$-agent structure, not from the
single-agent subset-removal problem alone), and (c) verifying the two
*other* agents are never pushed to a net-worse $\Phi$ contribution by whichever
move is chosen for agent $1$.

**Where this stands.** Not a completed proof. It is the most concrete,
best-tested, and most directly promising target found across this entire
session's attack on (Q′) — a single, clean, unconditional statement (no
orderings, no anchoring, no rigidity-to-divisibility translation needed) that
would finish Conjecture~`conj:main` at $n=3$ outright if proved. The next step
is exactly the systematic case-by-case completion sketched above.

### 7.16.22 Pinning down the no-single-pivotal case: the mechanism is not a single-cost fact

Pushed directly on the hardest remaining case. The natural hope was a clean
standalone lemma: *if $\cost(X)=2$ and no single element of $X$ is pivotal,
some pair is.* Tested this exact statement, restricted precisely to
$\cost(X)=2$ (not a general value) so it matches the spread-exactly-$2$
scenario that actually arises: **false**. Direct search across
$\abs M = 6,7,8,9$ found $357$ explicit subsets (out of $133{,}292$ checked
with no single pivotal element) where **no pair works either** — genuinely
needing $3$ elements removed to reach the intermediate value, at
$\cost(X)=2$ specifically, sizes $\abs X \in \set{4,\dots,7}$, not a rare
edge case restricted to large $\cost(X)$.

**This rules out the natural standalone lemma as the explanation.** Whatever
makes the full $2$-move sufficiency conjecture true for rigid triples (and it
does appear to be true — exhaustively verified at $\abs M=4,5,6$ with zero
exceptions, §7.16.21), it cannot be reducible to a fact about one agent's cost
function in isolation. The mechanism has to be genuinely emergent: either (a)
rigidity itself rules out this "hard" ($\ge3$-removal) subset structure from
ever coinciding with being the max-part of a $\Phi$-minimal-but-positive
partition, or (b) when agent $1$'s own fix would need $\ge3$ elements, the
$2$-move that actually works targets something else entirely — a different
agent, or elements not in $X$ at all (e.g. increasing $\cost_1(Y)$ via an
element from $Z$, rather than decreasing $\cost_1(X)$). Attempted to construct
a clean embedded example isolating which of these fires, but could not
assemble a small enough instance (the found "hard" subsets need most of a
$6$–$9$-element ground set for themselves, leaving too little room to also
build a controlled, verifiably-rigid $3$-agent scenario around them within
practical search effort).

### 7.16.23 The actual mechanism, found: removal-hardness forces a small insertion-witness

Continued past §7.16.22's negative finding by asking the right follow-up
question. §7.16.22 showed the fix cannot be "shrink $X$ by removing $\le2$
elements." But a hand-built, fully-understood example (a "redundant-OR"
gadget: $\cost(S) = [v_1{\in}S \lor w_1{\in}S \lor \{a,b\}{\subseteq}S] +
[\text{same pattern on a disjoint second team}]$, verified dichotomous by
direct marginal check, verified to need exactly $3$ elements removed to drop
from $2$ to $1$) revealed the real mechanism directly: moving $v_1$ and $w_1$
out of $X$ into the two low parts **doesn't shrink $X$ at all** ($X$ keeps
$\cost_1(X)=2$ throughout, via the surviving $\{a,b\}$ leaves) — it **raises
the two low parts instead**, because $v_1,w_1$ are redundant inside the
crowded set $X$ but individually sufficient ($\cost_1(\set{v_1})=1$) once
isolated. The fix was never about reducing the max; it was about the
elements causing the redundancy being independently powerful in a smaller
context.

**Generalised and tested at scale.** The natural hypothesis: a
removal-hard $X$ (no $\le2$-element removal reaches $\cost(X)-1$) always
contains a small *insertion-witness* — either two elements each individually
positive ($\cost(\set x)\ge1$), or one pair jointly positive
($\cost(\set{x,y})\ge1$) — obtainable at budget $\le2$ and usable to raise a
low part instead of shrinking $X$. Tested directly against $485$ removal-hard
instances ($\cost(X)=2$, $\abs M$ up to $10$, freshly generated, not reusing
§7.16.22's sample): **every single one** has such a witness ($485/485$).
Refined further by checking the *minimal* insertion-witness size directly
under the removal-hardness hypothesis across $546$ instances: size $1$ in
$545$, size $2$ in exactly $1$, **size $\ge3$ in zero**. Removal-hardness
appears to force insertion-easiness essentially always, and by a comfortable
margin (a lone counterexample at size $2$, none at size $3$, out of hundreds).

**Not yet a completed proof.** Attempted a direct argument via a chain
$x_1,\dots,x_k$ built up to $X$: since $\cost(X)=2$, exactly two steps of any
such chain are the "+1" steps, at positions $i<j$ say. The natural hope —
that $\cost(\set{x_i})\ge1$ on its own — does **not** follow just from $x_i$
causing a jump *in that chain*, since the jump is relative to whatever
elements preceded it, not to $\emptyset$; a genuine proof needs to relate a
chain-relative marginal to an absolute singleton/pair cost, which is exactly
where the argument currently stalls. The empirical margin (zero failures at
size $\ge3$ out of $546$, one at size $2$) is strong enough that this reads
as a true theorem waiting for the right argument, not a coincidence, but the
argument itself has not been found.

**If proved, this would complete the whole chain.** Removal-hardness forcing
a small insertion witness, combined with the already-complete easy-case proof
(§7.16.21) and the (already precisely identified) bookkeeping needed to check
the other two agents aren't pushed net-worse, would close the $2$-move
sufficiency conjecture, hence (Q′), hence Conjecture~`conj:main` at $n=3$ in
full generality — unconditionally, with no ordering/cut machinery and no
composed-cost structure required anywhere in the argument.

**Assessment at this point.** This session found the actual mechanism by
which the local-search route works — not a hoped-for property that turned
out false (§7.16.22), but a real, heavily-tested structural fact
(removal-hardness $\Rightarrow$ small insertion-witness) discovered by tracing
through a hand-built, fully-understood example rather than more random
search. What remains is one precise combinatorial lemma about dichotomous
set functions, stated exactly, tested at a scale that makes it very unlikely
to be false, with the general chain-based proof attempt identified and its
exact sticking point named. This is substantially closer to a full proof of
Conjecture~`conj:main` at $n=3$ than anything found earlier in this session.

### 7.16.24 Confirming the mechanism directly: a pure AND-gadget is forced to be removal-easy

Pushed on *why* large minimal witnesses (a "pure $k$-AND" with $k\ge3$, no
smaller subset triggering it, the one structure that would break the pattern)
never coexist with removal-hardness — tested this directly rather than only
by broad random search.

**A bare $3$-AND is removal-easy, exactly as hypothesised.** Built
$\cost(S) = [\set{p,q,r}\subseteq S] + [v\in S]$ (a pure $3$-AND term plus an
unrelated singleton term, $\cost(X)=2$ on $X=\set{p,q,r,v}$) and checked
removal directly: $\cost(X-p)=\cost(X-q)=\cost(X-r)=1$ — every one of
$p,q,r$ is individually pivotal, because nothing else can substitute for a
missing member of the AND. So a bare $k$-AND with $k\ge3$ makes $X$
removal-*easy*, never removal-hard — consistent with never appearing as an
obstruction to the $\le2$ insertion-witness claim.

**Adding the backup that would rescue $p,q,r$ from single-removal
reintroduces a small witness by construction.** Built
$\cost(S) = [\set{p,q,r}\subseteq S \lor v_1\in S \lor w_1\in S] + [z\in S]$.
Now $\cost(X-p)=\cost(X-q)=\cost(X-r)=2$ — $p,q,r$ are protected, exactly
because $v_1,w_1$ back them up. But $v_1,w_1,z$ are each themselves a
size-$1$ insertion witness ($\cost(\set{v_1})=\cost(\set{w_1})=\cost(\set z)=1$),
confirming directly: the *same* backup elements that make the AND-gadget's
members removal-safe are the small witnesses the conjecture needs. There is
no way seen so far to protect a large AND-witness from single-removal without
introducing exactly this kind of small independent witness alongside it.

**This is the shape a complete proof would take**, though it is not yet one:
by strong induction on the size of a minimal cost-$1$ witness $A\subseteq X$.
Base cases $\abs A\in\set{1,2}$ give the claim directly. For $\abs A\ge3$,
every $a\in A$ is pivotal *within $A$* (minimality), so removal-hardness of
$X$ (which says $a$ is *not* pivotal within the larger $X$) forces some
"backup" mechanism specific to $X\setminus A$ to be doing the protecting —
and by Lemma ivt applied to $X - a$ (which still has cost $2$, since $a$
wasn't pivotal), that backup manifests as a witness $Z_a \subseteq X - a$ with
$\cost(Z_a)=1$. The two hand-built examples above show concretely what $Z_a$
looks like when it exists cleanly ($\set{v_1}$ or $\set{w_1}$ — size $1$).
What is missing is a general argument that $Z_a$ (or a minimal witness inside
it) is *always* smaller than $A$ itself, which would close the induction; this
has not been established for arbitrary dichotomous cost structures, only
confirmed on hand-built and randomly-generated instances.

### 7.16.25 Working the induction with pure mathematics: the value-$2$ minimal witness

Switched from inducting on a minimal *value-$1$* witness $A$ (§7.16.23–24,
where large witnesses like a bare $k$-AND exist as standalone objects with no
further structure to exploit) to inducting on a minimal *value-$2$* witness
$B\subseteq X$ — i.e. $c(B)=2$ and no proper subset of $B$ reaches $2$. This
has genuinely more structure to work with.

\begin{lemma}
\label{lem:f5-value2shrink}
If $B$ is minimal with $\cost(B)=2$, then $\cost(B\setminus\set b)=1$ exactly,
for every $b\in B$.
\end{lemma}

\begin{proof}
Minimality gives $\cost(B\setminus\set b)\le1$ (else the proper subset
$B\setminus\set b$ would already reach $2$). The marginal bound gives
$\cost(B\setminus\set b)\ge\cost(B)-1=1$. Together, equality.
\end{proof}

**This resolves $\abs B=3$ completely, with no computation.** If $\abs B=3$,
then for any $b\in B$, $B\setminus\set b$ is a $2$-element set with cost
exactly $1\ge1$ — directly a valid $\le2$-element insertion witness. Done.

**For $\abs B=4$, the lemma pins down the exact internal structure.** Applying
Lemma~\ref{lem:f5-value2shrink} to all four $b\in B=\set{b_1,b_2,b_3,b_4}$,
and then minimality of each resulting triple $B\setminus\set{b_i}$ (cost $1$,
so every proper subset of it costs $0$), forces: every pair and singleton
*within $B$* costs $0$, and every triple costs $1$. This is realised exactly
by the threshold function $\cost(S) = \max(0,\abs{S\cap B}-2)$ — i.e. $B$'s
internal structure, if it resists a size-$2$ witness at all, is forced to look
like a simple counting threshold. Crucially, this internal function is
removal-*easy*: removing any single $b_i$ drops the cost from $2$ to $1$
directly. So for the *enclosing* $X\supseteq B$ to stay removal-hard despite
$B$'s internal easiness, $X\setminus B$ must supply a backup protecting each
$b_i$ — reintroducing exactly the "redundant-but-individually-powerful
element" mechanism found by hand in §7.16.23–24.

**A second, independent structural fact, proved directly.** For any two
elements $x,y\in X$: order $X$ as $(X\setminus\set{x,y})$, then $x$, then $y$.
Since $\cost(X\setminus\set y)=\cost(X)=2$ (single removal-hardness), $y$'s
marginal in this order is $0$; since
$\cost(X\setminus\set{x,y})=\cost(X\setminus\set y)=2$ (pair removal-hardness),
$x$'s marginal is also $0$. So **the full cost $2$ is already achieved by
$X$ minus any chosen pair** — removal-hardness is not merely "nothing helps
when removed," it means the entire value is already present in every
$(\abs X{-}2)$-sized subset. This is a clean, general, unconditionally proved
fact (not requiring $\abs B\ge4$ or any case split).

**Where the induction still stalls.** The natural next step is to iterate
this second fact — peel off disjoint pairs one at a time, always retaining
cost $2$, until reaching a residual set small enough to apply
Lemma~\ref{lem:f5-value2shrink} directly. This does not yet go through:
removal-hardness of $X$ gives $\cost(X - x - y) = 2$ for a pair removed
*directly from $X$*, but says nothing about whether $X - x - y$ is *itself*
removal-hard for a second pair — that would require
$\cost(X - x - y - x' - y') = 2$, a $4$-element removal from $X$, which is
outside the hypothesis entirely. Nothing in the argument so far propagates
removal-hardness down to derived subsets, which is exactly the barrier
identified from the other direction in §7.16.23 (the $Z_a$-smaller-than-$A$
gap). Both routes converge on the same missing step: some argument that lets
hardness (or a witness bound) survive being handed down to a smaller instance,
which has not been found.

**One more layer worked out: the forced internal structure is uniform, not
growing.** If $B$'s internal structure (assuming no $\le2$-witness anywhere)
is forced to the threshold form $\cost(S)=\max(0,\abs{S\cap B}-2)$ — verified
exactly for $\abs B=4$ above, and the same minimality cascade forces the
identical form for any $\abs B=k$: every pair costs $0$, every triple costs
$1$, matching $\max(0,m-2)$ at $m=2,3$ — then *every* minimal value-$1$
witness living purely inside $B$ has size exactly $3$ ($\max(0,3-2)=1$,
$\max(0,2-2)=0$), regardless of how large $k=\abs B$ grows. So Lemma ivt
applied inside $B$ alone can never produce a witness smaller than $3$ this
way — confirming precisely, not just by example, that if $B$ has this forced
form, the escape to a $\le2$ witness cannot come from within $B$'s own
elements at all, and must come from $X\setminus B$. This sharpens the
remaining target: show that whatever in $X\setminus B$ is needed to protect
$B$'s individually-pivotal elements from removal-hardness's violation is
itself forced to contain a $\le2$-element witness — the missing propagation
step is now confined to *that* specific sub-question, not the general one.

**Pushing the confined sub-question to its exact final form.** Fix
$b_i\in B$. Define $f:2^{X\setminus B}\to\set{1,2}$ by
$f(T) = \cost((B\setminus\set{b_i})\cup T)$; this is well-defined, monotone,
with $f(\emptyset)=\cost(B\setminus\set{b_i})=1$ and $f(X\setminus B) =
\cost(X\setminus\set{b_i}) = 2$, and inherits unit marginal steps from
$\cost$ itself. So $f$ is exactly a "shifted" dichotomous function
(base value $1$, not $0$), and Lemma~\ref{lem:f5-ivt}-style reasoning applies
to it directly: there is a *minimal* $T^\ast\subseteq X\setminus B$ with
$f(T^\ast)=2$, i.e. adding $T^\ast$ to $B\setminus\set{b_i}$ completes the
missing unit, and no proper subset of $T^\ast$ does.

If $\abs{T^\ast}=1$, write $T^\ast=\set{w^\ast}$: then $w^\ast$'s marginal
*on top of $B\setminus\set{b_i}$* is exactly $1$
($\cost((B\setminus\set{b_i})\cup\set{w^\ast})=2 \ne 1 =
\cost(B\setminus\set{b_i})$). This is precisely the situation realised by
$v_1,w_1$ in the §7.16.23–24 hand-built examples, where $w^\ast$ additionally
turned out to be *absolutely* positive ($\cost(\set{w^\ast})\ge1$ with no
help from $B$ at all) — which is exactly the $\le2$-element witness needed.
**This is exactly the point the argument does not close in general.** A
marginal of $1$ *conditional on* $B\setminus\set{b_i}$ being present does not,
for a general (non-submodular) dichotomous cost, imply a positive marginal on
the empty set — the compression argument used throughout the composed-cost
route (Lemma~`lem:f5-compress`) relied on the single-count structure of
composed costs precisely to rule this gap out, and no analogous fact is
available here. It is entirely possible, as far as this argument shows, for
$w^\ast$'s usefulness to depend essentially on $B\setminus\set{b_i}$'s
"almost-complete" presence, in which case $w^\ast$ alone contributes nothing
and the search for a small witness would have to continue elsewhere. Whether
this scenario can actually be realised by a valid dichotomous cost *while
simultaneously keeping $X$ removal-hard* is the single remaining open
question; every attempt to construct such an example by hand in this session
instead produced a $w^\ast$ (or similar element) with genuine absolute
positive cost, but no argument was found ruling out the alternative in
general.

### 7.16.26 A direct hand-built counterexample attempt, and why it fails

Attempted to directly construct the counterexample the previous section
could not rule out: a set $X$, fully removal-hard (single *and* pair), with
$c(X)=2$ and no absolute $\le2$-witness anywhere — i.e. an explicit witness
that Conjecture~\ref{conj:f5-2move} (informal name for the $2$-move
sufficiency claim) is false.

**Construction.** $B=\set{b_1,b_2,b_3,b_4}$ with the forced threshold
$\cost_B(S)=\max(0,\abs{S\cap B}-2)$. Add $w^\ast$ with
$\cost(S) = \min\!\big(2,\ \cost_B(S\cap B) + [\,w^\ast\in S \wedge
\abs{S\cap\set{b_2,b_3,b_4}}\ge2\,]\big)$ — $w^\ast$ conditionally completes
whichever single $b_i$ is missing, but $\cost(\set{w^\ast})=0$ absolutely
(checked directly: the trigger needs two of $\set{b_2,b_3,b_4}$ present,
which $\set{w^\ast}$ alone does not supply). Capping a monotone unit-step sum
at a constant $K$ always preserves the unit-step property (if $g(S)<K$ then
$g(S\cup x)\le K$ automatically, since marginals are $\le1$), so this
construction is a valid dichotomous cost.

**It fails pair-removal-hardness immediately.** $\cost(X - b_1 - w^\ast) =
\cost(\set{b_2,b_3,b_4}) = \cost_B(\dots) + 0 = 1 \ne 2$: removing $b_1$ and
$w^\ast$ together drops the cost, so this $X$ is not actually removal-hard by
the full (single-and-pair) definition the theorem needs.

**Patched — and immediately broken elsewhere.** Adding a second backup
$w_2^\ast$ with an OR-trigger
($[(w^\ast\in S \vee w_2^\ast\in S)\wedge\abs{S\cap\set{b_2,b_3,b_4}}\ge2]$)
fixes $\set{b_1,w^\ast}$ and $\set{b_1,w_2^\ast}$ (whichever backup survives
covers for the other). But now $\cost(X-b_1-b_2) = \cost_B(\set{b_3,b_4}) +
[(\top)\wedge\abs{\set{b_3,b_4}\cap\set{b_2,b_3,b_4}}\ge2] = 0 + 1 = 1 \ne 2$:
removing the *internal* pair $\set{b_1,b_2}$ breaks it, a vulnerability the
first fix never touched.

**Why this is not just bad luck — the deficit doubles but the fix cannot.**
$\cost_B(\set{b_3,b_4})=0$ is two below the target of $2$, but any single
OR-trigger is a $0/1$ indicator, contributing at most $+1$. No single
backup mechanism of this kind can ever repair a pair-removal that drops
$\cost_B$ by a full $2$ — repairing $\set{b_1,b_2}$ needs a *second*,
independent $+1$ source, which (being itself a fresh trigger) needs its own
protection against removal, on top of everything already patched. Each
patch closes one class of vulnerability while the combinatorics of
$\binom{4}{2}=6$ internal pairs (plus every cross-pair with each new backup
element) keeps producing more. This was not carried through to a formal
non-existence proof, but the obstruction is structural, not incidental: it
is the same "protection budget" tension identified abstractly in
§7.16.25's final gap, now seen concretely resisting an actual construction
attempt.

**Reading.** A genuine, serious, hands-on attempt to build the counterexample
that would refute the $2$-move sufficiency conjecture failed, and failed in a
way that points at *why* it's likely to keep failing (the deficit-vs-trigger
counting mismatch) rather than a superficial bug in one specific
construction. This is evidence, not proof, but it is evidence of a
qualitatively different kind than the computational testing in earlier
sections: a deliberate adversarial construction, pushed by hand to find the
exact failure mode, rather than a search over random instances.

**One genuine (partial) propagation result, found while revisiting the
induction barrier.** §7.16.25 stated that removal-hardness cannot be handed
down to a smaller instance. That is not quite right — it hands down by
exactly one level. For $b_1\in X$, write $Y := X\setminus\set{b_1}$; then
$\cost(Y)=2$ (single removal-hardness of $X$), and for any $y\in Y$,
$\cost(Y\setminus\set y) = \cost(X\setminus\set{b_1,y}) = 2$ by *pair*
removal-hardness of $X$ applied to $\set{b_1,y}$ — so $Y$ is itself
single-removal-hard, inherited directly. What does **not** propagate is $Y$'s
own pair-removal-hardness: that would need $\cost(Y\setminus\set{y,y'}) =
\cost(X\setminus\set{b_1,y,y'})=2$, a $3$-element removal from $X$, outside
the hypothesis entirely. So the descent runs out after exactly one step —
consistent with, and a sharper version of, the barrier already identified,
but confirming it is a *hard* stop after one level rather than an immediate
one.

### 7.16.27 Splitting on $\cost(X\setminus B)$: one full case closes, two remain

Returned to the minimal value-$2$ witness $B\subseteq X$ (the case $\abs
B\ge4$) and split on $\cost(X\setminus B)\in\set{0,1,2}$, using
removal-hardness of $X$ applied to *every* pair $\set{b_i,b_j}\subseteq B$ at
once: since $\cost(B\setminus\set{b_i,b_j})=0$ (any pair inside the forced
threshold structure), pair removal-hardness gives
$\cost\big((X\setminus B)\cup(B\setminus\set{b_i,b_j})\big)=2$, i.e.
$\cost\big((X\setminus B)\cup P\big)=2$ for *every* pair $P\subseteq B$
(relabelling the complementary pair as $P$).

\begin{itemize}
\item[$\cost(X\setminus B)=2$:] **This case is fully resolved.** $X\setminus
  B$ is itself a value-$2$ witness, strictly smaller than $X$ (as $B$ is
  nonempty). Apply Lemma ivt to it directly to get a minimal witness
  $B'\subseteq X\setminus B$. If $\abs{B'}\le3$,
  Lemma~\ref{lem:f5-value2shrink} finishes the whole argument immediately. If
  $\abs{B'}\ge4$ too, repeat — each round the *ground set itself* shrinks by
  at least $4$ elements (the size of the witness just peeled off), so on a
  finite $X$ this recursion **must terminate**, either at a witness of size
  $\le3$ or by exhausting the ground set. No gap remains in this case.

\item[$\cost(X\setminus B)=0$:] Building $(X\setminus B)\cup\set{b_i,b_j}$ in
  either order (add $b_i$ then $b_j$, or $b_j$ then $b_i$) must reach cost
  $2$ from $0$ over exactly $2$ steps each $\le1$ — forcing *both* steps to
  be exactly $+1$, in *either* order. This forces
  $\cost\big((X\setminus B)\cup\set{b_i}\big)=1$ for **every** $b_i\in B$
  individually (not just one of each pair) — sharper than the general
  $w^\ast$ analysis of §7.16.25, but the same fundamental question remains
  open: this is a marginal *conditional on $X\setminus B$*, and nothing here
  forces $\cost(\set{b_i})\ge1$ absolutely.

\item[$\cost(X\setminus B)=1$:] Strictly less constrained than the $0$ case —
  the single unit of increase across a pair's two steps can split unevenly
  between $b_i,b_j$ with no forced uniform conclusion for either.
\end{itemize}

**Net effect.** One of three cases is now completely closed by a clean,
terminating argument. The entire remaining difficulty in the whole $2$-move
sufficiency conjecture is confined to exactly two sub-cases
($\cost(X\setminus B)\in\set{0,1}$) of one step of one induction. Whether a
cleverer choice of *which* minimal witness $B$ to peel off (if $X$ admits
several) can always land in the resolved case, or whether the $0/1$ cases
themselves admit a similar closing argument, is the precise open frontier. Four facts are now fully
proved, unconditionally, for general dichotomous costs: Lemma ivt's
intermediate-value property; Lemma~\ref{lem:f5-value2shrink}
($\cost(B\setminus b)=1$ for a minimal value-$2$ witness); the $\abs B=3$
resolution; and the pair-removal-preserves-full-cost fact
("$\cost(X)=\cost(X\setminus\set{x,y})$ for a removal-hard $X$, any pair").
These combine to reduce the entire remaining question — the whole gap between
what is proved here and a full proof of Conjecture~`conj:main` at $n=3$ — to
one precisely stated combinatorial question about whether a *conditionally*
pivotal element (pivotal only in the presence of a specific large context)
must also be *absolutely* pivotal, under a removal-hardness hypothesis. This
is now a clean, self-contained, checkable mathematical statement — a real
narrowing, even though it was not resolved in this session.

### 7.17 Status

| statement | status |
|---|---|
| Observation 1, Proposition 2 | **proved** |
| **Lemma A** ($\Sigma\le3 \Rightarrow$ good) | **proved** |
| Corollary 3 (the reduction) | **proved** |
| Lemma A contains `thm:balanced-class` | **proved** |
| the $\Sigma=4$ pattern $v_i=v_k=(2,2,0)$, $v_j=0$ | **proved** |
| Lemma B, Lemma C | **proved** |
| **Lemma F** (individual minimum $\mu_i \le 1$) | **proved** |
| **Corollary G** (Lemma E needs a spread-$0$ agent) | **proved** |
| **Lemma H** (additive rigidity: spread $\ne 1$ when $3 \mid \lvert D_i\rvert$) | **proved** |
| **Theorem I** (exact refutation criterion for Lemma E) | **proved** |
| the residue reduction and signed reformulation | **proved** |
| **Theorem J** ((Q) holds when every set has $\le 2$ active regions) | **proved** |
| the complete constraint taxonomy by $(p_i,q_i)$ | **proved** |
| **Lemma K** (a private region suffices at $d_i = 3$) | **proved** |
| **Theorem M** ((Q) holds when every $d_i \in \{1,3\}$) | **proved** |
| **Lemma N** (the hypothesis forces the private region active) | **proved** |
| **Theorem I′** (Lemma E fails iff three *rigid* agents evade S4) | **proved** |
| rigidity computed for additive / capped / threshold | **proved** |
| **Lemma O** (compression), **Cor. P**, **Cor. Q**, **Cor. R** | **proved** |
| "non-additive $\Rightarrow$ not rigid" | **RETRACTED** — $\min(\lvert S\cap D\rvert,3)$, $\lvert D\rvert=4$ (§7.11) |
| **(Q′)** (can three rigid agents evade S4?) | **open** — closes $n=3$ if No |
| **Theorem S** (two sets balance simultaneously, any $k$) | **proved** |
| **Corollary T** (`prop:no-balance` needs all three sets) | **proved** |
| **Corollary U** (Lemma D for *composed* costs) | **proved** |
| **Lemma D** for arbitrary dichotomous costs | **open** |
| **Corollary V** (two sets of size $3\mid\lvert D\rvert$ go to spread $0$ together) | **proved** |
| the $K_4$ instance: no uniform balance, yet $\Sigma = 2$ | **proved** |
| **(R)** reduces to the Target Theorem in every case that arises | **proved** |
| **Lemma W** (greedy levelling — the engine; re-proves Lemma F and Theorem S) | **proved** |
| **Lemma X** (in-region placement of $D_3$) | **proved** |
| **Corollary Y** (structural feature every residual instance must have) | **proved** |
| **Target Theorem** (two sets within 1, third within 2) | ~~open~~ → **PROVED** as Theorem EE below; must be read in the *nominating* form (§7.16.11) |
| the "spread $0$ iff $3 \mid c(M)$" criterion | **RETRACTED** — false without additivity (§7.9) |
| **Theorem Z** ((Q) holds when no private region is active) | **proved** — subsumed by Z′ |
| **Lemma K″** (private knob absorbs a levelled shared part) | **proved** |
| **Lemma K‴** (knob rescue when $G_i$ has three distinct values) | **proved** |
| **Theorem Z′** — **(Q) holds in full** | **PROVED** |
| **Corollary Q′** (residual instance must contain a set of size divisible by 3) | **proved, now unconditional** |
| Theorem I′'s "only if" direction | **RETRACTED** — forward direction only (§7.16.2) |
| **Lemma E** | ~~open~~ → **PROVED for composed costs** (Theorem FF); open in general |
| **Theorem AA** (interleaved greedy: two within 1, third within 3) | **PROVED** |
| **Theorem BB** ($n=3$ closed when **two** sizes divisible by 3) | **PROVED** — subsumed by FF |
| **Lemma CC** (greedy keeps spread $\le \max(\text{old},1)$) | **PROVED** |
| **Lemma DD** (tie-break: $\mathrm{spread}(H) \le 2$) | **PROVED** |
| **Theorem EE — the Target Theorem** | **PROVED** |
| **Theorem FF — Conjecture 2 at $n=3$ for composed costs** | **PROVED** |
| rigid **non-composed** dichotomous costs exist (explicit witness) | **PROVED** — so FF's method cannot extend |
| general $n=3$ reduces to **(Q′)** | **PROVED** |
| **(Q′)** (three rigid costs vs uniform balance) | **open** — a *No* is necessary, not sufficient, for general $n=3$ (§7.16.11) |
| **Lemma E** ($\min \Sigma \le 3$), general dichotomous costs | **open** |
| **Lemma D** (two-agent balance) | **open** |
| audit of the user's verification dossier (§7.16.11) | **done** — chain correct; nominating form required; "residual ⇒ composed" false |
| audit of second findings pass (§7.16.12) | **done** — confirms Theorem EE/FF independently; no new math; one catalog of reported (unverified) leads for (Q′) |
| unbounded family of rigid non-composed costs (§7.16.13) | **proved** — corrects the "must be small" reading of the §7.16.9 witness |
| hunt for a (Q′) counterexample (§7.16.13) | **negative on every attempt** — 2 adversarial hand-constructions + 427 random rigid triples, all admit uniform balance; evidence toward (Q′) = No, not a proof |
| direct proof attempt on (Q′) via up-set-chain generalisation of Lemma K″ (§7.16.14) | **blocked, identified precisely** — no context-independent "private lever" outside composed costs |
| one-element induction for (Q′) | **fails** — explicit two-agent stuck configuration exhibited |
| pivotal-element / exchange property for general dichotomous costs | **REFUTED** — star-cover witness with no removable element |
| **Lemma D / Conjecture~`conj:f5-2balance`** (two agents, general costs, any 2-way split) | **overwhelmingly likely true, PROVED pending one step** (§7.16.15) — architecture (§§1-4,6,7) independently verified; §5's conclusion has $3.3M$+ trials with zero violations; §5's sign mechanism not independently reconstructed after two attempts; not yet promoted to LaTeX |
| (Q′) search with fully general (not just bottleneck) random costs (§7.16.16) | **negative on $100{,}000{+}$ triples** at $\abs M=4,5,6,7$ — broadens, does not replace, the evidence toward (Q′) $=$ No |
| **contiguous 2-cut conjecture** (§7.16.17) — strictly implies (Q′) via a necklace-splitting-style claim | **open, strong evidence** — exhaustive at $\abs M{=}4$ ($400$ triples incl. the adversarial cyclic witness), randomized at $\abs M{=}6,7,8$; two proof strategies attempted and stalled; most promising open lead |
| "every ordering works" simplification (§7.16.18) | **REFUTED** — genuine failing orderings exist, $\sim0.4\%$ rate, matching Lemma D's own failure rate |
| $B(\sigma)$ Lipschitz-$1$ law under adjacent transposition (§7.16.18) | **open, exhaustively/near-exhaustively tested** — jump never $>1$ at $\abs M=4,5$; only a Lipschitz-$2$ bound derived by hand; the tighter mechanism not found |
| $B(\sigma)$ invariance under full reversal (§7.16.18) | **tested, holds** — unlike Lemma D's winner, which always flips; rules out reusing Lemma D's exact contradiction mechanism |
| extremal-argument proof strategy for the contiguous conjecture (§7.16.18) | **precisely stated, not carried out** — needs a structural contradiction from local optimality at the unit-step level, analogous to Prop.~`prop:f5-pattern` |
| single-agent same-cut Lipschitz-1 (the natural completion of §7.16.18) | **REFUTED** (§7.16.19) — explicit jump-of-2 instance found, $(2,1,1)\to(3,0,1)$, not rare ($\sim\!10\%$ hit rate) |
| rescue mechanism when same-cut jump $\ge2$ occurs (§7.16.20) | **always re-optimised cut, never another agent** — $59/59$, $0/59$ |
| repairing cut $=$ single-element move (§7.16.20) | **$88\%$ of cases** ($52/59$) — cut shift $(+1,0)$ is algebraically a move of one element between adjacent bundles |
| **anchored two-way balance** (candidate lemma, §7.16.20) | **open, not yet tested** — the most concrete remaining target; would complete the contiguous conjecture, hence (Q′), hence Conjecture 2 at $n=3$ in general |
| $K_4$ (non-rigid) as a test of the 2-move claim's scope (§7.16.21) | **confirmed** — global-min $\Phi=1$, no move of *any* size improves it, correctly excluded by the rigid-only scoping |
| **2-move sufficiency conjecture** (§7.16.21) — direct, unconditional route to Conjecture 2 at $n=3$ | **open, exhaustively verified at $\abs M=4,5,6$** (properly rigid-scoped, zero exceptions across tens of thousands of states); **best candidate found this session** |
| single-pivotal-element case of the 2-move conjecture (§7.16.21) | **partially proved by hand** — resolves cleanly except when the third part ties the old max and the pivotal element's marginal there is $0$ |
| "no single ⟹ some pair works" as a standalone single-cost lemma (§7.16.22) | **REFUTED at $\cost(X)=2$ exactly** — $357$ explicit counterexamples; the 2-move mechanism cannot be single-agent, must be emergent from rigidity + all 3 agents jointly |
| overall assessment: six independent proof strategies for (Q′) | **all attempted, each blocked for an identified reason** — composed no-pivotal machinery, up-set chain, one-element induction, Sperner/necklace, anchored Lemma D, local-search 2-move; genuinely new mathematics needed to close it |
| **removal-hardness $\Rightarrow$ small insertion-witness** (the actual 2-move mechanism, §7.16.23) | **open, extremely strongly tested** — $485/485$ and $546/546$ ($545$ at size $1$, $1$ at size $2$, zero at size $\ge3$); precise chain-based proof attempt identified with exact sticking point named; the single remaining piece needed to close Conjecture 2 at $n=3$ in full |
| bare $k$-AND ($k\ge3$) forced removal-easy (§7.16.24) | **confirmed directly** — every AND-member individually pivotal when nothing backs it up |
| backup elements protecting an AND-gadget $=$ the small witnesses (§7.16.24) | **confirmed directly** on two hand-built examples — the induction's shape is right, general "$Z_a$ always smaller than $A$" step not yet established |
| **Lemma~`lem:f5-value2shrink`** ($\cost(B{-}b)=1$ for minimal value-$2$ witness $B$) | **PROVED** (§7.16.25), unconditional |
| $\abs B=3$ case of the value-$2$ induction | **PROVED** (§7.16.25) directly, no computation needed |
| $\abs B=k$ forced internal structure is the threshold $\max(0,\abs{S\cap B}-2)$ (§7.16.25) | **PROVED** — internal witnesses stuck at size $3$ uniformly, escape must come from $X\setminus B$ |
| pair-removal preserves the full value ($\cost(X)=\cost(X-x-y)$ for removal-hard $X$) (§7.16.25) | **PROVED**, unconditional, general |
| conditional-vs-absolute pivotal-ness of the backup element $w^\ast$ (§7.16.25) | **open — the single remaining gap.** Precisely stated: does a marginal of $1$ on top of a specific large context force a positive marginal on $\emptyset$, under removal-hardness? Closing this closes Conjecture 2 at $n=3$ in full |
| direct hand-built counterexample attempt (§7.16.26) | **FAILED to construct one** — single OR-trigger backup breaks on the first internal-pair removal it wasn't designed for; patching one vulnerability opens another (deficit-vs-trigger counting mismatch), suggestive but not a proof of non-existence |
| removal-hardness propagates one level (§7.16.26) | **PROVED** — $X$'s pair-hardness gives $X{-}b_1$ single-hardness directly; confirmed to run out after exactly one step, not zero |
| case $\cost(X\setminus B)=2$ of the value-2 induction (§7.16.27) | **FULLY CLOSED** — finite terminating recursion, no gap |
| case $\cost(X\setminus B)=0$ (§7.16.27) | **open, sharpened** — every $b_i\in B$ individually has marginal $1$ on $X\setminus B$ (not just one per pair); conditional-vs-absolute question remains |
| case $\cost(X\setminus B)=1$ (§7.16.27) | **open** — less constrained than the $0$ case, no forced uniform conclusion yet |
| $B(\sigma)$ Lipschitz-1 (the true, joint quantity) | **open** — must be an emergent 3-agent + re-optimised-cut phenomenon, not reducible to one agent or one cut |

(F5\*) at $n = 3$ is **closed on the composed family** — Theorem FF, via
Theorem EE and Lemma A — and open outside it, where it reduces to Lemma E for
general dichotomous costs and thence to (Q′). Everything above is unconditional.

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
