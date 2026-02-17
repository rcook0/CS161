#!/usr/bin/env python3
from __future__ import annotations
import argparse, os, shutil, json, hashlib
from pathlib import Path
import subprocess

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def walk_files(root: Path):
    for p in sorted(root.rglob("*")):
        if p.is_file():
            yield p

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", required=True)
    ap.add_argument("--out", required=True, help="golden output dir")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    tmp = out / "_tmp_run"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True)

    # run hooks into tmp
    subprocess.check_call(["python3", "scripts/run_hooks.py", "--registry", args.registry, "--out", str(tmp)])

    # copy per-hook evidence into golden/<hook_id>/ (events.jsonl + summary.json)
    hooks_index = json.loads((tmp / "_hooks_index.json").read_text(encoding="utf-8"))
    for h in hooks_index["hooks"]:
        hook_id = h["hook_id"]
        src = tmp / hook_id
        dst = out / hook_id
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

    # manifest
    manifest_lines = []
    for p in walk_files(out):
        if p.name == "MANIFEST.sha256":
            continue
        rel = p.relative_to(out).as_posix()
        manifest_lines.append(f"{sha256_file(p)}  {rel}")
    (out / "MANIFEST.sha256").write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    # cleanup tmp
    shutil.rmtree(tmp)

    print(f"Wrote goldens to: {out}")

if __name__ == "__main__":
    main()
