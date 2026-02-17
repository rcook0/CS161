#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERSION="v1.0"
OUT="$ROOT_DIR/dist/cs161_reader_${VERSION}"
BUILD="$ROOT_DIR/dist/_build"

rm -rf "$OUT"
mkdir -p "$OUT/pdf" "$OUT/meta"

# Build into BUILD
bash "$ROOT_DIR/build/pandoc_all.sh"

# Copy PDFs
cp -r "$BUILD/pdf/." "$OUT/pdf/"

# Copy metadata snapshots
cp "$ROOT_DIR/chapters.yaml" "$OUT/meta/chapters.yaml"
cp "$ROOT_DIR/docs/proof_patterns.md" "$OUT/meta/proof_patterns.md"
cp "$ROOT_DIR/docs/theorem_index.md" "$OUT/meta/theorem_index.md"

# Manifest
python3 "$ROOT_DIR/scripts/make_manifest.py" "$OUT" "$OUT/MANIFEST.sha256"

echo "Release written to: $OUT"
