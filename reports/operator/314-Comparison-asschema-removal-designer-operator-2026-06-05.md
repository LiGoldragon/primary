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

`SchemaSource::resolve()` should return an ephemeral, source-owned projection,
not a new artifact language. It may be a named Rust type, because typed data is
better than having the emitter rediscover semantics while rendering text. But
it must not get a file extension, a checked-in text form, a binary artifact, a
store, or a public handoff contract that components start depending on. If
that happens, Asschema has not been removed; it has been renamed.

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
3. The resolution result is computed on demand and stays in memory.
4. Rust emission consumes that resolved view and renders Rust.
5. `.asschema` text, `.asschema.rkyv`, `AsschemaArtifact`, `AsschemaStore`, and
   emitter APIs that accept Asschema retire after consumers move.

This preserves "schema is just NOTA" at the authored and codec boundary while
keeping the generated-code backend clean and reusable.

## Naming recommendation

Avoid `Asschema` entirely in the new spine. A reasonable noun is
`SchemaResolution` rather than `ResolvedSchema`: it names the operation result
without implying a second schema language.

The owning methods should read like:

- `SchemaSource::resolve(identity, imports, resolved_imports) -> SchemaResolution`
- `SchemaEngine::resolve_schema_source_with_resolver(...) -> SchemaResolution`
- `RustEmitter::emit_file_from_resolution(&SchemaResolution) -> GeneratedFile`
- later, `RustEmitter::emit_file_from_source(...)` as the convenience method
  that resolves then emits.

The exact names can shift during implementation, but the ownership should not:
source resolves; emitter renders.

## Safety net

The byte-identical Rust diff designer proposes is necessary and strong, but it
is not enough by itself. It proves end-to-end parity only after the whole path
runs; it does not localize which transformation changed when a mismatch
appears.

The first slice should add direct tests for the resolved projection:

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
resolution emission for real schemas, starting with spirit and then any
multi-plane package that exercises imports.

## Implementation slice

The smallest correct implementation sequence is:

1. Add `SchemaResolution` in `schema-next` and move the body of
   `SchemaSource::to_asschema` into `SchemaSource::resolve`.
2. Keep `to_asschema` temporarily as compatibility conversion from
   `SchemaResolution` into `Asschema`, not as the primary owner of the work.
3. Add `RustModule::from_resolution` and `RustEmitter` methods that consume
   `SchemaResolution`.
4. Change the build driver to source round-trip, resolve, and emit Rust without
   producing `.asschema` artifacts.
5. Move tests from "lowers to Asschema" assertions to "resolves to
   SchemaResolution" assertions, while keeping old-vs-new parity tests during
   migration.
6. Remove `.asschema` files and artifact freshness only after the driver no
   longer consumes or produces them.
7. Delete `Asschema`, `AsschemaArtifact`, and `AsschemaStore` once no public
   consumer remains.

## Final operator read

Designer report 520 is directionally correct and improves the operator
position by naming the real work: resolution relocation. The only guardrail I
would add is that the pragmatic projection must stay a computed view over
`SchemaSource`, not a durable IR with artifacts. With that guardrail, the
pragmatic path is not a compromise against the psyche's "no Asschema" intent;
it is the clean way to satisfy it without making the Rust emitter perform
schema semantics.
