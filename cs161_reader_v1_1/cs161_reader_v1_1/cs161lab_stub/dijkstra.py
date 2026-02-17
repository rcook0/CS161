from __future__ import annotations
from typing import Dict, Any, List, Tuple
import random, heapq
from hooks.context import current_sink

def _rand_weighted_digraph(n: int, m: int) -> List[List[Tuple[int,int]]]:
    adj = [[] for _ in range(n)]
    for _ in range(m):
        u = random.randrange(n)
        v = random.randrange(n)
        if u == v: continue
        w = random.randrange(1, 20)  # nonnegative
        adj[u].append((v,w))
    return adj

def run_hook(params: Dict[str, Any]) -> None:
    sink = current_sink()
    n = int(params.get("n", 40))
    m = int(params.get("m", 120))
    seed = params.get("seed", None)
    if seed is not None:
        random.seed(int(seed))
    adj = _rand_weighted_digraph(n,m)
    s = 0
    INF = 10**18
    d = [INF]*n
    d[s]=0
    pq = [(0,s)]
    seen = [False]*n
    while pq:
        dist,u = heapq.heappop(pq)
        if seen[u]: 
            continue
        seen[u]=True
        if sink: sink.emit("finalize", u=u, d=dist)
        for v,w in adj[u]:
            nd = dist + w
            if nd < d[v]:
                old = d[v]
                d[v]=nd
                if sink: sink.emit("relax", u=u, v=v, old=old, new=nd, w=w)
                heapq.heappush(pq,(nd,v))
