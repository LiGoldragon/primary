#!/usr/bin/env python3
"""Builds «Session handling as it is» from source.md (copied by extract.py); verifies source text, Mermaid text and every quote. No illustration files, no controls."""
import html, re, subprocess, sys, hashlib, pathlib, json
HERE = pathlib.Path(__file__).resolve().parent
PRIMARY = pathlib.Path("/home/li/primary")
PROJ = pathlib.Path("/home/li/.claude/projects/-home-li-primary")
esc = html.escape
def record(rel):
    p = PRIMARY / rel
    if p.exists(): return p.read_text()
    return subprocess.run(["git","-C",str(PRIMARY),"show",f"main:{rel}"],capture_output=True,text=True,check=True).stdout
def flat(s): return re.sub(r"\s*\n>\s*", " ", s)
RAW = (HERE / "source.md").read_text()
TITLE = "Session handling as it is"
m = re.match(r"```mermaid\n(.*?)\n```\n\n(.*)$", RAW, re.S)
MMD, rest = m.group(1), m.group(2)
secs = re.split(r"\n(?=## \d\. )", rest.strip("\n"))
assert len(secs) == 4
def inline(s):
    out = []
    for p in re.split(r"(`[^`]+`)", s):
        if p.startswith("`"): out.append(f"<code>{esc(p[1:-1])}</code>")
        else: out.append(re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", esc(p)))
    return "".join(out)
Q = {
 "zero": ("flows/6997eb/reports/psyche-since-28-september.md", "Just create new sessions, which really should be done with almost zero LLM calls, but not quite zero: very, very small calls that would be extremely fast and cost almost nothing.",
   "the living, 2026-10-01 17:11, flow e2a70a, line 585, typed, as gathered in flows/6997eb/reports/psyche-since-28-september.md"),
 "poll": ("flows/6997eb/reports/psyche-since-28-september.md", "Essentially we want to avoid polling, which means we're going to make this hook-based.",
   "the living, 2026-09-30 17:16, flow 7328f4, line 552, speech to text, as gathered in flows/6997eb/reports/psyche-since-28-september.md"),
 "nobody": ("flows/fe945a/vision/polling.md", "Nobody should be checking anything repeatedly.",
   "the living, 2026-10-01, flow fe945a, a comment on the book «Where books go, and the anatomy of the book pipeline», flows/fe945a/vision/polling.md"),
 "reap": ("flows/1ac573/vision/operational-reapReplacedSessions.md", "When a session gets replaced, it has to be reaped so it doesn't keep getting messages.",
   "the living, 2026-09-17, flow 1ac573, flows/1ac573/vision/operational-reapReplacedSessions.md"),
 "skill": ("RAW:fe945a2e-c785-4af4-9a46-766b6ea512e8:934", "For me subagents are a type of skill.",
   "the living, 2026-10-01 19:54, a comment, transcript fe945a line 934"),
}
def quote(k):
    _, text, prov = Q[k]
    return f'<blockquote class="living" data-q="{k}"><p class="said">{esc(text)}</p><p class="prov">-- {esc(prov)}</p></blockquote>'
def note(kind, words, date, body):
    verb = "agrees" if kind == "agree" else "disagrees"
    return f'<aside class="note {kind}" data-note="{kind}"><p class="tag">Psyche Sonnet {verb}</p><p>On “{esc(words)}” ({date}): {esc(body)}</p></aside>'
def txt(inner): return f'<section class="page txt"><div class="sheet">{inner}</div></section>'
def sec(i):
    lines = secs[i].split("\n"); h = lines[0][3:]; num, name = h.split(". ", 1)
    bl = [l[2:] for l in lines[1:] if l.strip()]
    assert all(l.startswith("- ") for l in lines[1:] if l.strip())
    return (f'<p class="eyebrow">Point {num} of 4</p><h2>{esc(name)}</h2>'
            f'<ul class="pts">' + "".join(f"<li>{inline(b)}</li>" for b in bl) + "</ul>")
N1 = note("agree","almost zero LLM calls","2026-10-01","the words name the target. The source reports a million tokens for one relaunch, so the gap between the word and the present is large and is the thing to close.")
N2 = note("agree","Nobody should be checking anything repeatedly","2026-10-01","the source finds two checkers still running, the launcher at one second and Herdr's screen reading. This seat holds that both fall under your word.")
graph = ('<section class="page txt"><div class="sheet"><p class="eyebrow">The shape today</p><h2>'+esc(TITLE)+'</h2>'
  f'<figure class="gfig"><div class="gbox" id="g1" data-src="{esc(MMD, quote=True)}"><pre class="mmsrc">{esc(MMD)}</pre></div></figure>'
  '<p class="mark"><strong>Direction</strong> The source wrote this graph left to right (<code>flowchart LR</code>); it is drawn as written.</p></div></section>')
pages = [graph, txt(sec(0)), txt(sec(1)+quote("zero")+N1), txt(sec(2)+quote("poll")+quote("nobody")+quote("reap")+N2), txt(sec(3)+quote("skill"))]
SRC = ('<p class="prov">The source, verbatim: Psyche Opus fe945a, transcript fe945a2e-c785-4af4-9a46-766b6ea512e8.jsonl, line 1435, uuid 394f8933-743a-461f-a9bc-fc675c9f35e9, 2026-10-02T17:16:09Z, the block between its to-the-living markers titled «Session handling as it is»; marker lines and its Presentation datom line are not shown. The block carries no rulings, so there is no rulings page.</p>')
pages[-1] = pages[-1].replace("</div></section>", SRC + "</div></section>")
N = len(pages)
dots = "".join('<span class="dot t"></span>' for _ in pages)
out = ((HERE/"shell.html").read_text().replace("{{TITLE}}", esc(TITLE)).replace("{{N}}", str(N)).replace("{{DOTS}}", dots).replace("{{PAGES}}", "\n".join(pages)))
(HERE/"book.html").write_text(out)
fail = 0
def plain(h): return html.unescape(re.sub(r"<[^>]+>", "", h))
P = plain(out)
for k,(src,text,_) in Q.items():
    if src.startswith("RAW:"):
        _, s, ln = src.split(":"); l = open(PROJ/f"{s}.jsonl").readlines()[int(ln)-1]; r = json.loads(l)
        c = r["message"]["content"]; t = c if isinstance(c,str) else "".join(b.get("text","") for b in c if isinstance(b,dict))
        ok = r["type"]=="user" and text in t.replace("\n"," ")
    else: ok = text in flat(record(src))
    print(("quote ok: " if ok else "QUOTE NOT VERBATIM "), k); fail += (not ok)
    if text not in P: print("QUOTE MISSING", k); fail += 1
for line in rest.split("\n"):
    if not line.strip(): continue
    t = re.sub(r"^(## \d\. |## |- )", "", line).strip().replace("`","").replace("**","")
    if t not in P: print("SOURCE LINE NOT VERBATIM:", t[:70]); fail += 1
assert html.unescape(re.search(r'data-src="([^"]*)"', out).group(1)) == MMD; print("mermaid source identical")
for pat in (r"<button", r"<a\s", r"<input", r"<select", r"<textarea", r"onclick", r"<details", r"<img", r"data:image", r"<pre class=\"code"):
    if re.search(pat, out): print("FORBIDDEN", pat); fail += 1
print("pages", N, "src sha", hashlib.sha256(RAW.encode()).hexdigest()[:12], "book bytes", len(out.encode()))
print("FAIL" if fail else "OK"); sys.exit(1 if fail else 0)
