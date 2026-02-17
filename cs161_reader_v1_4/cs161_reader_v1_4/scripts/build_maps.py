#!/usr/bin/env python3
from __future__ import annotations
import argparse, yaml
from pathlib import Path

DEFAULT_MAP = [
  {"lecture":"1–2","theme":"Asymptotics, induction & invariants (core proof mechanics)","anchors":"patterns P1/P2"},
  {"lecture":"3–4","theme":"Randomization toolkit (indicators, linearity, amplification)","anchors":"ch04: thm-4-3, thm-4-4, thm-4-6"},
  {"lecture":"5–7","theme":"Graph search: DFS/BFS, topo order, SCC intuitions","anchors":"ch05: inv-5-1, lem-5-2, thm-5-3"},
  {"lecture":"8–10","theme":"Shortest paths + relaxation worldview","anchors":"ch06: inv-6-1, thm-6-3, thm-6-6"},
  {"lecture":"11–12","theme":"Minimum spanning trees + cut property","anchors":"ch07: def-cut-property, thm-7-1, thm-7-2"},
  {"lecture":"13–14","theme":"Greedy correctness via exchange","anchors":"ch08: thm-8-1, lem-8-2, thm-8-3"},
  {"lecture":"15–17","theme":"Dynamic programming (state/recurrence/order/reconstruct)","anchors":"ch09: tpl-9-1"},
  {"lecture":"18–19","theme":"Amortized analysis + data structures","anchors":"ch10: thm-10-1, thm-10-2"},
  {"lecture":"20+","theme":"NP, reductions, completeness intuition","anchors":"ch11: tpl-11-1"},
]

def main():
  ap = argparse.ArgumentParser()
  ap.add_argument("--out", default="docs/maps.md")
  args = ap.parse_args()

  out = Path(args.out)
  out.parent.mkdir(parents=True, exist_ok=True)

  lines = []
  lines.append("# Maps\n")
  lines.append("## Lecture → Chapter map (Plotkin F10 approximate spine)\n")
  lines.append("| Lecture | Theme | Reader anchors |\n|---|---|---|\n")
  for r in DEFAULT_MAP:
    lines.append(f"| {r['lecture']} | {r['theme']} | {r['anchors']} |\n")

  out.write_text("".join(lines), encoding="utf-8")
  print(f"Wrote {out}")

if __name__ == "__main__":
  main()
