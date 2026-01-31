# Migration notes (legacy -> cs161lab)

The `cs161lab/legacy/` folder contains your original scripts (with only a minimal bug fix in `l1_MinCuts_Kargers.py`).

The new `cs161lab/` package provides:
- canonical graph models
- core algorithms (RandQS, RandSelect, topo sort, Dijkstra, Bellman–Ford, Prim, Karger)
- a small CLI

Next steps (if you want full parity with a CS161 syllabus):
- DP chapter implementations (LIS/LCS/Knapsack) + reconstruction.
- Greedy “exchange” exemplars (interval scheduling, Huffman).
- Reductions toolkit + NP-completeness exercise set.
- Amortized analysis exemplars (dynamic array, union-find).
