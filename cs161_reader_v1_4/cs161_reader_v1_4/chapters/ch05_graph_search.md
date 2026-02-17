% Chapter 05 — Graph Search and Topological Order
% CS161 Reader (Plotkin F10)
%

# Chapter 05 — Graph Search and Topological Order

## Invariant 5.1 (DFS Stack Invariant) [P2] {#inv-5-1}
Gray vertices correspond exactly to the recursion stack.

## Lemma 5.2 (Back Edge ⇒ Cycle) [P2] {#lem-5-2}
A back edge to a gray vertex certifies a directed cycle.

## Theorem 5.3 (Topo Order via Finishing Times) [P2] {#thm-5-3}
In a DAG, ordering vertices by decreasing finishing times yields a topological order.
