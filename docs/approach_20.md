# Approach 20 — (INTERVAL) reduced to two elementary lemmas

*The three-block balancing statement, which approach 19 could only verify, now
has a proof modulo two explicit facts about a single walk. Everything else in
the argument is proved outright, and both remaining facts are exhaustively true
over the entire valuation class at $m=3$ and $m=4$.*

---

## 0. The statement and the state of its proof

> **(INTERVAL).** For any general binary $v$ and any linear order
> $g_1,\dots,g_m$, there are cuts $0 \le a \le b \le m$ with
> $\max_j v(B_j) - \min_j v(B_j) \le 1$, where $B_1,B_2,B_3$ are the three
> consecutive blocks.

| step | status |
|---|---|
| 1. the two-bundle lemma | **proved** (approach 19 §1) |
| 2. the path $a \mapsto (a, b(a))$ exists | **proved** — step 1 applied to each suffix |
| 3. $v(L(a))$ is 1-Lipschitz | **proved** — one marginal |
| 4. **(L)** $\mu(a)$ is 1-Lipschitz | *open*; exhaustive at $m=3,4$ |
| 5. $D$ is 2-Lipschitz, so it cannot step over $\set{0,1}$ | **proved** from 3 + 4 |
| 6. **(E)** the endpoints straddle the window | *open*; exhaustive at $m=3,4$ |
| 7. $D \in \set{0,1} \Rightarrow$ spread $\le 1$ | **proved** |

Steps 5–7 are the intermediate-value argument. (L) and (E) are the whole gap,
and both are statements about one valuation and one walk — no envy graph, no
subsidy, no three-agent structure.

---

## 1. The construction

Fix the order. For $0 \le a \le b \le m$ write

$$L(a) = \set{g_1..g_a},\quad \mathrm{Mid}(a,b) = \set{g_{a+1}..g_b},\quad R(b) = \set{g_{b+1}..g_m}.$$

**The path.** For each $a$, the suffix $\set{g_{a+1},\dots,g_m}$ carries a
general binary valuation in its own right, so the two-bundle lemma applies to
it: some cut splits it into two blocks within $1$ of each other. Let $b(a)$ be
the least such cut. Along the path $a \mapsto (a,b(a))$,

$$\abs{v(\mathrm{Mid}) - v(R)} \le 1 \qquad \text{for every } a. \tag{$\ast$}$$

**The two quantities.** Put

$$\mu(a) = \min\bigl(v(\mathrm{Mid}), v(R)\bigr), \qquad D(a) = v(L(a)) - \mu(a).$$

By $(\ast)$ both middle and right blocks lie in $\set{\mu, \mu+1}$.

## 2. Step 7 — why the window is $\set{0,1}$, and it is an implication

> If $D(a) \in \set{0,1}$ then the cut $(a,b(a))$ has spread $\le 1$.

*Proof.* $D \in \set{0,1}$ says $v(L) \in \set{\mu, \mu+1}$. By $(\ast)$ the
other two blocks are also in $\set{\mu,\mu+1}$. All three values lie in a set of
two consecutive integers, so the spread is at most $1$. $\square$

This is where the earlier attempt went wrong. The natural guess is the window
$\abs{D} \le 1$, and it is **false**: $D = -1$ puts block 1 at $\mu-1$ while
another block sits at $\mu+1$, a spread of $2$. Measured, $\abs D \le 1$
occurred in every instance but implied a good cut in only 176,419 of 197,547 at
$m=4$ — about 89%. The window $\set{0,1}$ implies it in **all** of them, by the
proof above rather than by measurement.

## 3. Steps 5 and 6 — the intermediate-value argument

$v(L(a{+}1)) - v(L(a))$ is a single marginal, hence in $\set{-1,0,1}$. Given
**(L)**, $\mu$ moves by at most $1$ too, so

$$\abs{D(a{+}1) - D(a)} \le 2 .$$

A step from $D \le -1$ to $D \ge 2$ would be a jump of at least $3$. **So $D$
cannot step over the window** — it can only enter it.

The endpoints are computable. At $a=m$ both other blocks are empty, so
$\mu(m) = 0$ and $D(m) = v(M)$. At $a=0$ block 1 is empty, so $D(0) = -\mu(0)$.
Given **(E)** — that these lie on opposite sides of the window, or one of them
is already inside — $D$ must land in $\set{0,1}$, and step 7 finishes. $\square$

## 4. The two open lemmas, and their evidence

> **(L)** Along the path, $\abs{\mu(a{+}1) - \mu(a)} \le 1$.

This is the surprising one. The cut $b(a)$ is **not** Lipschitz — it jumps by up
to $5$ at $m=6$ — yet the *level* it defines moves by at most one. The balanced
level of a suffix is stable even when the cut achieving it moves a long way.

> **(E)** $D(0)$ and $D(m)$ are not on the same side of $\set{0,1}$.

| | (L) holds | (E) holds |
|---|---|---|
| $m=3$, all **495** valuations | 495 | 495 |
| $m=4$, all **197,547** valuations | 197,547 | 197,547 |
| $m=5$, 3,000 sampled | 3,000 | 3,000 |
| $m=6$, 800 | 800 | 800 |
| $m=7$, 250 | 250 | 250 |
| $m=8$, 80 | 80 | — |
| climbs at $m=5,6$ | 100 climbs, **0** refutations | **0** |

For (E) the split is worth recording: at $m=4$, an endpoint already lies in the
window in 189,980 cases and the endpoints straddle it in 7,567. **The same-side
case never occurred at all** — not once in 198,042 exhaustive valuations, nor
in any sample.

**A partial proof of (E).** The same-side-high case needs
$\mu(0) \le -2$ and $v(M) \ge 2$: both halves of $M$ at value $\le -1$ while
$M$ itself is $\ge 2$. Each half then differs from $M$ by at least $3$, so by
the marginal bound each of the two blocks has at least $3$ items and
$m \ge 6$. So **(E) is automatic for $m \le 5$**, which is a genuine fragment
— the remaining question is only whether the configuration can be realised at
all for larger $m$, and no search has produced one.

## 5. What (INTERVAL) does and does not give

It gives **(BAL-1)** — every single valuation admits a three-block partition of
spread $\le 1$ — for each agent separately. The chain to PS2 needs a *common*
partition:

$$\text{(INTERVAL)} \Rightarrow \text{(BAL-1)} \;\longrightarrow\;
\underbrace{\text{(TWO-BALANCE)}}_{\text{still open}} \Rightarrow
\text{(AVOID-1ROW)} \Rightarrow \text{(AVOID)} \Rightarrow \text{PS2}(n{=}3)$$

But (INTERVAL) reshapes (TWO-BALANCE) usefully. Since it holds for **every**
order, both agents' good cuts live in the *same* triangle of
$\binom{m+2}{2}$ points, for any order we care to fix. (TWO-BALANCE) becomes:

> do the good-cut sets of two general binary valuations, inside one triangle of
> cuts, necessarily intersect for at least one of the three pairs of agents?

That is a question about two subsets of a small explicit poset, rather than
about partitions of $M$. It is also known to be delicate in the right way: the
*every-pair* version is false (approach 19 §2, 28 counterexamples at $m=3$), so
whatever argument settles it must use the freedom to choose which pair.

## 6. Progress on (L): one lemma proved, one route closed

### Proved — sign constancy, and which side the level lives on

Along the walk on an ordered set $S$, write $d_t = v(P_t) - v(Q_t)$. Since
$P_0 = \emptyset$ and $Q_k = \emptyset$,

$$d_0 = -v(S), \qquad d_k = +v(S),$$

and steps satisfy $\abs{d_{t+1}-d_t} \le 2$ as in §3. So $d$ **cannot cross**
from $\le -2$ to $\ge 2$ without entering $[-1,1]$: before the least balanced
cut $t^*$, every $d_t$ has the same sign. That pins down which block realises
the level:

> **Fact 1 (proved).**
> - $v(S) \ge 2$: $d$ starts at $\le -2$, so $d_{t^*} \in \set{-1,0}$, hence
>   $v(P) \le v(Q)$ and $\beta(S) = v(P_{t^*})$ — the **prefix**.
> - $v(S) \le -2$: $d$ starts at $\ge 2$, so $d_{t^*} \in \set{0,1}$ and
>   $\beta(S) = v(Q_{t^*})$ — the **suffix**.
> - $\abs{v(S)} \le 1$: $d_0$ is already in $[-1,1]$, so $t^* = 0$ and
>   $\beta(S) = \min(0, v(S))$.

Verified in the corrected form on **1,485** ordered suffixes at $m=3$ and
**790,188** at $m=4$ — always, along with the step bound itself.

*Recorded because it cost a run:* the first version of this had the orientation
backwards, asserting $\beta$ was the suffix value in the main case. The machine
check failed at 972 of 990, which is what exposed it. The direction matters —
the prefix case is the useful one, since prefixes of $S$ and of
$S' = S \setminus \set{s_1}$ differ by exactly one item and so their values are
within 1.

### Refuted — the cut-shift route

That correspondence suggested a clean finish. Deleting the first element shifts
the cuts by one, and $P_{j+1}(S) = P'_j(S') \cup \set{s_1}$, so if the least
balanced cut also shifted by one, $\beta(S)$ and $\beta(S')$ would be values of
prefixes differing by a single item and (L) would follow at once. The claim to
check was

> **(SHIFT).** $\abs{\,t^*(S) - 1 - t^*(S')\,} \le 1$.

**It is false.** 962 of 990 at $m=3$, 576,381 of 592,641 at $m=4$, with shifts
of up to $3$ there and up to $4$ at $m=6,8$. The least balanced cut can move a
long way when one item is deleted. **This route is closed**, and the write-up
records it so it is not tried again.

### (L) itself, verified much more strongly

The same sweep tests (L) over *every* pair (suffix, shorter suffix) rather than
only those on one path:

| | pairs tested | (L) holds | largest $\abs{\beta(S)-\beta(S')}$ |
|---|---|---|---|
| $m=3$, exhaustive | 990 | **990** | 1 |
| $m=4$, exhaustive | **592,641** | **592,641** | 1 |
| $m=6$, sampled | 7,500 | 7,500 | 1 |
| $m=8$, sampled | 2,800 | 2,800 | 1 |

So (L) is not a fact about the particular path — it is a property of the
balanced level as a function of the suffix, and the bound of $1$ is attained,
so it is tight.

**Where a proof must now come from.** Fact 1 puts $\beta$ on the prefix side in
the main case, and prefix values move by at most one per cut, so
$\abs{\beta(S)-\beta(S')} \le \abs{t^*(S)-1-t^*(S')} + 1$. (SHIFT) would have
bounded that, and does not. What the data says instead is that when the cut
moves far, the prefix values along the way must be nearly flat — which is
plausible, because between the two cuts the walk is trapped at $d \le -2$, and
that constrains how $v(P_t)$ and $v(Q_t)$ can move together. Making that
precise is the next step.

## 7. Next

1. **Prove (L).** The statement to aim at is about suffixes alone: writing
   $\beta(S)$ for the balanced level of an ordered set $S$ at its least balanced
   cut, (L) says $\abs{\beta(S) - \beta(S \setminus \set{\text{first}})} \le 1$.
   No three-block structure is involved.
2. **Finish (E).** §4 proves it for $m \le 5$. What remains is to show the
   same-side configuration — every block of a balanced split at $\le -1$ while
   the whole set is $\ge 2$, or its mirror — cannot arise on the path.
3. **(TWO-BALANCE)** in the triangle formulation of §5.

### Scripts

`path.py` (the balanced path and that it always contains a good cut),
`path_ivt.py` (Lipschitz behaviour of $\mu$ and $D$; why $\abs D\le1$ is the
wrong window), `window.py` ((L), (E), and that the window implies a good cut),
`endpoints.py` (the endpoint classification of §4).
