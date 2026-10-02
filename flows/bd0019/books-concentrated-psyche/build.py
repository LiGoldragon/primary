#!/usr/bin/env python3
"""Builds «Concentrated psyche on the meta harness» from source.md (copied by extract.py); verifies every quote against raw records. No graph in this block, no illustrations, no controls."""
import html, re, subprocess, sys, hashlib, pathlib, json, glob
HERE = pathlib.Path(__file__).resolve().parent
PRIMARY = pathlib.Path("/home/li/primary"); PROJ = pathlib.Path("/home/li/.claude/projects/-home-li-primary")
esc = html.escape
TITLE = "Concentrated psyche on the meta harness"
RAW = (HERE / "source.md").read_text()

def norm(s): return re.sub(r"\s+", " ", s).strip()
def record(rel):
    p = PRIMARY / rel
    if p.exists(): t = p.read_text()
    else: t = subprocess.run(["git","-C",str(PRIMARY),"show",f"main:{rel}"],capture_output=True,text=True,check=True).stdout
    return norm(re.sub(r"\n>\s?", "\n", t))
def raw_texts(prefix, line):
    f = glob.glob(str(PROJ / f"{prefix}*.jsonl"))[0]
    with open(f) as fh:
        for i, l in enumerate(fh, 1):
            if i == line:
                r = json.loads(l); out = []
                if isinstance(r.get("content"), str): out.append(r["content"])
                m = r.get("message", {}).get("content")
                if isinstance(m, str): out.append(m)
                elif isinstance(m, list): out.append("".join(b.get("text","") for b in m if isinstance(b, dict)))
                if isinstance(r.get("attachment"), dict) and r["attachment"].get("prompt"): out.append(r["attachment"]["prompt"])
                return r, norm(" ".join(out))

# ---- parse source.md
lines = RAW.split("\n")
intro = lines[0]
sections, cur = [], None; opens = []
mode = "pts"
for ln in lines[1:]:
    if ln.startswith("## Open, for your word"): mode = "open"; continue
    if mode == "open":
        if ln.startswith("- "): opens.append(ln[2:])
        continue
    m = re.match(r"## (\d)\. (.*)$", ln)
    if m: cur = {"n": int(m.group(1)), "head": m.group(2), "q": []}; sections.append(cur); continue
    m = re.match(r'> "(.*)"$', ln)
    if m: cur["q"].append([m.group(1), None]); continue
    if ln.startswith("-- "): cur["q"][-1][1] = ln[3:]
assert len(sections) == 4 and len(opens) == 3 and all(q[1] for s in sections for q in s["q"])
nq = sum(len(s["q"]) for s in sections); assert nq == 19, nq
# every source line accounted for
rebuilt = {intro} | {f"## {s['n']}. {s['head']}" for s in sections} | {f'> "{t}"' for s in sections for t,_ in s["q"]} | {f"-- {p}" for s in sections for _,p in s["q"]} | {"## Open, for your word"} | {f"- {o}" for o in opens}
missing = [l for l in lines if l.strip() and l not in rebuilt]; assert not missing, missing

def inline(s):
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return re.sub(r"\*([^*]+?)\*", r"<em>\1</em>", s)
def quote(t, p, extra=""):
    return f'<blockquote class="living"><p class="said">{esc(t)}</p><p class="prov">{esc("-- "+p)}</p>{extra}</blockquote>'
def note(kind, words, date, body):
    verb = "agrees" if kind == "agree" else "disagrees"
    return f'<aside class="note {kind}"><p class="tag">Psyche Sonnet {verb}</p><p>On “{esc(words)}” ({date}): {esc(body)}</p></aside>'
def mark(label, body): return f'<p class="mark"><strong>{esc(label)}</strong>{esc(body)}</p>'
def txt(inner): return f'<section class="page txt"><div class="sheet">{inner}</div></section>'

MARKS = {
 1: [mark("Marks", "Three quotes carry the source’s own ellipses (the first, the fifth and the fourteenth); each piece between them is checked separately against the raw record. Typed and STT are as the source gives them. The raw transcripts carry no input mode, so they were read from the vision records, which agree except where marked. The raw transcript of flow e2a70a is not on this machine, so the “almost zero” quote is checked against flows/e2a70a/vision/codex-session-creation.md, which gives its words and the mark typed; the day and the line (L585, 17:11) come from the report on the psyche since 28 September.")],
 2: [mark("Mark", "The page-comment words on avoiding polling are from the vision record flows/7328f4/vision/hooks.md (page comment, 2026-09-30T18:47, STT). The raw transcript line that repeats them is a relayed task notification, so it is not used as the check. “The cluster needs to be able to not block itself” is marked STT by the source, and flows/fe945a/vision/cluster.md agrees, while flows/bd0019/vision/clusterNotBlocking.md says typed. The records differ, and the source’s STT stands as written.")],
 3: [mark("Mark", "The raw transcript for flow 1ac573 is not on this machine, so the 2026-09-17 reaping words are checked against flows/1ac573/vision/operational-reapReplacedSessions.md, where they are the opening of a longer sentence.")],
 4: [mark("Mark", "The first brackets are the source’s own: the raw record reads “Freshflow”, and the vision record corrects it to “a fresh flow”. The bracketed words are not the living’s as typed or heard.")],
}
NOTES = {
 1: note("agree", "Just create new sessions, which really should be done with almost zero LLM calls", "2026-10-01", "this is the line a restarted stack is built to keep: start from Flow, with the concentrated prompt composed by a program and one fat first prompt."),
 2: note("agree", "Nobody should be checking anything repeatedly.", "2026-10-01", "it is the sharpest statement on the page, and it settles the design of seat state: hooks report to Flow, and nothing watches a screen."),
}
ADD = [("I don't need to be able to see them in the chat. ... If it doesn't render it then there might be an advantage to that. Yeah maybe. Astra's vision is better.", "STT, 2026-10-01, to 6997eb"),
       ("Yeah the metadata is one datom line. That's brilliant. I love it. Let's do it.", "STT, 2026-10-01, to 6997eb")]
pages = []
for s in sections:
    inner = f'<p class="eyebrow">Point {s["n"]} of 4</p>'
    if s["n"] == 1: inner += f'<h2>{esc(TITLE)}</h2><p>{esc(intro)}</p><h3>{esc(s["head"])}</h3>'
    else: inner += f'<h2>{esc(s["head"])}</h2>'
    inner += "".join(quote(t, p) for t, p in s["q"])
    inner += NOTES.get(s["n"], "") + "".join(MARKS.get(s["n"], []))
    if s["n"] == 4:
        inner += ('<p class="eyebrow">Additions to point 4, relayed by Fable, not part of the source</p>'
                  + "".join(quote(t, p) for t, p in ADD) + mark("Mark", "These two quotes were added at Psyche Fable’s acceptance, relayed by Psyche Opus fe945a. They are not in the copied source text and are not Fable’s words. The first omits a sentence, as the relay does; the omitted sentence is in the raw record (6997eb L683), where the speech-to-text reads “pros”, which the vision record corrects to “prose”. Both match the raw record word for word."))
    pages.append(txt(inner))

OPEN_NOTE = note("agree", "imposing the old opinion on the new flow is the wrong approach", "2026-08-21", "the source’s reading, that only your own words pass forward, fits the later word of 2026-10-01 as well as this one. It stays a reading until you confirm it.")
SRC = ('<p class="prov">The source, verbatim: Psyche Opus fe945a, transcript fe945a2e-c785-4af4-9a46-766b6ea512e8.jsonl, line 1435, uuid 394f8933-743a-461f-a9bc-fc675c9f35e9, 2026-10-02T17:16:09Z, the second block between its to-the-living markers, titled «Concentrated psyche on the meta harness»; the marker lines and its Presentation line are not shown. It holds no graph, so this book draws none. The other block on that line is a separate book.</p>')
rul = "".join(f"<li>{inline(o)}</li>" for o in opens)
pages.append(txt('<p class="eyebrow">Open rulings</p><h2>Open, for your word</h2>' + f'<ul class="pts rulings" id="rulings">{rul}</ul>' + OPEN_NOTE +
    mark("Marks", "The “start flows, stop flows” words of 24 September are held by flows/88475f/vision/flow.md as relayed by e51411, with the original channel not stated. The 17 September words are held by flows/da1e3f/vision/operational-flowVsMessage.md, typed.") + SRC))
N = len(pages); dots = "".join('<span class="dot t"></span>' for _ in pages)
out = ((HERE/"shell.html").read_text().replace("{{TITLE}}", esc(TITLE)).replace("{{N}}", str(N)).replace("{{DOTS}}", dots).replace("{{PAGES}}", "\n".join(pages)))
out = out.replace("</style>", "h3{font:600 17px/1.3 var(--display);margin:0;color:var(--muted)}\n</style>", 1)
(HERE/"book.html").write_text(out)

# ---- verification
REF = {  # text start -> ("raw", prefix, line) | ("file", rel)
 "one block of text": ("raw","752e0f",427), "If we need to inject": ("raw","752e0f",595),
 "Starting a new session": ("raw","b81560",923), "Just create new sessions": ("file","flows/e2a70a/vision/codex-session-creation.md"),
 "Maybe we can even resume": ("raw","7328f4",898), "When that order comes in": ("file","flows/7328f4/vision/hooks.md"),
 "we shouldn't let the models compact": ("raw","6cc91b",1886), "Essentially we want to avoid polling": ("file","flows/7328f4/vision/hooks.md"),
 "Nobody should be checking": ("raw","fe945a",1031), "It makes perfect sense": ("raw","fe945a",1031),
 "The cluster needs": ("raw","bd0019",816), "When a session gets replaced": ("file","flows/1ac573/vision/operational-reapReplacedSessions.md"),
 "Everything that has a big context": ("raw","93ba9f",453), "Nothing is up to me": ("raw","93ba9f",297),
 "For me subagents": ("raw","fe945a",934), "And to be clear, now vision": ("raw","fe945a",1155),
 "the books become": ("raw","fe945a",977), "Files are not really": ("raw","bd0019",881),
 "Let's try to diminish": ("raw","7328f4",442),
}
fail = 0
def segs(t): return [x.strip() for x in re.split(r"\s*\.\.\.\s*|\[[^\]]*\]", t) if x.strip()]
def check(label, text, ref):
    global fail
    if ref[0] == "file": pool = record(ref[1]); where = ref[1]
    else:
        r, pool = raw_texts(ref[1], ref[2]); where = f"{ref[1]} L{ref[2]} {r.get('type')} {r.get('timestamp')}"
        if r.get("type") not in ("user","queue-operation","attachment"): fail += 1; print("NOT A HUMAN RECORD", where)
    bad = [s for s in segs(text) if norm(s) not in pool]
    print(("ok   " if not bad else "FAIL ") + label[:44].ljust(44), where, bad[:1]); fail += bool(bad)
P = html.unescape(re.sub(r"<[^>]+>", "", out))
for s in sections:
    for t, p in s["q"]:
        ref = next(v for k, v in REF.items() if t.startswith(k)); check(t, t, ref)
        if t not in P or p not in P: print("MISSING FROM BOOK", t[:40]); fail += 1
assert "Freshflow" in raw_texts("fe945a",934)[1]
for t, ref in [(ADD[0][0], ("raw","6997eb",683)), (ADD[1][0], ("raw","6997eb",1114))]:
    check(t, t, ref)
    if t not in P: print("MISSING FROM BOOK", t[:40]); fail += 1
# open-section quotes
OPEN_REF = [("there's no handoff file; the flow *reads its previous flow(s)*", ("file","flows/5c8be3ca/vision/flowArtifacts.md")),
 ("imposing the old opinion on the new flow is the wrong approach.", ("file","flows/5c8be3ca/vision/flowArtifacts.md")),
 ("Let's always get the concentrated vision from the current flow into the next one.", ("file","flows/fe945a/vision/concentratedVision.md")),
 ("I don't want subflows to start creating their own lanes. They just use their parents.", ("file","flows/01a05826/vision/subflowIdentity.md")),
 ("if the subflow is independent and can reply to a successor ... then we have an asynchronous system.", ("raw","f38926",774)),
 ("no, message, not flow-send. use the message nexus!", ("file","flows/da1e3f/vision/operational-flowVsMessage.md")),
 ("I want to be able to start flows, stop flows, and send messages with Flow because it gives me the bare input.", ("file","flows/88475f/vision/flow.md"))]
for t, ref in OPEN_REF:
    check(t, t, ref)
    if t.replace("*","") not in P: print("MISSING FROM BOOK", t[:40]); fail += 1
for l in lines:
    if not l.strip(): continue
    t = re.sub(r"^(## |- |> |-- )", "", l).replace("**","").replace("*","")
    t = re.sub(r"^\d\. ", "", t) if l.startswith("## ") else t
    t = t.strip('"') if l.startswith("> ") else t
    if t not in P: print("SOURCE LINE NOT IN BOOK:", t[:70]); fail += 1
if out.count("<pre"): print("pre blocks", out.count("<pre")); fail += 1
for pat in (r"<button", r"<a\s", r"<input", r"<select", r"<textarea", r"onclick", r'role="button"', r"tabindex", r"<details", r"<img", r"data:image", r"mermaid"):
    if re.search(pat, out): print("FORBIDDEN:", pat); fail += 1
print("pages", N, "source sha256", hashlib.sha256(RAW.encode()).hexdigest()); print("book sha256", hashlib.sha256(out.encode()).hexdigest(), len(out.encode()))
print("FAIL" if fail else "ALL VERBATIM; no controls"); sys.exit(1 if fail else 0)
