#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
for f in "$ROOT_DIR/chapters/"*.md; do
  bash "$ROOT_DIR/build/pandoc_chapter.sh" "chapters/$(basename "$f")"
done
pandoc "$ROOT_DIR/chapters/ch04_randomized_algorithms.md"        "$ROOT_DIR/chapters/ch05_graph_search.md"        "$ROOT_DIR/chapters/ch06_shortest_paths.md"   --defaults "$ROOT_DIR/build/pandoc_defaults.yaml"   -o "$ROOT_DIR/pdf/cs161_reader_v0_4.pdf"
echo "Wrote: $ROOT_DIR/pdf/cs161_reader_v0_4.pdf"
