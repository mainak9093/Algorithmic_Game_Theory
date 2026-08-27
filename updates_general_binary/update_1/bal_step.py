"""
Approach 15: (S1) reduces to a single-step lemma, and this measures its
strongest form.

Two observations collapse the picture.

FIRST, a move preserves balance exactly when it grows a minimum-size bundle.
If A is balanced its sizes lie in {k, k+1}. Adding an item to a size-k bundle
leaves sizes in {k, k+1}; adding to a size-(k+1) bundle creates k+2 while some
bundle still has k, giving spread 2. (If all sizes are equal, every bundle is
of minimum size and every move keeps balance.) So "balanced successor" and
"insert into a minimum-size bundle" are the same thing.

SECOND, steering_plus.py found that in BOTH pure classes the balanced step is
the only one ever used -- the minimum-bundle and free-choice fallbacks fired
zero times across every size tested. So in those classes the greedy rule "keep
balance" never needs help, and (S1) is exactly the claim that it works. With
the duality of section 23, the goods and chores halves are one statement, so
all of (S1) rests on:

    (BAL-STEP)  Let A be a valid balanced partial allocation and g an
                unallocated item. Is there a minimum-size bundle to grow by g,
                and a reassignment of the resulting bundles to the agents,
                landing on a valid balanced state?

Three strengths are measured, because they are different lemmas and only the
strongest gives an order-independent algorithm:

    SOME-ITEM   some unallocated g admits such a move  (what was tested before)
    EVERY-ITEM  every unallocated g admits one -- the algorithm may then insert
                items in any order, and only the recipient must be chosen
    EVERY-MIN   for every g, EVERY minimum-size bundle works as recipient,
                for some reassignment -- then nothing needs choosing at all

The general binary column is included to see where the pure-class behaviour
stops.
"""
import itertools
import random
import sys

from gb_valuations import (
    enumerate_class,
    enumerate_general_binary,
    arc_weights,
    is_envy_freeable,
    longest_paths,
)


def valid(vals, b):
    if not is_envy_freeable(vals, b):
        return False
    return all(q <= 1 for q in longest_paths(arc_weights(vals, b)))


def sizes(b):
    return [bin(x).count("1") for x in b]


def balanced(b):
    z = sizes(b)
    return max(z) - min(z) <= 1


def allocated(b):
    mask = 0
    for x in b:
        mask |= x
    return mask


def all_partial(n, m):
    out = set()
    for assign in itertools.product(list(range(n)) + [None], repeat=m):
        b = [0] * n
        for k, owner in enumerate(assign):
            if owner is not None:
                b[owner] |= 1 << k
        out.add(tuple(b))
    return sorted(out)


def works(vals, s, g, x, n, perms):
    """Grow bundle x by g, then try every reassignment; land valid+balanced."""
    grown = tuple(y | (1 << g) if i == x else y for i, y in enumerate(s))
    if not balanced(grown):
        return False
    for perm in perms:
        t = tuple(grown[perm[i]] for i in range(n))
        if valid(vals, t):
            return True
    return False


def run(pool, n, m, label, sample, seed=20260827):
    rng = random.Random(seed)
    perms = list(itertools.permutations(range(n)))
    states = all_partial(n, m)

    tested = 0
    fail_some = 0
    fail_every_item = 0
    fail_every_min = 0
    witness = None

    for _ in range(sample):
        vals = tuple(rng.choice(pool) for _ in range(n))
        for s in states:
            free = [k for k in range(m) if not allocated(s) & (1 << k)]
            if not free or not balanced(s) or not valid(vals, s):
                continue
            tested += 1
            z = sizes(s)
            lo = min(z)
            mins = [x for x in range(n) if z[x] == lo]

            ok_items = []
            all_min_ok = True
            for g in free:
                good_x = [x for x in mins if works(vals, s, g, x, n, perms)]
                if good_x:
                    ok_items.append(g)
                if len(good_x) != len(mins):
                    all_min_ok = False

            if not ok_items:
                fail_some += 1
                if witness is None:
                    witness = (vals, s)
            if len(ok_items) != len(free):
                fail_every_item += 1
            if not all_min_ok:
                fail_every_min += 1

    print("  %-18s n=%d m=%d : %d valid balanced states" % (label, n, m, tested))
    print("     SOME-ITEM  failures : %d" % fail_some)
    print("     EVERY-ITEM failures : %d" % fail_every_item)
    print("     EVERY-MIN  failures : %d" % fail_every_min)
    if witness:
        vals, s = witness
        print("     SOME-ITEM witness at state %s sizes=%s"
              % (str(s), sizes(s)))
        for i, v in enumerate(vals):
            print("        agent %d %s" % (i + 1, str(v)))
    return fail_some, fail_every_item


CLASSES = (
    ("goods {0,1}", {0, 1}),
    ("chores {-1,0}", {-1, 0}),
    ("general {-1,0,1}", {-1, 0, 1}),
)


def pool_for(m, allowed):
    if allowed == {-1, 0, 1}:
        return list(enumerate_general_binary(m))
    return enumerate_class(m, allowed)


def main():
    print("(BAL-STEP): can balance always be kept, and how much choice is")
    print("needed to do it?")
    print()
    for (n, m, sample) in ((3, 3, 2500), (3, 4, 500), (4, 4, 250)):
        for label, allowed in CLASSES:
            run(pool_for(m, allowed), n, m, label, sample)
        print()


if __name__ == "__main__":
    main()
