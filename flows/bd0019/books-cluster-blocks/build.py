#!/usr/bin/env python3
"""Builds «The cluster never blocks itself» from source.md (copied by extract.py) and verifies the source
text, the one living quote, and that the page has no controls. No illustration, no graph: the source has none."""
import html, re, sys, hashlib, pathlib, json
HERE = pathlib.Path(__file__).resolve().parent
PROJ = pathlib.Path("/home/li/.claude/projects/-home-li-primary")
esc = html.escape
RAW = (HERE / "source.md").read_text()
first, rest = RAW.split("\n", 1)
m = re.fullmatch(r"`Presentation\.\{ «(.+)» \}`", first); assert m, first
TITLE = m.group(1); assert TITLE == "The cluster never blocks itself"
paras = [p for p in rest.strip("\n").split("\n\n")]
assert len(paras) == 4 and all(p.startswith("**") for p in paras)

def inline(s):
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", esc(s))

S = ("bd0019dd-faeb-46b1-8ea6-f7423af3e6e6", 816, "c8ab32e1-8c3d-49ea-b373-a155c9fd4425")
QT = "The cluster needs to be able to not block itself."
PROV = "-- the living, 2026-10-01T19:47:22Z, to Psyche Sonnet bd0019 · transcript bd0019dd, line 816 · flows/bd0019/vision/clusterNotBlocking.md"
def quote():
    return (f'<blockquote class="living"><p class="said">{esc(QT)}</p><p class="prov">{esc(PROV)}</p></blockquote>')
def note(words, date, body):
    return (f'<aside class="note agree"><p class="tag">Psyche Sonnet agrees</p><p>On “{esc(words)}” ({date}): {esc(body)}</p></aside>')
SRC = ('<p class="prov">The source, verbatim: Psyche Opus fe945a, transcript fe945a2e-c785-4af4-9a46-766b6ea512e8.jsonl, '
       'line 855, uuid b942a2f7-61af-4580-9d74-1c42bc22d05e, 2026-10-01T19:53:03Z, between its to-the-living markers. '
       'Its first line, Presentation.{ «The cluster never blocks itself» }, gives this book its title and is not shown.</p>')
def txt(n, p, extra=""):
    return (f'<section class="page txt"><div class="sheet"><p class="eyebrow">Point {n} of 4</p>'
            f'<div class="src"><p>{inline(p)}</p></div>{extra}</div></section>')
pages = [
 txt(1, paras[0] + "", ""),
 txt(2, paras[1], note("The cluster needs to be able to not block itself", "2026-10-01",
     "a hook that answers every permission question at once is that sentence made mechanical: nothing waits on a person.") + quote()),
 txt(3, paras[2]),
 txt(4, paras[3]),
]
pages[0] = pages[0].replace('<div class="src">', SRC + '<div class="src">', 1)
N = len(pages)
dots = "".join('<span class="dot t"></span>' for _ in pages)
shell = (HERE / "shell.html").read_text()
out = (shell.replace("{{TITLE}}", esc(TITLE)).replace("{{N}}", str(N)).replace("{{DOTS}}", dots).replace("{{PAGES}}", "\n".join(pages)))
(HERE / "book.html").write_text(out)

fail = 0
P = html.unescape(re.sub(r"<[^>]+>", "", out))
with open(PROJ / f"{S[0]}.jsonl") as fh:
    for i, l in enumerate(fh, 1):
        if i == S[1]: r = json.loads(l); break
c = r["message"]["content"]; c = c if isinstance(c, str) else "".join(b.get("text", "") for b in c if isinstance(b, dict))
if not (r["uuid"] == S[2] and r["type"] == "user" and QT in c and r["timestamp"].startswith("2026-10-01T19:47:22")):
    print("QUOTE NOT VERBATIM IN RAW"); fail += 1
if QT not in P: print("QUOTE MISSING"); fail += 1
for p in paras:
    for piece in p.replace("`", "").split("**"):
        if piece.strip() and piece not in P: print("SOURCE NOT VERBATIM:", piece[:60]); fail += 1
if out.count("<pre") or "mermaid" in out.lower() or "<svg" in out or "<img" in out: print("PRE/GRAPH/IMG FOUND"); fail += 1
for pat in (r"<button", r"<a\s", r"<input", r"<select", r"<textarea", r"onclick", r"role=\"button\"", r"tabindex", r"<details"):
    if re.search(pat, out): print("CONTROL FOUND:", pat); fail += 1
print("title", TITLE, "pages", N, "source sha256", hashlib.sha256(RAW.encode()).hexdigest())
print("FAIL" if fail else "verbatim: quote and source OK; no controls")
sys.exit(1 if fail else 0)
