# cs161lab

An executable companion for CS161-style algorithms (e.g., Plotkin F10): clean reference implementations, a proof-pattern index, and structured **proof hooks** via a lightweight tracing API.

## What you get

- **Algorithms**
  - Randomized quicksort + randomized selection
  - Topological sort (cycle-detecting)
  - Dijkstra + Bellman–Ford (negative-cycle detection)
  - Prim MST (returns MSF if disconnected)
  - Karger min-cut with repetition schedule
  - DP exemplars: LIS, LCS, 0/1 knapsack (with reconstruction)
  - Greedy exemplars: interval scheduling, Huffman coding
  - Amortized exemplars: dynamic array resizing, union–find (rank + path compression)

- **Proof-pattern index**: `PROOF_PATTERNS.md`
- **Tracing (“proof hooks”)**: pass `Trace()` to algorithms to record decisions, invariants, and progress.

## Install

```bash
python -m pip install -e .
```

## CLI examples

```bash
cs161lab sort --ints 3,1,2 --seed 0
cs161lab select --ints 9,1,7,3 --k 2 --seed 0
cs161lab topo --edges "1:2,1:3,3:4"
cs161lab sssp --algo dijkstra --src s --edges "s:a:1,a:b:2,s:b:10"
cs161lab mst --edges "a:b:1,b:c:2,a:c:5"
cs161lab mincut --edges "a-b,b-c,c-a,a-b" --seed 0
cs161lab lis --ints 10,9,2,5,3,7,101,18
cs161lab lcs --a "ABCBDAB" --b "BDCABA"
cs161lab knapsack --capacity 7 --items "3:4:a,4:5:b,2:3:c"
cs161lab intervals --intervals "0:3:a,1:2:b,3:4:c"
cs161lab huffman --freq "a:5,b:2,c:1"
```

Add `--trace` to emit a JSON trace of proof-hook events.
