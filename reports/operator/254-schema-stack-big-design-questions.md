# 254 — Schema Stack Big Design Questions

*Kind: design questions · Topics: schema, nota, asschema, macros, runtime · 2026-05-30 · operator lane*

## Frame

The stack now has enough running shape that the questions are no longer
"can this work at all?" They are now boundary questions: where one layer ends,
which nouns are privileged, what becomes data first, and what gets to stay
bootstrap code.

These are the questions I think matter most before the next large
implementation wave.

## 1. What Is The Smallest Privileged Core?

The system wants everything to be data, including macros and schema itself.
But there is always a first reader. The big question is what belongs in that
irreducible Rust bootstrap core.

My current answer:

```text
NOTA parser
Asschema bootstrap Rust types
Asschema NOTA/rkyv codec
small loader for MacroLibrary
```

Everything else should move out into serialized artifacts. The danger is
letting the bootstrap core grow every time a shape is inconvenient. If that
happens, "everything is data" becomes rhetoric while the real compiler hides
in Rust branches.

The decision I need from design: name the privileged core explicitly and treat
new additions to it as suspicious.

## 2. What Is The Exact Boundary Between NOTA, Schema, And Asschema?

The current boundary I believe in:

```text
NOTA      = delimiter/value structure + text/binary codec surface
Schema    = authoring language, type references, declarations, macro surface
Asschema  = macro-free canonical data model consumed by emitters
```

The question is whether that boundary is accepted strongly enough to remove
all old syntax and old explanations.

Examples:

- `[]` is a vector value, not a type declaration.
- `(Vec Entry)` is Schema type-reference vocabulary, not a NOTA keyword.
- `Entry@{ @Topics @Kind }` is authored Schema sugar.
- `(Public Entry (Struct { topics Topics kind Kind }))` is assembled data.

The risk is syntax drifting back into mixed explanations: sometimes brackets
mean value, sometimes declaration, sometimes convenience. That is how the
stack becomes unreadable again.

## 3. How Powerful Are User Macros Allowed To Be?

User-declared macros are the hardest design frontier. If macros are too weak,
schema authors cannot create the domain languages you want. If macros are too
strong, schema expansion becomes a hidden programming language with all the
usual problems: nontermination, hygiene, unclear imports, and reader-locality
loss.

My preferred first version is deliberately constrained:

```text
MacroDefinition =
  name
  accepted position
  structural pattern enum
  typed expansion enum
```

No raw string templates. No arbitrary code. No recursive macro execution until
the macro data model can express and test recursion explicitly.

The big question: do we accept a small typed macro algebra first, then grow it,
or do we try to design the full macro language now?

## 4. What Is The Public Artifact Set Of A Schema Crate?

Right now I think every schema-bearing crate should eventually expose these
files:

```text
schema/lib.schema       authored source
schema/lib.asschema     assembled NOTA artifact
src/schema/lib.rs       emitted Rust
```

Maybe `.asschema.rkyv` is generated cache rather than checked in. The text
`.asschema` should probably be checked in because it is reviewable and proves
the middle layer exists.

The big question: is `schema/lib.asschema` a committed review artifact for
every crate, or only a generated build artifact?

My operator instinct is: commit the text artifact, generate the binary
artifact.

## 5. What Is The Crate Topology?

The stack is pulling toward more crates:

```text
nota-next
schema-next
schema-rust-next
schema-core-next
spirit-next
signal-spirit-next
owner-signal-spirit-next
spirit-next-engine
spirit-next-daemon
spirit-next-cli
```

The current single-crate `spirit-next` is useful because it proves the whole
chain with fewer moving parts. The cleaner long-term shape is workspace or
repo split by contract/runtime/client responsibility.

The big question: when does the running proof stop benefiting from a single
crate and start suffering from it?

My current answer: after checked-in `.asschema` and schema-core imports land.
Before that, splitting crates multiplies moving parts while the substrate is
still settling.

## 6. What Is Universal Core Support Versus Component Local Data?

Mail support is currently emitted locally. But nouns like these feel
universal:

```text
MessageIdentifier
OriginRoute
MessageSent
MessageProcessed
Signal<T>
Nexus<T>
Sema<T>
Plane
```

The question is where the line falls. If too much goes into schema-core,
component schemas become anemic. If too little goes into schema-core, every
component emits local copies of the same protocol vocabulary and import
discipline never gets exercised.

My current line:

- schema-core owns universal transport/lifecycle/envelope nouns;
- component schemas own domain operations and payloads;
- generated aliases make imports visible in `src/schema/lib.rs`.

## 7. What Is The Runtime Authority Of Asschema?

Asschema currently drives Rust generation. It could also become runtime
introspection data: a daemon could know its own schema, report it, compare it
to incoming messages, and expose upgrade/diff information.

The question: is `AsschemaArtifact` only a build-time compiler artifact, or is
it also a runtime object that daemons carry?

My instinct: both, but with different surfaces. Build-time asschema emits
Rust. Runtime asschema is metadata carried by the component for
introspection, compatibility checks, and upgrade planning. The daemon still
does not parse NOTA; it can carry binary `.asschema.rkyv`.

## 8. How Does Upgrade Become Real Without Becoming Ceremony?

The generated upgrade traits should not exist everywhere. They should appear
only when a typed diff says a noun changed.

The question is how strict the first version should be:

```text
old.asschema + new.asschema -> SchemaDiff -> UpgradePlan -> emitted traits
```

Do we require every schema version bump to produce a checked `SchemaDiff`
artifact immediately, or only once there is persisted data to protect?

My answer: start when `schema/lib.asschema` is checked in. From that point,
versioned artifacts exist and diffing becomes natural.

## 9. How Much Of Rust Emission Should Be Data Before More Runtime Work?

The runtime is already useful. But the emitter is still too string-heavy. The
big question is whether to pause runtime growth until `RustModule` exists.

My answer: do `RustModule` before the next major runtime feature. Otherwise
every new generated trait, support noun, or plane module makes the string
emitter harder to replace later.

Small runtime fixes can continue. Big runtime expansion should wait for
`RustModule`.

## 10. What Is The First Self-Hosting Milestone?

"Schema defines schema" is too large unless it has a first concrete milestone.
My preferred first milestone:

```text
Asschema's own type model is represented as schema/lib.asschema
schema-rust-next emits the same bootstrap Rust model from that artifact
the emitted model compiles in a fixture crate
```

This does not require deleting the bootstrap Rust types yet. It proves the
loop in parallel first.

The big question: is the first self-hosting milestone "emit the current
Asschema model from its own artifact" or "read the schema authoring language
using schema-defined macros"? I would do Asschema first; it is smaller and
more foundational.

## My Priority Stack

The questions collapse into one implementation order:

```text
1. commit .asschema text artifacts
2. add RustModule data model
3. define MacroLibrary as typed serialized data
4. extract schema-core support nouns
5. add SchemaDiff / UpgradePlan
6. split spirit-next once imports and artifacts are stable
7. close first self-hosting loop
```

The biggest design call is not syntax now. It is discipline: every new layer
must have a serialized data artifact before the next layer is allowed to hide
behind it.

