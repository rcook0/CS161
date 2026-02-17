
# Plotkin CS161 (Fall 2010) — Lecture Map

This document maps Plotkin Fall 2010 CS161 lectures to proof patterns and executable witnesses in `cs161lab`.

## Legend
- **Patterns**: induction, invariant, cut, exchange, expectation, amplification, relaxation, DP-opt-sub, amortized, reduction
- **Code**: fully qualified function/module names

## Mapping

| Lec | Topic | Core Theorems | Proof Patterns | Code |
|-----|-------|---------------|----------------|------|
| L1–2 | Models & Asymptotics | Comparison model; Ω(n log n) sorting | adversary | theory-only |
| L3 | Divide & Conquer | Master-style bounds | induction | cs161lab.algorithms.sorting.merge_sort |
| L4 | Randomized Algos I | Linearity of Expectation | expectation | cs161lab.algorithms.sorting.rand_quicksort |
| L5 | Randomized Algos II | Amplification; Union Bound | amplification | cs161lab.algorithms.mincut.karger |
| L6 | Selection | Expected Linear Time | expectation, induction | cs161lab.algorithms.sorting.quickselect |
| L7 | Graph Search | DFS Properties | invariant, induction | cs161lab.algorithms.graphs.dfs, toposort |
| L8 | Shortest Paths | Relaxation Invariant | relaxation | cs161lab.algorithms.sssp.dijkstra, bellman_ford |
| L9 | MST | Cut Property | cut | cs161lab.algorithms.mst.prim |
| L10 | Greedy | Exchange/Stays-Ahead | exchange | interval_scheduling, huffman |
| L11 | Dynamic Prog | Optimal Substructure | DP-opt-sub | lis, lcs, knapsack_01 |
| L12 | Amortized | Potential Method | amortized | DynamicArray, UnionFind |
| L13+ | NP & Reductions | NP-Completeness | reduction | theory-only |
