import itertools
from exhaustive_r1 import AGENTS
from which_strategy import identity_only_can_rescue

BOUND = 3

def has_tie(C, i):
    return any(C.get((i,j),0)==0 for j in AGENTS if j!=i)

def main():
    offdiag_pairs = [(i, j) for i in AGENTS for j in AGENTS if i != j]
    vals = range(BOUND + 1)
    needs_perm = []
    for Cvals in itertools.product(vals, repeat=len(offdiag_pairs)):
        C = dict(zip(offdiag_pairs, Cvals))
        for muvals in itertools.product((0, 1), repeat=len(offdiag_pairs)):
            mu = dict(zip(offdiag_pairs, muvals))
            if not identity_only_can_rescue(C, mu):
                needs_perm.append((C,mu))
    all_every_agent_tied = all(all(has_tie(C,i) for i in AGENTS) for C,mu in needs_perm)
    print("needs-permutation count:", len(needs_perm))
    print("ALL needs-permutation cases have every agent tied with someone:", all_every_agent_tied)

    # converse: among cases where every agent is tied with someone, how many actually need permutation?
    every_tied_total = 0
    every_tied_needs = 0
    for Cvals in itertools.product(vals, repeat=len(offdiag_pairs)):
        C = dict(zip(offdiag_pairs, Cvals))
        if not all(has_tie(C,i) for i in AGENTS):
            continue
        for muvals in itertools.product((0, 1), repeat=len(offdiag_pairs)):
            mu = dict(zip(offdiag_pairs, muvals))
            every_tied_total += 1
            if not identity_only_can_rescue(C, mu):
                every_tied_needs += 1
    print(f"among 'every agent tied' cases: {every_tied_needs}/{every_tied_total} actually need permutation")

if __name__ == "__main__":
    main()
