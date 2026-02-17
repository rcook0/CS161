#!/usr/bin/env python3
from __future__ import annotations
import argparse, os, re, json, subprocess, datetime
import yaml
from pathlib import Path

def iso_now() -> str:
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()

ANCHOR_RE = re.compile(r'\{#([A-Za-z0-9\-_.:]+)\}')
PAT_RE = re.compile(r'\[P[0-9]+(?:,P[0-9]+)*\]')

def read_text(p: Path) -> str:
    return p.read_text(encoding='utf-8')

def render_base(template: str, title: str, chapter_links: str, content: str) -> str:
    return template.replace("{{title}}", title).replace("{{chapter_links}}", chapter_links).replace("{{content}}", content)

def pandoc_md_to_html(md_path: Path, html_path: Path, title: str) -> tuple[bool,str]:
    # Use pandoc if available
    cmd = [
        "pandoc", str(md_path),
        "--standalone",
        "--toc",
        "--metadata", f"title={title}",
        "--section-divs",
        "-o", str(html_path)
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            return False, res.stderr + "\n" + res.stdout
        return True, ""
    except FileNotFoundError as e:
        return False, "pandoc not found"

def extract_entries(md_text: str, chapter_href: str):
    entries = []
    # Match headings of interest with anchors
    for line in md_text.splitlines():
        if line.startswith("## "):
            anchor = None
            m = ANCHOR_RE.search(line)
            if m:
                anchor = m.group(1)
            pats = PAT_RE.findall(line)
            # Normalize patterns like [P5,P2]
            pat_list = []
            if pats:
                pat_list = pats[0].strip("[]").split(",")
            # Title without patterns/anchor
            title = line[3:]
            title = PAT_RE.sub("", title)
            title = ANCHOR_RE.sub("", title).strip()
            kind = "heading"
            if title.startswith("Theorem"):
                kind="theorem"
            elif title.startswith("Lemma"):
                kind="lemma"
            elif title.startswith("Invariant"):
                kind="invariant"
            elif title.startswith("Template"):
                kind="template"
            elif title.startswith("Definition"):
                kind="definition"
            if anchor:
                entries.append({
                    "id": anchor,
                    "title": title,
                    "kind": kind,
                    "patterns": pat_list,
                    "href": f"{chapter_href}#{anchor}"
                })
    return entries

def li(text, href):
    return f'<li><a href="{href}">{text}</a></li>'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapters", required=True, help="chapters.yaml")
    ap.add_argument("--out", required=True, help="output dir (e.g. dist/site)")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out/"static").mkdir(exist_ok=True)
    # copy CSS
    src_css = Path(__file__).resolve().parents[1] / "site" / "static" / "style.css"
    (out/"static"/"style.css").write_text(src_css.read_text(encoding="utf-8"), encoding="utf-8")

    base_tpl = (Path(__file__).resolve().parents[1] / "site" / "templates" / "base.html").read_text(encoding="utf-8")

    cfg = yaml.safe_load(Path(args.chapters).read_text(encoding="utf-8"))
    chapters = cfg["chapters"]
    root_dir = Path(args.chapters).resolve().parent
    ch_dir = root_dir/"chapters"

    chapter_links = "\n".join([li(f'{c["id"].upper()} — {c["title"]}', f'{c["id"]}.html') for c in chapters])

    index_cards = []
    theorem_entries = []
    # Render each chapter
    for c in chapters:
        md_path = ch_dir / c["file"]
        ch_id = c["id"]
        html_out = out / f"{ch_id}.content.html"
        ok, err = pandoc_md_to_html(md_path, html_out, f'{ch_id.upper()} — {c["title"]}')
        if not ok:
            html_out.write_text(f"<h1>Build error</h1><pre>{err}</pre>", encoding="utf-8")
        # Wrap inside base template
        chapter_html = html_out.read_text(encoding="utf-8")
        full = render_base(base_tpl, f'{ch_id.upper()} — {c["title"]}', chapter_links, chapter_html)
        (out/f"{ch_id}.html").write_text(full, encoding="utf-8")

        # entries for indices
        md_text = md_path.read_text(encoding="utf-8")
        theorem_entries.extend(extract_entries(md_text, f"{ch_id}.html"))

        index_cards.append(f'''
<div class="card" data-search="{c['title']} {ch_id}">
  <div style="font-weight:700"><a href="{ch_id}.html">{ch_id.upper()} — {c['title']}</a></div>
  <div class="muted">{c['file']}</div>
</div>''')

    # Patterns page (render proof_patterns.md via pandoc too)
    pp_md = root_dir/"docs"/"proof_patterns.md"
    pp_content = out/"patterns.content.html"
    ok, err = pandoc_md_to_html(pp_md, pp_content, "Proof Patterns")
    if not ok:
        pp_content.write_text(f"<h1>Build error</h1><pre>{err}</pre>", encoding="utf-8")
    patterns_html = render_base(base_tpl, "Proof Patterns", chapter_links, pp_content.read_text(encoding="utf-8"))
    (out/"patterns.html").write_text(patterns_html, encoding="utf-8")

    
# Maps page
maps_md = root_dir/"docs"/"maps.md"
maps_content = out/"maps.content.html"
ok, err = pandoc_md_to_html(maps_md, maps_content, "Maps")
if not ok:
    maps_content.write_text(f"<h1>Build error</h1><pre>{err}</pre>", encoding="utf-8")
maps_html = render_base(base_tpl, "Maps", chapter_links, maps_content.read_text(encoding="utf-8"))
(out/"maps.html").write_text(maps_html, encoding="utf-8")

# Hooks page (docs/hooks_index.md)
hooks_md = root_dir/"docs"/"hooks_index.md"
hooks_content = out/"hooks.content.html"
ok, err = pandoc_md_to_html(hooks_md, hooks_content, "Hooks")
if not ok:
    hooks_content.write_text(f"<h1>Build error</h1><pre>{err}</pre>", encoding="utf-8")
hooks_html = render_base(base_tpl, "Hooks", chapter_links, hooks_content.read_text(encoding="utf-8"))
(out/"hooks.html").write_text(hooks_html, encoding="utf-8")

# Goldens page (docs/goldens.md)
gold_md = root_dir/"docs"/"goldens.md"
gold_content = out/"goldens.content.html"
ok, err = pandoc_md_to_html(gold_md, gold_content, "Goldens")
if not ok:
    gold_content.write_text(f"<h1>Build error</h1><pre>{err}</pre>", encoding="utf-8")
gold_html = render_base(base_tpl, "Goldens", chapter_links, gold_content.read_text(encoding="utf-8"))
(out/"goldens.html").write_text(gold_html, encoding="utf-8")
# Theorems page
    rows = []
    for e in sorted(theorem_entries, key=lambda x: (x["kind"], x["id"])):
        pats = ", ".join(e["patterns"]) if e["patterns"] else ""
        rows.append(f'''
<div class="card" data-search="{e['id']} {e['title']} {pats} {e['kind']}">
  <div style="font-weight:700"><a href="{e['href']}">{e['title']}</a></div>
  <div class="muted"><code>{e['id']}</code> · {e['kind']} · {pats}</div>
</div>''')
    theorems_content = "<h1>Theorem Index</h1><p class='muted'>Anchors extracted from chapter headings with <code>{#id}</code>.</p>" + "\n".join(rows)
    (out/"theorems.html").write_text(render_base(base_tpl, "Theorem Index", chapter_links, theorems_content), encoding="utf-8")

    # Hooks page (if hooks index exists, link; else placeholder)
    hooks_hint = "<h1>Hooks</h1><p class='muted'>Run hooks with <code>python3 scripts/run_hooks.py --registry hook_registry.yaml --out dist/hooks</code> then copy or point your UI here.</p>"
    (out/"hooks.html").write_text(render_base(base_tpl, "Hooks", chapter_links, hooks_hint), encoding="utf-8")

    # Home page
    home = "<h1>CS161 Reader</h1><p class='muted'>v1.2 navigable build. Use the sidebar to browse chapters, proof patterns, and theorem index.</p>" + "\n".join(index_cards)
    (out/"index.html").write_text(render_base(base_tpl, "CS161 Reader", chapter_links, home), encoding="utf-8")

    # JSON search index
    (out/"search_index.json").write_text(json.dumps({
        "generated_at": iso_now(),
        "chapters": [{"id": c["id"], "title": c["title"], "href": f"{c['id']}.html"} for c in chapters],
        "entries": theorem_entries
    }, indent=2), encoding="utf-8")

    # Build report
    (out/"BUILD_INFO.json").write_text(json.dumps({
        "generated_at": iso_now(),
        "pandoc_required": True,
        "chapters_count": len(chapters),
        "entries_count": len(theorem_entries),
    }, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()
