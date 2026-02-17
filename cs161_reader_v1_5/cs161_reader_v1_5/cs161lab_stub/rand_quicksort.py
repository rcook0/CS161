from __future__ import annotations
from typing import List, Dict, Any
import random
from hooks.context import current_sink

def _qsort(a: List[int]) -> List[int]:
    sink = current_sink()
    if len(a) <= 1:
        return a
    pivot = random.choice(a)
    if sink: sink.emit("pivot", pivot=pivot, n=len(a))
    left = [x for x in a if x < pivot]
    right = [x for x in a if x > pivot]
    if sink: sink.emit("partition", left=len(left), right=len(right))
    return _qsort(left) + [pivot] + _qsort(right)

def run_hook(params: Dict[str, Any]) -> None:
    sink = current_sink()
    n = int(params.get("n", 200))
    trials = int(params.get("trials", 10))
    seed = params.get("seed", None)
    if seed is not None:
        random.seed(int(seed))
    for t in range(trials):
        a = list(range(n))
        random.shuffle(a)
        if sink: sink.emit("trial_start", t=t)
        out = _qsort(a)
        if sink: sink.emit("trial_end", t=t, ok=(out == sorted(a)))
