from __future__ import annotations

import statistics
import time
from dataclasses import dataclass
from typing import Callable, Iterable, Any, Dict, List, Optional, Tuple

@dataclass
class BenchmarkResult:
    n: int
    trials: int
    times: List[float]

    @property
    def mean(self) -> float:
        return statistics.mean(self.times)

    @property
    def median(self) -> float:
        return statistics.median(self.times)

    @property
    def stdev(self) -> float:
        return statistics.pstdev(self.times) if len(self.times) > 1 else 0.0

def benchmark(
    fn: Callable[..., Any],
    generator: Callable[[int], Any],
    sizes: Iterable[int],
    trials: int = 10,
    warmup: bool = True,
    fn_args: Optional[Tuple[Any, ...]] = None,
    fn_kwargs: Optional[Dict[str, Any]] = None,
) -> List[BenchmarkResult]:
    """Benchmark `fn` over a set of input sizes.

    - Uses `time.perf_counter()` for wall-clock timing.
    - `generator(n)` should return a fresh input for size n.
    - Inputs are *not* reused between trials to avoid mutation artifacts.
    """
    fn_args = fn_args or ()
    fn_kwargs = fn_kwargs or {}
    results: List[BenchmarkResult] = []

    if warmup:
        x = generator(next(iter(sizes)))
        fn(x, *fn_args, **fn_kwargs)

    for n in sizes:
        times: List[float] = []
        for _ in range(trials):
            x = generator(n)
            t0 = time.perf_counter()
            fn(x, *fn_args, **fn_kwargs)
            t1 = time.perf_counter()
            times.append(t1 - t0)
        results.append(BenchmarkResult(n=n, trials=trials, times=times))
    return results
