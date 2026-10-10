#!/usr/bin/env python3
"""Builds «Six questions on sessions, re-asked» from source.md (copied by extract.py) and verifies source text and every quote.
No illustration files, no Mermaid in this block; no controls."""
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
TITLE = "Six questions on sessions, re-asked"
secs = RAW.split("\n## Rulings\n")
assert len(secs) == 2
head_md, rul_md = secs[0], secs[1]
hl, *rest = head_md.strip("\n").split("\n")
assert hl == "## " + TITLE
items = [x for x in rest if x.strip()]
assert len(items) == 4 and all(x.startswith(f"{i}. ") for i, x in enumerate(items, 1))
rulings = [x[2:] for x in rul_md.strip("\n").split("\n") if x.strip()]
assert len(rulings) == 3 and all(x.startswith("- ") for x in rul_md.strip("\n").split("\n"))

def inline(s):
    out = []
    for p in re.split(r"(`[^`]+`)", s):
        if p.startswith("`"): out.append(f"<code>{esc(p[1:-1])}</code>")
        else: out.append(re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", esc(p)))
    return "".join(out)

def R(session, line, uuid): return ("raw", session, line, uuid)
Q = {
 "arg": (("file","flows/9993b5/vision/easyFlowDispatch.md"), "Let's predefine them so that there's basically no argument to give except a small description of the goal, and it can find the information it needs.",
         "-- the living, 2026-09-17, flow 9993b5, typed, `flows/9993b5/vision/easyFlowDispatch.md`"),
 "zero": (("file","flows/6997eb/reports/psyche-since-28-september.md"), "Just create new sessions, which really should be done with almost zero LLM calls, but not quite zero: very, very small calls that would be extremely fast and cost almost nothing.",
         "-- the living, 2026-10-01 17:11, flow e2a70a, line 585, typed, as gathered in `flows/6997eb/reports/psyche-since-28-september.md`"),
 "poll": (("file","flows/6997eb/reports/psyche-since-28-september.md"), "Essentially we want to avoid polling, which means we're going to make this hook-based.",
         "-- the living, 2026-09-30 17:16, flow 7328f4, line 552, speech to text, as gathered in `flows/6997eb/reports/psyche-since-28-september.md`"),
 "nobody": (("file","flows/fe945a/vision/polling.md"), "Nobody should be checking anything repeatedly.",
         "-- the living, 2026-10-01, flow fe945a, a comment on the book «Where books go, and the anatomy of the book pipeline», `flows/fe945a/vision/polling.md`"),
 "reap": (("file","flows/1ac573/vision/operational-reapReplacedSessions.md"), "When a session gets replaced, it has to be reaped so it doesn't keep getting messages.",
         "-- the living, 2026-09-17, flow 1ac573, `flows/1ac573/vision/operational-reapReplacedSessions.md`"),
 "parents": (("file","flows/01a05826/vision/subflowIdentity.md"), "I don't want subflows to start creating their own lanes. They just use their parents.",
         "-- the living, 2026-08-31 14:53, flow 01a058, typed, `flows/01a05826/vision/subflowIdentity.md`"),
 "indep": (R("f38926bb-95bb-469d-83f1-3f5f0ff523d7",774,None), "if the subflow is independent and can reply to a successor of whoever it's supposed to respond to, then we have an asynchronous system.",
         "-- the living, 2026-09-19 22:33, spoken to PsycheHigh in the terminal, input mode not established, transcript f38926 line 774"),
 "skill": (R("fe945a2e-c785-4af4-9a46-766b6ea512e8",934,None), "For me subagents are a type of skill. They're a skill that is implemented by Freshflow basically.",
         "-- the living, 2026-10-01 19:54, a comment, transcript fe945a line 934; “Freshflow” is kept as written there and the source reads it as “a fresh flow”"),
 "old": (("file","flows/5c8be3ca/vision/flowArtifacts.md"), "imposing the old opinion on the new flow is the wrong approach.",
         "-- the living, 2026-08-21, design session 5c8be3ca, typed, `flows/5c8be3ca/vision/flowArtifacts.md`"),
 "conc": (("file","flows/fe945a/vision/concentratedVision.md"), "Let's always get the concentrated vision from the current flow into the next one.",
         "-- the living, 2026-10-01, flow fe945a, speech to text, `flows/fe945a/vision/concentratedVision.md`"),
 "verb": (("file","flows/fe945a/vision/concentratedVision.md"), "with the verbatim psyche that supports all of it attached to it.",
         "-- the same words of 2026-10-01, flow fe945a, speech to text"),
}
def quote(k, label=None):
    _, text, prov = Q[k]
    prov = re.sub(r"`([^`]+)`", r"\1", prov)
    return f'<blockquote class="living" data-q="{k}"><p class="said">{esc(text)}</p><p class="prov">{esc(prov)}</p></blockquote>'
def note(kind, words, date, body):
    verb = "agrees" if kind == "agree" else "disagrees"
    return (f'<aside class="note {kind}" data-note="{kind}"><p class="tag">Psyche Sonnet {verb}</p><p>On “{esc(words)}” ({date}): {esc(body)}</p></aside>')
def txt(inner): return f'<section class="page txt"><div class="sheet">{inner}</div></section>'
def eyebrow(t): return f'<p class="eyebrow">{t}</p>'
def question(n):
    num, body = items[n-1].split(". ", 1)
    return f'<section class="qs" id="q{n}"><p><span class="qn">{num}</span>{inline(body)}</p></section>'

NOTES = {
 1: note("agree", "almost zero LLM calls", "2026-10-01", "the re-asked question keeps to it: Flow composes the prompt itself from the concentrated vision, so starting a seat spends no model call."),
 2: note("agree", "Nobody should be checking anything repeatedly", "2026-10-01", "the re-asked question removes the last checker: one registry in Flow, fed by hooks, and a messenger that holds nothing it cannot deliver."),
 3: note("agree", "so it doesn't keep getting messages", "2026-09-17", "the single act of succession moves the route and retires the predecessor in one step, so no old pane keeps receiving."),
 4: note("agree", "if the subflow is independent and can reply to a successor", "2026-09-19", "the source does not pick between the 31 August and 19 September words. It names the tension and puts it to you."),
}
ps = [
 txt(eyebrow("Question 1 of 4") + f'<h2>{esc(TITLE)}</h2>' + question(1) + quote("arg") + quote("zero") + NOTES[1]),
 txt(eyebrow("Question 2 of 4") + question(2) + quote("poll") + quote("nobody") + NOTES[2]),
 txt(eyebrow("Question 3 of 4") + question(3) + quote("reap") + NOTES[3]),
 txt(eyebrow("Question 4 of 4") + question(4) + quote("parents") + quote("indep") + quote("skill") + NOTES[4]),
]
rul = "".join(f"<li>{inline(r)}</li>" for r in rulings)
NOTE5 = note("agree", "Let's always get the concentrated vision from the current flow into the next one", "2026-10-01",
             "the source's reading that this later word governs holds, because the same words attach the verbatim psyche to the vision, which is not the opinion the 21 August word warns against. The reading remains the source's inference and is yours to rule on.")
MARK = ('<p class="mark"><strong>Count</strong> The source’s title says six questions. The block as written holds four, and this book shows those four.</p>')
SRC_PROV = ('<p class="prov">The source, verbatim: Psyche Fable 6997eb, transcript 6997eb8a-30eb-49a1-a787-45279164a43b.jsonl, '
            'line 2463, uuid 6b5b3514-62e7-4393-9af4-bc2ccd8694ed, 2026-10-02T17:13:32Z, the block between its to-the-living markers titled «Six questions on sessions, re-asked»; '
            'the marker lines and its Presentation datom line are not shown. It holds no graph, so this book draws none.</p>')
ps.append(txt(eyebrow("The rulings you are asked for") + "<h2>Rulings</h2>" + f'<ul class="pts rulings" id="rulings">{rul}</ul>' + quote("old") + quote("conc") + quote("verb") + NOTE5 + MARK + SRC_PROV))
pages = ps; N = len(pages)
dots = "".join('<span class="dot t"></span>' for _ in pages)
out = ((HERE / "shell.html").read_text().replace("{{TITLE}}", esc(TITLE)).replace("{{N}}", str(N))
       .replace("{{DOTS}}", dots).replace("{{PAGES}}", "\n".join(pages)))
out = out.replace("</style>", ".qs p{margin:0}.qn{font:600 20px/1 var(--display);color:var(--red);margin-right:.5em}\n</style>", 1)
(HERE / "book.html").write_text(out)

fail = 0
def plain(h): return html.unescape(re.sub(r"<[^>]+>", "", h))
P = plain(out)
for k, (src, text, _) in Q.items():
    if src[0] == "file": ok = text in flat(record(src[1])); where = src[1]
    else:
        r = raw_line(src[1], src[2]); ok = r["type"] == "user" and text in raw_text(r).replace("\n"," "); where = f"{src[1][:6]} line {src[2]} {r['timestamp']}"
    print(("quote ok: " if ok else "QUOTE NOT VERBATIM IN RECORD "), k, where); fail += (not ok)
    if text not in P: print("QUOTE MISSING FROM BOOK", k); fail += 1
# every quoted phrase inside the source also lives in the living's words
for ph in ["no argument to give except a small description of the goal","almost zero LLM calls","avoid polling","hook-based","Nobody should be checking anything repeatedly.","so it doesn't keep getting messages","just use their parents","independent and can reply to a successor","subagents are a type of skill","implemented by a fresh flow","imposing the old opinion on the new flow is the wrong approach"]:
    inq = any(ph.lower() in q[1].lower() for q in Q.values())
    print(("source phrase backed: " if inq else "SOURCE PHRASE NOT BACKED (see note): "), ph)
for line in RAW.split("\n"):
    if not line.strip(): continue
    t = re.sub(r"^(## |- |\d\. )", "", line).strip().replace("`","").replace("**","")
    if t not in P: print("SOURCE LINE NOT VERBATIM:", t[:70]); fail += 1
print("pre blocks", out.count("<pre"))
if out.count("<pre"): fail += 1
for pat in (r"<button", r"<a\s", r"<input", r"<select", r"<textarea", r"onclick", r"addEventListener\('click'", r'role="button"', r"tabindex", r"<details", r"<summary", r"<img", r"data:image"):
    if re.search(pat, out): print("FORBIDDEN FOUND:", pat); fail += 1
print("title", TITLE, "pages", N, "source sha256", hashlib.sha256(RAW.encode()).hexdigest())
print("book sha256", hashlib.sha256(out.encode()).hexdigest(), "bytes", len(out.encode()))
print("FAIL" if fail else "verbatim: all quotes and source lines OK; no controls")
sys.exit(1 if fail else 0)
