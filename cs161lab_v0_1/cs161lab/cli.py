from __future__ import annotations

import argparse
import json
import random
from typing import List, Tuple

from cs161lab.algorithms.sorting import randomized_quicksort, randomized_select
from cs161lab.algorithms.graphs import topological_sort
from cs161lab.algorithms.sssp import dijkstra, bellman_ford
from cs161lab.algorithms.mst import prim_mst
from cs161lab.algorithms.mincut import karger_mincut
from cs161lab.graphs.directed import DiGraph
from cs161lab.graphs.weighted import WeightedDiGraph, WeightedUGraph

def _parse_int_list(s: str) -> List[int]:
    return [int(x) for x in s.split(",") if x.strip()]

def main(argv: List[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="cs161lab", description="Executable CS161 algorithms lab")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp_sort = sub.add_parser("sort", help="Randomized quicksort on a list of ints")
    sp_sort.add_argument("--n", type=int, default=20)
    sp_sort.add_argument("--seed", type=int, default=0)

    sp_sel = sub.add_parser("select", help="Randomized selection (k-th smallest) on a list of ints")
    sp_sel.add_argument("--n", type=int, default=20)
    sp_sel.add_argument("--k", type=int, default=0)
    sp_sel.add_argument("--seed", type=int, default=0)

    sp_topo = sub.add_parser("topo", help="Topological sort of a graph from edge list")
    sp_topo.add_argument("--edges", required=True, help="Edges like '1:2,1:3,3:4' meaning 1->2,1->3,3->4")

    sp_sssp = sub.add_parser("sssp", help="Shortest paths on weighted directed graph")
    sp_sssp.add_argument("--algo", choices=["dijkstra","bellman-ford"], required=True)
    sp_sssp.add_argument("--src", required=True)
    sp_sssp.add_argument("--edges", required=True, help="Edges like 'a:b:1.0,b:c:2.0'")

    sp_mst = sub.add_parser("mst", help="Minimum spanning tree on weighted undirected graph")
    sp_mst.add_argument("--start", default=None)
    sp_mst.add_argument("--edges", required=True, help="Edges like 'a:b:1.0,b:c:2.0' (undirected)")

    sp_cut = sub.add_parser("mincut", help="Karger min-cut on undirected multigraph")
    sp_cut.add_argument("--edges", required=True, help="Edges like 'a-b,b-c,c-a,a-b' (parallel edges allowed)")
    sp_cut.add_argument("--trials", type=int, default=None)
    sp_cut.add_argument("--seed", type=int, default=0)

    args = p.parse_args(argv)

    if args.cmd == "sort":
        rng = random.Random(args.seed)
        xs = [rng.randrange(0, 1000) for _ in range(args.n)]
        out = randomized_quicksort(xs, seed=args.seed)
        print(json.dumps({"in": xs, "out": out}))
        return 0

    if args.cmd == "select":
        rng = random.Random(args.seed)
        xs = [rng.randrange(0, 1000) for _ in range(args.n)]
        val = randomized_select(xs, args.k, seed=args.seed)
        print(json.dumps({"in": xs, "k": args.k, "value": val}))
        return 0

    if args.cmd == "topo":
        g = DiGraph()
        for part in args.edges.split(","):
            u,v = part.split(":")
            g.add_edge(u.strip(), v.strip())
        order = topological_sort(g)
        print(json.dumps({"order": order}))
        return 0

    if args.cmd == "sssp":
        g = WeightedDiGraph()
        for part in args.edges.split(","):
            u,v,w = part.split(":")
            g.add_edge(u.strip(), v.strip(), float(w))
        if args.algo == "dijkstra":
            dist, prev = dijkstra(g, args.src)
        else:
            dist, prev = bellman_ford(g, args.src)
        print(json.dumps({"dist": dist, "prev": prev}))
        return 0

    if args.cmd == "mst":
        g = WeightedUGraph()
        for part in args.edges.split(","):
            u,v,w = part.split(":")
            g.add_edge(u.strip(), v.strip(), float(w))
        edges = prim_mst(g, start=args.start)
        print(json.dumps({"mst": edges}))
        return 0

    if args.cmd == "mincut":
        edges: List[Tuple[str,str]] = []
        for part in args.edges.split(","):
            u,v = part.split("-")
            edges.append((u.strip(), v.strip()))
        cut = karger_mincut(edges, trials=args.trials, seed=args.seed)
        print(json.dumps({"mincut": cut}))
        return 0

    return 2
