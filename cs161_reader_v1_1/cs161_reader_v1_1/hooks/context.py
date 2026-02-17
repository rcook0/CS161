from __future__ import annotations
from contextlib import contextmanager
from typing import Optional
from .event_sink import EventSink

_CURRENT: Optional[EventSink] = None

def current_sink() -> Optional[EventSink]:
    return _CURRENT

@contextmanager
def bind_sink(sink: EventSink):
    global _CURRENT
    prev = _CURRENT
    _CURRENT = sink
    try:
        yield sink
    finally:
        _CURRENT = prev
