from __future__ import annotations
from typing import Dict, Hashable, List, Optional, Tuple
import heapq
import math

from cs161lab.graphs.weighted import WeightedDiGraph, Node, WEdge

def dijkstra(g: WeightedDiGraph, src: Node) -> Tuple[Dict[Node, float], Dict[Node, Optional[Node]]]:
    """Dijkstra's algorithm (requires nonnegative edge weights)."""
    dist: Dict[Node, float] = {u: math.inf for u in g.nodes()}
    prev: Dict[Node, Optional[Node]] = {u: None for u in g.nodes()}
    dist[src] = 0.0

    pq: List[Tuple[float, Node]] = [(0.0, src)]
    visited = set()

    while pq:
        du, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        if du != dist[u]:
            continue
        for v, w in g.neighbors(u):
            if w < 0:
                raise ValueError("Dijkstra requires nonnegative weights")
            nd = du + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    return dist, prev

def bellman_ford(g: WeightedDiGraph, src: Node) -> Tuple[Dict[Node, float], Dict[Node, Optional[Node]]]:
    """Bellman–Ford. Detects negative cycles reachable from src."""
    dist: Dict[Node, float] = {u: math.inf for u in g.nodes()}
    prev: Dict[Node, Optional[Node]] = {u: None for u in g.nodes()}
    dist[src] = 0.0

    edges = g.edges()
    n = len(g.nodes())

    for _ in range(n-1):
        changed = False
        for e in edges:
            if dist[e.u] != math.inf and dist[e.u] + e.w < dist[e.v]:
                dist[e.v] = dist[e.u] + e.w
                prev[e.v] = e.u
                changed = True
        if not changed:
            break

    # cycle check
    for e in edges:
        if dist[e.u] != math.inf and dist[e.u] + e.w < dist[e.v]:
            raise ValueError("negative cycle reachable from source")
    return dist, prev
