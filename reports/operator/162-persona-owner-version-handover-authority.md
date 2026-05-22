# 162 - Persona owner version-handover authority

## What Landed

This slice completed the owner-authority side of the version-handover stack.

- Created `owner-signal-version-handover` as a pure signal contract crate:
  `ForceFlip`, `Rollback`, `Quarantine`, their replies, typed reasons, and
  standard observable surface.
- Published the repo to
  `github.com:LiGoldragon/owner-signal-version-handover.git`.
- Added the repo to `protocols/active-repositories.md`.
- Wired Persona to consume the owner contract in
  `/git/github.com/LiGoldragon/persona` commit `d89c3ac5`.

Persona now has a `HandleOwnerVersionHandover` manager message. It handles:

- `ForceFlip` by appending an active-version override event and updating the
  active-version snapshot.
- `Rollback` by appending an active-version override event and updating the
  active-version snapshot to the restore version.
- `Quarantine` by appending a durable `VersionQuarantined` event.

Normal handover completion remains distinct: it is still marker-backed and
records a commit sequence from `signal-version-handover::HandoverMarker`.
ForceFlip and Rollback do not fake a commit sequence; their source is recorded
as explicit owner authority.

## Architecture Shape

The active-version state now distinguishes three sources:

```rust
pub enum ActiveVersionChangeSource {
    HandoverMarker { commit_sequence: u64 },
    ForceFlip { reason: ForceReason },
    Rollback { reason: RollbackReason },
}
```

This matters because a protocol-complete handover and an owner override are not
the same fact. A protocol-complete handover proves the target daemon supplied a
marker with a durable commit sequence. A force flip proves only that owner
authority overrode the selector.

Quarantine is not yet reduced into a snapshot table. It is a durable event-log
fact today. That is enough for the current witness; the next policy slice can
decide whether quarantine needs a selector table, an upgrade-deny gate, or both.

## Tests

Ran:

```text
CARGO_BUILD_JOBS=2 cargo test
nix flake check --option max-jobs 0 -L
```

Both passed in `/git/github.com/LiGoldragon/persona`.

New Persona tests prove:

- owner `ForceFlip` updates the active selector without commit-sequence fraud;
- owner `Rollback` updates the active selector to the restore version;
- owner `Quarantine` records a typed `VersionQuarantined` event.

The `owner-signal-version-handover` repo also passes:

```text
CARGO_BUILD_JOBS=2 cargo test
nix flake check --option max-jobs 0 -L
```

## Beads

- Closed `primary-7kge` — owner contract exists and is consumed by downstream
  Persona tests.
- Updated `primary-a5hu` — Persona epic now records commit `d89c3ac5`.
- Updated `primary-wvdl` — Track A now has owner authority consumption; next
  gap is real socket I/O.

## Remaining Work

The upgrade stack is still not deployment-ready. The next high-signal Persona
work is the socket driver:

1. Persona must connect to component private upgrade sockets and exchange real
   `signal-version-handover` frames.
2. Persona must drive `AskHandoverMarker`, `ReadyToHandover`, and
   `HandoverCompleted` against real daemons rather than only manager messages.
3. Spirit v0.1.0 still needs a protocol-aware maintenance build, or we need to
   intentionally accept that the first production cutover uses a different
   staged path.
4. Quarantine currently records an event but does not gate future upgrade
   attempts. That policy gate should land before owner authority is exposed to
   a real operator-facing socket.

