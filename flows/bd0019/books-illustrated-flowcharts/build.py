#!/usr/bin/env python3
"""Builds «Illustrated flowcharts, and vision becoming skill» from source.md (copied by extract.py) and verifies the source text,
the Mermaid blocks, every quote. No illustration files; Mermaid is drawn by the page script. No controls."""
import html, re, subprocess, sys, hashlib, pathlib, json
HERE = pathlib.Path(__file__).resolve().parent
PRIMARY = pathlib.Path("/home/li/primary")
PROJ = pathlib.Path("/home/li/.claude/projects/-home-li-primary")
esc = html.escape

def record(rel):
    p = PRIMARY / rel
    if p.exists(): return p.read_text()
    return subprocess.run(["git","-C",str(PRIMARY),"show",f"main:{rel}"],capture_output=True,text=True,check=True).stdout
def raw_line(session, line):
    with open(PROJ / f"{session}.jsonl") as fh:
        for i, l in enumerate(fh, 1):
            if i == line: return json.loads(l)
def raw_text(r):
    c = r["message"]["content"]
    return c if isinstance(c, str) else "".join(b.get("text","") for b in c if isinstance(b, dict))
def flat(s): return re.sub(r"\s*\n>\s*", " ", s)

RAW = (HERE / "source.md").read_text()
first, rest = RAW.split("\n", 1)
m = re.fullmatch(r"`Book\.«(.+)»`", first); assert m, first
TITLE = m.group(1); assert TITLE == "Illustrated flowcharts, and vision becoming skill"
BODY = rest.strip("\n")
secs = re.split(r"\n(?=## \d\. )", BODY)
assert len(secs) == 2 and all(s.startswith(f"## {i}. ") for i, s in enumerate(secs, 1))

def inline(s):
    out = []
    for p in re.split(r"(`[^`]+`)", s):
        if p.startswith("`"): out.append(f"<code>{esc(p[1:-1])}</code>")
        else: out.append(re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", esc(p)))
    return "".join(out)

MERMAID = []
def graph_html(src):
    MERMAID.append(src)
    return (f'<figure class="gfig"><div class="gbox" data-src="{esc(src, quote=True)}">'
            f'<pre class="mmsrc">{esc(src)}</pre></div></figure>')

def table_html(rows):
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    head, body = cells[0], cells[2:]
    return ('<div class="tw"><table class="ev"><thead><tr>' + "".join(f"<th>{inline(c)}</th>" for c in head)
            + "</tr></thead><tbody>" + "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body)
            + "</tbody></table></div>")

def md(lines):
    out, i = [], 0
    while i < len(lines):
        l = lines[i]
        if l.startswith("```mermaid"):
            j = i + 1
            while lines[j] != "```": j += 1
            out.append(graph_html("\n".join(lines[i+1:j]))); i = j + 1; continue
        if l.startswith("## "): out.append(f"<h2>{inline(l[3:])}</h2>")
        elif l.startswith("|"):
            j = i
            while j < len(lines) and lines[j].startswith("|"): j += 1
            out.append(table_html(lines[i:j])); i = j; continue
        elif l.startswith("- "):
            items = []
            while i < len(lines) and (lines[i].startswith("- ") or lines[i].startswith("  - ")):
                if lines[i].startswith("- "):
                    items.append([inline(lines[i][2:]), []])
                else: items[-1][1].append(inline(lines[i][4:]))
                i += 1
            out.append('<ul class="pts">' + "".join(
                f"<li>{t}" + (("<ul>" + "".join(f"<li>{x}</li>" for x in sub) + "</ul>") if sub else "") + "</li>"
                for t, sub in items) + "</ul>"); continue
        elif l.startswith("  ") and l.strip():
            out.append(f"<p>{inline(l.strip())}</p>")
        elif l.startswith(">"):
            ps = []
            while i < len(lines) and lines[i].startswith(">"):
                t = lines[i][1:].strip()
                if t: ps.append(f"<p>{inline(t)}</p>")
                i += 1
            out.append('<blockquote class="doc">' + "".join(ps) + "</blockquote>"); continue
        elif l.strip(): out.append(f"<p>{inline(l)}</p>")
        i += 1
    return "".join(out)

def block(lines): return '<div class="src">' + md(lines) + "</div>"
S = {n: secs[n-1].split("\n") for n in range(1, 3)}

SRC_ID = "fe945a2e-c785-4af4-9a46-766b6ea512e8"
Q = {
 "flow": (("fe945a2e-c785-4af4-9a46-766b6ea512e8", 1155, "f7313bbe-1f20-4679-823a-e2d0a2e02159") , "This is an example of a good or decent illustration which could be made from a flowchart accompanied by prose. The sonnet model can take the flowchart and give it more expressive power through this stylization. You could call that an illustrated flowchart.",
          "-- the living, comment of 2026-10-01T20:27 on «Your questions since 28 September», as read by Psyche Opus fe945a · transcript fe945a, line 1155"),
 "skill": (("fe945a2e-c785-4af4-9a46-766b6ea512e8", 1155, "f7313bbe-1f20-4679-823a-e2d0a2e02159"), "And to be clear, now vision is skill. Let's make that whole migration.",
          "-- the living, comment of 2026-10-01T20:29 on «Your questions since 28 September», as read by Psyche Opus fe945a · transcript fe945a, line 1155"),
}
def quote(k):
    _, text, prov = Q[k]
    return f'<blockquote class="living" data-q="{k}"><p class="said">{esc(text)}</p><p class="prov">{esc(prov)}</p></blockquote>'
def note(kind, words, date, body):
    verb = "agrees" if kind == "agree" else "disagrees"
    return (f'<aside class="note {kind}"><p class="tag">Psyche Sonnet {verb}</p><p>On “{esc(words)}” ({date}): {esc(body)}</p></aside>')
def txt(inner): return f'<section class="page txt"><div class="sheet">{inner}</div></section>'
def eyebrow(t): return f'<p class="eyebrow">{t}</p>'

NOTE1 = note("agree", "You could call that an illustrated flowchart", "2026-10-01",
             "the revised proposal is that word made a rule: each illustration starts from a flowchart, and the flowchart is written as Mermaid.")
NOTE2 = note("agree", "now vision is skill. Let's make that whole migration", "2026-10-01",
             "the source keeps to it. It builds nothing yet and puts the three open points to you before Mind Sol begins.")
PROPS = [
 "<strong>trial-flashbook: replace</strong> its first line on illustrations with the one-flowchart-or-a-few-lines paragraph (point 1).",
]
props = "".join(f'<li><span class="n">{i}</span><span><span class="box"></span>{t}<span class="badge sup">Not landed when checked</span></span></li>'
                 for i, t in enumerate(PROPS, 1))
SRC_PROV = ('<p class="prov">The source, verbatim: Psyche Opus fe945a, transcript fe945a2e-c785-4af4-9a46-766b6ea512e8.jsonl, '
            'line 1176, uuid 83222d01-a8a7-4490-aa65-470fbfcd2e86, 2026-10-01T20:56:19Z, between its to-the-living markers; '
            'its first line, Book.«Illustrated flowcharts, and vision becoming skill», gives this book its title and is not shown. '
            'The graph is drawn by this page’s own script from the source’s Mermaid text, unaltered, and stays left to right as the source has it.</p>')
s2 = S[2]; gi = s2.index("```mermaid"); ge = s2.index("```", gi + 1)
pages = [
 txt(eyebrow("Point 1 of 2") + block(S[1]) + quote("flow") + NOTE1),
 txt(eyebrow("Point 2 of 2") + block(s2[:gi]) + quote("skill") + NOTE2),
 txt(eyebrow("Point 2 of 2, continued") + block(s2[gi:ge + 1]) + eyebrow("Proposed in the source, by number") + f'<ol class="props">{props}</ol>'
     + '<p class="mark"><strong>Checked</strong> On 2026-10-01 the trial-flashbook skill still says the first page is always an illustration, so the replacement is not in.</p>'
     + SRC_PROV),
]
N = len(pages)
dots = "".join('<span class="dot t"></span>' for _ in pages)
out = ((HERE / "shell.html").read_text().replace("{{TITLE}}", esc(TITLE)).replace("{{N}}", str(N))
       .replace("{{DOTS}}", dots).replace("{{PAGES}}", "\n".join(pages)))
(HERE / "book.html").write_text(out)

fail = 0
def plain(h): return html.unescape(re.sub(r"<[^>]+>", "", h))
# strip the mermaid fallback text from prose check, but check mermaid separately
P = plain(out)
for k, (src, text, _) in Q.items():
    if isinstance(src, tuple):
        r = raw_line(src[0], src[1]); ok = r["uuid"] == src[2] and r["type"] == "user" and text in raw_text(r)
        where = f"{src[0][:8]} line {src[1]} {r['timestamp']}"
    else:
        ok = text in flat(record(src)); where = src
    print(("quote ok: " if ok else "QUOTE NOT VERBATIM IN RECORD "), k, where); fail += (not ok)
    if text not in P: print("QUOTE MISSING FROM BOOK", k); fail += 1
fences = re.findall(r"```mermaid\n(.*?)\n```", BODY, re.S)
print("mermaid blocks in source", len(fences), "in page", len(MERMAID))
if fences != MERMAID: print("MERMAID MISMATCH"); fail += 1
for f in fences:
    if f'data-src="{esc(f, quote=True)}"' not in out: print("MERMAID NOT IN data-src"); fail += 1
for line in BODY.split("\n"):
    if line.startswith("```") or not line.strip() or line.strip() == ">": continue
    if line.startswith("|"):
        if re.fullmatch(r"\|[-|]+\|", line): continue
        ts = [c.strip().replace("**","").replace("`","") for c in line.strip().strip("|").split("|")]
    else:
        ts = [re.sub(r"^\s*(## |- |> |>)", "", line).strip().replace("`","").replace("**","")]
    for t in ts:
        if t not in P and t not in "\n".join(fences): print("SOURCE LINE NOT VERBATIM:", t[:70]); fail += 1
print("pre blocks", out.count("<pre"), "(only the Mermaid source fallbacks expected:", len(fences), ")")
if out.count("<pre") != len(fences): fail += 1
for pat in (r"<button", r"<a\s", r"<input", r"<select", r"<textarea", r"onclick", r"addEventListener\('click'", r'role="button"', r"tabindex", r"<details", r"<summary", r"<img", r"data:image"):
    if re.search(pat, out): print("FORBIDDEN FOUND:", pat); fail += 1
print("title", TITLE, "pages", N, "source sha256", hashlib.sha256(RAW.encode()).hexdigest())
print("book sha256", hashlib.sha256(out.encode()).hexdigest(), "bytes", len(out.encode()))
print("FAIL" if fail else "verbatim: all quotes, mermaid and source lines OK; no controls")
sys.exit(1 if fail else 0)
