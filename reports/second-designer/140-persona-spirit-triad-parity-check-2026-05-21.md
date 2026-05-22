# 140 — persona-spirit triad parity check vs current substrate

*Audit verifying the persona-spirit triad still matches the latest
signal-frame macro output and the current intended design. Spirit
was the executor pilot and the template per `reports/operator/150`
§5.1; the audit asks whether spirit has drifted while signal-frame
was being improved alongside it.*

## 0 · TL;DR

The persona-spirit triad is **substantially current** and remains a
valid template for migrating other components. Six of eight parity
points are clean (alias-dance retired, ancestry-free runtime modules,
signal-executor in the request path, ToSemaOperation/ToSemaOutcome on
Command/Effect, observable block with OperationReceived/EffectEmitted,
StampedEntry composed rather than duplicated). Two minor drift points:
the owner contract still names its channel `OwnerSpirit` (ancestry
inside the owner-signal-persona-spirit crate); and the daemon module
re-exports the runtime client types as `SignalClient` and
`OwnerSignalClient` inside `daemon.rs` (the ancestry-prefixed name
survives at the type-definition site even though `lib.rs` re-routes
them through `ordinary::Client` / `owner::SignalClient` modules).

One open question worth psyche attention: the `EffectEmitted` payload
is `SemaObservation` in spirit, but the
`intent/component-shape.nota` 2026-05-20T15:00:00Z record reads as
"the event carries the typed component effect, not the universal Sema
classification" — which could be interpreted as the payload should be
the typed `Effect`, not `SemaObservation`. This is at most a payload
interpretation question; the variant-name discipline (drop `Sema`
prefix from `EffectEmitted`) is met either way.

## 1 · Parity points

For each item: Current / Drifted / Ahead.

### 1.1 — Alias dance vs clean unprefixed emission (primary-77hh)

**Status: Current.** Both contracts emit unprefixed type names
directly out of `signal_channel!`. No `pub type Frame = SpiritFrame;`
boilerplate exists.

Verified at `signal-persona-spirit/src/lib.rs:419-453` (channel
declaration; no trailing aliases) and
`owner-signal-persona-spirit/src/lib.rs:104-120` (channel
declaration; no trailing aliases). The macro itself
(`signal-frame/macros/src/emit.rs:531-566` for
`emit_frame_aliases`; `parse.rs:37` for the `request_name = Ident::new("Operation", ...)`
default) now emits `Frame`, `FrameBody`, `Operation`, `Reply`,
`Request`, `ReplyEnvelope`, `RequestBuilder`, `OperationKind`,
`ReplyKind`, `EventKind` without any channel-name prefix. The
round-trip test imports the bare names directly
(`signal-persona-spirit/tests/round_trip.rs:6-16`).

Spirit was migrated cleanly when the macro switched.

### 1.2 — SpiritClient/OwnerSpiritClient ancestry vs ordinary::/owner:: modules

**Status: Mostly current; one residue at the definition site.**

The public surface at `persona-spirit/src/lib.rs:23-34` exports
`ordinary::Client`, `ordinary::SignalClient`, `owner::SignalClient`
(via `OwnerSignalClient as SignalClient` re-alias in the `owner`
module), plus the matching `RequestText` / `ReplyText` shapes. This
is the shape /150 §3 names as the target: "runtime crates that expose
ordinary and owner client surfaces use side modules such as
`ordinary::Client`, `ordinary::SignalClient`, and `owner::SignalClient`
rather than crate-local ancestry prefixes such as `SpiritClient` or
`OwnerSpiritClient`."

Daemon test consumers use the right shape:
`persona-spirit/tests/daemon.rs:63-71` types its helpers as
`ordinary::SignalClient` and `owner::SignalClient`.

The residue: at the definition site
(`persona-spirit/src/daemon.rs:74-84`), the structs are still named
`SignalClient` and `OwnerSignalClient`. The `OwnerSignalClient` name
still carries the `Owner` prefix because it is the one disambiguator
the file uses to keep both types distinct in the same module.

This is a definition-site ancestry-prefix residue. The `lib.rs`
module rewiring (`owner::SignalClient = OwnerSignalClient`) hides it
at every call site, so the visible API is clean. But by the strict
"definitions also drop ancestry where possible" reading, the
`OwnerSignalClient` definition itself wants to live inside an
internal `owner` module so the type can be named `SignalClient`
without the owner prefix at the definition site too.

Minor; not load-bearing for the template.

### 1.3 — signal-executor in request path

**Status: Current.** The daemon's request path runs through
`signal-executor::Executor::execute(...)`.

Verified at `persona-spirit/src/actors/dispatch.rs:6-9` (imports
`BatchEffects, BatchPlan, CommandEffect, CommandExecutor, Executor,
Lowering, ObserverChannel, ObserverSet, OperationEffects,
OperationPlan`), `dispatch.rs:123` (`let mut executor = Executor::new(SpiritLowering,
command_executor, observers)`), `dispatch.rs:124` (`executor.execute(request).await`),
`dispatch.rs:166-196` (`impl Lowering for SpiritLowering`),
`dispatch.rs:461-483` (`impl CommandExecutor for SpiritCommandExecutor`),
`dispatch.rs:491-507` (`impl ObserverChannel`),
`Cargo.toml:31` (the `signal-executor` dependency).

This closes /255 Finding 1 — the pilot now actually pilots the
framework.

### 1.4 — ToSemaOperation/ToSemaOutcome on Command/Effect

**Status: Current.**

Verified at `persona-spirit/src/observation.rs:113-126`
(`impl ToSemaOperation for Command` mapping eleven Command variants
to Assert / Match / Subscribe / Retract) and
`observation.rs:128-143` (`impl ToSemaOutcome for Effect` mapping
nine Effect variants to Asserted / Matched / Subscribed / Retracted /
NoChange).

The projection is exercised both in unit tests
(`tests/sema_projection.rs`) and live in the executor's observer
publication path (`dispatch.rs:500-506` calls `effect.sema_observation()`
on each emitted `CommandEffect<Command, Effect>`).

### 1.5 — Observable block with OperationReceived/EffectEmitted

**Status: Current.** The contract declares the canonical block:

```rust
observable {
    filter default;
    operation_event OperationReceived;
    effect_event EffectEmitted;
}
```

at `signal-persona-spirit/src/lib.rs:448-452`. The macro injects
`Tap(ObserverFilter) opens ObserverStream` and
`Untap(ObserverSubscriptionToken)` operations, the
`ObserverSubscriptionOpened` reply variant, the typed
`ObserverFilter`, the `ObserverFilterMatch` trait, and the runtime
publish surface (`signal-frame/macros/src/emit.rs:64-160` for the
augmentation; `:678-...` for the runtime types).

The `OperationReceived` record (`lib.rs:409-412`) carries
`operation: OperationKind`; the `EffectEmitted` record
(`lib.rs:414-417`) carries `observation: SemaObservation`. See §3
below for the payload-interpretation open question.

Live publication is in `persona-spirit/src/actors/dispatch.rs:491-507`
via `SpiritObserverRecorder` implementing `ObserverChannel`.

The daemon's emit path currently traces-only (records via
`SharedTrace`); per `intent/persona.nota` 2026-05-20T20:00:00Z, live
fanout to subscribers is intentionally deferred until
`persona-introspect` lands. The contract surface and observer
plumbing are present; only subscriber wiring is paused. This is the
honest placeholder, not drift.

### 1.6 — Hand-written codec impls vs NotaEnum mixed-variant derives

**Status: Mostly current; two narrow hand-written codecs are
appropriate.**

The contract uses derives throughout for enums and records:

- `NotaEnum` on `Kind`, `Certainty`, `ObservationMode`, `Presence`,
  `UnimplementedReason` (all unit-only) at `lib.rs:197-231,386-392`.
- `NotaEnum` on `Observation` at `lib.rs:350-355` — **mixed-variant
  form**: unit `State`, data-carrying `Records(RecordQuery)`, unit
  `Questions`. This relies on the `nota-codec` mixed-enum support
  that landed per `intent/nota-mixed-enum-support.nota` 2026-05-20.
- `NotaEnum` on `Subscription`, `SubscriptionToken`,
  `SubscriptionSnapshot` at `lib.rs:357-373` (all mixed or
  data-only).
- `NotaRecord` on every record.

The two hand-written codec impls (`Date` at `lib.rs:125-136` and
`Time` at `lib.rs:155-170`) use the NOTA bare date/time literal
shapes via `encoder.write_date(...)` and `decoder.read_date(...)`.
These are correct: `Date` and `Time` are not records, they are
positional bare NOTA literals (e.g. `2026-05-21` and `14:30:00`)
with their own codec entry points. Deriving `NotaRecord` would emit
the wrong shape (parenthesised record form).

No drift here; the hand-written codecs are the right tool for those
two types.

### 1.7 — StampedEntry composition vs duplicated fields

**Status: Current.** At `persona-spirit/src/store.rs:43-48`:

```rust
pub struct StampedEntry {
    entry: Entry,
    date: Date,
    time: Time,
}
```

It composes the submitted `Entry` plus daemon-stamped `Date` /
`Time` rather than duplicating the six Entry fields. /150 §5.1 names
this composed shape as a parity target; spirit meets it.

### 1.8 — Multi-operation batch rejection (per /150 §6 final test list)

**Status: Current.** Two layered rejections are in place:

- multi-operation batch rejection at
  `persona-spirit/src/actors/dispatch.rs:475-478`
  (`if operation_count != 1 { return Err(Error::UnsupportedAtomicBatch
  { operation_count }); }`). Test:
  `tests/daemon.rs:178 persona_spirit_daemon_rejects_multi_operation_batches_before_any_commit`.
- multi-command operation-plan rejection at
  `dispatch.rs:228-235`
  (`single_command_from_operation_plan` rejecting when
  `commands.len() != 1`). Test:
  `dispatch.rs:559 spirit_rejects_multi_command_operation_plan_before_execution`.

These match /150 §6 (`Reject multi-operation batches before commit
until the component has a real transaction boundary; reject
multi-command operation plans before any command runs unless the
component executor has a real transaction boundary`). Spirit's
atomicity is honest degenerate (1 op → 1 command) and the framework
witnesses it.

### 1.9 — Daemon-stamped timestamps (per intent)

**Status: Current.** `ClockPlane` stamps `Date` and `Time` from
`SystemTime::now()` at `persona-spirit/src/actors/clock.rs:48-78`.
Clients submit `Entry` with only six domain fields (topic, kind,
summary, context, certainty, quote) — no date/time/identifier.

ARCH constraints witnessed: `persona-spirit/ARCHITECTURE.md:148-150`
covers "Submitted Entry records carry no client-provided capture
time", "The daemon stamps capture time before storage", and "Spirit
mints RecordIdentifier; agents never submit it" with tests rejecting
the old timestamp-bearing shape.

Aligns with `intent/persona.nota` 2026-05-20 21:53 (`Spirit clients
do not provide capture time`).

## 2 · Drift points worth catching up

Two narrow items, both small.

### 2.1 — Owner contract channel name carries ancestry

`owner-signal-persona-spirit/src/lib.rs:104` reads:

```rust
signal_channel! {
    channel OwnerSpirit {
        operation Start(Start),
        ...
    }
    ...
}
```

The channel name `OwnerSpirit` repeats `Spirit` inside a crate already
named `owner-signal-persona-spirit`. The macro no longer leaks
channel names into emitted types (the emitted `Operation`, `Reply`,
`Frame`, etc. are unprefixed), so this is a cosmetic ancestry leak
at the channel-name declaration only, not a wire-type problem.

Remediation: rename `channel OwnerSpirit { ... }` to `channel Owner
{ ... }` (or `channel Spirit { ... }` mirroring the ordinary contract
— either drops the owner-+spirit redundancy). Pick `channel Owner`
to keep symmetry against the ordinary contract's `channel Spirit`.

### 2.2 — Daemon struct names `SignalClient` / `OwnerSignalClient` at definition site

`persona-spirit/src/daemon.rs:74-84` defines:

```rust
pub struct SignalClient { ... }
pub struct OwnerSignalClient { ... }
```

`lib.rs:23-34` then exposes them through `ordinary::SignalClient`
(unchanged name) and `owner::SignalClient` (`OwnerSignalClient as
SignalClient`). The visible call-site API is module-disambiguated and
clean. But at the definition site the `OwnerSignalClient` name still
prefixes `Owner` to break the in-module name collision.

Remediation: split `daemon.rs` into `daemon/ordinary.rs` and
`daemon/owner.rs` (or push the two client structs into internal
`ordinary`/`owner` modules in `daemon.rs`) so each is just
`SignalClient` inside its module, then re-export via the
`ordinary`/`owner` outer modules. Minor — same outcome as today's
`pub use ... as ...` indirection, but the definition site stops
carrying the ancestry.

Apply 2.1 and 2.2 together; neither needs a psyche call.

## 3 · Items where spirit is AHEAD of other components

Spirit's migrated state contains a few patterns the still-stale
components should adopt.

### 3.1 — `signal_cli!` macro consumption pattern

`persona-spirit/src/runtime.rs:12-17`:

```rust
signal_frame::signal_cli! {
    pub struct CommandLineDispatch {
        working signal_persona_spirit::Operation;
        owner owner_signal_persona_spirit::Operation;
    }
}
```

This is the compile-time working/owner socket dispatch pattern that
`reports/second-designer/129` §"Option A" sketched and
`intent/component-shape.nota` 2026-05-20T22:27:40+02:00 affirmed.
Other components (persona daemon, mind, router, message, etc.) still
need to adopt this rather than hand-rolling CLI routing.

### 3.2 — Modules expose ordinary/owner runtime surfaces

`persona-spirit/src/lib.rs:23-34` shows the public crate surface
using `pub mod ordinary { pub use ... }` and `pub mod owner { pub
use ... }` so the call site reads `ordinary::Client`,
`ordinary::SignalClient`, `owner::SignalClient`, etc. This is the
`intent/component-shape.nota` 2026-05-21T10:30:00Z principle
("modules-not-options for macro disambiguation") applied to the
component runtime layer too. The persona daemon (engine manager)
should adopt this when its multi-channel crate adopts modules for
disambiguation per /258 §2.4.

### 3.3 — `Observation` as a mixed NotaEnum (unit + data variants)

`signal-persona-spirit/src/lib.rs:350-355`:

```rust
pub enum Observation {
    State,
    Records(RecordQuery),
    Questions,
}
```

This is the post-/255 cleanup of the earlier `StateObservation {}` /
`QuestionPending {}` empty-marker structs. Other contracts (e.g.
`signal-persona-terminal`'s `ListSessions {}` per /257 §1.7) still
carry empty markers that the mixed-enum derive can retire.

### 3.4 — `EffectEmitted` carries `SemaObservation` (variant name without Sema prefix)

The variant-name rule from `intent/component-shape.nota`
2026-05-20T15:00:00Z is met cleanly in spirit and is the canonical
shape other persona contracts should adopt when they add their
observable blocks per /257 §1.11. See §4 below for the payload-
interpretation open question.

### 3.5 — Daemon-stamped time + RecordIdentifier ownership

Spirit demonstrates the "daemon stamps, clients submit only domain
content" pattern cleanly. Other components recording time-stamped
events (engine-manager runtime, message router) should follow the
same shape.

## 4 · Open question worth psyche attention

### EffectEmitted payload: SemaObservation vs typed Effect

The spirit contract sets:

```rust
pub struct EffectEmitted {
    pub observation: SemaObservation,
}
```

(`signal-persona-spirit/src/lib.rs:414-417`). `/150` §5.1 documents
this as the template shape ("EffectEmitted carrying SemaObservation").

`reports/second-operator-assistant/11` §8 reads the canonical
2026-05-20T15:00:00Z Decision differently:

> *"the typed event carries the daemon's ComponentEffect, not the
> universal SemaObservation. The Sema prefix would be a misname
> suggesting the event carries Sema classification."*

The Decision verbatim
(`intent/component-shape.nota` 2026-05-20T15:00:00Z):

> *"The standardized observable event-pair generated by signal-
> frame's observable block is OperationReceived / EffectEmitted.
> The Sema prefix is dropped from EffectEmitted because the event
> carries the typed component effect, not the universal Sema
> classification."*

The verbatim can be read two ways:

- (a) the **variant-name** discipline only: drop the `Sema` prefix
  from the variant name; payload is the contract author's choice
  (spirit picked `SemaObservation`). /150 §3 also uses this reading
  ("The emitted event is a component effect projected to
  SemaObservation").
- (b) the **payload-type** discipline: payload must be the typed
  `ComponentEffect`, not `SemaObservation`. This is /11's reading.

Spirit meets (a); does not meet (b). Both readings agree on the
variant name `EffectEmitted` (no `Sema` prefix).

This is a one-line wire-shape question with cross-workspace
implications — every persona contract adds an observable block, so
the payload-type decision propagates. **Worth a psyche
clarification before the engine-manager triad and the persona-mind
contract add their observable blocks.**

Not blocking. Both readings carry the variant-name discipline; the
payload-type interpretation can be settled before the next
component lands its observable block.

## 5 · Recommended next slice

Prioritised parity catch-ups, no beads filed:

1. **Land the EffectEmitted payload clarification** (psyche call;
   §4 above). One line, but cross-workspace.
2. **Rename `channel OwnerSpirit` to `channel Owner`** in
   `owner-signal-persona-spirit/src/lib.rs:105`. Drops ancestry from
   the channel-name declaration. Trivial; doesn't change emitted
   types or wire shape.
3. **Split `persona-spirit/src/daemon.rs` into ordinary/owner
   submodules** so the two client struct definitions are each
   `SignalClient` inside their own scope, eliminating the
   `OwnerSignalClient` ancestry prefix at the definition site.
   Modest; doesn't change the public surface (the
   `ordinary::SignalClient` / `owner::SignalClient` re-exports stay).

Items 2 and 3 can land in a single small commit. Item 1 is a psyche
question.

The persona-spirit triad otherwise remains the workspace's most
current template; the engine-manager triad (per /258) and the still-
unmigrated persona components (per /257 §3.4 migration order) should
continue following spirit's shape.

## 6 · References

- `intent/persona.nota` 2026-05-20T15:00:00Z (spirit replaces
  intent-log substrate); 2026-05-20T20:00:00Z (Tap/Untap fanout
  deferred until introspect); 2026-05-20 21:53 (daemon stamps time);
  2026-05-21T10:00:00Z (debug the debugger — every persona component
  observable).
- `intent/signal.nota` 2026-05-20T17:10:00Z (persona-spirit pilot
  complete).
- `intent/component-shape.nota` 2026-05-20T15:00:00Z (canonical
  OperationReceived / EffectEmitted naming); 2026-05-20T22:27:40+02:00
  (`signal_cli!` macro); 2026-05-21T10:30:00Z (modules-not-options).
- `intent/nota-mixed-enum-support.nota` (mixed-enum NotaEnum
  support).
- `reports/operator/150` §5.1 — names spirit as the current
  template; flags drift possibility.
- `reports/designer/255-signal-spirit-pilot-audit-2026-05-20.md` —
  prior spirit audit (executor migration was the missing piece).
- `reports/designer/257-signal-contracts-names-and-shape-audit.md`
  — workspace-wide contract audit (spirit done; other components
  stale).
- `reports/designer/258-persona-signal-triad-audit-2026-05-21.md`
  — engine-manager triad audit using spirit as the template.
- `reports/second-designer/129-mind-orchestrate-payload-and-cli-dispatch-option-a-2026-05-20.md`
  — `signal_cli!` macro Option A sketch.
- `reports/second-operator-assistant/11-signal-type-naming-and-shape-design-guideline.md`
  — eight-principle guideline (Principle 8 reads EffectEmitted
  payload as typed `ComponentEffect`).
- Macro reference:
  `/git/github.com/LiGoldragon/signal-frame/macros/src/emit.rs:64-160`
  (observable augmentation); `:531-566` (`emit_frame_aliases`
  emitting clean unprefixed names); `:678-...` (observer runtime
  types).
- Code under audit:
  `/git/github.com/LiGoldragon/persona-spirit/src/{lib.rs, daemon.rs, runtime.rs, observation.rs, store.rs, actors/dispatch.rs, actors/clock.rs}`;
  `/git/github.com/LiGoldragon/persona-spirit/ARCHITECTURE.md`;
  `/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs`;
  `/git/github.com/LiGoldragon/owner-signal-persona-spirit/src/lib.rs`.

This report retires when (a) §4's psyche clarification lands AND
§2.1 / §2.2 cleanups land, OR (b) a successor parity check
supersedes.
