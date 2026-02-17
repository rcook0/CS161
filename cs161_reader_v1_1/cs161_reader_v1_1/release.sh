#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERSION="v1.1"
OUT="$ROOT_DIR/dist/cs161_reader_${VERSION}"
BUILD="$ROOT_DIR/dist/_build"

rm -rf "$OUT"
mkdir -p "$OUT/pdf" "$OUT/meta" "$OUT/hooks"

# Build PDFs (best-effort; if pandoc/pdflatex missing, you'll see errors)
bash "$ROOT_DIR/build/pandoc_all.sh" || true

# Copy PDFs if present
if [[ -d "$BUILD/pdf" ]]; then
  cp -r "$BUILD/pdf/." "$OUT/pdf/" || true
fi

# Copy metadata snapshots
cp "$ROOT_DIR/chapters.yaml" "$OUT/meta/chapters.yaml"
cp "$ROOT_DIR/docs/proof_patterns.md" "$OUT/meta/proof_patterns.md"
cp "$ROOT_DIR/docs/theorem_index.md" "$OUT/meta/theorem_index.md"
cp "$ROOT_DIR/docs/theorem_hooks.md" "$OUT/meta/theorem_hooks.md"
cp "$ROOT_DIR/docs/proof_hooks.md" "$OUT/meta/proof_hooks.md"

# Run hooks (best-effort)
python3 "$ROOT_DIR/scripts/run_hooks.py" --registry "$ROOT_DIR/hook_registry.yaml" --out "$OUT/hooks" || true

# Manifest
python3 "$ROOT_DIR/scripts/make_manifest.py" "$OUT" "$OUT/MANIFEST.sha256"

echo "Release written to: $OUT"
