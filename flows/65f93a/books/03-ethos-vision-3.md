<!-- to-the-living:start -->
Presentation.{ «The Ethos vision, 3rd edition» }

# The Ethos vision, 3rd edition

### Proposal 1: Infrastructure and the golden example, a new section after Flow, a current best example · psyche-context › vision/ethos.md

+ Ethos and the Nexus are the basic infrastructure everything is built from.
+ Chronos is the example project built with them: the golden example from which Flow is implemented properly, then the other nexuses.

Ruling: land, amend, or reject.

### Proposal 2: How Ethos is shown, added to What Ethos is · psyche-context › vision/ethos.md

+ Where types are shown, the Ethos is shown, never the Rust it generates, unless the work is on how Ethos generates Rust.
+ Ethos is never shown out of context: each declaration names the kind of object it is and says what its types are for.
+ A datom is never shown without its Ethos specification.

Ruling: land, amend, or reject.

### Proposal 3: The type ethos, a new section after Declaration: File · psyche-context › vision/ethos.md

+ A type ethos opens with `type` and defines a single type.
+ Every type it needs is declared inline, where it is used; a type from a source comes in by the inline import.
+ A type ethos may carry one or more examples of its datom.

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
+ VisionDistillation.[ { ethos 000000 } ]
```

Ruling: land, amend, or reject.

### Proposal 4: Whole programs in Ethos, added to Horizon · psyche-context › vision/ethos.md

+ The next step toward that horizon is the whole program written in Ethos: its function syntax, its implementations under traits, and a manifest for compiling and finding dependencies.
+ It stays pure description of a program, compact by having no repetition and no noise, never by shortening words.

Ruling: land, amend, or reject.

### Proposal 5: The cost of the datom payload, added to What Ethos is · psyche-context › vision/ethos.md

+ Ethos is designed with its datom payload in mind: machines write the datom, so what the datom costs to output weighs on every design.
+ System 1 models speak a subset of Ethos, so they can talk to an Ethos contract.

Ruling: land, amend, or reject.

### Proposal 6: Memory, the stored root, in Roots and Associations · psyche-context › vision/ethos.md

- Library, Signal, Operation, Memory.
- No version in a file.
- Signal's sections are queries and responses, since there is communication; Sema's are record types, the rest to be decided.
- Signal gives a Nexus its main types and Sema its database types.
+ No version in a file.
+ Signal's sections are queries and responses, since there is communication; Memory's are record types, the rest to be decided.
+ Signal gives a Nexus its main types and Memory its database types.
+ Every Nexus has all three: Signal, Operation and Memory.
- In the Signal and Sema roots the associations of the query, response and record types are implied and never written.
+ In the Signal and Memory roots the associations of the query, response and record types are implied and never written.

Ruling: land, amend, or reject.

### Proposal 7: The Ethos Nexus, a new section after Generation · psyche-context › vision/ethos.md

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


+ The Ethos Nexus has three parts, Signal, Memory and Operation, each written in Ethos.
+ It keeps the registry of Ethos sources.
+ Each repository carries datom files naming the sources it holds, kept by whoever keeps that repository.
+ They are loaded together, atomically, into one full registry.
+ The registry changes whenever an Ethos source is added, edited or renamed.

Ruling: land, amend, or reject.

### Proposal 8: Lowercase sources, capital built-ins, added to Imports · psyche-context › vision/ethos.md

+ A lowercase source names an entry of the registry.
+ A name with no source and a capital first letter is a core built-in, declared in the core library; the intrinsic names are among them.

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

### Proposal 9: Types taken from Rust, added to Imports · psyche-context › vision/ethos.md

+ The types Ethos takes directly from Rust are listed in one vector, specified and kept by hand.
+ The Ethos-to-Rust compiler reads that vector to know what each type links to.
+ In time, programmatic feedback on the code says where each type comes from, as it does for a built-in.

Ruling: land, amend, or reject.

### Proposal 10: The special representation, a new section after Every declared type bears both traits · psyche-context › vision/ethos.md

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


+ A type whose datom form differs from its runtime form bears the special representation trait: its own datom encoding and decoding.
+ Ethos describes the real type and its representation type, which fixes the trait's input and output; Rust does the implementation.
+ A hash is held in memory as bytes and written in datom in an alphanumeric encoding.
+ A flow id is written in datom as three camelCase words.

Ruling: land, amend, or reject.

### Proposal 11: New types, never aliases, in Every declared type bears both traits · psyche-context › vision/ethos.md

- An alias bears them through the type it names: an alias is not a new type and cannot carry a derive.
+ A type of one position is a new type, never a type alias, and bears both traits like every declared type.
+ A struct of one field is never written: `FlowId.String` declares the new type.
+ A new type never wraps another new type: if a job is a flow id, it is written flow id.
- Head then symbol is a variant of `Query` or `Response` in a Signal's first two sections, an alias in the types section.
+ Head then symbol is a variant of `Query` or `Response` in a Signal's first two sections, a new type in the types section.

```ethos
- [ FilePath.String   ; types: an alias
+ [ FilePath.String   ; types: a new type
```

Ruling: land, amend, or reject.

### Proposal 12: The flow id, a string for now, in Shapes and placement · psyche-context › vision/ethos.md

```ethos
-   FlowId.String
+   FlowId.String           ; very unideal: a
+                           ;   real id from the
+                           ;   flow's hash is
+                           ;   needed
```

Ruling: land, amend, or reject.

### Proposal 13: Inline is mandatory, in Inline types · psyche-context › vision/ethos.md

- A type used once is declared inline where it is used; a type used in more than one place is declared once and named.
+ A type used once must be declared inline where it is used, unless it is so deep that it needs too much recursion; an algorithm decides which.
+ A type used in more than one place is declared once and named.

Ruling: land, amend, or reject.

### Proposal 14: Seniority, and structs over chains, added to Shapes and placement · psyche-context › vision/ethos.md

+ Variants are ordered by seniority: the first is the most senior.
+ A struct is preferred over a chain of variants.

```ethos
+ Level.[ Spirit       ; most senior
+         Intent
+         Vision
+         Notion ]     ; least senior
```

Ruling: land, amend, or reject.

### Proposal 15: Names made of words, added to Naming · psyche-context › vision/ethos.md

+ A defined object, a type or a trait, and a variant are named in PascalCase.
+ Every other name is an uncapitalized camelCase identifier made of words, checked whenever one is created; its lowercase first letter tells it from a variant.
+ Such an identifier is a variant made on demand, with no recompiling.
+ Its check lives in a library shared across dialects: a cheap check that its parts are words, falling back to a System 1 judgment held to a certainty threshold.

```ethos
+ ; datom, a Metaflow: an aspect, a topic,
+ ; a layer; the topic is made of words
+ { Mind sourceNexus Tertiary }
```

Ruling: land, amend, or reject.

### Proposal 16: How a trait is named, in Naming · psyche-context › vision/ethos.md

- Traits are qualifier-named: Runnable, Textualizable, Structural, Embodied.
+ A trait is named for the capability it gives its type of object, by a qualifier or by a name: Runnable, Textualizable, Structural, Embodied, ClaudeHost.

Ruling: land, amend, or reject.

### Proposal 17: Every trait in Ethos, added to Trait · psyche-context › vision/ethos.md

+ Every feature is a capability, borne by a trait.
+ A trait carries weight: a trait with one function is suspicious, and one borne by a single type is doubly so.
+ Long term, every trait in a program is declared in Ethos, every implementation sits under one of them, and a mechanical check finds no trait outside the code Ethos generates.
+ Short term, hand-written traits are allowed.

Ruling: land, amend, or reject.

### Proposal 18: Vertical layout, in Spacing · psyche-context › vision/ethos.md

- Ethos expands vertically: a structure with more than one element opens on its line and its elements hang beneath the first, aligned; the closing delimiter ends the last element's line.
+ Ethos expands vertically, not horizontally: where a structure would run far to the right, its first element opens on a new line, indented, and each element with a next layer takes its own line.
+ The closing delimiter ends the last element's line; it never takes a line of its own.
+ Ethos indents by three spaces.
+ A comment sits above or beside what it comments on, never below, lined up with that object's indentation.
+ A vector may hold several items on a line; past a width it wraps, lined up with its first item.

```ethos
+ Metaflow.{                   ; who a flow is
+    Aspect.[ Psyche Mind Field ]
+    Topic                     ; core by default
+    Layer.[ Primary Secondary
+            Tertiary Quaternary ] }
```

Ruling: land, amend, or reject.

### Proposal 19: White square brackets for a vector, added to Shapes and placement · psyche-context › vision/ethos.md

+ The white square brackets are sugar for a vector, read at their own layer of interpretation and turned into the vector before the ethos reader sees the text.

```ethos
+ Names.⟦ String ⟧      ; sugar
+ Names.Vector<String>  ; what the reader sees
```

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
