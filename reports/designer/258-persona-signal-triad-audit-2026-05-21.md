# 258 — persona-signal triad audit (engine-manager)

*Audit of the engine-manager triad: `signal-persona` (the
contract) + `persona` (the daemon binary) + `persona` thin CLI.
None of the /257-flagged issues are fixed in this triad. Six new
issues specific to this triad surface.*

## 0 · TL;DR

The engine-manager triad is the workspace's apex infrastructure
component. Spirit was migrated to signal-frame, contract-local
verbs, and signal-executor (per /255 / /256). **The engine-manager
triad has not yet been touched by any of that work.**

State summary:

- `signal-persona` contract has been **partially** migrated:
  contract-local verbs (`Launch`, `Query`, `Retire`, `Start`,
  `Stop`) for the Engine channel ✓; supervision channel uses
  `Announce`, `Query`, `Stop` ✓.
- But: **/252 rename not executed** — 24+ `supervision`/`Supervision*`
  references; zero `engine_management`/`EngineManagement`.
- `persona` daemon **does not use signal-executor** — same gap
  that /255 surfaced for spirit (now resolved for spirit, still
  present here).
- `UnknownKindForVerb` references in **both** the contract (3
  refs) and the daemon (`persona/src/request.rs` — 2 refs);
  covered by bead `primary-k3bu`.
- Three hand-written codec impls in the contract (Query,
  SupervisionUnimplementedReason, supervision::Query); covered by
  bead `primary-u0lh`.
- **No observable block** on either signal-persona channel —
  engine manager is itself a persona component but is currently
  not Tappable. Per `intent/persona.nota` 2026-05-21T10:00:00Z
  (*"debug the debugger"*), it should be.
- Several contract-specific smells flagged in §2 below.

**Priority for the triad's migration slice**: bead `primary-k3bu`
first (codec rename — unblocks compile); then /252 (engine-
management rename); then persona-onto-signal-executor migration;
then observable block + the smaller cleanups.

## 1 · /257 findings status (mostly unfixed)

### /257 §1.13 — `supervision::` namespace stale

**Status: NOT FIXED.** Verified by grep:

```text
signal-persona/src/lib.rs:        24 supervision/Supervision references
                                  0  engine_management/EngineManagement
```

Specifically still in `signal-persona/src/lib.rs`:

- `SupervisionProtocolVersion` (line 335)
- `SupervisionUnimplementedReason` (line 472), `SupervisionUnimplemented` (line 528)
- `pub mod supervision` (line 555) — should be `engine_management`
- `signal_channel! { channel Supervision { ... } }` (line 614-628) — should be `EngineManagement`
- `supervision::Query` (line 568)
- Re-exports `SupervisionFrame`, `SupervisionFrameBody`,
  `SupervisionOperation`, `SupervisionOperationKind`,
  `SupervisionReply`, `SupervisionReplyKind` (lines 631-634)

Plus `SpawnEnvelope` fields `supervision_socket_path`,
`supervision_socket_mode`, `supervision_protocol_version` (lines
548-552) — all stale per /252.

In the daemon (`persona/src/`):

- `supervisor.rs` (file name) — should be `engine_manager.rs`
- `EngineSupervisor` struct + `EngineSupervisorInput` +
  `EngineSupervisorFailure` (lines 30, 43, 68, etc.)
- `supervision_readiness.rs` (file name) — should be
  `engine_management_readiness.rs`
- `ComponentSupervisionReadiness`, `ComponentSupervisionExpectation`,
  `ComponentSupervisionReadinessFailure` (referenced in supervisor.rs:24-26)
- `PrototypeSupervisionReport` (line 68 of supervisor.rs)
- `started_supervision_count` / `stopped_supervision_count` fields
  (lines 38-39)

Wide rename scope.

### /257 §1.6 — `*RequestUnimplemented.operation` redundancy

**Status: ALREADY CLEAN.** signal-persona's `SupervisionUnimplemented`
already only has `reason: SupervisionUnimplementedReason` (line
528-531). No redundant operation field. ✓

### /257 §1.7 — empty marker records

**Status: NOT PRESENT in this contract.** signal-persona doesn't
have empty marker structs.

### /257 §1.10 — frame type alias boilerplate

**Status: NOT FIXED (cross-workspace bead `primary-77hh`).** The
contract has the dance — `SupervisionFrame`, `SupervisionFrameBody`,
`SupervisionOperation` etc. re-exported via `pub use supervision::{...}`
(lines 631-634). The Engine channel's macro-emitted types
(`EngineFrame`, `EngineFrameBody`, etc.) are emitted but the
contract doesn't re-alias them (a reader has to use the prefixed
forms directly). Inconsistent within the same crate.

### /257 §1.11 — no observable block

**Status: NOT FIXED for this triad.** Neither the `Engine` channel
nor the `Supervision` channel declares an observable block. Per
`intent/persona.nota` 2026-05-21T10:00:00Z (*"debug the debugger"*),
the engine-manager is itself a persona component and should be
Tappable.

Two questions:
- Should the **Engine channel** be observable? (Watching the
  manager's external surface — engine launches, retirements,
  component start/stop requests — is useful meta-introspection.)
- Should the **Supervision/EngineManagement channel** be
  observable? (Watching manager↔component traffic could help
  debug bringup races but is a high-volume internal stream.)

Designer lean: Engine channel observable yes (public-facing
surface needs cross-component class-level monitoring like every
other persona component); Supervision channel **no** observable
block (internal infrastructure traffic; persona-introspect
shouldn't double-subscribe to both the manager and each
component's domain channel for the same effective view).

Confirm before adding.

### /257 §1.12 — single-field timestamps

**Status: NOT FIXED.** `TimestampNanos(u64)` at line 398. Used for
`component_started_at`, `drain_completed_at`. Subject to the still-
open psyche call on whether runtime/protocol timestamps stay
single-field or split to two like intent records.

### /257 §1.5 — ancestry prefixes

**Status: MIXED.** Most types in signal-persona are clean
(`ComponentName`, `EngineGeneration`, `EnginePhase`, `ComponentKind`,
`EngineStatus`, `EngineLaunch`, `EngineCatalog`, `PeerSocket`,
`SpawnEnvelope`). But some carry ancestry:
- `EngineLabel` — `Engine` is the contract's domain; fine.
- `LaunchAcceptance` / `LaunchRejection` / `RetirementRejection`
  / `ActionAcceptance` / `ActionRejection` — clean noun forms.
- `ComponentHealthReport` — `Component` is fine (the contract is
  about components and engines).
- See §2.1 for `GracefulStopAcknowledgement`.

### /257 §3 — bead coverage

The three building-block beads cover this triad's mechanical work:

- **`primary-77hh`** (frame alias-dance) — applies to both
  channels in signal-persona; fixes EngineFrame/EngineFrameBody
  and SupervisionFrame/SupervisionFrameBody emissions.
- **`primary-k3bu`** (UnknownKindForVerb rename) — applies to
  signal-persona/lib.rs (3 sites) and persona/src/request.rs (2
  sites).
- **`primary-u0lh`** (extend nota-codec derive coverage) — covers
  signal-persona's three hand-written codec impls (`Query`,
  `SupervisionUnimplementedReason`, `supervision::Query`); all
  three should move to `#[derive(NotaSum)]` or `#[derive(NotaEnum)]`.

## 2 · New findings specific to this triad

### 2.1 — `GracefulStopAcknowledgement` ancestry word

`signal-persona/src/lib.rs:455-457`:

```rust
pub struct GracefulStopAcknowledgement {
    pub drain_completed_at: Option<TimestampNanos>,
}
```

The `Graceful` prefix is redundant. The Supervision channel has
exactly one stop operation (`Stop(ComponentName)`); there is no
contrasting "ForceKill" or "Abort" verb. "Graceful" disambiguates
nothing — the contract guarantees stops are graceful.

Per ESSENCE §Naming: drop the redundant word. The type becomes
`StopAcknowledgement`.

Fields: `drain_completed_at: Option<TimestampNanos>` — clean
shape (an `Option` carrying "if we drained, when did the drain
finish"). The single-field timestamp question (§/257 §1.12) still
applies.

### 2.2 — persona daemon does not use signal-executor

The persona daemon's `Cargo.toml` does not depend on
`signal-executor`. No `use signal_executor::` imports across
`persona/src/*.rs`. No `Executor::new` calls. No `Lowering for`
impls. No `CommandExecutor for` impls.

This is exactly the gap /255 Finding 1 flagged for spirit pre-
migration. Spirit was migrated; persona-daemon was not.

The pattern that should apply (per /255 / /256):

```rust
struct EngineLowering { ... }
impl Lowering for EngineLowering {
    type Operation = EngineOperation;
    type Reply = EngineReply;
    type Command = EngineCommand;      // local enum
    type ComponentEffect = EngineEffect;  // local enum
    fn lower(...) -> Result<OperationPlan<EngineCommand>, EngineReply> { ... }
    fn reply_from_effects(...) -> EngineReply { ... }
}

struct EngineCommandExecutor { ... }
impl CommandExecutor for EngineCommandExecutor { ... }

impl BatchErrorClassification for EngineError { ... }
```

Today the request handling is in `persona/src/manager.rs` /
`request.rs` / `engine.rs` and dispatches directly through the
Kameo actor mesh. The `EngineSupervisor` actor *is* the closest
thing to a `CommandExecutor` but doesn't expose the signal-
executor surface.

This is non-trivial work. Persona daemon is larger than spirit;
the actor mesh is more involved. But the migration is structurally
the same as spirit's: wrap the actor mesh inside a
`CommandExecutor` impl; let signal-executor's `Executor::execute`
handle the request decode → lowering → atomic-batch → reply
correlation.

**This is the load-bearing next-slice item for the engine-manager
triad** once the smaller beads land. Filed as a candidate bead
below (recommendation §3).

### 2.3 — Engine channel emits no observable block; Supervision channel emits no observable block

Per `intent/persona.nota` 2026-05-21T10:00:00Z, every persona
component is observable. Engine manager is a persona component.

The current contract:

```rust
signal_channel! {
    channel Engine {
        operation Launch(EngineLaunch),
        ...
    }
    reply EngineReply { ... }
    // <-- no observable block
}

// later:
pub mod supervision {
    signal_channel! {
        channel Supervision {
            operation Announce(Presence),
            ...
        }
        reply SupervisionReply { ... }
        // <-- no observable block
    }
}
```

Add:

```rust
observable {
    filter default;
    operation_event OperationReceived;
    effect_event EffectEmitted;
}
```

to the Engine channel (at least). Designer lean: skip on
Supervision/EngineManagement (per §1's question) but confirm with
psyche.

### 2.4 — Engine vs Supervision channels: inconsistent module placement

`signal-persona/src/lib.rs`:

```rust
// Engine channel at top level (line 301-321):
signal_channel! { channel Engine { ... } }

// Supervision channel in a module (line 555-628):
pub mod supervision {
    signal_channel! { channel Supervision { ... } }
}
pub use supervision::{ SupervisionFrame, ... };  // re-exports
```

The `Engine` channel sits at the crate top level; the
`Supervision` channel sits in a `pub mod supervision`. Why the
asymmetry?

This is exactly the use case psyche named in 2026-05-21T10:30:00Z:
two channels in one crate, use modules to disambiguate. After bead
`primary-77hh` lands (drop channel-name prefix from macro
emissions), the natural shape is:

```rust
pub mod engine {
    signal_channel! { channel Engine { ... } }
    // emits Frame, FrameBody, Operation, Reply, ObserverFilter, etc.
}

pub mod engine_management {            // post-/252
    signal_channel! { channel EngineManagement { ... } }
    // same emitted name set
}
```

Then consumers write `signal_persona::engine::Frame` vs
`signal_persona::engine_management::Frame`. Clean.

The current `pub use supervision::{...}` re-export at line 631-634
**defeats the module isolation** the `pub mod supervision`
provides — both `signal_persona::SupervisionOperation` and
`signal_persona::supervision::SupervisionOperation` are reachable.
Once the unprefixed-emit macro fix lands, the re-export should be
removed and consumers should write the explicit module path.

### 2.5 — `EngineOperationKind` is hand-maintained AND propagates outward

`persona/src/engine_event.rs` lines 1-9:

```rust
pub use signal_persona::EngineOperationKind;
pub use signal_persona_harness::HarnessOperationKind;
pub use signal_persona_message::MessageOperationKind;
pub use signal_persona_mind::MindOperationKind;
pub use signal_persona_system::SystemOperationKind;
pub use signal_persona_terminal::TerminalOperationKind;
```

Persona daemon re-exports *every contract's* OperationKind enum.
Each is hand-maintained per /257 §3.1. Total ~70 variants across
six enums, all derivable from the operation declaration of each
contract.

This is the bead 77hh second concern (auto-generate OperationKind).
Once that lands, every `*OperationKind` enum is macro-emitted and
this re-export block stays the same (the consumer just imports the
macro-emitted name) — but the **drift risk** disappears: contracts
can't add an operation variant without the OperationKind updating.

### 2.6 — `SpawnEnvelope` carries the wide envelope of supervised-component startup

`signal-persona/src/lib.rs:540-553`:

```rust
pub struct SpawnEnvelope {
    pub engine_id: signal_persona_auth::EngineId,
    pub component_kind: ComponentKind,
    pub component_name: signal_persona_auth::ComponentName,
    pub owner_identity: signal_persona_auth::OwnerIdentity,
    pub state_dir: WirePath,
    pub domain_socket_path: WirePath,
    pub domain_socket_mode: SocketMode,
    pub supervision_socket_path: WirePath,     // <-- /252 stale
    pub supervision_socket_mode: SocketMode,    // <-- /252 stale
    pub peer_sockets: Vec<PeerSocket>,
    pub manager_socket: WirePath,
    pub supervision_protocol_version: SupervisionProtocolVersion,  // <-- /252 stale
}
```

Twelve fields. Honest — that's what each child needs to bind its
sockets and find its peers. But three fields are stale per /252:

- `supervision_socket_path` → `engine_management_socket_path`
- `supervision_socket_mode` → `engine_management_socket_mode`
- `supervision_protocol_version` → `engine_management_protocol_version`

Field type `SupervisionProtocolVersion` → `EngineManagementProtocolVersion`.

When /252 lands, every supervised daemon's startup code that reads
these fields needs the same rename.

`signal_persona_auth::OwnerIdentity` is interesting — comes from
the auth crate, not the persona crate. signal-persona-auth carries
the universal identity types (EngineId, ComponentName,
OwnerIdentity). Keep there.

Note also: `ComponentName` appears in BOTH `signal-persona`
(line 41) AND `signal_persona_auth::ComponentName`
(`SpawnEnvelope.component_name` is the auth one). One should retire.
Designer call: auth owns identity types; signal-persona's local
ComponentName retires.

### 2.7 — `persona/src/bin/wire_*` test binaries hand-roll wire decoding

```text
persona/src/bin/
  persona_component_fixture.rs
  persona_daemon.rs
  wire_decode_message_reply.rs
  wire_decode_message.rs
  wire_emit_message_reply.rs
  wire_emit_message.rs
  wire_router_client.rs
  wire_tap_router.rs
```

Six `wire_*` binaries that hand-emit / hand-decode signal frames
for testing. These would benefit from the `nota-codec` derive
coverage bead — if the contracts use derives, the wire roundtrip
becomes a generic harness rather than per-binary hand-rolled code.

Low priority; flagging because the binaries are themselves a
discovery surface of contract shape (they assume the contract is
correct; any /252 rename touches them).

## 3 · Recommended next slice for the engine-manager triad

In priority order:

1. **`primary-k3bu`** (rename UnknownKindForVerb in consumers).
   Unblocks compile against current nota-codec.
2. **Execute /252** (engine-management rename in signal-persona +
   persona daemon). Scope: ~24 contract references + ~5 daemon
   file/type renames + every supervised daemon's
   supervision_socket_* startup fields. Big mechanical pass; no
   design call needed since /252 already specs it.
3. **`primary-u0lh`** (extend nota-codec derive coverage; migrate
   hand-written codec impls). Three impls in signal-persona move to
   derives.
4. **`primary-77hh`** (drop channel-name prefix from macro). Then
   reshape signal-persona's two channels into `pub mod engine` +
   `pub mod engine_management` per /257 §3.4. Drop the
   `pub use supervision::{...}` re-export.
5. **Add observable block** to the Engine channel
   per /257 §1.11 + 2026-05-21T10:00:00Z. Confirm with psyche on
   the EngineManagement channel before adding there.
6. **Migrate persona daemon onto signal-executor** (the §2.2 work).
   This is the load-bearing structural change. Mechanically:
   - Define `EngineCommand` / `EngineEffect` enums in persona/src/.
   - Implement `Lowering for EngineLowering` wrapping the current
     manager's request-handling logic.
   - Implement `CommandExecutor for EngineCommandExecutor` wrapping
     the existing Kameo actor mesh.
   - Implement `BatchErrorClassification for EngineError`.
   - Wire `signal_executor::Executor::execute(request).await`
     into the daemon's socket handling.
   - Migrate `persona/src/bin/wire_*` test fixtures to use the
     framework path.
7. **Drop `Graceful` from `StopAcknowledgement`**. Small.
8. **Designer follow-up**: decide whether the EngineManagement
   channel needs Tap/Untap (per §1, designer lean: no).

Beads worth filing (subject to psyche approval):

- A new bead "Migrate persona daemon onto signal-executor"
  modeled on /255's template for spirit. Same shape, different
  actor mesh.

## 4 · Cross-cutting note

The engine-manager triad's migration is **structurally identical**
to spirit's migration that landed in /255 / /256:

| Step | Spirit | Engine-manager |
|---|---|---|
| signal-core → signal-frame | done (`33ab226`) | done (`0b8adc2`) |
| Old verbs → contract-local | done (`33ab226`) | done (`0b8adc2`) |
| Subscription collapse | done (`d87e4055`) | n/a (engine has no subscription replies) |
| Field/empty-marker cleanup | done (`d87e4055`) | partial (GracefulStop ancestry remains) |
| Daemon onto signal-executor | done (`786ab311`) | **NOT DONE** |
| Observable block | done (`a1909872`) | **NOT DONE** |
| `*Unimplemented.operation` drop | done (`d87e4055`) | already clean |
| Timestamp two-field | open (psyche call) | open |

The engine-manager triad is roughly half-migrated. Bead landings +
/252 execution close most of the gap; signal-executor migration is
the structural piece that brings parity with spirit.

## 5 · References

- `/252` — engine-management rename plan (unexecuted).
- `/255`, `/256` — spirit migration template (the engine-manager
  triad should follow the same shape).
- `/257` — workspace-wide name/shape audit.
- `intent/persona.nota` 2026-05-20T14:30:00Z + 14:50:00Z —
  engine-manager rename Decision.
- `intent/persona.nota` 2026-05-21T10:00:00Z — debug-the-debugger
  Clarification (every persona component is observable, including
  the apex).
- `intent/component-shape.nota` 2026-05-21T10:30:00Z — modules-
  not-options for macro disambiguation.
- Beads: `primary-77hh`, `primary-k3bu`, `primary-u0lh`.
- Code: `signal-persona/src/lib.rs`, `persona/src/*.rs`.

This report retires when (a) /252 is executed AND persona daemon
is migrated onto signal-executor AND the observable block is
added AND the smaller cleanups land, OR (b) a successor audit
supersedes.
