Presentation.{ «What a book is, 2nd edition» }

# What a book is, 2nd edition

```
          +----------------------+
          | a question of his    |
          +----------+-----------+
                     | names
                     v
          +----------------------+
          | a topic              |
          +----------+-----------+
                     | has
                     v
          +----------------------+
          | the topic's book     |
          +----------+-----------+
       shows         | proposes
       +-------------+-------------+
       v                           v
+---------------+        +------------------+
| modules as    |        | proposals        |
| they stand    |        | red / green      |
+---------------+        | code that lands  |
                         | figure, drawn    |
                         +---------+--------+
                                   | ruled
                                   v
                         +------------------+
                         | land amend reject|
                         +------------------+
```

## psyche-context › vision/book.md

```markdown
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
```


### Proposal 1: one specification of a book, the past removed · psyche-context › vision/book.md

- A book is a proposal into context modules, and the whole of it is its crystallization: a line removed shows in red, a line added in green, and a figure in it is a figure proposed for a module.
+ A book answers a question of the living on one topic. Every question he asks is answered in a book, never in chat; questions on one topic are gathered into the topic's book; a question on a topic that already has a book is answered by that book's next edition.
+
+ A book shows two things and nothing else. The first is each context module the topic lives in, as it stands, rendered as text under its location; it is not ruled. The second is its proposals: each names the file it lands in, carries the lines it removes, in red, the lines it adds, in green, and the code that lands it, and is ruled land, amend or reject. Every question in a book is such a proposal. A book has no prose of its own: no survey, no quotation, no history, no technical part.
+
+ A refresh carries a second look: the flow finds why the topic has not gone through, and the edition lands the line whose absence let it recur, the proposal's heading naming the fault it closes. A cause the flow has not witnessed is proposed as a hypothesis, named so.

  A book carries the proposals; it shows no verbatim quote, and the records it draws from are not shown.

  The records a proposal draws from live in an unrendered reference file, one per book, in a references/ directory beside the books; they are archived with the landing when some or all of the proposal is accepted.

- The first edition of a book is mostly questions.
-
- The book is the center of development: it is the evolution of an idea, and the list of unknowns lives in it.
+ The book is the center of development: it is the evolution of an idea, and an unknown of the idea is in it as the proposal that would settle it.

- A figure shows how a thing moves, one question per figure, readable in seconds. Its grammar: a box is a thing or a collection; an arrow is a one-way relation carrying a verb, so that box, verb, box reads as a sentence; nearness and enclosure are kinship; top to bottom is order; colour carries a role or is absent. A list in boxes, a tally, or a sentence in a rectangle is not a figure. A diagram in a book's source is ASCII in that grammar, laid out vertically and no wider than 52 characters so a phone shows it; a sketch without arrows is rewritten before it is sent. The published book never shows the ASCII, but a figure drawn from it by a Tertiary or Quaternary subflow that is given the grammar with the sketch, keeps every box, label and arrow, and adds nothing the source does not say; a figure that lost an arrow is returned. A sizable book carries several figures.
+ A figure stands where the idea has a shape: a branch, a loop, a join, a comparison; it shows one thing, readable in seconds, and its colours and marks mean the same in every book. Its grammar: a box is a thing or a collection; an arrow is a one-way relation carrying a verb, so that box, verb, box reads as a sentence; nearness and enclosure are kinship; top to bottom is order; colour carries a role or is absent. A list in boxes, a tally, or a sentence in a rectangle is not a figure. The source carries a figure as an ASCII sketch in that grammar; the published book shows the Illustrator's drawing of it, keeping every box, label and arrow and adding nothing the sketch does not say. A book is published only with every figure drawn, and a book he asked to see with visuals is not published before it has them.

  Markdown is never shown in a code block: a module written in Markdown is shown as rendered text.

- ## Pictures
-
- An idea reaches the living as a picture first. A figure shows one thing, where the idea has a shape, and its colours and marks mean the same in every book.
-
- A proposal is drawn as well as written: what it adds, removes and keeps, in one frame.
-
  A proposal that touches a code component shows the code it changes or adds.

  Every comment of his redoes the book it is on, unless the comment closes the topic; a book his comment affects is redone as well. A comment that opens a topic of its own gets a book of its own.
+
+ A rule of the book lives in this module, or in the book tools as its machinery, never only in a flow's brief or a compensation module: a fault that recurs across books is a line missing here.

Ruling: land, amend, or reject.

```
+--------------------+
| living asks        |
+---------+----------+
          | on a topic
          v
+--------------------+   none   +------------------+
| topic's book?      +--------->| first edition    |
+---------+----------+          +--------+---------+
          | exists                       |
          v                              |
+--------------------+                   |
| next edition with  |                   |
| a second look      |                   |
+---------+----------+                   |
          +-------------+----------------+
                        v
              +--------------------+
              | book-check refuses |
              | or passes          |
              +---------+----------+
                        | passes
                        v
              +--------------------+
              | Illustrator draws  |
              | every sketch       |
              +---------+----------+
                        | gives figures
                        v
              +--------------------+
              | book-build builds  |
              +---------+----------+
                        | publishes
                        v
              +--------------------+
              | living rules       |
              +---------+----------+
                        | comments
                        v
              +--------------------+
              | next edition       |
              +--------------------+
```

## field-context › compensation/book-crystallization.md

```markdown
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

A diagram in a book's source is ASCII, no wider than52 characters; the published book never shows the ASCII, but a figure the Illustrator draws of the same idea by the illustration rules, free of the source's boxes and arrows.

A proposal's heading names the file it lands in, by repository and path.

A book has no technical part; technical references stay out of the book.

A book is published only when every proposal names the file it lands in and carries the lines it adds, and every other section shows a current context module under its location, with no technical part; any other source goes back to its author unpublished.

A book has no technical part; location headings identify the context modules and proposals.
```


### Proposal 2: the compensation keeps the machinery only · field-context › compensation/book-crystallization.md

- A book shows current context modules and its crystallization proposals. Every proposal shows a word removed (red) or added (green) in a psyche module, or the code that line lands. A figure draws concepts as nodes linked by edges, with the forks, options and joins its subject has, each label a few words; its ASCII source is no wider than 52 characters. Nothing else is written.
-
- Outside its proposals, a book shows only context modules as they stand, each under its repo › path; it has no prose sections of its own.
-
  A changed figure is shown once, whole, in its new form.

  A proposal heading reads `### Proposal N: repository › path`, followed by `, a new file` when the file is new. The heading names the location; no `File:` line appears in the body.

  A page is built only by the book builder; a source it refuses goes back to its author.

  Below the proposal heading, each removed line starts with "- ", each added line with "+ ", and unchanged lines around them with two spaces. Concise machine results and concrete blockers may be sent outside a book.

  Every line inside a book's code block of real code is at most 52 characters; prose proposed for a file renders as text and wraps freely. A code block spans the full page width, outside nested or indented layout columns; the code inside keeps its own indentation, never wraps inside a token, and scrolls sideways. A short code value inside a choice stays inline. Check every book at phone width before publishing.

  A proposed statement is drawn from the living's records read whole, with their exceptions and later statements on the same subject. A skill line in the author's brief shows where a statement lands, never what it says; the brief marks machine-skill text as the machine's. A count or date claim about the records is made only when the author has witnessed it.

  A proposal to destroy or archive a record renders unmistakably apart from a landing: its own colour and a Destroy or Archive mark on the record it removes.

  Before publishing, reconcile the relevant current direction and exclude what the living has voided. A new edition carries only what is unruled or changed since the living last read it; what he approved is landed, not shown again.

- When the living's comments leave a topic open, a new book follows with the adaptation, or the inquiry, knowledge or compensation review it needs.
-
  A proposed code change shows the value it sets on each host, not only the name it reads it from.

- Every question in a book is one specific proposal: the exact lines it lands, in the named file, ruled land, amend or reject; a list of options without their lines is never asked.
-
- Every figure in a published book is the Illustrator's drawing, passed to the builder with --figures; the builder's own drawing is never published.
-
- A book puts vision to the living's ruling; the implementation of landed vision follows without a ruling of its own.
-
- A diagram in a book's source is ASCII, no wider than52 characters; the published book never shows the ASCII, but a figure the Illustrator draws of the same idea by the illustration rules, free of the source's boxes and arrows.
-
- A proposal's heading names the file it lands in, by repository and path.
-
- A book has no technical part; technical references stay out of the book.
-
- A book is published only when every proposal names the file it lands in and carries the lines it adds, and every other section shows a current context module under its location, with no technical part; any other source goes back to its author unpublished.
-
- A book has no technical part; location headings identify the context modules and proposals.
+ A diagram in a book's source is an ASCII sketch in its own fence, no wider than 52 characters; the builder replaces the Nth sketch with the Illustrator's fig-N.svg, passed with --figures, and refuses a source whose sketch has no figure.
+
+ A book on a topic that already has a book is that book's next edition, titled with the topic's title and the edition number.

Ruling: land, amend, or reject.

## field-context › compensation/book.md

```markdown
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
```


### Proposal 3: the figure grammar is said once, in vision · field-context › compensation/book.md

  Present the source faithfully and simply. The living responds by comment; use no buttons, fields, or other controls.

- A figure draws concepts as nodes linked by edges, with the forks, options and joins its subject has, each label a few words; its ASCII source is no wider than 52 characters.
  The book subflow obtains each figure from the Illustrator role composed by Curriculum; the page carries the resulting inline SVG, readable on a phone, never the ASCII or Mermaid.

  A presentation renders as a web page, never raw Markdown or prose in a code block. A proposed change shows its additions in green and its removals struck through in red, in one consistent style across books.

Ruling: land, amend, or reject.

## field-context › compensation/flashbook.md

```markdown
A flashbook is a short illustrated book the living reads, one subject per book, made from Markdown a higher psyche flow wrote in its transcript under an exact title. Find the exact Presentation block by title between its to-the-living
markers using tools/book-fetch.mjs --block, or use the source file named in the
brief. Check that source with tools/book-check.mjs and publish through the book
subflow; never cut it at a heading or edit its proposals.

Use a vertically scrolling document with stacked sections. Text is minimal; each section covers one thing. Give every section and chart its own visible heading for comment anchoring.

A message is read on a phone: few points, much drawing, short text under each heading.

Never use horizontal swipe or paging. Use no checkbox, button, copy control, form, or other interactive book control. The book receives answers only by comment; number choices for the living to name in a comment.

A flashbook keeps every point in its source and gives each point
full-size drawn imagery. Restyled text and one image are not a flashbook.

Do not quote the living back to him. Where the source has proposals,
show the named file, lines removed, lines added, and the ruling sought.
Render them as web, never raw Markdown or prose in a code block: added
lines in green, removed lines struck through in red, one consistent style.

Use the shared book-code.html page style unchanged, in both themes.
Keep prose in one reading column; a real-code block keeps its original
lines and fits the 52-character source limit.

Code in a book never wraps midline. Arrange ethos and datom blocks vertically, with every nested bracket on its own indented line, fitting the phone width.

The book shell is laid out with CSS Grid, never flexbox, and adapts with container queries.

Take no screenshots of a book. Commit no images or other binary files to the repository.

Make one fresh artifact for every presentation and every comment, each published from its own new file path, never a path an earlier artifact was published from. Preserve every older artifact, whether it has comments or not. After publication is complete, report titles and URLs with a very short
voice answer to the question; send no intermediate publishing progress. Load compensation-flashbook-illustration for every illustration. Publish the book's Markdown source as it is published; never the HTML or an image.
```


### Proposal 4: a flashbook draws where the idea has a shape, and publishes the built page · field-context › compensation/flashbook.md

  Use a vertically scrolling document with stacked sections. Text is minimal; each section covers one thing. Give every section and chart its own visible heading for comment anchoring.

- A message is read on a phone: few points, much drawing, short text under each heading.
+ A message is read on a phone: few points, short text under each heading, a figure where the idea has a shape.

  Never use horizontal swipe or paging. Use no checkbox, button, copy control, form, or other interactive book control. The book receives answers only by comment; number choices for the living to name in a comment.

- A flashbook keeps every point in its source and gives each point
- full-size drawn imagery. Restyled text and one image are not a flashbook.
+ A flashbook keeps every point in its source.

- Make one fresh artifact for every presentation and every comment, each published from its own new file path, never a path an earlier artifact was published from. Preserve every older artifact, whether it has comments or not. After publication is complete, report titles and URLs with a very short
- voice answer to the question; send no intermediate publishing progress. Load compensation-flashbook-illustration for every illustration. Publish the book's Markdown source as it is published; never the HTML or an image.
+ Make one fresh artifact for every presentation and every comment, each published from its own new file path, never a path an earlier artifact was published from. Preserve every older artifact, whether it has comments or not. After publication is complete, report titles and URLs with a very short voice answer to the question; send no intermediate publishing progress. Publish the page the book builder built from the source, with the Illustrator's figures; never an image of it.

Ruling: land, amend, or reject.

## field-context › compensation/flashbook-illustration.md

```markdown
An illustration is a literal picture, made to be rendered as a picture: inline SVG or an image. It is elaborate and artistically attractive, not straight lines and boxes: curved paths, gradients, layered shapes, organic forms. It carries the page's meaning through imagery drawn from the flashbook's own prose and nothing from outside its subject.

Simple yet complex: one thing, not trying to cover too much, drawn so it rewards looking. Words inside it are a title or a few labels at most, never below 16px on a 360px-wide screen, legible in both themes.

A flowchart is hand-written inline SVG, with no library. It uses a portrait viewBox about 360 units wide and runs top to bottom. Labels are at least 14px and measured to fit their shapes at 360 units wide. Use one colour per role consistently across all charts, numbered step badges, a solid bright chosen route, a dashed grey alternative, and short labels from the source.

An illustration may be a flowchart, and then the two are one: the flowchart itself is illustrated, its connections given a style and a feeling, a fat bright red hand-coloured arrow or whatever the page's meaning asks, with the things around it drawn in. A feeling description is as good as a visual one. Two bare charts never follow each other. Image, then text, then image again.
```


### Proposal 5: Destroy the organic-form illustration rule · field-context › compensation/flashbook-illustration.md, a deleted file

- ---
- description: An illustration for a flashbook page must be made.
- dependencies: []
- ---
-
- An illustration is a literal picture, made to be rendered as a picture: inline SVG or an image. It is elaborate and artistically attractive, not straight lines and boxes: curved paths, gradients, layered shapes, organic forms. It carries the page's meaning through imagery drawn from the flashbook's own prose and nothing from outside its subject.
-
- Simple yet complex: one thing, not trying to cover too much, drawn so it rewards looking. Words inside it are a title or a few labels at most, never below 16px on a 360px-wide screen, legible in both themes.
-
- A flowchart is hand-written inline SVG, with no library. It uses a portrait viewBox about 360 units wide and runs top to bottom. Labels are at least 14px and measured to fit their shapes at 360 units wide. Use one colour per role consistently across all charts, numbered step badges, a solid bright chosen route, a dashed grey alternative, and short labels from the source.
-
- An illustration may be a flowchart, and then the two are one: the flowchart itself is illustrated, its connections given a style and a feeling, a fat bright red hand-coloured arrow or whatever the page's meaning asks, with the things around it drawn in. A feeling description is as good as a visual one. Two bare charts never follow each other. Image, then text, then image again.

Ruling: land, amend, or reject.

## field-context › compensation/questions-book.md

```markdown
Gather one presentation of questions, proposed answers, and counterquestions.
```


### Proposal 6: Destroy the questions book · field-context › compensation/questions-book.md, a deleted file

- Gather one presentation of questions, proposed answers, and counterquestions.

Ruling: land, amend, or reject.

## field-context › role/illustrator-faithfulness.md

```markdown
Receive one idea or diagram and its book title. Return exactly one SVG and nothing else, drawing the same idea by compensation-illustration, free of the source boxes and arrows. Preserve the semantic relationships and invent no facts. The book title is context, not permission to add a diagram title. If the idea is ambiguous, report that refusal instead of inventing content.
```


### Proposal 7: the Illustrator keeps every box and arrow · field-context › role/illustrator-faithfulness.md

- Receive one idea or diagram and its book title. Return exactly one SVG and nothing else, drawing the same idea by compensation-illustration, free of the source boxes and arrows. Preserve the semantic relationships and invent no facts. The book title is context, not permission to add a diagram title. If the idea is ambiguous, report that refusal instead of inventing content.
+ Receive one ASCII sketch and its book title. Return exactly one SVG and nothing else, drawing the sketch by compensation-illustration, keeping every box, label and arrow and adding nothing the sketch does not say. The book title is context, not permission to add a diagram title. If the sketch is ambiguous, report that refusal instead of inventing content.

Ruling: land, amend, or reject.

## mind-context › knowledge/vocabulary.md

```markdown
Flow: one run of a voice, from launch to end: its main thread and every subflow it starts; also the Nexus that manages flows.

Flow identity: the canonical short `FLOW_ID` shared by that whole flow.

Flow directory: the main-flow-owned `FLOW_DIRECTORY` shared by that whole flow.

Thread: one running model session and its context. A `THREAD_ID` identifies one thread in a harness.

Transcript: the file the harness writes holding one thread from beginning to end.

Living messenger: the user interface through which a flow reaches the living, asynchronous to the chat; a presentation is one message in it.

Illustrated book: a book to which a model has added illustrations, deciding where each goes. Flashbook, picture book and photo book name the same thing.

Witness: an observation of the thing itself — a test run, a probe,
the code read. What someone says about the thing is a claim.

Quackery: output that stands in for understanding the flow does not
have — a claim it cannot ground, prose that sounds deep over a gap, a
test that only confirms itself.

The living: the living psyche.

Past: the flows a flow has remembered, and theirs in turn.

Base context: the harness-built portion of the top stratum — the instructions the harness itself composes ahead of everything authored here. Vendor parlance: system prompt.

Vision impurity: a working instruction (what to do now, in what order,
at what scope, on which project, through which dispatch) logged as a
vision record.

A defined term overrides competing terminology in the flow's own words.

Machine: short for thinking machine.

Use machine, not AI; use flow, not agent, except when reproducing an external name or quotation.
```


### Proposal 8: the vocabulary names a book as it is · mind-context › knowledge/vocabulary.md

- Illustrated book: a book to which a model has added illustrations, deciding where each goes. Flashbook, picture book and photo book name the same thing.
+ Book: the answer to a question of the living on one topic, shown as context modules and proposals; its figures are the Illustrator's drawings of the sketches in its source. Flashbook, illustrated book, picture book and photo book name the same thing.

Ruling: land, amend, or reject.

### Proposal 9: a proposal into a module the book does not show is refused · primary › tools/book-check.mjs

  const contextRepository = /^(?:psyche|mind|field)-context$/;
+ const viewed = new Set();
+ const landing = [];

  if (/^Proposal\b/i.test(heading[2])) {
    finish();
    if (located.test(heading[2])) {
      proposals++;
+     const target = heading[2].match(/([^\s›·]+ › [^\s,]+)/)[1];
+     if (!/, a (?:new|deleted) file$/.test(heading[2]) &&
+         contextRepository.test(target.split(" › ")[0]))
+       landing.push({ line: number, target });

  const location = heading[2].match(moduleLocation);
+ if (location)
+   viewed.add(`${location[1]} › ${location[2]}`);

  if (!proposals) errors.push({ line: 1, reason: "missing-proposal" });
+ for (const p of landing)
+   if (!viewed.has(p.target))
+     errors.push({ line: p.line,
+                   reason: "proposal-without-module-view" });

Ruling: land, amend, or reject.
