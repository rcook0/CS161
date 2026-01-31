# Proof patterns index (CS161 / Plotkin-style)

This index is meant to be used as the *spine* of a typed course reader. Each pattern includes:
(1) when it applies, (2) the canonical structure of the proof, and (3) where it shows up in `cs161lab`.

## Pattern P1 — Induction / structural recursion

**Use when:** divide-and-conquer algorithms; DP recurrences; recursive graph procedures.

**Template:**
1. Define the predicate on input size/structure.
2. Base case(s).
3. Inductive hypothesis on strictly smaller subproblems.
4. Show the algorithm’s combine step preserves correctness.

**Implementations:** mergesort (baseline), quicksort correctness (structural), topological sort (via DFS recursion).

## Pattern P2 — Loop invariant + termination

**Use when:** iterative algorithms with maintained partial correctness (BFS/DFS loops, scanning edges, etc).

**Template:**
1. Invariant statement (what is always true at loop head).
2. Initialization (true before first iteration).
3. Maintenance (true after one iteration).
4. Termination + postcondition (invariant + stopping condition implies goal).

**Implementations:** Dijkstra (priority queue loop), Bellman–Ford (relaxation rounds), Prim (growing tree).

## Pattern P3 — Exchange argument (greedy correctness)

**Use when:** greedy makes a locally optimal choice that can be “exchanged into” an optimal solution.

**Template:**
1. Take an optimal solution OPT.
2. Modify OPT to include the greedy choice.
3. Show objective value does not worsen and feasibility preserved.
4. Conclude greedy choice is safe.

**Implementations (planned):** interval scheduling, Huffman coding, some MST proofs.

## Pattern P4 — Cut / separation property

**Use when:** problems have “cuts” (partitions) and the optimal solution must cross cuts in structured ways.

**Template:**
1. Define a cut (S, V\S) with respect to the current partial solution.
2. Show a “safe” edge exists among the minimum crossing edges.
3. Argue adding a safe edge preserves existence of an optimum extending current partial solution.

**Implementations:** Prim’s MST.

## Pattern P5 — Relaxation invariant (shortest paths)

**Use when:** you maintain upper bounds on distances and improve them by relaxation.

**Template:**
1. Maintain: `dist[v]` is always an upper bound on true shortest path distance.
2. Show relaxation cannot violate the upper bound property.
3. Prove a “finalization lemma” (Dijkstra): when a node is extracted, `dist` is optimal (requires nonnegative weights).
4. For Bellman–Ford: after k rounds, paths with ≤k edges are correct.

**Implementations:** Dijkstra, Bellman–Ford.

## Pattern P6 — Adversary argument / lower bounds

**Use when:** proving *no algorithm* can beat a bound (comparison sorting Ω(n log n), etc).

**Template:**
- Specify what the algorithm can observe.
- Construct an adversary that responds to preserve ambiguity unless the algorithm does enough work.
- Translate ambiguity into a decision-tree/ information bound.

**Implementations (planned):** comparison sorting lower bound; online variants.

## Pattern P7 — Amortized analysis (accounting / potential)

**Use when:** individual operations can be expensive, but sequences are cheap on average.

**Template A (accounting):** charge each operation a “fee”; store credits to pay for rare expensive events.  
**Template B (potential):** define Φ(state); show total cost ≤ Σ(actual) + Φ(final) − Φ(initial).

**Implementations (planned):** dynamic arrays; union-find; hashing rehash.

## Pattern P8 — Randomization via linearity of expectation

**Use when:** expected value is easy to compute without independence.

**Template:**
1. Define indicators for “bad events” or contributions.
2. Compute expectation per indicator.
3. Sum expectations.

**Implementations:** Karger trial analysis (expected success), randomized quicksort expected comparisons (planned notes).

## Pattern P9 — Randomization tail bounds + amplification

**Use when:** you want high probability guarantees from constant success probability.

**Template:**
- Run independent trials; use union bound and/or Chernoff/Markov-style bounds.
- Choose repetitions r to drive failure probability below δ.

**Implementations:** Karger min-cut via repetition schedule.

## Pattern P10 — Reduction

**Use when:** relating problems (NP-completeness, equivalence, hardness transfer).

**Template:**
1. Define mapping f from instances of A to instances of B.
2. Prove: x in A ⇔ f(x) in B.
3. Prove f runs in polynomial time.

**Implementations (planned):** SAT reductions (notes), graph reductions.

## Pattern P11 — DP optimal substructure

**Use when:** optimal solution decomposes into optimal subsolutions under a well-defined boundary choice.

**Template:**
1. Define subproblem precisely.
2. Prove recurrence by considering the last/first decision (a cut lemma).
3. Fill table in a correct topological order.
4. Optional: reconstruct witness.

**Implementations (planned):** LCS, knapsack, LIS.

## Pattern P12 — Greedy stays-ahead / dominance

**Use when:** you can compare partial solutions prefix-by-prefix.

**Template:**
- Show after i steps, greedy’s partial solution is at least as good as any other partial solution on some dominance measure.

**Implementations (planned):** interval scheduling; some matroid settings.

## Coverage map (algorithms → proof patterns)

This package aims for **one canonical executable exemplar per proof pattern**.

- **Induction / recursion**
  - `randomized_quicksort` (divide-and-conquer recursion, base cases)
- **Invariants + termination**
  - `topo_sort` (DFS colors; back-edge implies cycle)
- **Relaxation invariant**
  - `dijkstra`, `bellman_ford` (upper bounds decrease; BF detects negative cycles)
- **Cut property**
  - `prim_mst` (safe edge across a cut)
- **Probabilistic method + amplification**
  - `karger_min_cut` (repeat trials; trace captures contractions and best-so-far)
- **DP optimal substructure + reconstruction**
  - `lis`, `lcs`, `knapsack_01`
- **Greedy exchange / stays-ahead**
  - `interval_scheduling` (earliest finish time)
  - `huffman_codes` (two-minimum merge step)
- **Amortized analysis**
  - `DynamicArray` (doubling/halving; resize events)
  - `UnionFind` (path compression + rank; find/union events)

All algorithms accept an optional `Trace` to emit structured “proof hooks.”
