from cs161lab.trace import Trace
from cs161lab.algorithms.amortized import DynamicArray, UnionFind

def test_dynamic_array_resizes():
    tr = Trace()
    da = DynamicArray[int](initial_capacity=1, trace=tr)
    for i in range(8):
        da.append(i)
    assert da.size == 8
    assert da.capacity >= 8
    # should have at least one resize event
    assert any(e.name == "resize" for e in tr.events)

def test_union_find_basic():
    tr = Trace()
    uf = UnionFind.make(5, trace=tr)
    uf.union(0,1)
    uf.union(1,2)
    assert uf.find(0) == uf.find(2)
    assert any(e.name == "find" for e in tr.events)
