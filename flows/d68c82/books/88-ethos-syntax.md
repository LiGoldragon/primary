<!-- to-the-living:start -->
Presentation.{ «Ethos: imports and definition brackets» }

# Ethos: imports and definition brackets

### Proposal 1: colon import, proposed syntax · psyche-context › vision/ethos.md

- An import names a source and a type: `protos:String` or
- `protos:[ String Integer ]`. An explicit import and an intrinsic name
- mean the same thing. Intrinsic names known without import: String,
+ An import starts with a colon, followed by uncapitalized namespace segments separated by colons, ending in the type: `:namespace:sub:Type`. It is usable inline in a type declaration or a field, and the import section uses the same syntax: `:protos:String`, or `:protos:[ String Integer ]` for several. An explicit import and an intrinsic name mean the same thing. Intrinsic names known without import: String,
  Integer, Decimal, Boolean, Meaning, Vector, Option, Result, Self.

```proposed
- Library
- [ protos:[ String Textualizable ]  datom:Datom ]   ; imports
- []                                                 ; types
- []                                                 ; traits
- []                                                 ; associations
+ Library
+ [ :protos:[ String Textualizable ] ; imports
+   :datom:Datom ]
+ []                                 ; types
+ []                                 ; traits
+ []                                 ; associations
```

  The generated code carries no `use` statements; each imported name is
- written fully qualified: `protos:String` appears as `protos::String`,
- `datom:Datom` as `datom::Datom`.
+ written fully qualified: `:protos:String` appears as `protos::String`,
+ `:datom:Datom` as `datom::Datom`.

- A type may be declared over a type from a source in place, with no entry in the imports section: `Topic.custom:Name` declares `Topic` over the type `Name` from the source `custom`. The source is known twice: its first letter is lowercase, and a colon follows it.
+ An import may stand where the type is used, with no entry in the imports section: `Topic.:custom:Name` declares `Topic` over the type `Name` from the namespace `custom`, and a field takes it the same way, `Failure.{ :protos:Error String }`. The leading colon marks it as an import; the namespace segments are uncapitalized and the type is capitalized.
+
```proposed
+ Library
+ []                              ; imports
+ [ Topic.:custom:Name            ; an alias, inline
+   Failure.{ :protos:Error       ; a field, inline
+             String } ]
+ []                              ; traits
+ []                              ; associations
```

```
+--------------------------------------------+
| the registry                               |
+--------------------------------------------+
                      |
                      | holds uncapitalized segments
                      v
+--------------------------------------------+
| :namespace:sub                             |
+--------------------------------------------+
                      |
                      | ends in the type
                      v
+--------------------------------------------+
| :namespace:sub:Type                        |
+--------------------------------------------+
         |                          |
         | listed in                | written in
         v                          v
+-------------------+  +---------------------+
| the import        |  | a declaration or    |
| section           |  | a field, inline     |
+-------------------+  +---------------------+
```

Ruling: land, amend, or reject.

### Proposal 2: white braces for a struct, proposed syntax · psyche-context › vision/ethos.md

  Everything is a type; there is no key-value. A type used once is declared inline where it is used; a type used in more than one place is declared once and named. A variant's payload is written in the variant and bears the variant's name; no second type is invented to hold it. Inline nesting goes about three deep; past that, the type comes from a Library.
+
+ ## White braces define a struct
+
+ White braces define a struct, so a struct definition looks different from a struct value. The definition, in ethos, names the types of its positions inside white braces; the value, in datom, fills them inside plain braces.
+
```proposed
+ Library
+ []                              ; imports
+ [ LockId.Integer                ; types
+   LockName.String
+   Lock.⦃ LockId LockName ⦄ ]    ; a definition
+ []                              ; traits
+ []                              ; associations
```
+
```datom
+ { 7 renew }
```

```
+--------------------------------------------+
| a struct                                   |
+--------------------------------------------+
         |                          |
         | is defined in            | is filled in
         v                          v
+-------------------+  +---------------------+
| white braces,     |  | plain braces,       |
| in ethos          |  | in datom            |
+-------------------+  +---------------------+
```

Ruling: land, amend, or reject.

### Proposal 3: white brackets for a vector, proposed syntax · psyche-context › vision/ethos.md

  Each section has its own parsing context; placement carries the
  meaning. Head then symbol is a variant of `Query` or `Response` in a
  Signal's first two sections, an alias in the types section. Where
- types are defined a bracket is an enum, never a vector. Ethos may
+ types are defined a plain bracket is an enum, never a vector. Ethos may
  generate default implementations for Query and Response, which is why
  Signal is its own root.
+
+ ## White square brackets define a vector
+
+ White square brackets around an item type define a vector type, replacing the word Vector, which is so common: `⟦String⟧` is the vector of String. The vector value keeps its plain brackets in datom.

- Integer, Decimal, Boolean, Meaning, Vector, Option, Result, Self.
+ Integer, Decimal, Boolean, Meaning, Option, Result, Self.

```proposed
- Type.CommitMessage.[ Landing.Vector<String>
+ Type.CommitMessage.[ Landing.⟦String⟧
                       Fix.String ]
```

```
+--------------------------------------------+
| a vector type                              |
+--------------------------------------------+
         |                          |
         | was written as           | is written as
         v                          v
+-------------------+  +---------------------+
| the word Vector   |  | white square        |
| and angle         |  | brackets around     |
| brackets          |  | the item type       |
+-------------------+  +---------------------+
```

Ruling: land, amend, or reject.

### Proposal 4: the white delimiters have ASCII spellings · psyche-context › vision/ethos.md

  Ethos carries a comment on every section and on every line that has a next layer, saying in plain words what the machine reads there; a comment runs from ; to the end of the line.
+
+ ## ASCII spellings of the white delimiters
+
+ White braces and white square brackets have ASCII spellings for any place that cannot show them in a fixed-width face: white braces `{|` and `|}`, white square brackets `[|` and `|]`. The glyph and its spelling are the same delimiter.
+
```proposed
+ Lock.⦃ LockId LockName ⦄
+ Lock.{| LockId LockName |}
+
+ ⟦String⟧
+ [|String|]
```

Ruling: land, amend, or reject.

### Proposal 5: what is open about the syntax · mind-context › inquiry/ethos-syntax-imports-and-brackets.md, a new file

+ ---
+ description: Ethos is written, read or generated with the leading-colon import and the white braces and brackets, and what is still open about them is judged.
+ dependencies: [vision-ethos]
+ ---
+
+ ## What is open
+
+ The living wants an import to start with a colon and be usable inline, white braces to define a struct, and white square brackets to define a vector. None of the three is read by ethos-zero yet. The forms below are checked: the first of each pair by ethos-zero, the second not yet parseable.
+
+ ## The import
+
```proposed
+ today (checked)
+ [ protos:[ Error Textualizable ]
+   datom:Datom ]
+ [ Topic.custom:Name
+   Failure.{ protos:Error String } ]
+
+ proposed (not yet parseable)
+ [ :protos:[ Error Textualizable ]
+   :datom:Datom ]
+ [ Topic.:custom:Name
+   Failure.{ :protos:Error String } ]
```
+
+ Today a source is one name, a colon, then the type, and the inline form already exists: the colon is in use. What is new is the leading colon and more than one segment. Open: the registry has no grammar for its segments yet, so what a segment may contain, how many levels it has and what separates them is undefined; today a source is one Rust path name and a hyphenated name is refused. Open: what the registry namespace `:signal:flow` becomes in generated Rust, and whether a namespace named `core` or `std` meets Rust's own crates. Open: the module text says a source begins with a lowercase letter while the reader accepts a capital; the new rule settles that by making uncapitalized segments the rule. What would settle it: a ruling on the registry segment grammar and the mapping of a namespace to generated Rust.
+
+ ## The colon elsewhere
+
+ The colon is also the receiver mark of a capability that takes no self, `create:[ Self ]`, and the kind:subject naming of context modules, `vision:book`, and the topic `core:Name`. A leading colon begins an import where a type is expected and a receiver colon follows a capability name, so the positions differ; the module and topic names are words about modules, not Ethos text. Datom has no colon separator of its own and quotes a string that begins with a colon. Open: whether a topic `core:Name` is ever written in ethos, and then whether it is an import.
+
+ ## The struct
+
```proposed
+ today (checked)
+ [ LockId.Integer
+   LockName.String
+   Lock.{ LockId LockName } ]
+
+ proposed (not yet parseable)
+ [ LockId.Integer
+   LockName.String
+   Lock.⦃ LockId LockName ⦄ ]
```
+
+ Open: which braces become white. The struct definition does; the root `Library.{`, a complex trait body and a capability with inputs also open with braces, and whether they stay plain is not ruled. The living's words say a struct definition against a struct declaration; read here as definition against value, in datom, which keeps plain braces. Earlier unmerged work made the white pair mean exactly what the plain pair means; this rule gives the white pair a meaning of its own. What would settle it: the list of the places a brace is written in ethos, each ruled white or plain.
+
+ ## The vector
+
```proposed
+ today (checked)
+ [ FilePath.String
+   SyntaxError.Vector<FilePath>
+   Report.{ String Vector<FilePath> } ]
+
+ proposed (not yet parseable)
+ [ FilePath.String
+   SyntaxError.⟦FilePath⟧
+   Report.⦃ String ⟦FilePath⟧ ⦄ ]
```
+
+ Ethos has no map and no set, and datom has none: a struct holds fixed keys and a vector of structs holds the rest. So no map or set takes a white bracket today. Open: whether a set or a map is ever wanted; if one is, it takes its own pair or a word. Open: whether the item type of a vector may itself be a vector, `⟦⟦String⟧⟧`, and whether the word Vector stays as the name of the type in field naming, `string_vector`.
+
+ ## The glyphs
+
+ Measured in a monospace stack on the author's machine, the white square brackets take one cell and the white braces take a wider cell, because no monospace face carries them and the page falls back to a proportional one. Open: how they show on the living's phone, which was not observed. The ASCII spellings are proposed for any place they fail.
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
+ The form reader splits a name at its colons, so a name that begins with a colon, and a heading followed by a colon, are not read as an import today. It must learn the leading colon, or ethos-zero must join the pieces back. The two white pairs are new delimiters for the form reader, which today knows only its own pairs, and datom must treat them as forms or quote a string that holds one. Ethos-zero conceives imports as one source and must hold a chain of segments; its checker, printer and Rust generator follow, and the generator must say what a registry namespace is in Rust. The editor and book tooling that colour ethos know none of the new characters. Every ethos file and fixture written with an import, a struct or the word Vector moves to the new forms, with the generated code checked against its source. Open: whether the form reader or ethos-zero owns the leading colon.
+
+ ## What would settle it
+
+ A ruling on Proposals 1 to 4, the registry segment grammar, the list of braces ruled white or plain, and a look at the glyphs on the living's phone.

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
