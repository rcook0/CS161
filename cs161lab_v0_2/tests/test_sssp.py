from cs161lab.algorithms.sssp import WeightedDigraph, dijkstra, bellman_ford

def test_dijkstra_basic():
    g = WeightedDigraph.from_edges([
        ("s","a",1),
        ("a","b",2),
        ("s","b",10),
    ])
    dist = dijkstra(g, "s")
    assert dist["b"] == 3.0

def test_bellman_ford_negative_edge_no_cycle():
    g = WeightedDigraph.from_edges([
        ("s","a",1),
        ("a","b",-2),
        ("s","b",10),
    ])
    dist, neg = bellman_ford(g, "s")
    assert neg is False
    assert dist["b"] == -1.0

def test_bellman_ford_detects_neg_cycle():
    g = WeightedDigraph.from_edges([
        ("s","a",1),
        ("a","b",-2),
        ("b","a",-2),
    ])
    dist, neg = bellman_ford(g, "s")
    assert neg is True
