import pytest
from cs161lab.graphs.weighted import WeightedDiGraph
from cs161lab.algorithms.sssp import dijkstra, bellman_ford

def test_dijkstra_basic():
    g = WeightedDiGraph.from_edges([
        ("s","a",1),
        ("a","b",2),
        ("s","b",10),
    ])
    dist, prev = dijkstra(g, "s")
    assert dist["b"] == 3.0
    assert prev["b"] == "a"

def test_bellman_ford_negative_edge():
    g = WeightedDiGraph.from_edges([
        ("s","a",1),
        ("a","b",-2),
        ("s","b",10),
    ])
    dist, prev = bellman_ford(g, "s")
    assert dist["b"] == -1.0

def test_bellman_ford_negative_cycle_detect():
    g = WeightedDiGraph.from_edges([
        ("s","a",1),
        ("a","b",-2),
        ("b","a",-2),
    ])
    with pytest.raises(ValueError):
        bellman_ford(g, "s")
