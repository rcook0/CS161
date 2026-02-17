#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$ROOT_DIR/dist/_build/pdf"
mkdir -p "$OUT_DIR"

python3 "$ROOT_DIR/scripts/chapters_list.py" "$ROOT_DIR/chapters.yaml" | while read -r ch; do
  bash "$ROOT_DIR/build/pandoc_chapter.sh" "chapters/$ch"
done

python3 "$ROOT_DIR/scripts/chapters_list.py" "$ROOT_DIR/chapters.yaml" --fullpath "$ROOT_DIR/chapters" > "$ROOT_DIR/dist/_build/chapters_fullpaths.txt"

pandoc $(cat "$ROOT_DIR/dist/_build/chapters_fullpaths.txt")   --defaults "$ROOT_DIR/build/pandoc_defaults.yaml"   -o "$OUT_DIR/cs161_reader.pdf"

echo "Wrote: $OUT_DIR/cs161_reader.pdf"
