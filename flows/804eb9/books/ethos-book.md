Presentation.{ «Ethos categories and sugar» }

# Ethos categories and sugar

## psyche-context › vision/ethos.md

````markdown
## Flow, a current best example

Flow is one of the best current examples of ethos; its ethos lives in the vision-flow-ethos skill, which carries the code.

## Where the golden ethos lives

```
┌──────────────────────────────────────────┐
│ vision-ethos                             │
│                                          │
│  what ethos is · its layout              │
│  its two anatomies: types and traits     │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │ the ethos of ethos                 │  │
│  │ the types an ethos file is made of │  │
│  │ the first golden ethos             │  │
│  └────────────────────────────────────┘  │
└───────────────────┬──────────────────────┘
                    │ example
                    ▼
        ┌───────────────────────┐
        │ vision-flow-ethos     │
        │ the Flow Nexus, in    │
        │ ethos; its own skill  │
        └───────────────────────┘
```

The anatomy of ethos lives in vision-ethos itself, as
the first golden ethos; Flow's ethos is one example,
in its own skill.

## What Ethos is

Ethos is the schema language. Of the two main syntaxes most agents
will face, Ethos specifies the types and Datom fills them with data.

Ethos is central. The anatomy of the system, every type and every trait
it uses, is read in its ethos; an implementation is mostly the
hand-written bodies.

## Why Ethos

All the legacy languages have a high noise ratio. Some lisps came
close but lacked the correctness of Rust or Haskell; those have the
correctness but allow no higher layer of abstraction that keeps the
correctness of the whole. Ethos writes the mental model and the code
in one swoop.

## Roots

Library, Signal, Operation, Memory. No version in a file. Signal's sections are
queries and responses, since there is communication; Sema's are record
types, the rest to be decided. Signal gives a Nexus its main types and
Sema its database types.

Four roots: Library, Signal, Operation, Memory. Signal declares what a Nexus says; Operation what it does, one operation type for every effect; Memory what it remembers; Library what they share. A memory trait carries a standard successful-or-unsuccessful change and, for each version, the upgrade from the previous format; that upgrade is the very edit the type needs.

## Non-repetition

Any repetition in ethos syntax is an implementation failure. Ethos
aims to be the most terse, non-repetitive syntax ever made.

Terseness is in the low amount of noise, never in shortened words.

## Self-description

A datom object's basic CLI help emits the Ethos that describes its
anatomy. The wanted mechanism extends this: point at any object —
CLI now, Mentci later — and its Ethos prints, self-describing and
self-evident. The schema syntax serves two audiences: it trains
agents to use things properly, and it shows where the design is
lacking.

## Horizon

Ethos will eventually replace everything, Rustlang becoming its
assembly layer. Designs are chosen for that horizon; what it
enables — generator emission among it — comes in its time.

## Trait

Trait is the word for the bearer of capabilities, the same word in
ethos and in Rust; kind might be used to also mean traits.
In ethos there are no generics, only traits. Declaring a new trait
declares a new trait in the Rust world and might imply more in the
ethos world.

A capability speaks in Self, the trait's own parameters and other traits; a concrete type in an input is a trait not yet named.

## Naming

Traits are qualifier-named: Runnable, Textualizable, Structural,
Embodied. Run is not a trait. The verbs Rust imposes, Write and Read
among them, are tolerated as legacy, for cognitive ease while Rust
and ethos code are switched between so often; once ethos is the
authored language that debt is removed.

## Identity

A trait is identified as a Rust trait is, by its name and its
constraints, written as one head: Processable<[Clonable Sendable]
Serializable>. A constraint is a trait, or a bracket of traits: what
Rust writes as a generic parameter with its bounds, ethos writes as
the bounds alone, since in ethos there are no generics, only traits; a
constraint in a trait declaration is a trait, never a type. Two heads
that differ in a constraint are two traits. Which constraints belong
to the identity is not a decision to make: the ethos compiles to
Rust, and what identifies the trait identifies the trait. What else a
trait declares, its supertraits, its associated types and constants,
its capabilities, is its definition. Angle brackets hold the
constraints; they are a protos delimiter, recycled from Rust as
Result and Self are.

```
Library
[ std:[ Clonable Sendable Serializable ] ]                  ; imports: where the three constraint traits come from
[]                                                          ; types
[ Processable<[Clonable Sendable] Serializable>.[ … ] ]     ; traits: the head is the identity, the name and two
                                                            ;   constraints, the first a bracket of two traits, the
                                                            ;   second one trait; the bracket after the dot holds
                                                            ;   its capabilities, its definition
[]                                                          ; associations
```
```rust
// The trait's identity: its name and its constraints, two generic parameters with their bounds.
// What ethos writes as the bounds alone, Rust writes as a named parameter carrying them;
// the parameter names are Rust's need, not the trait's.
pub trait Processable<A: Clone + Send, B: Serialize> { /* … */ }
```

## Declaration: File

The unit is File: one file, one Rust module. No namespace inside a
file. An ethos file is written in the sweet form: the root's head,
then the sections as siblings, the outer braces omitted. The braced
form — the root's head opening braces that hold every section — is
the canonical form. The sweet form is kept out of the main logic run:
before the text is read as ethos at all, the file is converted
mechanically to the canonical form, so the ethos reader sees only
proper ethos.

An ethos file carries no version; datom has no versions. What is
versioned is versioned in a manifest of some kind, never in the file.

A Library's sections, in order, are imports, types, traits and
associations. Every root's first section is its imports; its own
sections follow.

```
; the sweet form, as a file is written: the head, then the sections as siblings
Library
[ protos:String ]               ; imports
[ Record.{ String Integer } ]   ; types
[]                              ; traits
[]                              ; associations

; the canonical form the reader sees, after the mechanical conversion
Library.{
  [ protos:String ]
  [ Record.{ String Integer } ]
  []
  []
}
```

## The type ethos

`Type` is a single-field variant carrying one declaration, so its payload is the declaration's own form, as any single-field variant's is; it is no exception to the datom.

```
Type.CommitMessage.[ Landing.Vector<String>
                     Fix.String ]
```

## Imports

An import names a source and a type: `protos:String` or
`protos:[ String Integer ]`. An explicit import and an intrinsic name
mean the same thing. Intrinsic names known without import: String,
Integer, Decimal, Boolean, Meaning, Vector, Option, Result, Self.

```
Library
[ protos:[ String Textualizable ]  datom:Datom ]   ; imports
[]                                                 ; types
[]                                                 ; traits
[]                                                 ; associations
```

The generated code carries no `use` statements; each imported name is
written fully qualified: `protos:String` appears as `protos::String`,
`datom:Datom` as `datom::Datom`.

A type may be declared over a type from a source in place, with no entry in the imports section: `Topic.custom:Name` declares `Topic` over the type `Name` from the source `custom`. The source is known twice: its first letter is lowercase, and a colon follows it.

## What a declaration turns into

A declaration turns into the Rust type with named fields, bearing the
datom traits through the derive, which Ethos Zero emits with the type.
A field is named after its type in snake case; a constructed type
type-first, `string_vector`, `lock_option`; a repeated type as first
and second.

```
Library
[]                                            ; imports
[ LockId.Integer                              ; types
  LockName.String
  Lock.{ LockId LockName Vector<String> Option<Lock> }
  Generation.{ String String } ]
[]                                            ; traits
[]                                            ; associations
```
```rust
pub type LockId = Integer;
pub type LockName = String;
#[derive(Datomizable, Compositional)]
pub struct Lock { pub lock_id: LockId, pub lock_name: LockName, pub string_vector: Vec<String>, pub lock_option: Option<Lock> }
#[derive(Datomizable, Compositional)]
pub struct Generation { pub first_string: String, pub second_string: String }
```

## Inline types

A type may be declared where it is used. The inline struct or enum is
a full type whose derived name carries an underscore, non-idiomatic
for a Rust type, so it never collides and reads at a glance as
inferred from the sugar.

```
Library
[]                                                       ; imports
[ LockId.Integer                                         ; types
  LockName.String
  Lock.{ LockId LockName }
  LockRejection.[ DuplicateName.Lock                     ;   an enum: one variant naming a defined type,
                  PathOverlap.{ Lock Lock } ] ]          ;   one declaring its payload inline
[]                                                       ; traits
[]                                                       ; associations
```
```rust
pub type LockId = Integer;
pub type LockName = String;
#[derive(Datomizable, Compositional)]
pub struct Lock { pub lock_id: LockId, pub lock_name: LockName }
#[derive(Datomizable, Compositional)]
pub struct PathOverlap_Data { pub first_lock: Lock, pub second_lock: Lock }
#[derive(Datomizable, Compositional)]
pub enum LockRejection { DuplicateName(Lock), PathOverlap(PathOverlap_Data) }
```

Everything is a type; there is no key-value. A type used once is declared inline where it is used; a type used in more than one place is declared once and named. A variant's payload is written in the variant and bears the variant's name; no second type is invented to hold it. Inline nesting goes about three deep; past that, the type comes from a Library.

## A variant named as a defined type carries that type

When a variant's name is a type already defined in the library, that
type is the data the variant carries. Nothing further is written.

```
Library
[]                                         ; imports
[ FilePath.String                          ; types: FilePath is an alias of String
  SyntaxError.Vector<FilePath>             ;        SyntaxError is a vector of FilePath
  GenerationFailure.[ SyntaxError          ;        an enum: the variant SyntaxError is bare here,
                      Unwritable ] ]       ;        but SyntaxError is a defined type, so it carries one
[]                                         ; traits
[]                                         ; associations
```
```rust
pub type FilePath = String;
pub type SyntaxError = Vec<FilePath>;
#[derive(Datomizable, Compositional)]
pub enum GenerationFailure { SyntaxError(SyntaxError), Unwritable }
```
```
GenerationFailure.SyntaxError.[ /abs/orchestrate.ethos ]     ; the datom
```

## A variant may declare its payload inline

Instead of naming a defined type, a variant may declare what it
carries in place: a vector, a struct, or an enum, each a full type
with a derived name, recursively.

```
Library
[]                                                        ; imports
[ FilePath.String                                         ; types
  GenerationFailure.[ SyntaxError.Vector<FilePath>        ;   the payload declared inline: a vector
                      Unwritable.{ FilePath String } ] ]  ;   declared inline: a struct, derived name
[]                                                        ; traits
[]                                                        ; associations
```
```rust
pub type FilePath = String;
#[derive(Datomizable, Compositional)]
pub struct Unwritable_Data { pub file_path: FilePath, pub string: String }
#[derive(Datomizable, Compositional)]
pub enum GenerationFailure { SyntaxError(Vec<FilePath>), Unwritable(Unwritable_Data) }
```

## Every declared type bears both traits

Ethos Zero emits `Datomizable` and `Compositional` on every struct and
enum it generates, so every ethos-declared type always bears both
traits and no declared type can exist without them. An alias bears them
through the type it names: an alias is not a new type and cannot carry
a derive.

```rust
pub type FilePath = String;                  // an alias: String already bears both
pub type SyntaxError = Vec<FilePath>;        // an alias: Vec<T> bears both for any T that does
#[derive(Datomizable, Compositional)]        // a type: always derived
pub enum GenerationFailure { SyntaxError(SyntaxError), Unwritable }
```

## The datom traits are compiled in only where text is spoken

A generated signal library bears `Datomizable` and `Compositional`
conditionally, under a feature the CLI and client enable and the Nexus
does not. The Nexus compiles the same types without any
textualization capability and without datom-codec as a dependency.

```rust
// emitted by Ethos Zero into the signal crate
#[cfg_attr(feature = "datom", derive(Datomizable, Compositional))]
pub enum Query { Lock(LockRequest), Release(LockId) }
```
```toml
# the CLI's manifest
signal-orchestrate = { version = "…", features = ["datom"] }
# the Nexus's manifest
signal-orchestrate = { version = "…" }
```

## Shapes and placement

Each section has its own parsing context; placement carries the
meaning. Head then symbol is a variant of `Query` or `Response` in a
Signal's first two sections, an alias in the types section. Where
types are defined a bracket is an enum, never a vector. Ethos may
generate default implementations for Query and Response, which is why
Signal is its own root.

```
Signal
[]                                                     ; imports
[ Lock.LockRequest  Release.LockId ]                   ; queries
[ Locked.Lock  Released.Lock ]                         ; responses
[ LockId.Integer                                       ; types
  LockName.String
  FlowId.String
  LockRequest.{ LockName FlowId }
  Lock.{ LockId LockName } ]
```
```rust
pub enum Query    { Lock(LockRequest), Release(LockId) }
pub enum Response { Locked(Lock), Released(Lock) }
pub type LockId = Integer;
pub type LockName = String;
pub type FlowId = String;
```

## Traits are explicit; bodies are hand-written

A trait is declared, never inferred; an association asserts the type
bears it. The generated Rust carries a compile-time assertion that the
type bears the trait; the interaction body is hand-written Rust.

```
Library
[]                                                ; imports
[ Record.{ String Integer } ]                     ; types
[ Summarizable.[ summarize.[ String ] ] ]         ; traits
[ Record.[ Summarizable ] ]                       ; associations
```
```rust
#[derive(Datomizable, Compositional)]
pub struct Record { pub string: String, pub integer: Integer }
pub trait Summarizable { fn summarize(&self) -> String; }
// Compile-time assertion: Record bears Summarizable.
const _: () = {
    fn assert_record_summarizable<T: Summarizable>() {}
    let _ = assert_record_summarizable::<Record>;
};
```

## Trait syntax

A simple trait opens with a bracket after the dot. Its capabilities sit
inside. The receiver after a capability's head names who is called:
`.` takes self, `!` takes mutable self, `:` takes no self. A
capability with inputs is a headed brace: inputs in a bracket, yield
in a bracket. A yield bracket holds one type.

```
Library
[]                                                            ; imports
[ SinkError.[ Closed Full ] ]                                 ; types
[ Fillable.[ push!{ [ String ] [ Result<Integer SinkError> ] } ; traits
             drain![ Vector<String> ]
             create:[ Self ] ] ]
[]                                                            ; associations
```
```rust
#[derive(Datomizable, Compositional)]
pub enum SinkError { Closed, Full }
pub trait Fillable {
    fn push(&mut self, input: String) -> Result<Integer, SinkError>;
    fn drain(&mut self) -> Vec<String>;
    fn create() -> Self;
}
```

A complex trait opens with a brace after the dot. Inside: supertraits in
a bracket, associated types with their constraints in a bracket,
associated constants in a bracket — upper case, each the name, a dot,
and its type — and capabilities in a bracket.

```
Library
[ std:Serializable ]                                ; imports
[]                                                  ; types
[ Fillable.[ create:[ Self ] ]                      ; traits
  Streamable.{ [ Fillable ]
               [ Item<Serializable> ]
               [ CAPACITY.Integer ]
               [ next![ Option<Item> ] ] } ]
[]                                                  ; associations
```
```rust
pub trait Fillable { fn create() -> Self; }
pub trait Streamable: Fillable {
    type Item: Serializable;
    const CAPACITY: Integer;
    fn next(&mut self) -> Option<Self::Item>;
}
```

A trait's identity is its name and its constraints, as stated in the
Identity section above.

## Associations

An association declares that a type bears a trait: the type's name, a
dot, a bracket of its traits. In the Signal and Sema roots the
associations of the query, response and record types are implied and
never written. In a Library they are the fourth section, after the
traits.

```
Library
[]                                                       ; imports
[ Sink.{ String Integer } ]                              ; types
[ Summarizable.[ summarize.[ String ] ]                  ; traits
  Fillable.[ create:[ Self ] ] ]
[ Sink.[ Summarizable Fillable ] ]                       ; associations
```
```rust
// Compile-time assertion: Sink bears Summarizable and Fillable.
const _: () = {
    fn assert_sink_summarizable<T: Summarizable>() {}
    let _ = assert_sink_summarizable::<Sink>;
    fn assert_sink_fillable<T: Fillable>() {}
    let _ = assert_sink_fillable::<Sink>;
};
```

Interactions — the term for trait implementations — use the type
itself in all cases.

No tuple in the code we design; if some parts require it (standard
traits, dependencies), then it is allowed at that contact point only.

## Spacing

Space the delimiters and the inner content. Ethos follows the
canonical protos print: a space inside every bracket and brace
at both ends when non-empty.

Ethos expands vertically: a structure with more than one element opens on its line and its elements hang beneath the first, aligned; the closing delimiter ends the last element's line. Nothing that has a next layer sits on one line.

Ethos carries a comment on every section and on every line that has a next layer, saying in plain words what the machine reads there; a comment runs from ; to the end of the line.

## Zero

Ethos Zero was first named Ethos Monolith; the two are the same thing.
Zero as in version 0: no daemon yet, no Nexus. The ethos repository is
for the ethos nexus that follows.

## Generation

By request to ethos-zero, which is not a daemon, hence its name; committed, held fresh by a test.

```
ethos-zero 'Generate.{ /abs/orchestrate.ethos /abs/out }'
```
````

### Proposal 1: Names say what they name · psyche-context › vision/ethos.md

In Naming. Rule: land, amend or reject.

+ A name says what it names in the system's own words; a word that means something only beside its neighbours, such as First, is not a name.

```ethos
+ Library.{
+ []                                  ; imports
+ [ Prompt.[ SystemPrompt             ; types
+           StartupPrompt ] ]
+ [ Named.[ name.[ String ] ] ]       ; traits
+ [ Named.[ Prompt ] ] }              ; associations
```

### Proposal 2: A capability is named in lowercase · psyche-context › vision/ethos.md

In Trait syntax. Every capability in this book is written so and passes the checker. Rule: land, amend or reject.

+ A capability is named in lowercase camelCase, because it is not a variant: its lowercase first letter tells it from a variant, as a topic's does.

```ethos
+ Library.{
+ []                                  ; imports
+ [ Brief.String ]                    ; types
+ [ Briefing.[ brief.[ String ]       ; traits
+              rewriteBrief!{ [ Named ] [] } ]
+   Named.[ name.[ String ] ] ]
+ [ Brief.[ Briefing Named ] ] }      ; associations
```

### Proposal 3: Library.{ on one line · psyche-context › vision/ethos.md

In Declaration: File. Rule: land, amend or reject.

- An ethos file is written in the sweet form: the root's head, then the sections as siblings, the outer braces omitted.
- The sweet form is kept out of the main logic run: before the text is read as ethos at all, the file is converted mechanically to the canonical form, so the ethos reader sees only proper ethos.
+ A file's usual form is the root's variant, its dot and the brace on one line, then a break, its sections standing unindented one per line, because the root's variant only gives the file its type; this is good form, never a requirement.
+ A file that holds a single thing breaks nowhere.

```ethos
+ Library.{
+ []                                  ; imports
+ [ Sink.{ String Integer } ]         ; types
+ [ Fillable.[ create:[ Self ]        ; traits
+              drain![ Vector<String> ] ] ]
+ [ Fillable.[ Sink ] ] }             ; associations
```

### Proposal 4: One vector per category · psyche-context › vision/ethos.md

In Non-repetition. Rule: land, amend or reject.

+ Where entries share a category, the category holds a vector of them; no entry repeats its category.
+ In associations, a trait borne by several types holds the vector of them: `Prompting.[ SystemPrompt StartupPrompt ]`.
+ An association whose head is a type keeps the vector of traits that type bears.

```ethos
+ Library.{
+ [ flow:[ Key ] ]                    ; imports
+ [ SystemPrompt.⟦ Key ⟧              ; types
+   StartupPrompt.⟦ Key ⟧
+   Placements.⦃ SystemPrompt
+                StartupPrompt ⦄ ]
+ [ Prompting.[ text.[ String ] ] ]   ; traits
+ [ Prompting.[ SystemPrompt          ; associations
+               StartupPrompt
+               Placements ] ] }
```

### Proposal 5: White brackets and white braces · psyche-context › vision/ethos.md

In Shapes and placement. Rule: land, amend or reject.

+ The white square brackets are sugar for a vector, and the white braces for a struct: `⟦ Key ⟧` is `Vector<Key>`, and `⦃ String Integer ⦄` is `{ String Integer }`.
+ Both are read at their own layer and become the plain form before the ethos reader sees the text.

```ethos
+ Library.{
+ []                                  ; imports
+ [ BatchName.String                  ; types
+   Counts.⟦ Integer ⟧
+   Batch.⦃ BatchName Counts ⦄ ]
+ [ Named.[ name.[ String ] ]         ; traits
+   Listed.[ count.[ Integer ] ] ]
+ [ Named.[ BatchName Batch ]         ; associations
+   Listed.[ Counts ] ] }
```

## psyche-context › vision/flow.md

````markdown
## What it does

The Flow Nexus sets up and starts a model flow: its working
directory, system prompt, training files and instruction prompt. It
takes the place of the abandoned training daemon.

Flow is the Nexus that manages flows. A flow is one run of a voice; the component is named for what it manages. A flow the living asks for is launched, properly and surely. Flow holds the lock on flows.

Flow is for starting flows cheaply: clean lean flows, specialized flows and refreshed flows, each with a clean on-point context, which yields higher-quality output. A flow is taken down as easily as it is started. Starting flows is the cornerstone of the system. Flow is probably the most important component to bootstrap, designed together with the Nexus architecture and Ethos.

A flow is one LLM chat, linear and very limited; an agent is a whole being, a lot more than that. Many flows, properly structured and orchestrated, together resemble a synthetic intelligence, synthesized from human knowledge and mathematical probability.

The Capsule is the component that makes where a flow runs. Its first embodiment is the semi-sandbox: only the credential files are copied, everything else is recreated, with its own sockets and store, running light models. Later it encrypts the sensitive parts of the filesystem under a volatile key.

Flow manages metaflows. A metaflow is one address, { Aspect Topic Layer }, that continues through several flows one after another; the flow is its current run, and what is addressed is always the metaflow, never a flow. The default topic is core: the permanent topic, the thing that keeps the machine going, the last topic to stand.

Psyche, Mind and Field have similar payloads, and they go under one: the metaflow, whose aspect is Psyche, Mind or Field.

A topic never dies; it goes idle, its flows turned off. When the living touches on it again, whether to wake a flow for it, and at which layer, is a judgment, made by a small model; a topic is bound to its context modules, so Flow knows what to start it with, together with the new input that warrants it.

A topic's name is a camelCase identifier, uncapitalized. A flow's id is the hash of the harness's session id, kept to six characters and lengthened when two collide, so a transcript is found from the flow id. Where the harness lets Flow choose the session id, Flow chooses it before the flow starts and the flow reads it in its prompt; where the harness assigns it, Flow learns it when the flow binds. No flow declares its id: every call to Flow is identified by the calling process. Anybody may call Flow, a flow for its own refresh among them: because the CLI checks the calling process, a flow refreshes itself safely.

A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the living's words, a result, a notice. Message asks Flow to send a request to a metaflow; Flow owns the lock and the delivery, answers sent or queued, and Message subscribes to Flow's events, learning when a request has entered the flow's context. A metaflow idle is woken by a waking request and receives its whole queue, oldest first, in the first prompt; a metaflow under refresh queues what arrives until its successor has started. A metaflow a request needs is started whether or not it is running; with no working transcript to reawaken, it is fed the metaflow's context modules and the prompt it is to get now.

What has been queued for an idle metaflow, the vision touching its topic among it, is injected with the request that wakes it, so the flow knows it as soon as it wakes.
A metaflow is not woken each time something touching its topic accumulates.

Flow exposes everything from the harness, the bare input: a flow is started, stopped and sent a message through Flow, and Message makes use of it. Flow deploys first and is used raw to send messages, until Message sends through Flow's socket.

## Starting flows

A Nexus component decides the system prompt and everything about a
launch, replacing the harness's subagents with specialized harnesses
launched with specialized system prompts.

A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect; the layer decides the model, declared once in Flow as configuration and changed only over its meta socket. A launch names the metaflow, the context modules composed into its prompts, and a brief of a small paragraph; the Nexus composes the prompt from its module registry.

To the Nexus, a module's location is nothing but its registry entry.

The system prompt is not one thing: it is composed of modules of several types, and what a harness calls a skill overlaps with them.
Its anatomy is drawn up in ethos from a study of system prompts of every kind, each line placed by what it is and by the kind of guidance it belongs to.
Where the harness allows it, a part of a main flow's system prompt is the main flow's alone and is not passed down to its subagents.

Every flow has a topic; a flow with no special topic has the topic core, the heart of its aspect. A topic is a core:Name, a camelCaseExpression checked when created. A flow's title is one datom struct of its aspect, topic, layer and flow id: { Psyche core Secondary <id> }.

Who speaks to whom, within an aspect and across aspects at the same layer in a shared topic, is the vision-aspects skill's. Flow refuses a request that leaves those routes.

## Long term: modules checked by hash

Long term, every module composed into a prompt is checked against its source by its hash, once hashes update efficiently as edits are made; short term, no check is made.

## Repository and context modules

The flow repository holds the machinery of the Flow Nexus and is a runtime repository.
Every context module lives outside it, the basic modules included, so that a change to a module causes no Nix rebuild.
The basic modules give our own take on how an agent behaves in a harness, replacing the prompt the harnesses build in.

## A session is named after its direct ancestor

## A replaced session is reaped by the refresh itself

Reaping belongs to the refresh event, not to a later sweep. A refreshed flow
takes the replaced end out of receiving messages, so a dead end is never
left registered and addressable.

Every harness event reaches Flow through the harness's hooks calling the Flow CLI, so Flow knows each flow's state without polling; a marked block landing in a transcript becomes an action, a book among them, with no tool call by the flow; a flow nearing its context limit is told, writes its handover, and is refreshed as it goes idle. Polling is forbidden; a poller that must exist is registered and reported.

A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.

## Subflows replace the harness subagent facility

The harness subagent facility is replaced. It puts two flows into one
synchronous user interface and locks them both into a single main
flow. A subflow is instead an independent flow with its own system
prompt, which can reply to the successor of whoever it was meant to
answer; that makes the system asynchronous. Subflows run under their
own system prompts because they need different prompts.

## Subflows are created from the questions and requests a flow ends with

Creating a subflow is a routing job: whether there is already a flow
that should simply get this message or this question. A Field
Quaternary flow checks every question and every
request a flow ends with, and, according to the ending flow's
authority, spawns subflows given those questions and requests to
answer or fulfill.

## The requester holds only a request ID

The requester holds nothing of the subflow itself. It is assigned a
request ID, by which it asks later for status, asks for more detail
about what that subflow is doing, and sends the subflow messages
while it is alive. When the subflow is done, the requester receives a
message if it is still the flow in charge.
````

### Proposal 6: The Role and Subagent library · psyche-context › vision/flow.md

Rule: land, amend or reject.

+ A subagent definition names, for each prompt, the vector of modules that goes into it.

```ethos
+ Library.{
+ [ flow:[ Address Layer Key ] ]      ; imports
+ [ RoleName.String                   ; types
+   SubagentName.String
+   Effort.[ Low Medium High ]
+   Modules.⟦ Key ⟧
+   Reach.⟦ Layer ⟧
+   Roles.⟦ RoleName ⟧
+   SystemPrompt.⟦ Key ⟧
+   StartupPrompt.⟦ Key ⟧
+   Role.⦃ RoleName Layer Effort
+          Modules Reach ⦄
+   Definition.⦃ Address Roles ⦄
+   Subagent.⦃ SubagentName
+              SystemPrompt
+              StartupPrompt ⦄ ]
+ [ Named.[ name.[ String ] ]         ; traits
+   Costed.[ cost.[ Integer ] ]
+   Listed.[ count.[ Integer ] ]
+   Prompting.[ text.[ String ] ]
+   Seating.[ roles.[ Roles ] ] ]
+ [ Named.[ RoleName SubagentName     ; associations
+           Role Subagent ]
+   Costed.[ Effort ]
+   Listed.[ Modules Reach Roles ]
+   Prompting.[ SystemPrompt
+               StartupPrompt
+               Role Subagent ]
+   Seating.[ Definition ] ] }
```

```datom
+ { illustrator
+   [ { Intent core } ]
+   [ { Vision book } ] }
```

### Proposal 7: A trait holds the vector of its types · ethos-zero › src/checking.rs

Rule: land, amend or reject.

```rust
                  continue;
              };
-             let mut borne = false;
-             if let File::Library(library) = self {
-                 for association in &library.associations {
-                     if association.identity.name != identity.name {
-                         continue;
-                     }
-                     for reference in &association.traits {
-                         for declared in &library.traits {
-                             if reference.source.is_none()
-                                 && declared.identity.name == reference.name
-                             {
-                                 borne = true;
-                             }
-                         }
-                     }
-                 }
-             }
-             if !borne {
+             let name = &identity.name;
+             let borne = self.borne(name);
+             if borne.is_empty() {
                  let mut path = placed.path;
                  path.push(0);
  …
                  continue;
              };
-             let mut built = false;
-             if let File::Library(library) = self {
-                 for association in &library.associations {
-                     if association.identity.name != identity.name {
-                         continue;
-                     }
-                     for borne in &association.traits {
-                         for declared in &library.traits {
-                             if borne.source.is_none()
-                                 && declared.identity.name == borne.name
-                                 && declared.constructs()
-                             {
-                                 built = true;
-                             }
-                         }
-                     }
-                 }
-             }
-             if !built {
+             let name = &identity.name;
+             if !self.builds(name) {
                  let mut path = placed.path;
                  path.push(0);
  …
  impl Checkable for Association {
+         let head = &self.identity.name;
+         if scope.groups(head) {
+             self.identity.check(scope).place(0)?;
+             let members = &self.members;
+             let listed = members.list_all(scope);
+             return listed.place(1);
+         }
              return Err(Error::conceptual(
  …
          self.identity.check(scope).place(0)?;
-         self.traits.refer_each(scope, Role::Trait, 0).place(1)
+         self.members.bear(scope).place(1)
+     }
+ }
+ 
+ /// The trait whose capability tells whether an
+ /// association's head names a trait, declared or
+ /// Protos's own, so that it lists the types
+ /// bearing it.
+ pub(crate) trait Grouping {
+     fn groups(&self, head: &Name) -> bool;
+     /// The Protos intrinsic a head names, if any.
+     fn kind(&self, head: &Name) -> Kind;
+ }
+ 
+ /// The intrinsic a head names, if it names one.
+ type Kind = Option<Intrinsic>;
+ 
+ impl Grouping for Scope<'_> {
+     fn groups(&self, head: &Name) -> bool {
+         let resolved = self.resolve(head);
+         if let Resolution::Trait(_) = resolved {
+             return true;
+         }
+         let kind = self.kind(head);
+         let role = kind.map(|kind| kind.role());
+         role == Some(Role::Trait)
+     }
+ 
+     fn kind(&self, head: &Name) -> Kind {
+         use Resolution::Imported;
+         use Resolution::Intrinsic as Known;
+         let named = Intrinsic::identify(&head.0);
+         match self.resolve(head) {
+             Known(kind) => Some(kind),
+             Imported(origin, emitted) => {
+                 let from = origin.as_ref();
+                 let own = from == "protos";
+                 let same = &emitted == head;
+                 named.filter(|_| own && same)
+             }
+             _ => None,
+         }
+     }
+ }
+ 
+ /// The outcome of a check that reports no value.
+ type Checked = Result<(), Error>;
+ 
+ /// The trait whose capability checks a type
+ /// that a grouped association lists: an
+ /// unsourced type.
+ trait Listing {
+     fn list(&self, scope: &Scope) -> Checked;
+ }
+ 
+ impl Listing for Reference {
+     fn list(&self, scope: &Scope) -> Checked {
+         if self.source.is_none() {
+             return self.refer(scope, Role::Type);
+         }
+         let form = crate::Form::Name;
+         let problem = Problem::Expected(form);
+         Err(Error::conceptual(vec![], problem))
+     }
+ }
+ 
+ /// The trait whose capabilities check the
+ /// references an association lists.
+ trait Members {
+     /// Check each as a type a trait head lists.
+     fn list_all(&self, scope: &Scope) -> Checked;
+     /// Check each as a trait a type bears.
+     fn bear(&self, scope: &Scope) -> Checked;
+ }
+ 
+ impl Members for Vec<Reference> {
+     fn list_all(&self, scope: &Scope) -> Checked {
+         let mut offset = 0;
+         for member in self {
+             let listed = member.list(scope);
+             let beside = listed.beside(offset);
+             beside.place(0)?;
+             offset += member.span();
+         }
+         Ok(())
+     }
+ 
+     fn bear(&self, scope: &Scope) -> Checked {
+         self.refer_each(scope, Role::Trait, 0)
+     }
+ }
+ 
+ /// Traits a file declares, by reference.
+ type Traits<'a> = Vec<&'a TraitDeclaration>;
+ 
+ /// The trait whose capabilities read
+ /// associations as single types bearing traits,
+ /// a grouped entry spread over the types it
+ /// lists, in order.
+ pub(crate) trait Bearing {
+     /// Every association, one type to an entry.
+     fn bearings(&self) -> Vec<Association>;
+     /// The file's own traits a type bears.
+     fn borne(&self, bearer: &Name) -> Traits<'_>;
+     /// Whether a type bears a constructing trait.
+     fn builds(&self, bearer: &Name) -> bool;
+ }
+ 
+ impl Bearing for File {
+     fn bearings(&self) -> Vec<Association> {
+         let File::Library(library) = self else {
+             return vec![];
+         };
+         let scope = Scope {
+             file: self,
+             identity: None,
+             associated: &[],
+         };
+         let mut read = Vec::new();
+         for entry in &library.associations {
+             let head = &entry.identity.name;
+             if !scope.groups(head) {
+                 read.push(entry.clone());
+                 continue;
+             }
+             for member in &entry.members {
+                 let identity = Identity {
+                     name: member.name.clone(),
+                     constraints: vec![],
+                 };
+                 let borne = Reference {
+                     source: None,
+                     name: head.clone(),
+                     arguments: vec![],
+                 };
+                 read.push(Association {
+                     identity,
+                     members: vec![borne],
+                 });
+             }
+         }
+         read
+     }
+ 
+     fn borne(&self, bearer: &Name) -> Traits<'_> {
+         let File::Library(library) = self else {
+             return vec![];
+         };
+         let mut names = Vec::new();
+         for bearing in self.bearings() {
+             if &bearing.identity.name != bearer {
+                 continue;
+             }
+             for member in bearing.members {
+                 if member.source.is_none() {
+                     names.push(member.name);
+                 }
+             }
+         }
+         let mut borne = Vec::new();
+         for declared in &library.traits {
+             let name = &declared.identity.name;
+             if names.contains(name) {
+                 borne.push(declared);
+             }
+         }
+         borne
+     }
+ 
+     fn builds(&self, bearer: &Name) -> bool {
+         let borne = self.borne(bearer);
+         let mut traits = borne.into_iter();
+         traits.any(TraitDeclaration::constructs)
      }
  }
```

### Proposal 8: A trait holds the vector of its types · ethos-zero › src/conception.rs

Rule: land, amend or reject.

```rust
                  constraints: vec![],
              },
-             traits: body.bracket().place(1)?,
+             members: body.bracket().place(1)?,
          })
      }
```

### Proposal 9: A trait holds the vector of its types · ethos-zero › src/generation.rs

Rule: land, amend or reject.

```rust
  use quote::quote;
  
+ use crate::checking::Bearing;
  …
  impl Locked for File {
      fn locks(&self, name: &Name) -> bool {
-         let File::Library(library) = self else {
-             return false;
-         };
-         for association in &library.associations {
+         for association in self.bearings() {
              if !matches!(
              ) {
                  continue;
              }
-             for borne in &association.traits {
+             for borne in &association.members {
                      return true;
  …
-         let mut assertions = Vec::with_capacity(self.traits.len());
-         for trait_definition in &self.traits {
+         let mut assertions = Vec::new();
+         for trait_definition in &self.members {
              let assertion = Ident::new(
                  &format!(
  …
                  }
-                 for association in &library.associations {
-                     let item = association.emit(scope);
+                 for each in self.bearings() {
+                     let item = each.emit(scope);
                  }
```

### Proposal 10: A trait holds the vector of its types · ethos-zero › src/lib.rs

Rule: land, amend or reject.

```rust
  }
  
- /// An association: a type, by its identity, bears traits.
+ /// An association: a type, by its identity,
+ /// bears traits; or a trait, by its identity,
+ /// is borne by the types listed. The head's
+ /// role decides.
  #[derive(Clone, Debug, PartialEq, Eq)]
  pub struct Association {
-     /// The type's identity.
+     /// The head: a type's identity or a trait's.
      pub identity: Identity,
-     /// The traits it bears.
-     pub traits: Vec<Reference>,
+     /// The traits the type bears, or the types
+     /// bearing the trait.
+     pub members: Vec<Reference>,
  }
  
```

### Proposal 11: A trait holds the vector of its types · ethos-zero › src/protosization.rs

Rule: land, amend or reject.

```rust
  impl Protosizing for Association {
      fn protos(&self) -> Protos {
-         self.identity.heading(
-             Separator::Period,
-             "".enclosed(Enclosure::Bracketed, self.traits.reference_nodes()),
-         )
+         let members = &self.members;
+         let nodes = members.reference_nodes();
+         let bracket = Enclosure::Bracketed;
+         let body = "".enclosed(bracket, nodes);
+         let period = Separator::Period;
+         self.identity.heading(period, body)
      }
  }
```

### Proposal 12: A trait holds the vector of its types · ethos-zero › tests/proposals.rs

Rule: land, amend or reject.

```rust
  //! 5. `⟦ T ⟧` is `Vector<T>` in a type position.
+ //! 6. An association headed by a trait lists the
+ //!    types bearing it: `Trait.[ TypeA TypeB ]`.
  
  use ethos_zero::{
  …
      );
  }
+ 
+ // 6. A trait head lists the types bearing it --
+ 
+ fn keyed(associations: &str) -> String {
+     let key = "Key.{ String }";
+     let system = "SystemPrompt.⟦ Key ⟧";
+     let startup = "StartupPrompt.⟦ Key ⟧";
+     let all = [key, system, startup];
+     let types = all.join(" ");
+     let count = "count.[ Integer ]";
+     let traits = format!("Prompting.[ {count} ]");
+     format!(
+         "Library.{{ [] [ {types} ] [ {traits} ] \
+         [ {associations} ] }}"
+     )
+ }
+ 
+ #[test]
+ fn a_group_generates_as_its_types() {
+     let single = generated(&keyed(
+         "SystemPrompt.[ Prompting ] \
+         StartupPrompt.[ Prompting ]",
+     ));
+     let types = "SystemPrompt StartupPrompt";
+     let group = format!("Prompting.[ {types} ]");
+     let grouped = generated(&keyed(&group));
+     assert_eq!(grouped, single);
+     let mixed = generated(&keyed(
+         "SystemPrompt.[ Prompting ] \
+         Prompting.[ StartupPrompt ]",
+     ));
+     assert_eq!(mixed, single);
+     let file = read(&keyed("Prompting.[ Key ]"));
+     let printed = file.print();
+     let entry = "[ Prompting.[ Key ] ]";
+     assert!(printed.contains(entry), "{printed}");
+ }
+ 
+ #[test]
+ fn a_head_is_a_trait_or_a_type() {
+     let source = keyed("Nothing.[ Key ]");
+     let name = "Nothing".to_owned();
+     let problem = Problem::Undeclared(name);
+     let refused = (vec![1, 3, 0], problem);
+     assert_eq!(refusal(&source), refused);
+ }
+ 
+ #[test]
+ fn a_trait_head_lists_only_types() {
+     let both = "Prompting.[ Key Prompting ]";
+     let listed = keyed(both);
+     let name = "Prompting".to_owned();
+     let at = vec![1, 3, 0, 1, 0, 1];
+     let refused = (at, Problem::Role(name));
+     assert_eq!(refusal(&listed), refused);
+     let unknown = keyed("Prompting.[ Nothing ]");
+     let name = "Nothing".to_owned();
+     let problem = Problem::Undeclared(name);
+     assert_eq!(refusal(&unknown).1, problem);
+     let form = ethos_zero::Form::Name;
+     let problem = Problem::Expected(form);
+     let entry = "Prompting.[ protos:String ]";
+     let sourced = keyed(entry);
+     assert_eq!(refusal(&sourced).1, problem);
+ }
```

