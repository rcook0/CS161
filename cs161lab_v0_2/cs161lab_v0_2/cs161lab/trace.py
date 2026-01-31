from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TraceEvent:
    """A lightweight, structured event emitted by an algorithm.

    Purpose: provide 'proof hooks' (invariants, decisions, counts) without
    changing algorithm semantics.
    """
    name: str
    data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Trace:
    """Collects TraceEvents. Pass a Trace into algorithms to record proof hooks."""
    events: List[TraceEvent] = field(default_factory=list)

    def record(self, name: str, **data: Any) -> None:
        self.events.append(TraceEvent(name=name, data=data))

    def last(self, name: Optional[str] = None) -> Optional[TraceEvent]:
        if not self.events:
            return None
        if name is None:
            return self.events[-1]
        for e in reversed(self.events):
            if e.name == name:
                return e
        return None
