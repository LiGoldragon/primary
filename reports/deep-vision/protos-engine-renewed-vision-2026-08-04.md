# Protos Engine Renewed Psyche Vision

Date: 2026-08-04

Purpose: durable pickup point for implementation after the 2026-08-04 Claude
design session. This is a vision and authority map, not a replacement design
log and not an implementation report.

## Freshness and sources

The complete current Claude transcript was read from:

`/home/li/.claude/projects/-home-li-primary/6b31eff3-6477-4ee4-baed-cb491ebadd48.jsonl`

Audit point at the end of reacquisition:

- 498 JSONL records, 1,221,420 bytes
- SHA-256:
  `de65544057d3aaef42baaabae0bde0e1f578ea43353993a5a16c2ffad4c04f13`
- Last conversational turn: assistant UUID
  `1db4622c-b5d6-468f-9268-b82ae99a5372`, timestamp
  `2026-08-04T13:06:44.088Z`
- That turn reports commit `478c9654` and confirms the delimiter rulings are
  family-wide, including Dotos.
- Last timestamped transcript record: turn-duration UUID
  `34ce62f9-f66e-41e5-9bac-ee36caa790db`, timestamp
  `2026-08-04T13:06:44.116Z`.
- Four trailing un-timestamped Claude metadata records follow that turn:
  `last-prompt`, `ai-title`, `mode`, and `permission-mode`.

The read also covered the authoritative primary design logs through
`design/ProtosEngine/llmTokenOptimizationRulings-2026-08-04.md`, the earlier
Protos design logs linked from it, the compiled design and firsthand ruling
logs in `/git/github.com/LiGoldragon/protos-engine/design/ProtosEngine/`, and
the current Beads records for `primary-xqb` and its related MVP work.

## Provenance key

- **Psyche**: directly stated or directly confirmed by the psyche.
- **Approved proposal**: an agent supplied the detailed shape and the psyche
  explicitly confirmed it or proceeded on that basis.
- **Delegated**: the psyche explicitly gave agents authority to choose the
  provisional implementation shape.
- **Inference**: a useful synthesis that is not itself psyche authority.
- **Superseded**: formerly authoritative but displaced by a later ruling.

## Vision in one frame

**Psyche:** Protos is an LLM-first family of real languages whose recurring
text must minimize token cost. It relies on schema-once, positional,
non-repetitive representation rather than repeating field names and type tags.
Human readability still matters, but it is the readability of a trained human,
not JSON-style redundancy. Future models will be trained on Protos, so the
familiarity of current frozen models does not veto long-run token optimality.

**Psyche:** Encoded form is the truth. Text, including Rust, is a projection.
The final system is not a set of text codecs: it is a stateful, typed,
operationally edited language engine. Text files are the bootstrap interface;
the end state holds encoded objects in daemon slots, changes them through
atomic operations, and renders requested textual projections.

**Psyche:** The family has complementary surfaces:

- Dotos fills types with data.
- Ethos specifies types and is the terse, sweet declaration surface.
- Nomos is the typed transformer language that makes Ethos adaptable.
- Logos is the complete explicit program representation and the gateway to
  assembly-Rust.
- Rust is assembly and a Logos textual projection, not the authored semantic
  center.

All family members use the shared Protos TextualForm/EncodedForm machinery,
name tree, structure tree, expected-type-at-position parsing, and the same
family-wide delimiter rulings. They need not have literally identical
grammars or archive layouts.

## Desired character and engineering values

### Token cost and non-repetition

**Psyche:** Ethos is to be the most terse, non-repetitive syntax possible.
Anything that position, expected type, or the governing transformer can infer
must not be repeated. Inferable repetition is an implementation failure in
the transformer or grammar, not author burden.

**Psyche:** Positional records with no field names are the main token win.
Delimiter micro-optimization matters less, but still controls recurring cost
and cognitive regularity. The dot stays in `Name.{` because it is token-free
in measured vocabularies and visually superior.

### Correctness and refusal

**Psyche:** More correctness machinery pays for itself as a system grows.
Expected types, typed positions, strict encoded forms, traits, encoded
identity, and typed failures are all part of that correctness layer.

**Psyche:** Transformation and derivation dependencies form a DAG. Cycles
refuse with a typed error naming the loop, and the atomic operation changes
nothing. Lazy dependency evaluation, fixpoint evaluation, and constraint
regions are out.

### Working programs, not text preservation

**Psyche:** Textual byte identity is meaningless. A textual projection is
correct when decoding it yields the same encoded value. Layout whitespace is
presentation. Semantically encoded text, such as whitespace inside a string,
remains meaningful.

**Psyche:** The acceptance bar is working programs and aggressive real
testing, not byte-golden output. Vertical slices must reach compiling and
running emitted Rust.

### Deep-redesign license

**Psyche:** Current code is not binding. Existing code is evidence about
behavior and previous attempts, not design authority. Redesign and rewrite
anything whose existing abstraction is now inappropriate.

**Psyche, current implementation direction:** trivial decisions must not stop
the train. Make the most elegant choice, normally rewriting an obsolete
shape, leave a visible note where review is useful, and continue.

## Language and encoded-form model

### Shared machinery

**Psyche:** Name tree and structure tree data from `protos` drive all textual
encoding and decoding, including Rust. Boundary discovery is structural and
recursive; typed parsing happens after boundaries are known. File-kind-specific
parsers are an implementation failure. A new Ethos file kind is a new root
type plus, at most, a small trait implementation.

**Psyche:** Every Ethos file has exactly three top-level objects for now:
header, imports, body. The header carries the Ethos file kind and a writer-
bumped SemVer-style compatibility version. Imports are textual-projection
concerns only; encoded form references absolute encoded identities. The body
root type selects Interface, Nexus, Sema, Traits, or a future useful kind.

**Psyche:** Interface bodies have positional inputs, outputs, refusals, and
shared types. Membership is trait-based and implied by position. Nexus files
specify a daemon's behavior traits and the types in their signatures.
`sema.ethos` specifies its daemon's record types, tables, and keys.

### Strict encoded types

**Psyche:** Every encoded form has a purpose-designed type for exactly that
form. Catch-all carriers such as `Vec<Fields>` and a universal
`TransformerApplication { name, transformer, payload }` are rejected.

**Psyche:** There is one strict input type per transformer:
`StreamInitiation`, `StreamTermination`, and equivalents for other
transformers. Each carries its transformer's full input schema. The payload
decodes directly into that type; there is no generic transformer application
node between syntax and meaning.

**Inference caution:** The ruling rejects semantically untyped or catch-all
containers. It does not imply that an honest typed collection field is
forbidden when the schema itself says vector-of-`Topic`, map-of-`Name`, and so
on. The `primary-0l8` acceptance sentence, read literally as banning every
generic container anywhere on an encoded surface, is broader than the
psyche's examples and should be implemented according to semantic strictness,
not literal container prohibition.

## Current family-wide syntax

The following is the operative 2026-08-04 surface. It supersedes conflicting
examples in the 2026-08-02 primer and the 2026-08-03 pipe ruling.

### Declarations and applications

- `Name.{...}` declares a struct.
- `Name.[...]` declares an enum.
- `Name.Symbol` declares a newtype or unary type application as determined by
  the expected position.
- `Name.Transformer.(...)` is a standalone transformer application.
- `Name.(...)` is available when an enclosing typed position supplies the
  transformer.
- `|` has no grammar duty and is retired.
- The application dot never separates from its delimiter.

### Strings

**Psyche:** `“...”` is the sole string carrier across the Protos family. It
replaces parenthesized multi-word text and every pipe-text form. Curly quotes
are distinct from ASCII double quote, preserving quotation-safe embedding in
double-quote hosts.

**Approved proposal:** Curly strings use balanced nesting. Unbalanced literal
curly quotes use `\“` and `\”`; literal backslash uses `\\`. Multiline
strings dedent by minimal common indentation, preserving true content while
allowing pretty structural indentation.

`«»` remains approved as a delimiter pair but has no assigned grammar slot
and is disfavored for wire syntax because measured token cost varies sharply
between tokenizers.

### Angles, qualities, and declaration-side pickup

**Psyche:** One bare angle syntax serves the quality system:
`Vector<Ordered>` and `Result<Vector<Ordered> Error>`. The dot form is not
used for angle application.

**Approved proposal:** `Quality.[Shape Trait]` is the ontology exposed by
angle use.

- Shape names engine-provided structural constructors such as Vector,
  Option, and Map. They can accept unconstrained types and are not called
  generics in the Protos ontology.
- Trait names contractual qualities such as Ordered or Sortable. Authored
  declarations parameterize only through traits and are therefore always
  bounded. No universal `Anything` trait is needed.
- Resolution, not a second surface syntax, classifies names.
- A bare pickup occurrence such as `<Ordered>` in a declaration introduces
  the parameter. There is no separate generic-parameter head.
- Repeated bare mentions of the same trait co-refer to one parameter:
  `Range.{<Ordered> <Ordered>}` emits one `Ordered: Ord` parameter used twice.
- Distinct parameters with the same trait use names:
  `<Left.Sortable> <Right.Sortable>`.

**Inference caution:** The confirmed examples also allow concrete authored
types as angle arguments, such as `Error` in
`Result<Vector<Ordered> Error>`. The log's compact `Quality.[Shape Trait]`
wording does not separately spell the encoded representation of such a
concrete authored type argument. The implementation should preserve the
single angle syntax and let resolution produce a strict type-level reference;
it should leave a focused design/code note if the two-variant representation
needs a precise widening or nesting to cover authored concrete types.

### Naming at the Rust boundary

**Psyche:** Ethos, Nomos, and Logos use correct, legible full names:
`Ordered`, `Vector`, `Text`. Rust abbreviations are `incorrectNaming` and are
confined to Rust textual emission through a single translation table:
`Ordered` to `Ord`, `Vector` to `Vec`, `Text` to `String`, and so on. Emitted
type parameters retain the proper trait name, for example
`struct Sorted<Ordered: Ord>(Vec<Ordered>);`, rather than inventing `T`.

### Dotos impact

**Psyche:** Every delimiter ruling is family-wide. Dotos visibly changes in
one material place: `“...”` replaces both parenthesized multi-word strings and
pipe text. Dotos structs `{}`, vectors `[]`, dotted variant paths, `;;`
comments, and bare atoms remain. Angle qualities are type-side, so data text
usually does not write them. `Map.(...)` remains syntactically consistent
with the family application form; treating Map as a Nomos transformer rather
than merely a shape is not separately psyche-ruled.

## Type ontology and trait ontology

**Psyche:** Traits are the code ontology: a checked map of what roles exist
and what they mean. Implementations should live under named traits, including
hand-written Rust, with a long-run target of complete coverage.

**Psyche, most recent scope:** This is a soft implementation requirement,
encouraged but not blocking. Where the proper trait is not obvious, add the
case to a per-repository trait-migration file for later psyche review with a
Claude agent. It is not a mass-refactor pass and it must not stop an MVP
slice.

This latest soft/non-blocking rule supersedes older instructions to stop and
escalate every unclear trait placement during implementation. Trait-first
design remains the preferred first pass where the domain role is clear.

Contracts repositories contain traits and pure contract types, not behavior.
The component playing the role owns its implementations.

## Daemon and storage boundaries

### Stateful daemons and Sema

**Psyche:** Every language daemon is stateful and owns its own Sema database.
Sema is the shared database engine used by daemons, not a fourth downstream
language daemon and not a central `sema-storage` daemon.

**Psyche:** A separate small `sema-translator` daemon owns name/identity
allocation. This is distinct from Sema as storage. The detailed old translator
implementation is evidence and may be rewritten, but the authority boundary
and state ownership remain the vision.

**Psyche:** Sema's long arc is more than persistence: structured language
data should eventually avoid strings for finite vocabularies, using typed
integer-backed identities that may later compile into real enums while
retaining their translator position. Long prose can remain string data for
now. This is not an MVP blocker.

### Adjacent-daemon type ownership

**Psyche:** Each language daemon carries strict types sufficient to store and
type the objects of the next daemon down the chain:

- Ethos knows Nomos transformer input schemas.
- Nomos knows the Logos objects it produces.
- Sema persists each daemon's own objects; Sema is not another mirrored
  language layer.

**Approved proposal:** A dedicated `nomos-types` repository holds pure
per-transformer data types shared by core-ethos and core-nomos. The Nomos
transformer trait and every transformer implementation remain in Nomos. The
shared repository contains no behavior.

**Psyche:** The mirror is hand-written for the bootstrap. The end state
authors these schemas once in Ethos and shares/generated that source for both
Ethos and Nomos, eliminating repetition at its source.

### Identity and editing horizon

**Psyche:** Names have three layers:

- true name: content address, changing with content;
- encoded name: stable identity/slot reference;
- visible name: freely changeable human projection.

Imports and visible spellings do not carry encoded identity. Encoded objects
reference absolute encoded names; the registry maps encoded identity to the
current true name in content-addressed storage.

**Psyche:** Changes enter through an operation interface as atomic operations.
One operation may affect many objects and all cascaded transformer outputs,
but either all effects commit or none do. Daemons hold encoded forms in slots;
their change logs are the VCS. Text editing is the bootstrap route: the engine
derives an operation from the old/new encoded diff, using an LLM only where
the textual diff is ambiguous.

**Psyche:** A capsule is a program or library, the content required to produce
one compiled artifact. It is not a source file or namespace. Text rendering
may distribute one capsule across balanced files; imports and exports are
derived views.

## Transformation and generation

**Psyche:** Nomos performs typed encoded-form to encoded-form conversion.
There is no string templating, string introduction, or string reading inside
Ethos-to-Logos transformation. A template means a typed Logos skeleton with
typed future/value positions, never a text template.

**Psyche:** Nomos exists so transformations themselves can be authored and
changed in the Nomos language. If Nomos never becomes a real language and the
transforms stay hand-written forever, the engine has failed its purpose.

**Psyche:** Nomos must be able to reason over the whole Ethos payload, not
only one local declaration. Cross-declaration, compiler-grade analysis must
remain possible. Dependencies are still a DAG and evaluate topologically.

**Psyche:** Logos is ordinarily generated from Ethos through Nomos. Directly
authored Logos is allowed for inspection or testing, but is not the normal
source path. Logos is fully explicit. `rust-logos` transcribes Logos through
the family TextualForm machinery; FFI facilities belong at the Logos layer.

**Approved proposal with limited authority:** The earlier Template(X)
computed-twin experiment was authorized so the psyche could inspect concrete
code, not endorsed as permanent architecture. The 2026-08-04 strict-type and
one-type-per-transformer rulings control wherever old Template(X) carriers or
generic field/application nodes conflict.

## Stream vision

**Psyche:** Initiating a stream requires a query, and successful establishment
must produce a response. A special stream section is probably unnecessary.

**Approved proposal / psyche refinement:** The successful response is the
established stream object itself, `Stream<Event>`, rather than a separate
grant wrapper. The input type is named `StreamInitiation`; the symmetric close
input is `StreamTermination`. Termination is therefore an input operation,
not merely an in-process method on the returned object.

The lifecycle for MVP is:

1. A typed `StreamInitiation` query is sent through an ordinary transformer
   application.
2. Success returns a typed `Stream<Event>` object; refusal is typed like any
   other failed operation.
3. Typed events flow through the established object.
4. A typed `StreamTermination` closes the established stream.

**Delegated:** Agents choose the minimal provisional fields of
`StreamInitiation`, `StreamTermination`, and `Stream<Event>` needed for the
MVP. The design must be concrete and reviewable later. At minimum, it must
carry whatever typed identity is required to route events and terminate the
same established stream. It must not reintroduce a generic transformer node.

## Confirmed MVP boundary

**Psyche, confirmed in the current Codex conversation:** MVP is complete when
Spirit runs through the redesigned generated Protos stack and demonstrates a
live Stream lifecycle plus persisted restart.

The concrete finish line is therefore:

- Spirit interface, nexus, and Sema contracts are consumed through the
  redesigned generation path.
- The real guardian/admission path works.
- A record can be admitted and queried.
- Stream establishment returns a live `Stream<Event>`.
- At least one real Spirit event is delivered.
- Termination closes the stream through `StreamTermination`.
- Spirit restarts and persisted data remains queryable.

Mind, orchestrator/messenger conversion and renames, full projection-profile
work, tree-sitter, and ScopeOf remain later work. They belong to the broader
epic, not the MVP critical path.

## Slice path to MVP

The critical path is narrower than "close every child of `primary-xqb`".

### 1. Co-design `primary-xqb.1` and `primary-0l8`

Treat syntax and encoded representation as one vertical design act. Start by
enumerating every current encoded form and replacing catch-all carriers with
strict semantic types. Land the family-wide syntax in Dotos and Ethos together
with those types:

- accept curly strings, angle quality/application syntax, pickup by use, and
  `.(...)` transformer applications;
- reject parenthesized strings, every pipe-text form, and bare-pipe
  transformers;
- preserve encoded-value round trips rather than source bytes;
- update fixtures across every affected family surface, not only the two
  repositories named in the bead title;
- compile a real Logos-to-Rust witness rather than stopping at codec tests.

The `primary-xqb.4` traits directive applies during every touched repository,
but does not block this slice. Add trait-migration notes when placement is not
obvious and continue.

### 2. Pull the minimum `primary-xqb.7` emission support into the witness

Generic/quality fixtures cannot prove the full vertical path if rust-logos
falls back to `T`, `Ord`, `Vec`, and `String` throughout the concept layers.
Implement at least the correctNaming table entries exercised by the first
vertical fixtures. The rest of the table can grow without blocking MVP.

The Beads graph currently does not make `xqb.7` block the vertical syntax
slice; behaviorally it is a dependency of any witness that emits the new
generic naming semantics.

### 3. Implement `primary-xqb.2`

After the strict-type architecture is stable, create `nomos-types` with pure
per-transformer types. Both core-ethos and core-nomos consume them. Keep the
transformer trait and implementations in Nomos. Do not add a behavior layer or
generic application envelope to the shared crate.

### 4. Implement and strengthen `primary-xqb.3`

Design the provisional minimal stream carrier, then prove it through Ethos,
Nomos, Logos, emitted Rust, and runtime behavior. The current bead acceptance
only requires types to compile and be consumed. The confirmed MVP requires a
stronger proof: establishment, one event, and termination end to end, with no
deferred constructs on that path.

### 5. Land `primary-vq6.8` as the MVP integration slice

Use Spirit as the first real component. Rebuild its generated contracts on the
new syntax/types, preserve the real guardian/judge behavior, exercise live
streaming, and prove restart persistence in its Sema database.

The old Spirit manual-re-entry/no-migration wording is superseded for the
actual Spirit v13-to-v14 cut by the completed surface-removal migration work.
Do not regress that current store. Runtime compatibility machinery remains out;
offline migration history is not a compatibility adapter.

### 6. Continue the broader epic after MVP

- `primary-xqb.5`: full token-lean and human-pretty projection profiles.
- `primary-xqb.6`: tree-sitter/editor support.
- `primary-vq6.9`: Mind contracts.
- `primary-vq6.10` and `.12`: orchestrator/messenger contracts and renames.
- `protos-engine-po2.7`: ScopeOf as the first complex transformer.
- `protos-engine-po2.8`: enriched-generation class migration.
- database-evolution and Sema dissolution infrastructure where still open.

## Supersessions implementers must remember

- The six-slot Ethos root and any migration bridge are dead.
- `Name|Transformer.{...}` and all bare-pipe forms are dead.
- Parenthesized strings and `(| |)` / `[| |]` strings are dead.
- The 2026-08-03 rejection of dotted transformer chains is superseded by the
  distinct, token-cheaper `Name.Transformer.(...)` form. Parentheses, not
  angles or braces, mark transformer payloads.
- A generic `TransformerApplication` encoded node is dead; each transformer
  has its own type.
- The old universal/generic `Vec<Fields>` representation is dead.
- The old belief that every `<...>` use is a Rust-style generic is refined:
  angles are the single quality/application surface; Shape and Trait resolve
  differently in the Protos ontology.
- Generic pickup does not have a separate parameter head. Repeated bare trait
  mentions now co-refer; older position-distinguishes-same-trait text is
  superseded.
- A capsule is a program/library, not a file or namespace.
- Central `sema-storage` is dead; each daemon owns a Sema database.
- Existing code and completed old slices are historical evidence, not binding
  abstractions. Goals unrelated to the redesign remain goals.
- The technical statement about training future models is design-log matter,
  not Spirit. No Spirit capture was authorized.

## Explicit non-goals and boundaries

- No compatibility support for superseded syntax.
- No source-byte round-trip preservation.
- No string manipulation inside Nomos transformation.
- No parser dependency on a Nomos transformer lookup table; syntax marks the
  application structurally, schemas type the payload.
- No generic transformer/application carrier.
- No central Sema daemon.
- No lazy/fixpoint machinery for dependency cycles.
- No mass trait refactor that blocks delivery.
- No monorepo consolidation; protos-engine remains the assembly/integration
  sink, not a source monorepo.
- No requirement to finish full projection profiles, tree-sitter, ScopeOf,
  Mind, or orchestrator/messenger before the Spirit MVP.
- No need to settle the no-strings end state, database-evolution engine, or
  self-hosting Nomos before the first MVP.

## Remaining open or deliberately delegated matters

- **Delegated:** exact provisional Stream input/output fields.
- **Unresolved:** encoded-name minting from first-version true name versus a
  random stable value.
- **Unresolved:** the name and exact role of the per-object sub-unit beneath a
  capsule.
- **Unresolved representation detail:** how concrete authored type arguments
  are represented inside the compact `Quality.[Shape Trait]` account.
- **Unassigned:** `«»` has no grammar slot.
- **Matter:** the complete correctNaming table can grow from the minimum
  exercised mappings.
- **Later design:** exact self-hosting replacement for every handwritten
  Ethos/Nomos and Nomos/Logos mirror.

None of these should stop the first syntax/strict-type slice unless concrete
code proves that the choice changes a public semantic contract. Routine
choices are to be made elegantly, recorded close to the code or in the
trait-migration/design note appropriate to them, and carried forward.
