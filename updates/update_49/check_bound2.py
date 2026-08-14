import itertools
from exhaustive_r1 import AGENTS, solver_can_rescue

BOUND = 2

def main():
    offdiag_pairs = [(i, j) for i in AGENTS for j in AGENTS if i != j]
    vals = range(BOUND + 1)
    total = 0
    fails = 0
    for Cvals in itertools.product(vals, repeat=len(offdiag_pairs)):
        C = dict(zip(offdiag_pairs, Cvals))
        for muvals in itertools.product((0, 1), repeat=len(offdiag_pairs)):
            mu = dict(zip(offdiag_pairs, muvals))
            total += 1
            works, *_ = solver_can_rescue(C, mu)
            if not works:
                fails += 1
    print(f"BOUND=2: total={total} fails={fails}")

if __name__ == "__main__":
    main()
