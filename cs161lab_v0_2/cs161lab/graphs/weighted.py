from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple, Hashable, Optional

Node = Hashable

@dataclass(frozen=True)
class WEdge:
    u: Node
    v: Node
    w: float

class WeightedDiGraph:
    def __init__(self) -> None:
        self.adj: Dict[Node, List[Tuple[Node, float]]] = {}

    def add_node(self, u: Node) -> None:
        self.adj.setdefault(u, [])

    def add_edge(self, u: Node, v: Node, w: float) -> None:
        self.add_node(u)
        self.add_node(v)
        self.adj[u].append((v, float(w)))

    def nodes(self) -> List[Node]:
        return list(self.adj.keys())

    def neighbors(self, u: Node) -> List[Tuple[Node, float]]:
        return self.adj.get(u, [])

    def edges(self) -> List[WEdge]:
        out: List[WEdge] = []
        for u, lst in self.adj.items():
            for v,w in lst:
                out.append(WEdge(u,v,w))
        return out

    @classmethod
    def from_edges(cls, edges: Iterable[Tuple[Node, Node, float]]) -> "WeightedDiGraph":
        g = cls()
        for u,v,w in edges:
            g.add_edge(u,v,w)
        return g

class WeightedUGraph:
    def __init__(self) -> None:
        self.adj: Dict[Node, List[Tuple[Node, float]]] = {}

    def add_node(self, u: Node) -> None:
        self.adj.setdefault(u, [])

    def add_edge(self, u: Node, v: Node, w: float) -> None:
        self.add_node(u); self.add_node(v)
        w = float(w)
        self.adj[u].append((v,w))
        self.adj[v].append((u,w))

    def nodes(self) -> List[Node]:
        return list(self.adj.keys())

    def neighbors(self, u: Node) -> List[Tuple[Node, float]]:
        return self.adj.get(u, [])

    @classmethod
    def from_edges(cls, edges: Iterable[Tuple[Node, Node, float]]) -> "WeightedUGraph":
        g = cls()
        for u,v,w in edges:
            g.add_edge(u,v,w)
        return g
