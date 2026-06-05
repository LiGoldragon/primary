# 314 — Asschema removal — operator comparison with designer

## Scope

This compares the operator position against designer report
`reports/designer/520-Psyche-asschema-removal-design.md` and the current
main-branch code in `nota-next`, `schema-next`, and `schema-rust-next`.

The psyche-facing question is whether Asschema removal should mean:

- a pragmatic `SchemaSource::resolve()` projection consumed by Rust emission, or
- a stronger shape where the emitter walks `SchemaSource` directly and resolves
  semantics inline.

## Current implementation facts

The typed NOTA macro-node substrate is now live in `nota-next`.
`nota-next/ARCHITECTURE.md` documents `#[derive(StructuralMacroNode)]`, ordered
variant matching, recursive capture decode, and reverse structural NOTA
encoding. That fulfills the core clarified mechanism: the expected Rust enum
type defines the macro node before the value is read.

`schema-next` already has the source value that should become the center of the
stack. `schema-next/src/source.rs` defines `SchemaSource`, parses `.schema`
text into `SourceImports`, `SourceRootEnum`, and `SourceNamespace`, and writes
schema text back from the typed source object. It also already contains the
important resolution work inside `SchemaSource::to_asschema`: source namespace
collection, inline declaration hoisting, root inline declaration insertion,
root enum payload resolution, and final declaration ordering.

`schema-next` still returns `Asschema` from its public lowering path.
`SchemaEngine::lower_schema_source_with_resolver` resolves imports and then
calls `source.to_asschema(...)`. That makes `Asschema` the current endpoint,
but the work is already concentrated close to `SchemaSource`.

`schema-rust-next` still consumes `Asschema` directly.
`RustEmitter::emit_file(&Asschema)`, `RustEmitter::emit_module(&Asschema)`, and
`RustModule::from_asschema` are the load-bearing emission entry points.
`schema-rust-next/src/build.rs` also still lowers each module to Asschema,
writes an Asschema artifact, then emits Rust from that value. This is the
actual place where Asschema remains structurally real.

The repo docs already carry the compatibility posture. `schema-next/INTENT.md`
and `schema-next/ARCHITECTURE.md` say Asschema is no longer the target
intermediate language and that `.asschema`, `.asschema.rkyv`, and
`AsschemaArtifact` remain only compatibility endpoints. `schema-rust-next`
similarly says its current compatibility input is Asschema and the target is
typed schema source data decoded through structural macro node codecs.

## Agreement with designer

Designer's central correction is right: removing Asschema is not deleting
resolution. Rust emission cannot render correct Rust from unresolved authored
sugar. It needs to know which inline declarations were hoisted, which
declarations are private, what symbol paths mean, how root header shorthand
resolved, which scalar names are reserved, and which imports point to external
owned types.

The old mistake was making that resolved knowledge into a separate assembled
language with checked-in `.asschema` artifacts and a separate lowering phase.
The new target should keep authored `.schema` as specialized NOTA and compute
resolved facts from the typed source object when a consumer needs them.

Designer is also right that the hard work is not raw decoding anymore. The
decode side is mostly in place, and the formal derive path has been proven.
The hard work is relocating resolution and then moving Rust emission off
`Asschema`.

## Operator contention

I choose the pragmatic path, but with a stricter boundary than the phrase
"resolved-type vocabulary survives" might imply.

Correction after psyche question: the primary owner is not a new
`SchemaResolution` data type. The primary owner is the set of typed source
datatypes that `.schema` deserializes into. Those nouns are exactly where the
resolution behavior belongs.

An implementation may use a short-lived private context or cache while
resolving imports, collecting names, or avoiding recomputation. But that object
is not the new schema value, not the emitter's public input contract, and not a
replacement artifact language. It gets no file extension, no checked-in text
form, no binary artifact, no store, and no public handoff contract. If it
becomes a durable object components depend on, Asschema has not been removed;
it has been renamed.

The strong alternative, where `schema-rust-next` walks `SchemaSource` and
resolves inline as it emits, is worse design. It puts schema semantics inside
the Rust renderer. The emitter would need to understand source sugar,
declaration hoisting, symbol resolution, scalar reservation, and import
semantics while also rendering Rust. That makes the emitter a second schema
engine and violates the boundary: Schema owns schema meaning; Rust emission
owns Rust projection from typed facts.

So the correct future-facing pattern is:

1. `.schema` decodes through typed structural macro-node source nouns.
2. `SchemaSource` owns resolution as methods on source nouns.
3. Resolution facts are computed on demand by those nouns, optionally with a
   private source-owned context/cache.
4. Rust emission consumes the typed source value through those source-owned
   methods and renders Rust.
5. `.asschema` text, `.asschema.rkyv`, `AsschemaArtifact`, `AsschemaStore`, and
   emitter APIs that accept Asschema retire after consumers move.

This preserves "schema is just NOTA" at the authored and codec boundary while
keeping the generated-code backend clean and reusable.

## Ownership recommendation

Avoid `Asschema` entirely in the new spine, and avoid naming a new public
schema product too early. The correct public handoff should read as source-first:

- `SchemaSource` and its child source nouns own methods such as resolved
  imports, resolved root enums, resolved namespace declarations, symbol paths,
  and source validation.
- `SchemaEngine` coordinates dependency import resolution and calls those source
  methods; it does not manufacture a second schema language.
- `RustEmitter` should grow `emit_file_from_source(...)` /
  `RustModule::from_source(...)` as the durable entry point.
- Any object named something like `SourceResolution` or `ResolutionContext`
  should be private or narrowly source-owned unless implementation proves a
  public type is unavoidable.

The ownership must stay: source datatypes resolve; emitter renders.

## Safety net

The byte-identical Rust diff designer proposes is necessary and strong, but it
is not enough by itself. It proves end-to-end parity only after the whole path
runs; it does not localize which transformation changed when a mismatch
appears.

The first slice should add direct tests for the source-owned resolution
methods:

- inline declaration hoisting order,
- public versus private visibility,
- root bare-header payload resolution,
- inline root declaration insertion,
- struct single-field newtype collapse,
- derived field naming,
- enum variant payload resolution,
- reserved scalar validation,
- import resolution preservation,
- symbol path parity.

Then the end-to-end witness compares old Asschema emission against new
source-driven emission for real schemas, starting with spirit and then any
multi-plane package that exercises imports.

## Implementation slice

The smallest correct implementation sequence is:

1. Move the body of `SchemaSource::to_asschema` onto `SchemaSource` and child
   source nouns as source-owned resolution methods. If a private context/cache
   is needed, keep it clearly subordinate to the source nouns.
2. Keep `to_asschema` temporarily as a compatibility adapter that calls those
   source-owned methods and packages the old `Asschema` value.
3. Add `RustModule::from_source` and `RustEmitter` methods that consume the
   typed source value, with import-resolution context supplied by `SchemaEngine`
   or the build driver.
4. Change the build driver to source round-trip, resolve, and emit Rust without
   producing `.asschema` artifacts.
5. Move tests from "lowers to Asschema" assertions to assertions on
   source-owned resolved facts, while keeping old-vs-new parity tests during
   migration.
6. Remove `.asschema` files and artifact freshness only after the driver no
   longer consumes or produces them.
7. Delete `Asschema`, `AsschemaArtifact`, and `AsschemaStore` once no public
   consumer remains.

## Final operator read

Designer report 520 is directionally correct and improves the operator
position by naming the real work: resolution relocation. The correction after
the psyche's follow-up is that "relocation" means onto the datatypes schema
deserializes into, not into a new public `SchemaResolution` product. With that
guardrail, the pragmatic path is not a compromise against the psyche's "no
Asschema" intent; it is the clean way to satisfy it without making the Rust
emitter perform schema semantics.
