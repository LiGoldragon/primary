#!/usr/bin/env python3
"""Builds «The restart of the stack» from source.md (copied by extract.py). No quotes of the living, no graph, no illustrations, no controls, no notes."""
import html, re, sys, hashlib, pathlib
HERE = pathlib.Path(__file__).resolve().parent
esc = html.escape
TITLE = "The restart of the stack"
RAW = (HERE / "source.md").read_text()
lines = RAW.rstrip("\n").split("\n")
assert lines[0] == "## " + TITLE
pts, rul, mode = [], [], "pts"
for ln in lines[1:]:
    if not ln.strip(): continue
    if ln == "## Rulings": mode = "rul"; continue
    if mode == "pts":
        m = re.match(r"(\d)\. (.*)$", ln); assert m; pts.append((int(m.group(1)), m.group(2)))
    else:
        assert ln.startswith("- "); rul.append(ln[2:])
assert [n for n, _ in pts] == [1, 2, 3, 4] and len(rul) == 2
def inline(s):
    s = esc(s, quote=False)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
def mark(label, body): return f'<p class="mark"><strong>{esc(label)}</strong>{esc(body)}</p>'
def txt(inner): return f'<section class="page txt"><div class="sheet">{inner}</div></section>'
pages = []
for n, t in pts:
    inner = f'<p class="eyebrow">Point {n} of 4</p>'
    if n == 1: inner += f'<h2>{esc(TITLE)}</h2>'
    inner += f'<p class="pt">{inline(t)}</p>'
    pages.append(txt(inner))
SRC = ('<p class="prov">The source, verbatim: Psyche Fable 6997eb, transcript 6997eb8a-30eb-49a1-a787-45279164a43b.jsonl, line 2788, uuid 99b40699-cbb1-4088-a556-8df44d6e95d8, 2026-10-02T17:23:13Z, the block between its to-the-living markers titled «The restart of the stack»; the marker lines and its Presentation line are not shown. It holds no graph and no quotation of the living, so this book draws no graph and carries no verbatim quote.</p>')
items = "".join(f"<li>{inline(o)}</li>" for o in rul)
pages.append(txt('<p class="eyebrow">Rulings</p><h2>Rulings</h2>' + f'<ul class="pts rulings" id="rulings">{items}</ul>' +
    mark("Mark", "The brief for this book named line 2791 of that transcript; that line is the commission to this seat. The block itself is on line 2788, found by its title.") + SRC))
N = len(pages); dots = "".join('<span class="dot t"></span>' for _ in pages)
out = ((HERE/"shell.html").read_text().replace("{{TITLE}}", esc(TITLE)).replace("{{N}}", str(N)).replace("{{DOTS}}", dots).replace("{{PAGES}}", "\n".join(pages)))
out = out.replace("</style>", "p.pt{font-size:18px}\n.txt ul.pts{padding-left:1.1em}\n</style>", 1)
(HERE/"book.html").write_text(out)
P = html.unescape(re.sub(r"<[^>]+>", "", out)); fail = 0
for l in lines:
    if not l.strip(): continue
    t = re.sub(r"^(## |- |\d\. )", "", l).replace("**", "")
    if t not in P: print("SOURCE LINE NOT IN BOOK:", t[:70]); fail += 1
for pat in (r"<pre", r"<button", r"<a\s", r"<input", r"<select", r"<textarea", r"onclick", r"tabindex", r"<details", r"<img", r"data:image", r"mermaid"):
    if re.search(pat, out): print("FORBIDDEN:", pat); fail += 1
print("pages", N, "source sha256", hashlib.sha256(RAW.encode()).hexdigest()); print("book bytes", len(out.encode()))
print("FAIL" if fail else "ALL SOURCE LINES PRESENT; no controls"); sys.exit(1 if fail else 0)
