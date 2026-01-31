from cs161lab.algorithms.greedy import Interval, interval_scheduling, huffman_codes

def test_interval_scheduling():
    ivs = [
        Interval(0,3,"a"),
        Interval(1,2,"b"),
        Interval(3,4,"c"),
        Interval(2,5,"d"),
    ]
    chosen = interval_scheduling(ivs)
    # optimal is b then c (or b then d? d overlaps c) => 2
    assert len(chosen) == 2
    assert chosen[0].end <= chosen[1].start

def test_huffman_codes_prefix_free():
    codes = huffman_codes({"a":5,"b":2,"c":1})
    # prefix-free: no code is a prefix of another
    vals = list(codes.values())
    for i in range(len(vals)):
        for j in range(len(vals)):
            if i==j: continue
            assert not vals[i].startswith(vals[j])
