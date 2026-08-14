import itertools
from exhaustive_r1 import AGENTS
from which_strategy import identity_only_can_rescue

BOUND = 3

def main():
    offdiag_pairs = [(i, j) for i in AGENTS for j in AGENTS if i != j]
    vals = range(BOUND + 1)
    needs_perm_C = []
    for Cvals in itertools.product(vals, repeat=len(offdiag_pairs)):
        C = dict(zip(offdiag_pairs, Cvals))
        for muvals in itertools.product((0, 1), repeat=len(offdiag_pairs)):
            mu = dict(zip(offdiag_pairs, muvals))
            if not identity_only_can_rescue(C, mu):
                needs_perm_C.append(dict(C))
    max_val = max(v for C in needs_perm_C for v in C.values())
    print("max C-value seen among needs-permutation cases:", max_val)
    distinct_C = set(tuple(sorted(C.items())) for C in needs_perm_C)
    print("distinct C patterns:", len(distinct_C))
    for c in sorted(distinct_C):
        print("  ", dict(c))

if __name__ == "__main__":
    main()
