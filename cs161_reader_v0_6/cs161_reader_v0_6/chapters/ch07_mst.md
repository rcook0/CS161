# Chapter 07 — Minimum Spanning Trees

## Cut Property [P4]
For any cut, the lightest edge crossing it is safe (belongs to some MST).

## Theorem 7.1 (Prim Correctness) [P4, P2]
Maintaining a growing tree, selecting minimum crossing edge preserves optimality.

## Theorem 7.2 (Kruskal Correctness) [P4]
Edges added in increasing weight order, skipping cycles, produce an MST.
