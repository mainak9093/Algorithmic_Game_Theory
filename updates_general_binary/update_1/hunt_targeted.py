"""
Approach 15: a targeted counterexample hunt, where uniform sampling is useless.

hunt_counterexample.py's random mode reports max = 0 for general binary at
n=3, m=4: a uniformly random valuation from a class of 197547 almost never has
the knife-edge structure that forces any subsidy at all, so that sweep is not
evidence of anything. Two fixes here.

1. A GENERATOR instead of an enumerator. enumerate_general_binary(5) does not
   fit in memory, so valuations are built directly by walking the subset
   lattice and choosing each value at random within its admissible window.
   That reaches m = 5, 6 without materialising the class.

2. A HILL CLIMB on the quantity that matters. The objective is

       f(instance) = min over complete allocations of ( max_i p*_i ),

   which the conjecture says never exceeds 1. Starting from a random instance,
   repeatedly perturb one valuation at one subset (staying inside the class)
   and keep the change whenever f does not decrease. A counterexample is any
   instance reaching f >= 2. This searches the neighbourhood of the hardest
   instances found so far rather than the bulk of the class, which is where a
   counterexample would have to live.

3. A STRUCTURED seed aimed at fact F2. The path-increment lemma says a single
   insertion can raise a path by 2 only when some agent i has marginal +1 for
   an item at bundle A_x while its holder x has marginal -1 for the same item
   at the same bundle. Seeds are therefore biased toward disagreement: agents
   are generated with opposing preferences over the same items.

If the climb cannot reach 2 from many restarts at several (n, m), that is
meaningful evidence for the conjecture in a way uniform sampling is not.
"""
import random
import sys
import time

from gb_valuations import (
    masks_by_popcount,
    best_over_allocations,
    marginals_within,
)


def random_general_binary(m, rng, weights=(1, 1, 1)):
    """
    One uniformly-structured random general binary valuation, built by walking
    the lattice and choosing each value inside its admissible window. `weights`
    biases the choice of marginal toward -1, 0 or +1.
    """
    values = [0] * (1 << m)
    for S in masks_by_popcount(m):
        if S == 0:
            continue
        bits = [1 << b for b in range(m) if S & (1 << b)]
        lo = max(values[S ^ b] for b in bits) - 1
        hi = min(values[S ^ b] for b in bits) + 1
        # express the window as marginals off one predecessor, to apply the bias
        ref = values[S ^ bits[0]]
        options = list(range(lo, hi + 1))
        w = [weights[max(0, min(2, v - ref + 1))] for v in options]
        values[S] = rng.choices(options, weights=w)[0]
    return tuple(values)


def opposed_pair(m, rng):
    """
    Two valuations that disagree in sign about the same items, the shape fact
    F2 says is necessary for a path to grow by 2.
    """
    a = random_general_binary(m, rng, weights=(1, 1, 3))     # likes things
    b = random_general_binary(m, rng, weights=(3, 1, 1))     # dislikes things
    return a, b


def seed_unit_good(n, m):
    """
    The tight lower-bound instance on the goods side: one item everybody wants,
    everything else worthless. Its f is 1, so it gives the climb a foothold in
    the rare region where any subsidy is needed at all.
    """
    v = tuple(1 if S & 1 else 0 for S in range(1 << m))
    return [v] * n


def seed_unit_chores(n, m):
    """
    The mirrored tight instance: n-1 items are unit chores for everybody, the
    rest are neutral. Restricting to n-1 active items keeps f at 1 even when
    m >= n, where plain c(S) = |S| would let everyone take a share and f drop
    to 0.
    """
    active = (1 << max(1, min(m, n - 1))) - 1
    v = tuple(-bin(S & active).count("1") for S in range(1 << m))
    return [v] * n


def seed_opposed(n, m, rng):
    """One item wanted by half the agents and refused by the other half."""
    like = tuple(1 if S & 1 else 0 for S in range(1 << m))
    hate = tuple(-1 if S & 1 else 0 for S in range(1 << m))
    return [like if i % 2 == 0 else hate for i in range(n)]


def neighbours(v, m):
    """Every single-subset perturbation of v that stays in the class."""
    out = []
    for S in range(1, 1 << m):
        bits_in = [1 << b for b in range(m) if S & (1 << b)]
        bits_out = [1 << b for b in range(m) if not S & (1 << b)]
        lo = max(v[S ^ b] for b in bits_in) - 1
        hi = min(v[S ^ b] for b in bits_in) + 1
        for b in bits_out:
            lo = max(lo, v[S | b] - 1)
            hi = min(hi, v[S | b] + 1)
        for val in range(lo, hi + 1):
            if val != v[S]:
                w = list(v)
                w[S] = val
                out.append((S, tuple(w)))
    return out


def objective(vals, n, m):
    value, _ = best_over_allocations(vals, n, m)
    return -1 if value is None else value


def climb(n, m, rng, restarts, steps):
    """Hill climb on f; returns (best value, best instance)."""
    best_overall, best_instance = -1, None
    for r in range(restarts):
        # Cycle the structured f=1 seeds so most restarts begin inside the
        # region where a subsidy is needed at all; a uniformly random start is
        # almost always at f=0, where the objective is flat and the climb just
        # random-walks.
        pick = r % 4
        if pick == 0:
            vals = seed_unit_good(n, m)
        elif pick == 1:
            vals = seed_unit_chores(n, m)
        elif pick == 2:
            vals = seed_opposed(n, m, rng)
        else:
            a, b = opposed_pair(m, rng)
            vals = ([a, b] + [random_general_binary(m, rng)
                              for _ in range(n - 2)])[:n]
        cur = objective(vals, n, m)

        for _ in range(steps):
            i = rng.randrange(n)
            cands = neighbours(vals[i], m)
            if not cands:
                continue
            _, w = rng.choice(cands)
            trial = list(vals)
            trial[i] = w
            score = objective(trial, n, m)
            if score >= cur:
                vals, cur = trial, score
            if cur >= 2:
                break

        if cur > best_overall:
            best_overall, best_instance = cur, list(vals)
        if cur >= 2:
            break
    return best_overall, best_instance


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 20260827
    rng = random.Random(seed)

    print("Targeted hunt: hill climb on min-over-allocations of max subsidy")
    print("(the conjecture says this never reaches 2)")
    print()

    plan = ((2, 3, 300, 200), (3, 3, 300, 200), (3, 4, 250, 200),
            (4, 4, 200, 200), (3, 5, 120, 150), (4, 5, 100, 150),
            (5, 5, 80, 150))

    worst = -1
    for (n, m, restarts, steps) in plan:
        t0 = time.time()
        value, instance = climb(n, m, rng, restarts, steps)
        worst = max(worst, value)
        print("  n=%d m=%d : %d restarts x %d steps -> best f = %d  (%.1fs)"
              % (n, m, restarts, steps, value, time.time() - t0))
        if value >= 2:
            print("    COUNTEREXAMPLE:")
            for v in instance:
                print("      ", v)
        elif value >= 1:
            ok = all(marginals_within(v, m, {-1, 0, 1}) for v in instance)
            print("    hardest instance (f=%d, class check %s):"
                  % (value, "OK" if ok else "INVALID"))
            for v in instance:
                print("      ", v)
    print()
    print("best f found anywhere: %d  -> conjecture %s"
          % (worst, "VIOLATED" if worst >= 2 else "not violated"))


if __name__ == "__main__":
    main()
