from __future__ import annotations
from typing import Dict, Any, Tuple, List
import random
from hooks.context import current_sink

def _random_graph(n: int) -> List[Tuple[int,int]]:
    edges = [(i, i+1) for i in range(n-1)]
    for _ in range(n):
        u = random.randrange(n)
        v = random.randrange(n)
        if u != v:
            edges.append((u,v))
    return edges

def _karger(n: int, edges: List[Tuple[int,int]]) -> int:
    sink = current_sink()
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a,b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    remaining = n
    while remaining > 2:
        u,v = random.choice(edges)
        ru, rv = find(u), find(v)
        if ru == rv:
            if sink: sink.emit("self_loop")
            continue
        if sink: sink.emit("contract", remaining=remaining)
        union(ru, rv)
        remaining -= 1

    cut = 0
    for u,v in edges:
        if find(u) != find(v):
            cut += 1
    return cut

def run_hook(params: Dict[str, Any]) -> None:
    sink = current_sink()
    n = int(params.get("n", 25))
    trials = int(params.get("trials", 30))
    seed = params.get("seed", None)
    if seed is not None:
        random.seed(int(seed))
    edges = _random_graph(n)
    best = None
    for t in range(trials):
        c = _karger(n, edges)
        if sink: sink.emit("trial", t=t, cut=c)
        best = c if best is None else min(best, c)
    if sink: sink.emit("best", best=best)
