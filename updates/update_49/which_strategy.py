import itertools
from exhaustive_r1 import AGENTS, PERMS, SUBSIDIES, solver_can_rescue

BOUND = 3

def identity_only_can_rescue(C, mu):
    def Cget(i, j):
        return 0 if i == j else C[(i, j)]
    def muget(i, j):
        return 1 if i == j else mu[(i, j)]
    for m in AGENTS:
        D = {}
        for i in AGENTS:
            for j in AGENTS:
                base = Cget(i, j)
                if j == m:
                    base += muget(i, m)
                D[(i, j)] = base
        perm = (0,1,2)  # identity only
        for p in SUBSIDIES:
            ok = True
            for a in AGENTS:
                da = D[(a, perm[a])] - p[a]
                for b in AGENTS:
                    db = D[(a, perm[b])] - p[b]
                    if da > db:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                return True
    return False


def main():
    offdiag_pairs = [(i, j) for i in AGENTS for j in AGENTS if i != j]
    vals = range(BOUND + 1)
    total = 0
    identity_suffices = 0
    needs_perm = 0
    needs_perm_examples = []
    for Cvals in itertools.product(vals, repeat=len(offdiag_pairs)):
        C = dict(zip(offdiag_pairs, Cvals))
        for muvals in itertools.product((0, 1), repeat=len(offdiag_pairs)):
            mu = dict(zip(offdiag_pairs, muvals))
            total += 1
            if identity_only_can_rescue(C, mu):
                identity_suffices += 1
            else:
                needs_perm += 1
                if len(needs_perm_examples) < 5:
                    needs_perm_examples.append((dict(C), dict(mu)))
    print(f"total={total}  identity+subsidy(+choice of m) suffices: {identity_suffices}  needs real permutation: {needs_perm}")
    for ex in needs_perm_examples:
        print("  needs-permutation example:", ex)

if __name__ == "__main__":
    main()
