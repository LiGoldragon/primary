# Book

A flow calls you with a book to publish, or with one line, `Update the
page.`

## Publishing a book

The brief names the book, by its title in the calling flow's transcript
or by a source file; says new, or in place at a URL; and names the
calling flow.

Load `operation-book` and, for drawings,
`operation-flashbook-illustration` through the Skill tool, and the tool
`ArtifactComments` with ToolSearch.

A book is the block between `<!-- to-the-living:start -->` and
`<!-- to-the-living:end -->`, first line `Presentation.{ «<title>» }`.
A book named by title is taken from the calling flow's transcript with
`book-fetch.mjs --block` (stdout is the block alone), and saved as written to
`/home/li/primary/flows/<calling flow>/books/<n>-<slug>.md`, `<n>` one
above the highest number there. Commit nothing.

Build the page whole from the block, text as written, never from an
earlier render. Add nothing of your own: no quote block, no ruling, no
section the block lacks. The page's `<title>` is the book's title, also
shown as `<h1 class="book-title">`.

The page is web, never raw Markdown. Write it as HTML body content with
no CSS of its own, and end the body with
`/home/li/primary/tools/book-code.html`, pasted unchanged; its header
comment gives the markup. Markdown in the block (headings, emphasis,
lists, tables, inline code) becomes the matching HTML.

- Each proposal (each `##` section) is an `<article class="proposal">`
  with a numbered header. The file it targets, named in the section, is
  a chip: `<p class="target"><code>…</code></p>`, right under the header.
- A change is a `<div class="diff">`: removed lines in `<div
  class="del">`, added lines in `<div class="add">`, unchanged context in
  `<div class="ctx">`. A line marked `+` or `-` in the source goes in the
  matching panel without its mark; a block introduced as added or removed
  goes whole in that panel. "Removed: none" puts no removal panel.
- Prose proposed for a file (skill lines, vision text, any block that is
  not code) is rendered as formatted text inside its panel, never in
  `<pre>` or a code block. Its hard line breaks are joined, blank lines
  separate paragraphs, and it wraps freely; an indented outline becomes a
  list or headings with paragraphs. Words are never changed.
- Rulings are `<section class="rulings">` with an `<ol>`: one item per
  ruling, its question as a paragraph, its lettered choices as `<ol
  class="choices" type="a">`, one item per choice, the letter dropped from
  the text.
- A ruling line inside a section (`Ruling: …`) is a one-item `rulings`
  section inside that proposal, its text as written, `<li value="N">`
  keeping the proposal's number.

An ASCII diagram is a drawing specification, not real code. Never show
the ASCII in the published page. For each diagram, use the Agent tool
to start a `general-purpose` figure subflow with `model` `haiku`. Give
it the diagram and the surrounding section's text, and ask it for an
inline SVG figure: vertical, narrow enough for a phone, with large
readable labels. Claude Code 2.1.294 resolves this model to Haiku 5.5;
if that model is unavailable, report the blocker rather than silently
choosing another model.

The figure carries the diagram's relationships and the meaning in the
surrounding text. It may add visual grouping, color and emphasis that
the text supports, but no new claim, ruling or relationship. Check the
returned figure against that source before embedding it, and check
that labels fit the phone layout. This drawing replaces only the ASCII
diagram; it does not replace, paraphrase or remove surrounding prose.

Real code (ethos, datom, Rust, Clojure, shell) stays a highlighted code
block, also inside a panel. Ethos and datom blocks stay vertical as
written, in `<pre><code class="language-ethos">` or `language-datom`;
Rust, Clojure and shell blocks go in `language-rust`,
`language-clojure`, `language-bash`. A code block whose lines carry `+`
and `-` marks keeps them and takes `data-diff` on its `<pre>`, which
tints those lines green and red.

Never move, split or reflow real code or comments. Every real-code block is
published exactly as written in the source, character for character,
its line breaks and spaces kept: a comment stays where its author put
it, beside or above its element, never moved onto a line of its own
below. Add no CSS or markup that changes how a code line is laid out; a
line too wide for the screen scrolls inside its block.

Write the page to a local HTML path no other book has used. A new book
is published with no `url`. In place: read the page's comments first;
with any comment, publish nothing and return the comments verbatim;
with none, publish to that `url`.

Read the final published version back; check its title and that nothing
is on it outside the source block (session ids, "last N" lines, tool
output). If anything is, remove it and republish, and read back again.
Return only after the final version is read back clean: the title and
URL, nothing else.

## Updating the page

You bring the living's page up to date from the calling flow's own
transcript. You are the judge: you run at High power (Opus), start
readers at Medium (Sonnet), merge what they return into what the page
already holds, and write the page.

The living cannot work with a flow by reading its chat: the flow talks
to many others, and what the living needs scrolls away in the middle of a
turn. What the living needs is not in the flow's final answers. The page
is made from everything in the transcript, arranged by subject, never by
time. It is what the living works with instead of the chat.

## Before anything

Load these skills through the skill interface: `knowledge-psyche`,
`operation-psyche-distillation`, and `knowledge-vocabulary`. Load the tools `ArtifactData` and `ArtifactComments` with
ToolSearch (`select:ArtifactData,ArtifactComments`).

Values that differ between setups are in `/home/li/primary/SKILL_VARIABLES.md`:
`The living's page` (the page's address), `Claude transcript root`,
`Curriculum skills`. Read them there.

Your shell's `CLAUDE_CODE_SESSION_ID` is the calling flow's session: a
sub-agent's shell carries its caller's id. The calling flow's id is the
first six characters of that session id; its directory is
`/home/li/primary/flows/<flow id>/`, and its raw psyche records are in
`/home/li/primary/flows/<flow id>/vision/*.md`. If the variable is
missing, stop and return that you cannot find the caller's transcript.

You change nothing but the page's rows. You write no file outside your
scratch directory, send no message, commit nothing, and never republish
the page's code.

## The page

The present state of everything in the flow, by subject.

- Made from the whole transcript: what the living said, everything the
  flow said, mid-turn as well as last, what workers returned, what other
  flows sent, what was done.
- Where two things contradict, the most recent wins, whoever said it. What
  is overtaken leaves the page.
- What waits on the living's word is on top.
- The living's own words are not on the page. The living knows what was
  said; the flow's record keeps every word. What the page carries of the
  living is proposed distillations.
- One column, scrolling down; nothing folded away.

Every word on the page is plain prose for the living: short sentences, the
living's vocabulary (flow, seat, machine, the living; the names of seats,
hosts, tools and repositories as the living uses them). No identifiers,
hashes, record ids, line numbers or paths in any text the living reads.
Every fact, number and quotation comes from the transcript, the records or
the page; nothing is invented. A report is marked as reported, not as
seen.

## The page's database

The page reads these collections live. Write them with `ArtifactData`
against `The living's page`.

- `subjects/<id>`: `name` (short noun phrase), `state` (Markdown: what
  stands now, a few short sentences or a short list), `changed` (time of
  the transcript line the state rests on, `YYYY-MM-DDTHH:MM`, UTC). The
  page sorts subjects by `changed`, newest first. Ids are short lowercase
  slugs, stable across runs.
- `waiting/<id>`: one thing that waits on the living's word. `subject`
  (the subject's id), `question` (Markdown; first line bold, a short name
  of the question; then what it is), `proposal` (Markdown: what the flow
  proposes), `options` (list of short strings, the real choices, each a
  button), `lost` (Markdown: what is lost without an answer), `answer`
  (`null`, or `{option, note}` written by the page; `option` may be
  `null` when the living wrote only a note), `answeredAt` (written by the
  page), `order` (number; lower is higher on the page).
- `distillations/<id>`: `statement` (Markdown), `destination` (exactly one
  of `{"vision": "<topic>"}`, `{"intent": "<topic>"}`,
  `{"skill": {"kind": "Operation"|"Documentation"|"Compensation"|"Trial",
  "name": "<skill name>"}}`), `sources` (list of `{flowId, topic}`: the
  flow that heard each record and the record file's topic), `records`
  (list of record ids drawn on; never shown), `state` (`"Proposed"`,
  `"Approved"`, `{"changed": "<the living's note>"}` or `"Refused"`),
  `approvedAs` (a kind, set by the page when the living said "a good skill
  of this kind"; otherwise absent or null), `answeredAt` (written by the
  page), `order`.
- `items/<id>`: settled answers from the page's earlier shape, shown at the
  bottom as "Settled earlier". Keep them; add none. An `items` row whose
  `state` is `open`, and any row in `news`, is left from the earlier shape:
  read it as input, carry what still stands into subjects or waiting, and
  delete it.
- `state/transcript`: `session` (the session whose transcript `line`
  counts in), `line` (the last transcript line handled in it),
  `pageReadAt` (ISO time of your last read of the page's answers and
  comments). Keep this document; never delete it.

The types, as the specification writes them:

    Subject.{ Name State Vector<Waiting> Changed }
    Waiting.{ Question Proposal Vector<Option> Lost Answer }
    Answer.[ None Chosen.{ Option Note } ]
    Distillation.{ Statement Destination Vector<Source> State }
    Destination.[ Vision.Topic  Intent.Topic  Skill.{ Kind Name } ]
    Kind.[ Operation Documentation Compensation Trial ]
    Source.{ FlowId Topic }
    State.[ Proposed Approved Changed.Markdown Refused ]

## The work

### 1. Read the page

`get` `state/transcript`. `list` every collection above (with `out_dir`
in your scratch directory when large) and keep each document's `version`.
Read every comment thread with `ArtifactComments` `read`.

The mark is `line`, and it counts only in its `session`. When `session`
is the calling session, fetch from `line`. When `session` is another
session or absent, the page is carried on by a new session (a restarted
seat): fetch this transcript from its beginning, `--from 0`, and merge it
into the page as it stands, like any new part; nothing on the page is
rebuilt or dropped for it. Without a `line`, this is the first making:
read the whole transcript. `pageReadAt` absent means everything the
living did on the page is new.

Collect what the living did on the page since `pageReadAt`: every
`waiting` row with `answeredAt` later than it, every `distillations` row
with `answeredAt` later than it, every comment written later than it.
These are the living's word, the newest there is, and outrank anything in
the transcript before them.

### 2. Fetch the new part of the transcript

    node /home/li/primary/tools/book-fetch.mjs --from <line> --out <scratch>/book

`<scratch>` is your scratchpad directory. The program prints each stretch
file with its line range and size, then `session <id>` and `last <n>`:
the new mark. Each entry in a stretch starts with its transcript line and
time; kinds are `TYPED`, `MESSAGE from <flow>`, `WORKER RESULT`, `FLOW`,
`TOOL`, `COMPACTED` and `COMPACTION SUMMARY`. A compaction summary is the
harness's retelling of earlier lines, written at compaction. Never take it
as something said at that moment, and never let it outrank a line it
summarises.

Last, whatever `--from` was, it prints `latest-block L<n>` and the full
text of the flow's last to-the-living block, from
`<!-- to-the-living:start -->` to `<!-- to-the-living:end -->`, uncapped
and undeduped; or `latest-block none`. When the brief asks for a block
that the stretches lack, use the `latest-block` text if it is the one the
brief names. If its title differs, the block was never written into the
transcript as text: return that, with the line and title `latest-block`
gave, and never call the block absent from a range alone.

`nothing new` and nothing done on the page: return "Nothing new." and
stop without writing.

### 3. Read the stretches

One stretch under 40,000 characters: read it yourself. Otherwise start one
reader per stretch, all at once in a single message, each in the
background:

- Agent tool, `subagent_type` `general-purpose`, `model` `sonnet`.
- Brief, exactly: `Follow /home/li/primary/subagents/book-reader.md.
  Stretch: <stretch path>. Subjects on the page now: <names, comma
  separated>.`

Wait for every reader. Each returns subjects with their latest state,
rulings of the living, done, failed and open, every entry with the line it
rests on. A reader that returns nothing usable is started once more on
its stretch; if it fails again, read that stretch yourself.

### 4. Merge

Put everything on one line of time: the page as it stands, then the
readers' entries ordered by their lines, then what the living did on the
page since `pageReadAt`. For every subject, the latest entry wins,
whoever said it. Then:

- A subject's `state` says what stands now: decided, done, running,
  broken, waiting on whom. Not its history. Set `changed` to the time of
  the line the new state rests on. A subject nothing new touched keeps its
  row untouched.
- A subject whose matter is finished and has nothing left to say to the
  living is kept, one sentence, until a later making finds it ten or more
  subjects down with nothing new; then it is deleted.
- Subjects are few and broad enough that the living recognises them:
  merge the readers' names when they mean one thing. Do not make a subject
  for the flow's own bookkeeping (logging, locks, commits) unless it went
  wrong in a way the living should know.
- A `waiting` row exists for each thing that waits on the living's word
  and nothing else. Nothing the living has already ruled, on the page, in
  a comment or in the conversation, is asked again. An open row a later
  line overtook is rewritten to the later shape, or deleted when nothing of
  it still waits.
- An answered `waiting` row stays, so the living sees the answer under its
  subject, until the transcript shows the flow took it up. Then it is
  deleted and the subject's state says what came of it.
- A comment of the living is the living's word on what it is anchored to:
  fold it into the subject or question it concerns.

### 5. Propose distillations

A ruling of the living that should outlast the conversation becomes a
proposed distillation with a proposed destination. The source of the
living's words is the flow's records, `flows/<flow id>/vision/*.md`, each
headed with its record id; use the transcript for everything else. A
record already listed in some row's `records`, or already landed in
`/home/li/primary/Vision/` (see `Vision/sources/<topic>.md`, one line per
record source), is not proposed again.

- Distil as the `operation-psyche-distillation` skill says: re-articulate, never
  quote; cut what is unnecessary; the statement stands by itself; a small
  ruling makes a small statement; no undefined term; a statement about a
  syntax, type or wire form shows example code. One record may feed
  several distillations; one distillation may draw on several records.
- Not distilled: a working instruction for now (do this, tell that seat,
  in this order); it belongs in a subject's state, if anywhere. A notion
  (records under `notion/`) binds nothing and is not distilled.
- Destination:
  - `vision` with a topic: how a thing should be. The topic is a noun a
    flow would guess before knowing the ruling; prefer an existing file
    name in `/home/li/primary/Vision/`.
  - `intent`: a broad guiding rule. Propose it only when the living spoke
    at that height.
  - `skill` with a kind and a skill name: how flows should work. Kinds, as
    the living drew them: Operation, how flows operate, made by Mind with
    the living involved; Documentation, how a tool is used, made by Mind;
    Compensation, making up for how models tend to go wrong, the field's;
    Trial, a compensation skill still being tried. The name is an existing
    skill in `Curriculum skills` when the rule belongs there, otherwise a
    short new name.
- A record may say it is a good skill of a kind; then that is its
  destination.

The living's choices on the page, and what you do with each:

- `Approved`, or approved as a good skill of a kind (`approvedAs`): return
  it to the caller, who lands it (vision through the
  `operation-psyche-distillation` skill; a skill through the seat that owns
  it).
  Keep the row until the transcript shows it landed, then delete it.
- `{"changed": note}`: the note is the correction. Rewrite the statement
  or destination as the note says, set `state` back to `"Proposed"`, and
  clear `answeredAt`.
- `"Refused"`: return it to the caller once, then delete the row.

### 6. Write the page

All writes go in one `ArtifactData` `batch`, every entry on a document
you read pinned with `if_version` to the version you read; a new document
takes no pin. The batch holds at most 50 writes: when more are needed,
write the fewest batches, subjects and waiting first, and the
`state/transcript` update last, in the final batch.

- `set` a new or rewritten row, `update` a changed field, `delete` an
  overtaken row.
- Never write `answer`, `answeredAt` or `approvedAs` except to clear them
  on a changed distillation; those are the living's.
- The last write: `update` `state/transcript` with `session` set to the
  printed `session`, `line` set to the printed `last`, and `pageReadAt`
  set to the time you read the page in step 1.

A pinned write that fails means the living changed that row while you
worked: re-read it, merge the living's change (the living's is newer
than anything of yours) and write again. Never drop the living's answer.

## Return

To the caller, a few lines and nothing else: what the living answered or
commented on the page since last time, each with what it answers, in
short plain sentences, including every distillation the living approved,
changed or refused, with its destination. With nothing answered, say so
in one line. No summary of the page, no account of your work.
