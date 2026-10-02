# Structural Findings on Unit Subsidies for Objective Signed Dichotomous Valuations

## 1. Setup

Consider an envy-freeable allocation (A=(A_1,`\ldots`{=tex},A_n)) with
pointwise-minimal subsidy vector (p).

For the weighted envy graph, define \[ w_A(i,j)=v_i(A_j)-v_i(A_i). \]

Pointwise minimality gives, for every directed path
(P:i`\leadsto `{=tex}j), \[ w_A(P)`\le `{=tex}p_i-p_j. \]

Define the compensated tight graph \[ H_p=(N,E_p), `\qquad`{=tex}
(i,j)`\in `{=tex}E_p `\iff`{=tex} w_A(i,j)=p_i-p_j. \]

Equivalently, the compensated values are equal: \[
v_i(A_i)+p_i=v_i(A_j)+p_j. \]

For an unallocated good (g), define its marginal-labelled graph \[
D_g={(i,j):`\Delta`{=tex}\_i\^g(A_j)=1}, \] where \[
`\Delta`{=tex}\_i\^g(A_j) = v_i(A_j`\cup`{=tex}{g})-v_i(A_j). \]

The important structural object is therefore not (H_p) or (D_g)
separately, but their cyclic-tight intersection.

------------------------------------------------------------------------

## 2. Exact SCC characterization of one-good extendability

Let \[ M(p)={i:p_i=`\max`{=tex}\_j p_j}. \]

A good (g) is extendable from ((A,p)) precisely when there is a
marginal-1 edge \[ (i,j)`\in `{=tex}D_g \] such that

1.  (j`\in `{=tex}M(p)), and
2.  \(i\) and (j) lie in the same strongly connected component of (H_p).

Equivalently, \[ `\boxed{
g\text{ is extendable}
\iff
D_g\cap E(H_p)_{\mathrm{cyc}}
\text{ contains an edge entering }M(p),
}`{=tex} \] where (E(H_p)\_{`\mathrm{cyc}`{=tex}}) denotes the tight
edges lying on directed cycles of (H_p).

### Why

If an envy-freeable bundle permutation witnesses extendability, its
permutation cycles have total envy-graph weight zero. Since every edge
satisfies \[ w_A(i,j)`\le `{=tex}p_i-p_j, \] and the subsidy differences
telescope around a permutation cycle, every edge used by the permutation
must be tight. Hence the relevant marginal-1 edge lies on a directed
cycle of (H_p).

Conversely, a directed tight cycle has total weight zero, so rotating
the bundles along that cycle preserves welfare. If the relevant bundle
belongs to a maximally subsidized agent and has marginal value one for
the rotated recipient, this gives the required BKNS extension witness.

This is the graph-theoretic form of the EXTEND characterization used in
the one-good argument of Barman et al. \[BKNS22\].

------------------------------------------------------------------------

## 3. Structure inherited from the chore allocation

After ChoreAllocate, let (S\^`\star`{=tex}) denote the terminal tail SCC
of the equality graph from the chore construction, and let \[
T`\subseteq `{=tex}S\^`\star`{=tex} \] be the agents receiving the
residual chores.

The terminal construction has two important consequences:

-   \(T\) consists of maximally subsidized agents: \[
    T`\subseteq `{=tex}S\^`\star`{=tex}`\cap `{=tex}M(p). \]

-   The internal equality structure of (S\^`\star`{=tex}) survives in
    the compensated tight graph (H_p). Thus (S\^`\star`{=tex}) is
    contained in a tight SCC of (H_p).

Therefore, for an unallocated good (g), if \[
`\exists `{=tex}i`\in `{=tex}S\^`\star`{=tex}, t`\in `{=tex}T \] such
that \[ `\Delta`{=tex}\_i\^g(A_t)=1 \] and \[ (i,t)`\in `{=tex}E(H_p),
\] then (g) is immediately extendable through the chore-generated SCC.

More precisely, \[ `\boxed{
D_g\cap E(H_p)_{\mathrm{cyc}}\cap(S^\star\times T)\neq\varnothing
\quad\Longrightarrow\quad
g\text{ is EXTENDable}.
}`{=tex} \]

------------------------------------------------------------------------

## 4. FindSink as movement through tight paths

Suppose the above local extension certificate does not exist and
FindSink is invoked.

Let its selected agents be \[ s_0,s_1,s_2,`\ldots`{=tex}. \]

The first selected agent (s_0) is maximally subsidized. Whenever a later
agent (s\_{t+1}) is selected because the current placement of (g) would
require subsidy at least two, the FindSink proof yields a path \[
P\_{t+1}:s\_{t+1}`\leadsto `{=tex}s_t \] whose weight in the original
allocation is exactly zero.

Since \[ p\_{s\_{t+1}}=p\_{s_t}=1, \] the path satisfies \[
w_A(P\_{t+1}) = p\_{s\_{t+1}}-p\_{s_t} = 0. \]

Every edge of this path is therefore tight in (H_p).

Thus FindSink can be interpreted as traversing the tight graph: \[
`\boxed{
s_{t+1}\leadsto s_t
\quad\text{inside }H_p.
}`{=tex} \]

If a selected agent ever repeats, these tight paths concatenate into a
directed tight cycle. The marginal-1 edge created by the initial
placement of (g) then produces an EXTEND witness, contradicting the
assumption that the starting solution was non-extendable.

Hence FindSink selects each agent at most once.

------------------------------------------------------------------------

## 5. SCC migration theorem

The interaction between the chore SCC and good extension can now be
stated sharply.

Let (S\^`\star`{=tex}) be the terminal tail SCC from ChoreAllocate and
(T) its residual-chore recipient set.

For an unallocated good (g), there are two structural possibilities.

### Local extension

If \[
D_g`\cap `{=tex}E(H_p)\_{`\mathrm{cyc}`{=tex}}`\cap`{=tex}(S\^`\star`{=tex}`\times `{=tex}T)`\neq`{=tex}`\varnothing`{=tex},
\] then (g) can be extended using a tight cycle contained in the SCC
generated by (S\^`\star`{=tex}).

### Escape

If no such cyclic-tight marginal edge exists, then the first new
FindSink selection cannot lie in (S\^`\star`{=tex}).

To see this, suppose the first new selection were
(s_1`\in `{=tex}S\^`\star`{=tex}). The critical FindSink path from (s_1)
to the previous recipient (s_0`\in `{=tex}T) is a zero-weight tight
path. Because (S\^`\star`{=tex}) is strongly connected, this path
combines with a path inside (S\^`\star`{=tex}) to form a tight cycle.
Its final marginal-1 edge into (s_0) is therefore a cyclic-tight edge in
\[ D_g`\cap`{=tex}(S\^`\star`{=tex}`\times `{=tex}T), \] contradicting
the assumption.

Hence \[ `\boxed{
\text{no local cyclic-tight certificate}
\quad\Longrightarrow\quad
s_1\notin S^\star.
}`{=tex} \]

------------------------------------------------------------------------

## 6. No-reentry lemma

The stronger structural fact is that once FindSink leaves
(S\^`\star`{=tex}), it cannot return.

Suppose \[
s_0`\in `{=tex}S^`\star`{=tex},`\qquad `{=tex}s_1`\notin `{=tex}S^`\star`{=tex},
\] and assume for contradiction that some later selected agent \[
s_t`\in `{=tex}S\^`\star`{=tex} \] with (t`\ge2`{=tex}).

Then (s\_{t-1}`\notin `{=tex}S\^`\star`{=tex}). The FindSink critical
path gives a tight path \[ s_t`\leadsto `{=tex}s\_{t-1}. \]

Because both selected agents have subsidy one, \[
p\_{s_t}=p\_{s\_{t-1}}=1, \] every edge on this path is a zero-weight
edge of the original envy graph: \[ w_A(u,v)=0. \]

The path begins in (S\^`\star`{=tex}) and ends outside
(S\^`\star`{=tex}), so it must contain an edge \[ u`\to `{=tex}v,
`\qquad`{=tex}
u`\in `{=tex}S^`\star`{=tex},`\quad `{=tex}v`\notin `{=tex}S^`\star`{=tex},
\] with \[ w_A(u,v)=0. \]

But (S\^`\star`{=tex}) is a terminal/tail SCC of the original equality
graph. By construction there is no equality edge leaving it; in fact, \[
u`\in `{=tex}S^`\star`{=tex}, v`\notin `{=tex}S^`\star`{=tex}
`\quad`{=tex}`\Longrightarrow`{=tex}`\quad`{=tex} w_A(u,v)\<0. \]

Contradiction.

Therefore \[ `\boxed{
s_0\in S^\star,\ s_1\notin S^\star
\quad\Longrightarrow\quad
s_t\notin S^\star\ \text{for every }t\ge1.
}`{=tex} \]

So the good-extension dynamics have a genuine one-way SCC migration:

\[ `\boxed{
S^\star
\longrightarrow
N\setminus S^\star
\qquad\text{with no return}.
}`{=tex} \]

------------------------------------------------------------------------

## 7. Unified interpretation

The chore and good arguments can therefore be viewed through the same
compensated tight graph.

For an item (x), define \[ `\Delta`{=tex}\_i\^x(A_j) =
v_i(A_j`\cup`{=tex}{x})-v_i(A_j). \]

Adding (x) to recipient (j) changes only the incoming and outgoing
weighted-envy edges around (j): \[
w'(i,j)=w(i,j)+`\Delta`{=tex}\_i\^x(A_j), \] and \[
w'(j,k)=w(j,k)-`\Delta`{=tex}\_j\^x(A_j). \]

For a good, \[ `\Delta`{=tex}\_i\^g`\in`{=tex}{0,1}, \] so dangerous
path-weight increases propagate toward the recipient. The relevant
structure is cyclic tight marginal edges and, if none exists, FindSink
movement through tight paths.

For a chore, \[ `\Delta`{=tex}\_i\^c`\in`{=tex}{0,-1}, \] so the
perturbation direction is reversed. The terminal tail SCC and backward
subsidy closure in ChoreAllocate capture this opposite propagation.

The common structural object is therefore:

\[ `\boxed{
\text{tight compensated graph}
+
\text{marginal-labelled edges}
}`{=tex} \]

with the sign of the item determining the direction in which the
perturbation propagates.

------------------------------------------------------------------------

## 8. Current research target

The most promising next step is to understand the condensation structure
outside (S\^`\star`{=tex}).

We now know:

\[ `\boxed{
\begin{array}{c}
\text{cyclic-tight marginal edge into }S^\star
\\
\Downarrow
\\
\text{EXTEND inside }S^\star
\end{array}}`{=tex} \]

whereas

\[ `\boxed{
\begin{array}{c}
\text{no such edge}
\\
\Downarrow
\\
\text{FindSink exits }S^\star
\\
\Downarrow
\\
\text{FindSink never returns}
\end{array}}`{=tex} \]

This suggests studying the SCC condensation DAG of the tight graph after
removing (S\^`\star`{=tex}), and determining whether FindSink follows a
monotone path through that DAG.

If such a global condensation characterization can be established, the
existing procedural EXTEND/FindSink proof may admit a more unified
interpretation as **SCC migration under signed item perturbations**.

------------------------------------------------------------------------

## 9. Relation to the existing objective-signed result

The existing result for objective signed dichotomous valuations already
establishes the unit-subsidy guarantee by first solving the chore
instance and then inserting goods one at a time using the one-good
extension lemma. The structural results above do not replace that
theorem; they expose additional structure in the proof that may be
useful for a stronger unified treatment or for extensions toward broader
doubly monotone valuations.

The one-good extension lemma in the current paper explicitly extends the
BKNS good-side argument to bundles that may already contain chores. The
BKNS result itself establishes unit subsidies for general dichotomous
goods without additivity, submodularity, or subadditivity assumptions.
[BKNS22](https://www.ijcai.org/proceedings/2022/9)

------------------------------------------------------------------------

## 10. Core takeaway

The central object emerging from the investigation is not simply an
equality graph.

It is

\[ `\boxed{
\textbf{the cyclic tight marginal graph}
}`{=tex} \]

formed by intersecting:

\[ `\text{marginal-1 edges of }`{=tex}g \]

with

\[ `\text{tight edges of }`{=tex}H_p \]

that lie on directed cycles.

For the chore-generated terminal SCC (S\^`\star`{=tex}):

\[ `\boxed{
\text{local cyclic-tight marginal edge}
\Rightarrow
\text{good can be absorbed by }S^\star;
}`{=tex} \]

otherwise

\[ `\boxed{
\text{FindSink escapes }S^\star
\text{ and can never re-enter it}.
}`{=tex} \]

This gives a concrete structural bridge between the chore SCC
construction and the BKNS good-extension mechanism.
