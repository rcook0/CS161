from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Iterable, List, Set, Tuple, Hashable, Optional

Node = Hashable

@dataclass(frozen=True)
class Edge:
    u: Node
    v: Node

class DiGraph:
    """Simple directed unweighted graph."""
    def __init__(self) -> None:
        self.adj: Dict[Node, List[Node]] = {}

    def add_node(self, u: Node) -> None:
        self.adj.setdefault(u, [])

    def add_edge(self, u: Node, v: Node) -> None:
        self.add_node(u)
        self.add_node(v)
        self.adj[u].append(v)

    def nodes(self) -> List[Node]:
        return list(self.adj.keys())

    def neighbors(self, u: Node) -> List[Node]:
        return self.adj.get(u, [])

    @classmethod
    def from_edges(cls, edges: Iterable[Tuple[Node, Node]]) -> "DiGraph":
        g = cls()
        for u,v in edges:
            g.add_edge(u,v)
        return g
