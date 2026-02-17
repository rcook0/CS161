from __future__ import annotations
from typing import Dict, Any
import random
from hooks.context import current_sink

class DynArray:
    def __init__(self):
        self.cap=1
        self.n=0
        self.buf=[None]*self.cap
    def append(self,x):
        sink=current_sink()
        if self.n==self.cap:
            old=self.cap
            self.cap*=2
            nb=[None]*self.cap
            copies=0
            for i in range(self.n):
                nb[i]=self.buf[i]
                copies+=1
            self.buf=nb
            if sink: sink.emit("resize", old_cap=old, new_cap=self.cap, copies=copies, n=self.n)
        self.buf[self.n]=x
        self.n+=1
        if sink: sink.emit("append", n=self.n, cap=self.cap)

def run_hook(params: Dict[str, Any]) -> None:
    sink=current_sink()
    appends=int(params.get("appends",2000))
    seed=params.get("seed",None)
    if seed is not None:
        random.seed(int(seed))
    a=DynArray()
    for i in range(appends):
        a.append(i)
    if sink: sink.emit("done", n=a.n, cap=a.cap)
