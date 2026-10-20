<!-- to-the-living:start -->
Presentation.{ «The Ethos vision» }

# The Ethos vision

```
+-- the golden example ----------------+
|                                      |
|  +-------+                           |
|  | Ethos |                           |
|  +-------+                           |
|      | specifies                     |
|      v                               |
|  +-------+  is built as  +---------+ |
|  | Nexus |<--------------| Chronos | |
|  +-------+               +---------+ |
+------|-------------------------------+
       | guides
       v
   +------+
   | Flow |
   +------+
       | then guides
       v
   +---------------+
   | other nexuses |
   +---------------+
```

### Proposal 1: The golden example · psyche-context › vision/ethos.md

  Flow is one of the best current examples of ethos; its ethos lives in the vision-flow-ethos skill, which carries the code.
+ 
+ ## The golden example
+ 
+ Ethos, the Nexus and the Chronos example project together are the golden example: Flow is implemented properly from it, then the other nexuses.

Ruling: land, amend, or reject.

### Proposal 2: How Ethos is shown · psyche-context › vision/ethos.md

  Ethos is central. The anatomy of the system, every type and every trait
  it uses, is read in its ethos; an implementation is mostly the
  hand-written bodies.
+ 
+ Where types are shown, the Ethos is shown, never the Rust it generates, unless the work is on how Ethos generates Rust.
+ 
+ Ethos is never shown out of context: each declaration names the kind of object it is, and says what its types are for.
+ 
+ A datom is never shown without its Ethos specification.

Ruling: land, amend, or reject.

### Proposal 3: The type ethos · psyche-context › vision/ethos.md

+ ## The type ethos
+ 
+ A type ethos opens with `type` and defines a single type. Every type it needs is declared inline, where it is used; a type from a source comes in by the inline import. It may carry one or more examples of its datom.

```ethos
+ type
+ CommitMessage.[              ; one variant
+    VisionDistillation.Vector< ;  per kind
+       Reference.{            ; a topic and
+          Topic.String        ;   a flow id
+          FlowId.String } > ]
```

```ethos
+ ; datom, expecting CommitMessage
+ VisionDistillation.[ { ethos 081064 } ]
```

Ruling: land, amend, or reject.

### Proposal 4: Whole programs in Ethos · psyche-context › vision/ethos.md

  Ethos will eventually replace everything, Rustlang becoming its
  assembly layer. Designs are chosen for that horizon; what it
  enables — generator emission among it — comes in its time.
+ 
+ The next step toward that horizon is the whole program written in Ethos: its function syntax, its implementations under traits, and a manifest for compiling and finding dependencies. It stays pure description of a program, compact by having no repetition and no noise, never by shortening words.

Ruling: land, amend, or reject.

### Proposal 5: The cost of the datom payload · psyche-context › vision/ethos.md

  Ethos is central. The anatomy of the system, every type and every trait
  it uses, is read in its ethos; an implementation is mostly the
  hand-written bodies.
+ 
+ Ethos is designed with its datom payload in mind: machines write the datom, so what the datom costs to output weighs on every design.
+ 
+ System 1 models speak a subset of Ethos, so they can talk to an Ethos contract.

Ruling: land, amend, or reject.

### Proposal 6: Memory, the stored root · psyche-context › vision/ethos.md

- Library, Signal, Operation, Memory. No version in a file. Signal's sections are
- queries and responses, since there is communication; Sema's are record
- types, the rest to be decided. Signal gives a Nexus its main types and
- Sema its database types.
+ No version in a file. Signal's sections are queries and responses, since there is communication; Memory's are record types, the rest to be decided. Signal gives a Nexus its main types and Memory its database types.
  
  Four roots: Library, Signal, Operation, Memory. Signal declares what a Nexus says; Operation what it does, one operation type for every effect; Memory what it remembers; Library what they share. A memory trait carries a standard successful-or-unsuccessful change and, for each version, the upgrade from the previous format; that upgrade is the very edit the type needs.
+ 
+ Every Nexus has all three: Signal, Operation and Memory.

- dot, a bracket of its traits. In the Signal and Sema roots the
+ dot, a bracket of its traits. In the Signal and Memory roots the

Ruling: land, amend, or reject.

### Proposal 7: The Ethos Nexus · psyche-context › vision/ethos.md

```
 +--------------+    +--------------+
 | repository A |    | repository B |
 +--------------+    +--------------+
        | carries           | carries
        v                   v
 +--------------+    +--------------+
 | datom file   |    | datom file   |
 +--------------+    +--------------+
        | loaded together, atomically
        v
 +----------------------------------+
 | Ethos Nexus                      |
 |  Memory: the registry            |
 +----------------------------------+
        | resolves
        v
 +----------------------------------+
 | a lowercase source name          |
 +----------------------------------+
```

+ ## The Ethos Nexus
+ 
+ The Ethos Nexus has three parts, Signal, Memory and Operation, each written in Ethos.
+ 
+ It keeps the registry of Ethos sources. Each repository carries datom files naming the sources it holds, kept by whoever keeps that repository; they are loaded together, atomically, into one full registry.
+ 
+ The registry changes whenever an Ethos source is added, edited or renamed.

Ruling: land, amend, or reject.

### Proposal 8: Lowercase sources, capital built-ins · psyche-context › vision/ethos.md

  A type may be declared over a type from a source in place, with no entry in the imports section: `Topic.custom:Name` declares `Topic` over the type `Name` from the source `custom`. The source is known twice: its first letter is lowercase, and a colon follows it.
+ 
+ A lowercase source names an entry of the registry. A name with no source and a capital first letter is a core built-in, declared in the core library; the intrinsic names are among them.

```ethos
+ Library
+ []                     ; imports
+ [ Count.Integer        ; types: a core
+                        ;   built-in
+   Topic.custom:Name ]  ;   a registry source
+ []                     ; traits
+ []                     ; associations
```

Ruling: land, amend, or reject.

### Proposal 9: Types taken from Rust · psyche-context › vision/ethos.md

  An import names a source and a type: `protos:String` or
  `protos:[ String Integer ]`. An explicit import and an intrinsic name
  mean the same thing. Intrinsic names known without import: String,
  Integer, Decimal, Boolean, Meaning, Vector, Option, Result, Self.
+ 
+ The types Ethos takes directly from Rust are listed in one vector, specified and kept by hand; the Ethos-to-Rust compiler reads it to know what each type links to.
+ 
+ In time, programmatic feedback on the code says where each type comes from, as it does for a built-in.

Ruling: land, amend, or reject.

### Proposal 10: The special representation · psyche-context › vision/ethos.md

```
 +--------------+
 | runtime type |
 +--------------+
        | bears
        v
 +------------------------+
 | special representation |
 +------------------------+
     | encodes        ^
     | into           | decodes from
     v                |
 +------------------------+
 | representation type    |
 +------------------------+
        | is written as
        v
 +------------+
 | datom text |
 +------------+
```

+ ## The special representation
+ 
+ A type whose datom form differs from its runtime form bears the special representation trait: its own datom encoding and decoding.
+ 
+ Ethos describes the real type and its representation type, which fixes the trait's input and output; Rust does the implementation.
+ 
+ A hash is held in memory as bytes and written in datom in an alphanumeric encoding; a flow id is written as three camelCase words.

Ruling: land, amend, or reject.

### Proposal 11: New types, never aliases · psyche-context › vision/ethos.md

- Ethos Zero emits `Datomizable` and `Compositional` on every struct and
- enum it generates, so every ethos-declared type always bears both
- traits and no declared type can exist without them. An alias bears them
- through the type it names: an alias is not a new type and cannot carry
- a derive.
+ Ethos Zero emits `Datomizable` and `Compositional` on every type it generates, so every ethos-declared type always bears both traits and no declared type can exist without them.
+ 
+ A type of one position is a new type, never a type alias. A struct of one field is never written: `FlowId.String` is the new type. A new type never wraps another new type: if a job is a flow id, it is written flow id.

- pub type FilePath = String;                  // an alias: String already bears both
- pub type SyntaxError = Vec<FilePath>;        // an alias: Vec<T> bears both for any T that does

```rust
+ // a new type: always derived
+ #[derive(Datomizable, Compositional)]
+ pub struct FilePath(String);
+ #[derive(Datomizable, Compositional)]
+ pub struct SyntaxError(Vec<FilePath>);
```

- meaning. Head then symbol is a variant of `Query` or `Response` in a
- Signal's first two sections, an alias in the types section. Where
+ meaning. Head then symbol is a variant of `Query` or `Response` in a
+ Signal's first two sections, a new type in the types section. Where

- [ FilePath.String                          ; types: FilePath is an alias of String
+ [ FilePath.String                          ; types: FilePath is a new type over String

```rust
- pub type LockId = Integer;
- pub type LockName = String;
+ #[derive(Datomizable, Compositional)]
+ pub struct LockId(Integer);
+ #[derive(Datomizable, Compositional)]
+ pub struct LockName(String);
```

```rust
- pub type FilePath = String;
- pub type SyntaxError = Vec<FilePath>;
+ #[derive(Datomizable, Compositional)]
+ pub struct FilePath(String);
+ #[derive(Datomizable, Compositional)]
+ pub struct SyntaxError(Vec<FilePath>);
```

```rust
- pub type FlowId = String;
+ #[derive(Datomizable, Compositional)]
+ pub struct FlowId(String);
```

Ruling: land, amend, or reject.

### Proposal 12: The flow id, a string for now · psyche-context › vision/ethos.md

```ethos
  [ LockId.Integer          ; types
    LockName.String
-   FlowId.String
+   FlowId.String           ; very unideal: a
+                           ;   real id from the
+                           ;   flow's hash is
+                           ;   needed
```

Ruling: land, amend, or reject.

### Proposal 13: Inline is mandatory · psyche-context › vision/ethos.md

- Everything is a type; there is no key-value. A type used once is declared inline where it is used; a type used in more than one place is declared once and named. A variant's payload is written in the variant and bears the variant's name; no second type is invented to hold it. Inline nesting goes about three deep; past that, the type comes from a Library.
+ Everything is a type; there is no key-value. A type used once must be declared inline where it is used, unless it is so deep that it needs too much recursion; an algorithm decides which. A type used in more than one place is declared once and named. A variant's payload is written in the variant and bears the variant's name; no second type is invented to hold it. Inline nesting goes about three deep; past that, the type comes from a Library.

Ruling: land, amend, or reject.

### Proposal 14: Seniority, and structs over chains · psyche-context › vision/ethos.md

  types are defined a bracket is an enum, never a vector. Ethos may
  generate default implementations for Query and Response, which is why
  Signal is its own root.
+ 
+ Variants are ordered by seniority: the first is the most senior. A struct is preferred over a chain of variants.

```ethos
+ Level.[ Spirit       ; most senior
+         Intent
+         Vision
+         Notion ]     ; least senior
```

Ruling: land, amend, or reject.

### Proposal 15: Names made of words · psyche-context › vision/ethos.md

  and ethos code are switched between so often; once ethos is the
  authored language that debt is removed.
+ 
+ A defined object, a type or a trait, and a variant are named in PascalCase. Every other name is an uncapitalized camelCase identifier made of words, checked whenever one is created; its lowercase first letter tells it from a variant. It is a variant made on demand, with no recompiling. Its check lives in a library shared across dialects: a cheap check that its parts are words, falling back to a System 1 judgment held to a certainty threshold.

```ethos
+ ; datom, a Metaflow: an aspect, a topic,
+ ; a layer; the topic is made of words
+ { Mind sourceNexus Tertiary }
```

Ruling: land, amend, or reject.

### Proposal 16: How a trait is named · psyche-context › vision/ethos.md

- Traits are qualifier-named: Runnable, Textualizable, Structural,
- Embodied. Run is not a trait. The verbs Rust imposes, Write and Read
+ A trait is named for the capability it gives its type of object, by a qualifier or by a name: Runnable, Textualizable, Structural, Embodied, ClaudeHost. Run is not a trait. The verbs Rust imposes, Write and Read
  among them, are tolerated as legacy, for cognitive ease while Rust
  and ethos code are switched between so often; once ethos is the
  authored language that debt is removed.

Ruling: land, amend, or reject.

### Proposal 17: Every trait in Ethos · psyche-context › vision/ethos.md

  A capability speaks in Self, the trait's own parameters and other traits; a concrete type in an input is a trait not yet named.
+ 
+ Every feature is a capability, borne by a trait. A trait carries weight: a trait with one function is suspicious, and one borne by a single type is doubly so.
+ 
+ Long term, every trait in a program is declared in Ethos, every implementation sits under one of them, and a mechanical check finds no trait outside the code Ethos generates.
+ 
+ Short term, hand-written traits are allowed.

Ruling: land, amend, or reject.

### Proposal 18: Vertical layout · psyche-context › vision/ethos.md

- Ethos expands vertically: a structure with more than one element opens on its line and its elements hang beneath the first, aligned; the closing delimiter ends the last element's line. Nothing that has a next layer sits on one line.
+ Ethos expands vertically, not horizontally: where a structure would run far to the right, its first element opens on a new line, indented, and each element with a next layer takes its own line. The closing delimiter ends the last element's line; it never takes a line of its own. Nothing that has a next layer sits on one line.
+ 
+ Ethos indents by three spaces. A comment sits above or beside what it comments on, never below, lined up with that object's indentation. A vector may hold several items on a line; past a width it wraps, lined up with its first item.

```ethos
+ Metaflow.{                   ; who a flow is
+    Aspect.[ Psyche Mind Field ]
+    Topic                     ; core by default
+    Layer.[ Primary Secondary
+            Tertiary Quaternary ] }
```

Ruling: land, amend, or reject.

### Proposal 19: White square brackets for a vector · psyche-context › vision/ethos.md

  generate default implementations for Query and Response, which is why
  Signal is its own root.
+ 
+ The white square brackets are sugar for a vector, read at their own layer of interpretation and turned into the vector before the ethos reader sees the text.

```ethos
+ Names.⟦ String ⟧      ; sugar
+ Names.Vector<String>  ; what the reader sees
```

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
