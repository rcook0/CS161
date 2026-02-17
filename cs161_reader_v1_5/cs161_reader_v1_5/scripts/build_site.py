#!/usr/bin/env python3
from __future__ import annotations
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import argparse, json, re, subprocess
from pathlib import Path
import yaml

ANCHOR_RE = re.compile(r'\{#([A-Za-z0-9\-_.:]+)\}')
PAT_RE = re.compile(r'\[P[0-9]+(?:,P[0-9]+)*\]')
MAP_TOKEN_RE = re.compile(r'@([A-Za-z0-9\-_.:]+)')

def render(base: str, title: str, content: str) -> str:
    return base.replace("{{title}}", title).replace("{{content}}", content)

def md_to_html(md: Path, out: Path, title: str) -> str:
    try:
        res = subprocess.run(["pandoc", str(md), "--standalone", "--metadata", f"title={title}", "-o", str(out)], capture_output=True, text=True)
        if res.returncode == 0:
            return out.read_text(encoding="utf-8")
        return f"<pre>{res.stderr}</pre>"
    except FileNotFoundError:
        return "<pre>pandoc not found</pre>"

def extract_entries(md_text: str, ch_id: str):
    entries = []
    for line in md_text.splitlines():
        if line.startswith("## "):
            m = ANCHOR_RE.search(line)
            if not m: 
                continue
            anchor = m.group(1)
            pats = PAT_RE.findall(line)
            pat_list = pats[0].strip("[]").split(",") if pats else []
            title = line[3:]
            title = PAT_RE.sub("", title)
            title = ANCHOR_RE.sub("", title).strip()
            entries.append({"id":anchor,"title":title,"chapter":ch_id,"href":f"{ch_id}.html#{anchor}","patterns":pat_list})
    return entries

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--chapters", required=True)
    ap.add_argument("--out", required=True)
    a=ap.parse_args()
    out=Path(a.out); out.mkdir(parents=True, exist_ok=True)
    (out/"static").mkdir(exist_ok=True)
    root=Path(a.chapters).resolve().parent
    (out/"static"/"style.css").write_text((root/"site"/"static"/"style.css").read_text(encoding="utf-8"), encoding="utf-8")
    base=(root/"site"/"templates"/"base.html").read_text(encoding="utf-8")
    cfg=yaml.safe_load(Path(a.chapters).read_text(encoding="utf-8"))
    entries=[]
    # chapters
    for ch in cfg["chapters"]:
        ch_id=ch["id"]
        md=root/"chapters"/ch["file"]
        tmp=out/f"{ch_id}.content.html"
        content=md_to_html(md, tmp, ch["title"])
        (out/f"{ch_id}.html").write_text(render(base, ch["title"], content), encoding="utf-8")
        entries.extend(extract_entries(md.read_text(encoding="utf-8"), ch_id))
    # patterns
    patt=md_to_html(root/"docs"/"proof_patterns.md", out/"patterns.content.html", "Proof patterns")
    (out/"patterns.html").write_text(render(base,"Proof patterns",patt), encoding="utf-8")
    # theorems
    rows="".join([f"<div><a href='{e['href']}'>{e['title']}</a> <code>{e['id']}</code></div>" for e in sorted(entries, key=lambda x:x["id"])])
    (out/"theorems.html").write_text(render(base,"Theorems", "<h1>Theorems</h1>"+rows), encoding="utf-8")
    # maps actionable index
    maps_json = root/"docs"/"maps_actionable.json"
    if not maps_json.exists():
        subprocess.run(["python3","scripts/build_maps_actionable.py","--chapters","chapters.yaml","--hooks","hook_registry.yaml","--out",str(maps_json)], cwd=root)
    mj=json.loads(maps_json.read_text(encoding="utf-8")) if maps_json.exists() else {"anchors":{}, "hook_map":{}}
    anchors=mj.get("anchors",{})
    hook_map=mj.get("hook_map",{})
    maps_html=md_to_html(root/"docs"/"maps.md", out/"maps.content.html", "Maps")
    def repl(m):
        tok=m.group(1)
        if tok in anchors:
            ch=anchors[tok]["chapter_id"]
            return f"<a href='{ch}.html#{tok}'><code>{tok}</code></a>"
        if tok.startswith("hook-"):
            return f"<a href='../hooks/{tok}/summary.json'><code>{tok}</code></a>"
        return f"<code>@{tok}</code>"
    maps_html = MAP_TOKEN_RE.sub(repl, maps_html)
    # table of anchored nodes
    cards=[]
    for tid,info in sorted(anchors.items()):
        hook = hook_map.get(tid)
        cards.append(f"<div><a href='{info['chapter_id']}.html#{tid}'>{info['title']}</a> <code>{tid}</code>" + (f" · <a href='../hooks/{hook}/summary.json'><code>{hook}</code></a>" if hook else "") + "</div>")
    maps_page = maps_html + "<h2>Anchored nodes</h2>" + "".join(cards)
    (out/"maps.html").write_text(render(base,"Maps",maps_page), encoding="utf-8")
    # home
    home = "<h1>CS161 Reader</h1><ul>" + "".join([f"<li><a href='{c['id']}.html'>{c['id'].upper()} — {c['title']}</a></li>" for c in cfg["chapters"]]) + "</ul>"
    (out/"index.html").write_text(render(base,"CS161 Reader",home), encoding="utf-8")
    (out/"search_index.json").write_text(json.dumps({"entries":entries}, indent=2), encoding="utf-8")

if __name__=="__main__":
    main()
