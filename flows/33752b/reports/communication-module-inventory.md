# Communication module inventory

Flow 33752b. Gathered for a crystallization book on a new psyche module about how machines communicate with the living. Witnessed (W) means read from the file in this run. Nothing was edited. The classification (harness-independent versus harness-bound) is this flow's inference, not the living's.

## 1. Location facts (W)

- `vision-book.md` is at `/git/github.com/LiGoldragon/psyche-context/skills/vision-book.md` (14 lines).
- No `compensation-book*` file exists under psyche-context/skills. They are Field modules, in `/git/github.com/LiGoldragon/field-context/skills/` (the Field context variable). Six files: compensation-book, compensation-book-crystallization, compensation-flashbook, compensation-flashbook-illustration, compensation-presentation-book, compensation-questions-book. The name `compensation-book-distillation` (cited in older flow reports) is no longer in field-context; compensation-book-crystallization carries its place. field-skills (detached HEAD 5070467, uncommitted edits) lists the same six.
- Mind has the harness-bound counterparts `operation-book.md`, `operation-flashbook.md`, `operation-flashbook-illustration.md` in `/git/github.com/LiGoldragon/mind-context/skills/`; not classified below beyond the figure line.
- The grep for visual/figure/illustrat over psyche-context/skills matched only vision-book.md as a real hit (vision-model-roles, vision-nexus, vision-signal, intent-startup-prompt matched the substring "figure" inside "configure/configured"; not about visualization).

## 2. vision-book.md, full current text (W)

```
---
description: A book for the living is written or judged.
dependencies: [vision-crystallization]
---

## Books

A book is a proposal into context modules, and the whole of it is its crystallization: a line removed shows in red, a line added in green, and a figure in it is a figure proposed for a module.

The first edition of a book is mostly questions.

The book is the center of development: it is the evolution of an idea, and the list of unknowns lives in it.

A figure shows how a thing moves, one question per figure, readable in seconds. Its grammar: a box is a thing or a collection; an arrow is a one-way relation carrying a verb, so that box, verb, box reads as a sentence; nearness and enclosure are kinship; top to bottom is order; colour carries a role or is absent. A list in boxes, a tally, or a sentence in a rectangle is not a figure. A diagram in a book's source is ASCII in that grammar, laid out vertically and no wider than 52 characters so a phone shows it; a sketch without arrows is rewritten before it is sent. The published book never shows the ASCII, but a figure drawn from it by a Tertiary or Quaternary subflow that is given the grammar with the sketch, keeps every box, label and arrow, and adds nothing the source does not say; a figure that lost an arrow is returned. A sizable book carries several figures.
```

All four paragraphs (lines 8, 10, 12, 14) are harness-independent. Line 14 names "a Tertiary or Quaternary subflow", the one flow-bound phrase.

## 3. compensation-book* modules in field-context (W)

Path prefix `/git/github.com/LiGoldragon/field-context/skills/`. Wholly independent lines are quoted. Split lines hold an independent clause and a bound clause. Bound lines are listed with a reason only.

### compensation-book.md (24 lines)

Harness-independent (wholly):
> compensation-book:6: Make one new presentation for each message. A presentation is a new living-messenger user-interface item, never an update of a presentation that has comments.
> compensation-book:8: Present the source faithfully and simply. The living responds by comment; use no buttons, fields, or other controls.
> compensation-book:10: A drawing starts as a vertical, narrow ASCII specification in the source.

Split (independent part first):
> compensation-book:13: inline SVG, readable on a phone, never the ASCII or Mermaid.
> compensation-book:15: A presentation renders as a web page, never raw Markdown or prose in a code block. A proposed change shows its additions in green and its removals struck through in red, in one consistent style across books.
> compensation-book:17: After publication is complete, return its title and URL to the requester
> compensation-book:18: with a very short voice answer to the question.

Bound: 11-12 (book subflow, Quaternary, figure procedure), 13 "inline SVG ... never ASCII or Mermaid" (page format), 15 "renders as a web page", 17 "title and URL", 20-24 (subagents/book.md, tools/book-check.mjs, non-Claude caller, Secondary, hand-render a page). Line 24 "If the source lacks crystallization, return the defect to its author" is independent in content.

### compensation-book-crystallization.md (18 lines)

Wholly independent:
> compensation-book-crystallization:6: A book is its crystallizations. Every line it shows is a word removed (red) or added (green) in a psyche module, or the code that line lands. A figure in it is a figure proposed for a psyche module. Nothing else is written.
> compensation-book-crystallization:8: A change is written as a line File: <path>, then each removed line starting with "- ", each added line with "+ ", and unchanged lines around them starting with two spaces. Concise machine results and concrete blockers may be sent outside a book.
> compensation-book-crystallization:12: A proposed statement is drawn from the living's records read whole, with their exceptions and later statements on the same subject. A skill line in the author's brief shows where a statement lands, never what it says; the brief marks machine-skill text as the machine's. A count or date claim about the records is made only when the author has witnessed it.
> compensation-book-crystallization:14: A book does not restate the living's words. A proposal may cite the record it crystallizes by path and date.
> compensation-book-crystallization:16: A proposal to destroy or archive a record renders unmistakably apart from a landing: its own colour and a Destroy or Archive mark on the record it removes.
> compensation-book-crystallization:18: Before publishing, reconcile the relevant current direction and exclude what the living has voided. A new edition carries only what is unruled or changed since the living last read it; what he approved is landed, not shown again.

Split:
> compensation-book-crystallization:10: Every line inside a book's code block of real code is at most 52 characters; prose proposed for a file renders as text and wraps freely. A code block spans the full page width, outside nested or indented layout columns; the code inside keeps its own indentation, never wraps inside a token, and scrolls sideways. A short code value inside a choice stays inline. Check every book at phone width before publishing.

Bound: none beyond line 10's second and third sentences (page width, scrolls sideways, phone width check).

### compensation-flashbook.md (36 lines)

Wholly independent:
> compensation-flashbook:13: A message is read on a phone: few points, much drawing, short text under each heading.
> compensation-flashbook:15: Never use horizontal swipe or paging. Use no checkbox, button, copy control, form, or other interactive book control. The book receives answers only by comment; number choices for the living to name in a comment.
> compensation-flashbook:17: A flashbook keeps every point in its source and gives each point
> compensation-flashbook:18: full-size drawn imagery. Restyled text and one image are not a flashbook.
> compensation-flashbook:20: Do not quote the living back to him. Where the source has proposals,
> compensation-flashbook:21: show the named file, lines removed, lines added, and the ruling sought.

Split:
> compensation-flashbook:11: Use a vertically scrolling document with stacked sections. Text is minimal; each section covers one thing. Give every section and chart its own visible heading for comment anchoring.
> compensation-flashbook:22: Render them as web, never raw Markdown or prose in a code block: added
> compensation-flashbook:23: lines in green, removed lines struck through in red, one consistent style.
> compensation-flashbook:35: Make one fresh artifact for every presentation and every comment, each published from its own new file path, never a path an earlier artifact was published from. Preserve every older artifact, whether it has comments or not. After publication is complete, report titles and URLs with a very short
> compensation-flashbook:36: voice answer to the question; send no intermediate publishing progress. Load compensation-flashbook-illustration for every illustration. Publish the book's Markdown source as it is published; never the HTML or an image.

Bound: 6-9 (transcript source, tools/book-fetch.mjs, tools/book-check.mjs, book subflow), 25-27 (book-code.html, columns), 29 (ethos/datom block layout), 31 (CSS Grid, container queries), 33 (screenshots, binary in repository), 35-36 (artifact paths, publishing, Markdown source).

### compensation-flashbook-illustration.md (12 lines)

Independent in content:
> compensation-flashbook-illustration:8: Simple yet complex: one thing, not trying to cover too much, drawn so it rewards looking. Words inside it are a title or a few labels at most, never below 16px on a 360px-wide screen, legible in both themes.
> compensation-flashbook-illustration:12: An illustration may be a flowchart, and then the two are one: the flowchart itself is illustrated, its connections given a style and a feeling, a fat bright red hand-coloured arrow or whatever the page's meaning asks, with the things around it drawn in. A feeling description is as good as a visual one. Two bare charts never follow each other. Image, then text, then image again.

Split / bound (SVG and viewBox are a format):
> compensation-flashbook-illustration:6: An illustration is a literal picture, made to be rendered as a picture: inline SVG or an image. It is elaborate and artistically attractive, not straight lines and boxes: curved paths, gradients, layered shapes, organic forms. It carries the page's meaning through imagery drawn from the flashbook's own prose and nothing from outside its subject.
> compensation-flashbook-illustration:10: A flowchart is hand-written inline SVG, with no library. It uses a portrait viewBox about 360 units wide and runs top to bottom. Labels are at least 14px and measured to fit their shapes at 360 units wide. Use one colour per role consistently across all charts, numbered step badges, a solid bright chosen route, a dashed grey alternative, and short labels from the source.

### compensation-presentation-book.md (10 lines)

Wholly independent:
> compensation-presentation-book:8: A book answers the living's comments with the resulting proposal or change.
> compensation-presentation-book:10: Present one proposal at a time when review is proceeding proposal by proposal, then pause for the living's ruling.

Bound:
> compensation-presentation-book:6: In the same turn, directly after writing the presentation block, dispatch the compensation-flashbook subflow on that block's title from your own transcript; a block left for a later turn is a presentation the living has not received.

### compensation-questions-book.md (6 lines)

Wholly independent:
> compensation-questions-book:6: Gather one presentation of questions, proposed answers, and counterquestions.

### Tally (this flow's count)

- Wholly harness-independent lines in the six Field modules: 20 (book 3, crystallization 6, flashbook 6, illustration 2 [lines 8 and 12], presentation-book 2, questions-book 1).
- Split lines (one independent clause, one bound): about 12 (book 13, 15, 17, 18; crystallization 10; flashbook 11, 22, 23, 35, 36; illustration 6, 10).
- Plus 4 wholly independent paragraphs in vision-book.md (psyche-context).
- Modules they sit in: compensation-book, compensation-book-crystallization, compensation-flashbook, compensation-flashbook-illustration, compensation-presentation-book, compensation-questions-book, and vision-book.

## 4. Other visualization lines (W)

Field-context grep for visual/figure/illustrat outside the six modules: only compensation-agent-harness-packaging (match "configured", irrelevant). Mind-context:
> /git/github.com/LiGoldragon/mind-context/skills/knowledge-vocabulary.md:18:Illustrated book: a book to which a model has added illustrations, deciding where each goes. Flashbook, picture book and photo book name the same thing.
> /git/github.com/LiGoldragon/mind-context/skills/operation-flashbook-illustration.md:2:description: An illustration for a flashbook page must be made.
> /git/github.com/LiGoldragon/mind-context/skills/operation-flashbook-illustration.md:6:An illustration is a literal picture, made to be rendered as a picture: inline SVG or an image. It is elaborate and artistically attractive, not straight lines and boxes: curved paths, gradients, layered shapes, organic forms. It carries the page's meaning through imagery drawn from the flashbook's own prose and nothing from outside its subject.
> /git/github.com/LiGoldragon/mind-context/skills/operation-flashbook-illustration.md:12:An illustration may be a flowchart, and then the two are one: the flowchart itself is illustrated, its connections given a style and a feeling, a fat bright red hand-coloured arrow or whatever the page's meaning asks, with the things around it drawn in. A feeling description is as good as a visual one. Two bare charts never follow each other. Image, then text, then image again.
> /git/github.com/LiGoldragon/mind-context/skills/operation-book.md:3:dependencies: [operation-flashbook-illustration, vision-book, compensation-book-distillation]
> /git/github.com/LiGoldragon/mind-context/skills/operation-book.md:11:The book subflow delegates its figure to Haiku 5.5 with the surrounding
> /git/github.com/LiGoldragon/mind-context/skills/operation-book.md:12:text, following its figure procedure; the page carries the resulting
> /git/github.com/LiGoldragon/mind-context/skills/operation-flashbook.md:3:dependencies: [operation-flashbook-illustration, compensation-behavior, knowledge-vocabulary]
> /git/github.com/LiGoldragon/mind-context/skills/operation-flashbook.md:6:A flashbook is a short illustrated book the living reads, one subject per book, made from Markdown a higher psyche seat wrote in its transcript under an exact title. Find the exact Presentation block by title between its to-the-living
> /git/github.com/LiGoldragon/mind-context/skills/operation-flashbook.md:36:voice answer to the question; send no intermediate publishing progress. Load operation-flashbook-illustration for every illustration. Commit and push the book's Markdown source as it is published; never the HTML or an image.

## 5. Proposed visualization module and figure rules (W: read from the files)

### 5a. books/32-figures-that-move.md, the Crystallization section (the proposals) verbatim

(The file has no heading named Crystallization; the section is "## Distillation" with Proposals 1 and 2, lines 33-49, and the ruling question at 51-53.)

````
## Distillation

### Proposal 1: vision-book, the figure, and the figure paragraph leaves the Field module

Target: psyche-skills, vision-book, section «Books», after its paragraph; and field-skills, compensation-book-distillation, whose figure paragraph is removed. The Field paragraph as it stands:

"A diagram in a book's source is ASCII, laid out vertically and no wider than 52 characters so a phone shows it; the published book never shows the ASCII, but a figure drawn from it by a Sonnet or Haiku subflow that keeps every box, label and arrow of the source and adds nothing the source does not say; its colour and layout may carry the surrounding meaning."

Crystallized:

"A figure shows how a thing moves, one question per figure, readable in seconds. Its grammar: a box is a thing or a collection; an arrow is a one-way relation carrying a verb, so that box, verb, box reads as a sentence; nearness and enclosure are kinship; top to bottom is order; colour carries a role or is absent. A list in boxes, a tally, or a sentence in a rectangle is not a figure. A diagram in a book's source is ASCII in that grammar, laid out vertically and no wider than 52 characters so a phone shows it; a sketch without arrows is rewritten before it is sent. The published book never shows the ASCII, but a figure drawn from it by a Sonnet or Haiku subflow that is given the grammar with the sketch, keeps every box, label and arrow, and adds nothing the source does not say; a figure that lost an arrow is returned. A sizable book carries several figures."

### Proposal 2: the drawer's brief

Target: Primary, the book agent's figure procedure (the brief given to the Haiku drawer). As it stands, the drawer is asked for a vertical figure, narrow enough for a phone, with large readable labels, keeping every element and adding nothing.

Crystallized: the same brief carries the grammar of Proposal 1 in its own words, and the drawer returns the sketch instead of a figure when the sketch has no relation to draw.

## Question

Proposal 1 now lands in vision-book, by your ruling that a line shown to you is a candidate for vision and leaves the module it sat in; the drawer's brief of Proposal 2 stays machine-owned. The one sentence already before you in «Three lines from the chat», that a clear, concise flowchart is a book's most important part, is the first line of the same section. Do both land together?
<!-- to-the-living:end -->
````

### 5b. reports/visualization-research.md, section C "Candidate lines for the figure modules" (lines 103-128) verbatim

The report proposes no named new module; it gives drafts for the main flow to place (its own words: "The target module and any psyche review are its decision"). Candidates C1-C15:

````
## C. Candidate lines for the figure modules

Each candidate names the source it rests on. These are drafts for the main flow. The target module and any psyche review are its decision.

What a figure is for:
- C1. A figure answers one question, written as its title. It shows one concept: its parts, how they relate, and what moves where. [B11 focus question; compensation-book-distillation line 8]
- C2. It can be grasped in seconds without reading the page. Each label is a few words, set on the part it names. [line 8; B5 spatial contiguity]
- C3. It shows either one concrete case or the general shape, and says which. [B9]

Visual grammar:
- C4. A box is a thing or a collection of things. Its label is a noun. [B1, B4]
- C5. An arrow is a relation. It points one way and carries a verb that reads as a sentence: thing, verb, thing. A connection that cannot be given a verb is left out until it can. [B1, B2, B11, B12]
- C6. Within a figure, one arrow style has one meaning. A second meaning gets a second style, named in the figure. [B2, B12]
- C7. Nearness and enclosure mean kinship. Things placed together belong together, and a frame is drawn only where it groups. [B3, B4, NN/g]
- C8. Position carries meaning. The figure reads top to bottom as order, sequence or cause. Centre is focus. Size is weight. [B3; illustration module "runs top to bottom"]
- C9. Colour carries a role, the same role in every figure of the book, or it is absent. [B12; Material R; illustration module "one colour per role"]
- C10. A comparison is drawn as stacked panels in the same layout, so the difference is the only thing that changes. [B7]
- C11. Every mark earns its place. Ink that tells nothing new is removed. [B5 coherence; B6]

What a figure never is:
- C12. Never a list in boxes, a ledger of counts, or a sentence inside a rectangle. A list stays prose or a table. A movement or cause is drawn as an arrow. [B8; witnessed in books 25 and 29]

Sketch to drawing:
- C13. The ASCII sketch is the figure's grammar. It names its question, draws each relation as an arrow (`-->`, `v`) with its verb on or beside it, and groups kin by frame or nearness. A sketch with no arrow is a list and is rewritten before it is sent. [B2, B11; cause 1]
- C14. The drawer receives the grammar (C4-C9) with the sketch. It keeps every box, arrow, verb and grouping, and adds nothing the source does not say. It may give the arrows weight, curve and colour, and the things a drawn form, as the meaning asks. [line 10; illustration module; B13]
- C15. Before embedding, the book subflow checks the SVG. Each sketch arrow should be a drawn arrow with a head and its verb, and no label should be under 14 px at 360 wide. A figure with relations in its sketch and no arrowhead in its SVG is returned. [B13; witnessed SVG counts]
````

Origin note: the research report's sources B1-B13 are marked W, Q or R in that report; R items were relayed by search summaries and not read on the page. Its cause 5 is that subflow's inference, untested.

## 6. The living's records on communication with him (headings and dates only)

Command run: `grep -ril 'messenger\|multimodal\|voice\|communicat' flows/*/vision/ | head -20` returned 20 files, mostly about flow-to-flow messaging (Herdr, intercom, routing), not communication with the living. Those 20 paths are listed in 6b. The records about communicating with the living are in 6a, found by a second grep (`multimodal`, `living messenger`).

### 6a. Records about communicating with the living

Dates are the date strings found in each file; headings carry no date unless shown.

- `flows/33752b/vision/communication.md` (2026-10-14)
  - "# Communication with the living"
  - "## A module on communicating with the living, which the book module follows"
  - "## Books maximize communication: visual, minimal text, the least instruction for the biggest effect; the book is the proposal"
- `flows/d68c82/vision/books.md` (2026-10-11 to 2026-10-14; "multimodal" appears at line 101)
  - "## 2026-10-14 — a book never makes him read the same thing twice; visual, minimal, the proposal only"
  - "## 2026-10-14 — communicating with the living is its own skill; the book follows it"
  - also in the file: "## The context is a visual, then the proposal", "## The living is spoken to through the books", "## A visual shows the thing; text never assumes what he knows", "## Flowcharts are among the most important parts of a book", "## A flow speaks to the living only through a printed book", "## Everything in a book is red or green; a chart is a proposed addition", "## A first edition is mostly questions", "## A question must be intelligible", "## What is to be ruled sits in the proposal", "## A new edition shows only what is still open", "## The eye looks for the green section; a book about code shows code", "## A book shows what is being landed: the proposed code, in green", "## The whole book is a crystallization", "## Only the changed words are marked"
- `flows/33752b/vision/books.md`: "## The book is the center of development", "## A first edition mostly questions: approved", "## What he reviews is psyche; a book puts to him only psyche lines", "## A book is red and green; a chart is a chart proposed for a psyche module", "## A book is always a proposal into context modules; he may also review Mind content; an overview book on books, reviews and the hierarchy", "## A book line says what the book has; the value of his time is spirit core"
- `flows/01e496/vision/books.md` (2026-10-02): "## There is no page that is the living's", "## The book is the user interface, the living messenger", "## A commented book is not reused"
- `flows/91ea9f/vision/books.md` (2026-10-01, 2026-10-02): "## The comment markers need not render", "## The metadata is one datom line", "## Render flowcharts properly; trials with the bookmaker, rated by him", "## There is no page that is his", "## The book is the user interface, the living messenger", "## A commented book is a throwaway", "## Take out \"page\"; \"book\" is not right either; it is a user interface", "## A user interface Claude has, more asynchronous than the chat", "## Not reusable once commented on, nothing wider", "## The visual flowcharts he wants; the skill carries the guidance", "## No swipe between pages; he scrolls up and down", "## Checkboxes in the book: prohibited if the machine cannot see them", "## The swipe UI breaks comment anchoring; forbid it", "## A seat's status line must explain; a book or an answer here", "## He reads only the presentations; talk back in the book"
- `flows/41fa34/vision/living-messenger.md` (2026-10-02): "# The user interface; the living messenger"
- `flows/41fa34/vision/what-the-book-is.md` (living messenger mentioned): "# What the book is"
- `flows/5ed94b/vision/livingMessenger.md` (2026-10-03): "## Cloud artifacting is the best we have, and it sucks"
- `flows/8475a9/vision/livingMessenger.md` (2026-10-06): "## A universal commenting surface, not Claude artifacts: any model, syntax highlighting, our own styling"; "## The book replacement stack is not Fable's concern"
- `flows/d4ae97/vision/livingMessenger.md` (2026-10-06): "## Something universal, beyond Claude artifacts, to comment on with any model, with syntax highlighting and our own styling"
- `flows/024bc7/vision/speechToText.md` (2026-09-13): "## Host our own speech-to-text, personalized, post-trained on my voice"

### 6b. The 20 files the requested grep returned (headings of the first sections, mostly flow-to-flow)

flows/019fe121/vision/agentIntercom.md; flows/019fe728/vision/agentIntercom.md; flows/01a030aa/vision/herdr.md; flows/01a03d6e/vision/archive-ethosInterfaces.md; flows/024bc7/vision/speechToText.md; router.md; parallelSessions.md; flows/01e496/vision/books.md; flows/05c604/vision/messages.md; quota.md; flows/0625c3/vision/lateralThenUpRouting.md; flows/0c85a3/vision/aspect-topics.md; flows/0d557b/vision/partnerChannel.md; flows/1030529c/vision/flowNaming.md; flows/108ab0/vision/operational-flowDatomLauncherLanguage.md, operational-designMosaic.md, operational-hackyMessenger.md; flows/1ac573/vision/operational-agentToPsycheMessaging.md; flows/1b8ac0/vision/refresh.md, transcriptTool.md.

Not witnessed: record bodies were not read in this run; only headings and date strings.

## 7. Provenance

No provenance receipt handoff exists for this report; provenance receipt evidence is unavailable. The flow-evidence skill could not be loaded in this subflow (no Skill tool available), so the report follows the brief's path as given.
