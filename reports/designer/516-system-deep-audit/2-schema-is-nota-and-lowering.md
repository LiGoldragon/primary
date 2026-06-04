---
title: "Schema is NOTA, and lowering to Asschema"
role: designer
variant: Psyche
date: 2026-06-04
topics:
  - schema-next
  - nota
  - asschema
  - lowering
  - schema-derived-stack
  - spirit
  - signal-spirit
---

# Schema ↔ NOTA: a `.schema` is NOTA, and lowering it to Asschema

This is mechanism report #2 of the deep audit of the schema-derived
stack. Its single claim, stated plainly and then proven by running
real code:

> A `.schema` file is **itself a NOTA document** — positional records,
> bracket strings, no flags, no keywords. `schema-next` **lowers** that
> source-form NOTA into a second NOTA document, the `.asschema`, which
> is **ordered, macro-free, and fully explicit**. The `.asschema` is the
> derived artifact the rest of the stack consumes; the `.schema` is what
> a human writes.

Every code block below is either (a) a file you can open at the path
named, or (b) the verbatim stdout of a command named with its working
directory. Where I could not run something, I say so explicitly.

## 1. The two languages are the same language

There is a temptation to think "schema language" is a separate DSL with
its own grammar. It is not. A `.schema` file is parsed by exactly the
same `nota_next::Document::parse` that parses any NOTA string. The
schema layer is a *reading* imposed on a generic NOTA document, not a
new tokenizer. You can see this directly in the source-form reader,
`schema-next/src/source.rs`:

```rust
pub fn from_schema_text(source: &str) -> Result<Self, SchemaError> {
    let document = Document::parse(source)?;
    Self::from_document(&document)
}
```

`Document::parse` is the NOTA parser. The schema rules — "the first
block is imports, the second is the input enum, …" — are applied *after*
the document already exists as generic NOTA. That is the whole point of
the architecture: there is one syntax (NOTA), and "schema" is one
positional shape within it.

This is why every CLAUDE.md/AGENTS.md rule about NOTA applies verbatim
to `.schema` files: records are **positional, not labeled** (type head
first, then fields in declared order, no `key value` keywords); strings
come **exclusively from bracket forms** (`[Text]`, `[Integer]`), never
quotation marks; and there are **no flags**. A `.schema` is not
"NOTA-like." It is NOTA.

## 2. The three-block root struct (plus an optional fourth)

A schema's root document is a fixed positional shape. The canonical
small example is `signal-spirit/schema/signal-spirit.schema`, whose own
header comment documents the shape. Here is the file verbatim
(`/git/github.com/LiGoldragon/signal-spirit/schema/signal-spirit.schema`):

```
;; signal-spirit.schema — minimum one-operation wire contract for the
;; running-spirit-concept designer track. Per /368 + psyche 2026-05-26
;; record 845: the goal is end-to-end communication for ONE operation
;; through the schema-derived stack, NOT v0.3 capability parity.
;;
;; Three-section root struct per records 805 / /361:
;;   block 1 ({}) — imports / exports (empty here; no external bindings)
;;   block 2 ([]) — Input + Output surface declarations
;;   block 3 ({}) — namespace of user-defined types
;; ...
{}
[
  (Input (Record Entry))
  (Output (RecordAccepted RecordIdentifier))
]
{
  Topic [Text]
  Description [Text]
  RecordIdentifier [Integer]
  Entry [Topic Description]
}
```

The exact arity rule is enforced in `SchemaSource::from_document`
(`schema-next/src/source.rs`):

```rust
pub fn from_document(document: &Document) -> Result<Self, SchemaError> {
    if !matches!(document.holds_root_objects(), 3 | 4) {
        return Err(SchemaError::ExpectedRootObjectCount {
            expected: "3 root values (input output namespace) or 4 with leading imports",
            found: document.holds_root_objects(),
        });
    }

    let (imports, input_index, output_index, namespace_index) =
        if document.holds_root_objects() == 4 {
            (SourceImports::from_block(document.root_object_at(0)?), 1, 2, 3)
        } else {
            (SourceImports::empty(), 0, 1, 2)
        };
    // ... input = root_object_at(input_index), output = ..., namespace = ...
}
```

So the load-bearing shape is:

| Root position | Block | Meaning | NOTA delimiter |
|---|---|---|---|
| (optional) 0 | imports | external type bindings (`Import`/`Export`) | `{ }` map |
| input | input enum | the operation roots a client may *send* | `[ ]` enum |
| output | output enum | the reply roots the daemon may *return* | `[ ]` enum |
| namespace | namespace | every user-defined type the two enums reference | `{ }` map |

There are exactly **three required blocks** (input, output, namespace),
with imports as an optional leading fourth. This is what "three-block
root struct" means.

### The same shape in the real signal schema

`spirit/schema/signal.schema` is the full daemon contract and shows the
shape at scale. Verbatim head
(`/git/github.com/LiGoldragon/spirit/schema/signal.schema`):

```
{}
[Record Observe Lookup Count Remove LookupStash]
[RecordAccepted RecordsObserved RecordsStashed RecordFound RecordsCounted RecordRemoved Error Rejected]
{
  SourcePath String
  ...
  Record Entry
  Observe Query
  ...
  Entry { Topics * Kind * Description * Magnitude * Privacy * }
  Query { TopicMatch * kind (Optional Kind) privacy_selection PrivacySelection }
  ...
  Kind [Decision Principle Correction Clarification Constraint]
  Magnitude [Zero Minimum VeryLow Low Medium High VeryHigh Maximum]
}
```

Notice the two enum blocks here use the *bare-name* form
(`[Record Observe …]`) — the payload binding for each variant
(`Record Entry`, `Observe Query`) is declared down in the namespace
block, rather than inline as `(Record Entry)`. Both forms are legal
source; `signal-spirit.schema` uses the inline `(Record Entry)` form,
`signal.schema` uses the split form. **The lowering normalizes both to
the same explicit Asschema** — that normalization is exactly what we
prove next.

## 3. What "lowering" is, and proving it runs

Lowering is the function `SchemaEngine::lower_source(source_text,
identity) -> Asschema`. It takes the human-written source NOTA and
produces the explicit Asschema NOTA. The engine is the same one the
spirit daemon's `build.rs` calls; it is also exercised directly by the
`schema-next` example `examples/emit_artifacts.rs`:

```rust
let core_source = include_str!("../schemas/core.schema");
let core_asschema = SchemaEngine::default()
    .lower_source(core_source, SchemaIdentity::new("schema-next:core", "0.1.0"))
    .expect("core schema lowers");
println!("{}", core_asschema.to_nota());
```

### 3a. The test suite passes

Command run, in `/git/github.com/LiGoldragon/schema-next`:

```
$ ~/.nix-profile/bin/cargo test
```

Verbatim per-binary results (every test binary, no failures):

```
   Finished `test` profile [unoptimized + debuginfo] target(s) in 0.06s
     Running unittests src/lib.rs
test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
     Running tests/asschema_definition.rs
test result: ok. 8 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
     Running tests/big_examples.rs
test result: ok. 3 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
     Running tests/collections.rs
test result: ok. 13 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
     Running tests/design_examples.rs
test result: ok. 13 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
     Running tests/lowering.rs
test result: ok. 22 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
     Running tests/macro_exploration.rs
test result: ok. 14 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
     Running tests/operator_271_closed_claims.rs
test result: ok. 9 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
     Running tests/raw_core_schema.rs
test result: ok. 6 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
     Running tests/resolution.rs
test result: ok. 7 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
     Running tests/source_codec.rs
test result: ok. 4 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
     Running tests/symbol_path.rs
test result: ok. 5 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
     Running tests/syntax_layer.rs
test result: ok. 7 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
     Running tests/upgrade_pilot.rs
test result: ok. 5 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
   Doc-tests schema_next
test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

The directly relevant binary is `tests/lowering.rs` — **22 passed**.
Its first test, `lowers_spirit_schema_into_ordered_asschema`, lowers
`schemas/spirit-min.schema` and asserts the namespace comes out in a
specific *order* (`Topic, Topics, Description, RecordIdentifier, Entry,
Query, RecordSet, Kind, Magnitude`). Ordering is a deliberate property
of the artifact — see §5.

### 3b. A live lowering, source and output side by side

Command run, in `/git/github.com/LiGoldragon/schema-next`:

```
$ ~/.nix-profile/bin/cargo run --example emit_artifacts
```

The relevant stdout section, verbatim (the `=== core.asschema ===`
block printed by `core_asschema.to_nota()`):

```
=== core.asschema ===
(schema-next:core [0.1.0])
[]
[]
[]
[]
[(Public CoreSchema (Struct (CoreSchema {builtin_macro_positions (Plain BuiltinMacroPositions) ...
```

That output is **byte-identical** to the checked-in
`schema-next/schemas/core.asschema`, which I read independently. The
lowering is deterministic: the same source always produces the same
artifact. (Full `core.schema` source and `core.asschema` output are at
those two paths; the side-by-side I walk through in detail below uses
the smaller, daemon-real `signal` pair, §4.)

## 4. The real `.schema` and `.asschema`, side by side

This is the heart of the report: the spirit signal contract before and
after lowering. Both files are checked into the spirit repo and are kept
fresh by the daemon build (proven in §6).

### INPUT — `spirit/schema/signal.schema` (source NOTA, human-written)

```
{}
[Record Observe Lookup Count Remove LookupStash]
[RecordAccepted RecordsObserved RecordsStashed RecordFound RecordsCounted RecordRemoved Error Rejected]
{
  SourcePath String
  LocalPath String
  PublicPath String
  Import { SourcePath * LocalPath * }
  Export { LocalPath * PublicPath * }
  SignalReuse { Import * Export * }

  Record Entry
  Observe Query
  Lookup RecordIdentifier
  Count Query
  Remove RecordIdentifier
  LookupStash StashHandle

  RecordAccepted SemaReceipt
  ... (output payload bindings) ...

  Topic String
  Topics (Vec Topic)
  ...
  RecordIdentifier Integer
  ...
  DatabaseMarker { CommitSequence * StateDigest * }
  SemaReceipt { RecordIdentifier * DatabaseMarker * }
  ...
  ValidationError [EmptyTopic EmptyDescription EmptyQueryTopic StashHandleNotFound]
  ...
  Entry { Topics * Kind * Description * Magnitude * Privacy * }
  Query { TopicMatch * kind (Optional Kind) privacy_selection PrivacySelection }
  Records (Vec Entry)
  RecordSet (Vec Entry)
  Kind [Decision Principle Correction Clarification Constraint]
  Magnitude [Zero Minimum VeryLow Low Medium High VeryHigh Maximum]
}
```

(Full file is 71 lines; I have elided the middle of the namespace with
`...` for readability — the complete source is at
`/git/github.com/LiGoldragon/spirit/schema/signal.schema` and I read all
71 lines of it.)

### OUTPUT — `spirit/schema/signal.asschema` (lowered NOTA, machine-written)

Verbatim head, line by line
(`/git/github.com/LiGoldragon/spirit/schema/signal.asschema`):

```
(spirit:signal [0.1.0])
[]
[]
[(Record (Some (Plain Record))) (Observe (Some (Plain Observe))) (Lookup (Some (Plain Lookup))) (Count (Some (Plain Count))) (Remove (Some (Plain Remove))) (LookupStash (Some (Plain LookupStash)))]
[(RecordAccepted (Some (Plain RecordAccepted))) (RecordsObserved (Some (Plain RecordsObserved))) ... (Error (Some (Plain Error))) (Rejected (Some (Plain Rejected)))]
[(Public SourcePath (Alias (SourcePath String))) ... (Public Entry (Struct (Entry {topics (Plain Topics) kind (Plain Kind) description (Plain Description) magnitude (Plain Magnitude) privacy (Plain Privacy)}))) (Public Query (Struct (Query {topic_match (Plain TopicMatch) kind (Optional (Plain Kind)) privacy_selection (Plain PrivacySelection)}))) ... (Public Kind (Enum (Kind [(Decision None) (Principle None) (Correction None) (Clarification None) (Constraint None)]))) (Public Magnitude (Enum (Magnitude [(Zero None) (Minimum None) ... (Maximum None)])))]
```

The full 6-line file is at the path above. Both files are still NOTA —
positional records, bracket strings, no quotation marks, no keywords.
The output is just NOTA that has been made *fully explicit*.

## 5. What lowering actually DID — the five transformations

Comparing the two artifacts side by side, lowering performed five
distinct jobs. Each is visible in the diff between source and output.

### (a) Root layout: 3-or-4 blocks IN, exactly 6 lines OUT

The source root is the 3-block (here 4-with-empty-imports) shape. The
Asschema is a fixed **six-part** structure, set by the `Asschema` struct
field order in `schema-next/src/asschema.rs`:

```rust
pub struct Asschema {
    identity: super::SchemaIdentity,          // line 1: (spirit:signal [0.1.0])
    imports: Vec<ImportDeclaration>,          // line 2: []
    resolved_imports: Vec<super::ResolvedImport>, // line 3: []
    input: EnumDeclaration,                   // line 4: [(Record ...) ...]
    output: EnumDeclaration,                  // line 5: [(RecordAccepted ...) ...]
    namespace: Vec<Declaration>,              // line 6: [(Public ...) ...]
}
```

So lowering *adds two pieces of front matter the source never carried*:
the **identity** `(spirit:signal [0.1.0])` (the crate name + version,
passed to `lower_source` as `SchemaIdentity::new("spirit", "0.1.0")`),
and a separate **resolved_imports** block. The source's single optional
imports `{}` becomes two explicit blocks: declared imports and resolved
imports. The "three-block source → six-line artifact" expansion is the
first thing lowering does.

This is the "root-vs-box layout" distinction. The **roots** — input and
output — are not stored as ordinary namespace types; they are their own
top-level `EnumDeclaration` blocks (lines 4 and 5), because they are the
operation/reply surfaces the wire protocol roots on. Everything else is
a `namespace` `Declaration` (line 6). A reference *into* a type is a
`Plain Name` leaf; a recursive container reference (`Vec`, `Optional`,
`Map`) is `Box`-ed in the Rust `TypeReference` enum
(`Vector(Box<TypeReference>)`, `Optional(Box<TypeReference>)`), because
those are the points where a type contains another type and the
in-memory tree needs indirection. Roots sit at the document root; nested
references sit behind a box. That is the root-vs-box layout.

### (b) Every variant payload made explicit: `(Some (Plain X))` / `None`

In the source, the input enum is just bare names: `[Record Observe Lookup
…]`, with payloads declared separately (`Record Entry`). In the Asschema,
each variant is a complete `EnumVariant { name, payload: Option<...> }`:

- `Record` (which had payload `Entry` in the namespace) → `(Record (Some (Plain Record)))`
- a payloadless variant → `(Variant None)`, e.g. `(Decision None)` in `Kind`.

Look at the `Kind` enum: source `Kind [Decision Principle Correction
Clarification Constraint]` lowers to `(Public Kind (Enum (Kind
[(Decision None) (Principle None) (Correction None) (Clarification None)
(Constraint None)])))`. The bare names gain an **explicit `None`
payload**. There is no implicit "this variant has no data" — lowering
makes the `Option` concrete.

### (c) Declaration KIND classified: Alias / Newtype / Struct / Enum

The source namespace mixes forms tersely. Lowering classifies each into
one of four explicit `TypeDeclaration` kinds, tagging each with its
visibility (`Public`):

| Source form | Lowered declaration |
|---|---|
| `Topic String` | `(Public Topic (Alias (Topic String)))` |
| `Topics (Vec Topic)` | `(Public Topics (Alias (Topics (Vector (Plain Topic)))))` |
| `Record Entry` | `(Public Record (Alias (Record (Plain Entry))))` |
| `Entry { Topics * Kind * … }` | `(Public Entry (Struct (Entry {topics (Plain Topics) kind (Plain Kind) …})))` |
| `Kind [Decision …]` | `(Public Kind (Enum (Kind [(Decision None) …])))` |
| single-field `{ X * }` | `(Newtype …)` (transparent wrapper; see `tests/lowering.rs::single_field_brace_declarations_lower_to_newtypes`) |

A bare reference becomes an `Alias`; a single-field brace becomes a
transparent `Newtype`; a multi-field brace becomes a `Struct`; a bracket
list becomes an `Enum`. The source author never wrote the words `Alias`,
`Struct`, `Enum`, or `Newtype` — lowering *derives the kind from the
shape*.

### (d) Struct fields named and reference-typed; `*` resolved

The source struct field shorthand `Entry { Topics * Kind * Description *
Magnitude * Privacy * }` uses the `*` marker, which means "derive the
field name from the type name." Lowering resolves each `*` into an
explicit `field_name (Plain TypeName)` pair, lowercasing the field name:

```
Entry { Topics * Kind * Description * Magnitude * Privacy * }
```
becomes
```
(Public Entry (Struct (Entry {topics (Plain Topics) kind (Plain Kind)
  description (Plain Description) magnitude (Plain Magnitude)
  privacy (Plain Privacy)})))
```

`Topics *` → `topics (Plain Topics)`. The star is the source's
field-name-equals-type-name macro; the Asschema spells out both the
field name (`topics`) and the typed reference (`(Plain Topics)`).
Where the source already named a field — `Query { TopicMatch * kind
(Optional Kind) privacy_selection PrivacySelection }` — that name is
carried through and the type is wrapped explicitly: `kind (Optional
Kind)` → `kind (Optional (Plain Kind))`. Note the `(Optional (Plain
Kind))`: the inner reference is wrapped in `Plain`, because `Kind` is a
declared name, not a reserved scalar.

### (e) Macro-free, canonically ordered output

The source uses shorthand macros: the `*` field-name star, the
bare-name enum lists, the `(Vec T)`/`(Optional T)` reference forms, the
`[Text]`/`[Integer]` scalar shorthands (in `signal-spirit.schema`). The
Asschema has **none of these as macros** — every one has been *expanded*
into its canonical explicit form. `(Vec Topic)` → `(Vector (Plain
Topic))`; `[Text]` → the reserved `String` scalar; `*` → an explicit
named field. And the declarations come out in a deterministic order
(asserted by `tests/lowering.rs::lowers_spirit_schema_into_ordered_asschema`).

The pithy summary of lowering: **source NOTA is terse and macro-rich for
humans; the Asschema is verbose and macro-free for machines.** Same
language, opposite ends of the explicitness spectrum.

## 6. Proving the daemon build regenerates the `.asschema` from the `.schema`

The `.asschema` is not hand-maintained — it is the lowering output,
checked in, and the daemon build *verifies* it stays fresh. The spirit
build script (`spirit/build.rs`) ends with:

```rust
GenerationDriver::new(plan)
    .generate()
    .expect("generate spirit schema artifacts")
    .write_or_check("SPIRIT_UPDATE_SCHEMA_ARTIFACTS")
    .expect("checked-in spirit schema artifacts are fresh");
```

`write_or_check` has two modes: with the env var set it **writes** the
lowered artifacts; without it, it **checks** the checked-in artifacts
match what lowering produces, and fails the build if they drifted.

I exercised both. Command run, in
`/git/github.com/LiGoldragon/spirit`:

```
$ sha256sum schema/signal.asschema schema/signal.schema
d6e4ce34b044ab268196d60ef4a706a6953ea2e428a5804e61f73fa0d2b340db  schema/signal.asschema
089f08df592e6d8bca4d9f2ebb517cb8757826bde0f196f962c0f8edba13cfdd  schema/signal.schema
```

Then the **regenerate** path:

```
$ SPIRIT_UPDATE_SCHEMA_ARTIFACTS=1 ~/.nix-profile/bin/cargo build
   Compiling schema-next v0.1.1 (https://github.com/LiGoldragon/schema-next.git?branch=main#b14d14f7)
   Compiling schema-rust-next v0.1.8 (https://github.com/LiGoldragon/schema-rust-next.git?branch=main#e7d5f395)
   Compiling spirit v0.1.0 (/git/github.com/LiGoldragon/spirit)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 4.42s
```

Re-hash after regeneration — **unchanged**, because lowering is
deterministic and the checked-in artifact was already the exact lowering
output:

```
$ sha256sum schema/signal.asschema schema/signal.schema
d6e4ce34b044ab268196d60ef4a706a6953ea2e428a5804e61f73fa0d2b340db  schema/signal.asschema
089f08df592e6d8bca4d9f2ebb517cb8757826bde0f196f962c0f8edba13cfdd  schema/signal.schema
```

Then the **check** path (plain build, no env var), after `touch`-ing the
source to force the build script to rerun:

```
$ touch schema/signal.schema && ~/.nix-profile/bin/cargo build
   Compiling spirit v0.1.0 (/git/github.com/LiGoldragon/spirit)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.68s
```

The plain build **succeeds**, which means the freshness check passed:
the checked-in `signal.asschema` is byte-for-byte the lowering of
`signal.schema`. That is the proof that the `.asschema` is the lowered
`.schema`, enforced on every daemon build.

## 7. Where the chain goes next (the rest of the stack, briefly)

This report's scope ends at the `.asschema`. For completeness of the
mental model, the artifact I just proved feeds one more lowering:
`schema-rust-next`'s `RustEmitter` reads the Asschema and emits Rust.
The spirit build leaves the evidence at `spirit/src/schema/signal.rs`,
whose first line I read:

```
// @generated by schema-rust-next
```

So the full deterministic chain is:

```
signal.schema  (human NOTA, terse, macro-rich)
   │  schema-next  SchemaEngine::lower_source
   ▼
signal.asschema  (machine NOTA, explicit, macro-free, ordered)
   │  schema-rust-next  RustEmitter::emit_file
   ▼
src/schema/signal.rs  (@generated Rust the daemon compiles)
```

The `.asschema` is the pivot: the last NOTA artifact, and the input to
code generation. (The `.asschema → .rs` leg is the subject of a separate
mechanism report; I name it here only to place this one in the chain.)

## What I could NOT run

Nothing in this report was guessed. Two honesty notes:

- I did **not** run the deployed `spirit` CLI in this report — it is not
  needed to prove the schema↔asschema↔lowering relationship, which lives
  entirely in `schema-next` and the spirit *build*, both of which I ran.
  The deployed-CLI behaviour is a different mechanism (the daemon
  answering signals), out of scope here.
- The `signal-spirit` repo has its own `build.rs` that lowers
  `signal-spirit.schema` via the same `SchemaEngine::lower_source`, but
  it writes the generated Rust to `$OUT_DIR` and does **not** check in an
  `.asschema` (its `schema/` dir holds only the `.schema`). I read its
  `build.rs` to confirm it uses the identical lowering entry point; I did
  not separately rebuild `signal-spirit`, because the spirit build above
  already exercises the same `lower_source` codepath end to end with a
  checked-in artifact to diff against.

## Appendix: exact commands a verifier can re-run

1. `cd /git/github.com/LiGoldragon/schema-next && ~/.nix-profile/bin/cargo test`
   — all 14 test binaries pass; `tests/lowering.rs` = 22 passed.
2. `cd /git/github.com/LiGoldragon/schema-next && ~/.nix-profile/bin/cargo run --example emit_artifacts`
   — prints the live `core.asschema` lowering; matches checked-in
   `schemas/core.asschema` byte-for-byte.
3. `cd /git/github.com/LiGoldragon/spirit && sha256sum schema/signal.asschema schema/signal.schema`
   — baseline hashes.
4. `cd /git/github.com/LiGoldragon/spirit && SPIRIT_UPDATE_SCHEMA_ARTIFACTS=1 ~/.nix-profile/bin/cargo build`
   — regenerates artifacts; re-hashing shows them unchanged.
5. `cd /git/github.com/LiGoldragon/spirit && touch schema/signal.schema && ~/.nix-profile/bin/cargo build`
   — plain build = freshness CHECK mode; success proves `.asschema` is
   the lowering of `.schema`.

Files read in full (not commands, but load-bearing):
`/git/github.com/LiGoldragon/spirit/schema/signal.schema`,
`/git/github.com/LiGoldragon/spirit/schema/signal.asschema`,
`/git/github.com/LiGoldragon/schema-next/schemas/core.schema`,
`/git/github.com/LiGoldragon/schema-next/schemas/core.asschema`,
`/git/github.com/LiGoldragon/schema-next/schemas/spirit-min.schema`,
`/git/github.com/LiGoldragon/signal-spirit/schema/signal-spirit.schema`,
`/git/github.com/LiGoldragon/schema-next/src/source.rs` (root parsing),
`/git/github.com/LiGoldragon/schema-next/src/asschema.rs` (struct + TypeReference),
`/git/github.com/LiGoldragon/spirit/build.rs`,
`/git/github.com/LiGoldragon/signal-spirit/build.rs`.
