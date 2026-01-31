from __future__ import annotations
from typing import Dict, Hashable, List, Optional, Set, Tuple
import heapq
import math

from cs161lab.graphs.weighted import WeightedUGraph, Node

def prim_mst(g: WeightedUGraph, start: Optional[Node] = None) -> List[Tuple[Node, Node, float]]:
    """Prim's algorithm. Returns list of edges (u,v,w) in the MST (or MSF if disconnected).

    For disconnected graphs, it returns a minimum spanning *forest* (one tree per component).
    """
    nodes = g.nodes()
    if not nodes:
        return []
    if start is None:
        start = nodes[0]

    visited: Set[Node] = set()
    mst_edges: List[Tuple[Node, Node, float]] = []

    def run_component(s: Node) -> None:
        visited.add(s)
        pq: List[Tuple[float, Node, Node]] = []
        for v,w in g.neighbors(s):
            heapq.heappush(pq, (w, s, v))
        while pq:
            w,u,v = heapq.heappop(pq)
            if v in visited:
                continue
            visited.add(v)
            mst_edges.append((u,v,w))
            for x,wx in g.neighbors(v):
                if x not in visited:
                    heapq.heappush(pq, (wx, v, x))

    # First component
    run_component(start)
    # Other components (forest)
    for u in nodes:
        if u not in visited:
            run_component(u)

    return mst_edges
