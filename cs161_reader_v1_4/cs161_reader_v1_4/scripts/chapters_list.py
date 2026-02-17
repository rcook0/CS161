#!/usr/bin/env python3
import argparse, os, yaml
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("chapters_yaml")
    ap.add_argument("--fullpath", default=None)
    a=ap.parse_args()
    cfg=yaml.safe_load(open(a.chapters_yaml,"r",encoding="utf-8"))
    for ch in cfg["chapters"]:
        fn=ch["file"]
        if a.fullpath: fn=os.path.join(a.fullpath, fn)
        print(fn)
if __name__=="__main__":
    main()
