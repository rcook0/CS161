# Goldens

Goldens are *reference evidence bundles* captured from deterministic hook runs.

## Capture
```bash
python3 scripts/golden_capture.py --registry hook_registry.yaml --out golden
```

## Verify
```bash
python3 scripts/golden_verify.py --registry hook_registry.yaml --golden golden
```

Goldens are intentionally hash-based: they detect behavioral drift without pinning you to brittle text diffs.
