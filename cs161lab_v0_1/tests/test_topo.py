from cs161lab.graphs.directed import DiGraph
from cs161lab.algorithms.graphs import topological_sort

def test_topo_simple_dag():
    g = DiGraph.from_edges([(1,2),(1,3),(3,4)])
    order = topological_sort(g)
    pos = {v:i for i,v in enumerate(order)}
    assert pos[1] < pos[2]
    assert pos[1] < pos[3]
    assert pos[3] < pos[4]
