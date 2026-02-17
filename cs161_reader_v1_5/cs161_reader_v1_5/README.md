# CS161 Reader (Plotkin F10) — v1.5 (Actionable Maps)

v1.5 makes the **maps actionable**:
- Every map node links to the relevant **chapter** and **theorem anchor** (when available).
- When a theorem has a hook, the node links to the **evidence bundle** (events + summary).
- If goldens exist, the node links to the **golden bundle**.

## Build the site
```bash
python3 scripts/build_site.py --chapters chapters.yaml --out dist/site
```

## Run hooks
```bash
python3 scripts/run_hooks.py --registry hook_registry.yaml --out dist/hooks
```

## Goldens
```bash
python3 scripts/golden_capture.py --registry hook_registry.yaml --out golden
python3 scripts/golden_verify.py --registry hook_registry.yaml --golden golden
```

## Regenerate actionable map index
```bash
python3 scripts/build_maps_actionable.py --chapters chapters.yaml --hooks hook_registry.yaml --out docs/maps_actionable.json
```
