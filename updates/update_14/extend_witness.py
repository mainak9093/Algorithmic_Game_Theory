"""
Approach 14 / Step 1 obstruction, minimal recorded witness.

State: n=3, partial allocation A = [{}, {0}, {4}], p = (0,0,0), so
M(q) = {0,1,2} (all subsidies tied at 0). Item g=3 is being inserted.

Agent 0 holds the UNIQUE minimum-cardinality bundle (empty) and is a member
of M(q) -- exactly the agent Step 1 wants to grow. But v_0(3 | {}) = 0, so
item 3 is not a marginal-1 gain for agent 0 (it would go via the free-item
rule if a free agent existed, but no rule permits FORCING a marginal-0 item
onto a specific agent chosen for cardinality reasons -- EXTEND requires a
marginal-1 witness). The ONLY valid EXTEND option in the whole state grows
agent 1's bundle (currently {0}, size 1) -- strictly larger than agent 0's.

So Step 1's restriction ("assign the new good only to a minimum-cardinality
bundle whenever the allocation is not balanced") has NOTHING LEGAL to select
here: not a suboptimal choice among several, an EMPTY admissible set. This is
a per-call obstruction, sharper than the full-execution reachability gap
recorded in reach_sizes.py / RESIDUAL.md 7.16.40: it shows Step 1 cannot even
be well-defined as stated, before any question of which permutation to choose
(Step 2) or where the search eventually ends up.

Extracted from update_6/guidedR3.py's random search, trial 1 step 2, seed 1,
n=3 m=5 (see extend_forced.py). Reproduced here standalone for inspection.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "update_6"))
from guidedR3 import extend_options, M_of_p, compute_p, marginal

n = 3

v = [
    {  # agent 0
        frozenset(): 0, frozenset({0}): 0, frozenset({1}): 0, frozenset({2}): 1,
        frozenset({3}): 0, frozenset({4}): 0,
        frozenset({0, 1}): 0, frozenset({0, 2}): 1, frozenset({0, 3}): 1,
        frozenset({0, 4}): 0, frozenset({1, 2}): 1, frozenset({1, 3}): 0,
        frozenset({1, 4}): 1, frozenset({2, 3}): 1, frozenset({2, 4}): 1,
        frozenset({3, 4}): 1,
    },
    {  # agent 1
        frozenset(): 0, frozenset({0}): 1, frozenset({1}): 1, frozenset({2}): 0,
        frozenset({3}): 1, frozenset({4}): 0,
        frozenset({0, 1}): 2, frozenset({0, 2}): 1, frozenset({0, 3}): 2,
        frozenset({0, 4}): 1, frozenset({1, 2}): 1, frozenset({1, 3}): 1,
        frozenset({1, 4}): 1, frozenset({2, 3}): 1, frozenset({2, 4}): 0,
        frozenset({3, 4}): 1,
    },
    {  # agent 2
        frozenset(): 0, frozenset({0}): 0, frozenset({1}): 1, frozenset({2}): 1,
        frozenset({3}): 0, frozenset({4}): 1,
        frozenset({0, 1}): 1, frozenset({0, 2}): 1, frozenset({0, 3}): 0,
        frozenset({0, 4}): 1, frozenset({1, 2}): 1, frozenset({1, 3}): 1,
        frozenset({1, 4}): 1, frozenset({2, 3}): 1, frozenset({2, 4}): 2,
        frozenset({3, 4}): 1,
    },
]

A = [frozenset(), frozenset({0}), frozenset({4})]
p = [0, 0, 0]
g = 3


def main():
    sizes = [len(b) for b in A]
    Mq = M_of_p(p, n)
    print(f"A = {[sorted(b) for b in A]}   sizes = {sizes}   p = {p}   M(q) = {sorted(Mq)}")
    print(f"inserting item g = {g}")
    print(f"marginal of g for agent 0 on its own (min-cardinality) bundle: "
          f"v_0({g} | {{}}) = {marginal(v, 0, A[0], g)}   <- not 1, so agent 0 is NOT eligible")
    opts = extend_options(v, A, p, g, n)
    print(f"all valid EXTEND options: {len(opts)}")
    for rho, k in opts:
        target = A[rho[k]]
        print(f"   agent {k} grows bundle {sorted(target)} (size {len(target)})")
    min_size = min(sizes)
    forced_off_min = all(len(A[rho[k]]) != min_size for rho, k in opts)
    print(f"minimum bundle size = {min_size}; every EXTEND option targets a "
          f"LARGER bundle: {forced_off_min}")
    assert forced_off_min and len(opts) > 0
    print("CONFIRMED: Step 1's restriction has no legal choice in this state.")


if __name__ == "__main__":
    main()
