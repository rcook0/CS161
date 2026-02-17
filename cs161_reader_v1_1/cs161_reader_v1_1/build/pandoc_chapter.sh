#!/usr/bin/env bash
set -euo pipefail
CHAPTER_FILE="${1:-}"
if [[ -z "$CHAPTER_FILE" ]]; then
  echo "Usage: build/pandoc_chapter.sh chapters/<chapter>.md"
  exit 1
fi
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$ROOT_DIR/dist/_build/pdf"
mkdir -p "$OUT_DIR"
BASENAME="$(basename "$CHAPTER_FILE" .md)"
OUT_PDF="$OUT_DIR/${BASENAME}.pdf"
pandoc "$ROOT_DIR/$CHAPTER_FILE" --defaults "$ROOT_DIR/build/pandoc_defaults.yaml" -o "$OUT_PDF"
echo "Wrote: $OUT_PDF"
