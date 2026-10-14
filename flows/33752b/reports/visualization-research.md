# Visualization research: figures in books

Flow 33752b. Made by a delegated subflow. Witnessed (W) means read or run by this subflow. Q means a quote read on the source page. R means relayed by a search summary and not read on the page. Where this report infers, it says "inference".

## A. Current figure rules (W)

The local checkouts of field-skills and mind-skills are detached and behind origin/main. mind-skills also has uncommitted edits to operation-book.md and operation-flashbook.md. The lines below are read at origin/main: field-skills 14269e9, mind-skills c054cec.

field-skills `skills/compensation-book-distillation.md`, line 8:
> A figure shows the thing itself, its parts, how they connect and what moves where, so it can be understood without reading; text in it is a label he can follow with no knowledge of the session.

Line 10:
> A diagram in a book's source is ASCII, laid out vertically and no wider than 52 characters so a phone shows it; the published book never shows the ASCII, but a figure drawn from it by a Tertiary or Quaternary subflow that keeps every box, label and arrow of the source and adds nothing the source does not say; its colour and layout may carry the surrounding meaning.

mind-skills `skills/operation-book.md`:
> A drawing starts as a vertical, narrow ASCII specification in the source. The book subflow delegates its figure to Quaternary with the surrounding text, following its figure procedure; the page carries the resulting inline SVG, readable on a phone, never the ASCII or Mermaid.

Commit b605cd0 (2026-10-09) replaced this earlier line in operation-book.md:
> A drawing in a book is hand-written inline SVG, readable on a phone in portrait without zooming and drawn with more than black-and-white boxes and arrows.

mind-skills `skills/operation-flashbook.md`:
> A message is read on a phone: few points, much drawing, short text under each heading.

mind-skills `skills/operation-flashbook-illustration.md`. Of the files read, this is the only one that gives a flowchart grammar:
> A flowchart is hand-written inline SVG, with no library. It uses a portrait viewBox about 360 units wide and runs top to bottom. [...] Use one colour per role consistently across all charts, numbered step badges, a solid bright chosen route, a dashed grey alternative, and short labels from the source.

`/home/li/primary/.claude/agents/book.md`, lines 114-128. This is the whole procedure the figure subflow is given:
> For each diagram, use the Agent tool to start a `general-purpose` figure subflow with `model` `haiku`. Give it the diagram and the surrounding section's text, and ask it for an inline SVG figure: vertical, narrow enough for a phone, with large readable labels. The figure carries the diagram's relationships and the meaning in the surrounding text. It may add visual grouping, color and emphasis that the text supports, but no new claim, ruling or relationship.

### The symptom, witnessed in the SVG markup and its ASCII source

- Book 29 (context-modules-2). The ASCII is an undirected tree: `context modules` has `|` and `+---+` lines down to three columns of words, with the counts 3, 2 and 1. The SVG has 4 rect, 1 path, 13 text, and no marker, polygon or arrowhead. The tree became a root box and three stacked boxes, each a heading over a word list, joined by one bracket path. No edge has a label and nothing has a direction. The boxes all share one fill, so colour carries nothing.
- Book 25 (cleaning-skills-2). The ASCII is a text ledger with no diagram in it: dotted leaders, counts and a total. The SVG has 4 rect, 1 line (the sum rule), 17 text, and no arrow. It shows three boxes holding sentences and dotted count lines. "Moves verbatim to its vision module" is a movement, but it is written as a sentence inside a box and not drawn as an arrow. One dashed border marks "not moved".
- Both figures follow their sketches. The drawer added nothing and dropped nothing. The sketches had no arrows or relation labels, and in 25 there was no diagram at all.

### Possible causes (more than one; not ranked)

1. The sketch carries no relations. Nothing requires the ASCII to have arrows or verbs. Line 10's "keeps every box, label and arrow ... adds nothing" then holds the drawer to that poverty.
2. The figure subflow's brief asks only "vertical, narrow, large readable labels". The flowchart grammar in operation-flashbook-illustration.md is not passed to it.
3. Since b605cd0 no line requires "more than black-and-white boxes and arrows".
4. No line says what a figure is not, such as a list in boxes. Book 25 shows the author used a figure as a ledger.
5. A Haiku-class drawer gets no grammar of meaning, and with no guidance models tend toward generic output (B13). This is the flow's inference: it fits the evidence but was not tested.

## B. Sources (13)

B1. Barbara Tversky, "Visualizing Thoughts", Topics in Cognitive Science 3 (2011). https://www.tc.columbia.edu/faculty/bt2158/faculty-profile/files/2011_Tversky_VisualizingThoughts.pdf
Q: "Use dots for entities, lines for relations, arrows for asymmetric relations, boxes for collections."
For a phone book: each mark has a fixed job. A box means a collection, not a frame around text.

B2. Tversky, same paper. Q: "For the diagrams without arrows, students gave structural descriptions [...] For the diagrams with arrows, students gave functional descriptions that provided the step-by-step causal operations of the systems." Q: "many diagrams had different meanings of arrows in the same diagram, with no visual way to disambiguate them."
For a phone book: a figure without arrows can only show structure. One arrow should carry one meaning per figure.

B3. Tversky, same paper. Q: "things that are closer conceptually are placed closer on a page"; "up is readily associated with increases in amount, strength, goodness, and power"; "Although arrows can indicate causes and forces, the specific forces and causes may need language."
For a phone book: position carries meaning. On a tall page, top to bottom is the order. An arrow needs its verb written on it.

B4. Tversky, Mind in Motion (2019), chapter "Boxes, lines, and trees".
R: the book reviews what dots, lines, arrows and boxes reveal about thought. Also R, from a 2013 CogSci study: "lines link and boxes contain".
For a phone book: link and contain are the two basic acts of a figure.

B5. Richard E. Mayer, Multimedia Learning, 3rd ed. (2020), as quoted on a summary sheet: https://ugc.futurelearn.com/uploads/files/7d/d6/7dd6188d-c343-4311-b064-ac98d2c95abc/Multimedia_Principles._R._E._Mayer__2020.pdf Q (on the sheet): "Coherence Principle: People learn better when extraneous material is excluded rather than included." "Signaling Principle: [...] when cues are added that highlight the organization of the essential material." "Spatial Contiguity Principle: [...] when corresponding words and pictures are presented near rather than far".
For a phone book: cut whatever is extra. Arrows and colour should mark the organization, and each label sits on its part.

B6. Edward Tufte, The Visual Display of Quantitative Information (1983).
R: data-ink is the ink that cannot be erased without losing information. Chartjunk is "interior decoration" that "does not tell the viewer anything new". "Erase non-data-ink (within reason)".
For a phone book: a box border that groups nothing is non-data-ink.

B7. Tufte, Envisioning Information (1990), p. 67, as relayed: https://en.wikipedia.org/wiki/Small_multiple
R: "At the heart of quantitative reasoning is a single question: Compared to what?" Small multiples enforce comparison.
For a phone book: before and after, or option a against option b, can be drawn as small panels in the same layout, stacked vertically.

B8. Tufte, The Cognitive Style of PowerPoint (2003).
R: "As analysis becomes more causal, multivariate, comparative, evidence based, and resolution-intense, the more damaging the bullet list becomes." R: bullet outlines leave causal assumptions unstated.
For a phone book: a list in boxes is a bullet list. A relation belongs in an arrow or a sentence, never in a column of fragments.

B9. Bret Victor, "Up and Down the Ladder of Abstraction" (Oct 2011). https://worrydream.com/LadderOfAbstraction/
Q: "the most powerful way to gain insight into a system is by moving between levels of abstraction." Q: "We step up to an abstraction by devising a representation that depicts the system across all values of a parameter."
For a phone book: say whether a figure shows one concrete case or the general shape. The book can pair one concrete figure with one general figure.

B10. Bret Victor, "Explorable Explanations" (Mar 2011). https://worrydream.com/ExplorableExplanations/
Q: "A typical reading tool, such as a book or website, displays the author's argument, and nothing else."
For a phone book: a static book cannot offer play. The figure should therefore show the consequence, and not only the parts.

B11. Joseph Novak and Alberto Cañas, "The Theory Underlying Concept Maps and How to Construct and Use Them" (IHMC, 2006/2008). https://users.cs.northwestern.edu/~paritosh/papers/sketch-to-models/Novak-Canas-TheoryUnderlyingConceptMapsHQ.pdf
Q: "Words on the line, referred to as linking words or linking phrases, specify the relationship between the two concepts." Q: "Every concept map responds to a focus question". Q: "Students often comment that it is hard to add linking words [...] because they poorly understand the relationship".
For a phone book: each node, labelled arrow, node triple should read as a sentence. A link that cannot be labelled is a relation the author has not understood yet.

B12. Simon Brown, C4 model notation page (undated). https://c4model.com/diagrams/notation
Q: "Every line should represent a unidirectional relationship." "Every line should be labelled, the label being consistent with the direction and intent of the relationship". "ideally avoiding single words like, “Uses”." "any colour coding is consistent (within and across diagrams)". "Every diagram should have a key/legend".
For a phone book: one direction and one specific verb per arrow, and colour coding kept consistent across books.

B13. Anthropic, "Prompting for frontend aesthetics" cookbook (2025-10-21). https://platform.claude.com/cookbook/coding-prompting-for-frontend-aesthetics
Q: "without guidance it tends toward generic, conservative designs."
Q: "You tend to converge toward generic, "on distribution" outputs."
Q: "Guide specific design dimensions".
For a phone book: the drawer has to be given each dimension explicitly. Here that means the grammar of marks, and not "readable labels". No Anthropic or OpenAI guidance specific to SVG diagrams was found (R, from the search).

Also consulted, below the cut or relayed only:
- NN/g, Aurora Harley, "Proximity Principle in Visual Design" (2020-08-02), https://www.nngroup.com/articles/gestalt-proximity/. Q: "Items close together are likely to be perceived as part of the same group". Proximity "can overpower competing visual cues such as similarity of color or shape." R (NN/g topic page): elements connected by a line are seen as belonging together.
- Google Material data-visualization guidance. R: "use color with intent, not for decoration". Official page not read.
- Don Norman, Things That Make Us Smart (1993). R: the naturalness principle, that a representation's surface maps to what it represents. No verbatim found.
- Mermaid community style guides. R: label every connection, keep one direction, split a crowded diagram, dotted for optional, labelled. These are not official Mermaid docs.

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
