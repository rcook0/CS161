# Proof Pattern Registry (v0.5 Canonical)

Each theorem in this reader must reference one or more pattern IDs.

---

## P1 — Induction
Structural or size-based induction.
Used for:
- Divide & Conquer correctness
- Recurrence proofs
- DP correctness

---

## P2 — Invariant
Loop/DFS/BFS invariants and termination arguments.
Used for:
- DFS stack correctness
- Relaxation invariants
- Greedy stays-ahead arguments

---

## P3 — Exchange Argument
Transform optimal solution to match greedy choice without worsening cost.
Used for:
- Interval scheduling
- Huffman coding

---

## P4 — Cut Property
Any minimum spanning tree contains a safe edge crossing a cut.
Used for:
- Prim correctness
- Kruskal correctness

---

## P5 — Relaxation
Maintain upper bounds that converge to optimum.
Used for:
- Dijkstra
- Bellman–Ford

---

## P6 — Expectation (Indicator Method)
Define indicator variables and apply linearity of expectation.
Used for:
- Randomized QuickSort
- Expected comparison counting

---

## P7 — Amplification
Repeat Monte Carlo algorithm to reduce failure probability.
Used for:
- Karger’s Min-Cut

---

## P8 — DP Optimal Substructure
Prove optimal solution decomposes into optimal subsolutions.
Used for:
- LIS
- LCS
- Knapsack

---

## P9 — Amortized Analysis
Aggregate / Accounting / Potential method.
Used for:
- Dynamic array resizing
- Union-Find intuition

---

## P10 — Reduction
Polynomial-time mapping preserving correctness.
Used for:
- NP-completeness proofs

---

## P11 — Adversary / Decision Tree
Lower bounds via information or adaptive adversary.
Used for:
- Ω(n log n) sorting lower bound
