#!/usr/bin/env python3
"""Builds «Two kinds of output» (the same artifact as «Marking a presentation for the living»,
retitled) from source-two-kinds.md, svg/ and the living's records, and verifies the source,
every quote, and that the page has no buttons or clickable controls."""
import html, re, subprocess, sys, hashlib, pathlib

HERE = pathlib.Path(__file__).resolve().parent
VISION = pathlib.Path("/home/li/primary/flows/6997eb/vision")
esc = html.escape

def vision(name):
    p = VISION / name
    if p.exists():
        return p.read_text()
    return subprocess.run(["git", "-C", "/home/li/primary", "show", f"main:flows/6997eb/vision/{name}"],
                          capture_output=True, text=True, check=True).stdout

RAW = (HERE / "source-two-kinds.md").read_text()
fence = re.match(r"```yaml\n(.*?)\n```\n", RAW, re.S)
meta = dict(l.split(": ", 1) for l in fence.group(1).splitlines())
TITLE = meta["title"]
assert TITLE == "Two kinds of output"
BODY = RAW[fence.end():].strip("\n")           # the metadata is not shown
main_part, open_part = BODY.split("\n\n## Open\n\n")
head, *items = main_part.split("\n\n")
assert head == "## Two kinds of output" and len(items) == 4

def inline(s):
    parts = re.split(r"(`[^`]+`)", s)
    return "".join(f"<code>{esc(p[1:-1])}</code>" if p.startswith("`") else esc(p) for p in parts)

def item(n):
    m = re.match(r"(\d)\. \*\*(.+?)\*\* (.*)", items[n - 1], re.S)
    assert m and int(m.group(1)) == n
    return m.group(2), m.group(3)

D = "-- psyche, STT, 2026-10-01 · flows/6997eb/vision/"
Q = {
 "separate": ("presentation.md",
   "Okay put together a book now that you've wrapped your head around this way of separating the psyche or the living directed output from the more machine- and intent-free output, which is everything else.",
   D + "presentation.md"),
 "render": ("presentation.md",
   "I don't need to be able to see them in the chat. I think if we keep everything else that the machine says to a more mechanical logging-like behavior, then it'll be obvious when it's actually talking in [prose] and talking to me. If it doesn't render it then there might be an advantage to that. Yeah maybe. Astra's vision is better.",
   D + "presentation.md · transcription corrected: \"pros\" → \"[prose]\""),
 "markers": ("presentation.md",
   "Front matter is only at the beginning. I'm not taking out the markers here.",
   D + "presentation.md"),
 "sender": ("presentation.md",
   "You don't need to say who it's from because we know from which transcript we're getting it from.",
   D + "presentation.md"),
 "everywhere": ("presentation.md",
   "So what's going on here? You only gave me a title. Are you just knee-jerk putting front matter everywhere now?",
   D + "presentation.md"),
 "logging": ("commentary.md",
   "Whenever something happens there can be some small mention, very condensed, of it. It'll mostly be for machine stuff eventually, all of this logging, but let's minimize.",
   D + "commentary.md"),
}

def quote(k):
    _, text, prov = Q[k]
    return (f'<blockquote class="living" data-q="{k}"><p class="said">{esc(text)}</p>'
            f'<p class="prov">{esc(prov)}</p></blockquote>')

def note(kind, words, body):
    verb = "agrees" if kind == "agree" else "disagrees"
    return (f'<aside class="note {kind}"><p class="tag">Psyche Sonnet {verb}</p>'
            f'<p>On “{esc(words)}” (2026-10-01): {esc(body)}</p></aside>')

def mark(label, body):
    return f'<p class="mark"><strong>{label}</strong> {esc(body)}</p>'

def ill(name, caption):
    return (f'<section class="page ill"><figure>{(HERE / "svg" / name).read_text()}'
            f'<figcaption>{esc(caption)}</figcaption></figure></section>')

def txt(inner):
    return f'<section class="page txt"><div class="sheet">{inner}</div></section>'

def point(n, extra=""):
    lead, rest = item(n)
    return txt(f'<p class="eyebrow">Point {n} of 4</p><div class="src"><h2>{esc(lead)}</h2>'
               f'<p>{inline(rest)}</p></div>' + extra)

SRC_PROV = ('<p class="prov">The source, verbatim: Psyche Fable 6997eb, transcript '
            '6997eb8a-30eb-49a1-a787-45279164a43b.jsonl, line 844, uuid 43f51a8b-658e-4aeb-a9d7-6d87d42b6ec1, '
            '2026-10-01T18:20:03Z, between its to-the-living markers.</p>')

bullets = [b[2:] for b in open_part.split("\n")]
assert len(bullets) == 2 and all(b for b in bullets)
props = "".join(f'<li><span class="n">{i}</span><span>{inline(b)}</span></li>' for i, b in enumerate(bullets, 1))

pages = [
 ill("tk-1-cover.svg", "One stream from the machine, parted in two: a log, and prose to you."),
 point(1, SRC_PROV + quote("separate")
       + mark("Mark", "The source quotes “talking in prose”; the record holds “[prose]”, the transcription corrected from “pros”.")),
 ill("tk-2-unseen.svg", "The marks are there for the tool. Rendered, they vanish."),
 point(2, quote("render") + quote("markers")
       + mark("Mark", "The source joins “If it doesn't render it then there might be an advantage to that.” to “Astra's vision is better.” and leaves out, without an ellipsis, the words between them: “Yeah maybe.”")),
 ill("tk-3-tag.svg", "One tag, tied where the block opens. It names the book."),
 point(3, quote("sender")
       + note("agree", "You don't need to say who it's from",
              "the transcript already names the seat, so the tag carries only what nothing else can, the title.")),
 ill("3-hook.svg", "A hook on each harness lifts the wrapped block out of the finished reply."),
 point(4, quote("everywhere") + quote("logging")
       + note("agree", "Are you just knee-jerk putting front matter everywhere now?",
              "a conversational answer carries no markers and no metadata; only a block meant for a book is wrapped.")),
 ill("tk-5-open.svg", "Two questions the source leaves open."),
 txt('<p class="eyebrow">Still open</p><div class="src"><h2>Open</h2></div>'
     + f'<ol class="props">{props}</ol>' + SRC_PROV
     + mark("Not landed", "Neither item is badged landed: no hook and no chosen metadata form was seen landed when this book was made.")),
]

N = len(pages)
dots = "".join(f'<span class="dot{" t" if "page txt" in p[:40] else ""}"></span>' for p in pages)
shell = (HERE / "shell-two-kinds.html").read_text()
out = (shell.replace("{{TITLE}}", esc(TITLE)).replace("{{N}}", str(N))
            .replace("{{DOTS}}", dots).replace("{{PAGES}}", "\n".join(pages)))
(HERE / "book-two-kinds.html").write_text(out)

# ---- verification ----
fail = 0
def plain(h):
    return html.unescape(re.sub(r"<[^>]+>", "", h))
P = plain(out)
for k, (f, text, _) in Q.items():
    if text not in vision(f):
        print("QUOTE NOT VERBATIM IN RECORD", k, f); fail += 1
    if text not in P:
        print("QUOTE MISSING FROM BOOK", k); fail += 1
# every source paragraph, markdown syntax removed, verbatim in the book
for para in [head, "## Open"] + bullets:
    if para.replace("## ", "").replace("`", "") not in P:
        print("SOURCE PARAGRAPH NOT VERBATIM:", para[:70]); fail += 1
for n in range(1, 5):   # each item: bold lead as the page heading, the rest as its paragraph
    l, r = item(n)
    if l not in P or r.replace("`", "") not in P or f"{n}. **{l}** {r}" != items[n - 1]:
        want = items[n - 1]
        print("SOURCE PARAGRAPH NOT VERBATIM:", want[:70]); fail += 1
# the source's own quotes of the living, against the records
recs = vision("presentation.md") + vision("commentary.md")
for qt in re.findall(r'"([^"]+)"', BODY):
    for frag in qt.split(" ... "):
        f2 = frag.rstrip(".")
        if f2 not in recs and f2.replace("in prose", "in [prose]") not in recs:
            # try splitting at sentence joins the source made
            pieces = [s.rstrip(".") for s in re.split(r"(?<=\.) ", frag)]
            miss = [s for s in pieces if s not in recs]
            print("SOURCE QUOTE FRAGMENT", repr(frag[:60]), "pieces missing:", miss)
            if miss: fail += 1
        else:
            print("source quote ok:", frag[:50], "(via [prose])" if f2 not in recs else "")
# no buttons, no clickable controls
for pat in (r"<button", r"<a\s", r"<input", r"<select", r"onclick", r"addEventListener\('click'", r'role="button"', r"tabindex"):
    if re.search(pat, out):
        print("CONTROL FOUND:", pat); fail += 1
# prose never in a code block
if "<pre" in out:
    print("PRE BLOCK FOUND"); fail += 1
print("title", TITLE, "pages", N, "source sha256", hashlib.sha256(RAW.encode()).hexdigest())
print("book sha256", hashlib.sha256(out.encode()).hexdigest(), "bytes", len(out.encode()))
print("FAIL" if fail else "verbatim: all quotes and source paragraphs OK; no controls")
sys.exit(1 if fail else 0)
