# PS1 working note — FINDSINK, weight forcing, and the type-ordered restriction

**Version** v1, 2026-08-03.
**Status** Theorem F1, F2, F3 **proved** (F2 is the decisive one). Proposition F4
**refuted** by an explicit $n=3,m=2$ counterexample. Conjecture H1″ is **new and open**,
supported by exhaustive + randomised search (`typeorder.py`, `stress.py`).
**Depends on** `approach_3.tex` (replica transform, coverage, peel process) and R3
Algorithms 1–3 (`ALG`, `EXTEND`, `FINDSINK`).

---

## 0. The proposal

Two ingredients, which turn out to have opposite fates and must be assessed separately.

* **(O) Ordering.** Run R3's `ALG` on the replica instance $\hat I$ with the goods
  presented in *type blocks*: all $n-1$ copies of $b_1$, then all $n-1$ copies of $b_2$,
  and so on.
* **(W) Weight forcing.** Inflate the value of the block currently being allocated so that
  a copy of $b_j$ is worth far more than everything already handed out. The intended
  effect: receiving a copy drives the recipient's subsidy to $0$; since `ALG` allocates
  only to maximally subsidised agents, an agent who already holds a copy of $b_j$ is
  never chosen again inside block $j$; hence coverage.

The diagnosis behind the proposal is **correct** (§1). The remedy is **structurally
unable to reach the failure** (§2). The ordering, taken on its own, is **live and
appears to cost nothing** (§3), but the recipient rule proposed with it is **false**
(§4).

---

## 1. The diagnosis is right: only FINDSINK can create a duplicate

**Theorem F1.** In any run of `ALG` on $\hat I$, the `EXTEND` branch never places a
duplicate. Every coverage violation is created by `FINDSINK`.

*Proof.* `EXTEND` (R3 Alg. 2) only ever returns a pair $(\rho,k)$ drawn from the loop over
$k\in[n]$, $\ell \in \mathcal M(p)$ satisfying
$v_k(A_\ell \cup \{g\}) - v_k(A_\ell) = 1$, and it places $g$ into the bundle $B_k = A_\ell$.
So the bundle that receives $g$ has strictly positive marginal for $g$. In $\hat I$ a copy
of $b_j$ has marginal $\hat v_i(S \cup \{b\}) - \hat v_i(S) = 0$ whenever $j \in \tau(S)$,
because $\hat v_i$ factors through $\tau$. Hence the receiving bundle contains no copy of
$j$, and no duplicate is created. $\square$

So the proposal correctly localises the whole difficulty in one subroutine.

---

## 2. The weight lever cannot reach that subroutine

**Theorem F2 (FINDSINK operates only in the zero-marginal regime).** Suppose `ALG` reaches
Line 8, i.e. $(A,p)$ is **not** extendable with $g$. Then every agent $\ell \in \mathcal M(p)$
satisfies $v_\ell(A_\ell \cup \{g\}) - v_\ell(A_\ell) = 0$.

*Proof.* Suppose some $\ell \in \mathcal M(p)$ had marginal $1$. Run `EXTEND`'s loop at
$k = \ell$. Line 3 computes a maximum-weight matching $\rho$ on the complete bipartite
graph between $[n]\setminus\{\ell\}$ and $[n]\setminus\{\ell\}$ with weights $v_i(A_j)$;
maximality gives $\sum_{i \ne \ell} v_i(A_{\rho(i)}) \ge \sum_{i\ne\ell} v_i(A_i)$, since
the identity is one of the matchings compared. Line 4 sets $\rho(\ell)=\ell$, adding
$v_\ell(A_\ell)$ to both sides. So Line 5's welfare test passes and `EXTEND` returns
$(\rho,\ell)$ — contradicting non-extendability. $\square$

**Corollary F3 (the recipient's subsidy is *exactly preserved*, never zeroed).** Let $s$ be
the agent returned by `FINDSINK` and $A' = (A_1,\dots,A_s\cup\{g\},\dots,A_n)$. Then
$\ell_{A'}(s) = \ell_A(s)$.

*Proof.* R3's Lemma 9 gives $s \in \mathcal M(p)$, so Theorem F2 gives
$v_s(A_s\cup\{g\}) = v_s(A_s)$. Hence every arc out of $s$ is unchanged:
$w'(s,k) = v_s(A_k) - v_s(A_s \cup \{g\}) = w(s,k)$. Arcs not incident to $s$ are
unchanged; only arcs *into* $s$ can rise. By R3's Lemma 9 the allocation $A'$ is
envy-freeable, so it has no positive cycle and $\ell_{A'}$ is the maximum weight over
**simple** paths; a simple path out of $s$ never re-enters $s$ and therefore uses only
unchanged arcs. $\square$

This is fatal to (W), for three separate reasons.

1. **The lever multiplies a zero.** The premise "the receiving agent's subsidy is forced to
   $0$" holds only when the recipient's marginal for $g$ is positive. Theorem F2 says that
   in the `FINDSINK` branch it is provably $0$, and scaling by any weight $W_j$ leaves
   $0 \cdot W_j = 0$. Corollary F3 makes it exact: the recipient's subsidy does not move at
   all. Inflation works in the `EXTEND` branch, which by Theorem F1 was never broken.

2. **A duplicate is `FINDSINK`'s *safest* move.** The second copy of $b_j$ leaves
   $\tau(B_x)$ unchanged, hence changes **no arc of the envy graph whatsoever**
   (Duplicate-extraction lemma). So when `FINDSINK` tentatively assigns it to its initial
   arbitrary $s \in \mathcal M(p)$, the subsidy vector is literally identical, the guard
   "$\exists\, j$ with $\varphi_j \ge 2$" is false on the first test, and the while-loop
   exits immediately returning $s$. A duplicate is never rejected because there is nothing
   to detect. This is the same phenomenon recorded in the peel dead-end analysis: at the
   dead end the algorithm's one legal move is to spend a copy on a duplicate, and doing so
   is free.

3. **The scaling forfeits R3's guarantee anyway.** With block weights $W_1 \ll W_2 \ll \cdots$
   the marginals lie in $\{0, W_j\}$, not $\{0,1\}$. R3's Lemma 11 concludes $p \in \{0,1\}^n$
   from "*subsidies are nonnegative integers for dichotomous valuations*"; that step, and
   the weight-$\le 1$ path bounds throughout Lemmas 9–11, are gone. Using (W) is not
   *applying* R3, it is writing a new algorithm and a new proof.

**Where (W) does bite, and where it stops.** Within block $j$, once some agent has been
relieved of $a_j$ while others still hold it, the arcs into the relieved agent from any
holder $k$ with marginal $1$ carry $+W_j$, so $\mathcal M(p)$ collapses onto exactly the
holders who care — and those are precisely the agents for whom `EXTEND` applies. The lever
therefore *keeps `FINDSINK` from firing at all*, which is why it looks like it works. It
runs out exactly when every remaining holder of $a_j$ has marginal $0$: then nothing is
inflated, $\mathcal M(p)$ reverts to stale values from earlier blocks, and an
already-relieved agent can sit at the top of it. Minimal shape: $n=3$ and a chore $a_j$
with marginal $1$ for one agent and $0$ for the other two — after the single caring agent
is relieved, the two remaining holders are invisible to the weights.

---

## 3. The ordering, on its own, is live — and looks free

Strip (W) and read (O) in the peel frame, where coverage is automatic (a peel deletes $j$
from $\mathcal W_x$, so the same pair $(x,j)$ cannot be peeled twice). Then

> **(O) = decide the owner of $a_1$ first, then $a_2$, then $a_3$, …**

and the state after $r$ complete blocks is $\mathcal W_i = A_i^{(r)} \cup R$ with $R$ the
undecided chores — literally the conditioned-remainder principle, with the mid-block states
being $\mathcal W_i = A^{(r)}_i \cup R$ or $A^{(r)}_i \cup R \setminus \{j\}$. This is a
**far smaller state space** than the general peel process: a state is
(partial allocation, current chore, set of agents already relieved of it).

**Computational finding (`typeorder.py`, `stress.py`).**

| instance family | no legal schedule at all | no *type-ordered* legal schedule |
|---|---|---|
| obstruction witness $c_1=\max(0,|S|-1)$, $c_2=c_3=|\cdot|$ | 0 | **0** |
| random dichotomous $n{=}3,m{=}2$ (300) | 0 | **0** |
| random dichotomous $n{=}3,m{=}3$ (300) | 0 | **0** |
| random dichotomous $n{=}3,m{=}4$ (150) | 0 | **0** |
| random dichotomous $n{=}4,m{=}3$ (100) | 0 | **0** |
| random dichotomous $n{=}4,m{=}4$ (40) | 0 | **0** |

The chore *order* is not free — in $8/120$ instances at $n{=}3,m{=}3$, $16/60$ at
$n{=}3,m{=}4$ and $8/60$ at $n{=}4,m{=}3$ only some orders admit a legal schedule — but in
every instance tested **some** order does.

Note that the legal schedule exhibited for the witness in `approach_3.tex` is *not*
type-ordered (it interleaves $a_1$ and $a_2$). The table says a type-ordered one exists
anyway, which was not obvious.

**Conjecture H1″ (new, open).** From the root, some chore order $\pi$ and some choice of
owner and within-block sequence per chore reaches a terminal state with the invariant
holding at every intermediate state.

H1″ $\Rightarrow$ H1′ $\Rightarrow$ Conjecture 2, and H1″ is a strictly smaller search
problem than H1′. It is the right next target.

---

## 4. The proposed recipient rule is false

**Proposition F4 (refuted).** *"Give the next copy to an agent of maximum subsidy"* does not
suffice, even under the type-ordering.

*Counterexample.* $n=3$, $m=2$, all costs monotone with marginals in $\{0,1\}$:

| | $\emptyset$ | $\{a_1\}$ | $\{a_2\}$ | $\{a_1,a_2\}$ |
|---|---|---|---|---|
| $c_1$ | 0 | 0 | 0 | 1 |
| $c_2$ | 0 | 1 | 1 | 1 |
| $c_3$ | 0 | 0 | 0 | 1 |

Exhaustive search over both chore orders, both roles, and all within-block sequences finds
**no** legal type-ordered schedule in which every recipient lies in
$\arg\max_i \ell_{\mathcal W}(i)$. Dropping only the $\arg\max$ restriction, the schedule
relieve $1$ of $a_1$, relieve $3$ of $a_1$, relieve $1$ of $a_2$, relieve $3$ of $a_2$
is legal and terminates at $A = (\emptyset, \{a_1,a_2\}, \emptyset)$ with $\ell = (0,1,0)$.

This is the same signal as the balance remark in `approach_3.tex` — a subsidy-based
recipient rule alone is not enough — now confirmed *inside* the type-ordered restriction,
which is the sharper statement.

---

## 5. Where this leaves things

* **(W) is closed.** No weighting of the replica items can make `FINDSINK` reject a
  duplicate, because `FINDSINK` runs precisely where every candidate's marginal is $0$, and
  a duplicate moves no arc at all. Combined with the earlier no-go on valuation-level
  penalties, **the whole family "encode coverage into the numbers and reuse R3 as a black
  box" is now closed from two directions.**
* **(O) is promoted.** The type-ordered restriction survives every test and shrinks the
  state space substantially; Conjecture H1″ is the new target.
* **The open sub-problem is the recipient rule.** $\arg\max \ell$ is out. Given that the
  recipient in the hard case has zero marginal (Theorem F2), the rule cannot be read off
  the subsidy vector alone — it must see the *residual workload*, which is exactly what the
  conditioned-remainder arcs already encode. Candidate rules to test next: prefer the
  recipient minimising $\max_i \ell$ after the move; prefer the recipient whose relief is
  spectator-free ($\mu_k = 0$ for all $k \ne x$); prefer to keep bundle cardinalities
  balanced, per the balance remark.

## 6. Reproduction

```
python3 typeorder.py     # Check A: type-ordered schedules on the witness + small families
python3 stress.py        # randomised sweep, n=3,4 and m<=4
```
No randomness in `typeorder.py`; `stress.py` is seeded.
