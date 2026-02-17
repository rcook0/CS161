#!/usr/bin/env python3
import sys, yaml, argparse, os

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("chapters_yaml")
    ap.add_argument("--fullpath", default=None)
    args = ap.parse_args()

    with open(args.chapters_yaml, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    for ch in cfg.get("chapters", []):
        fn = ch["file"]
        if args.fullpath:
            fn = os.path.join(args.fullpath, fn)
        print(fn)

if __name__ == "__main__":
    main()
