from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Sequence, Tuple, TypeVar

from cs161lab.trace import Trace

T = TypeVar("T")


def lis(sequence: Sequence[T], *, trace: Optional[Trace] = None) -> List[T]:
    """Longest Increasing Subsequence (LIS) via O(n^2) DP with reconstruction.

    Returns one LIS (not necessarily unique).

    Proof hooks:
      - 'dp_init' with n
      - 'dp_update' when OPT[i] increases via predecessor j
      - 'reconstruct' with chosen indices
    """
    a = list(sequence)
    n = len(a)
    if trace is not None:
        trace.record("dp_init", n=n, problem="lis")
    if n == 0:
        return []

    # OPT[i] = length of LIS ending at i
    opt = [1] * n
    prev = [-1] * n

    for i in range(n):
        for j in range(i):
            if a[j] < a[i] and opt[j] + 1 > opt[i]:
                opt[i] = opt[j] + 1
                prev[i] = j
                if trace is not None:
                    trace.record("dp_update", i=i, j=j, opt_i=opt[i])

    # find best end
    end = max(range(n), key=lambda i: opt[i])
    idxs = []
    while end != -1:
        idxs.append(end)
        end = prev[end]
    idxs.reverse()

    if trace is not None:
        trace.record("reconstruct", indices=idxs, length=len(idxs))

    return [a[i] for i in idxs]


def lcs(a: Sequence[T], b: Sequence[T], *, trace: Optional[Trace] = None) -> List[T]:
    """Longest Common Subsequence (LCS) via DP with reconstruction.

    Returns one LCS (not necessarily unique).

    Proof hooks:
      - 'dp_init' with dimensions
      - 'dp_cell' optional sparse sampling (disabled by default)
      - 'reconstruct' with length
    """
    x = list(a)
    y = list(b)
    n, m = len(x), len(y)
    if trace is not None:
        trace.record("dp_init", n=n, m=m, problem="lcs")

    # dp[i][j] = LCS length of x[:i] and y[:j]
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        xi = x[i - 1]
        row = dp[i]
        prev_row = dp[i - 1]
        for j in range(1, m + 1):
            if xi == y[j - 1]:
                row[j] = prev_row[j - 1] + 1
            else:
                row[j] = row[j - 1] if row[j - 1] >= prev_row[j] else prev_row[j]

    # reconstruction
    i, j = n, m
    out: List[T] = []
    while i > 0 and j > 0:
        if x[i - 1] == y[j - 1]:
            out.append(x[i - 1])
            i -= 1
            j -= 1
        else:
            if dp[i][j - 1] >= dp[i - 1][j]:
                j -= 1
            else:
                i -= 1
    out.reverse()

    if trace is not None:
        trace.record("reconstruct", length=len(out), problem="lcs")

    return out


@dataclass(frozen=True)
class KnapsackItem:
    weight: int
    value: int
    label: str = ""


def knapsack_01(
    capacity: int,
    items: Sequence[KnapsackItem],
    *,
    trace: Optional[Trace] = None,
) -> Tuple[int, List[KnapsackItem]]:
    """0/1 Knapsack DP with reconstruction.

    Returns (max_value, chosen_items).

    Proof hooks:
      - 'dp_init' with n and capacity
      - 'dp_row' per item (optional summary)
      - 'reconstruct' with chosen labels
    """
    if capacity < 0:
        raise ValueError("capacity must be nonnegative")
    it = list(items)
    n = len(it)
    if trace is not None:
        trace.record("dp_init", n=n, capacity=capacity, problem="knapsack_01")

    # dp[i][w] = best value using first i items with capacity w
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        wi = it[i - 1].weight
        vi = it[i - 1].value
        for w in range(capacity + 1):
            best = dp[i - 1][w]
            if wi <= w:
                cand = dp[i - 1][w - wi] + vi
                if cand > best:
                    best = cand
            dp[i][w] = best
        if trace is not None:
            trace.record("dp_row", i=i, item=it[i - 1].label or str(i), best=dp[i][capacity])

    # reconstruction
    w = capacity
    chosen: List[KnapsackItem] = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            item = it[i - 1]
            chosen.append(item)
            w -= item.weight
    chosen.reverse()

    if trace is not None:
        trace.record("reconstruct", chosen=[c.label or "?" for c in chosen], total_value=dp[n][capacity])

    return dp[n][capacity], chosen
