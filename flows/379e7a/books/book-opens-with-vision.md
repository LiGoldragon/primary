<!-- to-the-living:start -->
Presentation.{ «A book opens with its vision» }

# A book opens with its vision

### Proposal 1: psyche-context › vision/book.md

**Comment** After the line that says what a book carries: the book opens with the vision proposals, then the case. The figure shows the order.

  A book carries context modules, as they stand and as they are proposed to change; it shows no verbatim quote, and the records it draws from are not shown.
+
+ A book opens with its vision proposals. The case follows: the context modules of the system it concerns, of related systems and of its ancestors, as they stand, and the compensation removed if the vision passes.

```
+------------------+
| vision proposal  |
+------------------+
        | is argued by
        v
+------------------+
| the case:        |
| modules as they  |
| stand            |
+------------------+
        | if it passes,
        | removes
        v
+------------------+
| conflicting      |
| compensation     |
+------------------+
```

### Proposal 2: psyche-context › vision/book.md

**Comment** Beside the line that says a compensation line reaches a book only to be removed: the removal is not left to the line alone, it follows from the vision that passes.

  A compensation line reaches a book only to be removed: the book shows the vision that makes it unnecessary and the line's deletion.
+
+ When a vision passes, every compensation line that conflicts with it is removed.

## psyche-context › vision/book.md

## Books

A book is a proposal into context modules, and the whole of it is its crystallization: a line removed shows in red, a line added in green, and a figure in it is a figure proposed for a module.

A book carries context modules, as they stand and as they are proposed to change; it shows no verbatim quote, and the records it draws from are not shown.

The records a proposal draws from live in an unrendered reference file, one per book, in a references/ directory beside the books; they are archived with the landing when some or all of the proposal is accepted.

The book is the center of development: it is the evolution of an idea, and each unknown in it is shown as an inquiry context module.

An inquiry context module is shown for one of three uses: to contrast with a vision being proposed, or to explain why that vision is proposed; to bring a question plainly to the living; or to compare with the implementation or the knowledge that may cover it.

A figure shows how a thing moves, one question per figure, readable in seconds. Its grammar: a box is a thing or a collection; an arrow is a one-way relation carrying a verb, so that box, verb, box reads as a sentence; nearness and enclosure are kinship; top to bottom is order; colour carries a role or is absent. A list in boxes, a tally, or a sentence in a rectangle is not a figure. A diagram in a book's source is ASCII in that grammar, laid out vertically and no wider than 52 characters so a phone shows it; a sketch without arrows is rewritten before it is sent. The published book never shows the ASCII, but a figure drawn from it by a Tertiary or Quaternary subflow that is given the grammar with the sketch, keeps every box, label and arrow, and adds nothing the source does not say; a figure that lost an arrow is returned. A sizable book carries several figures.

Markdown is never shown in a code block: a module written in Markdown is shown as rendered text.

## What a book shows

A book is context modules in the forms below, each under its repo › path; its headings, naming the module and the kind of change, are the only words it has of its own.

A module shown whole, as it stands, situates the landing.

A module shown beside another, both as they stand, serves comparison: psyche with knowledge, with compensation, with inquiry.

A line added shows in green.

A line removed shows in red.

A line replaced shows its removal and its addition together, and only the changed words are marked.

A new module shows whole in green, under the path it will have.

A module deleted shows whole in red, with a Destroy or Archive mark.

A line moved between modules is one proposal headed by both paths: the line in red under the module it leaves, the same line in green under the module it enters.

A dependency changed shows in the module's front matter: the dependency removed in red, the dependency added in green.

A module is leaned out by removing a line that repeats another, shown beside the line that makes it unnecessary; the compensation module is leaned out first, because vision replaces it.

A compensation line reaches a book only to be removed: the book shows the vision that makes it unnecessary and the line's deletion.

A question between alternative lines shows each alternative as its own proposal, with the exact lines it lands; the living rules land, amend or reject.

A figure shows as proposed for the module it will live in.

```
+--------------------------------------------+
| context module                             |
+--------------------------------------------+
    |              |                |
    | stays        | changes        | is born or
    |              |                | is deleted
    v              v                v
+-----------+ +------------+ +--------------+
| shown     | | line added | | shown whole, |
| whole or  | | in green,  | | in green or  |
| beside    | | removed in | | in red       |
| another   | | red        | +--------------+
+-----------+ +------------+        |
                    |               |
                    | proposed as   | proposed as
                    v               v
+--------------------------------------------+
| a proposal: land, amend or reject          |
+--------------------------------------------+
```

## Pictures

A figure shows one thing, where the idea has a shape, and its colours and marks mean the same in every book.

A proposal is drawn as well as written: what it adds, removes and keeps, in one frame.

A proposal that touches a code component shows the code it changes or adds.

Every comment of his redoes the book it is on, unless the comment closes the topic; a book his comment affects is redone as well. A comment that opens a topic of its own gets a book of its own.

## field-context › compensation/book.md

Make one new presentation for each message. A presentation is a new living-messenger user-interface item, never an update of a presentation that has comments.

Present the source faithfully and simply. The living responds by comment; use no buttons, fields, or other controls.

A figure draws concepts as nodes linked by edges, with the forks, options and joins its subject has, each label a few words; its ASCII source is no wider than 52 characters.
The book subflow obtains each figure from the Illustrator role composed by Curriculum; the page carries the resulting inline SVG, readable on a phone, never the ASCII or Mermaid.

A presentation renders as a web page, never raw Markdown or prose in a code block. A proposed change shows its additions in green and its removals struck through in red, in one consistent style across books.

A book's reference file is references/<book-source-basename>.md in the directory holding the book's source, written with the source; it lists, per proposal, the records each line draws from. When a proposal lands, its entries move to references/archive/ with the landing commit named.

A page is republished from its local source; a page read back from the host is never copied over that source.

A change to the book builder rebuilds every published book and compares it with the previous build before it is used.

After publication is complete, return its title and URL to the requester
with a very short voice answer to the question.

Use the book role composed by Curriculum to publish the exact source. Check it with tools/book-check.mjs before rendering. A non-Claude
caller sends its source to its Secondary; it
does not hand-render a replacement page. If the source lacks crystallization,
return the defect to its author rather than adding a proposal.

## field-context › compensation/book-crystallization.md

A book shows current context modules and its crystallization proposals. Every proposal shows a word removed (red) or added (green) in a psyche module, or the code that line lands. A figure draws concepts as nodes linked by edges, with the forks, options and joins its subject has, each label a few words; its ASCII source is no wider than 52 characters. Nothing else is written.

A changed figure is shown once, whole, in its new form.

A proposal heading reads `### Proposal N: repository › path`, followed by `, a new file` when the file is new. The heading names the location; no `File:` line appears in the body.

A page is built only by the book builder; a source it refuses goes back to its author.

Below the proposal heading, each removed line starts with "- ", each added line with "+ ", and unchanged lines around them with two spaces. Concise machine results and concrete blockers may be sent outside a book.

Every line inside a book's code block of real code is at most 52 characters; prose proposed for a file renders as text and wraps freely. A code block spans the full page width, outside nested or indented layout columns; the code inside keeps its own indentation, never wraps inside a token, and scrolls sideways. A short code value inside a choice stays inline. Check every book at phone width before publishing.

A proposed statement is drawn from the living's records read whole, with their exceptions and later statements on the same subject. A skill line in the author's brief shows where a statement lands, never what it says; the brief marks machine-skill text as the machine's. A count or date claim about the records is made only when the author has witnessed it.

Before publishing, reconcile the relevant current direction and exclude what the living has voided. A new edition carries only what is unruled or changed since the living last read it; what he approved is landed, not shown again.

A proposed code change shows the value it sets on each host, not only the name it reads it from.

Every figure in a published book is the Illustrator's drawing, passed to the builder with --figures; the builder's own drawing is never published.

A book puts vision to the living's ruling; the implementation of landed vision follows without a ruling of its own.

A book has no technical part; technical references stay out of the book.

### Proposal 3: field-context › compensation/book-crystallization.md

**Comment** Removed if Proposal 1 passes. The vision that makes it unnecessary: «A book carries context modules, as they stand and as they are proposed to change»; «A line added shows in green. A line removed shows in red.»; the figure grammar of vision/book.md (a box, a verb on an arrow, top to bottom, ASCII no wider than 52 characters). "Nothing else is written" conflicts with Proposal 1, which adds the case to the book.

- A book shows current context modules and its crystallization proposals. Every proposal shows a word removed (red) or added (green) in a psyche module, or the code that line lands. A figure draws concepts as nodes linked by edges, with the forks, options and joins its subject has, each label a few words; its ASCII source is no wider than 52 characters. Nothing else is written.

### Proposal 4: field-context › compensation/book-crystallization.md

**Comment** Removed if the vision passes. The vision that makes it unnecessary: «a figure in it is a figure proposed for a module», «A proposal that touches a code component shows the code it changes or adds», and «the records it draws from are not shown».

  Every figure in a published book is the Illustrator's drawing, passed to the builder with --figures; the builder's own drawing is never published.

  A book puts vision to the living's ruling; the implementation of landed vision follows without a ruling of its own.

- A book has no technical part; technical references stay out of the book.

### Proposal 5: field-context › compensation/book.md

**Comment** Removed if the vision passes. The vision that makes it unnecessary: the figure grammar of vision/book.md, a box and an arrow carrying a verb, laid out vertically and «no wider than 52 characters», which replaces nodes and edges.

- A figure draws concepts as nodes linked by edges, with the forks, options and joins its subject has, each label a few words; its ASCII source is no wider than 52 characters.
  The book subflow obtains each figure from the Illustrator role composed by Curriculum; the page carries the resulting inline SVG, readable on a phone, never the ASCII or Mermaid.

### Proposal 6: field-context › compensation/book.md

**Comment** Removed if the vision passes. The vision that makes it unnecessary: «Markdown is never shown in a code block: a module written in Markdown is shown as rendered text.», «A line added shows in green.», «A line removed shows in red.» and «its colours and marks mean the same in every book».

- A presentation renders as a web page, never raw Markdown or prose in a code block. A proposed change shows its additions in green and its removals struck through in red, in one consistent style across books.

### Proposal 7: field-context › compensation/psyche-interraction.md

**Comment** Under Conversation. Removed if the vision passes. The vision that makes it unnecessary: «its headings, naming the module and the kind of change», and «A line replaced shows its removal and its addition together». The two sentences after it stay.

- A proposal to the living names the psyche module, the lines removed, and the lines that replace them, verbatim. A book carries no "unknown" where a measurement is possible; the measurement is made first. A book that restates his words without a point is not sent.
+ A book carries no "unknown" where a measurement is possible; the measurement is made first. A book that restates his words without a point is not sent.

<!-- to-the-living:end -->
