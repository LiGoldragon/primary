#!/usr/bin/env python3
"""Builds «Skill proposals from Psyche Fable» from source.md (copied by extract.py) and verifies the
source text, the living quotes, and that the page has no controls, code blocks or images."""
import html, re, hashlib, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
PRIMARY = pathlib.Path("/home/li/primary")
esc = html.escape
flat = lambda s: re.sub(r"\s*\n>\s*", " ", s)
RAW = (HERE / "source.md").read_text()
first, rest = RAW.split("\n", 1)
m = re.fullmatch(r"Presentation\.\{ «(.+)» \}", first); assert m
TITLE = m.group(1); assert TITLE == "Skill proposals from Psyche Fable"
BODY = rest.strip("\n")
main_part, rulings = BODY.split("\n\n## Rulings\n\n")
head, intro, *items = main_part.split("\n\n")
assert head == "## Skill proposals from Psyche Fable" and len(items) == 4, (head, len(items))

def inline(s):
    return "".join(f"<code>{esc(p[1:-1])}</code>" if p.startswith("`") else esc(p) for p in re.split(r"(`[^`]+`)", s))
def parse(n):
    mm = re.fullmatch(r"(\d)\. \*\*(.+?)\*\* (.*)", items[n-1], re.S)
    assert mm and int(mm.group(1)) == n, n
    return mm.group(2), mm.group(3)

Q = {
 "transcript": ("flows/fe945a/vision/transcriptOverFiles.md", "What do you mean the prompt is committed? It's in your transcript.",
   "-- psyche, typed, 2026-09-29, to Psyche Opus 183ae0 · flows/fe945a/vision/transcriptOverFiles.md"),
 "nocopy": ("flows/e51411/vision/refresh.md", "The tool gets the right block of text because it has the right reference so we don't need to make a copy of anything. It just fetches it programmatically.",
   "-- living, 2026-09-24, to Mind Astra 47764b · flows/e51411/vision/refresh.md"),
}
def quote(k):
    _, t, p = Q[k]
    return f'<blockquote class="living" data-q="{k}"><p class="said">{esc(t)}</p><p class="prov">{esc(p)}</p></blockquote>'
def txt(cls, inner): return f'<section class="page txt {cls}"><div class="sheet">{inner}</div></section>'

PROV = ('<p class="prov">The source, verbatim: Psyche Fable, transcript 6997eb8a-30eb-49a1-a787-45279164a43b.jsonl, '
        'line 1468, uuid 6f84fff2-3ef5-4802-94d8-2a3c43732726, 2026-10-01T19:55:42Z, between its to-the-living markers. '
        'Its first line, the datom Presentation.{ «Skill proposals from Psyche Fable» }, gives this book its title and is not shown.</p>')

def point(n, extra=""):
    lead, body = parse(n)
    segs = re.split(r'("[^"]+")', body)
    parts = []
    for sg in segs:
        if not sg.strip(): continue
        if sg.startswith('"'):
            parts.append(f'<p class="skilltext">“{inline(sg[1:-1])}”</p>')
        else:
            parts.append(f'<p>{inline(sg.strip())}</p>')
    return txt("prop", f'<p class="eyebrow">Proposal {n} of 4</p><div class="src" data-p="{n}"><h2>{esc(lead)}</h2>'
        + "".join(parts) + '</div>' + extra)

# the quoted skill text keeps the source's straight quotes in the data; the page sets them as curly marks,
# so verification compares the text between the quotes.
note4 = ('<aside class="note agree"><p class="tag">Psyche Sonnet agrees</p>'
  '<p>On “It\'s in your transcript” (2026-09-29) and “we don\'t need to make a copy of anything” (2026-09-24): '
  'the proposal that the book’s source is the transcript record, taken by location and never copied, is these two sentences made into a rule.</p></aside>')
pages = [
 txt("cover", f'<p class="eyebrow">Presented by Psyche Fable</p><h2>{esc(TITLE)}</h2><p>{esc(intro)}</p>'
     '<p class="mark"><strong>Four proposals</strong> Each is exact skill text, set in a quoted panel. Swipe or scroll down; use the arrow keys on a keyboard.</p>' + PROV),
 point(1), point(2), point(3),
 point(4, quote("transcript") + quote("nocopy") + note4),
 txt("rul", '<p class="eyebrow">Asked of you</p><div class="src"><h2>Rulings</h2></div>'
     f'<ol class="props">' + "".join(f'<li><span class="n">{i}</span><span>{inline(b[2:])}</span></li>' for i, b in enumerate(rulings.split("\n"), 1)) + '</ol>'
     '<p class="mark"><strong>Ruling it needs</strong> The end of proposal 4 asks you one thing: pages scroll down, or swipe. This book scrolls down and also answers to arrow keys.</p>'
     '<p class="mark"><strong>Landed</strong> None of the four was seen landed when this book was made; nothing is badged.</p>'),
]
N = len(pages)
dots = "".join('<span class="dot t"></span>' for _ in pages)
out = (HERE/"shell.html").read_text().replace("{{TITLE}}", esc(TITLE)).replace("{{N}}", str(N)).replace("{{DOTS}}", dots).replace("{{PAGES}}", "\n".join(pages))
(HERE/"book.html").write_text(out)

fail = 0
plain = lambda h: html.unescape(re.sub(r"<[^>]+>", "", h))
P = plain(out)
for k, (f, t, _) in Q.items():
    rec = (PRIMARY/f).read_text()
    if t not in flat(rec): print("QUOTE NOT IN RECORD", k); fail += 1
    if t not in P: print("QUOTE NOT IN BOOK", k); fail += 1
for line in BODY.split("\n"):
    t = re.sub(r"^(## |\d\. |- )", "", line).replace("`", "").replace("**", "")
    t = t.strip()
    if not t or re.match(r"\d\. ", line): continue
    # skill text: compare with straight quotes mapped to the curly marks the page sets
    t2 = re.sub(r'"(.+?)"', lambda mm: "“" + mm.group(1) + "”", t, count=1) if re.match(r"^[a-z\-]+, ", t) is None and False else t
    if t not in P:
        t3 = re.sub(r' "(.+?)" ', lambda mm: " “" + mm.group(1) + "” ", t, count=1)
        if t3 not in P and t.replace('"', "") not in P.replace("“", "").replace("”", ""):
            print("SOURCE LINE NOT VERBATIM:", t[:70]); fail += 1
for n in range(1, 5):
    lead, body = parse(n)
    if lead not in P: print("LEAD MISSING", n); fail += 1
    if f"{n}. **{lead}** {body}" != items[n-1]: print("ITEM MISMATCH", n); fail += 1
    for sg in re.split(r'"[^"]+"|', ""): pass
    flatbody = body.replace("`", "").replace('"', "")
    Pn = P.replace("“", "").replace("”", "")
    for sg in re.split(r'"([^"]+)"', body):
        sg = sg.replace("`", "").strip()
        if sg and sg not in P: print("ITEM TEXT MISSING", n, sg[:50]); fail += 1
for pat in (r"<button", r"<a\s", r"<input", r"<select", r"<textarea", r"onclick", r"<img", r"<svg", r"<pre", r"tabindex", r"<details", r"role=\"button\""):
    if re.search(pat, out): print("FOUND", pat); fail += 1
print("title", TITLE, "pages", N, "source sha256", hashlib.sha256(RAW.encode()).hexdigest())
print("book sha256", hashlib.sha256(out.encode()).hexdigest(), len(out))
print("FAIL" if fail else "OK: source, quotes verbatim; no controls, images, code blocks")
sys.exit(1 if fail else 0)
