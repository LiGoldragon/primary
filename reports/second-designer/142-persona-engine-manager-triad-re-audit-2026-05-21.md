# 142 — persona engine-manager triad re-audit (companion to /258)

*Independent re-audit of the persona engine-manager triad, written
the same day as designer/258. Confirms /258's twelve findings,
surfaces five gaps /258 missed, and updates one of /258's claims that
silently became stale during today's signal-frame work.*

## 0 · TL;DR

/258 is substantively correct on the contract surface. It is **not
complete** on the daemon side or on cross-repository pin alignment —
both gaps are larger than /258's framing suggests, and one of /258's
"still pending" items already landed today.

Three things to know that /258 doesn't carry:

1. **persona daemon is pinned to a pre-migration signal-persona** —
   `Cargo.lock` pins `signal-persona @ cd57f48` (2026-05-19T17:22),
   which is *before* `0b8adc2` (2026-05-19T21:25) where signal-persona
   migrated to signal-frame + contract-local verbs. The /258 audit
   reads the live `main` of signal-persona and concludes the contract
   is "partially migrated"; the daemon hasn't even started consuming
   the migration. Half of /258's daemon findings are vacuous until the
   pin bumps, because the daemon currently compiles against types
   (`EngineRequest`, `EngineStatusQuery`, `EngineLaunchRejection`,
   `EngineRetirementRejectionReason`, …) that no longer exist on the
   current contract.

2. **persona daemon doesn't use signal-frame at all** — it still
   depends on `signal-core` (the retired crate, replaced by
   signal-frame on 2026-05-19T20:23) for every transport-level type
   (`ExchangeIdentifier`, `Reply`, `SignalVerb`, `SubReply`, `Request`,
   `NonEmpty`). /258 §2.2 frames the daemon gap as "doesn't use
   signal-executor"; the real gap is one layer deeper — it doesn't
   use signal-frame either. Migrating onto signal-executor implies
   migrating onto signal-frame first.

3. **/258's "bead `primary-77hh` not fixed" claim is now stale** — the
   signal-frame macro clean-output landing commit (`653773b`, "emit
   clean channel macro boilerplate") landed 2026-05-21T01:11, about
   nine hours before /258 was written. The macro now emits `Frame`,
   `FrameBody`, `Operation`, `ReplyEnvelope`, `RequestBuilder`
   unprefixed. signal-persona is pinned to a signal-frame revision
   from 2026-05-19T21:00 that predates the fix, so signal-persona
   *behaviour* still matches /258's description — but the macro work
   /258 says is pending has been done.

Beyond these three, /258 misses or under-covers: the wire_* test
binaries are deeper-stale than /258 says (they still emit through
`signal-core` types, not just hand-rolled codecs — see §2.1); cross-
contract SpawnEnvelope migration is a wider blast radius than /258
quantifies (every consumer's daemon, every Nix derivation, every
prototype topology — see §2.2); and the Engine-vs-EngineManagement
crate-split question /258 raises but doesn't take a position on has
a stronger answer than /258 leans toward (§2.4).

## 1 · /258 coverage check

/258's findings, restated by section, with confirm / refute /
updated-status notes.

### /258 §1 (/257 findings restatement)

- **§1.13 `supervision::` namespace stale** — Confirmed. 47
  `supervision`/`Supervision*` references in `signal-persona/ARCH`
  and 7 in signal-persona/src/lib.rs (24 was the source-only count;
  ARCH triples it). /252 unexecuted in both source and ARCH.
- **§1.6 `*RequestUnimplemented.operation` redundancy** — Confirmed
  already clean.
- **§1.7 empty marker records** — Confirmed not present.
- **§1.10 frame alias dance** — **Update: macro fix has landed.**
  /258 reports this as "NOT FIXED (cross-workspace bead
  `primary-77hh`)". Verified: signal-frame `main` HEAD is `653773b`
  ("signal-frame: emit clean channel macro boilerplate", 2026-05-21
  T01:11). The emitted aliases in
  `signal-frame/macros/src/emit.rs:531-566` are now `Frame`,
  `FrameBody`, `Request`, `ReplyEnvelope`, `RequestBuilder` —
  unprefixed. signal-persona's pinned signal-frame commit (`4bdf1e1`,
  2026-05-19T21:00) is still pre-fix, so the contract is unaffected
  *yet*. Bumping the pin will break the `pub use supervision::{
  SupervisionFrame, SupervisionFrameBody, SupervisionOperation, …}`
  re-export at `signal-persona/src/lib.rs:631-634` because those
  names no longer exist. The fix and the pin-bump together close
  this gap.
- **§1.11 no observable block** — Confirmed.
- **§1.12 single-field timestamps** — Confirmed; psyche call still
  open per /150 §8.
- **§1.5 ancestry prefixes** — Confirmed mixed; /258's specific call
  on `GracefulStopAcknowledgement` stands (see also §2 below).
- **§1 bead coverage** — Confirmed all three beads (`primary-77hh`,
  `primary-k3bu`, `primary-u0lh`) still open per `bd list`. The
  77hh *implementation* has landed; the bead hasn't been closed.

### /258 §2 (new findings specific to this triad)

- **§2.1 `GracefulStopAcknowledgement` ancestry word** — Confirmed
  at `signal-persona/src/lib.rs:454-457`. /258's argument holds: the
  Supervision channel has exactly one Stop verb; "Graceful" carries
  no disambiguation work. Rename to `StopAcknowledgement`.
- **§2.2 daemon doesn't use signal-executor** — Confirmed AND
  understated. See §2.3 of this report.
- **§2.3 no observable block** — Confirmed.
- **§2.4 Engine vs Supervision module asymmetry** — Confirmed.
  Verified at `signal-persona/src/lib.rs:301-321` (Engine, top
  level) vs `:555-628` (Supervision, in `pub mod supervision`).
  /258's proposed shape (`pub mod engine` + `pub mod
  engine_management`) is correct; see §2.5 of this report for an
  expansion on the open architectural question /258 raised but
  didn't answer.
- **§2.5 `EngineOperationKind` hand-maintained re-export** — Confirmed
  at `persona/src/engine_event.rs:2-9`. /258's framing as a
  drift-risk is right; the macro auto-emission (per
  `intent/component-shape.nota` 2026-05-21T01:15:44+02:00, the
  OperationKind constraint) closes it.
- **§2.6 SpawnEnvelope carries supervision fields** — Confirmed
  at `signal-persona/src/lib.rs:540-553`. /258 lists three stale
  fields; verified. /258's call on retiring the local `ComponentName`
  in favour of `signal_persona_auth::ComponentName` is correct —
  the auth crate already owns the canonical identity type.
- **§2.7 wire_* test binaries hand-roll wire decoding** — Confirmed
  but undersold. See §2.1 of this report.

### /258 §3 (recommended next slice) and §4 (cross-cutting note)

The seven-step ordering is sound and stands. /258 §4's "structurally
identical to spirit's migration" framing is correct but
underestimates effort: spirit's daemon was smaller (one channel, no
child-component lifecycle); the engine-manager has cross-component
state (catalog, readiness, supervision_readiness, manager_store) and
spawns subprocesses. The migration template applies; the surface
area is roughly 3-4× spirit's by line count.

## 2 · Gaps /258 may have missed

### 2.1 — wire_* binaries depend on signal-core, not signal-frame

/258 §2.7 mentions the six `wire_*` binaries as "hand-emit / hand-
decode signal frames for testing" and flags them as "low priority."
This understates the problem.

Verified at `persona/src/bin/`:

```text
wire_decode_message.rs        signal_core::RequestPayload
wire_decode_message_reply.rs  signal_core::{Reply, SubReply}
wire_emit_message.rs          signal_core::{ExchangeIdentifier,
                              ExchangeLane, LaneSequence, Request,
                              SessionEpoch}
wire_emit_message_reply.rs    signal_core::{...}
wire_tap_router.rs            signal_core::{ExchangeIdentifier,
                              NonEmpty, Reply, SignalVerb, SubReply}
wire_router_client.rs         (uses byte-level only, no signal-* dep)
persona_component_fixture.rs  signal_core::{ExchangeIdentifier,
                              NonEmpty, Reply, SignalVerb, SubReply}
```

These binaries don't just hand-roll codecs (the bead `primary-u0lh`
framing /258 used) — they depend on the *retired transport crate*
`signal-core`, including `SignalVerb`, the universal-verb enum that
intent/component-shape.nota 2026-05-19T19:45 deleted from the
public-contract layer. The whole "Assert/Match/Subscribe/Retract/
Mutate" universal-verb era is still alive in the persona daemon
through these binaries and through `transport.rs` /
`supervision_readiness.rs`.

This is structural, not a hand-rolling smell. Replacing hand-rolled
codecs with derives doesn't fix it — the framing crate itself is
wrong. Migration sequence:

1. Bump `persona`'s `signal-persona` dependency to current main
   (post-`0b8adc2`).
2. Add `signal-frame` as a direct dep; remove `signal-core`.
3. Replace every `signal_core::*` import with the corresponding
   `signal_frame::*` (or `signal_persona::Frame`,
   `signal_persona::FrameBody`, etc. once /77hh-fix bumps land).
4. Replace `SignalVerb`-tagged request construction with the
   contract-local-verb shape.
5. Replace consumer-visible types that no longer exist
   (`EngineRequest`, `EngineStatusQuery`, `EngineLaunchRejection`,
   `EngineRetirementRejection*`, …) with the current names from
   signal-persona.

Steps 1-5 are *prerequisite* to /258's §2.2 signal-executor
migration. The signal-executor work cannot land on top of a
signal-core daemon.

### 2.2 — SpawnEnvelope blast radius

/258 §2.6 enumerates the three stale fields on `SpawnEnvelope` and
calls out that "every supervised daemon's startup code that reads
these fields needs the same rename." That's right but doesn't sum
the cost.

`SpawnEnvelope` is the Nix-passed handshake between persona-daemon
(producer) and every supervised child component (consumer). The
fields cross three boundaries:

1. **Rust source** in each child component that reads the envelope
   (8 component repos per /252 §1.4).
2. **Daemon configuration** types (`DaemonConfiguration` per /252
   §1.4) with fields `supervision_socket_path` /
   `supervision_socket_mode`.
3. **Nix env vars** (`*_SUPERVISION_SOCKET` per /252 §1.4) — an
   ABI break for prototype topologies; the rename has to land
   atomically across Rust code + Nix derivation + manifest.

/258 doesn't reference the Nix-env-var blast or the per-component
DaemonConfiguration field rename; both are in /252 but /258 treats
the SpawnEnvelope rename as confined to the contract crate. The
real surface is wider, and *every supervised component bumps in
lockstep with persona-daemon*. This argues for a single coordinated
work-claim against `persona` + all 8 supervised consumers, not
serially.

The cross-cutting concern /258 doesn't surface: SpawnEnvelope
currently encodes the wire shape clients expect. **What's the
projection from current wire shape to the new (post-77hh) macro
output?** The current contract emits Frame/Body using
channel-prefixed names; once signal-persona bumps signal-frame to
post-`653773b`, every type alias in /258 §1.10 changes shape
without changing on-wire bytes (the rkyv encoding is the same;
it's the Rust type names that change). Consumers that import
`SupervisionFrame` directly today need to import `Frame` (or
`engine_management::Frame`) after the bump. This is a Rust-source-
visible churn point, not a wire churn.

### 2.3 — persona daemon's actor mesh shape vs the target

/258 §2.2 sketches the target ("`Lowering for EngineLowering` +
`CommandExecutor for EngineCommandExecutor` wrapping the Kameo
mesh"). I'll add a shape note /258 doesn't carry.

Current persona daemon actor topology (verified by reading
`persona/src/{manager,supervisor,manager_store,readiness,
supervision_readiness,direct_process,engine}.rs`):

```text
EngineManager (root request handler, manager.rs)
  └── ManagerStore (redb persistence, manager_store.rs)
EngineSupervisor (process supervisor, supervisor.rs)
  ├── ComponentCommandResolver (command catalog, launch/...)
  ├── DirectProcessLauncher (process spawn, direct_process.rs)
  ├── ComponentSocketReadiness (readiness.rs)
  └── ComponentSupervisionReadiness (supervision_readiness.rs)
```

`EngineManager` (the actor) handles `HandleEngineRequest`;
`EngineSupervisor` handles `StartPrototypeSupervision`. Both are
top-level actor refs the daemon holds. The relationship in /258
§2.2 maps `EngineSupervisor` to "the closest thing to a
CommandExecutor"; that's right, but **`EngineManager` is the actor
that should host the `Lowering` impl**, because it's the one with
direct request access. The `Executor::execute(request)` call lives
in the daemon-socket-actor layer (which is currently in
`transport.rs`, not in either actor). The split:

- `signal_executor::Executor::execute` orchestrates the
  request-decode → lowering → batch execution → reply correlation.
- `Lowering` (on persona's side) maps `EngineOperation` →
  `EngineCommand`.
- `CommandExecutor` (on persona's side) calls into
  `EngineManager.ask(...)` and `EngineSupervisor.ask(...)` for the
  state mutations and process actions respectively. The atomic-
  batch boundary is the request-scoped sequence of actor messages.

This is different from spirit's shape (spirit's CommandExecutor
calls directly into the sema-engine store). Persona's
CommandExecutor needs to fan out across two actor subsystems. The
fan-out happens *inside* the CommandExecutor impl; the executor
framework still sees one atomic boundary. Whether the actor-mesh
calls are *truly atomic* (against catalog mutations vs subprocess
launches) is the open architectural question: subprocess spawn
cannot rollback. The honest shape is that `Engine` operations have
two phases — the catalog mutation is atomic; the subprocess action
is best-effort *after* the catalog commits. This is closer to how
real OS supervisors work (systemd commits the unit-file change,
then asks the unit to do something), but it does mean
`BatchPlan<EngineCommand>` is structurally weaker than spirit's.

### 2.4 — Engine vs EngineManagement: one crate or two?

/258 §2.4 raises the question and leans toward `pub mod engine` +
`pub mod engine_management` modules within one crate. The reasoning
is correct given today's psyche intent (component-shape.nota
2026-05-21T10:30:00Z, "macros emit clean names; modules for
disambiguation"). But /258 doesn't take the broader question:
**should these channels be in the same crate at all?**

Arguments for keeping them together (current):

- They both serve `persona-daemon`. One contract crate per daemon
  is the natural unit.
- The intent record above explicitly authorises modules for
  multi-channel-per-crate; this is its motivating case.
- Splitting now means two more contract repos in the dependency
  graph.

Arguments for splitting:

- They have **different consumers**. The Engine channel is consumed
  by anything that wants to launch / catalog / start / stop engines
  — the CLI, external orchestration tooling, the future
  persona-introspect. The EngineManagement channel is consumed by
  the supervised child daemons only — internal infrastructure
  traffic.
- They have **different authority**. The Engine channel is the
  daemon's working surface; the EngineManagement channel is more
  like a peer-to-peer infrastructure stream between the manager
  and each supervised child.
- The triad framing per `skills/component-triad.md` says
  `<component>` daemon plus `signal-<component>` (ordinary) plus
  `owner-signal-<component>` (policy). EngineManagement isn't
  ordinary working traffic; it's not policy either; it's a third
  thing. By the workspace's vocabulary, it doesn't quite fit
  either slot.

The psyche framing per the prompt I was given:

> The engine-management channel inside signal-persona is the
> "owner-like" surface but at the wire level it's a second channel
> in the same contract crate.

The "owner-like" framing is interesting. The supervisor (systemd)
sits outside the persona system; the EngineManagement channel is
how the daemon expresses authority over its supervised children.
It's *the channel through which engine-manager exercises owner
authority over component lifecycle*. That's structurally similar
to what `owner-signal-<component>` does for sibling persona
components (mind → orchestrate, orchestrate → router, etc.) — it's
the authority surface, just with the OS as the actor instead of a
sibling daemon.

If that framing is right, the natural shape is **a third repo**:
not `signal-persona` + `owner-signal-persona`, but `signal-persona`
+ `signal-engine-management` (or kept as a module of the same
crate, but conceptually separate). The owner role differs (OS
supervisor vs sibling persona component) but the authority shape
is the same.

I'm not recommending the split — the psyche has stated
multi-channel-in-one-crate-with-modules is allowed, and the cost
of splitting now is real. I'm flagging that the conceptual fit
between EngineManagement and the workspace's "owner signal"
discipline is closer than /258 acknowledges, and worth a psyche
clarification before fully committing to the module-not-crate
shape. /258 takes a position; this is a question that deserves
asking. Concrete psyche question is in this report's chat reply.

### 2.5 — Persona's Cargo.lock is the silent blocker

This is the most load-bearing thing /258 misses. All of /258's
findings about the contract are correct, but the daemon's lockfile
points at signal-persona @ `cd57f48` which is from before any of
the contract-local-verb migration. The migration sequence:

| Date | Commit | Crate | Change |
|---|---|---|---|
| 2026-05-19T17:22 | `cd57f48` | signal-persona | (persona pin) — pre-migration |
| 2026-05-19T20:23 | `be04729` | signal-frame | initial signal-core fork |
| 2026-05-19T20:25 | `2426b94` | signal-persona | MUST IMPLEMENT note |
| 2026-05-19T20:41 | `3526c10` | signal-frame | macro contract-local operations |
| 2026-05-19T20:46 | `94fa087` | signal-persona | settle supervision verbs |
| 2026-05-19T21:00 | `4bdf1e1` | signal-frame | collapse Operation wrapper |
| 2026-05-19T21:25 | `0b8adc2` | signal-persona | migrate to signal-frame + contract-local verbs |
| 2026-05-20T12:53 | `8e43593` | signal-persona | align ARCH + skills (latest) |
| 2026-05-21T01:11 | `653773b` | signal-frame | emit clean macro boilerplate |

persona @ HEAD pins signal-persona @ `cd57f48`. Everything from
`0b8adc2` forward (contract-local verbs, supervision channel
re-shape, GracefulStopAcknowledgement, current Engine channel
verbs, current SpawnEnvelope fields) is not yet visible to the
daemon. **The daemon doesn't compile against current signal-persona
today**. /258's framing implicitly assumes the daemon and contract
are in sync; they're not.

This makes the migration ordering different from /258 §3:

1. Bump persona's `signal-persona` pin to current main. This will
   surface a wave of compile errors against renamed/dropped types.
2. Resolve those errors by following the type renames (matches /258
   §3.2 / /252 mechanical pass).
3. THEN bump signal-frame to post-`653773b` to pick up clean macro
   output.
4. THEN do signal-executor migration (/258 §3.6 / §2.2).
5. THEN /252 engine-management rename (since the daemon is using
   current names from step 2; the rename happens with the daemon
   on stable footing).

The point is steps 1-2 are *not optional* — the daemon is currently
broken against current main; it just doesn't know because nobody's
bumped its pin. Whoever picks up the persona-onto-signal-executor
work has to deal with the pin bump first.

## 3 · New findings

### 3.1 — `daemon/` referenced in the prompt doesn't exist

The pre-assignment in the psyche prompt names the daemon as
`/git/github.com/LiGoldragon/persona/daemon/`. The actual layout is
`/git/github.com/LiGoldragon/persona/src/` with the daemon binary
at `src/bin/persona_daemon.rs` (22 lines, just the entry point;
the actor mesh is in `src/{manager,supervisor,…}.rs`). Workspace-
prose convention varies — some repos do use a `daemon/` subdir.
Not a defect, just a navigation note for future agents.

### 3.2 — `EngineId::new("default")` magic string

`persona/src/manager.rs:38`: `engine: EngineId::new("default")`.
The default-catalog `EngineManager::start()` mints an EngineId from
the literal string `"default"`. This is the only "default engine"
in the codebase; it predates the multi-engine catalog work
(`EngineCatalog`, `EngineCatalogEntry` in the contract).

If the engine-manager is genuinely multi-engine per the catalog
shape, the "default" magic should be replaced with either (a) an
explicit "Default" engine variant on `EngineId` (typed, not
stringy), or (b) the manager declining to default-mint and instead
requiring the catalog to be loaded from store. The current shape
works for prototype-single-engine but reads like a workaround.

Outside the audit scope but worth flagging.

### 3.3 — Two declarations of `ComponentStatusQuery` (one in contract, one in daemon)

`persona/src/request.rs:23-26` defines a daemon-local
`ComponentStatusQuery` struct identical to `signal_persona::
ComponentStatusQuery` (which actually no longer exists on current
main — it's `ComponentStatusQuery` on the daemon side, the contract
now uses `Query::ComponentStatus(ComponentName)`). The daemon
defining its own version of each NOTA-Record shape suggests the
boundary between contract types and daemon types is mushy. The
target shape (per /150 §3 and /258 §2.2) is:

- Contract types (`signal_persona::*`) cross the wire.
- Daemon types (`persona::*Command`, `persona::*Effect`) are
  internal.
- The Lowering trait converts between them.

Currently persona defines its own `EngineStatusQuery`,
`ComponentStatusQuery`, `ComponentStartup`, `ComponentShutdown` —
all duplicate the contract names. This collapses to one set per
type once Lowering is in place, but it's a non-trivial cleanup
that /258 §2.2 doesn't enumerate.

## 4 · Recommended next slice

/258 §3's seven-step ordering stands. I'd insert two prerequisite
steps and modify one:

**Step 0 (prerequisite):** Bump `persona`'s Cargo.lock pin on
`signal-persona` to current main (`8e43593` or later). Resolve
compile errors by mapping deprecated type names to current ones.
Also replace `signal-core` with `signal-frame` in
`persona/Cargo.toml` and update transport.rs, supervision_
readiness.rs, persona_component_fixture.rs, and the wire_*
binaries.

**Step 0.5 (also prerequisite):** Bump signal-persona's signal-frame
pin from `4bdf1e1` to post-`653773b`. This makes the macro emit
clean unprefixed names. Drop the `pub use supervision::{
SupervisionFrame, SupervisionFrameBody, …}` re-export
(signal-persona/src/lib.rs:631-634). Consumers using
`SupervisionFrame` directly now have to write
`supervision::Frame` (or `engine_management::Frame` post-/252).

**Step 1** (modified from /258 §3.1): `primary-k3bu` rename now also
covers the wire_* binaries' inherited `UnknownKindForVerb` references
that come through signal-core. After step 0.5, signal-frame ships
the current `UnknownVariantForRecord` error; this becomes a straight
import-name rename.

**Steps 2-7**: as /258 §3.

**Open psyche question** (carry through to confirmation before
beginning the work): the Engine-vs-EngineManagement crate split per
§2.4 above. Designer-assistant lean (this report): keep one crate
with two modules, since psyche has already authorised that shape
(intent/component-shape.nota 2026-05-21T10:30:00Z). But the
"owner-like authority" framing the psyche themselves used (per the
prompt) suggests this might be a third real surface the workspace
vocabulary doesn't quite name. Worth a psyche clarification before
committing.

## 5 · References

- `/258` — the prior audit; this report adds rather than replaces.
- `/252` — the engine-management rename plan (unexecuted).
- `/255`, `/256` — spirit migration template.
- `/257` — workspace-wide name/shape audit.
- `/150` — operator lane's consolidated migration handoff.
- `intent/persona.nota` 2026-05-21T10:00:00Z — "debug the debugger".
- `intent/component-shape.nota` 2026-05-21T10:30:00Z — modules-not-options.
- `intent/component-shape.nota` 2026-05-21T01:15:44+02:00 — OperationKind macro auto-emit.
- Code under audit:
  - `/git/github.com/LiGoldragon/signal-persona/src/lib.rs` (634 lines).
  - `/git/github.com/LiGoldragon/persona/Cargo.toml` (pinned signal-core dep).
  - `/git/github.com/LiGoldragon/persona/Cargo.lock` (signal-persona pinned to `cd57f48`).
  - `/git/github.com/LiGoldragon/persona/src/main.rs`, `lib.rs`,
    `manager.rs`, `supervisor.rs`, `transport.rs`, `request.rs`,
    `engine_event.rs`, `supervision_readiness.rs`,
    `bin/wire_*.rs`, `bin/persona_component_fixture.rs`,
    `bin/persona_daemon.rs`.
- `/git/github.com/LiGoldragon/signal-frame/macros/src/emit.rs:531-566`
  — current clean-output alias emission.
- Beads: `primary-77hh` (implementation landed; bead still open),
  `primary-k3bu` (open), `primary-u0lh` (open).

This report retires when the persona daemon successfully builds
against current signal-persona main, OR a later audit supersedes.
