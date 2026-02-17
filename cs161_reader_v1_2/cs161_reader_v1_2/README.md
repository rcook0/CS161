# CS161 Reader (Plotkin F10) — v1.2 (Navigable)

v1.2 adds a **navigable site build**:
- Generates a static HTML site with sidebar navigation
- Pattern index + theorem index pages
- Per-chapter HTML with anchors preserved
- JSON search index (lightweight) for external search tooling / UI later

## Build site
```bash
python3 scripts/build_site.py --chapters chapters.yaml --out dist/site
```

## Build PDFs (optional)
```bash
bash build/pandoc_all.sh
```

## Run hooks (from v1.1)
```bash
python3 scripts/run_hooks.py --registry hook_registry.yaml --out dist/hooks
```
