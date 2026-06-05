---
title: 520 — Asschema removal — design
role: designer
variant: Psyche
date: 2026-06-05
topics: [schema, asschema, nota, structural-macro, schema-next, schema-rust-next, migration, port-readiness]
description: |
  Grounded design for removing Asschema (psyche record pv61). What "remove
  Asschema" precisely means, the resolution work it does that must be
  preserved, the full consumer map, the target architecture (SchemaSource
  + a resolve() projection; emission from source; no assembled artifacts),
  the migration slices in dependency order, and the one design crux.
---

# 520 — Asschema removal — design

Psyche record `pv61`: Asschema is to be removed. This is the grounded
design, from a recon of schema-next, schema-rust-next, and the
checked-in artifacts. It supersedes the operator's "keep Asschema for
now" recommendation (report 312).

## What "remove Asschema" precisely means

Asschema is three things bundled under one name; the decision kills two
of them and relocates the third:

1. **A separate ASSEMBLED IR** — the `Asschema` struct you lower *into*,
   serialize, check in as `.asschema`, and that schema-rust-next reads.
   **This dies.**
2. **A separate LOWERING STEP** — `SchemaSource::to_asschema()`, a
   distinct assemble pass. **This dies** as a step; its work moves onto
   the source types.
3. **The RESOLUTION WORK + the resolved-type vocabulary** — inline
   hoisting, visibility, ordering, symbol paths, etc., and the
   `TypeDeclaration`/`EnumVariant`/`TypeReference`/`SymbolPath` shapes
   that carry the result. **This survives**, but as an on-demand
   *projection of the typed source* (`SchemaSource::resolve()`), not a
   separately-lowered, stored, checked-in form.

The honest framing: Rust emission fundamentally needs a *resolved* type
tree (you cannot emit Rust without knowing the hoisted inlines and
resolved references). What the decision removes is the *separate assembled
artifact and lowering step*; the resolution becomes a method on the
NOTA-native source. Schema stays just-NOTA; the resolved view is computed,
not assembled-and-stored.

## What Asschema is, and the resolution it performs

The `Asschema` struct (`schema-next/src/asschema.rs:222`) holds identity,
imports, input/output `EnumDeclaration`s, and a namespace of
`Declaration{Visibility, TypeDeclaration}`. The load-bearing part is the
**resolution the lowering does** — every one of these must land on a
source-type method:

| Resolution | What it does | Lives today |
|---|---|---|
| Inline-declaration hoisting | PascalCase field / variant-payload declarations become inlined `Private` types inserted before their parent | `source.rs:595-602`, `:774-778`; `declarative.rs:1697` |
| Visibility assignment | namespace declarations are `Public` unless inlined (`Private`) | `asschema.rs:546-552`; `source.rs:1143-1153` |
| Ordering / flattening | inlines precede parent; namespace in source order | `source.rs:117-129`; `declarative.rs:835-849` |
| Symbol-path resolution | `SymbolPath` → `Type`/`RootVariant`/`Field`/`EnumVariant` position | `asschema.rs:139-142`, `:344-387` |
| Newtype/Alias collapse | single-field struct → `Newtype` | `source.rs:493-497` |
| Derived field naming | PascalCase → snake_case (`Vec Topic` → `topic_vector`) | `asschema.rs:41-56` |
| Variant payload resolution | bare variant name resolved against namespace | `source.rs:756-761`, `:1049-1052` |
| Reserved-scalar validation | `String`/`Integer`/`Boolean`/`Path` are scalar leaves; rejected as namespace names | `asschema.rs:961-963`; `engine.rs:797-800` |

## The consumer map

| Consumer | Uses Asschema for | Replacement |
|---|---|---|
| **`RustEmitter::emit_file(&Asschema)`** (schema-rust-next `lib.rs:51`) | **the load-bearing one** — Rust emission; `RustModule::from_asschema` reads `namespace()`, `input_and_output()`, `identity()`, `resolved_imports()` | consume `SchemaSource` + its `resolve()` projection; `RustModule::from_source` |
| `GenerationDriver` (schema-rust-next `build.rs:399`) | build-time lower→emit | lower source → resolve → emit; no Asschema |
| `AsschemaStore` (schema-next `store.rs`) | rkyv storage in redb | rkyv on the typed source / resolved projection |
| schema-next tests (`symbol_path`, `collections`, …) | `SymbolPath` from lowered Asschema | derive `SymbolPath` from source directly (same paths) |
| `upgrade.rs` `SchemaEdit` | edits applied to Asschema | edits on source declarations |
| `spirit/build.rs` + 10 checked-in `.asschema` files (spirit, cloud, domain-criome, upgrade, signal-cloud, schema-next core) | freshness check / emission input | regenerate from `.schema` on demand; drop `.asschema` |
| schema-rust-next `big_emission` tests | load `.asschema` then emit | load `.schema`, decode to source, emit |

## The decode side is mostly already there

The recon's good news: **most `Source*` types already decode by structure**
via inherent `from_block` shape-matching — `SourceImports`,
`SourceRootEnum`, `SourceNamespace`, `SourceDeclarationValue`,
`SourceStructBody`, `SourceEnumBody`, `SourceReference`. Only
`SourceVariantSignature` uses the formal `#[derive]`/trait today. So the
*type-directed decode* the psyche wants is largely in place. **The real
removal work is not decode — it is relocating the resolution and rewiring
emission.**

## Target architecture

```
authored .schema  (NOTA)
      │  structural-macro decode  (type-directed; already mostly here)
      ▼
  SchemaSource    (the typed NOTA-native representation — the source of truth)
      │  .resolve()  ← the resolution work, as METHODS on the source types
      ▼
  ResolvedSchema  (the resolved type tree: declarations + visibility +
      │            symbol paths — computed on demand, NOT a stored IR)
      ▼
  schema-rust-next  RustModule::from_source / from_resolved  →  Rust
```

`Asschema`, `to_asschema()`, `AsschemaArtifact`, `AsschemaStore`'s
Asschema coupling, and the `.asschema` files all leave. `SchemaSource`
plus an on-demand `resolve()` projection is what remains; emission reads
that projection.

## Migration slices (dependency order)

| # | Slice | Scope | Risk |
|---|---|---|---|
| 1 | **Resolution onto source** — move hoisting/visibility/ordering/symbol-path/collapse/naming/payload/validation from `to_asschema()` onto `Source*` methods; add `SchemaSource::resolve() -> ResolvedSchema` | schema-next, internal | high (subtle interplay; tests are the net) |
| 2 | **Emission from source** — `RustEmitter::emit_file` takes the resolved projection, not `&Asschema`; `RustModule::from_source` | schema-rust-next | high (load-bearing) |
| 3 | **Build + artifacts** — `GenerationDriver` lowers source→resolve→emit; delete `.asschema` files; drop `.asschema` freshness in spirit/cloud/upgrade/domain-criome build.rs | schema-rust-next + 5 repos | medium (multi-repo) |
| 4 | **Storage / upgrade / tests** — `AsschemaStore`, `SchemaEdit`, symbol-path tests onto source | schema-next | medium |
| 5 | **Delete** — remove `Asschema`, `to_asschema`, `AsschemaArtifact`, `.asschema` readers | schema-next | low (once 1–4 land) |
| 0 | *(optional, parallel)* migrate remaining `Source*` inherent `from_block` to `#[derive(StructuralMacroNode)]` for decode uniformity | schema-next | low |

The safety net for slices 1–2 is the existing schema-next test suite plus
**byte-identical Rust emission**: lower a real `.schema` (e.g. spirit's
three planes) the old way and the new way, and diff the generated `.rs`.
If the bytes match, the resolution relocation is faithful.

## The hard parts

- **The resolution interplay** (slice 1) is the genuine difficulty —
  inline hoisting + visibility + ordering are coupled in
  `to_asschema()`/`declarative.rs`. Relocating them onto source methods
  without changing emitted output is where the care goes.
- **Multi-repo artifacts** (slice 3): 10 `.asschema` files across 5 repos
  are freshness-checked. Dropping them is coordinated work touching each
  repo's build.
- **`SymbolPath` parity**: paths derived from source must equal those
  derived from Asschema today (tests pin this).

## The one design crux for you

What does schema-rust-next ultimately consume?

- **(Pragmatic)** A `resolve()` projection — the resolved declaration
  vocabulary survives (renamed out of the "Asschema" identity), computed
  on demand from the source. Less churn in the emitter; the resolution
  stays type-safe. *My recommendation.*
- **(Strong)** No resolved-tree type at all — the emitter walks the
  `SchemaSource` tree directly, resolving inline as it emits. Maximally
  "schema is just NOTA," but it pushes resolution into the emitter and
  rewrites more of schema-rust-next.

Both kill the assembled IR, the lowering step, and the `.asschema`
artifacts. They differ only in whether a resolved-type vocabulary exists
as a projection output (pragmatic) or is dissolved into the emitter
(strong). I recommend **pragmatic** — it removes everything the decision
names while keeping the resolution type-checked and the emitter change
contained.

## Cross-lane plan

schema-next and schema-rust-next `main` are operator-owned; this is a
multi-repo migration the operator integrates. My next step as designer:
prototype the **spine** on a feature branch — slice 1 (`resolve()` on
source) + slice 2 (`RustModule::from_source`) — and prove it with the
byte-identical-emission diff on spirit's schema. The operator owns landing
slices across `main`. The decision is captured (`pv61`) so the operator
sees the reversal of their keep-Asschema recommendation.

## Where it lives

- This design: report 520.
- Decision: Spirit record `pv61`. Lineage: `lcwu` (conditional), `i0e6`
  (the type-directed clarification), `pv61` (the removal decision).
- Structural-macro substrate: branch `structural-macro-nodes`
  (`add64661`), reports 517/518/519.
