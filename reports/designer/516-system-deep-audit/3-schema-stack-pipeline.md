---
title: The schema stack pipeline — nota-next → schema-next → schema-rust-next → Rust
role: designer
variant: Psyche
date: 2026-06-04
topics:
  - schema-derived-stack
  - nota-next
  - schema-next
  - schema-rust-next
  - spirit-build
  - code-generation
  - freshness-check
---

# The schema stack pipeline, proven end to end

This is mechanism report #3 of the system deep audit. It explains the
full emission pipeline that turns a hand-written `.schema` file into the
checked-in Rust source the daemon compiles against, and it proves every
behavioural claim with a command that was actually run in this
environment, with verbatim output pasted in.

The pipeline has four stages, each living in its own crate:

1. **`nota-next`** — the structural NOTA reader. It parses bytes into
   `Block`s carrying `SourceSpan`s, and exposes *candidate* classifiers
   (`qualifies_as_pascal_case_symbol`, etc.) WITHOUT imposing schema
   semantics. It is the substrate; it knows nothing about types.
2. **`schema-next`** — the position-aware macro engine plus the
   assembled schema model (`Asschema`). It consumes `nota-next` blocks,
   dispatches them by structural *position* (root input, root output,
   namespace, struct fields, enum variants, type reference), and lowers
   them into a typed `Asschema`. It also serialises `Asschema` back out
   as a `.asschema` NOTA artifact.
3. **`schema-rust-next`** — the Rust source emitter. It consumes an
   `Asschema` and produces Rust source *text*. It owns the build
   orchestration: `GenerationPlan` / `ModuleEmission` / `GenerationDriver`
   in `build.rs`, plus the `write_or_check` freshness gate.
4. **`spirit`** (the consumer) — its own `build.rs` declares a
   `GenerationPlan` of three modules (`signal`, `nexus`, `sema`), drives
   generation, and writes-or-checks the result against the checked-in
   `src/schema/*.rs`.

The repos and their versions, verbatim from their `Cargo.toml`:

```
nota-next        0.1.0   "Structural NOTA reader for the schema-derived stack."
schema-next      0.1.1   "Position-aware schema macro engine and assembled schema model."
schema-rust-next 0.1.8   "Rust source emitter for schema-next assembled schemas."
```

`schema-next` depends on `nota-next` (git/main); `schema-rust-next`
depends on `schema-next` (git/main). The dependency arrows run strictly
downstream — the reader knows nothing of schemas, the schema model knows
nothing of Rust.

## Environment and tooling, confirmed

```
$ ~/.nix-profile/bin/cargo --version
cargo 1.95.0 (f2d3ce0bd 2026-03-21)

$ which spirit
/home/li/.nix-profile/bin/spirit

$ spirit --version          # NOTA-only binary, no flags
/nix/store/20zk48jr4sn8yrjyq925gvzz3p4x3zkm-spirit/bin/spirit accepts
NOTA or signal-file input, not flag-style argument --version
```

The `spirit --version` line is itself a proof of the single-argument
NOTA rule — the deployed CLI rejects `--version` because every component
binary takes exactly one NOTA argument and no flags. (That CLI is the
runtime consumer of the emitted contract; it is not part of the
generation pipeline, but it is what the generated `signal.rs` ultimately
serves.)

## Stage 1 — nota-next: structural blocks, spans, qualifies_as_*

`nota-next` parses source into a `Document` of `Block`s. The block enum
(`/git/github.com/LiGoldragon/nota-next/src/parser.rs:57`):

```rust
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum Block {
    Delimited {
        delimiter: Delimiter,
        span: SourceSpan,
        root_objects: Vec<Block>,
    },
    PipeText(PipeText),
    Atom(Atom),
}
```

Every block carries a `SourceSpan` (`parser.rs:11`), which is a pair of
`SourcePosition { byte_offset, line, column }`. The span is what lets a
block re-emit the exact original text it came from
(`Block::reemit`, `parser.rs:76`):

```rust
pub fn reemit<'source>(&self, source: &'source str) -> &'source str {
    let span = self.source_span();
    &source[span.start.byte_offset..span.end.byte_offset]
}
```

This is the load-bearing reason spans exist: the schema layer above can
quote a block's literal text for error messages and round-trip checks
without re-serialising.

Crucially, `nota-next` exposes *candidate* classifications, never schema
judgements. An `Atom` is classified once at parse time into one of four
`AtomClassification` candidates (`parser.rs:572`): `SymbolCandidate`,
`IntegerCandidate`, `DecimalCandidate`, `TextCandidate`. The
`qualifies_as_*` family layers naming-shape predicates on top of the
symbol candidacy (`parser.rs:542`):

```rust
pub fn qualifies_as_symbol(&self) -> bool {
    self.classification == AtomClassification::SymbolCandidate
}

pub fn qualifies_as_pascal_case_symbol(&self) -> bool {
    self.qualifies_as_symbol()
        && self.text.chars().next()
            .is_some_and(|character| character.is_ascii_uppercase())
        && !self.text.contains('-')
}

pub fn qualifies_as_camel_case_symbol(&self) -> bool {
    self.qualifies_as_symbol()
        && self.text.chars().next()
            .is_some_and(|character| character.is_ascii_lowercase())
        && !self.text.contains('-')
}

pub fn qualifies_as_kebab_case_symbol(&self) -> bool {
    self.qualifies_as_symbol() && self.text.contains('-')
}
```

The word "qualifies" is deliberate: the reader reports *whether a block
could be read as* a PascalCase type name, a camelCase field name, a
kebab identifier — it never decides that it *is* one. That decision
belongs to the position-aware engine in `schema-next`. The reader is
schema-agnostic substrate; the same `Document` could feed a different
schema dialect. One of nota-next's own design tests names this contract
exactly: `design_example_reader_exposes_candidates_not_schema_semantics`.

### Proof: nota-next test suite

Command and verbatim per-binary results, run in
`/git/github.com/LiGoldragon/nota-next`:

```
$ ~/.nix-profile/bin/cargo test
deps/nota_next ............. ok. 0 passed
deps/block_queries ......... ok. 8 passed
deps/codec ................. ok. 8 passed
deps/derive ................ ok. 8 passed
deps/design_examples ....... ok. 7 passed
deps/macro_nodes ........... ok. 5 passed
doc-tests .................. ok. 0 passed
```

Total: **36 tests passed, 0 failed.** The `design_examples` binary is
the one that pins the span-propagation and candidate-not-semantics
contracts (`design_example_source_spans_propagate_through_nested_blocks`,
`design_example_reader_exposes_candidates_not_schema_semantics`, both
shown `ok` in the run).

## Stage 2 — schema-next: position-aware macros → Asschema

`schema-next` is where structural blocks acquire schema meaning. The key
type is `MacroPosition` (`schema-next/src/macros.rs:25`):

```rust
pub enum MacroPosition {
    RootImports,
    RootInput,
    RootOutput,
    RootNamespace,
    NamespaceDeclaration,
    StructFields,
    EnumVariants,
    TypeReference,
}
```

This is the "position-aware" part. The four top-level root objects of a
`.schema` document map positionally: imports block, input root enum,
output root enum, namespace block. Inside the namespace, each declaration
is dispatched by what *position* its block sits in — a `{ ... }` block in
field position is read as struct fields, the same shape in variant
position is read as enum variants, an atom in type-reference position is
read as a `TypeReference`. The macro registry's `lower` method
(`macros.rs:275`) walks registered handlers, asks each whether it
`matches(object, position)`, and dispatches the first that does; if none
match and the position isn't `TypeReference`, it falls back to the
registered node definition for that position. **Position, not keyword, is
the disambiguator** — this is the architectural payoff of NOTA being
positional rather than labelled.

The output of lowering is an `Asschema` (`schema-next/src/asschema.rs:222`):

```rust
#[nota(known_root)]
pub struct Asschema {
    identity: super::SchemaIdentity,
    imports: Vec<ImportDeclaration>,
    resolved_imports: Vec<super::ResolvedImport>,
    #[nota(name = "Input")]
    input: EnumDeclaration,
    #[nota(name = "Output")]
    output: EnumDeclaration,
    namespace: Vec<Declaration>,
}
```

`Asschema` is the *assembled* schema: identity (component + version),
the resolved imports, the two root enums (input operations and output
replies), and the flat namespace of declarations. It is itself a
NOTA-codec type (`#[nota(known_root)]`), so it round-trips to a
`.asschema` file via `AsschemaArtifact`.

The lowering entry the build uses is on `SchemaModuleSource`
(`schema-next/src/module.rs:199`):

```rust
pub fn lower(&self, engine: &SchemaEngine) -> Result<Asschema, SchemaError> {
    engine.lower_schema_source(&self.to_schema_source()?, self.identity.clone())
}

pub fn lower_with_resolver(
    &self,
    engine: &SchemaEngine,
    resolver: &ImportResolver,
) -> Result<Asschema, SchemaError> {
    engine.lower_schema_source_with_resolver(
        &self.to_schema_source()?, self.identity.clone(), resolver,
    )
}
```

`to_schema_source` first parses the raw `.schema` text into a
`SchemaSource` (the syntactic layer), then the engine lowers that into
the semantic `Asschema`, resolving cross-crate imports through the
`ImportResolver` when one is supplied.

### What the intermediate Asschema looks like (real artifact)

The `.asschema` file is the serialised `Asschema` — the exact handoff
artifact between stage 2 and stage 3. Head of
`/git/github.com/LiGoldragon/spirit/schema/signal.asschema`, verbatim:

```
(spirit:signal [0.1.0])
[]
[]
[(Record (Some (Plain Record))) (Observe (Some (Plain Observe))) (Lookup (Some (Plain Lookup))) (Count (Some (Plain Count))) (Remove (Some (Plain Remove))) (LookupStash (Some (Plain LookupStash)))]
[(RecordAccepted (Some (Plain RecordAccepted))) ... (Error (Some (Plain Error))) (Rejected (Some (Plain Rejected)))]
[(Public SourcePath (Alias (SourcePath String))) (Public Import (Struct (Import {source_path (Plain SourcePath) local_path (Plain LocalPath)}))) ... (Public Magnitude (Enum (Magnitude [(Zero None) (Minimum None) ... (Maximum None)])))]
```

Read this against the positional `Asschema` struct: line 1 is
`identity` (`spirit:signal` at version `0.1.0`), lines 2–3 are the empty
`imports` and `resolved_imports`, line 4 is the `Input` `EnumDeclaration`
(the six operation roots `Record/Observe/Lookup/Count/Remove/LookupStash`),
line 5 is the `Output` `EnumDeclaration` (the reply roots), and line 6 is
the `namespace` (`Vec<Declaration>`) — every alias, struct, and enum the
contract declares, each tagged `Public` with its lowered shape (`Alias`,
`Struct`, `Enum`). Note the field names are already lowercased to
snake_case here (`source_path`, `local_path`) — that name transform
happens in the lowering, via `Name::field_name` (`asschema.rs:41`), not
in the Rust emitter.

### Proof: schema-next test suite

Command and verbatim per-binary results, run in
`/git/github.com/LiGoldragon/schema-next`:

```
$ ~/.nix-profile/bin/cargo test
deps/schema_next ................... ok. 0 passed
deps/asschema_definition ........... ok. 8 passed
deps/big_examples .................. ok. 3 passed
deps/collections ................... ok. 13 passed
deps/design_examples ............... ok. 13 passed
deps/lowering ...................... ok. 22 passed
deps/macro_exploration ............. ok. 14 passed
deps/operator_271_closed_claims .... ok. 9 passed
deps/raw_core_schema ............... ok. 6 passed
deps/resolution .................... ok. 7 passed
deps/source_codec .................. ok. 4 passed
deps/symbol_path ................... ok. 5 passed
deps/syntax_layer .................. ok. 7 passed
deps/upgrade_pilot ................. ok. 5 passed
```

Total: **116 tests passed, 0 failed.** The `lowering` (22) and
`macro_exploration` (14) binaries are the ones that exercise the
position-aware dispatch and the source→Asschema transform.

## Stage 3 — schema-rust-next: Asschema → Rust source text

This crate has two halves. `lib.rs` is the emitter proper
(`RustEmitter` → `RustModule` → `RustWriter` → `RustCode`). `build.rs` is
the orchestration: `GenerationPlan`, `ModuleEmission`, `GenerationDriver`,
`GeneratedPackage`, and the `write_or_check` freshness gate.

### The emitter: emit_file and the render pipeline

`RustEmitter::emit_file` (`schema-rust-next/src/lib.rs:51`) builds a
`RustModule` from the `Asschema` and renders it:

```rust
pub fn emit_file(&self, asschema: &Asschema) -> GeneratedFile {
    let module = self.emit_module(asschema);
    GeneratedFile {
        path: module.file_path().to_owned(),
        code: module.render(),
    }
}
```

`RustModule::from_asschema` (`lib.rs:101`) maps each `Asschema`
component to a Rust construct: `namespace()` declarations become
`RustDeclaration`s, the two `input_and_output()` enums become
`RustEnum`s, `resolved_imports()` become `RustImport`s, plus default
scalar aliases (`String`/`Integer`/`Boolean`/`Path`). `render`
(`lib.rs:158`) is the ordered writer pass that produces the final text —
it opens with the generated header, emits scalar aliases, imports, NOTA
support, then each declaration, then the root enums, then a long tail of
support impls (variant constructors, payload `From` impls, NOTA bridges,
short headers, signal-frame support, and — when the target is a runtime
rather than a bare wire contract — plane/route/trace/mail/upgrade
support). The very first emitted line is the provenance header
(`lib.rs:162`):

```rust
writer.line(format!("// @generated by {}", self.generator_name));
```

where `generator_name` is the literal `"schema-rust-next"`
(`lib.rs:46`). That single line is the marker every consuming repo greps
for to know a file is machine-owned and must not be hand-edited.

### The orchestration: GenerationPlan / ModuleEmission / GenerationDriver

A `GenerationPlan` (`build.rs:14`) bundles a `SchemaPackage` (crate root
+ name + version), a list of `ModuleEmission`s, and a list of
`DependencySchema`s (for cross-crate imports). A `ModuleEmission`
(`build.rs:108`) pairs a module `Name` with `RustEmissionOptions` — and
the named constructors encode the emission *target*. The relevant ones
for spirit:

```rust
pub fn signal_runtime_module(module: impl Into<String>) -> Self {
    Self::new(module, RustEmissionOptions::feature_gated_nota("nota-text")
        .with_target(RustEmissionTarget::SignalRuntime))
}
pub fn nexus_runtime() -> Self {
    Self::new("nexus", RustEmissionOptions::feature_gated_nota("nota-text")
        .with_target(RustEmissionTarget::NexusRuntime))
}
pub fn sema_runtime() -> Self {
    Self::new("sema", RustEmissionOptions::feature_gated_nota("nota-text")
        .with_target(RustEmissionTarget::SemaRuntime))
}
```

`feature_gated_nota("nota-text")` is why every emitted type carries
`#[cfg_attr(feature = "nota-text", derive(nota_next::NotaDecode,
nota_next::NotaEncode))]` — the NOTA text surface is opt-in behind a
cargo feature so binary-only daemons can drop `nota-next` from their
dependency closure entirely. The target (`SignalRuntime` vs
`NexusRuntime`/`SemaRuntime`) selects which support impls the render tail
emits.

`GenerationDriver` (`build.rs:273`) holds the plan and a `SchemaEngine`.
Its `generate` (`build.rs:291`) builds the import resolver from the
plan's dependencies, then produces one `GeneratedModule` per emission:

```rust
pub fn generate(&self) -> Result<GeneratedPackage, BuildError> {
    let resolver = self.plan.import_resolver();
    let mut modules = Vec::new();
    for emission in self.plan.modules() {
        modules.push(GeneratedModule::from_emission(
            self.plan.package(), emission, &self.engine, &resolver,
        )?);
    }
    Ok(GeneratedPackage::new(
        self.plan.package().root().to_path_buf(), modules,
    ))
}
```

`GeneratedModule::from_emission` (`build.rs:387`) is where all three
stages compose in one place:

```rust
let source = package.load_module(emission.module().clone())?;       // stage 1+2 read .schema
let source_artifact = SourceArtifactRoundTrip::new(
    source.path().to_path_buf(),
    SchemaSourceArtifact::new(source.to_schema_source()?),
).validate()?;                                                       // round-trip the .schema text
let asschema = source.lower_with_resolver(engine, resolver)?;       // stage 2 lower → Asschema
let asschema_artifact = AsschemaArtifact::new(asschema.clone()).to_nota_source(); // serialise .asschema
let rust_file = RustEmitter::new(emission.options().clone()).emit_file(&asschema); // stage 3 emit .rs
```

Note the `SourceArtifactRoundTrip::validate` step (`build.rs:442`): it
re-parses the schema text it just serialised and errors with
`SchemaSourceRoundTrip` if the result differs. So the build doesn't just
emit — it verifies the `.schema` text is a fixed point of the
parse/serialise pair before trusting it.

### write_or_check: the freshness gate

This is the load-bearing mechanism for keeping checked-in generated code
honest. `GeneratedPackage::write_or_check` (`build.rs:345`):

```rust
pub fn write_or_check(
    self,
    update_environment_variable: impl Into<String>,
) -> Result<(), BuildError> {
    self.check_with(FreshnessCheck::from_environment(update_environment_variable))
}
```

`FreshnessCheck::from_environment` (`build.rs:527`) reads the named env
var ONCE and records whether it is present:

```rust
fn from_environment(update_environment_variable: impl Into<String>) -> Self {
    let update_environment_variable = update_environment_variable.into();
    let update_files = env::var_os(&update_environment_variable).is_some();
    Self { update_environment_variable, update_files }
}
```

Then `GeneratedArtifact::check_with` (`build.rs:474`) branches on that
single boolean — and this is the entire write-vs-check decision:

```rust
fn check_with(&self, check: &FreshnessCheck) -> Result<(), BuildError> {
    if check.updates_files() {
        self.write()?;            // env var SET: overwrite the file on disk
        return Ok(());
    }
    if self.matches_existing()? { // env var ABSENT: compare against disk
        return Ok(());
    }
    Err(BuildError::StaleGeneratedArtifact {  // differs → hard error
        path: self.path.clone(),
        update_environment_variable: check.update_environment_variable().to_owned(),
    })
}
```

So with the env var present, the emitter is the source of truth and
overwrites the checked-in file. With the env var absent — the normal CI
and `cargo build` case — the freshly emitted text is compared
byte-for-byte against what is on disk (`matches_existing`, `build.rs:488`,
which treats a missing file as a non-match), and any divergence is a
build-breaking `StaleGeneratedArtifact` error naming the env var to set.
The same `check_with` runs over both the `.asschema` artifact and the
`.rs` file (`GeneratedModule::check_generated_artifacts`, `build.rs:413`).

`assert_checked_in` (`build.rs:341`) is the stricter sibling: it calls
`FreshnessCheck::check_only()`, which can never write — used in tests
that must fail rather than silently regenerate.

### Proof: schema-rust-next test suite

Command and verbatim per-binary results, run in
`/git/github.com/LiGoldragon/schema-rust-next`:

```
$ ~/.nix-profile/bin/cargo test
deps/schema_rust_next .......... ok. 0 passed
deps/big_emission .............. ok. 9 passed
deps/cross_crate_import ........ ok. 2 passed
deps/emission .................. ok. 30 passed
deps/generation_driver ......... ok. 4 passed
deps/upgrade_emission .......... ok. 6 passed
```

Total: **51 tests passed, 0 failed.** `generation_driver` (4) covers the
`GenerationPlan`/`GenerationDriver`/`write_or_check` orchestration;
`emission` (30) covers the `Asschema`→Rust text rules.

## Stage 4 — spirit: the real end-to-end build

spirit's own `build.rs` (`/git/github.com/LiGoldragon/spirit/build.rs`)
declares a three-module plan and drives it:

```rust
let plan = GenerationPlan::new(&self.crate_root, "spirit", "0.1.0")
    .with_module(ModuleEmission::signal_runtime_module("signal"))
    .with_module(ModuleEmission::nexus_runtime())
    .with_module(ModuleEmission::sema_runtime());
GenerationDriver::new(plan)
    .generate()
    .expect("generate spirit schema artifacts")
    .write_or_check("SPIRIT_UPDATE_SCHEMA_ARTIFACTS")
    .expect("checked-in spirit schema artifacts are fresh");
```

So `SPIRIT_UPDATE_SCHEMA_ARTIFACTS` is the env var threaded into
`write_or_check`. With it set, `build.rs` rewrites
`src/schema/{signal,nexus,sema}.rs` and `schema/*.asschema`; without it,
`build.rs` checks them and panics on staleness (the `.expect` message
"checked-in spirit schema artifacts are fresh").

### The input: signal.schema (head)

`/git/github.com/LiGoldragon/spirit/schema/signal.schema`, verbatim head:

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
  ...
```

The four positional root objects are visible: `{}` imports, the
`[...]` input operation list, the `[...]` output reply list, and the
`{ ... }` namespace. This is the human-authored surface — terse,
positional, no keywords.

### Proof A: end-to-end emission with the update env var

I forced `build.rs` to re-run (by touching its `rerun-if-changed`
inputs) and ran the update build, then checksummed the artifacts.
Commands run in `/git/github.com/LiGoldragon/spirit`:

```
$ md5sum src/schema/signal.rs ...    # BEFORE
a6e7c73ead1b888d8061c9fcfda883c7  src/schema/signal.rs
b21f723a9897564fb2291ad952fc73c4  src/schema/nexus.rs
a0f2ea00d41f6a565db144b763425d09  src/schema/sema.rs
dee372b2a5c8b5aedc0a985feb2100e4  schema/signal.asschema

$ touch schema/signal.schema schema/nexus.schema schema/sema.schema
$ SPIRIT_UPDATE_SCHEMA_ARTIFACTS=1 ~/.nix-profile/bin/cargo build
   Compiling spirit v0.1.0 (/git/github.com/LiGoldragon/spirit)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.72s
=== exit: 0 ===

$ md5sum src/schema/signal.rs ...    # AFTER update build
a6e7c73ead1b888d8061c9fcfda883c7  src/schema/signal.rs
b21f723a9897564fb2291ad952fc73c4  src/schema/nexus.rs
a0f2ea00d41f6a565db144b763425d09  src/schema/sema.rs
dee372b2a5c8b5aedc0a985feb2100e4  schema/signal.asschema
```

`spirit` recompiled (so `build.rs` genuinely re-ran the emitter), and the
checksums are byte-identical before and after. **This proves the
checked-in `src/schema/*.rs` is exactly the deterministic output of the
current emitter** — the source is not ahead of or behind the generator.

### The output: generated signal.rs (head)

`/git/github.com/LiGoldragon/spirit/src/schema/signal.rs`, verbatim head:

```rust
// @generated by schema-rust-next

pub type String = std::string::String;
pub type Integer = u64;
pub type Boolean = bool;
pub type Path = std::string::String;

#[cfg(feature = "nota-text")]
pub use nota_next::{
    NotaDecode, NotaDecodeError, NotaEncode, NotaSource,
};

pub type SourcePath = String;

pub type LocalPath = String;

pub type PublicPath = String;

#[cfg_attr(feature = "nota-text", derive(nota_next::NotaDecode, nota_next::NotaEncode))]
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub struct Import {
    pub source_path: SourcePath,
    pub local_path: LocalPath,
}

#[cfg_attr(feature = "nota-text", derive(nota_next::NotaDecode, nota_next::NotaEncode))]
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub struct Export {
    pub local_path: LocalPath,
    pub public_path: PublicPath,
}
```

And the `Input` root enum, generated from the `[Record Observe Lookup
Count Remove LookupStash]` input list in the source
(`src/schema/signal.rs:264`):

```rust
#[cfg_attr(feature = "nota-text", derive(nota_next::NotaDecode, nota_next::NotaEncode))]
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub enum Input {
    Record(Record),
    Observe(Observe),
    Lookup(Lookup),
    Count(Count),
    Remove(Remove),
    LookupStash(LookupStash),
}
```

Trace one type all the way through: `Import { SourcePath * LocalPath * }`
in `signal.schema` → `(Public Import (Struct (Import {source_path (Plain
SourcePath) local_path (Plain LocalPath)})))` in the `.asschema` → the
`pub struct Import { pub source_path: SourcePath, pub local_path:
LocalPath }` in `signal.rs`. The PascalCase field references became
snake_case fields, every derive (rkyv archive + serialise + deserialise,
and the feature-gated NOTA codec) is attached, and `*` field markers in
the source became individual fields. Each stage is observable in its own
on-disk artifact.

### Proof B: freshness CHECK passes when the env var is absent

I forced `build.rs` to re-run again, this time WITHOUT the env var, so
the build takes the `matches_existing` branch:

```
$ touch schema/signal.schema schema/nexus.schema schema/sema.schema
$ ~/.nix-profile/bin/cargo build
   Compiling spirit v0.1.0 (/git/github.com/LiGoldragon/spirit)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 1.22s
=== exit: 0 ===
```

The plain build succeeds (exit 0): the emitter ran, compared its output
against the checked-in files, found them identical, and did not write.
This is the steady-state CI guarantee — the build proves the generated
code is in sync without mutating the tree.

### Proof C: freshness CHECK FAILS on a stale artifact

The most important proof: that `write_or_check` is not a no-op. I copied
`signal.rs` aside, appended a corruption line, forced `build.rs` to
re-run without the env var, captured the failure, then restored the
original and confirmed the checksum:

```
$ cp src/schema/signal.rs /tmp/signal.rs.bak
$ printf '\n// CORRUPTION-FOR-AUDIT\n' >> src/schema/signal.rs
$ touch schema/signal.schema
$ ~/.nix-profile/bin/cargo build
error: failed to run custom build command for `spirit v0.1.0`
  thread 'main' panicked at build.rs:39:14:
  checked-in spirit schema artifacts are fresh: StaleGeneratedArtifact {
    path: "/git/github.com/LiGoldragon/spirit/src/schema/signal.rs",
    update_environment_variable: "SPIRIT_UPDATE_SCHEMA_ARTIFACTS"
  }
$ ~/.nix-profile/bin/cargo build > /dev/null 2>&1; echo $?
101

$ cp /tmp/signal.rs.bak src/schema/signal.rs
$ md5sum src/schema/signal.rs
a6e7c73ead1b888d8061c9fcfda883c7  src/schema/signal.rs
```

The corrupted file made the plain build fail with exactly
`StaleGeneratedArtifact`, naming the file and the env var to set, exit
code 101 (the `.expect` panic at `build.rs:39`). After restore, the
checksum is back to the original `a6e7c73e...`. I then re-ran the plain
build to confirm the tree is green again:

```
$ touch schema/signal.schema && ~/.nix-profile/bin/cargo build
   Compiling spirit v0.1.0 (/git/github.com/LiGoldragon/spirit)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.78s
exit: 0
```

This closes the loop: the freshness gate genuinely rejects drift, the
error is actionable (it names the file and the update env var), and the
audit left the tree exactly as it found it.

## What this pipeline teaches, in one breath

- **One source, two derived artifacts, both checked in.** Each `.schema`
  module produces a `.asschema` (the serialised `Asschema` handoff) and a
  `.rs` (the emitted Rust). Both are regenerated and freshness-checked
  on every build. The `.asschema` is not a throwaway — it is the stable
  inter-crate contract that a *dependent* crate's emitter reads via
  `ImportResolver` to reference upstream types without re-declaring them.
- **Position is the only disambiguator.** Because NOTA records are
  positional, `schema-next` reads meaning from *where* a block sits
  (`MacroPosition`), never from a keyword. The reader below it
  (`nota-next`) refuses to even decide a symbol's role — it only reports
  `qualifies_as_*` candidacy. That separation is what lets the same
  reader serve any schema dialect.
- **The build IS the verifier.** `write_or_check` makes the emitter the
  single source of truth: set the env var to regenerate, leave it unset
  and any hand-edit to a `@generated` file breaks the build with a named,
  actionable error. There is no way for the checked-in Rust to silently
  drift from the schema.
- **Determinism is real and now proven.** Re-running the emitter over an
  unchanged schema produced byte-identical output (checksums held across
  a forced regeneration), which is the precondition that makes the
  check-mode comparison meaningful.

## Anything I could not run

Nothing in the assigned scope was un-runnable. All three test suites ran
to completion with real pass counts (nota-next 36, schema-next 116,
schema-rust-next 51), the end-to-end spirit emission ran in both
update-mode and check-mode, and the stale-artifact failure path was
exercised directly (and the tree restored). The only command that
"failed" did so by design — the corrupted-artifact `cargo build` in
Proof C, which is the failure I set out to provoke.
