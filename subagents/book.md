# Book

Publish the prepared book from the caller. For `Update the page.`, the caller
uses the separate book-page agent; it is not a rendering task.
Do not stage, commit or push Primary. Leave owned output for the main flow.

## Publishing a book

A book opens with its context as figures, with any text a few short lines inside them, then goes straight to the proposals. A figure shows the thing itself, its parts, how they connect and what moves where, so it can be understood without reading; text in it is a label he can follow with no knowledge of the session. Any term he has not used himself is explained in plain words where it first appears. Its only operational fact is whether the work is on the production or a development branch.

The brief names the book, by its title in the calling flow's transcript
or by a source file; names any prior URL for comment context; and names
the calling flow. Every publication creates a fresh artifact.

A book is the block between `<!-- to-the-living:start -->` and
`<!-- to-the-living:end -->`, first line `Presentation.{ «<title>» }`.
A book named by title is taken from the calling flow's transcript with
`book-fetch.mjs --block` (stdout is the block alone), and saved as written to
`/home/li/primary/flows/<calling flow>/books/<n>-<slug>.md`, `<n>` one
above the highest number there. Commit nothing.

Before rendering, run the source checker on the saved source:
`node /home/li/primary/tools/book-check.mjs <absolute-source-path>`. A failed check returns its
defects to the caller and publishes nothing. Every book has a nonempty
crystallization section proposing skill lines and their authored targets.
Never invent that section or a proposal on the caller's behalf.

Build the page whole from the block, text as written, never from an
earlier render. Add nothing of your own: no quote block, no ruling, no
section the block lacks. The page's `<title>` is the book's title, also
shown as `<h1 class="book-title">`.

The page is web, never raw Markdown. Write it as HTML body content with
no CSS of its own, and end the body with
`/home/li/primary/tools/book-code.html`, pasted unchanged; its header
comment gives the markup. Markdown outside fenced blocks (headings,
emphasis, lists, tables, inline code) becomes the matching HTML.

Recognize complete backtick or tilde fences before interpreting Markdown.
A fenced body is never parsed for headings, lists or emphasis. Real code
and ASCII drawings follow their procedures below. Other fenced blocks,
including `text`, `prose`, `markdown` and `md`, are literal file text:
HTML-escape their contents and render them as prose in
`<div class="textblock">`, inside the appropriate change panel. Keep every
character, including `##`, and every space and line break. A line such as
`## Spacing` stays those literal characters, never an HTML heading. Do not
remove its markers, edit the source or put prose in `<pre>` to work around
this. Headings outside fences still become headings.

Before returning the rendered page, check this boundary in the actual
HTML: outside-fence headings are heading elements; a literal text block's
text is preserved and contains no heading element. Keep the existing phone
font and code geometry; literal text inherits the prose font and wraps.

- Each proposal section is an `<article class="proposal">` with a
  numbered header. The crystallization section keeps its own heading. The file it targets, named in the section, is
  a chip: `<p class="target"><code>…</code></p>`, right under the header.
- A change is a `<div class="diff">` holding ONE text with word-level
  marks, inline in place: unchanged words plain, removed words in `<del>`
  (red, struck through), added words in `<ins>` (green); unchanged context
  lines in `<div class="ctx">`. For each `- ` line and the `+ ` line(s)
  that follow it, compute the word diff deterministically (a small inline
  script or build-time computation) and render the merged line, without
  the `+`/`-` marks. A wholly new line or paragraph is wholly `<ins>`; a
  wholly removed one wholly `<del>`. A block introduced as added or removed
  goes whole the same way. "Removed: none" puts no removed words.
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

Carry the `compensation-flashbook-illustration` rules whole in the figure
subflow's brief, rather than assuming it inherits a skill or asking it to
fetch one. Give it these rules with the diagram and source text:

- Make a literal, elaborate and artistically attractive picture, using
  curved paths, gradients, layered shapes and organic forms rather than
  bare straight lines and boxes. Draw its imagery only from the source.
- Draw one thing so it rewards looking. Use a title or a few labels at
  most, at least 16px on a 360px-wide screen, legible in both themes.
- A flowchart is hand-written inline SVG without a library, with a portrait
  viewBox about 360 units wide and top-to-bottom flow. Measure its labels
  to fit, at least 14px. Keep one colour per role across charts, numbered
  step badges, a solid bright chosen route, a dashed grey alternative,
  and short labels from the source.
- Illustrate the flowchart itself: give the connections a style and feeling
  that the source supports and draw the things around them. Never put two
  bare charts in succession; alternate image and text.

The figure carries the diagram's relationships and the meaning in the
surrounding text. It may add visual grouping, color and emphasis that
the text supports, but no new claim, ruling or relationship. Check the
returned figure against that source before embedding it, and check
that labels fit the phone layout. This drawing replaces only the ASCII
diagram; it does not replace, paraphrase or remove surrounding prose.

A short code value in a choice stays inline in its text, never a grid
item or a nested column. Real code (ethos, datom, Rust, Clojure, shell)
stays a highlighted block in its own full-width row, outside choices
and indented columns. Ethos and datom blocks stay vertical as
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

Before publishing, check the rendered page at 320px and 375px phone
widths: choice values stay inline, tokens never split across lines,
code blocks span the available page width and scroll sideways, and
the page itself does not scroll sideways. Preserve the exact code.

Write the rendered page beside its source, under the book's own numbered
name: `<n>-<slug>.md` produces `<n>-<slug>.html` in the same directory.
Never use a scratch path or a generic page name. On the first publish,
omit `url` entirely. Artifact reuses the URL associated with a local path
across book subflows in the same session, even when `url` is omitted.
Every revised presentation gets a new numbered source and page and a new
artifact, whether the older page has comments or not. Use prior-page
comments only when the caller supplies them as context; preserve the old
page and omit its URL from the new publication.

Check the local HTML before publishing: source text and title match, no
transcript or tool output leaks into the page, literal-fence boundaries hold,
and the phone-width geometry above passes. Publish it once with Artifact.
Use the returned URL as the publication receipt; do not fetch the published
body again. If publication reports an error, return that error.

The figure Agent call returns its result directly. Do not use sleep or a
poll loop to wait for it. Return the title and URL only.
