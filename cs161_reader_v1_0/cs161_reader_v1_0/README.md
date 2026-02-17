# CS161 Reader (Plotkin F10) — v1.0

v1.0 turns the reader into a **buildable product**:
- `chapters.yaml` is the single source of truth for chapter assembly/order.
- One-command release: `./release.sh`
- Versioned `dist/` bundle: per-chapter PDFs + combined PDF + manifests.
- Canonical proof-pattern registry + theorem index skeleton.

Markdown/Pandoc-first. LaTeX is optional via Pandoc’s PDF engine (`pdflatex`).

## Quickstart

Build all PDFs (local):
```bash
bash build/pandoc_all.sh
```

Produce a versioned release bundle:
```bash
bash release.sh
```

Outputs:
- `dist/cs161_reader_v1.0/`
  - `pdf/` (chapter PDFs + combined)
  - `meta/` (chapters.yaml snapshot + indices)
  - `MANIFEST.sha256`

## Conventions
- Theorems/lemmas/invariants carry IDs + pattern tags:
  - `Theorem 6.3 ... [P5,P2] {#thm-6-3}`
- Pattern IDs are canonical in `docs/proof_patterns.md`.
