#!/usr/bin/env python3
from __future__ import annotations
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import argparse, re, json
from pathlib import Path
import yaml

ANCHOR_RE = re.compile(r'\{#([A-Za-z0-9\-_.:]+)\}')
PAT_RE = re.compile(r'\[P[0-9]+(?:,P[0-9]+)*\]')

def extract_anchors(md: str, chapter_id: str):
    out = {}
    for line in md.splitlines():
        if line.startswith("## "):
            m = ANCHOR_RE.search(line)
            if not m:
                continue
            anchor = m.group(1)
            pats = PAT_RE.findall(line)
            pat_list = []
            if pats:
                pat_list = pats[0].strip("[]").split(",")
            title = line[3:]
            title = PAT_RE.sub("", title)
            title = ANCHOR_RE.sub("", title).strip()
            out[anchor] = {"title": title, "patterns": pat_list, "chapter_id": chapter_id}
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapters", required=True)
    ap.add_argument("--hooks", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    root = Path(args.chapters).resolve().parent
    cfg = yaml.safe_load(Path(args.chapters).read_text(encoding="utf-8"))
    chapters = cfg["chapters"]

    anchors = {}
    for ch in chapters:
        cid = ch["id"]
        md = (root/"chapters"/ch["file"]).read_text(encoding="utf-8")
        anchors.update(extract_anchors(md, cid))

    hook_cfg = yaml.safe_load(Path(args.hooks).read_text(encoding="utf-8"))
    hook_map = {h["theorem_id"]: h["hook_id"] for h in hook_cfg.get("hooks", [])}

    payload = {"generated_at": "now", "anchors": anchors, "hook_map": hook_map}
    Path(args.out).write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

if __name__ == "__main__":
    main()
