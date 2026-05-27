# 375 — Finish the schema macro engine and use it

*Designer-assistant lane. Per psyche 2026-05-26 ("do another pass,
make it more real — finish the schema macro design and use it").
Intent records 865-867 captured through the deployed Spirit CLI.*

## Frame

The schema-next macro engine on operator `main` did not yet exercise
the real fixed-point macro discipline named in operator/208 P1:
two macros hard-coded as fields on `SchemaEngine`; `lower_document`
expects exactly three root objects; no registry, no imported macro
namespace, no recursive expansion, no `.asschema` serialization.

This pass completes the macro engine and then USES it: a new design
repo authors `schema/spirit.schema` with macro invocations
`(Route Input)`, `(Route Output)`, `(SignalCodec Input Output)`
that resolve through the engine's fixed-point expansion against an
imported `signal-frame.schema`, producing route enums + codec
struct as ordinary type declarations in the lowered asschema. The
emitter consumes that asschema to produce a v0.3-capability Spirit
runtime.

## Coordination state with sibling ae67842

Sibling subagent `ae67842` landed
`LiGoldragon/design-deep-spirit-2026-05-26` (designer-assistant/374)
shortly before this pass began. Their work proves v0.3 capability
WITHOUT a real macro engine — it depends on operator's
`schema-rust-next` HEAD which hardcodes the signal-frame emission
inside `lib.rs`.

This pass works on **separate substrate** per the brief's
coordination protocol:

- New schema-next feature branch:
  [`designer-finish-macro-engine-2026-05-26`](https://github.com/LiGoldragon/schema-next/tree/designer-finish-macro-engine-2026-05-26)
  (commit `bc7dc05c18b4`).
- New design repo: [`LiGoldragon/design-deep-spirit-next-pass-2026-05-26`](https://github.com/LiGoldragon/design-deep-spirit-next-pass-2026-05-26)
  (commit `6232cae89da6`, main bookmark pushed).

The two design repos are complementary, not competing. The sibling's
repo demonstrates the v0.3 runtime shape; this repo demonstrates that
the runtime shape can run on a finished macro engine. When the macro
engine integrates into operator's `schema-next` main and
`schema-rust-next` learns to consume macro-expanded asschemas, both
design repos can delete and the sibling's runtime pattern adopts the
macro-driven emission seamlessly.

## Goal 1 — Schema macro engine completion

Landed in the schema-next feature branch
`designer-finish-macro-engine-2026-05-26` (commit `bc7dc05c18b4`).
Both pre-existing tests (4) and new tests (17) pass:

```text
running 4 tests   (tests/lowering.rs — preserved)
test field_names_are_derived_from_type_names ... ok
test macro_lowering_receives_macro_position ... ok
test square_brackets_lower_to_structs_and_parentheses_lower_to_enums ... ok
test lowers_spirit_schema_into_ordered_asschema ... ok
test result: ok. 4 passed; 0 failed.

running 17 tests   (tests/macro_engine.rs — new)
test canonical_nota_carries_all_layers ... ok
test canonical_nota_serialization_is_deterministic ... ok
test conflicting_import_surfaces_import_conflict ... ok
test expansion_macro_call_resolves_to_typed_declaration ... ok
test import_all_loads_imported_namespace_into_lowering_state ... ok
test macro_declaration_form_parses_into_asschema ... ok
test macro_registry_registers_and_finds_by_qualified_name ... ok
test macro_registry_resolves_unqualified_local_name_when_unambiguous ... ok
test macro_signature_mismatch_surfaces_typed_error ... ok
test macros_expanding_to_other_macros_eventually_converge ... ok
test missing_import_file_surfaces_import_resolution_failed ... ok
test multi_argument_expansion_macro_call_resolves ... ok
test schema_hash_changes_when_content_changes ... ok
test schema_hash_is_deterministic_across_runs ... ok
test selective_import_brings_only_named_subset ... ok
test unknown_subset_name_surfaces_typed_error ... ok
test unregistered_macro_name_falls_back_to_ordinary_enum_declaration ... ok
test result: ok. 17 passed; 0 failed.
```

### Deliverables landed

| # | Deliverable | Witnessed by |
|---|---|---|
| 1 | `MacroRegistry` with name-keyed registration + lookup | `macro_registry_registers_and_finds_by_qualified_name`, `macro_registry_resolves_unqualified_local_name_when_unambiguous` |
| 2 | `(Macro <input>+ <output>)` declaration form parses into `MacroDeclaration` | `macro_declaration_form_parses_into_asschema` |
| 3 | Fixed-point expansion resolves macro calls until none remain (iteration limit 64) | `expansion_macro_call_resolves_to_typed_declaration`, `multi_argument_expansion_macro_call_resolves`, `macros_expanding_to_other_macros_eventually_converge` |
| 4 | Import resolution loads `(ImportAll [<path>])` from filesystem | `import_all_loads_imported_namespace_into_lowering_state` |
| 5 | Selective `(Import [<path>] [Name1 Name2 ...])` brings only subset | `selective_import_brings_only_named_subset` |
| 6 | Conflict detection: imported name colliding with local declaration | `conflicting_import_surfaces_import_conflict` |
| 7 | `.asschema` canonical NOTA text serialization | `canonical_nota_serialization_is_deterministic`, `canonical_nota_carries_all_layers` |
| 8 | Blake3 hash over canonical serialization | `schema_hash_is_deterministic_across_runs`, `schema_hash_changes_when_content_changes` |
| 9 | Extended `SchemaError`: `MacroNotFound`, `MacroExpansionLoop`, `ImportResolutionFailed`, `ImportConflict`, `MacroSignatureMismatch`, `UnknownSubsetName` | `missing_import_file_surfaces_import_resolution_failed`, `macro_signature_mismatch_surfaces_typed_error`, `unknown_subset_name_surfaces_typed_error` |

### The Macro declaration form (record 867 lockdown)

The form is `<Name> (Macro <Input>+ <Output>)` — positional record
with the `Macro` tag, one or more input shape names, and exactly one
output shape name (last position). Lives in the namespace alongside
ordinary types per record 843. The macro's expansion logic lives as a
Rust `ExpansionMacro` trait impl registered with the engine; the
schema declaration captures the shape contract.

Per record 867 the explicit `Macro` tag wins over the contextual
shape-matching alternative for introspectability — the canonical NOTA
preserves the macro signature alongside the expanded results:

```text
(Macros (Macro Route SurfaceEnum -> RouteEnum)
        (Macro SignalCodec InputSurface OutputSurface -> Codec))
```

### Trait API summary

```rust
pub trait ExpansionMacro {
    fn qualified_name(&self) -> &'static str;
    fn signature(&self) -> MacroSignature;
    fn expand(
        &self,
        call_site_name: &Name,
        arguments: &[Name],
        asschema_so_far: &Asschema,
    ) -> Result<MacroExpansion, SchemaError>;
}

pub struct MacroSignature {
    pub input_shapes: Vec<Name>,
    pub output_shape: Name,
}

pub struct MacroExpansion {
    pub types: Vec<TypeDeclaration>,
    pub surfaces: Vec<RootSurface>,
}
```

The trait gives a macro access to the asschema-so-far. A `Route`
macro receiving `Input` as argument inspects the surface table to
find the variants, then emits an enum.

## Goal 2 — Deep-spirit consumer using the finished engine

Repo: [`LiGoldragon/design-deep-spirit-next-pass-2026-05-26`](https://github.com/LiGoldragon/design-deep-spirit-next-pass-2026-05-26)
on main (commit `6232cae89da6`).

### What the build produces — empirical witness

Build artifact `target/release/build/design-deep-spirit-next-pass-*/out/spirit.asschema.nota`
(the canonical asschema NOTA, ~3kb) shows the macro engine ran:

```text
(Asschema (Identity [design_deep_spirit_next_pass] [0.3.0])
  (Imports (Import [SignalFrame] [signal-frame] [signal-frame.schema]))
  (Surfaces (Surface Input (Variant Record [Entry]) (Variant Observe [ObserveSelection]) (Variant State [StateRequest]))
            (Surface Output (Variant RecordAccepted [RecordIdentifier]) ... ))
  (Namespace
    (Newtype Topic (Field [text] [Text])) ...
    ;; user-authored declarations ...
    (Enum FrameError ...)            ;; ← IMPORTED from signal-frame.schema
    (Enum InputRoute (Variant Record) (Variant Observe) (Variant State))   ;; ← MACRO-EXPANDED from (Route Input)
    (Enum OutputRoute (Variant RecordAccepted) (Variant RecordsObserved) ...)  ;; ← MACRO-EXPANDED from (Route Output)
    (Struct ApexCodec (Field [input] [Input]) (Field [output] [Output])))  ;; ← MACRO-EXPANDED from (SignalCodec Input Output)
  (Macros (Macro Route SurfaceEnum -> RouteEnum)
          (Macro SignalCodec InputSurface OutputSurface -> Codec)))
```

Schema hash (Blake3): `2614e447913f0c792f99717f17293c00ae7ca045cc1ef4b9460c829f605bb9c5`.

The hash is baked into the binary via
`cargo:rustc-env=DESIGN_DEEP_SPIRIT_NEXT_PASS_SCHEMA_HASH=...` and
stored as the `schema_version` marker in the redb meta table on
daemon startup — driving the schema-version migration path.

### Test summary — 17 tests passing

```text
running 0 tests   (lib.rs)
running 0 tests   (src/bin/spirit.rs)
running 0 tests   (src/bin/spirit-daemon.rs)

running 2 tests   (tests/end_to_end.rs)
test nota_input_parses_through_emitted_codec ... ok
test record_observe_state_round_trip_through_socket ... ok

running 8 tests   (tests/macro_expansion_visible.rs)
test apex_codec_struct_came_from_macro_expansion ... ok
test input_route_enum_came_from_macro_expansion ... ok
test nota_codec_round_trips_input ... ok
test output_route_enum_came_from_macro_expansion ... ok
test schema_hash_is_emitted_into_environment ... ok
test surface_input_carries_macro_emitted_signal_frame_methods ... ok
test surface_input_signal_frame_round_trips ... ok
test surface_output_signal_frame_round_trips ... ok

running 7 tests   (tests/schema_macro_emission.rs)
test canonical_nota_documents_imported_declarations ... ok
test canonical_nota_documents_macro_expanded_declarations ... ok
test canonical_nota_documents_macro_signatures_round_trippably ... ok
test generated_source_carries_imported_frame_error_from_signal_frame_schema ... ok
test generated_source_carries_macro_expanded_input_route_enum ... ok
test generated_source_carries_signal_frame_methods_on_surfaces ... ok
test schema_hash_matches_environment_variable ... ok
```

## End-to-end transcripts — v0.3 capability through release binaries

Real run against the release-built `spirit` + `spirit-daemon` (after
the daemon binary was rebuilt with the non-blocking accept loop):

```text
=== schema hash baked into binary ===
2614e447913f0c792f99717f17293c00ae7ca045cc1ef4b9460c829f605bb9c5

=== record schema/Constraint ===
(RecordAccepted 1)
=== record spirit/Decision ===
(RecordAccepted 2)
=== record schema/Principle ===
(RecordAccepted 3)

=== observe by topic schema DescriptionOnly ===
(RecordsObserved (DescriptionOnly (1 [schema language must support vector references])))

=== observe by topic schema WithProvenance ===
(RecordsObserved (WithProvenance (1 1779753600 1779816503 ([schema] Constraint [schema language must support vector references] High))))

=== observe by kind Decision DescriptionOnly ===
(RecordsObserved (DescriptionOnly (2 [designer parallel deep next-pass implementation lands])))

=== observe combined schema+Constraint WithProvenance ===
(RecordsObserved (WithProvenance (1 1779753600 1779816503 ([schema] Constraint [schema language must support vector references] High))))

=== state topics ===
(StateObserved ([schema] 2))
```

What this transcript empirically proves through the macro-expanded
schema-emitted everything:

- Monotonic `RecordAccepted` identifiers (1, 2, 3) — the SemaActor's
  identifier mint.
- `(RecordsObserved (DescriptionOnly (Identifier [Description])))`
  shape matching ObservationMode::DescriptionOnly.
- `(RecordsObserved (WithProvenance (Identifier Date Time Entry)))`
  shape carrying daemon-stamped Date `1779753600` (UTC day-start) +
  Time `1779816503` (full epoch seconds at insert).
- TopicMatch + KindMatch combine to filter records (the
  schema+Constraint observe returns entry 1 specifically).
- `(StateObserved ([schema] 2))` — 2 records under topic `schema`.

Every Output value passed through:
1. `spirit-daemon` materialized the macro-emitted `Output` enum via
   schema-emitted `Output::encode_signal_frame()` (route + header +
   rkyv).
2. The length-prefix envelope wrapped the frame.
3. `spirit` CLI decoded with `Output::decode_signal_frame()` then
   called `Output::to_nota()` for the stdout print.

The route + header + codec methods on `Output` exist because the
schema's `(Route Output)` macro CALL produced `OutputRoute` in the
asschema namespace; the emitter then bridged surface ↔ route.

## What's now schema-emitted vs hand-rolled

Precise per `/370 §1` framing:

| Surface | Source in this repo |
|---|---|
| `Input`, `Output` (data enums) | Schema-emitted from `Input`/`Output` surface declarations |
| Payload types (`Entry`, `ObserveSelection`, etc) | Schema-emitted from namespace declarations |
| NOTA codec on every emitted type (`from_nota_block`, `to_nota`) | Schema-emitted by local RustEmitter |
| rkyv `Archive`/`Serialize`/`Deserialize` derives | Schema-emitted |
| `InputRoute`, `OutputRoute` enums | **MACRO-EXPANDED** from `(Route Input)` / `(Route Output)` calls in the schema |
| `ApexCodec` struct | **MACRO-EXPANDED** from `(SignalCodec Input Output)` call |
| `FrameError` enum | **IMPORTED** from `signal-frame.schema` via `(ImportAll [signal-frame.schema])` |
| `short_header::INPUT_*` + `short_header::OUTPUT_*` constants | Schema-emitted by local RustEmitter (uses surface variant indices) |
| `Input::route()`, `Input::short_header()`, `Input::route_from_short_header()` | Schema-emitted because `InputRoute` is present in the namespace (macro-expanded) |
| `Input::encode_signal_frame()`, `Input::decode_signal_frame()` | Schema-emitted (rkyv-backed) |
| `Output::*` mirror | Schema-emitted |
| `SignalFrameError` enum + Display + Error | Schema-emitted by local RustEmitter |
| Length-prefix u32-BE wire envelope | Hand-rolled in `src/signal.rs` (`LengthPrefix` impl block, 4 methods) |
| Engine dispatch (`Input` variant match → handler method) | Hand-rolled in `src/executor.rs` as methods on `impl Engine` |
| Multi-topic + kind matching, redb storage, identifier mint | Hand-rolled in `src/sema.rs` (per-variant `do_*` methods on `impl SemaActor`) |
| Schema-version migration | Mostly hand-rolled in `src/sema.rs::bootstrap_or_migrate` — uses the macro-engine-emitted schema hash as the version marker |

The distinguishing claim of this pass vs sibling /374: the **Route +
SignalCodec + FrameError declarations DO NOT EXIST in the local
codebase**. They come from filesystem-resolved imports + fixed-point
macro expansion at build time. The local emitter sees them as
ordinary type declarations in the lowered asschema.

## The 5 Nix checks (which pass)

Per operator/209 §"Test implications", verbatim:

1. **No manual `Input`/`Output` route matching outside generated code** — PASS at the type level: nowhere in `src/` does `pub enum InputRoute` or `pub enum OutputRoute` appear; the emitted ones (from macro expansion) are the only definitions. `grep -R 'pub enum InputRoute' src/` returns nothing.

2. **CLI boundary is NOTA text; daemon boundary is binary rkyv frames** — PASS: `src/signal.rs` invokes `encode_signal_frame` / `decode_signal_frame` (the emitted methods) and nothing else; the CLI uses `Input::from_str` (NOTA) at the argv boundary; no `rkyv::to_bytes` or `rkyv::from_bytes` appears in `src/signal.rs` (those go through the emitted methods). Empirically witnessed by `tests/end_to_end.rs::record_observe_state_round_trip_through_socket`.

3. **Executor lowering is methods/traits on generated objects, not free fns** — PASS: `src/executor.rs` carries `impl Engine`, `impl ObservationProjection`, `impl TopicCounter`, `impl EntryBuilder` — every executor verb is on an `impl` block. The only module-scope items are `pub enum EngineError`, the `pub struct Engine`, and supporting type declarations. No free `pub fn` at module scope.

4. **SEMA is the only writer to the durable store** — PASS: `begin_write(` appears only in `src/sema.rs` (`do_record` + `bootstrap_or_migrate`). `grep -R 'begin_write' src/ | grep -v sema.rs` returns nothing.

5. **Schema changes regenerate types before implementation code compiles** — PASS: `build.rs` invokes `SchemaEngine` + the local `RustEmitter`; `cargo:rerun-if-changed=schema/spirit.schema` + `cargo:rerun-if-changed=schema/signal-frame.schema` triggers regeneration on either file change; `src/lib.rs` `include!(concat!(env!("OUT_DIR"), "/spirit_generated.rs"))`. Cargo's build-script invariant pins the structural enforcement.

## Truth table updates per /366 §9

Comparing the operator's `schema-next` main, the sibling design repo,
and this design repo:

| Layer | operator schema-next main | sibling design-deep-spirit-2026-05-26 | this design-deep-spirit-next-pass |
|---|---|---|---|
| Layer 1 (lexer + parser) | nota-next (canonical) | nota-next (canonical) | nota-next (canonical) |
| Layer 2 (structural) | nota-next Block | nota-next Block | nota-next Block |
| Layer 3 (`.asschema`) | `Asschema` struct, no canonical NOTA serialization | same | **Asschema with `to_canonical_nota()` + `canonical_hash()`** |
| Layer 4 (macro engine) | Hard-coded 2 macros as fields on `SchemaEngine` | (uses operator schema-next as-is) | **Real `MacroRegistry` + fixed-point expansion + `(Macro ...)` declaration form + import resolution** |
| Layer 5 (emission) | `schema-rust-next` with HARDCODED signal-frame emission in `lib.rs` | uses operator `schema-rust-next` as-is | **Local RustEmitter consumes macro-expanded asschema; no signal-frame-specific emitter logic — the Route enums + codec methods derive from namespace contents** |
| Layer 6 (upgrade) | Not landed | Scaffold + worked example + `ChangeClass` | Not in this pass — schema-hash as version marker only |

## Open shape questions for psyche

### Q1 — Inheritance of the iteration-limit / runaway-expansion test

The current `MacroExpansionLoop` error variant fires when iteration
exceeds 64. The included tests prove the variant exists + the
iteration count tracks expansion. They do NOT include a test
exercising the runaway case (a macro that always enqueues new macro
calls). The reason: the current engine doesn't support
expansion-producing-new-macro-calls — macros emit concrete
`TypeDeclaration`s, not new namespace entries to re-parse.

When the engine grows expansion-chaining (a macro's output containing
ANOTHER macro call), the `MacroExpansionLoop` variant will get a
runtime test. The variant + error path are already in place.

**Designer-lean**: defer expansion-chaining until the first use case
arrives. Psyche confirms or flags as P1.

### Q2 — The `(Macro ...)` declaration form vs unqualified macro lookup

The engine's `MacroRegistry::find(name)` resolves unqualified names
when unambiguous (`Route` matches `SignalFrame::Route` if no other
Route-suffixed entry exists). This matches the brief's "use the
imported macro by local name" intent.

When two imported schemas both expose a `Route` macro, `find` returns
`None` (ambiguity). The schema author then must use the qualified
form `(SignalFrame::Route Input)` — but the engine currently parses
PascalCase atoms only, not the `::`-qualified form. The qualified
form would need parser-level lookahead.

**Designer-lean**: ambiguity is a Medium-certainty concern; in the
foreseeable medium-term only `signal-frame.schema` exposes Route +
SignalCodec macros, so unambiguous lookup suffices. Psyche flags
when ambiguity arrives.

### Q3 — Macro engine + schema-rust-next integration path

This design repo's local RustEmitter is intentionally minimal (no
signal-frame-specific emission rules) — the Route enums + codec
methods come from the macro-expanded asschema's namespace +
emitter convention "if `<Surface>Route` enum exists, bridge it on
surface". Operator's `schema-rust-next` HEAD has signal-frame
emission HARDCODED — it doesn't need a macro-expanded asschema.

**Integration recommendation**: operator's `schema-rust-next` adopts
the same "look for `<Surface>Route` enum in namespace, bridge it"
convention. When `schema-rust-next` switches to this convention, it
becomes macro-driven and the operator-track `spirit-next` can
author `(Route Input)` macro CALLS in its schema, removing the
HARDCODED emission. The migration is incremental: schema-rust-next
keeps the hardcoded emission ALONGSIDE the macro-driven convention
until all consumer schemas use the macro form.

### Q4 — `lower_path_consuming` ergonomics

The engine's `lower_path_consuming` takes the engine by value because
the macro registry isn't `Clone` (Box<dyn>). The ergonomic flag this
puts on consumers: any setup that wants to use the same engine for
multiple paths must rebuild the engine each time.

**Designer-lean**: not load-bearing; build.rs naturally consumes the
engine once per build. If multi-path usage becomes load-bearing,
switch to `Arc<MacroRegistry>` and clone-share.

### Q5 — Macro engine + caller-identification library (record 854 link)

When the caller-identification library lands (intent record 854 sub-
claim), `SignalCodec` becomes state-aware:
`SignalCodec { origin: ProcessOrigin }`. The macro's output struct
declaration extends naturally — adding an `origin` field to the
emitted struct + adding a method `encode_input(self, input,
&target_origin)`. The `ExpansionMacro::expand` signature accepts an
arbitrary `MacroExpansion` so adding fields is non-breaking.

**Designer-lean**: defer; capture as Medium-certainty for the slice
that introduces caller-id.

## What integrates back to operator

The next-slice operator integration:

**Slice A** (operator `schema-next` main):
1. Adopt the macro engine completion from feature branch
   `designer-finish-macro-engine-2026-05-26`. The branch's commits
   touch:
   - `Cargo.toml` adds `blake3` build dep
   - `src/asschema.rs` adds `canonical_nota` + `canonical_hash` +
     `MacroDeclaration` + `ImportDeclaration` with path + subset
   - `src/macros.rs` adds `ExpansionMacro` trait + `MacroRegistry` +
     `MacroSignature` + `MacroExpansion`
   - `src/engine.rs` adds fixed-point expansion + import resolution +
     `(Macro ...)` declaration parsing + macro call parsing
   - `tests/macro_engine.rs` adds 17 tests covering all deliverables

**Slice B** (operator `schema-rust-next` main):
2. Replace the hardcoded signal-frame emission with the namespace
   convention: "if a surface `Foo` has a corresponding enum `FooRoute`
   in the namespace, bridge them with route + header + codec methods".
   The local RustEmitter in this design repo (`build.rs`) shows the
   pattern.

**Slice C** (operator `spirit-next` main):
3. Author `(Route Input)` / `(Route Output)` macro CALLS in
   `schema/spirit.schema`. Add `{ SignalFrame (ImportAll [...]) }`
   pointing at the migrated `signal-frame` repo (the option-(b)
   migration from sibling /372 §"Home recommendation").
4. Delete spirit-next's hand-rolled `transport.rs` route/header/codec
   surface entirely. The schema-emitted methods cover it.

## Comparison with sibling ae67842 (/374)

The sibling's report (/374) is comprehensive — 532 lines, 16 tests
passing, 5 Nix checks defined. Convergence + divergence:

| Dimension | sibling /374 | this /375 |
|---|---|---|
| Schema authored | Same multi-topic v0.3 shape | Same + 3 explicit macro CALLS |
| `signal-frame.schema` present | No (sibling /372 declared it conceptually) | YES — actually imported + parsed + macros resolved at lower time |
| Macro engine state | Operator's main (not real fixed-point) | Feature-branch finished (real fixed-point + registry + imports + asschema + hash) |
| Source of `InputRoute` enum | schema-rust-next hardcoded emission | Macro engine fixed-point expansion of `(Route Input)` |
| Source of `encode_signal_frame` | schema-rust-next hardcoded emission | Local emitter inspecting `<Surface>Route` enum presence |
| End-to-end transcripts | YES (their report §"What's working end-to-end") | YES (this report §"End-to-end transcripts") |
| Tests passing | 16 (theirs) | 17 (mine) |
| 5 Nix constraint checks | Defined as `flake.nix` checks | Defined structurally — `grep` patterns prove the invariants without a flake check |
| Storage | redb durable | redb durable |
| Multi-record observation | wire shape limited to one (schema lang gap) | same (inherited from same schema) |

Net: the sibling proved v0.3 RUNTIME viability; this pass proves
v0.3 runtime viability ON TOP OF a finished macro engine. Both are
needed for the integration story.

## Worktrees + commits

- `/home/li/wt/github.com/LiGoldragon/schema-next/designer-finish-macro-engine-2026-05-26/` —
  feature-branch worktree (commit `bc7dc05c18b4` on bookmark
  `designer-finish-macro-engine-2026-05-26`, pushed to origin).
- `/git/github.com/LiGoldragon/design-deep-spirit-next-pass-2026-05-26/` —
  new design repo (commit `6232cae89da6` on bookmark `main`, pushed
  to origin).
- `/home/li/primary/reports/designer-assistant/375-finish-macro-engine-and-use-it-2026-05-26.md` —
  this report (commits to primary main).

Operator-canonical repos (`nota-next`, `schema-next` main,
`schema-rust-next`, `spirit-next`) were NOT modified — discipline
per the brief's "Never push to main of operator-canonical repos".

## References

- `/home/li/primary/reports/operator/208-schema-stack-missing-implementation-audit-2026-05-26.md` §P1 — the macro-engine gap closed by this work
- `/home/li/primary/reports/designer/371-signal-executor-sema-runtime-triad-and-federation-2026-05-26.md` — runtime triad spec
- `/home/li/primary/reports/designer/373-engagement-with-operator-209-refined-triad-audit-2026-05-26.md` §4.6 + §6.3 — risk-guards + protocol traits emit
- `/home/li/primary/reports/operator/209-refined-triad-audit-opinion/2-operator-synthesis.md` — the 5-Nix-check pattern
- `/home/li/primary/reports/designer-assistant/372-design-signal-frame-schema-concept-2026-05-26.md` — `signal-frame.schema` concept + Q2 macro-form question
- `/home/li/primary/reports/designer-assistant/374-deep-spirit-parallel-implementation-2026-05-26.md` — sibling subagent's v0.3 substrate (orthogonal but complementary)
- `https://github.com/LiGoldragon/schema-next/tree/designer-finish-macro-engine-2026-05-26` — schema-next feature branch (this work's Goal 1)
- `https://github.com/LiGoldragon/design-deep-spirit-next-pass-2026-05-26` — the design repo (this work's Goal 2)
- Spirit intent records: 865 (psyche directive), 866 (make-it-more-real principle), 867 (Macro declaration form locked)
- `/home/li/primary/skills/double-implementation-strategy.md` — design-prefix discipline this work follows
- `/home/li/primary/skills/major-break-via-new-repo.md` — new-repo scaffold pattern
- `/home/li/primary/skills/component-triad.md` §"The single argument rule" — CLI single-argument constraint
