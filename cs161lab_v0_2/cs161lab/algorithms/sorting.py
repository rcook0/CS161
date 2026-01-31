from __future__ import annotations

from typing import Callable, List, Optional, TypeVar
import random

from cs161lab.trace import Trace

T = TypeVar("T")


def randomized_quicksort(
    a: List[T],
    *,
    key: Optional[Callable[[T], object]] = None,
    seed: Optional[int] = None,
    trace: Optional[Trace] = None,
) -> List[T]:
    """Return a new sorted list using randomized quicksort (3-way partition).

    Proof hooks:
      - emits 'pivot' events (pivot value + subproblem size)
      - emits 'partition' events (sizes of lt/eq/gt)
      - emits 'base' events for subproblems of size 0/1
    """
    rng = random.Random(seed)
    key = key or (lambda x: x)

    def _q(xs: List[T]) -> List[T]:
        n = len(xs)
        if n <= 1:
            if trace is not None:
                trace.record("base", n=n)
            return xs
        pivot = xs[rng.randrange(n)]
        if trace is not None:
            trace.record("pivot", n=n, pivot=pivot)
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
        if trace is not None:
            trace.record("partition", n=n, lt=len(lt), eq=len(eq), gt=len(gt))
        return _q(lt) + eq + _q(gt)

    return _q(list(a))


def randomized_select(
    a: List[T],
    k: int,
    *,
    key: Optional[Callable[[T], object]] = None,
    seed: Optional[int] = None,
    trace: Optional[Trace] = None,
) -> T:
    """Select the k-th smallest element (0-indexed) in expected linear time.

    Proof hooks:
      - emits 'pivot' and 'partition' events per iteration
      - emits 'shrink' event describing which side is kept
    """
    if k < 0 or k >= len(a):
        raise IndexError("k out of range")
    rng = random.Random(seed)
    key = key or (lambda x: x)
    xs = list(a)

    while True:
        n = len(xs)
        pivot = xs[rng.randrange(n)]
        if trace is not None:
            trace.record("pivot", n=n, pivot=pivot, k=k)
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
        if trace is not None:
            trace.record("partition", n=n, lt=len(lt), eq=len(eq), gt=len(gt), k=k)
        if k < len(lt):
            xs = lt
            if trace is not None:
                trace.record("shrink", side="lt", new_n=len(xs), k=k)
        elif k < len(lt) + len(eq):
            if trace is not None:
                trace.record("found", pivot=pivot, k=k)
            return eq[0]
        else:
            k = k - len(lt) - len(eq)
            xs = gt
            if trace is not None:
                trace.record("shrink", side="gt", new_n=len(xs), k=k)
