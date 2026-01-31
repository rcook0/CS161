from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Hashable, List, Optional, Tuple
import random

from cs161lab.trace import Trace

Node = Hashable
Edge = Tuple[Node, Node]


@dataclass
class UnionFind:
    parent: Dict[Node, Node]
    rank: Dict[Node, int]

    @classmethod
    def from_nodes(cls, nodes: List[Node]) -> "UnionFind":
        return cls(parent={x: x for x in nodes}, rank={x: 0 for x in nodes})

    def find(self, x: Node) -> Node:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: Node, b: Node) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


def karger_min_cut_once(
    edges: List[Edge],
    *,
    seed: Optional[int] = None,
    trace: Optional[Trace] = None,
) -> int:
    """Run a single contraction trial of Karger's min-cut algorithm.

    Input: list of undirected edges (u,v). Parallel edges allowed; self-loops ignored.

    Proof hooks:
      - 'contract' events (picked edge + remaining supernodes)
      - 'self_loop' events (when a loop is encountered and ignored)
      - 'result' event (cut size)
    """
    rng = random.Random(seed)
    nodes = sorted({u for e in edges for u in e}, key=str)
    uf = UnionFind.from_nodes(nodes)
    remaining = len(nodes)

    # Keep contracting until 2 supernodes remain
    while remaining > 2:
        u, v = edges[rng.randrange(len(edges))]
        ru, rv = uf.find(u), uf.find(v)
        if ru == rv:
            if trace is not None:
                trace.record("self_loop", u=u, v=v, root=ru)
            continue
        uf.union(ru, rv)
        remaining -= 1
        if trace is not None:
            trace.record("contract", u=u, v=v, remaining=remaining)

    # Count crossing edges
    cut = 0
    for u, v in edges:
        if uf.find(u) != uf.find(v):
            cut += 1

    if trace is not None:
        trace.record("result", cut=cut)
    return cut


def karger_min_cut(
    edges: List[Edge],
    *,
    trials: Optional[int] = None,
    seed: Optional[int] = None,
    trace: Optional[Trace] = None,
) -> int:
    """Karger's min cut with repetition.

    If trials not specified, uses n^2 * log n (rounded up) where n is number of nodes.

    Proof hooks:
      - 'trial' events per run (trial index, cut)
      - 'best' events when best cut improves
    """
    nodes = {u for e in edges for u in e}
    n = len(nodes)
    if n < 2:
        return 0
    if trials is None:
        # Classic repetition schedule (not optimal, but standard & simple).
        import math
        trials = max(1, int(math.ceil(n * n * math.log(max(n, 2), 2))))

    rng = random.Random(seed)
    best = None
    for i in range(trials):
        trial_seed = rng.randrange(2**32)
        cut = karger_min_cut_once(edges, seed=trial_seed)
        if trace is not None:
            trace.record("trial", i=i, cut=cut, seed=trial_seed)
        if best is None or cut < best:
            best = cut
            if trace is not None:
                trace.record("best", i=i, best=cut)
    return int(best)
