#!/usr/bin/env python3
"""Builds «Books as the interface, rendered by a tool» from source.md (copied by extract.py) and the
living's records; verifies source text, every quote, and that the page has no controls."""
import html, re, subprocess, sys, hashlib, pathlib
HERE = pathlib.Path(__file__).resolve().parent
PRIMARY = pathlib.Path("/home/li/primary")
esc = html.escape
def record(rel):
    p = PRIMARY / rel
    return p.read_text() if p.exists() else subprocess.run(["git","-C",str(PRIMARY),"show",f"main:{rel}"],capture_output=True,text=True,check=True).stdout
def flat(s): return re.sub(r"\s*\n>\s*", " ", s)

RAW = (HERE / "source.md").read_text()
first, rest = RAW.split("\n", 1)
m = re.fullmatch(r"Presentation\.\{ «(.+)» \}", first); assert m, first
TITLE = m.group(1); assert TITLE == "Books as the interface, rendered by a tool"
BODY = rest.strip("\n")
main_part, rulings_part = BODY.split("\n\n## Rulings\n\n")
head, *items = main_part.split("\n\n")
assert head == "## Books as the interface, rendered by a tool" and len(items) == 4

def inline(s):
    parts = re.split(r"(`[^`]+`)", s)
    return "".join(f"<code>{esc(p[1:-1])}</code>" if p.startswith("`") else esc(p) for p in parts)
def item(n):
    mm = re.match(r"(\d)\. \*\*(.+?)\*\* (.*)", items[n-1], re.S)
    assert mm and int(mm.group(1)) == n
    return mm.group(2), mm.group(3)

Q = {
 "mechanical": ("flows/fe945a/vision/books.md",
   "My point, my whole point, is that the books become the user interface. It's not a question anymore. If a secondary or primary flow gives a presentation output, that's what makes it go into the pipeline. It doesn't mean it's necessarily instantly rendered although we're going towards that, because really rendering is mechanical when you think about it. We should be able to just write a tool that does it.",
   "-- psyche, STT, 2026-10-01, to Psyche Opus fe945a · flows/fe945a/vision/books.md"),
 "noillus": ("flows/fe945a/vision/books.md",
   "To be honest there's a version of this that only needs nothing [sic] because there's no illustration. To call an AI LLM just to make a render, just to display something, is ridiculous but I asked for alternatives.",
   "-- psyche, STT, 2026-10-01, to Psyche Opus fe945a · flows/fe945a/vision/books.md"),
 "mentciweb": ("flows/1b8ac0/vision/mentciWeb.md",
   "That's Menchi Web. Why don't we just make Menchi Web?",
   "-- psyche, STT, 2026-09-21, to PsycheHigh 1b8ac0, \"Menchi\" read as \"Mentci\" · flows/1b8ac0/vision/mentciWeb.md"),
 "unity": ("flows/4a2502/vision/operational-unityIsMentciClient.md",
   "Unity is basically a Menchi server. Menchi is the server. Menchi is the input device of our world, right? Menchi is the mind tool, and Unity is just a client to it.",
   "-- psyche, typed (artifact comment), 2026-09-18, flow 4a2502 · flows/4a2502/vision/operational-unityIsMentciClient.md"),
 "security": ("flows/fe945a/vision/books.md",
   "using the harness like this (the remote control and a harness) is not only clumsy, it's a security issue. If this system gets hacked on the cloud server side, then they basically gain access to all the machines that are exposed through this remote control environment by just giving the agents whatever order ...",
   "-- psyche, STT, 2026-10-01, to Psyche Opus fe945a; the last sentence breaks off · flows/fe945a/vision/books.md"),
}
def quote(k):
    _, t, prov = Q[k]
    return f'<blockquote class="living" data-q="{k}"><p class="said">{esc(t)}</p><p class="prov">{esc(prov)}</p></blockquote>'
def note(kind, words, date, body):
    verb = "agrees" if kind == "agree" else "disagrees"
    return (f'<aside class="note {kind}"><p class="tag">Psyche Sonnet {verb}</p>'
            f'<p>On “{esc(words)}” ({date}): {esc(body)}</p></aside>')
def mark(label, body):
    return f'<p class="mark"><strong>{label}</strong> {esc(body)}</p>'
def txt(inner): return f'<section class="page txt"><div class="sheet">{inner}</div></section>'
def point(n, extra=""):
    lead, rest = item(n)
    return txt(f'<p class="eyebrow">Point {n} of 4</p><div class="src"><h2>{esc(lead)}</h2><p>{inline(rest)}</p></div>' + extra)

SRC_PROV = ('<p class="prov">The source, verbatim: Psyche Fable 6997eb, transcript '
 '6997eb8a-30eb-49a1-a787-45279164a43b.jsonl, line 1606, uuid d27421e2-72a7-45d4-941e-799713a6e2fd, '
 '2026-10-01T20:11:01Z, between its to-the-living markers. Its first line, the datom '
 'Presentation.{ «Books as the interface, rendered by a tool» }, gives this book its title and is not shown.</p>')

bullets = [b[2:] for b in rulings_part.split("\n")]
assert len(bullets) == 3 and all(b.startswith("- ") for b in rulings_part.split("\n"))
props = "".join(f'<li><span class="n">{i}</span><span>{inline(b)}<span class="open">not yet ruled</span></span></li>' for i, b in enumerate(bullets, 1))

pages = [
 txt('<p class="eyebrow">A book of four points</p><div class="src"><h2>' + esc(TITLE) + '</h2>'
     '<p>Psyche Fable 6997eb reads your words of 1 October as a decision: the books are the interface, and drawing them is a tool\'s work.</p></div>'
     + SRC_PROV + mark("Mark", "This book has no illustration pages and no diagram, because the source has neither.")),
 point(1, quote("mechanical") + quote("noillus")
       + note("agree", "really rendering is mechanical when you think about it", "2026-10-01",
              "the source takes this literally, and so does this seat: extracting, shelling and checking are scripts; only the drawing, the choice of four points and the notes need a model.")
       + mark("Mark", "The source quotes you as “there's a version of this that only needs nothing because there's no illustration.” The record has “[sic]” after “nothing”; the source left it out.")),
 point(2, quote("mentciweb") + quote("unity")
       + mark("Mark", "The source dates “That's Mentci Web” to 21 September and cites “Unity is just a client to it” to 4a2502. Both are right. The records carry the speech-to-text spelling “Menchi”, shown here as recorded.")
       + mark("Tension", "In that same 4a2502 record you call Unity “basically a Mentci server”. The source reads the Nexus as Mentci and Unity as one client of it; you have not ruled between the two.")),
 point(3),
 point(4, quote("security")
       + note("agree", "it's a security issue", "2026-10-01",
              "the source adds that a compromised display would read books and return comments but reach no shell, which is what makes it a smaller surface than the relay.")
       + mark("Mark", "The source's witness of six sessions with remote control on, three Claude and three Codex, is its own observation. It is not in your records.")),
 txt('<p class="eyebrow">Asked of you</p><div class="src"><h2>Rulings</h2></div>' + f'<ol class="props">{props}</ol>' + SRC_PROV
     + mark("Badge", "None is badged landed. Nothing of the display Nexus, pulldown-cmark or the tailnet web app was seen built when this book was made.")),
]
N = len(pages)
dots = "".join(f'<span class="dot t"></span>' for _ in pages)
out = ((HERE/"shell.html").read_text().replace("{{TITLE}}", esc(TITLE)).replace("{{N}}", str(N))
       .replace("{{DOTS}}", dots).replace("{{PAGES}}", "\n".join(pages)))
(HERE/"book.html").write_text(out)

fail = 0
def plain(h): return html.unescape(re.sub(r"<[^>]+>", "", h))
P = plain(out)
for k, (f, text, _) in Q.items():
    if text not in flat(record(f)): print("QUOTE NOT IN RECORD", k); fail += 1
    if text not in P: print("QUOTE MISSING FROM BOOK", k); fail += 1
for para in [head[3:], "Rulings"] + [b.replace("`","") for b in bullets]:
    if para not in P: print("SOURCE PARA MISSING", para[:60]); fail += 1
for n in range(1,5):
    l, r = item(n)
    if l not in P or r.replace("`","") not in P or f"{n}. **{l}** {r}" != items[n-1]: print("ITEM MISSING", n); fail += 1
# the source's own quotes of the living
for qt in ["there's a version of this that only needs nothing because there's no illustration.", "That's Mentci Web. Why don't we just make Mentci Web?", "Unity is just a client to it", "basically a Mentci server"]:
    assert qt in BODY, qt
for qt, f in [("there's a version of this that only needs nothing", "flows/fe945a/vision/books.md"),
              ("there's no illustration.", "flows/fe945a/vision/books.md"),
              ("Why don't we just make", "flows/1b8ac0/vision/mentciWeb.md"),
              ("Unity is just a client to it", "flows/4a2502/vision/operational-unityIsMentciClient.md"),
              ("basically a Menchi server", "flows/4a2502/vision/operational-unityIsMentciClient.md")]:
    ok = qt in flat(record(f)); print("source quote in record (spelling aside):", ok, qt)
    if not ok: fail += 1
for pat in (r"<button", r"<a\s", r"<input", r"<select", r"<textarea", r"onclick", r"role=\"button\"", r"tabindex", r"<details", r"<summary", r"<pre", r"<img", r"<svg"):
    if re.search(pat, out): print("FOUND", pat); fail += 1
print("title", TITLE, "pages", N, "book sha256", hashlib.sha256(out.encode()).hexdigest(), len(out.encode()))
print("FAIL" if fail else "OK")
sys.exit(1 if fail else 0)
