# Plotkin CS161 (Fall 2010) — Lecture Map

Maps Plotkin Fall 2010 CS161 lectures to proof patterns and executable witnesses in `cs161lab`.

## Proof-pattern vocabulary
- induction, invariant, exchange, cut, relaxation, expectation, amplification, DP-opt-sub, amortized, reduction, adversary

## Mapping (lecture-granular spine)

| Lec | Topic | Core results / what you must be able to prove | Proof patterns | Executable witness (cs161lab) |
|-----|------|-----------------------------------------------|----------------|-------------------------------|
| L1 | Models, asymptotics | Model discipline; asymptotic reasoning | invariant | theory-only |
| L2 | Lower bounds | Comparison sorting Ω(n log n); decision trees | adversary | theory-only |
| L3 | Divide & Conquer | Correctness by induction; solve recurrences | induction | `cs161lab.algorithms.sorting.merge_sort` |
| L4 | Randomization I | Indicators; expected comparisons | expectation | `cs161lab.algorithms.sorting.rand_quicksort` |
| L5 | Randomization II | Amplification; union bound; Monte Carlo | amplification, expectation | `cs161lab.algorithms.mincut.karger` |
| L6 | Selection | Expected linear time selection | expectation, induction | `cs161lab.algorithms.sorting.quickselect` |
| L7 | Graph search | DFS invariants; topo correctness; cycles | invariant, induction | `cs161lab.algorithms.graphs.dfs`, `...toposort` |
| L8 | Shortest paths | Relaxation; Dijkstra finalization; BF neg cycles | relaxation, invariant | `cs161lab.algorithms.sssp.dijkstra`, `...bellman_ford` |
| L9 | MST | Cut property; Prim/Kruskal correctness | cut | `cs161lab.algorithms.mst.prim` |
| L10 | Greedy | Exchange / stays-ahead; Huffman lemma | exchange, invariant | `cs161lab.algorithms.greedy.interval_scheduling`, `...huffman_codes` |
| L11 | Dynamic programming | Recurrences; reconstruction | DP-opt-sub, induction | `cs161lab.algorithms.dp.lis`, `...lcs`, `...knapsack_01` |
| L12 | Amortized | Potential method; UF intuition | amortized | `cs161lab.ds.dynamic_array.DynamicArray`, `cs161lab.ds.union_find.UnionFind` |
| L13+ | NP & reductions | NP-completeness via reductions | reduction | theory-only |

## Chapter assignment (this reader)
- Chapter 04: L4–L6 (Randomization + Selection) + Karger amplification (L5)
- Chapter 05: L7 (Graph search + topological order)
- Chapter 06: L8 (Shortest paths: Dijkstra + Bellman–Ford)
