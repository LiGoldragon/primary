# 194 — Operator reading: NOTA and schema as one restacked language system

User prompt source: forwarded designer prompt on 2026-05-26 after
reports 349 and 350. This report is the operator-side representation
of that prompt, with the capture gap filled through Spirit records
740-745.

## Capture status

Designer had already captured the delimiter-to-section rule, macro
shape-dispatch, and the current two-socket permission stance in Spirit
records 737-739. The forwarded prompt added stronger restack material
that was not yet represented in the recent records, so I gap-filled it
as records 740-745:

- NOTA itself should eventually have a schema.
- NOTA is the delimiter-based embedded language; schema gives context
  and meaning.
- Schema compiles into reusable precompiled libraries with an
  implicitly loaded core namespace.
- A schema daemon or schema agent resolves and caches assembled schema
  material.
- Schema is an ordered representation of data as stored.
- Schema macros are the basis for domain-specific actor/component
  interaction languages.

## The big shape

The design is no longer "NOTA parser here, schema parser there, Rust
macro somewhere else." The emerging stack is one continuous lowering
pipeline:

```text
NOTA text
  -> delimiter object tree
  -> schema macro expansion passes
  -> AssembledSchema
  -> Rust code composer
  -> component wire/runtime/storage/query types
```

NOTA is the substrate language. Schema is the interpretation layer that
tells a NOTA object tree what it means in a particular domain. The Rust
composer is then just a projection from a fully structured
`AssembledSchema`, not an independent old macro system that re-parses
a text DSL.

That means `emit_schema!` should ultimately operate on typed schema
data, not on legacy `signal_channel!`-style token bodies. The macro is
not a string templater. It is a Rust code composer whose input is an
assembled tree of types, endpoints, namespace imports, headers,
payloads, replies, and upgrade relationships.

## Four layers

### 1. Generic NOTA object pass

The first pass must not know schema semantics. It only identifies the
NOTA object structure:

```text
Atom       -> bare token / scalar-like text
(...)      -> parenthesized record-like object
[...]      -> sequence, struct field vector, or bracket string source
{...}      -> key-value map / namespace object
```

This is what the new `schema::object_pass` starts doing. It preserves
root order, delimiter kind, object paths, positions, and namespace
prefix. It intentionally avoids deciding "this is a struct" or "this
is an enum" too early.

### 2. Authored schema interpretation

Schema then assigns meaning to those NOTA shapes by position and
context.

Current best operator reading of the delimiter discipline:

- Parentheses are for enum and variant forms.
- Square brackets are for struct field vectors, ordered bodies, and
  string-derived token vectors.
- Curly braces are for user-defined namespace maps: name to definition.

Example namespace map:

```nota
{
  Topic [String]
  Topics [(Vec Topic)]
  Entry [Topics Kind Description Magnitude]
  Kind (Decision Principle Correction Clarification Constraint)
  Observation (State (Records RecordQuery) Topics Questions)
}
```

The map key gives the local type name. The value is a type definition.
No field names are written. A struct field name is derived from the
field type name when Rust is emitted. If a field needs a different
name, the schema needs a more specific type name, normally a newtype.

### 3. Macro expansion into AssembledSchema

Schema has macro-like nodes. A macro is a typed schema object that
owns its own recognizer and lowering rule. The macro does not introduce
a second text syntax; it interprets NOTA shapes by delimiter, arity,
case, and position.

Expansion is multi-pass:

```text
load object tree with built-in macros
  -> expand recognized schema nodes
  -> resolve imports and namespace references
  -> discover any newly available macros
  -> repeat until no macro nodes remain
  -> emit AssembledSchema
```

`AssembledSchema` is the long form: every imported name resolved,
every type fully qualified, every enum/struct/newtype explicit, every
header route derivable, and every generated Rust module boundary known.

The authored schema is the short, design-facing form. The assembled
schema is the typed compiler-facing form.

### 4. Rust emission and runtime use

Rust generation should happen only after the assembled tree exists.
That emission can create:

- ordinary signal types;
- owner signal types;
- daemon configuration records;
- request/reply/event/filter types;
- short-header encoders and dispatch triage;
- schema version hashes;
- upgrade implementations where the schema diff is mechanically known;
- hooks for hand-written upgrade methods where the diff is ambiguous.

The schema defines data. Effects, fan-out, and dispatch tables do not
belong as user-authored schema sections. Runtime logic may derive or
cache helper structures from schema, but authored schema files should
not carry a `Features` surface.

## NOTA itself needs a schema

The new restack pushes schema all the way down:

```text
nota-core.schema
  defines Atom / Record / Sequence / Map / String forms

schema-core.schema
  defines SchemaFile / Import / Export / Namespace / Struct / Enum /
  Newtype / MacroNode / AssembledSchema input types

component.schema
  defines the component's actual signal/owner/sema surfaces using
  schema-core's primitives
```

This cannot be self-hosting on day one. There is a bootstrap layer:
hand-written Rust definitions for the minimal NOTA object tree and the
minimal schema macro engine. Once that exists, the schema for NOTA and
schema can be represented in the system and checked against the
hand-written bootstrap.

The target is self-description without pretending the bootstrap does
not exist.

## Schema daemon / schema agent

The prompt introduces an important runtime role: schema material should
be resolvable, cached, and shareable.

The schema daemon or schema agent would own:

- the implicit core namespace;
- built-in macro definitions;
- precompiled schema libraries;
- imported schema resolution;
- assembled schema cache;
- namespace lookup;
- schema version hashes;
- maybe later, schema-diff and upgrade-plan derivation.

The immediate operator reading is: start this as a library cache in the
schema crate, then graduate it into a daemon when multiple components
need live resolution. The daemon shape is real, but the MVP does not
need IPC just to prove the compiler path.

## Standard schema parts

The prompt is still exploring this, but the rough standard object
shape is:

```text
specification / imports / exports / namespace sharing
input / receive surface
output / give surface
```

Each may have header implications, but the header should usually be
derived from the assembled schema rather than authored redundantly.
Where the authored file does need a route-selector surface, it should
still be data-shaped and delimiter-honest, not a special text DSL.

The important constraint: schema files can be split by kind. We do not
need one monolithic file that carries ordinary signal, owner signal,
sema projection, storage, daemon config, and upgrade rules all at once.
Per-file parsing keeps root object positions meaningful.

For Spirit, a plausible split is:

```text
spirit-signal.schema        ordinary socket
spirit-owner.schema         owner socket
spirit-sema.schema          command/outcome classification
spirit-storage.schema       persisted data shape
spirit-config.schema        daemon single-argument config
```

Those files can import shared local and core namespaces. The assembled
component view can still combine them later.

## Header and namespace ranges

The prompt reopens root variant numbering. Rust can assign enum
discriminants explicitly, and schema can reserve ranges for high-level
spaces.

Operator reading:

```text
root byte / root variant
  0..N       ordinary receive / query / command space
  N..M       response / reflection space
  M..K       owner or permissioned space if encoded in-band
```

The user used the image of solar/lunar: query as solar, response as
reflection. I would not bake those words into code yet, but the
structural point is strong: schema can reserve numeric namespaces so a
64-bit short header can triage without decoding the full payload.

Current implementation should keep separate ordinary and owner sockets.
The permission split can still be represented in schema data, but file
system socket permissions remain the active access-control mechanism.

## Inline NOTA as a programming interface

The quote-free NOTA discipline matters here. Because NOTA strings use
brackets, a whole NOTA object can live inside double quotes in shell,
Rust strings, JSON strings, Nix strings, etc. That makes it suitable
as an inline agent/programming interface:

```sh
spirit "(Record ([schema nota] Principle [NOTA can live inline inside double quotes] Maximum))"
```

Schema gives that inline value meaning. The same delimiter language
can be embedded in component CLIs, tests, macro invocations, examples,
and eventually agent-to-agent messages.

This is why NOTA and schema should not drift apart. NOTA is the compact
object notation; schema is the strict meaning system that turns those
objects into typed interfaces.

## Where current code stands

Implemented now in the operator schema worktree:

- `SchemaObjectPass` parses schema text as generic NOTA object trees.
- It preserves delimiter, root order, object position, object path, and
  file-derived namespace prefix.
- Existing `multi_pass` readers now start from that object pass and
  adapt into the older six-position reader.
- Cargo tests and Nix flake checks pass.

Still not done:

- the old authored `Feature` variants remain in parts of the POC code;
- `AssembledSchema` is not yet the complete long-form intermediate;
- NOTA itself does not yet have a schema;
- schema-core does not yet define the built-in macro object types;
- there is no schema daemon/cache yet;
- Spirit is not yet fully generated from the schema restack.

## Operator critique

The strongest part of the prompt is the insistence that schema parsing
starts with delimiter objects, not a bespoke schema grammar. That
prevents the old failure mode: every layer invents a nearby syntax and
then the system has three half-compatible parsers.

The second strongest part is "schema as ordered storage truth." If
schema is allowed to become a friendly unordered config language, it
loses the migration and header benefits. The authored form can be
beautiful, but it must stay close to layout, order, and discriminants.

The risky part is scope. Pulling NOTA itself, schema-core, component
signals, upgrade derivation, and schema daemon cache into one immediate
implementation would sprawl. The right implementation order is:

1. Finish the generic object pass and shape predicates.
2. Define hand-written `AssembledSchema` Rust types.
3. Define `schema-core` authored examples against those types.
4. Make `emit_schema!` consume assembled schema only.
5. Prove one Spirit surface end-to-end.
6. Only then introduce schema daemon resolution/cache.

## Immediate next operator slice

The next clean implementation target is not "full schema daemon." It
is:

```text
object_pass
  -> schema_core recognizers
  -> AssembledSchema structs/enums
  -> emit_schema! from AssembledSchema
  -> one Spirit signal surface generated and tested
```

That slice keeps the design honest, removes the drifted Features
surface, and gives a concrete place for NOTA/schema self-description to
attach.

The main constraint to add as tests: schema code must demonstrate it is
using the object pass and assembled schema path directly. A test should
fail if a schema file is parsed by an old text-body macro route or if
authored `Feature` sections are accepted.
