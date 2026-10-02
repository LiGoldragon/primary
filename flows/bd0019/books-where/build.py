#!/usr/bin/env python3
"""Builds «Where books go, and the anatomy of the book pipeline» from source.md (copied by extract.py),
svg/ and the living's records, and verifies the source text, every quote, and that the page has no
buttons or clickable controls. Prose is never put in a code block; only the source's own fenced code is."""
import html, re, subprocess, sys, hashlib, pathlib, json

HERE = pathlib.Path(__file__).resolve().parent
PRIMARY = pathlib.Path("/home/li/primary")
PROJ = pathlib.Path("/home/li/.claude/projects/-home-li-primary")
esc = html.escape

def record(rel):
    p = PRIMARY / rel
    if p.exists():
        return p.read_text()
    return subprocess.run(["git", "-C", str(PRIMARY), "show", f"main:{rel}"],
                          capture_output=True, text=True, check=True).stdout

def raw_line(session, line):
    with open(PROJ / f"{session}.jsonl") as fh:
        for i, l in enumerate(fh, 1):
            if i == line:
                return json.loads(l)

def raw_text(r):
    c = r["message"]["content"]
    return c if isinstance(c, str) else "".join(b.get("text", "") for b in c if isinstance(b, dict))

def flat(s):
    return re.sub(r"\s*\n>\s*", " ", s)

RAW = (HERE / "source.md").read_text()
first, rest = RAW.split("\n", 1)
m = re.fullmatch(r"`Book\.«(.+)»`", first)
assert m, first
TITLE = m.group(1)                              # the metadata line gives the title and is not shown
assert TITLE == "Where books go, and the anatomy of the book pipeline"
BODY = rest.strip("\n")
secs = re.split(r"\n(?=## \d\. )", BODY)
assert len(secs) == 4 and all(s.startswith(f"## {i}. ") for i, s in enumerate(secs, 1)), [s[:20] for s in secs]

def inline(s):
    out = []
    for p in re.split(r"(`[^`]+`)", s):
        if p.startswith("`"):
            out.append(f"<code>{esc(p[1:-1])}</code>")
        else:
            out.append(re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", esc(p)))
    return "".join(out)

def md(block):
    """Renders one section of the source: heading, bullets, paragraphs, blockquote, fenced code."""
    lines, out, i = block.split("\n"), [], 0
    while i < len(lines):
        l = lines[i]
        if l.startswith("```"):
            j = i + 1
            while lines[j] != "```": j += 1
            out.append('<div class="codewrap"><pre class="code"><code>' + esc("\n".join(lines[i + 1:j])) + "</code></pre></div>")
            i = j + 1; continue
        if l.startswith("## "):
            out.append(f"<h2>{inline(l[3:])}</h2>")
        elif l.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(f"<li>{inline(lines[i][2:])}</li>"); i += 1
            out.append('<ul class="pts">' + "".join(items) + "</ul>"); continue
        elif l.startswith("> "):
            out.append(f'<blockquote class="doc"><p>{inline(l[2:])}</p></blockquote>')
        elif l.strip():
            out.append(f"<p>{inline(l)}</p>")
        i += 1
    return '<div class="src">' + "".join(out) + "</div>"

S881 = ("bd0019dd-faeb-46b1-8ea6-f7423af3e6e6", 881, "12f03b17-25c6-4024-8b0f-ae285a55e78b")
S977 = ("fe945a2e-c785-4af4-9a46-766b6ea512e8", 977, "867f78c8-62d7-4125-8c8d-b79d23322c7b")
P881 = "-- the living, 2026-10-01T19:52Z, to Psyche Sonnet bd0019 · transcript bd0019dd, line 881 · flows/bd0019/vision/transcriptNotFiles.md"
P977 = "-- the living, 2026-10-01T20:08Z, to Psyche Opus fe945a, twelve minutes after this source was written · transcript fe945a, line 977"
HOOKF = "flows/cf3553/vision/operational-finalResponseLifecycleHook.md"
Q = {
 "where": (S881, "I want to know where that book is going and if it's already being version-controlled. Not that I would want to version-control the HTML, but at least the Markdown and what's happening with that now.", P881),
 "hook": (HOOKF, "We should have an end-of-last-reply hook that notifies the Flow component using the Flow CLI of all the information it can give it.",
          "-- psyche, relayed verbatim by root on 2026-09-19 · " + HOOKF),
 "mech": (S977, "It doesn't mean it's necessarily instantly rendered although we're going towards that, because really rendering is mechanical when you think about it. We should be able to just write a tool that does it.", P977),
 "llm": (S977, "To call an AI LLM just to make a render, just to display something, is ridiculous but I asked for alternatives.", P977),
 "noq": (S977, "My point, my whole point, is that the books become the user interface. It's not a question anymore.", P977),
}

def quote(k):
    _, text, prov = Q[k]
    return (f'<blockquote class="living" data-q="{k}"><p class="said">{esc(text)}</p>'
            f'<p class="prov">{esc(prov)}</p></blockquote>')

def note(kind, words, date, body):
    verb = "agrees" if kind == "agree" else "disagrees"
    return (f'<aside class="note {kind}"><p class="tag">Psyche Sonnet {verb}</p>'
            f'<p>On “{esc(words)}” ({date}): {esc(body)}</p></aside>')

def mark(label, body):
    return f'<p class="mark"><strong>{label}</strong> {inline(body)}</p>'

def ill(name, caption):
    return (f'<section class="page ill"><figure>{(HERE / "svg" / name).read_text()}'
            f'<figcaption>{esc(caption)}</figcaption></figure></section>')

def txt(inner):
    return f'<section class="page txt"><div class="sheet">{inner}</div></section>'

def point(n, extra=""):
    return txt(f'<p class="eyebrow">Point {n} of 4</p>' + md(secs[n - 1]) + extra)

SRC_PROV = ('<p class="prov">The source, verbatim: Psyche Opus fe945a, transcript '
            'fe945a2e-c785-4af4-9a46-766b6ea512e8.jsonl, line 972, uuid b7a214ca-4043-4c39-83d6-77d147edd483, '
            '2026-10-01T19:56:37Z, between its to-the-living markers; its first line, '
            'Book.«Where books go, and the anatomy of the book pipeline», gives this book its title and is not shown.</p>')

SOL = ("Psyche Fable 6997eb's log records, as Mind Sol 5104af's own account (a claim), that Mind Sol landed "
       "signal-flow 6.3.0 on 2026-10-01, logged after this source was written: `Presentation.{ Title }`, "
       "`TurnEndRequest.{ SessionId TurnId Option<TranscriptPath> }` and the query `QueueTurnEnd`. By the source's "
       "own condition, Mind Sol's type replaces the one proposed here. It landed as a minor version, where this "
       "page expects Flow's next major version.")

PROPS = [
 ("Psyche Sonnet commits each book's Markdown itself, under its flow's books folder, named by the turn that produced it. The HTML is published as a page and not committed, and screenshots are not kept.",
  "Done for this book: Markdown committed, HTML not, screenshots deleted. Not yet named by the turn"),
 ("The block's title line as the `Library` type `Presentation.[ Book.BookTitle ]` (point 3).",
  "Superseded, a claim: signal-flow 6.3.0 has Presentation.{ Title }"),
 ("The Transcript Nexus with `ReadLivingBlock.TurnPointer` and its replies (point 3).", None),
 ("Flow gains `EndTurn.TurnPointer` and `ObserveTurns.TurnFilter`, and moves to its next major version (point 3).",
  "Superseded in part, a claim: signal-flow 6.3.0 has QueueTurnEnd"),
]
kind = lambda b: "" if not b else ("ruled" if b.startswith("Done") else "sup")
props = "".join(
    f'<li class="{kind(b)}"><span class="n">{i}</span><span>{inline(t)}'
    + (f'<span class="badge {kind(b)}">{esc(b)}</span>' if b else "") + "</span></li>"
    for i, (t, b) in enumerate(PROPS, 1))

pages = [
 ill("w1-roads.svg", "Three roads out of one book: a private page, a committed ledger of Markdown, and screenshots that are not kept."),
 txt(SRC_PROV + f'<p class="eyebrow">Point 1 of 4</p>' + md(secs[0]) + quote("where")
     + note("agree", "Not that I would want to version-control the HTML, but at least the Markdown", "2026-10-01",
            "the proposal keeps exactly the Markdown, lets the HTML and the screenshots go, and answers where the book is going.")),
 ill("p3-bell.svg", "The turn ends; the Stop hook rings flow. The card it sends names the session and the turn, nothing of the reply."),
 point(2, quote("hook")
       + note("agree", "an end-of-last-reply hook that notifies the Flow component using the Flow CLI", "2026-09-19",
              "the hook calling the flow CLI is this word, kept small: it decides nothing but whether the marker is there.")
       + quote("llm") + quote("mech")
       + note("disagree", "To call an AI LLM just to make a render, just to display something, is ridiculous", "2026-10-01",
              "the anatomy ends at Sonnet for every book, so a model is called even when a block has no illustration. Your word, said after it was written, asks for a mechanical render there.")),
 ill("p2-line.svg", "The block's first line, set in type: one datom that names the book. The dashed front matter drifts away."),
 point(3, mark("Mark", SOL)),
 ill("p4-pointer.svg", "One scroll. The reader points into it between the two markers; no copy is carried away."),
 point(4, mark("Answered", "The source closes by asking your word. You gave it after the source was written:") + quote("noq")),
 ill("p1-cover.svg", "The whole anatomy: the transcript, the marked stretch, the hook and its bell, the reader, the book."),
 txt('<p class="eyebrow">Proposed in the source</p><div class="src"><h2>Proposals</h2></div>'
     + f'<ol class="props">{props}</ol>'
     + mark("Badges", "Only what was seen when this book was made is badged. No hook, no turn-ended signal into Flow and no Transcript read was seen landed.")),
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
for k, (src, text, _) in Q.items():
    if isinstance(src, tuple):
        r = raw_line(src[0], src[1])
        ok = r["uuid"] == src[2] and r["type"] == "user" and text in raw_text(r)
        where = f"{src[0][:8]} line {src[1]} {r['timestamp']}"
    else:
        ok = text in flat(record(src)); where = src
    if not ok:
        print("QUOTE NOT VERBATIM IN RECORD", k, where); fail += 1
    else:
        print("quote ok:", k, where)
    if text not in P:
        print("QUOTE MISSING FROM BOOK", k); fail += 1
if Q["where"][1] not in flat(record("flows/bd0019/vision/transcriptNotFiles.md")):
    print("881 QUOTE NOT IN VISION FILE"); fail += 1
# the source, line by line, in the page text
for line in BODY.split("\n"):
    t = re.sub(r"^(## |- |> )", "", line).replace("`", "").replace("**", "")
    if line.startswith("```") or not t.strip():
        continue
    if t not in P:
        print("SOURCE LINE NOT VERBATIM:", t[:70]); fail += 1
codes = re.findall(r"```\n(.*?)\n```", BODY, re.S)
for c in codes:
    if f"<pre class=\"code\"><code>{esc(c)}</code></pre>" not in out:
        print("CODE BLOCK NOT EXACT:", c[:40]); fail += 1
print("code blocks", len(codes), "pre blocks", out.count("<pre"))
if out.count("<pre") != len(codes):
    print("EXTRA PRE (prose in code?)"); fail += 1
for s in ["Presentation.{ Title }", "TurnEndRequest.{ SessionId TurnId Option<TranscriptPath> }", "QueueTurnEnd", "landed signal-flow 6.3.0", "Mind Sol 5104af"]:
    if s not in record("flows/6997eb/log.md"):
        print("SOL CLAIM NOT IN LOG:", s); fail += 1
for pat in (r"<button", r"<a\s", r"<input", r"<select", r"<textarea", r"onclick", r"addEventListener\('click'", r'role="button"', r"tabindex", r"<details", r"<summary"):
    if re.search(pat, out):
        print("CONTROL FOUND:", pat); fail += 1
print("title", TITLE, "pages", N, "source sha256", hashlib.sha256(RAW.encode()).hexdigest())
print("book sha256", hashlib.sha256(out.encode()).hexdigest(), "bytes", len(out.encode()))
print("FAIL" if fail else "verbatim: all quotes and source lines OK; no controls")
sys.exit(1 if fail else 0)
