from __future__ import annotations

import argparse
import json
from typing import Dict, List, Tuple

from cs161lab.trace import Trace
from cs161lab.algorithms.sorting import randomized_quicksort, randomized_select
from cs161lab.algorithms.graphs import DirectedGraph, topo_sort
from cs161lab.algorithms.sssp import WeightedDigraph, dijkstra, bellman_ford
from cs161lab.algorithms.mst import WeightedUndirected, prim_mst
from cs161lab.algorithms.mincut import karger_min_cut
from cs161lab.algorithms.dp import KnapsackItem, lis, lcs, knapsack_01
from cs161lab.algorithms.greedy import Interval, interval_scheduling, huffman_codes
from cs161lab.algorithms.amortized import DynamicArray, UnionFind


def _parse_csv(s: str) -> List[str]:
    if not s.strip():
        return []
    return [p.strip() for p in s.split(",") if p.strip()]


def _parse_edges_uv(s: str, sep: str = ":") -> List[Tuple[str, str]]:
    edges: List[Tuple[str, str]] = []
    for part in _parse_csv(s):
        u, v = part.split(sep)
        edges.append((u.strip(), v.strip()))
    return edges


def _parse_edges_uvw(s: str) -> List[Tuple[str, str, float]]:
    edges: List[Tuple[str, str, float]] = []
    for part in _parse_csv(s):
        u, v, w = part.split(":")
        edges.append((u.strip(), v.strip(), float(w)))
    return edges


def main(argv: List[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="cs161lab", description="Executable CS161 algorithms lab")
    p.add_argument("--trace", action="store_true", help="Emit proof-hook trace events in JSON output.")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("sort")
    sp.add_argument("--ints", required=True, help="Comma-separated integers, e.g. 3,1,2")
    sp.add_argument("--seed", type=int, default=None)

    sp = sub.add_parser("select")
    sp.add_argument("--ints", required=True)
    sp.add_argument("--k", type=int, required=True)
    sp.add_argument("--seed", type=int, default=None)

    sp = sub.add_parser("topo")
    sp.add_argument("--edges", required=True, help="Edges u:v,u:v,...")
    sp = sub.add_parser("sssp")
    sp.add_argument("--algo", choices=["dijkstra", "bellman_ford"], required=True)
    sp.add_argument("--src", required=True)
    sp.add_argument("--edges", required=True, help="Edges u:v:w,u:v:w,...")

    sp = sub.add_parser("mst")
    sp.add_argument("--edges", required=True, help="Undirected edges u:v:w,u:v:w,...")

    sp = sub.add_parser("mincut")
    sp.add_argument("--edges", required=True, help="Undirected edges u-v,u-v,... (parallel edges allowed)")
    sp.add_argument("--trials", type=int, default=None)
    sp.add_argument("--seed", type=int, default=None)

    sp = sub.add_parser("lis")
    sp.add_argument("--ints", required=True)

    sp = sub.add_parser("lcs")
    sp.add_argument("--a", required=True, help="String or comma-separated tokens")
    sp.add_argument("--b", required=True)

    sp = sub.add_parser("knapsack")
    sp.add_argument("--capacity", type=int, required=True)
    sp.add_argument("--items", required=True, help="Items w:v:label,w:v:label,... label optional")

    sp = sub.add_parser("intervals")
    sp.add_argument("--intervals", required=True, help="Intervals start:end:label,start:end:label,...")

    sp = sub.add_parser("huffman")
    sp.add_argument("--freq", required=True, help="Frequencies sym:count,sym:count,...")

    sp = sub.add_parser("dynarray_demo")
    sp.add_argument("--n", type=int, default=32, help="Number of appends then pops (half).")

    sp = sub.add_parser("unionfind_demo")
    sp.add_argument("--n", type=int, required=True)
    sp.add_argument("--unions", required=True, help="Pairs a:b,a:b,...")
    sp.add_argument("--finds", default="", help="Queries x,x,...")

    args = p.parse_args(argv)
    trace = Trace() if args.trace else None

    def out(payload: Dict) -> int:
        if trace is not None:
            payload["trace"] = [{"name": e.name, "data": e.data} for e in trace.events]
        print(json.dumps(payload))
        return 0

    if args.cmd == "sort":
        ints = [int(x) for x in _parse_csv(args.ints)]
        res = randomized_quicksort(ints, seed=args.seed, trace=trace)
        return out({"sorted": res})

    if args.cmd == "select":
        ints = [int(x) for x in _parse_csv(args.ints)]
        res = randomized_select(ints, args.k, seed=args.seed, trace=trace)
        return out({"selected": res})

    if args.cmd == "topo":
        edges = _parse_edges_uv(args.edges)
        g = DirectedGraph.from_edges(edges)
        order = topo_sort(g, trace=trace)
        return out({"order": order})

    if args.cmd == "sssp":
        edges = _parse_edges_uvw(args.edges)
        g = WeightedDigraph.from_edges(edges)
        if args.algo == "dijkstra":
            dist = dijkstra(g, args.src, trace=trace)
            return out({"dist": dist})
        dist, neg = bellman_ford(g, args.src, trace=trace)
        return out({"dist": dist, "neg_cycle": neg})

    if args.cmd == "mst":
        edges = _parse_edges_uvw(args.edges)
        g = WeightedUndirected.from_edges(edges)
        forest = prim_mst(g, trace=trace)
        return out({"msf": forest})

    if args.cmd == "mincut":
        edges: List[Tuple[str, str]] = []
        for part in _parse_csv(args.edges):
            u, v = part.split("-")
            edges.append((u.strip(), v.strip()))
        cut = karger_min_cut(edges, trials=args.trials, seed=args.seed, trace=trace)
        return out({"mincut": cut})

    if args.cmd == "lis":
        ints = [int(x) for x in _parse_csv(args.ints)]
        seq = lis(ints, trace=trace)
        return out({"lis": seq, "length": len(seq)})

    if args.cmd == "lcs":
        def parse_seq(x: str) -> List[str]:
            return _parse_csv(x) if "," in x else list(x)
        a = parse_seq(args.a)
        b = parse_seq(args.b)
        seq = lcs(a, b, trace=trace)
        return out({"lcs": seq, "length": len(seq)})

    if args.cmd == "knapsack":
        items: List[KnapsackItem] = []
        for part in _parse_csv(args.items):
            comps = part.split(":")
            if len(comps) < 2:
                raise SystemExit("item must be w:v:label (label optional)")
            w = int(comps[0]); v = int(comps[1])
            label = comps[2] if len(comps) >= 3 else ""
            items.append(KnapsackItem(weight=w, value=v, label=label))
        best, chosen = knapsack_01(args.capacity, items, trace=trace)
        return out({"best_value": best, "chosen": [c.label for c in chosen]})

    if args.cmd == "intervals":
        ivs: List[Interval] = []
        for part in _parse_csv(args.intervals):
            comps = part.split(":")
            if len(comps) < 2:
                raise SystemExit("interval must be start:end:label (label optional)")
            s = float(comps[0]); e = float(comps[1])
            label = comps[2] if len(comps) >= 3 else ""
            ivs.append(Interval(start=s, end=e, label=label))
        chosen = interval_scheduling(ivs, trace=trace)
        return out({"chosen": [{"start": i.start, "end": i.end, "label": i.label} for i in chosen]})

    if args.cmd == "huffman":
        freq: Dict[str, int] = {}
        for part in _parse_csv(args.freq):
            sym, c = part.split(":")
            freq[sym] = int(c)
        codes = huffman_codes(freq, trace=trace)
        return out({"codes": codes})

    if args.cmd == "dynarray_demo":
        da = DynamicArray[int](initial_capacity=1, trace=trace)
        for i in range(args.n):
            da.append(i)
        for _ in range(args.n // 2):
            da.pop()
        return out({"size": da.size, "capacity": da.capacity})

    if args.cmd == "unionfind_demo":
        uf = UnionFind.make(args.n, trace=trace)
        for a, b in _parse_edges_uv(args.unions, sep=":"):
            uf.union(int(a), int(b))
        roots = [uf.find(int(x)) for x in _parse_csv(args.finds)] if args.finds else []
        return out({"roots": roots})

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
