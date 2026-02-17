#!/usr/bin/env python3
from __future__ import annotations
import argparse, os, json, hashlib, subprocess, sys
from pathlib import Path
import shutil

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def load_manifest(path: Path) -> dict[str,str]:
    m = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, rel = line.split("  ", 1)
        m[rel.strip()] = digest.strip()
    return m

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", required=True)
    ap.add_argument("--golden", required=True)
    ap.add_argument("--work", default="dist/_verify_run")
    args = ap.parse_args()

    golden = Path(args.golden)
    manifest_path = golden / "MANIFEST.sha256"
    if not manifest_path.exists():
        print("Missing golden MANIFEST.sha256. Run golden_capture.py first.", file=sys.stderr)
        return 2

    expected = load_manifest(manifest_path)

    work = Path(args.work)
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    subprocess.check_call(["python3", "scripts/run_hooks.py", "--registry", args.registry, "--out", str(work)])

    # compare only files present in golden manifest
    mismatches = []
    for rel, digest in expected.items():
        cur = (golden / rel)  # note: rel is under golden; but we want corresponding under work when applicable
        # map: golden/<hook_id>/file -> work/<hook_id>/file
        rel_path = Path(rel)
        work_path = work / rel_path
        if not work_path.exists():
            mismatches.append((rel, "MISSING", digest, None))
            continue
        got = sha256_file(work_path)
        if got != digest:
            mismatches.append((rel, "DIFF", digest, got))

    if mismatches:
        out = {
            "status":"FAIL",
            "mismatches":[{"rel":r,"type":t,"expected":e,"got":g} for r,t,e,g in mismatches]
        }
        print(json.dumps(out, indent=2))
        return 1

    print(json.dumps({"status":"OK","checked_files":len(expected)}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
