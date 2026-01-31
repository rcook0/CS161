from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple, TypeVar
import heapq
import math

from cs161lab.trace import Trace

Node = TypeVar("Node")


@dataclass(frozen=True)
class WeightedDigraph:
    adj: Dict[Node, List[Tuple[Node, float]]]

    @classmethod
    def from_edges(cls, edges: Iterable[Tuple[Node, Node, float]]) -> "WeightedDigraph":
        adj: Dict[Node, List[Tuple[Node, float]]] = {}
        for u, v, w in edges:
            adj.setdefault(u, []).append((v, float(w)))
            adj.setdefault(v, [])
        return cls(adj=adj)

    def nodes(self) -> List[Node]:
        return list(self.adj.keys())

    def neighbors(self, u: Node) -> List[Tuple[Node, float]]:
        return self.adj.get(u, [])


def dijkstra(
    g: WeightedDigraph,
    src: Node,
    *,
    trace: Optional[Trace] = None,
) -> Dict[Node, float]:
    """Dijkstra's algorithm (requires nonnegative edge weights).

    Proof hooks:
      - 'finalize' when a node's distance is settled
      - 'relax' for every successful relaxation
      - 'skip_stale' when discarding stale heap entries
    """
    dist: Dict[Node, float] = {u: math.inf for u in g.nodes()}
    dist[src] = 0.0
    pq: List[Tuple[float, Node]] = [(0.0, src)]
    visited: Dict[Node, bool] = {u: False for u in g.nodes()}

    while pq:
        du, u = heapq.heappop(pq)
        if du != dist[u]:
            if trace is not None:
                trace.record("skip_stale", node=u, heap_du=du, dist=dist[u])
            continue
        if visited[u]:
            continue
        visited[u] = True
        if trace is not None:
            trace.record("finalize", node=u, dist=du)

        for v, w in g.neighbors(u):
            if w < 0:
                raise ValueError("negative edge weight encountered in Dijkstra")
            nd = du + w
            if nd < dist[v]:
                old = dist[v]
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
                if trace is not None:
                    trace.record("relax", u=u, v=v, w=w, old=old, new=nd)

    return dist


def bellman_ford(
    g: WeightedDigraph,
    src: Node,
    *,
    trace: Optional[Trace] = None,
) -> Tuple[Dict[Node, float], bool]:
    """Bellman–Ford: returns (dist, has_negative_cycle_reachable).

    Proof hooks:
      - 'iteration' per pass (with count of relaxations)
      - 'relax' for each successful relaxation
      - 'neg_cycle' if a reachable negative cycle is detected
    """
    nodes = g.nodes()
    dist: Dict[Node, float] = {u: math.inf for u in nodes}
    dist[src] = 0.0

    edges: List[Tuple[Node, Node, float]] = []
    for u in nodes:
        for v, w in g.neighbors(u):
            edges.append((u, v, w))

    # Relax edges |V|-1 times
    for i in range(len(nodes) - 1):
        changed = 0
        for u, v, w in edges:
            if dist[u] != math.inf and dist[u] + w < dist[v]:
                old = dist[v]
                dist[v] = dist[u] + w
                changed += 1
                if trace is not None:
                    trace.record("relax", iter=i, u=u, v=v, w=w, old=old, new=dist[v])
        if trace is not None:
            trace.record("iteration", iter=i, relaxations=changed)
        if changed == 0:
            break

    # Check for negative cycles reachable from src
    for u, v, w in edges:
        if dist[u] != math.inf and dist[u] + w < dist[v]:
            if trace is not None:
                trace.record("neg_cycle", u=u, v=v, w=w)
            return dist, True

    return dist, False
