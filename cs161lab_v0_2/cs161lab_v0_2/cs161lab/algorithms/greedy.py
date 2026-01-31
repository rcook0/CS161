from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple
import heapq

from cs161lab.trace import Trace


@dataclass(frozen=True)
class Interval:
    start: float
    end: float
    label: str = ""


def interval_scheduling(
    intervals: Sequence[Interval],
    *,
    trace: Optional[Trace] = None,
) -> List[Interval]:
    """Select a maximum-cardinality set of non-overlapping intervals.

    Greedy algorithm: sort by earliest finishing time.

    Proof hooks:
      - 'sorted' with order of end times
      - 'accept' / 'reject' decisions
    """
    xs = sorted(intervals, key=lambda it: (it.end, it.start))
    if trace is not None:
        trace.record("sorted", ends=[it.end for it in xs], problem="interval_scheduling")

    chosen: List[Interval] = []
    current_end = float("-inf")

    for it in xs:
        if it.start >= current_end:
            chosen.append(it)
            old_end = current_end
            current_end = it.end
            if trace is not None:
                trace.record("accept", label=it.label, start=it.start, end=it.end, prev_end=old_end)
        else:
            if trace is not None:
                trace.record("reject", label=it.label, start=it.start, end=it.end, current_end=current_end)

    return chosen


@dataclass
class HuffmanNode:
    weight: int
    symbol: Optional[str] = None
    left: Optional["HuffmanNode"] = None
    right: Optional["HuffmanNode"] = None


def huffman_codes(
    frequencies: Dict[str, int],
    *,
    trace: Optional[Trace] = None,
) -> Dict[str, str]:
    """Build Huffman codes for given symbol frequencies.

    Returns dict {symbol: bitstring}.

    Proof hooks:
      - 'merge' for each heap merge (two smallest weights)
      - 'code' for final assigned codes
    """
    if not frequencies:
        return {}

    # heap items: (weight, unique_id, node)
    heap: List[Tuple[int, int, HuffmanNode]] = []
    uid = 0
    for sym, w in frequencies.items():
        heapq.heappush(heap, (int(w), uid, HuffmanNode(weight=int(w), symbol=sym)))
        uid += 1

    if trace is not None:
        trace.record("init_heap", k=len(heap), problem="huffman")

    while len(heap) > 1:
        w1, _, n1 = heapq.heappop(heap)
        w2, _, n2 = heapq.heappop(heap)
        merged = HuffmanNode(weight=w1 + w2, left=n1, right=n2)
        heapq.heappush(heap, (merged.weight, uid, merged))
        if trace is not None:
            trace.record("merge", w1=w1, w2=w2, merged=merged.weight)
        uid += 1

    root = heap[0][2]
    codes: Dict[str, str] = {}

    def dfs(node: HuffmanNode, prefix: str) -> None:
        if node.symbol is not None:
            codes[node.symbol] = prefix or "0"  # handle single-symbol case
            return
        assert node.left is not None and node.right is not None
        dfs(node.left, prefix + "0")
        dfs(node.right, prefix + "1")

    dfs(root, "")

    if trace is not None:
        for s, c in codes.items():
            trace.record("code", symbol=s, code=c)

    return codes
