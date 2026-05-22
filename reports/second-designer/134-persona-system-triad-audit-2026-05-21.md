# 134 — persona-system triad audit

*Audit of the persona-system triad: `signal-persona-system` (working
contract) + `persona-system` (daemon binary + thin CLI). The owner
signal contract `owner-signal-persona-system` does NOT exist; this
report proposes one. The component is **paused** per its own
`ARCHITECTURE.md` §1.5 and the workspace's `protocols/active-repositories.md`
("Deferred system observation component"). The audit is conservative
about owner-side scope on purpose.*

## 0 · TL;DR

The persona-system triad is **stale and half-shaped**:

- **`signal-persona-system`** is still on `signal_core` with the
  old universal-verb shape (`Subscribe FocusSubscription`,
  `Retract FocusSubscriptionRetraction`, `Match FocusSnapshot`,
  `Match SystemStatusQuery`). Every workspace-wide /257 pattern
  fires here: universal-verb prefixes, `System*` ancestry on most
  types, `*RequestUnimplemented { operation, reason }` redundancy,
  no observable block, and the specific single-variant-enum
  speculative-future shape called out in
  `reports/operator/150-triad-signal-sema-migration-current-state.md` §6.6
  (system contract should NOT preserve speculative single-variant
  enums for future window-manager backends).
- **`persona-system` daemon** does not depend on `signal-executor`,
  hand-rolls its own frame codec
  (`persona-system/src/daemon.rs:206-291`), reads the
  `PERSONA_SOCKET_MODE` environment variable on a daemon
  (`persona-system/src/daemon.rs:136-141` — daemons never read
  env vars per `intent/component-shape.nota` 2026-05-20T13:00:00Z),
  and uses `Supervision*` vocabulary that /252 retired in favour of
  engine-management.
- **`owner-signal-persona-system` is MISSING.** This is the load-bearing
  gap. The ARCHITECTURE.md already names privileged actions
  (`ForceFocus`, `SuppressDrift`) and a privileged-vs-observation
  authority boundary as deferred work; that authority surface is
  what an owner signal contract carries. The persona-system daemon
  is **stateful** (focus subscription registrations, backend cursors,
  the `FocusTracker` actor's recorded state), so it falls under the
  universal owner-contract rule from
  `intent/component-shape.nota` 2026-05-20T12:11:26Z.

The system component sits in a deferred state, but the owner signal
contract is part of the triad and ships with the daemon, not after it
(`skills/component-triad.md` §"4. Two authority tiers"). The conservative
proposal in §3 of this report covers only the operations that are
already discussed in `ARCHITECTURE.md` and existing intent; speculative
additions are flagged explicitly and held back.

**Priority for the triad's migration slice** (in order):

1. Confirm psyche scope on the owner signal proposal in §3 (named
   privileged operations, lifecycle scope question).
2. Workspace mechanical: rename `Supervision*` → `EngineManagement*` per /252;
   migrate `signal_core` → `signal-frame`; rename to contract-local verbs.
3. Collapse the speculative single-variant enums per /150 §6.6.
4. Drop `System*` ancestry prefixes per /257 §1.5 and ESSENCE §Naming.
5. Migrate the daemon onto `signal-executor`.
6. Create the `owner-signal-persona-system` repository populated with
   the §3 proposal.
7. Add the observable block.

## 1 · /257 findings status

This triad has not been touched by the /255 / /256 spirit migration
or the /258 engine-manager audit. Every applicable /257 finding is
present.

### /257 §1.1 — Universal-verb shape — NOT FIXED

`signal-persona-system/src/lib.rs:303-330` (the only channel
declaration in the contract):

```text
request SystemRequest {
    Subscribe FocusSubscription(FocusSubscription) opens FocusEventStream,
    Retract FocusSubscriptionRetraction(FocusSubscriptionToken),
    Match FocusSnapshot(FocusSnapshot),
    Match SystemStatusQuery(SystemStatusQuery),
}
```

All four operations carry universal-verb prefixes
(`Subscribe / Retract / Match`). Per
`intent/component-shape.nota` 2026-05-19T19:45:00Z (Sema verbs
retired at the public contract layer) and 2026-05-20T02:00:00Z
(three-layer model), this should be contract-local verbs only.
Proposed shape lives in §2.4 below.

### /257 §1.2 — Doubling smell — present

`Match FocusSnapshot(FocusSnapshot)` and
`Match SystemStatusQuery(SystemStatusQuery)` — variant tag equals
payload type name. Two instances, both clean up under the §2.4
parent-enum lift.

### /257 §1.5 — Ancestry prefixes — present

`signal-persona-system` repeats `System*` on the following types
that the crate's namespace already supplies:

- `SystemTarget` (`signal-persona-system/src/lib.rs:46`) → `Target`
- `SystemBackend` (line 175) → `Backend`
- `SystemHealth` (line 261) → `Health`
- `SystemReadiness` (line 268) → `Readiness`
- `SystemStatusQuery` (line 170) → covered by the query-lift in §2.4
- `SystemStatus` (line 254) → `Status` (or covered by reply-lift)
- `SystemRequestUnimplemented` (line 290) → `RequestUnimplemented`
- `SystemUnimplementedReason` (line 295) → `UnimplementedReason`
- `SystemOperationKind` (line 182) → `OperationKind` (macro-emit
  once `primary-77hh`-style prefix-drop lands)
- `SystemDaemonConfiguration` (line 361) → `DaemonConfiguration`

Keep: `NiriWindowId` (line 63) — `Niri` is a backend brand name,
not an ancestor of the crate. `WindowClosed` (line 220) — `Window`
is the domain noun, not the crate name. `ObservationGeneration`
(line 123) — `Observation` is the domain.

### /257 §1.6 — `*RequestUnimplemented { operation, reason }` — present

`signal-persona-system/src/lib.rs:290-293`:

```text
pub struct SystemRequestUnimplemented {
    pub operation: SystemOperationKind,
    pub reason: SystemUnimplementedReason,
}
```

Drop the `operation` field; per-operation replies are positionally
addressed (per the spirit fix template). Keep only `reason`.

### /257 §1.7 — Empty marker records — none

The contract has no empty struct payloads. Clean ✓.

### /257 §1.8 — Single-variant enums — present, called out explicitly

Per `reports/operator/150` §6.6 (*"the system contract should NOT
preserve speculative single-variant enums for possible future
window-manager backends. Use today's concrete shape; introduce an
enum when a second real backend appears."*):

- `SystemTarget` is `enum { NiriWindow(NiriWindowId) }`
  (line 46-48). The docstring at lines 41-45 is explicit
  speculative scaffolding (*"Currently only Niri windows; future
  backends (Mac, Hyprland, etc.) add variants through a coordinated
  schema upgrade..."*).
- `SystemBackend` is `enum { Niri }` (line 175-177). Same shape.
- `SubscriptionKind` is `enum { Focus }` (line 234-237).

Per ESSENCE.md §"What I am not optimising for" (no speculative
extensibility) and the /150 directive, all three collapse. Concrete
shape:

- `SystemTarget` becomes a transparent alias for `NiriWindowId` — or
  drop the type and use `NiriWindowId` directly at every use site.
  The latter is cleaner because the docstring's "what does this
  type model" question already has the answer `NiriWindowId`.
- `SystemBackend` retires entirely; the daemon presents a Niri
  backend without a typed wrapper enum. When a second backend
  appears, introduce the enum with both real variants then.
- `SubscriptionKind` retires; the subscription is always a focus
  subscription today, so the `kind` field in `SubscriptionAccepted`
  retires alongside.

This collapses the `SubscriptionAccepted` record too — with
`kind: SubscriptionKind::Focus` gone, the record becomes
`{ target: Target }`. With `target` being the only field on
`FocusSubscription` already (line 138-141), `SubscriptionAccepted`
could just echo back the `FocusSubscriptionToken` like
`SubscriptionRetracted` does. See §2.2 for the proposed shape.

### /257 §1.9 — Frame type alias boilerplate — present

The contract emits `SystemFrame`, `SystemFrameBody`, etc. (consumed
in `persona-system/src/daemon.rs:11-14` and `lib.rs:13`). Today the
contract does not have the alias-dance block (no
`pub type Frame = SystemFrame;`), so consumers reach for the
channel-prefixed forms. Once the macro-side prefix-drop bead
(`primary-77hh`, *the signal-frame macro prefix-drop work*) lands,
the macro should emit `Frame`, `FrameBody`, etc. directly and this
contract benefits with no extra work.

### /257 §1.10 — Missing observable block — present

Per `intent/component-shape.nota` 2026-05-20T02:00:00Z (Tap/Untap is
mandatory for persona components, no author override) and
`intent/persona.nota` 2026-05-21T10:00:00Z (debug the debugger —
every persona component is observable including the apex):

`signal-persona-system` does not declare an observable block.
Required:

```text
observable {
    filter default;
    operation_event OperationReceived;
    effect_event EffectEmitted;
}
```

`persona-system` is unambiguously a persona component (it carries
the `persona-` prefix, sits in the persona authority chain, and is
named in `signal-persona`'s `ComponentKind` alongside the other
persona components). The mandate applies.

The "paused" state in `ARCHITECTURE.md` §1.5 does not exempt the
contract from declaring the observable surface — observable is
declared today; emission can be a no-op until the focus subscription
path activates.

### /257 §1.12 — Single-field timestamps — partially present

The contract has no inline `TimestampNanos`-shape field today.
However, `SubscriptionAccepted`, `FocusObservation`, and
`SystemStatus` are unstamped — observation events don't carry a
timestamp on the wire. The /257 §1.11 boundary
(*"protocol/runtime timestamps may be OK as single fields"*) is
not violated. The two-field timestamp rule is intent-record-specific.

When the focus event-stream unpauses, the question whether
`FocusObservation` should be daemon-stamped (per
`intent/persona.nota` 2026-05-20 21:53 — spirit's daemon-stamped
date/time rule) is a real open. Designer lean: yes — focus
observations are facts the daemon witnessed, not facts the caller
asserts; daemon-stamping carries provenance. Held back pending
psyche call.

### /257 §1.13 — `supervision::` namespace stale — present

Wider than just the namespace: `SpawnEnvelope` in `signal-persona`
already names `supervision_socket_path` / `supervision_socket_mode`
/ `supervision_protocol_version` (per /258 §2.6). `SystemDaemonConfiguration`
mirrors this at `signal-persona-system/src/lib.rs:366-369`:

```text
pub supervision_socket_path: signal_persona::WirePath,
pub supervision_socket_mode: signal_persona::SocketMode,
```

These two fields rename to `engine_management_socket_path` and
`engine_management_socket_mode` when /252 lands. Daemon-side
references in `persona-system/src/daemon.rs:33-39` and
`persona-system/src/supervision.rs` rename to match.

### /257 §3 — Bead coverage

The three building-block beads from /257 §3 apply here:

- **`primary-77hh`** *(signal-frame macro: drop channel-name prefix
  from emitted types)* — applies; once it lands, the contract gets
  unprefixed `Frame`, `FrameBody`, etc. for free.
- **`primary-k3bu`** *(consumer rename of UnknownKindForVerb)* —
  search needed; if `signal-persona-system` and `persona-system`
  reference `UnknownKindForVerb` (likely, given the contract has an
  `operation_kind()` method), the rename applies.
- **`primary-u0lh`** *(extend nota-codec derive coverage)* — applies;
  the contract has hand-written codec impls at lines 87-106
  (`SystemTarget`). With the §1.8 collapse to a transparent alias,
  the hand-written codec retires entirely. Other types are already
  derived.

## 2 · New findings specific to this triad

### 2.1 — Persona-system daemon does not use signal-executor

`persona-system/Cargo.toml` does not depend on `signal-executor`.
The daemon hand-rolls request handling in
`persona-system/src/daemon.rs:111-125` and
`SystemRequestHandler::reply_for_request` (lines 409-427). It
bypasses the canonical execution shape entirely.

Same gap /255 surfaced for spirit pre-migration and /258 §2.2
surfaced for the engine-manager. The fix is the same template:

- Define `Command` and `Effect` enums in `persona-system/src/`.
  Today's two real commands are `RecordSystemStatusServed` and
  `EmitFocusObservation` (the second deferred until unpause).
- Implement `Lowering for SystemLowering` wrapping the current
  `SystemSupervisor` actor logic.
- Implement `CommandExecutor for SystemCommandExecutor` over the
  Kameo actor (already there as `SystemSupervisor`).
- Implement `ToSemaOperation for Command` (Match for status query,
  Subscribe for the focus subscription path, Assert for an
  observation emit).
- Implement `ToSemaOutcome for Effect`.
- Wire `signal_executor::Executor::execute(request).await` into
  the daemon's socket handler at
  `persona-system/src/daemon.rs:111-125`.

This work is **load-bearing** for the triad's parity with spirit
and engine-manager. The "paused" status does NOT defer it — the
executor migration is structural, not domain.

### 2.2 — The current SubscriptionAccepted/SubscriptionRetracted asymmetry

Current shape (lines 226-237):

```text
pub struct SubscriptionAccepted {
    pub target: SystemTarget,
    pub kind: SubscriptionKind,
}

pub enum SubscriptionKind { Focus }

pub struct SubscriptionRetracted {
    pub token: FocusSubscriptionToken,
}
```

`SubscriptionAccepted` carries `(target, kind)`;
`SubscriptionRetracted` carries the typed `FocusSubscriptionToken`.
The retraction shape is correct (per /181's Path A discipline cited
in the contract header). The acceptance shape is **structurally
mismatched** — it should also carry the token, so the caller can
correlate.

Today `FocusSubscriptionToken` is itself just `{ target: SystemTarget }`
(line 150-153), so `SubscriptionAccepted { target, kind: Focus }`
is almost the same data. But once `SubscriptionKind` retires (per
§1.8), the natural shape is:

```text
pub struct SubscriptionAccepted {
    pub token: FocusSubscriptionToken,
}
```

Symmetric with `SubscriptionRetracted`. The caller's
"correlate this ack to that request" workflow becomes one shape on
both sides.

If `FocusSubscriptionToken` later grows beyond `{ target }` (e.g.,
to disambiguate concurrent subscriptions on the same target — a
real future need), the symmetric shape continues to work.

### 2.3 — `FocusSnapshotReply` variant has the `Reply` suffix smell

`signal-persona-system/src/lib.rs:317`:

```text
FocusSnapshotReply(FocusObservation),
```

The reply variant carries the `Reply` suffix even though it sits
inside the `SystemReply` enum — restating the namespace (per /257
§1.5 and the second-operator-assistant /11 smell catalogue entry
*"`*Order` / `*Request` / `*Reply` suffix duplicating the variant's
role"*).

Drop the suffix. The variant is `FocusSnapshot(FocusObservation)`.
The payload is `FocusObservation` (already correct — past-tense
descriptive noun naming what was observed).

### 2.4 — Tree-shape of operations and replies

Applying contract-local verbs, the parent-enum lift for queries,
and the §1.8 collapse, the proposed working signal tree:

```text
signal_channel! {
    channel System {
        operation Watch(FocusSubscription) opens FocusEventStream,
        operation Unwatch(FocusSubscriptionToken),
        operation Query(Query),
    }
    reply Reply {
        Watching(SubscriptionAccepted),
        Unwatched(SubscriptionRetracted),
        Queried(QueryResult),
        ObservationTargetMissing(ObservationTargetMissing),
        RequestUnimplemented(RequestUnimplemented),
    }
    event Event {
        FocusObservation(FocusObservation) belongs FocusEventStream,
        WindowClosed(WindowClosed) belongs FocusEventStream,
    }
    stream FocusEventStream {
        token FocusSubscriptionToken;
        opened SubscriptionAccepted;
        event FocusObservation;
        close Unwatch;
    }
    observable {
        filter default;
        operation_event OperationReceived;
        effect_event EffectEmitted;
    }
}

pub enum Query {
    FocusSnapshot(FocusSnapshot),
    Status(StatusQuery),
}

pub enum QueryResult {
    FocusSnapshot(FocusObservation),
    Status(Status),
}
```

Notes:

- `Watch` and `Unwatch` are the standard subscription open/close
  verbs settled in /256's spirit migration and named in /150 §3.
  `Subscribe` (the universal Sema verb) drops away.
- `Query` lifts the two read operations (one-shot focus probe +
  status) into a typed sum. With only two read targets today the
  lift is borderline by /257's "third sibling" rule, but the
  tree-shape is already the workspace's convergent pattern (per
  /150 §6 + /256 + second-operator-assistant /11 §2). Lifting now
  is conservative — it costs little and matches the rest of the
  workspace.
- `ObservationTargetMissing` is the typed "window does not exist
  / cannot observe" reply — it's a domain failure, not a generic
  unimplemented, so it stays as its own variant rather than folding
  into `RequestUnimplemented`.
- `RequestUnimplemented` keeps only `reason` (per §1.6).

### 2.5 — Hand-rolled frame codec in the daemon

`persona-system/src/daemon.rs:206-291` defines `SystemFrameCodec`
with its own `read_frame`, `read_request`, `write_reply`, and a
4-byte length-prefix protocol. This is exactly the pre-`signal-frame`
shape that the workspace's `signal-frame` crate replaces.

The hand-rolled codec retires when the daemon migrates onto
`signal-executor` (§2.1). `signal-frame::Frame` carries the same
length-prefix-and-rkyv encoding the hand-roll implements; reusing
it removes ~80 lines of error-prone protocol code.

### 2.6 — Daemon reads PERSONA_SOCKET_MODE environment variable

`persona-system/src/daemon.rs:136-141`:

```text
pub fn from_environment() -> Option<Self> {
    std::env::var("PERSONA_SOCKET_MODE")
        .ok()
        .and_then(|value| u32::from_str_radix(value.as_str(), 8).ok())
        .map(Self::from_octal)
}
```

Used in `from_socket` at line 54 (the non-canonical constructor
that pre-dates `SystemDaemonConfiguration`). Per
`intent/component-shape.nota` 2026-05-20T13:00:00Z, daemons **never**
read environment variables; all daemon configuration is NOTA. The
env-var carve-out is CLI-only (socket-path override for testing).

The fix: retire `SocketMode::from_environment` and `SystemDaemon::from_socket`
entirely; the canonical `from_configuration` path is the only one.
Tests that used the env-var path migrate to constructing a typed
`SystemDaemonConfiguration` and passing it in.

### 2.7 — CLI binary surface

`persona-system/src/command.rs` defines `CommandLine` — needs a read.
Per `intent/component-shape.nota` 2026-05-20T13:00:00Z, the daemon
binary is `persona-system-daemon` (current name matches:
`src/daemon_main.rs`) and the CLI is `system` (binary name = daemon
name minus `-daemon`, persona-prefix dropped).

The CLI must use the generated `signal_cli!` macro
(per `intent/component-shape.nota` 2026-05-20T22:27:40+02:00) to
dispatch between the working and owner sockets. Until
`owner-signal-persona-system` exists, the dispatch table is
single-sided (working only); once §3 lands, the CLI dispatch table
covers both contracts.

### 2.8 — Privileged actions are named in ARCH but unmodeled

`persona-system/ARCHITECTURE.md` lines 79-83 name `ForceFocus` and
`SuppressDrift` as deferred privileged actions, and lines 169-170
state the invariant *"privileged actions are not observations; they
require the persona daemon's system connection class."* Today these
actions have no code, no contract type, no CLI surface. The
authorization boundary is also deferred.

This is precisely the surface an owner signal contract carries. §3
proposes a conservative initial shape that names the privileged
actions as candidates for the owner contract without claiming
implementation intent.

The negative naming `ForceFocus` / `SuppressDrift` — flagged in the
ARCH itself (line 102-106, *"`ForceFocus` is a negative name (states
what the action overrides, not what it is)... the verb is reframed
positively"*) — should be resolved before the verbs land. Held back
for psyche; conservative proposal in §3 uses positive renames as
candidates only.

## 3 · Proposed owner signal: `owner-signal-persona-system`

The persona-system daemon is stateful (focus subscription
registrations, the `FocusTracker` actor's recorded state, planned
backend cursor state for unpause). Per
`intent/component-shape.nota` 2026-05-20T12:11:26Z (every stateful
component has an owner contract because management and configuration
must enter through an owner-only signal surface), the contract is
required.

The proposal is **conservative**: it carries the minimum
authority-surface a triad daemon needs, plus a single named
privileged-domain operation drawn directly from ARCH text. Anything
beyond that is held back for psyche scope.

### 3.1 — Operation root proposal

```text
signal_channel! {
    channel OwnerSystem {
        operation Configure(Configuration),
        operation Inspect(Inspection),
        operation Reload(BootstrapPolicy),
    }
    reply Reply {
        Configured(Configured),
        Inspected(Inspection),
        BootstrapPolicyReloaded(BootstrapPolicyReloaded),
        RequestUnimplemented(RequestUnimplemented),
    }
}
```

The three operations mirror what `owner-signal-persona-mind`
(already migrated per /257) and `owner-signal-persona-spirit`
(per /252) carry as their cognitive-policy core. They are the
minimum for "the owner can change my policy state and read it back."

- **`Configure(Configuration)`** — the owner sets the daemon's
  durable policy state (configuration record's exact shape pending;
  candidate fields below).
- **`Inspect(Inspection)`** — the owner reads policy state for
  audit.
- **`Reload(BootstrapPolicy)`** — the owner re-runs the bootstrap
  step (used for factory reset / rollback to known good policy).
  Mirrors `owner-signal-persona-spirit::Reload(BootstrapPolicy)`.

### 3.2 — Privileged-action operations (CONSERVATIVE; awaits psyche scope)

The ARCH names two privileged actions. Conservative proposal: model
them as operations on the owner contract, with positive renames per
ARCH line 102-106. These are **candidates**; the actual verb set
is held back for psyche scope per the conservative-by-default
principle (`intent/workspace.nota` 2026-05-20T14:40:00Z).

```text
operation FocusTarget(FocusOrder),         // candidate rename of "ForceFocus"
operation HoldFocus(FocusHold),            // candidate rename of "SuppressDrift"
operation ReleaseFocusHold(FocusHoldToken),
```

Payload sketches (positional records; field types use existing
contract types where they fit):

- `FocusOrder { target: NiriWindowId }` — order the system to put
  focus on the target window. Replaces the negative "force" framing
  with "this is what focus should be."
- `FocusHold { target: NiriWindowId }` — order the system to hold
  focus on the target window, suppressing drift. The hold persists
  until `ReleaseFocusHold` arrives. Replaces the negative "suppress"
  framing with the positive "hold."
- `FocusHoldToken` — typed handle minted by the daemon when a hold
  is established; the caller passes it back to release. Same shape
  as `FocusSubscriptionToken` — symmetric with the ordinary
  subscription path.

Replies on the same operations:

```text
FocusTargeted(FocusOrderAccepted),
FocusHeld(FocusHoldAccepted),
FocusHoldReleased(FocusHoldReleased),
```

Each carries the relevant token / target plus any backend-side
acknowledgement detail (e.g. *"backend confirmed the focus order
took effect"* vs *"backend reports the window is gone"* — which
would be a `FocusTargetRejected` reply variant).

**Held back for psyche scope (per the conservative-by-default
principle):**

- Whether the three privileged operations land in the initial owner
  contract or wait for the first real consumer that "concretizes
  the requirement" (per ARCH line 81-83). Designer lean: include
  the three above as the initial owner-domain operations because
  they are already named in ARCH and there are no other plausible
  owner-domain operations for system today. But the lean is held
  back because /150 §6.6 also says "introduce when a second real
  backend appears" — analogous logic could apply here ("introduce
  when a real privileged consumer appears").
- The authorization-class question (which authority can issue these
  versus which can only observe) — ARCH §1.5 names this as deferred.
  The owner contract by definition restricts callers to owner;
  finer-grained classes inside owner are out of scope until the
  router-grant model concretizes.
- Lifecycle verbs (`Start` / `Drain` / `Stop` / `Reload`). Per
  `intent/component-shape.nota` 2026-05-20T13:45:00Z, whether
  lifecycle lives on the owner signal at all is an open question.
  `owner-signal-persona-spirit` carries them; designer lean is to
  follow that template for consistency until psyche settles the
  question workspace-wide. The `Reload(BootstrapPolicy)` shape in
  §3.1 is the lifecycle floor (factory reset).

### 3.3 — Configuration record sketch

```text
pub struct Configuration {
    pub backend: Backend,                  // single backend until §1.8's enum-collapse
    pub focus_hold_default_duration: Option<HoldDurationSeconds>,
    pub focus_drift_tolerance: Option<DriftTolerance>,
}
```

These three field candidates come from the privileged-action surface
in ARCH. They are **candidate shapes**, not psyche-stated. A real
configuration record waits on the first privileged consumer that
exercises the focus-hold/drift surface.

For the conservative initial owner contract (without the privileged
actions), `Configuration` could be empty (`{}`) — just the proof
that the policy surface exists. Empty struct configuration is the
shape used in the spirit owner contract's `Drain {}` and
`BootstrapPolicy {}` records; the precedent works.

### 3.4 — Inspection shape

```text
pub struct Inspection {}                  // empty: returns full Inspection reply

pub struct Inspection {                   // reply payload (same name OK; positional)
    pub configuration: Configuration,
    pub active_focus_holds: Vec<FocusHoldRecord>,    // empty when no holds
    pub active_focus_subscriptions: Vec<FocusSubscriptionRecord>,
}
```

Naming note: the request `Inspection` and the reply `Inspection`
share the name but live at different positions in the contract
(request enum variant vs reply enum variant). Per
`intent/naming.nota` 2026-05-19T21:15:00Z (verb/noun homograph
collisions are not a problem because position disambiguates), this
is fine.

If the privileged actions are held back (§3.2 conservative path),
the `active_focus_holds` field retires from `Inspection`; only
`configuration` and `active_focus_subscriptions` remain.

### 3.5 — Operation root summary table

| Operation | Payload | Purpose | Status |
|---|---|---|---|
| `Configure` | `Configuration` | Owner sets daemon policy state | Initial |
| `Inspect` | `Inspection` (empty) | Owner reads policy state | Initial |
| `Reload` | `BootstrapPolicy` | Re-run bootstrap step | Initial |
| `FocusTarget` | `FocusOrder` | Order focus to a window | Candidate (psyche) |
| `HoldFocus` | `FocusHold` | Establish a focus hold | Candidate (psyche) |
| `ReleaseFocusHold` | `FocusHoldToken` | Release a focus hold | Candidate (psyche) |

The three "Initial" rows are the conservative minimum. The three
"Candidate" rows are designer-derived from ARCH but require psyche
scope confirmation before landing.

## 4 · Recommended next slice

In priority order:

1. **Confirm psyche scope** on the §3 proposal:
   - Should the privileged actions (FocusTarget / HoldFocus /
     ReleaseFocusHold) land in the initial owner contract, or wait
     for a real consumer?
   - Should lifecycle verbs (`Start` / `Drain` / `Stop`) land on
     the owner contract (following spirit's template), or stay
     out-of-band?
   - The positive renames (FocusTarget / HoldFocus) — psyche
     approval requested before the verbs land.

2. **Mechanical workspace pass** (no design call needed):
   - Rename `Supervision*` → `EngineManagement*` in
     `SystemDaemonConfiguration` per /252. Wait until /258's main
     /252 sweep lands and follow its lead so the rename is workspace-
     coherent.
   - `signal_core` → `signal-frame` dependency migration in
     `signal-persona-system/Cargo.toml` and consumers.
   - `Subscribe` / `Retract` / `Match` → contract-local verbs
     (`Watch` / `Unwatch` / `Query`) per §2.4.

3. **Collapse speculative single-variant enums** per /150 §6.6 and
   /257 §1.8:
   - `SystemTarget` → `NiriWindowId` directly (or transparent alias).
   - `SystemBackend` retires.
   - `SubscriptionKind` retires.

4. **Drop ancestry prefixes** per /257 §1.5 (System* → bare).

5. **Drop `Graceful`-style smells**:
   - `FocusSnapshotReply` → `FocusSnapshot` per §2.3.
   - `SystemRequestUnimplemented { operation, reason }` →
     `RequestUnimplemented { reason }` per §1.6.

6. **Migrate persona-system daemon onto `signal-executor`** per
   §2.1. Same template as spirit (/255 / /256) and engine-manager
   (/258 §2.2).

7. **Retire daemon environment-variable reading** per §2.6.

8. **Create `owner-signal-persona-system` repository** populated
   with the §3 proposal (initial three operations only, conservative).

9. **Add the observable block** to `signal-persona-system` per /257
   §1.10 and the 2026-05-21T10:00:00Z "debug the debugger" intent.

10. **Designer follow-up** (not in this report's scope): the
    positive-rename of the privileged actions
    (`ForceFocus`/`SuppressDrift`) once psyche scopes the owner
    contract surface. The candidate names in §3.2 are starting
    points, not psyche-stated.

## 5 · References

### Intent records

- `intent/component-shape.nota` 2026-05-18T22:13:54Z — two authority
  tiers (working + policy, no middle).
- `intent/component-shape.nota` 2026-05-19T19:30 / 19:45 / 20:00 /
  20:30 — contract-local verbs supersede universal Sema-verb shape
  at the contract layer.
- `intent/component-shape.nota` 2026-05-20T02:00:00Z — three-layer
  model affirmation; Tap/Untap mandatory for persona components.
- `intent/component-shape.nota` 2026-05-20T12:11:26Z — every
  stateful component has an owner contract; working/policy
  vocabulary; "signal-type naming is architecture" principle.
- `intent/component-shape.nota` 2026-05-20T13:00:00Z — six CLI-design
  records; daemons never read environment variables.
- `intent/component-shape.nota` 2026-05-20T13:45:00Z — mind/body
  analogy + lifecycle open question.
- `intent/component-shape.nota` 2026-05-20T22:27:40+02:00 — CLI
  uses `signal_cli!` macro for working/owner dispatch.
- `intent/persona.nota` 2026-05-19T15:30:00Z — canonical authority
  chain.
- `intent/persona.nota` 2026-05-20T14:30:00Z + 14:50:00Z —
  engine-manager rename Decision (/252's substrate).
- `intent/persona.nota` 2026-05-21T10:00:00Z — debug the debugger
  (every persona component is observable).
- `intent/naming.nota` 2026-05-19T18:50:00Z — query is its own logic
  plane; tree-shape over flat tables.
- `intent/workspace.nota` 2026-05-20T14:40:00Z — conservative
  by default; understatement over over-extension.

### Reports

- `reports/operator/150-triad-signal-sema-migration-current-state.md`
  §6.6 — *system contract should NOT preserve speculative
  single-variant enums for possible future window-manager backends.*
- `reports/designer/257-signal-contracts-names-and-shape-audit.md` —
  workspace-wide name/shape audit.
- `reports/second-operator-assistant/11-signal-type-naming-and-shape-design-guideline.md`
  — naming/shape principles consolidated.
- `reports/second-designer/129-mind-orchestrate-payload-and-cli-dispatch-option-a-2026-05-20.md`
  — `signal_cli!` macro sketch consumed by the §2.7 CLI dispatch.

### Source code

- `/git/github.com/LiGoldragon/persona-system/ARCHITECTURE.md` —
  paused-state skeleton, deferred privileged actions
  (`ForceFocus`/`SuppressDrift`), invariants.
- `/git/github.com/LiGoldragon/persona-system/src/lib.rs` — module
  layout.
- `/git/github.com/LiGoldragon/persona-system/src/daemon.rs` —
  hand-rolled `SystemFrameCodec`, `SocketMode::from_environment`,
  `SystemRequestHandler::reply_for_request`.
- `/git/github.com/LiGoldragon/signal-persona-system/src/lib.rs` —
  the working contract; channel declaration at lines 303-330.

### Skills

- `skills/component-triad.md` — triad invariants; owner contract is
  part of the triad, ships with the daemon.
- `skills/naming.md` — full English words + no redundant ancestry.
- `skills/reporting.md` — report-as-staging-ground discipline.

This report retires when (a) the owner contract proposal in §3 is
psyche-confirmed and `owner-signal-persona-system` ships with the
initial three operations, AND the workspace mechanical sweep (steps
2-5 of §4) has landed in `signal-persona-system`, OR (b) a successor
audit supersedes it.
