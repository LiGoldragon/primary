#!/usr/bin/env python3
"""Builds «Hooks, graphs and the book maker» from source.md (copied by extract.py) and verifies the source text,
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
TITLE = m.group(1); assert TITLE == "Hooks, graphs and the book maker"
BODY = rest.strip("\n")
secs = re.split(r"\n(?=## \d\. )", BODY)
assert len(secs) == 4 and all(s.startswith(f"## {i}. ") for i, s in enumerate(secs, 1))

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
S = {n: secs[n-1].split("\n") for n in range(1, 5)}

S977 = ("fe945a2e-c785-4af4-9a46-766b6ea512e8", 977, "867f78c8-62d7-4125-8c8d-b79d23322c7b")
P977 = "-- the living, 2026-10-01T20:08Z, to Psyche Opus fe945a · transcript fe945a, line 977"
HOOKF = "flows/cf3553/vision/operational-finalResponseLifecycleHook.md"
Q = {
 "hook": (HOOKF, "We should have an end-of-last-reply hook that notifies the Flow component using the Flow CLI of all the information it can give it.",
          "-- psyche, relayed verbatim by root on 2026-09-19 · " + HOOKF),
 "llm": (S977, "To call an AI LLM just to make a render, just to display something, is ridiculous but I asked for alternatives.", P977),
 "mech": (S977, "It doesn't mean it's necessarily instantly rendered although we're going towards that, because really rendering is mechanical when you think about it. We should be able to just write a tool that does it.", P977),
}
def quote(k):
    _, text, prov = Q[k]
    return f'<blockquote class="living" data-q="{k}"><p class="said">{esc(text)}</p><p class="prov">{esc(prov)}</p></blockquote>'
def note(kind, words, date, body):
    verb = "agrees" if kind == "agree" else "disagrees"
    return (f'<aside class="note {kind}"><p class="tag">Psyche Sonnet {verb}</p><p>On “{esc(words)}” ({date}): {esc(body)}</p></aside>')
def txt(inner): return f'<section class="page txt"><div class="sheet">{inner}</div></section>'
def eyebrow(t): return f'<p class="eyebrow">{t}</p>'

NOTE1 = note("agree", "an end-of-last-reply hook that notifies the Flow component using the Flow CLI", "2026-09-19",
             "the graph is that word drawn out: each harness's hook calls the flow CLI. The table shows the end-of-reply hook exists in Claude Code and Codex as Stop, and only as an idle status in OpenCode.")
NOTE3 = note("agree", "To call an AI LLM just to make a render, just to display something, is ridiculous", "2026-10-01",
             "this section keeps to it: the graph is written in Mermaid and a script in the page draws it, so no model call goes into drawing.")

PROPS = [
 "<strong>trial-flashbook: replace</strong> its alternating-pages paragraph with the one-graph-or-few-lines paragraph (point 4).",
 "<strong>trial-flashbook: remove</strong> its line loading trial-flashbook-illustration (point 4).",
 "<strong>New skill, trial-graph</strong>, with its description and its rule on showing the mechanism (point 4).",
 "<strong>New subagent, book-maker</strong>, Sonnet at light effort, loading trial-flashbook and trial-graph (point 4).",
]
props = "".join(f'<li><span class="n">{i}</span><span><span class="box"></span>{t}<span class="badge sup">Not landed when checked</span></span></li>'
                 for i, t in enumerate(PROPS, 1))
SRC_PROV = ('<p class="prov">The source, verbatim: Psyche Opus fe945a, transcript fe945a2e-c785-4af4-9a46-766b6ea512e8.jsonl, '
            'line 1121, uuid 5bf7bef0-8a5c-4264-8258-e75a81f4c09b, 2026-10-01T20:43:45Z, between its to-the-living markers; '
            'its first line, Book.«Hooks, graphs and the book maker», gives this book its title and is not shown. '
            'Graphs are drawn by this page’s own script from the source’s Mermaid text; the table and the lists are the source’s.</p>')

s1 = S[1]; gi = s1.index("```mermaid"); ge = s1.index("```", gi + 1)
tbl_start = next(i for i, x in enumerate(s1) if x.startswith("|"))
s3 = S[3]; g3e = s3.index("```", s3.index("```mermaid") + 1)

pages = [
 txt(eyebrow("Point 1 of 4") + block(s1[:ge + 1])),
 txt(eyebrow("Point 1 of 4, continued") + block(s1[ge + 1:]) + quote("hook") + NOTE1),
 txt(eyebrow("Point 2 of 4") + block(S[2])),
 txt(eyebrow("Point 3 of 4") + block(s3[:g3e + 1])),
 txt(eyebrow("Point 3 of 4, continued") + block(s3[g3e + 1:]) + quote("llm") + quote("mech") + NOTE3),
 txt(eyebrow("Point 4 of 4") + block(S[4]) + eyebrow("Proposed in the source, by number") + f'<ol class="props">{props}</ol>'
     + '<p class="mark"><strong>Checked</strong> On 2026-10-01 no trial-graph skill and no book-maker agent exist, and trial-flashbook still carries both lines named above.</p>'
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
