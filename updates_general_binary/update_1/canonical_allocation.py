"""
Approach 15: is there a CANONICAL allocation that always works?

An observation makes this worth asking. Let F be any family of allocations
closed under permuting the bundles among the agents -- for instance "all
allocations with spread <= K", since permuting does not change the multiset of
bundle sizes. Let A maximise utilitarian welfare over F. Then A beats every
permutation of itself, because those permutations lie in F too, and that is
exactly Halpern-Shah condition (ii):

    A welfare-maximal allocation within any permutation-closed family is
    automatically ENVY-FREEABLE.

So for each K the allocation is well defined and its minimal subsidy exists.
The only question left is whether that subsidy stays within {0,1}^n. This
script tests three canonical choices:

    GWM   welfare-maximal over ALL allocations
    2WM   welfare-maximal over allocations with spread <= 2
    1WM   welfare-maximal over allocations with spread <= 1 (balanced)

bounded_excursion.py already showed that spread <= 2 always suffices for
SOME valid allocation to exist while spread <= 1 does not, so 1WM is expected
to fail and is included as the calibration: a test that everything passes is
not measuring anything.

For each rule two things are recorded, because they are different strengths of
statement:

    ALL   every welfare-maximiser in the family has subsidy in {0,1}^n
          -- if true, the rule is a theorem needing no tie-breaking;
    SOME  at least one does -- if only this holds, the rule needs a tie-break
          and the tie-break is then the real content.
"""
import itertools
import random
import sys

from gb_valuations import (
    enumerate_general_binary,
    enumerate_class,
    arc_weights,
    is_envy_freeable,
    longest_paths,
)


def min_subsidy(vals, bundles):
    if not is_envy_freeable(vals, bundles):
        return None
    return longest_paths(arc_weights(vals, bundles))


def sizes(bundles):
    return [bin(b).count("1") for b in bundles]


def spread(bundles):
    z = sizes(bundles)
    return max(z) - min(z)


def complete_allocations(n, m):
    for assign in itertools.product(range(n), repeat=m):
        b = [0] * n
        for k, owner in enumerate(assign):
            b[owner] |= 1 << k
        yield tuple(b)


def welfare(vals, bundles, n):
    return sum(vals[i][bundles[i]] for i in range(n))


def maximisers(vals, n, m, allocs, K):
    best, out = None, []
    for b in allocs:
        if K is not None and spread(b) > K:
            continue
        w = welfare(vals, b, n)
        if best is None or w > best:
            best, out = w, [b]
        elif w == best:
            out.append(b)
    return out


RULES = (("GWM", None), ("2WM", 2), ("1WM", 1))


def run(pool, n, m, label, sample, seed=20260827):
    rng = random.Random(seed)
    allocs = list(complete_allocations(n, m))

    multisets = [tuple(sorted(rng.choice(pool) for _ in range(n)))
                 for _ in range(sample)]

    stats = {name: {"all": 0, "some": 0, "none": 0, "empty": 0,
                    "witness": None}
             for name, _ in RULES}

    for vals in multisets:
        for name, K in RULES:
            best = maximisers(vals, n, m, allocs, K)
            if not best:
                stats[name]["empty"] += 1
                continue
            good = 0
            for b in best:
                p = min_subsidy(vals, b)
                if p is None:
                    continue          # cannot happen: see the module docstring
                if all(q <= 1 for q in p):
                    good += 1
            if good == len(best):
                stats[name]["all"] += 1
                stats[name]["some"] += 1
            elif good > 0:
                stats[name]["some"] += 1
                if stats[name]["witness"] is None:
                    stats[name]["witness"] = ("needs tie-break", vals)
            else:
                stats[name]["none"] += 1
                if stats[name]["witness"] is None:
                    stats[name]["witness"] = ("fails outright", vals)

    total = len(multisets)
    print("  %-22s n=%d m=%d : %d instances" % (label, n, m, total))
    for name, _ in RULES:
        s = stats[name]
        print("     %-4s  ALL maximisers valid: %5d/%d   SOME valid: %5d/%d"
              "   none: %d" % (name, s["all"], total, s["some"], total,
                               s["none"]))
    for name, _ in RULES:
        s = stats[name]
        if s["witness"] is not None and s["none"] > 0:
            kind, vals = s["witness"]
            print("     %s witness (%s):" % (name, kind))
            for i, v in enumerate(vals):
                print("        agent %d %s" % (i + 1, str(v)))
    return stats


CLASSES = (
    ("control goods {0,1}", {0, 1}),
    ("control chores {-1,0}", {-1, 0}),
    ("general {-1,0,1}", {-1, 0, 1}),
)


def pool_for(m, allowed):
    if allowed == {-1, 0, 1}:
        return list(enumerate_general_binary(m))
    return enumerate_class(m, allowed)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "small"
    print("Canonical allocations: welfare-maximal inside a spread-bounded "
          "family")
    print()
    plan = (((3, 3, 4000), (3, 4, 1500)) if mode == "small"
            else ((4, 4, 400), (3, 5, 400), (4, 5, 150)))
    for (n, m, sample) in plan:
        for label, allowed in CLASSES:
            run(pool_for(m, allowed), n, m, label, sample)
        print()


if __name__ == "__main__":
    main()
