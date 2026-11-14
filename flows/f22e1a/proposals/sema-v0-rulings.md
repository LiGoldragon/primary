Presentation.{ «Sema version 0: a module, read whole» Proposal }

# Sema version 0: a module, read whole

Created by Fable 5.1, on the living's words and on the questions of the Sema lanes. Edition 12 redoes edition 11 on his rulings: the type is SemaZero, a module has two forms, and a Sema value in datom sits in the Meaning delimiter.

### Proposal 1: The type is SemaZero · psyche-belief › vision/sema-v0.md

::: comment
Document was Markdown's word for the tree; the value is version 0 of Sema, and an incompatible version is its own type, named as Ethos Zero is. The language keeps the bare name.
:::

- Version 0 of Sema is Markdown with a typed reading. Markdown is the edge form, as Datom is for signal: text comes in as Markdown and is composed into the tree, and goes out by projecting the tree back into Markdown, one walk in two directions. Memory holds the tree and never the text.
+ Version 0 of Sema is Markdown with a typed reading, and its type is SemaZero. Markdown is the edge form, as Datom is for signal: text comes in as Markdown and is composed into the tree, and goes out by projecting the tree back into Markdown, one walk in two directions. Memory holds the tree and never the text.

```ethos
- [ Document.Vector<Block>
+ [ SemaZero.{ Option<FrontMatter> Vector<Block> } ; a document: its front matter, when it opens with one, and its blocks
```

```ethos
- [ Document.[ Structural ] ]
+ [ SemaZero.[ Structural ] ]
```

### Proposal 2: A module has two forms · psyche-belief › vision/sema-v0.md

::: comment
The real modules open with YAML front matter, which the tree did not hold. A module is written in two forms, and each is its own type. ModuleText is Sema alone: the module as it is filed, the front matter inline in its text, YAML being Sema version 0's text for that part as Markdown is for the body. Module is a struct: the front matter typed in datom, then the body as Sema. The front matter is declared in Ethos; the translator reads the YAML by field name into it and prints it back in the type's order. Inside the Nexus there is no YAML.
:::

+ A belief module is written in two forms, each its own type. ModuleText is Sema alone, the module as it is filed: a SemaZero whose text opens with its front matter. Module is a struct of the front matter, typed, and the body as a SemaZero with no front matter of its own. The one converts into the other by moving the front matter out of the text into its type, and back.

+ FrontMatter has three fields: the description, the dependencies, and the placement, which may be absent. YAML is its text form and nothing more: the translator reads the YAML by field name, in whatever order the fields come, into a FrontMatter value, and prints a FrontMatter back as YAML with the fields in the type's order. A YAML field outside the three is refused as Unsupported; a missing or empty description or dependencies is refused as Missing.

```ethos
+ Library
+ [ sema:[ SemaZero ] ]                         ; imports
+ [ ModuleName.String                           ; types: a module's name, kind-subject, as written in the YAML
+   Placement.[ SystemPrompt Skill ]            ;   where the module is placed: system, or skill
+   FrontMatter.{ Description.String            ;   the front matter, typed; the three fields, in print order
+                 Dependencies.Vector<ModuleName>
+                 Option<Placement> }
+   ModuleText.SemaZero                         ;   the module as filed: Sema alone, front matter inline in the text
+   Module.{ FrontMatter SemaZero } ]           ;   the module as held: the front matter typed, then the body
+ [ Typing.[ type.[ Module ] ]                  ; traits: a filed module becomes a held one,
+   Filing.[ file.[ ModuleText ] ] ]            ;   and a held one becomes a filed one
+ [ ModuleText.[ Typing ]                       ; associations
+   Module.[ Filing ] ]
```

+ A Sema value in datom sits in the Meaning delimiter, ⟪ ⟫, its text being Markdown, indented under the delimiter by the protos margin rule; the same module in its two forms:

```datom
+ ; ModuleText: Sema alone, the front matter inline
+ ⟪
+   ---
+   description: A Field flow uses the tools Mind makes and keeps the system running.
+   dependencies: [vision-aspects]
+   ---
+
+   # The Field aspect
+
+   A Field flow keeps the running system.
+ ⟫
+ ; Module: the front matter typed, then the body
+ { { «A Field flow uses the tools Mind makes and keeps the system running.»
+     [ vision-aspects ]
+     None }
+   ⟪
+     # The Field aspect
+
+     A Field flow keeps the running system.
+   ⟫ }
```

### Proposal 3: The document schema, each type declared once · psyche-belief › vision/sema-v0.md

::: comment
Title, Code and Reference were declared inline and used elsewhere, which Ethos refuses. Code named two things, the fence and the span inside a sentence; a variant named as a defined type carries that type, so the span was illegal, and the names now say which code. Run, the typesetter's word, is renamed TextPart. Outline yields one per top-level section, none for a document without sections; a search hit carries its block; the edit's refusal is declared; Toml is a language the modules use. A link target is a Url in version 0; a link naming a place in a document is a later version's.
:::

+ The tree is typed to its parts: inside a paragraph or a heading, the text is a vector of parts, plain words, emphasis, strong, inline code or a link, so that every query is a walk over types and no text is read inside the Nexus. Markdown is read and printed at the translator alone, and the translator also renders a listing's titles and places as plain lines for the reader.

```ethos
- Section.{ Title.Text Vector<Block> }      ; a heading and what is under it
+ Section.{ Title Vector<Block> }           ; a heading and what is under it
```

```ethos
-         Code.{ Language Text }            ; a fence; Mermaid is a figure
+         CodeBlock                         ; a fence; Mermaid is a figure
```

```ethos
- Language.[ Ethos Datom Rust Nix Shell Ini Mermaid Plain ]
+ Title.Text                                ; a heading's words
+ ProgrammingLanguage.[ Ethos Datom Rust Nix Shell Ini Toml Mermaid Plain ]
```

```ethos
- Text.Vector<Run>                          ; inside a paragraph
- Run.[ Words.String
+ Text.Vector<TextPart>                     ; inside a paragraph or a heading
+ TextPart.[ Words.String                   ; one part of a text, in one style
        Emphasis.Text
        Strong.Text
-       Code.String
-       Reference.{ Text Target } ]         ; a link
+       InlineCode.String                   ; code inside a sentence, between backticks
+       Reference ]                         ; a link
+ CodeBlock.{ ProgrammingLanguage String }  ; a fence: its programming language and its text, plain
+ Reference.{ Text Url }                    ; a link: its words and its target
```

```ethos
- Target.[ Place Url.String ]
+ Url.String                                ; the link target, as written
```

```ethos
- Outline.{ Title.Text Vector<Outline> }
+ Outline.{ Title Vector<Outline> }
```

```ethos
- Kind.[ Headings Statements Code References ]
+ Kind.[ Headings Statements CodeBlocks InlineCode References ]
+ Hit.{ Place Block }                       ; where a search matched, and the block it matched in
```

```ethos
-        Remove.{ Place Block } ] ]
+        Remove.{ Place Block } ]
+ EditRefusal.[ NoSuchPlace.Place           ; why an edit is refused: no block at the place,
+               Mismatch.{ Place            ;   or the block found is not the one expected
+                          Expected.Block
+                          Found.Block } ] ]
```

```ethos
- [ Structural.[ outline.{ [ Depth ] [ Outline ] }          ; the headings, to a depth
+ [ Structural.[ outline.{ [ Depth ] [ Vector<Outline> ] } ; the headings, to a depth: one per top-level section
```

```ethos
-                code.{ [ Place ] [ Vector<Code> ] }         ; the code blocks under a section
+                code.{ [ Place ] [ Vector<CodeBlock> ] }    ; the code blocks under a section
```

```ethos
-                search.{ [ Kind Pattern ] [ Vector<Place> ] } ; a string search over one kind
+                search.{ [ Kind Pattern ] [ Vector<Hit> ] }   ; a string search over one kind; each hit with its block
```

```ethos
-                edit!{ [ Edit ] [ Result<Document Refusal> ] } ] ]
+                edit!{ [ Edit ] [ Result<SemaZero EditRefusal> ] } ] ]
```

### Proposal 4: The reading and its refusal · psyche-belief › vision/sema-v0.md

::: comment
The reading named an Error declared nowhere. A reading fails at a line, for one of two reasons: a construct the tree has no place for, or a front-matter field missing. The library reads all of Markdown; what is Unsupported is what the tree cannot hold.
:::

- Reading and printing are two kinds on two types, named for what each becomes: the Markdown text becomes a Document, the Document becomes Markdown text.
+ Reading and printing are two kinds on two types, named for what each becomes: the Markdown text becomes a SemaZero, the SemaZero becomes Markdown text.

```ethos
- [ sema:[ Document ] ]
- [ Markdown.String ]                          ; the text, as it is written
- [ Composable.[ compose.[ Result<Document Error> ] ]
+ [ sema:[ SemaZero ] ]
+ [ Markdown.String                            ; the text, as it is written
+   ReadRefusal.{ Line.Integer Problem }       ; where reading stopped, and why
+   Problem.[ Unsupported.String               ; a construct the tree has no place for, as written
+             Missing.FrontMatterField ]       ; a front-matter field absent, or empty
+   FrontMatterField.[ Description Dependencies ] ]
+ [ Composable.[ compose.[ Result<SemaZero ReadRefusal> ] ]
```

```ethos
- [ Markdown.[ Composable ]
-   Document.[ Printable ] ]
+ [ Markdown.[ Composable ]
+   SemaZero.[ Printable ] ]
```

### Proposal 5: How the edge reads · psyche-belief › vision/sema-v0.md

::: comment
Rulings the lanes asked for, inferred from the vision: depth is the nesting, so the written level is relative and the print canonical; a link's anchor is text; Place is Sema's own.
:::

+ Depth is the nesting, so the reading is relative: the shallowest heading in the document is the top, each deeper level a child, and a heading skipping a level is Unsupported, since a Section has no depth of its own and the skip has no place in the tree. The print is canonical, a top section at one mark, so a module written from a second-level heading prints back one level up.

+ A link's target, an anchor among them, is read and printed as a Url, the string as written; version 0 has no link that names a place in a document. Place is what Sema yields, in search results and edits, named by the titles from the root, and is never read out of Markdown.

+ A fence's language is the Markdown tag as the modules write it: ethos, datom, rust, nix, sh, ini, toml, mermaid, and no tag for Plain.

### Proposal 6: A type in an input position · psyche-belief › vision/ethos.md

::: comment
His ruling, his words: «we can allow types and traits signatures for now». The line as it stood made the generator refuse every capability that takes data.
:::

- A capability speaks in Self, the trait's own parameters and other traits; a concrete type in an input is a trait not yet named.
+ A capability speaks in Self, the trait's own parameters, other traits and the types declared in the file. A trait stands in an input where any bearer is wanted; a declared type stands there where the data itself is, and is, for now, taken as that type.

### Proposal 7: Markdown is read and printed by a library · psyche-belief › vision/sema-v0.md

::: comment
His first word on version 0, never landed: the edge is an existing Markdown library, both ways. Sema writes no Markdown reader of its own; the typed tree is what is Sema's.
:::

+ Markdown is read and printed by an existing Markdown library, in both directions: the library turns Markdown into its tree and back, and Sema composes its SemaZero from that tree and projects it back into it. Sema writes no Markdown reader of its own.
