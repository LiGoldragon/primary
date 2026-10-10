#!/usr/bin/env python3
"""Builds «Handling skills» from source.md (copied by extract.py): no illustration files, no Mermaid in this block, no controls.
Verifies source text and every quote against raw records."""
import html, re, sys, hashlib, pathlib, json, glob
HERE = pathlib.Path(__file__).resolve().parent
PROJ = pathlib.Path("/home/li/.claude/projects/-home-li-primary")
esc = html.escape

def raw_line(session, line):
    with open(glob.glob(str(PROJ / f"{session}*.jsonl"))[0]) as fh:
        for i, l in enumerate(fh, 1):
            if i == line: return json.loads(l)
def raw_text(r):
    c = r["message"]["content"]
    return c if isinstance(c, str) else "".join(b.get("text", "") for b in c if isinstance(b, dict))
def flat(s): return re.sub(r"\s*\n(&gt;|>)\s*", " ", html.unescape(s))

RAW = (HERE / "source.md").read_text()
lines = [l for l in RAW.split("\n")]
assert lines[0] == "" and lines[1] == "## Handling skills"
TITLE = "Handling skills"
pts = [l for l in lines if re.match(r"\d\. \*\*", l)]
assert len(pts) == 4
RUL = [l for l in lines if l.startswith("- ")]
assert lines.index("## Ruling") and len(RUL) == 1

def inline(s):
    out = []
    for p in re.split(r"(`[^`]+`)", s):
        if p.startswith("`"): out.append(f"<code>{esc(p[1:-1])}</code>")
        else: out.append(re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", esc(p, quote=False)))
    return "".join(out)
def pt(i):
    m = re.fullmatch(r"\d\. (.*)", pts[i]); return f'<div class="src"><p>{inline(m.group(1))}</p></div>'

# (session, line, uuid prefix, [verbatim segments], display text, provenance)
Q = {
 "vision": ("fe945a", 1155, "f7313b", ["now vision is skill. Let's make that whole migration"],
   "And to be clear, now vision is skill. Let's make that whole migration.",
   "-- the living, comment of 2026-10-01T20:29 on «Your questions since 28 September», as read by Psyche Opus fe945a · transcript fe945a, line 1155, uuid f7313b"),
 "nexus": ("183ae0", 156, "a420fa", ["We need to make a nexus to deploy skills", "changes the ones that have the same name. That sounds simple to me."],
   "We need to make a nexus to deploy skills. … changes the ones that have the same name. That sounds simple to me.",
   "-- the living, 2026-09-28 (Psyche Fable 6997eb dates it 15:54, 8904b1 line 5779, mode not stated), relayed verbatim in transcript 183ae0, line 156, uuid a420fa; the 8904b1 transcript is not on disk here"),
 "scrap": ("183ae0", 826, "b4ccc3", ["we need to finish designing that or we just scrap the whole idea of deploying skills for now. I don't know."],
   "we need to finish designing that or we just scrap the whole idea of deploying skills for now. I don't know.",
   "-- the living, 2026-09-29 16:09, mode not stated, transcript 183ae0, line 826, uuid b4ccc3"),
 "typed": ("183ae0", 857, "84888d", ["the skills will be typed", "a nexus that has a fully typed specification for the different types of inputs that it can take"],
   "the skills will be typed. … a nexus that has a fully typed specification for the different types of inputs that it can take.",
   "-- the living, 2026-09-29 16:11, mode not stated, transcript 183ae0, line 857, uuid 84888d"),
 "daemon": ("183ae0", 156, "a420fa", ["eventually the skills will live in a daemon not in a Git repo anymore."],
   "Well eventually the skills will live in a daemon not in a Git repo anymore.",
   "-- the living, 2026-09-28 (Psyche Fable 6997eb dates it 17:29, 8904b1 line 6741, mode not stated), relayed verbatim as 8904b1-23 in transcript 183ae0, line 156, uuid a420fa"),
}
def quote(k):
    return f'<blockquote class="living" data-q="{k}"><p class="said">{esc(Q[k][4])}</p><p class="prov">{esc(Q[k][5])}</p></blockquote>'
def note(kind, words, date, body):
    verb = "agrees" if kind == "agree" else "disagrees"
    return f'<aside class="note {kind}"><p class="tag">Psyche Sonnet {verb}</p><p>On “{esc(words)}” ({date}): {esc(body)}</p></aside>'
def txt(inner): return f'<section class="page txt"><div class="sheet">{inner}</div></section>'
def eyebrow(t): return f'<p class="eyebrow">{t}</p>'

NOTE_SIMPLE = note("agree", "That sounds simple to me", "2026-09-28",
  "the design view in the source is that sentence worked out: one act, one event, no person in the loop.")
NOTE_SCRAP = note("agree", "we just scrap the whole idea of deploying skills for now. I don't know", "2026-09-29",
  "the source leaves this open and does not decide it for you. It narrows what remains to one ruling.")
rul = f'<ol class="props"><li><span class="n">1</span><span><span class="box"></span>{inline(RUL[0][2:])}<span class="badge sup">Open</span></span></li></ol>'
SRC_PROV = ('<p class="prov">The source, verbatim: Psyche Fable 6997eb, transcript 6997eb8a-30eb-49a1-a787-45279164a43b.jsonl, '
            'line 2463, uuid 6b5b3514-62e7-4393-9af4-bc2ccd8694ed, 2026-10-02T17:13:32Z, the block between its first to-the-living markers; '
            'its Presentation line gives this book its title and is not shown. The block holds no Mermaid graph.</p>')
pages = [
 txt(eyebrow("Point 1 of 4") + pt(0)),
 txt(eyebrow("Point 2 of 4") + pt(1)),
 txt(eyebrow("Point 3 of 4") + pt(2) + quote("vision") + quote("nexus") + NOTE_SIMPLE),
 txt(eyebrow("Point 3 of 4, continued") + quote("scrap") + NOTE_SCRAP + quote("typed") + quote("daemon")),
 txt(eyebrow("Point 4 of 4") + pt(3)),
 txt(eyebrow("Open rulings") + "<h2>Ruling</h2>" + rul + SRC_PROV),
]
N = len(pages)
dots = "".join('<span class="dot t"></span>' for _ in pages)
out = ((HERE / "shell.html").read_text().replace("{{TITLE}}", esc(TITLE)).replace("{{N}}", str(N))
       .replace("{{DOTS}}", dots).replace("{{PAGES}}", "\n".join(pages)))
(HERE / "book.html").write_text(out)

fail = 0
P = html.unescape(re.sub(r"<[^>]+>", "", out))
for k, (s, ln, u, segs, text, _) in Q.items():
    r = raw_line(s, ln); t = flat(raw_text(r))
    ok = r["uuid"].startswith(u) and r["type"] == "user" and all(x in t for x in segs)
    print(("quote ok: " if ok else "QUOTE NOT VERBATIM IN RECORD "), k, s, ln, r["timestamp"]); fail += (not ok)
    if text not in P: print("QUOTE MISSING FROM BOOK", k); fail += 1
    if not all(x in text for x in segs): print("DISPLAY != SEGMENTS", k); fail += 1
for l in lines:
    if not l.strip() or l.startswith("## "): continue
    t = re.sub(r"^(\d\. |- )", "", l).replace("**", "").replace("`", "")
    if t not in P: print("SOURCE LINE NOT VERBATIM:", t[:70]); fail += 1
if "## Handling skills" in P or "Presentation.{" in P or "to-the-living" in re.sub(r'<p class="prov">.*?</p>', "", out): print("MARKER/DATOM LEAK"); fail += 1
if "<pre" in out or "```" in P: print("pre/code block present"); fail += 1
for pat in (r"<button", r"<a\s", r"<input", r"<select", r"<textarea", r"onclick", r"role=\"button\"", r"tabindex", r"<details", r"<summary", r"<img", r"data:image", r"<svg"):
    if re.search(pat, out): print("FORBIDDEN FOUND:", pat); fail += 1
print("title", TITLE, "pages", N, "source sha256", hashlib.sha256(RAW.encode()).hexdigest())
print("book sha256", hashlib.sha256(out.encode()).hexdigest(), "bytes", len(out.encode()))
print("FAIL" if fail else "verbatim: all quotes and source lines OK; no controls")
sys.exit(1 if fail else 0)
