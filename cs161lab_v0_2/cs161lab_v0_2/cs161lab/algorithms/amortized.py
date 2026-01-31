from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar

from cs161lab.trace import Trace

T = TypeVar("T")


class DynamicArray(Generic[T]):
    """A tiny dynamic array to illustrate amortized analysis.

    This is not intended to replace Python lists; it's an educational artifact.

    Proof hooks:
      - 'resize' when capacity grows/shrinks
      - 'append' / 'pop' with size/capacity snapshots
    """

    def __init__(self, *, initial_capacity: int = 1, trace: Optional[Trace] = None):
        if initial_capacity < 1:
            raise ValueError("initial_capacity must be >= 1")
        self._cap = int(initial_capacity)
        self._n = 0
        self._a: List[Optional[T]] = [None] * self._cap
        self._trace = trace

    @property
    def size(self) -> int:
        return self._n

    @property
    def capacity(self) -> int:
        return self._cap

    def _resize(self, new_cap: int) -> None:
        old_cap = self._cap
        b: List[Optional[T]] = [None] * new_cap
        for i in range(self._n):
            b[i] = self._a[i]
        self._a = b
        self._cap = new_cap
        if self._trace is not None:
            self._trace.record("resize", old_cap=old_cap, new_cap=new_cap, size=self._n)

    def append(self, x: T) -> None:
        if self._n == self._cap:
            self._resize(self._cap * 2)
        self._a[self._n] = x
        self._n += 1
        if self._trace is not None:
            self._trace.record("append", size=self._n, capacity=self._cap)

    def pop(self) -> T:
        if self._n == 0:
            raise IndexError("pop from empty DynamicArray")
        self._n -= 1
        x = self._a[self._n]
        self._a[self._n] = None
        # Optional shrink rule: halve when quarter-full (classic).
        if self._cap > 1 and self._n <= self._cap // 4:
            self._resize(max(1, self._cap // 2))
        if self._trace is not None:
            self._trace.record("pop", size=self._n, capacity=self._cap)
        assert x is not None
        return x


@dataclass
class UnionFind:
    """Union-Find (Disjoint Set Union) with union by rank + path compression.

    Proof hooks:
      - 'find' with compression steps
      - 'union' decisions and rank changes
    """
    parent: List[int]
    rank: List[int]
    trace: Optional[Trace] = None

    @classmethod
    def make(cls, n: int, *, trace: Optional[Trace] = None) -> "UnionFind":
        if n < 0:
            raise ValueError("n must be nonnegative")
        return cls(parent=list(range(n)), rank=[0] * n, trace=trace)

    def find(self, x: int) -> int:
        if x < 0 or x >= len(self.parent):
            raise IndexError("x out of range")
        # Iterative compression with event counts
        steps = 0
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
            steps += 1

        # compress
        y = x
        compress = 0
        while self.parent[y] != y:
            nxt = self.parent[y]
            self.parent[y] = root
            y = nxt
            compress += 1

        if self.trace is not None:
            self.trace.record("find", x=x, root=root, steps=steps, compress=compress)
        return root

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            if self.trace is not None:
                self.trace.record("union", a=a, b=b, merged=False, reason="same_set")
            return False

        # union by rank
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        rank_inc = False
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
            rank_inc = True

        if self.trace is not None:
            self.trace.record("union", a=a, b=b, merged=True, root=ra, child=rb, rank_inc=rank_inc)
        return True
