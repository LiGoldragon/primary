# trait-rename

Draft diff of psyche-skills skills/vision-ethos.md,
kind renamed to trait where it names the ethos
concept. Base: psyche-skills HEAD f9d74b ("vision-
ethos: trait is the word"), which landed after the
brief and already rewrote the old lines 56-58 into
lines 56-57: "Trait is the word for the bearer of
capabilities, the same word in ethos and in Rust;
kind might be used to also mean traits." This diff
keeps those two lines as context and renames the
rest of that section. Hunk line numbers are HEAD's.

Display: lines longer than 52 characters are wrapped
at 52 at a word boundary; each continuation keeps
its line's prefix ("- ", "+ ", or two spaces for
context).

Left unchanged: line 30 "A memory kind" (its
meaning, ethos trait or sort of memory record, is
unclear and is left for a ruling), line 117 "a
manifest of some kind" (English idiom), the Sources
record names "kinds" (cited record names), line 432
"Interactions — the term for trait implementations"
(already trait), and every Rust-general trait line.

18 hunks.


Hunk 1, from line 1:

~~~
  ---
- description: An ethos file is written, or a type,
- kind or layout is judged against what the living
- wants ethos to be.
+ description: An ethos file is written, or a type,
+ trait or layout is judged against what the living
+ wants ethos to be.
  dependencies: [knowledge-datom, knowledge-protos]
  ---
+
+ ## Flow, a current best example
+
+ Flow is one of the best current examples of ethos;
+ its ethos lives in the vision-flow-ethos skill,
+ which carries the code.

  ## What Ethos is

  Ethos is the schema language. Of the two main
  syntaxes most agents
  will face, Ethos specifies the types and Datom
  fills them with data.

- Ethos is central. The anatomy of the system, every
- type and every kind
+ Ethos is central. The anatomy of the system, every
+ type and every trait
  it uses, is read in its ethos; an implementation
  is mostly the
  hand-written bodies.

~~~

Hunk 2, from line 51:

~~~
  assembly layer. Designs are chosen for that
  horizon; what it
  enables — generator emission among it — comes in
  its time.

- ## Kind
+ ## Trait

  Trait is the word for the bearer of capabilities,
  the same word in
  ethos and in Rust; kind might be used to also mean
  traits.
- In ethos there are no generics, only kinds.
- Declaring a new kind
+ In ethos there are no generics, only traits.
+ Declaring a new trait
  declares a new trait in the Rust world and might
  imply more in the
  ethos world.

- A capability speaks in Self, the kind's own
- parameters and other kinds; a concrete type in an
- input is a kind not yet named.
+ A capability speaks in Self, the trait's own
+ parameters and other traits; a concrete type in an
+ input is a trait not yet named.

  ## Naming

- Kinds are qualifier-named: Runnable,
- Textualizable, Structural,
- Embodied. Run is not a kind. The verbs Rust
- imposes, Write and Read
+ Traits are qualifier-named: Runnable,
+ Textualizable, Structural,
+ Embodied. Run is not a trait. The verbs Rust
+ imposes, Write and Read
  among them, are tolerated as legacy, for cognitive
  ease while Rust
  and ethos code are switched between so often; once
  ethos is the
  authored language that debt is removed.

  ## Identity

- A kind is identified as a Rust trait is, by its
- name and its
+ A trait is identified as a Rust trait is, by its
+ name and its
  constraints, written as one head:
  Processable<[Clonable Sendable]
- Serializable>. A constraint is a kind, or a
- bracket of kinds: what
+ Serializable>. A constraint is a trait, or a
+ bracket of traits: what
  Rust writes as a generic parameter with its
  bounds, ethos writes as
- the bounds alone, since in ethos there are no
- generics, only kinds; a
- constraint in a kind declaration is a kind, never
- a type. Two heads
- that differ in a constraint are two kinds. Which
- constraints belong
+ the bounds alone, since in ethos there are no
+ generics, only traits; a
+ constraint in a trait declaration is a trait,
+ never a type. Two heads
+ that differ in a constraint are two traits. Which
+ constraints belong
  to the identity is not a decision to make: the
  ethos compiles to
- Rust, and what identifies the trait identifies the
- kind. What else a
- kind declares, its superkinds, its associated
- types and constants,
+ Rust, and what identifies the trait in Rust
+ identifies it in ethos. What else a
+ trait declares, its supertraits, its associated
+ types and constants,
  its capabilities, is its definition. Angle
  brackets hold the
  constraints; they are a protos delimiter, recycled
  from Rust as
  Result and Self are.

  ```
  Library
- [ std:[ Clonable Sendable Serializable ] ]
- ; imports: where the three constraint kinds come
- from
+ [ std:[ Clonable Sendable Serializable ] ]
+ ; imports: where the three constraint traits come
+ from
  []
  ; types
- [ Processable<[Clonable Sendable] Serializable>.[
- … ] ]     ; kinds: the head is the identity, the
- name and two
-
- ;   constraints, the first a bracket of two kinds,
- the
-
- ;   second one kind; the bracket after the dot
- holds
+ [ Processable<[Clonable Sendable] Serializable>.[
+ … ] ]     ; traits: the head is the identity, the
+ name and two
+
+ ;   constraints, the first a bracket of two
+ traits, the
+
+ ;   second one trait; the bracket after the dot
+ holds
  
  ;   its capabilities, its definition
  []
  ; associations
  ```
  ```rust
  // The trait's identity: its name and its
  constraints, two generic parameters with their
  bounds.
  // What ethos writes as the bounds alone, Rust
  writes as a named parameter carrying them;
- // the parameter names are Rust's need, not the
- kind's.
+ // the parameter names are Rust's need, not the
+ trait's.
  pub trait Processable<A: Clone + Send, B:
  Serialize> { /* … */ }
  ```

~~~

Hunk 3, from line 116:

~~~
  An ethos file carries no version; datom has no
  versions. What is
  versioned is versioned in a manifest of some kind,
  never in the file.

- A Library's sections, in order, are imports,
- types, kinds and
+ A Library's sections, in order, are imports,
+ types, traits and
  associations. Every root's first section is its
  imports; its own
  sections follow.

~~~

Hunk 4, from line 125:

~~~
  Library
  [ protos:String ]               ; imports
  [ Record.{ String Integer } ]   ; types
- []                              ; kinds
+ []                              ; traits
  []                              ; associations

  ; the canonical form the reader sees, after the
  mechanical conversion
~~~

Hunk 5, from line 148:

~~~
  Library
  [ protos:[ String Textualizable ]  datom:Datom ]
  ; imports
  []
  ; types
- []
- ; kinds
+ []
+ ; traits
  []
  ; associations
  ```

~~~

Hunk 6, from line 159:

~~~
  ## What a declaration turns into

  A declaration turns into the Rust type with named
  fields, bearing the
- datom kinds through the derive, which Ethos Zero
- emits with the type.
+ datom traits through the derive, which Ethos Zero
+ emits with the type.
  A field is named after its type in snake case; a
  constructed type
  type-first, `string_vector`, `lock_option`; a
  repeated type as first
  and second.
~~~

Hunk 7, from line 171:

~~~
    LockName.String
    Lock.{ LockId LockName Vector<String>
  Option<Lock> }
    Generation.{ String String } ]
- []                                            ;
- kinds
+ []                                            ;
+ traits
  []                                            ;
  associations
  ```
  ```rust
~~~

Hunk 8, from line 198:

~~~
    Lock.{ LockId LockName }
    LockRejection.[ DuplicateName.Lock
  ;   an enum: one variant naming a defined type,
                    PathOverlap.{ Lock Lock } ] ]
  ;   one declaring its payload inline
- []
- ; kinds
+ []
+ ; traits
  []
  ; associations
  ```
  ```rust
~~~

Hunk 9, from line 226:

~~~
    SyntaxError.Vector<FilePath>             ;
  SyntaxError is a vector of FilePath
    GenerationFailure.[ SyntaxError          ;
  an enum: the variant SyntaxError is bare here,
                        Unwritable ] ]       ;
  but SyntaxError is a defined type, so it carries
  one
- []                                         ; kinds
+ []                                         ;
+ traits
  []                                         ;
  associations
  ```
  ```rust
~~~

Hunk 10, from line 251:

~~~
  [ FilePath.String
  ; types
    GenerationFailure.[ SyntaxError.Vector<FilePath>
  ;   the payload declared inline: a vector
                        Unwritable.{ FilePath String
  } ] ]  ;   declared inline: a struct, derived name
- []
- ; kinds
+ []
+ ; traits
  []
  ; associations
  ```
  ```rust
~~~

Hunk 11, from line 262:

~~~
  pub enum GenerationFailure {
  SyntaxError(Vec<FilePath>),
  Unwritable(Unwritable_Data) }
  ```

- ## Every declared type bears both kinds
+ ## Every declared type bears both traits

  Ethos Zero emits `Datomizable` and `Compositional`
  on every struct and
  enum it generates, so every ethos-declared type
  always bears both
- kinds and no declared type can exist without them.
- An alias bears them
+ traits and no declared type can exist without
+ them. An alias bears them
  through the type it names: an alias is not a new
  type and cannot carry
  a derive.

~~~

Hunk 12, from line 277:

~~~
  pub enum GenerationFailure {
  SyntaxError(SyntaxError), Unwritable }
  ```

- ## The datom kinds are compiled in only where text
- is spoken
+ ## The datom traits are compiled in only where
+ text is spoken

  A generated signal library bears `Datomizable` and
  `Compositional`
  conditionally, under a feature the CLI and client
  enable and the Nexus
~~~

Hunk 13, from line 324:

~~~
  pub type FlowId = String;
  ```

- ## Kinds are explicit; bodies are hand-written
+ ## Traits are explicit; bodies are hand-written

- A kind is declared, never inferred; an association
- asserts the type
+ A trait is declared, never inferred; an
+ association asserts the type
  bears it. The generated Rust carries a
  compile-time assertion that the
- type bears the kind; the interaction body is
- hand-written Rust.
+ type bears the trait; the interaction body is
+ hand-written Rust.

  ```
  Library
  []
  ; imports
  [ Record.{ String Integer } ]
  ; types
- [ Summarizable.[ summarize.[ String ] ] ]
- ; kinds
+ [ Summarizable.[ summarize.[ String ] ] ]
+ ; traits
  [ Record.[ Summarizable ] ]
  ; associations
  ```
  ```rust
~~~

Hunk 14, from line 348:

~~~
  };
  ```

- ## Kind syntax
+ ## Trait syntax

- A simple kind opens with a bracket after the dot.
- Its capabilities sit
+ A simple trait opens with a bracket after the dot.
+ Its capabilities sit
  inside. The receiver after a capability's head
  names who is called:
  `.` takes self, `!` takes mutable self, `:` takes
  no self. A
  capability with inputs is a headed brace: inputs
  in a bracket, yield
~~~

Hunk 15, from line 360:

~~~
  Library
  []
  ; imports
  [ SinkError.[ Closed Full ] ]
  ; types
- [ Fillable.[ push!{ [ String ] [ Result<Integer
- SinkError> ] } ; kinds
+ [ Fillable.[ push!{ [ String ] [ Result<Integer
+ SinkError> ] } ; traits
               drain![ Vector<String> ]
               create:[ Self ] ] ]
  []
  ; associations
~~~

Hunk 16, from line 375:

~~~
  }
  ```

- A complex kind opens with a brace after the dot.
- Inside: superkinds in
+ A complex trait opens with a brace after the dot.
+ Inside: supertraits in
  a bracket, associated types with their constraints
  in a bracket,
  associated constants in a bracket — upper case,
  each the name, a dot,
  and its type — and capabilities in a bracket.
~~~

Hunk 17, from line 384:

~~~
  Library
  [ std:Serializable ]
  ; imports
  []
  ; types
- [ Fillable.[ create:[ Self ] ]
- ; kinds
+ [ Fillable.[ create:[ Self ] ]
+ ; traits
    Streamable.{ [ Fillable ]
                 [ Item<Serializable> ]
                 [ CAPACITY.Integer ]
~~~

Hunk 18, from line 400:

~~~
  }
  ```

- A kind's identity is its name and its constraints,
- as stated in the
+ A trait's identity is its name and its
+ constraints, as stated in the
  Identity section above.

  ## Associations

- An association declares that a type bears a kind:
- the type's name, a
- dot, a bracket of its kinds. In the Signal and
- Sema roots the
+ An association declares that a type bears a trait:
+ the type's name, a
+ dot, a bracket of its traits. In the Signal and
+ Sema roots the
  associations of the query, response and record
  types are implied and
  never written. In a Library they are the fourth
  section, after the
- kinds.
+ traits.

  ```
  Library
  []
  ; imports
  [ Sink.{ String Integer } ]
  ; types
- [ Summarizable.[ summarize.[ String ] ]
- ; kinds
+ [ Summarizable.[ summarize.[ String ] ]
+ ; traits
    Fillable.[ create:[ Self ] ] ]
  [ Sink.[ Summarizable Fillable ] ]
  ; associations
  ```
~~~

