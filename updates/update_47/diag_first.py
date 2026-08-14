"""Diagnostic: why does the first-chore criterion mismatch on 5 of 6272 cases?"""
import random
import sys

sys.path.insert(0, "../update_6")
sys.path.insert(0, "../update_32")
sys.path.insert(0, "../update_44")
sys.path.insert(0, "../update_17")
from peel_general import ell                                    # noqa: E402
from counterexample_hunt import FAMILIES                        # noqa: E402
from cri_sweep import profile, cr_legal                         # noqa: E402


def main():
    rng = random.Random(1357)
    shown = 0
    for _ in range(400):
        n = rng.choice([3, 4, 5])
        m = rng.choice([3, 4, 5])
        name, gen = FAMILIES[rng.randrange(len(FAMILIES))]
        cs = gen(m, n, rng)
        root = tuple([n] * m)
        full = frozenset(range(m))
        for a in range(m):
            b = [cs[i][full] - cs[i][full - {a}] for i in range(n)]
            for x in range(n):
                s = list(root)
                s[a] = x
                s = tuple(s)
                pred = (b[x] <= min(b))
                act = cr_legal(cs, s, n, m)
                if act != pred:
                    shown += 1
                    W = profile(s, n, m)
                    print("MISMATCH #%d  family=%s n=%d m=%d  chore a=%d owner x=%d"
                          % (shown, name, n, m, a, x))
                    print("   beta = c_i(M) - c_i(M-a) : %s   (min %d, beta_x %d)"
                          % (b, min(b), b[x]))
                    print("   predicted legal=%s   actual legal=%s" % (pred, act))
                    print("   W = %s" % [sorted(t) for t in W])
                    print("   arcs w(i,k) = c_i(W_i) - c_i(W_k):")
                    for i in range(n):
                        print("      %s" % [cs[i][W[i]] - cs[i][W[k]]
                                            for k in range(n)])
                    print("   ell = %s" % ell(cs, W, n))
                    print("   is c_i dichotomous?")
                    for i in range(n):
                        bad = []
                        for S in cs[i]:
                            for g in range(m):
                                if g in S:
                                    continue
                                d = cs[i][frozenset(S | {g})] - cs[i][S]
                                if d not in (0, 1):
                                    bad.append((sorted(S), g, d))
                        print("      agent %d: %d violations %s"
                              % (i, len(bad), bad[:3]))
                    print()
                    if shown >= 5:
                        return


if __name__ == "__main__":
    main()
