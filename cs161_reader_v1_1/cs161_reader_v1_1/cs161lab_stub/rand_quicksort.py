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
    mid = [x for x in a if x == pivot]
    right = [x for x in a if x > pivot]
    if sink: sink.emit("partition", left=len(left), mid=len(mid), right=len(right))
    return _qsort(left) + mid + _qsort(right)

def run_hook(params: Dict[str, Any]) -> None:
    sink = current_sink()
    n = int(params.get("n", 200))
    trials = int(params.get("trials", 20))
    seed = params.get("seed", None)
    if seed is not None:
        random.seed(int(seed))
    total_comp_proxy = 0
    for t in range(trials):
        a = list(range(n))
        random.shuffle(a)
        if sink: sink.emit("trial_start", t=t, n=n)
        out = _qsort(a)
        # proxy: count partition events as "work" (not exact comparisons, but a stable witness)
        if sink: sink.emit("trial_end", t=t, sorted_ok=(out == sorted(a)))
    if sink: sink.emit("note", msg="This stub emits pivot/partition events as witnesses; wire to real impl for true comparison counts.")
