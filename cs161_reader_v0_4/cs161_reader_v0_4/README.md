# CS161 Reader (Plotkin F10) — v0.4 (clean)

Pandoc-first CS161 reader with executable witnesses in `cs161lab`.

## Contents
- `docs/LECTURE_MAP.md`
- `chapters/ch04_randomized_algorithms.md` (+ `pdf/`)
- `chapters/ch05_graph_search.md` (+ `pdf/`)
- `chapters/ch06_shortest_paths.md` (+ `pdf/`)
- `pdf/cs161_reader_v0_4.pdf` (combined)

## Build
Requirements:
- `pandoc`
- `pdflatex` (TeX Live)

Build all chapters + combined:
```bash
bash build/pandoc_all.sh
```

Build one chapter:
```bash
bash build/pandoc_chapter.sh chapters/ch06_shortest_paths.md
```
