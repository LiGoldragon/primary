Presentation.{ «How a proposal is made» }

# How a proposal is made

Created by Fable, from his comments on Version one.

### Proposal 1: A proposal states what is wanted · psyche-belief › vision/proposal.md

**Comment** Why "Version 1 is proven when" is not vision: a proposal says what is wanted, and a done-criterion is a step of work, an order.

  A proposal is the prose and the code that describe the system.

+ A proposal lives in its source file and is edited on his comments. A book is one publication of a proposal, at one link; the edited proposal is published as a new book, and the commented one stays as he left it.
+
+ A proposal states what is wanted of the system; it documents nothing. A proof, a test, a milestone or a sequence of work is an order, and goes to a bead; written into a proposal it is a vision impurity.
+
+ A versioned module is self-contained: everything true of that version is in it, and the version is named once, in its description. Another version is not mentioned.

### Proposal 2: Code and charts before prose · psyche-belief › vision/proposal.md

**Comment** He prefers arrows and Ethos to prose; Ethos is itself a flowchart, the types its nodes, the traits the actions between them.

  What can be expressed in code is shown as code, with a comment where the code needs one; prose is the comment on the code. A method is shown with the trait it belongs to and that trait's ethos, so its inputs and its yield are read. Code not yet settled is marked tentative. A "never" or an "always" is code: the rule is shown as the code that enforces it.

+ A shape is a flowchart, written in a mermaid fence and drawn by the bookmaker as a vector graphic. Prose carries only what neither code nor chart can. Ethos is the first chart: its types are the nodes and its traits the actions between them.
+
+ Code shown is complete: every name it uses is declared in the proposal, a method with its trait in ethos. A type wraps nothing without purpose: a variant carries a type bare when the wrapping would name nothing the type does not.

```ethos
Emission
[]
[ Command.{ Verb Vector<Argument> } ]  ; the emission is the type
[ Outcome.[ Done Refused.Integer ] ]   ; not Ran.Outcome
[ Verb.[ List Show ] Argument.[ Name.String Quiet ] ]
[ Arguable.[ argv.[ Vector<String> ] ] ]
[ Command.[ Arguable ] ]
```

### Proposal 3: A commented book is edited · mind-belief › knowledge/book-making.md

**Comment** His word on the flowcharts: written in mermaid, drawn by the bookmaker as vertical vector graphics, never run through a renderer. The rule that a commented book is never republished stands as it is.

- An unlabelled fence holds a box-and-arrow sketch and nothing else; each one has its figure, `fig-N.svg` in the figures directory, drawn by the illustrator from the sketch with every box, label and arrow kept. A figure shows how a thing moves, one question per figure, is at most 52 columns wide, and is drawn in the figure grammar of vision-book. Every other fence carries its language: `ethos`, `datom`, `rust`, `sh`, `yaml`, `text`. An `ethos` fence is code that passes ethos-zero's Check, run by the author before the book is sent. A module written in Markdown is shown as rendered text. A book shows belief modules as rendered text and change marks.
+ A flowchart is written in a `mermaid` fence and drawn by the bookmaker, never run through a diagram renderer: each becomes a custom vector graphic, `fig-N.svg` in the figures directory, with every box, label and arrow kept. It runs vertically, a narrow column reading top to bottom that fits a phone without sideways scrolling; a chart that would sprawl sideways is restacked. Nothing is cut off: every box is sized to its text, and a long label wraps inside its box. Colour tells kinds of thing or flow apart, line thickness marks what matters most, dashing, box weight and grouping show structure. Every other fence carries its language: `ethos`, `datom`, `rust`, `sh`, `yaml`, `text`. An `ethos` fence is code that passes ethos-zero's Check, run by the author before the book is sent. A module written in Markdown is shown as rendered text. A book shows belief modules as rendered text and change marks.
