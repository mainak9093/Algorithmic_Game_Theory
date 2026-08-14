# PS1 working note — the duplicate-penalty (item-weight) idea is a dead end

**Version** v1, 2026-08-03.
**Status** Theorem W1, W2, W3, W4 **proved**. Theorem W4 additionally machine-verified
by `dupsep.py` (exhaustive, no heuristics). Nothing here is conjectural.
**Depends on** `approach_3.tex` §Approach 3 (replica transform, coverage, peel process).
**Terms flagged for the glossary** *faithful reweighting*, *duplicate budget*, *separation
programme*, *holder-blindness*.

---

## 0. What the idea was

After the replica transform, Conjecture 2 reduces to Corollary (Coverage is the entire
gap): every replica instance $\hat I$ must admit a **coverage** allocation $B$ (no bundle
holds two copies of one type) with $\ell_B(i) \le 1$ for all $i$. Applying R3 to $\hat I$
as a black box is legal but returns an allocation free to place two copies of a type in
one bundle.

The proposal: *re-weight the replica items so that a first copy is worth a lot and a second
copy nothing, so that nobody wants a duplicate.* This note settles it.

Throughout, $\hat M$ is the replica item set, $\tau(S)$ the set of types in $S$,
$d(S) := |S| - |\tau(S)|$ the **duplicate count**, and
$\hat v_i(S) = c_i(M) - c_i(M \setminus \tau(S))$ the dual valuation.
Arc weights are $w^u_B(i,k) = u_i(B_k) - u_i(B_i)$ and $\ell^u_B(i)$ is the longest-path
weight out of $i$ ($=+\infty$ if a positive cycle exists).

---

## 1. The literal proposal is a no-op

**Theorem W1.** In $\hat I$ the marginal value of a second copy of a type is already
exactly $0$, for every agent and every set. Formally, if $b$ has type $j$ and
$j \in \tau(S)$ then $\hat v_i(S \cup \{b\}) - \hat v_i(S) = 0$.

*Proof.* $\tau(S \cup \{b\}) = \tau(S)$ and $\hat v_i$ factors through $\tau$. $\square$

So "first copy carries weight, second copy carries zero weight" is not a modification of
$\hat I$ — it **is** $\hat I$, by construction (see the Remark on the naive reading, which
records that the *other* choice, a flat $+1$ per copy, destroys the transform).

**The reason this does not help.** Zero marginal means *indifferent*, not *averse*. The
Duplicate-extraction lemma is the exact statement of the damage: a duplicate is
**envy-neutral** — it changes no arc of the envy graph at all. An objective built out of
envy comparisons therefore cannot see duplicates, and the peel dead ends exist *because*
of this, not in spite of it: at the dead end $(\{a_1,a_2\},\{g\},\{g\})$ the only legal
move in $\hat I$ is to spend the last copy of $b_g$ as a duplicate, which is free and
which is precisely the loss of coverage.

To repel rather than merely fail to attract, a duplicate must be made **visible**.

---

## 2. The separation programme (the idea, correctly stated)

Call $u = (u_1,\dots,u_n)$ on $\hat M$ a **faithful reweighting** if

* **(D)** each $u_i$ is dichotomous — $u_i(\emptyset)=0$, monotone, all marginals in
  $\{0,1\}$ — so that R3 applies to $(\hat M, u)$; and
* **(F)** $u_i(S) = \hat v_i(S)$ for every duplicate-free $S$, so that the envy graph of a
  coverage allocation is unchanged.

Say $u$ **separates** if every non-coverage allocation $B$ has $\max_i \ell^u_B(i) \ge 2$.

**Observation W0 (the programme is logically valid).** If some faithful $u$ separates,
Conjecture 2 follows for that instance. Indeed R3 applied to $(\hat M,u)$ returns $B$ with
$\ell^u_B \in \{0,1\}^n$; separation forces $B$ to be a coverage allocation; on a coverage
allocation (F) gives $u_i(B_k)=\hat v_i(B_k)$ for all $i,k$, so
$\ell^{\hat v}_B = \ell^u_B \le 1$; the replica transform then hands back a chore partition
with per-agent subsidy in $\{0,1\}$ and total $\le n-1$. $\square$

This is worth stating because it shows the idea is not confused — it is a genuine reduction
template. §§3–5 show it cannot be filled in.

---

## 3. The duplicate budget

**Theorem W2 (budget).** Every faithful reweighting satisfies, for all $i$ and all
$S \subseteq \hat M$,
$$\hat v_i(S) \;\le\; u_i(S) \;\le\; \hat v_i(S) + d(S).$$
In particular the penalty $f_i := u_i - \hat v_i$ is non-negative, vanishes on
duplicate-free sets, and is bounded by one unit per duplicated copy.

*Proof.* Let $T \subseteq S$ be duplicate-free with $\tau(T) = \tau(S)$, so
$|S \setminus T| = d(S)$ and $\hat v_i(T) = \hat v_i(S)$. Monotonicity of $u_i$ gives
$u_i(S) \ge u_i(T) = \hat v_i(T) = \hat v_i(S)$ by (F). Adding the $d(S)$ elements of
$S \setminus T$ one at a time raises $u_i$ by at most $1$ each by (D), so
$u_i(S) \le u_i(T) + d(S)$. $\square$

The extreme $f_i = d$ is attained: $u_i = \hat v_i + d$ is monotone, normalised, and has
marginals in $\{0,1\}$ (a fresh copy inherits $\hat v_i$'s marginal and leaves $d$ fixed;
a duplicate copy has $\hat v_i$-marginal $0$ and raises $d$ by one). So **"a duplicate is
worth $+1$ to everybody" is the strongest legal penalty there is.** Any scaling by
$\varepsilon \notin \{0,1\}$ leaves the dichotomous class and forfeits R3.

---

## 4. The strongest uniform penalty is a potential, hence useless

**Theorem W3.** Let $u_i = \hat v_i + \varepsilon d$ for every $i$, with the same
$\varepsilon$ and the same $d$ for all agents. Then for every allocation $B$
$$w^u_B(i,k) \;=\; w^{\hat v}_B(i,k) \;+\; \varepsilon\bigl(d(B_k) - d(B_i)\bigr).$$
Consequently

1. **every directed cycle has the same weight in both graphs**, so $B$ is envy-freeable
   under $u$ iff it is under $\hat v$ — a uniform penalty can never *disqualify* an
   allocation;
2. $\ell^u_B(i) = \max_t \bigl[\,\hat\ell_B(i \to t) + \varepsilon(d(B_t) - d(B_i))\,\bigr]$,
   so the agent holding the **most** duplicates has *weakly smaller* subsidy and everyone
   else *weakly larger* — the penalty lands on the wrong agents;
3. if $d(B_1) = \cdots = d(B_n)$ the two graphs are **identical**, so such allocations are
   invisible to the penalty however large $\varepsilon$ is.

*Proof.* The displayed identity is immediate. (1) The correction telescopes to $0$ around
any cycle. (2) It telescopes along a path to endpoint minus start. (3) All corrections
vanish. $\square$

**Witness for (3).** $n=3$, $m=3$, $c_i(S)=|S|$ for all $i$. Take $B_i = $ both copies of
$b_i$. Then $d(B_i)=1$ for every $i$, $\hat v_i(B_k) = |\tau(B_k)| = 1$ for all $i,k$, every
arc is $0$ and $\ell^u = 0$. Yet $\Psi(B)_i = M \setminus \{a_i\}$ gives every chore two
owners — maximally non-coverage. R3 run on this $u$ may return exactly this allocation.

So the natural instantiation of the idea fails, and fails at the maximum legal strength.

---

## 5. No reweighting whatsoever separates

Theorem W3 leaves open the asymmetric case: let different agents charge for duplicates of
different types. That does break the potential structure and can create positive cycles, so
it must be ruled out separately. It is.

**Theorem W4 (no-go).** There is a negative dichotomous instance on which **no** faithful
reweighting separates. Concretely: $n=3$, $m=2$, $c_1=c_2=c_3=|\cdot|$.

*Proof.* Replica: types $a_1,a_2$, two copies each, $\hat v_i(S) = |\tau(S)|$. Write
$D = \{b_1^{(1)},b_1^{(2)}\}$ and $s_1=\{b_2^{(1)}\}$, $s_2=\{b_2^{(2)}\}$. For
$x \in \{1,2,3\}$ let $B^{(x)}$ be the allocation giving $D$ to agent $x$ and one of
$s_1,s_2$ to each of the other two. Each $B^{(x)}$ is non-coverage.

Let $u$ be faithful. The singletons are duplicate-free, so $u_i(s_1)=u_i(s_2)=1$ for every
$i$ by (F). $D$ has $\hat v_i(D)=1$ and $d(D)=1$, so by Theorem W2
$$u_i(D) = 1 + \delta_i, \qquad \delta_i \in \{0,1\},$$
and $\delta = (\delta_1,\delta_2,\delta_3)$ is the **entire** freedom $u$ has on this
family. Fix $x$ and let $\{y,z\} = [3] \setminus \{x\}$. The arcs of $B^{(x)}$ are
$$w(y,x) = \delta_y,\quad w(z,x) = \delta_z,\quad w(x,y)=w(x,z) = -\delta_x,\quad
  w(y,z)=w(z,y)=0 .$$

*Case $\delta_x = 1$.* Every arc out of $x$ is $-1$, every arc into $x$ is at most $1$, and
the arcs between $y$ and $z$ are $0$. Any directed cycle uses one arc into $x$ and one out,
so has weight $\le 1-1 = 0$: no positive cycle. Any path out of $y$ has weight
$\max(0,\delta_y,\delta_z) \le 1$ (it may cross into $x$ at most once, and continuing out of
$x$ costs $1$); likewise for $z$; and $\ell(x)=0$. Hence $\max_i \ell(i) \le 1$ and
$B^{(x)}$ **survives**.

*Case $\delta_x = 0$ and $\delta_y = \delta_z = 0$.* Every arc is $0$, so $\ell \equiv 0$ and
$B^{(x)}$ **survives**.

*Case $\delta_x = 0$, some $\delta_k = 1$ ($k \ne x$).* The $2$-cycle $k \to x \to k$ has
weight $\delta_k - \delta_x = 1 > 0$, so $\ell = +\infty$ and $B^{(x)}$ is excluded.

So $B^{(x)}$ is excluded **iff** $\delta_x = 0$ and $\delta_k = 1$ for some $k \ne x$.
Separation demands all three of $B^{(1)},B^{(2)},B^{(3)}$ be excluded, hence
$\delta_1=\delta_2=\delta_3=0$, hence no $\delta_k = 1$ — a contradiction. $\square$

**Theorem W4′ (machine-verified strengthening).** On the same instance, separation fails
even if (F) is dropped entirely: among **all** $990$ dichotomous valuations on the four
replica copies, no triple $(u_1,u_2,u_3)$ — that is, none of the $990^3$ candidates —
excludes all twelve non-coverage allocations of the shape "one duplicated pair plus two
singletons". Verified exhaustively by `dupsep.py` (class collapsing, no heuristics; $30$
behaviour classes on the critical family, $0$ surviving class-triples).

Also verified by the same script: the $P$-family
$u_i(S) = \hat v_i(S) + \sum_{j \in P_i}(|S_j|-1)^+$ — "agent $i$ charges for duplicates of
the types in $P_i$", which for $n=3$ is the whole separable penalty family — contains no
separating member on $n=3,m=2$ (all $64$ triples), $n=3,m=3$ unit costs (all $512$), or the
$n=3,m=3$ obstruction witness $c_1 = \max(0,|S|-1)$, $c_2=c_3=|\cdot|$ (all $512$).

**The instance is not a counterexample to Conjecture 2.** On $n=3,m=2$ unit costs the
coverage allocation $B = (\{b_1^{(1)},b_2^{(1)}\}, \{b_1^{(2)}\}, \{b_2^{(2)}\})$ — chore
partition $(\emptyset,\{a_2\},\{a_1\})$ — has $\ell = (0,1,1)$, total $2 = n-1$. What
Theorem W4 refutes is the **method**, on the easiest possible instance.

---

## 6. Why it fails — holder-blindness

The mechanism is worth naming because it is the same shape as the obstruction in
Approach 1, in new coordinates.

A duplicate penalty bites only through the arcs, and the arc effect of agent $k$ charging
$+1$ for the duplicates in bundle $B_x$ is $+1$ on $w(k,x)$ — but the *same* charge levied
by $x$ itself is $+1$ on $u_x(B_x)$, which is $-1$ on every arc **out of** $x$. Those two
cancel around every cycle. So a penalty can only disqualify an allocation if the agent who
*holds* the duplicate does not feel it while somebody else does.

But $u$ is fixed before the allocation is chosen, and the allocation decides who holds the
duplicate. Requiring the holder to be blind for **every** possible holder forces the
penalty to zero. That is exactly the $\delta$ argument of Theorem W4.

Compare the Orientation-reversal table in `approach_3.tex`: there the difficulty was that
R3's navigation rule sends the item to the agent who must not receive it. Here the
difficulty is that the penalty must be levied on the agent who cannot be identified in
advance. Both are the same species of failure — a *rule fixed ex ante* against a
*quantity determined ex post*.

**Corollary W5 (what this rules out and what it does not).**
Ruled out: encoding coverage into the **valuations** of the replica instance, so that R3
can be used as a black box. Any such encoding is a dichotomous reweighting and Theorem W4′
kills it.
Not ruled out: coverage-aware **algorithms** — i.e. Conjecture H1′ and the search for a
peel rule that never enters a deadlock. Coverage is a constraint on the allocation, and the
right place to enforce a constraint on the allocation is the procedure that builds it, not
the objective it is scored against.

---

## 7. Reproduction

`dupsep.py` reproduces every number in §§4–5:

```
python3 dupsep.py                 # Theorem W3 witness, W4 hand-proof table, W4' exhaustive
python3 dupsep.py pfamily         # the P-family sweeps on all three instances
```

Runtime is a few seconds. No randomness, no heuristics, no external dependencies.
