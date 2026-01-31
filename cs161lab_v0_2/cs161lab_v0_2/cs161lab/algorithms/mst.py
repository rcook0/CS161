from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Set, Tuple, TypeVar
import heapq

from cs161lab.trace import Trace

Node = TypeVar("Node")


@dataclass(frozen=True)
class WeightedUndirected:
    adj: Dict[Node, List[Tuple[Node, float]]]

    @classmethod
    def from_edges(cls, edges: Iterable[Tuple[Node, Node, float]]) -> "WeightedUndirected":
        adj: Dict[Node, List[Tuple[Node, float]]] = {}
        for u, v, w in edges:
            w = float(w)
            adj.setdefault(u, []).append((v, w))
            adj.setdefault(v, []).append((u, w))
        return cls(adj=adj)

    def nodes(self) -> List[Node]:
        return list(self.adj.keys())

    def neighbors(self, u: Node) -> List[Tuple[Node, float]]:
        return self.adj.get(u, [])


def prim_mst(
    g: WeightedUndirected,
    *,
    trace: Optional[Trace] = None,
) -> List[Tuple[Node, Node, float]]:
    """Prim's algorithm for MST (or MSF if disconnected).

    Returns edges (u, v, w) of the minimum spanning forest.

    Proof hooks:
      - 'component_start' when starting a new component
      - 'push' when a crossing edge is added to the heap
      - 'accept' when an edge is chosen (cut property 'safe edge')
      - 'skip' for edges whose head is already in the tree
    """
    nodes = g.nodes()
    in_tree: Set[Node] = set()
    forest: List[Tuple[Node, Node, float]] = []

    for start in nodes:
        if start in in_tree:
            continue
        if trace is not None:
            trace.record("component_start", start=start)
        in_tree.add(start)
        pq: List[Tuple[float, Node, Node]] = []  # (w, u, v)

        for v, w in g.neighbors(start):
            heapq.heappush(pq, (w, start, v))
            if trace is not None:
                trace.record("push", u=start, v=v, w=w)

        while pq:
            w, u, v = heapq.heappop(pq)
            if v in in_tree:
                if trace is not None:
                    trace.record("skip", u=u, v=v, w=w)
                continue
            in_tree.add(v)
            forest.append((u, v, w))
            if trace is not None:
                trace.record("accept", u=u, v=v, w=w, tree_size=len(in_tree))

            for x, wx in g.neighbors(v):
                if x not in in_tree:
                    heapq.heappush(pq, (wx, v, x))
                    if trace is not None:
                        trace.record("push", u=v, v=x, w=wx)

    return forest
