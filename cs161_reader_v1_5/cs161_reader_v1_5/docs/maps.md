# Maps

Approximate/accurate navigation maps for CS161.

Tokens:
- `@thm-…` links to a theorem anchor.
- `@hook-…` links to hook evidence bundle (when built).

## Lecture-to-chapter spine (approx)
- Randomization → **CH04**
- Graph search (DFS/BFS/topo) → **CH05**
- Shortest paths (Dijkstra/Bellman–Ford) → **CH06**
- MST (Prim/Kruskal, cut property) → **CH07**
- Greedy (exchange arguments, Huffman) → **CH08**
- Dynamic programming core → **CH09**
- Amortized analysis + classic DS → **CH10**
- NP, reductions, NP-completeness → **CH11**

## Concept dependency (approx)
- Invariants (P2) ⇒ Topological sorting (@thm-5-3)
- Relaxation (P5) ⇒ Dijkstra (@thm-6-3) ⇒ Bellman–Ford (@thm-6-6)
- Cut property (P4) ⇒ MST correctness (@thm-7-1, @thm-7-2)
- Exchange (P3) ⇒ interval scheduling (@thm-8-1) ⇒ Huffman (@thm-8-3)
- DP template (P8) ⇒ state/recurrence/reconstruction (@tpl-9-1)
- Potential/accounting (P9) ⇒ dynamic arrays (@thm-10-1)
- Reduction template (P10) ⇒ NP-completeness (@tpl-11-1)

## Actionable nodes (with evidence)
- QuickSort expectation witness: @thm-4-3 + @hook-thm-4-3-quicksort-indicators
- Karger min-cut amplification witness: @thm-4-6 + @hook-thm-4-6-karger-amplify
- Dijkstra finalization witness: @thm-6-3 + @hook-thm-6-3-dijkstra-finalize
- Dynamic array amortized witness: @thm-10-1 + @hook-thm-10-1-dynarray-credits
