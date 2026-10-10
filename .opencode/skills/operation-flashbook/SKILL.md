---
name: operation-flashbook
description: A flashbook must be made from a source written in a flow's transcript, or an existing flashbook is judged.
dependencies: [operation-flashbook-illustration, compensation-behavior, knowledge-vocabulary]
---

A flashbook is a short illustrated book the living reads, one subject per book, made from Markdown a higher psyche seat wrote in its transcript under an exact title. Find the exact Presentation block by title between its to-the-living
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
voice answer to the question; send no intermediate publishing progress. Load operation-flashbook-illustration for every illustration. Commit and push the book's Markdown source as it is published; never the HTML or an image.
