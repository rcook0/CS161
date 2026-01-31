# cs161lab

A compact, reusable “CS161 Algorithms Lab” package:

- Reference implementations (sorting/selection, graph traversal, shortest paths, MST, min-cut).
- Benchmark harness with reproducible runs and CSV/JSON output.
- A proof-pattern index intended to accompany typed lecture notes (e.g., Plotkin F10).

## Quick start

```bash
python -m pip install -e .
cs161lab --help
```

## Layout

- `cs161lab/algorithms/` — canonical algorithms with trace-friendly outputs.
- `cs161lab/graphs/` — small graph data models (directed, weighted).
- `cs161lab/bench.py` — timing/benchmark utilities.
- `PROOF_PATTERNS.md` — index of correctness/analysis proof patterns.

## Philosophy

The goal is not maximal performance; it is *clarity + correctness + reproducibility*.
