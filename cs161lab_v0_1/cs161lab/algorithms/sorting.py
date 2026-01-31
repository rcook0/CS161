from __future__ import annotations
from typing import List, TypeVar, Callable, Optional
import random

T = TypeVar("T")

def randomized_quicksort(a: List[T], *, key: Optional[Callable[[T], object]] = None, seed: Optional[int] = None) -> List[T]:
    """Return a new sorted list using randomized quicksort (3-way partition).

    Designed for clarity and stable expected performance; not stable sort.
    """
    rng = random.Random(seed)
    key = key or (lambda x: x)

    def _q(xs: List[T]) -> List[T]:
        if len(xs) <= 1:
            return xs
        pivot = xs[rng.randrange(len(xs))]
        kp = key(pivot)
        lt, eq, gt = [], [], []
        for x in xs:
            kx = key(x)
            if kx < kp:
                lt.append(x)
            elif kx > kp:
                gt.append(x)
            else:
                eq.append(x)
        return _q(lt) + eq + _q(gt)

    return _q(list(a))

def randomized_select(a: List[T], k: int, *, key: Optional[Callable[[T], object]] = None, seed: Optional[int] = None) -> T:
    """Select the k-th smallest element (0-indexed) in expected linear time."""
    if k < 0 or k >= len(a):
        raise IndexError("k out of range")
    rng = random.Random(seed)
    key = key or (lambda x: x)
    xs = list(a)

    while True:
        pivot = xs[rng.randrange(len(xs))]
        kp = key(pivot)
        lt, eq, gt = [], [], []
        for x in xs:
            kx = key(x)
            if kx < kp:
                lt.append(x)
            elif kx > kp:
                gt.append(x)
            else:
                eq.append(x)
        if k < len(lt):
            xs = lt
        elif k < len(lt) + len(eq):
            return eq[0]
        else:
            k = k - len(lt) - len(eq)
            xs = gt
