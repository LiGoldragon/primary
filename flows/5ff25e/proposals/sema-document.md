Presentation.{ «Sema version 0: Markdown, read structurally» Proposal }

# Sema version 0: Markdown, read structurally

Created by Fable 5.1, on the living's words.

### Proposal 1: Sema version 0 · psyche-belief › modules/vision:sema:v0.md

::: comment
Version 0 writes no syntax of its own: Markdown is the text, the typed tree is the record, and every structural question is a walk over the tree.
:::

+ ---
+ description: Sema, version 0: Markdown read into a typed tree and printed back from it, so a document is held, edited and searched by its structure.
+ dependencies: [vision:sema, vision:datom, vision:ethos]
+ ---

+ # Markdown, read structurally

+ Version 0 of Sema is Markdown with a typed reading. Markdown is the edge form, as Datom is for signal: text comes in as Markdown and is composed into the tree, and goes out by projecting the tree back into Markdown, one walk in two directions. Memory holds the tree and never the text.

+ The tree is what Markdown already has, named: a heading opens a section and its depth is the nesting; a paragraph is a statement, the unit a reviewer rules on; a fence is code in a language, a Mermaid fence a figure; a link is a reference; a list, a quote and a table are what they are. A block is placed by the titles of the sections above it.

```ethos
+ Library
+ []
+ [ Document.Vector<Block>
+   Section.{ Title.Text Vector<Block> }      ; a heading and what is under it
+   Block.[ Statement.Text                    ; a paragraph
+           Section
+           Code.{ Language Text }            ; a fence; Mermaid is a figure
+           List.Vector<Block>
+           Quote.Vector<Block>
+           Table.Vector<Row> ]
+   Row.Vector<Text>
+   Language.[ Ethos Datom Rust Nix Shell Ini Mermaid Plain ]
+   Text.Vector<Run>                          ; inside a paragraph
+   Run.[ Words.String
+         Emphasis.Text
+         Strong.Text
+         Code.String
+         Reference.{ Text Target } ]         ; a link
+   Target.[ Place Url.String ]
+   Place.Vector<Text>                        ; the titles above a block, from the root
+   Depth.Integer
+   Outline.{ Title.Text Vector<Outline> }
+   Kind.[ Headings Statements Code References ]
+   Pattern.String
+   Edit.[ Insert.{ Place Block }
+          Replace.{ Place Old.Block New.Block }
+          Remove.{ Place Block } ] ]
+ ; what is asked of a document
+ [ Structural.[ outline.{ [ Depth ] [ Outline ] }          ; the headings, to a depth
+                code.{ [ Place ] [ Vector<Code> ] }         ; the code blocks under a section
+                references.{ [ Place ] [ Vector<Reference> ] }
+                search.{ [ Kind Pattern ] [ Vector<Place> ] } ; a string search over one kind
+                edit!{ [ Edit ] [ Result<Document Refusal> ] } ] ]
+ [ Document.[ Structural ] ]
```

+ Reading and printing are two kinds on two types, named for what each becomes: the Markdown text becomes a Document, the Document becomes Markdown text.

```ethos
+ Library
+ [ sema:[ Document ] ]
+ [ Markdown.String ]                          ; the text, as it is written
+ [ Composable.[ compose.[ Result<Document Error> ] ]
+   Printable.[ print.[ Markdown ] ] ]
+ [ Markdown.[ Composable ]
+   Document.[ Printable ] ]
```

```datom
+ ; outline to depth 2 of the Belief Nexus module
+ { «The Belief Nexus» [ { «Signal» [] } { «Meta» [] } { «Memory» [] } ] }
+ ; the code under one section
+ [ { Ethos «Signal …» } ]
+ ; a search over headings alone
+ [ [ «The Belief Nexus» «Signal» ] ]
```

### Proposal 2: Belief imports the document · psyche-belief › vision/belief-nexus-v1.md

::: comment
The Belief Nexus holds modules as Documents and edits them structurally.
:::

```ethos
- [ datom:[ Meaning ] ]
+ [ sema:[ Document Block Edit Place Outline ] ]
```

### Proposal 3: the written form, a brainstorm · mind-belief › modules/notion:sema:v1.md

::: comment
What was tried today for a syntax of Sema's own, kept as a notion in Mind: ideas, none intended yet, for the version that gives Sema a text of its own.
:::

+ ---
+ description: Sema's own written form, a brainstorm: delimiters as kinds, heads as names, depth by mark; ideas, none ruled.
+ dependencies: [vision:sema:v0, vision:datom]
+ ---

+ # The written form, a brainstorm

+ Sema is an extension of Datom: a parenthesis opens it, and inside, every delimiter may take a meaning of Sema's own. The machine writes now, so the keyboard's limits are gone: every pair Unicode gives is available, and a notation can be chosen for the eye alone.

+ A delimiter says what kind of thing a thing is; a head names a particular thing. Datom's manners keep their meaning inside: a guillemet string is a run of text, a bracket a list, a brace a struct by position, a head types what follows, a semicolon a comment, and Ethos's angle bracket a constraint. Delimiters are precious: a pair is spent only where structure cannot already tell, and a pair per sentence is too many.

+ A paragraph is a boundary, not a container: one move of thought, set down before the next. One character marks it, the pilcrow, inside the text.

+ Section titles may carry their own delimiters, a size per depth, so a title has spaces and the path to a block is the titles as written.

```sema
+ ( ◀The Belief Nexus▶
+   «Holds the belief modules and furnishes workspaces with them.
+    ¶ Belief is what a model believes when it starts.»
+   ◄Signal►
+   «What it says.»
+   Ethos.⟦
+     Signal
+     [] ⟧
+   ◂Inputs▸
+   «Register takes a module source.»
+   ◄Memory►
+   «What it remembers; its inputs are in ⟨◀The Belief Nexus▶◄Signal►⟩.» )
```

+ The anatomy of expression, for the version that types the inside of a statement: an expression has a predicate, participants in an order of necessity, and a force that the context supplies. The kind of an expression is read from its shape alone, the count of its fields and the shape of each, never from its words; two kinds that need the same shape are one kind, or one of them takes a delimiter. The positions English fixes are kept in English order; past them a role goes on the word as a head, as a case ending does in Sanskrit, and is then order-free.

```sema
+ (flow idle)                       ; a thing and its state
+ (fable Model)                     ; a thing and its type
+ (flow sends message To.opus)      ; three positions, then roles on the word
+ ((flow idle) (nexus refreshes flow))   ; two expressions: a condition
```

### Proposal 4: a notion is a Mind belief · psyche-belief › vision/psyche.md

::: comment
A notion is not yet intended, and psyche is intention; so it leaves psyche for Mind.
:::

- Psyche contains Spirit, Intent, Vision, and Notion, in descending authority.
+ Psyche contains Spirit, Intent and Vision, in descending authority. A notion is an idea not yet intended, a brainstorm the living has had and not ruled on; it is a Mind belief, kept in the mind repository under its own kind, and a notion that he rules into vision leaves Mind for Psyche.
