# Proof Hooks (v1.1)

A **proof hook** is an executable evidence generator that produces:
- event trace (`events.jsonl`)
- summary (`summary.json`, `summary.md`)

Each hook corresponds to one theorem or proof pattern claim.

## Hook anatomy
- **hook_id**: stable identifier (e.g. `hook-thm-6-3-dijkstra-finalize`)
- **theorem_id**: theorem anchor (e.g. `thm-6-3`)
- **target**: module:function to execute (or a built-in runner)
- **params**: inputs; should include a deterministic seed where relevant
- **evidence checks**: light checks that align with the proof story (not full formal verification)

## Event schema
Each event line is JSON conforming to `schemas/trace_event.schema.json` and includes:
- `t` (timestamp), `hook_id`, `theorem_id`
- `event` (string)
- `data` (event payload)
- `seed` (optional)
- `run_id`

## Adding a hook
1. Add entry to `hook_registry.yaml`
2. Implement target function to accept an `EventSink` or use `hooks.context.current_sink()`
3. Re-run `scripts/run_hooks.py`

## Evidence philosophy
We don't "prove" the theorem by running code.
We generate **witness traces** that match the logical checkpoints in the proof:
- Dijkstra: each `finalize(u)` should be consistent with "no shorter path exists"
- Dynamic array: total copies per append should stay bounded on average
- Karger: repetition schedule should show success frequency consistent with lower bound
