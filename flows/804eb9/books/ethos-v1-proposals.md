```
+-------------+
|    Ethos    |
+-------------+
   | declares
   v
+-------------+   fills    +-------------+
| types and   |<-----------|    Datom    |
| traits      |            +-------------+
+-------------+
   | generates through Ethos Zero
   v
+-------------+
| Rust types  |
| and traits  |
+-------------+
   | are given bodies by
   v
+-------------+
| hand-written|
| capabilities|
+-------------+
```

```
+-------------------------+
| a file: a vector of     |
| roots                   |
+-------------------------+
   | holds            | holds
   v                  |
+-----------------+   |
| Library: what   |   |
| is shared       |   |
+-----------------+   |
   | is shared by     |
   v                  v
+-------------------------+
| Signal: what it says    |
| Operation: what it does |
| Memory: what it keeps   |
+-------------------------+
```

```
+------------+
|    type    |
+------------+
   | bears
   v
+------------+
|   trait    |
+------------+
   | holds
   v
+------------+
| capability |
+------------+
   | is
   v
+------------+
| what the   |
| type does  |
+------------+
```

### Proposal 1: A file is a vector of roots · psyche-context › vision/ethos.md

In Roots. Rule: land, amend or reject.

+ A file is a vector of roots, so a library, a signal, a memory and an operation may stand in one file; which roots share a file is file management only.

```ethos
+ [ Library.{
+   []
+   [ Name.String
+     Shape.[ Round Square ]
+     Sink.{ Name Shape } ]
+   [ Named.[ name.[ String ] ]
+     Shaped.[ shape.[ Shape ] ] ]
+   [ Named.[ Name Sink ]
+     Shaped.[ Shape Sink ] ] }
+   Memory.{
+   []
+   [ Record.{ Name Integer } ]
+   [ Stored.[ store![ Record ] ] ]
+   [ Stored.[ Record ] ] } ]
```

### Proposal 2: A file of one root may drop the vector · psyche-context › vision/ethos.md

Added to Proposal 1. Reject it, and every file is written as a vector. Rule: land, amend or reject.

+ A file that holds one root may write it without the vector.

### Proposal 3: Every root carries traits · psyche-context › vision/ethos.md

In Roots and Associations. Rule: land, amend or reject.

+ Every root ends with a traits section and an associations section, as a Library does, because a type does things only through the traits it bears.
- In the Signal and Sema roots the associations of the query, response and record types are implied and never written.

### Proposal 4: A type that bears no trait is refused · psyche-context › vision/ethos.md

In Traits are explicit; bodies are hand-written. Rule: land, amend or reject.

+ Every declared type bears at least one trait; a type that bears none is refused, because it does nothing.

### Proposal 5: A type over one type is a new type · psyche-context › vision/ethos.md

In What a declaration turns into. Rule: land, amend or reject.

+ A type declared over one other type is a new type, never an alias: `Name.String` is a struct of one unnamed position.
+ A struct has at least two positions; a type of one position is written as a new type, `Name.String`, never `Name.{ String }`.
+ An enum has at least two variants.

### Proposal 6: Ethos is shown as Ethos · psyche-context › vision/ethos.md

In What Ethos is. Rule: land, amend or reject.

+ Ethos is shown as Ethos; the Rust it generates is shown only where the subject is how Ethos generates Rust.

### Proposal 7: A new type is written as its value · psyche-context › vision/datom.md

Follows Proposal 5. Reject it, and a new type is written as a struct of one position, `{ Ada }`. Rule: land, amend or reject.

+ A new type is written as the value it wraps: a `Name` reads `Ada`, never `{ Ada }`.

```datom
+ { Ada 1990 }
```
