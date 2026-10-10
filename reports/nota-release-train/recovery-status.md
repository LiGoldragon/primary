# NOTA Release Train — Recovery Status (LanguageEngine/NotaReleaseTrain)

Recovery conductor: Opus 4.8 generalist. Inherited the live lane, its five claims,
and the dangling witness working copy from the dead predecessor (Recovery register
returned `RecoveryInherited`). Bar: working programs.

This report is the Manager pickup point for the Stage 4 scope decision. The lane
delivered every safely-in-scope item and reached consistent green on main
workspace-wide; the enumerated Stage 4 "dead set" was found to be mostly LIVE code,
which is returned below as a scope/authority blocker rather than executed blind.

## Landed chain (verified, unchanged by this lane — inherited green)

- nota main `7d0651a0` — next-generation grammar integrated (dotted application,
  `{}`/`[]`/`()` delimiter reshuffle, `(| |)` multiline, `Map.(k.V …)`, dotted
  options/variants). cargo test offline: all suites green (incl. still-present
  legacy tests).
- schema-language main `eccc2262` — macro-node expansion pass dropped from
  lowering (`src/expansion.rs` deleted); native kind-dispatch is the sole lowering.
- schema-engine main `0ec95c19` — re-pins schema-language `eccc2262`.
- core-schema main `8507b656` — native next-gen (untouched).
- schema-rust main `79a9e5c9` — already pins next-gen nota `7d0651a0` and uses
  next-gen CLI syntax; cargo test offline green. (Handoff's "still old syntax at
  tests/cli.rs:73" was STALE — the committed tree is already next-gen.)

## Stage 2 — consumer consistency: NO red window exists (verified)

The manager's premise ("~122 consumers floating nota branch=main may be RED on
main") is disproven by Cargo lockfile semantics. A `git` dependency with
`branch=main` still resolves to a fixed rev recorded in `Cargo.lock`; a consumer
builds against its locked rev regardless of where nota's `main` points. nota's
main advancing to `7d0651a0` therefore cannot turn a rev-locked consumer red.

Distinct nota revs across all `*/Cargo.lock` (top hits): `ce7c564d` ×86,
`bea7e284` ×76, `f8de7a51` ×42, `d25c08a8` ×38 — all OLD-grammar ancestors of the
`next-gen` branch. Only the next-gen rev `7d0651a0` appears, in exactly these
repos: nota consumers **logos-runtime, schema-engine, schema-language, schema-rust,
language-engine-witness**; plus **signal-frame** on `nota-next.git` next-gen tip
`18e2e8d0`.

Empirical green (cargo test --offline):
- logos-runtime `b6ca1daf` — green. (No nota text surface; rkyv wire only.)
- signal-frame `f46872e7` — green, 20-test binary incl. NOTA text fixtures. Its
  main commit is literally "align NOTA text fixtures with pinned codec".
- schema-rust `79a9e5c9` — green.
- nota `7d0651a0` — green.

The ~116 remaining consumers lock OLD-grammar nota and are unaffected/green. **No
consumer golden migration was needed; the workspace is consistent green on main.**

## Stage 3 — macro-supersession audit (recorded)

Claim: native kind-dispatch supersedes every `MacroRegistry::with_schema_defaults`
built-in macro on the live lowering path.

Evidence — the sole live lowering path never consults the registry:
`SchemaEngine::lower_document_with_resolver` (engine.rs:539) →
`SchemaSource::from_document` (engine.rs:559) →
`lower_schema_source_with_resolver`. `self.registry` is read only by the public
`registry()` getter (engine.rs:580); it is never consulted while lowering. The
registry is still *constructed* in the engine default (engine.rs:405
`with_schema_defaults()`) but drives nothing.

Each `with_schema_defaults` built-in (engine.rs:586–609) —
`root_imports/input/output/namespace`, `namespace_declaration`, `struct_fields`,
`enum_variants`, `type_reference`, and the `RootImports/RootEnum/RootNamespace/
KeyValueDeclaration` handlers — is superseded by the typed-source archive built
directly from the parsed next-gen document (Vector/Optional/Map as core-schema
kinds). Confirmed by the landing commit `eccc2262` ("Native next-gen kind dispatch
is now the sole lowering semantics … supersedes the retired MacroExpansionPass;
27 suites green; schema-engine live LegacySchemaIngest::migrate_text green") and by
the full offline green above. **Supersession proven.**

## Stage 4 — dead-code removal: BLOCKED (scope/authority — for the Manager)

The enumerated dead set is largely LIVE and cannot be deleted as written without
breaking working programs (the bar). The cleanly-separable dead code (expansion.rs,
the pass-firing tests, the schema-rust oracle byte-comparison) was ALREADY removed
by the predecessor and the peer ProvenanceAndWitnessRetirement lane. What remains
is a thin dead dispatch/registry layer fused into the live codec.

Precise dead/live map (verified by call-graph tracing):

LIVE — must NOT delete (the enumeration says to; doing so breaks the schema engine):
- `nota/src/macros.rs` is ~90% the LIVE `StructuralMacroNode` codec runtime. The
  `nota_derive` `StructuralMacroNode` derive (derive/src/lib.rs:688–729) generates
  decode code using `StructuralVariantSet::dispatch`, `MacroCandidate`, `MacroMatch`
  (macros.rs:463). That dispatch uses `Pattern`, `PatternElement`,
  `PositionPredicate`, `StructuralVariant`, `AtomShape`, `BlockShape`,
  `DelimitedShape`, `SigilSpec`, `MacroDelimiter`, `CaptureName`, `MacroObjectCount`.
  All LIVE.
- The live schema-language typed-source decode depends on this codec:
  `SourceVariantSignature/Name/Payload::from_structural_block` (source.rs ~2570–2856,
  invoked by `from_document` at source.rs:2713–2714) and `Name`/`TypeReference`
  `impl nota::StructuralMacroNode` (schema.rs:135, 2513) via
  `from_structural_candidate`/`MacroCandidate`.
- `MacroContext` (schema-language) is live (engine lower path calls
  `remember_structure_header`).

DEAD sliver (fused into the live files; removal is a careful cross-repo refactor):
- nota: `MacroRegistry` + `MacroNodeDefinition` (macros.rs:985/115) — used only by
  the `lib.rs` re-export, `tests/macro_nodes.rs`, and schema-language's dead
  registry wrapper. `tests/macro_nodes.rs`, `tests/fixtures/macro-node/
  strict-namespace.nota`. (`tests/operator_271_closed_claims.rs` is NOT dead — it
  witnesses live derive-source shape; keep/port, do not delete.)
- schema-language: its own `MacroRegistry`, `MacroNodeDefinition`, `MacroPosition`,
  `SchemaMacroHandler`, `MacroObject`, `MacroOutput`, `MacroPair`, `MacroDispatch`,
  `with_schema_defaults`, the engine.rs macro handlers (`RootImportsMacro`,
  `RootEnumMacro`, `RootNamespaceMacro`, `KeyValueDeclarationMacro`), and the
  declarative macro library (`MacroLibrary`, `SchemaMacro`, `MacroPattern`,
  `MacroTemplate`, `DeclarativeSchemaMacro`, `into_macros`) — none reachable from
  the live lower path (source.rs/schema.rs/view.rs/core.rs do not reference them).
  Plus dead tests (`design_examples.rs`, `legacy_reference_pipeline.rs`,
  `macro_exploration.rs`, `lowering.rs` registry cases, `typeref_structural_macro.rs`
  — each to be triaged for live-behavior witnesses before deletion).

Why this is a blocker, not routine deletion:
1. The dead sliver is type-level fused into the live codec files (macros.rs,
   declarative.rs, engine.rs, schema.rs, source.rs — ~400KB), so excision is a
   careful surgical refactor, not the "straightforward" file deletion the psyche
   ruling assumed. This is the plausible cause of the predecessor's 3146s stall.
2. It removes PUBLIC exports from core crates (schema-language: `MacroRegistry`,
   `MacroLibrary`, `SchemaMacro`, `MacroPosition`, `SchemaMacroHandler`, …; nota:
   `MacroRegistry`, `MacroNodeDefinition`) consumed elsewhere (`schema`,
   `schema-structural-pipe-retirement`). That is a material public-contract change;
   the psyche accepted "remove dead code" but not this specific API break, and the
   enumeration that framed it was factually wrong (named live code for deletion).
3. engine.rs:574–580 deliberately retains the registry as "the seam a future
   archive-time type-reference-macro expansion would consult" — a documented
   intentional retention that directly contradicts "remove all dead code". This
   conflict is the psyche's to settle, not mine to resolve by taste.

Recommendation: scope a dedicated careful-excision lane (general-code-implementer +
rust-auditor) with the map above, compiler+tests+witness as the green oracle, in
order: (a) remove schema-language's registry/handler/declarative-library glue while
still pinned to nota `7d0651a0` → cargo green → push; (b) remove nota's
`MacroRegistry`/`MacroNodeDefinition` + `macro_nodes.rs` + fixture, bump nota
version → push; (c) re-pin schema-language → schema-engine → witness, run witness
flake checks → green. OR surface to the psyche that the residual "dead code" is a
thin dispatch layer fused to the live StructuralMacroNode codec and confirm the
public-API break before cutting. Do NOT execute the manager's file-level
enumeration verbatim — it deletes live code.

## Epic

primary-56d1.5 (nota settled-wave grammar migration) and .6 (delimiter-reshuffle
wave) are ALREADY CLOSED (✓) with landed evidence (nota main `7d0651a0`). No tracker
advancement was required. Stage-4 dead-code removal maps to no open .5/.6 work; it
belongs under a new/re-opened item if the excision lane is scoped.

## Witness

Predecessor's dangling dirty working copy completed and verified: re-pin to the
final landed chain (schema-engine `0ec95c19`, transitively schema-language
`eccc2262`), flake.nix/flake.lock/Cargo.toml/Cargo.lock consistent, no stale
`bf05d105` refs. Committed + pushed: language-engine-witness main = `1cc03b99`
(from `3ca879b7`). Witness `test` nix check GREEN on the final pins:
`nix build .#checks.x86_64-linux.test` exit 0; e2e
`one_document_pushes_through_four_processes_and_recovers` passed (four real daemons,
compile + public-surface behavior, durable restart recovery) under the
working-programs bar. Corroborating cargo `--offline`: nota, schema-language (27
suites), schema-rust, logos-runtime, signal-frame all green.
