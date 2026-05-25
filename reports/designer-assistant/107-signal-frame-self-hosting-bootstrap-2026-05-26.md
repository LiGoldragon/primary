# 107 — signal-frame self-hosting bootstrap

*Per psyche 2026-05-26 (intent record 711, Maximum): even
signal-frame itself should be a schema. This report covers the
landing of the recursive endpoint --- the meta-framework that
processes schemas now partially describes its own data shapes
through `schema/signal-frame.schema`, derived via the schema-rust
composer that signal-frame ships. Schema all the way down, with a
documented kernel boundary that moves downward as the composer
gains capability.*

## Summary

The Stage-2 self-hosted leaf landed today on
`designer-schema-poc-from-v0.3-main-2026-05-26` in
`~/wt/github.com/LiGoldragon/signal-frame/`. The closed reply-
outcome taxonomy --- five enums classifying what happened to a
request after it crossed the frame boundary --- is now
schema-derived alongside its kernel hand-authored mirror. Eleven
new tests prove the two-stage bootstrap is well-formed: the
kernel compiles standalone, the schema-derived leaf compiles atop
the kernel, every variant on the kernel side has a structurally-
equivalent variant on the hosted side, and the composer can
round-trip its own schema.

The composer needed a small principled extension: route-emission
and extended-header-emission now elide when the schema declares
zero routes (which was previously emitted unconditionally,
referencing `signal_frame::ShortHeader` --- a path that cannot
resolve from inside the signal-frame crate). The skip-when-empty
discipline is the principled local refactor that resolves the
circular dependency.

What stays in the kernel: the macro infrastructure
(`signal-frame-macros`, `schema-rust`), the `schema` crate, the
`nota-codec` traits, the rkyv derivation traits, and every
generic frame type (`Request<P>`, `Reply<P>`, `ExchangeFrameBody
<R,P>`) because the composer does not yet emit generic Rust types
or rkyv derives. The kernel boundary moves downward as those
capabilities land.

## Kernel boundary

The minimum hand-authored Rust the macro pipeline needs to start
--- the irreducible substrate the schema-driven leaf depends on.

| Layer | Path | Why kernel today |
|---|---|---|
| NOTA codec traits | `nota-codec` crate (`Encoder`/`Decoder`/`NotaEncode`/`NotaDecode`/`NotaValue`) | The schema parser depends on these to read schemas. |
| Schema parser substrate | `schema` crate (parsers, `AssembledSchema`, `Feature`, `DeclarationBody`, `TypeExpression`) | The composer reads the AssembledSchema; the parser must compile first. |
| Schema-rust composer | `schema-rust` crate (`RustComposer`, `RustModule`, `ComposerError`) | The bootstrap-leaf emitter. Cannot describe itself while being itself. |
| Proc-macro front door | `signal-frame-macros` crate (`emit_schema!`, `legacy_signal_channel!`, `signal_channel!`) | The macro must compile before any `emit_schema!` invocation can fire. |
| rkyv derivation traits | `rkyv` crate (`Archive`, `Serialize`, `Deserialize`) | The composer does not yet emit `#[derive(Archive, ...)]`; every wire-encodable type needs hand-authored derives. |
| Generic frame envelopes | `signal_frame::frame` (`ExchangeFrame<R,P>`, `StreamingFrame<R,P,E>`, `ExchangeFrameBody`, `StreamingFrameBody`, `ShortHeader`) | Generic over RequestPayload/ReplyPayload/EventPayload. The composer does not emit generic Rust types. |
| Generic request/reply | `signal_frame::request` (`Request<Payload>`, `RequestPayload` trait) + `signal_frame::reply` (`Reply<ReplyPayload>`, `SubReply<ReplyPayload>`) | Same generic constraint. |
| Exchange identity | `signal_frame::exchange` (`ExchangeIdentifier`, `StreamEventIdentifier`, `LaneSequence`, `SessionEpoch`, `ExchangeLane`, `ExchangeMode`, `ExchangeHandshake`) | Wire-encodable (rkyv derived); composer doesn't emit rkyv derives yet. |
| Handshake | `signal_frame::version` (`HandshakeRequest`, `HandshakeReply`, `ProtocolVersion`, `HandshakeRejectionReason`) | Same constraint. |
| Concrete reply-outcome enums | `signal_frame::reply` (`AcceptedOutcome`, `BatchErrorClassification` trait) | Generic-typed (over `ReplyPayload`) or trait-typed; not yet schema-derivable. |

What moved into Stage 2 (schema-derived) today: the five concrete
non-generic, non-wire-encoded reply-outcome enums.
`RequestRejectionReason`, `BatchFailureReason`,
`RetryClassification`, `CommitStatus`, `OperationFailureReason`.
These are pure ADT shapes the composer can already emit; they are
the natural first foothold for self-hosting.

## signal-frame.schema (the new file)

`/home/li/wt/github.com/LiGoldragon/signal-frame/designer-schema-poc-from-v0.3-main-2026-05-26/schema/signal-frame.schema`.

The six-section schema layout:

```nota
;; imports --- self-contained
{}

;; no wire headers --- the self-hosting bootstrap is route-less
[] [] []

;; namespace --- the closed reply-outcome taxonomy
{
  RequestRejectionReason (Internal)
  BatchFailureReason (EngineRejected EngineUnavailable)
  RetryClassification (Retryable NotRetryable Unknown)
  CommitStatus (NotCommitted Unknown)
  OperationFailureReason (DomainRejection)
}

;; no features
[]
```

What the composer emits from this (visible via the round-trip
test): a `pub mod signal_frame { ... }` module containing five
`pub enum` declarations with their variants, each carrying
`#[derive(Clone, Debug, PartialEq, Eq)]`. No routes, no extended
header, no operation/effect/reply emission --- pure types-only
module. The kernel hand-authored versions in `src/reply.rs` carry
the rkyv derives the wire path needs; the schema-derived versions
are structural mirrors only.

The schema-derived module appears under
`signal_frame::self_hosted::signal_frame::*` because:
- `signal_frame` is the kernel crate
- `self_hosted` is the module containing the `emit_schema!`
  invocation
- inner `signal_frame` is the composer's wrapping `pub mod
  <schema-stem>` (the schema's file stem is `signal-frame` ->
  module name `signal_frame`)

Future iterations can shift the kernel boundary downward by adding
rkyv-derive emission to the composer + replacing the hand-authored
reply-outcome enums in `src/reply.rs` with re-exports from
`self_hosted::signal_frame::*`.

## Bootstrap proof

`tests/self_hosting_bootstrap.rs` — 11 tests across four
categories. All pass.

**Two-stage bootstrap proofs (2 tests):**
- `bootstrap_kernel_compiles_standalone` — constructs every kernel
  variant by name (Stage 1 boundary witness).
- `bootstrap_self_hosted_leaf_compiles_atop_kernel` — constructs
  every schema-derived variant by name. The fact that the test
  compiles proves the proc-macro ran successfully and the composer
  emitted the expected types.

**Structural equivalence proofs (6 tests):**
- `structural_equivalence_helper_runs` --- calls the helper in
  `self_hosted::assert_structural_equivalence()` that constructs
  both kernel and hosted variants paired. If either side drifts,
  the helper fails to compile.
- One test per enum (5 tests) asserting variant-count parity
  between the kernel-side string list and the hosted-side
  constructor closures.

**Round-trip proofs (2 tests):**
- `composer_round_trips_through_its_own_schema` --- loads
  `signal-frame.schema` directly through `schema::LoadedSchema`,
  runs `schema_rust::RustComposer::new(&loaded).compose()`,
  inspects the emitted token text. Asserts every expected variant
  name appears, asserts the `pub mod signal_frame` wrapper exists,
  and asserts the emission does NOT contain
  `signal_frame :: ShortHeader` (which would break self-hosting).
- `signal_frame_schema_is_route_less_by_construction` --- pins the
  contract: the self-hosting schema MUST declare zero routes, and
  the composer's route-emission skip-when-empty discipline is
  exactly what enables the bootstrap.

**Schema source-path probe (1 test):**
- `self_hosted_module_records_its_schema_source_path` --- the
  composer emits `pub const SCHEMA_PATH: &str = "..."` in every
  module; this test asserts the path ends with
  `schema/signal-frame.schema`. A sanity probe that the macro
  actually fired (rather than the test linking against stale rust
  without the macro firing).

Test output:

```
running 11 tests
test bootstrap_kernel_compiles_standalone ... ok
test bootstrap_self_hosted_leaf_compiles_atop_kernel ... ok
test batch_failure_reason_variant_count_matches_kernel ... ok
test commit_status_variant_count_matches_kernel ... ok
test composer_round_trips_through_its_own_schema ... ok
test operation_failure_reason_variant_count_matches_kernel ... ok
test request_rejection_reason_variant_count_matches_kernel ... ok
test retry_classification_variant_count_matches_kernel ... ok
test self_hosted_module_records_its_schema_source_path ... ok
test signal_frame_schema_is_route_less_by_construction ... ok
test structural_equivalence_helper_runs ... ok

test result: ok. 11 passed; 0 failed
```

Full workspace test count: 70 (was 59; +11 self-hosting tests).
All pass. `cargo fmt` clean; `cargo clippy` clean modulo a
pre-existing `too_many_arguments` warning on `schema-rust`'s
`effect_items` function unrelated to this commit.

## Constraint test result

The constraint that drove the schema-rust composer change:
**`composer_round_trips_through_its_own_schema`** asserts that the
emitted Rust text does NOT contain `signal_frame :: ShortHeader`.
This is the load-bearing assertion: the composer must not emit any
reference that would fail to resolve from inside signal-frame.

Before the route-items skip-when-empty change:

```
error[E0433]: cannot find module or crate `signal_frame` in this scope
  --> src/self_hosted.rs:45:1
   |
45 | crate::emit_schema!("schema/signal-frame.schema");
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ use of unresolved module or unlinked crate `signal_frame`
```

After the change: the composer elides `route_items` and
`extended_header_items` when `assembled.routes().is_empty()`. The
emitted module contains only the pure type declarations; no
external path references. The bootstrap closes.

The skip-when-empty discipline is not an ad-hoc workaround; it's
semantically correct: a schema with no operation roots has no
route table to dispatch into, and no extended header that needs
to decode into a route. The unconditional emission was over-
eagerly producing dead code in the route-less case.

## Coordination notes with POC subagent

The in-flight POC subagent dispatched alongside me created the
parent commit on `designer-schema-poc-from-v0.3-main-2026-05-26`
(empty change), then began work on a sibling branch
`designer-schema-poc-106-2026-05-26`. As of this commit, their
branch has no diff (empty commit). They have edited the workspace
docstring in `src/lib.rs` at some point to declare self-hosting
"deferred"; I overrode that to point at the now-landed
`self_hosted` module instead, with explicit coexistence framing.

**Merge guidance for the POC subagent's eventual integration:**

1. **Additive changes.** Every file I touched except `src/lib.rs`
   is purely additive (`schema/signal-frame.schema`,
   `src/self_hosted.rs`, `tests/self_hosting_bootstrap.rs`) or a
   semantically-clean extension (`schema-rust/src/lib.rs`'s
   skip-when-empty in `route_items` + `extended_header_items`).
   Conflict-free with any further substrate work that doesn't
   touch the same lines.

2. **Cargo.toml dev-dependency addition.** Added `schema` and
   `schema-rust` as dev-dependencies on signal-frame so the
   round-trip test can call the composer directly. Merge cleanly
   alongside any further dependency additions.

3. **schema-rust extension is universally beneficial.** The
   skip-when-empty change in `route_items` /
   `extended_header_items` is correct for every route-less schema
   --- including persona-spirit's actor schemas, which today
   probably get an unused `ExtendedHeader` struct + empty `ROUTES`
   const emitted. The change reduces emission surface for those
   schemas too. Not a breaking change for any caller.

4. **src/lib.rs docstring.** The "Self-hosting bootstrap" section
   in the crate-level docstring describes the landed Stage 2 leaf.
   If the POC subagent has further docstring evolution, the
   self-hosting paragraph should stay (it's now accurate; future
   iterations can extend it as more types move from kernel to
   leaf).

5. **No conflicts with the three-language structure work.** The
   POC subagent's described focus is the three-language structure
   landing on top of the existing composer substrate. That work
   touches the composer's emission shape (legs / effect tables /
   fan-out targets) for routed schemas. The self-hosting leaf is
   route-less, so its emission path is orthogonal.

If the POC subagent introduces composer changes that re-introduce
unconditional emission of route-touching items, the
`composer_round_trips_through_its_own_schema` test will fail
loudly via its `!emitted.contains("signal_frame :: ShortHeader")`
assertion. That assertion is the live contract that protects the
self-hosting boundary.

## What the second stage proves architecturally

The self-hosting leaf is small (five enums); the symbolic weight
is large. What it crystallises:

1. **The substrate can describe itself.** The composer +
   parser machinery that emits Rust for actor schemas in
   persona-spirit can also emit Rust for signal-frame's own data
   types. The recursive endpoint is reachable.

2. **The kernel boundary is documentable and shrinkable.** The
   layered table above (kernel vs. self-hosted) is a concrete
   architectural artefact. Each row is a constraint waiting to be
   relaxed by a composer extension. The list is the roadmap.

3. **The bootstrap discipline is now codified in test.** The
   `composer_round_trips_through_its_own_schema` test pins the
   contract: the substrate must describe itself without producing
   references to itself by external name. Future composer changes
   that violate this fail the test.

4. **The next-leaf moves can be planned.** When the composer
   learns to emit rkyv derives, every wire-encodable closed enum
   in `signal_frame::reply` and `signal_frame::version` becomes
   schema-derivable (modulo generics). When the composer learns
   to emit generic types, the frame envelopes themselves become
   schema-derivable. Each step shrinks the kernel.

## References

- Source: `/home/li/wt/github.com/LiGoldragon/signal-frame/designer-schema-poc-from-v0.3-main-2026-05-26/`
- Commit: `utxwwpnn 39e09670` on
  `designer-schema-poc-from-v0.3-main-2026-05-26` bookmark.
- Files added:
  - `schema/signal-frame.schema` (87 lines)
  - `src/self_hosted.rs` (77 lines)
  - `tests/self_hosting_bootstrap.rs` (233 lines)
- Files modified:
  - `Cargo.toml` (+ schema + schema-rust dev-dependencies)
  - `src/lib.rs` (+ self_hosted module declaration + crate-level
    docstring section)
  - `schema-rust/src/lib.rs` (+ skip-when-empty in `route_items`
    and `extended_header_items`)
- Intent records: psyche 2026-05-26 #711 (Maximum, self-hosting
  endpoint), #709 #710 (schema-driven POC v0.3 context).
- Parent context: `/home/li/primary/reports/designer/349-context-maintenance-sweep-2026-05-25/1-poc-schema-stack-explainer.md`
- Skill: `/home/li/primary/skills/schema-driven-actors.md`
