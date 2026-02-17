# CS161 Reader (Plotkin F10) — v1.4 (Determinism + Golden Evidence)

v1.4 makes the reader **replayable**:
- Hooks produce evidence bundles (events + summaries).
- A **golden set** captures expected evidence hashes for deterministic runs.
- CI-friendly verification script compares current evidence to goldens.

## Key commands

### Build site
```bash
python3 scripts/build_site.py --chapters chapters.yaml --out dist/site
```

### Run hooks (produce evidence)
```bash
python3 scripts/run_hooks.py --registry hook_registry.yaml --out dist/hooks
```

### Capture goldens (writes to ./golden/)
```bash
python3 scripts/golden_capture.py --registry hook_registry.yaml --out golden
```

### Verify against goldens
```bash
python3 scripts/golden_verify.py --registry hook_registry.yaml --golden golden
```

## What “deterministic” means here
- We fix RNG seeds per hook.
- We verify **hashes** of output artifacts (events.jsonl + summary.json), not floating-point exactness.
- If a hook is inherently non-deterministic (e.g., uses time), it must record stable fields only
  or be excluded from the golden suite.

## Outputs
- `dist/site/` — navigable HTML
- `dist/hooks/` — current evidence
- `golden/` — captured reference evidence + MANIFEST.sha256
