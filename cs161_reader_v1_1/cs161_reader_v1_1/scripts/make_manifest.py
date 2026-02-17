#!/usr/bin/env python3
import sys, os, hashlib

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    if len(sys.argv) != 3:
        print("Usage: make_manifest.py <dir> <out_manifest>", file=sys.stderr)
        sys.exit(2)
    root, out = sys.argv[1], sys.argv[2]
    entries = []
    for folder, _, files in os.walk(root):
        for fn in files:
            full = os.path.join(folder, fn)
            rel = os.path.relpath(full, root).replace("\\","/")
            if rel == os.path.basename(out):
                continue
            entries.append((rel, sha256_file(full)))
    entries.sort()
    with open(out, "w", encoding="utf-8") as f:
        for rel, digest in entries:
            f.write(f"{digest}  {rel}\n")

if __name__ == "__main__":
    main()
