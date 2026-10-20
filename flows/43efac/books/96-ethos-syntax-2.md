<!-- to-the-living:start -->
Presentation.{ «Ethos: imports and definition brackets, second edition» }

# Ethos: imports and definition brackets, second edition

### Proposal 1: Vector among the intrinsic names, keep or remove · psyche-context › vision/ethos.md

```
+--------------------------------------------+
| the name Vector                            |
+--------------------------------------------+
         |                          |
         | keep: stays known        | remove: leaves
         v                          v
+-------------------+  +---------------------+
| Vector<String>    |  | only ⟦String⟧       |
| and ⟦String⟧      |  | names the type      |
| are one type      |  |                     |
+-------------------+  +---------------------+
```

  Alternative a, keep: the sentence on the names known without import stays as it is, and one line follows it.

+ Vector stays a known name: `Vector<String>` and `⟦String⟧` are one type, the second its short form.

  Alternative b, remove: the word leaves that sentence, and each place that still writes it moves to the white brackets.

- The names known without import depend on the Ethos object type; a Library, the standard library, knows String, Integer, Decimal, Boolean, Meaning, Vector, Option, Result, Self and Sized.
+ The names known without import depend on the Ethos object type; a Library, the standard library, knows String, Integer, Decimal, Boolean, Meaning, Option, Result, Self and Sized.

```text
-   Lock.{ LockId LockName Vector<String> Option<Lock> }
+   Lock.{ LockId LockName ⟦String⟧ Option<Lock> }
```

```text
-   SyntaxError.Vector<FilePath>             ;        SyntaxError is a vector of FilePath
+   SyntaxError.⟦FilePath⟧                   ;        SyntaxError is a vector of FilePath
```

```text
-   GenerationFailure.[ SyntaxError.Vector<FilePath>        ;   the payload declared inline: a vector
+   GenerationFailure.[ SyntaxError.⟦FilePath⟧              ;   the payload declared inline: a vector
```

```text
-              drain![ Vector<String> ]
+              drain![ ⟦String⟧ ]
```

Ruling: land alternative a, land alternative b, amend, or reject.

### Proposal 2: The old import syntax in the remaining examples · psyche-context › vision/ethos.md

  In Identity, the imports line of the trait example. It imports Clonable, Sendable and Serializable, and the head Processable<[Clonable Sendable] Serializable> uses all three.

```text
- [ std:[ Clonable Sendable Serializable ] ]                  ; imports: where the three constraint traits come from
+ [ :std:[ Clonable Sendable Serializable ] ]                 ; imports: where the three constraint traits come from
```

  In Declaration: File, the imports line of the sweet form. It imports String, and Record uses it.

```proposed
  Library
- [ protos:String ]               ; imports
+ [ :protos:String ]              ; imports
  [ Record.{ String Integer } ]   ; types
```

  In Declaration: File, the same line in the canonical form.

```proposed
  Library.{
-   [ protos:String ]
+   [ :protos:String ]
    [ Record.{ String Integer } ]
```

  In the complex trait example of Trait syntax. It imports Serializable, and the associated type Item<Serializable> uses it.

```text
- [ std:Serializable ]                                ; imports
+ [ :std:Serializable ]                               ; imports
```

Ruling: land, amend, or reject.

### Proposal 3: An enum is a vector of its variants, in the two places that treat them as apart · psyche-context › vision/ethos.md

  In A variant may declare its payload inline.

  Instead of naming a defined type, a variant may declare what it
- carries in place: a vector, a struct, or an enum, each a full type
- with a derived name, recursively.
+ carries in place: a vector of one item type, a struct, or an enum, which is a vector of its variants, each a full type with a derived name, recursively.

  In White square brackets define a vector, after its first paragraph.

  White square brackets around an item type define a vector type, replacing the word Vector, which is so common: `⟦String⟧` is the vector of String. The vector value keeps its plain brackets in datom.
+
+ An enum declaration is a vector too, of its variants, and keeps its plain brackets; white square brackets name a vector of items of one type.

Ruling: land, amend, or reject.

### Proposal 4: What is open about the syntax · mind-context › inquiry/ethos-syntax-imports-and-brackets.md, a new file

+ ---
+ description: The leading-colon import, the white braces and the white square brackets of Ethos are landed in the vision; what is still open about their colon, their braces and the reader and generators that must learn them is judged.
+ dependencies: [vision-ethos]
+ ---
+
+ ## What is open
+
+ The vision lands three forms: an import that starts with a colon, white braces for a struct definition, and white square brackets for a vector type. None is read by ethos-zero yet: when the first edition was written, ethos-zero main (17.0.0, 07714b0) refused a file written with all three as Expected.Import. The examples below are the landed forms, each beside today's.
+
+ ## The import
+
+ Today:
+
```proposed
+ Library
+ [ protos:[ Error Textualizable ]
+   datom:Datom ]
+ [ Record.{ Error Datom } ]
+ []
+ [ Record.[ Textualizable ] ]
```
+
+ Landed:
+
```proposed
+ Library
+ [ :protos:[ Error Textualizable ]
+   :datom:Datom ]
+ [ Record.{ Error Datom } ]
+ []
+ [ Record.[ Textualizable ] ]
```
+
+ Inline, today and landed:
+
```proposed
+ [ Topic.custom:Name
+   Failure.{ protos:Error String } ]
+
+ [ Topic:custom:Name
+   Failure.{ :protos:Error String } ]
```
+
+ What is new is the leading colon, more than one segment, and the colon in place of the dot. Open: the registry has no grammar for its segments, so what a segment may contain, how many levels it has and what separates them is undefined; a source is one Rust path name today and a hyphenated name is refused. Open: what a registry namespace such as `:signal:flow` becomes in generated Rust, and whether a namespace named `core` or `std` meets Rust's own crates. Open: with the dot gone, a declared name and the namespace share the colon in `Topic:custom:Name`; the capital of the first segment tells them apart, and what `Topic:Name`, with no namespace, means is not ruled, since the alias is written `Topic.Name`. Open: the reader accepts a source that begins with a capital; the vision requires uncapitalized segments. What would settle it: a ruling on the registry segment grammar, on `Topic:Name`, and on the mapping of a namespace to generated Rust.
+
+ ## The colon elsewhere
+
+ The colon is also the receiver mark of a capability that takes no self, `create:[ Self ]`, and the kind:subject naming of context modules, `vision:book`, and the topic `core:Name`. A capability name is lowercase and its colon is followed by a bracket; an import colon leads, or follows a capitalized declared name. The module and topic names are words about modules, not Ethos text. Datom has no colon separator of its own and quotes a string that begins with a colon. Open: whether a topic `core:Name` is ever written in Ethos; it has no leading colon, so it would not be an import.
+
+ ## The braces
+
```proposed
+ Library
+ [ LockId.Integer
+   LockName.String
+   Lock.⦃ LockId LockName ⦄ ]
```
+
+ The struct definition is white. Open: which other braces become white. The root `Library.{` of the canonical form, a complex trait body, a capability with inputs and an inline payload struct also open with braces, and the vision does not say which are definitions. Every struct definition in the vision's own examples, the types section, the inline payloads and the imports example among them, is still written in plain braces; they move when the list is ruled. The white pair is a struct definition against a struct value in datom, which keeps plain braces. What would settle it: the list of the places a brace is written in Ethos, each ruled white or plain.
+
+ ## The vector
+
```proposed
+ Library
+ [ FilePath.String
+   SyntaxError.⟦FilePath⟧
+   Failure.⦃ String SyntaxError ⦄
+   Report.⦃ String ⟦FilePath⟧ ⦄ ]
```
+
+ Ethos has no map and no set. The living has asked for a set, for a flow's models; whether a set or a map takes a white pair of its own or a word is not ruled. Open: whether the item type of a vector may itself be a vector, `⟦⟦String⟧⟧`. Open: whether the word Vector stays known (Proposal 1), and so whether a field of a vector type is still named `string_vector`.
+
+ ## The reader and the generators
+
+ Each of the three changes meets the same path: the text is read for its form, then conceived as ethos, then checked, printed and generated.
+
```
+--------------------------------------------+
| ethos text                                 |
+--------------------------------------------+
                      |
                      | is read for form by
                      v
+--------------------------------------------+
| the protos reader                          |
+--------------------------------------------+
                      |
                      | is conceived as ethos by
                      v
+--------------------------------------------+
| ethos-zero                                 |
+--------------------------------------------+
         |                          |
         | checks and prints        | generates
         v                          v
+-------------------+  +---------------------+
| the checker and   |  | the Rust generator  |
| the printer       |  |                     |
+-------------------+  +---------------------+
```
+
+ The form reader splits a name at its colons, so a name that begins with a colon, and a heading followed by a colon, are not read as an import today. It must learn the leading colon and the colon in place of the dot, or ethos-zero must join the pieces back. The two white pairs are new delimiters for the form reader, which today knows only its own pairs, and datom must treat them as forms or quote a string that holds one. Ethos-zero conceives imports as one source and must hold a chain of segments; its checker, printer and Rust generator follow, and the generator must say what a registry namespace is in Rust. The editor and book tooling that colour Ethos know none of the new characters. Every Ethos file and fixture written with an import, a struct definition or the word Vector moves to the new forms, with the generated code checked against its source. Open: whether the form reader or ethos-zero owns the leading colon.
+
+ ## What would settle it
+
+ A ruling on the registry segment grammar, on `Topic:Name`, on the list of braces ruled white or plain, and on the set.

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
