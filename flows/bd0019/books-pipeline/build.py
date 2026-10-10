#!/usr/bin/env python3
"""Builds «The anatomy of the book pipeline» from source.md (copied by extract.py), svg/ and the
living's records, and verifies the source text, every quote, and that the page has no buttons or
clickable controls."""
import html, re, subprocess, sys, hashlib, pathlib

HERE = pathlib.Path(__file__).resolve().parent
PRIMARY = pathlib.Path("/home/li/primary")
esc = html.escape

def record(rel):
    p = PRIMARY / rel
    if p.exists():
        return p.read_text()
    return subprocess.run(["git", "-C", str(PRIMARY), "show", f"main:{rel}"],
                          capture_output=True, text=True, check=True).stdout

def flat(s):   # joins a blockquote wrapped over several "> " lines
    return re.sub(r"\s*\n>\s*", " ", s)

RAW = (HERE / "source.md").read_text()
first, rest = RAW.split("\n", 1)
m = re.fullmatch(r"Presentation\.\{ «(.+)» \}", first)
assert m, first
TITLE = m.group(1)                              # ruled metadata: the datom line gives the title
assert TITLE == "The anatomy of the book pipeline"
BODY = rest.strip("\n")                         # the datom line is not shown
main_part, rulings_part = BODY.split("\n\n## Rulings\n\n")
head, *items = main_part.split("\n\n")
assert head == "## The anatomy, revised with Opus's view" and len(items) == 4

def inline(s):
    parts = re.split(r"(`[^`]+`)", s)
    return "".join(f"<code>{esc(p[1:-1])}</code>" if p.startswith("`") else esc(p) for p in parts)

def item(n):
    mm = re.match(r"(\d)\. \*\*(.+?)\*\* (.*)", items[n - 1], re.S)
    assert mm and int(mm.group(1)) == n
    return mm.group(2), mm.group(3)

V = "flows/6997eb/vision/"
Q = {
 "bad": (V + "presentation.md", "That wasn't a question. I said it is bad.",
   "-- psyche, typed, 2026-10-01 · " + V + "presentation.md"),
 "datom": (V + "presentation.md", "Yeah the metadata is one datom line. That's brilliant. I love it. Let's do it.",
   "-- psyche, STT, 2026-10-01, after this revision was written · " + V + "presentation.md"),
 "hook": ("flows/cf3553/vision/operational-finalResponseLifecycleHook.md",
   "We should have an end-of-last-reply hook that notifies the Flow component using the Flow CLI of all the information it can give it. In the last response, possibly we should also send that to Flow, and then Flow would send that to the reaping agent to decide if that's the end of Flow and if it should be reaped.",
   "-- psyche, relayed verbatim by root on 2026-09-19 · flows/cf3553/vision/operational-finalResponseLifecycleHook.md"),
 "which": (V + "pipeline.md",
   "They're going to call the Nexus CLI so which Nexus do we use for this? Is this Flow, or is it Transcript, or is it something else?",
   "-- psyche, typed (comment on «Two kinds of output»), 2026-10-01 · " + V + "pipeline.md"),
 "transcript": ("flows/fe945a/vision/transcriptOverFiles.md",
   "What do you mean the prompt is committed? It's in your transcript.",
   "-- psyche, typed, 2026-09-29, to Psyche Opus 183ae0 · flows/fe945a/vision/transcriptOverFiles.md"),
 "nocopy": ("flows/e51411/vision/refresh.md",
   "The tool gets the right block of text because it has the right reference so we don't need to make a copy of anything. It just fetches it programmatically.",
   "-- living, 2026-09-24, to Mind Astra 47764b · flows/e51411/vision/refresh.md"),
 "flownexus": ("flows/b05237/vision/operational-reportIsTranscript.md",
   "That's what the logs are: they're just references to transcripts. You find a way to address the transcript efficiently and make a tool to acquire that data quickly. That's what the Flow Nexus needs to do.",
   "-- psyche, to Psyche opus b05237, 2026-09-18 · flows/b05237/vision/operational-reportIsTranscript.md"),
 "another": ("flows/e06e4c07/vision/flowKnowledge.md",
   "obviously another nexus. But we might want a small clever tool to help search those files more efficiently for now.",
   "-- psyche, typed, 2026-08-19, design session e06e4c07 · flows/e06e4c07/vision/flowKnowledge.md"),
}

# Field Astra's witness: an addition relayed by Psyche Fable 6997eb, not part of the copied source.
ASTRA = ("Field Astra witnessed that the Stop hook fires before the turn's final record is written and that "
         "Codex continues the turn if a handler blocks; so the hook only enqueues a turn-ended request and "
         "returns, and the nexus verifies completion and deduplicates.")

def quote(k):
    _, text, prov = Q[k]
    return (f'<blockquote class="living" data-q="{k}"><p class="said">{esc(text)}</p>'
            f'<p class="prov">{esc(prov)}</p></blockquote>')

def note(kind, words, date, body):
    verb = "agrees" if kind == "agree" else "disagrees"
    return (f'<aside class="note {kind}"><p class="tag">Psyche Sonnet {verb}</p>'
            f'<p>On “{esc(words)}” ({date}): {esc(body)}</p></aside>')

def mark(label, body):
    return f'<p class="mark"><strong>{label}</strong> {esc(body)}</p>'

def witness():
    return ('<aside class="witness"><p class="tag">Field Astra’s witness · 2026-10-01 · '
            'an addition, not part of the source</p>'
            f'<p>{esc(ASTRA)}</p><p class="prov">Relayed by Psyche Fable 6997eb for this book, '
            'to stand beside point 1.</p></aside>')

def ill(name, caption):
    return (f'<section class="page ill"><figure>{(HERE / "svg" / name).read_text()}'
            f'<figcaption>{esc(caption)}</figcaption></figure></section>')

def txt(inner):
    return f'<section class="page txt"><div class="sheet">{inner}</div></section>'

def point(n, extra="", lead_extra=""):
    lead, rest = item(n)
    return txt(f'{lead_extra}<p class="eyebrow">Point {n} of 4</p><div class="src"><h2>{esc(lead)}</h2>'
               f'<p>{inline(rest)}</p></div>' + extra)

SRC_PROV = ('<p class="prov">The source, verbatim: Psyche Fable 6997eb, transcript '
            '6997eb8a-30eb-49a1-a787-45279164a43b.jsonl, line 1091, uuid c3a069fb-6003-4e12-8d6f-baf4683f399e, '
            '2026-10-01T19:41:42Z, between its to-the-living markers; its first line, the datom '
            'Presentation.{ «The anatomy of the book pipeline» }, gives this book its title and is not shown.</p>')

bullets = [b[2:] for b in rulings_part.split("\n")]
assert len(bullets) == 3 and all(rulings_part.split("\n")[i].startswith("- ") for i in range(3))
RULED = {1: "Ruled by the living, 2026-10-01"}
props = "".join(
    f'<li class="{"ruled" if i in RULED else ""}"><span class="n">{i}</span><span>{inline(b)}'
    + (f'<span class="badge">{RULED[i]}</span>' if i in RULED else "") + '</span></li>'
    for i, b in enumerate(bullets, 1))

pages = [
 ill("p2-line.svg", "The book's own first line: one datom, set in type. The dashed front matter drifts away."),
 point(1, quote("bad") + quote("datom")
       + note("agree", "Yeah the metadata is one datom line", "2026-10-01",
              "one plain line survives any renderer, so what the Android view did to the dashed block cannot happen to it.")
       + mark("Mark", "The phrase the source quotes as yours, “a typed datom value the end-of-turn hook recognises” (7328f4), is not in any record of your words. It is Psyche Opus 7328f4's own question to you, which read “Is it a typed datom value, such as one called Presentation, that the end-of-turn hook recognises and passes to the flow nexus?” (7328f4 transcript, line 958, 2026-10-01).")
       + witness(),
       lead_extra='<div class="src"><h2 class="src-h">' + esc(head[3:]) + '</h2></div>' + SRC_PROV),
 ill("p3-bell.svg", "The turn ends; the Stop hook rings flow. The card it sends names the session and the path, nothing of the reply."),
 point(2, quote("hook")
       + mark("Tension", "The source has Flow record “never the content”. In the same relay you added “possibly we should also send that to Flow”, meaning the last response.")),
 ill("p4-pointer.svg", "One scroll. The reader points into it between the two markers; no copy is carried away."),
 point(3, quote("transcript") + quote("nocopy")
       + note("agree", "we don't need to make a copy of anything", "2026-09-24",
              "reading the block by pointer through Transcript is this word made into a pipeline.")
       + mark("Mark", "“It's in your transcript” is cited to 183ae0, the seat you said it to; the record was written by fe945a.")),
 ill("p5-scale.svg", "The turn event in one pan, the transcript in the other. Which nexus holds what is yours to say."),
 point(4, quote("flownexus") + quote("another") + quote("which")),
 ill("p1-cover.svg", "The whole anatomy: the transcript, the marked stretch, the hook and its bell, the reader, the book."),
 txt('<p class="eyebrow">Asked of you</p><div class="src"><h2>Rulings</h2></div>'
     + f'<ol class="props">{props}</ol>' + SRC_PROV
     + mark("Badge", "Only the first is badged: you ruled it after this revision was written. No hook, no Flow turn-ended request and no Transcript read was seen landed when this book was made.")),
]

N = len(pages)
dots = "".join(f'<span class="dot{" t" if "page txt" in p[:40] else ""}"></span>' for p in pages)
shell = (HERE / "shell.html").read_text()
out = (shell.replace("{{TITLE}}", esc(TITLE)).replace("{{N}}", str(N))
            .replace("{{DOTS}}", dots).replace("{{PAGES}}", "\n".join(pages)))
(HERE / "book.html").write_text(out)

# ---- verification ----
fail = 0
def plain(h):
    return html.unescape(re.sub(r"<[^>]+>", "", h))
P = plain(out)
for k, (f, text, _) in Q.items():
    if text not in flat(record(f)):
        print("QUOTE NOT VERBATIM IN RECORD", k, f); fail += 1
    if text not in P:
        print("QUOTE MISSING FROM BOOK", k); fail += 1
if ASTRA not in P:
    print("ASTRA WITNESS MISSING"); fail += 1
for para in ["The anatomy, revised with Opus's view", "Rulings"] + [b.replace("`", "") for b in bullets]:
    if para not in P:
        print("SOURCE PARAGRAPH NOT VERBATIM:", para[:70]); fail += 1
for n in range(1, 5):
    l, r = item(n)
    if l not in P or r.replace("`", "") not in P or f"{n}. **{l}** {r}" != items[n - 1]:
        print("SOURCE PARAGRAPH NOT VERBATIM:", items[n - 1][:70]); fail += 1
# the Mark's quote of 7328f4's question, against that seat's transcript
import json
Q7 = "Is it a typed datom value, such as one called Presentation, that the end-of-turn hook recognises and passes to the flow nexus?"
with open("/home/li/.claude/projects/-home-li-primary/7328f4ba-d5c4-440f-aa68-7e1d969deab8.jsonl") as fh:
    for i, l in enumerate(fh, 1):
        if i == 958:
            r7 = json.loads(l); break
t7 = "".join(c.get("text", "") for c in r7["message"]["content"] if isinstance(c, dict))
if not (r7["type"] == "assistant" and Q7 in t7 and Q7 in P):
    print("7328f4 QUOTE NOT VERBATIM"); fail += 1
else:
    print("7328f4 line 958 quote ok (assistant record)", r7.get("timestamp"))
# the source's own quotes of the living, against the records
recs = {
 "a typed datom value the end-of-turn hook recognises": None,   # not the living's: see the Mark
 "an end-of-last-reply hook that notifies the Flow component using the Flow CLI": "flows/cf3553/vision/operational-finalResponseLifecycleHook.md",
 "It's in your transcript": "flows/fe945a/vision/transcriptOverFiles.md",
 "what the Flow Nexus needs to do": "flows/b05237/vision/operational-reportIsTranscript.md",
 "obviously another nexus": "flows/e06e4c07/vision/flowKnowledge.md",
}
found = re.findall(r'"([^"]+)"', BODY)
assert sorted(found) == sorted(recs), found
for qt, f in recs.items():
    if f is None:
        allrec = "".join(record(str(p.relative_to(PRIMARY))) for p in PRIMARY.glob("flows/*/vision/*.md"))
        print("source quote NOT in any living record (marked):", qt, "->", qt in allrec)
        if qt in allrec: print("  unexpectedly found; revisit the Mark"); fail += 1
    elif qt not in flat(record(f)):
        print("SOURCE QUOTE NOT IN RECORD", qt); fail += 1
    else:
        print("source quote ok:", qt)
for pat in (r"<button", r"<a\s", r"<input", r"<select", r"<textarea", r"onclick", r"addEventListener\('click'", r'role="button"', r"tabindex", r"<details", r"<summary"):
    if re.search(pat, out):
        print("CONTROL FOUND:", pat); fail += 1
if "<pre" in out:
    print("PRE BLOCK FOUND"); fail += 1
print("title", TITLE, "pages", N, "source sha256", hashlib.sha256(RAW.encode()).hexdigest())
print("book sha256", hashlib.sha256(out.encode()).hexdigest(), "bytes", len(out.encode()))
print("FAIL" if fail else "verbatim: all quotes and source paragraphs OK; no controls")
sys.exit(1 if fail else 0)
