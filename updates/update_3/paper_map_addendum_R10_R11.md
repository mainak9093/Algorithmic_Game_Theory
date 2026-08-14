# Paper Map — Addendum: R10, R11

> **MERGED, 2026-08-15.** §§1–2 and §3 are now in `docs/map.md` (the canonical file,
> renamed from `paper_map_R1_to_R9.md`), which also gained a fresh §12 for R12. The
> §3.3 warning below travelled with them and is restated in `map.md`'s footer — it is
> still unverified. §4's test instance was never promoted and is still only here.
> Retained as a session record; superseded, not deleted.

**Status:** merge candidate. Sections 1–2 are drop-in §§ for `paper_map_R1_to_R9.md`;
§3 lists edits to existing content in that file; §4 is a new test instance derived from R10
and belongs in the PS1 note, not the paper map. On merge, retitle the canonical file
`paper_map_R1_to_R11.md`, bump its version header, and delete the old upload before
re-uploading (one version at a time).

**Warning flag for §3.3:** the dependency claim about R9's EF1 input has *not* been verified
against R9's own text in this session. Verify before promoting it to the canonical file.

---

## 1. R10 — Bhaskar, Sricharan, Vaish, *On Approximate Envy-Freeness for Indivisible Chores and Mixed Resources* (APPROX/RANDOM 2021; arXiv 2012.06788v3, 27 Aug 2022)

**No subsidies anywhere in this paper.** It is in the corpus because it supplies two things the
subsidy line for chores needs and did not have: a hardness floor for the *zero*-subsidy question
on exactly PS1's item class, and a correct EF1 algorithm for non-additive chores.

**Setting.** $n$ agents, $m$ indivisible chores; monotone non-increasing valuations, and the
doubly monotone class (each agent partitions $M$ into her own goods and chores). Also a mixed
model with a divisible *bad cake*.

**Results.**

- **Theorem 2 (the one that matters here).** Deciding whether a chores instance admits an
  **exact EF** allocation is **strongly NP-complete**, already for **binary additive** chores,
  $v_{ij} \in \{0,-1\}$. Reduction from **Set Splitting**: $q=|U|$, $r=|F|$, $r'=\max\{q,r\}$;
  build $m = r'+q$ chores ($r'$ dummies $+$ $q$ vertex chores) and $n = r'+2$ agents
  ($r'$ edge agents $+$ 2 colour agents). Dummies are $-1$ for everyone; vertex chore $V_j$ is
  $-1$ for edge agent $e_i$ iff $v_j \in E_i$, and $0$ for both colour agents. EF allocation
  $\iff$ the hypergraph is 2-colourable with no monochromatic edge.
  (The goods analogue — EF existence for binary goods — was already known NP-complete;
  R10's contribution is *strong* hardness on the chores side.)
- **Example 1 (a correction to the literature).** The natural chores adaptation of Lipton et al.'s
  envy-cycle elimination — give the next chore to a sink, resolve arbitrary envy cycles — **fails
  to return an EF1 allocation**, already for additive monotone non-increasing valuations
  ($n=3$, $m=6$). This refutes a claim of Aziz et al. Bérczi et al. had shown failure for
  non-monotone non-additive valuations; R10's counterexample is strictly stronger.
  *Reason:* for chores the EF1 witness item is removed from the **envious** agent's bundle, so a
  cycle swap can hand an agent a strictly better bundle containing no single chore large enough
  to absorb the envy. **Which cycle you resolve matters for chores and does not for goods.**
- **Theorem 3.** Resolving **top-trading envy cycles** — the subgraph of the envy graph keeping
  only arcs into an agent's *weakly most preferred* bundle — repairs it: EF1 for **monotone**
  chores, polynomial time. Every agent on a resolved top-trading cycle receives her favourite
  bundle and is therefore envy-free in the next round, which is why EF1 survives.
- **Theorem 4.** Two-phase extension (Lipton-style goods phase restricted to interested agents,
  then a top-trading chores phase) gives EF1 for **doubly monotone** instances.
- **Theorems 16–18.** EFM (envy-freeness for mixed goods) exists for doubly monotone indivisible
  items $+$ bad cake; and, for indivisible chores $+$ good cake, in two special cases (identical
  rankings; $m \le n+1$). Complements Bei et al. Peripheral to the subsidy line.

**Improves on.** Lipton et al. (goods $\to$ chores analogue, now correct); Aziz et al. (repairs
the refuted claim); Bei et al. (bad cake, doubly monotone items).

**Leaves open.** EFM for indivisible chores $+$ good cake in general.

---

## 2. R11 — Lu, Mackenzie, Suzuki, *Optimal Subsidy Bounds for Goods and Chores: One Dollar Each Suffices* (arXiv 2607.10089v1, 11 Jul 2026)

**The current end of the trunk, and it lands directly on PS1.** Setting: $n$ agents, $m$
indivisible items, **additive** utilities normalised to $u_i(j) \in [-1,1]$; each item may be a
good for some agents and a chore for others (fully mixed manna). Standard subsidy model.

**Theorem 1.1.** Every such instance admits an envy-free outcome $(A,p)$ with $0 \le p_i \le 1$
for every agent, computable in polynomial time. Hence total $\le n-1$. Tight, since the bound is
already tight for goods only (R2).

**Machinery — two iterated matching procedures.**

- **IMWM** (goods style): rounds of maximum-weight matching on the bipartite agent–object graph,
  ties broken toward maximum cardinality; agents may go unmatched in a round.
- **IMWPM** (chores style): rounds of maximum-weight **perfect** matching; the object set is
  padded with $0$-valued dummies to a multiple of $n$, so **every agent takes exactly one object
  every round**. The output is therefore **balanced** (bundle sizes differ by at most one).

**Proposition 3.1** (subjective goods only, $u_i(g) \le 1$, each item non-negative to someone):
IMWM gives $p_i \le 1$. **Proposition 3.2** (objective chores only, $u_i(g) \ge -1$): **IMWPM
gives $p_i \le 1$.** Both by the same telescoping argument: additivity splits any envy path's
weight into per-round contributions, $w_A(P) = \sum_t w_{\mu^t}(P)$; optimality of the round-$t$
matching against a rerouted alternative gives
$w_{\mu^t}(P) \le \max_{g \in J^t} u_k(g) - \max_{g \in J^{t+1}} u_k(g)$ for the path's terminal
agent $k$; the sum telescopes, and the final round is handled by a cyclic alternative matching,
leaving $w_A(P) \le -u_k(\mu^T_1) \le 1$.

**The general mixed case** (Theorem 1.1) needs more: a *conditional pairwise merging* routine
(Algorithm 3) that bundles items into **meta-goods** which are unit-bounded, chore-maximal, and
have pairwise disjoint interest sets, then three cases on $|Z_{\mathrm{rem}}|$ vs. $|G|$ —
$|Z_{\mathrm{rem}}|=0$ runs IMWM directly; $|Z_{\mathrm{rem}}| \ge |G|$ reduces to objective
chores and runs IMWPM; the sparse-chores middle case is the hard one and is built incrementally
with equality paths and a payment-reduction step, closed by a flow argument.

**Improves on.** R2 (goods only $\to$ mixed, same constant, and a much shorter proof of the
goods case via Prop. 3.1); R9 on the additive part of doubly monotone, by a factor of $n$
($n-1$ per agent $\to$ 1). Does **not** subsume R3 or R9 in general: both are non-additive.

**Leaves open, in their own words (§6).** Everything non-additive. They state that additivity
is load-bearing in two places — defining meta-goods, and getting telescoping envy-path bounds
out of iterated matchings — and ask whether a constant per-agent bound holds for submodular or
XOS valuations, noting this is open even for goods only.

---

## 3. Edits to the existing canonical file

**3.1 §0, the structure table and the DAG.** Add:

| Reading | Year | Short name | Setting |
|---|---|---|---|
| R10 | 2021 (APPROX) / 2022 | Bhaskar–Sricharan–Vaish | unweighted, monotone **chores**, *no money* |
| R11 | 2026 | Lu–Mackenzie–Suzuki | unweighted, additive **mixed manna**, money |

R11 hangs off R2 on the trunk (same constant, wider item model, new proof). R10 belongs on
branch (B) beside R5/R8 — no money — but with a wire into branch (A), see §3.3.

**3.2 §10, unweighted bound table.** Add rows:

| Valuation class | Bound | Source | Superseded by |
|---|---|---|---|
| additive, mixed goods and chores | $1$/agent, $n-1$ total, tight | R11 | — |
| additive chores (objective) | $1$/agent, $n-1$ total, via IMWPM | R11 | — |
| binary additive chores | $p_i \in \{0,1\}$, $n-1$ total | R11 + integrality | — |

The last row is a corollary, not a theorem of R11: with $u_i(j) \in \{0,-1\}$ every arc weight
is an integer, so $\ell_A(i) \in \mathbb{Z}_{\ge 0}$, and $\ell_A(i) \le 1$ forces
$p \in \{0,1\}^n$.

Also add to §10's commentary: **for chores, the doubly-monotone row of R9 ($n-1$ per agent) is
now the best published bound only for the *non-additive* part of that class.**

**3.3 §11, where the corpus is thin — rewrite the chores gap.** The gap is no longer "chores
with subsidy" but precisely **non-additive chores with subsidy**. Concretely: on the goods side
the dichotomous class is closed by R3 with $p \in \{0,1\}$; on the chores side nothing
non-additive beats R9's $n-1$ per agent. The corpus is asymmetric by exactly one paper, and
that paper is PS1.

**[Unverified — check against R9's text before promoting.]** R9's Theorem 1 is conditional: it
converts a *given* EF1 allocation into a subsidised EF one. For **non-additive** doubly monotone
instances, the supply of that input appears to trace back to the Aziz et al. envy-cycle claim
that R10's Example 1 refutes; if so, R10's Theorems 3–4 are what actually make R9's bound
non-vacuous on PS1's class, and the two should be linked in the DAG.

---

## 4. New test instance for PS1 (from R10's reduction)

Not paper-map material — file under the PS1 note. Take the smallest Set-Splitting **NO**
instance, $U = \{v_1,v_2,v_3\}$, $F = \{\{v_1,v_2\},\{v_1,v_3\},\{v_2,v_3\}\}$ (a triangle: no
2-colouring splits all three pairs). R10's reduction gives $n=5$, $m=6$, binary additive chores:

|  | $D_1$ | $D_2$ | $D_3$ | $V_1$ | $V_2$ | $V_3$ |
|---|---|---|---|---|---|---|
| $e_1$ | $-1$ | $-1$ | $-1$ | $-1$ | $-1$ | $0$ |
| $e_2$ | $-1$ | $-1$ | $-1$ | $-1$ | $0$ | $-1$ |
| $e_3$ | $-1$ | $-1$ | $-1$ | $0$ | $-1$ | $-1$ |
| $c_1$ | $-1$ | $-1$ | $-1$ | $0$ | $0$ | $0$ |
| $c_2$ | $-1$ | $-1$ | $-1$ | $0$ | $0$ | $0$ |

Exhaustive check over all $5^6 = 15625$ allocations (`setsplit.py`):

- **No EF allocation exists** — as the reduction predicts. Minimum subsidy is strictly positive.
- $3375$ allocations are envy-freeable; $12250$ are not.
- **Every** envy-freeable allocation has total subsidy **exactly 3** $(\le n-1 = 4)$. Selecting
  by total subsidy is completely uninformative on this instance.
- Per-agent maxima across those $3375$: $\max_i \ell_A(i) = 1$ for $1620$, $=2$ for $1620$,
  $=3$ for $135$. So only **48%** meet PS1's target, and the per-agent max is the only
  discriminating statistic.
- The **utilitarian-optimal set coincides exactly with the envy-freeable set** here (welfare
  $-3$, $3375$ allocations, none of them non-envy-freeable). This reproduces the project's
  "utilitarian optimality is necessary but not sufficient" finding on a structurally hard
  instance rather than a random one, and with a 52% failure rate rather than a marginal one.

Witness meeting the target: $e_i$ takes one dummy each plus the one vertex chore it values at
$0$; $c_1, c_2$ take nothing; $p = (1,1,1,0,0)$.

**Why this instance is worth keeping.** It is the smallest certified-hard instance available:
hardness of the zero-subsidy question is *concentrated* in it, it sits inside the project's
existing randomised search range ($n \le 5$, $m \le 6$), and it is additive — so R11 guarantees
a target-meeting allocation exists, making it a test of *navigation rules*, not of the
conjecture. Larger members of the family (Fano plane: $q=r=7$, giving $n=9$, $m=14$) are beyond
exhaustive search but still admit an IMWPM certificate.

---

*Addendum v1, 2026-08-02. Delete on merge.*
