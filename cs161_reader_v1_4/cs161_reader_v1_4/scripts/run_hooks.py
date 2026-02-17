#!/usr/bin/env python3
from __future__ import annotations
import argparse, importlib, json, os, datetime, hashlib
import yaml
from typing import Any, Dict
from hooks.event_sink import EventSink, new_run_id
from hooks.context import bind_sink
from hooks.metrics import summarize_events

def iso_now() -> str:
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()

def import_target(spec: str):
    mod, fn = spec.split(":", 1)
    m = importlib.import_module(mod)
    return getattr(m, fn)

def write_json(path: str, obj: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, sort_keys=True)

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    cfg = yaml.safe_load(open(args.registry, "r", encoding="utf-8"))
    hooks = cfg.get("hooks", [])
    out_index = []

    for h in hooks:
        hook_id = h["hook_id"]
        theorem_id = h["theorem_id"]
        target = h["target"]
        params: Dict[str, Any] = h.get("params", {})
        seed = params.get("seed")

        out_dir = os.path.join(args.out, hook_id)
        os.makedirs(out_dir, exist_ok=True)
        events_path = os.path.join(out_dir, "events.jsonl")
        open(events_path, "w", encoding="utf-8").write("")

        run_id = new_run_id()
        sink = EventSink(out_path=events_path, hook_id=hook_id, theorem_id=theorem_id, run_id=run_id, seed=seed)

        status = "OK"
        err = None
        try:
            fn = import_target(target)
            with bind_sink(sink):
                sink.emit("hook_start", params=params, target=target)
                fn(params)
                sink.emit("hook_end")
        except Exception as e:
            status = "ERROR"
            err = str(e)
            sink.emit("hook_error", error=err)

        summary = summarize_events(events_path)
        summary.update({
            "hook_id": hook_id, "theorem_id": theorem_id, "target": target,
            "params": params, "status": status, "error": err,
            "run_id": run_id, "generated_at": iso_now(),
            "events_sha256": sha256_file(events_path),
        })
        write_json(os.path.join(out_dir, "summary.json"), summary)
        out_index.append(summary)

    write_json(os.path.join(args.out, "_hooks_index.json"), {"generated_at": iso_now(), "hooks": out_index})

if __name__ == "__main__":
    main()
