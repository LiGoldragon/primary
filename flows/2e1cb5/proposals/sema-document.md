Presentation.{ «The document: Sema version 0 and version 1» Proposal }

# The document: Sema version 0 and version 1

Created by Fable 5.1, on the living's words.

### Proposal 1: Sema version 0, the document · psyche-belief › modules/vision:sema:v0.md

::: comment
Version 0 types language and expression; the inside of an expression stays text, and a block is placed by the names of the sections above it.
:::

+ ---
+ description: Sema, version 0, the document: what Markdown does, as types, with the inside of an expression left as text.
+ dependencies: [vision:sema, vision:ethos]
+ ---

+ # The document

+ Language is how expressions are arranged: a document holds blocks, a section is a block that holds blocks, and depth is nesting. Expression is what a piece of text does: it states, asks or orders; a statement is the unit a reviewer rules on. The inside of an expression is text. Inside the parentheses that open a Sema, the delimiters carry Sema's own meanings, so the written form is as succinct as Markdown and no expression is prefixed by its kind; the types here are what the written form reads into, and the written form is designed after them.

```ethos
+ Library
+ []
+ ; language: how expressions are arranged
+ [ Document.{ Title.Text Vector<Block> }
+   Block.[ Section.{ Title.Text Vector<Block> }
+           Expression
+           Code.{ Language Text }
+           Figure.Flowchart ]
+   ; expression: what a piece of text does
+   Expression.[ Statement.Text
+                Inquiry.Text
+                Injunction.Text ]
+   Text.String
+   Language.[ Ethos Datom Rust Nix Shell Ini
+              Text ]
+   ; Mermaid in the figure grammar; tentative
+   Flowchart.String
+   ; a block's place: the titles of the sections
+   ;   above it, from the root; the block is named
+   ;   by itself within that section
+   Place.Vector<Text>
+   Edit.[ Insert.{ Place Block }
+          Replace.{ Place Old.Block New.Block }
+          Remove.{ Place Block } ]
+   ; the tree of section names
+   Outline.{ Title.Text Vector<Outline> } ]
+ []
+ []
```

```datom
+ { «The Belief Nexus»
+   [ Statement.«Belief is what a model believes
+                when it starts.»
+     Section.{ «Signal»
+               [ Code.{ Ethos «Signal …» } ] } ] }
```

### Proposal 2: Belief imports the document · psyche-belief › vision/belief-nexus-v1.md

::: comment
Block and Edit come from Sema.
:::

```ethos
- [ datom:[ Meaning ] ]
+ [ sema:[ Block Edit Place Outline ] ]
```

### Proposal 3: Sema version 1, the shapes of expression · psyche-belief › modules/vision:sema:v1.md

::: comment
Version 1 opens the expression: each shape a statement takes is one variant with its terms, and a term may be an expression nested.
:::

+ ---
+ description: Sema, version 1, the shapes of expression: each shape a statement takes is one variant with its terms, over version 0's document.
+ dependencies: [vision:sema, vision:ethos]
+ ---

+ # The shapes of expression

+ A statement has a shape, and each shape is a variant with its terms, so a statement is written as its shape and its terms. The shapes are those the vision speaks in; a shape met that none covers is added, and a statement no shape fits is plain text. A term is a name, plain text or an expression nested.

```ethos
+ Library
+ [ :sema:v0:[ Document Block Code Figure
+              Text Language Flowchart Place Edit
+              Outline ] ]
+ ; expression: each shape one variant
+ [ Expression.[ Statement Inquiry Injunction
+                Plain.Text ]
+   Statement.[
+      Is.{ Subject.Term Predicate.Term }
+      For.{ Thing.Term Purpose.Term }
+      Holds.{ Holder.Term Held.Term }
+      Lives.{ Thing.Term Place.Term }
+      Decides.{ Decider.Term Decided.Term }
+      Names.{ Namer.Term Named.Term }
+      Reaches.{ From.Term To.Term
+                Option<Through.Term> }
+      Replaces.{ New.Term Old.Term }
+      Becomes.{ Thing.Term Result.Term
+                Option<When.Term> }
+      Carries.{ Carrier.Term Carried.Term }
+      Written.{ Thing.Term Form.Term }
+      MadeOf.{ Whole.Term Vector<Term> }
+      OneOf.{ Thing.Term Vector<Term> }
+      Every.{ Thing.Term Predicate.Term }
+      When.{ If.Term Then.Term }
+      Example.{ Of.Term Instance.Term }
+      Does.{ Agent.Term Action.Term
+             Option<Object.Term> } ]
+   Inquiry.[ Which.{ Of.Term }
+             Whether.Term
+             Why.Term
+             How.Term ]
+   Injunction.[ Do.{ Agent.Term Action.Term
+                     Option<Object.Term> }
+                Send.{ To.Term What.Term }
+                Read.Term ]
+   ; a term: a name, text, or an expression
+   Term.[ Name.String
+          Plain.Text
+          Nested.Expression ] ]
+ []
+ []
```

```datom
+ ; the Nexus holds every module
+ Holds.{ Name.nexus
+         Nested.Every.{ Name.module
+                        Plain.«held» } }
+ ; a correct system goes quiet when nothing changes
+ When.{ Plain.«nothing changes»
+        Nested.Does.{ Name.system
+                      Plain.«goes quiet» None } }
```
