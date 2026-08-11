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
| **Target Theorem** (two sets within 1, third within 2) | **open** — closes $n=3$ on the composed family |
| the "spread $0$ iff $3 \mid c(M)$" criterion | **RETRACTED** — false without additivity (§7.9) |
| **Theorem Z** ((Q) holds when no private region is active) | **proved** |
| **(Q)** in general | **open** — only $d_i = 4$ sets survive, and only one sub-case |
| **Lemma E** ($\min \Sigma \le 3$) | **open** — reduces to (Q) on the additive side |
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

---

## 9. Session update — 2026-08-11: the next obstruction is isolated

This section records the conclusions reached in the latest proof attack. It is deliberately separated from the earlier development so that a future AI agent can distinguish established results from the remaining conjectural step.

### 9.1 Status correction: do **not** promote Lemma D to an arbitrary-dichotomous theorem

The file `lemma_D_full_proof.md` contains a proof attempt for the following statement:

> **Lemma D (claimed general form).** For any two dichotomous costs on a finite ground set, there exists a bipartition $S,U\setminus S$ for which both agents have spread at most $1$.

This proof is **not currently certified**. In particular, the current main development already correctly records that Lemma D for arbitrary dichotomous costs is open. Do not cite the proof attempt as an established theorem.

What *is* established is the following stronger-in-its-own-domain result:

> **Theorem S (two-set balance).** For any two set-based additive/composed costs represented by underlying sets $D_1,D_2$, and any number $k$ of bundles, there is a $k$-colouring that splits both underlying sets within one.

The proof is the Venn-region/excess-vector construction in §7.13. fileciteturn58file5L300-L328

For composed costs $c_i(S)=f_i(|S\cap D_i|)$ with monotone $0/1$ increments, this implies simultaneous spread-$\le1$ for the composed costs themselves. This follows from the compression lemma. fileciteturn58file8L454-L469

### 9.2 The $\Sigma=4$ obstruction is unique

At $n=3$, Lemma A establishes:

1. If a minimum-cost assignment has an arc of weight at least $2$, then $\Sigma\ge4$.
2. If all arcs have weight at most $1$ but a two-path has weight $2$, then $\Sigma\ge5$.
3. Therefore, if $\Sigma\le3$, every minimum-cost assignment is good.

The proof is purely matching-optimality based and does not use family minimality, balance, or an exchange argument. fileciteturn56file2L120-L147

Consequently, if Lemma E fails, the first possible obstruction is exactly at $\Sigma=4$, and it must be an arc-weight-$2$ obstruction. Equality in the matching optimality inequalities forces, after relabelling agents and bundles,

$$
\boxed{v_i=v_k=(2,2,0),\qquad v_j=(0,0,0).}
$$

Here the coordinates are ordered as $(\sigma(i),\sigma(j),\sigma(k))$. fileciteturn57file0L47-L55

Equivalently, the two problematic agents $i,k$ have cost profiles

$$
(m_i+2,m_i+2,m_i),\qquad
(m_k+2,m_k+2,m_k),
$$

while agent $j$ is constant across the three bundles.

This is the **only** $\Sigma=4$ failure mode currently known/proved from the matching optimality analysis.

### 9.3 Why the obvious two-bundle attack is insufficient

A tempting next step is to merge $B_1$ and $B_2$, apply a two-agent balancing theorem to $B_1\cup B_2$, and then restore $B_3$.

This does not solve the problem. Balancing the restriction to $B_1\cup B_2$ only proves

$$
|c_i(X)-c_i(Y)|\le1,
\qquad
|c_k(X)-c_k(Y)|\le1,
$$

for $X\sqcup Y=B_1\cup B_2$. It gives no control over the comparison with the fixed third bundle $B_3$.

The generic failure mode is already visible for a capped cost such as

$$c(S)=\min(|S|,2),$$

with

$$
B_1=\{1,2\},\quad B_2=\{3,4\},\quad B_3=\varnothing.
$$

The merged two-way partition can have costs $(2,2)$, perfectly balanced on $B_1\cup B_2$, while the three-way profile remains $(2,2,0)$ and therefore has spread $2$.

Thus:

> **Negative result.** A proof of the residual theorem cannot merely balance $B_1\cup B_2$ while keeping $B_3$ fixed. The third bundle must participate in the exchange.

### 9.4 The correct local objective: turn $(2,2,0)$ into a spread-$\le1$ profile

For either problematic agent, the obstruction is

$$
(2,2,0)
$$

up to an additive constant. The desired repair is therefore of the form

$$
(2,2,0)\longrightarrow(2,1,1),
$$

or another profile with spread at most $1$.

A single-item move $x:B_a\to B_b$ changes each dichotomous cost by a binary marginal at the source and a binary marginal at the destination. For a problematic agent, the move that reduces a heavy bundle by one without increasing the destination has the marginal signature

$$
(1,0)
$$

in the natural ``loss at source / gain at destination'' convention.

To repair **both** problematic agents with one move, the desired common signature is therefore

$$
\boxed{(1,1)}
$$

for the pair $(i,k)$.

### 9.5 What has been ruled out: a common-pivotal-item proof is not enough

The latest attack considered whether the existence of the two simultaneous gaps

$$
(c_i(B_1)-c_i(B_3),\;c_k(B_1)-c_k(B_3))=(2,2)
$$

forces an item with a common improving marginal signature.

It does not follow from dichotomousness alone. Different items may realize incompatible marginal signatures for $i$ and $k$, and there is no currently proved pigeonhole principle forcing a single item to be pivotal for both agents in the required direction.

Therefore:

> **Negative result.** The remaining $\Sigma=4$ obstruction cannot be closed by a one-item/common-pivot argument alone.

The missing information must come from **global consistency of the marginal system across the three bundles**, not from an isolated item.

### 9.6 The remaining precise target: a three-bundle exchange theorem

The clean remaining target is to prove that the profile

$$
(2,2,0)\text{ for both }i,k
$$

cannot be exchange-minimal.

A useful formalization is to examine the six directed elementary transfers

$$
B_1\to B_2,\ B_1\to B_3,\ B_2\to B_1,\ B_2\to B_3,
\ B_3\to B_1,\ B_3\to B_2.
$$

For each transfer, record its two-agent marginal signature

$$
\tau(x;a\to b)=(\tau_i,\tau_k)\in\{-1,0,1\}^2.
$$

The desired proof should establish a global statement of the following form:

> **Open Exchange Target.** If both $i$ and $k$ have profile $(2,2,0)$ (up to additive constants), then the six directed transfer signatures cannot all avoid a sequence of transfers that reduces the total spread. Equivalently, the obstruction is not exchange-minimal.

This is **not proved yet**. It is the next mathematically precise target.

### 9.7 Why this target is better than the discarded routes

The exchange target uses all three bundles simultaneously, exactly where the merged-two-bundle argument loses information. It also avoids assuming a common pivotal item. Most importantly, it attacks the only remaining $\Sigma=4$ configuration rather than reopening the already settled cases.

The logical chain to preserve is:

$$
\boxed{
\text{Lemma E}
\Longrightarrow
\text{a family with }\Sigma\le3
\Longrightarrow
\text{good minimum-cost assignment}
\Longrightarrow
\text{F5* at }n=3.
}
$$

The first implication remains the only open existence step in the residual $n=3$ route. The reduction to Lemma E is unconditional. fileciteturn57file0L36-L45

### 9.8 Established structural reductions that should not be retried

The following facts are already established and should be treated as lemmas/results, not conjectures:

- A minimum-cost assignment depends only on normalized costs $v_i$, and its objective is the minimum of $F(\sigma)=\sum_i v_i(\sigma(i))$. fileciteturn56file0L18-L28
- For $n=3$, goodness is characterized by: (a) every assigned normalized cost $x_i\le1$, and (b) no two consecutive weight-$1$ arcs forming a weight-$2$ path. fileciteturn56file0L30-L50
- $\Sigma\le3$ implies every minimum-cost assignment is good. fileciteturn56file2L120-L147
- Hence F5* at $n=3$ reduces to Lemma E: every three-agent dichotomous instance admits a partition with total spread at most $3$. fileciteturn57file0L34-L45
- Every individual dichotomous agent can be made spread $\le1$; consequently, if no uniformly balanced family exists, a minimum-total-spread obstruction must have profile $(0,0,2)$, $(0,0,3)$, or $(0,1,2)$. fileciteturn58file4L239-L254
- For additive costs, the divisibility rigidity lemma holds: if $3\nmid|D_i|$, spread $0$ is impossible; if $3\mid|D_i|$, spread $1$ is impossible. fileciteturn58file6L357-L366
- For composed costs $f_i(|S\cap D_i|)$ with monotone $0/1$ increments, spread is compressed relative to the underlying additive count cost. fileciteturn58file8L459-L469
- If $3\mid|D_i|$, an equal split of $D_i$ gives that agent spread exactly $0$, independently of the particular composed function $f_i$. fileciteturn58file9L526-L536
- The two-set balance theorem is proved for underlying sets, and therefore all known residual composed instances reduce to a genuinely three-set interaction rather than a two-set obstruction. fileciteturn58file5L306-L328

### 9.9 AI-agent continuation protocol

When continuing this project, do **not** restart the entire search. Start from the following state:

1. **Do not retry:** CRI-depth, arbitrary spread-2 selection, balanced bundle sizes, nonempty-bundle selection, or the already refuted broad selectors. Their failures are recorded in §6.
2. **Do not treat `lemma_D_full_proof.md` as a certified proof** of arbitrary dichotomous Lemma D.
3. **Do use Theorem S** for two underlying sets and composed costs.
4. **Do use Lemma A** to reduce every possible $\Sigma\le3$ failure to the unique $\Sigma=4$ arc obstruction.
5. **Attack only:**
   $$
   v_i=v_k=(2,2,0),\qquad v_j=0.
   $$
6. First test a **three-bundle exchange theorem**. Do not assume the existence of a single item simultaneously pivotal for both problematic agents.
7. Any new claimed lemma must be checked against capped costs and arbitrary monotone $0/1$-marginal costs before being promoted to the main theorem chain.
8. Preserve the distinction between:
   - arbitrary dichotomous costs;
   - additive costs $|S\cap D|$;
   - composed costs $f(|S\cap D|)$.

### 9.10 Current frontier

At the end of this session, the mathematically honest status is:

$$
\boxed{
\begin{array}{c}
\text{F5* at }n=3\\[2mm]
\Downarrow\\[2mm]
\text{Lemma E: }\min_B\Sigma(B)\le3\\[2mm]
\Downarrow\\[2mm]
\text{only possible first obstruction: }\Sigma=4,\\
(v_i,v_k,v_j)=((2,2,0),(2,2,0),(0,0,0))\\[2mm]
\Downarrow\\[2mm]
\textbf{OPEN: three-bundle exchange theorem.}
\end{array}}
$$

No stronger conclusion should be recorded until that final exchange step is proved or a genuine counterexample is constructed.
