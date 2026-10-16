---
description: A presentation must be made available to the living messenger.
dependencies: [compensation-flashbook-illustration, vision-book, compensation-book-crystallization]
---

Make one new presentation for each message. A presentation is a new living-messenger user-interface item, never an update of a presentation that has comments.

Present the source faithfully and simply. The living responds by comment; use no buttons, fields, or other controls.

A figure draws concepts as nodes linked by edges, with the forks, options and joins its subject has, each label a few words; its ASCII source is no wider than 52 characters.
The book subflow delegates its figure to Quaternary with the surrounding
text, following its figure procedure; the page carries the resulting
inline SVG, readable on a phone, never the ASCII or Mermaid.

A presentation renders as a web page, never raw Markdown or prose in a code block. A proposed change shows its additions in green and its removals struck through in red, in one consistent style across books.

A book's reference file is references/<book-source-basename>.md in the directory holding the book's source, written with the source; it lists, per proposal, the records each line draws from. When a proposal lands, its entries move to references/archive/ with the landing commit named.

A page is republished from its local source; a page read back from the host is never copied over that source.

After publication is complete, return its title and URL to the requester
with a very short voice answer to the question.

Use the book subflow defined by subagents/book.md to publish the exact
source. Check it with tools/book-check.mjs before rendering. A non-Claude
caller sends its source to its Secondary; it
does not hand-render a replacement page. If the source lacks crystallization,
return the defect to its author rather than adding a proposal.
