# Hooks

Hooks generate trace evidence aligned to proof checkpoints.

Run:
```bash
python3 scripts/run_hooks.py --registry hook_registry.yaml --out dist/hooks
```

Then inspect:
- `dist/hooks/<hook_id>/events.jsonl`
- `dist/hooks/<hook_id>/summary.json`
