<!-- to-the-living:start -->
Presentation.{ «What a book shows» }

# What a book shows

## psyche-context › vision/book.md

````markdown
## Books

A book is a proposal into context modules, and the whole of it is its crystallization: a line removed shows in red, a line added in green, and a figure in it is a figure proposed for a module.

A book carries the proposals; it shows no verbatim quote, and the records it draws from are not shown.

The records a proposal draws from live in an unrendered reference file, one per book, in a references/ directory beside the books; they are archived with the landing when some or all of the proposal is accepted.

The first edition of a book is mostly questions.

The book is the center of development: it is the evolution of an idea, and the list of unknowns lives in it.

A figure shows how a thing moves, one question per figure, readable in seconds. Its grammar: a box is a thing or a collection; an arrow is a one-way relation carrying a verb, so that box, verb, box reads as a sentence; nearness and enclosure are kinship; top to bottom is order; colour carries a role or is absent. A list in boxes, a tally, or a sentence in a rectangle is not a figure. A diagram in a book's source is ASCII in that grammar, laid out vertically and no wider than 52 characters so a phone shows it; a sketch without arrows is rewritten before it is sent. The published book never shows the ASCII, but a figure drawn from it by a Tertiary or Quaternary subflow that is given the grammar with the sketch, keeps every box, label and arrow, and adds nothing the source does not say; a figure that lost an arrow is returned. A sizable book carries several figures.

Markdown is never shown in a code block: a module written in Markdown is shown as rendered text.

## Pictures

An idea reaches the living as a picture first. A figure shows one thing, where the idea has a shape, and its colours and marks mean the same in every book.

A proposal is drawn as well as written: what it adds, removes and keeps, in one frame.

A proposal that touches a code component shows the code it changes or adds.

Every comment of his redoes the book it is on, unless the comment closes the topic; a book his comment affects is redone as well. A comment that opens a topic of its own gets a book of its own.
````

## field-context › compensation/book-crystallization.md

````markdown
A book shows current context modules and its crystallization proposals. Every proposal shows a word removed (red) or added (green) in a psyche module, or the code that line lands. A figure draws concepts as nodes linked by edges, with the forks, options and joins its subject has, each label a few words; its ASCII source is no wider than 52 characters. Nothing else is written.

Outside its proposals, a book shows only context modules as they stand, each under its repo › path; it has no prose sections of its own.

A changed figure is shown once, whole, in its new form.

A proposal heading reads `### Proposal N: repository › path`, followed by `, a new file` when the file is new. The heading names the location; no `File:` line appears in the body.

A page is built only by the book builder; a source it refuses goes back to its author.

Below the proposal heading, each removed line starts with "- ", each added line with "+ ", and unchanged lines around them with two spaces. Concise machine results and concrete blockers may be sent outside a book.

Every line inside a book's code block of real code is at most 52 characters; prose proposed for a file renders as text and wraps freely. A code block spans the full page width, outside nested or indented layout columns; the code inside keeps its own indentation, never wraps inside a token, and scrolls sideways. A short code value inside a choice stays inline. Check every book at phone width before publishing.

A proposed statement is drawn from the living's records read whole, with their exceptions and later statements on the same subject. A skill line in the author's brief shows where a statement lands, never what it says; the brief marks machine-skill text as the machine's. A count or date claim about the records is made only when the author has witnessed it.

A proposal to destroy or archive a record renders unmistakably apart from a landing: its own colour and a Destroy or Archive mark on the record it removes.

Before publishing, reconcile the relevant current direction and exclude what the living has voided. A new edition carries only what is unruled or changed since the living last read it; what he approved is landed, not shown again.

When the living's comments leave a topic open, a new book follows with the adaptation, or the inquiry, knowledge or compensation review it needs.

A proposed code change shows the value it sets on each host, not only the name it reads it from.

Every question in a book is one specific proposal: the exact lines it lands, in the named file, ruled land, amend or reject; a list of options without their lines is never asked.

Every figure in a published book is the Illustrator's drawing, passed to the builder with --figures; the builder's own drawing is never published.

A book puts vision to the living's ruling; the implementation of landed vision follows without a ruling of its own.

A diagram in a book's source is ASCII, no wider than52 characters; the published book never shows the ASCII, but a figure the Illustrator draws by the illustration rules, keeping every box, label and arrow of the source sketch and adding nothing the source does not say.

A proposal's heading names the file it lands in, by repository and path.

A book has no technical part; technical references stay out of the book.

A book is published only when every proposal names the file it lands in and carries the lines it adds, and every other section shows a current context module under its location, with no technical part; any other source goes back to its author unpublished.

A book has no technical part; location headings identify the context modules and proposals.
````

### Proposal 1: Replace · psyche-context › vision/book.md

- A book carries the proposals; it shows no verbatim quote, and the records it draws from are not shown.
+ A book carries context modules, as they stand and as they are proposed to change; it shows no verbatim quote, and the records it draws from are not shown.

Ruling: land, amend, or reject.

### Proposal 2: Replace · psyche-context › vision/book.md

  The first edition of a book is mostly questions.

- The book is the center of development: it is the evolution of an idea, and the list of unknowns lives in it.
+ The book is the center of development: it is the evolution of an idea, and each unknown in it is a question between alternative lines.

Ruling: land, amend, or reject.

### Proposal 3: Remove · psyche-context › vision/book.md

- An idea reaches the living as a picture first. A figure shows one thing, where the idea has a shape, and its colours and marks mean the same in every book.
+ A figure shows one thing, where the idea has a shape, and its colours and marks mean the same in every book.

Ruling: land, amend, or reject.

### Proposal 4: Add · psyche-context › vision/book.md

  Markdown is never shown in a code block: a module written in Markdown is shown as rendered text.

+ ## What a book shows
+
+ A book is context modules in the forms below, each under its repo › path; its headings, naming the module and the kind of change, are the only words it has of its own.
+
+ A module shown whole, as it stands, situates the landing.
+
+ A module shown beside another, both as they stand, serves comparison: psyche with knowledge, with compensation, with inquiry.
+
+ A line added shows in green.
+
+ A line removed shows in red.
+
+ A line replaced shows its removal and its addition together, and only the changed words are marked.
+
+ A new module shows whole in green, under the path it will have.
+
+ A module deleted shows whole in red, with a Destroy or Archive mark.
+
+ A dependency changed shows in the module's front matter: the dependency removed in red, the dependency added in green.
+
+ A question between alternative lines shows each alternative as its own proposal, with the exact lines it lands; the living rules land, amend or reject.
+
+ A figure shows as proposed for the module it will live in.

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

Ruling: land, amend, or reject.

### Proposal 5: Question (a), a moved line is two proposals · psyche-context › vision/book.md

  A module deleted shows whole in red, with a Destroy or Archive mark.

+ A line moved between modules is a removal in the module it leaves and an addition in the module it enters, each its own proposal.

  A dependency changed shows in the module's front matter: the dependency removed in red, the dependency added in green.

Ruling: land, amend, or reject.

### Proposal 6: Question (b), a moved line is one proposal · psyche-context › vision/book.md

  A module deleted shows whole in red, with a Destroy or Archive mark.

+ A line moved between modules is one proposal headed by both paths: the line in red under the module it leaves, the same line in green under the module it enters.

  A dependency changed shows in the module's front matter: the dependency removed in red, the dependency added in green.

Ruling: land (a), land (b), amend, or reject.
<!-- to-the-living:end -->
