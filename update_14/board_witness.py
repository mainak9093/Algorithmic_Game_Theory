"""
Approach 14, final closure witness (hand-derived on the whiteboard, verified
here). This is a THIRD and sharpest obstruction to the Steps 1-4 proof
program, on top of the two already on record (reach_sizes.py's whole-search
reachability gap, and extend_witness.py's single-EXTEND-call empty-option
witness).

Setting (goods side, v-hat = size-shifted from chores): n=3 agents, and a
partial allocation already balanced at

    A1 = {b1, b2}      A2 = {a1, a2}      A3 = {a3}

with values (v_i on each of the THREE bundles, i.e. the state BEFORE
inserting the next item c1):

           A1    A2    A3
    v_1:    1     2     1
    v_2:    0     2     1
    v_3:    0     2     1

The identity assignment (agent i keeps A_i) is welfare-maximal (welfare 4,
tied with no better option), so it is envy-freeable, with minimal subsidy
q = (1, 0, 1) via Halpern-Shah longest path -- i.e. M(q) = {1, 3}. Agent 3
holds the unique minimum-cardinality bundle (|A3|=1 < |A1|=|A2|=2) and is
correctly in M(q): exactly the situation invariant (I3) wants.

Now insert a fresh item c1. Its marginal value on A3 is:

    v_1(c1 | A3) = 1        v_2(c1 | A3) = 0        v_3(c1 | A3) = 0

So EXTEND's own selection rule (marginal-1 witness required) can only route
c1 into A3 via agent 1 -- NOT via agent 3, even though agent 3 is the one
holding A3 and sitting in M(q). This reproduces the mechanism of
extend_witness.py from a different, hand-built instance.

What is NEW and sharper here: after inserting c1, the three resulting
bundles are exactly

    A1 = {b1,b2}   A2 = {a1,a2}   A3+c1 = {a3,c1}

all of size 2 -- i.e. PERFECTLY balanced by cardinality (I2 is achieved!).
And yet: EVERY one of the 6 possible assignments of these three fixed
bundles to the three agents gives subsidy spread exactly 2, none achieve
spread <= 1. This is checked exhaustively below -- it is not a bad tie-break
among options that include a good one; there is no good option among the
six.

In particular the "obvious" fix -- let agent 3 simply keep growing its own
bundle, so nobody is displaced by a permutation -- is assignment #1 below,
and it ALSO has spread 2. So the failure is not caused by EXTEND's
permutation logic choosing badly; it is already forced by the VALUES of the
three final bundles, independent of who ends up holding which.

Conclusion: at this state, Steps 1-4 cannot succeed no matter how they are
implemented, because the only bundle that can legally receive c1 (via a
marginal-1 witness, per EXTEND's own rule) is A3, and once c1 is in A3, no
assignment of {A1,A2,A3+c1} to the three agents keeps subsidy in {0,1}.
"""
import itertools

agents = [1, 2, 3]

# v_i on the three ORIGINAL bundles, before inserting c1
v_before = {
    1: {'A1': 1, 'A2': 2, 'A3': 1},
    2: {'A1': 0, 'A2': 2, 'A3': 1},
    3: {'A1': 0, 'A2': 2, 'A3': 1},
}

# v_i on A3 after adding c1 (only agent 1's value changes)
v_A3_plus_c1 = {1: 2, 2: 1, 3: 1}


def longest_path(W, agents, s):
    best = 0
    for r in range(1, len(agents)):
        for rest in itertools.permutations([a for a in agents if a != s], r):
            path = (s,) + rest
            w = sum(W[(path[t], path[t + 1])] for t in range(len(path) - 1))
            best = max(best, w)
    return best


def q_of(assign, values):
    W = {(i, j): values[i][assign[j]] - values[i][assign[i]]
         for i in agents for j in agents if i != j}
    return {i: longest_path(W, agents, i) for i in agents}


def main():
    print("=== Step 0: the state before inserting c1 ===")
    identity = {1: 'A1', 2: 'A2', 3: 'A3'}
    welfare = sum(v_before[i][identity[i]] for i in agents)
    best_welfare = max(
        sum(v_before[i][mapping[i]] for i in agents)
        for perm in itertools.permutations(['A1', 'A2', 'A3'])
        for mapping in [dict(zip(agents, perm))]
    )
    print(f"identity welfare = {welfare}, best possible = {best_welfare} "
          f"-> identity is welfare-maximal: {welfare == best_welfare}")
    q0 = q_of(identity, v_before)
    print(f"q (before) = {q0},  M(q) = {[i for i in agents if q0[i] == max(q0.values())]}")
    print("bundle sizes before: |A1|=2, |A2|=2, |A3|=1  "
          "-> agent 3 holds the UNIQUE min-cardinality bundle and is in M(q). Good so far.")

    print("\n=== Step 1: marginal of c1 on A3, per agent ===")
    marg = {i: v_A3_plus_c1[i] - v_before[i]['A3'] for i in agents}
    print("marginals:", marg)
    eligible = [i for i in agents if marg[i] == 1]
    print(f"only agent(s) {eligible} have a genuine EXTEND witness for growing A3 "
          f"-- agent 3 itself (size-0-marginal) is NOT eligible under BKNS's own rule.")

    print("\n=== Step 2: after insertion, bundles are A1={b1,b2}, A2={a1,a2}, "
          "A3+c1={a3,c1} -- ALL size 2 (perfectly balanced) ===")
    v_after = {
        1: {'A1': 1, 'A2': 2, 'A3c1': 2},
        2: {'A1': 0, 'A2': 2, 'A3c1': 1},
        3: {'A1': 0, 'A2': 2, 'A3c1': 1},
    }
    print("checking ALL 6 assignments of these three fixed bundles to the three agents:")
    any_good = False
    for perm in itertools.permutations(['A1', 'A2', 'A3c1']):
        assign = dict(zip(agents, perm))
        welfare = sum(v_after[i][assign[i]] for i in agents)
        q = q_of(assign, v_after)
        spread = max(q.values()) - min(q.values())
        tag = " <-- 'agent 3 keeps growing its own bundle'" if assign[3] == 'A3c1' and assign[1] == 'A1' else ""
        print(f"  {assign}  welfare={welfare}  q={q}  spread={spread}{tag}")
        if spread <= 1:
            any_good = True
    print(f"\nAny assignment achieving spread <= 1: {any_good}")
    assert not any_good
    print("CONFIRMED: no assignment of {A1, A2, A3+c1} to the three agents keeps "
          "subsidy spread <= 1, even though bundle sizes are perfectly balanced (2,2,2).")
    print("Steps 1-4 cannot rescue this state: the only legal insertion target (A3, "
          "via agent 1's marginal-1 witness) leads to a partition with NO good assignment.")


if __name__ == "__main__":
    main()
