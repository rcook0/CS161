from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Hashable, List, Tuple, Optional
import random
import math

Node = Hashable
Edge = Tuple[Node, Node]

def karger_mincut_trial(edges: List[Edge], seed: Optional[int] = None) -> int:
    """Single Karger contraction trial on an undirected multigraph.

    Input: list of undirected edges (u,v). Parallel edges are allowed.
    Returns: cut size found by the trial.
    """
    rng = random.Random(seed)

    # Union-Find
    parent: Dict[Node, Node] = {}
    rank: Dict[Node, int] = {}

    def find(x: Node) -> Node:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: Node, b: Node) -> None:
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if rank[ra] < rank[rb]:
            parent[ra] = rb
        elif rank[ra] > rank[rb]:
            parent[rb] = ra
        else:
            parent[rb] = ra
            rank[ra] += 1

    # init sets
    nodes = set()
    for u,v in edges:
        nodes.add(u); nodes.add(v)
    for u in nodes:
        parent[u] = u
        rank[u] = 0

    # contraction: keep merging random edges until 2 supernodes
    num_sets = len(nodes)

    # To avoid expensive edge filtering, we sample edges until we hit a crossing edge.
    while num_sets > 2:
        u,v = edges[rng.randrange(len(edges))]
        ru, rv = find(u), find(v)
        if ru == rv:
            continue
        union(ru, rv)
        num_sets -= 1

    # count crossing edges
    cut = 0
    for u,v in edges:
        if find(u) != find(v):
            cut += 1
    return cut

def karger_mincut(edges: List[Edge], trials: Optional[int] = None, seed: Optional[int] = None) -> int:
    """Run repeated Karger trials; return the minimum cut size observed.

    Default trials: n^2 * log n (common heuristic). For small graphs, this is adequate.
    """
    nodes = set()
    for u,v in edges:
        nodes.add(u); nodes.add(v)
    n = max(2, len(nodes))
    if trials is None:
        trials = int(n * n * math.log(n, 2) + 1)

    rng = random.Random(seed)
    best = math.inf
    for _ in range(trials):
        s = rng.randrange(1<<30)
        best = min(best, karger_mincut_trial(edges, seed=s))
    return int(best)
