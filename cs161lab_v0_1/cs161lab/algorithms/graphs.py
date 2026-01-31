from __future__ import annotations
from typing import Dict, List, Optional, Set, Tuple, Hashable

from cs161lab.graphs.directed import DiGraph, Node

def dfs_postorder(g: DiGraph) -> List[Node]:
    """Return nodes in DFS postorder (useful for topo/SCC)."""
    visited: Set[Node] = set()
    post: List[Node] = []

    def visit(u: Node) -> None:
        visited.add(u)
        for v in g.neighbors(u):
            if v not in visited:
                visit(v)
        post.append(u)

    for u in g.nodes():
        if u not in visited:
            visit(u)
    return post

def topological_sort(g: DiGraph) -> List[Node]:
    """Topological sort via DFS postorder. Raises ValueError on cycles."""
    color: Dict[Node, int] = {}  # 0=unseen,1=visiting,2=done
    order: List[Node] = []

    def visit(u: Node) -> None:
        c = color.get(u, 0)
        if c == 1:
            raise ValueError("graph has a cycle; not a DAG")
        if c == 2:
            return
        color[u] = 1
        for v in g.neighbors(u):
            visit(v)
        color[u] = 2
        order.append(u)

    for u in g.nodes():
        if color.get(u, 0) == 0:
            visit(u)
    order.reverse()
    return order
