# Component Port Readiness Audit

Assigned scope: read-only audit of adjacent components for the next schema-derived triad stack. Repos inspected: `introspect`, `signal-introspect`, `persona`, `upgrade`, `signal-upgrade`, `owner-signal-upgrade`, plus the clearly adjacent `version-projection`, `signal-version-handover`, `owner-signal-version-handover`, and `spirit-next` as the current working pilot/control.

## Recommendation

The best next port is the `upgrade` triad, not `introspect` or `persona`.

Reasons:

- It is architecturally central to the next wave: `upgrade` is the target home for schema/version migration orchestration, handover driver code, policy, selector control, rollback, and quarantine. A port here exercises the mechanics the later component ports need.
- It has a bounded surface: `signal-upgrade` ordinary verbs, `owner-signal-upgrade` owner verbs, runtime command/effect lowering, one compiled migration, and a handover driver. That is smaller than Persona's engine manager and more structurally meaningful than only porting an observation wrapper.
- It is already partially materialized: all three repos have concept schemas; both contract repos have `signal_channel!` contracts with `observable` Tap/Untap blocks; `upgrade` has `signal-executor` lowering, Sema classification tests, a Unix-socket handover driver test, and a `spirit-sandbox-upgrade-test` app.
- The current gaps are exactly next-stack gaps: replace hand-written contracts/dispatcher/runtime command enums with schema-authored generated Signal/Nexus/SEMA roots and prove CLI to daemon to generated engine path.

`introspect` is the better second port. It has a real old-stack daemon, peer Signal query, Kameo actor root, store, and process-boundary tests, but the port is wider because it must convert an already-running actor component from old `signal_core::SignalVerb` request wrapping into contract-local `Observe` plus generated Tap/Untap and peer subscription consumption.

`persona` should wait. It is large, apex-level, and still mixes manager state, supervision, direct process launching, SCM_RIGHTS handoff, upgrade lifecycle participation, and cross-component Nix composition. It should consume the pattern after a smaller triad proves it.

## Minimal Full E2E Witness

For `upgrade`, the minimal full witness should prove this path:

```text
schema files
  -> schema-next Asschema
  -> schema-rust-next generated Rust in signal-upgrade / owner-signal-upgrade / upgrade
  -> generated Signal Input/Output, Nexus Work/Action, SEMA write/read roots
  -> upgrade CLI accepts one NOTA request
  -> CLI sends binary rkyv signal-frame to upgrade-daemon
  -> daemon dispatches through generated SignalEngine
  -> generated NexusEngine lowers AttemptUpgrade to generated SEMA command/effect roots
  -> generated SemaEngine persists an upgrade event in upgrade-owned state
  -> daemon replies with generated Output over binary rkyv
  -> CLI renders one NOTA reply
  -> testing-trace build emits typed trace events proving Signal/Nexus/SEMA trait calls
```

The concrete first operation should be `AttemptUpgrade` for the existing `persona-spirit` `0.1.0 -> 0.1.1` prototype migration, because current `upgrade` already has catalogue and migration tests around that path.

The negative witnesses should reject the tempting shortcuts:

- daemon rejects NOTA/text bytes on its socket;
- CLI does not open durable state;
- runtime cannot use hand-written `Command` / `Effect` as the load-bearing dispatch path once generated roots exist;
- contract repos contain no daemon/Tokio/redb runtime;
- owner operations cannot be invoked through the ordinary contract;
- handover `Mirror` raw bytes cannot enter the typed database before projection.

## Repo Findings

### `upgrade`

Status: partially ported in intent and prototype mechanics, not schema-next ported.

What exists:

- `schema/upgrade.concept.schema` sketches ordinary and owner operation groups, but it is concept-only and not consumed by build generation.
- `src/execution.rs` has a hand-written `Command` / `Effect` layer using `signal-executor`, with `ToSemaOperation` and `ToSemaOutcome` classification.
- `src/handover.rs` drives real Unix-socket frame exchange using `signal-upgrade` handover operations.
- `src/catalogue.rs` and `src/migrations/persona_spirit/version_0_1_0_to_0_1_1.rs` provide one concrete migration catalogue path.
- `tests/runtime.rs` proves catalogue lookup, Sema classification, `signal-executor` execution, typed rejection, and multi-operation atomic reply.
- `tests/handover_driver.rs` proves marker matching and marker drift rejection over live Unix sockets.
- `flake.nix` exposes build/test checks and a `spirit-sandbox-upgrade-test` app.

Missing for next-stack readiness:

- Real `schema/upgrade.schema` and generated `src/schema/*.rs`; current schema file is `.concept.schema`.
- Generated Signal/Nexus/SEMA plane roots and generated engine traits.
- Daemon socket path that accepts binary `signal-frame` requests and dispatches through generated engine traits. Current `upgrade` and `upgrade-daemon` binaries still print placeholder `RequestUnimplemented` for one argument.
- Durable upgrade state through generated SEMA descriptors: migration catalogue policy, completion/rejection event log, active version event log, quarantine list, and handover history.
- Process-boundary test equivalent to `spirit-next/tests/process_boundary.rs`.
- Testing-trace witness that generated engine trait methods are called.

### `signal-upgrade`

Status: hand-written ordinary contract, useful shape, not schema-next generated.

What exists:

- `schema/signal-upgrade.concept.schema` sketches the desired ordinary surface.
- `src/lib.rs` declares hand-written records and a `signal_channel!` with `Inspect`, `AttemptUpgrade`, `Report`, `AskHandoverMarker`, `ReadyToHandover`, `HandoverCompleted`, `Mirror`, `Divergence`, and `RecoverFromFailure`.
- `observable` block is present with `OperationReceived` and `EffectEmitted`.
- `tests/round_trip.rs` covers Signal-frame and NOTA round trips for catalogue, handover, replies, and raw byte payloads.

Missing:

- Generated contract from schema-next/schema-rust-next.
- Contract-local generated roots compatible with the new triad engine traits.
- Schema-authored ShortHeader/object-name/trace vocabulary.
- Round-trip tests over generated types rather than the macro hand-written surface.

### `owner-signal-upgrade`

Status: hand-written owner contract, useful shape, not schema-next generated.

What exists:

- `schema/owner-signal-upgrade.concept.schema`.
- `src/lib.rs` declares owner policy and selector operations: `Register`, `Allow`, `Block`, `Query`, `ForceFlip`, `Rollback`, `Quarantine`.
- `observable` block is present.
- `tests/round_trip.rs` covers frame and NOTA round trips.

Missing:

- Generated owner contract and generated dispatcher surface.
- Runtime policy state descriptors consumed by `upgrade`.
- Witness that owner-only operations cannot cross the ordinary signal.

### `introspect`

Status: strong old-stack runtime; conceptually ready but not schema-next ported.

What exists:

- `schema/introspect.concept.schema` sketches `Observe`, `Tap`, `Untap`.
- `src/daemon.rs` binds `introspect.sock`, decodes `signal-introspect` frames, and routes through `IntrospectionRoot`.
- `src/runtime.rs` has a real Kameo actor topology: root, target directory, query planner, peer clients, store, and projection.
- `RouterClient` sends a real `signal-router::RouterFrame` Match request for `RouterRequest::Summary`.
- `IntrospectionStore` uses `sema-engine` for `introspect.redb`.
- Nix checks expose daemon socket, router-client live summary, supervision relation, spawn-envelope socket mode, actor runtime truth, and store witnesses.

Missing:

- Replace `signal-introspect`'s old `Match` variants with contract-local `Observe` and mandatory generated `Tap`/`Untap`.
- Generated schema roots and generated Signal/Nexus/SEMA traits for the introspect runtime.
- Actual peer Tap subscription consumption; manager and terminal clients remain scaffolds.
- Full subscribe lifecycle: snapshot, token, pushed deltas, Retract close, final ack.
- Testing-trace generated trait witness.

### `signal-introspect`

Status: hand-written envelope contract with an explicit migration note.

What exists:

- `schema/signal-introspect.concept.schema` sketches `Observe`, `Tap`, `Untap`.
- `ARCHITECTURE.md` already says "MUST IMPLEMENT — three-layer migration".
- Current `src/lib.rs` still uses old `signal_core::signal_channel!` with `Match EngineSnapshot`, `Match ComponentSnapshot`, `Match DeliveryTrace`, and `Match PrototypeWitness`.
- Tests cover frame round trips, canonical NOTA examples, closed enum integrity, four-field delivery trace keys, and wrapper-not-row-bucket discipline.

Missing:

- The migration the architecture calls for: one contract-local `Observe` root with closed payload enum, generated Tap/Untap observability, and `signal-frame` rather than old `signal-core`.
- Generated request/reply roots and object-name trace hooks.

### `persona`

Status: apex manager is heavily implemented, but not a good first schema-next port.

What exists:

- `schema/persona.concept.schema` sketches engine/component/status/policy groups.
- `src/manager.rs`, `src/manager_store.rs`, `src/direct_process.rs`, `src/transport.rs`, and related tests implement manager state, supervision, direct process launching, active-version snapshots, and public socket handoff machinery.
- `Cargo.toml` already depends on `upgrade`, `owner-signal-upgrade`, `signal-upgrade` in dev, `version-projection`, `signal-frame`, and still `signal-core`.
- `ARCHITECTURE.md` correctly narrows Persona's upgrade role after the upgrade-triad merger: Persona starts/stops versioned units; the upgrade triad owns migration catalogue, handover driver, owner commands, and quarantine.

Missing:

- Actual schema-next generation for Persona's manager contract and storage surface.
- Separation from remaining old-stack `signal-core` use.
- A small enough E2E witness. Persona's current witness surface is broad; porting it first risks testing many unrelated concerns before the new stack is proven in a bounded component.

### Adjacent support repos

`version-projection` is library-only and already shaped as the projection/policy substrate. It should not become a daemon port. Its next-stack work is schema-diff-generated `VersionProjection` impls and schema-version hash constants.

`signal-version-handover` and `owner-signal-version-handover` are predecessor/adjacent contracts. Their ordinary and owner surfaces have mostly merged into `signal-upgrade` and `owner-signal-upgrade`. They remain useful historical/reference contracts, but the next port target should be the merged upgrade triad, not these predecessors.

`spirit-next` is already partially ported and is the control case. It has checked-in `schema/lib.schema`, `schema/lib.asschema`, generated `src/schema/lib.rs`, binary-only daemon dependency guards, process-boundary tests, socket-negative tests, runtime-triad tests, and testing-trace packages/tests. It sets the witness bar for the next component.

## Port Order

1. `upgrade` + `signal-upgrade` + `owner-signal-upgrade`: first/next port.
2. `introspect` + `signal-introspect`: second port, using generated Tap/Untap and subscription lifecycle.
3. `persona`: later, after upgrade/introspect prove generated stack mechanics on smaller surfaces.

## Immediate Code/Test Gaps to File or Assign

- Create real schema files for the upgrade triad, not `.concept.schema` sketches.
- Generate checked-in Rust artifacts from schema-next/schema-rust-next and make build freshness fail on stale generated code.
- Replace `upgrade::Command` / `upgrade::Effect` as the load-bearing runtime dispatch with generated Nexus/SEMA roots.
- Add `upgrade-daemon` binary frame serving and keep `upgrade` CLI as one-argument NOTA-to-binary client.
- Add a process-boundary E2E test for `AttemptUpgrade`.
- Add a testing-trace build and trace-socket witness proving generated Signal/Nexus/SEMA trait calls.
- Add owner/ordinary split negative tests.
- Add raw mirror payload separation witness before any typed database write.
