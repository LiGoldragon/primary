# schema-next refresh for the new lojix stack

Crate: `schema-next` — the schema engine. Resolves authored `.schema` NOTA into
the semantic schema-in-Rust value (`Schema`). It is upstream of
`schema-rust-next` (the emitter) and does NOT itself emit Rust source.
Path: `/git/github.com/LiGoldragon/schema-next`.

HEAD: `77e71a4`. lojix's transitive pin (from
`/git/github.com/LiGoldragon/lojix/triad-port/Cargo.lock`):
`schema-next = 5311f9a`. So the drift baseline for lojix is `5311f9a`, NOT
`c0a331a` — `c0a331a` is the schema-rust-next pin given in the brief; the brief
did not state a schema-next pin, and the actual lock value is `5311f9a`.

## The single most important correction to the brief's baseline

Two of the six focus commits the brief flagged as "the recent arc" are ALREADY
in lojix's pin and are therefore NOT new for lojix:

- `a2123f8` (preserve source field naming) — ancestor of `5311f9a` (verified via
  `git merge-base --is-ancestor a2123f8 5311f9a` → yes).
- `5311f9a` (same-name payload recovery out of namespace enums) — IS lojix's pin.
- `6a12bcc` (remove asschema compatibility surface) — ancestor of `5311f9a`.

The genuinely NEW schema-next commits for lojix (`5311f9a..77e71a4`, oldest-first):

1. `c2b3546` schema-next: add stream lifecycle metadata
2. `30a88be` schema-next: align direct stream lowering
3. `77e71a4` GAP 2 derive adoption + Assembled→MacroExpansion rename + Asschema-retired docs

Everything below is judged against that corrected baseline. The
already-included commits are addressed adversarially at the end ("Commits that
do NOT apply") because the brief asked about them.

## Crate direction (INTENT.md + ARCHITECTURE.md)

`schema-next` is now firmly on the schema-in-Rust pipeline:
`.schema` → `SchemaSource` (typed source nouns that own resolution) → `Schema`
(semantic, rkyv-serializable) → Rust (emitted downstream by schema-rust-next).
Asschema is RETIRED, not preserved: the `.asschema` text artifact, the
`.asschema.rkyv` binary, `AsschemaArtifact`, the old `src/store.rs` redb-backed
semantic store, and `schemas/core.asschema` are all removed
(`6a12bcc`: `src/asschema.rs`→`src/schema.rs`, `-1291` lines). `Schema` has no
`to_nota`, no text artifact owner, and no store wrapper. Authored source text is
a NOTA projection of a typed `SchemaSource` object owned by
`SchemaSourceArtifact`; database work lives in production SEMA engines, not here.

The crate is also converging on the "structural macro node" mechanism living at
the NOTA layer: nota-next owns the pattern matcher + the new
`StructuralMacroNode` derive; schema-next supplies schema positions + handlers.

## New development 1 — stream lifecycle metadata (`c2b3546`)

What changed (`src/schema.rs`):

- `Schema` gains a fourth product field `streams: Vec<StreamDeclaration>` with a
  `Schema::streams()` accessor and a `streams` argument to `Schema::new`.
- New `StreamDeclaration { name, token, opened, event, close }` — five
  `TypeReference`-typed legs describing a push stream's lifecycle.
- `EnumVariant` gains `stream_relation: Option<StreamRelation>` plus
  `EnumVariant::new` + `with_stream_relation`.
- New `StreamRelation::{Opens(Name), Belongs(Name)}` with `stream_name()`.

Authoring surface (ARCHITECTURE.md §Authored Schema Source,
INTENT.md): a stream is declared inside the namespace map as
`StreamName (Stream { token Token opened Snapshot event Event close Close })`;
it lowers to `Schema::streams()` and is EXCLUDED from `Schema::namespace()` (so a
stream never masquerades as an ordinary payload type). Data-carrying variants may
attach `(Variant Payload opens StreamName)` and
`(Variant Payload belongs StreamName)` — the four-object variant forms — to point
at a stream declaration.

Bearing on lojix — DIRECT and load-bearing. This is the schema-engine half of
the exact feature lojix's contract documents as MISSING. `signal-lojix`
`triad-port/schema/lib.schema:11-20` says verbatim: "schema-next cannot yet emit
a daemon-pushed event frame — no event/stream root, no opens/belongs construct
(verified against schema-next + schema-rust-next…)". That statement is now
OBSOLETE: the `opens`/`belongs` construct and the `Stream { … }` declaration
exist, and the downstream emitter consumes them (see "Cross-crate readiness").
lojix today fakes streaming as an ordinary request/reply handshake
(`Watch* → SubscriptionToken`) with the two event payloads
(`DeploymentPhaseEvent`, `CacheRetentionTransitionEvent`) defined as plain
namespace records (lib.schema:90-111). Those event payloads are precisely the
`event` leg of a `StreamDeclaration`; `SubscriptionOpened`/`SubscriptionClosed`
are the `opened`/`close` legs; `SubscriptionToken` is the `token` leg. The schema
is already SHAPED for streams — it just spells them as ordinary records.

Does lojix's schema need to declare stream lifecycle now? Not to keep building —
the present request/reply form still lowers and emits. But to GAIN
daemon-pushed event frames (the named follow-on the contract itself points at in
lib.schema:18-20 + ARCHITECTURE §4), the contract would author its two streams
as `Stream { … }` declarations and mark `WatchDeployments`/`WatchCacheRetention`
with `opens` and the delta variants with `belongs`.

## New development 2 — direct stream lowering (`30a88be`)

What changed (`src/engine.rs`): the engine now lowers streams as part of the
default `Schema` build. After lowering the namespace it runs
`NamespaceStreamProbe::contains_stream()`; if any namespace value is a
`(Stream …)` head it re-decodes through `SchemaSource::stream_declarations()` and
populates `Schema::streams` instead of `Vec::new()`. `NamespaceBlock` skips
`(Stream …)` pairs during ordinary namespace declaration lowering via
`StreamDefinitionProbe` (so the stream does not also become a namespace type).
`src/declarative.rs` (+49) and `src/source.rs` (+4) align.

Bearing on lojix — enabling, not yet load-bearing. Without this, a schema with
`Stream { … }` would either error or leak the stream into the namespace; with it,
the stream populates `Schema::streams()` and the namespace stays clean. This is
the wiring that makes development 1 usable through the normal lower path lojix's
build uses. It only bites lojix if/when lojix authors a `Stream { … }`. For
lojix's CURRENT (stream-free) schemas it is a strict no-op — the probe finds no
`(Stream …)` head, `Schema::streams()` stays empty, and emission is unchanged.

## New development 3 — GAP 2 derive adoption + Assembled→MacroExpansion rename (`77e71a4`)

Two distinct changes in one commit.

### 3a. Assembled* → MacroExpansion* rename (internal, `src/declarative.rs`)

Pure rename of the macro-template lowering machinery: `AssembledTemplate` →
`MacroExpansionTemplate`, `AssembledType/Fields/Variants/Reference/StructBody` →
`MacroExpansion*`, and `SchemaError::UnknownAssembledTemplate` →
`UnknownMacroExpansionTemplate`. These are all crate-internal types (the only
public-facing surface is the renamed `SchemaError` variant).

Bearing on lojix — NONE. lojix never names these types and never matches on
`SchemaError::UnknownAssembledTemplate` (it consumes schema-next only
transitively, through schema-rust-next's `build` API; it does not import
schema-next's error enum). The rename does not touch generated code shape.

### 3b. `SourceVariantSignature` becomes a `#[derive(StructuralMacroNode)]` enum (`src/source.rs`, ±348 lines)

The hand-written `SourceVariantSignature` struct + its hand-written
`StructuralMacroNode` impl + the hand-written `to_schema_text` string-ladder are
DELETED. It is now a derive-generated enum with `#[shape(...)]` cases:

```
pub enum SourceVariantSignature {
    #[shape(pascal_atom)]                 Unit(SourceVariantName),
    #[shape(pascal_head, arity = 2)]      Data(SourceVariantName, SourceVariantPayload),
    #[shape(pascal_head, arity = 4)]      Streaming(SourceVariantName, SourceVariantPayload,
                                                    StreamRelationKeyword, SourceVariantName),
}
```

plus `StreamRelationKeyword { #[shape(keyword="opens")] Opens, #[shape(keyword="belongs")] Belongs }`
and `SourceVariantName`/`SourceVariantPayload` impls. The derive generates BOTH
directions (decode from NOTA + re-emit to canonical `.schema` text), replacing
the deleted `match macro_name()` ladder and `to_schema_text`. This is the
schema-next half of "GAP 2": variant-signature handling is now schema-as-data
rather than a hand-rolled parser/printer, satisfying the no-hand-rolled-parsers
discipline.

Build-dependency consequence: this requires nota-next `f0e435a6` (the commit that
adds the `StructuralMacroNode` derive with `pascal_atom`/`pascal_head`/`keyword`
shape attributes — verified present at that sha in `derive/src/lib.rs:846-880`).
lojix's triad-port pins nota-next `fb600e3`, which is an ANCESTOR of `f0e435a6`
(verified). So bumping schema-next to HEAD forces a nota-next bump to ≥
`f0e435a6` somewhere in the build-dep graph.

Bearing on lojix — INDIRECT, build-graph only. The change is to how schema-next
PARSES authored variant signatures; it does not change the generated nexus.rs /
sema.rs SHAPE for lojix's existing variants (a `(Variant Payload)` still lowers
to the same `EnumVariant`). lojix gains nothing functionally from 3b directly —
it is a consumer of the result, not of the parser. But schema-next is in lojix's
build-dep graph (transitively via schema-rust-next's build feature), so to adopt
the stream metadata (developments 1+2) lojix's resolved schema-next must be at
HEAD, which drags in the nota-next ≥ `f0e435a6` requirement.

## Cross-crate readiness — does the stream feature reach Rust?

Adversarial check: schema-next metadata is worthless to lojix if the emitter
ignores it. It does NOT ignore it. `schema-rust-next` HEAD (`6685e7b`)
references `streams()` / `StreamDeclaration` / `stream_relation` in
`src/daemon_emit.rs`, `src/lib.rs`, `src/migration.rs`. `daemon_emit.rs:155`
gates on `!schema.streams().is_empty()` to emit an `EmittedSubscriptions`
registry built on `triad_runtime`'s `SubscriptionRegistry` +
`SubscriptionEventPublisher`, which its own doc comment says "replaces a
hand-written `SubscriptionHub`". The stream-emission commits
(`4ee2c89` emit schema streams through signal-frame; `799f678`/`b75c7f5`
frame-codec + deliver fixes; `d8e0a37` tokenize streaming; `b9dc094` triad-runtime
streaming dep) are all in `c0a331a..HEAD` — i.e. NONE are at lojix's
schema-rust-next pin `c0a331a` (verified: `git grep` for `streams()` at
`c0a331a` returns empty). So the end-to-end push-stream pipeline
(schema-next metadata → schema-rust-next emitter → triad-runtime subscription
machinery) exists only at the HEADs of all three, above every lojix pin.

This matters because lojix's runtime HAND-WROTE its concurrency and would
otherwise hand-write a subscription hub too. The emitted `EmittedSubscriptions`
+ `SubscriptionRegistry` is exactly the kind of runtime concern lojix should NOT
duplicate. (Confirming the emitter side is the job of the schema-rust-next and
triad-runtime survey reports in this session; here it is cited only to prove the
schema-next metadata is consumed.)

## Recommendations for lojix

### MUST-PORT

None are strictly must-port to keep building: lojix's current schemas are
stream-free and lower/emit fine at the new HEADs. The "must" framing applies
only to the streaming follow-on the contract itself promised.

### SHOULD-DO (the streaming follow-on lojix already named)

1. Author lojix's two streams with the `Stream { … }` + `opens`/`belongs`
   construct, and bump the pins. This is the realization of the day-one
   decision `2tfa` deferral recorded in `signal-lojix` lib.schema:11-20. Concretely:
   declare `DeploymentPhaseStream (Stream { token SubscriptionToken opened
   SubscriptionOpened event DeploymentPhaseEvent close SubscriptionClosed })` and
   the analogous cache-retention stream in `signal-lojix/lib.schema`; mark
   `WatchDeployments`/`WatchCacheRetention` as `opens` variants and add the delta
   variants as `belongs`. Then bump schema-next → `77e71a4`, schema-rust-next →
   HEAD, nota-next → ≥ `f0e435a6`, triad-runtime → the streaming-capable rev.
   Delete the obsolete "schema-next cannot yet" comment block.
   Effort: LARGE (touches all three contracts + lojix runtime, which must adopt
   the emitted `EmittedSubscriptions` and drop its faked handshake; cross-crate
   pin coordination; the M1 daemon's per-request `SchemaRuntime` must hold the
   subscription registry across requests, which is a real runtime-shape change).
   Risk: HIGH. Streaming is the most-moving surface across all four crates right
   now (multiple "fix" commits land weekly in schema-rust-next). Pinning into it
   buys churn. Defer until the schema-rust-next/triad-runtime streaming surface
   settles — track it, don't adopt it mid-flight. The contract is already shaped
   to absorb the change later (the event payloads exist as records), so deferral
   costs little.

### NICE-TO-HAVE / HYGIENE

2. When lojix next bumps its schema-next pin for ANY reason, take `77e71a4`
   wholesale (it is the current HEAD). The Assembled→MacroExpansion rename (3a)
   and the variant-signature derive (3b) are invisible to lojix's generated
   code; the only adopt-cost is the nota-next ≥ `f0e435a6` bump that the derive
   forces. Verify lojix's checked-in nexus.rs/sema.rs are unchanged by
   re-running the build with `LOJIX_UPDATE_SCHEMA_ARTIFACTS` set and diffing.
   Effort: SMALL (pin bump + artifact-freshness re-check). Risk: LOW — no schema
   shape change for stream-free schemas; the nota-next bump is +2 commits.

## Commits that do NOT apply to lojix (the brief asked; stated explicitly)

- `6a12bcc` (remove asschema) — NOT new for lojix (ancestor of its pin). And it
  never applied at the source level: lojix's build.rs uses schema-rust-next's
  `GenerationDriver`/`GenerationPlan` + `write_or_check`; there is NO assemble
  step, no `.asschema`, no `AsschemaArtifact` anywhere in lojix/signal-lojix/
  meta-signal-lojix triad-port (grep returns empty). Answer to brief question
  (a): lojix's authoring and build wiring assume NO assemble step. Already clean.

- `a2123f8` (preserve source field naming) — NOT new for lojix (ancestor of its
  pin). Its effect (a reference-typed field uses the canonical derived field
  name, `Name::new(self.name.field_name())`, i.e. camelCase →
  snake_case) is ALREADY reflected in lojix's checked-in generated code:
  `signal-lojix` lib.rs has `from_slot`/`to_slot`, `meta-signal-lojix` lib.rs has
  `build_attribute`, lojix nexus.rs has `public_key`/`reclaimed_paths`, sema.rs
  has `deployment_events`. lojix authors fields in both `recordIdentifier
  RecordIdentifier` and `Name *` forms (e.g. signal lib.schema:58,72-74,99,107),
  so it DOES exercise this path — and the generated names are already correct.
  Answer to brief question (c) re field names: this change does not alter
  lojix's generated field names because lojix already builds on a pin that has
  it. No re-emit will move.

- `5311f9a` (same-name payload recovery out of namespace enums) — this IS lojix's
  pin, so by definition baseline, not new. Its rule: a NAMESPACE enum body
  (`Kind [Decision Correction]`) lowers variants with
  `SourceVariantPayloadResolution::explicit_only()`, i.e. a bare PascalCase
  variant in a namespace enum does NOT silently acquire a same-named payload;
  only ROOT input/output headers do same-name recovery. lojix's namespace enums
  are all bare-unit enums (`DeploymentKind [FullOs OsOnly HomeOnly]`,
  `SystemAction [Eval Build …]`, the rejection-reason enums, `EffectStage`,
  `ContainerState`, etc.) with no same-named namespace types, so the behavior is
  correct for lojix regardless — and again it is already in its pin.

## Answers to the brief's key questions (consolidated)

(a) Asschema fully retired, resolution lives as methods on schema-in-Rust source
types: lojix is ALREADY clean. No assemble step in any lojix authoring or build
wiring. build.rs uses `GenerationPlan::daemon_runtime(...).with_dependency_schema`
+ `write_or_check`. Nothing to port.

(b) Stream lifecycle metadata + direct stream lowering: lojix's schema does NOT
need to declare stream lifecycle to keep building (its current request/reply
handshake still lowers + emits). It GAINS, when it adopts the construct, real
daemon-pushed event frames over the schema-rust-next-emitted
`EmittedSubscriptions`/`SubscriptionRegistry` — replacing the faked handshake
and matching the contract's own named follow-on. The cost is pinning into the
fast-moving four-crate streaming surface; recommend tracking, deferring adoption
until that surface settles. The contract is pre-shaped for the migration, so
deferral is cheap.

(c) Assembled→MacroExpansion rename + preserve source field naming + same-name
payload out of namespace enums: NONE of these change the SHAPE of generated code
lojix checks in. The rename is internal types + one `SchemaError` variant lojix
never names. Field naming is already reflected in lojix's generated snake_case
fields. Same-name payload recovery already matches lojix's bare-unit namespace
enums. Re-emitting lojix's artifacts at HEAD should produce byte-identical
nexus.rs/sema.rs/lib.rs for the stream-free schemas.

(d) Does lojix use any affected construct? It uses namespace enums (affected by
5311f9a — but correctly, and already in pin), reference-typed + `*`-derived
struct fields (affected by a2123f8 — but correctly, already in pin), and
data-carrying variants (the `Data` case of the new derive — same lowering
result). It does NOT use the stream construct (`opens`/`belongs`/`Stream { … }`)
— zero occurrences across all three triad-port schemas — which is exactly why
developments 1+2 are a deliberate future adoption, not a forced port.
