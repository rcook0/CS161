import random
from cs161lab.algorithms.sorting import randomized_quicksort, randomized_select

def test_quicksort_matches_builtin():
    rng = random.Random(0)
    xs = [rng.randrange(0, 1000) for _ in range(200)]
    assert randomized_quicksort(xs, seed=1) == sorted(xs)

def test_select_kth():
    rng = random.Random(0)
    xs = [rng.randrange(0, 1000) for _ in range(101)]
    for k in [0, 1, 50, 100]:
        assert randomized_select(xs, k, seed=2) == sorted(xs)[k]
