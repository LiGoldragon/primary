#!/usr/bin/env python3
"""Builds «Marking a presentation for the living» from source.md, the svg/ folder
and the living's records, and verifies every quote and the source verbatim."""
import html, re, subprocess, sys, hashlib, pathlib

HERE = pathlib.Path(__file__).resolve().parent
TITLE = "Marking a presentation for the living"
VISION = pathlib.Path("/home/li/primary/flows/6997eb/vision")
esc = html.escape

def vision(name):
    p = VISION / name
    if p.exists():
        return p.read_text()
    return subprocess.run(["git", "-C", "/home/li/primary", "show", f"main:flows/6997eb/vision/{name}"],
                          capture_output=True, text=True, check=True).stdout

SRC = (HERE / "source.md").read_text()
heading1 = "## The marker: two instincts"
heading2 = "## Ruling"
marker_part = SRC[:SRC.index(heading2)].rstrip("\n")
ruling_part = SRC[SRC.index(heading2):]

def md(block):
    """Minimal verbatim render: headings and paragraphs, inline code. No word changes."""
    out = []
    for para in block.split("\n\n"):
        if para.startswith("## "):
            out.append(f'<h2 class="src-h">{esc(para[3:])}</h2>')
            continue
        parts = re.split(r"(`[^`]+`)", para)
        inner = "".join(f"<code>{esc(p[1:-1])}</code>" if p.startswith("`") else esc(p) for p in parts)
        out.append(f"<p>{inner}</p>")
    return "\n".join(out)

# The living's words: (record file, verbatim excerpt, provenance)
Q = {
 "mark": ("presentation.md",
   "We're going to train all of the main flows to, whenever they want to talk to the living, mark that block as intended for the living at the beginning and at the end. They'll be easy to differentiate.",
   "-- psyche, STT, 2026-10-01 · flows/6997eb/vision/presentation.md"),
 "comfort": ("presentation.md",
   "There's something to be said about what models are comfortable with. What can be good is if it's harnessed properly because the models are able to do it well or they're comfortable with it.",
   "-- psyche, STT, 2026-10-01 · flows/6997eb/vision/presentation.md"),
 "tool": ("presentation.md",
   "When it's addressed to the psyche, it's marked as such. We can write a tool that could easily detect the pattern that we agree on for marking the beginning and the end of the blocks that are intended to be either turned into a book, updated, or changed in an already existing one.",
   "-- psyche, STT, 2026-10-01 · flows/6997eb/vision/presentation.md"),
 "logging": ("commentary.md",
   "Eventually we'll turn this whole commentary thing into more of a system logging kind of thing, notifying us of errors, unexpected outcomes or results.",
   "-- psyche, STT, 2026-10-01 · flows/6997eb/vision/commentary.md"),
 "render": ("presentation.md",
   "I don't need to be able to see them in the chat. I think if we keep everything else that the machine says to a more mechanical logging-like behavior, then it'll be obvious when it's actually talking in [prose] and talking to me. If it doesn't render it then there might be an advantage to that. Yeah maybe. Astra's vision is better.",
   "-- psyche, STT, 2026-10-01, said at 18:13Z · flows/6997eb/vision/presentation.md · transcription corrected: \"pros\" → \"[prose]\""),
}

def quote(k):
    _, text, prov = Q[k]
    return (f'<blockquote class="living" data-q="{k}"><p class="said">{esc(text)}</p>'
            f'<p class="prov">{esc(prov)}</p></blockquote>')

def note(kind, words, date, body):
    return (f'<aside class="note {kind}"><p class="tag">Psyche Sonnet {"agrees" if kind=="agree" else "disagrees"}</p>'
            f'<p>On “{esc(words)}” ({date}): {esc(body)}</p></aside>')

def svg(name):
    return (HERE / "svg" / name).read_text()

def ill(name, caption):
    return f'<section class="page ill"><figure>{svg(name)}<figcaption>{esc(caption)}</figcaption></figure></section>'

def txt(inner):
    return f'<section class="page txt"><div class="sheet">{inner}</div></section>'

SRC_PROV = ('<p class="prov">The source, verbatim: Psyche Fable 6997eb, transcript '
            '6997eb8a-30eb-49a1-a787-45279164a43b.jsonl, line 623, uuid 187e77eb-8069-4648-9f38-a29ad72ed12f, '
            '2026-10-01T18:10:27Z.</p>')

pages = [
 ill("1-cover.svg", "One block in the flow of a reply is addressed to you; two marks hold it."),
 txt('<p class="eyebrow">Point 1 of 4</p><h2>Mark the beginning and the end</h2>'
     + quote("mark")
     + '<p>The block between the marks is the part written to you. Everything outside it is not.</p>'),
 ill("2-instincts.svg", "Two marks in trial: one you can see, one that vanishes when rendered."),
 txt('<p class="eyebrow">Point 2 of 4 · the source</p>'
     + f'<div class="src">{md(marker_part)}</div>' + SRC_PROV
     + quote("comfort")),
 ill("3-hook.svg", "A hook lifts the marked block out of the transcript and carries it to a book."),
 txt('<p class="eyebrow">Point 3 of 4</p><h2>A tool finds the block</h2>'
     + quote("tool")
     + '<p>Both marks are a fixed pattern on its own line, so either is easy to match.</p>'),
 ill("4-log.svg", "Outside the block, short machine lines. Inside it, prose to you."),
 txt('<p class="eyebrow">Point 4 of 4</p><h2>Outside the block, a log</h2>'
     + quote("logging") + quote("render")
     + note("agree", "If it doesn't render it then there might be an advantage to that", "2026-10-01",
            "an unrendered mark puts no scaffolding in the book, and the hook still matches it. The reader sees only prose.")
     + '<p class="mark"><strong>Mark</strong> The source read “they\'ll be easy to differentiate” as wanting to see the marks. The words above, said three minutes after the source was written, say the marks need not be seen in the chat.</p>'),
 ill("5-fork.svg", "The fork the source put before you."),
 txt('<p class="eyebrow">The source asked · ruled by the living, 2026-10-01</p>'
     + f'<div class="src">{md(ruling_part)}</div>' + SRC_PROV.replace("The source, verbatim", "Verbatim, same record")
     + '<ol class="props">'
       '<li><span class="n">1</span><span>Visible pair: <code>=== To the living ===</code> and <code>=== End ===</code> (Fable, Opus).</span></li>'
       '<li class="ruled"><span class="n">2</span><span>Comment pair: <code>&lt;!-- to-the-living:start --&gt;</code> and <code>&lt;!-- to-the-living:end --&gt;</code> (Field Astra).</span></li>'
       '<li><span class="n">3</span><span>Both allowed, one tool reading either.</span></li>'
       '<li><span class="n">4</span><span>The chosen lines go into the main-flow skill; Astra, Opus and Fable practice them from the next reply.</span></li>'
     '</ol>'
     + '<p class="mark"><strong>Ruled</strong> By the living, 2026-10-01, in his words on page 8: “Astra\'s vision is better.” That is item 2. None of the four is badged landed: no skill change was seen when it was made.</p>'),
]

N = len(pages)
dots = "".join(f'<span class="dot{" t" if "txt" in p[:40] else ""}"></span>' for i, p in enumerate(pages))
shell = (HERE / "shell.html").read_text()
out = shell.replace("{{TITLE}}", esc(TITLE)).replace("{{N}}", str(N)).replace("{{DOTS}}", dots).replace("{{PAGES}}", "\n".join(pages))
(HERE / "book.html").write_text(out)

# ---- verification ----
fail = 0
for k, (f, text, _) in Q.items():
    rec = vision(f)
    if text not in rec:
        print("QUOTE NOT VERBATIM", k, f); fail += 1
    if esc(text) not in out:
        print("QUOTE MISSING FROM BOOK", k); fail += 1
def plain(h):
    return html.unescape(re.sub(r"<[^>]+>", "", h))
for part in (marker_part, ruling_part):
    for para in part.split("\n\n"):
        want = para[3:] if para.startswith("## ") else para.replace("`", "")
        if want not in plain(out):
            print("SOURCE PARAGRAPH NOT VERBATIM:", want[:60]); fail += 1
print("pages", N, "source sha256", hashlib.sha256(SRC.encode()).hexdigest())
print("book sha256", hashlib.sha256(out.encode()).hexdigest(), "bytes", len(out.encode()))
print("FAIL" if fail else "verbatim: all quotes and source paragraphs OK")
sys.exit(1 if fail else 0)
