"""
Is the incompatibility an n = 2 artefact, or a family?

The n = 2 witness has both agents sharing the saturating cost
c(S) = min(|S|, 2): chores are painful up to a point and free thereafter. That
is what makes concentration socially efficient while envy-freeness forbids it.

This script sweeps the whole family c(S) = min(|S|, t) for a range of n, m and
threshold t, and for each asks whether ANY allocation is simultaneously Pareto
optimal and envy-free with p in {0,1}^n. Identical agents are used throughout,
which is the cleanest form of the obstruction and keeps the instances easy to
state in a paper.
"""
import itertools
import sys


def make_instance(n, m, t):
    def c(S):
        return min(bin(S).count("1"), t)
    return [c] * n


def every_allocation(n, m):
    for assign in itertools.product(range(n), repeat=m):
        b = [0] * n
        for k, owner in enumerate(assign):
            b[owner] |= 1 << k
        yield tuple(b)


def analyse(n, m, t):
    CS = make_instance(n, m, t)
    allocs = list(every_allocation(n, m))
    profs = [tuple(CS[i](A[i]) for i in range(n)) for A in allocs]

    # Identical agents mean many allocations share a cost profile, so the
    # quadratic domination scan runs over the DISTINCT profiles only.
    uniq = sorted(set(profs))
    dom_flag = {}
    for pa in uniq:
        dom_flag[pa] = any(pb != pa
                           and all(pb[i] <= pa[i] for i in range(n))
                           and any(pb[i] < pa[i] for i in range(n))
                           for pb in uniq)
    po = [not dom_flag[pa] for pa in profs]

    valid = []
    for k, A in enumerate(allocs):
        ok = False
        for p in itertools.product((0, 1), repeat=n):
            if all(CS[i](A[i]) - p[i] <= CS[i](A[j]) - p[j]
                   for i in range(n) for j in range(n)):
                ok = True
                break
        if ok:
            valid.append(k)

    both = [k for k in valid if po[k]]
    n_po = sum(po)
    best_po_cost = min(sum(profs[k]) for k in range(len(allocs)) if po[k])
    best_valid_cost = (min(sum(profs[k]) for k in valid) if valid else None)
    return len(valid), n_po, len(both), best_po_cost, best_valid_cost


def main():
    print("family c(S) = min(|S|, t), identical agents")
    print("incompatible = some allocation is valid, but none is both valid and PO")
    print()
    print("   %-3s %-3s %-3s %8s %6s %6s %10s %10s  %s"
          % ("n", "m", "t", "valid", "PO", "both", "cost(PO)", "cost(val)",
             "incompatible"))

    hits = []
    for n in range(2, 5):
        for m in range(2, 8):
            if n ** m > 6000:
                continue
            for t in range(1, m + 1):
                nv, npo, nb, cpo, cval = analyse(n, m, t)
                bad = (nv > 0 and nb == 0)
                if bad:
                    hits.append((n, m, t))
                if bad or (t <= 3 and m <= 4):
                    print("   %-3d %-3d %-3d %8d %6d %6d %10s %10s  %s"
                          % (n, m, t, nv, npo, nb, cpo, cval,
                             "YES" if bad else ""))
    print()
    print("incompatible (n, m, t) triples found: %d" % len(hits))
    for h in hits:
        print("   n=%d m=%d t=%d" % h)


if __name__ == "__main__":
    main()
