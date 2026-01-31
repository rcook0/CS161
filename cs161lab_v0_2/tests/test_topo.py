import pytest
from cs161lab.algorithms.graphs import DirectedGraph, topo_sort

def test_topo_order():
    g = DirectedGraph.from_edges([
        ("a","b"),
        ("a","c"),
        ("c","d"),
    ])
    order = topo_sort(g)
    pos = {u:i for i,u in enumerate(order)}
    assert pos["a"] < pos["b"]
    assert pos["a"] < pos["c"]
    assert pos["c"] < pos["d"]

def test_topo_cycle_raises():
    g = DirectedGraph.from_edges([
        ("a","b"),
        ("b","a"),
    ])
    with pytest.raises(ValueError):
        topo_sort(g)
