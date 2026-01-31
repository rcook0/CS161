from cs161lab.algorithms.dp import lis, lcs, KnapsackItem, knapsack_01

def test_lis():
    xs = [10,9,2,5,3,7,101,18]
    seq = lis(xs)
    assert len(seq) == 4
    # must be increasing
    assert all(seq[i] < seq[i+1] for i in range(len(seq)-1))

def test_lcs():
    a = list("ABCBDAB")
    b = list("BDCABA")
    seq = lcs(a, b)
    assert len(seq) == 4  # one of the known optimal lengths

def test_knapsack():
    items = [
        KnapsackItem(weight=3, value=4, label="a"),
        KnapsackItem(weight=4, value=5, label="b"),
        KnapsackItem(weight=2, value=3, label="c"),
    ]
    best, chosen = knapsack_01(7, items)
    assert best == 9  # a+b
    assert {c.label for c in chosen} == {"a","b"}
