#!/usr/bin/env python3
from __future__ import annotations

import argparse, importlib, json, os, sys
import yaml
from typing import Any, Dict
from hooks.event_sink import EventSink, new_run_id
from hooks.context import bind_sink
from hooks.metrics import summarize_events
import datetime

def iso_now() -> str:
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()

def import_target(spec: str):
    # "module:function"
    if ":" not in spec:
        raise ValueError(f"Invalid target spec (expected module:function): {spec}")
    mod, fn = spec.split(":", 1)
    m = importlib.import_module(mod)
    f = getattr(m, fn)
    return f

def write_json(path: str, obj: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, sort_keys=True)

def write_md(path: str, md: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)

    with open(args.registry, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    hooks = cfg.get("hooks", [])
    results = []

    for h in hooks:
        hook_id = h["hook_id"]
        theorem_id = h["theorem_id"]
        target = h["target"]
        params: Dict[str, Any] = h.get("params", {})

        out_dir = os.path.join(args.out, hook_id)
        os.makedirs(out_dir, exist_ok=True)

        events_path = os.path.join(out_dir, "events.jsonl")
        # truncate
        open(events_path, "w", encoding="utf-8").write("")

        seed = params.get("seed")
        run_id = new_run_id()
        sink = EventSink(out_path=events_path, hook_id=hook_id, theorem_id=theorem_id, run_id=run_id, seed=seed)

        status = "OK"
        err = None

        try:
            fn = import_target(target)
        except Exception as e:
            status = "SKIP"
            err = f"Import failed: {e}"
            sink.emit("hook_skip", reason=err, target=target)
            fn = None

        if fn is not None:
            try:
                with bind_sink(sink):
                    sink.emit("hook_start", params=params, target=target)
                    fn(params)  # convention: runner consumes params dict
                    sink.emit("hook_end")
            except Exception as e:
                status = "ERROR"
                err = str(e)
                sink.emit("hook_error", error=err)

        summary = summarize_events(events_path)
        summary.update({
            "hook_id": hook_id,
            "theorem_id": theorem_id,
            "target": target,
            "params": params,
            "status": status,
            "error": err,
            "run_id": run_id,
            "generated_at": iso_now(),
        })
        write_json(os.path.join(out_dir, "summary.json"), summary)

        md = f"""# Hook Summary — {hook_id}

- theorem_id: `{theorem_id}`
- status: **{status}**
- target: `{target}`
- run_id: `{run_id}`

## Event counts
"""
        for k, v in summary["event_counts"].items():
            md += f"- `{k}`: {v}\n"
        if err:
            md += f"\n## Error\n\n``\n{err}\n```\n"
        write_md(os.path.join(out_dir, "summary.md"), md)

        results.append(summary)

    write_json(os.path.join(args.out, "_hooks_index.json"), {"generated_at": iso_now(), "hooks": results})

if __name__ == "__main__":
    main()
