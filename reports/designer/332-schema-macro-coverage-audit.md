*Kind: Audit · Topic: schema-macro vision adoption across the workspace · Date: 2026-05-24 · Lane: designer*

# 332 · Schema-macro coverage audit — what's actually used in code today

## §1 Question

Of everything the schema-macro was designed to do — header derivation, signal types, dispatch trait, version projection, storage descriptors, CLI client, extensible macro variants — how much is wired into current production code, and how much is still hand-written? Run with 4 parallel audit subagents per the parallel-implementation + context-compaction directives.

## §2 Headline answer

| Surface | Schema-derived today | Notes |
|---|---|---|
| **persona-spirit triad** | ~55% | Operation/Reply enums + OperationDispatch trait + LogVariant header GENERATED from `spirit.schema`. Payloads + storage + version projection HAND-WRITTEN. |
| **Upgrade migration stack** | 0% | `V010ToV011` typed projection, `MigrationCatalogue::prototype()`, signal-version-handover types — all hand-written. |
| **New `schema` repo** | ~25% of design | `SchemaMacro` trait + 4 builtin lowerers + 4 `NodeDefinitionPoint` variants + assembler exist as a LIBRARY. Not yet wired as a `proc_macro`. |
| **All other contracts (mind/router/message/orchestrate/terminal/harness/lojix/engine-management/…)** | 0% | 75 `.concept.schema` files exist as inert v0.1 markers; ZERO files `include_str!` a `.schema`; all wire shapes are hand-written `signal_channel!` invocations. |

**Workspace-wide reach:** the schema-macro vision is alive in exactly ONE place — persona-spirit. Everywhere else, `.schema` files are markers that no code reads.

## §3 Where the schema engine actually lives

Newly created today: `/git/github.com/LiGoldragon/schema/` (2026-05-24, head `b3a1c8d`-era). Source layout:

- `src/engine.rs` — `SchemaMacro` trait (line 42) + `BuiltinMacroVariant` data-carrying enum (4 variants: Import / Header / Type / Feature) + `NodeDefinitionPoint` cursor (4 variants: ImportMapValue / HeaderRoot / NamespaceValue / FeatureItem)
- `src/document.rs` — Schema document model + `assemble()` dispatching to builtin lowerers
- `src/assembled.rs` — `AssembledSchema` struct + Route / Type / Feature collections (matches operator/174's spec)
- `src/reader.rs` — `LoadedSchema::read_path()` reads `.schema` files + recursively resolves imports
- `src/parser.rs` — NOTA parser for `.schema` text

**What's missing vs operator/175.4 design:** 3 of 7 NodeDefinitionPoints (FieldType, HeaderEndpoint, UpgradeRule) and the registry plugin for non-builtin macros. Per `/329`'s 7 BuiltinSchemaMacro variants, the schema repo has 4; missing NewtypeDefinition + FieldType + UpgradeRule.

**What's missing vs the brilliant-macro promise:** the schema repo is a runtime LIBRARY (assemble → AssembledSchema). It is NOT a `proc_macro` that takes a `.schema` and emits Rust code. The gap from "AssembledSchema exists" to "compile-time codegen of types + dispatch + storage" is the next major operator slice.

## §4 The persona-spirit anomaly — the one place where schema-derived works

`signal-persona-spirit` is the MVP pilot for `primary-ezqx.1`. Key file: `src/lib.rs:435` invokes `signal_channel!([schema])` where `[schema]` is the inline NOTA grammar. The macro reads `spirit.schema` via `signal-frame/macros/src/schema_reader.rs:91-136` and emits:

- `Operation` enum — 5 variants from header roots + 1 injected `Tap` for observability (100% schema-derived)
- `Reply` enum — 9 variants from reply feature (100%)
- `Event` enum — 2 variants + 2 stream witnesses (100%)
- `OperationHandler` trait + `OperationDispatch` blanket impl (100%)
- `LogVariant` impl (header byte assignment: `bytes[0] = #index` per emit.rs:370) (100%)
- `NotaEncode`/`NotaDecode` codecs + frame builders (100%)

**Hand-written:** payload types (Statement / Entry / Topic / Summary / Quote / StateSubscriptionToken / …) — these are domain types the macro consumes by name reference. Per /326-v13's split: the macro composes the wire shape; the developer authors the leaves.

This pattern works. The schema-macro vision IS proven in persona-spirit. The question is just propagation to the other ~50 triads.

## §5 The upgrade stack is 100% hand-written

Per audit slice B:

- `upgrade/src/catalogue.rs:158-162` — `MigrationCatalogue::prototype()` returns a hardcoded vector containing one migration module
- `upgrade/src/migrations/persona_spirit/version_0_1_0_to_0_1_1.rs:102-318` — `historical` mod (rkyv reproduction of v0.1.0 types) + `current_shape` mod (current types with explicit `From` impls)
- 6 hand-written `From` impls do the actual projection: `Certainty → Magnitude` (lines 303-311), `Kind → Kind` (291-301), `StampedEntry → StampedEntry` (268-276), `Entry → Entry` (278-289)
- `signal-version-handover/src/lib.rs:1-197` — every handover type (HandoverMarker, ReadinessReport, MirrorPayload, …) is a hand-typed record with rkyv + NotaRecord derives

`upgrade/schema/upgrade.concept.schema`, `version-projection/schema/…`, `signal-version-handover/schema/…` all exist as v0.1 markers. None are read by code.

**The gap is named:** to make the upgrade schema-derived would need (a) `UpgradeRule` macro variant landed in the schema repo, (b) a proc_macro that diffs v0.1.0.schema vs v0.1.1.schema and emits the `From`-chain projections, (c) `historical` mod auto-generated from the older schema. None exist.

## §6 The workspace-wide picture is bleaker than the persona-spirit picture suggests

Per audit slice D:

- **75 `.concept.schema` files** scattered across reachable repos (per operator/175.3 spread)
- **0 files** `include_str!` a `.schema` outside of the new `schema` repo's own tests
- **0 `schema_macro!`** invocations workspace-wide
- **13 `AssembledSchema`** references — all inside the new `schema` crate itself; ZERO in any contract/component code
- **Every contract** (`signal-mind`, `signal-router`, `signal-message`, `signal-orchestrate`, `signal-terminal`, `signal-harness`, `signal-lojix`, `signal-engine-management`) uses **hand-written `signal_channel!`** with manually-declared enums + records + derives

The 73 (now 75+) concept schemas are pure markers awaiting a consumer. They were filed per /327 but the engine that should read them doesn't yet read them.

## §7 What this means for the spirit cutover (and for /331)

Good news: the cutover doesn't need any of this work. The cutover uses the EXISTING hand-written migration code (`upgrade-spirit-sandbox-test` → `MigrationCatalogue::prototype()`), which is proven on a copy of the live DB. So the brief-outage MVP cutover ships independent of schema-engine maturity.

Bad news: every future component upgrade will repeat the hand-written-migration cost until the schema-engine path lands. We've eaten the cost once (Spirit v0.1.0→v0.1.1). The second time will hurt.

## §8 Recommendation — three concrete next slices

In order of leverage:

1. **Promote one more contract to schema-derived.** Pick a small, well-bounded one — `signal-version-handover` is a great candidate (it's already needed for live handover; its types are short; promoting it would force the schema engine to handle the import + small-enum + struct patterns end-to-end). Cost: half-day to a day. Reward: validates the engine on a second contract; sets the migration pattern.
2. **Land `UpgradeRule` as a `BuiltinSchemaMacro` variant.** Even if the proc_macro for emission isn't ready, the schema model + assembler needs the upgrade vocabulary so future schemas can express their migrations. Cost: extend `BuiltinMacroVariant` enum + add `UpgradeInput` struct + a lowerer that pushes `AssembledFragment::UpgradeRule` entries. Half-day.
3. **Wire the `schema` crate as a proc_macro.** This is the big slice — turn the runtime assembler into a compile-time codegen. Operator territory; multi-day. The 75 concept schemas all become live once this lands.

## §9 Operator beads from this audit

I will file two new beads (one per the next two slices above; #3 already partly covered by `primary-ezqx.1`):

- **promote-signal-version-handover-to-schema-derived** (P1) — replicate the spirit pattern in signal-version-handover; second pilot.
- **land-UpgradeRule-macro-variant** (P1) — extend the `schema` repo `BuiltinMacroVariant` + `NodeDefinitionPoint` enums for the upgrade vocabulary.

The third (proc_macro wiring) belongs to operator's `primary-ezqx.1` epic and doesn't need a new bead from designer.

## §10 References

- Designer prior: `reports/designer/326-v13-spirit-complete-schema-vision.md`, `reports/designer/329-schema-macro-component-extensibility.md`, `reports/designer/330-parallel-implementation-pivot-and-spirit-nspawn-plan.md`
- Operator prior: `reports/operator/170-schema-spirit-mvp-implementation-2026-05-24.md`, `reports/operator/174-v5-schema-import-header-design-critique-2026-05-24.md`, `reports/operator/175-schema-engine-prep/`
- New repo: `/git/github.com/LiGoldragon/schema/` (head `b3a1c8d`)
- The MVP-pilot file: `/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs:435` `signal_channel!([schema])`
- The migration hand-written file: `/git/github.com/LiGoldragon/upgrade/src/migrations/persona_spirit/version_0_1_0_to_0_1_1.rs`
- The 75 concept schemas: `/git/github.com/LiGoldragon/*/schema/*.concept.schema`
