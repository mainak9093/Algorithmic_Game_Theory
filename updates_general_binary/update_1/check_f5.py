"""
Approach 15, fact F5: BKNS's FINDSINK (Algorithm 3 of References/Reading_3.pdf)
does not terminate on chores.

Rather than assert this from reading the pseudocode, this script implements
EXTEND (Algorithm 2) and FINDSINK (Algorithm 3) literally as printed and runs
them on the witness, with an iteration cap so the non-termination shows up as a
detected repeat rather than a hang.

THE WITNESS. n = 2, additive unit costs c_i(S) = |S|, so v_i(S) = -|S|, which
is negative dichotomous. Current state:

    A = ({e}, {})        p = (1, 0)

(A, p) is an envy-free solution: agent 1 has -1 + 1 = 0 against agent 2's
bundle 0 + 0 = 0, and agent 2 has 0 + 0 = 0 against agent 1's -1 + 1 = 0. The
subsidy is minimal -- l_A(1) = w(1,2) = v_1(A_2) - v_1(A_1) = 0 - (-1) = 1 and
l_A(2) = max(0, w(2,1)) = max(0, -1) = 0 -- and lies in {0,1}^2.

Now insert one more chore f.

WHAT ALG DOES. Extendability (Definition 3) requires an agent with a marginal
of EXACTLY +1 for the new item. Every marginal of a chore is <= 0, so no
extendable configuration exists and ALG falls through to FINDSINK (line 8).
FINDSINK line 1 selects s from M(p), the MOST subsidised agents -- here
M(p) = {1} -- and forms X = ({e,f}, {}). Its subsidy is phi_1 = 2, so the
while-loop on line 3 fires, and line 4 sets s <- j for an agent with phi_j >= 2.
The only such agent is 1, which is already s: X does not change, and the loop
runs forever.

WHY IT BREAKS. Lemma 10 proves FINDSINK terminates by showing that a repeated
agent forces an edge with marginal exactly +1 (Claim 2), contradicting
non-extendability. On chores no marginal is ever +1, so Claim 2 is
unavailable and the termination proof has nothing to run on.

THE FIX THE WITNESS POINTS AT. The correct recipient here is agent 2, who is
in argmin p, not in M(p) = argmax p. Chores should be routed to a MINIMALLY
subsidised agent -- the dual of BKNS's rule. The script confirms that this
choice does keep the subsidy in {0,1}^2.
"""
import itertools

from gb_valuations import arc_weights, is_envy_freeable, longest_paths

N = 2
E, F = 0, 1          # item indices: e = the already-allocated chore, f = new


def v_unit_cost(mask):
    """v_i(S) = -|S| for both agents: additive unit costs, a chore instance."""
    return -bin(mask).count("1")


VALS = [ [v_unit_cost(S) for S in range(4)] for _ in range(N) ]


def min_subsidy(bundles):
    if not is_envy_freeable(VALS, bundles):
        return None
    return longest_paths(arc_weights(VALS, bundles))


def M(p):
    """The maximally subsidised agents, BKNS's M(p)."""
    top = max(p)
    return [i for i in range(N) if p[i] == top]


def is_extendable(bundles, p, g):
    """
    Definition 3: some permutation sigma makes A_sigma envy-freeable with
    subsidy q = p_sigma, and some agent kappa in M(q) has marginal exactly 1
    for g at its bundle.
    """
    for perm in itertools.permutations(range(N)):
        permuted = tuple(bundles[perm[i]] for i in range(N))
        q = min_subsidy(permuted)
        if q is None:
            continue
        for kappa in M(q):
            b = permuted[kappa]
            if VALS[kappa][b | (1 << g)] - VALS[kappa][b] == 1:
                return True, perm, kappa
    return False, None, None


def findsink(bundles, p, g, cap=12):
    """
    Algorithm 3, transcribed. Returns (agent, trace) on termination, or
    (None, trace) if an agent repeats -- which is the non-termination the
    lemma is supposed to rule out.
    """
    trace = []
    seen = []
    s = M(p)[0]                                   # line 1: arbitrary s in M(p)
    for _ in range(cap):
        X = tuple(b | (1 << g) if i == s else b for i, b in enumerate(bundles))
        phi = min_subsidy(X)
        trace.append((s, X, phi))
        if phi is None:
            return None, trace
        over = [j for j in range(N) if phi[j] >= 2]     # line 3
        if not over:
            return s, trace
        if s in seen:
            return None, trace
        seen.append(s)
        s = over[0]                                     # line 4
    return None, trace


def show(bundles):
    names = {0: "{}", 1: "{e}", 2: "{f}", 3: "{e,f}"}
    return "(" + ", ".join(names[b] for b in bundles) + ")"


def main():
    bundles = (1 << E, 0)                              # A = ({e}, {})
    p = min_subsidy(bundles)
    print("state   A = %s" % show(bundles))
    print("        minimal subsidy p = %s   -> in {0,1}^n: %s"
          % (p, all(x in (0, 1) for x in p)))
    print("        M(p) = %s   argmin p = %s"
          % ([i + 1 for i in M(p)],
             [i + 1 for i in range(N) if p[i] == min(p)]))
    print()

    ext, perm, kappa = is_extendable(bundles, p, F)
    print("insert chore f")
    print("        extendable?  %s   (Definition 3 needs a marginal of +1; "
          "chores have none)" % ext)
    print()

    print("        ALG therefore calls FINDSINK:")
    agent, trace = findsink(bundles, p, F)
    for k, (s, X, phi) in enumerate(trace):
        print("          iter %d: s = agent %d, X = %s, subsidy = %s"
              % (k + 1, s + 1, show(X), phi))
    if agent is None:
        print("        FINDSINK DID NOT TERMINATE: agent %d recurs with the "
              "same X, so line 4 makes no progress." % (trace[-1][0] + 1))
    else:
        print("        FINDSINK returned agent %d" % (agent + 1))
    print()

    print("        the recipient that actually works:")
    for x in range(N):
        X = tuple(b | (1 << F) if i == x else b for i, b in enumerate(bundles))
        phi = min_subsidy(X)
        ok = phi is not None and all(q <= 1 for q in phi)
        print("          give f to agent %d -> X = %s, subsidy = %s   %s"
              % (x + 1, show(X), phi,
                 "OK" if ok else "subsidy 2, violates the bound"))
    print()
    print("        agent 2 is in argmin p, not in M(p): BKNS's routing rule "
          "picks the wrong agent on chores.")


if __name__ == "__main__":
    main()
