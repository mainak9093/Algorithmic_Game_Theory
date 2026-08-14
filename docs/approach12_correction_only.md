# Approach 12 — Correction Only

## Purpose

This note records **only the correction needed in `approach_12(1).tex`**.

The main proof of Conjecture 2 for \(n=3\) does **not** need the finite `Saturation` enumeration. The structural proofs of the one-leftover and two-leftover theorems are stated in the main body of Approach 12, and the file explicitly says that the verification section is not used by those proofs. Therefore the correction below is an audit/cleanup of the verification appendix, not a change to the main theorem chain.

---

# 1. Exact location that needs correction

File:

```text
approach_12(1).tex
```

The section that needs correction is:

```latex
\subsection{Verification (not part of any proof)}
\label{sec:g2-verification}
```

In the current file this begins at approximately **line 490**.

The problematic subsection inside it is:

```latex
\begin{lemma}[Saturation]
\label{lem:g2-saturation}
...
\end{lemma}
```

The file currently claims:

> if a base matrix \(C\) has zero diagonal and off-diagonal entries in \(\{0,1,2\}\), enumerating all such \(C\) covers every case an unbounded cost table could produce.

The corresponding text is at approximately **lines 499–510**.

The exact problematic claim is:

\[
C_{ii}=0,\qquad C_{ij}\in\{0,1,2\}
\]

is sufficient to represent every relevant \(3\times3\) cost table.

---

# 2. Why the Saturation statement is wrong as written

The first part of the lemma is correct:

For subsidy \(p\in\{0,1\}^3\),

\[
D_{ij}-p_j\le D_{ik}-p_k
\]

depends on the difference

\[
D_{ij}-D_{ik}
\]

only through the four categories

\[
\le -1,\qquad 0,\qquad 1,\qquad \ge2.
\]

That part is valid.

The error is the next assertion:

> after normalizing the diagonal to \(0\), restricting both off-diagonal entries of every row to \(\{0,1,2\}\) automatically realizes every possible relevant comparison pattern.

This is false.

### Counterexample

Consider a normalized row

\[
(0,1,100).
\]

The relevant difference between the two off-diagonal entries is

\[
100-1=99,
\]

which belongs to the category

\[
\ge2.
\]

Replacing the row by

\[
(0,1,2)
\]

changes that difference to

\[
2-1=1,
\]

which belongs to a different category.

Therefore the replacement does **not** preserve the four-category comparison data.

So the proof sentence

> “entries in \(\{0,1,2\}\) already realise differences across \(\{-2,\dots,2\}\), hitting all four cases”

is insufficient: realizing each individual difference category somewhere is not the same as simultaneously realizing an arbitrary row's complete comparison pattern.

---

# 3. What should be done with this section

There are two safe options.

## Preferred option: remove the Saturation lemma from the proof record

Because `approach_12(1).tex` itself states:

> “No step relies on a computation”

and labels the entire section as:

```latex
\subsection{Verification (not part of any proof)}
```

the cleanest correction is:

\[
\boxed{
\textbf{Remove the Saturation lemma and its dependent enumeration claims from the final proof version.}
}
\]

This is the preferred choice.

The main mathematical proof does not need them.

---

# 4. If the verification appendix is retained

Then the `Saturation` lemma must be replaced by a **correct finite-canonicalization theorem**.

A safe formulation is to preserve the actual four comparison categories directly rather than asserting that every row can be represented by entries in \(\{0,1,2\}\).

For each row \(i\), only the signs/categories of

\[
D_{ij}-D_{ik}
\]

matter for subsidy feasibility:

\[
\le -1,\quad 0,\quad1,\quad\ge2.
\]

A finite verifier may therefore enumerate **comparison signatures**, not arbitrary bounded cost values.

Alternatively, after row normalization one can use a larger bounded representation that preserves all comparison categories simultaneously. The earlier audit found that allowing sufficiently separated levels (for example using a bounded range larger than \(\{0,1,2\}\)) resolves this issue, but the cleanest mathematically is to enumerate the comparison signatures themselves.

The important point is:

\[
\boxed{
\text{enumerate the equivalence classes induced by the four comparison categories,}
}
\]

not

\[
\boxed{
\text{truncate every off-diagonal cost to }0,1,2.
}
\]

---

# 5. What does NOT need correction

The following parts of `approach_12(1).tex` are unaffected by this issue.

### Main theorem dependency

The file explicitly states that the verification section is not used by the proof. fileciteturn133file1L91-L100

### One-leftover proof

The theorem for one leftover is analytic and does not depend on enumeration.

### Two-leftover proof

The two-leftover theorem uses the terminal structure forced by the TWYZ algorithm, specifically the fact that with \(n=3\) and two remaining items, the terminal tail SCC must contain all three agents.

The file explicitly distinguishes this structural proof from arbitrary abstract cost-table enumerations. fileciteturn132file2L47-L58

### Main theorem

The final theorem is derived from the zero-, one-, and two-leftover cases, not from the verification appendix.

---

# 6. Recommended exact edit

For the final proof manuscript, replace the current verification appendix with something like:

> **Verification note (non-proof).**  
> Computational checks were used during discovery and independently confirm the one- and two-leftover constructions on bounded abstract instances and randomly generated genuine dichotomous instances. These computations are not used in the proof of the main theorem.
>
> The previous `Saturation` lemma based on restricting normalized off-diagonal entries to \(\{0,1,2\}\) is omitted because that truncation does not preserve all row-wise comparison signatures.

This is enough.

---

# 7. Final audit status

After this correction:

\[
\boxed{
\text{Main proof: unaffected.}
}
\]

\[
\boxed{
\text{Saturation lemma: remove or replace.}
}
\]

\[
\boxed{
\text{Verification appendix: nonessential.}
}
\]

The problematic material is exactly the `Saturation` lemma in:

```text
approach_12(1).tex
§ Verification (not part of any proof)
≈ lines 490–510
```

The current file itself identifies that section as not part of the proof, so correcting/removing it does not alter the core theorem chain. fileciteturn133file0L11-L20
