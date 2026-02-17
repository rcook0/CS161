# CS161 Reader (Plotkin F10) — v1.1 (Proof Hooks)

v1.1 adds **proof hooks**: a lightweight instrumentation + harness layer that turns
algorithm executions into **trace evidence** (events + summaries) that correspond to
the proof patterns and theorem claims in the reader.

This is intentionally *minimal* and *pluggable*:
- You can point hooks at real implementations (e.g. your `cs161lab` package),
  or use the included `cs161lab_stub` demos.

## New in v1.1
- `hooks/` instrumentation primitives (event sink + context)
- `schemas/trace_event.schema.json` for JSONL event lines
- `hook_registry.yaml` defines runnable hooks (theorem → runner → parameters)
- `scripts/run_hooks.py` executes all hooks, writes evidence bundles
- `docs/proof_hooks.md` and `docs/theorem_hooks.md` map theorems to hook IDs

## Run
```bash
python3 scripts/run_hooks.py --registry hook_registry.yaml --out dist/hooks
```

Outputs per hook:
- `events.jsonl` (one JSON object per line)
- `summary.json`
- `summary.md`

## Notes
- For deterministic runs, hooks set seeds where applicable.
- If a target module/function is missing, the harness records a SKIP with reason.
