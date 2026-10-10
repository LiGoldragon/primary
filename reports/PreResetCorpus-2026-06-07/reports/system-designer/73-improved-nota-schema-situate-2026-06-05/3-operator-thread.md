# 3 — Operator thread digest: improved NOTA/schema mechanism

System-designer situate report, sub-file 3. Digests the operator-lane thread
on the improved NOTA/schema mechanism (structural macro nodes + Asschema
removal + schema-as-codec pipeline) as it stands across operator reports
306-316. Operator owns main and implementation, so this file is the
landed-vs-proposed ledger.

## 1. Operator's understanding of the mechanism

Operator's model of the improved mechanism (most directly in reports 312, 314,
316) is the two-arrow schema pipeline:

```text
schema (.schema text, specialized NOTA)
  -> deserialize into typed Rust datatypes that fully define schema
  -> schema-in-Rust value (rkyv-serializable)
  -> lower into Rust interface code
```

The substrate beneath arrow 1 is **structural macro nodes**: an enum-shaped
consumer lists structural variants in source/declaration order, NOTA dispatches
a parsed `Block` through those ordered structural patterns, the first match
wins, the matched payload is decoded into the typed Rust value, and the same
value encodes back to structural NOTA (bidirectional). Schema is a specialized
NOTA dialect built on this — not a separate language lowered through text.

Operator agrees with the designer thread on the core direction on every major
point:

- Schema is just NOTA at the authored + codec boundary (report 314).
- Structural matching happens first, before semantic interpretation; variant
  declaration order is semantic and the psyche explicitly wants variants tried
  in written order (312, 315).
- Removing Asschema is NOT deleting resolution — Rust emission cannot render
  correct Rust from unresolved authored sugar (hoisting, visibility, symbol
  paths, root header shorthand, reserved scalars, external imports) (314).
- Rust-specific shaping (no nested type declarations, module/visibility/import
  aliasing) belongs in arrow 2 / `schema-rust-next`, not a new schema IR (316).
- `SchemaResolution` should NOT exist as a public target; resolution lives as
  methods on the typed source nouns (314, 316).

## 2. Where operator DIVERGES from the designer thread

The comparison reports (313, 314, 315) are the divergence ledger. Operator
accepts the designer's design corrections but refuses a wholesale retreat to
the designer prototype branch. Four substantive divergences:

1. **Keep the existing `Pattern`/`StructuralVariant` matcher; do not adopt the
   designer branch's parallel `BlockShape` matcher as-is** (313, 315). Designer
   branch `structural-macro-nodes` @ `c2b4cc72` added a new `BlockShape` enum
   (`PascalAtom`, `HeadedParenthesis`, `PascalHeadedParenthesis`) — a second
   structural language. Operator main reuses the pre-existing
   `MacroNodeDefinition` / `Pattern` / `MacroRegistry::dispatch` substrate,
   which already supports captures, nested child patterns, delimiter/count
   checks, rest captures, body streams, and no-match diagnostics that the
   designer prototype lists as open questions. Operator's synthesis: keep
   operator's matcher substrate, lift designer's `BlockShape` in only as a thin
   authoring vocabulary that *lowers into* `Pattern`, plus designer's better
   teaching example (the `(Vec (Map (Optional RecordIdentifier)))` round-trip).
   "Do not merge designer's branch wholesale."

2. **Pragmatic resolution-on-source-nouns, NOT emitter-walks-source** (314).
   On the asschema-removal question, operator chose the pragmatic path
   (resolution as methods on the typed source datatypes) and explicitly rejects
   the stronger alternative where `schema-rust-next` walks `SchemaSource` and
   resolves sugar inline as it emits — that would make the Rust emitter a
   second schema engine and violate the boundary "Schema owns schema meaning;
   Rust emission owns Rust projection from typed facts." Any private
   resolution context/cache "gets no file extension, no checked-in text form,
   no binary artifact, no store, no public handoff contract. If it becomes a
   durable object components depend on, Asschema has not been removed; it has
   been renamed."

3. **Direct typed derive decode — stop the string re-dispatch seam** (315).
   Operator's key finding against the *current main implementation*: the
   `#[derive(StructuralMacroNode)]` path on main still routes decode through
   `StructuralVariantSet::dispatch`, gets a `MacroMatch`, then re-identifies
   the selected variant with `match matched.macro_name()` — a string-shaped
   final dispatch even though the type picked the variant set. Operator's
   correction: the derive should generate direct typed construction from the
   variant's structural shape; stop generating `match macro_name()` for derived
   enums; keep `from_structural_match` only as a compatibility hook for
   hand-written low-level users until schema no longer needs it. Operator's
   durable synthesis is explicitly "not designer branch versus operator main.
   It is main plus two improvements: direct typed derive decode, and
   dead-variant shadowing detection."

4. **Conflict detection: dead-variant shadowing, not forbid-all-overlap**
   (315). Current `validate_no_silent_conflicts` is exact-pattern only
   (`first.pattern() == second.pattern()`). Operator wants it strengthened to
   catch a general earlier shape subsuming a specific later shape (the
   demonstrated `pascal_head` before `head = "Optional"` at the same arity
   footgun) — but NOT to forbid intentional overlap, because declaration order
   is the author's intended priority. Concrete rule: exact duplicate = error;
   earlier-general-subsumes-later-specific = error; partial overlap where both
   stay reachable = allow.

One precision edit operator pushes back on the designer thread (report 316):
say "canonical/semantic round-trip" not byte-identical round-trip, and make
rkyv apply to the clean schema-in-Rust value, not every parse helper (source
spans, diagnostics, transitional raw blocks can stay parse-time helpers).

## 3. What is LANDED vs PROPOSED

LANDED on main (operator owns main):

- `nota-next` main `35786532` (later `87991f83`-era schema sibling) — the typed
  `StructuralMacroNode` trait surface: `structural_position`,
  `structural_variants`, `from_structural_match`, `to_structural_nota`, plus
  `from_structural_block/pair/candidate` helpers and `MacroMatch` capture
  accessors (`capture`, `block_capture`, `body_capture`). Tests +
  clippy green. (report 312)
- `schema-next` main `87991f83` — `SourceVariantSignature` implements
  `StructuralMacroNode`; authored enum bodies parsed from `Block` (not the old
  `RawNotaDatatype` mirror); unit/data/inline-declaration variants round-trip
  `.schema` -> typed source -> `.schema` and lower to Asschema. (312)
- `schema-next` `b14d14f7` — multi-module per-package loading (`load_modules`),
  package self-registration, nested-import resolver preservation. (311)
- `schema-rust-next` `e7d5f395` — `RustEmissionTarget::SignalRuntime`,
  `GenerationPlan`/`ModuleEmission`/`GenerationDriver`, generated
  `NexusRunnerAdapter` + total `NexusAction -> NextStep` projection,
  runtime-module feature gating. (311)
- `triad-runtime` `6daf2954`/`e40d1e96` — `LengthPrefixedCodec`/`FrameBody`,
  `ComponentCommand`/`ComponentArgument`, shared recursive Nexus runner core
  (`Runner::drive`, `NextStep`, `RunnerEngines`, `ContinuationLimit`,
  `ContinuationExhausted`). This SUPERSEDES report 306's "none of the three
  cleanups landed" status for cleanups 1+2. (307, 311)
- `spirit` `e0c2edc2` (rename complete) then `8d0e32cf` (split runtime schemas
  by plane) — canonical schema-derived Spirit: `schema/{signal,nexus,sema}.schema`
  generated into `src/schema/{signal,nexus,sema}.rs`, storage through
  `sema-engine` over `.sema`, Nexus delegates to the generated runner adapter +
  `triad_runtime::Runner`. (308, 311)
- `spirit` `6a339e20` — SEMA storage routed through `sema-engine`, no direct
  redb in daemon runtime; closes the sema-engine bypass from system-designer 63.

PROPOSED / NOT YET LANDED (operator's named next slices):

- Direct typed derive decode in `nota-next` (kill `match macro_name()` for
  derived enums) — operator's #1 near-term patch BEFORE spreading the derive
  into more of schema-next, else the string-dispatch seam spreads. (315)
- `#[derive(StructuralMacroNode)]` proc-macro in `nota-next-derive` — only the
  runtime trait target exists; the derive itself is not written. (312)
- Dead-variant shadowing conflict check (narrow `pascal_head`-subsumes-literal
  rule first). (315)
- Asschema removal proper: move `SchemaSource::to_asschema` body onto source
  nouns as resolution methods; add `RustModule::from_source` /
  `RustEmitter::emit_file_from_source`; flip the build driver off `.asschema`
  artifacts; delete `Asschema`/`AsschemaArtifact`/`AsschemaStore` last, only
  after no public consumer remains. (314, 316) Asschema is STILL the live
  endpoint: `schema-next` returns it from `lower_schema_source_with_resolver`,
  `schema-rust-next` consumes `RustEmitter::emit_file(&Asschema)` and writes
  `.asschema` artifacts in `build.rs`. (314)
- Migrate remaining schema positions (namespace decl, struct fields, root
  sections, type-reference macro calls) onto typed structural nodes. (312, 315)
- thiserror runtime-error cleanup — bead `primary-kwm2`, still open, correctly
  sequenced AFTER frame/argument extraction. (306, 307)
- Generic daemon runner SHELL beyond the landed Nexus loop — bead
  `primary-es8u` (listener binding, stale socket cleanup, transport handoff,
  one-line main, meta listener, single engine-owner loop). The core runner
  landed; the host-shell did not. (310, 311)

## 4. Spirit pilot + production readiness as it relates to the schema change

Operator's verdict (reports 308, 311): the new schema-derived `spirit` is a
**credible development pilot and the exemplar for the three-plane runtime
shape**, but it is **NOT production-cutover ready** to replace `persona-spirit`.

It crossed concept->running: generated wire/Nexus/SEMA types in the runtime
path, daemon takes binary frames and never parses NOTA, CLI is the text edge
emitting binary signal frames, durable storage through `sema-engine`/`.sema`
(redb 2.x proven absent from the runtime tree; remaining redb is build-time
schema tooling), recursive Nexus loop is shared library code, process-boundary
+ `.sema`-durability tests pass. The schema pipeline is live end-to-end:
`.schema` -> `schema-next` -> `.asschema` -> checked-in Rust, with build
freshness checks enforcing the path.

This is the direct payoff of the schema change: the pilot proves the structural
macro-node + schema-as-codec stack runs a real daemon. Anchor intent: Spirit
record 2540 ("new schema-derived spirit is the forward target, nearly ready
for production; new functionality targets it") and 2558 (operator runtime
cleanup sequence).

## 5. Operator-flagged risks / blockers

- **P1 schema-correctness blocker — dual-lowering bare-header bug**
  (`primary-vllc`): the registry lowering path lowers a bare PascalCase enum
  variant to payload `None` (`src/declarative.rs:1846-1850`) while the
  `SchemaSource` path resolves a same-named namespace payload
  (`src/source.rs:765-772`). The two lowering routes can silently DISAGREE on
  whether a header variant carries data. Operator calls this "the most
  conceptually dangerous open item" — schema-as-codec is unreliable until ONE
  authoritative lowering exists. Fix toward the `SchemaSource` path. (311)
- **String re-dispatch seam** in the derive decode path — flagged as the thing
  to fix before spreading the derive into more schema positions, or it
  contaminates the schema reader. (315)
- **Asschema-rename risk**: if a resolution context becomes a durable
  depended-on object with an artifact/store, "Asschema has not been removed; it
  has been renamed." (314)
- **Emitter shape**: `schema-rust-next` is still hundreds of hand-indented
  `self.line` string writes (`primary-myku`, Rust item token model owed); and
  self-package imports emit `spirit::...` needing the `extern crate self as
  spirit;` workaround (`primary-j0wo`). Not compile-blockers but raise error
  rates as more components copy generator output. (311)
- **Daemon runner shell not extracted** (`primary-es8u`) — strict engine
  separation is not yet structurally enforced while every daemon could
  hand-write `daemon.rs`. (310, 311)
- **Production cutover blockers** (311): full daemon runner shell; real
  `signal-spirit` + `meta-signal-spirit` triad repos (current `signal-spirit`
  is an MVP not matching the six-operation pilot surface); meta policy leg;
  fresh production feature parity matrix; production data migration from
  `persona-spirit.redb` into `.sema` (no migration done); real schema
  upgrade/diff (`UpgradeFrom`/`AcceptPrevious` named-but-unimplemented).
- **Verification not falsifiable / slow** (`primary-vjl5`): the local-stack Nix
  check ran ~27 min and was interrupted — "not passing evidence." Operator
  wants a fast consumer check + a named slow full-flake path. (311)
- **SymbolPath structured-vs-flat** is an unresolved design/intent thread
  (record 1577 at Medium, 1586 at Zero); operator report 304's claim that flat
  is fully canonical is flagged stale — do not use as implementation license. (307)
- **Intent-duplication**: schema-pipeline captured twice — designer record
  `fkbz` and operator record `ydvg`; Asschema-removal records also overlap.
  Operator leaves both, flags a later intent-maintenance consolidation. (315, 316)
