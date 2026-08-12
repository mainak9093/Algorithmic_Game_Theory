import itertools
from exhaustive_r1 import AGENTS
from which_strategy import identity_only_can_rescue

BOUND = 3

def main():
    offdiag_pairs = [(i, j) for i in AGENTS for j in AGENTS if i != j]
    vals = range(BOUND + 1)
    needs_perm = []
    for Cvals in itertools.product(vals, repeat=len(offdiag_pairs)):
        C = dict(zip(offdiag_pairs, Cvals))
        for muvals in itertools.product((0, 1), repeat=len(offdiag_pairs)):
            mu = dict(zip(offdiag_pairs, muvals))
            if not identity_only_can_rescue(C, mu):
                needs_perm.append((dict(C), dict(mu)))
    all_C_zero = all(all(v == 0 for v in C.values()) for C, mu in needs_perm)
    print(f"{len(needs_perm)} cases need a real permutation.")
    print(f"ALL of them have C entirely zero (fully mutually tied)? {all_C_zero}")
    if not all_C_zero:
        for C, mu in needs_perm:
            if any(v != 0 for v in C.values()):
                print("counterexample to that pattern:", C, mu)
                break
    # among those, what mu patterns appear? count distinct mu's
    mus = set(tuple(sorted(mu.items())) for C, mu in needs_perm)
    print(f"distinct mu patterns among needs-permutation cases: {len(mus)} (out of 64 possible)")
    for muset in sorted(mus):
        print("  ", dict(muset))

if __name__ == "__main__":
    main()
