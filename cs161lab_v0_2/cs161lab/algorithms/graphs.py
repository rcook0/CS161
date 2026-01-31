from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Set, Tuple, TypeVar, Optional

from cs161lab.trace import Trace

Node = TypeVar("Node")


@dataclass(frozen=True)
class DirectedGraph:
    adj: Dict[Node, List[Node]]

    @classmethod
    def from_edges(cls, edges: Iterable[Tuple[Node, Node]]) -> "DirectedGraph":
        adj: Dict[Node, List[Node]] = {}
        for u, v in edges:
            adj.setdefault(u, []).append(v)
            adj.setdefault(v, [])
        return cls(adj=adj)

    def nodes(self) -> List[Node]:
        return list(self.adj.keys())

    def neighbors(self, u: Node) -> List[Node]:
        return self.adj.get(u, [])


def topo_sort(
    g: DirectedGraph,
    *,
    trace: Optional[Trace] = None,
) -> List[Node]:
    """Topological sort using DFS postorder.

    Raises ValueError if a directed cycle exists.

    Proof hooks:
      - 'enter' / 'exit' events per node
      - 'back_edge' events when a cycle is detected
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color: Dict[Node, int] = {u: WHITE for u in g.nodes()}
    order: List[Node] = []

    def dfs(u: Node) -> None:
        color[u] = GRAY
        if trace is not None:
            trace.record("enter", node=u)
        for v in g.neighbors(u):
            if color[v] == WHITE:
                dfs(v)
            elif color[v] == GRAY:
                if trace is not None:
                    trace.record("back_edge", u=u, v=v)
                raise ValueError("cycle detected")
        color[u] = BLACK
        order.append(u)
        if trace is not None:
            trace.record("exit", node=u)

    for u in g.nodes():
        if color[u] == WHITE:
            dfs(u)

    order.reverse()
    return order
