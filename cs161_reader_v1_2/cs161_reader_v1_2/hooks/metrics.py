from __future__ import annotations
from typing import Dict, Any
import json

def summarize_events(events_path: str) -> Dict[str, Any]:
    counts: Dict[str,int] = {}
    n = 0
    with open(events_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            n += 1
            obj = json.loads(line)
            ev = obj.get("event","")
            counts[ev] = counts.get(ev, 0) + 1
    return {"events_total": n, "event_counts": counts}
