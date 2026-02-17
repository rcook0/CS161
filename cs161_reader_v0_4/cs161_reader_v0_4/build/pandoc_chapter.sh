#!/usr/bin/env bash
set -euo pipefail
CHAPTER_PATH="${1:-}"
if [[ -z "$CHAPTER_PATH" ]]; then
  echo "Usage: build/pandoc_chapter.sh chapters/<chapter>.md"
  exit 1
fi
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$ROOT_DIR/pdf"
BASENAME="$(basename "$CHAPTER_PATH" .md)"
OUT_PDF="$OUT_DIR/${BASENAME}.pdf"
mkdir -p "$OUT_DIR"
pandoc "$ROOT_DIR/$CHAPTER_PATH" --defaults "$ROOT_DIR/build/pandoc_defaults.yaml" -o "$OUT_PDF"
echo "Wrote: $OUT_PDF"
