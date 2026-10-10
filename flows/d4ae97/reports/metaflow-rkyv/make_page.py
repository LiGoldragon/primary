#!/usr/bin/env python3
# Builds the book page from the source block and the measured medians.
import html, json, math, re, pathlib

here = pathlib.Path(__file__).parent
books = here.parent.parent / "books"
src = (books / "11-the-fixed-metaflow-record.md").read_text()
m = json.loads((here / "medians.json").read_text())
code = pathlib.Path("/home/li/primary/tools/book-code.html").read_text()
run = json.loads((here / "run1.json").read_text())
c = run["constancy"]

T = lambda s: html.escape(s, quote=False)


def inline(s):
    s = T(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


# ---------- charts ----------
W = 360


def range_chart():
    rows = [
        ("Proposed Metaflow record", c["proposed"]["min"], c["proposed"]["max"], "one size", "var(--add-edge)"),
        ("Succession row", c["succession"]["min"], c["succession"]["max"], "one size", "var(--add-edge)"),
        ("String ids, six hex", c["string_ids_hex6"]["min"], c["string_ids_hex6"]["max"], "one size", "var(--accent)"),
        ("String ids, three words", c["string_ids_words"]["min"], c["string_ids_words"]["max"],
         f'{c["string_ids_words"]["distinct"]} sizes', "var(--del-edge)"),
        ("Vector of 0 to 16 past flows", c["vectored_past_0_16"]["min"], c["vectored_past_0_16"]["max"],
         f'{c["vectored_past_0_16"]["distinct"]} sizes', "var(--del-edge)"),
    ]
    x0, x1, vmax = 12, 348, 200
    sx = lambda v: x0 + (x1 - x0) * v / vmax
    rh = 40
    h = 26 + rh * len(rows) + 22
    out = [f'<figure><svg viewBox="0 0 {W} {h}" width="100%" role="img" aria-label="Bytes per archived record, by shape" style="max-width:100%;height:auto;font-family:var(--f-label)">']
    for v in range(0, vmax + 1, 50):
        out.append(f'<line x1="{sx(v):.1f}" x2="{sx(v):.1f}" y1="18" y2="{h-22}" style="stroke:var(--line);stroke-width:1"/>')
        out.append(f'<text x="{sx(v):.1f}" y="{h-8}" text-anchor="middle" style="fill:var(--muted);font-size:10px">{v}</text>')
    out.append(f'<text x="{x1}" y="12" text-anchor="end" style="fill:var(--muted);font-size:10px">bytes per record</text>')
    for i, (label, lo, hi, note, col) in enumerate(rows):
        y = 26 + i * rh
        out.append(f'<text x="{x0}" y="{y+8}" style="fill:var(--fg);font-size:11.5px">{T(label)}</text>')
        size = f"{lo}" if lo == hi else f"{lo} to {hi}"
        out.append(f'<text x="{x1}" y="{y+8}" text-anchor="end" style="fill:var(--muted);font-size:10.5px">{size} B, {note}</text>')
        if lo == hi:
            out.append(f'<rect x="{sx(lo)-2:.1f}" y="{y+14}" width="4" height="14" rx="1" style="fill:{col}"><title>{T(label)}: {lo} bytes</title></rect>')
        else:
            out.append(f'<rect x="{sx(lo):.1f}" y="{y+16}" width="{sx(hi)-sx(lo):.1f}" height="10" rx="3" style="fill:{col};opacity:.75"><title>{T(label)}: {lo} to {hi} bytes</title></rect>')
    out.append('</svg><figcaption>Bytes per archived record, a million records of each shape. A vector of 1,024 past flows takes '
               f'{dict(c["vectored_growth"]).get(1024) if isinstance(c["vectored_growth"], dict) else [g[1] for g in c["vectored_growth"] if g[0]==1024][0]:,} bytes.</figcaption></figure>')
    return "\n".join(out)


def log_chart(label, rows, lo_exp, hi_exp, unit_note):
    x0, x1 = 12, 348
    sx = lambda v: x0 + (x1 - x0) * (math.log10(v) - lo_exp) / (hi_exp - lo_exp)
    rh = 40
    top = 34
    h = top + rh * len(rows) + 22
    ticks = {0: "1 ns", 1: "10 ns", 2: "100 ns", 3: "1 µs", 4: "10 µs", 5: "100 µs", 6: "1 ms", 7: "10 ms"}
    out = [f'<figure><svg viewBox="0 0 {W} {h}" width="100%" role="img" aria-label="{T(label)}" style="max-width:100%;height:auto;font-family:var(--f-label)">']
    for e in range(lo_exp, hi_exp + 1):
        out.append(f'<line x1="{sx(10**e):.1f}" x2="{sx(10**e):.1f}" y1="{top-6}" y2="{h-22}" style="stroke:var(--line);stroke-width:1"/>')
        out.append(f'<text x="{sx(10**e):.1f}" y="{h-8}" text-anchor="middle" style="fill:var(--muted);font-size:10px">{ticks[e]}</text>')
    # legend
    out.append(f'<circle cx="{x0+5}" cy="12" r="4.5" style="fill:var(--sheet);stroke:var(--accent);stroke-width:2"/>')
    out.append(f'<text x="{x0+14}" y="16" style="fill:var(--muted);font-size:10.5px">10,000 records</text>')
    out.append(f'<circle cx="{x0+112}" cy="12" r="4.5" style="fill:var(--accent)"/>')
    out.append(f'<text x="{x0+121}" y="16" style="fill:var(--muted);font-size:10.5px">1,000,000 records</text>')
    out.append(f'<text x="{x1}" y="16" text-anchor="end" style="fill:var(--muted);font-size:10px">log scale</text>')

    def fmt(v):
        if v >= 1e6: return f"{v/1e6:.2f} ms"
        if v >= 1e3: return f"{v/1e3:.2f} µs"
        return f"{v:.1f} ns" if v < 100 else f"{v:.0f} ns"
    for i, (name, a, b) in enumerate(rows):
        y = top + i * rh
        out.append(f'<text x="{x0}" y="{y+8}" style="fill:var(--fg);font-size:11.5px">{T(name)}</text>')
        out.append(f'<text x="{x1}" y="{y+8}" text-anchor="end" style="fill:var(--muted);font-size:10.5px">{fmt(a)} · {fmt(b)}</text>')
        out.append(f'<line x1="{sx(a):.1f}" x2="{sx(b):.1f}" y1="{y+21}" y2="{y+21}" style="stroke:var(--accent);stroke-width:1.5;opacity:.5"/>')
        out.append(f'<circle cx="{sx(a):.1f}" cy="{y+21}" r="5" style="fill:var(--sheet);stroke:var(--accent);stroke-width:2"><title>{T(name)}, 10,000 records: {fmt(a)}</title></circle>')
        out.append(f'<circle cx="{sx(b):.1f}" cy="{y+21}" r="5" style="fill:var(--accent)"><title>{T(name)}, 1,000,000 records: {fmt(b)}</title></circle>')
    out.append(f'</svg><figcaption>{T(unit_note)}</figcaption></figure>')
    return "\n".join(out)


lookup = log_chart("One lookup by id", [
    ("Position, index × size", m["10000.fixed.direct_ns"], m["1000000.fixed.direct_ns"]),
    ("Binary search, sorted block", m["10000.fixed.binary_ns"], m["1000000.fixed.binary_ns"]),
    ("redb row, fixed record", m["10000.fixed.redb_access_ns"], m["1000000.fixed.redb_access_ns"]),
    ("redb row, vectored record", m["10000.vectored.redb_access_ns"], m["1000000.vectored.redb_access_ns"]),
    ("Linear scan of the block", m["10000.fixed.linear_ns"], m["1000000.fixed.linear_ns"]),
], 0, 7, "One lookup by id, read to the current flow. The redb rows are stored as Sema stores them: one archive per key, validated on read.")

update = log_chart("One update of the current flow", [
    ("In place, raw bytes", m["10000.fixed.update_raw_ns"], m["1000000.fixed.update_raw_ns"]),
    ("In place, validated", m["10000.fixed.update_seal_ns"], m["1000000.fixed.update_seal_ns"]),
    ("redb row, fixed record", m["10000.fixed.redb_update_patch_ns"], m["1000000.fixed.redb_update_patch_ns"]),
    ("redb row, append to vector", m["10000.vectored.redb_append_update_ns"], m["1000000.vectored.redb_append_update_ns"]),
], 0, 5, "One update of the current flow; redb updates are 20,000 in one transaction.")

charts = {
    "[Chart: bytes per archived record, by shape]": range_chart(),
    "[Chart: one lookup by id, ten thousand and a million records]": lookup,
    "[Chart: one update of the current flow]": update,
}

# ---------- block to HTML ----------
block = src.split("<!-- to-the-living:start -->")[1].split("<!-- to-the-living:end -->")[0].strip()
lines = block.splitlines()
title = re.search(r"«(.+?)»", lines[0]).group(1)
body = lines[1:]

sections = []
cur = None
for l in body:
    if l.startswith("## "):
        cur = {"head": l[3:], "lines": []}
        sections.append(cur)
    elif cur is not None:
        cur["lines"].append(l)


def paragraphs(ls):
    """Split lines into blocks: code fences, lists, paragraphs."""
    out, i = [], 0
    while i < len(ls):
        l = ls[i]
        if l.startswith("```"):
            j = i + 1
            while not ls[j].startswith("```"):
                j += 1
            out.append(("code", "\n".join(ls[i + 1:j])))
            i = j + 1
        elif l.startswith("- "):
            items = []
            while i < len(ls) and ls[i].startswith("- "):
                items.append(ls[i][2:])
                i += 1
            out.append(("list", items))
        elif l.strip() == "":
            i += 1
        else:
            buf = []
            while i < len(ls) and ls[i].strip() and not ls[i].startswith("```") and not ls[i].startswith("- "):
                buf.append(ls[i])
                i += 1
            out.append(("p", " ".join(buf)))
    return out


def code_block(text):
    return f'<pre><code class="language-ethos">{T(text)}</code></pre>'


def ruling_html(text, number):
    q, rest = text.split(":", 1)
    parts = re.split(r"\s*\(([a-z])\)\s*", rest.strip())
    question = parts[0].strip()
    choices = [parts[k].strip() for k in range(2, len(parts), 2)]
    qp = f"<p>{inline(question)}</p>" if question else f"<p>Proposal {number}:</p>"
    lis = "".join(f"<li>{inline(ch)}</li>" for ch in choices)
    return f'<section class="rulings"><h2>Ruling</h2><ol><li value="{number}">{qp}<ol class="choices" type="a">{lis}</ol></li></ol></section>'


out = [f"<title>{T(title)}</title>", f'<h1 class="book-title">{T(title)}</h1>']
for s in sections:
    mm = re.match(r"Proposal (\d+): `([^`]+)`, (.+)", s["head"])
    blocks = paragraphs(s["lines"])
    if not mm:
        out.append("<section>")
        out.append(f"<h2>{inline(s['head'])}</h2>")
        for kind, val in blocks:
            if kind == "p" and val in charts:
                out.append(charts[val])
            elif kind == "p":
                out.append(f"<p>{inline(val)}</p>")
            elif kind == "list":
                out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in val) + "</ul>")
        out.append("</section>")
        continue
    num, target, what = mm.groups()
    out.append('<article class="proposal">')
    out.append(f'<header><span class="pnum">{num}</span><h2>{inline(what[0].upper() + what[1:])}</h2></header>')
    out.append(f'<p class="target"><code>{T(target)}</code></p>')
    mode = None
    diff_open = False
    pending = []
    for kind, val in blocks:
        if kind == "p" and val.startswith("Ruling"):
            if diff_open:
                out.append("</div>"); diff_open = False
            out.append(ruling_html(val, num))
            continue
        if kind == "p" and (val.startswith("Removed:") or val.startswith("Added:") or val.startswith("Removed: none")):
            if val.startswith("Removed: none"):
                if diff_open:
                    out.append("</div>"); diff_open = False
                out.append(f"<p>{inline(val)}</p>")
                out.append('<div class="diff">'); diff_open = True
                mode = "add"
                continue
            if not diff_open:
                out.append('<div class="diff">'); diff_open = True
            mode = "del" if val.startswith("Removed") else "add"
            continue
        if kind == "code" and mode:
            out.append(f'<div class="{mode}">{code_block(val)}</div>')
            continue
        if kind == "p" and mode == "add" and diff_open and s["head"].startswith("Proposal 4"):
            out.append(f'<div class="add"><p>{inline(val)}</p></div>')
            continue
        if diff_open:
            out.append("</div>"); diff_open = False; mode = None
        out.append(f"<p>{inline(val)}</p>")
    if diff_open:
        out.append("</div>")
    out.append("</article>")

page = "\n".join(out) + "\n" + code
dest = books / "11-the-fixed-metaflow-record.page.html"
dest.write_text(page)
print(dest, len(page))
