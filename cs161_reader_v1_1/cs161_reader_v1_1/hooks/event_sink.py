from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Optional, Iterable
import json, os, datetime, uuid

def iso_now() -> str:
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()

@dataclass
class EventSink:
    out_path: str
    hook_id: str
    theorem_id: str
    run_id: str
    seed: Optional[int] = None

    def emit(self, event: str, **data: Any) -> None:
        rec = {
            "t": iso_now(),
            "run_id": self.run_id,
            "hook_id": self.hook_id,
            "theorem_id": self.theorem_id,
            "event": event,
            "data": data,
            "seed": self.seed,
        }
        with open(self.out_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, sort_keys=True) + "\n")

def new_run_id() -> str:
    return uuid.uuid4().hex
